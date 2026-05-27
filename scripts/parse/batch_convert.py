#!/usr/bin/env python3
"""
batch_convert.py — Batch PDF-to-Markdown converter for the speech-generation corpus.

Processes all accepted papers through convert_paper.py, producing LLM-ready
Markdown in raw/parsed/{id}/.

State model:
  DONE    — paper.md exists and no error.json  (skipped by default)
  FAILED  — error.json exists                  (retried by default)
  PENDING — neither file exists                (always processed)

Usage:
    python scripts/parse/batch_convert.py
    python scripts/parse/batch_convert.py --status
    python scripts/parse/batch_convert.py --limit 5 --dry-run
    python scripts/parse/batch_convert.py --retry-failed
    python scripts/parse/batch_convert.py --ids 2501.12345 2502.67890
    python scripts/parse/batch_convert.py --workers 2
"""

import argparse
import json
import signal
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from scripts.parse.convert_paper import (  # noqa: E402 (after sys.path setup)
    ConversionResult,
    _make_converter,
    build_corpus_index,
    convert_paper,
)

RAW_METADATA = ROOT / "raw" / "metadata"
RAW_PAPERS   = ROOT / "raw" / "papers"
RAW_PARSED   = ROOT / "raw" / "parsed"
BATCH_LOG    = RAW_PARSED / "batch_convert.log"


# ---------------------------------------------------------------------------
# State helpers
# ---------------------------------------------------------------------------

def _paper_state(paper_id: str) -> str:
    out = RAW_PARSED / paper_id
    if (out / "paper.md").exists() and not (out / "error.json").exists():
        return "done"
    if (out / "error.json").exists():
        return "failed"
    return "pending"


def _load_queue(
    ids_filter: list[str] | None,
    force: bool,
    retry_failed_only: bool,
) -> list[dict]:
    queue = []
    for f in sorted(RAW_METADATA.glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if d.get("status") != "accepted":
            continue
        paper_id = d.get("id")
        if not paper_id:
            continue
        if ids_filter and paper_id not in ids_filter:
            continue
        pdf_rel = d.get("pdf_path")
        if not pdf_rel:
            continue
        pdf_path = ROOT / pdf_rel
        if not pdf_path.exists():
            continue

        state = _paper_state(paper_id)

        if retry_failed_only:
            if state != "failed":
                continue
        elif not force and state == "done":
            continue

        queue.append({"id": paper_id, "pdf_path": pdf_path, "state": state})
    return queue


# ---------------------------------------------------------------------------
# Status reporting
# ---------------------------------------------------------------------------

def _print_status() -> None:
    done = failed = pending = no_pdf = 0
    for f in sorted(RAW_METADATA.glob("*.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue
        if d.get("status") != "accepted":
            continue
        paper_id = d.get("id")
        if not paper_id:
            continue
        pdf_rel = d.get("pdf_path")
        if not pdf_rel or not (ROOT / pdf_rel).exists():
            no_pdf += 1
            continue
        state = _paper_state(paper_id)
        if state == "done":
            done += 1
        elif state == "failed":
            failed += 1
        else:
            pending += 1

    total = done + failed + pending + no_pdf
    print(f"Accepted papers : {total}")
    print(f"  done          : {done}")
    print(f"  failed        : {failed}")
    print(f"  pending       : {pending}")
    print(f"  no PDF on disk: {no_pdf}")


# ---------------------------------------------------------------------------
# Log helper
# ---------------------------------------------------------------------------

def _append_log(record: dict) -> None:
    BATCH_LOG.parent.mkdir(parents=True, exist_ok=True)
    with BATCH_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record) + "\n")


# ---------------------------------------------------------------------------
# Multi-worker support
# ---------------------------------------------------------------------------

# Module-level globals — populated once per worker process in the initializer.
_CONVERTER:    object = None
_CORPUS_INDEX: dict   = None


def _worker_init(corpus_index: dict) -> None:
    global _CONVERTER, _CORPUS_INDEX
    # sys.path may not be inherited in spawn mode (Python 3.12 on macOS uses spawn)
    sys.path.insert(0, str(ROOT))
    from scripts.parse.convert_paper import _make_converter as _mc
    _CONVERTER    = _mc()
    _CORPUS_INDEX = corpus_index


def _convert_worker(paper_id: str, pdf_path_str: str, output_dir_str: str, force: bool) -> ConversionResult:
    return convert_paper(
        paper_id=paper_id,
        pdf_path=Path(pdf_path_str),
        output_dir=Path(output_dir_str),
        force=force,
        corpus_index=_CORPUS_INDEX,
        converter=_CONVERTER,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--workers", type=int, default=1, metavar="N",
        help="Parallel worker processes (default: 1). Each loads ~3–5 GB of ML models.",
    )
    parser.add_argument(
        "--limit", type=int, metavar="N",
        help="Process at most N papers (useful for smoke-testing)",
    )
    parser.add_argument(
        "--offset", type=int, default=0, metavar="N",
        help="Skip the first N papers in the queue (for manual batching)",
    )
    parser.add_argument(
        "--ids", nargs="+", metavar="ID",
        help="Convert only these specific paper IDs",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="Re-extract papers that are already DONE",
    )
    parser.add_argument(
        "--retry-failed", action="store_true",
        help="Process only FAILED papers (skip PENDING and DONE)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print the queue and exit without converting anything",
    )
    parser.add_argument(
        "--status", action="store_true",
        help="Print DONE/FAILED/PENDING counts and exit",
    )
    args = parser.parse_args()

    if args.status:
        _print_status()
        return

    queue = _load_queue(
        ids_filter=args.ids,
        force=args.force,
        retry_failed_only=args.retry_failed,
    )

    # offset and limit applied after state filtering, in sorted ID order
    if args.offset:
        queue = queue[args.offset:]
    if args.limit:
        queue = queue[: args.limit]

    if not queue:
        print("Nothing to convert.")
        return

    if args.dry_run:
        print(f"Queue: {len(queue)} papers")
        for p in queue:
            print(f"  [{p['state']:>7}] {p['id']}")
        return

    total = len(queue)
    print(f"Papers to convert : {total}")
    print(f"Workers           : {args.workers}")
    mode = "force" if args.force else "retry-failed" if args.retry_failed else "normal (PENDING + FAILED)"
    print(f"Mode              : {mode}")
    print(f"Log               : {BATCH_LOG}")
    print()

    print("Building corpus index…", flush=True)
    corpus_index = build_corpus_index(RAW_METADATA)
    print(f"  {len(corpus_index.get('arxiv', {}))} arXiv  +  {len(corpus_index.get('doi', {}))} DOI entries")
    print()

    t_start      = time.monotonic()
    done_count   = 0
    failed_count = 0
    skipped_count = 0

    # ------------------------------------------------------------------
    # Single-worker: plain sequential loop (no multiprocessing overhead)
    # ------------------------------------------------------------------
    if args.workers == 1:
        stop = False

        def _handle_sigint(sig, frame):
            nonlocal stop
            print("\nInterrupted — finishing current paper then stopping…", flush=True)
            stop = True

        signal.signal(signal.SIGINT, _handle_sigint)

        print("Loading Docling model (first paper takes ~30s)…", flush=True)
        converter = _make_converter()
        print()

        for i, paper in enumerate(queue, 1):
            if stop:
                break

            paper_id   = paper["id"]
            output_dir = RAW_PARSED / paper_id

            print(f"[{i:>4}/{total}] {paper_id:<45}", end="  ", flush=True)

            result = convert_paper(
                paper_id=paper_id,
                pdf_path=paper["pdf_path"],
                output_dir=output_dir,
                force=args.force,
                corpus_index=corpus_index,
                converter=converter,
            )

            if result.skipped:
                skipped_count += 1
                print("skipped (already done)", flush=True)
            elif result.success:
                done_count += 1
                print(f"done  ({result.elapsed_s:.1f}s)", flush=True)
            else:
                failed_count += 1
                print(f"FAILED  {result.error_type}: {result.error_message}", flush=True)

            _append_log({
                "ts":            datetime.now().isoformat(),
                "id":            paper_id,
                "success":       result.success,
                "skipped":       result.skipped,
                "elapsed_s":     round(result.elapsed_s, 2),
                "error_type":    result.error_type,
                "error_message": result.error_message,
            })

    # ------------------------------------------------------------------
    # Multi-worker: ProcessPoolExecutor
    # ------------------------------------------------------------------
    else:
        import threading
        stop_event = threading.Event()

        def _handle_sigint(sig, frame):
            print("\nInterrupted — waiting for in-flight papers to finish…", flush=True)
            stop_event.set()

        signal.signal(signal.SIGINT, _handle_sigint)

        with ProcessPoolExecutor(
            max_workers=args.workers,
            initializer=_worker_init,
            initargs=(corpus_index,),
        ) as executor:
            futures = {
                executor.submit(
                    _convert_worker,
                    paper["id"],
                    str(paper["pdf_path"]),
                    str(RAW_PARSED / paper["id"]),
                    args.force,
                ): paper["id"]
                for paper in queue
            }

            completed = 0
            for future in as_completed(futures):
                completed += 1
                paper_id = futures[future]

                try:
                    result = future.result()
                except Exception as exc:
                    failed_count += 1
                    print(f"[{completed:>4}/{total}] {paper_id:<45}  FAILED  {exc}", flush=True)
                    _append_log({
                        "ts":            datetime.now().isoformat(),
                        "id":            paper_id,
                        "success":       False,
                        "skipped":       False,
                        "elapsed_s":     0.0,
                        "error_type":    type(exc).__name__,
                        "error_message": str(exc),
                    })
                else:
                    if result.skipped:
                        skipped_count += 1
                        print(f"[{completed:>4}/{total}] {paper_id:<45}  skipped (already done)", flush=True)
                    elif result.success:
                        done_count += 1
                        print(f"[{completed:>4}/{total}] {paper_id:<45}  done  ({result.elapsed_s:.1f}s)", flush=True)
                    else:
                        failed_count += 1
                        print(f"[{completed:>4}/{total}] {paper_id:<45}  FAILED  {result.error_type}: {result.error_message}", flush=True)

                    _append_log({
                        "ts":            datetime.now().isoformat(),
                        "id":            paper_id,
                        "success":       result.success,
                        "skipped":       result.skipped,
                        "elapsed_s":     round(result.elapsed_s, 2),
                        "error_type":    result.error_type,
                        "error_message": result.error_message,
                    })

                if stop_event.is_set():
                    executor.shutdown(cancel_futures=True)
                    break

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    elapsed = time.monotonic() - t_start
    print()
    print("=" * 60)
    print(f"Done    : {done_count}")
    print(f"Failed  : {failed_count}")
    print(f"Skipped : {skipped_count}")
    print(f"Elapsed : {elapsed:.0f}s  ({elapsed / 60:.1f} min)")
    if failed_count:
        print()
        print(f"Re-run with --retry-failed to retry {failed_count} failed paper(s).")
    print(f"Log: {BATCH_LOG}")


if __name__ == "__main__":
    main()
