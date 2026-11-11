import json
import tempfile
import unittest
from pathlib import Path

from scripts.checks.metadata import _check as check_metadata
from scripts.ingest.use_peer_reviewed import move_preprint_parse, peer_from_duplicate, switch_record

ARXIV_RECORD = {
    "id": "2608.00011",
    "title": "Example",
    "status": "accepted",
    "venue": "arXiv",
    "venue_type": "preprint",
    "url": "https://arxiv.org/abs/2608.00011",
    "pdf_url": "https://arxiv.org/pdf/2608.00011.pdf",
    "pdf_path": "raw/papers/2608.00011.pdf",
    "source_ids": {"arxiv": "2608.00011"},
    "preprint_date": "2026-08-01",
    "arxiv_version": 1,
    "version_date": "2026-08-01",
    "version_estimated": False,
    "conference_date": None,
    "published_date": "2026-08-01",
    "year": 2026,
    "month": 8,
}

PEER = {
    "url": "https://www.isca-archive.org/interspeech_2026/x26_interspeech.html",
    "pdf_url": "https://www.isca-archive.org/interspeech_2026/x26_interspeech.pdf",
    "venue": "Interspeech",
    "venue_type": "conference",
    "date": "2026-09-27",
    "source_ids": {"isca": "x26_interspeech", "doi": "10.21437/Interspeech.2026-1"},
}


class UsePeerReviewedTests(unittest.TestCase):
    def test_switch_record_fields_and_idempotence(self) -> None:
        pdf = "raw/papers/2608.00011.peer-reviewed.pdf"
        new = switch_record(ARXIV_RECORD, PEER, pdf)
        self.assertEqual(new["url"], PEER["url"])
        self.assertEqual(new["url_peer_reviewed"], PEER["url"])
        self.assertEqual(new["url_preprint"], "https://arxiv.org/abs/2608.00011")
        self.assertEqual(new["pdf_path"], pdf)
        self.assertEqual(new["pdf_path_preprint"], "raw/papers/2608.00011.pdf")
        self.assertEqual(new["venue"], "Interspeech")
        self.assertEqual(new["published_date"], "2026-09-27")
        self.assertEqual((new["year"], new["month"]), (2026, 9))
        self.assertEqual(new["source_ids"]["arxiv"], "2608.00011")
        self.assertEqual(new["source_ids"]["isca"], "x26_interspeech")
        self.assertEqual(switch_record(new, PEER, pdf), new)
        self.assertEqual(check_metadata("2608.00011", new, "error"), [])

    def test_bad_preprint_url_is_reported(self) -> None:
        record = dict(switch_record(ARXIV_RECORD, PEER, "raw/papers/x.pdf"), url_preprint="http://example.org")
        checks = {issue.check for issue in check_metadata("2608.00011", record, "error")}
        self.assertIn("url_preprint_valid", checks)

    def test_peer_from_duplicate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            meta = Path(tmp)
            dup = {
                "id": "interspeech-2026-0001", "is_duplicate": True, "canonical_id": "2608.00011",
                "status": "rejected", "venue": "Interspeech", "venue_type": "conference",
                "conference_date": "2026-09-27", "url": PEER["url"], "pdf_url": PEER["pdf_url"],
                "source_ids": {"isca": "x26_interspeech", "arxiv": "2608.00011"},
            }
            (meta / "interspeech-2026-0001.json").write_text(json.dumps(dup))
            (meta / "2608.00011.json").write_text(json.dumps(ARXIV_RECORD))
            peer = peer_from_duplicate("2608.00011", meta)
            self.assertEqual(peer["date"], "2026-09-27")
            self.assertEqual(peer["source_ids"], {"isca": "x26_interspeech"})
            with self.assertRaises(ValueError):
                peer_from_duplicate("2699.99999", meta)

    def test_move_preprint_parse_once(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp) / "2608.00011"
            (base / "assets").mkdir(parents=True)
            (base / "paper.md").write_text("preprint")
            (base / "assets" / "figure-1.png").write_text("png")
            self.assertTrue(move_preprint_parse("2608.00011", Path(tmp)))
            self.assertEqual((base / "preprint" / "paper.md").read_text(), "preprint")
            self.assertTrue((base / "preprint" / "assets" / "figure-1.png").exists())
            self.assertFalse((base / "paper.md").exists())
            self.assertFalse(move_preprint_parse("2608.00011", Path(tmp)))


if __name__ == "__main__":
    unittest.main()
