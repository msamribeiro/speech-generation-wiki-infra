#!/usr/bin/env python3
"""
citation_index.py — Build out-of-corpus citation index from parsed papers.

Scans all raw/parsed/{id}/references.json files, counts how many corpus papers
cite each out-of-corpus reference, deduplicates by arXiv ID > DOI > normalized
title, and flags entries that match corpus speech-synthesis keywords.

Deduplication runs in two passes:
  1. At collection time: canonical key (arxiv: > doi: > title: > raw:) prevents
     most duplicates when the same reference carries an arXiv ID in every sighting.
  2. Post-hoc merge: after collection, entries sharing the same normalized title
     are collapsed into the most canonical key, merging cited_by sets. This catches
     the common case where one corpus paper cites a reference with an arXiv ID and
     another cites the same reference without one.

After merging, a fuzzy candidate pass (token Jaccard >= 0.85) surfaces pairs that
may be the same paper but couldn't be merged deterministically. These are written
to the merge_candidates field for human review.

Output: raw/citation_index.json

Usage:
    python scripts/discover/citation_index.py
    python scripts/discover/citation_index.py --min-citations 3
    python scripts/discover/citation_index.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from lib.keyword_filter import load_keyword_filter, passes_filter  # noqa: E402

RAW_PARSED              = ROOT / "raw" / "parsed"
CITATION_INDEX          = ROOT / "raw" / "citation_index.json"
MERGE_OVERRIDES         = ROOT / "raw" / "citation_merge_overrides.json"
PIPELINE_LOG            = ROOT / "raw" / "pipeline_log.md"

DEFAULT_MIN_CITATIONS = 1


# ---------------------------------------------------------------------------
# Normalization and title helpers
# ---------------------------------------------------------------------------

def _normalize(text: str) -> str:
    """Lowercase, alphanumeric-only — used as dedup key component."""
    return re.sub(r"[^a-z0-9]", "", text.lower())


def _extract_title_from_raw(raw: str) -> str | None:
    """
    Try to extract a paper title from a raw bibliography string.

    Handles two common citation styles:
    - IEEE/Interspeech: authors, 'Title in single quotes,' venue, year
    - Typographic quotes: 'Title'
    """
    for pattern in [
        r"‘(.+?)’",   # typographic single quotes
        r"'(.+?)'",              # straight single quotes
        r'"(.+?)"',              # double quotes
    ]:
        m = re.search(pattern, raw)
        if m:
            candidate = m.group(1).strip().rstrip(".,;:")
            if len(candidate) > 10:
                return candidate
    return None


def _best_title(ref: dict) -> str | None:
    return ref.get("title") or _extract_title_from_raw(ref.get("raw") or "")


def _canonical_key(ref: dict) -> str:
    """Stable dedup key: arXiv ID > DOI > normalized title > normalized raw prefix."""
    if ref.get("arxiv_id"):
        return f"arxiv:{ref['arxiv_id']}"
    if ref.get("doi"):
        return f"doi:{ref['doi']}"
    title = _best_title(ref)
    if title:
        norm = _normalize(title)
        if norm:
            return f"title:{norm[:120]}"
    raw = ref.get("raw") or ""
    return f"raw:{_normalize(raw[:100])}"


# ---------------------------------------------------------------------------
# Post-hoc merge (deterministic)
# ---------------------------------------------------------------------------

def _key_rank(key: str) -> int:
    """Lower rank = more canonical. arxiv: > doi: > title: > raw:"""
    if key.startswith("arxiv:"): return 0
    if key.startswith("doi:"):   return 1
    if key.startswith("title:"): return 2
    return 3


def _post_hoc_merge(entries: dict[str, dict]) -> tuple[dict[str, dict], int]:
    """
    Merge entries that share an identical normalized title.

    Canonical priority: arxiv: > doi: > title: > raw:
    The canonical entry absorbs cited_by from all others. If the canonical entry
    gains an arxiv_id via merge, it is re-keyed to arxiv:{id}.

    Returns (merged_dict, number_of_groups_collapsed).
    """
    norm_to_keys: dict[str, list[str]] = defaultdict(list)
    for key, entry in entries.items():
        title = entry.get("title")
        if title:
            nt = _normalize(title)[:120]
            if nt:
                norm_to_keys[nt].append(key)

    to_delete: set[str] = set()
    merge_count = 0

    for nt, keys in norm_to_keys.items():
        if len(keys) < 2:
            continue
        merge_count += 1

        keys_sorted = sorted(keys, key=_key_rank)
        canonical_key = keys_sorted[0]
        canonical = entries[canonical_key]

        all_cited_by = set(canonical["cited_by"])
        for other_key in keys_sorted[1:]:
            other = entries[other_key]
            all_cited_by.update(other["cited_by"])
            if not canonical.get("arxiv_id") and other.get("arxiv_id"):
                canonical["arxiv_id"] = other["arxiv_id"]
            if not canonical.get("doi") and other.get("doi"):
                canonical["doi"] = other["doi"]
            if not canonical.get("year") and other.get("year"):
                canonical["year"] = other["year"]
            to_delete.add(other_key)

        canonical["cited_by"] = sorted(all_cited_by)
        canonical["citation_count"] = len(all_cited_by)

        # Re-key if canonical now has an arxiv_id but was stored under title: or doi:
        if canonical.get("arxiv_id") and not canonical_key.startswith("arxiv:"):
            new_key = f"arxiv:{canonical['arxiv_id']}"
            if new_key not in entries:
                canonical["key"] = new_key
                entries[new_key] = canonical
                to_delete.add(canonical_key)

    for k in to_delete:
        entries.pop(k, None)

    return entries, merge_count


# ---------------------------------------------------------------------------
# Manual merge overrides
# ---------------------------------------------------------------------------

def _apply_overrides(
    entries: dict[str, dict],
    overrides_path: Path,
    kf: object,
) -> tuple[dict[str, dict], int]:
    """
    Apply manual merge overrides from raw/citation_merge_overrides.json.

    Each group specifies a canonical_key and a list of merge_keys. All
    merge_keys are collapsed into the canonical, with cited_by unioned and
    missing title/doi/arxiv_id fields upgraded. Missing keys are silently
    skipped. Returns (updated_entries, count_of_entries_merged_away).
    """
    if not overrides_path.exists():
        return entries, 0

    overrides = json.loads(overrides_path.read_text())
    merged_away = 0

    for group in overrides.get("groups", []):
        canonical_key = group.get("canonical_key", "")
        if canonical_key not in entries:
            continue
        canonical = entries[canonical_key]

        all_cited_by = set(canonical["cited_by"])
        for other_key in group.get("merge_keys", []):
            if other_key not in entries or other_key == canonical_key:
                continue
            other = entries[other_key]
            all_cited_by.update(other["cited_by"])
            if not canonical.get("arxiv_id") and other.get("arxiv_id"):
                canonical["arxiv_id"] = other["arxiv_id"]
            if not canonical.get("doi") and other.get("doi"):
                canonical["doi"] = other["doi"]
            if not canonical.get("year") and other.get("year"):
                canonical["year"] = other["year"]
            if not canonical.get("title") and other.get("title"):
                canonical["title"] = other["title"]
                canonical["speech_relevant"] = passes_filter(other["title"], "", kf)
            entries.pop(other_key)
            merged_away += 1

        canonical["cited_by"] = sorted(all_cited_by)
        canonical["citation_count"] = len(all_cited_by)

    return entries, merged_away


# ---------------------------------------------------------------------------
# Fuzzy candidate detection (for human review)
# ---------------------------------------------------------------------------

_STOPWORDS = frozenset({
    "a", "an", "the", "and", "or", "for", "with", "via", "from", "using",
    "based", "end", "towards", "toward", "into", "over", "out", "are", "not",
    "its", "our", "new", "of", "in", "on", "to", "at", "by", "as", "is", "it",
    "be", "do", "has", "have", "that", "this", "which", "we", "their", "these",
    "can", "but", "all", "more", "also", "than", "two", "one",
})


def _title_tokens(title: str) -> frozenset[str]:
    words = set(re.findall(r"\b[a-z0-9]{3,}\b", title.lower()))
    return frozenset(words - _STOPWORDS)


def _find_fuzzy_candidates(
    entries: dict[str, dict],
    min_count: int = 5,
    jaccard_threshold: float = 0.85,
    max_candidates: int = 100,
) -> list[dict]:
    """
    Find pairs of titled entries that might be the same paper but weren't merged
    deterministically. Uses token Jaccard similarity.

    Only considers entries with citation_count >= min_count to limit noise.
    Returns up to max_candidates pairs sorted by max citation count descending.
    """
    titled = [
        (key, e, _title_tokens(e["title"]))
        for key, e in entries.items()
        if e.get("title") and e["citation_count"] >= min_count
    ]

    # Inverted index: token -> set of indices into titled[]
    token_to_idx: dict[str, set[int]] = defaultdict(set)
    for i, (key, e, tokens) in enumerate(titled):
        for tok in tokens:
            token_to_idx[tok].add(i)

    candidates: list[dict] = []
    seen_pairs: set[tuple[int, int]] = set()

    for i, (key_a, entry_a, tokens_a) in enumerate(titled):
        if not tokens_a:
            continue
        # Candidate set: entries sharing at least one token
        candidate_idxs: set[int] = set()
        for tok in tokens_a:
            candidate_idxs.update(token_to_idx[tok])
        candidate_idxs.discard(i)

        for j in candidate_idxs:
            if j <= i:
                continue
            pair = (i, j)
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)

            key_b, entry_b, tokens_b = titled[j]
            if not tokens_b:
                continue

            intersection = tokens_a & tokens_b
            union = tokens_a | tokens_b
            jaccard = len(intersection) / len(union)

            if jaccard < jaccard_threshold:
                continue

            # Skip pairs already caught by exact normalization (same norm title)
            nt_a = _normalize(entry_a["title"])[:120]
            nt_b = _normalize(entry_b["title"])[:120]
            if nt_a == nt_b:
                continue

            candidates.append({
                "jaccard": round(jaccard, 3),
                "entries": [
                    {
                        "key": key_a,
                        "title": entry_a["title"],
                        "count": entry_a["citation_count"],
                        "arxiv_id": entry_a.get("arxiv_id"),
                    },
                    {
                        "key": key_b,
                        "title": entry_b["title"],
                        "count": entry_b["citation_count"],
                        "arxiv_id": entry_b.get("arxiv_id"),
                    },
                ],
            })

    candidates.sort(key=lambda x: -max(e["count"] for e in x["entries"]))
    return candidates[:max_candidates]


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

def build_index(min_citations: int) -> dict:
    kf = load_keyword_filter()

    ref_files = sorted(RAW_PARSED.glob("*/references.json"))
    entries: dict[str, dict] = {}
    total_refs = 0

    for ref_file in ref_files:
        paper_id = ref_file.parent.name
        try:
            refs = json.loads(ref_file.read_text())
        except Exception as exc:
            print(f"  Warning: could not read {ref_file}: {exc}")
            continue

        for ref in refs:
            if ref.get("in_corpus"):
                continue
            total_refs += 1
            key = _canonical_key(ref)

            if key not in entries:
                title = _best_title(ref)
                raw = ref.get("raw") or ""
                speech_relevant: bool | None = (
                    passes_filter(title, "", kf) if title is not None else None
                )
                entries[key] = {
                    "key": key,
                    "arxiv_id": ref.get("arxiv_id"),
                    "doi": ref.get("doi"),
                    "title": title,
                    "raw_sample": raw[:200] if raw else None,
                    "year": ref.get("year"),
                    "citation_count": 0,
                    "cited_by": [],
                    "speech_relevant": speech_relevant,
                }

            entry = entries[key]

            if paper_id not in entry["cited_by"]:
                entry["cited_by"].append(paper_id)
                entry["citation_count"] += 1

            # Upgrade missing fields when a later sighting has more data
            if not entry["arxiv_id"] and ref.get("arxiv_id"):
                entry["arxiv_id"] = ref["arxiv_id"]
            if not entry["doi"] and ref.get("doi"):
                entry["doi"] = ref["doi"]
            if entry["title"] is None:
                t = _best_title(ref)
                if t is not None:
                    entry["title"] = t
                    entry["speech_relevant"] = passes_filter(t, "", kf)

    unique_before_merge = len(entries)

    # Post-hoc merge: collapse entries sharing the same normalized title
    entries, merge_groups = _post_hoc_merge(entries)
    merged_away = unique_before_merge - len(entries)

    # Manual overrides: apply user-confirmed merges that normalization can't catch
    entries, override_merged = _apply_overrides(entries, MERGE_OVERRIDES, kf)
    merged_away += override_merged

    # Fuzzy candidate detection: surface remaining near-duplicates for human review
    fuzzy_candidates = _find_fuzzy_candidates(entries)

    filtered = sorted(
        (e for e in entries.values() if e["citation_count"] >= min_citations),
        key=lambda e: (-e["citation_count"], e.get("title") or ""),
    )

    return {
        "generated": date.today().isoformat(),
        "corpus_papers": len(ref_files),
        "total_out_of_corpus_refs": total_refs,
        "unique_out_of_corpus_before_merge": unique_before_merge,
        "merge_groups_collapsed": merge_groups,
        "override_entries_merged": override_merged,
        "entries_merged_away": merged_away,
        "unique_out_of_corpus": len(entries),
        "min_citations": min_citations,
        "entries_above_threshold": len(filtered),
        "fuzzy_merge_candidates": len(fuzzy_candidates),
        "entries": filtered,
        "merge_candidates": fuzzy_candidates,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--min-citations", type=int, default=DEFAULT_MIN_CITATIONS,
        help=f"Minimum citation count to include in output (default: {DEFAULT_MIN_CITATIONS})",
    )
    p.add_argument(
        "--dry-run", action="store_true",
        help="Print results but do not write files",
    )
    args = p.parse_args()

    print(f"Scanning {RAW_PARSED} ...")
    index = build_index(args.min_citations)

    speech_count  = sum(1 for e in index["entries"] if e["speech_relevant"])
    unknown_count = sum(1 for e in index["entries"] if e["speech_relevant"] is None)

    print(f"Corpus papers            : {index['corpus_papers']}")
    print(f"Out-of-corpus refs       : {index['total_out_of_corpus_refs']}")
    print(f"Unique refs (raw)        : {index['unique_out_of_corpus_before_merge']}")
    print(f"  Merge groups collapsed : {index['merge_groups_collapsed']}  "
          f"({index['entries_merged_away'] - index['override_entries_merged']} entries merged away)")
    print(f"  Manual overrides       : {index['override_entries_merged']} entries merged")
    print(f"Unique refs (deduped)    : {index['unique_out_of_corpus']}")
    print(f"Above threshold (≥{args.min_citations})      : {index['entries_above_threshold']}")
    print(f"  Speech-relevant        : {speech_count}")
    print(f"  Not speech-relevant    : {index['entries_above_threshold'] - speech_count - unknown_count}")
    print(f"  Title unknown          : {unknown_count}")
    print(f"Fuzzy merge candidates   : {index['fuzzy_merge_candidates']}")
    print()

    if not args.dry_run:
        CITATION_INDEX.write_text(json.dumps(index, indent=2, ensure_ascii=False))
        print(f"Wrote {CITATION_INDEX}")

        today = date.today().isoformat()
        log_line = (
            f"- discover | {index['entries_above_threshold']} entries "
            f"({index['merge_groups_collapsed']} merge groups collapsed, "
            f"{index['fuzzy_merge_candidates']} fuzzy candidates), "
            f"{index['corpus_papers']} corpus papers\n"
        )
        _append_to_pipeline_log(today, log_line)
        print(f"Appended discover entry to {PIPELINE_LOG.name}")
    else:
        print("[DRY RUN] No files written.")

    print("\nTop 20 entries:")
    for e in index["entries"][:20]:
        if e["speech_relevant"] is True:
            flag = " [SPEECH]"
        elif e["speech_relevant"] is None:
            flag = " [?]"
        else:
            flag = ""
        title = (e["title"] or e.get("raw_sample") or "(no title)")[:70]
        print(f"  {e['citation_count']:3d}x  {title}{flag}")

    if index["merge_candidates"]:
        print(f"\nFuzzy merge candidates (review manually):")
        for c in index["merge_candidates"][:15]:
            print(f"  Jaccard={c['jaccard']:.2f}")
            for entry in c["entries"]:
                arxiv = f"  arxiv:{entry['arxiv_id']}" if entry["arxiv_id"] else ""
                print(f"    [{entry['count']:3d}x] {entry['title'][:65]}{arxiv}")


def _append_to_pipeline_log(today: str, log_line: str) -> None:
    """Append a log bullet under today's ## YYYY-MM-DD section (newest at top)."""
    path = PIPELINE_LOG
    if not path.exists():
        path.write_text(f"# Pipeline Log\n\n---\n\n## {today}\n\n{log_line}")
        return

    content = path.read_text()
    section_header = f"## {today}"
    if section_header in content:
        # Append bullet to existing today section
        content = content.replace(
            section_header + "\n",
            section_header + "\n" + log_line,
            1,
        )
    else:
        # Insert new section at top (after the --- divider)
        divider = "---\n\n"
        if divider in content:
            content = content.replace(
                divider,
                divider + f"{section_header}\n\n{log_line}\n",
                1,
            )
        else:
            content = f"{section_header}\n\n{log_line}\n\n" + content

    path.write_text(content)


if __name__ == "__main__":
    main()
