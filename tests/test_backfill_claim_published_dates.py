from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from backfill_claim_published_dates import MigrationError, build_plan


CLAIM_TEXT = """concept: example
last_updated: 2026-01-01
paper_count: 1
papers:
  - id: "2501.00001"
    entry_date: 2026-01-02
    year: 2025
    venue: arXiv
    relevance: high
    evidence_role: [core_evidence]
    current_role: active_evidence
    claims: []
claim_clusters: []
method_families: []
open_questions: []
trend_notes: []
"""


class BackfillClaimPublishedDatesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.infra = self.root / "infra"
        self.wiki = self.root / "wiki"
        (self.infra / "raw" / "metadata").mkdir(parents=True)
        (self.wiki / "papers").mkdir(parents=True)
        (self.wiki / "_claims").mkdir()
        (self.infra / "raw" / "metadata" / "2501.00001.json").write_text(
            json.dumps({"id": "2501.00001", "published_date": "2025-01-03"}),
            encoding="utf-8",
        )
        (self.wiki / "papers" / "2501.00001.md").write_text(
            '---\nid: "2501.00001"\npublished_date: 2025-01-03\n---\n',
            encoding="utf-8",
        )
        self.claim_path = self.wiki / "_claims" / "example.yaml"
        self.claim_path.write_text(CLAIM_TEXT, encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def test_plan_inserts_only_published_date_line(self) -> None:
        plan = build_plan(self.infra, self.wiki)[0]
        self.assertTrue(plan.changed)
        expected = CLAIM_TEXT.replace(
            '  - id: "2501.00001"\n',
            '  - id: "2501.00001"\n    published_date: "2025-01-03"\n',
        )
        self.assertEqual(plan.migrated, expected)
        self.assertEqual(yaml.safe_load(plan.migrated)["paper_count"], 1)

    def test_second_plan_is_idempotent(self) -> None:
        first = build_plan(self.infra, self.wiki)[0]
        self.claim_path.write_text(first.migrated, encoding="utf-8")
        second = build_plan(self.infra, self.wiki)[0]
        self.assertFalse(second.changed)

    def test_source_conflict_fails(self) -> None:
        page = self.wiki / "papers" / "2501.00001.md"
        page.write_text(page.read_text().replace("2025-01-03", "2025-01-04"))
        with self.assertRaisesRegex(MigrationError, "published_date conflict"):
            build_plan(self.infra, self.wiki)

    def test_existing_claim_conflict_fails(self) -> None:
        self.claim_path.write_text(
            CLAIM_TEXT.replace(
                '  - id: "2501.00001"\n',
                '  - id: "2501.00001"\n    published_date: "2025-01-04"\n',
            ),
            encoding="utf-8",
        )
        with self.assertRaisesRegex(MigrationError, "conflicts with canonical"):
            build_plan(self.infra, self.wiki)


if __name__ == "__main__":
    unittest.main()
