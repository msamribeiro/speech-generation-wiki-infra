#!/usr/bin/env python3
"""One-time normalization of `related_concepts` frontmatter to bracket-unquoted form.

Rewrites `wiki/papers/*.md` in the content repository so every `related_concepts` field
uses the canonical `related_concepts: [slug-one, slug-two]` serialization documented in
docs/content.md, regardless of whether the source used bracket-quoted or YAML block-list
form. Only the `related_concepts` line(s) are touched; the rest of each file is left
byte-for-byte identical.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

_FIELD_RE = re.compile(r"^related_concepts:\s*(.*)$")
_BLOCK_ITEM_RE = re.compile(r"^\s*-\s")


def normalize_frontmatter(frontmatter: str) -> tuple[str, bool]:
    lines = frontmatter.split("\n")
    out_lines: list[str] = []
    i = 0
    changed = False

    while i < len(lines):
        line = lines[i]
        match = _FIELD_RE.match(line)
        if match is None:
            out_lines.append(line)
            i += 1
            continue

        rest = match.group(1).strip()
        if rest == "":
            block_lines = [line]
            j = i + 1
            while j < len(lines) and _BLOCK_ITEM_RE.match(lines[j]):
                block_lines.append(lines[j])
                j += 1
            parsed = yaml.safe_load("\n".join(block_lines))
            i = j
        else:
            parsed = yaml.safe_load(line)
            i += 1

        slugs = parsed.get("related_concepts") or []
        canonical = "related_concepts: [" + ", ".join(slugs) + "]"
        out_lines.append(canonical)
        changed = True

    new_frontmatter = "\n".join(out_lines)
    return new_frontmatter, new_frontmatter != frontmatter and changed


def normalize_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return False
    close = text.index("\n---", 4)
    frontmatter = text[4:close]
    new_frontmatter, changed = normalize_frontmatter(frontmatter)
    if not changed:
        return False
    new_text = text[:4] + new_frontmatter + text[close:]
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--wiki-dir", type=Path, required=True, help="Content repo root")
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing")
    args = parser.parse_args()

    papers_dir = args.wiki_dir / "papers"
    if not papers_dir.is_dir():
        print(f"papers directory not found: {papers_dir}", file=sys.stderr)
        return 1

    changed_files: list[Path] = []
    for path in sorted(papers_dir.glob("*.md")):
        if path.name == "index.md":
            continue
        if args.dry_run:
            text = path.read_text(encoding="utf-8")
            if not text.startswith("---\n"):
                continue
            close = text.index("\n---", 4)
            _, changed = normalize_frontmatter(text[4:close])
            if changed:
                changed_files.append(path)
        else:
            if normalize_file(path):
                changed_files.append(path)

    action = "would change" if args.dry_run else "changed"
    print(f"{action} {len(changed_files)} file(s)")
    for path in changed_files:
        print(f"  {path.relative_to(args.wiki_dir)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
