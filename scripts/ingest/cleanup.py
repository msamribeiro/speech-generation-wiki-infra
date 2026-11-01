#!/usr/bin/env python3
"""
Main-session cleanup for one ingested paper (Mitigation B; docs/ingest-protocol.md section 5).

After an ingest agent has written only the paper page, this script does the bookkeeping:
  1. appends the papers/index.md row (bare [[id]], title truncated to 55 chars, Org, tasks, archs)
  2. sets all three paper-count occurrences in index.md from the papers/index.md row count
  3. inserts the log.md entry under today's dated section (never appended to the end of file)
  4. sets metadata status/ingested_date and appends a version-2 generation_history entry

Provenance (runtime, provider, model, agent) is read from the page's own `generation` block.
Every step is idempotent: re-running for the same ID does not duplicate rows or entries.

Usage:
    .venv/bin/python scripts/ingest/cleanup.py ID [--org "Org A / Org B"] [--wiki-dir DIR] [--dry-run]

--org overrides the page's `organization` for the index Org column (use " / " between orgs).
Metadata `organization` is null on most 2026 records, so the Org column is filled by hand.
"""

import argparse
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
TITLE_CHARS = 55


def resolve_wiki(arg: str | None) -> Path:
    if arg:
        return Path(arg)
    out = subprocess.check_output([sys.executable, str(ROOT / "scripts" / "resolve_wiki_dir.py")], text=True)
    return Path(out.strip())


def frontmatter(page: str) -> dict:
    parts = page.split("---", 2)
    if len(parts) < 3:
        sys.exit("page has no YAML frontmatter")
    return yaml.safe_load(parts[1]) or {}


def join(values) -> str:
    return ", ".join(str(v) for v in (values or []))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paper_id")
    parser.add_argument("--org", help="Org column override (default: page organization)")
    parser.add_argument("--wiki-dir", help="content repo (default: scripts/resolve_wiki_dir.py)")
    parser.add_argument("--dry-run", action="store_true", help="print what would change, write nothing")
    args = parser.parse_args()

    pid = args.paper_id
    wiki = resolve_wiki(args.wiki_dir)
    today = datetime.date.today().isoformat()
    page_path = wiki / "papers" / f"{pid}.md"
    if not page_path.exists():
        sys.exit(f"no page at {page_path}")
    fm = frontmatter(page_path.read_text())
    gen = fm.get("generation") or {}
    if gen.get("schema_version") != 2 or not gen.get("model"):
        sys.exit("page generation block is not version 2 with a model; fix the page first")

    org = args.org or fm.get("organization") or ""
    if isinstance(org, list):
        org = " / ".join(org)
    writes = {}

    # 1. papers/index.md row
    idx_path = wiki / "papers" / "index.md"
    idx = idx_path.read_text()
    if f"| [[{pid}]] |" in idx:
        print("index row: already present")
    else:
        title = str(fm["title"])[:TITLE_CHARS]
        row = (f"| [[{pid}]] | [{title}](papers/{pid}.md) | {org} | {fm.get('venue', '')} | "
               f"{fm.get('year', '')} | {join(fm.get('task'))} | {join(fm.get('architecture'))} | {today} |")
        idx = idx.rstrip("\n") + "\n" + row + "\n"
        writes[idx_path] = idx
        print("index row:", row)
    if not org:
        print("WARNING: Org column is empty; re-run with --org")

    # 2. index.md counts (sole authority: rows in papers/index.md)
    count = len(re.findall(r"^\| \[\[", idx, re.M))
    main_path = wiki / "index.md"
    main_idx = main_path.read_text()
    updated = re.sub(r"contains \d+ paper", f"contains {count} paper", main_idx)
    updated = re.sub(r"Browse all \d+ papers", f"Browse all {count} papers", updated)
    found = re.findall(r"\b(\d+) paper", updated)
    if updated != main_idx:
        writes[main_path] = updated
    print(f"paper count: {count} | index.md occurrences: {found}")
    if len(found) != 3 or set(found) != {str(count)}:
        print("WARNING: index.md does not carry exactly three matching counts; fix by hand")

    # 3. log.md entry under today's section
    log_path = wiki / "log.md"
    log = log_path.read_text()
    if f"- ingest | {pid} |" in log:
        print("log entry: already present")
    else:
        entry = (f"- ingest | {pid} | {fm['title']} | {fm.get('venue', '')} {fm.get('year', '')} | "
                 f"runtime: {gen.get('runtime')} | provider: {gen.get('provider')} | model: {gen['model']}")
        head = f"## {today}\n\n"
        if head in log:
            log = log.replace(head, head + entry + "\n", 1)
        else:
            first = re.search(r"^## \d{4}-\d{2}-\d{2}", log, re.M)
            if not first:
                sys.exit("log.md has no dated section to insert before")
            log = log[:first.start()] + head + entry + "\n\n" + log[first.start():]
        writes[log_path] = log
        print("log entry:", entry[:110])

    # 4. metadata
    meta_path = ROOT / "raw" / "metadata" / f"{pid}.json"
    raw = meta_path.read_text()
    meta = json.loads(raw)
    meta["status"] = "ingested"
    meta["ingested_date"] = today
    history = meta.get("generation_history") or []
    if any(h.get("op") == "ingest" and h.get("date") == today for h in history):
        print("metadata: ingest history entry already present")
    else:
        history.append({
            "schema_version": 2, "date": today, "op": "ingest",
            "runtime": gen.get("runtime"), "provider": gen.get("provider"),
            "agent": gen.get("agent", "speech-generation-ingest-agent"),
            "model": gen["model"], "commit": gen.get("commit"),
        })
    meta["generation_history"] = history
    writes[meta_path] = json.dumps(meta, indent=2, ensure_ascii=False) + ("\n" if raw.endswith("\n") else "")
    print(f"metadata: status ingested, ingested_date {today}, model {gen['model']}")

    if args.dry_run:
        print("dry run: nothing written")
        return
    for path, text in writes.items():
        path.write_text(text)


if __name__ == "__main__":
    main()
