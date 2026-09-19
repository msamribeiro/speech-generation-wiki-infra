# Q4 2025 Integration and Synthesis Session

**Started:** 2026-09-19
**Status:** Active; subjective-evaluation complete through Phase 2
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

3. Recompute the live Q4 candidate queue for `evaluation-metrics`; do not rely only on the
   baseline table below.
4. Start `evaluation-metrics` Phase 1 with the oldest eligible Q4 papers, processing sequentially
   in batches of at most 20. The planning baseline was 61 candidates and no existing Q4 entries,
   but live discovery is authoritative.
5. Run and independently verify the concept-scoped integration health check after every batch.
6. Append a dated Session Log entry before ending the session, including the exact next paper or
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
