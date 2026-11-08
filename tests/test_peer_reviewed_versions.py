import json
import tempfile
import unittest
from pathlib import Path

import yaml

from lib.peer_reviewed_versions import (
    acceptance_comment_candidate,
    isca_peer_url,
    load_frozen_memberships,
)
from scripts.audit_peer_reviewed_versions import build_inventory, render_json


class PeerReviewedVersionTests(unittest.TestCase):
    def test_claim_membership_is_the_only_freeze_authority(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            wiki = Path(tmp)
            (wiki / "_claims" / "_reconciliation").mkdir(parents=True)
            (wiki / "_claims" / "a.yaml").write_text(
                yaml.safe_dump({"papers": [{"id": "p1"}, {"id": 123}]})
            )
            (wiki / "_claims" / "_reconciliation" / "snapshot.yaml").write_text(
                yaml.safe_dump({"papers": [{"id": "derived-only"}]})
            )
            self.assertEqual(load_frozen_memberships(wiki), {"123": ["a"], "p1": ["a"]})

    def test_submitted_comment_is_not_an_acceptance_candidate(self) -> None:
        candidate, venue = acceptance_comment_candidate(
            {"arxiv_comment": "Submitted to Interspeech 2026"}
        )
        self.assertFalse(candidate)
        self.assertEqual(venue, "Interspeech")

    def test_isca_url_requires_key_and_doi_year(self) -> None:
        self.assertEqual(
            isca_peer_url(
                {
                    "source_ids": {
                        "isca": "smith26_interspeech",
                        "doi": "10.21437/Interspeech.2026-1",
                    }
                }
            ),
            "https://www.isca-archive.org/interspeech_2026/smith26_interspeech.html",
        )
        self.assertIsNone(isca_peer_url({"source_ids": {"isca": "smith26_interspeech"}}))

    def test_inventory_is_deterministic_and_never_apply_ready_without_date(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            wiki = Path(tmp) / "wiki"
            (wiki / "_claims").mkdir(parents=True)
            (wiki / "_claims" / "concept.yaml").write_text(
                yaml.safe_dump({"papers": [{"id": "2601.00001"}]})
            )
            records = [
                {
                    "id": "2601.00001",
                    "title": "Example",
                    "status": "ingested",
                    "venue": "arXiv",
                    "venue_type": "preprint",
                    "published_date": "2026-01-01",
                    "url": "https://arxiv.org/abs/2601.00001",
                    "source_ids": {
                        "arxiv": "2601.00001",
                        "isca": "example26_interspeech",
                        "doi": "10.21437/Interspeech.2026-1",
                    },
                }
            ]
            first = render_json(build_inventory(records, wiki))
            second = render_json(build_inventory(list(reversed(records)), wiki))
            self.assertEqual(first, second)
            parsed = json.loads(first)
            entry = parsed["entries"][0]
            self.assertTrue(entry["frozen"])
            self.assertEqual(entry["frozen_concepts"], ["concept"])
            self.assertEqual(entry["readiness"], "unresolved")
            self.assertIn("peer_reviewed_date_missing", entry["readiness_issues"])


if __name__ == "__main__":
    unittest.main()
