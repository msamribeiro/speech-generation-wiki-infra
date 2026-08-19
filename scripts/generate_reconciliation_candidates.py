#!/usr/bin/env python3
"""Generate a deterministic, advisory cross-concept reconciliation review queue."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import statistics
import subprocess
import sys

import yaml


ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib.reconciliation import (
    ClusterRecord,
    canonical_digest,
    classify_theme,
    cluster_records,
    cosine,
    jaccard,
    load_concept_graphs,
    polarity_compatible,
    stable_candidate_id,
    status_compatible,
    tfidf_vectors,
)


DEFAULT_WEIGHTS = {
    "text_similarity": 0.40,
    "shared_evidence": 0.30,
    "status_polarity": 0.15,
    "technical_vocabulary": 0.15,
}


class GenerationError(RuntimeError):
    """Raised when candidate generation cannot proceed deterministically."""


@dataclass(frozen=True)
class PairScore:
    left: ClusterRecord
    right: ClusterRecord
    text_similarity: float
    shared_evidence_score: float
    shared_supporting_papers: tuple[str, ...]
    status_compatible: bool
    polarity_compatible: bool
    status_polarity_score: float
    technical_vocabulary_score: float
    shared_terms: tuple[str, ...]
    aggregate_score: float

    @property
    def key(self) -> tuple[str, str]:
        return self.left.ref, self.right.ref


def _round(value: float) -> float:
    return round(value + 0.0, 6)


def _git_commit(path: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short=7", "HEAD"], cwd=path, text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except subprocess.CalledProcessError as exc:
        raise GenerationError(f"cannot resolve git commit for {path}") from exc


def _git_clean(path: Path) -> bool:
    try:
        output = subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=path, text=True,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as exc:
        raise GenerationError(f"cannot inspect git worktree for {path}") from exc
    return not output.strip()


def _validate_date(value: str, name: str) -> str:
    try:
        parsed = datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise GenerationError(f"{name} must be YYYY-MM-DD: {value!r}") from exc
    if parsed.strftime("%Y-%m-%d") != value:
        raise GenerationError(f"{name} must be canonical YYYY-MM-DD: {value!r}")
    return value


def _validate_published_dates(graphs: dict[str, dict], cutoff: str) -> None:
    cutoff_date = datetime.strptime(cutoff, "%Y-%m-%d").date()
    for concept, data in graphs.items():
        for paper in data.get("papers") or []:
            pid = paper.get("id", "?")
            value = paper.get("published_date")
            text = value.isoformat() if hasattr(value, "isoformat") else str(value or "")
            _validate_date(text, f"{concept}:{pid}:published_date")
            if datetime.strptime(text, "%Y-%m-%d").date() > cutoff_date:
                raise GenerationError(
                    f"{concept}:{pid}: published_date {text} exceeds evidence cutoff {cutoff}"
                )


def score_pairs(
    records: list[ClusterRecord], weights: dict[str, float]
) -> list[PairScore]:
    vectors = tfidf_vectors(records)
    pairs: list[PairScore] = []
    for index, left in enumerate(records):
        for right in records[index + 1:]:
            if left.concept == right.concept:
                continue
            shared_papers = tuple(sorted(set(left.supporting_papers) & set(right.supporting_papers)))
            shared_terms = tuple(sorted(set(left.technical_terms) & set(right.technical_terms)))
            text_score = cosine(vectors[left.ref], vectors[right.ref])
            evidence_score = jaccard(left.supporting_papers, right.supporting_papers)
            status_ok = status_compatible(left, right)
            polarity_ok = polarity_compatible(left, right)
            status_score = (float(status_ok) + float(polarity_ok)) / 2
            technical_score = jaccard(left.technical_terms, right.technical_terms)
            aggregate = (
                weights["text_similarity"] * text_score
                + weights["shared_evidence"] * evidence_score
                + weights["status_polarity"] * status_score
                + weights["technical_vocabulary"] * technical_score
            )
            pairs.append(PairScore(
                left=left,
                right=right,
                text_similarity=_round(text_score),
                shared_evidence_score=_round(evidence_score),
                shared_supporting_papers=shared_papers,
                status_compatible=status_ok,
                polarity_compatible=polarity_ok,
                status_polarity_score=_round(status_score),
                technical_vocabulary_score=_round(technical_score),
                shared_terms=shared_terms,
                aggregate_score=_round(aggregate),
            ))
    return pairs


def select_candidates(
    pairs: list[PairScore], *, neighbors: int, review_cap: int, shared_support_minimum: int
) -> tuple[list[PairScore], dict]:
    by_ref: dict[str, list[PairScore]] = {}
    for pair in pairs:
        by_ref.setdefault(pair.left.ref, []).append(pair)
        by_ref.setdefault(pair.right.ref, []).append(pair)

    selected_keys: set[tuple[str, str]] = set()
    for ref in sorted(by_ref):
        ranked = sorted(
            by_ref[ref],
            key=lambda pair: (-pair.aggregate_score, pair.left.ref, pair.right.ref),
        )
        selected_keys.update(pair.key for pair in ranked[:neighbors])

    shared_pairs = {
        pair.key for pair in pairs
        if len(pair.shared_supporting_papers) >= shared_support_minimum
    }
    selected_keys.update(shared_pairs)
    pre_cap = [pair for pair in pairs if pair.key in selected_keys]
    ranked_pre_cap = sorted(
        pre_cap,
        key=lambda pair: (-pair.aggregate_score, pair.left.ref, pair.right.ref),
    )
    # The nominal cap limits ranking-only candidates. Evidence-backed candidates are
    # never discarded, even when they cause the review queue to exceed that cap.
    selected_keys_after_cap = set(shared_pairs)
    remaining_slots = max(0, review_cap - len(selected_keys_after_cap))
    for pair in ranked_pre_cap:
        if pair.key in selected_keys_after_cap:
            continue
        if remaining_slots == 0:
            break
        selected_keys_after_cap.add(pair.key)
        remaining_slots -= 1
    selected = [pair for pair in pre_cap if pair.key in selected_keys_after_cap]
    selected = sorted(
        selected,
        key=lambda pair: (-pair.aggregate_score, pair.left.ref, pair.right.ref),
    )
    scores = [pair.aggregate_score for pair in pre_cap]
    diagnostics = {
        "cross_concept_pairs": len(pairs),
        "pre_cap_candidates": len(pre_cap),
        "emitted_candidates": len(selected),
        "shared_evidence_candidates": len(shared_pairs),
        "score_distribution": {
            "minimum": _round(min(scores)) if scores else 0.0,
            "median": _round(statistics.median(scores)) if scores else 0.0,
            "maximum": _round(max(scores)) if scores else 0.0,
        },
        "cap_excluded_shared_evidence": bool(shared_pairs - selected_keys_after_cap),
    }
    return selected, diagnostics


def candidate_mapping(pair: PairScore) -> dict:
    return {
        "id": stable_candidate_id(pair.left.ref, pair.right.ref),
        "left": pair.left.ref,
        "right": pair.right.ref,
        "theme": classify_theme(pair.left, pair.right),
        "signals": {
            "text_similarity": pair.text_similarity,
            "shared_evidence_score": pair.shared_evidence_score,
            "shared_supporting_papers": list(pair.shared_supporting_papers),
            "status_compatible": pair.status_compatible,
            "polarity_compatible": pair.polarity_compatible,
            "status_polarity_score": pair.status_polarity_score,
            "technical_vocabulary_score": pair.technical_vocabulary_score,
            "shared_terms": list(pair.shared_terms),
            "aggregate_score": pair.aggregate_score,
        },
        "disposition": "pending",
        "relationship": None,
        "registry_target": None,
        "rationale": None,
        "reconsideration_trigger": None,
    }


def generate_run(
    *,
    wiki_dir: Path,
    run_id: str,
    trigger: str,
    evidence_cutoff: str,
    assessment_as_of: str,
    neighbors: int,
    review_cap: int,
    shared_support_minimum: int,
    weights: dict[str, float] | None = None,
    infra_commit: str | None = None,
    content_commit: str | None = None,
) -> tuple[dict, dict]:
    weights = dict(weights or DEFAULT_WEIGHTS)
    if set(weights) != set(DEFAULT_WEIGHTS) or abs(sum(weights.values()) - 1.0) > 1e-9:
        raise GenerationError("generator weights must contain the four canonical components and sum to 1")
    _validate_date(evidence_cutoff, "evidence_cutoff")
    _validate_date(assessment_as_of, "assessment_as_of")
    graphs = load_concept_graphs(wiki_dir)
    _validate_published_dates(graphs, evidence_cutoff)
    records = cluster_records(graphs)
    pairs = score_pairs(records, weights)
    selected, diagnostics = select_candidates(
        pairs,
        neighbors=neighbors,
        review_cap=review_cap,
        shared_support_minimum=shared_support_minimum,
    )
    run = {
        "schema_version": 1,
        "run_id": run_id,
        "trigger": trigger,
        "evidence_cutoff": evidence_cutoff,
        "assessment_as_of": assessment_as_of,
        "status": "in_progress",
        "supersedes_run": None,
        "source": {
            "infra_commit": infra_commit or _git_commit(ROOT),
            "content_commit": content_commit or _git_commit(wiki_dir),
            "concept_digests": {
                concept: canonical_digest(data) for concept, data in sorted(graphs.items())
            },
        },
        "generator": {
            "version": 1,
            "neighbors_per_cluster": neighbors,
            "review_cap": review_cap,
            "shared_support_minimum": shared_support_minimum,
            "weights": weights,
        },
        "diagnostics": diagnostics,
        "candidates": [candidate_mapping(pair) for pair in selected],
    }
    registry = {
        "schema_version": 1,
        "last_updated": assessment_as_of,
        "relationships": [],
        "broader_claims": [],
    }
    return run, registry


def dump_yaml(data: dict) -> str:
    return yaml.safe_dump(
        data,
        allow_unicode=True,
        sort_keys=False,
        width=120,
        default_flow_style=False,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wiki-dir", type=Path, required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--trigger", choices=["quarterly-integration", "large-integration-round", "corrective-review"], required=True)
    parser.add_argument("--evidence-cutoff", required=True)
    parser.add_argument("--assessment-as-of", required=True)
    parser.add_argument("--neighbors", type=int, default=10)
    parser.add_argument("--review-cap", type=int, default=500)
    parser.add_argument("--shared-support-minimum", type=int, default=2)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    wiki_dir = args.wiki_dir.resolve()
    try:
        if args.apply:
            dirty = [str(path) for path in (ROOT, wiki_dir) if not _git_clean(path)]
            if dirty:
                raise GenerationError(
                    f"apply requires clean infra and content worktrees: {', '.join(dirty)}"
                )
        run, registry = generate_run(
            wiki_dir=wiki_dir,
            run_id=args.run_id,
            trigger=args.trigger,
            evidence_cutoff=args.evidence_cutoff,
            assessment_as_of=args.assessment_as_of,
            neighbors=args.neighbors,
            review_cap=args.review_cap,
            shared_support_minimum=args.shared_support_minimum,
        )
    except (GenerationError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    reconciliation_dir = wiki_dir / "_claims" / "_reconciliation"
    registry_path = reconciliation_dir / "registry.yaml"
    run_path = reconciliation_dir / "runs" / f"{args.run_id}.yaml"
    if args.apply:
        if registry_path.exists() or run_path.exists():
            print("ERROR: refusing to overwrite existing registry or run record", file=sys.stderr)
            return 1
        run_path.parent.mkdir(parents=True, exist_ok=True)
        (reconciliation_dir / "snapshots").mkdir(parents=True, exist_ok=True)
        registry_path.write_text(dump_yaml(registry), encoding="utf-8")
        run_path.write_text(dump_yaml(run), encoding="utf-8")

    print(json.dumps({
        "mode": "apply" if args.apply else "dry-run",
        "run_id": args.run_id,
        "concepts": len(run["source"]["concept_digests"]),
        "cross_concept_pairs": run["diagnostics"]["cross_concept_pairs"],
        "pre_cap_candidates": run["diagnostics"]["pre_cap_candidates"],
        "emitted_candidates": run["diagnostics"]["emitted_candidates"],
        "shared_evidence_candidates": run["diagnostics"]["shared_evidence_candidates"],
        "cap_excluded_shared_evidence": run["diagnostics"]["cap_excluded_shared_evidence"],
        "registry_path": str(registry_path),
        "run_path": str(run_path),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
