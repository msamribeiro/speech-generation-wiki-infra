"""Deterministic projections for snapshot-backed temporal reports."""

from __future__ import annotations

from collections import Counter
from datetime import date, datetime
import re
from typing import Any

import yaml

from lib.reconciliation import canonical_digest


QUARTERLY_SECTIONS = (
    "Scope and retrospective assessment",
    "Executive synthesis",
    "Publication activity during the quarter",
    "Changes in assessed knowledge",
    "New methods and capability directions",
    "Evaluation and evidence-quality changes",
    "Contested, weakened, or unresolved findings",
    "Attention versus evidence caveat",
    "Representative reading path",
    "Snapshot and provenance references",
)


def validate_trend_snapshots(snapshots: list[dict]) -> None:
    """Require distinct published snapshots in strictly increasing cutoff order."""

    if len(snapshots) < 2:
        raise ValueError("trend reports require at least two published snapshots")
    seen_ids: set[str] = set()
    previous_cutoff: str | None = None
    for snapshot in snapshots:
        validate_published_snapshot(snapshot)
        snapshot_id = str(snapshot["snapshot_id"])
        if snapshot_id in seen_ids:
            raise ValueError(f"trend snapshots contain duplicate ID: {snapshot_id}")
        seen_ids.add(snapshot_id)
        cutoff = _iso(snapshot["evidence_cutoff"])
        if previous_cutoff is not None and cutoff <= previous_cutoff:
            raise ValueError("trend snapshots must be ordered by increasing evidence cutoff")
        previous_cutoff = cutoff


def trend_comparability(snapshots: list[dict]) -> list[dict]:
    """Describe like-for-like concept and claim coverage for adjacent snapshots."""

    validate_trend_snapshots(snapshots)
    comparisons: list[dict] = []
    for earlier, later in zip(snapshots, snapshots[1:]):
        earlier_concepts = {
            str(item["concept"]): item for item in earlier.get("concepts") or []
        }
        later_concepts = {
            str(item["concept"]): item for item in later.get("concepts") or []
        }
        shared_concepts = sorted(earlier_concepts.keys() & later_concepts.keys())
        earlier_claims = {
            str(claim["ref"])
            for slug in shared_concepts
            for claim in earlier_concepts[slug].get("claim_clusters") or []
        }
        later_claims = {
            str(claim["ref"])
            for slug in shared_concepts
            for claim in later_concepts[slug].get("claim_clusters") or []
        }
        comparisons.append({
            "from_snapshot": str(earlier["snapshot_id"]),
            "to_snapshot": str(later["snapshot_id"]),
            "from_cutoff": _iso(earlier["evidence_cutoff"]),
            "to_cutoff": _iso(later["evidence_cutoff"]),
            "schema_changed": earlier.get("schema_version") != later.get("schema_version"),
            "shared_concepts": shared_concepts,
            "added_concepts": sorted(later_concepts.keys() - earlier_concepts.keys()),
            "removed_concepts": sorted(earlier_concepts.keys() - later_concepts.keys()),
            "shared_local_claim_refs": sorted(earlier_claims & later_claims),
            "added_local_claim_refs": sorted(later_claims - earlier_claims),
            "removed_local_claim_refs": sorted(earlier_claims - later_claims),
        })
    return comparisons


def select_venue_papers(
    snapshot: dict,
    *,
    venue: str,
    start: str,
    end: str,
) -> list[dict]:
    """Select one canonical venue over an inclusive publication-date range."""

    validate_published_snapshot(snapshot)
    start_date = _iso(start)
    end_date = _iso(end)
    if start_date > end_date:
        raise ValueError("venue report start date must not exceed end date")
    if end_date > _iso(snapshot["evidence_cutoff"]):
        raise ValueError("venue report range exceeds snapshot evidence cutoff")

    canonical_venues = sorted({str(item["venue"]) for item in snapshot["included_papers"]})
    if venue not in canonical_venues:
        case_matches = [item for item in canonical_venues if item.casefold() == venue.casefold()]
        if case_matches:
            raise ValueError(f"venue must use canonical value: {case_matches[0]}")
        raise ValueError(f"venue is not represented in snapshot: {venue}")

    return sorted(
        (
            item for item in snapshot["included_papers"]
            if str(item["venue"]) == venue
            and start_date <= _iso(item["published_date"]) <= end_date
        ),
        key=lambda item: (_iso(item["published_date"]), str(item["id"])),
    )


def venue_projection(
    snapshot: dict,
    *,
    venue: str,
    start: str,
    end: str,
) -> dict:
    """Project venue activity and the snapshot claims its papers inform."""

    selected = select_venue_papers(snapshot, venue=venue, start=start, end=end)
    selected_ids = {str(item["id"]) for item in selected}
    concept_counts = Counter(
        str(concept) for item in selected for concept in item.get("concepts") or []
    )
    local_claims: list[dict] = []
    for concept in snapshot.get("concepts") or []:
        slug = str(concept["concept"])
        for claim in concept.get("claim_clusters") or []:
            assessment = claim.get("cutoff_assessment") or {}
            roles = {
                "supporting": sorted(selected_ids & set(map(str, assessment.get("supporting_papers") or []))),
                "contradicting": sorted(selected_ids & set(map(str, assessment.get("contradicting_papers") or []))),
                "refining": sorted(selected_ids & set(map(str, assessment.get("refining_papers") or []))),
            }
            evidence_ids = sorted(set().union(*map(set, roles.values())))
            if evidence_ids:
                local_claims.append({
                    "ref": str(claim["ref"]),
                    "concept": slug,
                    "proposition": str(claim["proposition"]),
                    "status": assessment.get("status"),
                    "confidence": assessment.get("confidence"),
                    "venue_evidence_papers": evidence_ids,
                    "venue_evidence_roles": roles,
                })
    return {
        "snapshot_id": str(snapshot["snapshot_id"]),
        "snapshot_digest": str(snapshot["digest"]),
        "venue": venue,
        "start": _iso(start),
        "end": _iso(end),
        "paper_count": len(selected),
        "paper_ids": [str(item["id"]) for item in selected],
        "concept_counts": dict(sorted(concept_counts.items())),
        "local_claims": sorted(local_claims, key=lambda item: item["ref"]),
    }


def validate_venue_synthesis_readiness(
    projection: dict,
    *,
    minimum_claims: int = 2,
    minimum_concepts: int = 2,
) -> None:
    """Refuse venue output that cannot support evidence-backed thematic synthesis."""

    if not projection.get("paper_ids"):
        raise ValueError("venue selection contains no papers")
    claim_refs = {str(item["ref"]) for item in projection.get("local_claims") or []}
    claim_concepts = {str(item["concept"]) for item in projection.get("local_claims") or []}
    if len(claim_refs) < minimum_claims or len(claim_concepts) < minimum_concepts:
        raise ValueError(
            "venue selection cannot support a synthesis: "
            f"requires at least {minimum_claims} assessed claims across "
            f"{minimum_concepts} concepts"
        )


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


def _markdown_frontmatter(markdown: str) -> tuple[dict, str]:
    if not markdown.startswith("---\n"):
        raise ValueError("report must begin with YAML frontmatter")
    try:
        raw, body = markdown[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise ValueError("report frontmatter is not terminated") from exc
    metadata = yaml.safe_load(raw)
    if not isinstance(metadata, dict):
        raise ValueError("report frontmatter must be a mapping")
    return metadata, body


def validate_quarterly_report(
    markdown: str,
    snapshot: dict,
    *,
    reports_index: str | None = None,
    changelog: str | None = None,
) -> None:
    """Validate a published quarterly report against its immutable snapshot."""

    projection = quarterly_projection(snapshot)
    metadata, body = _markdown_frontmatter(markdown)
    expected = {
        "report_type": "quarterly",
        "period": snapshot["period"],
        "snapshot_id": snapshot["snapshot_id"],
        "snapshot_digest": snapshot["digest"],
        "evidence_cutoff": _iso(snapshot["evidence_cutoff"]),
        "baseline_cutoff": _iso(snapshot["baseline_cutoff"]),
        "assessment_as_of": _iso(snapshot["assessment_as_of"]),
        "assessment_mode": "retrospective",
        "included_paper_count": len(snapshot["included_papers"]),
        "baseline_paper_count": len(snapshot["baseline_papers"]),
        "activity_paper_count": projection["activity"]["paper_count"],
        "concept_count": len(snapshot.get("concepts") or []),
        "concept_membership_count": sum(
            len(item.get("concepts") or []) for item in snapshot["included_papers"]
        ),
        "activity_concept_membership_count": projection["activity"]["concept_membership_count"],
    }
    for key, value in expected.items():
        actual = _iso(metadata[key]) if key.endswith("cutoff") or key == "assessment_as_of" else metadata.get(key)
        if actual != value:
            raise ValueError(f"report {key} does not match snapshot: {actual!r} != {value!r}")
    if {
        "start": _iso(metadata["activity_window"]["start"]),
        "end": _iso(metadata["activity_window"]["end"]),
    } != {
        "start": _iso(snapshot["activity_window"]["start"]),
        "end": _iso(snapshot["activity_window"]["end"]),
    }:
        raise ValueError("report activity_window does not match snapshot")

    generation = metadata.get("generation") or {}
    if generation.get("schema_version") != 2:
        raise ValueError("report generation provenance must use schema version 2")
    if generation.get("stage") != "report" or generation.get("mode") != "quarterly":
        raise ValueError("report generation provenance has the wrong stage or mode")
    if not generation.get("commit"):
        raise ValueError("report generation provenance must record an infra commit")

    meta_sections = {
        "Scope and retrospective assessment",
        "Snapshot and provenance references",
    }
    for section in QUARTERLY_SECTIONS:
        marker = section if section in meta_sections else f"## {section}"
        if marker not in body:
            raise ValueError(f"report is missing required section: {section}")
    if "retrospective" not in body.lower():
        raise ValueError("report must explicitly describe the assessment as retrospective")
    if "adoption" not in body.lower() or "attention" not in body.lower():
        raise ValueError("report must distinguish attention from adoption")

    included_ids = {str(item["id"]) for item in snapshot["included_papers"]}
    cited_ids = set(re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", body))
    missing = sorted(cited_ids - included_ids)
    if missing:
        raise ValueError(f"report cites papers outside snapshot: {', '.join(missing)}")
    if not cited_ids:
        raise ValueError("report must cite representative papers")

    if reports_index is not None and f"quarterly/{snapshot['snapshot_id']}" not in reports_index:
        raise ValueError("reports index does not link the quarterly report")
    if changelog is not None and f"report | {snapshot['snapshot_id']}" not in changelog:
        raise ValueError("changelog does not record the report operation")
