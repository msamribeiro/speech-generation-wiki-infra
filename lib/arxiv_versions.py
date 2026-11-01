"""arXiv version history, used to pin the version a record's content comes from.

The OAI arXivRaw format lists every version with its submission date. A record's
``version_date`` is the date of the version we fetched or downloaded (see
docs/schemas/metadata.md, "Paper Dates"); ``preprint_date`` is always v1.
"""

from __future__ import annotations

import re
import time
from datetime import datetime
from email.utils import parsedate_to_datetime

import requests

from lib.paper_dates import apply_date_rule

OAI_URL = "https://oaipmh.arxiv.org/oai"


def fetch_versions(arxiv_id: str, retries: int = 3) -> list[tuple[int, str]]:
    """Return [(version_number, 'YYYY-MM-DD'), ...] in order, or [] if unavailable."""
    url = f"{OAI_URL}?verb=GetRecord&identifier=oai:arXiv.org:{arxiv_id}&metadataPrefix=arXivRaw"
    for attempt in range(retries):
        try:
            resp = requests.get(url, timeout=90, headers={"User-Agent": "speech-generation-wiki/1.0 (research corpus tooling)"})
            resp.raise_for_status()
            text = resp.text
        except Exception:
            time.sleep(5 * (attempt + 1))
            continue
        out = []
        for num, stamp in re.findall(r'<version version="v(\d+)">\s*<date>(.*?)</date>', text, re.S):
            out.append((int(num), parsedate_to_datetime(stamp).date().isoformat()))
        if out:
            return out
        time.sleep(5 * (attempt + 1))
    return []


def pick_version(versions: list[tuple[int, str]], as_of: str | None) -> tuple[int, str]:
    """Latest version submitted on or before `as_of`; the first version if none qualify.

    `as_of=None` means "now": the latest version.
    """
    if as_of is None:
        return versions[-1]
    eligible = [v for v in versions if v[1] <= as_of]
    return eligible[-1] if eligible else versions[0]


def pin_version(record: dict, versions: list[tuple[int, str]], as_of: str | None, estimated: bool) -> bool:
    """Record preprint_date (v1) and the pinned version, then re-apply the date rule.

    Returns True if any field changed.
    """
    if not versions:
        return False
    number, version_date = pick_version(versions, as_of)
    updates = {
        "preprint_date": versions[0][1],
        "arxiv_version": number,
        "version_date": version_date,
        "version_estimated": estimated,
    }
    changed = False
    for key, value in updates.items():
        if record.get(key) != value:
            record[key] = value
            changed = True
    return apply_date_rule(record) or changed


def feed_entry_version(entry) -> tuple[int | None, str | None]:
    """Version number and date of an arXiv API (Atom) entry: the id carries `vN`, `updated` is its date."""
    m = re.search(r"v(\d+)$", str(entry.get("id", "")))
    tp = entry.get("updated_parsed")
    date_str = f"{tp.tm_year}-{tp.tm_mon:02d}-{tp.tm_mday:02d}" if tp else None
    return (int(m.group(1)) if m else None), date_str


def today() -> str:
    return datetime.now().date().isoformat()
