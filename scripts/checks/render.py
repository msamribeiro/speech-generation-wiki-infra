"""Render module for the Pipeline Health Suite.

Validates the two human-facing renderings derived from each concept claim YAML:

- wiki/concepts/{slug}.md (Overview)
- wiki/concepts/{slug}-in-depth.md (In Depth)

Missing renderings are warnings because rendering is intentionally on demand. Once a
rendering exists, malformed frontmatter, missing required sections, invalid provenance,
or citations to papers outside the concept graph are errors.
"""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
import re

import yaml

from checks._base import CheckArgs, Issue, ModuleResult


ROOT = Path(__file__).parent.parent.parent
_DEFAULT_WIKI = ROOT / "wiki"

OVERVIEW_SECTIONS = (
    "Current State",
    "Method Landscape",
    "Key Trade-offs",
    "Open Questions",
    "Go Deeper",
    "Scope",
)
IN_DEPTH_SECTIONS = (
    "Findings at a Glance",
    "Scope",
    "Research Landscape",
    "What the Research Shows",
    "Where Findings Disagree",
    "How the Field Is Changing",
    "Implications",
    "Representative Reading Path",
    "Structured Source",
)
GENERATION_FIELDS = (
    "schema_version",
    "date",
    "stage",
    "mode",
    "runtime",
    "provider",
    "agent",
    "model",
    "commit",
)


def _issue(severity: str, slug: str, check: str, message: str) -> Issue:
    return Issue(
        severity=severity,
        module="render",
        paper_id=slug,
        check=check,
        message=message,
    )


def _as_iso(value) -> str | None:
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
        except ValueError:
            return None
    return None


def _parse_page(path: Path, slug: str) -> tuple[dict | None, str, list[Issue]]:
    issues: list[Issue] = []
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return None, text, [_issue("error", slug, "frontmatter_parses", f"{path.name}: missing YAML frontmatter")]
    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return None, text, [_issue("error", slug, "frontmatter_parses", f"{path.name}: {exc}")]
    if not isinstance(frontmatter, dict):
        return None, text, [_issue("error", slug, "frontmatter_parses", f"{path.name}: frontmatter is not a mapping")]
    return frontmatter, text[match.end():], issues


def _word_count(body: str) -> int:
    without_frontmatter = re.sub(r"^---\n.*?\n---\n", "", body, count=1, flags=re.DOTALL)
    return len(re.findall(r"\b[\w’'-]+\b", without_frontmatter))


def _validate_generation(slug: str, path: Path, frontmatter: dict) -> list[Issue]:
    issues: list[Issue] = []
    generation = frontmatter.get("generation")
    if not isinstance(generation, dict):
        return [_issue("error", slug, "generation_v2", f"{path.name}: generation block missing or invalid")]
    missing = [field for field in GENERATION_FIELDS if generation.get(field) in (None, "")]
    if missing:
        issues.append(_issue("error", slug, "generation_v2", f"{path.name}: missing generation fields {missing}"))
    if generation.get("schema_version") != 2:
        issues.append(_issue("error", slug, "generation_v2", f"{path.name}: schema_version must be 2"))
    if generation.get("stage") != "render":
        issues.append(_issue("error", slug, "generation_v2", f"{path.name}: stage must be 'render'"))
    if generation.get("mode") not in {"full", "light"}:
        issues.append(_issue("error", slug, "generation_v2", f"{path.name}: mode must be full or light"))
    if generation.get("agent") != "speech-generation-render-agent":
        issues.append(_issue("error", slug, "generation_v2", f"{path.name}: unexpected generation agent"))
    if _as_iso(generation.get("date")) is None:
        issues.append(_issue("error", slug, "generation_v2", f"{path.name}: generation date is invalid"))
    return issues


def _validate_page(
    slug: str,
    path: Path,
    expected_type: str,
    required_sections: tuple[str, ...],
    yaml_data: dict,
    known_paper_ids: set[str],
) -> list[Issue]:
    frontmatter, body, issues = _parse_page(path, slug)
    if frontmatter is None:
        return issues

    if frontmatter.get("draft") is True:
        issues.append(_issue("error", slug, "not_draft", f"{path.name}: production page still has draft: true"))
    if frontmatter.get("concept") != slug:
        issues.append(_issue("error", slug, "concept_matches", f"{path.name}: concept must be {slug!r}"))
    if frontmatter.get("render_type") != expected_type:
        issues.append(_issue(
            "error", slug, "render_type_valid",
            f"{path.name}: render_type {frontmatter.get('render_type')!r}, expected {expected_type!r}",
        ))

    yaml_date = _as_iso(yaml_data.get("last_updated"))
    page_date = _as_iso(frontmatter.get("source_digest_date"))
    if page_date != yaml_date:
        issues.append(_issue(
            "warning", slug, "source_digest_consistent",
            f"{path.name}: source_digest_date {page_date!r}, YAML last_updated {yaml_date!r}",
        ))
    if frontmatter.get("paper_count") != yaml_data.get("paper_count"):
        issues.append(_issue(
            "warning", slug, "paper_count_consistent",
            f"{path.name}: paper_count {frontmatter.get('paper_count')!r}, YAML {yaml_data.get('paper_count')!r}",
        ))

    issues.extend(_validate_generation(slug, path, frontmatter))

    headings = set(re.findall(r"^## (.+?)\s*$", body, re.MULTILINE))
    missing_sections = [section for section in required_sections if section not in headings]
    if missing_sections:
        issues.append(_issue(
            "error", slug, "required_sections",
            f"{path.name}: missing sections {missing_sections}",
        ))

    h1 = re.search(r"^# (.+?)\s*$", body, re.MULTILINE)
    if h1:
        issues.append(_issue(
            "error", slug, "no_body_h1",
            f"{path.name}: body H1 duplicates Quartz article title {h1.group(1)!r}",
        ))

    for heading in re.findall(r"^### (.+?)\s*$", body, re.MULTILINE):
        if re.match(r"^\d+\.\s", heading):
            issues.append(_issue(
                "warning", slug, "toc_heading_style",
                f"{path.name}: H3 should not use a numeric prefix: {heading!r}",
            ))
        if len(heading) > 60:
            issues.append(_issue(
                "warning", slug, "toc_heading_length",
                f"{path.name}: H3 is {len(heading)} characters; keep TOC labels at 60 or fewer: {heading!r}",
            ))

    count = _word_count(body)
    low, high = (700, 1400) if expected_type == "overview" else (2500, 6000)
    if count < low or count > high:
        issues.append(_issue(
            "warning", slug, "word_count_range",
            f"{path.name}: {count} words, expected {low}-{high}",
        ))

    if f"wiki/_claims/{slug}.yaml" not in body:
        issues.append(_issue(
            "error", slug, "structured_source_link",
            f"{path.name}: missing structured source path wiki/_claims/{slug}.yaml",
        ))

    linked_targets = re.findall(r"\[\[([^\]|]+)", body)
    cited_paper_ids = {
        target for target in linked_targets
        if not target.startswith("concepts/") and target not in {"overview"}
    }
    unknown_ids = sorted(cited_paper_ids - known_paper_ids)
    if unknown_ids:
        issues.append(_issue(
            "error", slug, "citations_in_claim_graph",
            f"{path.name}: citations not present in {slug}.yaml: {unknown_ids}",
        ))

    return issues


def _index_has_row(index_text: str, slug: str) -> bool:
    return (
        f"[[concepts/{slug}\\|" in index_text
        and f"[[concepts/{slug}-in-depth\\|" in index_text
    )


def _declares_render_type(path: Path) -> bool:
    """Distinguish an intentional concept placeholder from a production render."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return True  # Let normal validation report malformed frontmatter.
    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return True
    return not isinstance(frontmatter, dict) or frontmatter.get("render_type") is not None


def run(args: CheckArgs) -> ModuleResult:
    wiki_root = args.wiki_dir if args.wiki_dir else _DEFAULT_WIKI
    claims_dir = wiki_root / "_claims"
    concepts_dir = wiki_root / "concepts"
    all_yaml_paths = sorted(claims_dir.glob("*.yaml")) if claims_dir.exists() else []
    target_paths = [claims_dir / f"{args.concept}.yaml"] if args.concept else all_yaml_paths

    issues: list[Issue] = []
    rendered_overviews = 0
    rendered_in_depth = 0
    index_path = concepts_dir / "index.md"
    index_text = index_path.read_text(encoding="utf-8") if index_path.exists() else ""

    for yaml_path in target_paths:
        slug = yaml_path.stem
        if not yaml_path.exists():
            issues.append(_issue("error", slug, "yaml_parses", f"Concept YAML not found: {yaml_path}"))
            continue
        try:
            yaml_data = yaml.safe_load(yaml_path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            issues.append(_issue("error", slug, "yaml_parses", str(exc)))
            continue
        if not isinstance(yaml_data, dict):
            issues.append(_issue("error", slug, "yaml_parses", "YAML did not parse to a mapping"))
            continue

        known_paper_ids = {
            str(p.get("id")) for p in (yaml_data.get("papers") or [])
            if isinstance(p, dict) and p.get("id") is not None
        }
        overview_path = concepts_dir / f"{slug}.md"
        in_depth_path = concepts_dir / f"{slug}-in-depth.md"

        if not overview_path.exists() or not _declares_render_type(overview_path):
            issues.append(_issue(
                "warning", slug, "overview_exists",
                (
                    f"Missing {overview_path.relative_to(wiki_root)}"
                    if not overview_path.exists()
                    else f"{overview_path.relative_to(wiki_root)} is still a pre-render placeholder"
                ),
            ))
        else:
            rendered_overviews += 1
            issues.extend(_validate_page(
                slug, overview_path, "overview", OVERVIEW_SECTIONS, yaml_data, known_paper_ids,
            ))

        if not in_depth_path.exists():
            issues.append(_issue(
                "warning", slug, "in_depth_exists",
                f"Missing {in_depth_path.relative_to(wiki_root)}",
            ))
        else:
            rendered_in_depth += 1
            issues.extend(_validate_page(
                slug, in_depth_path, "in-depth", IN_DEPTH_SECTIONS, yaml_data, known_paper_ids,
            ))

        if overview_path.exists() and in_depth_path.exists():
            overview_text = overview_path.read_text(encoding="utf-8")
            in_depth_text = in_depth_path.read_text(encoding="utf-8")
            if f"[[concepts/{slug}-in-depth|" not in overview_text:
                issues.append(_issue(
                    "warning", slug, "reciprocal_links",
                    f"{overview_path.name}: missing link to In Depth page",
                ))
            if f"[[concepts/{slug}|" not in in_depth_text:
                issues.append(_issue(
                    "warning", slug, "reciprocal_links",
                    f"{in_depth_path.name}: missing link to Overview page",
                ))
            if not _index_has_row(index_text, slug):
                issues.append(_issue(
                    "warning", slug, "concept_index_entry",
                    "concepts/index.md lacks an Overview + In Depth row",
                ))

    errors = sum(issue.severity == "error" for issue in issues)
    warnings = sum(issue.severity == "warning" for issue in issues)
    return ModuleResult(
        module="render",
        passed=errors == 0,
        issues=issues,
        stats={
            "errors": errors,
            "warnings": warnings,
            "concepts_checked": len(target_paths),
            "overviews_rendered": rendered_overviews,
            "in_depth_rendered": rendered_in_depth,
        },
    )
