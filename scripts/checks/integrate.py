"""
Integrate module for the Pipeline Health Suite.

Validates the claim graph in wiki/_claims/*.yaml for structural correctness.
Integration is split into Phase 1 (paper entry extraction) and Phase 2 (claim
cluster / method family synthesis) — see the integration agent spec
(.claude/agents/speech-generation-integration-agent.md) and the design notes
at docs/records/2026-06-24-integrate-health-check-design.md.

Phase is auto-detected per YAML (non-empty claim_clusters => post-Phase-2)
unless --phase is passed explicitly.
"""

import json
import re
from datetime import date, datetime
from pathlib import Path

import yaml

from checks._base import CheckArgs, Issue, ModuleResult

ROOT = Path(__file__).parent.parent.parent
_DEFAULT_WIKI = ROOT / "wiki"
METADATA_DIR = ROOT / "raw" / "metadata"
CONTENT_DOC = ROOT / "docs" / "content.md"
CLAIMS_SCHEMA_DOC = ROOT / "docs" / "schemas" / "claims.md"
HEALTH_CHECK_CONFIG = ROOT / "config" / "health_check.yaml"

RELEVANCE_VALUES = {"high", "medium", "low"}
CONFIDENCE_VALUES = {"high", "medium", "low"}
DEFAULT_STALENESS_DAYS = 180

REQUIRED_TOP_KEYS = ["concept", "last_updated", "paper_count", "papers"]
REQUIRED_PAPER_FIELDS = [
    "id", "entry_date", "year", "venue", "relevance", "evidence_role", "current_role", "claims",
]
REQUIRED_CLAIM_FIELDS = [
    "claim_id", "role", "claim", "source", "evidence", "confidence", "relevance",
]
REQUIRED_SYNTHESIS_KEYS = ["claim_clusters", "method_families", "open_questions", "trend_notes"]
REQUIRED_CLUSTER_FIELDS = ["id", "claim", "status", "confidence", "last_reviewed"]
REQUIRED_FAMILY_FIELDS = ["id", "name", "summary", "papers"]

CLUSTER_PAPER_REF_FIELDS = ["supporting_papers", "contradicting_papers", "refining_papers"]


# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

def _load_config() -> dict:
    if not HEALTH_CHECK_CONFIG.exists():
        return {"concept_registry": [], "cluster_staleness_days": DEFAULT_STALENESS_DAYS}
    full = yaml.safe_load(HEALTH_CHECK_CONFIG.read_text(encoding="utf-8")) or {}
    data = full.get("integrate") or {}
    data.setdefault("concept_registry", [])
    data.setdefault("cluster_staleness_days", DEFAULT_STALENESS_DAYS)
    return data


def _load_docs_registry_slugs() -> set[str]:
    """Extract backtick-span slugs from the category rows of docs/content.md's
    Concept Page Registry section (skips the trailing explanatory paragraph,
    which also contains a backtick-quoted field name)."""
    if not CONTENT_DOC.exists():
        return set()
    text = CONTENT_DOC.read_text(encoding="utf-8")
    m = re.search(r"## Concept Page Registry\n(.*?)\n## ", text, re.DOTALL)
    if not m:
        return set()
    slugs: set[str] = set()
    for line in m.group(1).splitlines():
        if line.strip().startswith("**"):
            slugs.update(re.findall(r"`([a-z0-9-]+)`", line))
    return slugs


# ---------------------------------------------------------------------------
# Vocabulary loading (from docs/schemas/claims.md)
# ---------------------------------------------------------------------------

def _load_vocab_section(text: str, heading: str) -> set[str]:
    m = re.search(rf"## {re.escape(heading)}\n(.*?)\n## ", text, re.DOTALL)
    if not m:
        return set()
    values: set[str] = set()
    for line in m.group(1).splitlines():
        cell = re.match(r"\|\s*`([^`]+)`\s*\|", line)
        if cell:
            values.add(cell.group(1))
    return values


def _load_claims_vocabulary() -> dict:
    if not CLAIMS_SCHEMA_DOC.exists():
        return {"evidence_role": set(), "current_role": set(), "claim_status": set(), "claim_role": set()}
    text = CLAIMS_SCHEMA_DOC.read_text(encoding="utf-8")
    return {
        "evidence_role": _load_vocab_section(text, "Evidence Role Vocabulary"),
        "current_role": _load_vocab_section(text, "Current Role Vocabulary"),
        "claim_status": _load_vocab_section(text, "Claim Status Vocabulary"),
        "claim_role": _load_vocab_section(text, "Claim Role Vocabulary"),
    }


# ---------------------------------------------------------------------------
# Metadata loading
# ---------------------------------------------------------------------------

def _load_all_metadata() -> dict[str, dict]:
    metadata: dict[str, dict] = {}
    if not METADATA_DIR.exists():
        return metadata
    for path in METADATA_DIR.glob("*.json"):
        try:
            metadata[path.stem] = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
    return metadata


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _issue(severity: str, ref: str, check: str, message: str) -> Issue:
    return Issue(severity=severity, module="integrate", paper_id=ref, check=check, message=message)


def _valid_date(value) -> bool:
    # PyYAML auto-parses unquoted YYYY-MM-DD scalars into date/datetime objects
    # rather than leaving them as strings — accept both.
    if isinstance(value, (date, datetime)):
        return True
    if not isinstance(value, str):
        return False
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def _as_date(value) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


def _detect_phase(data: dict, forced_phase: int | None) -> int:
    if forced_phase is not None:
        return forced_phase
    return 2 if data.get("claim_clusters") else 1


# ---------------------------------------------------------------------------
# Phase 1 checks
# ---------------------------------------------------------------------------

def _check_phase1(slug: str, data: dict, papers: list, metadata: dict, claims_vocab: dict, config: dict) -> tuple[list[Issue], set[str]]:
    issues: list[Issue] = []

    declared_count = data.get("paper_count")
    if declared_count != len(papers):
        issues.append(_issue("error", slug, "paper_count_matches",
                             f"paper_count declared {declared_count!r}, actual {len(papers)}"))

    raw_ids = [p.get("id") for p in papers if isinstance(p, dict)]
    dupes = sorted({pid for pid in raw_ids if pid is not None and raw_ids.count(pid) > 1})
    if dupes:
        issues.append(_issue("error", slug, "no_duplicate_paper_ids", f"Duplicate paper IDs: {dupes}"))

    known_paper_ids = {pid for pid in raw_ids if pid is not None}

    for p in papers:
        if not isinstance(p, dict):
            issues.append(_issue("error", slug, "paper_entry_required_fields", f"Paper entry is not a mapping: {p!r}"))
            continue
        pid = p.get("id", "?")
        ref = f"{slug}:{pid}"

        # arXiv-style IDs (e.g. 1412.6980) parse as YAML floats unless quoted, which
        # silently drops trailing zeros (1412.6980 -> 1412.698) and breaks every
        # downstream lookup against raw/metadata/. Same hazard the ingest module
        # guards against for paper-page frontmatter (checks/ingest.py, id_is_string).
        if pid != "?" and not isinstance(pid, str):
            issues.append(_issue("error", ref, "paper_id_is_string",
                                 f"id field parsed as {type(pid).__name__} ({pid!r}), not string — "
                                 f"add quotes in the YAML: id: \"{pid}\""))

        missing = [f for f in REQUIRED_PAPER_FIELDS if f not in p or p[f] is None]
        if missing:
            issues.append(_issue("error", ref, "paper_entry_required_fields", f"Missing field(s): {missing}"))

        if not _valid_date(p.get("entry_date")):
            issues.append(_issue("error", ref, "entry_date_present",
                                 f"entry_date missing or invalid: {p.get('entry_date')!r}"))

        relevance = p.get("relevance")
        if relevance is not None and relevance not in RELEVANCE_VALUES:
            issues.append(_issue("error", ref, "vocabulary_paper_level", f"Invalid relevance: {relevance!r}"))

        current_role = p.get("current_role")
        if current_role is not None and current_role not in claims_vocab["current_role"]:
            issues.append(_issue("error", ref, "vocabulary_paper_level", f"Invalid current_role: {current_role!r}"))

        for er in (p.get("evidence_role") or []):
            if er not in claims_vocab["evidence_role"]:
                issues.append(_issue("error", ref, "vocabulary_paper_level", f"Invalid evidence_role: {er!r}"))

        meta = metadata.get(pid)
        if meta is None:
            issues.append(_issue("error", ref, "paper_ids_exist", f"No raw/metadata/{pid}.json found"))
        else:
            if str(meta.get("ingest_tier")) == "2":
                issues.append(_issue("error", ref, "no_tier2_papers",
                                     "Tier 2 paper must not appear in a concept YAML"))
            status = meta.get("status")
            if status != "ingested":
                issues.append(_issue("warning", ref, "paper_ids_ingested",
                                     f"Paper status is {status!r}, expected 'ingested'"))

        claims = p.get("claims") or []
        claim_ids = [c.get("claim_id") for c in claims if isinstance(c, dict)]
        claim_dupes = sorted({cid for cid in claim_ids if cid is not None and claim_ids.count(cid) > 1})
        if claim_dupes:
            issues.append(_issue("error", ref, "no_duplicate_claim_ids", f"Duplicate claim_id(s): {claim_dupes}"))

        for c in claims:
            if not isinstance(c, dict):
                issues.append(_issue("error", ref, "claim_required_fields", f"Claim entry is not a mapping: {c!r}"))
                continue
            cref = f"{ref}:{c.get('claim_id', '?')}"

            missing_c = [f for f in REQUIRED_CLAIM_FIELDS if f not in c or c[f] is None]
            if missing_c:
                issues.append(_issue("error", cref, "claim_required_fields", f"Missing field(s): {missing_c}"))

            source = c.get("source")
            if not source or not str(source).strip():
                issues.append(_issue("error", cref, "claim_source_nonnull", "source field is null or empty"))

            role = c.get("role")
            if role is not None and role not in claims_vocab["claim_role"]:
                issues.append(_issue("error", cref, "vocabulary_claim_level", f"Invalid role: {role!r}"))

            confidence = c.get("confidence")
            if confidence is not None and confidence not in CONFIDENCE_VALUES:
                issues.append(_issue("error", cref, "vocabulary_claim_level", f"Invalid confidence: {confidence!r}"))

            c_relevance = c.get("relevance")
            if c_relevance is not None and c_relevance not in RELEVANCE_VALUES:
                issues.append(_issue("error", cref, "vocabulary_claim_level", f"Invalid relevance: {c_relevance!r}"))

    concept_slug = data.get("concept")
    if concept_slug not in config["concept_registry"]:
        issues.append(_issue("error", slug, "concept_in_registry",
                             f"Concept slug {concept_slug!r} not in config/health_check.yaml registry"))

    return issues, known_paper_ids


# ---------------------------------------------------------------------------
# Phase 2 checks
# ---------------------------------------------------------------------------

def _check_phase2(slug: str, data: dict, papers: list, known_paper_ids: set[str], claims_vocab: dict, config: dict) -> list[Issue]:
    issues: list[Issue] = []

    missing_syn = [k for k in REQUIRED_SYNTHESIS_KEYS if k not in data]
    if missing_syn:
        issues.append(_issue("error", slug, "required_synthesis_keys", f"Missing key(s): {missing_syn}"))
        return issues

    clusters = data.get("claim_clusters") or []
    families = data.get("method_families") or []

    cluster_ids = [c.get("id") for c in clusters if isinstance(c, dict)]
    dupe_clusters = sorted({cid for cid in cluster_ids if cid is not None and cluster_ids.count(cid) > 1})
    if dupe_clusters:
        issues.append(_issue("error", slug, "no_duplicate_cluster_ids", f"Duplicate cluster id(s): {dupe_clusters}"))

    known_family_ids = {f.get("id") for f in families if isinstance(f, dict) and f.get("id") is not None}
    staleness_days = config.get("cluster_staleness_days", DEFAULT_STALENESS_DAYS)

    for c in clusters:
        if not isinstance(c, dict):
            issues.append(_issue("error", slug, "cluster_required_fields", f"Cluster entry is not a mapping: {c!r}"))
            continue
        cid = c.get("id", "?")
        cref = f"{slug}:cluster:{cid}"

        missing = [f for f in REQUIRED_CLUSTER_FIELDS if f not in c or c[f] is None]
        if missing:
            issues.append(_issue("error", cref, "cluster_required_fields", f"Missing field(s): {missing}"))

        status = c.get("status")
        if status is not None and status not in claims_vocab["claim_status"]:
            issues.append(_issue("error", cref, "vocabulary_cluster", f"Invalid status: {status!r}"))

        confidence = c.get("confidence")
        if confidence is not None and confidence not in CONFIDENCE_VALUES:
            issues.append(_issue("error", cref, "vocabulary_cluster", f"Invalid confidence: {confidence!r}"))

        for field_name in CLUSTER_PAPER_REF_FIELDS:
            for pid in (c.get(field_name) or []):
                if pid not in known_paper_ids:
                    issues.append(_issue("error", cref, "cluster_paper_refs_valid",
                                         f"{field_name} references unknown paper id: {pid!r}"))

        last_reviewed_date = _as_date(c.get("last_reviewed"))
        if last_reviewed_date is not None:
            days_stale = (date.today() - last_reviewed_date).days
            if days_stale > staleness_days:
                issues.append(_issue("warning", cref, "cluster_last_reviewed",
                                     f"last_reviewed {last_reviewed_date.isoformat()} is {days_stale} days old (threshold {staleness_days})"))

    for f in families:
        if not isinstance(f, dict):
            issues.append(_issue("error", slug, "method_family_required_fields", f"Family entry is not a mapping: {f!r}"))
            continue
        fid = f.get("id", "?")
        fref = f"{slug}:family:{fid}"

        missing = [k for k in REQUIRED_FAMILY_FIELDS if k not in f or f[k] is None]
        if missing:
            issues.append(_issue("error", fref, "method_family_required_fields", f"Missing field(s): {missing}"))

        for pid in (f.get("papers") or []):
            if pid not in known_paper_ids:
                issues.append(_issue("error", fref, "method_family_paper_refs_valid",
                                     f"papers references unknown paper id: {pid!r}"))

    for p in papers:
        if not isinstance(p, dict):
            continue
        pid = p.get("id", "?")
        ref = f"{slug}:{pid}"
        mf = p.get("method_family") or []
        if mf:
            for fid in mf:
                if fid not in known_family_ids:
                    issues.append(_issue("error", ref, "paper_method_family_refs_valid",
                                         f"method_family references unknown family id: {fid!r}"))
        else:
            issues.append(_issue("warning", ref, "method_family_coverage",
                                 "method_family is empty after Phase 2 synthesis"))

    return issues


# ---------------------------------------------------------------------------
# Per-file dispatcher
# ---------------------------------------------------------------------------

def _check_concept_yaml(path: Path, config: dict, claims_vocab: dict, metadata: dict, forced_phase: int | None) -> list[Issue]:
    slug = path.stem

    try:
        text = path.read_text(encoding="utf-8")
        data = yaml.safe_load(text)
    except yaml.YAMLError as e:
        return [_issue("error", slug, "yaml_parses", f"YAML parse error: {e}")]

    if not isinstance(data, dict):
        return [_issue("error", slug, "yaml_parses", "YAML did not parse to a mapping")]

    missing_top = [k for k in REQUIRED_TOP_KEYS if k not in data]
    if missing_top:
        return [_issue("error", slug, "required_top_keys", f"Missing top-level key(s): {missing_top}")]

    papers = data.get("papers")
    if not isinstance(papers, list):
        return [_issue("error", slug, "required_top_keys", "'papers' is not a list")]

    issues, known_paper_ids = _check_phase1(slug, data, papers, metadata, claims_vocab, config)

    phase = _detect_phase(data, forced_phase)
    if phase >= 2:
        issues.extend(_check_phase2(slug, data, papers, known_paper_ids, claims_vocab, config))

    return issues


# ---------------------------------------------------------------------------
# Corpus-wide stats (always global, regardless of --concept scope — see
# docs/records/2026-06-24-integrate-health-check-design.md, open question 3)
# ---------------------------------------------------------------------------

def _compute_stats(all_yaml_paths: list[Path], metadata: dict, concepts_checked: int) -> dict:
    total_paper_entries = 0
    total_clusters = 0
    strongly_supported = 0
    contested = 0
    covered_paper_ids: set[str] = set()

    for path in all_yaml_paths:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except yaml.YAMLError:
            continue
        if not isinstance(data, dict):
            continue

        papers = data.get("papers")
        if isinstance(papers, list):
            total_paper_entries += len(papers)
            for p in papers:
                if isinstance(p, dict) and p.get("id"):
                    covered_paper_ids.add(p["id"])

        clusters = data.get("claim_clusters")
        if isinstance(clusters, list):
            total_clusters += len(clusters)
            for c in clusters:
                if isinstance(c, dict):
                    if c.get("status") == "strongly_supported":
                        strongly_supported += 1
                    elif c.get("status") == "contested":
                        contested += 1

    eligible_ids = {
        pid for pid, m in metadata.items()
        if m.get("status") == "ingested" and str(m.get("ingest_tier")) != "2"
    }
    papers_not_in_any_yaml = len(eligible_ids - covered_paper_ids)

    return {
        "concepts_checked": concepts_checked,
        "concept_files": len(all_yaml_paths),
        "total_paper_entries": total_paper_entries,
        "total_clusters": total_clusters,
        "strongly_supported": strongly_supported,
        "contested": contested,
        "papers_not_in_any_yaml": papers_not_in_any_yaml,
    }


# ---------------------------------------------------------------------------
# Module entry point
# ---------------------------------------------------------------------------

def run(args: CheckArgs) -> ModuleResult:
    wiki_root = args.wiki_dir if args.wiki_dir else _DEFAULT_WIKI
    claims_dir = wiki_root / "_claims"

    config = _load_config()
    claims_vocab = _load_claims_vocabulary()
    metadata = _load_all_metadata()

    all_yaml_paths = sorted(claims_dir.glob("*.yaml")) if claims_dir.exists() else []

    if args.concept:
        target_paths = [claims_dir / f"{args.concept}.yaml"]
    else:
        target_paths = all_yaml_paths

    issues: list[Issue] = []

    if not args.concept:
        docs_slugs = _load_docs_registry_slugs()
        config_slugs = set(config["concept_registry"])
        if docs_slugs and docs_slugs != config_slugs:
            only_docs = sorted(docs_slugs - config_slugs)
            only_config = sorted(config_slugs - docs_slugs)
            detail = []
            if only_docs:
                detail.append(f"in docs/content.md but not config/health_check.yaml: {only_docs}")
            if only_config:
                detail.append(f"in config/health_check.yaml but not docs/content.md: {only_config}")
            issues.append(_issue("warning", "registry", "registry_config_matches_docs", "; ".join(detail)))

    for path in target_paths:
        if not path.exists():
            issues.append(_issue("error", path.stem, "yaml_parses", f"Concept YAML not found: {path}"))
            continue
        issues.extend(_check_concept_yaml(path, config, claims_vocab, metadata, args.phase))

    stats = _compute_stats(all_yaml_paths, metadata, len(target_paths))
    errors = sum(1 for i in issues if i.severity == "error")
    warnings = sum(1 for i in issues if i.severity == "warning")
    stats["errors"] = errors
    stats["warnings"] = warnings

    return ModuleResult(module="integrate", passed=errors == 0, issues=issues, stats=stats)
