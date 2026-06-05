#!/usr/bin/env python3
"""
make_batch_queue.py — Generate or refresh the batch conversion queue.

Creates raw/parsed/batch_queue.json listing all pending papers split into
batches of N (default 20), ordered alphabetically by paper ID.

If the queue file already exists, only NEW pending papers (not already in any
batch) are appended as new batches at the end.  Existing batches and their
statuses are preserved.

Use --sync to reconcile batch statuses with actual disk state (paper.md
presence). Run this after completing a batch to keep the queue readable.

Usage:
    python scripts/parse/make_batch_queue.py
    python scripts/parse/make_batch_queue.py --batch-size 40
    python scripts/parse/make_batch_queue.py --sync        # update statuses from disk
    python scripts/parse/make_batch_queue.py --refresh     # rebuild from scratch
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


def _batch_status_from_disk(papers: list[str]) -> tuple[str, int, int]:
    """
    Derive batch status from disk state.
    Returns (status, succeeded, failed) where status is one of:
      "done"    — all papers have paper.md and no error.json
      "partial" — some papers done, some pending or failed
      "failed"  — all papers have error.json
      "pending" — no papers have paper.md yet
    """
    done = failed = pending = 0
    for pid in papers:
        paper_md   = RAW_PARSED / pid / "paper.md"
        error_json = RAW_PARSED / pid / "error.json"
        if paper_md.exists() and not error_json.exists():
            done += 1
        elif error_json.exists():
            failed += 1
        else:
            pending += 1

    total = len(papers)
    if done == total:
        status = "done"
    elif failed == total:
        status = "failed"
    elif pending == total:
        status = "pending"
    else:
        status = "partial"

    return status, done, failed


def _sync_queue(queue: dict) -> int:
    """Update all batch statuses from disk. Returns number of batches changed."""
    changed = 0
    for b in queue["batches"]:
        status, succeeded, failed = _batch_status_from_disk(b["papers"])
        if b["status"] != status or b["succeeded"] != succeeded or b["failed"] != failed:
            b["status"]    = status
            b["succeeded"] = succeeded
            b["failed"]    = failed if failed else None
            changed += 1
    return changed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--batch-size", type=int, default=20, metavar="N")
    parser.add_argument("--refresh", action="store_true", help="Rebuild queue from scratch (discards status history)")
    parser.add_argument("--sync",    action="store_true", help="Reconcile batch statuses with disk state (paper.md presence)")
    args = parser.parse_args()

    RAW_PARSED.mkdir(parents=True, exist_ok=True)

    # --sync: update existing queue statuses from disk, then exit
    if args.sync:
        if not QUEUE_FILE.exists():
            print("No queue file found — run without --sync first.")
            return
        queue = json.loads(QUEUE_FILE.read_text(encoding="utf-8"))
        changed = _sync_queue(queue)
        QUEUE_FILE.write_text(json.dumps(queue, indent=2), encoding="utf-8")
        print(f"Synced. {changed} batch(es) updated.")
        print()
        _print_summary(queue)
        return

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
            _print_summary(queue)
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
    print(f"{action}.")
    _print_summary(queue)


def _print_summary(queue: dict) -> None:
    from collections import Counter
    n_batches = len(queue["batches"])
    n_papers  = queue["total_papers"]
    status_counts = Counter(b["status"] for b in queue["batches"])

    print(f"Queue file  : {QUEUE_FILE}")
    print(f"Papers      : {n_papers}")
    print(f"Batches     : {n_batches}  ({', '.join(f'{v} {k}' for k, v in sorted(status_counts.items()))})")
    print()
    print("Batch summary:")
    status_tag = {"pending": "[ ]", "running": "[~]", "done": "[✓]", "partial": "[!]", "failed": "[✗]"}
    for b in queue["batches"]:
        tag   = status_tag.get(b["status"], "[?]")
        count = f"{b['succeeded']}/{len(b['papers'])}" if b.get("succeeded") is not None else f"{len(b['papers'])} papers"
        print(f"  {tag} Batch {b['id']:>3} — {count:>12}  ({b['papers'][0]} … {b['papers'][-1]})")


if __name__ == "__main__":
    main()
