#!/usr/bin/env python3
"""Materialize a deterministic publication-bounded reconciliation snapshot."""

from __future__ import annotations

import argparse
from datetime import date, datetime, timedelta
import json
from pathlib import Path
import re
import subprocess
import sys

import yaml


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib.reconciliation import canonical_digest, load_concept_graphs, load_yaml


class SnapshotError(RuntimeError):
    """Raised when a snapshot cannot be materialized safely."""


def _date_text(value: object, field: str) -> str:
    text = value.isoformat() if isinstance(value, (date, datetime)) else str(value or "")
    try:
        parsed = datetime.strptime(text, "%Y-%m-%d").date()
    except ValueError as exc:
        raise SnapshotError(f"{field} must be YYYY-MM-DD: {value!r}") from exc
    if parsed.isoformat() != text:
        raise SnapshotError(f"{field} must be canonical YYYY-MM-DD: {value!r}")
    return text


def _git_commit(path: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short=7", "HEAD"],
            cwd=path,
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError as exc:
        raise SnapshotError(f"cannot resolve git commit for {path}") from exc


def _git_clean(path: Path) -> bool:
    try:
        output = subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=path, text=True, stderr=subprocess.DEVNULL
        )
    except subprocess.CalledProcessError as exc:
        raise SnapshotError(f"cannot inspect git worktree for {path}") from exc
    return not output.strip()


def dump_yaml(data: dict) -> str:
    return yaml.safe_dump(
        data,
        allow_unicode=True,
        sort_keys=False,
        width=120,
        default_flow_style=False,
    )


FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _paper_frontmatter(wiki_dir: Path, paper_id: str) -> dict:
    path = wiki_dir / "papers" / f"{paper_id}.md"
    if not path.exists():
        raise SnapshotError(f"paper page does not exist: {paper_id}")
    match = FRONTMATTER_RE.match(path.read_text(encoding="utf-8"))
    if match is None:
        raise SnapshotError(f"paper page has no valid frontmatter: {paper_id}")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise SnapshotError(f"paper frontmatter is not a mapping: {paper_id}")
    return data


def _paper_catalog(wiki_dir: Path, graphs: dict[str, dict]) -> dict[str, dict]:
    catalog: dict[str, dict] = {}
    for concept, graph in sorted(graphs.items()):
        for paper in graph.get("papers") or []:
            if not isinstance(paper, dict) or not isinstance(paper.get("id"), str):
                raise SnapshotError(f"{concept}: every paper requires a string id")
            paper_id = paper["id"]
            published_date = _date_text(
                paper.get("published_date"), f"{concept}:{paper_id}:published_date"
            )
            frontmatter = _paper_frontmatter(wiki_dir, paper_id)
            canonical_date = _date_text(
                frontmatter.get("published_date"), f"papers/{paper_id}:published_date"
            )
            if published_date != canonical_date:
                raise SnapshotError(
                    f"{concept}:{paper_id}: published_date differs from canonical paper page"
                )
            venue = frontmatter.get("venue")
            if not isinstance(venue, str) or not venue.strip():
                raise SnapshotError(f"papers/{paper_id}: venue must be non-empty")
            current = catalog.setdefault(
                paper_id,
                {"id": paper_id, "published_date": published_date, "venue": venue, "concepts": []},
            )
            if current["published_date"] != published_date or current["venue"] != venue:
                raise SnapshotError(f"{paper_id}: conflicting canonical paper-page metadata")
            current["concepts"].append(concept)
    for paper in catalog.values():
        paper["concepts"] = sorted(set(paper["concepts"]))
    return catalog


def _bounded_assessment(cluster: dict, eligible: set[str]) -> dict | None:
    roles = {
        "supporting_papers": sorted(set(map(str, cluster.get("supporting_papers") or [])) & eligible),
        "contradicting_papers": sorted(
            set(map(str, cluster.get("contradicting_papers") or [])) & eligible
        ),
        "refining_papers": sorted(set(map(str, cluster.get("refining_papers") or [])) & eligible),
    }
    evidence_count = len(set().union(*map(set, roles.values())))
    if evidence_count == 0:
        return None

    live_status = cluster.get("status")
    if roles["contradicting_papers"]:
        status = "contested"
    elif live_status == "emerging":
        status = "emerging"
    else:
        status = "strongly_supported" if len(roles["supporting_papers"]) >= 3 else "emerging"

    confidence_order = {"low": 0, "medium": 1, "high": 2}
    evidence_confidence = "low" if evidence_count == 1 else "medium" if evidence_count == 2 else "high"
    live_confidence = cluster.get("confidence")
    if live_confidence not in confidence_order:
        raise SnapshotError(f"invalid live confidence: {live_confidence!r}")
    confidence = min(
        (evidence_confidence, live_confidence), key=lambda value: confidence_order[value]
    )
    return {"status": status, "confidence": confidence, **roles}


def _validate_runs(
    reconciliation_dir: Path,
    run_ids: list[str],
    graphs: dict[str, dict],
    registry: dict,
    evidence_cutoff: str,
) -> None:
    authoritative = {
        item["id"]: item
        for collection in (registry.get("relationships") or [], registry.get("broader_claims") or [])
        for item in collection
        if isinstance(item, dict) and item.get("review_status") == "human_approved"
    }
    current_digests = {concept: canonical_digest(graph) for concept, graph in sorted(graphs.items())}
    for run_id in run_ids:
        path = reconciliation_dir / "runs" / f"{run_id}.yaml"
        if not path.exists():
            raise SnapshotError(f"reconciliation run does not exist: {run_id}")
        run = load_yaml(path)
        if run.get("run_id") != run_id or run.get("status") != "finalized":
            raise SnapshotError(f"run must be finalized: {run_id}")
        if run.get("review_mode") != "human_review":
            raise SnapshotError(f"snapshot run must use human_review mode: {run_id}")
        if _date_text(run.get("evidence_cutoff"), f"{run_id}:evidence_cutoff") != evidence_cutoff:
            raise SnapshotError(f"run cutoff does not match snapshot cutoff: {run_id}")
        if run.get("source", {}).get("concept_digests") != current_digests:
            raise SnapshotError(f"run concept digests do not match current graphs: {run_id}")
        for candidate in run.get("candidates") or []:
            if candidate.get("disposition") == "pending":
                raise SnapshotError(f"finalized run contains a pending candidate: {run_id}")
            if candidate.get("disposition") == "accepted":
                target = authoritative.get(candidate.get("registry_target"))
                if target is None:
                    raise SnapshotError(
                        f"accepted candidate lacks human-approved target: {candidate.get('id')}"
                    )


def generate_snapshot(
    *,
    wiki_dir: Path,
    snapshot_id: str,
    period: str,
    evidence_cutoff: str,
    activity_start: str,
    activity_end: str,
    baseline_cutoff: str,
    assessment_as_of: str,
    run_ids: list[str],
    status: str = "draft",
    infra_commit: str | None = None,
    content_commit: str | None = None,
) -> dict:
    if status not in {"draft", "published"}:
        raise SnapshotError(f"unsupported generated snapshot status: {status}")
    dates = {
        name: _date_text(value, name)
        for name, value in {
            "evidence_cutoff": evidence_cutoff,
            "activity_start": activity_start,
            "activity_end": activity_end,
            "baseline_cutoff": baseline_cutoff,
            "assessment_as_of": assessment_as_of,
        }.items()
    }
    baseline_date = datetime.strptime(dates["baseline_cutoff"], "%Y-%m-%d").date()
    start_date = datetime.strptime(dates["activity_start"], "%Y-%m-%d").date()
    end_date = datetime.strptime(dates["activity_end"], "%Y-%m-%d").date()
    cutoff_date = datetime.strptime(dates["evidence_cutoff"], "%Y-%m-%d").date()
    if baseline_date + timedelta(days=1) != start_date or not start_date <= end_date <= cutoff_date:
        raise SnapshotError("quarterly boundaries must be contiguous and ordered")

    graphs = load_concept_graphs(wiki_dir)
    reconciliation_dir = wiki_dir / "_claims" / "_reconciliation"
    registry = load_yaml(reconciliation_dir / "registry.yaml")
    _validate_runs(reconciliation_dir, run_ids, graphs, registry, dates["evidence_cutoff"])
    catalog = _paper_catalog(wiki_dir, graphs)
    included_ids = {
        paper_id
        for paper_id, paper in catalog.items()
        if paper["published_date"] <= dates["evidence_cutoff"]
    }
    baseline_ids = {
        paper_id
        for paper_id in included_ids
        if catalog[paper_id]["published_date"] <= dates["baseline_cutoff"]
    }
    activity_ids = {
        paper_id
        for paper_id in included_ids
        if dates["activity_start"] <= catalog[paper_id]["published_date"] <= dates["activity_end"]
    }
    if baseline_ids | activity_ids != included_ids or baseline_ids & activity_ids:
        raise SnapshotError("baseline and activity papers must partition included papers")

    concepts: list[dict] = []
    cluster_by_ref: dict[str, dict] = {}
    for concept, graph in sorted(graphs.items()):
        graph_papers = {str(item["id"]) for item in graph.get("papers") or []}
        eligible = graph_papers & included_ids
        baseline = graph_papers & baseline_ids
        clusters = []
        for cluster in sorted(graph.get("claim_clusters") or [], key=lambda item: item["id"]):
            ref = f"{concept}#{cluster['id']}"
            cluster_by_ref[ref] = cluster
            clusters.append(
                {
                    "ref": ref,
                    "proposition": cluster["claim"],
                    "baseline_assessment": _bounded_assessment(cluster, baseline),
                    "cutoff_assessment": _bounded_assessment(cluster, eligible),
                    "caveats": list(cluster.get("caveats") or []),
                }
            )
        families = []
        for family in sorted(graph.get("method_families") or [], key=lambda item: item["id"]):
            family_papers = set(map(str, family.get("papers") or []))
            if not family_papers.issubset(graph_papers):
                raise SnapshotError(f"{concept}:{family['id']}: method family contains unknown papers")
            families.append(
                {
                    "id": family["id"],
                    "baseline_papers": sorted(family_papers & baseline_ids),
                    "cutoff_papers": sorted(family_papers & included_ids),
                }
            )
        concepts.append(
            {
                "concept": concept,
                "eligible_papers": sorted(eligible),
                "claim_clusters": clusters,
                "method_families": families,
            }
        )

    broader_claims = []
    for broader in sorted(registry.get("broader_claims") or [], key=lambda item: item["id"]):
        if broader.get("review_status") != "human_approved":
            continue
        members = sorted(member["claim"] for member in broader.get("members") or [])
        derived = {field: set() for field in ("supporting_papers", "contradicting_papers", "refining_papers")}
        for member in members:
            if member not in cluster_by_ref:
                raise SnapshotError(f"broader claim contains unknown member: {member}")
            cluster = cluster_by_ref[member]
            for field in derived:
                derived[field].update(map(str, cluster.get(field) or []))
        for field, papers in derived.items():
            if papers != set(map(str, broader.get(field) or [])):
                raise SnapshotError(f"{broader['id']}: {field} differs from member-derived evidence")
        bounded = {**broader, **{field: sorted(papers) for field, papers in derived.items()}}
        broader_claims.append(
            {
                "id": broader["id"],
                "proposition": broader["proposition"],
                "members": members,
                "baseline_assessment": _bounded_assessment(bounded, baseline_ids),
                "cutoff_assessment": _bounded_assessment(bounded, included_ids),
                "caveats": list(broader.get("caveats") or []),
            }
        )

    snapshot = {
        "schema_version": 1,
        "snapshot_id": snapshot_id,
        "period": period,
        "evidence_cutoff": dates["evidence_cutoff"],
        "activity_window": {"start": dates["activity_start"], "end": dates["activity_end"]},
        "baseline_cutoff": dates["baseline_cutoff"],
        "assessment_as_of": dates["assessment_as_of"],
        "assessment_mode": "retrospective",
        "status": status,
        "supersedes": None,
        "supersession_reason": None,
        "source": {
            "infra_commit": infra_commit or _git_commit(ROOT),
            "content_commit": content_commit or _git_commit(wiki_dir),
            "reconciliation_runs": list(run_ids),
            "registry_digest": canonical_digest(registry),
            "concept_digests": {
                concept: canonical_digest(graph) for concept, graph in sorted(graphs.items())
            },
        },
        "included_papers": [catalog[paper_id] for paper_id in sorted(included_ids)],
        "baseline_papers": sorted(baseline_ids),
        "activity_papers": sorted(activity_ids),
        "concepts": concepts,
        "broader_claims": broader_claims,
    }
    snapshot["digest"] = canonical_digest(snapshot, omit_digest=True)
    return snapshot


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wiki-dir", required=True, type=Path)
    parser.add_argument("--snapshot-id", required=True)
    parser.add_argument("--period", required=True)
    parser.add_argument("--evidence-cutoff", required=True)
    parser.add_argument("--activity-start", required=True)
    parser.add_argument("--activity-end", required=True)
    parser.add_argument("--baseline-cutoff", required=True)
    parser.add_argument("--assessment-as-of", required=True)
    parser.add_argument("--run-id", action="append", dest="run_ids", required=True)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--publish", action="store_true")
    args = parser.parse_args()

    wiki_dir = args.wiki_dir.resolve()
    path = wiki_dir / "_claims" / "_reconciliation" / "snapshots" / f"{args.snapshot_id}.yaml"
    try:
        if args.apply and (not _git_clean(ROOT) or not _git_clean(wiki_dir)):
            raise SnapshotError("draft creation requires clean infra and content worktrees")
        existing = load_yaml(path) if path.exists() else None
        if existing and existing.get("status") == "published" and not args.check:
            raise SnapshotError(f"refusing to modify published snapshot: {path}")

        requested_status = "published" if args.publish else (existing or {}).get("status", "draft")
        snapshot = generate_snapshot(
            wiki_dir=wiki_dir,
            snapshot_id=args.snapshot_id,
            period=args.period,
            evidence_cutoff=args.evidence_cutoff,
            activity_start=args.activity_start,
            activity_end=args.activity_end,
            baseline_cutoff=args.baseline_cutoff,
            assessment_as_of=args.assessment_as_of,
            run_ids=args.run_ids,
            status=requested_status,
        )
        rendered = dump_yaml(snapshot)
        if args.apply:
            if existing is not None:
                raise SnapshotError(f"refusing to overwrite existing snapshot: {path}")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(rendered, encoding="utf-8")
        elif args.check:
            if existing is None or path.read_text(encoding="utf-8") != rendered:
                raise SnapshotError(f"snapshot is not byte-reproducible: {path}")
        elif args.publish:
            if existing is None or existing.get("status") != "draft":
                raise SnapshotError("publish requires an existing draft snapshot")
            draft = generate_snapshot(
                wiki_dir=wiki_dir,
                snapshot_id=args.snapshot_id,
                period=args.period,
                evidence_cutoff=args.evidence_cutoff,
                activity_start=args.activity_start,
                activity_end=args.activity_end,
                baseline_cutoff=args.baseline_cutoff,
                assessment_as_of=args.assessment_as_of,
                run_ids=args.run_ids,
                status="draft",
            )
            if path.read_text(encoding="utf-8") != dump_yaml(draft):
                raise SnapshotError("draft changed since deterministic materialization")
            path.write_text(rendered, encoding="utf-8")
    except (OSError, ValueError, SnapshotError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "mode": "publish" if args.publish else "check" if args.check else "apply" if args.apply else "dry-run",
                "snapshot_id": snapshot["snapshot_id"],
                "status": snapshot["status"],
                "concepts": len(snapshot["concepts"]),
                "claim_clusters": sum(len(item["claim_clusters"]) for item in snapshot["concepts"]),
                "broader_claims": len(snapshot["broader_claims"]),
                "included_papers": len(snapshot["included_papers"]),
                "baseline_papers": len(snapshot["baseline_papers"]),
                "activity_papers": len(snapshot["activity_papers"]),
                "digest": snapshot["digest"],
                "path": str(path),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
