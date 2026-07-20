from __future__ import annotations

from pathlib import Path
import sys
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from checks import agents
from checks._base import CheckArgs


class AgentHealthTests(unittest.TestCase):
    def test_current_repository_passes(self) -> None:
        result = agents.run(CheckArgs())
        self.assertTrue(result.passed)
        self.assertEqual(result.issues, [])
        self.assertEqual(result.stats["workflows_checked"], 6)

    def test_validation_errors_become_health_issues(self) -> None:
        with mock.patch.object(agents, "validate", return_value=["broken adapter"]):
            result = agents.run(CheckArgs())
        self.assertFalse(result.passed)
        self.assertEqual(result.stats["errors"], 1)
        self.assertEqual(result.issues[0].module, "agents")
        self.assertEqual(result.issues[0].check, "agent_compat")
        self.assertEqual(result.issues[0].message, "broken adapter")


if __name__ == "__main__":
    unittest.main()
