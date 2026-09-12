from __future__ import annotations

import unittest

from lib.field_overview import project_field_conclusions


class FieldOverviewProjectionTests(unittest.TestCase):
    def test_linked_clusters_become_one_conclusion_and_keep_caveats(self) -> None:
        graphs = {
            "concept-a": {
                "papers": [{"id": "paper-a"}, {"id": "shared"}],
                "claim_clusters": [{
                    "id": "claim_a",
                    "claim": "Local A",
                    "status": "strongly_supported",
                    "confidence": "high",
                    "supporting_papers": ["paper-a", "shared"],
                    "contradicting_papers": [],
                    "refining_papers": [],
                    "caveats": ["Qualification A"],
                }],
            },
            "concept-b": {
                "papers": [{"id": "paper-b"}, {"id": "shared"}],
                "claim_clusters": [{
                    "id": "claim_b",
                    "claim": "Local B",
                    "status": "emerging",
                    "confidence": "medium",
                    "supporting_papers": ["paper-b", "shared"],
                    "contradicting_papers": [],
                    "refining_papers": ["paper-r"],
                    "caveats": ["Qualification B"],
                }],
            },
        }
        registry = {
            "broader_claims": [{
                "id": "broader_ab",
                "proposition": "Broader conclusion",
                "status": "strongly_supported",
                "confidence": "high",
                "review_status": "human_approved",
                "members": [
                    {"claim": "concept-a#claim_a", "relationship": "supports"},
                    {"claim": "concept-b#claim_b", "relationship": "refines"},
                ],
                "caveats": ["Broader qualification"],
            }],
        }

        result = project_field_conclusions(graphs, registry)

        self.assertEqual(len(result["broader_conclusions"]), 1)
        self.assertEqual(result["local_conclusions"], [])
        conclusion = result["broader_conclusions"][0]
        self.assertEqual(
            conclusion["evidence"]["supporting_papers"],
            ["paper-a", "paper-b", "shared"],
        )
        self.assertEqual(conclusion["caveats"], ["Broader qualification"])
        self.assertEqual(
            [member["caveats"] for member in conclusion["members"]],
            [["Qualification A"], ["Qualification B"]],
        )
        self.assertEqual(result["stats"]["concept_paper_memberships"], 4)
        self.assertEqual(result["stats"]["unique_papers"], 3)
        self.assertEqual(result["stats"]["overlapping_memberships"], 1)

    def test_agent_proposals_do_not_suppress_local_clusters(self) -> None:
        graphs = {
            "concept-a": {
                "papers": [{"id": "paper-a"}],
                "claim_clusters": [{
                    "id": "claim_a",
                    "claim": "Local A",
                    "status": "emerging",
                    "confidence": "medium",
                    "supporting_papers": ["paper-a"],
                    "contradicting_papers": [],
                    "refining_papers": [],
                    "caveats": [],
                }],
            }
        }
        registry = {
            "broader_claims": [{
                "id": "proposed",
                "review_status": "agent_proposed",
                "members": [{"claim": "concept-a#claim_a"}],
            }]
        }

        result = project_field_conclusions(graphs, registry)

        self.assertEqual(result["broader_conclusions"], [])
        self.assertEqual(
            [item["ref"] for item in result["local_conclusions"]],
            ["concept-a#claim_a"],
        )


if __name__ == "__main__":
    unittest.main()
