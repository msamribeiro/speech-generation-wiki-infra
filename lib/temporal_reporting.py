"""Deterministic projections for snapshot-backed temporal reports."""

from __future__ import annotations

from collections import Counter
from datetime import date, datetime
from typing import Any

from lib.reconciliation import canonical_digest


def _iso(value: Any) -> str:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str):
        return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
    raise ValueError(f"not an ISO date: {value!r}")


def validate_published_snapshot(snapshot: dict) -> None:
    """Validate the immutable fields required by a quarterly report."""

    if snapshot.get("status") != "published":
        raise ValueError("report source snapshot must be published")
    if snapshot.get("assessment_mode") != "retrospective":
        raise ValueError("report source snapshot must be retrospective")
    if snapshot.get("digest") != canonical_digest(snapshot, omit_digest=True):
        raise ValueError("snapshot digest mismatch")

    start = _iso(snapshot["activity_window"]["start"])
    end = _iso(snapshot["activity_window"]["end"])
    baseline = _iso(snapshot["baseline_cutoff"])
    cutoff = _iso(snapshot["evidence_cutoff"])
    _iso(snapshot["assessment_as_of"])
    if not baseline < start <= end == cutoff:
        raise ValueError("invalid quarterly snapshot boundaries")

    included = {str(item["id"]): item for item in snapshot.get("included_papers") or []}
    baseline_ids = list(map(str, snapshot.get("baseline_papers") or []))
    activity_ids = list(map(str, snapshot.get("activity_papers") or []))
    if len(included) != len(snapshot.get("included_papers") or []):
        raise ValueError("included_papers contains duplicate IDs")
    if len(set(baseline_ids)) != len(baseline_ids) or len(set(activity_ids)) != len(activity_ids):
        raise ValueError("snapshot paper partitions contain duplicate IDs")
    if set(baseline_ids) & set(activity_ids):
        raise ValueError("baseline and activity papers overlap")
    if set(baseline_ids) | set(activity_ids) != set(included):
        raise ValueError("baseline and activity partitions do not cover included papers")
    for paper_id in baseline_ids:
        if _iso(included[paper_id]["published_date"]) > baseline:
            raise ValueError(f"baseline paper exceeds cutoff: {paper_id}")
    for paper_id in activity_ids:
        published = _iso(included[paper_id]["published_date"])
        if not start <= published <= end:
            raise ValueError(f"activity paper outside quarter: {paper_id}")


def _assessment_transition(ref: str, proposition: str, baseline: dict | None, cutoff: dict) -> dict:
    baseline_status = baseline.get("status") if baseline else None
    cutoff_status = cutoff.get("status")
    baseline_confidence = baseline.get("confidence") if baseline else None
    cutoff_confidence = cutoff.get("confidence")
    return {
        "ref": ref,
        "proposition": proposition,
        "baseline_status": baseline_status,
        "cutoff_status": cutoff_status,
        "baseline_confidence": baseline_confidence,
        "cutoff_confidence": cutoff_confidence,
        "new": baseline is None,
        "status_changed": baseline is not None and baseline_status != cutoff_status,
        "confidence_changed": baseline is not None and baseline_confidence != cutoff_confidence,
        "baseline_evidence_count": len(set(
            (baseline or {}).get("supporting_papers", [])
            + (baseline or {}).get("contradicting_papers", [])
            + (baseline or {}).get("refining_papers", [])
        )),
        "cutoff_evidence_count": len(set(
            cutoff.get("supporting_papers", [])
            + cutoff.get("contradicting_papers", [])
            + cutoff.get("refining_papers", [])
        )),
    }


def quarterly_projection(snapshot: dict) -> dict:
    """Separate quarterly publication activity from assessed knowledge changes."""

    validate_published_snapshot(snapshot)
    activity_ids = set(map(str, snapshot["activity_papers"]))
    activity_records = [
        item for item in snapshot["included_papers"] if str(item["id"]) in activity_ids
    ]
    venue_counts = Counter(str(item["venue"]) for item in activity_records)
    concept_counts = Counter(
        str(concept)
        for item in activity_records
        for concept in item.get("concepts") or []
    )

    local: list[dict] = []
    new_families: list[dict] = []
    expanded_families: list[dict] = []
    for concept in snapshot.get("concepts") or []:
        slug = str(concept["concept"])
        for cluster in concept.get("claim_clusters") or []:
            local.append(_assessment_transition(
                str(cluster["ref"]),
                str(cluster["proposition"]),
                cluster.get("baseline_assessment"),
                cluster["cutoff_assessment"],
            ))
        for family in concept.get("method_families") or []:
            baseline_papers = list(map(str, family.get("baseline_papers") or []))
            cutoff_papers = list(map(str, family.get("cutoff_papers") or []))
            record = {
                "concept": slug,
                "id": str(family["id"]),
                "baseline_papers": baseline_papers,
                "cutoff_papers": cutoff_papers,
            }
            if not baseline_papers and cutoff_papers:
                new_families.append(record)
            elif len(cutoff_papers) > len(baseline_papers):
                expanded_families.append(record)

    broader = [
        _assessment_transition(
            str(claim["id"]),
            str(claim["proposition"]),
            claim.get("baseline_assessment"),
            claim["cutoff_assessment"],
        )
        for claim in snapshot.get("broader_claims") or []
    ]
    new_local = [item for item in local if item["new"]]
    status_changed_local = [item for item in local if item["status_changed"]]
    newly_contested = [
        item for item in local
        if item["cutoff_status"] == "contested"
        and (item["new"] or item["baseline_status"] != "contested")
    ]
    strengthened_local = [
        item for item in status_changed_local
        if item["baseline_status"] == "emerging"
        and item["cutoff_status"] == "strongly_supported"
    ]

    return {
        "snapshot_id": snapshot["snapshot_id"],
        "snapshot_digest": snapshot["digest"],
        "activity": {
            "paper_count": len(activity_records),
            "concept_membership_count": sum(concept_counts.values()),
            "venue_counts": dict(sorted(venue_counts.items())),
            "concept_counts": dict(sorted(concept_counts.items())),
        },
        "knowledge_changes": {
            "local": local,
            "broader": broader,
            "new_local_count": len(new_local),
            "strengthened_local_count": len(strengthened_local),
            "newly_contested_local_count": len(newly_contested),
            "changed_broader_count": sum(
                item["status_changed"] or item["confidence_changed"] for item in broader
            ),
        },
        "methods": {
            "new_families": sorted(new_families, key=lambda item: (item["concept"], item["id"])),
            "expanded_families": sorted(expanded_families, key=lambda item: (item["concept"], item["id"])),
        },
    }
