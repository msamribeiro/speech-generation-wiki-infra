#!/usr/bin/env python3
"""
acl.py — Fetch ACL Anthology proceedings metadata for the speech-generation-wiki.

Data source: per-venue XML files from the ACL Anthology GitHub repository.
  https://raw.githubusercontent.com/acl-org/acl-anthology/master/data/xml/{year}.{venue}.xml

The old bulk JSON (anthology+abstracts.json.gz) no longer exists; this fetcher
uses the current XML-based data model.

Scope:
  - Main proceedings: ACL, EMNLP, NAACL
  - Findings: findings (combined across all venues in one XML per year)
  - Workshops: all co-located workshops when --all-workshops is set.
    Workshop XMLs are discovered via the GitHub contents API and downloaded
    only if they exist. The keyword filter handles relevance.

Venues are processed in this order so that August+ conferences appear first
in the output: EMNLP (Nov), findings, ACL (Jul), NAACL (Apr), then workshops.

arXiv deduplication — prefer peer-reviewed version:
  A title-index is built from existing raw/metadata/ records. When an Anthology
  paper's normalised title matches an existing record, that record is enriched
  in place: venue, venue_type, doi, and pdf_url (camera-ready) are updated.
  The existing canonical ID (typically an arXiv ID) is preserved.
  Records with status='ingested' are left untouched; a warning is printed.

XML files are cached in raw/anthology_xml_cache/ and only re-downloaded if
older than CACHE_MAX_AGE_DAYS days.

Usage:
    python scripts/fetch/acl.py                      # 2025, main + findings
    python scripts/fetch/acl.py --all-workshops      # also fetch all co-located workshops
    python scripts/fetch/acl.py --years 2024 2025
    python scripts/fetch/acl.py --dry-run
    python scripts/fetch/acl.py --no-cache
"""

import argparse
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Iterator, List, Optional, Tuple

import requests

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from lib.keyword_filter import load_keyword_filter, passes_filter

# ---------------------------------------------------------------------------
# Paths and constants
# ---------------------------------------------------------------------------

RAW_METADATA = ROOT / "raw" / "metadata"
FETCH_LOG = ROOT / "raw" / "fetch_log.jsonl"
XML_CACHE_DIR = ROOT / "raw" / "anthology_xml_cache"

ANTHOLOGY_RAW = (
    "https://raw.githubusercontent.com/acl-org/acl-anthology/master/data/xml"
)
ANTHOLOGY_BASE = "https://aclanthology.org"
GITHUB_CONTENTS_API = (
    "https://api.github.com/repos/acl-org/acl-anthology/contents/data/xml"
)

CACHE_MAX_AGE_DAYS = 7
RATE_LIMIT_SECONDS = 0.5   # between XML downloads

# Main venue XML stems, per year. The findings XML covers all venues together.
MAIN_VENUE_STEMS = ["acl", "emnlp", "naacl", "findings"]

# Processing order: EMNLP (Nov) before ACL (Jul) before NAACL (Apr),
# so August+ conferences appear first in output.
VENUE_ORDER = ["emnlp", "findings", "acl", "naacl"]

# Maps (canonical_venue, year) → conference metadata
_CONF_META: Dict[Tuple[str, int], Dict] = {
    ("ACL",   2024): {"date": "2024-08-11", "month": 8},
    ("ACL",   2025): {"date": "2025-07-27", "month": 7},
    ("EMNLP", 2024): {"date": "2024-11-12", "month": 11},
    ("EMNLP", 2025): {"date": "2025-11-05", "month": 11},
    ("NAACL", 2024): {"date": "2024-06-16", "month": 6},
    ("NAACL", 2025): {"date": "2025-04-29", "month": 4},
}

# ---------------------------------------------------------------------------
# XML download and caching
# ---------------------------------------------------------------------------

def get_xml(
    session: requests.Session,
    xml_stem: str,
    no_cache: bool = False,
) -> Optional[str]:
    """
    Fetch an Anthology XML file, using a local cache if fresh.
    Returns XML text or None on 404 / error.
    """
    cache = XML_CACHE_DIR / f"{xml_stem}.xml"

    if not no_cache and cache.exists():
        age_days = (date.today() - date.fromtimestamp(cache.stat().st_mtime)).days
        if age_days < CACHE_MAX_AGE_DAYS:
            return cache.read_text(encoding="utf-8")

    url = f"{ANTHOLOGY_RAW}/{xml_stem}.xml"
    try:
        resp = session.get(url, timeout=30)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        XML_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cache.write_text(resp.text, encoding="utf-8")
        return resp.text
    except Exception as exc:
        print(f"  Error fetching {xml_stem}.xml: {exc}")
        return None


def discover_workshop_slugs(
    session: requests.Session,
    years: List[int],
) -> List[str]:
    """
    Find all workshop XML stems for the target years via the GitHub git-tree API.
    Uses the tree SHA for data/xml/ in a single request rather than paginating
    through the contents API (which hits rate limits at ~60 pages).
    Returns a list of full xml_stems like ['2025.sigdial', '2025.dstc', ...].
    """
    print("Discovering workshop XML files from GitHub...")
    year_strs = {str(y) for y in years}
    main_stems = {f"{y}.{v}" for y in years for v in MAIN_VENUE_STEMS}

    # Step 1: get the tree SHA for data/xml/
    try:
        resp = session.get(
            "https://api.github.com/repos/acl-org/acl-anthology/contents/data",
            timeout=30,
        )
        resp.raise_for_status()
        xml_sha = next(
            (e["sha"] for e in resp.json() if e.get("name") == "xml"),
            None,
        )
    except Exception as exc:
        print(f"  Could not get data/ tree: {exc}")
        return []

    if not xml_sha:
        print("  Could not locate data/xml/ SHA.")
        return []

    # Step 2: fetch the full tree for data/xml/ in one call
    try:
        resp = session.get(
            f"https://api.github.com/repos/acl-org/acl-anthology/git/trees/{xml_sha}",
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        print(f"  Could not fetch data/xml/ tree: {exc}")
        return []

    if data.get("truncated"):
        print("  WARNING: GitHub tree response truncated — some workshops may be missing.")

    found: List[str] = []
    for entry in data.get("tree", []):
        name = entry.get("path", "")
        if not name.endswith(".xml"):
            continue
        stem = name[:-4]
        year_str = stem.split(".")[0]
        if year_str in year_strs and stem not in main_stems:
            found.append(stem)

    print(f"  Found {len(found)} workshop file(s) for years {years}.")
    return sorted(found)


# ---------------------------------------------------------------------------
# XML parsing
# ---------------------------------------------------------------------------

def strip_inline_tags(text: Optional[str]) -> str:
    """Remove inline XML tags like <fixed-case>, <tex-math>, <url>."""
    if not text:
        return ""
    return re.sub(r"<[^>]+>", "", text).strip()


def elem_full_text(elem: ET.Element, tag: str) -> str:
    """Extract full text of a child element, including text across inline subelements."""
    child = elem.find(tag)
    if child is None:
        return ""
    parts = [child.text or ""]
    for sub in child:
        parts.append(sub.text or "")
        parts.append(sub.tail or "")
    return strip_inline_tags("".join(parts)).strip()


def parse_authors(paper: ET.Element) -> List[str]:
    authors = []
    for a in paper.findall("author"):
        first = (a.findtext("first") or "").strip()
        last = (a.findtext("last") or "").strip()
        name = f"{first} {last}".strip() if first else last
        if name:
            authors.append(name)
    return authors


def volume_to_canonical_venue(volume_id: str, collection_id: str) -> str:
    """
    Map a volume ID to an AGENTS.md canonical venue name.
    For 'findings' collections the volume ID encodes the parent venue
    (e.g. 'acl-2025', 'emnlp-2025', 'naacl-2025').
    """
    if "findings" in collection_id:
        if "naacl" in volume_id:
            return "NAACL"
        if "emnlp" in volume_id:
            return "EMNLP"
        return "ACL"  # ACL findings or unknown
    base = collection_id.split(".")[-1]  # e.g. 'acl', 'emnlp', 'naacl'
    return base.upper()


def iter_papers(
    xml_text: str,
    xml_stem: str,
    year: int,
    is_workshop: bool = False,
) -> Iterator[dict]:
    """
    Parse an Anthology XML file and yield one raw dict per paper.
    Skips entries with no title (frontmatter).
    """
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        print(f"  XML parse error in {xml_stem}: {exc}")
        return

    collection_id = root.get("id", xml_stem)  # e.g. "2025.acl"

    for volume in root.findall("volume"):
        volume_id = volume.get("id", "")  # e.g. "long", "main", "acl-2025"
        acl_volume = f"{collection_id}-{volume_id}"  # e.g. "2025.acl-long"

        if is_workshop:
            c_venue = "workshop"
            v_type = "workshop"
        else:
            c_venue = volume_to_canonical_venue(volume_id, collection_id)
            v_type = "conference"

        conf_meta = _CONF_META.get((c_venue, year), {})

        for paper in volume.findall("paper"):
            paper_id = paper.get("id", "")
            acl_id = f"{acl_volume}.{paper_id}"

            title = elem_full_text(paper, "title")
            if not title:
                continue

            abstract = elem_full_text(paper, "abstract")
            doi = (paper.findtext("doi") or "").strip()

            url_elem = paper.find("url")
            url_slug = (url_elem.text or acl_id).strip() if url_elem is not None else acl_id
            paper_url = f"{ANTHOLOGY_BASE}/{url_slug}"
            pdf_url = f"{ANTHOLOGY_BASE}/{url_slug}.pdf"

            yield {
                "acl_id": acl_id,
                "title": title,
                "abstract": abstract,
                "authors": parse_authors(paper),
                "doi": doi or None,
                "paper_url": paper_url,
                "pdf_url": pdf_url,
                "canonical_venue": c_venue,
                "venue_type": v_type,
                "year": year,
                "month": conf_meta.get("month"),
                "published_date": conf_meta.get("date", f"{year}-01-01"),
            }


# ---------------------------------------------------------------------------
# Title-based dedup index
# ---------------------------------------------------------------------------

def normalize_title(title: str) -> str:
    t = title.lower()
    t = re.sub(r"[^\w\s]", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def build_title_index(metadata_dir: Path) -> Dict[str, Path]:
    """Map normalised title → metadata file path for all existing records."""
    index: Dict[str, Path] = {}
    for path in metadata_dir.glob("*.json"):
        try:
            record = json.loads(path.read_text())
            norm = normalize_title(record.get("title", ""))
            if norm:
                index[norm] = path
        except Exception:
            pass
    return index


# ---------------------------------------------------------------------------
# Metadata builder
# ---------------------------------------------------------------------------

def build_metadata(paper: dict) -> dict:
    return {
        "id": paper["acl_id"],
        "source_ids": {
            "acl": paper["acl_id"],
            "arxiv": None,
            "doi": paper["doi"],
        },
        "title": paper["title"],
        "authors": paper["authors"][:10],
        "authors_full": paper["authors"] if len(paper["authors"]) > 10 else None,
        "organization": None,
        "venue": paper["canonical_venue"],
        "venue_type": paper["venue_type"],
        "year": paper["year"],
        "month": paper["month"],
        "published_date": paper["published_date"],
        "ingested_date": None,
        "url": paper["paper_url"],
        "pdf_url": paper["pdf_url"],
        "pdf_path": None,
        "pdf_source": "anthology",
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
# Enrich existing record with conference info (prefer peer-reviewed version)
# ---------------------------------------------------------------------------

def enrich_existing_record(path: Path, paper: dict) -> bool:
    """
    Update an existing metadata record in place with ACL conference info.
    Skips records with status='ingested'.
    Returns True if updated.
    """
    record = json.loads(path.read_text())

    if record.get("status") == "ingested":
        print(f"      WARN: {path.name} already ingested — skipping enrich (update wiki manually)")
        return False

    record["venue"] = paper["canonical_venue"]
    record["venue_type"] = paper["venue_type"]
    record["year"] = paper["year"]
    if paper.get("month"):
        record["month"] = paper["month"]
    # Preserve arXiv published_date; store conference date separately
    if paper.get("published_date"):
        record["conference_date"] = paper["published_date"]

    record.setdefault("source_ids", {})
    record["source_ids"]["acl"] = paper["acl_id"]
    if paper.get("doi"):
        record["source_ids"]["doi"] = paper["doi"]

    # Prefer camera-ready anthology PDF over preprint
    if paper.get("pdf_url"):
        record["pdf_url"] = paper["pdf_url"]
        record["pdf_source"] = "anthology"

    record["source_ids"]["url_acl"] = paper["paper_url"]
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False))
    return True


# ---------------------------------------------------------------------------
# Main fetcher
# ---------------------------------------------------------------------------

def fetch_acl(
    years: List[int],
    all_workshops: bool = False,
    dry_run: bool = False,
    no_cache: bool = False,
) -> dict:
    RAW_METADATA.mkdir(parents=True, exist_ok=True)
    kf = load_keyword_filter()

    print(f"Years         : {years}")
    print(f"All workshops : {all_workshops}")
    print(f"Dry run       : {dry_run}")
    print()

    session = requests.Session()
    session.headers["User-Agent"] = "speech-generation-wiki/1.0 (research use)"

    # Build ordered list of (xml_stem, year, is_workshop)
    # Main venues first in August+ priority order, then workshops
    targets: List[Tuple[str, int, bool]] = []
    for venue_stem in VENUE_ORDER:
        for year in years:
            targets.append((f"{year}.{venue_stem}", year, False))

    if all_workshops:
        workshop_stems = discover_workshop_slugs(session, years)
        for stem in workshop_stems:
            year = int(stem.split(".")[0])
            targets.append((stem, year, True))

    # Build title index for dedup against existing records
    print("Building title index from existing records...")
    title_index = build_title_index(RAW_METADATA)
    print(f"  {len(title_index)} existing records indexed.")
    print()

    discovered = after_filter = written = enriched = skipped = 0
    needs_manual_pdf = 0
    errors: List[str] = []
    last_was_workshop = False

    for xml_stem, year, is_workshop in targets:
        if is_workshop and not last_was_workshop:
            print("--- workshops ---")
        last_was_workshop = is_workshop

        time.sleep(RATE_LIMIT_SECONDS)
        xml_text = get_xml(session, xml_stem, no_cache)
        if xml_text is None:
            continue  # 404: this venue/year doesn't exist yet

        papers_in_file = 0
        matched_in_file = 0

        for paper in iter_papers(xml_text, xml_stem, year, is_workshop):
            discovered += 1
            papers_in_file += 1

            if not passes_filter(paper["title"], paper["abstract"] or "", kf):
                continue

            after_filter += 1
            matched_in_file += 1

            try:
                norm = normalize_title(paper["title"])
                existing_path = title_index.get(norm)

                if existing_path and existing_path.exists():
                    if not dry_run:
                        updated = enrich_existing_record(existing_path, paper)
                        if updated:
                            enriched += 1
                            print(f"  ~ [{xml_stem}] {existing_path.stem}: {paper['title'][:60]}")
                        else:
                            skipped += 1
                    else:
                        print(f"  ~ [DRY] [{xml_stem}] enrich {existing_path.stem}: {paper['title'][:55]}")
                        enriched += 1
                    continue

                # New paper not yet in metadata
                out_path = RAW_METADATA / f"{paper['acl_id']}.json"
                if out_path.exists():
                    skipped += 1
                    continue

                if not dry_run:
                    out_path.write_text(
                        json.dumps(build_metadata(paper), indent=2, ensure_ascii=False)
                    )
                    title_index[norm] = out_path  # prevent duplicates within same run
                written += 1
                print(f"  + [{xml_stem}] {paper['acl_id']}: {paper['title'][:60]}")

            except Exception as exc:
                msg = f"{paper['acl_id']}: {exc}"
                errors.append(msg)
                print(f"  ERROR: {msg}")

        if matched_in_file > 0 or not is_workshop:
            label = "workshop" if is_workshop else "venue"
            print(f"  {xml_stem}: {papers_in_file} papers, {matched_in_file} passed filter")

    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": "acl",
        "venue": f"ACL Anthology {years}",
        "query": f"years={years} all_workshops={all_workshops}",
        "discovered": discovered,
        "after_keyword_filter": after_filter,
        "written": written,
        "enriched_existing": enriched,
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
    print(f"  Discovered (total)      : {discovered}")
    print(f"  Passed keyword filter   : {after_filter}")
    print(f"  Written (new)           : {written}")
    print(f"  Enriched (arXiv→conf)   : {enriched}")
    print(f"  Skipped (already exist) : {skipped}")
    print(f"  Errors                  : {len(errors)}")

    return log_entry


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--years",
        nargs="+",
        type=int,
        default=[2025],
        help="Conference years to fetch (default: 2025)",
    )
    p.add_argument(
        "--all-workshops",
        action="store_true",
        help="Also fetch all co-located workshop XMLs (uses GitHub API to discover them)",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Filter and report but do not write any files",
    )
    p.add_argument(
        "--no-cache",
        action="store_true",
        help="Force re-download of all XML files",
    )
    args = p.parse_args()

    fetch_acl(
        years=args.years,
        all_workshops=args.all_workshops,
        dry_run=args.dry_run,
        no_cache=args.no_cache,
    )


if __name__ == "__main__":
    main()
