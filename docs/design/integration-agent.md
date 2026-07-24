# Integration Agent — Design Document

**Status:** Implemented (prototype tested 2026-06-24)  
**Agent spec:** `.agents/skills/speech-generation-integration-agent/SKILL.md`
**Schema:** `docs/schemas/claims.md`  
**Health check:** `docs/records/2026-06-24-integrate-health-check-design.md`

---

## Purpose

The integration agent sits between the ingest stage (paper pages) and the render stage
(concept renderings). Its job is to build and maintain the claim graph in `wiki/_claims/` — the
structured YAML layer from which all rendered wiki output is derived.

```
wiki/papers/{id}.md          (ingest output — ground truth for what a paper says)
        ↓
wiki/_claims/{slug}.yaml     (integration output — living review's interpretation)
        ↓
wiki/concepts/{slug}.md      (render output — human-readable synthesis)
```

The YAML is the single source of truth. Concept Overviews and In Depth pages are derived
artifacts and can always be regenerated from the YAML without loss.

---

## Two-Phase Model

Integration is split into two independent phases with different cost profiles and
different reasoning requirements.

### Phase 1 — Paper Entry Extraction

**Unit of work:** one paper for one concept.  
**Input:** a wiki paper page (`wiki/papers/{id}.md`).  
**Output:** one new entry in `papers:` in `wiki/_claims/{slug}.yaml`.  
**Reasoning:** single-paper, no cross-paper knowledge required.

Phase 1 reads a paper page and writes a structured entry capturing:

- Bibliographic fields (`year`, `venue`, `task`, `architecture`)
- `entry_date` — when the entry was written (used for staleness detection)
- `relevance` — how central this concept is to the paper overall
- `evidence_role` — what kind of evidence the paper contributes to the concept
- `current_role` — the living review's current judgment of the paper's importance *for this concept*
- `method_family: []` — always empty after Phase 1; Phase 2 assigns family membership
- `claims` — all claims from the paper's `## Claims` section, each with a per-claim `relevance`
  score indicating how directly the claim bears on this concept

**Idempotency:** Phase 1 checks whether a paper ID is already present in `papers:` before
writing. If it is, the entry is skipped (unless `--force` is set). This means Phase 1 can be
invoked repeatedly on the same concept without re-processing existing entries.

**Context budget:** at most 20 new paper pages are read per invocation. For large concepts,
multiple Phase 1 invocations are used before Phase 2 runs. A parent orchestrator manages the
queue.

### Phase 2 — Synthesis

**Unit of work:** one concept YAML.  
**Input:** the full `papers:` list in the concept YAML.  
**Output:** `claim_clusters`, `method_families`, `open_questions`, `trend_notes` written to
the same YAML.  
**Reasoning:** cross-paper, reads YAML entries only — no wiki page reads.

Phase 2 derives three synthesis sections from the complete `papers:` list:

**`method_families`** — papers grouped by architectural pattern. Phase 2 also back-fills
`method_family` on each paper entry to reference the assigned family id. Method families
are regenerated from scratch on every Phase 2 run.

**`claim_clusters`** — canonical field-level propositions with status and evidence linkage.
Updated incrementally: new papers are merged into existing clusters; clusters are promoted
or marked contested based on evidence accumulation rules:

- `emerging` — 1–2 supporting papers, or with methodological caveats
- `strongly_supported` — ≥3 independent papers with `high` or `medium` claim relevance
- `contested` — at least one paper contradicts a `strongly_supported` or `emerging` cluster
- `weakened` — multiple papers reduce confidence in a previously supported cluster

Only claims with `relevance: high` or `medium` contribute to cluster promotion. `low`
relevance claims are included in the entry for completeness but do not drive status changes.

**`open_questions` and `trend_notes`** — human-curated longitudinal annotations. These are
never cleared by synthesis runs, including `--regenerate-clusters`.

---

## Per-Concept Invocation

The primary invocation unit is the concept, not the paper batch. This is the key design
choice that makes processing tractable and coherent.

**Why per-concept:**

- The claim graph for `flow-matching` is self-contained: no entry depends on the state of
  `zero-shot-tts.yaml`. Concepts can be processed independently and in any order.
- Phase 1 can be scoped precisely: grep paper pages for `related_concepts` containing the
  target slug, diff against existing YAML entries, write only the gap.
- Phase 2 synthesises over a coherent, complete set: all papers relevant to this concept,
  not a random 25-paper batch that may touch a dozen concepts partially.

**Convenience mode:** `"last N papers"` resolves to a concept list (collect `related_concepts`
from the N most recently ingested papers, deduplicate) and then runs the per-concept path for
each affected concept. The per-concept logic is always the underlying mechanism.

---

## Invocation Modes

### Phase flags

| Flag | Behaviour |
|------|-----------|
| `--phase 1` | Paper entry extraction only. No synthesis runs. |
| `--phase 2` | Synthesis only. No paper pages are read. Works from existing `papers:` list. |
| *(none)* | Both phases sequentially. Suitable for small concepts or incremental updates. |

### Content flags

| Flag | Behaviour |
|------|-----------|
| `--force [id ...]` | Rewrite paper entries even if already present. All candidates if no IDs given; specific IDs otherwise. Useful after a review pass that updated a paper page. |
| `--regenerate-clusters` | Rebuild `claim_clusters` and `method_families` from scratch from the full `papers:` list. Preserves `open_questions`, `trend_notes`, `reassessment_queue`. Designed for quarterly passes as the corpus grows. |

### Typical workflows

**Adding newly ingested papers to a concept (most common):**
```
"Run integration pass on concept: flow-matching --phase 1"
# repeat until all papers processed (up to 20 per invocation)
"Run integration pass on concept: flow-matching --phase 2"
```

**After a review pass that corrected specific paper pages:**
```
"Run integration pass on concept: flow-matching --phase 1 --force 2025.acl-long.313 2406.18009"
"Run integration pass on concept: flow-matching --phase 2"
```

**Quarterly synthesis refresh (all concepts):**
```
"Run integration pass on concepts: flow-matching diffusion-tts zero-shot-tts [...] --regenerate-clusters"
```

**Broad sweep after a large ingest batch:**
```
"Run integration pass on last 40 papers"
# → resolves to affected concepts, runs Phase 1 per concept, then Phase 2 per concept
```

---

## Claim-Level Relevance

Every claim entry in the YAML carries two relevance signals:

- **Paper-level `relevance`** (`high | medium | low`) — how central this concept is to the
  paper as a whole. Set once per paper entry.

- **Per-claim `relevance`** (`high | medium | low`) — how directly this specific claim bears
  on the enclosing concept. Set per claim during Phase 1 extraction.

The motivation: a paper tagged with `related_concepts: [flow-matching, evaluation-metrics]`
will have claims relevant to both concepts. When the integration agent processes
`flow-matching.yaml`, it includes *all* of the paper's claims (none are dropped), but sets
`low` relevance on claims primarily about evaluation metrics. Phase 2 uses the per-claim
relevance to filter which claims drive cluster promotion — `low` relevance claims are present
for cross-concept traceability but do not count toward `strongly_supported` thresholds.

This design means the per-claim relevance field is the primary mechanism for concept-scoped
synthesis from a shared paper entry. It can be manually edited or revised without re-running
Phase 1.

---

## `current_role` Is Concept-Scoped

`current_role` in a paper entry records the living review's judgment of the paper's
importance *for this specific concept*. The same paper may carry different roles in different
concept YAMLs:

- A paper that established the flow-matching objective is `foundational` in `flow-matching.yaml`
  but `minor` in `evaluation-metrics.yaml` if its evaluation contribution is peripheral.
- A paper primarily about voice conversion may be `active_evidence` in `voice-conversion.yaml`
  but `historical_context` in `flow-matching.yaml` if it uses an older FM variant.

Do not derive `current_role` mechanically from the paper's global `field_significance.level`.
Use `field_significance.level` as a prior, but override it based on the paper's actual
contribution to this concept.

---

## `entry_date` and Staleness Detection

Every paper entry carries `entry_date: YYYY-MM-DD` recording when the entry was written or
last force-rewritten. This enables staleness detection:

- A paper page carries `generation.date` (when the page was last written by the ingest or
  review agent).
- If `generation.date` on a paper page is newer than `entry_date` in a concept YAML, the
  entry may be stale — the paper was reviewed after the last integration run.

The integration agent (or health check) can compare these dates to surface a list of entries
that should be re-extracted with `--force`.

`entry_date` replaces the old `integrated_date` field in `raw/metadata/`. The old field was
a single timestamp per paper with no concept granularity; `entry_date` is per-entry and
per-concept, giving precise provenance.

---

## Tier 2 Papers

Papers with `ingest_tier: 2` in `raw/metadata/` are citation-discovery stubs with minimal
wiki pages. They are excluded from the claim graph entirely:

- The integration agent skips them during discovery (Step 1).
- The health check flags any Tier 2 paper ID found in a concept YAML as an error.

Tier 2 papers are tracked separately via `wiki/papers/index.md` and are not expected to
contribute evidence to concept-level claims.

---

## What Is Preserved vs. Derived

| Section | Source | Cleared by synthesis? |
|---------|--------|-----------------------|
| `papers[].id`, `entry_date`, `year`, `venue`, `task`, `architecture` | Phase 1 extraction | No — Phase 2 reads only |
| `papers[].relevance`, `evidence_role`, `current_role`, `claims` | Phase 1 judgment | No — unless `--force` |
| `papers[].method_family` | Phase 2 assignment | Yes — regenerated each Phase 2 |
| `method_families` | Phase 2 synthesis | Yes — regenerated each Phase 2 |
| `claim_clusters` | Phase 2 synthesis | Incremental by default; yes with `--regenerate-clusters` |
| `open_questions` | Human/agent annotation | Never cleared |
| `trend_notes` | Human/agent annotation | Never cleared |
| `reassessment_queue` | Human/agent annotation | Never cleared |

---

## Validation

Validation is split between an inline gate (in the agent spec) and a deep module (health check).

**Inline (agent spec, after every YAML write):**
- YAML parses without error
- Required top-level keys present
- `paper_count` == `len(papers)`
- No duplicate paper IDs (Phase 1) or cluster IDs (Phase 2)

**Deep (health check `--integrate`, on demand):**
- Per-record required fields
- Controlled vocabulary enforcement
- Cross-reference consistency (method_family IDs, cluster paper refs)
- Tier 2 exclusion
- `entry_date` and `source` non-null checks

See `docs/records/2026-06-24-integrate-health-check-design.md` for the full check set.
