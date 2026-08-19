from __future__ import annotations

from datetime import date
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from checks.integrate import _check_published_date


class IntegratePublishedDateTests(unittest.TestCase):
    def test_matching_string_date_passes(self) -> None:
        issues = _check_published_date(
            "concept:paper", "2025-01-03", {"published_date": "2025-01-03"}
        )
        self.assertEqual(issues, [])

    def test_yaml_date_object_passes(self) -> None:
        issues = _check_published_date(
            "concept:paper", date(2025, 1, 3), {"published_date": "2025-01-03"}
        )
        self.assertEqual(issues, [])

    def test_missing_date_fails(self) -> None:
        issues = _check_published_date(
            "concept:paper", None, {"published_date": "2025-01-03"}
        )
        self.assertEqual({issue.check for issue in issues}, {"published_date_valid"})

    def test_noncanonical_iso_format_fails(self) -> None:
        issues = _check_published_date(
            "concept:paper", "2025-1-3", {"published_date": "2025-01-03"}
        )
        self.assertEqual({issue.check for issue in issues}, {"published_date_valid"})

    def test_metadata_disagreement_fails(self) -> None:
        issues = _check_published_date(
            "concept:paper", "2025-01-04", {"published_date": "2025-01-03"}
        )
        self.assertEqual({issue.check for issue in issues}, {"published_date_canonical"})


if __name__ == "__main__":
    unittest.main()
