#!/usr/bin/env python3
"""
openreview.py — Fetch conference proceedings metadata via the OpenReview API v2.

Supports ICLR and NeurIPS (both have used OpenReview since 2023). Fetches only
accepted papers, identified by content.venueid matching the conference. Applies
the standard keyword filter.

ID scheme: {venue-slug}-{year}-{forum_id}  (e.g. iclr-2025-VX8TLEKBNm)
  — stable, unique, traces directly to openreview.net/forum?id={forum_id}.
arXiv IDs are extracted best-effort from paper metadata and stored in
source_ids.arxiv. Conference IDs are canonical; arXiv versions are
duplicates if already in the corpus (handled by the post-fetch dedup pass).

Usage:
    python scripts/fetch/openreview.py --venue ICLR --year 2025
    python scripts/fetch/openreview.py --venue NeurIPS --year 2025
    python scripts/fetch/openreview.py --venue ICLR --years 2025 2026
    python scripts/fetch/openreview.py --venue ICLR --year 2025 --dry-run
"""

import argparse
import json
import re
import sys
import time
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from lib.keyword_filter import load_keyword_filter, passes_filter

# ---------------------------------------------------------------------------
# Paths and constants
# ---------------------------------------------------------------------------

RAW_METADATA = ROOT / "raw" / "metadata"
FETCH_LOG = ROOT / "raw" / "fetch_log.jsonl"

OR_API_BASE = "https://api2.openreview.net"
RATE_LIMIT_SECONDS = 1.0
MAX_RETRIES = 5
RETRY_BASE_SECONDS = 10
PAGE_SIZE = 1000

ARXIV_ID_RE = re.compile(
    r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?", re.IGNORECASE
)

# ---------------------------------------------------------------------------
# Venue configuration
# ---------------------------------------------------------------------------

# CLI name / alias → canonical form used in table keys below
_VENUE_ALIASES: Dict[str, str] = {
    "iclr":    "ICLR",
    "neurips": "NeurIPS",
    "nips":    "NeurIPS",
}

# (canonical_name, year) → (id_slug, openreview_venue_id, conf_date, conf_month)
#   id_slug    : prefix for our paper IDs, e.g. "iclr"
#   venue_id   : content.venueid value on OpenReview for accepted papers
#   conf_date  : conference start date (YYYY-MM-DD); used as published_date
#   conf_month : numeric month
_VENUE_TABLE: Dict[Tuple[str, int], Tuple[str, str, str, int]] = {
    ("ICLR",    2025): ("iclr",    "ICLR.cc/2025/Conference",   "2025-04-24", 4),
    ("ICLR",    2026): ("iclr",    "ICLR.cc/2026/Conference",   "2026-04-27", 4),
    ("NeurIPS", 2025): ("neurips", "NeurIPS.cc/2025/Conference", "2025-12-10", 12),
}

# Controlled vocabulary venue names (CLAUDE.md schema)
_VENUE_CV: Dict[str, str] = {
    "ICLR":    "ICLR",
    "NeurIPS": "NeurIPS",
}


def normalize_venue(name: str) -> str:
    return _VENUE_ALIASES.get(name.lower(), name)


def get_venue_config(venue: str, year: int) -> Tuple[str, str, str, int]:
    key = (normalize_venue(venue), year)
    if key not in _VENUE_TABLE:
        known = ", ".join(f"{v} {y}" for v, y in sorted(_VENUE_TABLE))
        raise ValueError(f"Unsupported venue/year: {venue} {year}. Known: {known}")
    return _VENUE_TABLE[key]


# ---------------------------------------------------------------------------
# OpenReview API layer
# ---------------------------------------------------------------------------

def or_get(session: requests.Session, path: str, params: dict) -> Optional[dict]:
    """Single OpenReview API GET with retry on 429 / 5xx."""
    url = OR_API_BASE + path
    for attempt in range(MAX_RETRIES):
        wait = RETRY_BASE_SECONDS * (2 ** attempt)
        try:
            resp = session.get(url, params=params, timeout=60)
            if resp.status_code in (429, 500, 502, 503, 504):
                print(f"  HTTP {resp.status_code} — waiting {wait}s (attempt {attempt + 1}/{MAX_RETRIES})...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as exc:
            print(f"  Request error: {exc} — waiting {wait}s...")
            time.sleep(wait)
    return None


def fetch_all_notes(session: requests.Session, venue_id: str) -> List[dict]:
    """
    Page through the OpenReview API and return all accepted notes for venue_id.
    Accepted papers are those whose content.venueid exactly matches venue_id —
    withdrawn and desk-rejected submissions use a different venueid value.
    """
    notes: List[dict] = []
    offset = 0
    total: Optional[int] = None

    while True:
        params = {
            "content.venueid": venue_id,
            "offset": offset,
            "limit": PAGE_SIZE,
            "sort": "cdate:asc",
        }
        data = or_get(session, "/notes", params)
        if data is None:
            print(f"  Failed to fetch page at offset {offset} — stopping early.")
            break

        page_notes = data.get("notes", [])
        if total is None:
            total = data.get("count", 0)

        notes.extend(page_notes)
        print(f"  offset={offset}: {len(page_notes)} notes (total={total}, fetched={len(notes)})")

        if not page_notes or len(notes) >= (total or 0):
            break

        offset += PAGE_SIZE
        time.sleep(RATE_LIMIT_SECONDS)

    return notes


# ---------------------------------------------------------------------------
# arXiv ID extraction
# ---------------------------------------------------------------------------

def extract_arxiv_id(note: dict) -> Optional[str]:
    """
    Scan URL-bearing content fields for an arXiv link and return the bare ID
    (e.g. "2503.12345"). Returns None if not found. Best-effort only.
    """
    content = note.get("content", {})
    for field in ("html", "code", "data", "video", "website", "supplementary_material"):
        val = content.get(field, {})
        if isinstance(val, dict):
            val = val.get("value", "")
        if isinstance(val, str):
            m = ARXIV_ID_RE.search(val)
            if m:
                return m.group(1)
    return None


# ---------------------------------------------------------------------------
# Note parser and metadata builder
# ---------------------------------------------------------------------------

def _cv(note: dict, field: str, default=None):
    """Read content.{field}.value from an OpenReview note dict."""
    return note.get("content", {}).get(field, {}).get("value", default)


def parse_note(note: dict) -> Optional[dict]:
    """
    Parse one raw OpenReview note into an intermediate paper dict.
    Returns None if the note is missing required fields.
    """
    forum_id = note.get("forum") or note.get("id")
    if not forum_id:
        return None

    title = _cv(note, "title")
    if not title:
        return None
    title = str(title).replace("\n", " ").strip()

    abstract = _cv(note, "abstract") or ""
    abstract = str(abstract).replace("\n", " ").strip()

    authors = _cv(note, "authors") or []
    if isinstance(authors, str):
        authors = [a.strip() for a in authors.split(",") if a.strip()]

    return {
        "forum_id": forum_id,
        "title": title,
        "abstract": abstract,
        "authors": list(authors),
        "arxiv_id": extract_arxiv_id(note),
    }


def build_metadata(
    paper: dict,
    venue: str,
    year: int,
    slug: str,
    conf_date: str,
    conf_month: int,
) -> dict:
    forum_id = paper["forum_id"]
    paper_id = f"{slug}-{year}-{forum_id}"

    source_ids: dict = {"openreview": forum_id}
    if paper.get("arxiv_id"):
        source_ids["arxiv"] = paper["arxiv_id"]

    authors = paper["authors"]

    return {
        "id": paper_id,
        "source_ids": source_ids,
        "title": paper["title"],
        "authors": authors[:10],
        "authors_full": authors if len(authors) > 10 else None,
        "organization": None,
        "venue": _VENUE_CV[normalize_venue(venue)],
        "venue_type": "conference",
        "year": year,
        "month": conf_month,
        "published_date": conf_date,
        "ingested_date": None,
        "url": f"https://openreview.net/forum?id={forum_id}",
        "pdf_url": f"https://openreview.net/pdf?id={forum_id}",
        "pdf_path": None,
        "pdf_source": "openreview",
        "abstract": paper["abstract"] or None,
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
# Main fetcher
# ---------------------------------------------------------------------------

def fetch_openreview(venue: str, year: int, dry_run: bool = False) -> dict:
    RAW_METADATA.mkdir(parents=True, exist_ok=True)
    kf = load_keyword_filter()

    slug, venue_id, conf_date, conf_month = get_venue_config(venue, year)
    venue_cv = _VENUE_CV[normalize_venue(venue)]

    print(f"Venue    : {venue_cv} {year}")
    print(f"OR ID    : {venue_id}")
    print(f"Dry run  : {dry_run}")
    print()

    session = requests.Session()
    session.headers["User-Agent"] = "speech-generation-wiki/1.0 (research use)"

    print("Fetching accepted papers from OpenReview...")
    notes = fetch_all_notes(session, venue_id)
    print(f"  Total returned: {len(notes)}")
    print()

    discovered = len(notes)
    after_filter = written = skipped = 0
    errors: List[str] = []

    for note in notes:
        paper = parse_note(note)
        if paper is None:
            continue

        if not passes_filter(paper["title"], paper["abstract"], kf):
            continue

        after_filter += 1
        metadata = build_metadata(paper, venue, year, slug, conf_date, conf_month)
        out_path = RAW_METADATA / f"{metadata['id']}.json"

        if out_path.exists():
            skipped += 1
            continue

        print(f"  + {metadata['id']}: {paper['title'][:72]}")
        if paper.get("arxiv_id"):
            print(f"      arXiv: {paper['arxiv_id']}")

        if not dry_run:
            out_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))
        written += 1

    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": "openreview",
        "venue": f"{venue_cv} {year}",
        "query": f"content.venueid={venue_id}",
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

    return log_entry


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--venue",
        required=True,
        help="Conference name: ICLR, NeurIPS",
    )
    year_group = p.add_mutually_exclusive_group(required=True)
    year_group.add_argument(
        "--year",
        type=int,
        help="Single year to fetch",
    )
    year_group.add_argument(
        "--years",
        type=int,
        nargs="+",
        help="One or more years to fetch sequentially",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and filter but do not write any files",
    )
    args = p.parse_args()

    years = args.years if args.years else [args.year]
    for year in years:
        fetch_openreview(venue=args.venue, year=year, dry_run=args.dry_run)
        if len(years) > 1:
            print()


if __name__ == "__main__":
    main()
