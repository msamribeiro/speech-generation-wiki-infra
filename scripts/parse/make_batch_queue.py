#!/usr/bin/env python3
"""
make_batch_queue.py — Generate or refresh the batch conversion queue.

Creates raw/parsed/batch_queue.json listing all pending papers split into
batches of N (default 20), ordered alphabetically by paper ID.

If the queue file already exists, only NEW pending papers (not already in any
batch) are appended as new batches at the end.  Existing batches and their
statuses are preserved.

Usage:
    python scripts/parse/make_batch_queue.py
    python scripts/parse/make_batch_queue.py --batch-size 10
    python scripts/parse/make_batch_queue.py --refresh   # rebuild from scratch
"""

import argparse
import json
from datetime import datetime
from pathlib import Path

ROOT         = Path(__file__).parent.parent.parent
RAW_METADATA = ROOT / "raw" / "metadata"
RAW_PAPERS   = ROOT / "raw" / "papers"
RAW_PARSED   = ROOT / "raw" / "parsed"
QUEUE_FILE   = RAW_PARSED / "batch_queue.json"


def _load_eligible_papers() -> list[str]:
    """Return sorted list of paper IDs that are accepted, have a PDF, and are not yet DONE."""
    eligible = []
    for f in sorted(RAW_METADATA.glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if d.get("status") != "accepted":
            continue
        pid = d.get("id")
        if not pid:
            continue
        pdf_rel = d.get("pdf_path")
        if not pdf_rel or not (ROOT / pdf_rel).exists():
            continue
        # Skip already-done papers
        paper_md = RAW_PARSED / pid / "paper.md"
        if paper_md.exists() and not (RAW_PARSED / pid / "error.json").exists():
            continue
        eligible.append(pid)
    return eligible


def _chunked(lst: list, size: int) -> list[list]:
    return [lst[i : i + size] for i in range(0, len(lst), size)]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--batch-size", type=int, default=20, metavar="N")
    parser.add_argument("--refresh", action="store_true", help="Rebuild queue from scratch (discards status history)")
    args = parser.parse_args()

    RAW_PARSED.mkdir(parents=True, exist_ok=True)

    eligible = _load_eligible_papers()

    if args.refresh or not QUEUE_FILE.exists():
        # Build from scratch
        chunks = _chunked(eligible, args.batch_size)
        batches = [
            {
                "id": i + 1,
                "status": "pending",
                "papers": chunk,
                "started_at": None,
                "completed_at": None,
                "succeeded": None,
                "failed": None,
            }
            for i, chunk in enumerate(chunks)
        ]
        queue = {
            "generated_at": datetime.now().date().isoformat(),
            "batch_size": args.batch_size,
            "total_papers": len(eligible),
            "batches": batches,
        }
        action = "Created"
    else:
        # Incremental: add only papers not already in any batch
        queue = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
        existing_ids: set[str] = set()
        for b in queue["batches"]:
            existing_ids.update(b["papers"])

        new_papers = [pid for pid in eligible if pid not in existing_ids]
        if not new_papers:
            print(f"Queue already up-to-date. {len(queue['batches'])} batches, no new papers.")
            return

        next_id = max(b["id"] for b in queue["batches"]) + 1
        for i, chunk in enumerate(_chunked(new_papers, args.batch_size)):
            queue["batches"].append({
                "id": next_id + i,
                "status": "pending",
                "papers": chunk,
                "started_at": None,
                "completed_at": None,
                "succeeded": None,
                "failed": None,
            })
        queue["total_papers"] = sum(len(b["papers"]) for b in queue["batches"])
        action = f"Appended {len(new_papers)} new papers in {len(_chunked(new_papers, args.batch_size))} batch(es)"

    QUEUE_FILE.write_text(json.dumps(queue, indent=2), encoding="utf-8")

    n_batches = len(queue["batches"])
    n_papers  = queue["total_papers"]
    print(f"{action}.")
    print(f"Queue file  : {QUEUE_FILE}")
    print(f"Papers      : {n_papers}")
    print(f"Batches     : {n_batches}  (batch size {args.batch_size})")
    print()
    print("Batch summary:")
    for b in queue["batches"]:
        status_tag = {
            "pending":  "[ ]",
            "running":  "[~]",
            "done":     "[✓]",
            "partial":  "[!]",
        }.get(b["status"], "[?]")
        print(f"  {status_tag} Batch {b['id']:>3} — {len(b['papers'])} papers  ({b['papers'][0]} … {b['papers'][-1]})")


if __name__ == "__main__":
    main()
