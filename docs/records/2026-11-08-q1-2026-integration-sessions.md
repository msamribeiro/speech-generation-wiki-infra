# Q1 2026 Integration and Synthesis Session

**Started:** 2026-11-08
**Status:** Phase 1 in progress
**Evidence scope:** Q1 2026 (`2026-01-01 <= published_date <= 2026-03-31`), layered onto the
completed Q4-and-earlier claim graphs
**Evidence cutoff:** 2026-03-31
**Owner:** current Codex session until a recorded handoff

This is the authoritative operating record for Q1 integration. Candidate membership is frozen in
`docs/records/2026-11-08-q1-2026-integration-manifest.json`; do not recompute or expand the set
informally after Phase 1 begins.

## Resume Here

1. Use the dedicated worktrees:
   - infrastructure: `speech-generation-wiki-infra-q1-integrate` at `7808b25`;
   - content: `speech-generation-wiki-content-q1-integrate` at `844fb57`.
2. Export the explicit content checkout:

   ```bash
   export SPEECH_WIKI_CONTENT_DIR=/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content-q1-integrate
   ```

3. Continue `subjective-evaluation` Phase 1 from the next frozen ID recorded below.
4. After every batch, validate the concept with `health_check.py --module integrate --phase 1`,
   compare actual IDs with the frozen batch, and record the result here.
5. Do not edit paper pages, the paper catalog, reconciliation state, snapshots, renders, or reports.

## Ownership and Parallel-Work Gate

Integration owns top-level `_claims/{concept}.yaml` files and integration entries in `log.md`.
Ingestion owns paper pages, metadata, the catalog, and ingest log entries. The content ingestion
worktree already contains the peer-reviewed-version release. The infrastructure ingestion worktree
has active uncommitted data and remains untouched; it must merge released `main` after that work is
secured. No ingestion-side change enters this frozen Q1 manifest ad hoc.

## Frozen Manifest

- Manifest: `docs/records/2026-11-08-q1-2026-integration-manifest.json`
- SHA-256: `db4bb694fa33f0f0f0e7cfcbe52e5cb0ac3e59a533dacb5ba159adf8c0aad4c0`
- Infrastructure start: `7808b25`
- Content start: `844fb57`
- Eligible paper pages: **116**
- Assigned paper pages: **115**
- Intentional unassigned pages: **1**
- Affected concepts: **22**
- Candidate memberships: **453**
- Already-present Q1 memberships: **0**
- Phase 1 queue memberships: **453**
- Active duplicate, Tier-2, or missing-page exclusions: **0**
- Manifest validation errors: **0**

Two independent generations were byte-identical. Candidate papers are ordered by canonical
`published_date`, then stable paper ID. The manifest records every paper and every per-concept ID
set, so exact closure is auditable without relying on aggregate counts.

### Intentional unassigned page

`2603.04145` (VietNormalizer) remains unassigned. Its page explicitly records that it is a
rule-based Vietnamese text-normalization library with no speech-generation, conditioning, or
evaluation mechanism meeting a tracked concept definition. It reports no quantitative
normalization, latency, or downstream synthesis evaluation. This is an intentional scope result,
not a missing integration membership.

### Concept queues

| Order | Concept | Candidates | Already | Phase 1 queue |
|---:|---|---:|---:|---:|
| 1 | subjective-evaluation | 52 | 0 | 52 |
| 2 | evaluation-metrics | 50 | 0 | 50 |
| 3 | zero-shot-tts | 41 | 0 | 41 |
| 4 | neural-codec | 36 | 0 | 36 |
| 5 | spoken-language-model | 34 | 0 | 34 |
| 6 | speech-to-speech | 30 | 0 | 30 |
| 7 | multilingual-tts | 24 | 0 | 24 |
| 8 | flow-matching | 23 | 0 | 23 |
| 9 | emotion-synthesis | 21 | 0 | 21 |
| 10 | self-supervised-speech | 17 | 0 | 17 |
| 11 | autoregressive-codec-tts | 16 | 0 | 16 |
| 12 | streaming-tts | 16 | 0 | 16 |
| 13 | voice-conversion | 15 | 0 | 15 |
| 14 | disentanglement | 14 | 0 | 14 |
| 15 | prosody-control | 13 | 0 | 13 |
| 16 | speaker-adaptation | 13 | 0 | 13 |
| 17 | instruction-conditioned-tts | 11 | 0 | 11 |
| 18 | gan-vocoder | 10 | 0 | 10 |
| 19 | rlhf-speech | 8 | 0 | 8 |
| 20 | diffusion-tts | 4 | 0 | 4 |
| 21 | singing | 3 | 0 | 3 |
| 22 | transformer-enc-dec-tts | 2 | 0 | 2 |
| **Total** |  | **453** | **0** | **453** |

## Reproduction Commands

```bash
python scripts/freeze_integration_manifest.py \
  --wiki-dir /Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content-q1-integrate \
  --quarter 2026-Q1 \
  --start 2026-01-01 \
  --end 2026-03-31 \
  --infra-commit 7808b25 \
  --content-commit 844fb57 \
  --output docs/records/2026-11-08-q1-2026-integration-manifest.json

python scripts/health_check.py \
  --wiki-dir /Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content-q1-integrate
```

## Phase 1 — Concept-Local Evidence

Process the concepts in the table order. Each invocation adds at most 20 new paper pages, preserves
all relevant page claims and limitations, and ends with an exact-ID comparison plus concept-scoped
Phase 1 validation. Phase 2 follows immediately after each concept's Phase 1 queue closes.

### subjective-evaluation

**Progress:** 52/52. Six invocations wrote all 52 entries; Phase 1 and Phase 2 are complete.

**Frozen queue prefix (first 20 IDs):**

1. `2601.01459`
2. `2601.04233`
3. `2601.02073`
4. `2601.02753`
5. `2601.02776`
6. `2601.01568`
7. `2601.05329`
8. `2601.05554`
9. `2505.15727`
10. `2602.06053`
11. `2601.12966`
12. `2601.13055`
13. `2602.11172`
14. `2601.10629`
15. `2601.14960`
16. `2601.17086`
17. `2601.13742`
18. `2601.18281`
19. `2601.22661`
20. `2026.iwsds-1.16`

**Invocation 1 — complete (1 ID):**

- Added `2601.01459` with all four page claims, canonical date `2026-01-04`, and
  concept-specific relevance, limitations, and caveats.
- `paper_count` advanced from 255 to 256; the ID occurs exactly once.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Next frozen ID: `2601.04233`.

**Invocation 2 — complete (4 IDs):**

- Added `2601.04233`, `2601.02073`, `2601.02753`, and `2601.02776` in frozen order.
- Preserved all 16 page claims with concept-specific relevance, limitations, and caveats.
- `paper_count` advanced from 256 to 260; all five Q1 IDs occur exactly once.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Next frozen ID: `2601.01568`.

**Invocation 3 — complete (4 IDs):**

- Added `2601.01568`, `2601.05329`, `2601.05554`, and `2505.15727` in frozen order.
- Preserved all 17 page claims with concept-specific relevance, limitations, and caveats.
- `paper_count` advanced from 260 to 264; all nine Q1 IDs occur exactly once.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Next frozen ID: `2602.06053`.

**Invocation 4 — complete (20 IDs):**

- Added `2602.06053`, `2601.12966`, `2601.13055`, `2602.11172`, `2601.10629`,
  `2601.14960`, `2601.17086`, `2601.13742`, `2601.18281`, `2601.22661`,
  `2026.iwsds-1.16`, `2026.iwsds-1.3`, `2602.03420`, `2602.09041`, `2601.05564`,
  `2602.04683`, `2602.11072`, `2602.11477`, `2602.13891`, and `2602.14664` in
  frozen order.
- Preserved all 89 page claims with concept-specific relevance, limitations, and caveats.
- `paper_count` advanced from 264 to 284; the integrated Q1 IDs equal the first 29 frozen queue
  IDs exactly, with no missing, extra, or duplicate IDs.
- Canonical peer-reviewed IDs in this batch remain `2026.iwsds-1.16` and `2026.iwsds-1.3`;
  no preprint aliases were added separately.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Next frozen ID: `2026.africanlp-main.23`. The remaining 23 entries fit in two invocations
  of 20 and 3 papers.

**Invocation 5 — complete (20 IDs):**

- Added the frozen range `2026.africanlp-main.23` through `2603.22252` in order.
- Preserved all 88 page claims with concept-specific relevance, limitations, and caveats.
- `paper_count` advanced from 284 to 304; the integrated Q1 IDs equal the first 49 frozen queue
  IDs exactly, with no missing, extra, or duplicate IDs.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Next frozen ID: `2603.23938`.

**Invocation 6 — complete (3 IDs; Phase 1 closure):**

- Added `2603.23938`, `2601.13802`, and `2604.01247` in frozen order.
- Preserved all 15 page claims with concept-specific relevance, limitations, and caveats.
- `paper_count` advanced from 304 to 307; the integrated Q1 IDs equal the complete 52-ID frozen
  queue exactly, with no missing, extra, or duplicate IDs.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Phase 1 is closed for `subjective-evaluation`; Phase 2 synthesis is the next operation.

**Phase 2 — complete:**

- Updated all 17 established claim clusters and added one strongly supported cluster:
  `conversational_evaluation_requires_interaction_context`.
- The new cluster captures the Q1 evidence that spoken-dialogue evaluation must retain multi-turn,
  dual-channel, turn-taking, and paralinguistic context rather than rely on single utterances or
  transcripts alone.
- Back-filled 57 reciprocal method-family memberships for 39 Q1 papers across all seven existing
  architecture families. Thirteen Q1 evaluation or benchmark papers have no architecture label and
  remain legitimate family outliers.
- Added two open questions and three Q1 trend notes covering conversational protocol design,
  deployment usability, structured automatic judges, and low-resource metric confounds.
- No reassessment items were open or triggered.
- Concept-scoped Phase 2 health: 0 errors and 74 expected method-family coverage warnings, all for
  architecture-unspecified papers across the full 307-paper concept history.
- Main-cluster summary written to the Git-ignored local Phase 2 summary log.
- No commit or push was made for the Phase 1 closure or Phase 2 work.

### evaluation-metrics

**Progress:** 50/50. Three invocations wrote all 50 entries; Phase 1 and Phase 2 are complete.

**Invocation 1 — complete (20 IDs):**

- Added the frozen range `2601.02073` through `2602.03420` in order, including the canonical
  peer-reviewed IWSDS IDs `2026.iwsds-1.10`, `2026.iwsds-1.16`, `2026.iwsds-1.4`, and
  `2026.iwsds-1.9` without separate preprint aliases.
- Preserved all 86 page claims with evaluation-specific relevance, limitations, and caveats.
- `paper_count` advanced from 346 to 366; the integrated Q1 IDs equal the first 20 frozen queue
  IDs exactly, with no missing, extra, or duplicate IDs.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Next frozen ID: `2601.05564`; 30 entries remain.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Invocation 2 — complete (20 IDs):**

- Added the frozen range `2601.05564` through `2603.05413` in order, including the canonical
  peer-reviewed IDs `2026.abjadnlp-1.6` and `2026.africanlp-main.23` without separate preprint
  aliases.
- Preserved all 87 page claims with evaluation-specific relevance, limitations, and caveats.
- `paper_count` advanced from 366 to 386; the integrated Q1 IDs equal the first 40 frozen queue
  IDs exactly, with no missing, extra, or duplicate IDs.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Next frozen ID: `2603.16483`; 10 entries remain.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Invocation 3 — complete (10 IDs; Phase 1 closure):**

- Added the final frozen range `2603.16483` through `2603.29339` in order.
- Preserved all 42 available page claims. `2603.29339` has an empty source-page Claims section and
  was retained as `claims: []` rather than receiving inferred claims.
- `paper_count` advanced from 386 to 396; the integrated Q1 IDs equal the complete 50-ID frozen
  queue exactly, with no missing, extra, or duplicate IDs.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Phase 1 is closed for `evaluation-metrics`; Phase 2 synthesis is the next operation.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Phase 2 — complete:**

- Updated 27 established claim clusters and added one strongly supported cluster:
  `conversational_evaluation_requires_real_multiturn_context`.
- The new cluster captures the Q1 evidence that conversational metrics require real multi-turn,
  multi-speaker, timing, overlap, and interruption context rather than single utterances,
  transcripts, or synthetically mixed dialogue alone.
- Back-filled 161 reciprocal evaluation-method-family memberships for 49 Q1 papers across 14 of
  the 17 existing method families. `2603.29339`, whose source Claims section is empty, is the sole
  Q1 family outlier.
- Added two open questions and three Q1 trend notes covering conversational benchmark calibration,
  evaluation leakage, structured automatic judges, and deployment-context validation.
- Checked all six reassessment items. None triggered; the full-duplex automatic-metrics item was
  updated to record that the new Q1 pipelines remain bespoke and do not meet its replication trigger.
- Concept-scoped Phase 2 health: 0 errors and 21 expected method-family coverage warnings across
  the full 396-paper concept history.
- Main-cluster summary appended to the Git-ignored local Phase 2 summary log.

### neural-codec

**Progress:** 36/36. Two invocations wrote all 36 entries; Phase 1 and Phase 2 are complete.

**Invocation 1 — complete (20 IDs):**

- Added the frozen range `2601.02776` through `2602.11072` in order, including the canonical
  peer-reviewed ID `2026.iwsds-1.4` without a separate preprint alias.
- Preserved all 81 available page claims. `2601.15621` has an empty source-page Claims section and
  was retained as `claims: []`.
- `paper_count` advanced from 240 to 260; the integrated Q1 IDs equal the first 20 frozen queue
  IDs exactly, with no missing, extra, or duplicate IDs.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Next frozen ID: `2602.10934`; 16 entries remain.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Invocation 2 — complete (16 IDs; Phase 1 closure):**

- Added the final frozen range `2602.10934` through `2603.26364` in order.
- Preserved all 58 available page claims. `2603.08823`, `2603.18090`, and `2603.26364` have empty
  source-page Claims sections and were retained as `claims: []`.
- `paper_count` advanced from 260 to 276; the integrated Q1 IDs equal the complete 36-ID frozen
  queue exactly, with no missing, extra, or duplicate IDs.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Phase 1 is closed for `neural-codec`; Phase 2 synthesis is the next operation.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Phase 2 — complete:**

- Updated all 18 established claim clusters; no new cluster was required because the Q1 evidence
  strengthens the existing rate, quantization, semantic-acoustic, robustness, and evaluation themes.
- Back-filled 74 reciprocal architecture-family memberships for 35 Q1 papers across all seven
  existing method families. `2602.00269`, an architecture-unspecified serving paper, remains the
  sole Q1 family outlier.
- Added two open questions and three Q1 trend notes covering variable and linguistically aligned
  token rates, privacy and speaker leakage, explicit semantic-acoustic factorization, and broader
  robustness evaluation.
- Checked all five reassessment items. None triggered; all five are overdue because Q1 did not
  provide the matched representation study, shared listener-calibrated benchmark, matched semantic
  integration comparisons, conventional-codec reproduction, or task-separated leakage study named
  by their triggers.
- Concept-scoped Phase 2 health: 0 errors and 22 expected method-family coverage warnings across
  the full 276-paper concept history.
- Main-cluster summary appended to the Git-ignored local Phase 2 summary log.

### spoken-language-model

**Progress:** 34/34. Two invocations wrote all 34 entries; Phase 1 and Phase 2 are complete.

**Invocation 1 — complete (20 IDs):**

- Added the frozen range `2505.15727` through `2602.13891` in order, including the canonical
  peer-reviewed IWSDS IDs `2026.iwsds-1.10`, `2026.iwsds-1.4`, and `2026.iwsds-1.9` without
  separate preprint aliases.
- Preserved all 86 page claims with concept-specific relevance, limitations, and caveats.
- `paper_count` advanced from 173 to 193; the integrated Q1 IDs equal the first 20 frozen queue
  IDs exactly, with no missing, extra, or duplicate IDs.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Next frozen ID: `2602.23068`; 14 entries remain.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Invocation 2 — complete (14 IDs; Phase 1 closure):**

- Added the final frozen range `2602.23068` through `2603.25750` in order.
- Preserved all 63 page claims with concept-specific relevance, limitations, and caveats.
- `paper_count` advanced from 193 to 207; the integrated Q1 IDs equal the complete 34-ID frozen
  queue exactly, with no missing, extra, or duplicate IDs.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Phase 1 is closed for `spoken-language-model`; Phase 2 synthesis is the next operation.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Phase 2 — complete:**

- Updated all 18 established claim clusters and added one emerging cluster:
  `explicit_reasoning_traces_improve_spoken_response_accuracy`.
- The new cluster captures the first direct Q1 evidence that generating an intermediate text reasoning
  trace alongside speech can improve spoken-answer accuracy, while retaining the synthetic-data and
  English-only limitations that keep the finding emerging.
- Assigned 25/34 Q1 papers to 56 reciprocal memberships across the seven existing method families and
  two new families: masked-diffusion speech language models and modular dialogue-state control models.
  Nine benchmark, evaluation, serving, or tutorial papers remain legitimate architecture-family outliers.
- The full-duplex family-boundary reassessment triggered: four Q1 systems form a stable explicit
  dialogue-state-control subgroup. The queue item now watches for matched unified-versus-modular
  comparisons and another stable subgroup.
- Added two open questions and three Q1 trend notes covering natural-data reasoning traces,
  unified-versus-modular turn control, architectural diversification, conversational data curation,
  and multidimensional interaction evaluation.
- Concept-scoped Phase 2 health: 0 errors and 48 expected method-family coverage warnings across the
  full 207-paper concept history, including the nine Q1 architecture-family outliers.
- Reciprocal family audit passed with 0 mismatches; main-cluster summary appended to the Git-ignored
  local Phase 2 summary log.

### speech-to-speech

**Progress:** 30/30. Two invocations wrote all 30 entries; Phase 1 and Phase 2 are complete.

**Invocation 1 — complete (20 IDs):**

- Added the frozen range `2505.15727` through `2603.07599` in order, including the canonical
  peer-reviewed IDs `2026.iwsds-1.10`, `2026.iwsds-1.16`, `2026.iwsds-1.4`, and
  `2026.loreslm-1.54` without separate preprint aliases.
- Preserved all 87 page claims with concept-specific relevance, limitations, and caveats.
- `paper_count` advanced from 94 to 114; the integrated Q1 IDs equal the first 20 frozen queue
  IDs exactly, with no missing, extra, or duplicate IDs.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Next frozen ID: `2603.09180`; 10 entries remain.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Invocation 2 — complete (10 IDs; Phase 1 closure):**

- Added the final frozen range `2603.09180` through `2603.25750` in order.
- Preserved all 44 page claims with concept-specific relevance, limitations, and caveats.
- `paper_count` advanced from 114 to 124; the integrated Q1 IDs equal the complete 30-ID frozen
  queue exactly, with no missing, extra, or duplicate IDs.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Phase 1 is closed for `speech-to-speech`; Phase 2 synthesis is the next operation.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Phase 2 — complete:**

- Updated 18 applicable established clusters; the retrieval/tool-use cluster received no Q1 evidence
  and remains unchanged.
- Added one strongly supported cluster:
  `conversational_data_structure_shapes_turn_taking_behavior`, backed by three independent Q1 papers
  on corpus interaction patterns, behavior-conditioned fine-tuning, and overlap-preserving preprocessing.
- Assigned 22/30 Q1 papers to 34 reciprocal memberships across the seven existing method families and
  two new families: masked-diffusion speech-to-speech models and explicit dialogue-state control agents.
  Eight benchmark, evaluation, or data-infrastructure papers remain legitimate family outliers.
- Audited all six reassessment items. None of their substantive triggers fired; three older items are
  overdue (`2412.15649`, `2025.naacl-long.484`, and `2025.iwsds-1.27`) because their canonical-ID or
  concept-scope decisions remain unresolved.
- Added two open questions and three Q1 trend notes covering conversational-data preservation, explicit
  versus implicit dialogue-state control, semantic triggering, and long-form simultaneous translation.
- Concept-scoped Phase 2 health: 0 errors and 36 expected method-family coverage warnings across the
  full 124-paper concept history, including the eight Q1 family outliers.
- Reciprocal family audit passed with 0 mismatches; main-cluster summary appended to the Git-ignored
  local Phase 2 summary log.

### multilingual-tts

**Progress:** 24/24. Two invocations wrote all 24 entries; Phase 1 and Phase 2 are complete.

**Invocation 1 — complete (20 IDs):**

- Added the frozen range `2601.04233` through `2602.09823` in order, including canonical
  peer-reviewed IDs `2026.abjadnlp-1.6`, `2026.eacl-short.16`, and `2026.loreslm-1.54`
  without separate preprint aliases.
- Preserved all 75 available page claims. `2601.03888`, `2601.15621`, and `2603.08823` have
  empty source-page Claims sections and were retained as `claims: []`.
- `paper_count` advanced from 105 to 125; the integrated Q1 IDs equal the first 20 frozen queue
  IDs exactly, with no missing, extra, or duplicate IDs.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Next frozen ID: `2603.14853`; four entries remain.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Invocation 2 — complete (4 IDs; Phase 1 closure):**

- Added the final frozen range `2603.14853` through `2603.29339` in order.
- Preserved all nine available page claims. `2603.18090` and `2603.29339` have empty source-page
  Claims sections and were retained as `claims: []`.
- `paper_count` advanced from 125 to 129; the integrated Q1 IDs equal the complete 24-ID frozen
  queue exactly, with no missing, extra, or duplicate IDs.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Phase 1 is closed for `multilingual-tts`; Phase 2 synthesis is the next operation.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Phase 2 — complete:**

- Updated 16 applicable established clusters; code-switching, parameter-efficient extension, and
  synthetic-parallel-data clusters received no qualifying Q1 evidence and remain unchanged.
- Added one emerging cluster: `accent_control_without_accented_training_data_is_feasible`, backed by
  two Q1 approaches using parameter-space accent vectors and phonological rules.
- Assigned 22/24 Q1 papers to 46 reciprocal memberships across all seven existing architecture
  families. Two architecture-unspecified application papers remain legitimate family outliers.
- Audited all eight reassessment items. None triggered; five October 2026 items are overdue because
  Q1 did not provide the matched, balanced, or cross-family studies named in their triggers.
- Added two open questions and three Q1 trend notes covering training-free accent control,
  script-aware extension, low-resource adaptation, evaluation bias, and expanding cross-lingual tasks.
- Concept-scoped Phase 2 health: 0 errors and 12 expected method-family coverage warnings across the
  full 129-paper concept history, including the two Q1 architecture-family outliers.
- Reciprocal family audit passed with 0 mismatches; main-cluster summary appended to the Git-ignored
  local Phase 2 summary log.

### flow-matching

**Progress:** 23/23. Two invocations wrote all 23 entries; Phase 1 and Phase 2 are complete.

**Invocation 1 — complete (20 IDs):**

- Added the frozen range `2601.00303` through `2603.16280` in order.
- Preserved all 83 available page claims. `2601.03888` has an empty source-page Claims section
  and was retained as `claims: []`.
- `paper_count` advanced from 125 to 145; the integrated Q1 IDs equal the first 20 frozen queue
  IDs exactly, with no missing, extra, or duplicate IDs.
- A first validation caught and corrected list indentation for this file's indented `papers:` style;
  the corrected concept-scoped Phase 1 health check passed with 0 errors and 0 warnings.
- Next frozen ID: `2603.16783`; three entries remain.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Invocation 2 — complete (3 IDs; Phase 1 closure):**

- Added `2603.16783`, `2601.13802`, and `2603.29339` in frozen order.
- Preserved all nine available page claims. `2603.29339` has an empty source-page Claims section
  and was retained as `claims: []`.
- `paper_count` advanced from 145 to 148; the integrated Q1 IDs equal the complete 23-ID frozen
  queue exactly, with no missing, extra, or duplicate IDs.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Phase 1 is closed for `flow-matching`; Phase 2 synthesis is the next operation.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Phase 2 — complete:**

- Updated 15 applicable established clusters and added four emerging clusters covering disentangled
  counterfactual speech, joint audio-visual generation, density-path-conditioned speech editing, and
  codec-latent bandwidth extension. Twenty established clusters received no qualifying Q1 evidence.
- The classifier-free-guidance reassessment triggered. Two independent Q1 papers confirmed that naive
  transfer is insufficient; the cluster was narrowed and changed from contested to strongly supported,
  and the completed queue item was removed.
- Assigned all 23 Q1 papers to 28 reciprocal memberships across five of the seven established method
  families. No Q1 paper remains a family outlier; the historical-guidance and auxiliary-attribute
  families received no new members.
- Audited all three reassessment items: one triggered, none are overdue after the completed item was
  resolved, and two remain open for future continuous-AR and discrete-space-flow evidence.
- Added two open questions and three Q1 trend notes covering guidance portability, new application
  domains, one-step training strategies, and the resolved CFG consensus.
- Concept-scoped Phase 2 health: 0 errors and six expected historical method-family coverage warnings
  across the full 148-paper concept history.
- Reciprocal family audit passed with 0 mismatches; main-cluster summary appended to the Git-ignored
  local Phase 2 summary log.

### autoregressive-codec-tts

**Progress:** 16/16. One invocation wrote all 16 entries; Phase 1 is complete and Phase 2 has not started.

**Invocation 1 — complete (16 IDs; Phase 1 closure):**

- Added the complete frozen range `2601.03888` through `2603.26364` in order.
- Preserved all 50 available page claims. `2601.03888`, `2601.15621`, `2603.08823`,
  `2603.18090`, and `2603.26364` have empty source-page Claims sections and were retained as
  `claims: []`.
- `paper_count` advanced from 196 to 212; the integrated Q1 IDs equal the complete 16-ID frozen
  queue exactly, with no missing, extra, or duplicate IDs.
- Used the canonical peer-reviewed AbjadNLP ID `2026.abjadnlp-1.6` without adding a duplicate
  preprint alias.
- Initial validation caught this older file's indented `papers:` list format; the inserted block was
  normalized to match it before closure.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Phase 1 is closed for `autoregressive-codec-tts`; Phase 2 synthesis is the next operation.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Phase 2 — complete:**

- Updated 13 established clusters and added one strongly supported cluster covering post-hoc null-space
  weight editing and activation steering for pronunciation, emotion, and accent control. Six established
  clusters received no qualifying Q1 evidence and remain unchanged.
- Assigned all 16 Q1 papers to 34 reciprocal memberships across eight of the 14 established method families;
  no Q1 paper remains a family outlier.
- Audited all six reassessment items. None triggered and none is overdue; Q1 did not provide the matched
  architecture, renderer, grouped-decoding, or end-to-end efficiency comparisons named in their triggers.
- Added two open questions and three Q1 trend notes covering intervention composition, full inference-cost
  reporting, variable-depth codecs, data diversity, and perceptual checkpoint selection.
- Concept-scoped Phase 2 health: 0 errors and one expected historical method-family coverage warning across
  the full 212-paper concept history.
- Reciprocal family audit passed with 0 mismatches; main-cluster summary appended to the Git-ignored local
  Phase 2 summary log.

### self-supervised-speech

**Progress:** 17/17. One invocation wrote all 17 entries; Phase 1 is complete and Phase 2 has not started.

**Invocation 1 — complete (17 IDs; Phase 1 closure):**

- Added the complete frozen range `2601.09239` through `2602.23765` in order.
- Preserved all 74 available page claims.
- `paper_count` advanced from 176 to 193; the integrated Q1 IDs equal the complete 17-ID frozen
  queue exactly, with no missing, extra, or duplicate IDs.
- Used the canonical peer-reviewed LoResLM ID `2026.loreslm-1.54` without adding a duplicate
  preprint alias.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Phase 1 is closed for `self-supervised-speech`; Phase 2 synthesis is the next operation.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Phase 2 — complete:**

- Updated 16 established clusters; masked and contrastive pretraining received no qualifying Q1 evidence and
  remains unchanged. No new cluster was needed because the Q1 findings refine established representation,
  hierarchy, adaptation, codec, and evaluation claims.
- The automatic-judge reassessment triggered. Listener-calibrated Q1 studies distinguish task-trained SSL
  predictors from general-purpose or out-of-domain judges; the claim was narrowed and changed from contested
  to strongly supported, and the completed queue item was removed.
- Assigned all 17 Q1 papers to 30 reciprocal memberships across all seven established method families; no Q1
  paper remains a family outlier.
- Audited all five reassessment items: one triggered and four remain overdue for matched continuous/discrete,
  scaling, hybrid-family, or task-conditioned leakage evidence.
- Added two open questions and three Q1 trend notes covering semantic-supervision placement, evaluator
  calibration, frozen-backbone reuse, and representation interfaces.
- Concept-scoped Phase 2 health: 0 errors and 19 expected historical method-family coverage warnings across
  the full 193-paper concept history.
- Reciprocal family audit passed with 0 mismatches; main-cluster summary appended to the Git-ignored local
  Phase 2 summary log.

### emotion-synthesis

**Progress:** 20/21. One Phase 1 invocation has written the first 20 entries; Phase 2 has not started.

**Invocation 1 — complete (20 IDs):**

- Added the frozen range `2601.03888` through `2603.17231` in order.
- Preserved all 86 available page claims. `2601.03888` has an empty source-page Claims section
  and was retained as `claims: []`.
- `paper_count` advanced from 98 to 118; the integrated Q1 IDs equal the first 20 frozen queue
  IDs exactly, with no missing, extra, or duplicate IDs.
- Used the canonical peer-reviewed AAAI venue metadata for `2601.12289` while retaining the page's
  explicit boundary that its claims summarize the ingested version.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Next frozen ID: `2603.22252`; one entry remains.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Invocation 2 — complete (1 ID; Phase 1 closure):**

- Added `2603.22252` with all four page claims.
- `paper_count` advanced from 118 to 119; the integrated Q1 IDs equal the complete 21-ID frozen
  queue exactly, with no missing, extra, or duplicate IDs.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Phase 1 is closed for `emotion-synthesis`; Phase 2 synthesis is the next operation.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Phase 2 — complete:**

- Updated 15 applicable established clusters and added two emerging clusters covering training-free
  internal-representation steering and the human-to-synthetic emotional-speech domain gap. Fine-grained
  temporal conditioning and cross-lingual transfer received no qualifying Q1 evidence and remain unchanged.
- Assigned 14/21 Q1 papers to 28 reciprocal memberships across five of the seven established method
  families. Seven architecture-unspecified evaluation, dialogue, or representation papers remain legitimate
  family outliers.
- Audited all four reassessment items. None triggered; all four October 2026 items remain overdue because
  Q1 did not provide the matched multilingual, control-strength, or factorial listener studies named in
  their triggers.
- Added two open questions and three Q1 trend notes covering internal steering transfer, reward hacking,
  causal disentanglement, and synthetic-emotion domain shift.
- Concept-scoped Phase 2 health: 0 errors and 23 expected method-family coverage warnings across the full
  119-paper concept history, including the seven Q1 architecture-family outliers.
- Reciprocal family audit passed with 0 mismatches; main-cluster summary appended to the Git-ignored local
  Phase 2 summary log.

### zero-shot-tts

**Progress:** 41/41. Three invocations wrote all 41 entries; Phase 1 and Phase 2 are complete.

**Invocation 1 — complete (20 IDs):**

- Added the frozen range `2601.04233` through `2602.04683` in order.
- Preserved all 76 available page claims. `2601.03888` and `2601.15621` have empty source-page
  Claims sections and were retained as `claims: []`.
- `paper_count` advanced from 262 to 282; the integrated Q1 IDs equal the first 20 frozen queue
  IDs exactly, with no missing, extra, or duplicate IDs.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Next frozen ID: `2602.10735`; 21 entries remain.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Invocation 2 — complete (20 IDs):**

- Added the frozen range `2602.10735` through `2603.29339` in order, including the canonical
  peer-reviewed ID `2026.abjadnlp-1.6` without a separate preprint alias.
- Preserved all 71 available page claims. `2603.08823`, `2603.18090`, `2603.26364`, and
  `2603.29339` have empty source-page Claims sections and were retained as `claims: []`.
- `paper_count` advanced from 282 to 302; the integrated Q1 IDs equal the first 40 frozen queue
  IDs exactly, with no missing, extra, or duplicate IDs.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Next frozen ID: `2604.01247`; one entry remains.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Invocation 3 — complete (1 ID; Phase 1 closure):**

- Added `2604.01247` with all five page claims.
- `paper_count` advanced from 302 to 303; the integrated Q1 IDs equal the complete 41-ID frozen
  queue exactly, with no missing, extra, or duplicate IDs.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Phase 1 is closed for `zero-shot-tts`; Phase 2 synthesis is the next operation.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Phase 2 — complete:**

- Updated 19 established claim clusters and added one strongly supported cluster:
  `training_free_steering_enables_posthoc_identity_and_accent_control`.
- The new cluster captures Q1 evidence that activation or parameter steering can alter accent or
  suppress speaker identity without retraining the base model, while exposing linguistic-fidelity
  and correlated-attribute trade-offs.
- Assigned all 41 Q1 papers to reciprocal architecture families across six of the nine existing
  method families; no Q1 paper remains a family outlier.
- Added two open questions and three Q1 trend notes covering privacy safeguards, steering transfer,
  low-resource and cross-lingual cloning, and expansion beyond short-form timbre copying.
- No reassessment items were open or triggered.
- Concept-scoped Phase 2 health: 0 errors and 24 expected method-family coverage warnings, all from
  earlier papers in the full 303-paper concept history.
- Main-cluster summary appended to the Git-ignored local Phase 2 summary log.

## Preflight Validation

- [x] Peer-reviewed-version Q1 migration released on both main branches.
- [x] Dedicated worktrees created from released main commits.
- [x] Metadata/page dates agree for every eligible page.
- [x] Every eligible page has exactly one paper-index row.
- [x] Duplicate pointers and Tier-2 pages audited.
- [x] `related_concepts` values resolve to canonical top-level claim YAMLs.
- [x] Intentional unassigned page reviewed and justified.
- [x] Deterministic manifest generated twice with identical bytes.
- [x] Full health suite rerun from the dedicated worktrees: 54 tests and all six modules pass with
      zero errors.
- [x] Bootstrap tooling and record committed as `85a2a49` before the first claim write.
