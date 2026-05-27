#!/usr/bin/env python3
"""
download_pdfs.py — Download PDFs for all accepted papers in the corpus.

Reads raw/metadata/*.json, downloads pdf_url for each accepted paper that
doesn't already have a local file, and writes pdf_path back to the JSON.

Resumable: re-running skips any paper whose PDF already exists on disk.

Usage:
    python scripts/parse/download_pdfs.py
    python scripts/parse/download_pdfs.py --max-errors 3
    python scripts/parse/download_pdfs.py --source arxiv
    python scripts/parse/download_pdfs.py --limit 10 --dry-run
"""

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urlparse

import requests
from typing import Optional

ROOT = Path(__file__).parent.parent.parent

RAW_METADATA = ROOT / "raw" / "metadata"
RAW_PAPERS   = ROOT / "raw" / "papers"
DOWNLOAD_LOG = ROOT / "raw" / "download_log.jsonl"

# ---------------------------------------------------------------------------
# Per-domain rate limits (seconds between successive requests)
# ---------------------------------------------------------------------------

DOMAIN_DELAY: dict[str, float] = {
    "arxiv.org":         3.0,
    "isca-archive.org":  1.0,
    "aclanthology.org":  1.0,
}
DEFAULT_DELAY = 2.0

# Retry schedule for transient errors (seconds to wait before attempt 1, 2, 3)
RETRY_BACKOFF = [15, 45, 90]
MAX_RETRIES   = len(RETRY_BACKOFF)

# Minimum plausible PDF size — smaller files are treated as error pages
MIN_PDF_BYTES = 10_240  # 10 KB


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_domain(url: str) -> str:
    host = urlparse(url).netloc.lower()
    for known in DOMAIN_DELAY:
        if host.endswith(known):
            return known
    return host


def load_accepted(metadata_dir: Path, source_filter: Optional[str]) -> list[dict]:
    papers = []
    for f in sorted(metadata_dir.glob("*.json")):
        try:
            d = json.loads(f.read_text())
        except json.JSONDecodeError:
            print(f"  [warn] Cannot parse {f.name} — skipping")
            continue
        if d.get("status") != "accepted":
            continue
        if not d.get("pdf_url"):
            continue
        if source_filter and d.get("pdf_source") != source_filter:
            continue
        d["_meta_path"] = f
        papers.append(d)
    return papers


def append_log(record: dict) -> None:
    with DOWNLOAD_LOG.open("a") as fh:
        fh.write(json.dumps(record) + "\n")


def update_pdf_path(meta_path: Path, paper_id: str) -> None:
    data = json.loads(meta_path.read_text())
    data["pdf_path"] = f"raw/papers/{paper_id}.pdf"
    meta_path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Download (single paper, with retries)
# ---------------------------------------------------------------------------

def download_pdf(
    session:      requests.Session,
    url:          str,
    dest:         Path,
    last_request: dict[str, float],
    dry_run:      bool,
) -> tuple[bool, str]:
    """
    Download *url* to *dest*, respecting per-domain rate limits.

    Returns (success, error_description).
    Retries on transient failures (5xx, connection errors, 429).
    Does NOT retry on permanent 4xx errors (except 429).
    """
    domain = get_domain(url)
    delay  = DOMAIN_DELAY.get(domain, DEFAULT_DELAY)

    # Enforce rate limit before every attempt
    since_last = time.monotonic() - last_request.get(domain, 0.0)
    if since_last < delay:
        time.sleep(delay - since_last)

    if dry_run:
        last_request[domain] = time.monotonic()
        return True, ""

    for attempt in range(MAX_RETRIES + 1):
        # Re-enforce rate limit on retries (we slept above, but retries need it too)
        if attempt > 0:
            since_last = time.monotonic() - last_request.get(domain, 0.0)
            if since_last < delay:
                time.sleep(delay - since_last)

        try:
            resp = session.get(url, stream=True, timeout=60)
        except requests.RequestException as exc:
            last_request[domain] = time.monotonic()
            if attempt < MAX_RETRIES:
                wait = RETRY_BACKOFF[attempt]
                print(f"\n      connection error: {exc}; retrying in {wait}s…", flush=True)
                time.sleep(wait)
                continue
            return False, f"connection error: {exc}"

        last_request[domain] = time.monotonic()

        if resp.status_code == 200:
            dest.parent.mkdir(parents=True, exist_ok=True)
            tmp = dest.with_suffix(".tmp")
            try:
                with tmp.open("wb") as fh:
                    for chunk in resp.iter_content(chunk_size=65_536):
                        fh.write(chunk)
                size = tmp.stat().st_size
                if size < MIN_PDF_BYTES:
                    tmp.unlink()
                    return False, f"file too small ({size} B) — likely an error page"
                tmp.replace(dest)
                return True, ""
            except OSError as exc:
                tmp.unlink(missing_ok=True)
                return False, f"write error: {exc}"

        elif resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", RETRY_BACKOFF[min(attempt, MAX_RETRIES - 1)]))
            if attempt < MAX_RETRIES:
                print(f"\n      429 rate limited; waiting {retry_after}s…", flush=True)
                time.sleep(retry_after)
                continue
            return False, "429 rate limited — exhausted retries"

        elif resp.status_code >= 500:
            if attempt < MAX_RETRIES:
                wait = RETRY_BACKOFF[attempt]
                print(f"\n      {resp.status_code} server error; retrying in {wait}s…", flush=True)
                time.sleep(wait)
                continue
            return False, f"server error {resp.status_code} after {MAX_RETRIES} retries"

        else:
            # Permanent 4xx — do not retry
            return False, f"HTTP {resp.status_code}"

    return False, "max retries exceeded"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--max-errors", type=int, default=5, metavar="N",
        help="Abort after N consecutive download failures (default: 5)",
    )
    parser.add_argument(
        "--source", choices=["arxiv", "isca", "anthology"],
        help="Only download papers from this source",
    )
    parser.add_argument(
        "--limit", type=int, metavar="N",
        help="Stop after downloading N papers (useful for testing)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Simulate downloads without writing files or updating metadata",
    )
    args = parser.parse_args()

    # ------------------------------------------------------------------
    # Load and partition
    # ------------------------------------------------------------------
    all_papers = load_accepted(RAW_METADATA, args.source)

    pending:  list[dict] = []
    skipped:  list[str]  = []
    stale:    list[dict] = []  # file exists but pdf_path not set in JSON

    for p in all_papers:
        dest = RAW_PAPERS / f"{p['id']}.pdf"
        if dest.exists() and dest.stat().st_size >= MIN_PDF_BYTES:
            if p.get("pdf_path"):
                skipped.append(p["id"])
            else:
                stale.append(p)   # file downloaded but metadata not updated
        else:
            pending.append(p)

    if args.limit:
        pending = pending[: args.limit]

    print(f"Accepted papers : {len(all_papers)}" + (f"  (source={args.source})" if args.source else ""))
    print(f"Already done    : {len(skipped)}")
    print(f"Stale metadata  : {len(stale)}  (file exists, pdf_path missing — will fix)")
    print(f"To download     : {len(pending)}" + (f"  (capped at {args.limit})" if args.limit else ""))
    print(f"Consecutive err : abort after {args.max_errors}")
    if args.dry_run:
        print("DRY RUN — no files will be written")
    print()

    # ------------------------------------------------------------------
    # Fix stale metadata (file exists but pdf_path not recorded)
    # ------------------------------------------------------------------
    for p in stale:
        pid = p["id"]
        if not args.dry_run:
            update_pdf_path(p["_meta_path"], pid)
        print(f"  [fix] {pid} — pdf_path updated")

    if not pending:
        print("Nothing to download.")
        return

    # ------------------------------------------------------------------
    # Download loop
    # ------------------------------------------------------------------
    session = requests.Session()
    session.headers["User-Agent"] = (
        "speech-generation-wiki/1.0 "
        "(academic research; mailto:msam.web@outlook.com)"
    )

    last_request: dict = {}
    consecutive_errors = 0
    success_count      = 0
    failures:          list[dict]       = []

    total = len(pending)
    for i, paper in enumerate(pending, 1):
        pid     = paper["id"]
        url     = paper["pdf_url"]
        dest    = RAW_PAPERS / f"{pid}.pdf"
        meta    = paper["_meta_path"]
        source  = paper.get("pdf_source", "?")

        print(f"[{i:>4}/{total}] [{source:>10}] {pid}", end="  ", flush=True)

        ok, err = download_pdf(session, url, dest, last_request, args.dry_run)

        if ok:
            consecutive_errors = 0
            success_count += 1
            size_kb = dest.stat().st_size // 1024 if dest.exists() else 0
            print(f"✓  {size_kb} KB", flush=True)
            if not args.dry_run:
                update_pdf_path(meta, pid)
                append_log({
                    "ts":      datetime.now().isoformat(),
                    "id":      pid,
                    "source":  source,
                    "status":  "ok",
                    "size_kb": size_kb,
                })
        else:
            consecutive_errors += 1
            failures.append({"id": pid, "source": source, "url": url, "error": err})
            print(f"✗  {err}", flush=True)
            if not args.dry_run:
                append_log({
                    "ts":     datetime.now().isoformat(),
                    "id":     pid,
                    "source": source,
                    "status": "error",
                    "error":  err,
                })

            if consecutive_errors >= args.max_errors:
                print()
                print(f"FAILSAFE: {consecutive_errors} consecutive failures — aborting early.")
                print(f"Last error : {err}")
                print(f"Last paper : {pid}  ({url})")
                print(f"Re-run to resume from where this stopped.")
                print(f"Log        : {DOWNLOAD_LOG}")
                break

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print()
    print("=" * 60)
    print(f"Downloaded   : {success_count}")
    print(f"Failed       : {len(failures)}")
    print(f"Remaining    : {total - success_count - len(failures)}")

    if failures:
        print()
        print("Failed papers:")
        for f in failures:
            print(f"  [{f['source']}] {f['id']}: {f['error']}")
        print()
        print(f"Full log: {DOWNLOAD_LOG}")


if __name__ == "__main__":
    main()
