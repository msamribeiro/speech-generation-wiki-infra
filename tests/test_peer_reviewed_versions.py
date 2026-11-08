import json
import tempfile
import unittest
from pathlib import Path

import yaml

from lib.paper_dates import apply_date_rule
from lib.peer_reviewed_versions import (
    acceptance_comment_candidate,
    isca_peer_url,
    load_frozen_memberships,
)
from scripts.audit_peer_reviewed_versions import build_inventory, render_json
from scripts.migrate_peer_reviewed_versions import (
    NOTE_MARKER,
    render_manifest,
    transform_index,
    transform_page,
)
from scripts.checks.metadata import _check as check_metadata


class PeerReviewedVersionTests(unittest.TestCase):
    def test_page_and_index_transform_are_idempotent(self) -> None:
        page = """---
id: "2601.00001"
organization: "Example"
venue: arXiv
venue_type: preprint
year: 2026
month: 1
published_date: 2026-01-05
url: "https://arxiv.org/abs/2601.00001"
---

> [!abstract] arXiv · 2026 · Preprint
> **A. Author** · [→ Paper](https://arxiv.org/abs/2601.00001) · Demo: ?
>
> Summary.

## Problem

Text.
"""
        entry = {
            "venue": "ICASSP",
            "venue_type": "conference",
            "conference_date": "2026-05-03",
            "url": "https://ieeexplore.ieee.org/document/1/",
        }
        once = transform_page(page, entry, frozen=False)
        twice = transform_page(once, entry, frozen=False)
        self.assertEqual(once, twice)
        self.assertIn("published_date: \"2026-05-03\"", once)
        self.assertIn("[!abstract] ICASSP · 2026 · Conference", once)
        self.assertEqual(once.count(NOTE_MARKER), 1)
        index = "| [[2601.00001]] | [Title](papers/2601.00001.md) | Org | arXiv | 2026 | TTS | — |\n"
        changed = transform_index(index, "2601.00001", entry, frozen=False)
        self.assertEqual(transform_index(changed, "2601.00001", entry, frozen=False), changed)
        self.assertIn("| ICASSP | 2026 |", changed)

    def test_frozen_page_keeps_summarized_venue(self) -> None:
        page = """---
id: "p1"
organization: "Example"
venue: arXiv
venue_type: preprint
year: 2025
month: 9
published_date: 2025-09-01
url: "https://arxiv.org/abs/p1"
---

> [!abstract] arXiv · 2025 · Preprint
> **A. Author** · [→ Paper](https://arxiv.org/abs/p1)
>
> Summary.

## Problem
"""
        entry = {
            "venue": "Interspeech",
            "venue_type": "conference",
            "conference_date": "2026-09-27",
            "url": "https://www.isca-archive.org/example.html",
        }
        changed = transform_page(page, entry, frozen=True)
        self.assertIn("venue: arXiv", changed)
        self.assertIn('peer_reviewed_venue: "Interspeech"', changed)
        self.assertIn("[!abstract] arXiv · 2025 · Preprint", changed)

    def test_manifest_is_deterministic(self) -> None:
        plan = [{"id": "p1", "metadata_changed": True, "page_changed": True,
                 "index_changed": True, "frozen": False,
                 "old": {"quarter": "2026-Q1"}, "new": {"quarter": "2026-Q2"}}]
        overrides = {"scope": "test", "deferred": []}
        self.assertEqual(render_manifest(plan, overrides), render_manifest(list(plan), overrides))

    def test_metadata_mismatch_requires_claim_membership_to_freeze(self) -> None:
        record = {
            "published_date": "2025-09-01",
            "year": 2025,
            "month": 9,
            "preprint_date": "2025-09-01",
            "version_date": "2025-09-01",
            "conference_date": "2026-09-27",
            "url_peer_reviewed": "https://www.isca-archive.org/example.html",
            "peer_reviewed_venue": "Interspeech",
            "peer_reviewed_venue_type": "conference",
        }
        unfrozen = check_metadata("p1", record, "error")
        frozen = check_metadata("p1", record, "error", frozen_concepts=["concept"])
        self.assertTrue(any(issue.check == "published_date_rule" for issue in unfrozen))
        self.assertFalse(any(issue.check == "published_date_rule" for issue in frozen))

    def test_date_rule_can_preserve_integrated_date(self) -> None:
        record = {
            "published_date": "2025-09-15",
            "year": 2026,
            "month": 5,
            "conference_date": "2026-05-03",
        }
        self.assertTrue(apply_date_rule(record, preserve_published_date=True))
        self.assertEqual(record["published_date"], "2025-09-15")
        self.assertEqual(record["year"], 2025)
        self.assertEqual(record["month"], 9)

    def test_default_date_rule_moves_unintegrated_record(self) -> None:
        record = {
            "published_date": "2026-01-12",
            "year": 2026,
            "month": 1,
            "conference_date": "2026-05-03",
        }
        self.assertTrue(apply_date_rule(record))
        self.assertEqual(record["published_date"], "2026-05-03")
        self.assertEqual(record["month"], 5)

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
