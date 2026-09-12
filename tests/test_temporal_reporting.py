from __future__ import annotations

from copy import deepcopy
import unittest

from lib.reconciliation import canonical_digest
from lib.temporal_reporting import (
    QUARTERLY_SECTIONS,
    quarterly_projection,
    select_venue_papers,
    trend_comparability,
    validate_published_snapshot,
    validate_quarterly_report,
    validate_trend_snapshots,
    validate_venue_synthesis_readiness,
    venue_projection,
)


def _snapshot() -> dict:
    snapshot = {
        "schema_version": 1,
        "snapshot_id": "2025-Q3",
        "period": "2025-Q3",
        "evidence_cutoff": "2025-09-30",
        "activity_window": {"start": "2025-07-01", "end": "2025-09-30"},
        "baseline_cutoff": "2025-06-30",
        "assessment_as_of": "2026-09-12",
        "assessment_mode": "retrospective",
        "status": "published",
        "supersedes": None,
        "supersession_reason": None,
        "source": {},
        "included_papers": [
            {"id": "old", "published_date": "2025-06-01", "venue": "ACL", "concepts": ["a"]},
            {"id": "new", "published_date": "2025-07-01", "venue": "Interspeech", "concepts": ["a", "b"]},
        ],
        "baseline_papers": ["old"],
        "activity_papers": ["new"],
        "concepts": [{
            "concept": "a",
            "eligible_papers": ["new", "old"],
            "claim_clusters": [{
                "ref": "a#claim",
                "proposition": "A claim",
                "baseline_assessment": {
                    "status": "emerging", "confidence": "low",
                    "supporting_papers": ["old"], "contradicting_papers": [], "refining_papers": [],
                },
                "cutoff_assessment": {
                    "status": "strongly_supported", "confidence": "medium",
                    "supporting_papers": ["new", "old"], "contradicting_papers": [], "refining_papers": [],
                },
                "caveats": [],
            }],
            "method_families": [{"id": "family", "baseline_papers": [], "cutoff_papers": ["new"]}],
        }],
        "broader_claims": [],
        "digest": None,
    }
    snapshot["digest"] = canonical_digest(snapshot, omit_digest=True)
    return snapshot


def _later_snapshot() -> dict:
    snapshot = deepcopy(_snapshot())
    snapshot.update({
        "snapshot_id": "2025-Q4",
        "period": "2025-Q4",
        "baseline_cutoff": "2025-09-30",
        "activity_window": {"start": "2025-10-01", "end": "2025-12-31"},
        "evidence_cutoff": "2025-12-31",
        "assessment_as_of": "2026-09-13",
        "baseline_papers": ["new", "old"],
        "activity_papers": [],
    })
    snapshot["digest"] = canonical_digest(snapshot, omit_digest=True)
    return snapshot


class TemporalReportingTests(unittest.TestCase):
    def test_quarterly_projection_separates_activity_from_knowledge_change(self) -> None:
        projection = quarterly_projection(_snapshot())

        self.assertEqual(projection["activity"]["paper_count"], 1)
        self.assertEqual(projection["activity"]["concept_membership_count"], 2)
        self.assertEqual(projection["activity"]["venue_counts"], {"Interspeech": 1})
        self.assertEqual(projection["knowledge_changes"]["strengthened_local_count"], 1)
        self.assertEqual(projection["knowledge_changes"]["new_local_count"], 0)
        self.assertEqual(len(projection["methods"]["new_families"]), 1)

    def test_snapshot_digest_mismatch_fails_before_projection(self) -> None:
        snapshot = deepcopy(_snapshot())
        snapshot["activity_papers"].append("not-included")

        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            validate_published_snapshot(snapshot)

    def test_non_published_snapshot_is_rejected(self) -> None:
        snapshot = _snapshot()
        snapshot["status"] = "draft"
        snapshot["digest"] = canonical_digest(snapshot, omit_digest=True)

        with self.assertRaisesRegex(ValueError, "must be published"):
            quarterly_projection(snapshot)

    def test_quarterly_report_is_bound_to_snapshot_and_citations(self) -> None:
        snapshot = _snapshot()
        sections = "\n".join(f"## {name}\n\nText." for name in QUARTERLY_SECTIONS)
        report = f'''---
title: "Test"
report_type: quarterly
period: 2025-Q3
activity_window: {{start: "2025-07-01", end: "2025-09-30"}}
baseline_cutoff: "2025-06-30"
evidence_cutoff: "2025-09-30"
assessment_as_of: "2026-09-12"
assessment_mode: retrospective
snapshot_id: 2025-Q3
snapshot_digest: "{snapshot['digest']}"
included_paper_count: 2
baseline_paper_count: 1
activity_paper_count: 1
concept_count: 1
concept_membership_count: 3
activity_concept_membership_count: 2
generation:
  schema_version: 2
  date: "2026-09-13"
  stage: report
  mode: quarterly
  runtime: codex
  provider: openai
  agent: speech-generation-report-agent
  model: "gpt-5"
  commit: "1234567"
---

This is a retrospective assessment. Attention is not evidence of adoption. [[new|New]].

{sections}
'''
        validate_quarterly_report(
            report,
            snapshot,
            reports_index="[[quarterly/2025-Q3|Q3]]",
            changelog="report | 2025-Q3",
        )

        outside = report.replace("[[new|New]]", "[[outside|Outside]]")
        with self.assertRaisesRegex(ValueError, "outside snapshot"):
            validate_quarterly_report(outside, snapshot)

    def test_quarterly_meta_sections_may_use_distinct_presentation(self) -> None:
        snapshot = _snapshot()
        narrative_sections = QUARTERLY_SECTIONS[1:-1]
        sections = "\n".join(f"## {name}\n\nText." for name in narrative_sections)
        report = f'''---
title: "Test"
report_type: quarterly
period: 2025-Q3
activity_window: {{start: "2025-07-01", end: "2025-09-30"}}
baseline_cutoff: "2025-06-30"
evidence_cutoff: "2025-09-30"
assessment_as_of: "2026-09-12"
assessment_mode: retrospective
snapshot_id: 2025-Q3
snapshot_digest: "{snapshot['digest']}"
included_paper_count: 2
baseline_paper_count: 1
activity_paper_count: 1
concept_count: 1
concept_membership_count: 3
activity_concept_membership_count: 2
generation:
  schema_version: 2
  date: "2026-09-13"
  stage: report
  mode: quarterly
  runtime: codex
  provider: openai
  agent: speech-generation-report-agent
  model: "gpt-5"
  commit: "1234567"
---

> [!note] About this report
> **Scope and retrospective assessment.** Attention is not evidence of adoption. [[new|New]].

{sections}

<details>
<summary><strong>Snapshot and provenance references</strong></summary>

Technical metadata.

</details>
'''
        validate_quarterly_report(report, snapshot)

    def test_trend_requires_two_snapshots_and_increasing_cutoffs(self) -> None:
        first = _snapshot()
        second = _later_snapshot()

        with self.assertRaisesRegex(ValueError, "at least two"):
            validate_trend_snapshots([first])
        with self.assertRaisesRegex(ValueError, "increasing evidence cutoff"):
            validate_trend_snapshots([second, first])

        comparison = trend_comparability([first, second])
        self.assertEqual(comparison[0]["from_snapshot"], "2025-Q3")
        self.assertEqual(comparison[0]["to_snapshot"], "2025-Q4")
        self.assertEqual(comparison[0]["shared_concepts"], ["a"])
        self.assertEqual(comparison[0]["shared_local_claim_refs"], ["a#claim"])

    def test_venue_selection_uses_canonical_name_and_inclusive_dates(self) -> None:
        snapshot = _snapshot()
        selected = select_venue_papers(
            snapshot,
            venue="Interspeech",
            start="2025-07-01",
            end="2025-07-01",
        )
        self.assertEqual([item["id"] for item in selected], ["new"])

        with self.assertRaisesRegex(ValueError, "canonical value: Interspeech"):
            select_venue_papers(
                snapshot,
                venue="interspeech",
                start="2025-07-01",
                end="2025-07-01",
            )

    def test_venue_readiness_rejects_a_thin_inventory(self) -> None:
        snapshot = _snapshot()
        projection = venue_projection(
            snapshot,
            venue="Interspeech",
            start="2025-07-01",
            end="2025-07-01",
        )
        with self.assertRaisesRegex(ValueError, "cannot support a synthesis"):
            validate_venue_synthesis_readiness(projection)

        projection["local_claims"].append({"ref": "b#claim", "concept": "b"})
        validate_venue_synthesis_readiness(projection)


if __name__ == "__main__":
    unittest.main()
