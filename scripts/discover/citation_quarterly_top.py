#!/usr/bin/env python3
"""
citation_quarterly_top.py — Per-quarter top-N out-of-corpus citations (quarter-close step).

For each requested quarter, counts how many corpus papers published in that quarter cite each
reference, takes the top N titled references, and unions the per-quarter lists. Every candidate
is then checked against the *current* metadata (arXiv ID, DOI, normalized title), because the
`in_corpus` flags in `references.json` were set at parse time and go stale once a cited paper is
ingested later.

Citing papers: active records (`accepted` or `ingested`) with a parse, not `is_duplicate`, not
`discovery_source: citation-discovery` (those are foundational papers pulled in by an earlier
run, not part of the quarter's literature), bucketed by canonical `published_date`.

Keys are resolved through `raw/citation_index.json` (post-hoc title merge and manual overrides
applied), so rebuild it first: `python scripts/discover/citation_index.py`.

Usage:
    python scripts/discover/citation_quarterly_top.py --quarters 2025Q3 2025Q4 2026Q1 2026Q2
    python scripts/discover/citation_quarterly_top.py --quarters 2026Q3 --top-n 100 \\
        --output docs/records/2026-12-01-discovery-quarterly-top100-2026Q3
    # --compare: an earlier run's JSON, to report entries/exits against it
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

from scripts.discover.citation_period_compare import _build_resolver, _resolve  # noqa: E402

RAW_PARSED = ROOT / "raw" / "parsed"
RAW_META = ROOT / "raw" / "metadata"
CITATION_INDEX = ROOT / "raw" / "citation_index.json"
ACTIVE = {"accepted", "ingested"}


def _norm(s: str | None) -> str:
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())[:120]


def quarter_bounds(q: str) -> tuple[str, str]:
    m = re.fullmatch(r"(\d{4})Q([1-4])", q)
    if not m:
        raise SystemExit(f"bad quarter {q!r}; use e.g. 2026Q2")
    y, n = int(m.group(1)), int(m.group(2))
    start_m = 3 * (n - 1) + 1
    end_m = start_m + 2
    end_d = {3: 31, 6: 30, 9: 30, 12: 31}[end_m]
    return f"{y}-{start_m:02d}-01", f"{y}-{end_m:02d}-{end_d:02d}"


def load_metadata() -> list[dict]:
    out = []
    for f in sorted(RAW_META.glob("*.json")):
        try:
            out.append(json.loads(f.read_text()))
        except Exception:
            pass
    return out


def corpus_lookup(meta: list[dict]) -> dict[str, dict[str, dict]]:
    """arXiv / DOI / normalized-title → metadata record (any status)."""
    by_arxiv: dict[str, dict] = {}
    by_doi: dict[str, dict] = {}
    by_title: dict[str, dict] = {}
    rank = {"ingested": 0, "accepted": 1, "review": 2, "pending": 3, "rejected": 4}

    def put(d: dict, k: str, rec: dict) -> None:
        old = d.get(k)
        if old is None or rank.get(rec.get("status"), 9) < rank.get(old.get("status"), 9):
            d[k] = rec

    for m in meta:
        ax = (m.get("source_ids") or {}).get("arxiv")
        if ax:
            put(by_arxiv, ax, m)
        if re.fullmatch(r"\d{4}\.\d{4,5}", m.get("id", "")):
            put(by_arxiv, m["id"], m)
        doi = m.get("doi") or (m.get("source_ids") or {}).get("doi")
        if doi:
            put(by_doi, doi.lower(), m)
        nt = _norm(m.get("title"))
        if nt:
            put(by_title, nt, m)
    return {"arxiv": by_arxiv, "doi": by_doi, "title": by_title}


def corpus_status(entry: dict, lk: dict) -> dict:
    """Best-ranked matching record across arXiv, DOI and title routes, so a rejected arXiv
    alternate (e.g. F5-TTS 2410.06885) yields to the active proceedings record."""
    rank = {"ingested": 0, "accepted": 1, "review": 2, "pending": 3, "rejected": 4}
    found = []
    if entry.get("arxiv_id") and entry["arxiv_id"] in lk["arxiv"]:
        found.append((lk["arxiv"][entry["arxiv_id"]], "arxiv"))
    if entry.get("doi") and entry["doi"].lower() in lk["doi"]:
        found.append((lk["doi"][entry["doi"].lower()], "doi"))
    if _norm(entry.get("title")) and _norm(entry.get("title")) in lk["title"]:
        found.append((lk["title"][_norm(entry.get("title"))], "title"))
    if not found:
        return {"status": "not in corpus"}
    rec, how = min(found, key=lambda f: rank.get(f[0].get("status"), 9))
    page = rec.get("wiki_page_id") or rec.get("canonical_id") or rec["id"]
    return {"status": rec.get("status"), "record": rec["id"], "page": page, "matched_by": how,
            "is_duplicate": bool(rec.get("is_duplicate"))}


def run(quarters: list[str], top_n: int) -> dict:
    meta = load_metadata()
    resolver = _build_resolver(CITATION_INDEX)
    idx = json.loads(CITATION_INDEX.read_text())
    entries = {e["key"]: e for e in idx["entries"]}
    lk = corpus_lookup(meta)

    citers = [m for m in meta
              if m.get("status") in ACTIVE and not m.get("is_duplicate")
              and m.get("discovery_source") != "citation-discovery"
              and m.get("published_date")
              and (RAW_PARSED / m["id"] / "references.json").exists()]

    per_q: dict[str, dict[str, set[str]]] = {}
    sizes: dict[str, int] = {}
    for q in quarters:
        a, b = quarter_bounds(q)
        ids = [m["id"] for m in citers if a <= str(m["published_date"]) <= b]
        sizes[q] = len(ids)
        counts: dict[str, set[str]] = defaultdict(set)
        for pid in ids:
            for ref in json.loads((RAW_PARSED / pid / "references.json").read_text()):
                k = _resolve(ref, resolver)
                if k:
                    counts[k].add(pid)
        per_q[q] = counts

    tops: dict[str, list[str]] = {}
    for q in quarters:
        ranked = sorted(
            ((k, len(v)) for k, v in per_q[q].items()
             if entries.get(k, {}).get("title") or entries.get(k, {}).get("arxiv_id")),
            key=lambda kv: (-kv[1], kv[0]))
        tops[q] = [k for k, _ in ranked[:top_n]]

    union = sorted({k for q in quarters for k in tops[q]},
                   key=lambda k: -sum(len(per_q[q].get(k, ())) for q in quarters))
    rows = []
    for k in union:
        e = entries.get(k, {"key": k})
        by_q = {q: len(per_q[q].get(k, ())) for q in quarters}
        rows.append({
            "key": k, "arxiv_id": e.get("arxiv_id"), "doi": e.get("doi"),
            "title": e.get("title"), "year": e.get("year"),
            "speech_relevant": e.get("speech_relevant"),
            "window_total": sum(by_q.values()), "index_total": e.get("citation_count"),
            "by_quarter": by_q, "in_top_n_of": [q for q in quarters if k in tops[q]],
            "corpus": corpus_status(e, lk),
        })
    return {"generated": date.today().isoformat(), "quarters": quarters, "top_n": top_n,
            "citing_papers": sizes, "candidates": len(rows), "rows": rows}


def to_markdown(res: dict, compare: dict | None) -> str:
    qs = res["quarters"]
    head = " | ".join(f"{q[2:4]}{q[4:]}" for q in qs)
    lines = [f"# Quarterly Top-{res['top_n']} Citation Discovery ({qs[0]}–{qs[-1]})", "",
             f"**Generated:** {res['generated']}  ",
             "**Method:** `scripts/discover/citation_quarterly_top.py`. Per quarter, the "
             f"{res['top_n']} references most cited by corpus papers published in that quarter "
             "(active, non-duplicate, excluding citation-discovery records); union of the lists. "
             "Corpus status is checked against current metadata.", "",
             "Citing papers per quarter: " + ", ".join(f"{q} {res['citing_papers'][q]}" for q in qs),
             f"; candidates in the union: {res['candidates']}.", ""]
    new = [r for r in res["rows"] if r["corpus"]["status"] == "not in corpus"]
    rej = [r for r in res["rows"] if r["corpus"]["status"] == "rejected"]
    lines += [f"Not in corpus: {len(new)}; in corpus but rejected: {len(rej)}; "
              f"already accepted or ingested: {len(res['rows']) - len(new) - len(rej)}.", ""]
    if compare:
        old_rows = compare if isinstance(compare, list) else compare.get("rows", [])
        old = {r.get("arxiv_id") or r["key"] for r in old_rows}
        lines += [f"New to the union since the compared run: "
                  f"{sum(1 for r in res['rows'] if (r['arxiv_id'] or r['key']) not in old)}.", ""]

    def table(rows: list[dict], title: str) -> None:
        lines.extend([f"## {title} ({len(rows)})", "",
                      f"| # | arXiv | Title | SR | Window | {head} | Corpus |",
                      "|---|---|---|---|---|" + "---|" * len(qs) + "---|"])
        for i, r in enumerate(rows, 1):
            t = (r["title"] or r["key"])[:70].replace("|", "/")
            sr = {True: "Y", False: "N"}.get(r["speech_relevant"], "?")
            c = r["corpus"]
            cs = c["status"] if c["status"] == "not in corpus" else f"{c['status']} `{c['page']}`"
            qv = " | ".join(str(r["by_quarter"][q]) for q in qs)
            lines.append(f"| {i} | {r['arxiv_id'] or '—'} | {t} | {sr} | {r['window_total']} | "
                         f"{qv} | {cs} |")
        lines.append("")

    table(new, "Not in corpus")
    table(rej, "In corpus metadata but rejected")
    table([r for r in res["rows"] if r not in new and r not in rej], "Already accepted or ingested")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--quarters", nargs="+", required=True)
    ap.add_argument("--top-n", type=int, default=100)
    ap.add_argument("--output", help="path stem: writes {stem}.md and {stem}.json")
    ap.add_argument("--compare", help="earlier run JSON to diff against")
    a = ap.parse_args()
    res = run(a.quarters, a.top_n)
    cmp = json.loads(Path(a.compare).read_text()) if a.compare else None
    md = to_markdown(res, cmp)
    if a.output:
        Path(a.output + ".json").write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n")
        Path(a.output + ".md").write_text(md + "\n")
        print(f"wrote {a.output}.md and .json")
    else:
        print(md)


if __name__ == "__main__":
    main()
