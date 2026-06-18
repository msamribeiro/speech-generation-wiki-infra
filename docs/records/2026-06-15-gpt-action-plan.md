# GPT Action Plan — 2026-06-15

Concrete implementation plan for stabilizing the wiki workflow, upgrading the evidence model, and adding dashboard/brief support.

## Phase 1: Stabilize Current Workflow

### 1. Fix ingest agent contradictions

File: `.claude/agents/speech-generation-ingest-agent.md`

- Clarify exact files the agent may write.
- Decide whether `generation_history` is allowed in metadata.
- Promote duplicate-page check into Step 1.
- Fix invariant saying metadata edits are only `status`/`ingested_date` if `generation_history` remains.

### 2. Fix paper index row generation

- Change ingest agent's `papers/index.md` row format from plain IDs to wikilinks.
- Standardize existing inconsistent rows in `wiki/papers/index.md`.
- Decide one canonical format:
  - `| [[id]] | Title | ... |`
  - or `| [[id]] | [Title](papers/id.md) | ... |`

### 3. Add post-ingest validation

Create:

```text
scripts/wiki/validate_paper_page.py
```

Checks:

- YAML frontmatter parses.
- Required fields exist.
- Required sections exist.
- Claims have inline source citations.
- Controlled vocabulary fields are valid.
- Figure links point to existing assets.
- `related_concepts` slugs exist.

### 4. Move figure selection after significance assignment

In ingest agent:

- Draft frontmatter/significance first.
- Then select figures if `field_significance.type` includes `architectural-novelty`.
- Then write final paper page.

## Phase 2: Repair Existing Data Drift

### 5. Build one-off wiki integrity audit

Create:

```text
scripts/wiki/audit_integrity.py
```

Checks:

- Metadata `status: ingested` but missing paper page.
- Paper page but missing metadata.
- Ingested but not integrated.
- Count mismatches across `STATUS.md`, `wiki/index.md`, `wiki/overview.md`, `wiki/papers/index.md`.
- Plain IDs in paper index.
- Broken wikilinks.
- Missing claim citations.

### 6. Repair malformed concept evidence digests

Start with:

```text
wiki/concepts/_evidence/flow-matching.yaml
```

Actions:

- Parse with YAML parser.
- Move misplaced paper entries from `trend_notes` into `papers`.
- Normalize top-level structure.
- Recompute `paper_count`.

### 7. Backfill claim citations where missing

Prioritize:

- foundational papers
- high-significance papers
- papers heavily used by concept pages
- recent papers feeding active claims

Track pages as:

```yaml
claim_citation_status: complete | partial | missing
```

## Phase 3: Upgrade Evidence Schema

### 8. Define concept evidence YAML schema

Add:

```text
docs/CONCEPT_EVIDENCE_SCHEMA.md
```

Include:

- `papers`
- `claim_clusters`
- `method_families`
- `reassessment_queue`
- `role_history`
- allowed values for `role`, `status`, `evidence_role`, `confidence`

### 9. Add schema validation

Create:

```text
scripts/wiki/validate_concept_evidence.py
```

Checks:

- YAML parses.
- Required top-level keys exist.
- Paper IDs exist.
- Claim IDs are unique.
- Claim clusters reference valid paper IDs.
- `paper_count` matches evidence policy.
- Reassessment entries have `trigger`, `due`, and `current_assessment`.

### 10. Update integration agent spec

File: `.claude/agents/speech-generation-integration-agent.md`

Changes:

- Require YAML validation after digest edits.
- Store structured claim evidence with:
  - `claim`
  - `role`
  - `source`
  - `confidence`
  - `concepts`
- Maintain claim clusters explicitly.
- Add reassessment queue updates.
- Stop treating concept `## All Papers` as the exhaustive sink.

## Phase 4: Split Concept Page and Appendix

### 11. Define lightweight concept page template

Add to `CLAUDE.md` or a new doc:

```text
docs/CONCEPT_PAGE_TEMPLATE.md
```

Sections:

- Executive Summary
- Current Assessment
- Major Claims
- Method Families
- Current Tensions
- Open Questions
- Recommended Reader Path

### 12. Define generated appendix template

New target path:

```text
wiki/concepts/evidence/{slug}.md
```

Sections:

- Claim clusters
- Method-family evidence tables
- Paper evidence inventory
- Evidence strength notes
- Reassessment queue
- Data hygiene notes

### 13. Create appendix generator

Create:

```text
scripts/wiki/generate_concept_appendix.py
```

Inputs:

- `wiki/concepts/_evidence/{slug}.yaml`
- paper page frontmatter as fallback metadata

Output:

- `wiki/concepts/evidence/{slug}.md`

### 14. Pilot on `flow-matching`

Use the experimental files as design references:

```text
flow-matching-gpt-experimental-06-15.md
flow-matching-gpt-experimental-appendix-06-15.md
```

Then implement production versions in the wiki content repo.

## Phase 5: Add Reassessment Workflow

### 15. Add reassessment queue to evidence YAML

Start with high-change concepts:

- `flow-matching`
- `autoregressive-codec-tts`
- `neural-codec`
- `evaluation-metrics`

### 16. Add reassessment logic to integration pass

Integration agent should:

- check whether triggers fired
- mark overdue reassessment items
- update `current_role` or claim `status` when warranted
- log reassessment changes separately from normal integration

### 17. Add periodic review command

Example invocation:

```text
"Review reassessment queue for flow-matching"
```

Output:

- role changes
- claim status changes
- stale items
- proposed concept page updates

## Phase 6: Build Dashboard

### 18. Create dashboard generator

Create:

```text
scripts/wiki/dashboard.py
```

Output:

```text
STATUS_DASHBOARD.md
```

### 19. Implement initial dashboard checks

Start with:

- metadata/wiki consistency
- YAML parse validation
- required paper sections
- missing claim citations
- concept digest count mismatch
- count mismatch across status/index/overview
- broken wikilinks

### 20. Add claim graph dashboard section

Once schema is upgraded, track:

- total claim clusters
- status distribution
- claims missing citations
- contested claims
- overdue reassessments
- claims changed this month

### 21. Add dashboard to routine workflow

Run after:

- ingest batch
- integration pass
- monthly report generation

Optionally log dashboard deltas in `STATUS.md`.

## Phase 7: Add Briefs

### 22. Define brief template

Add:

```text
docs/BRIEF_TEMPLATE.md
```

Sections:

- Question
- Short Answer
- Evidence Table
- Caveats
- Recommendation
- Papers to Read First
- Last Reviewed

### 23. Add brief candidate detection

Integration agent logs candidates when:

- claim changes status
- contested claim appears
- new high/foundational paper lands
- reassessment changes paper role

### 24. Create first briefs manually

Good pilots:

- `flow-matching-vs-ar-codec-tts`
- `tts-evaluation-metrics-that-matter`
- `codec-frame-rate-tradeoffs`
- `best-open-weight-zero-shot-tts`

## Suggested Execution Order

Do these first:

1. Fix ingest agent contradictions and paper index wikilinks.
2. Add validation scripts.
3. Repair `flow-matching.yaml`.
4. Define concept evidence schema.
5. Update integration agent around structured claims.
6. Generate concept appendix from YAML.
7. Build dashboard.

Briefs should come after the claim/evidence layer is stable.
