#!/usr/bin/env python3
"""Switch an accepted, not-yet-ingested record to its verified peer-reviewed version.

Rule: docs/schemas/metadata.md, "Source Version at Ingest". The page keeps the canonical ID; the
summarized text becomes the peer-reviewed version and the preprint is kept as context:

- the peer-reviewed PDF is downloaded to raw/papers/{id}.peer-reviewed.pdf;
- an existing preprint parse moves from raw/parsed/{id}/ to raw/parsed/{id}/preprint/;
- metadata: url and url_peer_reviewed -> peer-reviewed landing page, url_preprint -> old arXiv
  url, pdf_path_preprint -> old pdf_path, pdf_path/pdf_url -> peer-reviewed PDF, venue,
  venue_type, conference_date or journal_date, source IDs; then the canonical date rule.

Dry run by default; --apply performs the switch. Afterwards re-parse with
`batch_convert.py --ids {id}`. The peer-reviewed identity must already be verified (title,
authors, landing page, date); this script does no matching.

Usage:
    python scripts/ingest/use_peer_reviewed.py --wiki-dir DIR --id 2608.00011 --from-duplicate
    python scripts/ingest/use_peer_reviewed.py --wiki-dir DIR --id 2606.10591 \\
        --url https://www.isca-archive.org/interspeech_2026/liang26d_interspeech.html \\
        --pdf-url https://www.isca-archive.org/interspeech_2026/liang26d_interspeech.pdf \\
        --venue Interspeech --venue-type conference --date 2026-09-27 \\
        --source isca=liang26d_interspeech --source doi=10.21437/Interspeech.2026-3355
"""

from __future__ import annotations

import argparse
import copy
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT))

from lib.paper_dates import apply_date_rule, valid_iso_date  # noqa: E402
from lib.peer_reviewed_versions import load_frozen_memberships  # noqa: E402

METADATA_DIR = ROOT / "raw" / "metadata"
PAPERS_DIR = ROOT / "raw" / "papers"
PARSED_DIR = ROOT / "raw" / "parsed"
PEER_TYPES = {"conference", "journal", "workshop"}


def peer_from_duplicate(paper_id: str, metadata_dir: Path = METADATA_DIR) -> dict:
    """Read the peer-reviewed version from the rejected duplicate record pointing at paper_id."""
    found = []
    for path in sorted(metadata_dir.glob("*.json")):
        record = json.loads(path.read_text())
        if record.get("is_duplicate") and record.get("canonical_id") == paper_id:
            if record.get("venue_type") in PEER_TYPES and record.get("url") and record.get("pdf_url"):
                found.append(record)
    if len(found) != 1:
        raise ValueError(f"expected one peer-reviewed duplicate of {paper_id}, found {len(found)}")
    dup = found[0]
    date_key = "journal_date" if dup["venue_type"] == "journal" else "conference_date"
    sources = {k: v for k, v in (dup.get("source_ids") or {}).items() if k != "arxiv"}
    return {
        "url": dup["url"],
        "pdf_url": dup["pdf_url"],
        "venue": dup["venue"],
        "venue_type": dup["venue_type"],
        "date": dup.get(date_key),
        "source_ids": sources,
        "duplicate_id": dup["id"],
    }


def switch_record(record: dict, peer: dict, pdf_path: str) -> dict:
    """Return the switched metadata record (pure; idempotent on an already-switched record)."""
    if peer["venue_type"] not in PEER_TYPES:
        raise ValueError(f"venue_type must be one of {sorted(PEER_TYPES)}")
    if not valid_iso_date(peer.get("date")):
        raise ValueError(f"invalid peer-reviewed date: {peer.get('date')!r}")
    if not str(peer["url"]).startswith("https://"):
        raise ValueError(f"invalid landing page: {peer['url']!r}")
    new = copy.deepcopy(record)
    old_url = record.get("url") or ""
    if old_url.startswith("https://arxiv.org/abs/") and old_url != peer["url"]:
        new["url_preprint"] = old_url
    if record.get("pdf_path") and record.get("pdf_path") != pdf_path:
        new["pdf_path_preprint"] = record["pdf_path"]
    new["url"] = peer["url"]
    new["url_peer_reviewed"] = peer["url"]
    new["pdf_url"] = peer["pdf_url"]
    new["pdf_path"] = pdf_path
    new["venue"] = peer["venue"]
    new["venue_type"] = peer["venue_type"]
    new["journal_date" if peer["venue_type"] == "journal" else "conference_date"] = peer["date"]
    sources = new.setdefault("source_ids", {})
    sources.update(peer.get("source_ids") or {})
    apply_date_rule(new)
    return new


def move_preprint_parse(paper_id: str, parsed_dir: Path = PARSED_DIR) -> bool:
    """Move raw/parsed/{id}/* into raw/parsed/{id}/preprint/. Returns True if anything moved."""
    base = parsed_dir / paper_id
    target = base / "preprint"
    if target.exists() or not (base / "paper.md").exists():
        return False
    target.mkdir()
    for child in sorted(base.iterdir()):
        if child.name != "preprint":
            shutil.move(str(child), str(target / child.name))
    return True


def download(url: str, dest: Path) -> None:
    import requests

    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=120)
    resp.raise_for_status()
    if not resp.content.startswith(b"%PDF"):
        raise ValueError(f"not a PDF: {url}")
    dest.write_bytes(resp.content)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--wiki-dir", required=True, type=Path, help="Canonical content checkout")
    parser.add_argument("--id", required=True)
    parser.add_argument("--from-duplicate", action="store_true",
                        help="Take the peer-reviewed version from the duplicate record pointing at --id")
    parser.add_argument("--url")
    parser.add_argument("--pdf-url")
    parser.add_argument("--venue")
    parser.add_argument("--venue-type", choices=sorted(PEER_TYPES))
    parser.add_argument("--date", help="conference_date or journal_date (YYYY-MM-DD)")
    parser.add_argument("--source", action="append", default=[], help="KEY=VALUE source ID, repeatable")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    paper_id = args.id
    meta_path = METADATA_DIR / f"{paper_id}.json"
    record = json.loads(meta_path.read_text())
    if record.get("status") != "accepted":
        sys.exit(f"{paper_id}: status is {record.get('status')!r}; only accepted records are switched")
    if (args.wiki_dir / "papers" / f"{paper_id}.md").exists():
        sys.exit(f"{paper_id}: page already exists; record url_peer_reviewed and the note instead")
    if paper_id in load_frozen_memberships(args.wiki_dir):
        sys.exit(f"{paper_id}: in a claim YAML (date-frozen); not switched")

    if args.from_duplicate:
        peer = peer_from_duplicate(paper_id)
    else:
        missing = [n for n in ("url", "pdf_url", "venue", "venue_type", "date") if not getattr(args, n)]
        if missing:
            sys.exit(f"missing: {', '.join('--' + m.replace('_', '-') for m in missing)}")
        peer = {"url": args.url, "pdf_url": args.pdf_url, "venue": args.venue,
                "venue_type": args.venue_type, "date": args.date,
                "source_ids": dict(s.split("=", 1) for s in args.source)}

    pdf_rel = f"raw/papers/{paper_id}.peer-reviewed.pdf"
    new = switch_record(record, peer, pdf_rel)
    changes = {k: (record.get(k), new.get(k)) for k in sorted(set(record) | set(new)) if record.get(k) != new.get(k)}
    print(f"{paper_id}: {record.get('title')}")
    for key, (old, value) in changes.items():
        print(f"  {key}: {old!r} -> {value!r}")
    if not changes:
        print("  already switched; no metadata change")
    if not args.apply:
        print("dry run; re-run with --apply")
        return

    dest = ROOT / pdf_rel
    if not dest.exists():
        download(peer["pdf_url"], dest)
        print(f"  downloaded {pdf_rel}")
    if move_preprint_parse(paper_id):
        print(f"  moved preprint parse to raw/parsed/{paper_id}/preprint/")
    if changes:
        meta_path.write_text(json.dumps(new, indent=2, ensure_ascii=False) + "\n")
        print(f"  wrote {meta_path.relative_to(ROOT)}")
    print(f"next: .venv/bin/python scripts/parse/batch_convert.py --ids {paper_id}")


if __name__ == "__main__":
    main()
