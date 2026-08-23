"""Validate cross-concept reconciliation registries, runs, and snapshots."""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
import re
import sys

import yaml

from checks._base import CheckArgs, Issue, ModuleResult


ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

from lib.reconciliation import (
    DIGEST_RE,
    QUALIFIED_REF_RE,
    canonical_digest,
    find_cycles,
    load_concept_graphs,
    stable_candidate_id,
)


_DEFAULT_WIKI = ROOT / "wiki"
RELATIONSHIP_TYPES = {"equivalent", "specialization", "supports", "refines", "contradicts", "tradeoff", "related"}
SYMMETRIC_TYPES = {"equivalent", "contradicts", "tradeoff", "related"}
DIRECTED_TYPES = {"specialization", "supports", "refines"}
RUN_TRIGGERS = {"quarterly-integration", "large-integration-round", "corrective-review"}
RUN_STATUSES = {"in_progress", "finalized", "superseded"}
REVIEW_MODES = {"agent_adjudication", "human_review"}
REGISTRY_REVIEW_STATUSES = {"agent_proposed", "human_approved"}
DISPOSITIONS = {"pending", "accepted", "rejected", "deferred"}
THEMES = {"evaluation", "efficiency", "speaker", "controllability", "robustness", "codecs-language-modeling", "streaming-agents", "post-training"}
CLAIM_STATUSES = {"strongly_supported", "emerging", "contested", "weakened", "superseded", "historical"}
CONFIDENCE = {"high", "medium", "low"}
SIGNAL_FIELDS = {
    "text_similarity", "shared_evidence_score", "shared_supporting_papers",
    "status_compatible", "polarity_compatible", "status_polarity_score",
    "technical_vocabulary_score", "shared_terms", "aggregate_score",
}


def _high_similarity_threshold() -> float:
    config_path = ROOT / "config" / "health_check.yaml"
    try:
        config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        value = float((config.get("reconcile") or {}).get("high_similarity_warning_threshold", 0.65))
    except (OSError, TypeError, ValueError, yaml.YAMLError):
        return 0.65
    return value if 0.0 <= value <= 1.0 else 0.65


def _issue(severity: str, ref: str, check: str, message: str) -> Issue:
    return Issue(severity=severity, module="reconcile", paper_id=ref, check=check, message=message)


def _iso(value: object) -> str | None:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str) and re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
        except ValueError:
            return None
    return None


def _read_mapping(path: Path, artifact: str) -> tuple[dict | None, list[Issue]]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        return None, [_issue("error", artifact, "yaml_parses", f"{path}: {exc}")]
    if not isinstance(data, dict):
        return None, [_issue("error", artifact, "yaml_parses", f"{path}: expected a mapping")]
    return data, []


def _missing(data: dict, fields: set[str]) -> list[str]:
    return sorted(field for field in fields if field not in data or data[field] is None)


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _duplicate_values(values: list[object]) -> list[str]:
    seen: set[object] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(str(value))
        seen.add(value)
    return sorted(duplicates)


def _validate_qualified_ref(ref: object, known_refs: set[str], artifact: str) -> list[Issue]:
    if not isinstance(ref, str) or QUALIFIED_REF_RE.fullmatch(ref) is None:
        return [_issue("error", artifact, "qualified_refs_resolve", f"invalid qualified reference: {ref!r}")]
    if ref not in known_refs:
        return [_issue("error", artifact, "qualified_refs_resolve", f"unknown qualified reference: {ref}")]
    return []


def _concept_state(graphs: dict[str, dict]) -> tuple[set[str], dict[str, dict], set[str]]:
    refs: set[str] = set()
    clusters: dict[str, dict] = {}
    papers: set[str] = set()
    for concept, graph in graphs.items():
        papers.update(str(item.get("id")) for item in graph.get("papers") or [] if isinstance(item, dict))
        for cluster in graph.get("claim_clusters") or []:
            if isinstance(cluster, dict) and isinstance(cluster.get("id"), str):
                ref = f"{concept}#{cluster['id']}"
                refs.add(ref)
                clusters[ref] = cluster
    return refs, clusters, papers


def _validate_registry(
    data: dict,
    known_refs: set[str],
    clusters: dict[str, dict],
    known_papers: set[str],
) -> tuple[list[Issue], dict[str, dict], dict[str, dict]]:
    issues: list[Issue] = []
    ref = "registry"
    missing = _missing(data, {"schema_version", "last_updated", "relationships", "broader_claims"})
    if missing:
        issues.append(_issue("error", ref, "registry_required_fields", f"missing fields: {missing}"))
    if data.get("schema_version") != 1:
        issues.append(_issue("error", ref, "registry_schema_version", "schema_version must be 1"))
    if _iso(data.get("last_updated")) is None:
        issues.append(_issue("error", ref, "registry_required_fields", "last_updated must be YYYY-MM-DD"))
    relationships = data.get("relationships") or []
    broader_claims = data.get("broader_claims") or []
    if not isinstance(relationships, list) or not isinstance(broader_claims, list):
        issues.append(_issue("error", ref, "registry_required_fields", "relationships and broader_claims must be lists"))
        return issues, {}, {}

    relationship_by_id: dict[str, dict] = {}
    agent_proposed = 0
    directed_edges: dict[str, set[str]] = {}
    for item in relationships:
        if not isinstance(item, dict):
            issues.append(_issue("error", ref, "relationship_required_fields", f"relationship is not a mapping: {item!r}"))
            continue
        rid = item.get("id", "?")
        item_ref = f"registry:relationship:{rid}"
        missing = _missing(item, {"id", "source", "target", "type", "rationale", "review_status", "reviewed_on", "accepted_in"})
        if missing:
            issues.append(_issue("error", item_ref, "relationship_required_fields", f"missing fields: {missing}"))
        if not isinstance(rid, str) or not rid.startswith("rel_"):
            issues.append(_issue("error", item_ref, "registry_ids_unique", "relationship id must start with rel_"))
        elif rid in relationship_by_id:
            issues.append(_issue("error", item_ref, "registry_ids_unique", f"duplicate relationship id: {rid}"))
        else:
            relationship_by_id[rid] = item
        source, target, relation_type = item.get("source"), item.get("target"), item.get("type")
        issues.extend(_validate_qualified_ref(source, known_refs, item_ref))
        issues.extend(_validate_qualified_ref(target, known_refs, item_ref))
        if relation_type not in RELATIONSHIP_TYPES:
            issues.append(_issue("error", item_ref, "relationship_vocabulary", f"invalid type: {relation_type!r}"))
        if isinstance(source, str) and isinstance(target, str):
            if source.split("#", 1)[0] == target.split("#", 1)[0]:
                issues.append(_issue("error", item_ref, "relationship_cross_concept", "endpoints must be from different concepts"))
            if relation_type in SYMMETRIC_TYPES and source >= target:
                issues.append(_issue("error", item_ref, "relationship_endpoint_order", "symmetric endpoints must be lexically ordered"))
            if relation_type in DIRECTED_TYPES:
                directed_edges.setdefault(source, set()).add(target)
        if not _nonempty(item.get("rationale")):
            issues.append(_issue("error", item_ref, "relationship_required_fields", "rationale must be non-empty"))
        if item.get("review_status") not in REGISTRY_REVIEW_STATUSES:
            issues.append(_issue("error", item_ref, "registry_review_status", f"invalid review_status: {item.get('review_status')!r}"))
        elif item.get("review_status") == "agent_proposed":
            agent_proposed += 1
        if _iso(item.get("reviewed_on")) is None:
            issues.append(_issue("error", item_ref, "relationship_required_fields", "reviewed_on must be YYYY-MM-DD"))
        if not _nonempty(item.get("accepted_in")):
            issues.append(_issue("error", item_ref, "relationship_required_fields", "accepted_in must be non-empty"))

    for cycle in find_cycles(directed_edges):
        issues.append(_issue("error", ref, "no_cycles", "directed relationship cycle: " + " -> ".join(cycle)))

    broader_by_id: dict[str, dict] = {}
    equivalent_memberships: dict[str, list[str]] = {}
    role_fields = {
        "supporting_papers": "supporting_papers",
        "contradicting_papers": "contradicting_papers",
        "refining_papers": "refining_papers",
    }
    for item in broader_claims:
        if not isinstance(item, dict):
            issues.append(_issue("error", ref, "broader_required_fields", f"broader claim is not a mapping: {item!r}"))
            continue
        bid = item.get("id", "?")
        item_ref = f"registry:broader:{bid}"
        required = {"id", "proposition", "status", "confidence", "review_status", "members", *role_fields, "caveats", "review_rationale", "evidence_cutoff", "assessment_date", "reviewed_in"}
        missing = _missing(item, required)
        if missing:
            issues.append(_issue("error", item_ref, "broader_required_fields", f"missing fields: {missing}"))
        if not isinstance(bid, str) or not bid.startswith("broader_"):
            issues.append(_issue("error", item_ref, "registry_ids_unique", "broader id must start with broader_"))
        elif bid in broader_by_id or bid in relationship_by_id:
            issues.append(_issue("error", item_ref, "registry_ids_unique", f"duplicate registry id: {bid}"))
        else:
            broader_by_id[bid] = item
        if item.get("status") not in CLAIM_STATUSES or item.get("confidence") not in CONFIDENCE:
            issues.append(_issue("error", item_ref, "broader_vocabulary", "invalid status or confidence"))
        if item.get("review_status") not in REGISTRY_REVIEW_STATUSES:
            issues.append(_issue("error", item_ref, "registry_review_status", f"invalid review_status: {item.get('review_status')!r}"))
        elif item.get("review_status") == "agent_proposed":
            agent_proposed += 1
        if not _nonempty(item.get("proposition")) or not _nonempty(item.get("review_rationale")):
            issues.append(_issue("error", item_ref, "broader_required_fields", "proposition and review_rationale must be non-empty"))
        for field in ("evidence_cutoff", "assessment_date"):
            if _iso(item.get(field)) is None:
                issues.append(_issue("error", item_ref, "broader_required_fields", f"{field} must be YYYY-MM-DD"))
        members = item.get("members") or []
        if not isinstance(members, list):
            issues.append(_issue("error", item_ref, "broader_membership_valid", "members must be a list"))
            members = []
        member_refs = [member.get("claim") for member in members if isinstance(member, dict)]
        duplicates = _duplicate_values(member_refs)
        if duplicates:
            issues.append(_issue("error", item_ref, "broader_membership_valid", f"duplicate members: {duplicates}"))
        concepts: set[str] = set()
        for member in members:
            if not isinstance(member, dict):
                issues.append(_issue("error", item_ref, "broader_membership_valid", f"member is not a mapping: {member!r}"))
                continue
            claim_ref = member.get("claim")
            issues.extend(_validate_qualified_ref(claim_ref, known_refs, item_ref))
            if isinstance(claim_ref, str) and "#" in claim_ref:
                concepts.add(claim_ref.split("#", 1)[0])
            relation = member.get("relationship")
            if relation not in RELATIONSHIP_TYPES:
                issues.append(_issue("error", item_ref, "relationship_vocabulary", f"invalid member relationship: {relation!r}"))
            if not _nonempty(member.get("rationale")):
                issues.append(_issue("error", item_ref, "broader_membership_valid", "member rationale must be non-empty"))
            if relation == "equivalent" and isinstance(claim_ref, str):
                equivalent_memberships.setdefault(claim_ref, []).append(str(bid))
        if len(members) < 2 or len(concepts) < 2:
            issues.append(_issue("error", item_ref, "broader_membership_valid", "broader claim must span at least two members and two concepts"))

        for field, cluster_field in role_fields.items():
            values = list(map(str, item.get(field) or []))
            if len(values) != len(set(values)):
                issues.append(_issue("error", item_ref, "evidence_deduplicated", f"{field} contains duplicates"))
            unknown = sorted(set(values) - known_papers)
            if unknown:
                issues.append(_issue("error", item_ref, "evidence_papers_valid", f"{field} contains unknown papers: {unknown}"))
            derived: set[str] = set()
            for member_ref in member_refs:
                if member_ref in clusters:
                    derived.update(map(str, clusters[member_ref].get(cluster_field) or []))
            if set(values) != derived:
                issues.append(_issue("error", item_ref, "broader_evidence_derived", f"{field} does not equal deduplicated member evidence"))

    for member_ref, broader_ids in equivalent_memberships.items():
        if len(broader_ids) > 1:
            issues.append(_issue("error", member_ref, "incompatible_canonical_memberships", f"equivalent member of multiple broader claims: {sorted(broader_ids)}"))
    if agent_proposed:
        issues.append(_issue("warning", ref, "agent_proposed_registry", f"{agent_proposed} registry records await human approval and are not rendering or snapshot authority"))
    return issues, relationship_by_id, broader_by_id


def _score(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool) and 0.0 <= float(value) <= 1.0


def _validate_run(
    path: Path,
    data: dict,
    graphs: dict[str, dict],
    known_refs: set[str],
    relationships: dict[str, dict],
    broader_claims: dict[str, dict],
) -> list[Issue]:
    issues: list[Issue] = []
    run_id = data.get("run_id", path.stem)
    ref = f"run:{run_id}"
    required = {"schema_version", "run_id", "trigger", "evidence_cutoff", "assessment_as_of", "status", "review_mode", "supersedes_run", "source", "generator", "diagnostics", "candidates"}
    missing = sorted(field for field in required if field not in data)
    if missing:
        issues.append(_issue("error", ref, "run_required_fields", f"missing fields: {missing}"))
    if data.get("schema_version") != 1 or run_id != path.stem:
        issues.append(_issue("error", ref, "run_identity", "schema_version must be 1 and run_id must match filename"))
    if data.get("trigger") not in RUN_TRIGGERS or data.get("status") not in RUN_STATUSES:
        issues.append(_issue("error", ref, "run_vocabulary", "invalid trigger or status"))
    if data.get("review_mode") not in REVIEW_MODES:
        issues.append(_issue("error", ref, "run_vocabulary", f"invalid review_mode: {data.get('review_mode')!r}"))
    for field in ("evidence_cutoff", "assessment_as_of"):
        if _iso(data.get(field)) is None:
            issues.append(_issue("error", ref, "run_required_fields", f"{field} must be YYYY-MM-DD"))

    source = data.get("source") or {}
    source_digests = source.get("concept_digests") or {}
    if not _nonempty(source.get("infra_commit")) or not _nonempty(source.get("content_commit")) or not isinstance(source_digests, dict):
        issues.append(_issue("error", ref, "run_source_valid", "source commits and concept_digests are required"))
    else:
        if set(source_digests) != set(graphs):
            issues.append(_issue("error", ref, "run_source_valid", "concept digest keys must match all concept graphs"))
        for concept, digest in source_digests.items():
            if not isinstance(digest, str) or DIGEST_RE.fullmatch(digest) is None:
                issues.append(_issue("error", ref, "run_source_valid", f"invalid digest for {concept}: {digest!r}"))
            elif data.get("status") == "in_progress" and concept in graphs and digest != canonical_digest(graphs[concept]):
                issues.append(_issue("error", ref, "run_source_stale", f"in-progress source digest is stale for {concept}"))

    generator = data.get("generator") or {}
    weights = generator.get("weights") or {}
    if generator.get("version") != 1 or any(not isinstance(generator.get(field), int) or generator.get(field) < 1 for field in ("neighbors_per_cluster", "review_cap", "shared_support_minimum")):
        issues.append(_issue("error", ref, "generator_config_valid", "invalid generator version or limits"))
    if set(weights) != {"text_similarity", "shared_evidence", "status_polarity", "technical_vocabulary"} or any(not _score(value) for value in weights.values()) or abs(sum(map(float, weights.values())) - 1.0) > 1e-9:
        issues.append(_issue("error", ref, "generator_config_valid", "weights must contain four scores summing to 1"))

    candidates = data.get("candidates") or []
    if not isinstance(candidates, list):
        return issues + [_issue("error", ref, "candidate_required_fields", "candidates must be a list")]
    ids = [candidate.get("id") for candidate in candidates if isinstance(candidate, dict)]
    pairs = [(candidate.get("left"), candidate.get("right")) for candidate in candidates if isinstance(candidate, dict)]
    if _duplicate_values(ids):
        issues.append(_issue("error", ref, "candidate_ids_unique", f"duplicate candidate ids: {_duplicate_values(ids)}"))
    if _duplicate_values(pairs):
        issues.append(_issue("error", ref, "candidate_pairs_unique", "duplicate candidate pairs"))
    pending = deferred = high_similarity = 0
    expected_order: list[tuple[float, str, str]] = []
    reviewed = False
    for candidate in candidates:
        if not isinstance(candidate, dict):
            issues.append(_issue("error", ref, "candidate_required_fields", f"candidate is not a mapping: {candidate!r}"))
            continue
        cid = candidate.get("id", "?")
        candidate_ref = f"{ref}:{cid}"
        required_candidate = {"id", "left", "right", "theme", "signals", "disposition", "relationship", "registry_target", "rationale", "reconsideration_trigger"}
        missing = sorted(field for field in required_candidate if field not in candidate)
        if missing:
            issues.append(_issue("error", candidate_ref, "candidate_required_fields", f"missing fields: {missing}"))
        left, right = candidate.get("left"), candidate.get("right")
        issues.extend(_validate_qualified_ref(left, known_refs, candidate_ref))
        issues.extend(_validate_qualified_ref(right, known_refs, candidate_ref))
        if isinstance(left, str) and isinstance(right, str):
            if left >= right:
                issues.append(_issue("error", candidate_ref, "candidate_pair_order", "left must be lexically smaller than right"))
            if left.split("#", 1)[0] == right.split("#", 1)[0]:
                issues.append(_issue("error", candidate_ref, "candidate_cross_concept", "candidate endpoints must be from different concepts"))
            if cid != stable_candidate_id(left, right):
                issues.append(_issue("error", candidate_ref, "candidate_id_stable", "candidate id does not match stable pair hash"))
        if candidate.get("theme") not in THEMES:
            issues.append(_issue("error", candidate_ref, "candidate_theme_valid", f"invalid theme: {candidate.get('theme')!r}"))
        signals = candidate.get("signals") or {}
        if not isinstance(signals, dict) or not SIGNAL_FIELDS.issubset(signals):
            issues.append(_issue("error", candidate_ref, "candidate_signals_valid", f"missing signal fields: {sorted(SIGNAL_FIELDS - set(signals) if isinstance(signals, dict) else SIGNAL_FIELDS)}"))
            aggregate = -1.0
        else:
            numeric_fields = {"text_similarity", "shared_evidence_score", "status_polarity_score", "technical_vocabulary_score", "aggregate_score"}
            for field in numeric_fields:
                if not _score(signals.get(field)):
                    issues.append(_issue("error", candidate_ref, "candidate_signals_valid", f"{field} must be between 0 and 1"))
            for field in ("shared_supporting_papers", "shared_terms"):
                values = signals.get(field)
                if not isinstance(values, list) or values != sorted(set(map(str, values))):
                    issues.append(_issue("error", candidate_ref, "candidate_signals_valid", f"{field} must be sorted and unique"))
            for field in ("status_compatible", "polarity_compatible"):
                if not isinstance(signals.get(field), bool):
                    issues.append(_issue("error", candidate_ref, "candidate_signals_valid", f"{field} must be boolean"))
            aggregate = float(signals.get("aggregate_score", -1.0))
            if aggregate >= _high_similarity_threshold():
                high_similarity += 1
        if isinstance(left, str) and isinstance(right, str):
            expected_order.append((-aggregate, left, right))
        disposition = candidate.get("disposition")
        if disposition not in DISPOSITIONS:
            issues.append(_issue("error", candidate_ref, "decision_valid", f"invalid disposition: {disposition!r}"))
        elif disposition == "pending":
            pending += 1
            if data.get("status") != "in_progress":
                issues.append(_issue("error", candidate_ref, "finalized_run_complete", "pending candidate in non-in-progress run"))
            proposal = candidate.get("proposal")
            if proposal is not None:
                if not isinstance(proposal, dict) or proposal.get("review_status") != "agent_proposed" or proposal.get("relationship") not in RELATIONSHIP_TYPES or proposal.get("registry_target") not in relationships | broader_claims or not _nonempty(proposal.get("rationale")):
                    issues.append(_issue("error", candidate_ref, "proposal_valid", "proposal requires agent_proposed status, relationship, registry target, and rationale"))
        elif disposition == "accepted":
            reviewed = True
            relation = candidate.get("relationship")
            target_id = candidate.get("registry_target")
            if relation not in RELATIONSHIP_TYPES or not _nonempty(candidate.get("rationale")) or target_id not in relationships | broader_claims:
                issues.append(_issue("error", candidate_ref, "accepted_decisions_reciprocal", "accepted candidate requires relationship, rationale, and registry target"))
            elif target_id in relationships:
                target = relationships[target_id]
                if {target.get("source"), target.get("target")} != {left, right} or target.get("type") != relation:
                    issues.append(_issue("error", candidate_ref, "accepted_decisions_reciprocal", "candidate does not match relationship target"))
            else:
                members = {member.get("claim") for member in broader_claims[target_id].get("members") or [] if isinstance(member, dict)}
                if not {left, right}.issubset(members):
                    issues.append(_issue("error", candidate_ref, "accepted_decisions_reciprocal", "candidate endpoints are not both members of broader target"))
            if target_id in relationships | broader_claims and data.get("review_mode") == "human_review" and (relationships | broader_claims)[target_id].get("review_status") != "human_approved":
                issues.append(_issue("error", candidate_ref, "human_approval_required", "accepted human-review decision must target a human_approved registry record"))
        elif disposition == "rejected":
            reviewed = True
            if not _nonempty(candidate.get("rationale")) or candidate.get("registry_target") is not None:
                issues.append(_issue("error", candidate_ref, "decision_valid", "rejected candidate requires rationale and no registry target"))
        elif disposition == "deferred":
            reviewed = True
            deferred += 1
            if not _nonempty(candidate.get("rationale")) or not _nonempty(candidate.get("reconsideration_trigger")):
                issues.append(_issue("error", candidate_ref, "decision_valid", "deferred candidate requires rationale and reconsideration trigger"))
    actual_order = [(-float((candidate.get("signals") or {}).get("aggregate_score", -1)), candidate.get("left"), candidate.get("right")) for candidate in candidates if isinstance(candidate, dict)]
    if actual_order != sorted(actual_order):
        issues.append(_issue("error", ref, "candidate_order_stable", "candidates are not sorted by score descending then qualified references"))
    diagnostics = data.get("diagnostics") or {}
    if diagnostics.get("emitted_candidates") != len(candidates):
        issues.append(_issue("error", ref, "diagnostics_consistent", "emitted_candidates does not match candidates length"))
    if diagnostics.get("cap_excluded_shared_evidence") is True:
        issues.append(_issue("error", ref, "shared_evidence_priority", "review cap excluded a shared-evidence candidate"))
    if reviewed and not isinstance(data.get("review"), dict):
        issues.append(_issue("error", ref, "review_provenance_required", "review block required after any reviewed disposition"))
    if data.get("status") == "finalized" and pending:
        issues.append(_issue("error", ref, "finalized_run_complete", f"finalized run has {pending} pending candidates"))
    if pending or deferred or high_similarity:
        issues.append(_issue("warning", ref, "unresolved_candidates", f"pending={pending}, deferred={deferred}, high_similarity={high_similarity}"))
    return issues


def _validate_snapshot(path: Path, data: dict, known_refs: set[str], known_papers: set[str]) -> list[Issue]:
    issues: list[Issue] = []
    snapshot_id = data.get("snapshot_id", path.stem)
    ref = f"snapshot:{snapshot_id}"
    required = {"schema_version", "snapshot_id", "period", "evidence_cutoff", "activity_window", "baseline_cutoff", "assessment_as_of", "assessment_mode", "status", "source", "included_papers", "baseline_papers", "activity_papers", "concepts", "broader_claims", "digest"}
    missing = _missing(data, required)
    if missing:
        issues.append(_issue("error", ref, "snapshot_required_fields", f"missing fields: {missing}"))
        return issues
    if data.get("schema_version") != 1 or snapshot_id != path.stem:
        issues.append(_issue("error", ref, "snapshot_identity", "schema_version must be 1 and snapshot_id must match filename"))
    if data.get("assessment_mode") != "retrospective" or data.get("status") not in {"draft", "published", "superseded"}:
        issues.append(_issue("error", ref, "snapshot_vocabulary", "invalid assessment_mode or status"))
    for field in ("evidence_cutoff", "baseline_cutoff", "assessment_as_of"):
        if _iso(data.get(field)) is None:
            issues.append(_issue("error", ref, "snapshot_dates_valid", f"{field} must be YYYY-MM-DD"))
    if data.get("digest") != canonical_digest(data, omit_digest=True):
        issues.append(_issue("error", ref, "snapshot_digest_valid", "snapshot digest does not recompute"))
    included = {str(item.get("id")) for item in data.get("included_papers") or [] if isinstance(item, dict)}
    if not included.issubset(known_papers):
        issues.append(_issue("error", ref, "snapshot_papers_valid", f"unknown included papers: {sorted(included - known_papers)}"))
    for concept in data.get("concepts") or []:
        for cluster in concept.get("claim_clusters") or [] if isinstance(concept, dict) else []:
            issues.extend(_validate_qualified_ref(cluster.get("ref"), known_refs, ref))
    return issues


def run(args: CheckArgs) -> ModuleResult:
    wiki_root = args.wiki_dir if args.wiki_dir else _DEFAULT_WIKI
    reconciliation_dir = wiki_root / "_claims" / "_reconciliation"
    issues: list[Issue] = []
    try:
        graphs = load_concept_graphs(wiki_root)
    except ValueError as exc:
        issues.append(_issue("error", "concepts", "concept_graphs_load", str(exc)))
        graphs = {}
    known_refs, clusters, known_papers = _concept_state(graphs)

    if not reconciliation_dir.is_dir():
        issues.append(_issue("warning", "reconciliation", "reconciliation_not_initialized", f"directory not found: {reconciliation_dir}"))
        stats = {"relationships": 0, "broader_claims": 0, "runs": 0, "snapshots": 0, "candidates": 0, "errors": 0, "warnings": 1}
        return ModuleResult(module="reconcile", passed=True, issues=issues, stats=stats)

    registry_path = reconciliation_dir / "registry.yaml"
    if not registry_path.exists():
        issues.append(_issue("error", "registry", "registry_exists", f"missing {registry_path}"))
        registry_data: dict = {}
        relationships: dict[str, dict] = {}
        broader_claims: dict[str, dict] = {}
    else:
        registry_data, parse_issues = _read_mapping(registry_path, "registry")
        issues.extend(parse_issues)
        if registry_data is None:
            registry_data = {}
            relationships, broader_claims = {}, {}
        else:
            registry_issues, relationships, broader_claims = _validate_registry(registry_data, known_refs, clusters, known_papers)
            issues.extend(registry_issues)

    run_paths = sorted((reconciliation_dir / "runs").glob("*.yaml")) if (reconciliation_dir / "runs").is_dir() else []
    snapshot_paths = sorted((reconciliation_dir / "snapshots").glob("*.yaml")) if (reconciliation_dir / "snapshots").is_dir() else []
    if args.reconciliation_id:
        run_paths = [path for path in run_paths if path.stem == args.reconciliation_id]
        snapshot_paths = [path for path in snapshot_paths if path.stem == args.reconciliation_id]
        if not run_paths and not snapshot_paths:
            issues.append(_issue("error", args.reconciliation_id, "reconciliation_id_exists", "no matching run or snapshot"))

    candidates = 0
    run_ids: set[str] = set()
    for path in run_paths:
        data, parse_issues = _read_mapping(path, f"run:{path.stem}")
        issues.extend(parse_issues)
        if data is None:
            continue
        if path.stem in run_ids:
            issues.append(_issue("error", path.stem, "run_ids_unique", "duplicate run id"))
        run_ids.add(path.stem)
        candidates += len(data.get("candidates") or [])
        issues.extend(_validate_run(path, data, graphs, known_refs, relationships, broader_claims))

    for path in snapshot_paths:
        data, parse_issues = _read_mapping(path, f"snapshot:{path.stem}")
        issues.extend(parse_issues)
        if data is not None:
            issues.extend(_validate_snapshot(path, data, known_refs, known_papers))

    errors = sum(issue.severity == "error" for issue in issues)
    warnings = sum(issue.severity == "warning" for issue in issues)
    stats = {
        "relationships": len(relationships),
        "broader_claims": len(broader_claims),
        "runs": len(run_paths),
        "snapshots": len(snapshot_paths),
        "candidates": candidates,
        "errors": errors,
        "warnings": warnings,
    }
    return ModuleResult(module="reconcile", passed=errors == 0, issues=issues, stats=stats)
