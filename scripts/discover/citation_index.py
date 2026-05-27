#!/usr/bin/env python3
"""
citation_index.py — Build out-of-corpus citation index from parsed papers.

Scans all raw/parsed/{id}/references.json files, counts how many corpus papers
cite each out-of-corpus reference, deduplicates by arXiv ID > DOI > normalized
title, and flags entries that match corpus speech-synthesis keywords.

Entries with citation_count < --min-citations are excluded from the output.

Output: raw/citation_index.json

Usage:
    python scripts/discover/citation_index.py
    python scripts/discover/citation_index.py --min-citations 5
    python scripts/discover/citation_index.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from lib.keyword_filter import load_keyword_filter, passes_filter  # noqa: E402

RAW_PARSED     = ROOT / "raw" / "parsed"
CITATION_INDEX = ROOT / "raw" / "citation_index.json"
WIKI_LOG       = ROOT / "wiki" / "log.md"

DEFAULT_MIN_CITATIONS = 4


# ---------------------------------------------------------------------------
# Deduplication helpers
# ---------------------------------------------------------------------------

def _normalize(text: str) -> str:
    """Lowercase, alphanumeric-only — used as dedup key component."""
    return re.sub(r"[^a-z0-9]", "", text.lower())


def _extract_title_from_raw(raw: str) -> str | None:
    """
    Try to extract a paper title from a raw bibliography string.

    Handles two common citation styles:
    - IEEE/Interspeech: authors, 'Title in single quotes,' venue, year
    - Typographic quotes: ‘Title’
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

    filtered = sorted(
        (e for e in entries.values() if e["citation_count"] >= min_citations),
        key=lambda e: (-e["citation_count"], e.get("title") or ""),
    )

    return {
        "generated": date.today().isoformat(),
        "corpus_papers": len(ref_files),
        "total_out_of_corpus_refs": total_refs,
        "unique_out_of_corpus": len(entries),
        "min_citations": min_citations,
        "entries_above_threshold": len(filtered),
        "entries": filtered,
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

    print(f"Corpus papers          : {index['corpus_papers']}")
    print(f"Out-of-corpus refs     : {index['total_out_of_corpus_refs']}")
    print(f"Unique refs            : {index['unique_out_of_corpus']}")
    print(f"Above threshold (≥{args.min_citations})    : {index['entries_above_threshold']}")
    print(f"  Speech-relevant      : {speech_count}")
    print(f"  Not speech-relevant  : {index['entries_above_threshold'] - speech_count - unknown_count}")
    print(f"  Title unknown        : {unknown_count}")
    print()

    if not args.dry_run:
        CITATION_INDEX.write_text(json.dumps(index, indent=2, ensure_ascii=False))
        print(f"Wrote {CITATION_INDEX}")

        log_line = (
            f"\n## [{date.today().isoformat()}] discover | "
            f"{index['entries_above_threshold']} candidates surfaced "
            f"({speech_count} speech-relevant), {index['corpus_papers']} corpus papers"
        )
        with open(WIKI_LOG, "a") as f:
            f.write(log_line)
        print(f"Appended discover entry to {WIKI_LOG.name}")
    else:
        print("[DRY RUN] No files written.")

    print("\nTop entries:")
    for e in index["entries"][:20]:
        if e["speech_relevant"] is True:
            flag = " [SPEECH]"
        elif e["speech_relevant"] is None:
            flag = " [?]"
        else:
            flag = ""
        title = (e["title"] or e.get("raw_sample") or "(no title)")[:70]
        print(f"  {e['citation_count']:3d}x  {title}{flag}")


if __name__ == "__main__":
    main()
