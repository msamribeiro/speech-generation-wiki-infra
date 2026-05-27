#!/usr/bin/env python3
"""
isca.py — Fetch Interspeech proceedings metadata from the ISCA archive.

Two-stage strategy:
  1. Scrape the proceedings index page to extract all paper slugs, titles, and authors.
  2. For papers passing the title-only keyword filter, fetch individual paper pages
     to retrieve abstracts and DOIs (polite: 2s between requests).

Output: one raw/metadata/{id}.json per passing paper, where id = interspeech-{year}-{seq}
        (seq extracted from DOI 10.21437/Interspeech.{year}-{seq}).

Usage:
    python scripts/fetch/isca.py
    python scripts/fetch/isca.py --year 2025
    python scripts/fetch/isca.py --year 2025 --dry-run
"""

import argparse
import json
import re
import sys
import time
from datetime import date
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from lib.keyword_filter import load_keyword_filter, _include_terms, passes_filter

# ---------------------------------------------------------------------------
# Paths and constants
# ---------------------------------------------------------------------------

RAW_METADATA = ROOT / "raw" / "metadata"
FETCH_LOG = ROOT / "raw" / "fetch_log.jsonl"

ISCA_BASE = "https://www.isca-archive.org"
RATE_LIMIT_SECONDS = 2.0
REQUEST_TIMEOUT = 30


# ---------------------------------------------------------------------------
# Title-only pre-filter (unique to ISCA two-stage strategy)
# ---------------------------------------------------------------------------

def passes_title_filter(title: str, kf: dict) -> bool:
    """Coarse pre-filter on title only, to avoid fetching every individual page."""
    include = _include_terms(kf)
    exclude = [t.lower() for t in kf["exclude"]]
    title_lower = title.lower()
    if any(t in title_lower for t in exclude):
        return False
    return sum(1 for t in include if t in title_lower) >= kf["title_min_matches"]


# ---------------------------------------------------------------------------
# HTTP helpers
# ---------------------------------------------------------------------------

def get_html(session: requests.Session, url: str) -> Optional[str]:
    """Fetch a URL and return its text, or None on failure."""
    try:
        resp = session.get(url, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.text
    except Exception as exc:
        print(f"  Fetch error for {url}: {exc}")
        return None


# ---------------------------------------------------------------------------
# Index scraper
# ---------------------------------------------------------------------------

def scrape_index(session: requests.Session, year: int) -> list[dict]:
    """
    Scrape the ISCA proceedings index and return a list of dicts:
      { slug, title, authors, paper_url, pdf_url }

    The index page lists papers as <a href="{slug}.html">Title\nAuthors\n</a>.
    """
    index_url = f"{ISCA_BASE}/interspeech_{year}/"
    print(f"Scraping index: {index_url}")
    html = get_html(session, index_url)
    if html is None:
        return []

    soup = BeautifulSoup(html, "html.parser")
    papers = []

    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        # Paper links match pattern: slug_interspeech.html (relative, no path separator)
        if not re.match(r"^[a-z0-9_]+_interspeech\.html$", href, re.IGNORECASE):
            continue

        text = a.get_text("\n", strip=True)
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        if len(lines) < 2:
            continue

        title = lines[0]
        authors_raw = " ".join(lines[1:])
        # Normalise whitespace in authors
        authors = re.sub(r"\s+", " ", authors_raw).strip()

        slug = href[: -len(".html")]
        paper_url = f"{ISCA_BASE}/interspeech_{year}/{href}"
        pdf_url = f"{ISCA_BASE}/interspeech_{year}/{slug}.pdf"

        papers.append(
            {
                "slug": slug,
                "title": title,
                "authors": authors,
                "paper_url": paper_url,
                "pdf_url": pdf_url,
            }
        )

    print(f"  Found {len(papers)} papers in index.")
    return papers


# ---------------------------------------------------------------------------
# Individual paper page scraper
# ---------------------------------------------------------------------------

def scrape_paper_page(session: requests.Session, paper: dict, year: int) -> dict:
    """
    Fetch the individual paper page and enrich the paper dict with:
      abstract, doi, isca_seq (sequence number from DOI), authors_list (list)
    Returns the same dict, modified in place.
    """
    html = get_html(session, paper["paper_url"])
    if html is None:
        paper["abstract"] = None
        paper["doi"] = None
        paper["isca_seq"] = None
        paper["authors_list"] = _split_authors(paper["authors"])
        return paper

    soup = BeautifulSoup(html, "html.parser")

    # Title: <h3>
    h3 = soup.find("h3")
    if h3:
        paper["title"] = h3.get_text(" ", strip=True)

    # Authors: <h5> immediately after <h3>
    h5 = soup.find("h5")
    if h5:
        paper["authors"] = h5.get_text(" ", strip=True)
    paper["authors_list"] = _split_authors(paper["authors"])

    # Abstract: inside <div id="abstract"><p>...</p></div>
    abstract = None
    abstract_div = soup.find("div", id="abstract")
    if abstract_div:
        p = abstract_div.find("p")
        if p:
            abstract = p.get_text(" ", strip=True)
    paper["abstract"] = abstract

    # DOI: scan all text for 10.21437/Interspeech.{year}-{seq}
    full_text = soup.get_text(" ")
    doi_match = re.search(
        rf"10\.21437/Interspeech\.{year}-(\d+)", full_text
    )
    if doi_match:
        paper["doi"] = f"10.21437/Interspeech.{year}-{doi_match.group(1)}"
        paper["isca_seq"] = int(doi_match.group(1))
    else:
        paper["doi"] = None
        paper["isca_seq"] = None

    return paper


def _split_authors(authors_str: str) -> list[str]:
    """Split 'First Last, First Last, ...' into a list."""
    return [a.strip() for a in authors_str.split(",") if a.strip()]


# ---------------------------------------------------------------------------
# Metadata builder
# ---------------------------------------------------------------------------

# Approximate conference dates per year
_CONF_DATES = {
    2024: "2024-09-01",
    2025: "2025-08-17",
}

_CONF_MONTHS = {
    2024: 9,
    2025: 8,
}


def build_metadata(paper: dict, year: int) -> dict:
    isca_id = f"interspeech-{year}-{paper['isca_seq']:04d}" if paper.get("isca_seq") else f"interspeech-{year}-{paper['slug']}"

    return {
        "id": isca_id,
        "source_ids": {
            "isca": paper["slug"],
            "doi": paper.get("doi"),
        },
        "title": paper["title"],
        "authors": paper["authors_list"][:10],
        "authors_full": paper["authors_list"] if len(paper["authors_list"]) > 10 else None,
        "organization": None,
        "venue": "Interspeech",
        "venue_type": "conference",
        "year": year,
        "month": _CONF_MONTHS.get(year, None),
        "published_date": _CONF_DATES.get(year, f"{year}-01-01"),
        "ingested_date": None,
        "url": paper["paper_url"],
        "pdf_url": paper["pdf_url"],
        "pdf_path": None,
        "pdf_source": "isca",
        "abstract": paper.get("abstract"),
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

def fetch_isca(year: int, dry_run: bool = False) -> dict:
    RAW_METADATA.mkdir(parents=True, exist_ok=True)
    kf = load_keyword_filter()

    session = requests.Session()
    session.headers["User-Agent"] = "speech-generation-wiki/1.0 (research use)"

    print(f"Year   : {year}")
    print(f"Dry run: {dry_run}")
    print()

    # Stage 1: scrape index
    papers = scrape_index(session, year)
    if not papers:
        print("No papers found in index — aborting.")
        return {}

    # Stage 2: title pre-filter
    title_candidates = [p for p in papers if passes_title_filter(p["title"], kf)]
    print(f"  {len(title_candidates)}/{len(papers)} papers pass title filter → fetching individual pages...")
    print()

    discovered = len(papers)
    after_filter = written = skipped = 0
    errors: list[str] = []
    needs_manual_pdf = 0

    for i, paper in enumerate(title_candidates):
        slug = paper["slug"]
        print(f"  [{i+1}/{len(title_candidates)}] {slug}")

        # Check for existing file before fetching the page
        # We don't know the final ID yet (need DOI), so check by slug
        existing = list(RAW_METADATA.glob(f"interspeech-{year}-*"))
        already_have = any(
            json.loads(f.read_text()).get("source_ids", {}).get("isca") == slug
            for f in existing
            if f.suffix == ".json"
        )
        if already_have:
            print(f"    already fetched — skipping")
            skipped += 1
            after_filter += 1
            time.sleep(0.1)
            continue

        time.sleep(RATE_LIMIT_SECONDS)
        paper = scrape_paper_page(session, paper, year)

        abstract = paper.get("abstract") or ""
        if not passes_filter(paper["title"], abstract, kf):
            print(f"    filtered out (abstract check)")
            continue

        after_filter += 1
        metadata = build_metadata(paper, year)

        out_path = RAW_METADATA / f"{metadata['id']}.json"
        if out_path.exists():
            print(f"    {metadata['id']} already exists — skipping")
            skipped += 1
            continue

        print(f"    + {metadata['id']}: {paper['title'][:72]}")
        if not dry_run:
            out_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))
        written += 1

    # Log
    log_entry = {
        "timestamp": f"{date.today().isoformat()}T00:00:00Z",
        "source": "isca",
        "venue": f"Interspeech {year}",
        "query": f"interspeech_{year} index scrape + individual page fetch",
        "discovered": discovered,
        "after_keyword_filter": after_filter,
        "written": written,
        "skipped_existing": skipped,
        "errors": errors,
        "needs_manual_pdf_count": needs_manual_pdf,
    }

    if not dry_run:
        with open(FETCH_LOG, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    prefix = "[DRY RUN] " if dry_run else ""
    print()
    print(f"{prefix}Done.")
    print(f"  Discovered (index)    : {discovered}")
    print(f"  Passed keyword filter : {after_filter}")
    print(f"  Written               : {written}")
    print(f"  Skipped existing      : {skipped}")
    print(f"  Errors                : {len(errors)}")

    return log_entry


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--year",
        type=int,
        default=2025,
        help="Interspeech year (default: 2025)",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Scrape and filter but do not write any files",
    )
    args = p.parse_args()
    fetch_isca(year=args.year, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
