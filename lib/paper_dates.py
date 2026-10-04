"""Canonical paper-date rule shared by fetchers, migrations, and health checks.

Dates recorded in each metadata JSON (see docs/schemas/metadata.md, "Paper Dates"):

- ``preprint_date``   first public arXiv submission (v1), or null when there is no preprint
- ``conference_date`` date of the peer-reviewed proceedings the paper appeared in, or null
- ``journal_date``    optional; first online publication date in a peer-reviewed journal
- ``version_date``    date of the arXiv version whose content we fetched/ingested
                      (``arxiv_version``); equals ``preprint_date`` when that is v1
- ``published_date``  the canonical date the wiki follows: ``conference_date`` when set, then
                      ``journal_date``, then ``version_date``, otherwise ``preprint_date``

A preprint revision counts only as the version we actually ingested; later revisions we have not
fetched are never used.
"""

from __future__ import annotations

import re
from datetime import date

ISO_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def valid_iso_date(value: object) -> bool:
    if not isinstance(value, str) or not ISO_DATE_RE.match(value):
        return False
    try:
        date.fromisoformat(value)
    except ValueError:
        return False
    return True


def canonical_published_date(record: dict) -> str | None:
    """Return the date `published_date` must hold for this record, or None if unresolvable."""
    for key in ("conference_date", "journal_date", "version_date", "preprint_date"):
        value = record.get(key)
        if valid_iso_date(value):
            return value
    return None


def apply_date_rule(record: dict) -> bool:
    """Set `published_date`, `year`, and `month` from the rule. Returns True if anything changed."""
    target = canonical_published_date(record)
    if target is None:
        return False
    changed = False
    for key, value in (
        ("published_date", target),
        ("year", int(target[:4])),
        ("month", int(target[5:7])),
    ):
        if record.get(key) != value:
            record[key] = value
            changed = True
    return changed
