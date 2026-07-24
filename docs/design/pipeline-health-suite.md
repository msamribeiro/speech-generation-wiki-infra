# Pipeline Health Suite — Design Document

**Project:** Speech Synthesis Research Wiki  
**Scope:** Automated validation of pipeline outputs at each stage, combined with a health dashboard for the knowledge base  
**Depends on:** All pipeline stages (fetch, parse, ingest, integrate, render) — the suite reads their outputs but does not run them  
**Status:** Partially implemented — `ingest` module complete (2026-06-19), `integrate` module complete (2026-07-15); `fetch`, `parse`, `render`, `corpus` modules and `--report` dashboard still planned  

---

## 1. Goals and Non-Goals

### Goals

- Provide a single command (`scripts/health_check.py`) that validates the output of every pipeline stage
- Catch problems as close to their source as possible — run per-stage checks immediately after each pass, not only at the end
- Generate `STATUS_DASHBOARD.md` as a human-readable summary of corpus health, replacing any standalone dashboard script
- Serve as the authoritative source for corpus counts (paper totals, ingested, integrated) so these are never maintained by hand
- Be wirable into a pre-commit or pre-push hook in the wiki content repo so failures surface before they reach the published site
- Allow scoping to a single paper (`--id`) for fast post-ingest validation

### Non-Goals

- Running pipeline stages — the suite validates outputs, it does not produce them
- Fixing issues automatically — it reports; humans (or targeted scripts) fix
- Replacing the corpus_summary.py script — that script serves a different purpose (month-by-month pipeline progress); the health suite reports correctness, not progress
- Semantic quality review — whether a paper page is *well written* is out of scope; the ingest module checks structural correctness only. The page quality audit (manual editorial review) is a separate activity

---

## 2. Architecture

### 2.1 Entry Point

`scripts/health_check.py` is the single entry point. It discovers and runs all check modules, or a named subset.

```
python scripts/health_check.py                    # run all modules
python scripts/health_check.py --module ingest    # run one module
.venv/bin/python scripts/health_check.py --module agents  # validate Claude/Codex workflow parity
python scripts/health_check.py --module fetch,parse  # run multiple
python scripts/health_check.py --module ingest --id 2501.12345  # scope to one paper
python scripts/health_check.py --module integrate --concept flow-matching --phase 2  # scope to one concept YAML, force Phase 2 checks
python scripts/health_check.py --wiki-dir /path/to/standalone/content/checkout  # override wiki root (e.g. standalone content repo, not the infra submodule)
python scripts/health_check.py --report           # run all + write STATUS_DASHBOARD.md
```

Exit codes: `0` on clean (no errors), `1` if any module reports at least one error-level issue.

### 2.2 Module Layout

```
scripts/
  health_check.py          # entry point
  checks/
    agents.py              # validates shared agent instructions, skills, and adapters
    fetch.py               # validates raw/metadata/
    parse.py               # validates raw/parsed/
    ingest.py              # validates wiki/papers/
    integrate.py           # validates wiki/_claims/
    render.py              # validates concept Overview and In Depth pages
    corpus.py              # cross-cutting consistency
    _base.py               # shared dataclasses and helpers
```

The `agents` module is cross-cutting rather than a pipeline stage. It delegates to
`scripts/check_agent_compat.py`, runs as part of the default full suite, and should be run directly
after changes to agent contracts, skills, Claude adapters, or wiki path resolution. It is not a
session-start check because those files are static between edits.

### 2.3 Module Interface

Each module implements a single function:

```python
def run(args: CheckArgs) -> ModuleResult:
    ...
```

Where (matches `scripts/checks/_base.py` as actually implemented):

```python
@dataclass
class CheckArgs:
    paper_id: str | None = None    # if set, scope checks to this paper only (ingest)
    wiki_dir: Path | None = None   # override wiki root; defaults to the wiki/ submodule
    concept: str | None = None     # if set, scope checks to this concept YAML only (integrate)
    phase: int | None = None       # force Phase 1 or 2 checks (integrate); default auto-detects per YAML

@dataclass
class Issue:
    severity: str              # "error" | "warning"
    module: str                # which module raised it
    paper_id: str | None       # context ref, if applicable — a paper ID, concept slug, or
                                # concept-scoped composite ref (e.g. "{slug}:{paper_id}")
    check: str                 # short check name, e.g. "frontmatter_parses"
    message: str               # human-readable description

@dataclass
class ModuleResult:
    module: str
    passed: bool               # True if no error-level issues
    issues: list[Issue]
    stats: dict                # module-specific counts (e.g. papers_checked: 338)
```

`passed` is False if any issue has `severity == "error"`. Warnings do not affect `passed`.

**No central config injection.** There is no `config: dict` field on `CheckArgs` — each module
self-loads whatever config or reference docs it needs (e.g. `ingest.py` loads
`docs/schemas/vocabulary.md` directly; `integrate.py` loads `config/health_check.yaml` and
`docs/schemas/claims.md` directly). This was already the ingest module's pattern before the
integrate module existed; `integrate.py` follows the same precedent rather than the originally
sketched central-config design below, which was never implemented.

### 2.4 Severity Levels

| Severity | Meaning | Blocks hook? |
|----------|---------|-------------|
| `error` | Definite problem — a page is broken, a required field is missing, counts are inconsistent | Yes |
| `warning` | Likely problem requiring human judgement — parse output is suspiciously short, a reference count is zero | No |

### 2.5 Output Format

**Console output** (default), as actually implemented in `health_check.py::_print_result`:
errors and warnings lead, followed by a generic `key=value` dump of the remaining `stats` dict.
This was chosen over a hardcoded per-module noun ("N claim files", "N paper pages" as originally
sketched below) because `stats` dicts vary more across modules than a single count can express —
`integrate`, for instance, needs `concepts_checked`, `concept_files`, `total_paper_entries`, and
`papers_not_in_any_yaml` simultaneously visible, not folded into one number:

```
[ingest    ] PASS  (0 errors, 4 warnings | papers_checked=338)
[integrate ] PASS  (0 errors, 0 warnings | concepts_checked=1, concept_files=24, total_paper_entries=338, total_clusters=142, strongly_supported=48, contested=3, papers_not_in_any_yaml=12)
```

With `-v`/`--verbose`, or on any failing module, each issue prints on its own line:

```
  WARNING  parse  2511.21229  references_nonzero  references.json is empty (known: non-Latin heading)
  ERROR    corpus  —  count_mismatch  wiki/index.md reports 335 papers; metadata shows 338 ingested
```

**With `--report`:** also writes `STATUS_DASHBOARD.md` (see §8).

---

## 3. Fetch Module

**File:** `scripts/checks/fetch.py`  
**Reads:** `raw/metadata/*.json`  
**Scope:** All metadata files, or a single file if `--id` is set  

### Checks

| Check | Severity | Description |
|-------|----------|-------------|
| `json_parses` | error | Each metadata file must parse as valid JSON |
| `required_fields` | error | Fields `id`, `title`, `published_date`, `status`, `venue` must be present and non-null |
| `status_valid` | error | `status` must be one of `pending`, `review`, `accepted`, `rejected`, `ingested` |
| `no_duplicate_ids` | error | No two metadata files may share the same `id` value |
| `title_collision` | warning | Two accepted/ingested papers whose normalised titles are ≥ 90% similar (Levenshtein); flag for dedup review |
| `arxiv_id_collision` | error | Two metadata files reference the same arXiv ID in different fields |

**Notes:**

- Title collision detection uses the same normalisation as `scripts/discover/` (lowercase, strip punctuation, collapse whitespace). The 90% threshold is tunable in config.
- This module absorbs the planned `scripts/discover/dedup_check.py`. Running it after each fetch batch is the intended workflow.

---

## 4. Parse Module

**File:** `scripts/checks/parse.py`  
**Reads:** `raw/metadata/*.json`, `raw/parsed/*/`, `raw/papers/`  
**Scope:** All accepted/ingested papers, or a single paper if `--id` is set  

### Checks

| Check | Severity | Description |
|-------|----------|-------------|
| `pdf_exists` | warning | Accepted papers (not yet ingested) should have a local PDF at `raw/papers/{id}.pdf` |
| `paper_md_exists` | error | Papers with `status: ingested` must have `raw/parsed/{id}/paper.md` |
| `paper_md_length` | warning | `paper.md` with fewer than 200 lines is flagged for manual review (possible truncation) |
| `references_nonzero` | warning | `references.json` with zero entries is flagged unless the paper ID appears in `parse_quality_review.md` exceptions |
| `assets_present` | warning | If `paper.md` contains `[FIGURE` placeholders, `raw/parsed/{id}/assets/` must exist and be non-empty |
| `abstract_nonnull` | warning | `raw/parsed/{id}/metadata.json` abstract field must be non-null |

**Notes:**

- `parse_quality_review.md` serves as the exception list for known-good zero-reference papers (e.g. `2511.21229`, which has a Thai-language reference heading). The module reads this file to avoid false positives.
- The 200-line threshold for `paper_md_length` is a warning, not an error, because short papers (challenge reports, 2-page papers) are genuinely short. A human decides whether to re-parse.
- `pdf_exists` is a warning because PDFs are gitignored and may not be present on all machines; it is informational rather than a correctness failure.

---

## 5. Ingest Module

**File:** `scripts/checks/ingest.py`  
**Reads:** `wiki/papers/*.md`, `raw/metadata/*.json`, `config/`, `wiki/papers/index.md`, `wiki/concepts/`  
**Scope:** All ingested paper pages, or a single page if `--id` is set  

This is the primary post-ingest validation module. Running `health_check.py --module ingest --id <id>` immediately after ingesting a paper is the intended workflow.

### Checks

| Check | Severity | Description |
|-------|----------|-------------|
| `frontmatter_parses` | error | YAML frontmatter must parse without errors |
| `required_fields` | error | Frontmatter fields `paper_id`, `title`, `venue`, `published_date`, `tasks`, `field_significance` must be present |
| `required_sections` | error | Page must contain `## Abstract`, `## Context in Speech Generation`, and at least one of `## Key Contributions` / `## Methods` |
| `vocabulary_valid` | error | `field_significance.type` must be one of the allowed values in `docs/schemas/vocabulary.md`; `tasks` entries must be from the controlled task list |
| `claim_citations` | warning | Each claim bullet under `## Key Contributions` or `## Methods` should include at least one `*(§N.N*)` inline citation |
| `figure_links_exist` | warning | Figure references in the page body must point to files that exist under `raw/parsed/{id}/assets/` |
| `related_concepts_exist` | warning | Each slug in `related_concepts` frontmatter must correspond to a file in `wiki/concepts/` |
| `wikilink_format` | warning | Wikilinks should use `[[id\|Display Name]]` format; bare `[[id]]` without display name is flagged |
| `in_paper_index` | error | The paper ID must appear as a row in `wiki/papers/index.md` |
| `tier2_has_callout` | error | Pages with `tier: 2` in frontmatter must contain a `> [!note] Citation Stub` callout block |

**Notes:**

- `vocabulary_valid` requires loading `docs/schemas/vocabulary.md` and extracting the allowed value lists. These are parsed once at module startup and cached.
- `related_concepts_exist` is a warning (not error) because concept pages are created in the render stage and may not yet exist when a paper page is first ingested.
- The `claim_citations` check is intentionally a warning — older pages written before the §N.N citation convention was established will fail it; the page quality audit handles the retroactive pass.

---

## 6. Integrate Module

**File:** `scripts/checks/integrate.py`  
**Reads:** `wiki/_claims/*.yaml`, `raw/metadata/*.json`, `config/health_check.yaml`, `docs/content.md`, `docs/schemas/claims.md`  
**Scope:** All claim YAML files, or a single one via `--concept {slug}` (replaces `--id` for this module — concept YAMLs are not paper-scoped)  
**Implemented:** 2026-07-15

Integration is split into Phase 1 (paper entry extraction) and Phase 2 (claim cluster / method
family synthesis). The module is phase-aware per YAML: a heuristic (non-empty `claim_clusters`
→ post-Phase-2) picks the check tier, unless `--phase 1` or `--phase 2` forces it explicitly.

```bash
python scripts/health_check.py --module integrate                        # all YAMLs, full checks
python scripts/health_check.py --module integrate --concept {slug}       # single YAML, full checks
python scripts/health_check.py --module integrate --concept {slug} --phase 1  # Phase 1 checks only
python scripts/health_check.py --module integrate --concept {slug} --phase 2  # full checks
```

This module absorbs `scripts/wiki/validate_concept_evidence.py` (never built as a standalone
script — this module was implemented directly instead).

### Phase 1 checks (run after every paper entry write, and standalone with `--phase 1`)

| Check | Severity | Description |
|-------|----------|-------------|
| `yaml_parses` | error | Each `wiki/_claims/{slug}.yaml` must parse as valid YAML |
| `required_top_keys` | error | `concept`, `last_updated`, `paper_count`, `papers` must be present |
| `paper_count_matches` | error | `paper_count` must equal `len(papers)` |
| `no_duplicate_paper_ids` | error | No two entries in `papers` may share the same `id` |
| `paper_id_is_string` | error | Each paper entry's `id` must parse as a YAML string, not a float — unquoted arXiv-style IDs (e.g. `1412.6980`) parse as floats and silently lose trailing zeros, corrupting every downstream lookup |
| `paper_entry_required_fields` | error | Each paper entry must have: `id`, `entry_date`, `year`, `venue`, `relevance`, `evidence_role`, `current_role`, `claims` |
| `entry_date_present` | error | `entry_date` must be non-null and a valid date (string or YAML date/datetime) |
| `claim_required_fields` | error | Each claim under a paper entry must have: `claim_id`, `role`, `claim`, `source`, `evidence`, `confidence`, `relevance` |
| `claim_source_nonnull` | error | Every claim's `source` field must be non-null and non-empty |
| `no_duplicate_claim_ids` | error | `claim_id` values must be unique within each paper entry |
| `vocabulary_paper_level` | error | `relevance`, `current_role` must be from the controlled vocabulary in `docs/schemas/claims.md`; `evidence_role` values must all be from the Evidence Role Vocabulary |
| `vocabulary_claim_level` | error | `role`, `confidence`, `relevance` on each claim must be from controlled vocabulary |
| `no_tier2_papers` | error | No paper entry may reference a paper ID with `ingest_tier: 2` in `raw/metadata/` |
| `paper_ids_exist` | error | Every paper `id` must have a corresponding `raw/metadata/{id}.json` |
| `paper_ids_ingested` | warning | Papers in the YAML should have `status: ingested` in metadata; `status: accepted` is flagged |
| `concept_in_registry` | error | The top-level `concept` slug must appear in the canonical slug list in `config/health_check.yaml` |
| `registry_config_matches_docs` | warning | `config/health_check.yaml`'s slug list must match the backtick-span slugs in `docs/content.md`'s Concept Page Registry section (runs once per full pass, not per-concept) |

### Phase 2 checks (run after synthesis; include all Phase 1 checks plus the following)

| Check | Severity | Description |
|-------|----------|-------------|
| `required_synthesis_keys` | error | `claim_clusters`, `method_families`, `open_questions`, `trend_notes` must be present |
| `cluster_required_fields` | error | Each cluster must have: `id`, `claim`, `status`, `confidence`, `last_reviewed` |
| `no_duplicate_cluster_ids` | error | `id` values must be unique across all `claim_clusters` entries |
| `cluster_paper_refs_valid` | error | Every paper ID in `supporting_papers`, `contradicting_papers`, `refining_papers` must exist in `papers[].id` within the same file |
| `vocabulary_cluster` | error | `status` and `confidence` on each cluster must be from controlled vocabulary |
| `method_family_required_fields` | error | Each family entry must have: `id`, `name`, `summary`, `papers` |
| `method_family_paper_refs_valid` | error | Every paper ID in `method_families[].papers` must exist in `papers[].id` |
| `paper_method_family_refs_valid` | error | Non-empty `method_family` values on paper entries must reference IDs that exist in `method_families[].id` |
| `method_family_coverage` | warning | Paper entries with `method_family: []` after Phase 2 are flagged (expected during Phase 1, not after synthesis) |
| `cluster_last_reviewed` | warning | Clusters with `last_reviewed` older than `cluster_staleness_days` (config, default 180) are flagged as potentially stale |

### Stats emitted

```python
{
    "concepts_checked": 1,         # concept YAMLs whose issues were evaluated this run (scope-dependent)
    "concept_files": 24,           # number of _claims/*.yaml files (always corpus-wide)
    "total_paper_entries": 338,    # sum of len(papers) across all YAMLs (always corpus-wide)
    "total_clusters": 142,         # sum of len(claim_clusters) across all YAMLs
    "strongly_supported": 48,      # clusters with status: strongly_supported
    "contested": 3,                # clusters with status: contested
    "papers_not_in_any_yaml": 12,  # ingested, non-Tier-2 papers with no entry in any concept YAML
}
```

`papers_not_in_any_yaml` is the key integration-backlog signal and is always computed globally —
it cannot be meaningfully scoped by `--concept` (see design notes for rationale). No caching: at
current corpus scale a full scan is sub-second to low-single-digit seconds; revisit only if this
becomes a measured bottleneck.

**Design notes:** `docs/records/2026-06-24-integrate-health-check-design.md` — full rationale
and the four open implementation questions (all resolved 2026-07-15).

---

## 7. Render Module

**File:** `scripts/checks/render.py`  
**Reads:** `wiki/_claims/*.yaml`, `wiki/concepts/*.md`
**Scope:** All concepts with a corresponding claim YAML  

### Checks

| Check | Severity | Description |
|-------|----------|-------------|
| `overview_exists` | warning | Every `wiki/_claims/{slug}.yaml` should have a corresponding `wiki/concepts/{slug}.md`; missing pages are flagged as not yet rendered |
| `in_depth_exists` | warning | Every `wiki/_claims/{slug}.yaml` should have a corresponding `wiki/concepts/{slug}-in-depth.md` |
| `render_type_valid` | error | Overview and In Depth frontmatter must declare `overview` and `in-depth` respectively |
| `required_sections` | error | Each format must contain the required sections from `docs/design/concept-rendering.md` |
| `reciprocal_links` | warning | Overview and In Depth pages must link to each other |
| `source_digest_consistent` | warning | Each format's digest date must match YAML `last_updated` |
| `paper_count_consistent` | warning | Each format's `paper_count` must match the corresponding claim YAML |

**Notes:**

- Missing renderings are warnings because render runs are on demand and newly integrated concepts
  may have YAML before the next render pass.

---

## 8. Corpus Module

**File:** `scripts/checks/corpus.py`  
**Reads:** `raw/metadata/*.json`, `wiki/papers/*.md`, `wiki/papers/index.md`, `wiki/index.md`, `wiki/overview.md`, `wiki/venues/*.md`, `wiki/log.md`  
**Scope:** Always global — cannot be scoped to a single paper  

This module checks cross-cutting consistency across the pipeline. Its `stats` output is the authoritative source for corpus counts in `STATUS_DASHBOARD.md`.

### Checks

| Check | Severity | Description |
|-------|----------|-------------|
| `ingested_has_page` | error | Every `raw/metadata/{id}.json` with `status: ingested` must have a corresponding `wiki/papers/{id}.md` |
| `page_has_metadata` | error | Every `wiki/papers/{id}.md` must have a corresponding `raw/metadata/{id}.json` (orphaned pages) |
| `index_count_matches` | error | Paper count in `wiki/index.md` must match the number of ingested metadata entries |
| `overview_count_matches` | warning | Paper count in `wiki/overview.md` must match the number of ingested metadata entries |
| `venue_counts_match` | warning | Per-venue paper counts in `wiki/venues/*.md` must match counts derivable from metadata |
| `broken_wikilinks` | error | Any `[[id]]` or `[[id\|Name]]` wikilink in a wiki page that does not resolve to a file in `wiki/papers/` or `wiki/concepts/` |
| `log_has_recent_entry` | warning | `wiki/log.md` should have an entry dated within the last ingest or integration pass |

**Stats emitted (used by `--report`):**

```python
{
    "total_metadata": 1037,
    "accepted": 699,
    "ingested": 338,
    "papers_not_in_any_yaml": 12,  # from the integrate module — replaces the old "integrated" count
    "rejected": 0,
    "pending": 0,
    "concept_files": 24,
    "rendered_concepts": 24,
}
```

---

## 9. Dashboard Report

Running `health_check.py --report` writes `STATUS_DASHBOARD.md` in the infra repo root after running all modules.

### Format

```markdown
# Pipeline Health Dashboard

Generated: 2026-06-19  
Corpus: 1037 total | 699 ready | 338 ingested | 276 integrated | 24 concepts

## Summary

| Module   | Status | Errors | Warnings |
|----------|--------|--------|----------|
| fetch    | PASS   | 0      | 0        |
| parse    | PASS   | 0      | 2        |
| ingest   | PASS   | 0      | 4        |
| integrate| PASS   | 0      | 0        |
| render   | PASS   | 0      | 1        |
| corpus   | FAIL   | 1      | 0        |

## Issues

### corpus

| Severity | Paper | Check | Message |
|----------|-------|-------|---------|
| ERROR | — | count_mismatch | wiki/index.md reports 335 papers; metadata shows 338 ingested |

### parse (warnings)

| Severity | Paper | Check | Message |
|----------|-------|-------|---------|
| WARNING | 2511.21229 | references_nonzero | references.json is empty (known: non-Latin heading) |
| WARNING | 2512.17293 | paper_md_length | paper.md is 117 lines (< 200 threshold) |
```

---

## 10. Configuration

```yaml
# config/health_check.yaml

fetch:
  title_collision_threshold: 0.90   # Levenshtein similarity for dedup warning

parse:
  paper_md_min_lines: 200
  known_zero_ref_exceptions: "raw/parsed/parse_quality_review.md"

ingest:
  vocabulary_doc: "docs/schemas/vocabulary.md"
  claim_citation_pattern: "§\\d+\\.\\d+"

integrate:
  concept_registry:                 # canonical concept slugs; kept in sync with
    - flow-matching                 # docs/content.md's Concept Page Registry via
    - diffusion-tts                 # the registry_config_matches_docs warning check
    # ...                           # (see config/health_check.yaml for the full list)
  cluster_staleness_days: 180       # cluster_last_reviewed warning threshold, Phase 2

```

---

## 11. Running the Suite

### After an ingest pass

```bash
python scripts/health_check.py --module ingest --id 2501.12345
# Validates the single paper page just written; fast feedback
```

### After an integration pass

```bash
python scripts/health_check.py --module integrate,corpus
# Checks all claim YAML files and cross-cutting counts
```

### After a render pass

```bash
python scripts/health_check.py --module render,corpus
```

### Full health check with dashboard

```bash
python scripts/health_check.py --report
# Runs all modules, writes STATUS_DASHBOARD.md
```

### Pre-commit hook (wiki content repo)

The hook calls `health_check.py --module ingest,integrate,render,corpus` (skipping fetch and parse, which read from the infra repo rather than the content repo). Exit code 1 blocks the commit.

---

## 12. Open Questions

1. **Where does `health_check.py` live?** Currently specified at `scripts/health_check.py` in the infra repo. The fetch and parse modules read from infra (`raw/`); the ingest, integrate, render, and corpus modules read from the wiki content repo (via the `wiki/` submodule path). This means the full suite can only run from the infra repo. The pre-commit hook in the wiki content repo would need to either invoke it via a relative path to the infra checkout, or a subset of modules could be split into a standalone runner in the wiki content repo. Decide before implementation.

2. **Parse quality review exception list:** The parse module cross-references `raw/parsed/parse_quality_review.md` for known-good zero-reference papers. This file is prose, not machine-readable. Either convert it to a structured exception list (e.g. `config/parse_exceptions.yaml`) or add a simple parsing step. Recommend: add a `## Known Zero-Reference Papers` section to `parse_quality_review.md` with a YAML code block the module can extract.

3. **Broken wikilink scope:** The corpus module checks wikilinks across all wiki pages. For a 338-paper corpus this is manageable, but as the corpus grows, scanning every page on each run will slow down. Consider caching wikilink extractions and only re-scanning pages modified since the last run (via git mtime or a manifest file).

4. **Hook scope in wiki content repo:** The pre-commit hook should run fast. The ingest module scoping (`--id`) helps for single-paper commits, but the corpus module is always global. Profiling will be needed once the suite is implemented to decide whether the global checks are fast enough for a pre-commit hook or should be relegated to a pre-push hook.

5. **`STATUS_DASHBOARD.md` location:** Currently specified as infra repo root. It could instead live in the wiki content repo (`wiki/STATUS_DASHBOARD.md`) so it is visible alongside the published content. Tradeoff: infra root is closer to where `health_check.py` runs and keeps the wiki content repo clean of operational files.
