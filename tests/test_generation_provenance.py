from __future__ import annotations

from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from checks.ingest import _check_generation_provenance


class GenerationProvenanceTests(unittest.TestCase):
    def test_legacy_block_is_grandfathered(self) -> None:
        fm = {"generation": {"date": "2026-01-01", "model": "claude-sonnet"}}
        self.assertEqual(_check_generation_provenance("paper", fm), [])

    def test_valid_codex_block(self) -> None:
        fm = {
            "generation": {
                "schema_version": 2,
                "date": "2026-07-20",
                "runtime": "codex",
                "provider": "openai",
                "agent": "speech-generation-ingest-agent",
                "model": "gpt-5",
                "commit": "abc1234",
            }
        }
        self.assertEqual(_check_generation_provenance("paper", fm), [])

    def test_missing_required_fields_fail(self) -> None:
        issues = _check_generation_provenance("paper", {"generation": {"schema_version": 2}})
        messages = {issue.message for issue in issues}
        self.assertIn("Version-2 generation block missing: runtime", messages)
        self.assertIn("Version-2 generation block missing: provider", messages)
        self.assertIn("Version-2 generation block missing: model", messages)

    def test_invalid_runtime_and_provider_fail(self) -> None:
        fm = {
            "generation": {
                "schema_version": 2,
                "date": "2026-07-20",
                "runtime": "other",
                "provider": "other",
                "agent": "agent",
                "model": "model",
                "commit": "abc1234",
            }
        }
        issues = _check_generation_provenance("paper", fm)
        self.assertEqual({issue.check for issue in issues}, {"generation_provenance"})
        self.assertEqual(len(issues), 2)


if __name__ == "__main__":
    unittest.main()
