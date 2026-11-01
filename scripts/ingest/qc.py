#!/usr/bin/env python3
"""
Per-paper QC after ingest cleanup (docs/ingest-protocol.md section 6).

Runs the scoped ingest health check, then the checks it does not cover:
  - frontmatter summary (task / architecture / related_concepts / significance) for a manual read
  - YAML quoting: id, dates and related_papers must be strings (unquoted IDs parse as floats)
  - related_concepts above the hard cap of 6 (or empty); 1-2 is allowed when scope limits it
  - callouts: at most two, only abstract/important/tip/warning, never note
  - em dashes outside template separators; "SCA" in prose; bare paper wikilinks in prose
  - `[[` outside real wikilinks (Quartz parses it even inside math)
  - citation integrity: every link target has a page; related_papers without a page or rejected
  - adoption language, leaked instruction text, "inconsistency" claims (verify each by hand)
  - papers/index.md row present exactly once with a non-empty Org; index.md counts consistent

Findings are prompts for a human check, not automatic failures; the exit code is non-zero only
when the health check itself fails.

Usage:
    .venv/bin/python scripts/ingest/qc.py ID [--wiki-dir DIR]
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ALLOWED_CALLOUTS = {"abstract", "important", "tip", "warning"}
QUOTED_KEYS = ("id", "published_date", "preprint_date", "conference_date", "version_date",
               "journal_date", "ingested_date", "date", "related_papers")
TEMPLATE_DASH = re.compile(r"^(- \[\[[^\]]+\]\] — |(> )?(foundational|high|moderate|low) — )", re.I)


def resolve_wiki(arg: str | None) -> Path:
    if arg:
        return Path(arg)
    out = subprocess.check_output([sys.executable, str(ROOT / "scripts" / "resolve_wiki_dir.py")], text=True)
    return Path(out.strip())


def status(pid: str) -> str:
    path = ROOT / "raw" / "metadata" / f"{pid}.json"
    return json.loads(path.read_text()).get("status", "?") if path.exists() else "no metadata"


def section(title: str, lines: list[str]) -> None:
    print(f"--- {title}")
    for line in lines:
        print(f"  {line}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paper_id")
    parser.add_argument("--wiki-dir", help="content repo (default: scripts/resolve_wiki_dir.py)")
    args = parser.parse_args()

    pid = args.paper_id
    wiki = resolve_wiki(args.wiki_dir)
    page_path = wiki / "papers" / f"{pid}.md"
    page = page_path.read_text()
    _, fm_text, body = page.split("---", 2)

    health = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "health_check.py"), "--module", "ingest",
         "--id", pid, "--wiki-dir", str(wiki), "-v"],
        capture_output=True, text=True)
    print((health.stdout + health.stderr).strip())

    keys = ("task", "architecture", "related_concepts", "organization", "  level", "  type", "tags", "ingest_tier")
    section("frontmatter", [l for l in fm_text.splitlines() if l.startswith(keys)])

    unquoted = []
    for key in QUOTED_KEYS:
        for value in re.findall(rf"^\s*{key}:\s*(.+)$", fm_text, re.M):
            items = [v.strip() for v in value.strip("[]").split(",")] if value.startswith("[") else [value.strip()]
            bad = [v for v in items if v and v != "null" and not v.startswith('"') and v[0].isdigit()]
            if bad:
                unquoted.append(f"{key}: {bad[:5]}")
    section("unquoted IDs or dates", unquoted)

    concepts = re.search(r"^related_concepts:\s*\[(.*)\]", fm_text, re.M)
    n_concepts = len([c for c in concepts.group(1).split(",") if c.strip()]) if concepts else 0
    section("related_concepts count", [] if 1 <= n_concepts <= 6 else [f"{n_concepts} (cap is 6; empty only on the 2604.11803 precedent)"])

    callouts = re.findall(r"^> \[!(\w+)\]", body, re.M)
    problems = [f"disallowed [!{c}]" for c in callouts if c not in ALLOWED_CALLOUTS]
    if len(callouts) > 2:
        problems.append(f"{len(callouts)} callouts (limit is two, abstract included)")
    section(f"callouts {callouts}", problems)

    lines = body.splitlines()
    section("em dashes outside template separators",
            [l[:140] for l in lines if "—" in l and not TEMPLATE_DASH.match(l)])
    section("SCA in prose", [l[:140] for l in lines if re.search(r"\bSCA\b", l)])
    section("bare paper wikilinks in prose", re.findall(r"\[\[[^\]|]*\d[^\]|]*\]\]", body))

    stray = [m for m in re.findall(r"\[\[([^\]]*)", page) if not re.fullmatch(r"[\w.\-]+(\|[^\]]*)?", m)]
    section("[[ outside real wikilinks", stray)

    integrity = []
    for target in sorted(set(re.findall(r"\[\[([^\]|#]+)", page))):
        if not (wiki / "papers" / f"{target}.md").exists() and not (wiki / "concepts" / f"{target}.md").exists():
            integrity.append(f"link without page: {target} ({status(target)})")
    related = re.search(r"^related_papers:\s*\[(.*)\]", fm_text, re.M)
    for rid in [r.strip().strip('"') for r in related.group(1).split(",")] if related else []:
        if rid and not (wiki / "papers" / f"{rid}.md").exists():
            integrity.append(f"related_papers without page: {rid} ({status(rid)})")
        elif rid and status(rid) == "rejected":
            integrity.append(f"related_papers rejected: {rid}")
    section("citation integrity (accepted-but-unwritten is fine in related_papers)", integrity)

    section("adoption language", [l[:140] for l in lines
                                  if re.search(r"de facto|dominant|widely adopted|has become", l, re.I)])
    section("leaked instruction text", [l[:140] for l in lines if "Grounding rule" in l])
    section("inconsistency claims (verify against source tables)",
            [l[:140] for l in lines if re.search(r"inconsisten", l, re.I)])

    index = (wiki / "papers" / "index.md").read_text()
    rows = [l for l in index.splitlines() if l.startswith(f"| [[{pid}]] |")]
    row_problems = [f"{len(rows)} rows (expected 1)"] if len(rows) != 1 else []
    if rows and not rows[0].split("|")[3].strip():
        row_problems.append("Org column empty")
    section("index row", rows + row_problems)
    count = len(re.findall(r"^\| \[\[", index, re.M))
    found = re.findall(r"\b(\d+) paper", (wiki / "index.md").read_text())
    section(f"counts: papers/index.md rows {count}, index.md {found}",
            [] if len(found) == 3 and set(found) == {str(count)} else ["index.md counts inconsistent"])

    return 0 if "PASS" in health.stdout else 1


if __name__ == "__main__":
    sys.exit(main())
