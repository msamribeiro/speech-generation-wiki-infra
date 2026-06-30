#!/usr/bin/env python3
"""
Corpus summary by month, plus integration coverage per concept.

Prints two tables:
  1. Corpus state (total / parsed / ingested) grouped by published_date month.
     Only accepted and ingested papers are counted; rejected/pending/review excluded.
  2. Integration coverage per concept: papers that reference the concept in
     related_concepts vs. papers currently integrated into wiki/_claims/{slug}.yaml.

Usage:
    python scripts/corpus_summary.py [--tsv] [--group-before YYYY-MM]

Options:
    --tsv               Output tab-separated values instead of a formatted table.
    --group-before      Collapse all months strictly before YYYY-MM into a single row.
"""

import argparse
import glob
import json
import os
import re
import sys
from collections import defaultdict

import yaml

METADATA_DIR = "raw/metadata"
PARSED_DIR = "raw/parsed"
CLAIMS_DIR = "wiki/_claims"
PAPERS_DIR = "wiki/papers"
IN_CORPUS = {"accepted", "ingested"}
PLACEHOLDER_SUFFIX = "-01-01"


def load_corpus():
    rows = defaultdict(lambda: {"total": 0, "parsed": 0, "ready": 0, "ingested": 0})
    placeholder_ids = []
    placeholder_months = set()

    for path in sorted(glob.glob(f"{METADATA_DIR}/*.json")):
        with open(path) as fh:
            m = json.load(fh)

        if m.get("status") not in IN_CORPUS:
            continue

        pid = m["id"]
        date = m.get("published_date") or ""

        # Flag placeholder dates (year-only scrapes stored as YYYY-01-01)
        if date.endswith(PLACEHOLDER_SUFFIX):
            placeholder_ids.append(pid)
            key = date[:7]
            placeholder_months.add(key)
        elif len(date) >= 7:
            key = date[:7]  # YYYY-MM
        else:
            key = "unknown"

        rows[key]["total"] += 1

        has_paper_md = os.path.exists(f"{PARSED_DIR}/{pid}/paper.md")

        if has_paper_md:
            rows[key]["parsed"] += 1

        if m.get("status") == "accepted" and has_paper_md:
            rows[key]["ready"] += 1

        if m.get("status") == "ingested":
            rows[key]["ingested"] += 1

    return rows, placeholder_ids, placeholder_months


def print_table(rows, placeholder_ids, placeholder_months, tsv=False, group_before=None):
    if group_before:
        grouped_label = f"< {group_before}"
        grouped = {"total": 0, "parsed": 0, "ready": 0, "ingested": 0}
        grouped_has_placeholder = False
        remaining = {}
        for k, v in rows.items():
            if k != "unknown" and k < group_before:
                for c in grouped:
                    grouped[c] += v[c]
                if k in placeholder_months:
                    grouped_has_placeholder = True
            else:
                remaining[k] = v
        rows = {grouped_label: grouped, **remaining}
        placeholder_months = placeholder_months | ({grouped_label} if grouped_has_placeholder else set())
        keys = [grouped_label] + sorted(remaining.keys())
    else:
        keys = sorted(rows.keys())

    # Column headers
    cols = ["month", "total", "parsed", "to_ingest", "ingested", "ingested%"]

    if tsv:
        print("\t".join(cols))
        for k in keys:
            r = rows[k]
            ing_pct = f"{100 * r['ingested'] / r['total']:.0f}%" if r["total"] else "—"
            print(f"{k}\t{r['total']}\t{r['parsed']}\t{r['ready']}\t{r['ingested']}\t{ing_pct}")
    else:
        # Formatted table with a vertical divider before the percentage columns
        col_w = [10, 7, 8, 10, 9, 10]
        header = (
            f"{'Month':<{col_w[0]}}  "
            f"{'Total':>{col_w[1]}}  "
            f"{'Parsed':>{col_w[2]}}  "
            f"{'To Ingest':>{col_w[3]}}  "
            f"{'Ingested':>{col_w[4]}}  "
            f"|  "
            f"{'Ingested%':>{col_w[5]}}"
        )
        sep = "-" * len(header)
        print(sep)
        print(header)
        print(sep)

        totals = {"total": 0, "parsed": 0, "ready": 0, "ingested": 0}
        for k in keys:
            r = rows[k]
            label = k if k != "unknown" else "unknown  "
            flag = " *" if k in placeholder_months else ""
            ing_pct = f"{100 * r['ingested'] / r['total']:.0f}%" if r["total"] else "—"
            print(
                f"{label:<{col_w[0]}}  "
                f"{r['total']:>{col_w[1]}}  "
                f"{r['parsed']:>{col_w[2]}}  "
                f"{r['ready']:>{col_w[3]}}  "
                f"{r['ingested']:>{col_w[4]}}  "
                f"|  "
                f"{ing_pct:>{col_w[5]}}  "
                f"{flag}"
            )
            for c in totals:
                totals[c] += r[c]

        print(sep)
        total_ing_pct = f"{100 * totals['ingested'] / totals['total']:.0f}%" if totals["total"] else "—"
        print(
            f"{'TOTAL':<{col_w[0]}}  "
            f"{totals['total']:>{col_w[1]}}  "
            f"{totals['parsed']:>{col_w[2]}}  "
            f"{totals['ready']:>{col_w[3]}}  "
            f"{totals['ingested']:>{col_w[4]}}  "
            f"|  "
            f"{total_ing_pct:>{col_w[5]}}  "
        )
        print(sep)

        if placeholder_ids:
            print(
                f"\n* {len(placeholder_ids)} papers have placeholder published_date "
                f"(YYYY-01-01 — year-only from scraper); dates are approximate."
            )


_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)


def _parse_frontmatter(path):
    with open(path) as fh:
        head = fh.read(4096)
    m = _FRONTMATTER_RE.match(head)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}


def load_integration_stats():
    """Return (integrated, covers) dicts keyed by concept slug.

    integrated[slug] = number of papers in the concept's _claims YAML
    covers[slug]     = number of ingested paper pages listing slug in related_concepts
    """
    integrated = {}
    for path in sorted(glob.glob(f"{CLAIMS_DIR}/*.yaml")):
        slug = os.path.basename(path)[:-5]
        with open(path) as fh:
            data = yaml.safe_load(fh)
        integrated[slug] = len(data.get("papers", []))

    covers = defaultdict(int)
    for path in glob.glob(f"{PAPERS_DIR}/*.md"):
        fm = _parse_frontmatter(path)
        for concept in fm.get("related_concepts") or []:
            covers[concept] += 1

    return integrated, covers


def print_integration_table(integrated, covers, tsv=False):
    all_slugs = set(integrated.keys()) | set(covers.keys())
    if not all_slugs:
        return

    slugs = sorted(all_slugs)

    if tsv:
        print("\nconcept\tcovers\tintegrated\tintegrated%")
        for slug in slugs:
            n_int = integrated.get(slug, 0)
            n_cov = covers.get(slug, 0)
            pct = f"{100 * n_int / n_cov:.0f}%" if n_cov else "—"
            print(f"{slug}\t{n_cov}\t{n_int}\t{pct}")
        return

    # Formatted table
    slug_w = max(len(s) for s in slugs)
    slug_w = max(slug_w, len("Concept"))
    col_w = [slug_w, 8, 12, 13]
    header = (
        f"{'Concept':<{col_w[0]}}  "
        f"{'Covers':>{col_w[1]}}  "
        f"{'Integrated':>{col_w[2]}}  "
        f"|  "
        f"{'Integrated%':>{col_w[3]}}"
    )
    sep = "-" * len(header)
    print(f"\n\nIntegration coverage by concept")
    print(sep)
    print(header)
    print(sep)

    total_int = 0
    total_cov = 0
    for slug in slugs:
        n_int = integrated.get(slug, 0)
        n_cov = covers.get(slug, 0)
        pct = f"{100 * n_int / n_cov:.0f}%" if n_cov else "—"
        print(
            f"{slug:<{col_w[0]}}  "
            f"{n_cov:>{col_w[1]}}  "
            f"{n_int:>{col_w[2]}}  "
            f"|  "
            f"{pct:>{col_w[3]}}"
        )
        total_int += n_int
        total_cov += n_cov

    print(sep)
    total_pct = f"{100 * total_int / total_cov:.0f}%" if total_cov else "—"
    print(
        f"{'TOTAL':<{col_w[0]}}  "
        f"{total_cov:>{col_w[1]}}  "
        f"{total_int:>{col_w[2]}}  "
        f"|  "
        f"{total_pct:>{col_w[3]}}"
    )
    print(sep)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tsv", action="store_true", help="Output TSV instead of formatted table")
    parser.add_argument("--group-before", metavar="YYYY-MM", help="Collapse all months before YYYY-MM into a single row")
    args = parser.parse_args()

    rows, placeholder_ids, placeholder_months = load_corpus()
    print_table(rows, placeholder_ids, placeholder_months, tsv=args.tsv, group_before=args.group_before)

    integrated, covers = load_integration_stats()
    print_integration_table(integrated, covers, tsv=args.tsv)


if __name__ == "__main__":
    main()
