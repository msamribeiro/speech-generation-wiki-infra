#!/usr/bin/env python3
"""Apply the canonical paper-date rule to raw/metadata/*.json.

Rule (docs/schemas/metadata.md, "Paper Dates"):
  published_date = conference_date if the paper appeared in peer-reviewed proceedings,
                   else journal_date if it appeared in a peer-reviewed journal,
                   else version_date (date of the arXiv version we fetched/ingested),
                   otherwise preprint_date (arXiv v1).

Scope: records with status accepted, review, or pending are rewritten. Ingested records are
never written: their wiki pages and claim YAML copy published_date, so they are only reported.
Rejected records are ignored.

arXiv version history comes from the OAI arXivRaw format (one request per ID, cached). The version
of a record not yet pinned at download time is estimated: the latest version submitted on or
before the local PDF's modification date, else `fetched_date`. Estimated records carry
`version_estimated: true`; `scripts/parse/download_pdfs.py` re-pins them (`false`) on download.

Usage:
    python scripts/apply_date_rule.py                  # dry run: print planned changes
    python scripts/apply_date_rule.py --apply          # write changes + pipeline_log entry
    python scripts/apply_date_rule.py --report-ingested  # list ingested records that deviate
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from collections import Counter
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from lib.arxiv_versions import fetch_versions, pin_version  # noqa: E402
from lib.paper_dates import apply_date_rule, canonical_published_date, valid_iso_date  # noqa: E402
from scripts.fetch.acl import _CONF_META  # noqa: E402

METADATA_DIR = ROOT / "raw" / "metadata"
PIPELINE_LOG = ROOT / "raw" / "pipeline_log.md"
WRITE_STATUSES = {"accepted", "review", "pending"}
REPORT_STATUSES = {"ingested"}
PROCEEDINGS_TYPES = {"conference", "workshop"}
VERSION_CACHE = Path("/tmp/arxiv_versions_cache.json")
ARXIV_ID_RE = re.compile(r"^(\d{4}\.\d{4,5}|[a-z\-]+/\d{7})$")


def resolve_versions(arxiv_ids: list[str]) -> dict[str, list[tuple[int, str]]]:
    """Map arXiv ID -> [(version, date)], from the OAI arXivRaw format (cached on disk)."""
    cache: dict[str, list] = json.loads(VERSION_CACHE.read_text()) if VERSION_CACHE.exists() else {}
    todo = [i for i in arxiv_ids if i not in cache]
    for n, aid in enumerate(todo, 1):
        cache[aid] = fetch_versions(aid)
        if n % 25 == 0:
            VERSION_CACHE.write_text(json.dumps(cache))
            print(f"  fetched versions {n}/{len(todo)}", flush=True)
        time.sleep(1.5)
    VERSION_CACHE.write_text(json.dumps(cache))
    return {i: [tuple(v) for v in cache[i]] for i in arxiv_ids}


def download_date(record: dict) -> str | None:
    """Best estimate of when the content version was obtained: PDF mtime, else fetched_date."""
    pdf = ROOT / "raw" / "papers" / f"{record['id']}.pdf"
    if pdf.exists():
        return datetime.fromtimestamp(pdf.stat().st_mtime).date().isoformat()
    fetched = record.get("fetched_date")
    return fetched if valid_iso_date(fetched) else None


def plan_record(record: dict, versions: dict[str, list[tuple[int, str]]]) -> tuple[dict, list[str]]:
    """Return (updated copy, notes). Notes flag records the rule could not fully resolve."""
    new = dict(record)
    notes: list[str] = []
    src = record.get("source_ids") or {}
    arxiv_id = src.get("arxiv")
    old_pd = record.get("published_date")

    preprint = record.get("preprint_date")
    if arxiv_id:
        vers = versions.get(arxiv_id)
        if vers:
            pinned = record.get("version_estimated") is False and record.get("version_date")
            if pinned:
                new["preprint_date"] = vers[0][1]
            else:
                pin_version(new, vers, download_date(record), estimated=True)
            preprint = new["preprint_date"]
        elif not valid_iso_date(preprint):
            notes.append(f"arXiv version history unavailable for {arxiv_id}")
    new["preprint_date"] = preprint if valid_iso_date(preprint) else None

    conference = record.get("conference_date")
    if not valid_iso_date(conference):
        conference = None
        if record.get("venue_type") in PROCEEDINGS_TYPES:
            # Records created from a proceedings source (OpenReview, ISCA, Anthology; their IDs
            # are not arXiv IDs) already carry the proceedings date in published_date.
            # Records created from an arXiv ID carry the preprint date.
            if not ARXIV_ID_RE.match(str(record.get("id"))) and valid_iso_date(old_pd):
                conference = old_pd
            else:
                notes.append("proceedings venue but conference date unknown; defaulting to preprint date")
    # Anthology volume months carry a day-01 placeholder; upgrade to the curated exact date
    # when the venue table has one for that month.
    if conference and conference.endswith("-01"):
        meta = _CONF_META.get((record.get("venue"), int(conference[:4])))
        if meta and meta["date"][:7] == conference[:7]:
            conference = meta["date"]
    new["conference_date"] = conference
    if "journal_date" in record:
        new["journal_date"] = record["journal_date"] if valid_iso_date(record["journal_date"]) else None

    if canonical_published_date(new) is None and valid_iso_date(old_pd):
        # No preprint and no proceedings date resolved: keep the existing value.
        notes.append("no preprint or conference date; published_date left unchanged")
    else:
        apply_date_rule(new)
    return new, notes


DATE_KEYS = ("preprint_date", "arxiv_version", "version_date", "version_estimated", "conference_date", "journal_date")


def ordered(record: dict) -> dict:
    """Place the supporting date fields directly after published_date."""
    out: dict = {}
    for key, value in record.items():
        if key in DATE_KEYS:
            continue
        out[key] = value
        if key == "published_date":
            for k in DATE_KEYS:
                if k in record or k in ("preprint_date", "conference_date"):
                    out[k] = record.get(k)
    if "published_date" not in record:
        for k in DATE_KEYS:
            if k in record or k in ("preprint_date", "conference_date"):
                out[k] = record.get(k)
    return out


def quarter(value: str | None) -> str:
    if not valid_iso_date(value):
        return "unknown"
    return f"{value[:4]}-Q{(int(value[5:7]) - 1) // 3 + 1}"


def load(statuses: set[str], ingested_from: str | None = None) -> dict[str, tuple[Path, dict, bool]]:
    """Load records by status. With `ingested_from`, only ingested records whose current
    published_date is on or after that date are loaded; dedup pointers (`wiki_page_id`) are skipped
    because their page belongs to the canonical record."""
    records = {}
    for path in sorted(METADATA_DIR.glob("*.json")):
        text = path.read_text()
        record = json.loads(text)
        if record.get("status") not in statuses:
            continue
        if ingested_from and (record.get("wiki_page_id") or (record.get("published_date") or "") < ingested_from):
            continue
        records[path.stem] = (path, record, text.endswith("\n"))
    return records


def update_page(wiki_dir: Path, pid: str, new: dict) -> bool:
    """Sync published_date/year/month in the paper page frontmatter. Returns True if changed."""
    page = wiki_dir / "papers" / f"{pid}.md"
    if not page.exists():
        return False
    text = page.read_text()
    head, sep, body = text.partition("\n---\n")
    for key in ("published_date", "year", "month"):
        match = re.search(rf"^{key}: *(.*)$", head, flags=re.M)
        if not match:
            continue
        value = str(new[key])
        if key == "published_date" and match.group(1).startswith('"'):
            value = f'"{value}"'  # keep the page's existing quoting style
        head = head[:match.start()] + f"{key}: {value}" + head[match.end():]
    updated = head + sep + body
    if updated == text:
        return False
    page.write_text(updated)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true", help="Write changes to non-ingested metadata records")
    parser.add_argument("--report-ingested", action="store_true", help="Report (never write) ingested records that deviate")
    parser.add_argument(
        "--ingested-from", metavar="YYYY-MM-DD",
        help="Migrate ingested records published on/after this date: metadata plus paper-page frontmatter "
             "(earlier ingested records stay as-is). Combine with --apply to write.",
    )
    args = parser.parse_args()

    statuses = REPORT_STATUSES if (args.report_ingested or args.ingested_from) else WRITE_STATUSES
    records = load(statuses, args.ingested_from)
    arxiv_ids = sorted({r["source_ids"]["arxiv"] for _, r, _ in records.values() if (r.get("source_ids") or {}).get("arxiv")})
    print(f"{len(records)} records in scope ({', '.join(sorted(statuses))}); resolving {len(arxiv_ids)} arXiv version histories")
    versions = resolve_versions(arxiv_ids)

    changed: list[tuple[str, dict, dict, list[str]]] = []
    flagged: list[tuple[str, list[str]]] = []
    for pid, (path, record, _) in records.items():
        new, notes = plan_record(record, versions)
        new = ordered(new)
        if notes:
            flagged.append((pid, notes))
        if new != ordered(dict(record)) or any(k not in record for k in ("preprint_date", "conference_date")):
            changed.append((pid, record, new, notes))

    moved = Counter()
    for pid, old, new, _ in changed:
        if old.get("published_date") != new.get("published_date"):
            moved[(quarter(old.get("published_date")), quarter(new.get("published_date")))] += 1
    date_changes = [c for c in changed if c[1].get("published_date") != c[2].get("published_date")]

    print(f"{len(changed)} records change ({len(date_changes)} change published_date)")
    for (old_q, new_q), n in sorted(moved.items()):
        print(f"  {old_q} -> {new_q}: {n}")
    for pid, old, new, _ in date_changes:
        print(f"  {pid:<28} {old.get('published_date')} -> {new.get('published_date')}"
              f"  (v1={new.get('preprint_date')}, version=v{new.get('arxiv_version')} {new.get('version_date')}, conference={new.get('conference_date')})")
    for pid, notes in flagged:
        for note in notes:
            print(f"  NOTE {pid}: {note}")

    if args.report_ingested or (args.ingested_from and not args.apply) or not args.apply:
        if args.report_ingested:
            print("Ingested records are never written by this script.")
        else:
            print("Dry run; pass --apply to write.")
        return

    wiki_dir = None
    if args.ingested_from:
        import subprocess
        wiki_dir = Path(subprocess.check_output([sys.executable, str(ROOT / "scripts" / "resolve_wiki_dir.py")], text=True).strip())
    pages_updated = 0
    for pid, _, new, _ in changed:
        path, _, trailing_newline = records[pid]
        path.write_text(json.dumps(new, indent=2, ensure_ascii=False) + ("\n" if trailing_newline else ""))
    if wiki_dir:
        for pid, (_, record, _) in records.items():
            new, _ = plan_record(record, versions)
            if update_page(wiki_dir, pid, ordered(new)):
                pages_updated += 1

    scope = f"ingested records from {args.ingested_from} ({pages_updated} pages synced)" if args.ingested_from else "non-ingested records"
    quarter_summary = "; ".join(f"{a}->{b}: {n}" for (a, b), n in sorted(moved.items())) or "none"
    entry = (
        f"- metadata | paper-date rule | {len(changed)} {scope} ({len(date_changes)} published_date changes) | "
        f"added preprint_date (arXiv v1), arxiv_version/version_date (version fetched) and conference_date; published_date = conference_date, else journal_date, else version_date, else preprint_date | "
        f"quarter moves: {quarter_summary} | {"other" if args.ingested_from else "ingested and rejected"} records untouched | {date.today().isoformat()}\n"
    )
    log_text = PIPELINE_LOG.read_text()
    heading = f"## {date.today().isoformat()}\n"
    if log_text.startswith(heading):
        log_text = heading + "\n" + entry + log_text[len(heading):].lstrip("\n")
    else:
        log_text = heading + "\n" + entry + "\n" + log_text
    PIPELINE_LOG.write_text(log_text)
    print(f"Wrote {len(changed)} records and appended to {PIPELINE_LOG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
