"""Metadata module for the Pipeline Health Suite.

Validates the paper-date rule on raw/metadata/*.json (docs/schemas/metadata.md, "Paper Dates"):
published_date must equal conference_date when set, then journal_date, then version_date (date of the arXiv version fetched), otherwise preprint_date; year and month must
match published_date. A claim-membership-proven frozen record may retain an older canonical date.
Non-ingested records must be fully migrated (error). Ingested records are legacy until their pages
are migrated: missing date fields are counted, and rule violations are reported as warnings.
"""

import json
import sys
from pathlib import Path

from checks._base import CheckArgs, Issue, ModuleResult

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from lib.paper_dates import canonical_published_date, valid_iso_date  # noqa: E402
from lib.peer_reviewed_versions import load_frozen_memberships  # noqa: E402

METADATA_DIR = ROOT / "raw" / "metadata"
STRICT_STATUSES = {"pending", "review", "accepted"}


def _check(
    pid: str,
    record: dict,
    severity: str,
    legacy_ok: bool = False,
    frozen_concepts: list[str] | None = None,
) -> list[Issue]:
    def issue(check: str, message: str) -> Issue:
        return Issue(severity, "metadata", pid, check, message)

    issues: list[Issue] = []
    pd = record.get("published_date")
    if not valid_iso_date(pd):
        return [issue("published_date_valid", f"published_date missing or invalid: {pd!r}")]
    if record.get("journal_date") is not None and not valid_iso_date(record["journal_date"]):
        issues.append(issue("date_fields_valid", f"journal_date invalid: {record['journal_date']!r}"))
    for key in ("preprint_date", "conference_date"):
        if key not in record:
            if legacy_ok:
                continue
            issues.append(issue("date_fields_present", f"{key} field missing"))
        elif record[key] is not None and not valid_iso_date(record[key]):
            issues.append(issue("date_fields_valid", f"{key} invalid: {record[key]!r}"))
    expected = canonical_published_date(record)
    frozen = bool(frozen_concepts)
    if expected is not None and pd != expected and not frozen:
        issues.append(issue(
            "published_date_rule",
            f"published_date {pd} != {next(k for k in ('conference_date', 'journal_date', 'version_date', 'preprint_date') if record.get(k))} {expected}",
        ))
    peer_url = record.get("url_peer_reviewed")
    if peer_url and not (isinstance(peer_url, str) and peer_url.startswith(("https://", "http://"))):
        issues.append(issue("url_peer_reviewed_valid", f"invalid peer-reviewed URL: {peer_url!r}"))
    if peer_url and not (valid_iso_date(record.get("conference_date")) or valid_iso_date(record.get("journal_date"))):
        issues.append(issue(
            "peer_reviewed_date_present",
            "url_peer_reviewed is set but no valid conference_date or journal_date is present",
        ))
    if peer_url and frozen:
        if not record.get("peer_reviewed_venue"):
            issues.append(issue(
                "peer_reviewed_venue_present",
                "frozen record has url_peer_reviewed but no peer_reviewed_venue",
            ))
        if record.get("peer_reviewed_venue_type") not in {"conference", "journal", "workshop"}:
            issues.append(issue(
                "peer_reviewed_venue_type_valid",
                "frozen record has url_peer_reviewed but no valid peer_reviewed_venue_type",
            ))
    preprint_url = record.get("url_preprint")
    if preprint_url and not (isinstance(preprint_url, str) and preprint_url.startswith("https://arxiv.org/abs/")):
        issues.append(issue("url_preprint_valid", f"url_preprint must be an arXiv abstract URL: {preprint_url!r}"))
    if record.get("pdf_path_preprint") and record.get("pdf_path_preprint") == record.get("pdf_path"):
        issues.append(issue("pdf_path_preprint_distinct", "pdf_path_preprint equals pdf_path"))
    if record.get("year") != int(pd[:4]) or record.get("month") != int(pd[5:7]):
        issues.append(issue("year_month_match", f"year/month {record.get('year')}/{record.get('month')} do not match published_date {pd}"))
    if not legacy_ok and (record.get("source_ids") or {}).get("arxiv"):
        if not record.get("preprint_date"):
            issues.append(issue("preprint_date_present", "record has an arXiv ID but no preprint_date"))
        if not record.get("version_date"):
            issues.append(issue("version_date_present", "record has an arXiv ID but no version_date"))
    vd, pre = record.get("version_date"), record.get("preprint_date")
    if vd is not None and not valid_iso_date(vd):
        issues.append(issue("date_fields_valid", f"version_date invalid: {vd!r}"))
    elif vd and pre and vd < pre:
        issues.append(issue("version_after_v1", f"version_date {vd} precedes preprint_date {pre}"))
    return issues


def run(args: CheckArgs) -> ModuleResult:
    issues: list[Issue] = []
    checked = legacy = 0
    wiki_dir = args.wiki_dir if args.wiki_dir else ROOT / "wiki"
    frozen = load_frozen_memberships(wiki_dir) if (wiki_dir / "_claims").exists() else {}
    for path in sorted(METADATA_DIR.glob("*.json")):
        pid = path.stem
        if args.paper_id and pid != args.paper_id:
            continue
        record = json.loads(path.read_text())
        status = record.get("status")
        if status in STRICT_STATUSES:
            checked += 1
            issues.extend(_check(pid, record, "error", frozen_concepts=frozen.get(pid)))
        elif status == "ingested":
            checked += 1
            if "preprint_date" not in record:
                legacy += 1
            issues.extend(
                _check(
                    pid,
                    record,
                    "warning",
                    legacy_ok=True,
                    frozen_concepts=frozen.get(pid),
                )
            )
    errors = sum(1 for i in issues if i.severity == "error")
    return ModuleResult(
        module="metadata",
        passed=errors == 0,
        issues=issues,
        stats={
            "errors": errors,
            "warnings": len(issues) - errors,
            "records_checked": checked,
            "legacy_ingested_unmigrated": legacy,
        },
    )
