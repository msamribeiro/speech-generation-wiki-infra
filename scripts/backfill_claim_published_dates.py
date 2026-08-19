#!/usr/bin/env python3
"""Backfill canonical published dates into concept claim YAML paper entries.

The migration is intentionally surgical: it inserts one quoted `published_date` line after each
paper-entry `id` and preserves every other byte. Dates must exist and agree in raw metadata and
paper-page frontmatter. The command requires exactly one of `--dry-run` or `--apply`.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime
import json
from pathlib import Path
import re
import sys

import yaml


ROOT = Path(__file__).resolve().parent.parent
_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
_ENTRY_ID_RE = re.compile(r'^(?P<indent>\s*)- id:\s*(?P<value>.+?)\s*$')
_PUBLISHED_DATE_RE = re.compile(r"^\s*published_date:\s*(.+?)\s*$")
_TOP_LEVEL_KEY_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*:\s*")


class MigrationError(RuntimeError):
    """Raised when canonical dates cannot be resolved without guessing."""


@dataclass(frozen=True)
class FilePlan:
    path: Path
    original: str
    migrated: str
    entries: int

    @property
    def changed(self) -> bool:
        return self.original != self.migrated


def _iso_date(value: object, context: str) -> str:
    if value is None:
        raise MigrationError(f"{context}: published_date is missing")
    text = value.isoformat() if hasattr(value, "isoformat") else str(value)
    try:
        parsed = datetime.strptime(text, "%Y-%m-%d")
    except ValueError as exc:
        raise MigrationError(f"{context}: invalid published_date {text!r}") from exc
    if parsed.strftime("%Y-%m-%d") != text:
        raise MigrationError(f"{context}: published_date is not canonical ISO format: {text!r}")
    return text


def load_canonical_dates(infra_dir: Path, wiki_dir: Path) -> dict[str, str]:
    metadata_dir = infra_dir / "raw" / "metadata"
    papers_dir = wiki_dir / "papers"
    if not metadata_dir.is_dir():
        raise MigrationError(f"metadata directory not found: {metadata_dir}")
    if not papers_dir.is_dir():
        raise MigrationError(f"paper directory not found: {papers_dir}")

    metadata_dates: dict[str, str] = {}
    for path in sorted(metadata_dir.glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise MigrationError(f"invalid metadata JSON: {path}") from exc
        pid = str(data.get("id", path.stem))
        metadata_dates[pid] = _iso_date(data.get("published_date"), f"metadata {pid}")

    page_dates: dict[str, str] = {}
    for path in sorted(papers_dir.glob("*.md")):
        if path.name == "index.md":
            continue
        match = _FRONTMATTER_RE.match(path.read_text(encoding="utf-8"))
        if match is None:
            raise MigrationError(f"paper frontmatter missing or malformed: {path}")
        try:
            frontmatter = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError as exc:
            raise MigrationError(f"paper frontmatter is invalid YAML: {path}") from exc
        pid = str(frontmatter.get("id", path.stem))
        page_dates[pid] = _iso_date(frontmatter.get("published_date"), f"paper page {pid}")

    canonical: dict[str, str] = {}
    for pid in sorted(metadata_dates.keys() & page_dates.keys()):
        if metadata_dates[pid] != page_dates[pid]:
            raise MigrationError(
                f"published_date conflict for {pid}: metadata={metadata_dates[pid]}, "
                f"paper_page={page_dates[pid]}"
            )
        canonical[pid] = metadata_dates[pid]
    return canonical


def _parse_id(value: str, path: Path, line_number: int) -> str:
    try:
        parsed = yaml.safe_load(f"id: {value}")
    except yaml.YAMLError as exc:
        raise MigrationError(f"{path}:{line_number}: invalid paper id scalar") from exc
    pid = parsed.get("id") if isinstance(parsed, dict) else None
    if not isinstance(pid, str):
        raise MigrationError(
            f"{path}:{line_number}: paper id must be a quoted/string scalar, got {pid!r}"
        )
    return pid


def migrate_text(path: Path, text: str, canonical_dates: dict[str, str]) -> tuple[str, int]:
    """Return migrated text and paper-entry count without changing unrelated bytes."""
    lines = text.splitlines(keepends=True)
    in_papers = False
    entries = 0
    seen_ids: set[str] = set()
    output: list[str] = []

    for index, line in enumerate(lines):
        bare = line.rstrip("\r\n")
        if bare == "papers:":
            in_papers = True
            output.append(line)
            continue
        if in_papers and _TOP_LEVEL_KEY_RE.match(bare) and bare != "papers:":
            in_papers = False

        match = _ENTRY_ID_RE.match(bare) if in_papers else None
        if match is None:
            output.append(line)
            continue

        pid = _parse_id(match.group("value"), path, index + 1)
        if pid in seen_ids:
            raise MigrationError(f"{path}:{index + 1}: duplicate paper entry {pid}")
        seen_ids.add(pid)
        entries += 1
        output.append(line)

        if pid not in canonical_dates:
            raise MigrationError(
                f"{path}:{index + 1}: no agreeing metadata and paper-page date for {pid}"
            )

        next_bare = lines[index + 1].rstrip("\r\n") if index + 1 < len(lines) else ""
        existing = _PUBLISHED_DATE_RE.match(next_bare)
        expected = canonical_dates[pid]
        if existing is not None:
            existing_date = _iso_date(
                yaml.safe_load(f"published_date: {existing.group(1)}").get("published_date"),
                f"{path}:{index + 2}",
            )
            if existing_date != expected:
                raise MigrationError(
                    f"{path}:{index + 2}: published_date {existing_date} conflicts with "
                    f"canonical {expected} for {pid}"
                )
            continue

        newline = "\r\n" if line.endswith("\r\n") else "\n"
        key_indent = match.group("indent") + "  "
        output.append(f'{key_indent}published_date: "{expected}"{newline}')

    try:
        parsed = yaml.safe_load(text) or {}
    except yaml.YAMLError as exc:
        raise MigrationError(f"invalid concept YAML: {path}") from exc
    declared_entries = parsed.get("papers") if isinstance(parsed, dict) else None
    if not isinstance(declared_entries, list):
        raise MigrationError(f"{path}: papers is not a list")
    if entries != len(declared_entries):
        raise MigrationError(
            f"{path}: located {entries} paper id lines but YAML contains {len(declared_entries)} entries"
        )

    migrated = "".join(output)
    try:
        migrated_data = yaml.safe_load(migrated) or {}
    except yaml.YAMLError as exc:
        raise MigrationError(f"migration produced invalid YAML: {path}") from exc
    for paper in migrated_data.get("papers", []):
        pid = str(paper.get("id"))
        if _iso_date(paper.get("published_date"), f"{path}:{pid}") != canonical_dates[pid]:
            raise MigrationError(f"{path}:{pid}: migrated date failed verification")
    return migrated, entries


def build_plan(infra_dir: Path, wiki_dir: Path) -> list[FilePlan]:
    claims_dir = wiki_dir / "_claims"
    if not claims_dir.is_dir():
        raise MigrationError(f"claim directory not found: {claims_dir}")
    canonical_dates = load_canonical_dates(infra_dir, wiki_dir)
    plans: list[FilePlan] = []
    for path in sorted(claims_dir.glob("*.yaml")):
        original = path.read_text(encoding="utf-8")
        migrated, entries = migrate_text(path, original, canonical_dates)
        plans.append(FilePlan(path=path, original=original, migrated=migrated, entries=entries))
    if not plans:
        raise MigrationError(f"no top-level concept YAML files found in {claims_dir}")
    return plans


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wiki-dir", type=Path, required=True, help="Standalone content repo root")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true", help="Validate and report without writing")
    mode.add_argument("--apply", action="store_true", help="Apply the verified surgical migration")
    args = parser.parse_args()

    try:
        plans = build_plan(ROOT, args.wiki_dir.resolve())
    except MigrationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    changed = [plan for plan in plans if plan.changed]
    entries = sum(plan.entries for plan in plans)
    if args.apply:
        for plan in changed:
            plan.path.write_text(plan.migrated, encoding="utf-8")

    action = "would change" if args.dry_run else "changed"
    print(
        f"{action} {len(changed)}/{len(plans)} concept files; "
        f"validated {entries} entries"
    )
    for plan in changed:
        print(f"  {plan.path.relative_to(args.wiki_dir)} ({plan.entries} entries)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
