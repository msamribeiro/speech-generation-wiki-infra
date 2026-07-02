"""
Ingest module for the Pipeline Health Suite.

Validates wiki paper pages (wiki/papers/*.md) for structural correctness:
frontmatter, required sections, controlled vocabulary, claim citations,
figure links, concept slugs, wikilink format, index presence, and tier stubs.
"""

import re
from pathlib import Path

import yaml

from checks._base import CheckArgs, Issue, ModuleResult

ROOT = Path(__file__).parent.parent.parent
_DEFAULT_WIKI = ROOT / "wiki"
PARSED_DIR = ROOT / "raw" / "parsed"
VOCABULARY = ROOT / "docs" / "schemas" / "vocabulary.md"

REQUIRED_FM_FIELDS = ["id", "title", "venue", "published_date", "task", "field_significance"]

_PAPER_ID_RE = re.compile(
    r"^\d{4}\.\d{4,5}$"
    r"|^(iclr|neurips|interspeech|icassp|acl|emnlp|naacl|asru|slt|coling|eacl|findings-naacl|findings-acl|findings-emnlp)-\d{4}-"
)


# ---------------------------------------------------------------------------
# Vocabulary loading
# ---------------------------------------------------------------------------

def _load_vocabulary() -> dict:
    text = VOCABULARY.read_text(encoding="utf-8")
    lines = text.splitlines()

    valid_tasks: set[str] = set()
    valid_levels: set[str] = set()
    valid_types: set[str] = set()

    section = None
    in_type_list = False

    for line in lines:
        if line.startswith("## Tasks"):
            section = "tasks"
            in_type_list = False
        elif line.startswith("## Field Significance"):
            section = "field_significance"
            in_type_list = False
        elif line.startswith("## "):
            section = None
            in_type_list = False

        if section == "tasks":
            for m in re.finditer(r"`([^`]+)`", line):
                valid_tasks.add(m.group(1))

        if section == "field_significance":
            level_match = re.match(r"\*\*level:\*\*\s*(.+)", line)
            if level_match:
                for m in re.finditer(r"`([^`]+)`", level_match.group(1)):
                    valid_levels.add(m.group(1))

            if re.match(r"\*\*type\*\*", line):
                in_type_list = True

            if in_type_list and line.startswith("- `"):
                for m in re.finditer(r"`([^`]+)`", line):
                    valid_types.add(m.group(1))
                    break  # only the first backtick term per line is the value

    return {"valid_tasks": valid_tasks, "valid_levels": valid_levels, "valid_types": valid_types}


# ---------------------------------------------------------------------------
# Index loading
# ---------------------------------------------------------------------------

def _load_index_ids(index_md: Path) -> set[str]:
    if not index_md.exists():
        return set()
    text = index_md.read_text(encoding="utf-8")
    ids: set[str] = set()
    # [[id]] wikilink format
    ids.update(re.findall(r"\[\[([^\]|]+)\]\]", text))
    # plain | id | row format (first cell, no brackets)
    for m in re.finditer(r"^\|\s*([^\[|\s][^|]*?)\s*\|", text, re.MULTILINE):
        candidate = m.group(1).strip()
        if candidate and candidate not in ("ID", "---", "----"):
            ids.add(candidate)
    return ids


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

def _parse_frontmatter(content: str) -> tuple[dict, str]:
    if not content.startswith("---"):
        return {}, content
    end = content.index("---", 3)
    fm = yaml.safe_load(content[3:end]) or {}
    body = content[end + 3:]
    return fm, body


# ---------------------------------------------------------------------------
# Individual checks
# ---------------------------------------------------------------------------

def _issue(severity: str, paper_id: str, check: str, message: str) -> Issue:
    return Issue(severity=severity, module="ingest", paper_id=paper_id, check=check, message=message)


def _check_id_is_string(paper_id: str, fm: dict) -> list[Issue]:
    raw_id = fm.get("id")
    if raw_id is not None and not isinstance(raw_id, str):
        return [_issue("error", paper_id, "id_is_string",
                       f"id field parsed as {type(raw_id).__name__} ({raw_id!r}), not string — "
                       f"add quotes in frontmatter: id: \"{paper_id}\"")]
    return []


def _check_required_fields(paper_id: str, fm: dict) -> list[Issue]:
    issues = []
    for f in REQUIRED_FM_FIELDS:
        if f not in fm or fm[f] is None:
            issues.append(_issue("error", paper_id, "required_fields", f"Missing required frontmatter field: {f}"))
    fs = fm.get("field_significance")
    if isinstance(fs, dict):
        if "level" not in fs:
            issues.append(_issue("error", paper_id, "required_fields", "field_significance missing sub-key: level"))
        if "type" not in fs:
            issues.append(_issue("error", paper_id, "required_fields", "field_significance missing sub-key: type"))
    return issues


def _check_required_sections(paper_id: str, fm: dict, body: str) -> list[Issue]:
    issues = []
    if "[!abstract]" not in body.lower():
        issues.append(_issue("error", paper_id, "required_sections", "Missing abstract callout (> [!abstract])"))
    if "## Wiki Connections" not in body:
        issues.append(_issue("error", paper_id, "required_sections", "Missing required section: ## Wiki Connections"))
    # Tier 2 stubs must have Context in Speech Generation (or Scope and Coverage for surveys)
    if fm.get("ingest_tier") == 2:
        tags = fm.get("tags") or []
        is_survey = "survey" in tags
        has_context = "## Context in Speech Generation" in body
        has_scope = "## Scope and Coverage" in body
        if not has_context and not (is_survey and has_scope):
            issues.append(_issue("error", paper_id, "required_sections",
                                 "Tier 2 paper missing required section: ## Context in Speech Generation "
                                 "(or ## Scope and Coverage for survey papers)"))
    return issues


def _check_vocabulary(paper_id: str, fm: dict, vocab: dict) -> list[Issue]:
    issues = []

    task_list = fm.get("task") or []
    if isinstance(task_list, list):
        for t in task_list:
            if t not in vocab["valid_tasks"]:
                issues.append(_issue("error", paper_id, "vocabulary_valid", f"Invalid task value: {t!r}"))

    fs = fm.get("field_significance") or {}
    if isinstance(fs, dict):
        level = fs.get("level")
        if level and level not in vocab["valid_levels"]:
            issues.append(_issue("error", paper_id, "vocabulary_valid", f"Invalid field_significance.level: {level!r}"))

        types = fs.get("type") or []
        if isinstance(types, list):
            for t in types:
                if t not in vocab["valid_types"]:
                    issues.append(_issue("error", paper_id, "vocabulary_valid", f"Invalid field_significance.type: {t!r}"))

    return issues


def _check_claims_section(paper_id: str, fm: dict, body: str) -> list[Issue]:
    if fm.get("ingest_tier") == 2:
        return []

    if "## Claims" not in body:
        return [_issue("error", paper_id, "claims_section", "Missing ## Claims section")]

    # Extract section body up to the next ## heading
    start = body.index("## Claims") + len("## Claims")
    next_heading = re.search(r"\n## ", body[start:])
    section = body[start : start + next_heading.start()] if next_heading else body[start:]

    # Group each "- " bullet with its continuation lines. The citation lives on
    # the Evidence line, not the bullet itself. Two formats are accepted:
    #   New:  "  > *Evidence:* ... *(§N.N)*"  (blockquote, post-2026-07-02)
    #   Old:  "  Evidence: ... *(§N.N)*"       (inline continuation, legacy)
    lines = section.splitlines()
    blocks: list[str] = []
    for ln in lines:
        if ln.strip().startswith("- "):
            blocks.append(ln)
        elif blocks and ln.strip():
            blocks[-1] += "\n" + ln

    if not blocks:
        return [_issue("error", paper_id, "claims_section",
                       "## Claims section has no bullet points")]

    uncited = [b for b in blocks if "*(§" not in b and "*(Appendix" not in b]
    if uncited:
        return [_issue("error", paper_id, "claims_section",
                       f"{len(uncited)}/{len(blocks)} claims missing *(§N.N)* citation")]

    return []


def _check_figure_links(paper_id: str, body: str) -> list[Issue]:
    issues = []
    assets_dir = PARSED_DIR / paper_id / "assets"
    for m in re.finditer(r"assets/(figure-\d+\.png)", body):
        asset_name = m.group(1)
        if not (assets_dir / asset_name).exists():
            issues.append(_issue("warning", paper_id, "figure_links_exist",
                                 f"Referenced asset not found: assets/{asset_name}"))
    return issues


def _check_related_concepts(paper_id: str, fm: dict, concept_slugs: set[str]) -> list[Issue]:
    issues = []
    for slug in (fm.get("related_concepts") or []):
        if slug not in concept_slugs:
            issues.append(_issue("warning", paper_id, "related_concepts_exist",
                                 f"Concept slug not found in wiki/concepts/: {slug!r}"))
    return issues


def _check_wikilink_format(paper_id: str, body: str) -> list[Issue]:
    issues = []
    for m in re.finditer(r"\[\[([^\]]+)\]\]", body):
        link = m.group(1)
        if "|" not in link and _PAPER_ID_RE.match(link):
            issues.append(_issue("warning", paper_id, "wikilink_format",
                                 f"Bare paper ID wikilink — prefer [[{link}|Display Name]]: [[{link}]]"))
    return issues


def _check_in_index(paper_id: str, fm: dict, index_ids: set[str]) -> list[Issue]:
    # Use filename stem as canonical ID — fm["id"] may parse as float (YAML) for arXiv IDs
    if paper_id not in index_ids:
        return [_issue("error", paper_id, "in_paper_index",
                       f"Paper not found in wiki/papers/index.md")]
    return []


def _check_tier2_callout(paper_id: str, fm: dict, body: str) -> list[Issue]:
    if fm.get("ingest_tier") == 2:
        if "[!info]" not in body.lower():
            return [_issue("error", paper_id, "tier2_has_callout",
                           "Tier 2 paper missing > [!info] Citation Stub callout")]
    return []


# ---------------------------------------------------------------------------
# Index document check (corpus-wide, skipped in single-paper mode)
# ---------------------------------------------------------------------------

_EXPECTED_INDEX_COLS = 8
_INDEX_SEPARATOR_RE = re.compile(r"^\|[-| ]+\|$")


def _check_index_document(wiki_papers: Path, index_md: Path) -> list[Issue]:
    if not index_md.exists():
        return [_issue("error", "index.md", "index_document", "wiki/papers/index.md not found")]

    text = index_md.read_text(encoding="utf-8")
    page_stems = {p.stem for p in wiki_papers.glob("*.md") if p.name != "index.md"}
    seen: dict[str, int] = {}  # paper_id -> first line number
    issues: list[Issue] = []

    in_table = False
    for lineno, line in enumerate(text.splitlines(), 1):
        if "| ID |" in line:
            in_table = True
        if in_table and line.strip() == "":
            issues.append(_issue("error", "index.md", "index_blank_row",
                                 f"Line {lineno}: blank line inside table breaks rendering"))
        if not line.startswith("|"):
            continue
        if "| ID |" in line or _INDEX_SEPARATOR_RE.match(line):
            continue

        cells = [c.strip() for c in line.split("|")[1:-1]]

        if len(cells) != _EXPECTED_INDEX_COLS:
            issues.append(_issue("error", "index.md", "index_column_count",
                                 f"Line {lineno}: expected {_EXPECTED_INDEX_COLS} columns, got {len(cells)}"))
            continue

        id_cell, title_cell = cells[0], cells[1]

        # [[id]] wikilink format in ID column
        wl = re.match(r"^\[\[([^\]]+)\]\]$", id_cell)
        if not wl:
            issues.append(_issue("error", "index.md", "index_wikilink_format",
                                 f"Line {lineno}: ID column not in [[id]] format: {id_cell!r}"))
            continue

        paper_id = wl.group(1)

        # Duplicate IDs
        if paper_id in seen:
            issues.append(_issue("error", paper_id, "index_duplicate",
                                 f"Line {lineno}: duplicate entry (first seen line {seen[paper_id]})"))
        else:
            seen[paper_id] = lineno

        # Corresponding page file exists
        if paper_id not in page_stems:
            issues.append(_issue("error", paper_id, "index_page_missing",
                                 f"Line {lineno}: [[{paper_id}]] in index has no wiki/papers/{paper_id}.md"))

        # Title link target matches ID column
        link = re.search(r"\(papers/([^)]+)\.md\)", title_cell)
        if link:
            if link.group(1) != paper_id:
                issues.append(_issue("error", paper_id, "index_link_mismatch",
                                     f"Line {lineno}: link target 'papers/{link.group(1)}.md' does not match [[{paper_id}]]"))
        else:
            issues.append(_issue("warning", paper_id, "index_title_format",
                                 f"Line {lineno}: title cell has no markdown link"))

    return issues


# ---------------------------------------------------------------------------
# Per-page dispatcher
# ---------------------------------------------------------------------------

def _check_page(
    page: Path,
    vocab: dict,
    index_ids: set[str],
    concept_slugs: set[str],
) -> list[Issue]:
    paper_id = page.stem
    content = page.read_text(encoding="utf-8")

    try:
        fm, body = _parse_frontmatter(content)
    except yaml.YAMLError as e:
        return [_issue("error", paper_id, "frontmatter_parses", f"YAML parse error: {e}")]
    except ValueError:
        return [_issue("error", paper_id, "frontmatter_parses", "Could not find closing --- delimiter")]

    if not fm:
        return [_issue("error", paper_id, "frontmatter_parses", "No YAML frontmatter found")]

    issues: list[Issue] = []
    issues += _check_id_is_string(paper_id, fm)
    issues += _check_required_fields(paper_id, fm)
    issues += _check_required_sections(paper_id, fm, body)
    issues += _check_vocabulary(paper_id, fm, vocab)
    issues += _check_claims_section(paper_id, fm, body)
    issues += _check_figure_links(paper_id, body)
    issues += _check_related_concepts(paper_id, fm, concept_slugs)
    issues += _check_wikilink_format(paper_id, body)
    issues += _check_in_index(paper_id, fm, index_ids)
    issues += _check_tier2_callout(paper_id, fm, body)
    return issues


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def run(args: CheckArgs) -> ModuleResult:
    wiki_root = args.wiki_dir if args.wiki_dir else _DEFAULT_WIKI
    wiki_papers = wiki_root / "papers"
    wiki_concepts = wiki_root / "concepts"
    index_md = wiki_papers / "index.md"

    vocab = _load_vocabulary()
    index_ids = _load_index_ids(index_md)
    concept_slugs = {p.stem for p in wiki_concepts.glob("*.md") if p.stem != "index"} if wiki_concepts.exists() else set()

    if args.paper_id:
        pages = [wiki_papers / f"{args.paper_id}.md"]
    else:
        pages = sorted(p for p in wiki_papers.glob("*.md") if p.name != "index.md")

    issues: list[Issue] = []
    if not args.paper_id:
        issues.extend(_check_index_document(wiki_papers, index_md))

    for page in pages:
        if not page.exists():
            issues.append(_issue("error", args.paper_id or page.stem, "frontmatter_parses",
                                 f"Page not found: {page}"))
            continue
        issues.extend(_check_page(page, vocab, index_ids, concept_slugs))

    errors = sum(1 for i in issues if i.severity == "error")
    warnings = sum(1 for i in issues if i.severity == "warning")

    return ModuleResult(
        module="ingest",
        passed=errors == 0,
        issues=issues,
        stats={"papers_checked": len(pages), "errors": errors, "warnings": warnings},
    )
