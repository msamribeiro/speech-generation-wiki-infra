# Q4 2025 Integration and Synthesis Session

**Started:** 2026-09-19
**Status:** Active; six concepts complete through Phase 2
**Evidence scope:** Q4 2025 (`2025-10-01 <= published_date <= 2025-12-31`) layered onto the
completed Q3-and-earlier claim graphs
**Goal:** Complete the seven-stage Q4 cycle: Phase 1 integration, Phase 2 synthesis, validation,
cross-concept reconciliation, concept rendering, field-overview rendering, and—if approved—the
retrospective snapshot and quarterly report.

This is the authoritative multi-session handoff note for the Q4 2025 content cycle. It follows the
concept-by-concept batching discipline established in `Q3_INTEGRATION_SESSIONS.md` and the gated
reconciliation, snapshot, render, and report sequence recorded in
`docs/records/2026-09-13-cross-concept-synthesis-and-temporal-reporting.md`.

---

## Resume Here

1. Inspect both worktrees and confirm unrelated changes are preserved.
2. Export the writable content checkout because the resolver's default sibling is not writable in
   the managed workspace:

   ```bash
   export SPEECH_WIKI_CONTENT_DIR=/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content-integrate
   ```

3. Begin `autoregressive-codec-tts` Phase 1 after recomputing its live Q4 queue; the current
   dashboard estimate is 31 pending entries.
4. Run and independently verify the concept-scoped integration health check after every batch.
5. Append a dated Session Log entry before ending the session, including the exact next paper or
   next phase.

Starting commits recorded at bootstrap:

- Infrastructure: `df5176b` on `main`.
- Content: `872959f` on `work/integrate`.

Both worktrees were clean when the Q4 plan was created.

---

## Scope and boundaries

Q4 eligibility is determined only by canonical `published_date`, inclusive from 2025-10-01 through
2025-12-31. Do not infer the quarter from an arXiv ID, ingest date, filesystem timestamp, or the
historical Q4 ingestion-session denominator.

Include an ingested paper in a concept's Phase 1 queue when:

- its canonical publication date is inside Q4 2025;
- it has a production paper page;
- it is not Tier 2; and
- the target concept occurs in `related_concepts` and belongs to the canonical registry.

Do not:

- fold Q1 2026 or later papers into this cycle;
- rewrite paper pages, parsed sources, PDFs, or substantive metadata;
- let similarity tooling accept reconciliation relationships automatically;
- render from reconciliation candidates or agent-only proposals;
- freeze a snapshot before a finalized human-review reconciliation run exists; or
- draft a quarterly report from the living graph instead of a published snapshot.

Two Q4 Tier 1 pages currently have no concept assignment. Audit them as a data-quality issue, but
do not invent concept memberships merely to drive the unique-paper coverage statistic to zero.
They are `2512.16832` (prosody/text information analysis) and `2511.21229` (Isan conversational
speech corpus). The two Q4 papers already present in claim YAMLs are `2508.16790` (TaDiCodec) and
`2503.14345` (MoonCast); verify their canonical publication dates and existing entries during the
first relevant concept passes.

---

## Reviewed baseline

Baseline measured on 2026-09-19 against the writable content checkout.

| Measure | Value |
|---|---:|
| Q4 ingested, non-Tier-2 paper pages | 174 |
| Q4 pages with at least one canonical concept | 172 |
| Q4 pages with no concept assignment | 2 |
| Q4 Tier 2 pages skipped | 2 |
| Q4 pages already present in at least one listed concept YAML | 2 |
| Affected concepts | 22/23 |
| Approximate missing concept-paper entries | 660 |
| Existing concept YAMLs | 23 |
| Starting concept paper entries | 2,226 |
| Starting claim clusters | 406 |
| Starting rendered Overview/In Depth pairs | 21/23 |
| Starting reconciliation authority | Q3: 64 relationships and 11 broader claims |
| Published snapshots | 1 (`2025-Q3`) |

Health baseline:

```text
integrate: PASS — 0 errors, 241 warnings; 23 concepts, 2,226 entries, 406 clusters,
           papers_not_in_any_yaml=345
render:    PASS — 0 errors, 7 warnings; 21 Overview and 21 In Depth pages
reconcile: PASS — 0 errors, 1 warning; 64 relationships, 11 broader claims,
           2 runs, 1 snapshot
```

The corpus-wide `papers_not_in_any_yaml` value includes Q4 and later papers, so it is a useful
directional signal but not the Q4 closure criterion. Q4 closure requires an exact bounded
candidate-versus-YAML audit.

### Q4 concept queues

`Already` means the Q4 paper ID currently occurs in that concept YAML. Recheck those entries for
date and scope consistency rather than assuming that their early presence is automatically valid.

| Concept | Q4 candidates | Already | Queue |
|---|---:|---:|---:|
| subjective-evaluation | 73 | 0 | 73 |
| evaluation-metrics | 61 | 0 | 61 |
| zero-shot-tts | 61 | 2 | 59 |
| neural-codec | 58 | 2 | 56 |
| spoken-language-model | 49 | 2 | 47 |
| speech-to-speech | 35 | 0 | 35 |
| autoregressive-codec-tts | 33 | 2 | 31 |
| multilingual-tts | 31 | 1 | 30 |
| self-supervised-speech | 31 | 1 | 30 |
| voice-conversion | 29 | 0 | 29 |
| flow-matching | 30 | 2 | 28 |
| emotion-synthesis | 24 | 0 | 24 |
| gan-vocoder | 21 | 0 | 21 |
| prosody-control | 21 | 0 | 21 |
| streaming-tts | 21 | 0 | 21 |
| rlhf-speech | 20 | 0 | 20 |
| speaker-adaptation | 19 | 0 | 19 |
| disentanglement | 16 | 0 | 16 |
| instruction-conditioned-tts | 13 | 0 | 13 |
| diffusion-tts | 11 | 0 | 11 |
| singing | 10 | 0 | 10 |
| transformer-enc-dec-tts | 5 | 0 | 5 |
| **Total** | **671** | **11** | **660** |

`fine-tuning` has no current Q4 candidate. Its missing production render remains in scope for the
render stage only if its evidence supports a useful page.

---

## Seven-stage program

### Stage 1 — Q4 Phase 1 integration

- [ ] Recompute each concept's eligible Q4 queue from canonical metadata and YAML-parsed paper
      frontmatter.
- [ ] Process candidates oldest-first, sequentially, in batches of at most 20 papers per concept.
- [ ] Preserve every paper-page claim, role, source, limitation, and concept-local caveat.
- [ ] Skip Tier 2 pages and record justified concept-specific exclusions explicitly.
- [ ] Validate after every write and append a batch summary to this note and `log.md`.

**Gate:** For each affected concept, the exact eligible Q4 candidate set equals the Q4 IDs present
in its YAML, except for documented and justified concept-specific exclusions. No Q1 2026+ paper is
introduced by the Q4 pass.

### Stage 2 — Q4 Phase 2 synthesis

- [ ] Run only after the target concept's Phase 1 queue is closed.
- [ ] Update method families and reciprocal paper memberships from the complete YAML.
- [ ] Merge Q4 evidence into existing claim clusters or create narrowly supported new clusters.
- [ ] Reassess status, confidence, caveats, and triggered reassessment items without using paper
      counts as a substitute for evidence independence.
- [ ] Update open questions and trend notes with Q4-specific changes.

**Gate:** Every affected concept has a coherent Q4-updated synthesis; `paper_count == len(papers)`;
all cluster and family references resolve; warnings are inspected and explained.

### Stage 3 — Integration validation and closure audit

- [ ] Run concept-scoped health after every Phase 1 batch and Phase 2 pass.
- [ ] Run the corpus-wide integrate module after all 22 concepts close.
- [ ] Compare the exact bounded Q4 candidate and YAML ID sets for every concept.
- [ ] Audit the two Q4 pages without concept assignments.
- [ ] Record all intentional exclusions and remaining warnings.

**Gate:** Integrate health reports zero errors, all Q4 discrepancies are explained, and the Q4
claim-graph state is stable enough to become the source for reconciliation.

### Stage 4 — Q4 cross-concept reconciliation

- [ ] Generate deterministic `2025-Q4` candidates only after Stage 3 closes.
- [ ] Preserve existing Q3 human-approved registry authority and audit history.
- [ ] Review candidates in themed batches: evaluation; efficiency; speaker; controllability;
      robustness; codecs/language modeling; streaming/spoken agents; post-training.
- [ ] Keep agent recommendations separate from human decisions.
- [ ] Obtain explicit human accept/reject/defer decisions before finalization.
- [ ] Validate qualified references, cycles, evidence deduplication, source digests, and complete
      dispositions.

**Gate:** The Q4 run is finalized with no pending candidates; only human-approved relationships and
broader claims are authoritative downstream.

### Stage 5 — Concept rendering

- [ ] Identify every Overview/In Depth pair stale against its Q4-updated YAML.
- [ ] Render both formats from one shared editorial plan per concept.
- [ ] Preserve uncertainty, evidence roles, scope limits, and representative traceability.
- [ ] Render `singing` and `fine-tuning` if their complete evidence now supports useful production
      synthesis; otherwise document why a placeholder remains.
- [ ] Update the concept catalog and content log.

**Gate:** Render health reports zero errors; every Q4-updated concept either has current production
formats or an explicit evidence-based reason for deferral.

### Stage 6 — Field overview rendering

- [ ] Regenerate `overview.md` from all 23 concept YAMLs and the human-approved registry.
- [ ] Deduplicate linked clusters and paper evidence while retaining local caveats.
- [ ] Separate Q4 evidence change from publication volume and attention.
- [ ] State the evidence cutoff and retrospective assessment date precisely.
- [ ] Refresh reader navigation if concept or report availability changes.

**Gate:** All 23 concepts inform the field view; no candidate or agent-only proposal affects the
published synthesis; every factual conclusion remains traceable.

### Stage 7 — Optional Q4 snapshot and quarterly report

- [ ] Obtain approval to continue from current-state rendering into immutable temporal reporting.
- [ ] Freeze `2025-Q4` from the finalized human-review run with baseline cutoff `2025-09-30`,
      activity window `2025-10-01` through `2025-12-31`, and evidence cutoff `2025-12-31`.
- [ ] Validate canonical dates, source commits and digests, retrospective assessment semantics,
      reproducibility, and published-snapshot immutability.
- [ ] Generate `reports/quarterly/2025-Q4.md` only from the published snapshot.
- [ ] Compare Q4 activity and knowledge-state changes against the Q3 boundary without equating
      publication counts with evidence strength, adoption, or consensus.
- [ ] Update the reports index, navigation, provenance, and log.

**Gate:** Snapshot and report validation pass; the report is reproducible from the immutable Q4
snapshot and is explicitly labeled as a retrospective assessment.

---

## Integration methodology

Use `.agents/skills/speech-generation-integration-agent/SKILL.md` and
`docs/schemas/claims.md` as the operational authority.

Phase 1 reads paper pages and writes paper entries only. It is idempotent and capped at 20 new
papers per concept per invocation. Phase 2 reads only the concept YAML and performs cross-paper
synthesis. Never combine concept YAML writes concurrently.

Q4 pages should predominantly use the structured claims format:

```markdown
- **supports:** {generalized claim.}
  > *Evidence:* {paper-local fact.} *(§4.2, Table 1)*
```

Legacy claims remain supported. Include every claim. A missing source is a reported data-hygiene
issue, not permission to drop the claim. Quote YAML IDs and dates to avoid numeric or date coercion.

### Concept cadence

Default order is largest Q4 queue first, because it closes the largest evidence surfaces early:

1. `subjective-evaluation`
2. `evaluation-metrics`
3. `zero-shot-tts`
4. `neural-codec`
5. `spoken-language-model`
6. remaining concepts in descending live queue size

Within one concept:

1. Recompute live discovery.
2. Run sequential Phase 1 batches of at most 20.
3. Audit candidate IDs against written YAML IDs.
4. Run Phase 2 only after Phase 1 closure.
5. Run the health check and spot-check claims against paper pages.
6. Commit at an approved concept or coherent batch boundary.
7. Update this note with exact resume state.

The user may choose a different ordering or smaller approval cadence. Follow the most recent
instruction rather than silently reverting to this default.

### Validation commands

```bash
export SPEECH_WIKI_CONTENT_DIR=/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content-integrate

.venv/bin/python scripts/health_check.py --module integrate \
  --concept {slug} --phase 1 --wiki-dir "$SPEECH_WIKI_CONTENT_DIR" -v

.venv/bin/python scripts/health_check.py --module integrate \
  --concept {slug} --phase 2 --wiki-dir "$SPEECH_WIKI_CONTENT_DIR" -v

.venv/bin/python scripts/health_check.py --module integrate \
  --wiki-dir "$SPEECH_WIKI_CONTENT_DIR" -v

.venv/bin/python scripts/health_check.py --module reconcile \
  --wiki-dir "$SPEECH_WIKI_CONTENT_DIR"

.venv/bin/python scripts/health_check.py --module render \
  --wiki-dir "$SPEECH_WIKI_CONTENT_DIR"
```

Independently verify the agent's summary against actual YAML, health output, and sampled paper-page
claims. A plausible narrative is not validation.

---

## Repository ownership and commits

| Stage | Infrastructure repository | Content repository |
|---|---|---|
| Integration | This session note, status/backlog | `_claims/*.yaml`, `log.md` |
| Reconciliation/snapshot | Schemas or tooling only if changed; this note | `_claims/_reconciliation/`, `log.md` |
| Rendering | Tooling only if changed; this note | `concepts/`, `overview.md`, indexes, `log.md` |
| Report | Tooling only if changed; this note | `reports/`, indexes, navigation, `log.md` |

Keep infra and content commits separate at coherent phase boundaries. Do not write through the
infra `wiki/` submodule. A pure integration change does not need a site-content bump; visible
render or report publication follows the repository's normal publication workflow.

---

## Completion criteria

- All eligible Q4 concept-paper memberships are integrated or explicitly excluded with rationale.
- All 22 affected concepts complete Phase 2 synthesis and pass integration health with zero errors.
- Q4 reconciliation is finalized through explicit human decisions with no pending candidates.
- All stale concept pages and the field overview are regenerated and validated.
- If Stage 7 is approved, the Q4 snapshot and quarterly report are published, immutable,
  retrospective, and reproducible.
- `STATUS.md`, `BACKLOG.md`, this note, and the content log agree on the final state.
- Both repositories are clean at closeout, and the completed session note is archived under
  `docs/records/` with a dated filename.

---

## Session Log

### 2026-09-20 — speech-to-speech Phase 2 synthesis complete

- Synthesized the complete 94-paper YAML without re-reading paper pages; all 34 Q4 entries were
  included in the evidence review.
- Expanded the five established method families and added two Q4 families for incremental/concurrent
  reasoning and retrieval/tool-augmented spoken agents. Reciprocal assignments cover 24/34 Q4 papers;
  the other 10 are intentional benchmark, evaluation, or peripheral-task outliers.
- Updated all 16 existing claim clusters and added three strongly supported Q4 clusters: incremental
  reasoning during listening, structured and synthetic training for direct S2ST, and uneven
  multilingual/code-switched performance. All 33 Q4 papers with high- or medium-relevance claims
  map to at least one cluster.
- Reviewed all five prior reassessment items. The staged-pretraining and cascade-gap triggers remain
  unmet; the three due or overdue paper/scope items remain surfaced for human review. Added one
  reassessment for natural-interaction transfer of incremental reasoning results.
- Added two open questions and three Q4 trend notes. Appended the required sub-200-word cluster
  summary to the ignored local review log.
- The concept-scoped Phase 2 check passes with 0 errors and 28 accepted method-family warnings.
  The corpus-wide integration check passes with 0 errors and 299 warnings, with 2,555 paper entries,
  413 clusters (288 strongly supported, 15 contested), and `papers_not_in_any_yaml=184`.
- Next: begin `autoregressive-codec-tts` Q4 Phase 1 after recomputing its live queue; the dashboard
  currently shows 31 pending entries.

### 2026-09-20 — speech-to-speech Phase 1 batch 2 and closure (80 → 94 cumulative)

- Recomputed the live queue after batch 1 and processed the remaining 14 papers oldest-first,
  from `2025.emnlp-main.1492` through `2512.20296`.
- Preserved all 57 claims from 13 structured-claim pages and one legacy page (`2511.15848`), with
  no empty claim lists or `source: not specified` entries.
- Assigned concept-specific paper relevance of 12 high and 2 medium; claim relevance totals are 48
  high, 4 medium, and 5 low. Persona-aware dialogue, direct retrieval, dubbing and translation,
  multi-round full-duplex evaluation, audio-visual dialogue, acoustically grounded reasoning, and
  modular cascaded interaction received the strongest relevance.
- Canonical metadata dates match every written `published_date`; the YAML now contains 94
  cumulative papers with no duplicate IDs.
- The exact Q4 candidate-versus-YAML audit closes at 34/34, with no missing or extra candidate IDs,
  superseding the 35-paper planning estimate.
- The concept-scoped Phase 1 health check passes with 0 errors and 0 warnings. The corpus-wide
  integration check passes with 0 errors and 323 non-blocking warnings, with 2,555 total paper
  entries and `papers_not_in_any_yaml=184`.
- Next: run `speech-to-speech` Phase 2 synthesis across the complete 94-paper YAML.

### 2026-09-20 — speech-to-speech Phase 1 batch 1 (60 → 80 cumulative)

- Recomputed the bounded live Q4 queue from canonical metadata and YAML-parsed paper frontmatter.
  The live set is 34 candidates with none already in the concept YAML, superseding the dashboard
  baseline of 35 candidates.
- Processed the first 20 eligible papers oldest-first, from `2510.00499` through
  `2025.emnlp-main.1160`.
- Preserved all 88 claims from 18 structured-claim pages and two legacy pages (`2510.07838` and
  `2025.emnlp-demos.70`), with no empty claim lists or `source: not specified` entries.
- Assigned concept-specific paper relevance of 15 high, 4 medium, and 1 low; claim relevance totals
  are 65 high, 14 medium, and 9 low. Text-free dialogue, streaming retrieval and reasoning,
  full-duplex interaction, code switching, direct translation, prosody transfer, persona and
  emotional evaluation, and modular-versus-native architecture trade-offs received the strongest
  relevance.
- Canonical metadata dates match every written `published_date`; the YAML contains 80 cumulative
  papers with no duplicate IDs after the batch.
- The concept-scoped Phase 1 health check passes with 0 errors and 0 warnings. Q4 progress is
  20/34, with 14 eligible papers remaining.
- Next: close Phase 1 with `2025.emnlp-main.1492` through `2512.20296`.

### 2026-09-20 — spoken-language-model Phase 2 synthesis complete

- Synthesized the complete 173-paper YAML without re-reading paper pages; all 46 Q4 entries were
  included in the evidence review.
- Reviewed all 17 existing clusters and mapped every Q4 paper carrying high- or medium-relevance
  claims to at least one cluster. Added one strongly supported cluster for incremental reasoning
  and tool use during the user-listening window.
- Promoted the safety, privacy, misuse, and provenance cluster from emerging to strongly supported
  after new Q4 evidence on traceability gaps, multilingual refusal fragility, audio-channel
  jailbreaks, deepfake-detector limits, and multi-round safety evaluation. All 18 clusters are now
  strongly supported; none is contested.
- Updated the six existing method families and added a 21-paper full-duplex streaming-dialogue
  family spanning both earlier and Q4 systems. The graph now has 211 reciprocal memberships across
  134/173 papers; 35/46 Q4 papers are assigned, while 11 Q4 and 28 earlier architecture-unspecified
  benchmark, survey, dataset, or evaluation papers remain intentional outliers.
- Added one method-family reassessment for future full-duplex subgroup boundaries, added two open
  questions, and refreshed seven trend notes through Q4 2025.
- The concept-scoped Phase 2 health check passes with 0 errors and 39 accepted method-family
  warnings. The corpus-wide integration check passes with 0 errors and 289 non-blocking warnings;
  totals remain 2,521 paper entries and rise to 410 clusters, with 285 strongly supported and 15
  contested, and `papers_not_in_any_yaml=184`.
- Added the required 150-word cluster overview to the local, ignored Phase 2 summary log.
- Next: begin `speech-to-speech` Q4 Phase 1 after recomputing its live queue; the dashboard
  baseline is 35 candidates and none already present.

### 2026-09-20 — spoken-language-model Phase 1 batch 3 and closure (167 → 173 cumulative)

- Recomputed the live queue after batch 2 and confirmed the final six eligible Q4 papers, from
  `neurips-2025-vhPy3NMsO5` through `2512.23808`.
- Extracted all 24 claims from six structured-claim pages, with no empty claim lists or
  `source: not specified` entries.
- Assigned concept-specific paper relevance of 5 high and 1 medium; claim relevance totals are 21
  high and 3 medium. Online multimodal response generation, natural multi-turn evaluation,
  modular low-latency dialogue, large-scale unified speech modeling, and full-duplex behavior
  reasoning received the strongest relevance.
- Canonical metadata dates match every written `published_date`; the YAML now contains 173
  cumulative papers with no duplicate IDs.
- The exact Q4 candidate-versus-YAML audit closes at 46/46, with no missing or extra candidate IDs.
- The concept-scoped Phase 1 health check passes with 0 errors and 0 warnings. The corpus-wide
  integration check passes with 0 errors and 324 non-blocking warnings, with 2,521 total paper
  entries and `papers_not_in_any_yaml=184`.
- Next: run `spoken-language-model` Phase 2 synthesis across the complete 173-paper YAML.

### 2026-09-20 — spoken-language-model Phase 1 batch 2 (147 → 167 cumulative)

- Recomputed the live queue and confirmed 46 eligible Q4 papers, 20 already integrated, and 26
  pending before this batch.
- Processed the next 20 papers oldest-first, from `2511.01261` through
  `neurips-2025-AsRB5nmlOD`.
- Extracted all 85 paper-page claims. Fifteen pages used structured role/evidence claims; five
  pages used the legacy format. Fifteen legacy evidence statements were reused from reviewed
  entries in other concept YAMLs, while the remaining nine were reconstructed only from the
  existing OpenS2S and Step-Audio-R1 paper-page methods, results, and limitations.
- Assigned concept-specific paper relevance of 16 high, 2 medium, and 2 low; claim relevance totals
  are 69 high, 10 medium, and 6 low. Human-aligned dialogue evaluation, empathetic generation,
  multimodal grounding, persona-aware interaction, retrieval, multi-token prediction, audio-native
  judging, full-duplex evaluation, and acoustically grounded reasoning received the strongest
  relevance.
- The batch has no empty claim lists or `source: not specified` entries. Canonical metadata dates
  match every written `published_date`; the YAML contains 167 cumulative papers with no duplicate
  IDs after the batch.
- The concept-scoped Phase 1 health check passes with 0 errors and 0 warnings. Q4 progress is
  40/46, with six eligible papers remaining.
- Next: close Phase 1 with `neurips-2025-vhPy3NMsO5` through `2512.23808`.

### 2026-09-20 — spoken-language-model Phase 1 batch 1 (127 → 147 cumulative)

- Recomputed the bounded live Q4 queue from canonical metadata and YAML-parsed paper frontmatter.
  The live set is 46 candidates with none already in the concept YAML, superseding the planning
  baseline of 49 candidates with 2 already present.
- Processed the first 20 eligible papers oldest-first, from `2510.00499` through `2511.00850`.
- Extracted all 90 paper-page claims. Eighteen pages used structured role/evidence claims;
  `2510.00981` and `2510.07838` used the legacy format, so their ten evidence statements were
  carried over from the already-reviewed neural-codec and evaluation-metrics entries.
- Assigned concept-specific paper relevance of 14 high, 3 medium, and 3 low; claim relevance totals
  are 66 high, 12 medium, and 12 low. Incremental reasoning, streaming retrieval and tool use,
  full-duplex evaluation, multi-turn spoken context, modality-preserving architectures,
  multilingual agent behavior, and expressive-dialogue data received the strongest relevance.
- The batch has no empty claim lists or `source: not specified` entries. Canonical metadata dates
  match every written `published_date`; the YAML now contains 147 cumulative papers with no
  duplicate IDs.
- The concept-scoped Phase 1 health check passes with 0 errors and 0 warnings. The corpus-wide
  integration check passes with 0 errors and 298 non-blocking warnings, with 2,495 total paper
  entries and `papers_not_in_any_yaml=191`.
- Q4 progress is 20/46, with 26 eligible papers remaining. The next five are `2511.01261`,
  `2025.emnlp-demos.70`, `2025.emnlp-main.1160`, `2025.emnlp-main.1447`, and
  `2025.emnlp-main.1492`.
- Phase 2 remains blocked until all 46 live Q4 candidates are integrated.
- Next: `spoken-language-model` Phase 1 batch 2, starting at `2511.01261`.

### 2026-09-20 — neural-codec Phase 2 synthesis complete

- Synthesized the complete 239-paper YAML without re-reading paper pages; all 56 Q4 entries were
  included in the evidence review.
- Updated all seven established method families and assigned 47/56 Q4 papers. Nine Q4 papers
  remain deliberate evaluation, benchmark, dialogue-context, or peripheral-use outliers. Overall
  reciprocal family coverage is 218/239 papers with 351 memberships; all 21 warnings correspond
  exactly to the retained outliers.
- Updated all 17 existing claim clusters and added one strongly supported Q4 cluster:
  `codec_robustness_requires_domain_aware_training`. All 18 clusters are strongly supported; none
  is contested.
- Reviewed all five reassessment items. Q4 evidence strengthens their rationales, but none meets
  its explicit trigger for resolution or family subdivision. Replaced two open questions and
  added one on ultra-low-rate designs; added three Q4 trend notes.
- Appended the required sub-200-word cluster summary to the local ignored review log.
- The concept-scoped Phase 2 health check passes with 0 errors and 21 accepted method-family
  warnings. The corpus-wide integration check passes with 0 errors and 278 non-blocking warnings;
  totals are 2,475 paper entries and 409 clusters, with 283 strongly supported and 15 contested,
  and `papers_not_in_any_yaml=197`.
- Next: begin `spoken-language-model` Q4 Phase 1 after recomputing its live queue; the planning
  baseline is 49 candidates, 2 already present, and 47 pending.

### 2026-09-20 — neural-codec Phase 1 batch 3 and closure (223 → 239 cumulative)

- Recomputed the live queue and confirmed the final 16 eligible Q4 papers, from `2511.19734`
  through `2512.23808`.
- Extracted all 69 paper-page claims. Twelve pages used structured role/evidence claims;
  `2512.04720`, `2502.03930`, `2512.13251`, and `2512.14291` used the legacy format, so their 19
  evidence statements were reconstructed only from existing paper-page results and limitations.
- Assigned concept-specific paper relevance of 12 high, 2 medium, and 2 low; claim relevance totals
  are 51 high, 6 medium, and 12 low. Geometry-aware and semantic quantization, continuous VAE
  tokens, streaming flow decoding, factorized codec control, anti-aliasing, and domain robustness
  received the strongest relevance.
- The batch has no empty claim lists or `source: not specified` entries. Canonical metadata dates
  match every written `published_date`; the YAML now contains 239 cumulative papers with no
  duplicate IDs.
- The exact Q4 candidate-versus-YAML audit closes at 56/56, with no missing or extra candidate IDs.
- The concept-scoped Phase 1 health check passes with 0 errors and 0 warnings.
- Next: run `neural-codec` Phase 2 synthesis across the complete 239-paper YAML.

### 2026-09-20 — neural-codec Phase 1 batch 2 (203 → 223 cumulative)

- Recomputed the live queue and confirmed 56 eligible Q4 papers, 20 already integrated, and 36
  pending before this batch.
- Processed the next 20 eligible papers oldest-first, from `2510.16718` through `2511.16639`.
- Extracted all 87 paper-page claims. Eighteen pages used structured role/evidence claims;
  `2025.emnlp-main.989` and `2511.12347` used the legacy format, so their ten evidence statements
  were reconstructed only from the existing paper-page Key Results and limitations sections.
- Assigned concept-specific paper relevance of 12 high, 6 medium, and 2 low; claim relevance totals
  are 51 high, 12 medium, and 24 low. Ultra-low-rate reconstruction, separate semantic/acoustic
  streams, compressed-spectrum streaming, spatial audio, continuous tokenization, codec evaluation,
  controllable and factorized representations, and codec-token SSL received the strongest relevance.
- The batch has no empty claim lists or `source: not specified` entries. Canonical metadata dates
  match every written `published_date`; the YAML now contains 223 cumulative papers with no
  duplicate IDs.
- The concept-scoped Phase 1 health check passes with 0 errors and 0 warnings. The corpus-wide
  integration check passes with 0 errors and 309 non-blocking warnings, with 2,459 total paper
  entries and `papers_not_in_any_yaml=201`.
- Q4 progress is 40/56, with 16 eligible papers remaining. The final batch starts with
  `2511.19734`, `2511.20974`, `2511.22687`, `2512.01537`, and `2512.01865`.
- Phase 2 remains blocked until all 56 live Q4 candidates are integrated.
- Next: close `neural-codec` Phase 1 with the final 16-paper batch, starting at `2511.19734`.

### 2026-09-20 — neural-codec Phase 1 batch 1 (183 → 203 cumulative)

- Recomputed the bounded live Q4 queue from canonical metadata and YAML-parsed paper frontmatter.
  The live set is 56 candidates with none already in the concept YAML, superseding the planning
  baseline of 58 candidates with 2 already present.
- Processed the first 20 eligible papers oldest-first, from `2510.00499` through `2510.15364`.
- Extracted all 87 paper-page claims. Sixteen pages used structured role/evidence claims;
  `2510.00981`, `2510.02848`, `2510.05758`, and `2510.12210` used the legacy format, so their 17
  evidence statements were reconstructed only from the existing paper-page Key Results and
  limitations sections.
- Assigned concept-specific paper relevance of 9 high, 5 medium, and 6 low; claim relevance totals
  are 36 high, 18 medium, and 33 low. Dynamic low-rate tokenization, 2D and single-codebook
  compression, factorized sub-latents, sparse-to-dense bridging, controllable RVQ depth, and
  low-compute decoding received the strongest relevance.
- The batch has no empty claim lists or `source: not specified` entries. Canonical metadata dates
  match every written `published_date`; the YAML now contains 203 cumulative papers with no
  duplicate IDs.
- The concept-scoped Phase 1 health check passes with 0 errors and 0 warnings. The corpus-wide
  integration check passes with 0 errors and 289 non-blocking warnings, with 2,439 total paper
  entries and `papers_not_in_any_yaml=206`.
- Q4 progress is 20/56, with 36 eligible papers remaining. The next five are `2510.16718`,
  `2510.16841`, `2510.19509`, `2510.21209`, and `2510.22241`.
- Phase 2 remains blocked until all 56 live Q4 candidates are integrated.
- Next: `neural-codec` Phase 1 batch 2, starting at `2510.16718`.

### 2026-09-20 — zero-shot-tts Phase 2 synthesis complete

- Synthesized the complete 262-paper YAML without re-reading paper pages; all 59 Q4 entries were
  included in the evidence review.
- Updated all nine method families and assigned 51/59 Q4 papers. Eight Q4 papers remain intentional
  architecture, evaluation, optimization, or dataset outliers; together with 16 preserved
  Q3-and-earlier outliers, method-family coverage is 238/262 and accounts for all 24 warnings.
- Updated all 18 existing claim clusters and added two narrowly supported Q4 clusters. Preference
  and reinforcement optimization is strongly supported, with explicit reward-control caveats;
  non-audio conditioning from faces or descriptions is emerging and remains coarser than acoustic
  reference conditioning.
- The two previously contested conclusions remain contested: cross-lingual cloning still faces
  language and accent leakage, and automatic metrics still do not fully capture perceived cloning
  quality. No reassessment item was triggered or resolved.
- Added two open questions on reward safeguards and multimodal identity validity and bias, plus
  three trend notes covering broader generation settings, acceleration strategies, and Q4
  post-training practices. The required sub-200-word cluster summary was appended to the local,
  ignored review log.
- The concept-scoped Phase 2 health check passes with 0 errors and 24 accepted method-family
  warnings. The corpus-wide integration check passes with 0 errors and 269 non-blocking warnings;
  totals are 2,419 paper entries and 408 clusters, with 282 strongly supported and 15 contested,
  and `papers_not_in_any_yaml=213`.
- Next: begin `neural-codec` Q4 Phase 1 after recomputing its live queue; the planning baseline is
  58 candidates, 2 already present, and 56 pending.

### 2026-09-20 — zero-shot-tts Phase 1 batch 3 and closure (243 → 262 cumulative)

- Recomputed the live queue and confirmed the final 19 eligible Q4 papers, from `2512.00451`
  through `2512.23808`.
- Extracted all 87 paper-page claims. Fifteen pages used structured role/evidence claims;
  `2512.04720`, `2502.03930`, `2512.13251`, and `2512.14291` used the legacy format, so their 19
  evidence statements were reconstructed only from the existing paper-page Key Results and
  limitations sections.
- Assigned concept-specific paper relevance of 13 high and 6 medium; claim relevance totals are 58
  high, 27 medium, and 2 low. Foundation speech generation, continuous-latent autoregression,
  multilingual adaptation, fine-grained control, long-context dialogue, and robust zero-shot
  generation received the strongest relevance.
- The batch has no empty claim lists or `source: not specified` entries. Canonical metadata dates
  match every written `published_date`; the YAML now contains 262 cumulative papers with no
  duplicate IDs.
- The exact Q4 candidate-versus-YAML audit closes at 59/59, with no missing or extra candidate IDs.
- The concept-scoped Phase 1 health check passes with 0 errors and 0 warnings. The corpus-wide
  integration check passes with 0 errors and 320 non-blocking warnings, with 2,419 total paper
  entries and `papers_not_in_any_yaml=213`.
- Next: run `zero-shot-tts` Phase 2 synthesis across the complete 262-paper YAML.

### 2026-09-20 — zero-shot-tts Phase 1 batch 2 (223 → 243 cumulative)

- Recomputed the live queue and confirmed 59 eligible Q4 papers, 20 already integrated, and 39
  pending before this batch.
- Processed the next 20 eligible papers oldest-first, from `2510.23541` through `2511.21270`.
- Extracted all 87 paper-page claims. Eighteen pages used structured role/evidence claims;
  `2025.emnlp-main.40` and `2511.12347` used the legacy format, so their ten evidence statements
  were reconstructed only from the existing paper-page synthesis and Key Results sections.
- Assigned concept-specific paper relevance of 11 high, 5 medium, and 4 low; claim relevance totals
  are 41 high, 30 medium, and 16 low. Long-form and streaming generation, multilingual cloning,
  representation alignment, multimodal speaker control, accent mitigation, and evaluation validity
  received the strongest relevance.
- The batch has no empty claim lists or `source: not specified` entries. Canonical metadata dates
  match every written `published_date`; the YAML now contains 243 cumulative papers with no
  duplicate IDs.
- The concept-scoped Phase 1 health check passes with 0 errors and 0 warnings. The corpus-wide
  integration check passes with 0 errors and 301 non-blocking warnings, with 2,400 total paper
  entries and `papers_not_in_any_yaml=225`.
- Q4 progress is 40/59, with 19 eligible papers remaining. The next five are `2512.00451`,
  `2512.04720`, `2512.04779`, `2512.04793`, and `2502.03930`.
- Phase 2 remains blocked until all 59 live Q4 candidates are integrated.
- Next: close `zero-shot-tts` Phase 1 with the final 19-paper batch, starting at `2512.00451`.

### 2026-09-20 — zero-shot-tts Phase 1 batch 1 (203 → 223 cumulative)

- Recomputed the live Q4 queue from canonical metadata and YAML-parsed paper frontmatter. The live
  set is 59 candidates with none already in the concept YAML, superseding the planning baseline of
  61 candidates with 2 already present.
- Processed the first 20 eligible papers oldest-first, from `2025.vlsp-1.14` through
  `2511.05516`.
- Extracted all 87 paper-page claims. Seventeen pages used structured role/evidence claims;
  `2510.02848`, `2510.07979`, and `2510.12210` used the legacy format, so their 13 evidence
  statements were reconstructed only from the existing paper-page Key Results sections.
- Assigned concept-specific paper relevance of 11 high, 7 medium, and 2 low; claim relevance totals
  are 34 high, 42 medium, and 11 low. Direct voice-cloning architectures, sparse or continuous
  representations, cross-lingual conditioning, evaluator-guided correction, and emotion control
  received the strongest relevance.
- The batch has no empty claim lists or `source: not specified` entries. Canonical metadata dates
  match every written `published_date`; the YAML now contains 223 cumulative papers with no
  duplicate IDs.
- The concept-scoped Phase 1 health check passes with 0 errors and 0 warnings. The corpus-wide
  integration check passes with 0 errors and 281 non-blocking warnings, with 2,380 total paper
  entries and `papers_not_in_any_yaml=231`.
- Q4 progress is 20/59, with 39 eligible papers remaining. The next five are `2510.23541`,
  `2510.24372`, `2510.25577`, `2510.26190`, and `2511.01261`.
- Phase 2 remains blocked until all 59 live Q4 candidates are integrated.
- Next: `zero-shot-tts` Phase 1 batch 2, starting at `2510.23541`.

### 2026-09-20 — evaluation-metrics Phase 2 synthesis complete

- Synthesized the complete 346-paper YAML without re-reading paper pages; all 61 Q4 entries were
  included in the evidence review.
- Updated all 17 existing method families and assigned 55/61 Q4 papers. Six Q4 papers remain
  intentional architecture, optimization, or robustness outliers; together with 14 preserved
  Q3-and-earlier outliers, method-family coverage is 326/346 and accounts for all 20 warnings.
- Reviewed and updated 24/31 existing claim clusters. No distinct Q4 proposition required a new
  cluster, and the existing LLM/audio-judge cluster remains contested rather than resolving in
  either direction.
- Promoted `corpus_quality_filtering_criteria_introduce_data_distortions` from emerging to
  strongly supported after independent Q4 evidence covered preprocessing trade-offs,
  expressiveness filtering, automatic annotation/filtering, synthetic support-set construction,
  and segmentation choices.
- Reassessed the oversized `objective_perceptual_quality_metric_divergence` family after it
  reached 120 papers. The umbrella is retained because narrower overlapping families already
  isolate learned MOS predictors, codec suites, WER, speaker similarity, prosody, and
  pronunciation; its completed reassessment item was removed. Six reassessment items remain.
- Replaced the stale taxonomy-count open question with a modality-gap attribution question and
  added Q4 trend notes on the shift toward audio-native, multi-turn, comprehension-based,
  confounder-paired, and natural-human-speech evaluation protocols.
- The concept-scoped Phase 2 health check passes with 0 errors and 20 accepted method-family
  warnings. The corpus-wide integration check passes with 0 errors and 261 non-blocking warnings;
  totals remain 2,360 paper entries and 406 clusters, now with 281 strongly supported and 15
  contested, and `papers_not_in_any_yaml=242`.
- Next: begin `zero-shot-tts` Q4 Phase 1 after recomputing its live queue.

### 2026-09-20 — evaluation-metrics Phase 1 batch 4 and closure (345 → 346 cumulative)

- Recomputed the live queue and confirmed `2512.23808` was the only remaining eligible Q4 paper.
- Read the full paper page and extracted all four structured claims with their roles, evidence,
  and cited sources; no legacy reconstruction or unspecified source was required.
- Classified the paper as medium relevance to evaluation metrics, with SpeechMMLU's cross-modal
  modality-gap diagnostic as the direct high-relevance claim and three scaling, instruction, and
  reasoning findings as medium-relevance evidence.
- Verified the written `published_date` (`2025-12-29`) against canonical metadata. The concept
  YAML now contains 346 cumulative papers with no duplicate IDs or empty claim lists.
- The exact Q4 candidate-versus-YAML audit closes at 61/61, with no missing or extra Q4 IDs.
- The concept-scoped Phase 1 health check passes with 0 errors and 0 warnings. The corpus-wide
  integration check passes with 0 errors and 316 non-blocking warnings, with 2,360 total paper
  entries and `papers_not_in_any_yaml=242`.
- Next: run `evaluation-metrics` Phase 2 synthesis across the complete 346-paper YAML.

### 2026-09-20 — evaluation-metrics Phase 1 batch 3 (325 → 345 cumulative)

- Recomputed the live Q4 queue and confirmed 61 eligible papers, 40 already integrated, and 21
  pending before this batch.
- Processed the next 20 eligible papers oldest-first, from `2511.06150` through `2512.14865`.
- Extracted all 84 paper-page claims. All 20 pages used the structured role/evidence format, so no
  legacy evidence reconstruction was required.
- Assigned concept-specific paper relevance of 6 high and 14 medium; claim relevance totals are
  40 high, 26 medium, and 18 low. Audio-native judges, multi-round/full-duplex benchmarks,
  harmful-audio safety evaluation, codec-metric validity, multimodal singing feedback, and
  natural multi-turn dialogue evaluation received the strongest relevance.
- The finished batch has no empty claim lists and no `source: not specified` entries. Canonical
  metadata dates match every written `published_date`; the YAML now contains 345 cumulative
  papers with no duplicate IDs.
- The concept-scoped Phase 1 health check passes with 0 errors and 0 warnings. The corpus-wide
  integration check passes with 0 errors and 315 non-blocking warnings, with 2,359 total paper
  entries and `papers_not_in_any_yaml=243`.
- Q4 progress is 60/61. The exact oldest-first audit confirms that only `2512.23808` remains.
- Phase 2 remains blocked until that final paper is integrated and the 61/61 closure audit passes.
- Next: close `evaluation-metrics` Phase 1 with `2512.23808`, then run Phase 2 synthesis.

### 2026-09-20 — evaluation-metrics Phase 1 batch 2 (305 → 325 cumulative)

- Recomputed the live Q4 queue and confirmed 61 eligible papers, 20 already integrated, and 41
  pending before this batch; the apparent earlier `2510.14664` page is Tier 2 and remains excluded.
- Processed the next 20 eligible papers oldest-first, from `2510.22241` through
  `2025.arabicnlp-main.38`.
- Extracted all 83 paper-page claims: 18 pages used the structured role/evidence format, while
  `2025.emnlp-main.40` and `2025.findings-emnlp.424` used the legacy format. Reconstructed their
  ten evidence statements only from the existing Method, Key Results, and Limitations sections.
- Assigned concept-specific paper relevance of 10 high and 10 medium; claim relevance totals are
  55 high, 8 medium, and 20 low. Dedicated evaluation frameworks, benchmark-design evidence,
  metric divergence, and human-aligned judge validation received the strongest relevance.
- The finished batch has no empty claim lists and no `source: not specified` entries. The YAML now
  contains 325 cumulative papers and remains internally consistent with no duplicate IDs.
- The concept-scoped Phase 1 health check passes with 0 errors and 0 warnings. The corpus-wide
  integration check passes with 0 errors and 295 non-blocking warnings, with 2,339 total paper
  entries and `papers_not_in_any_yaml=255`.
- Q4 progress is 40/61, with 21 eligible papers remaining. The next five are `2511.06150`,
  `2508.20916`, `2511.07135`, `2511.10112`, and `2511.10262`.
- Phase 2 remains blocked until all 61 Q4 candidates are integrated.
- Next: `evaluation-metrics` Phase 1 batch 3, starting at `2511.06150`.

### 2026-09-20 — evaluation-metrics Phase 1 batch 1 (285 → 305 cumulative)

- Recomputed the live Q4 queue and confirmed 61 eligible papers with no Q4 entries already in the
  concept YAML.
- Processed the first 20 papers oldest-first, from `2025.vlsp-1.13` through `2510.21209`.
- Extracted all 88 paper-page claims: 18 pages used the structured role/evidence format, while
  `2510.07838` and `2510.07979` used the legacy format and required evidence reconstruction from
  their existing Method, Key Results, and Limitations sections.
- Assigned concept-specific paper relevance of 11 high, 7 medium, and 2 low; claim relevance totals
  are 40 high, 24 medium, and 24 low. Dedicated benchmarks, metric-validity studies, and evaluation
  frameworks received the strongest evaluation-metrics relevance.
- Corrected four source-parser misses on `2510.21209` caused by punctuation after the citation
  marker. The finished batch has no empty claim lists and no `source: not specified` entries.
- Validated after every paper write. The concept-scoped Phase 1 health check passes with 0 errors
  and 0 warnings; the corpus-wide integration check passes with 0 errors and 275 non-blocking
  warnings, with 2,319 total paper entries and `papers_not_in_any_yaml=264`.
- Q4 progress is 20/61, with 41 remaining. The next five are `2510.22241`, `2510.23312`,
  `2510.24372`, `2510.25566`, and `2510.25577`.
- Phase 2 remains blocked until all 61 Q4 candidates are integrated.
- Next: `evaluation-metrics` Phase 1 batch 2, starting at `2510.22241`.

### 2026-09-19 — subjective-evaluation Phase 2 synthesis complete

- Synthesized the complete 253-paper YAML without re-reading paper pages; all 73 Q4 entries were
  included in the Phase 2 evidence review.
- Updated all 7 existing method families and assigned 59 Q4 papers with recognized architecture
  values. The remaining 14 Q4 papers are intentional architecture-unspecified evaluation,
  benchmark, dataset, or metric outliers.
- Reviewed all 17 existing claim clusters and mapped every Q4 paper carrying high- or
  medium-relevance claims to at least one cluster. No distinct proposition met the threshold for a
  new cluster.
- Promoted `speaker_similarity_metrics_are_confounded` from emerging to strongly supported after
  independent Q4 evidence linked identity-score instability to protocol choice, pitch, duration,
  language adaptation, and reference design.
- Changed `learned_quality_metrics_outperform_classical_metrics` from strongly supported to
  contested after `2511.19734` found classical signal metrics could match or exceed learned
  predictors on neural-codec reconstruction quality.
- Added 2 open questions and 3 trend notes covering automatic-judge calibration, downstream codec
  usefulness, direct audio evaluation of dialogue systems, broader codec/vocoder test domains, and
  fine-grained control axes. No reassessment items were pending or triggered.
- The concept-scoped Phase 2 health check passes with 0 errors and 61 accepted method-family
  warnings. The corpus-wide integration check passes with 0 errors and 255 non-blocking warnings;
  totals remain 2,299 paper entries and 406 clusters, with 280 strongly supported and 15 contested.
- Next: begin `evaluation-metrics` Q4 Phase 1, the next-largest live queue, unless the user selects
  another concept.

### 2026-09-19 — subjective-evaluation Phase 1 batch 4 and closure (240 → 253/253 cumulative)

- Recomputed the live Q4 queue and confirmed the expected closing state: 73 eligible papers, 60
  already integrated, and 13 pending before this batch.
- Processed all 13 remaining papers oldest-first, from `2512.04779` through `2512.20944`.
- Extracted all 56 paper-page claims; all 13 pages used the structured role/evidence format, so no
  legacy evidence reconstruction was required.
- Assigned concept-specific paper relevance of 8 high and 5 medium; claim relevance totals are
  25 high, 22 medium, and 9 low. Multidimensional listener studies, human/automatic divergence,
  and perceptual trade-offs received the strongest subjective-evaluation relevance.
- Validated after every paper write, then ran the exact candidate-versus-YAML closure audit. All
  73 eligible Q4 IDs are present with no missing or extra IDs; the batch has no empty claim lists
  and no `source: not specified` entries.
- `subjective-evaluation.yaml` now contains 253 cumulative papers, closing Q4 Phase 1 at 73/73.
- The concept-scoped Phase 1 health check passes with 0 errors and 0 warnings. The corpus-wide
  integration check passes with 0 errors and 314 non-blocking warnings;
  `papers_not_in_any_yaml` is now 272.
- Next: run `subjective-evaluation` Phase 2 synthesis across the complete 253-paper YAML before
  moving to the next concept's Phase 1 queue.

### 2026-09-19 — subjective-evaluation Phase 1 batch 3 (220 → 240/253 cumulative)

- Recomputed the live Q4 queue and confirmed the expected resume state: 73 eligible papers, 40
  already integrated, and 33 pending before this batch.
- Processed the next 20 papers oldest-first, from `2025.emnlp-main.180` through `2512.04552`.
- Extracted all 85 paper-page claims: 18 pages used the structured role/evidence format and
  `2025.emnlp-main.180` plus `2511.12347` used the legacy format. Reconstructed their ten evidence
  statements only from the existing Method, Key Results, and Limitations sections.
- Assigned concept-specific paper relevance of 11 high and 9 medium; claim relevance totals are
  32 high, 23 medium, and 30 low. Human-evaluation methods and perceptual failure analyses remain
  distinguished from papers that use listening tests only to compare systems.
- Validated after every paper write, then ran the concept-scoped Phase 1 health check; all checks
  passed with 0 errors and 0 warnings. The finished batch has no empty claim lists and no
  `source: not specified` entries.
- `subjective-evaluation.yaml` now contains 240 cumulative papers. Q4 progress is 60/73, with 13
  remaining; the next five are `2512.04779`, `2512.08006`, `2512.09504`,
  `neurips-2025-1cURNMriee`, and `neurips-2025-SYcggdxX6W`.
- The corpus-wide integration check passes with 0 errors and 301 non-blocking warnings;
  `papers_not_in_any_yaml` is now 285.
- Phase 2 remains blocked until all 73 Q4 candidates are integrated.
- Next: `subjective-evaluation` Phase 1 batch 4, starting at `2512.04779` and closing the remaining
  13-paper queue.

### 2026-09-19 — subjective-evaluation Phase 1 batch 2 (200 → 220/253 cumulative)

- Recomputed the live Q4 queue and confirmed the expected resume state: 73 eligible papers, 20
  already integrated, and 53 pending before this batch.
- Processed the next 20 papers oldest-first, from `2510.15364` through
  `2025.emnlp-main.1730`.
- Extracted all 84 paper-page claims: 19 pages used the structured role/evidence format and
  `2025.emnlp-main.1730` used the legacy format. Reconstructed its five evidence statements only
  from the existing Method, Key Results, and Limitations sections.
- Assigned concept-specific paper relevance of 12 high, 6 medium, and 2 low; claim relevance totals
  are 37 high, 35 medium, and 12 low. Papers that merely report listening scores remain distinct
  from papers directly studying human evaluation protocols or human-aligned judges.
- Validated after every paper write, then ran the concept-scoped Phase 1 health check; all checks
  passed with 0 errors and 0 warnings. The finished batch has no empty claim lists and no
  `source: not specified` entries.
- `subjective-evaluation.yaml` now contains 220 cumulative papers. Q4 progress is 40/73, with 33
  remaining; the next five are `2025.emnlp-main.180`, `2025.findings-emnlp.933`, `2511.13732`,
  `2511.05143`, and `2511.07116`.
- The corpus-wide integration check passes with 0 errors and 281 non-blocking warnings;
  `papers_not_in_any_yaml` is now 305.
- Phase 2 remains blocked until all 73 Q4 candidates are integrated.
- Next: `subjective-evaluation` Phase 1 batch 3, starting at `2025.emnlp-main.180`.

### 2026-09-19 — subjective-evaluation Phase 1 batch 1 (180 → 200/253 cumulative)

- Recomputed the Q4-bounded queue and confirmed 73 eligible papers, no Q4 entries already present,
  four Tier 2 pages skipped corpus-wide, and 180 Q3-and-earlier entries already in the YAML.
- Processed the first 20 papers oldest-first, from `2025.vlsp-1.13` through `2510.13293`.
- Extracted all 86 paper-page claims: 19 pages used the structured role/evidence format and
  `2510.07979` used the legacy format. Reconstructed the legacy evidence only from its existing
  Method, Key Results, and Limitations sections.
- Assigned concept-specific paper relevance of 7 high, 8 medium, and 5 low; claim relevance totals
  are 35 high, 18 medium, and 33 low. Low-relevance claims remain present for completeness but will
  not drive Phase 2 status changes.
- Corrected five citation-parser misses on `2510.05150` caused by a period after the italic source
  marker; the finished batch has zero empty claim lists and zero `source: not specified` entries.
- Ran the concept-scoped Phase 1 health check after every paper and again after the closure audit;
  every run passed with 0 errors and 0 warnings. The exact first-batch ID set matches the first 20
  live Q4 candidates.
- `subjective-evaluation.yaml` now contains 200 cumulative papers. Q4 progress is 20/73, with 53
  remaining; the next five are `2510.15364`, `2510.16841`, `2510.19509`, `2510.20210`, and
  `2510.20513`.
- Phase 2 remains blocked until all 73 Q4 candidates are integrated.
- Next: `subjective-evaluation` Phase 1 batch 2, starting at `2510.15364`.

### 2026-09-19 — Q4 program bootstrap

- Confirmed the infrastructure `main` and content `work/integrate` worktrees were clean.
- Reviewed the completed Q3 integration record and the archived cross-concept synthesis and
  temporal-reporting program.
- Verified that Q3 is complete through human-reviewed reconciliation, retrospective snapshot,
  23-concept field overview, and quarterly report.
- Measured the current Q4 scope: 174 non-Tier-2 paper pages, 172 with canonical concept
  assignments, 22 affected concepts, 671 candidate memberships, 11 already present, and an
  estimated 660-entry Phase 1 queue.
- Ran integration, render, and reconciliation health checks; all passed with zero errors.
- Refreshed `STATUS.md`, promoted the Q4 content cycle to active P0 in `BACKLOG.md`, and created
  this seven-stage operating record.
- No content-repository files changed.
- Next: recompute and begin `subjective-evaluation` Phase 1 batch 1, unless the user selects a
  different concept or cadence.
