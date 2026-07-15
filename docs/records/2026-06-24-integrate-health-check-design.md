# Integrate Module — Health Check Design Notes (2026-06-24)

## Context

These notes document the design of `scripts/checks/integrate.py` following a session that
redesigned the integration agent from scratch. Read alongside:

- `docs/design/pipeline-health-suite.md` §6 — the existing thin stub for this module
- `docs/schemas/claims.md` — the full YAML schema (updated this session)
- `.claude/agents/speech-generation-integration-agent.md` — the rewritten agent spec

The existing §6 in the design doc is out of date and must be replaced with the checks defined
here before implementation begins.

---

## Key Design Changes That Affect the Module

### 1. Two-phase model

Integration is now split into Phase 1 (paper entry extraction) and Phase 2 (synthesis). The
health check module must be phase-aware: some checks are valid after Phase 1 only; full
cross-reference checks require Phase 2 to have run.

Invocation:

```bash
python scripts/health_check.py --module integrate                        # all YAMLs, full checks
python scripts/health_check.py --module integrate --concept {slug}       # single YAML, full checks
python scripts/health_check.py --module integrate --concept {slug} --phase 1  # Phase 1 checks only
python scripts/health_check.py --module integrate --concept {slug} --phase 2  # full checks
```

The `--concept` flag replaces `--id` for this module (concept YAMLs are not scoped to a paper ID).

### 2. `integrated_date` removed from metadata

`raw/metadata/{id}.json` no longer carries an `integrated_date` field. The per-concept
integration date is now `entry_date` on each paper entry in the YAML. Any check that
previously referenced `integrated_date` in metadata is dropped or reworked.

### 3. New schema fields

Two fields added to paper entries (see `docs/schemas/claims.md`):
- `entry_date: YYYY-MM-DD` — when the entry was written or last force-rewritten
- Per-claim `relevance: high | medium | low` — how central this claim is to the enclosing concept

Both must be validated.

### 4. Tier 2 papers excluded

Papers with `ingest_tier: 2` in `raw/metadata/` must not appear in any concept YAML. The
module should flag any that do as an error.

### 5. `method_family` written empty by Phase 1

Phase 1 always writes `method_family: []`. Phase 2 populates it. A paper entry with
`method_family: []` after Phase 2 is a warning, not an error (the family may not yet exist
with enough papers to warrant creation). A paper entry with a non-empty `method_family` that
references a non-existent family ID is an error.

---

## Full Check Set

### Phase 1 checks (run after every paper entry write, and standalone with `--phase 1`)

| Check | Severity | Description |
|-------|----------|-------------|
| `yaml_parses` | error | YAML must parse without errors |
| `required_top_keys` | error | `concept`, `last_updated`, `paper_count`, `papers` must be present |
| `paper_count_matches` | error | `paper_count` must equal `len(papers)` |
| `no_duplicate_paper_ids` | error | No two entries in `papers` may share the same `id` |
| `paper_entry_required_fields` | error | Each paper entry must have: `id`, `entry_date`, `year`, `venue`, `relevance`, `evidence_role`, `current_role`, `claims` |
| `entry_date_present` | error | `entry_date` must be non-null and parse as a valid date |
| `claim_required_fields` | error | Each claim under a paper entry must have: `claim_id`, `role`, `claim`, `source`, `evidence`, `confidence`, `relevance` |
| `claim_source_nonnull` | error | Every claim's `source` field must be non-null and non-empty |
| `no_duplicate_claim_ids` | error | `claim_id` values must be unique within each paper entry |
| `vocabulary_paper_level` | error | `relevance`, `current_role` must be from the controlled vocabulary in `docs/schemas/claims.md`; `evidence_role` values must all be from the Evidence Role Vocabulary |
| `vocabulary_claim_level` | error | `role`, `confidence`, `relevance` on each claim must be from controlled vocabulary |
| `no_tier2_papers` | error | No paper entry may reference a paper ID with `ingest_tier: 2` in `raw/metadata/` |
| `paper_ids_exist` | error | Every paper `id` must have a corresponding `raw/metadata/{id}.json` |
| `paper_ids_ingested` | warning | Papers in the YAML should have `status: ingested` in metadata; `status: accepted` is flagged |
| `concept_in_registry` | error | The top-level `concept` slug must appear in the canonical slug list in `config/health_check.yaml` |
| `registry_config_matches_docs` | warning | `config/health_check.yaml`'s slug list must match the backtick-span slugs in `docs/content.md`'s Concept Page Registry section (run once per full pass, not per-concept) |

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
| `cluster_last_reviewed` | warning | Clusters with `last_reviewed` older than 180 days are flagged as potentially stale |

---

## Stats Emitted

The module should emit these stats for use by `--report` / `STATUS_DASHBOARD.md`:

```python
{
    "concept_files": 24,          # number of _claims/*.yaml files
    "total_paper_entries": 338,   # sum of len(papers) across all YAMLs
    "total_clusters": 142,        # sum of len(claim_clusters) across all YAMLs
    "strongly_supported": 48,     # clusters with status: strongly_supported
    "contested": 3,               # clusters with status: contested
    "papers_not_in_any_yaml": 12, # ingested papers with no entry in any YAML (integration backlog)
}
```

`papers_not_in_any_yaml` is the key integration backlog signal: how many ingested, Tier 1
papers have no entry in any concept YAML. This replaces the `integrated` count previously
derived from `integrated_date` in metadata.

---

## Changes Required to the Design Doc (§6)

When implementing `scripts/checks/integrate.py`, replace §6 of
`docs/design/pipeline-health-suite.md` entirely with the check table above. Specific changes:

1. Replace the existing 7-check table with the Phase 1 and Phase 2 tables.
2. Drop the `claim_sources_present` warning — this is now `claim_source_nonnull` at error
   severity (the spec treats it as an invariant, not a best-effort check).
3. Drop `paper_ids_ingested` as the integration-tracking proxy — it's now a secondary
   warning, not the primary integration signal.
4. Add the `--concept` flag to the invocation examples (replacing `--id`).
5. Update the `stats` dict in §8 (Corpus Module) to remove `"integrated": 276` and add
   `papers_not_in_any_yaml` derived from the integrate module output.
6. Create `config/health_check.yaml` with the canonical concept slug list (source for
   `concept_in_registry`) and `cluster_staleness_days: 180` (source for `cluster_last_reviewed`).
   Add `registry_config_matches_docs` to the Phase 1 check table.

---

## Open Questions for Implementation — resolved 2026-07-15

1. **Registry parsing.** Decided: add `config/health_check.yaml` with a flat canonical slug
   list as the source of truth for `concept_in_registry` (structured, robust to parse — a
   script, not an LLM, is consuming this). To prevent the config and `docs/content.md`'s
   "Concept Page Registry" prose section from silently drifting apart, add a second check,
   `registry_config_matches_docs` (**warning** severity), that regex-extracts the backtick-span
   slugs from `docs/content.md` and diffs them against the config list. Drift becomes a visible
   dashboard warning instead of a silent parser miss.

2. **Phase detection.** Decided: accept the heuristic as specified — non-empty `claim_clusters`
   → post-Phase-2 (full check set); empty/absent → Phase-1-only. `--phase` overrides. Traced
   through the main edge cases (new Phase 1 entries appended after a prior Phase 2 run; a
   supporting paper removed after clustering) and the heuristic behaves correctly in both —
   no changes needed.

3. **`papers_not_in_any_yaml` scope.** Decided: no caching for now. Checked current scale —
   1,326 files in `raw/metadata/`, `_claims/` just getting started (1 YAML) — a full scan is
   sub-second to low-single-digit seconds even scaled to ~23 concept YAMLs. Revisit caching
   only if `--report` becomes noticeably slow in practice; premature at this corpus size.
   Note: this stat is a partial, free detector for the `related_concepts` completeness bug
   tracked in `BACKLOG.md` (Pipeline Health Suite) — it catches papers with a fully empty
   `related_concepts` list, but not papers missing just one of several correct concept tags
   (those still show up in the YAMLs they *were* tagged into). The two checks are
   complementary, not redundant; the dedicated ingest-module check is still needed.

4. **Staleness threshold.** Decided: keep 180 days as the default, made tunable via
   `config/health_check.yaml` (`cluster_staleness_days: 180`) — same config file as (1). Low
   stakes since this check is warning-severity only.
