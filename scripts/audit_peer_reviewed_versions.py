#!/usr/bin/env python3
"""Generate a deterministic, read-only inventory of peer-reviewed-version candidates.

The output is evidence for review, not an apply plan.  Explicit proceedings source IDs are marked
``source_verified``; arXiv acceptance comments remain ``claim_unverified`` until an authoritative
landing page and venue date are supplied.  Rejected records are used for counterpart discovery but
are never emitted as canonical migration targets.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from lib.peer_reviewed_versions import (  # noqa: E402
    acceptance_comment_candidate,
    is_preprint_canonical,
    load_frozen_memberships,
    matching_source_records,
    source_peer_candidates,
)


ACTIVE_STATUSES = {"accepted", "ingested"}


def load_records(metadata_dir: Path) -> list[dict]:
    return [json.loads(path.read_text()) for path in sorted(metadata_dir.glob("*.json"))]


def build_inventory(records: list[dict], wiki_dir: Path) -> dict:
    frozen = load_frozen_memberships(wiki_dir)
    entries: list[dict] = []
    for record in records:
        if record.get("status") not in ACTIVE_STATUSES or record.get("is_duplicate"):
            continue
        if not is_preprint_canonical(record):
            continue

        source_candidates = source_peer_candidates(record)
        comment_candidate, inferred_venue = acceptance_comment_candidate(record)
        frozen_concepts = frozen.get(str(record.get("id")), [])
        date_mismatch = bool(
            frozen_concepts
            and record.get("conference_date")
            and record.get("published_date") != record.get("conference_date")
        )
        if not source_candidates and not comment_candidate and not date_mismatch:
            continue

        signals: list[str] = []
        if source_candidates:
            signals.append("source_verified")
        if comment_candidate:
            signals.append("acceptance_comment")
        if date_mismatch:
            signals.append("frozen_date_mismatch")

        peer_urls = sorted({candidate["url"] for candidate in source_candidates})
        readiness_issues: list[str] = []
        if not source_candidates:
            readiness_issues.append("peer_reviewed_identity_unverified")
        if not peer_urls:
            readiness_issues.append("peer_reviewed_url_missing")
        if not record.get("conference_date") and not record.get("journal_date"):
            readiness_issues.append("peer_reviewed_date_missing")
        if len(peer_urls) > 1:
            readiness_issues.append("multiple_peer_reviewed_urls")

        entries.append(
            {
                "id": str(record.get("id")),
                "title": record.get("title"),
                "status": record.get("status"),
                "signals": signals,
                "frozen": bool(frozen_concepts),
                "frozen_concepts": frozen_concepts,
                "current": {
                    "venue": record.get("venue"),
                    "venue_type": record.get("venue_type"),
                    "published_date": record.get("published_date"),
                    "conference_date": record.get("conference_date"),
                    "journal_date": record.get("journal_date"),
                    "url": record.get("url"),
                    "url_peer_reviewed": record.get("url_peer_reviewed"),
                },
                "candidate": {
                    "inferred_venue": inferred_venue,
                    "source_candidates": source_candidates,
                    "matching_source_records": matching_source_records(record, records),
                    "arxiv_comment": record.get("arxiv_comment"),
                },
                "readiness": "ready_for_review" if not readiness_issues else "unresolved",
                "readiness_issues": readiness_issues,
            }
        )

    entries.sort(key=lambda item: item["id"])
    signal_counts = Counter(signal for item in entries for signal in item["signals"])
    issue_counts = Counter(issue for item in entries for issue in item["readiness_issues"])
    return {
        "schema_version": 1,
        "kind": "peer_reviewed_version_inventory",
        "mutation_allowed": False,
        "candidate_policy": {
            "statuses": sorted(ACTIVE_STATUSES),
            "requires_preprint_canonical": True,
            "acceptance_comments_are_unverified": True,
            "frozen_by": "top-level canonical claim YAML membership",
        },
        "summary": {
            "candidates": len(entries),
            "frozen": sum(1 for item in entries if item["frozen"]),
            "resolved_for_review": sum(1 for item in entries if item["readiness"] == "ready_for_review"),
            "unresolved": sum(1 for item in entries if item["readiness"] == "unresolved"),
            "signals": dict(sorted(signal_counts.items())),
            "issues": dict(sorted(issue_counts.items())),
        },
        "entries": entries,
    }


def render_json(inventory: dict) -> str:
    return json.dumps(inventory, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wiki-dir", type=Path, required=True, help="Explicit canonical content checkout")
    parser.add_argument("--metadata-dir", type=Path, default=ROOT / "raw" / "metadata")
    parser.add_argument("--output", type=Path, help="Write the deterministic JSON inventory")
    args = parser.parse_args()

    inventory = build_inventory(load_records(args.metadata_dir), args.wiki_dir)
    text = render_json(inventory)
    if args.output:
        args.output.write_text(text)
        print(f"Wrote {args.output}")
    else:
        print(text, end="")
    print(f"sha256={hashlib.sha256(text.encode()).hexdigest()}", file=sys.stderr)


if __name__ == "__main__":
    main()
