#!/usr/bin/env python3
"""
Corpus summary by month.

Prints a table of corpus state (total / parsed / ingested / integrated)
grouped by paper published_date month. Only accepted and ingested papers
are counted; rejected/pending/review are excluded.

Usage:
    python scripts/corpus_summary.py [--tsv]

Options:
    --tsv   Output tab-separated values instead of a formatted table.
"""

import argparse
import glob
import json
import os
import sys
from collections import defaultdict

METADATA_DIR = "raw/metadata"
PARSED_DIR = "raw/parsed"
IN_CORPUS = {"accepted", "ingested"}
PLACEHOLDER_SUFFIX = "-01-01"


def load_corpus():
    rows = defaultdict(lambda: {"total": 0, "parsed": 0, "ready": 0, "ingested": 0, "integrated": 0})
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
            if m.get("integrated_date"):
                rows[key]["integrated"] += 1

    return rows, placeholder_ids, placeholder_months


def print_table(rows, placeholder_ids, placeholder_months, tsv=False):
    keys = sorted(rows.keys())

    # Column headers
    cols = ["month", "total", "parsed", "ready", "ingested", "integrated", "ingested%", "integrated%"]

    if tsv:
        print("\t".join(cols))
        for k in keys:
            r = rows[k]
            ing_pct = f"{100 * r['ingested'] / r['total']:.0f}%" if r["total"] else "—"
            int_pct = f"{100 * r['integrated'] / r['total']:.0f}%" if r["total"] else "—"
            print(f"{k}\t{r['total']}\t{r['parsed']}\t{r['ready']}\t{r['ingested']}\t{r['integrated']}\t{ing_pct}\t{int_pct}")
    else:
        # Formatted table with a vertical divider before the percentage columns
        col_w = [10, 7, 8, 7, 9, 11, 10, 12]
        header = (
            f"{'Month':<{col_w[0]}}  "
            f"{'Total':>{col_w[1]}}  "
            f"{'Parsed':>{col_w[2]}}  "
            f"{'Ready':>{col_w[3]}}  "
            f"{'Ingested':>{col_w[4]}}  "
            f"{'Integrated':>{col_w[5]}}  "
            f"|  "
            f"{'Ingested%':>{col_w[6]}}  "
            f"{'Integrated%':>{col_w[7]}}"
        )
        sep = "-" * len(header)
        print(sep)
        print(header)
        print(sep)

        totals = {"total": 0, "parsed": 0, "ready": 0, "ingested": 0, "integrated": 0}
        for k in keys:
            r = rows[k]
            label = k if k != "unknown" else "unknown  "
            flag = " *" if k in placeholder_months else ""
            ing_pct = f"{100 * r['ingested'] / r['total']:.0f}%" if r["total"] else "—"
            int_pct = f"{100 * r['integrated'] / r['total']:.0f}%" if r["total"] else "—"
            print(
                f"{label:<{col_w[0]}}  "
                f"{r['total']:>{col_w[1]}}  "
                f"{r['parsed']:>{col_w[2]}}  "
                f"{r['ready']:>{col_w[3]}}  "
                f"{r['ingested']:>{col_w[4]}}  "
                f"{r['integrated']:>{col_w[5]}}  "
                f"|  "
                f"{ing_pct:>{col_w[6]}}  "
                f"{int_pct:>{col_w[7]}}"
                f"{flag}"
            )
            for c in totals:
                totals[c] += r[c]

        print(sep)
        total_ing_pct = f"{100 * totals['ingested'] / totals['total']:.0f}%" if totals["total"] else "—"
        total_int_pct = f"{100 * totals['integrated'] / totals['total']:.0f}%" if totals["total"] else "—"
        print(
            f"{'TOTAL':<{col_w[0]}}  "
            f"{totals['total']:>{col_w[1]}}  "
            f"{totals['parsed']:>{col_w[2]}}  "
            f"{totals['ready']:>{col_w[3]}}  "
            f"{totals['ingested']:>{col_w[4]}}  "
            f"{totals['integrated']:>{col_w[5]}}  "
            f"|  "
            f"{total_ing_pct:>{col_w[6]}}  "
            f"{total_int_pct:>{col_w[7]}}"
        )
        print(sep)

        if placeholder_ids:
            print(
                f"\n* {len(placeholder_ids)} papers have placeholder published_date "
                f"(YYYY-01-01 — year-only from scraper); dates are approximate."
            )


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tsv", action="store_true", help="Output TSV instead of formatted table")
    args = parser.parse_args()

    rows, placeholder_ids, placeholder_months = load_corpus()
    print_table(rows, placeholder_ids, placeholder_months, tsv=args.tsv)


if __name__ == "__main__":
    main()
