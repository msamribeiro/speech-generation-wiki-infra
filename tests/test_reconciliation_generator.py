from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from lib.reconciliation import canonical_digest, stable_candidate_id
from scripts.generate_reconciliation_candidates import dump_yaml, generate_run


ROOT = Path(__file__).resolve().parents[1]


def _write_graph(path: Path, concept: str, cluster_id: str, claim: str, papers: list[str]) -> None:
    paper_rows = "\n".join(
        f'  - id: "{paper}"\n    published_date: "2025-08-01"' for paper in papers
    )
    supporting = ", ".join(f'"{paper}"' for paper in papers)
    path.write_text(
        f"""concept: {concept}
papers:
{paper_rows}
claim_clusters:
  - id: {cluster_id}
    claim: \"{claim}\"
    status: emerging
    supporting_papers: [{supporting}]
    contradicting_papers: []
    refining_papers: []
""",
        encoding="utf-8",
    )


class ReconciliationGeneratorTests(unittest.TestCase):
    def test_output_is_byte_stable_and_cross_concept(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            wiki = Path(directory)
            claims = wiki / "_claims"
            claims.mkdir()
            _write_graph(claims / "alpha.yaml", "alpha", "shared_claim", "Codec tokens improve speech quality", ["p1", "p2"])
            _write_graph(claims / "beta.yaml", "beta", "shared_claim", "Codec tokens improve generated speech quality", ["p1", "p2"])
            _write_graph(claims / "gamma.yaml", "gamma", "other_claim", "Streaming reduces response latency", ["p3"])

            kwargs = dict(
                wiki_dir=wiki,
                run_id="2025-Q3",
                trigger="quarterly-integration",
                evidence_cutoff="2025-09-30",
                assessment_as_of="2026-08-19",
                neighbors=1,
                review_cap=10,
                shared_support_minimum=2,
                infra_commit="abc1234",
                content_commit="def5678",
            )
            first, _ = generate_run(**kwargs)
            second, _ = generate_run(**kwargs)

            self.assertEqual(dump_yaml(first), dump_yaml(second))
            self.assertTrue(first["candidates"])
            for candidate in first["candidates"]:
                self.assertLess(candidate["left"], candidate["right"])
                self.assertNotEqual(candidate["left"].split("#")[0], candidate["right"].split("#")[0])
                self.assertEqual(candidate["id"], stable_candidate_id(candidate["left"], candidate["right"]))
            shared = next(item for item in first["candidates"] if item["left"].startswith("alpha#") and item["right"].startswith("beta#"))
            self.assertEqual(shared["signals"]["shared_supporting_papers"], ["p1", "p2"])
            self.assertFalse(first["diagnostics"]["cap_excluded_shared_evidence"])

    def test_shared_evidence_candidates_survive_a_smaller_cap(self) -> None:
        from lib.reconciliation import ClusterRecord
        from scripts.generate_reconciliation_candidates import PairScore, select_candidates

        def record(ref: str) -> ClusterRecord:
            concept, cluster_id = ref.split("#")
            return ClusterRecord(ref, concept, cluster_id, "claim", "emerging", (), (), (), (), ())

        pairs = []
        for number in range(2):
            left, right = record(f"alpha#c{number}"), record(f"beta#c{number}")
            pairs.append(PairScore(left, right, 0.1, 1.0, ("p1", "p2"), True, True, 1.0, 0.0, (), 0.4))
        selected, diagnostics = select_candidates(pairs, neighbors=1, review_cap=1, shared_support_minimum=2)
        self.assertEqual(len(selected), 2)
        self.assertFalse(diagnostics["cap_excluded_shared_evidence"])

    def test_canonical_digest_ignores_mapping_order(self) -> None:
        self.assertEqual(canonical_digest({"a": 1, "b": [2]}), canonical_digest({"b": [2], "a": 1}))


if __name__ == "__main__":
    unittest.main()
