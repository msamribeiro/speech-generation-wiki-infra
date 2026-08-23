from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from checks._base import CheckArgs
from checks import reconcile
from lib.reconciliation import canonical_digest, stable_candidate_id


class ReconcileHealthTests(unittest.TestCase):
    def _wiki(self, directory: str) -> tuple[Path, dict[str, dict]]:
        wiki = Path(directory)
        claims = wiki / "_claims"
        recon = claims / "_reconciliation"
        (recon / "runs").mkdir(parents=True)
        graphs = {
            "alpha": {
                "concept": "alpha",
                "papers": [{"id": "p1", "published_date": "2025-08-01"}],
                "claim_clusters": [{"id": "claim", "claim": "Codec tokens improve quality", "status": "emerging", "supporting_papers": ["p1"], "contradicting_papers": [], "refining_papers": []}],
            },
            "beta": {
                "concept": "beta",
                "papers": [{"id": "p1", "published_date": "2025-08-01"}],
                "claim_clusters": [{"id": "claim", "claim": "Codec tokens improve speech quality", "status": "emerging", "supporting_papers": ["p1"], "contradicting_papers": [], "refining_papers": []}],
            },
        }
        for concept, graph in graphs.items():
            (claims / f"{concept}.yaml").write_text(yaml.safe_dump(graph, sort_keys=False), encoding="utf-8")
        registry = {"schema_version": 1, "last_updated": "2026-08-19", "relationships": [], "broader_claims": []}
        (recon / "registry.yaml").write_text(yaml.safe_dump(registry, sort_keys=False), encoding="utf-8")
        return wiki, graphs

    def _run(self, graphs: dict[str, dict]) -> dict:
        left, right = "alpha#claim", "beta#claim"
        return {
            "schema_version": 1, "run_id": "2025-Q3", "trigger": "quarterly-integration",
            "evidence_cutoff": "2025-09-30", "assessment_as_of": "2026-08-19",
            "status": "in_progress", "supersedes_run": None,
            "review_mode": "human_review",
            "source": {"infra_commit": "abc1234", "content_commit": "def5678", "concept_digests": {key: canonical_digest(value) for key, value in graphs.items()}},
            "generator": {"version": 1, "neighbors_per_cluster": 10, "review_cap": 500, "shared_support_minimum": 2, "weights": {"text_similarity": 0.4, "shared_evidence": 0.3, "status_polarity": 0.15, "technical_vocabulary": 0.15}},
            "diagnostics": {"cross_concept_pairs": 1, "pre_cap_candidates": 1, "emitted_candidates": 1, "shared_evidence_candidates": 0, "score_distribution": {"minimum": 0.7, "median": 0.7, "maximum": 0.7}, "cap_excluded_shared_evidence": False},
            "candidates": [{"id": stable_candidate_id(left, right), "left": left, "right": right, "theme": "codecs-language-modeling", "signals": {"text_similarity": 0.7, "shared_evidence_score": 1.0, "shared_supporting_papers": ["p1"], "status_compatible": True, "polarity_compatible": True, "status_polarity_score": 1.0, "technical_vocabulary_score": 0.5, "shared_terms": ["codec", "quality", "tokens"], "aggregate_score": 0.7}, "disposition": "pending", "relationship": None, "registry_target": None, "rationale": None, "reconsideration_trigger": None}],
        }

    def test_valid_in_progress_run_passes_with_warning(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            wiki, graphs = self._wiki(directory)
            run = self._run(graphs)
            (wiki / "_claims/_reconciliation/runs/2025-Q3.yaml").write_text(yaml.safe_dump(run, sort_keys=False), encoding="utf-8")
            result = reconcile.run(CheckArgs(wiki_dir=wiki))
            self.assertTrue(result.passed, [issue.message for issue in result.issues])
            self.assertEqual(result.stats["errors"], 0)
            self.assertEqual(result.stats["warnings"], 1)

    def test_broken_reference_and_finalized_pending_are_errors(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            wiki, graphs = self._wiki(directory)
            run = self._run(graphs)
            run["status"] = "finalized"
            run["candidates"][0]["right"] = "beta#missing"
            (wiki / "_claims/_reconciliation/runs/2025-Q3.yaml").write_text(yaml.safe_dump(run, sort_keys=False), encoding="utf-8")
            result = reconcile.run(CheckArgs(wiki_dir=wiki))
            checks = {issue.check for issue in result.issues if issue.severity == "error"}
            self.assertFalse(result.passed)
            self.assertIn("qualified_refs_resolve", checks)
            self.assertIn("finalized_run_complete", checks)

    def test_human_acceptance_requires_human_approved_registry_target(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            wiki, graphs = self._wiki(directory)
            left, right = "alpha#claim", "beta#claim"
            registry = yaml.safe_load((wiki / "_claims/_reconciliation/registry.yaml").read_text())
            registry["relationships"] = [{
                "id": "rel_claims", "source": left, "target": right, "type": "related",
                "rationale": "Both claims concern codec-token quality, but retain concept-specific scope.",
                "review_status": "agent_proposed", "reviewed_on": "2026-08-23", "accepted_in": "2025-Q3",
            }]
            (wiki / "_claims/_reconciliation/registry.yaml").write_text(yaml.safe_dump(registry, sort_keys=False))
            run = self._run(graphs)
            run["status"] = "finalized"
            run["candidates"][0].update({
                "disposition": "accepted", "relationship": "related", "registry_target": "rel_claims",
                "rationale": "A human accepted the proposed related relationship.",
            })
            run["review"] = {"completed_on": "2026-08-23"}
            (wiki / "_claims/_reconciliation/runs/2025-Q3.yaml").write_text(yaml.safe_dump(run, sort_keys=False))
            result = reconcile.run(CheckArgs(wiki_dir=wiki))
            self.assertIn("human_approval_required", {issue.check for issue in result.issues if issue.severity == "error"})


if __name__ == "__main__":
    unittest.main()
