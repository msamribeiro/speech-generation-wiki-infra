from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from lib.reconciliation import canonical_digest
from scripts.freeze_reconciliation_snapshot import (
    SnapshotError,
    _bounded_assessment,
    generate_snapshot,
)


class SnapshotGeneratorTests(unittest.TestCase):
    def test_complete_boundary_preserves_reviewed_assessment(self) -> None:
        cluster = {
            "status": "strongly_supported",
            "confidence": "high",
            "supporting_papers": ["p0", "p1"],
            "contradicting_papers": ["p2"],
            "refining_papers": [],
        }
        complete = _bounded_assessment(cluster, {"p0", "p1", "p2"})
        filtered = _bounded_assessment(cluster, {"p0", "p2"})
        self.assertEqual(complete["status"], "strongly_supported")
        self.assertEqual(complete["confidence"], "high")
        self.assertEqual(filtered["status"], "contested")
        self.assertEqual(filtered["confidence"], "medium")

    def _wiki(self, directory: str) -> Path:
        wiki = Path(directory)
        claims = wiki / "_claims"
        recon = claims / "_reconciliation"
        (recon / "runs").mkdir(parents=True)
        (wiki / "papers").mkdir()
        graphs = {
            "alpha": {
                "concept": "alpha",
                "papers": [
                    {"id": "p0", "published_date": "2025-06-30", "venue": "A"},
                    {"id": "p1", "published_date": "2025-07-01", "venue": "B"},
                    {"id": "p2", "published_date": "2025-10-01", "venue": "C"},
                ],
                "claim_clusters": [{
                    "id": "claim", "claim": "A bounded claim", "status": "strongly_supported",
                    "confidence": "high", "supporting_papers": ["p0", "p1", "p2"],
                    "contradicting_papers": [], "refining_papers": [], "caveats": [],
                }],
                "method_families": [{"id": "family", "papers": ["p0", "p1", "p2"]}],
            },
            "beta": {
                "concept": "beta",
                "papers": [
                    {"id": "p0", "published_date": "2025-06-30", "venue": "A"},
                    {"id": "p1", "published_date": "2025-07-01", "venue": "B"},
                ],
                "claim_clusters": [{
                    "id": "claim", "claim": "A related bounded claim", "status": "emerging",
                    "confidence": "medium", "supporting_papers": ["p0", "p1"],
                    "contradicting_papers": [], "refining_papers": [], "caveats": [],
                }],
                "method_families": [],
            },
        }
        for concept, graph in graphs.items():
            (claims / f"{concept}.yaml").write_text(yaml.safe_dump(graph, sort_keys=False))
        for paper_id, published_date, venue in (
            ("p0", "2025-06-30", "A"),
            ("p1", "2025-07-01", "B"),
            ("p2", "2025-10-01", "C"),
        ):
            (wiki / "papers" / f"{paper_id}.md").write_text(
                f'---\nid: "{paper_id}"\npublished_date: "{published_date}"\nvenue: {venue}\n---\n'
            )
        registry = {
            "schema_version": 1,
            "last_updated": "2026-09-12",
            "relationships": [],
            "broader_claims": [{
                "id": "broader_claim", "proposition": "The broader claim", "status": "strongly_supported",
                "confidence": "high", "review_status": "human_approved",
                "members": [
                    {"claim": "alpha#claim", "relationship": "supports", "rationale": "Alpha support."},
                    {"claim": "beta#claim", "relationship": "supports", "rationale": "Beta support."},
                ],
                "supporting_papers": ["p0", "p1", "p2"], "contradicting_papers": [],
                "refining_papers": [], "caveats": [], "review_rationale": "Reviewed.",
                "evidence_cutoff": "2025-09-30", "assessment_date": "2026-09-12",
                "reviewed_in": "review",
            }],
        }
        (recon / "registry.yaml").write_text(yaml.safe_dump(registry, sort_keys=False))
        run = {
            "schema_version": 1, "run_id": "review", "review_mode": "human_review",
            "status": "finalized", "evidence_cutoff": "2025-09-30",
            "source": {"concept_digests": {k: canonical_digest(v) for k, v in sorted(graphs.items())}},
            "candidates": [],
        }
        (recon / "runs/review.yaml").write_text(yaml.safe_dump(run, sort_keys=False))
        return wiki

    def test_materialization_is_deterministic_and_filters_cutoff(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            wiki = self._wiki(directory)
            kwargs = dict(
                wiki_dir=wiki, snapshot_id="2025-Q3", period="2025-Q3",
                evidence_cutoff="2025-09-30", activity_start="2025-07-01",
                activity_end="2025-09-30", baseline_cutoff="2025-06-30",
                assessment_as_of="2026-09-12", run_ids=["review"],
                infra_commit="abc1234", content_commit="def5678",
            )
            first = generate_snapshot(**kwargs)
            second = generate_snapshot(**kwargs)
            self.assertEqual(first, second)
            self.assertEqual(first["baseline_papers"], ["p0"])
            self.assertEqual(first["activity_papers"], ["p1"])
            self.assertNotIn("p2", {p["id"] for p in first["included_papers"]})
            assessment = first["concepts"][0]["claim_clusters"][0]
            self.assertEqual(assessment["baseline_assessment"]["confidence"], "low")
            self.assertEqual(assessment["cutoff_assessment"]["confidence"], "medium")
            self.assertEqual(first["digest"], canonical_digest(first, omit_digest=True))

    def test_run_must_be_finalized_human_review(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            wiki = self._wiki(directory)
            path = wiki / "_claims/_reconciliation/runs/review.yaml"
            run = yaml.safe_load(path.read_text())
            run["review_mode"] = "agent_adjudication"
            path.write_text(yaml.safe_dump(run, sort_keys=False))
            with self.assertRaisesRegex(SnapshotError, "human_review"):
                generate_snapshot(
                    wiki_dir=wiki, snapshot_id="2025-Q3", period="2025-Q3",
                    evidence_cutoff="2025-09-30", activity_start="2025-07-01",
                    activity_end="2025-09-30", baseline_cutoff="2025-06-30",
                    assessment_as_of="2026-09-12", run_ids=["review"],
                    infra_commit="abc1234", content_commit="def5678",
                )


if __name__ == "__main__":
    unittest.main()
