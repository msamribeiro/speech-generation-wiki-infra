#!/usr/bin/env python3
"""
citation_period_compare.py — Compare citation rates across two time windows.

Splits corpus papers by published_date into two windows (A and B), builds
per-window citation rates (unique citers / papers in window), and produces a
ranked comparison showing risers, fallers, and papers unique to each window.

Deduplication uses the canonical keys from raw/citation_index.json — which
already has the post-hoc title merge and manual overrides applied — so counts
are consistent with the global index. Rebuild citation_index.json first if the
parsed corpus has changed.

Usage:
    # Default: H2 2025 vs H1 2026
    python scripts/discover/citation_period_compare.py

    # Custom windows
    python scripts/discover/citation_period_compare.py \\
        --window-a 2025-07-01 2025-12-31 --label-a "H2 2025" \\
        --window-b 2026-01-01 2026-06-30 --label-b "H1 2026" \\
        --top-n 100

    # Write markdown report
    python scripts/discover/citation_period_compare.py \\
        --output wiki/reports/analyses/citation-h2-2025-vs-h1-2026.md
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

from scripts.discover.citation_index import _canonical_key, _best_title  # noqa: E402

RAW_PARSED     = ROOT / "raw" / "parsed"
RAW_META       = ROOT / "raw" / "metadata"
CITATION_INDEX = ROOT / "raw" / "citation_index.json"
PIPELINE_LOG   = ROOT / "raw" / "pipeline_log.md"

ACTIVE_STATUSES = {"accepted", "ingested"}


# ---------------------------------------------------------------------------
# Key resolution using the global deduped index
# ---------------------------------------------------------------------------

def _build_resolver(index_path: Path) -> dict[str, str]:
    """
    Build a lookup from any key variant → canonical key, using the global
    citation index (which has post-hoc merges and manual overrides applied).

    Resolves by: arxiv_id → canonical key, doi → canonical key,
    normalized title → canonical key.
    """
    if not index_path.exists():
        print(f"Warning: {index_path} not found — dedup will be partial.")
        return {}

    idx = json.loads(index_path.read_text())

    def _norm(s: str) -> str:
        return re.sub(r"[^a-z0-9]", "", s.lower())[:120] if s else ""

    arxiv_to_canon: dict[str, str] = {}
    doi_to_canon: dict[str, str] = {}
    norm_to_canon: dict[str, str] = {}

    for entry in idx.get("entries", []):
        canon = entry["key"]
        if entry.get("arxiv_id"):
            arxiv_to_canon[entry["arxiv_id"]] = canon
        if entry.get("doi"):
            doi_to_canon[entry["doi"]] = canon
        if entry.get("title"):
            nt = _norm(entry["title"])
            if nt:
                norm_to_canon[nt] = canon

    return {"arxiv": arxiv_to_canon, "doi": doi_to_canon, "norm": norm_to_canon}


def _resolve(ref: dict, resolver: dict) -> str:
    """Map a raw reference to its canonical key in the global index."""
    arxiv_id = ref.get("arxiv_id")
    if arxiv_id and arxiv_id in resolver.get("arxiv", {}):
        return resolver["arxiv"][arxiv_id]

    doi = ref.get("doi")
    if doi and doi in resolver.get("doi", {}):
        return resolver["doi"][doi]

    title = _best_title(ref)
    if title:
        nt = re.sub(r"[^a-z0-9]", "", title.lower())[:120]
        if nt in resolver.get("norm", {}):
            return resolver["norm"][nt]

    return _canonical_key(ref)


# ---------------------------------------------------------------------------
# Per-period citation count builder
# ---------------------------------------------------------------------------

def _load_metadata() -> dict[str, dict]:
    meta = {}
    for f in sorted(RAW_META.glob("*.json")):
        try:
            d = json.loads(f.read_text())
            if d.get("status") in ACTIVE_STATUSES and d.get("published_date"):
                meta[d["id"]] = d
        except Exception:
            pass
    return meta


def _papers_in_window(meta: dict, start: str, end: str) -> set[str]:
    return {pid for pid, d in meta.items() if start <= d["published_date"] <= end}


def _build_period_counts(
    paper_ids: set[str],
    resolver: dict,
) -> dict[str, set[str]]:
    """
    For each out-of-corpus reference cited by any paper in paper_ids, return
    a mapping canonical_key → set of citing paper IDs.
    """
    cited_by: dict[str, set[str]] = defaultdict(set)

    for paper_id in paper_ids:
        ref_file = RAW_PARSED / paper_id / "references.json"
        if not ref_file.exists():
            continue
        try:
            refs = json.loads(ref_file.read_text())
        except Exception:
            continue
        for ref in refs:
            if ref.get("in_corpus"):
                continue
            canon = _resolve(ref, resolver)
            if canon:
                cited_by[canon].add(paper_id)

    return dict(cited_by)


# ---------------------------------------------------------------------------
# Comparison logic
# ---------------------------------------------------------------------------

def _citation_rate(counts: dict[str, set[str]], total: int) -> dict[str, float]:
    return {k: len(v) / total for k, v in counts.items()} if total > 0 else {}


def _top_n_titled(
    rate: dict[str, float],
    index_entries: dict[str, dict],
    n: int,
) -> list[tuple[str, float]]:
    """Return top-N entries that have a title in the global index."""
    ranked = sorted(
        [(k, r) for k, r in rate.items() if index_entries.get(k, {}).get("title")],
        key=lambda x: -x[1],
    )
    return ranked[:n]


def compare_periods(
    window_a: tuple[str, str],
    label_a: str,
    window_b: tuple[str, str],
    label_b: str,
    top_n: int = 100,
) -> dict:
    meta = _load_metadata()
    resolver = _build_resolver(CITATION_INDEX)

    idx = json.loads(CITATION_INDEX.read_text()) if CITATION_INDEX.exists() else {"entries": []}
    index_entries = {e["key"]: e for e in idx.get("entries", [])}

    papers_a = _papers_in_window(meta, *window_a)
    papers_b = _papers_in_window(meta, *window_b)

    print(f"{label_a} corpus papers : {len(papers_a)}")
    print(f"{label_b} corpus papers : {len(papers_b)}")

    counts_a = _build_period_counts(papers_a, resolver)
    counts_b = _build_period_counts(papers_b, resolver)

    rate_a = _citation_rate(counts_a, len(papers_a))
    rate_b = _citation_rate(counts_b, len(papers_b))

    top_a = _top_n_titled(rate_a, index_entries, top_n)
    top_b = _top_n_titled(rate_b, index_entries, top_n)

    keys_a = {k: (i + 1, r) for i, (k, r) in enumerate(top_a)}
    keys_b = {k: (i + 1, r) for i, (k, r) in enumerate(top_b)}

    both   = set(keys_a) & set(keys_b)
    a_only = set(keys_a) - set(keys_b)
    b_only = set(keys_b) - set(keys_a)

    # Risers and fallers: papers in both, sorted by rate_b/rate_a
    in_both = []
    for k in both:
        ra, rb = keys_a[k][1], keys_b[k][1]
        ratio = rb / ra if ra > 0 else 999
        e = index_entries.get(k, {})
        in_both.append({
            "key": k,
            "title": e.get("title", ""),
            "year": e.get("year"),
            "rank_a": keys_a[k][0],
            "rank_b": keys_b[k][0],
            "rate_a": round(ra, 4),
            "rate_b": round(rb, 4),
            "ratio": round(ratio, 3),
        })
    in_both.sort(key=lambda x: -x["ratio"])

    def _entry_list(key_set, rank_dict):
        result = []
        for k in key_set:
            e = index_entries.get(k, {})
            rank, rate = rank_dict[k]
            result.append({
                "key": k,
                "title": e.get("title", ""),
                "year": e.get("year"),
                "rank": rank,
                "rate": round(rate, 4),
            })
        return sorted(result, key=lambda x: x["rank"])

    return {
        "generated": date.today().isoformat(),
        "label_a": label_a,
        "label_b": label_b,
        "window_a": list(window_a),
        "window_b": list(window_b),
        "papers_a": len(papers_a),
        "papers_b": len(papers_b),
        "top_n": top_n,
        "overlap": len(both),
        "a_only_count": len(a_only),
        "b_only_count": len(b_only),
        "top_a": [{"key": k, "rate": round(r, 4),
                   "title": index_entries.get(k, {}).get("title", ""),
                   "year": index_entries.get(k, {}).get("year"),
                   "rank": i + 1} for i, (k, r) in enumerate(top_a)],
        "top_b": [{"key": k, "rate": round(r, 4),
                   "title": index_entries.get(k, {}).get("title", ""),
                   "year": index_entries.get(k, {}).get("year"),
                   "rank": i + 1} for i, (k, r) in enumerate(top_b)],
        "in_both": in_both,
        "b_only": _entry_list(b_only, keys_b),
        "a_only": _entry_list(a_only, keys_a),
    }


# ---------------------------------------------------------------------------
# Markdown report generator
# ---------------------------------------------------------------------------

def _md_report(result: dict) -> str:
    la, lb = result["label_a"], result["label_b"]
    wa, wb = result["window_a"], result["window_b"]

    lines = [
        f"# Citation Rate Comparison: {la} vs {lb}",
        "",
        f"**Generated:** {result['generated']}  ",
        f"**Reproduced with:** `python scripts/discover/citation_period_compare.py "
        f"--window-a {wa[0]} {wa[1]} --label-a \"{la}\" "
        f"--window-b {wb[0]} {wb[1]} --label-b \"{lb}\" "
        f"--top-n {result['top_n']}`",
        "",
        "## Overview",
        "",
        f"| | {la} | {lb} |",
        "|-|-------|-------|",
        f"| Corpus papers in window | {result['papers_a']} | {result['papers_b']} |",
        f"| Papers in both top-{result['top_n']} | {result['overlap']} | {result['overlap']} |",
        f"| Papers unique to this window | {result['a_only_count']} | {result['b_only_count']} |",
        "",
        "Citation rate = fraction of papers in the window citing this work. "
        "A rate of 0.20 means 20% of the window's papers cite it.",
        "",
    ]

    # Top-N tables
    for label, top in [(la, result["top_a"]), (lb, result["top_b"])]:
        lines += [
            f"## Top {result['top_n']}: {label}",
            "",
            f"| Rank | Rate | Title | Year |",
            "|------|------|-------|------|",
        ]
        for e in top:
            lines.append(
                f"| {e['rank']} | {e['rate']:.3f} | {e['title']} | {e.get('year') or '—'} |"
            )
        lines.append("")

    # Risers
    lines += [
        f"## Biggest risers ({la} → {lb})",
        "",
        f"Papers in both top-{result['top_n']}, sorted by rate ratio (B/A). "
        "Ratio > 1 means citation rate increased.",
        "",
        f"| Ratio | {la} rank→{lb} rank | {la} rate | {lb} rate | Title | Year |",
        "|-------|---------------------|-----------|-----------|-------|------|",
    ]
    risers = [x for x in result["in_both"] if x["ratio"] >= 1.0]
    for e in risers[:20]:
        lines.append(
            f"| ×{e['ratio']:.2f} | #{e['rank_a']}→#{e['rank_b']} "
            f"| {e['rate_a']:.3f} | {e['rate_b']:.3f} "
            f"| {e['title'][:60]} | {e.get('year') or '—'} |"
        )
    lines.append("")

    # Fallers
    lines += [
        f"## Biggest fallers ({la} → {lb})",
        "",
        f"| Ratio | {la} rank→{lb} rank | {la} rate | {lb} rate | Title | Year |",
        "|-------|---------------------|-----------|-----------|-------|------|",
    ]
    fallers = sorted([x for x in result["in_both"] if x["ratio"] < 1.0], key=lambda x: x["ratio"])
    for e in fallers[:20]:
        lines.append(
            f"| ×{e['ratio']:.2f} | #{e['rank_a']}→#{e['rank_b']} "
            f"| {e['rate_a']:.3f} | {e['rate_b']:.3f} "
            f"| {e['title'][:60]} | {e.get('year') or '—'} |"
        )
    lines.append("")

    # New entries in B
    lines += [
        f"## New in {lb} top-{result['top_n']} (not in {la})",
        "",
        f"| Rank | Rate | Title | Year |",
        "|------|------|-------|------|",
    ]
    for e in result["b_only"]:
        lines.append(
            f"| {e['rank']} | {e['rate']:.3f} | {e['title']} | {e.get('year') or '—'} |"
        )
    lines.append("")

    # Dropped from A
    lines += [
        f"## Dropped from {la} top-{result['top_n']} (not in {lb})",
        "",
        f"| Rank | Rate | Title | Year |",
        "|------|------|-------|------|",
    ]
    for e in result["a_only"]:
        lines.append(
            f"| {e['rank']} | {e['rate']:.3f} | {e['title']} | {e.get('year') or '—'} |"
        )
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--window-a", nargs=2, metavar=("START", "END"),
                   default=["2025-07-01", "2025-12-31"])
    p.add_argument("--window-b", nargs=2, metavar=("START", "END"),
                   default=["2026-01-01", "2026-06-30"])
    p.add_argument("--label-a", default="H2 2025")
    p.add_argument("--label-b", default="H1 2026")
    p.add_argument("--top-n", type=int, default=100)
    p.add_argument("--output", help="Write markdown report to this path")
    p.add_argument("--json-output", help="Write raw JSON results to this path")
    args = p.parse_args()

    result = compare_periods(
        window_a=tuple(args.window_a),
        label_a=args.label_a,
        window_b=tuple(args.window_b),
        label_b=args.label_b,
        top_n=args.top_n,
    )

    la, lb = result["label_a"], result["label_b"]
    print(f"\nOverlap in both top-{args.top_n} : {result['overlap']}")
    print(f"Only in {la:<12}        : {result['a_only_count']}")
    print(f"Only in {lb:<12}        : {result['b_only_count']}")

    print(f"\n=== TOP 20: {la} ===")
    for e in result["top_a"][:20]:
        print(f"  {e['rank']:3d}. {e['rate']:.3f}  {e['title'][:65]}  ({e.get('year') or '?'})")

    print(f"\n=== TOP 20: {lb} ===")
    for e in result["top_b"][:20]:
        print(f"  {e['rank']:3d}. {e['rate']:.3f}  {e['title'][:65]}  ({e.get('year') or '?'})")

    risers = [x for x in result["in_both"] if x["ratio"] >= 1.0][:10]
    print(f"\n=== TOP RISERS ===")
    for e in risers:
        print(f"  ×{e['ratio']:.2f}  #{e['rank_a']}→#{e['rank_b']}  "
              f"{e['rate_a']:.3f}→{e['rate_b']:.3f}  {e['title'][:55]}  ({e.get('year') or '?'})")

    fallers = sorted([x for x in result["in_both"] if x["ratio"] < 1.0],
                     key=lambda x: x["ratio"])[:10]
    print(f"\n=== TOP FALLERS ===")
    for e in fallers:
        print(f"  ×{e['ratio']:.2f}  #{e['rank_a']}→#{e['rank_b']}  "
              f"{e['rate_a']:.3f}→{e['rate_b']:.3f}  {e['title'][:55]}  ({e.get('year') or '?'})")

    if args.output:
        out = Path(args.output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(_md_report(result))
        print(f"\nWrote report to {out}")

    if args.json_output:
        out = Path(args.json_output)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"Wrote JSON to {out}")


if __name__ == "__main__":
    main()
