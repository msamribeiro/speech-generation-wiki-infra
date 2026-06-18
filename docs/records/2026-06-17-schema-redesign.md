# Evidence Schema Redesign — Session Notes (2026-06-17)

## Context

These notes record the discussion and decisions from a session reviewing the four GPT-generated files (`GPT-suggestions-06-15.md`, `flow-matching-gpt-experimental-06-15.md`, `flow-matching-gpt-experimental-appendix-06-15.md`, `gpt-action-plan-06-15.md`) and evaluating whether and how to adopt their proposals.

---

## Key Architectural Decision

The evidence YAML (`wiki/concepts/_evidence/{slug}.yaml`) should be treated as the **single machine-readable layer between individual paper pages and all synthesized wiki output**. Everything above the paper layer — concept pages, evidence dossiers, briefs, trend reports, dashboards — is generated from this file.

This framing changes the schema complexity question: fields that looked like overengineering in isolation are justified because the YAML must be self-contained for synthesis without having to reload all paper pages each time.

The layered architecture is:

```
Paper pages (wiki/papers/{id}.md)
  ↓ integration agent reads and extracts
Evidence YAML (wiki/concepts/_evidence/{slug}.yaml)   ← single source of truth
  ↓ generated from
Concept pages, evidence dossiers, briefs, reports, dashboard
```

Paper pages are the ground truth for what a paper says. The YAML is the living review's current interpretation of what papers mean for each concept.

---

## Proposed Schema

After simplifying the full GPT proposal (dropping fields redundant with paper frontmatter), the target schema is:

```yaml
concept: {slug}
last_updated: YYYY-MM-DD
paper_count: N

papers:
  - id: {paper_id}
    year: YYYY
    venue: ACL          # cached from paper frontmatter for synthesis efficiency
    task: [TTS]
    architecture: [flow-matching]
    relevance: high | medium | low
    evidence_role:      # how this paper contributes to the concept
      - core_evidence
    current_role: influential | foundational | active_evidence | minor | frontier_probe | historical_context
    method_family: [pure_nar_fm_tts]   # links to method_families section
    claims:
      - claim_id: {slug_for_this_claim}
        role: supports | contradicts | complicates | refines
        claim: "..."
        source: "§3.4, Table 2"
        evidence: "One-sentence supporting fact."
        confidence: high | medium | low
    limitations:
      - "..."
    caveats:           # concept-specific limits (distinct from paper's general limitations)
      - "..."

claim_clusters:
  - id: {slug}
    claim: "Canonical field-level claim."
    status: strongly_supported | emerging | contested | weakened | superseded | historical
    confidence: high | medium | low
    supporting_papers: [{paper_id}, ...]
    contradicting_papers: []
    refining_papers: []
    caveats: [...]
    last_reviewed: YYYY-MM-DD

method_families:
  - id: {slug}
    name: "Human-readable name"
    summary: "1–2 sentence description."
    papers: [{paper_id}, ...]
    open_questions:
      - "..."

reassessment_queue:
  - id: {paper_id or claim_id}
    type: paper_role | claim_status | method_family | benchmark_validity
    reason: "Why reassessment is needed."
    trigger: "What evidence would cause reassessment."
    due: YYYY-MM          # calendar fallback if trigger never fires
    current_assessment: {current_role or claim_status value}
    watch_for:
      - "Concrete sign to look for in incoming papers."

open_questions:
  - "..."

trend_notes:
  - "..."
```

### Fields dropped from the GPT proposal

| Field | Reason dropped |
|-------|---------------|
| `metrics` per paper | Paper frontmatter is the source of truth; redundant |
| `contribution_type` per paper | Already in paper frontmatter (`field_significance.type`) |
| `related_concepts` per paper | In paper frontmatter; per-concept YAML doesn't need per-paper cross-concept links |
| `role_history` per paper | Overkill; update `current_role` when reassessment fires |
| `publication_role` | Inferrable from ingest date + initial `current_role` |
| `possible_outcomes` in reassessment queue | Redundant with `watch_for` |

---

## Evidence Role Vocabulary

Controlled values for `evidence_role`:

```yaml
evidence_role:
  - core_evidence          # directly advances the concept
  - architecture_variant   # new system placement or design variant
  - acceleration_evidence  # speed, NFE, latency, RTF
  - control_evidence       # speaker/prosody/emotion/language/dialogue control
  - evaluation_caution     # metric or benchmark caution relevant to concept
  - historical_context     # predecessor or lineage evidence; does not validate current paradigm
  - negative_evidence      # contradicts or weakens a claim
  - infrastructure         # dataset, codec, benchmark, toolkit
```

---

## The Reassessment Queue

The queue is the mechanism that makes the review genuinely living. Without it, paper importance freezes at ingest time. With it, the integration agent can check each incoming batch against open triggers and surface whether any paper's `current_role` or a claim's `status` should change.

The pattern is:
- `current_assessment` = what the review believes now
- `trigger` = what evidence would change that belief
- `due` = calendar fallback if no trigger fires
- `watch_for` = concrete signals to look for in new papers

The integration agent, during each pass, checks whether any trigger conditions are met by papers in the current batch. If a trigger fires, it updates `current_role` (paper entry) or `status` (claim cluster) and removes the queue item. If `due` has passed without a trigger, it surfaces the item for human review.

---

## Concept Page Redesign

The experimental page (`flow-matching-gpt-experimental-06-15.md`) demonstrates the target format. The key differences from the current CLAUDE.md template:

| Current template | New template |
|-----------------|-------------|
| `Current Status` + `Why This Matters` + `Core Idea` | Single **Current Assessment** (1–2 paragraphs) |
| `Methods and Variants` | **Method Families** (prose per family, linking to YAML `method_families`) |
| Scattered contested claims | Explicit **Current Tensions** section |
| `Representative Papers` with subsections | **Recommended Reader Path** (ordered, with rationale) |
| `## All Papers` exhaustive table | Removed from concept page; generated separately in evidence dossier |
| No temporal interpretation | **How to Interpret Older and Newer Evidence** section |

The `## All Papers` table is the most important removal. It's what makes concept pages grow to monograph length and what makes them serve two conflicting audiences (humans wanting synthesis vs. agents needing exhaustive inventory). The exhaustive inventory belongs in a generated evidence dossier, not the concept page.

The new concept page is purely editorial: what does the field currently believe, why, where is the evidence strong or weak, what is contested, and what should a reader actually read?

---

## Migration Plan

### What needs updating
1. CLAUDE.md — concept page template, YAML schema definition
2. Integration agent spec — generate new concept page format, write upgraded YAML
3. 24 existing evidence digests — structural migration
4. 24 existing concept pages — regeneration with new template

### Migration approach for existing digests

The hard part is that existing claims are flat strings without `role` or `source`. Full migration requires re-reading source papers to add provenance. A pragmatic two-step:

**Step 1 (structural):** Migrate the scaffold without claim provenance:
- Add `evidence_role`, `current_role`, `method_family` to paper entries
- Convert flat claim strings to `{claim_id, claim, role: null, source: null, confidence: null}` objects
- Add `method_families` section (new; seed from existing Methods and Variants prose)
- Upgrade `claim_clusters` with `id`, `confidence`, `refining_papers`, `caveats`, `last_reviewed`
- Add `reassessment_queue` (start empty or with obvious candidates)

**Step 2 (provenance backfill):** During future integration passes that load paper pages anyway, fill in `source`, `role`, and `confidence` for existing claims. New claims added after the migration always get full provenance.

### Sequencing relative to ingest

Ingest is the volume priority (731 papers to go). The redesign should happen in one dedicated session:

1. Finalize schema (this document + any adjustments)
2. Update CLAUDE.md concept page template and YAML schema section
3. Update integration agent spec
4. Run one integration pass targeting all 24 concept pages (format refresh, not new evidence synthesis)
5. Resume standard ingest — future integration passes use the new format

The concept page regeneration pass is feasible in a single session because it's a format refresh: the integration agent has already read the source papers; it's translating existing evidence into a new schema, not re-deriving synthesis from scratch.

---

## Three-Stage Pipeline Architecture

The pipeline separates into three distinct, independently triggerable stages. Each has a single responsibility and a clear input/output contract.

### Stage 1: Ingest

Paper-scoped, self-contained. No cross-paper knowledge required or produced.

- **Input:** one parsed paper (`raw/parsed/{id}/paper.md` + frontmatter + references)
- **Output:** one paper page (`wiki/papers/{id}.md`) + index/venue/log entries + metadata status update
- **Agent:** `speech-generation-ingest-agent` (unchanged)
- **Cadence:** any time; papers can be ingested independently

### Stage 2: Integrate

Evidence-scoped. Reads paper pages (or frontmatter), writes evidence YAMLs only. No wiki pages are touched.

- **Input:** new paper pages or frontmatter; existing evidence YAMLs
- **Output:** updated `wiki/concepts/_evidence/{slug}.yaml` — per-paper entries, claim clusters, method families, reassessment queue; existing papers' `current_role` and claim statuses revised when triggers fire
- **Agent:** `speech-generation-integration-agent` (revised — remove all page-writing steps)
- **Cadence:** every ~25 ingested papers, or on demand

This is the knowledge accumulation stage. The YAML is the only output.

### Stage 3: Synthesize (Render)

Page production. Derives all human-readable output from the evidence YAML. Stateless with respect to history — always regenerates from current YAML state.

- **Input:** evidence YAML as primary; paper pages or frontmatter as optional supplemental reads
- **Output:** any subset of concept pages, evidence dossiers, briefs, trend reports, overview
- **Agent:** `speech-generation-synthesis-agent` (new)
- **Cadence:** monthly light update; semester or yearly full rewrite; on-demand for individual targets (e.g., "update only flow-matching")
- **Modes:**
  - *Light:* update only sections affected by papers added since last synthesis; faster and cheaper
  - *Full:* regenerate page from scratch from YAML; produces a more coherent result; safe because YAML is self-contained

The synthesis stage is independently triggerable on any target (`--concept flow-matching`, `--all-concepts`, `--briefs`, `--overview`). Because the input is structured YAML rather than raw papers, it does not need to know about individual papers unless it chooses to read them for prose quality.

### Separation of concerns

The critical property of this design: **concept pages are derived artifacts, not source of truth**. The YAML is the source of truth. Concept pages can always be fully regenerated without loss of information. Direct edits to concept pages are never made — all updates flow through the YAML.

Under the current design, the integration agent writes both YAMLs and concept pages in one pass, creating drift risk. Under this design, the two stages are cleanly separated and the only path to updating a concept page is via a synthesis pass.

### Cadence model

| Frequency | What runs |
|-----------|-----------|
| Monthly | Ingest batch → integrate → light synthesis pass on affected concepts |
| Semester / yearly | Full synthesis pass: regenerate all concept pages, dossiers, overview from scratch |
| On demand | Any single stage on any target |

---

## Model Flexibility in the Synthesis Stage

The structured YAML input makes the synthesis stage model-agnostic. Because the hard work — reading raw PDFs, understanding paper contributions, extracting claims and evidence — is done during ingest and integration, the synthesis stage receives clean structured data. Any model capable of generating coherent prose from structured input can run it.

This matters for the quality/cost trade-off:

| Mode | Model | Use case |
|------|-------|----------|
| Light update | Haiku or Sonnet | Monthly incremental updates; fast and cheap |
| Full concept rewrite | Opus | Semester/yearly; maximize prose quality and coherence |
| Experimental | GPT-5 or any frontier model | A/B comparison; the structured input is model-agnostic |

The structured evidence layer is what makes this possible. A synthesis agent reading YAML claim clusters and method families is doing an editorially simpler job than an integration agent reading raw paper text. The complexity has been absorbed upstream.

### Provenance tracking

Every generated artifact must record which model produced it and when. This is already in the backlog (`future_generation_tracking_gaps.md`: concept pages, venue pages, and `overview.md` need `generation` frontmatter before Opus passes begin). Under the three-stage design this becomes systematic: every output of the synthesis stage gets a `generation` frontmatter block.

```yaml
generation:
  date: YYYY-MM-DD
  stage: synthesis
  mode: full | light
  agent: speech-generation-synthesis-agent
  model: claude-opus-4-8 | claude-sonnet-4-6 | claude-haiku-4-5 | ...
  source_digest_date: YYYY-MM-DD   # last_updated of the evidence YAML used
  commit: abc1234
```

`source_digest_date` is the key field: it tells you whether the concept page is current with the evidence YAML, or whether a new synthesis pass is needed because integration has added papers since the last generation.

This supports the dashboard check: "concept pages whose `source_digest_date` is behind the YAML `last_updated` are stale and should be queued for the next synthesis pass."

---

## What Was Deprioritized (for later)

- Evidence dossier generation (`wiki/concepts/evidence/{slug}.md` or `wiki/dossiers/`) — generated from YAML; implement after schema is stable
- Briefs (`wiki/briefs/`) — decision-oriented memos; implement after claim layer is solid
- Dashboard script (`scripts/wiki/dashboard.py`) — operational health checks; implement after schema is stable
- Wiki integrity audit script (`scripts/wiki/audit_integrity.py`) — useful but not blocking
- Claim provenance backfill for pre-migration pages — fill in during future integration passes
