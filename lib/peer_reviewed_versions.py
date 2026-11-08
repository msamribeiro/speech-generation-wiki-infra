"""Shared discovery helpers for peer-reviewed versions of canonical paper records.

Discovery is deliberately conservative.  A proceedings source identifier is strong evidence that
the peer-reviewed version exists; an arXiv comment is only a review candidate until its identity,
date, and URL are verified.  This module never mutates metadata or content pages.
"""

from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Iterable

import yaml


ACCEPTANCE_RE = re.compile(
    r"\b(accepted|to appear|appeared|published|publication|conference paper)\b", re.IGNORECASE
)

VENUE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("Interspeech", re.compile(r"\binterspeech\b", re.IGNORECASE)),
    ("ICASSP", re.compile(r"\bicassp\b", re.IGNORECASE)),
    ("Speech Prosody", re.compile(r"\bspeech\s+prosody\b", re.IGNORECASE)),
    ("ICML", re.compile(r"\bicml\b|international conference on machine learning", re.IGNORECASE)),
    ("IJCAI", re.compile(r"\bijcai(?:-ecai)?\b", re.IGNORECASE)),
    ("AAAI", re.compile(r"\baaai(?:-\d+)?\b", re.IGNORECASE)),
    ("ICLR", re.compile(r"\biclr\b", re.IGNORECASE)),
    ("NeurIPS", re.compile(r"\bneurips\b", re.IGNORECASE)),
    ("NAACL", re.compile(r"\bnaacl\b", re.IGNORECASE)),
    ("EMNLP", re.compile(r"\bemnlp\b", re.IGNORECASE)),
    ("ACL", re.compile(r"\bacl\b", re.IGNORECASE)),
    ("LREC", re.compile(r"\blrec\b", re.IGNORECASE)),
    ("ICME", re.compile(r"\bicme\b", re.IGNORECASE)),
    ("ICPR", re.compile(r"\bicpr\b", re.IGNORECASE)),
    ("ASRU", re.compile(r"\basru\b", re.IGNORECASE)),
    ("SLT", re.compile(r"\bslt\b|spoken language technology workshop", re.IGNORECASE)),
)


def load_frozen_memberships(wiki_dir: Path) -> dict[str, list[str]]:
    """Return canonical paper ID -> sorted concept slugs proving date freeze.

    Only top-level canonical concept YAMLs participate.  Reconciliation runs, snapshots, and
    rendered pages are derived state and must never create a freeze by themselves.
    """

    claims_dir = wiki_dir / "_claims"
    memberships: dict[str, set[str]] = defaultdict(set)
    for path in sorted(claims_dir.glob("*.yaml")):
        data = yaml.safe_load(path.read_text()) or {}
        for paper in data.get("papers", []):
            if isinstance(paper, dict) and paper.get("id") is not None:
                memberships[str(paper["id"])].add(path.stem)
    return {paper_id: sorted(concepts) for paper_id, concepts in sorted(memberships.items())}


def infer_venue(comment: str | None) -> str | None:
    """Infer a venue name from acceptance prose without treating it as verified evidence."""

    text = comment or ""
    for venue, pattern in VENUE_PATTERNS:
        if pattern.search(text):
            return venue
    return None


def acceptance_comment_candidate(record: dict) -> tuple[bool, str | None]:
    """Return whether an arXiv comment asserts publication and its inferred venue."""

    comment = record.get("arxiv_comment") or ""
    venue = infer_venue(comment)
    return bool(venue and ACCEPTANCE_RE.search(comment)), venue


def is_preprint_canonical(record: dict) -> bool:
    """Whether the canonical record represents an arXiv/preprint version of the work."""

    source_ids = record.get("source_ids") or {}
    url = str(record.get("url") or "")
    return (
        record.get("venue_type") == "preprint"
        or record.get("venue") == "arXiv"
        or source_ids.get("arxiv") == record.get("id")
        or "arxiv.org" in url
    )


def isca_peer_url(record: dict) -> str | None:
    """Return the canonical ISCA landing page when an ISCA key is present."""

    source_ids = record.get("source_ids") or {}
    key = source_ids.get("isca")
    doi = str(source_ids.get("doi") or "")
    match = re.search(r"Interspeech\.(\d{4})-", doi, re.IGNORECASE)
    if not key or not match:
        return None
    return f"https://www.isca-archive.org/interspeech_{match.group(1)}/{key}.html"


def source_peer_candidates(record: dict) -> list[dict[str, str]]:
    """Return peer-reviewed landing pages derived from explicit source identifiers."""

    source_ids = record.get("source_ids") or {}
    candidates: list[dict[str, str]] = []
    isca_url = isca_peer_url(record)
    if isca_url:
        candidates.append({"source": "isca", "venue": "Interspeech", "url": isca_url})
    acl_url = source_ids.get("url_acl")
    if acl_url:
        candidates.append({"source": "acl", "venue": str(record.get("venue") or "ACL"), "url": str(acl_url)})
    openreview = source_ids.get("openreview")
    if openreview:
        candidates.append(
            {
                "source": "openreview",
                "venue": str(record.get("venue") or infer_venue(record.get("arxiv_comment")) or "OpenReview"),
                "url": f"https://openreview.net/forum?id={openreview}",
            }
        )
    return candidates


def matching_source_records(record: dict, records: Iterable[dict]) -> list[str]:
    """Return other record IDs sharing a non-null proceedings source identifier."""

    source_ids = record.get("source_ids") or {}
    matches: set[str] = set()
    for other in records:
        if other.get("id") == record.get("id"):
            continue
        other_sources = other.get("source_ids") or {}
        for key in ("isca", "acl", "openreview", "doi"):
            value = source_ids.get(key)
            if value and other_sources.get(key) == value:
                matches.add(str(other.get("id")))
    return sorted(matches)
