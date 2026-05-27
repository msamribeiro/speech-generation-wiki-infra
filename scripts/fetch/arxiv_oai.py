#!/usr/bin/env python3
"""
arxiv_oai.py — Harvest arXiv metadata via OAI-PMH for the speech-generation-wiki.

Uses the OAI-PMH bulk-harvest endpoint (export.arxiv.org/oai2), which is designed
for large category sweeps and has separate, more generous rate limits than the
search API. Pagination uses resumption tokens — no offset arithmetic, no large-
query timeouts. arXiv policy: ≥5 seconds between requests.

Usage:
    python scripts/fetch/arxiv_oai.py --set cs.CL --date-from 2025-12-01 --date-to 2026-02-28
    python scripts/fetch/arxiv_oai.py --set cs.CL --date-from 2026-03-01
    python scripts/fetch/arxiv_oai.py --set cs.CL --date-from 2025-12-01 --dry-run
    python scripts/fetch/arxiv_oai.py --set cs.CL --resume-token <token>  # resume interrupted run
"""

import argparse
import json
import sys
import time
import xml.etree.ElementTree as ET
from datetime import date, datetime
from pathlib import Path
from typing import List, Optional

import requests

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from lib.keyword_filter import load_keyword_filter, passes_filter

# ---------------------------------------------------------------------------
# Paths and constants
# ---------------------------------------------------------------------------

RAW_METADATA = ROOT / "raw" / "metadata"
FETCH_LOG = ROOT / "raw" / "fetch_log.jsonl"

OAI_BASE = "https://export.arxiv.org/oai2"
OAI_NS = "http://www.openarchives.org/OAI/2.0/"
ARXIV_NS = "http://arxiv.org/OAI/arXiv/"

RATE_LIMIT_SECONDS = 5.0   # arXiv OAI-PMH policy: minimum 5s between requests
MAX_RETRIES = 6            # retry attempts per request
RETRY_BASE_SECONDS = 30    # 30, 60, 120, 240, 480, 960


# OAI-PMH uses colon-separated hierarchy: cs.CL → cs:cs:CL, eess.AS → eess:eess:AS
def to_oai_set(s: str) -> str:
    """Convert familiar arXiv category notation (cs.CL) to OAI-PMH set identifier (cs:cs:CL)."""
    if "." in s:
        top, sub = s.split(".", 1)
        return f"{top}:{top}:{sub}"
    return s  # already in OAI format or top-level (e.g. "cs")


# ---------------------------------------------------------------------------
# OAI-PMH HTTP layer with retry
# ---------------------------------------------------------------------------

def oai_get(session: requests.Session, params: dict) -> Optional[ET.Element]:
    """
    Make one OAI-PMH request and return the parsed root element.
    Retries on 429 / 5xx with exponential backoff. Returns None on permanent failure.
    """
    for attempt in range(MAX_RETRIES):
        wait = RETRY_BASE_SECONDS * (2 ** attempt)
        try:
            resp = session.get(OAI_BASE, params=params, timeout=60)
            if resp.status_code in (429, 500, 502, 503, 504):
                print(f"  HTTP {resp.status_code} — waiting {wait}s (attempt {attempt + 1}/{MAX_RETRIES})...")
                time.sleep(wait)
                continue
            resp.raise_for_status()
            return ET.fromstring(resp.content)
        except ET.ParseError as exc:
            print(f"  XML parse error: {exc} — waiting {wait}s...")
            time.sleep(wait)
        except requests.RequestException as exc:
            print(f"  Request error: {exc} — waiting {wait}s...")
            time.sleep(wait)
    return None


# ---------------------------------------------------------------------------
# OAI-PMH record parser
# ---------------------------------------------------------------------------

def _text(elem: Optional[ET.Element]) -> str:
    if elem is None:
        return ""
    return (elem.text or "").strip()


def parse_authors(arxiv_elem: ET.Element) -> List[str]:
    authors = []
    authors_elem = arxiv_elem.find(f"{{{ARXIV_NS}}}authors")
    if authors_elem is None:
        return authors
    for author in authors_elem.findall(f"{{{ARXIV_NS}}}author"):
        keyname = _text(author.find(f"{{{ARXIV_NS}}}keyname"))
        forenames = _text(author.find(f"{{{ARXIV_NS}}}forenames"))
        name = f"{forenames} {keyname}".strip() if forenames else keyname
        if name:
            authors.append(name)
    return authors


def parse_record(record: ET.Element) -> Optional[dict]:
    """
    Parse one OAI-PMH <record> element into a raw paper dict.
    Returns None for deleted or malformed records.
    """
    header = record.find(f"{{{OAI_NS}}}header")
    if header is None:
        return None
    # Skip deleted records
    if header.get("status") == "deleted":
        return None

    identifier = _text(header.find(f"{{{OAI_NS}}}identifier"))
    # identifier is like "oai:arXiv.org:2512.00001"
    arxiv_id = identifier.split(":")[-1] if ":" in identifier else identifier
    datestamp = _text(header.find(f"{{{OAI_NS}}}datestamp"))

    metadata_elem = record.find(f"{{{OAI_NS}}}metadata")
    if metadata_elem is None:
        return None
    arxiv_elem = metadata_elem.find(f"{{{ARXIV_NS}}}arXiv")
    if arxiv_elem is None:
        return None

    title = _text(arxiv_elem.find(f"{{{ARXIV_NS}}}title")).replace("\n", " ")
    abstract = _text(arxiv_elem.find(f"{{{ARXIV_NS}}}abstract")).replace("\n", " ")
    categories = _text(arxiv_elem.find(f"{{{ARXIV_NS}}}categories"))
    created = _text(arxiv_elem.find(f"{{{ARXIV_NS}}}created"))  # YYYY-MM-DD
    comments = _text(arxiv_elem.find(f"{{{ARXIV_NS}}}comments")) or None

    authors = parse_authors(arxiv_elem)

    # Parse year/month from created date (fall back to datestamp)
    ref_date = created or datestamp
    try:
        dt = datetime.strptime(ref_date[:10], "%Y-%m-%d")
        year, month, published_date = dt.year, dt.month, ref_date[:10]
    except (ValueError, TypeError):
        year, month, published_date = None, None, None

    return {
        "arxiv_id": arxiv_id,
        "title": title,
        "abstract": abstract,
        "authors": authors,
        "categories": categories,
        "published_date": published_date,
        "year": year,
        "month": month,
        "arxiv_comment": comments,
    }


# ---------------------------------------------------------------------------
# Metadata builder (matches arxiv.py schema)
# ---------------------------------------------------------------------------

def build_metadata(paper: dict) -> dict:
    authors_all = paper["authors"]
    return {
        "id": paper["arxiv_id"],
        "source_ids": {"arxiv": paper["arxiv_id"]},
        "title": paper["title"],
        "authors": authors_all[:10],
        "authors_full": authors_all if len(authors_all) > 10 else None,
        "organization": None,
        "venue": "arXiv",
        "venue_type": "preprint",
        "year": paper["year"],
        "month": paper["month"],
        "published_date": paper["published_date"],
        "ingested_date": None,
        "url": f"https://arxiv.org/abs/{paper['arxiv_id']}",
        "pdf_url": f"https://arxiv.org/pdf/{paper['arxiv_id']}.pdf",
        "pdf_path": None,
        "pdf_source": "arxiv",
        "abstract": paper["abstract"] or None,
        "arxiv_comment": paper.get("arxiv_comment"),
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
# Main OAI-PMH harvester
# ---------------------------------------------------------------------------

def fetch_oai(
    oai_set: str,
    date_from: Optional[str],
    date_to: Optional[str],
    resume_token: Optional[str] = None,
    dry_run: bool = False,
) -> dict:
    RAW_METADATA.mkdir(parents=True, exist_ok=True)
    kf = load_keyword_filter()

    print(f"Set      : {oai_set}")
    print(f"Window   : {date_from or '(start)'} → {date_to or date.today().isoformat()}")
    print(f"Dry run  : {dry_run}")
    if resume_token:
        print(f"Resuming : {resume_token[:40]}...")
    print()

    session = requests.Session()
    session.headers["User-Agent"] = "speech-generation-wiki/1.0 (research bulk harvest)"

    discovered = after_filter = written = skipped = 0
    errors: List[str] = []
    page = 0
    total_size: Optional[int] = None

    # First request: either resume from token or start fresh
    if resume_token:
        params: dict = {"verb": "ListRecords", "resumptionToken": resume_token}
    else:
        params = {
            "verb": "ListRecords",
            "metadataPrefix": "arXiv",
            "set": oai_set,
        }
        if date_from:
            params["from"] = date_from
        if date_to:
            params["until"] = date_to

    while True:
        page += 1
        size_str = f"/{total_size}" if total_size else ""
        print(f"Page {page}{size_str} — fetching...")

        root = oai_get(session, params)
        if root is None:
            msg = f"Page {page}: failed after {MAX_RETRIES} retries"
            errors.append(msg)
            print(f"  Giving up. {msg}")
            print(f"  To resume, rerun with: --resume-token {params.get('resumptionToken', '(unavailable)')}")
            break

        # Check for OAI-PMH protocol errors
        error_elem = root.find(f"{{{OAI_NS}}}error")
        if error_elem is not None:
            code = error_elem.get("code", "unknown")
            msg_text = _text(error_elem)
            msg = f"OAI error [{code}]: {msg_text}"
            errors.append(msg)
            print(f"  {msg}")
            break

        list_records = root.find(f"{{{OAI_NS}}}ListRecords")
        if list_records is None:
            errors.append(f"Page {page}: no ListRecords element in response")
            break

        records = list_records.findall(f"{{{OAI_NS}}}record")
        page_discovered = len(records)
        discovered += page_discovered

        for record in records:
            paper = parse_record(record)
            if paper is None:
                continue

            if not passes_filter(paper["title"], paper["abstract"] or "", kf):
                continue

            after_filter += 1
            out_path = RAW_METADATA / f"{paper['arxiv_id']}.json"

            if out_path.exists():
                skipped += 1
                continue

            if not dry_run:
                out_path.write_text(
                    json.dumps(build_metadata(paper), indent=2, ensure_ascii=False)
                )
            written += 1
            print(f"  + {paper['arxiv_id']}: {paper['title'][:72]}")

        print(f"  Page {page}: {page_discovered} records, {after_filter} passed filter so far "
              f"({written} written, {skipped} skipped)")

        # Check resumption token
        token_elem = list_records.find(f"{{{OAI_NS}}}resumptionToken")
        if token_elem is None:
            # No token element at all — end of list
            break

        # Update total size if available
        if token_elem.get("completeListSize"):
            total_size = int(token_elem.get("completeListSize", 0))

        token_text = (token_elem.text or "").strip()
        if not token_text:
            # Empty token — end of list
            break

        # Pause before next request (arXiv OAI-PMH policy)
        time.sleep(RATE_LIMIT_SECONDS)
        params = {"verb": "ListRecords", "resumptionToken": token_text}

    # Log
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": "arxiv-oai",
        "venue": None,
        "query": f"set={oai_set} from={date_from} until={date_to}",
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
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--set",
        default="cs.CL",
        help="OAI-PMH set identifier, e.g. cs.CL, cs.SD, eess.AS (default: cs.CL)",
    )
    p.add_argument(
        "--date-from",
        default=None,
        help="Start of harvest window, YYYY-MM-DD (default: no lower bound)",
    )
    p.add_argument(
        "--date-to",
        default=None,
        help="End of harvest window, YYYY-MM-DD (default: today)",
    )
    p.add_argument(
        "--resume-token",
        default=None,
        help="OAI-PMH resumption token to continue an interrupted run",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch and filter but do not write any files",
    )
    args = p.parse_args()

    fetch_oai(
        oai_set=to_oai_set(args.set),
        date_from=args.date_from,
        date_to=args.date_to,
        resume_token=args.resume_token,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
