#!/usr/bin/env python3
"""
arxiv.py — Fetch and keyword-filter arXiv preprints for the speech-generation-wiki.

Queries the arXiv API for cs.SD and eess.AS papers submitted within a date
window, applies the keyword filter from config/keyword_filter.yaml, and writes
one raw/metadata/{arxiv_id}.json per passing paper.

Can also fetch specific papers by arXiv ID (bypasses keyword filter — use for
targeted corpus expansion, e.g. highly-cited papers from citation discovery).

Usage:
    python scripts/fetch/arxiv.py
    python scripts/fetch/arxiv.py --date-from 2025-08-01
    python scripts/fetch/arxiv.py --date-from 2025-08-01 --date-to 2026-01-01
    python scripts/fetch/arxiv.py --dry-run
    python scripts/fetch/arxiv.py --ids 2407.05407 2301.02111 2412.10117
"""

import argparse
import json
import re
import sys
import time
from datetime import date, datetime
from pathlib import Path

import feedparser
import requests

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from lib.keyword_filter import load_keyword_filter, passes_filter

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

RAW_METADATA = ROOT / "raw" / "metadata"
FETCH_LOG = ROOT / "raw" / "fetch_log.jsonl"

ARXIV_API_URL = "https://export.arxiv.org/api/query"
BATCH_SIZE = 100
RATE_LIMIT_SECONDS = 3.0


# ---------------------------------------------------------------------------
# arXiv helpers
# ---------------------------------------------------------------------------

def build_query(categories: list[str], date_from: str, date_to: str) -> str:
    cat_part = " OR ".join(f"cat:{c}" for c in categories)
    d_from = date_from.replace("-", "") + "000000"
    d_to = date_to.replace("-", "") + "235959"
    return f"({cat_part}) AND submittedDate:[{d_from} TO {d_to}]"


def arxiv_id_from_url(url: str) -> str:
    # URL is like http://arxiv.org/abs/2501.12345v2
    m = re.search(r"abs/([^v\s/]+?)(?:v\d+)?$", url)
    return m.group(1) if m else url.rstrip("/").split("/")[-1]


def build_metadata(entry, arxiv_id: str) -> dict:
    # feedparser exposes published_parsed as a time.struct_time in UTC
    tp = entry.get("published_parsed")
    if tp:
        published_date = f"{tp.tm_year}-{tp.tm_mon:02d}-{tp.tm_mday:02d}"
        year, month = tp.tm_year, tp.tm_mon
    else:
        published_date, year, month = None, None, None

    authors_all = [a["name"] for a in entry.get("authors", [])]
    authors = authors_all[:10]

    return {
        "id": arxiv_id,
        "source_ids": {"arxiv": arxiv_id},
        "title": entry.title.replace("\n", " ").strip(),
        "authors": authors,
        "authors_full": authors_all if len(authors_all) > 10 else None,
        "organization": None,
        "venue": "arXiv",
        "venue_type": "preprint",
        "year": year,
        "month": month,
        "published_date": published_date,
        "ingested_date": None,
        "url": f"https://arxiv.org/abs/{arxiv_id}",
        "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
        "pdf_path": None,
        "pdf_source": "arxiv",
        "abstract": entry.get("summary", "").replace("\n", " ").strip(),
        "arxiv_comment": getattr(entry, "arxiv_comment", None),
        "task": [],
        "relevance_score": None,
        "relevance_note": None,
        "status": "pending",
        "fetched_date": date.today().isoformat(),
        "needs_manual_pdf": False,
        "is_duplicate": False,
        "canonical_id": None,
    }


# ---------------------------------------------------------------------------
# Fetcher
# ---------------------------------------------------------------------------

def fetch_arxiv(
    categories: list[str],
    date_from: str,
    date_to: str,
    dry_run: bool = False,
) -> dict:
    RAW_METADATA.mkdir(parents=True, exist_ok=True)

    kf = load_keyword_filter()
    query = build_query(categories, date_from, date_to)

    print(f"Query  : {query}")
    print(f"Window : {date_from} → {date_to}")
    print(f"Dry run: {dry_run}")
    print()

    session = requests.Session()
    session.headers["User-Agent"] = "speech-generation-wiki/1.0"

    discovered = after_filter = written = skipped = 0
    errors: list[str] = []
    start = 0

    while True:
        print(f"Fetching records {start}–{start + BATCH_SIZE - 1}...")
        feed = None
        for attempt in range(5):
            wait = 30 * (2 ** attempt)  # 30s, 60s, 120s, 240s, 480s
            try:
                resp = session.get(
                    ARXIV_API_URL,
                    params={
                        "search_query": query,
                        "start": start,
                        "max_results": BATCH_SIZE,
                        "sortBy": "submittedDate",
                        "sortOrder": "ascending",
                    },
                    timeout=60,
                )
                resp.raise_for_status()
                feed = feedparser.parse(resp.text)
                break
            except requests.exceptions.HTTPError as exc:
                code = exc.response.status_code if exc.response is not None else 0
                if code in (429, 500, 502, 503, 504):
                    print(f"  HTTP {code} — waiting {wait}s before retry {attempt + 1}/5...")
                    time.sleep(wait)
                else:
                    errors.append(str(exc))
                    print(f"  HTTP error: {exc}")
                    break
            except Exception as exc:
                print(f"  Request error (attempt {attempt + 1}/5): {exc} — waiting {wait}s...")
                time.sleep(wait)
        if feed is None:
            errors.append(f"Failed to fetch batch starting at {start} after retries")
            print(f"  Giving up on batch {start}.")
            break

        entries = feed.entries
        if not entries:
            print("  No entries returned — done.")
            break

        try:
            total = int(feed.feed.opensearch_totalresults)
        except AttributeError:
            total = start + len(entries)

        discovered += len(entries)

        for entry in entries:
            try:
                arxiv_id = arxiv_id_from_url(entry.id)
                title = entry.title.replace("\n", " ").strip()
                abstract = entry.get("summary", "").replace("\n", " ").strip()

                if not passes_filter(title, abstract, kf):
                    continue

                after_filter += 1
                out_path = RAW_METADATA / f"{arxiv_id}.json"

                if out_path.exists():
                    skipped += 1
                    continue

                metadata = build_metadata(entry, arxiv_id)
                if not dry_run:
                    out_path.write_text(
                        json.dumps(metadata, indent=2, ensure_ascii=False)
                    )
                written += 1
                print(f"  + {arxiv_id}: {title[:72]}")

            except Exception as exc:
                msg = f"{getattr(entry, 'id', '?')}: {exc}"
                errors.append(msg)
                print(f"  Parse error: {msg}")

        start += len(entries)
        if start >= total:
            break

        print(f"  Progress: {start}/{total} fetched, {after_filter} passed filter so far")
        time.sleep(RATE_LIMIT_SECONDS)

    # Summary
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": "arxiv",
        "venue": None,
        "query": query,
        "discovered": discovered,
        "after_keyword_filter": after_filter,
        "written": written,
        "skipped_existing": skipped,
        "errors": errors,
        "needs_manual_pdf_count": 0,
    }

    if not dry_run:
        with open(FETCH_LOG, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    prefix = "[DRY RUN] " if dry_run else ""
    print()
    print(f"{prefix}Done.")
    print(f"  Discovered       : {discovered}")
    print(f"  Passed filter    : {after_filter}")
    print(f"  Written          : {written}")
    print(f"  Skipped existing : {skipped}")
    print(f"  Errors           : {len(errors)}")
    if errors:
        for e in errors[:5]:
            print(f"    {e}")

    return log_entry


# ---------------------------------------------------------------------------
# Targeted fetch by ID
# ---------------------------------------------------------------------------

def fetch_by_ids(ids: list[str], dry_run: bool = False) -> dict:
    """Fetch specific arXiv papers by ID, bypassing the keyword filter."""
    RAW_METADATA.mkdir(parents=True, exist_ok=True)

    # Normalise IDs (strip version suffix if present, e.g. 2407.05407v2)
    ids = [re.sub(r"v\d+$", "", i.strip()) for i in ids]

    print(f"Fetching {len(ids)} specific IDs: {', '.join(ids)}")
    print(f"Dry run: {dry_run}")
    print()

    session = requests.Session()
    session.headers["User-Agent"] = "speech-generation-wiki/1.0"

    written = skipped = 0
    errors: list[str] = []

    # arXiv API handles id_list queries in one request for reasonable counts;
    # chunk into batches of 50 to stay well within API limits.
    CHUNK = 50
    fetched_entries: list = []
    for i in range(0, len(ids), CHUNK):
        chunk = ids[i : i + CHUNK]
        for attempt in range(5):
            wait = 30 * (2 ** attempt)
            try:
                resp = session.get(
                    ARXIV_API_URL,
                    params={"id_list": ",".join(chunk), "max_results": len(chunk)},
                    timeout=60,
                )
                resp.raise_for_status()
                feed = feedparser.parse(resp.text)
                fetched_entries.extend(feed.entries)
                break
            except requests.exceptions.HTTPError as exc:
                code = exc.response.status_code if exc.response is not None else 0
                if code in (429, 500, 502, 503, 504):
                    print(f"  HTTP {code} — waiting {wait}s before retry {attempt + 1}/5...")
                    time.sleep(wait)
                else:
                    errors.append(str(exc))
                    print(f"  HTTP error: {exc}")
                    break
            except Exception as exc:
                print(f"  Request error (attempt {attempt + 1}/5): {exc} — waiting {wait}s...")
                time.sleep(wait)
        if i + CHUNK < len(ids):
            time.sleep(RATE_LIMIT_SECONDS)

    for entry in fetched_entries:
        try:
            arxiv_id = arxiv_id_from_url(entry.id)
            title = entry.title.replace("\n", " ").strip()
            out_path = RAW_METADATA / f"{arxiv_id}.json"

            if out_path.exists():
                skipped += 1
                print(f"  ~ {arxiv_id}: already exists — skipped")
                continue

            metadata = build_metadata(entry, arxiv_id)
            if not dry_run:
                out_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))
            written += 1
            print(f"  + {arxiv_id}: {title[:72]}")

        except Exception as exc:
            msg = f"{getattr(entry, 'id', '?')}: {exc}"
            errors.append(msg)
            print(f"  Parse error: {msg}")

    # Warn about any requested IDs that came back with no entry
    returned_ids = {arxiv_id_from_url(e.id) for e in fetched_entries}
    for rid in ids:
        if rid not in returned_ids:
            errors.append(f"{rid}: not found in arXiv response")
            print(f"  ! {rid}: not returned by arXiv (withdrawn or invalid?)")

    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": "arxiv-ids",
        "ids_requested": ids,
        "written": written,
        "skipped_existing": skipped,
        "errors": errors,
    }

    if not dry_run:
        with open(FETCH_LOG, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    prefix = "[DRY RUN] " if dry_run else ""
    print()
    print(f"{prefix}Done.")
    print(f"  Requested        : {len(ids)}")
    print(f"  Written          : {written}")
    print(f"  Skipped existing : {skipped}")
    print(f"  Errors           : {len(errors)}")
    if errors:
        for e in errors[:5]:
            print(f"    {e}")

    return log_entry


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--ids",
        nargs="+",
        metavar="ARXIV_ID",
        help="Fetch specific arXiv IDs (bypasses keyword filter and date window)",
    )
    p.add_argument(
        "--date-from",
        default="2025-08-01",
        help="Start of submission window, YYYY-MM-DD (default: 2025-08-01)",
    )
    p.add_argument(
        "--date-to",
        default=date.today().isoformat(),
        help="End of submission window, YYYY-MM-DD (default: today)",
    )
    p.add_argument(
        "--categories",
        nargs="+",
        default=["cs.SD", "eess.AS"],
        help="arXiv categories to query (default: cs.SD eess.AS)",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and filter but do not write any files",
    )
    args = p.parse_args()

    if args.ids:
        fetch_by_ids(ids=args.ids, dry_run=args.dry_run)
    else:
        fetch_arxiv(
            categories=args.categories,
            date_from=args.date_from,
            date_to=args.date_to,
            dry_run=args.dry_run,
        )


if __name__ == "__main__":
    main()
