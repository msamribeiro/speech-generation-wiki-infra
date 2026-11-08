#!/usr/bin/env python3
"""Apply verified peer-reviewed versions without rewriting summarized content.

The command is dry-run by default.  Its override file is a reviewed, authoritative input; this
script performs no fuzzy identity matching and no network access.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from lib.paper_dates import apply_date_rule  # noqa: E402
from lib.peer_reviewed_versions import load_frozen_memberships  # noqa: E402

METADATA_DIR = ROOT / "raw" / "metadata"
NOTE_MARKER = "This page, including its metrics and claims, summarizes the ingested version."


def _quarter(value: str | None) -> str | None:
    if not value:
        return None
    return f"{value[:4]}-Q{(int(value[5:7]) - 1) // 3 + 1}"


def _set_frontmatter_field(text: str, key: str, value: str | int, *, after: str) -> str:
    boundary = text.find("\n---", 4)
    if boundary < 0:
        raise ValueError("page has no closing frontmatter delimiter")
    front, body = text[:boundary], text[boundary:]
    rendered = json.dumps(value, ensure_ascii=False) if isinstance(value, str) else str(value)
    pattern = re.compile(rf"(?m)^{re.escape(key)}:.*$")
    if pattern.search(front):
        front = pattern.sub(f"{key}: {rendered}", front, count=1)
    else:
        anchor = re.compile(rf"(?m)^({re.escape(after)}:.*)$")
        if not anchor.search(front):
            raise ValueError(f"frontmatter anchor {after!r} missing")
        front = anchor.sub(rf"\1\n{key}: {rendered}", front, count=1)
    return front + body


def transform_page(text: str, entry: dict, *, frozen: bool) -> str:
    """Return one surgically updated paper page; safe to call repeatedly."""
    venue = str(entry["venue"])
    venue_type = str(entry["venue_type"])
    peer_url = str(entry["url"])
    date_key = "journal_date" if venue_type == "journal" else "conference_date"
    peer_date = str(entry[date_key])
    result = text

    result = _set_frontmatter_field(result, "url_peer_reviewed", peer_url, after="url")
    result = _set_frontmatter_field(result, date_key, peer_date, after="published_date")
    if frozen:
        result = _set_frontmatter_field(result, "peer_reviewed_venue", venue, after="venue_type")
        result = _set_frontmatter_field(
            result, "peer_reviewed_venue_type", venue_type, after="peer_reviewed_venue"
        )
    else:
        result = _set_frontmatter_field(result, "venue", venue, after="organization")
        result = _set_frontmatter_field(result, "venue_type", venue_type, after="venue")
        result = _set_frontmatter_field(result, "published_date", peer_date, after="month")
        result = _set_frontmatter_field(result, "year", int(peer_date[:4]), after="venue_type")
        result = _set_frontmatter_field(result, "month", int(peer_date[5:7]), after="year")

    front_end = result.find("\n---", 4)
    card_start = result.find("> [!abstract]", front_end)
    if card_start < 0:
        raise ValueError("abstract card missing")
    card_end = result.find("\n\n", card_start)
    if card_end < 0:
        raise ValueError("abstract card terminator missing")
    card = result[card_start:card_end]
    if not frozen:
        label = venue_type.replace("-", " ").title()
        card = re.sub(
            r"(?m)^> \[!abstract\] .*?$",
            f"> [!abstract] {venue} · {peer_date[:4]} · {label}",
            card,
            count=1,
        )
    if "[→ Peer-reviewed version]" not in card:
        card = re.sub(
            r"(\[→ Paper\]\([^)]+\))",
            rf"\1 · [→ Peer-reviewed version]({peer_url})",
            card,
            count=1,
        )
    else:
        card = re.sub(
            r"\[→ Peer-reviewed version\]\([^)]+\)",
            f"[→ Peer-reviewed version]({peer_url})",
            card,
            count=1,
        )
    result = result[:card_start] + card + result[card_end:]

    note = (
        f"*A [peer-reviewed version]({peer_url}) appeared at {venue} {peer_date[:4]}. "
        f"{NOTE_MARKER}*"
    )
    if NOTE_MARKER in result:
        result = re.sub(
            r"(?m)^\*A \[peer-reviewed version\].*summarizes the ingested version\.\*$",
            note,
            result,
            count=1,
        )
    else:
        heading = result.find("\n## ", card_end)
        if heading < 0:
            raise ValueError("first section heading missing")
        result = result[:heading] + "\n\n" + note + result[heading:]
    result = re.sub(
        r"\n{2,}(\*A \[peer-reviewed version\].*summarizes the ingested version\.\*)\n+(?=## )",
        r"\n\n\1\n\n",
        result,
        count=1,
    )
    return result


def transform_index(text: str, paper_id: str, entry: dict, *, frozen: bool) -> str:
    lines = text.splitlines(keepends=True)
    matches = [i for i, line in enumerate(lines) if f"[[{paper_id}]]" in line]
    if len(matches) != 1:
        raise ValueError(f"expected one catalog row for {paper_id}, found {len(matches)}")
    if not frozen:
        idx = matches[0]
        ending = "\n" if lines[idx].endswith("\n") else ""
        parts = lines[idx].rstrip("\n").split("|")
        if len(parts) < 7:
            raise ValueError(f"malformed catalog row for {paper_id}")
        parts[4] = f" {entry['venue']} "
        date_key = "journal_date" if entry["venue_type"] == "journal" else "conference_date"
        parts[5] = f" {str(entry[date_key])[:4]} "
        lines[idx] = "|".join(parts) + ending
    return "".join(lines)


def _updated_record(record: dict, entry: dict, *, frozen: bool) -> dict:
    updated = copy.deepcopy(record)
    date_key = "journal_date" if entry["venue_type"] == "journal" else "conference_date"
    updated[date_key] = entry[date_key]
    updated["url_peer_reviewed"] = entry["url"]
    source_ids = updated.setdefault("source_ids", {})
    if entry.get("doi"):
        source_ids["doi"] = entry["doi"]
    if frozen:
        updated["peer_reviewed_venue"] = entry["venue"]
        updated["peer_reviewed_venue_type"] = entry["venue_type"]
    else:
        updated["venue"] = entry["venue"]
        updated["venue_type"] = entry["venue_type"]
    apply_date_rule(updated, preserve_published_date=frozen)
    return updated


def build_plan(overrides: dict, wiki_dir: Path) -> tuple[list[dict], dict[str, tuple[dict, dict]]]:
    frozen = load_frozen_memberships(wiki_dir)
    plan: list[dict] = []
    records: dict[str, tuple[dict, dict]] = {}
    for entry in sorted(overrides.get("entries", []), key=lambda item: str(item["id"])):
        paper_id = str(entry["id"])
        path = METADATA_DIR / f"{paper_id}.json"
        if not path.exists():
            raise ValueError(f"metadata missing for {paper_id}")
        old = json.loads(path.read_text())
        new = _updated_record(old, entry, frozen=paper_id in frozen)
        page_path = wiki_dir / "papers" / f"{paper_id}.md"
        page_changed = False
        index_changed = False
        if page_path.exists():
            page_changed = transform_page(
                page_path.read_text(), entry, frozen=paper_id in frozen
            ) != page_path.read_text()
            index_path = wiki_dir / "papers" / "index.md"
            index_changed = transform_index(
                index_path.read_text(), paper_id, entry, frozen=paper_id in frozen
            ) != index_path.read_text()
        item = {
            "id": paper_id,
            "title": old.get("title"),
            "status": old.get("status"),
            "frozen": paper_id in frozen,
            "frozen_concepts": frozen.get(paper_id, []),
            "old": {
                "venue": old.get("venue"),
                "venue_type": old.get("venue_type"),
                "published_date": old.get("published_date"),
                "quarter": _quarter(old.get("published_date")),
                "url_peer_reviewed": old.get("url_peer_reviewed"),
            },
            "new": {
                "venue": new.get("venue"),
                "venue_type": new.get("venue_type"),
                "peer_reviewed_venue": new.get("peer_reviewed_venue"),
                "peer_reviewed_venue_type": new.get("peer_reviewed_venue_type"),
                "published_date": new.get("published_date"),
                "quarter": _quarter(new.get("published_date")),
                "url_peer_reviewed": new.get("url_peer_reviewed"),
            },
            "metadata_changed": old != new,
            "page_exists": page_path.exists(),
            "page_changed": page_changed,
            "index_changed": index_changed,
            "verification": entry.get("verified_by"),
        }
        plan.append(item)
        records[paper_id] = (old, new)
    return plan, records


def render_manifest(plan: list[dict], overrides: dict) -> str:
    payload = {
        "schema_version": 1,
        "scope": overrides.get("scope"),
        "summary": {
            "records": len(plan),
            "metadata_changes": sum(item["metadata_changed"] for item in plan),
            "page_changes": sum(item["page_changed"] for item in plan),
            "index_changes": sum(item["index_changed"] for item in plan),
            "frozen": sum(item["frozen"] for item in plan),
            "quarter_moves": sum(item["old"]["quarter"] != item["new"]["quarter"] for item in plan),
            "deferred": len(overrides.get("deferred", [])),
        },
        "entries": plan,
        "deferred": overrides.get("deferred", []),
    }
    canonical = json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    return json.dumps({"sha256": digest, **payload}, indent=2, ensure_ascii=False, sort_keys=True) + "\n"


def apply_plan(plan: list[dict], records: dict[str, tuple[dict, dict]], overrides: dict, wiki_dir: Path) -> None:
    entries = {str(item["id"]): item for item in overrides["entries"]}
    changed_ids: list[str] = []
    index_path = wiki_dir / "papers" / "index.md"
    index_text = index_path.read_text()
    frozen = {item["id"]: item["frozen"] for item in plan}
    for item in plan:
        paper_id = item["id"]
        old, new = records[paper_id]
        if old != new:
            (METADATA_DIR / f"{paper_id}.json").write_text(
                json.dumps(new, indent=2, ensure_ascii=False) + "\n"
            )
            changed_ids.append(paper_id)
        page_path = wiki_dir / "papers" / f"{paper_id}.md"
        if page_path.exists():
            transformed = transform_page(page_path.read_text(), entries[paper_id], frozen=frozen[paper_id])
            if transformed != page_path.read_text():
                page_path.write_text(transformed)
            index_text = transform_index(index_text, paper_id, entries[paper_id], frozen=frozen[paper_id])
    if index_text != index_path.read_text():
        index_path.write_text(index_text)
    if changed_ids:
        content_log = wiki_dir / "log.md"
        log_line = (
            f"- misc | peer-reviewed version migration | {len(changed_ids)} verified records | "
            "canonical dates moved only for records absent from top-level claim YAMLs | "
            "existing pages continue to summarize their ingested versions\n"
        )
        if log_line.strip() not in content_log.read_text():
            with content_log.open("a") as handle:
                handle.write(log_line)
        pipeline_log = ROOT / "raw" / "pipeline_log.md"
        pipeline_line = (
            f"- review | peer-reviewed version migration | {len(changed_ids)} verified records | "
            "metadata and canonical dates updated under claim-membership freeze rule\n"
        )
        if pipeline_line.strip() not in pipeline_log.read_text():
            with pipeline_log.open("a") as handle:
                handle.write(pipeline_line)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wiki-dir", type=Path, required=True)
    parser.add_argument("--overrides", type=Path, required=True)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    overrides = yaml.safe_load(args.overrides.read_text()) or {}
    plan, records = build_plan(overrides, args.wiki_dir)
    manifest = render_manifest(plan, overrides)
    if args.manifest:
        args.manifest.write_text(manifest)
    else:
        print(manifest, end="")
    if args.apply:
        apply_plan(plan, records, overrides, args.wiki_dir)


if __name__ == "__main__":
    main()
