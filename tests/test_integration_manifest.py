import json
import tempfile
import unittest
from pathlib import Path

import yaml

from scripts.freeze_integration_manifest import build_manifest, render_manifest


class IntegrationManifestTests(unittest.TestCase):
    def test_manifest_is_deterministic_and_reports_queue(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            metadata = root / "metadata"
            wiki = root / "wiki"
            metadata.mkdir()
            (wiki / "papers").mkdir(parents=True)
            (wiki / "_claims").mkdir()
            record = {
                "id": "p1",
                "title": "Example",
                "status": "ingested",
                "published_date": "2026-01-02",
                "venue": "arXiv",
            }
            (metadata / "p1.json").write_text(json.dumps(record))
            (wiki / "papers" / "p1.md").write_text(
                "---\nid: p1\npublished_date: 2026-01-02\nrelated_concepts: [example]\n---\n"
            )
            (wiki / "papers" / "index.md").write_text("| [[p1]] | Example |\n")
            (wiki / "_claims" / "example.yaml").write_text(
                yaml.safe_dump({"concept": "example", "papers": []})
            )
            first = build_manifest(
                metadata,
                wiki,
                quarter="2026-Q1",
                start="2026-01-01",
                end="2026-03-31",
                infra_commit="infra",
                content_commit="content",
            )
            second = build_manifest(
                metadata,
                wiki,
                quarter="2026-Q1",
                start="2026-01-01",
                end="2026-03-31",
                infra_commit="infra",
                content_commit="content",
            )
            self.assertEqual(render_manifest(first), render_manifest(second))
            self.assertEqual(first["summary"]["eligible_papers"], 1)
            self.assertEqual(first["summary"]["phase_1_queue_memberships"], 1)
            self.assertEqual(first["concepts"][0]["queue_ids"], ["p1"])


if __name__ == "__main__":
    unittest.main()
