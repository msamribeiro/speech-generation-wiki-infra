#!/usr/bin/env python3
"""Resolve and validate the writable sibling wiki-content repository."""

from __future__ import annotations

import argparse
import configparser
import os
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlparse


def git_output(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        raise ValueError(result.stderr.strip() or f"git {' '.join(args)} failed")
    return result.stdout.strip()


def expected_remote(infra_root: Path) -> str:
    parser = configparser.ConfigParser()
    parser.read(infra_root / ".gitmodules")
    try:
        return parser['submodule "wiki"']["url"]
    except KeyError as exc:
        raise ValueError(".gitmodules does not define the wiki submodule URL") from exc


def normalize_remote(value: str) -> str:
    value = value.strip().removesuffix("/").removesuffix(".git")
    if value.startswith("git@") and ":" in value:
        host, path = value[4:].split(":", 1)
        return f"{host}/{path}".lower()
    parsed = urlparse(value)
    if parsed.hostname:
        return f"{parsed.hostname}/{parsed.path.lstrip('/')}".lower()
    return value.lower()


def resolve_wiki_dir(infra_root: Path) -> Path:
    override = os.environ.get("SPEECH_WIKI_CONTENT_DIR")
    target = Path(override).expanduser() if override else infra_root.parent / "speech-generation-wiki-content"
    target = target.resolve()
    if not target.is_dir():
        raise ValueError(f"wiki content repository not found: {target}")
    if git_output(target, "rev-parse", "--is-inside-work-tree") != "true":
        raise ValueError(f"wiki content target is not a Git worktree: {target}")
    actual = git_output(target, "remote", "get-url", "origin")
    expected = expected_remote(infra_root)
    if normalize_remote(actual) != normalize_remote(expected):
        raise ValueError(f"wiki origin mismatch: expected {expected!r}, found {actual!r}")
    if not os.access(target, os.W_OK):
        raise ValueError(f"wiki content repository is not writable: {target}")
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--infra-root", type=Path, help="Override infra root for validation/tests")
    args = parser.parse_args()
    infra_root = (args.infra_root or Path(__file__).resolve().parents[1]).resolve()
    try:
        print(resolve_wiki_dir(infra_root))
    except ValueError as exc:
        print(f"wiki directory resolution failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
