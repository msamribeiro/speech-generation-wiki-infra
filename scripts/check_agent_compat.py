#!/usr/bin/env python3
"""Validate the checked-in Claude/Codex interoperability layer."""

from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILLS = (
    "speech-generation-filter-agent",
    "speech-generation-ingest-agent",
    "speech-generation-lightweight-ingest-agent",
    "speech-generation-review-agent",
    "speech-generation-integration-agent",
    "speech-generation-render-agent",
)


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def validate() -> list[str]:
    errors: list[str] = []
    claude = (ROOT / "CLAUDE.md").read_text()
    if not claude.startswith("@AGENTS.md"):
        fail("CLAUDE.md must import AGENTS.md first", errors)
    claude_skills = ROOT / ".claude" / "skills"
    if not claude_skills.is_symlink() or claude_skills.resolve() != (ROOT / ".agents" / "skills").resolve():
        fail(".claude/skills must link to the canonical .agents/skills directory", errors)

    active_files = [ROOT / "AGENTS.md", ROOT / "CLAUDE.md"]
    for name in SKILLS:
        skill = ROOT / ".agents" / "skills" / name / "SKILL.md"
        adapter = ROOT / ".claude" / "agents" / f"{name}.md"
        metadata = ROOT / ".agents" / "skills" / name / "agents" / "openai.yaml"
        for path in (skill, adapter, metadata):
            if not path.is_file():
                fail(f"missing {path.relative_to(ROOT)}", errors)
        if not skill.is_file() or not adapter.is_file():
            continue
        skill_text = skill.read_text()
        adapter_text = adapter.read_text()
        active_files.extend((skill, adapter))
        if not re.search(rf"^name: {re.escape(name)}$", skill_text, re.MULTILINE):
            fail(f"skill name mismatch: {name}", errors)
        if f"  - {name}" not in adapter_text:
            fail(f"Claude adapter does not preload {name}", errors)
        frontmatter = skill_text.split("---", 2)[1]
        if "model:" in frontmatter or "tools:" in frontmatter or "color:" in frontmatter:
            fail(f"non-portable skill frontmatter in {name}", errors)
        if "RUNTIME" not in skill_text or "PROVIDER" not in skill_text or "MODEL" not in skill_text:
            fail(f"runtime/provider/model provenance missing from {name}", errors)

    for name in (
        "speech-generation-ingest-agent",
        "speech-generation-lightweight-ingest-agent",
        "speech-generation-review-agent",
        "speech-generation-render-agent",
    ):
        skill_text = (ROOT / ".agents" / "skills" / name / "SKILL.md").read_text()
        if "schema_version: 2" not in skill_text or "docs/schemas/generation.md" not in skill_text:
            fail(f"version-2 page provenance missing from {name}", errors)

    legacy = ROOT / ".claude" / "agents" / "speech-generation-render-agent-v2.md"
    if legacy.exists():
        fail("legacy renderer-v2 adapter still exists", errors)

    local_path = re.compile(r"/Users/[^/]+/")
    for path in active_files:
        if path.is_file() and local_path.search(path.read_text()):
            fail(f"machine-specific path in {path.relative_to(ROOT)}", errors)

    for required in (
        "docs/fetch.md",
        "docs/parse.md",
        "docs/content.md",
        "docs/schemas/metadata.md",
        "docs/schemas/claims.md",
        "docs/schemas/vocabulary.md",
        "docs/schemas/generation.md",
        "scripts/resolve_wiki_dir.py",
    ):
        if not (ROOT / required).exists():
            fail(f"missing referenced file: {required}", errors)

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("agent compatibility validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print(f"agent compatibility validation passed ({len(SKILLS)} shared workflows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
