from __future__ import annotations

from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "reconciliation"


class ReconciliationContractFixtureTests(unittest.TestCase):
    def test_contract_fixtures_parse_as_mappings(self) -> None:
        for path in sorted(FIXTURES.glob("*.yaml")):
            with self.subTest(path=path.name):
                data = yaml.safe_load(path.read_text())
                self.assertIsInstance(data, dict)
                self.assertEqual(data["schema_version"], 1)

    def test_qualified_reference_fixture_covers_duplicate_cluster_id(self) -> None:
        registry = yaml.safe_load((FIXTURES / "registry.yaml").read_text())
        relationship = registry["relationships"][0]
        self.assertEqual(relationship["source"].count("#"), 1)
        self.assertEqual(relationship["target"].count("#"), 1)
        self.assertNotEqual(
            relationship["source"].split("#", 1)[0],
            relationship["target"].split("#", 1)[0],
        )

    def test_finalized_run_has_no_pending_candidates(self) -> None:
        run = yaml.safe_load((FIXTURES / "run.yaml").read_text())
        self.assertEqual(run["status"], "finalized")
        self.assertNotIn("pending", {item["disposition"] for item in run["candidates"]})

    def test_snapshot_is_explicitly_retrospective(self) -> None:
        snapshot = yaml.safe_load((FIXTURES / "snapshot.yaml").read_text())
        self.assertEqual(snapshot["assessment_mode"], "retrospective")
        self.assertLessEqual(snapshot["activity_window"]["end"], snapshot["evidence_cutoff"])
        cluster = snapshot["concepts"][0]["claim_clusters"][0]
        self.assertIn("baseline_assessment", cluster)
        self.assertIn("cutoff_assessment", cluster)


if __name__ == "__main__":
    unittest.main()
