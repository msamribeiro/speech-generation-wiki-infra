# Q1 2026 Integration and Synthesis Session

**Started:** 2026-11-08
**Status:** Local closeout checked. Content, infrastructure, and site release pending.
**Evidence scope:** Q1 2026 (`2026-01-01 <= published_date <= 2026-03-31`), layered onto the
completed Q4-and-earlier claim graphs
**Evidence cutoff:** 2026-03-31
**Owner:** current Codex session until a recorded handoff

This is the authoritative operating record for Q1 integration. Candidate membership is frozen in
`docs/records/2026-11-08-q1-2026-integration-manifest.json`; do not recompute or expand the set
informally after Phase 1 begins.

## Resume Here

1. Use the dedicated Q1 integration worktrees:
   - infrastructure: `speech-generation-wiki-infra-q1-integrate`;
   - content: `speech-generation-wiki-content-q1-integrate`, with snapshot and report at `2d6cd33`.
2. Export the explicit content checkout:

   ```bash
   export SPEECH_WIKI_CONTENT_DIR=/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content-q1-integrate
   ```

3. Phase 1 is closed at 453/453 frozen memberships across all 22 concepts; all 22 concepts are complete through Phase 2.
4. Reconciliation is finalized at 919 accepted, 4,395 rejected, and zero pending.
5. The 23 concept pairs and field overview are current. The published Q1 snapshot and quarterly
   report are validated on the content integration branch.
6. Follow `docs/integration-protocol.md` section 9 for the release and validate the merged content
   before deploying.

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

## Integration Closeout Audit

- Exact frozen-manifest closure: 453/453 memberships across 22/22 concepts, with no missing, extra, duplicate, or out-of-order IDs.
- Corpus-wide integration health: 0 errors and 366 accepted method-family coverage warnings across 3,345 paper entries and 464 clusters.
- Reciprocal method-family audit: 0 mismatches across all 23 concept graphs.
- Initial cluster-coverage audit found one earlier omission: multilingual streaming paper `2603.16924` had high/medium evidence but no cluster reference. It was added as refining evidence to `duration_and_alignment_are_language_sensitive`.
- Corrected high/medium-relevance cluster coverage: 0 uncovered Q1 papers.
- Forty-two Q1 family outliers remain intentional evaluation, benchmark, architecture-unspecified, or peripheral-system records already accepted in their per-concept Phase 2 summaries.
- This audit recorded the end of the concept-local integration stage.

## Local Closeout Checkpoint

- The live Q1 concept memberships exactly match all 453 manifest entries across 22 concepts,
  including their order. The snapshot contains the same 115 Q1 papers.
- Verified 1,061 unique paper pages, one catalog row per page, and matching homepage counts.
- Finalized reconciliation and refreshed the concept renderings and field overview. The immutable
  snapshot uses content checkpoint `7d721e0` and infrastructure checkpoint `af8eb5e`.
- The snapshot reproduced byte for byte after publication. The repository report validator passed
  against the snapshot, report index, and changelog.
- All 54 tests and all six health modules passed with zero errors. The render and agent modules
  had zero warnings. The remaining modules report non-blocking corpus and historical warnings.
- Local closeout covers the two integration branches. Merge, push, site deployment, and branch
  cleanup are release steps.

### Release merge and the MOSS publication date

The ingestion worktree re-dated MOSS-Audio-Tokenizer (`2602.10934`) to July 6, 2026, when it
recorded the ICML version. The Q1 integration worktree had already assigned the summarized arXiv
v2 to five canonical claim graphs with the February 12, 2026 date. The release merge applies the
claim-membership freeze once across metadata, the paper page, and the catalog. It records ICML
2026 and its link as later publication metadata. The frozen Q1 snapshot and its source claims
retain the original date.

## Phase 1 — Concept-Local Evidence

Process the concepts in the table order. Each invocation adds at most 20 new paper pages, preserves
all relevant page claims and limitations, and ends with an exact-ID comparison plus concept-scoped
Phase 1 validation. Phase 2 follows immediately after each concept's Phase 1 queue closes.

### gan-vocoder

**Progress:** 10/10. One invocation wrote all 10 entries; Phase 1 and Phase 2 are complete.

**Invocation 1 — complete (10 IDs; Phase 1 closure):**

- Added the complete frozen queue and preserved all 42 source-page claims.
- `paper_count` advanced from 82 to 92; exact queue closure passed with no missing, extra, or duplicate IDs.
- Retained canonical peer-reviewed AAAI metadata for `2601.13758` while keeping evidence bounded to the ingested paper page.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings. No commit or push was made.

**Phase 2 — complete:**

- Updated 12 established clusters; no new cluster or status transition was needed.
- Assigned all 10 Q1 papers to 22 reciprocal memberships across all seven method families and repaired one historical reciprocal membership.
- Audited all five reassessment items. None triggered and all five remain overdue.
- Added two open questions and three Q1 trend notes covering configuration generalization, metric calibration, structured inverse modeling, codec decoders, and metric disagreement.
- Phase 2 health: 0 errors and three expected historical family warnings; reciprocal audit: 0 mismatches.
- Main-cluster summary appended to the Git-ignored local Phase 2 summary log.

### rlhf-speech

**Progress:** 8/8. One invocation wrote all eight entries; Phase 1 and Phase 2 are complete.

**Invocation 1 — complete (8 IDs; Phase 1 closure):**

- Added the complete frozen queue and preserved all 38 source-page claims across structured and legacy claim formats.
- `paper_count` advanced from 49 to 57; exact queue closure passed with no missing, extra, or duplicate IDs.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings. No commit or push was made.

**Phase 2 — complete:**

- Updated 11 established clusters; no new cluster or status transition was needed.
- Assigned all eight Q1 papers to 13 reciprocal memberships across all six method families.
- Audited both reassessment items. Neither triggered and neither is overdue.
- Added two open questions and three Q1 trend notes covering reward balancing, judge calibration, generative reward models, and expansion into dialogue and simultaneous translation.
- Phase 2 health: 0 errors and five expected historical family warnings; reciprocal audit: 0 mismatches.
- Main-cluster summary appended to the Git-ignored local Phase 2 summary log.

### diffusion-tts

**Progress:** 4/4. One invocation wrote all four entries; Phase 1 and Phase 2 are complete.

**Invocation 1 — complete (4 IDs; Phase 1 closure):**

- Added the complete frozen queue and preserved all 20 source-page claims across structured and legacy claim formats.
- `paper_count` advanced from 58 to 62; exact queue closure passed with no missing, extra, or duplicate IDs.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings. No commit or push was made.

**Phase 2 — complete:**

- Updated 14 established clusters, promoted masked discrete diffusion from emerging to strongly supported, and added one emerging bidirectional speech-editing cluster.
- Assigned all four Q1 papers to five reciprocal memberships across four method families.
- No reassessment items were present.
- Added two open questions and three Q1 trend notes covering editing, representation complexity, waveform latents, masked diffusion, and prosody encoders.
- Phase 2 health: 0 errors and seven expected historical family warnings; reciprocal audit: 0 mismatches.
- Main-cluster summary appended to the Git-ignored local Phase 2 summary log.

### singing

**Progress:** 3/3. One invocation wrote all three entries; Phase 1 and Phase 2 are complete.

**Invocation 1 — complete (3 IDs; Phase 1 closure):**

- Added the complete frozen queue and preserved all 13 source-page claims.
- `paper_count` advanced from 21 to 24; exact queue closure passed with no missing, extra, or duplicate IDs.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings. No commit or push was made.

**Phase 2 — complete:**

- Updated seven established clusters and added one emerging cluster for latent-distribution alignment in cVAE singing synthesis.
- Assigned all three Q1 papers to six reciprocal memberships across four method families.
- Audited all five reassessment items. None triggered; all remain due in November 2026.
- Added two open questions and three Q1 trend notes covering latent transport, scale attribution, factorized control, and unified audio-language models.
- Phase 2 health: 0 errors and three expected historical family warnings; reciprocal audit: 0 mismatches.
- Main-cluster summary appended to the Git-ignored local Phase 2 summary log.

### transformer-enc-dec-tts

**Progress:** 2/2. One invocation wrote both entries; Phase 1 and Phase 2 are complete.

**Invocation 1 — complete (2 IDs; Phase 1 closure):**

- Added the complete frozen queue and preserved all eight source-page claims.
- `paper_count` advanced from 33 to 35; exact queue closure passed with no missing, extra, or duplicate IDs.
- Q1 Phase 1 reached 453/453 frozen memberships across all 22 concepts.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings. No commit or push was made.

**Phase 2 — complete:**

- Updated three established clusters and added one emerging cluster for segmental-prosody lexical generalization failure.
- Assigned both Q1 papers to reciprocal membership in the transformer encoder–decoder family.
- Audited all five reassessment items. None triggered and all five remain overdue.
- Added two open questions and three Q1 trend notes covering causal mediation, voice-quality cues, phonetic probes, and aggregate-metric blind spots.
- Phase 2 health: 0 errors and one expected historical family warning; reciprocal audit: 0 mismatches.
- Main-cluster summary appended to the Git-ignored local Phase 2 summary log.

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

### instruction-conditioned-tts

**Progress:** 11/11. One invocation wrote all 11 entries; Phase 1 is complete and Phase 2 has not started.

**Invocation 1 — complete (11 IDs; Phase 1 closure):**

- Added the complete frozen range `2601.01459` through `2603.17231` and preserved 39 claims.
- `2601.15621` and `2603.08823` have empty source Claims sections and remain `claims: []`.
- `paper_count` advanced from 57 to 68; exact queue closure passed.
- Retained peer-reviewed AAAI metadata with ParaMETA's ingested-version evidence boundary.
- Phase 1 health: 0 errors, 0 warnings. No commit or push was made.

**Phase 2 — complete:**

- Updated 16 established clusters; demographic-bias amplification received no qualifying Q1 evidence and remains unchanged. No new cluster was needed.
- Assigned all 11 Q1 papers to 34 reciprocal memberships across all nine method families.
- Audited all four reassessment items. None triggered and all four remain overdue.
- Added two open questions and three Q1 trend notes covering ambiguity, reward alignment, staged interpretation and rendering, and internal interventions.
- Phase 2 health: 0 errors and two expected historical family warnings; reciprocal audit: 0 mismatches.
- Main-cluster summary appended to the Git-ignored local Phase 2 summary log.

### speaker-adaptation

**Progress:** 13/13. One invocation wrote all 13 entries; Phase 1 is complete and Phase 2 has not started.

**Invocation 1 — complete (13 IDs; Phase 1 closure):**

- Added the complete frozen range `2506.12537` through `2603.16280` in order and preserved all 57 claims.
- `paper_count` advanced from 98 to 111; exact queue closure passed with no missing, extra, or duplicate IDs.
- Used canonical peer-reviewed EACL metadata without a duplicate preprint entry.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Phase 2 — complete:**

- Updated 18 established clusters; personalized assistive voices received no qualifying Q1 evidence and remains unchanged. No new cluster was needed.
- Assigned all 13 Q1 papers to 25 reciprocal memberships across all seven method families.
- Audited all five reassessment items. None triggered and all five remain overdue.
- Added two open questions and three Q1 trend notes on data diversity, representation placement, privacy, and expanding adaptation domains.
- Phase 2 health: 0 errors and 11 expected historical family warnings; reciprocal audit: 0 mismatches.
- Main-cluster summary appended to the Git-ignored local Phase 2 summary log.

### prosody-control

**Progress:** 13/13. One invocation wrote all 13 entries; Phase 1 is complete and Phase 2 has not started.

**Invocation 1 — complete (13 IDs; Phase 1 closure):**

- Added the complete frozen range `2601.04233` through `2603.21078` in order.
- Preserved all 51 available page claims. `2603.18090` has an empty source-page Claims section and
  was retained as `claims: []`.
- `paper_count` advanced from 115 to 128; the integrated Q1 IDs equal the complete 13-ID frozen
  queue exactly, with no missing, extra, or duplicate IDs.
- Used the canonical peer-reviewed IWSDS ID `2026.iwsds-1.3` without adding a duplicate preprint alias.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Phase 1 is closed for `prosody-control`; Phase 2 synthesis is the next operation.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Phase 2 — complete:**

- Updated 16 established clusters and added one emerging cluster covering segmental prosodic rules that fail
  to generalize from familiar to unseen lexical items. Stochastic modeling, scale-driven implicit prosody, and
  reward-guided post-training received no qualifying Q1 evidence and remain unchanged.
- Assigned all 13 Q1 papers to 48 reciprocal memberships across 14 of the 15 method families; no Q1 paper
  remains a family outlier. Reward-optimized prosody received no Q1 member.
- Audited all seven reassessment items. None triggered; all seven remain overdue because Q1 did not provide
  the matched frontier, metric-correlation, interface, SSL-layer, prompt-leakage, or stable family-subdivision
  studies named in their triggers.
- Added two open questions and three Q1 trend notes covering segmental diagnostics, cross-modal timing,
  causal mediators, rule-based accent rhythm, and cross-attribute interference.
- Concept-scoped Phase 2 health: 0 errors and 13 expected historical method-family coverage warnings across
  the full 128-paper concept history.
- Reciprocal family audit passed with 0 mismatches; main-cluster summary appended to the Git-ignored local
  Phase 2 summary log.

### disentanglement

**Progress:** 14/14. One invocation wrote all 14 entries; Phase 1 is complete and Phase 2 has not started.

**Invocation 1 — complete (14 IDs; Phase 1 closure):**

- Added the complete frozen range `2601.00303` through `2604.01247` in order.
- Preserved all 59 available page claims.
- `paper_count` advanced from 116 to 130; the integrated Q1 IDs equal the complete 14-ID frozen
  queue exactly, with no missing, extra, or duplicate IDs.
- Used canonical peer-reviewed AAAI and EACL metadata without duplicate preprint entries while retaining
  ParaMETA's explicit boundary that its claims summarize the ingested version.
- Initial validation caught this older file's indented `papers:` list format; the inserted block was
  normalized to match it before closure.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Phase 1 is closed for `disentanglement`; Phase 2 synthesis is the next operation.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Phase 2 — complete:**

- Updated all 19 established clusters and added one strongly supported cluster covering causal, null-space,
  and activation-subspace interventions for post-hoc attribute control.
- The GRL reassessment triggered. Q1 clean ablations show that correctly targeted gradient reversal can reduce
  leakage without an inherent quality penalty; the claim was narrowed, changed from contested to strongly
  supported, and the completed queue item was removed.
- Assigned all 14 Q1 papers to 34 reciprocal memberships across nine of the ten method families; no Q1 paper
  remains a family outlier. Mutual-information minimization received no qualifying Q1 member.
- Audited all five reassessment items: one triggered, two October 2026 items remain overdue, and two January
  2027 items are not yet due.
- Added two open questions and three Q1 trend notes covering transferable causal subspaces, meaningful versus
  spurious coupling, GRL placement, and compositional evaluation.
- Concept-scoped Phase 2 health: 0 errors and 16 expected historical method-family coverage warnings across
  the full 130-paper concept history.
- Reciprocal family audit passed with 0 mismatches; main-cluster summary appended to the Git-ignored local
  Phase 2 summary log.

### voice-conversion

**Progress:** 15/15. One invocation wrote all 15 entries; Phase 1 is complete and Phase 2 has not started.

**Invocation 1 — complete (15 IDs; Phase 1 closure):**

- Added the complete frozen range `2601.01568` through `2603.22252` in order.
- Preserved all 64 available page claims, including four newly structured claims from `2602.14686`
  on pitch–creak disentanglement and identity preservation.
- `paper_count` advanced from 117 to 132; the integrated Q1 IDs equal the complete 15-ID frozen
  queue exactly, with no missing, extra, or duplicate IDs.
- Used the canonical peer-reviewed EACL ID `2026.eacl-short.16` without adding a duplicate preprint alias.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Phase 1 is closed for `voice-conversion`; Phase 2 synthesis is the next operation.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Phase 2 — complete:**

- Updated 17 established clusters and added one strongly supported cluster covering correlations among
  speaker identity, accent, pitch, creak, and emotion. Non-parallel training and generated-speaker embedding
  clusters received no qualifying Q1 evidence and remain unchanged.
- Assigned 14/15 Q1 papers to 25 reciprocal memberships across all seven method families. Architecture-
  unspecified robustness benchmark `2602.00443` remains the sole Q1 family outlier.
- Audited all five reassessment items. None triggered; all five remain overdue because Q1 did not provide
  the matched listener, balanced multilingual, stable family-split, or cross-domain adaptive-attacker studies
  named in their triggers.
- Added two open questions and three Q1 trend notes covering spurious versus meaningful attribute coupling,
  listener-calibrated evaluation, internal steering, and expanding deployment domains.
- Concept-scoped Phase 2 health: 0 errors and 15 expected method-family coverage warnings across the full
  132-paper concept history, including the one Q1 architecture-family outlier.
- Reciprocal family audit passed with 0 mismatches; main-cluster summary appended to the Git-ignored local
  Phase 2 summary log.

### streaming-tts

**Progress:** 16/16. One invocation wrote all 16 entries; Phase 1 is complete and Phase 2 has not started.

**Invocation 1 — complete (16 IDs; Phase 1 closure):**

- Added the complete frozen range `2601.11141` through `2603.18090` in order.
- Preserved all 54 available page claims. `2601.15621`, `2603.08823`, and `2603.18090`
  have empty source-page Claims sections and were retained as `claims: []`.
- `paper_count` advanced from 75 to 91; the integrated Q1 IDs equal the complete 16-ID frozen
  queue exactly, with no missing, extra, or duplicate IDs.
- Used the canonical peer-reviewed IWSDS ID `2026.iwsds-1.10` without adding a duplicate preprint alias.
- Concept-scoped Phase 1 health: 0 errors, 0 warnings.
- Phase 1 is closed for `streaming-tts`; Phase 2 synthesis is the next operation.
- No commit or push was made; this concept will be committed only after Phase 2 is complete.

**Phase 2 — complete:**

- Updated 15 established clusters and added one strongly supported cluster covering modular streaming policies
  that add low-latency or full-duplex behavior without retraining the core speech backbone. Four established
  clusters received no qualifying Q1 evidence and remain unchanged.
- Assigned all 16 Q1 papers to 27 reciprocal memberships across four of the five established method families;
  no Q1 paper remains a family outlier. The flow-matching family received no qualifying Q1 member.
- Audited all five reassessment items. None triggered; all five remain overdue because Q1 did not provide the
  matched hardware, codec-listening, duplex-definition, or one-step continuous-generator studies named in
  their triggers.
- Added two open questions and three Q1 trend notes covering modular-policy transfer, deadline-aware serving,
  backend coordination, long-form input, and language-sensitive chunks.
- Concept-scoped Phase 2 health: 0 errors and three expected historical method-family coverage warnings across
  the full 91-paper concept history.
- Reciprocal family audit passed with 0 mismatches; main-cluster summary appended to the Git-ignored local
  Phase 2 summary log.

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

## Reconciliation

Candidate generation produced 5,314 deterministic shared-evidence candidates across eight themes.
Human review began with evaluation. Through bundle 15, evaluation is complete at 146 accepted and
869 rejected candidates with zero pending. Codecs/language-modeling bundle 1 then reaffirmed 101
Q4 human-approved decisions and resolved three newly emitted pairs through existing human-approved
broader claims. The codec theme now has 104 accepted and 1,170 pending candidates; the full run has
250 accepted, 869 rejected, and 4,195 pending candidates. Reconciliation validation passes with zero
errors and two expected warnings.

Codecs/language-modeling bundle 2 accepted 15 newly emitted representation and generation-interface
pairs: seven unified codec, SSL, and language-model links, six semantic-acoustic organization links,
and two modular-generation or leakage-control links. Fourteen were recorded as conservative `related`
relationships and the early-RVQ semantic-layer result as a narrower `specialization`. The codec theme
now has 119 accepted and 1,155 pending candidates; the full run has 265 accepted, 869 rejected, and
4,180 pending candidates. The registry contains 424 direct relationships and 11 broader claims, and
reconciliation validation continues to pass with zero errors and two expected warnings.

Codecs/language-modeling bundle 3 accepted 14 newly emitted transfer, reconstruction, and deployment
pairs: five cross-task token-interface and transfer links, five token-rate and streaming-cost links,
and four robustness or reconstruction links. Twelve were recorded as conservative `related`
relationships and two as `supports` relationships. The codec theme now has 133 accepted and 1,141
pending candidates; the full run has 279 accepted, 869 rejected, and 4,166 pending candidates. The
registry contains 438 direct relationships and 11 broader claims, and reconciliation validation
continues to pass with zero errors and two expected warnings.

Codecs/language-modeling bundle 4 closed the theme by rejecting 1,141 candidates in one categorized
human-review bundle: 629 unchanged prior scope gaps, 283 prior gaps with added shared evidence, two
individually audited core-claim changes, and 227 newly emitted scope mismatches. Every rejection has
a candidate-specific rationale and reconsideration trigger. The completed theme contains 133 accepted
and 1,141 rejected candidates with zero deferred or pending. The full run now has 279 accepted, 2,010
rejected, and 3,025 pending candidates. Reconciliation validation passes with zero errors and two
expected warnings; the registry remains at 438 direct relationships and 11 broader claims.

Speaker bundle 1 accepted 78 existing-authority candidates: 67 Q4 human-approved decisions were
reaffirmed, eight newly emitted pairs resolved through the existing multiattribute-disentanglement
claim, and three resolved through the existing multidimensional-evaluation claim. The audit covered
33 direct registry targets and 45 broader-claim resolutions without creating duplicate records. The
speaker theme now has 78 accepted and 1,184 pending candidates; the full run has 357 accepted, 2,010
rejected, and 2,947 pending candidates. Reconciliation validation passes with zero errors and two
expected warnings; the registry remains at 438 direct relationships and 11 broader claims.

Speaker bundle 2 accepted 16 disentanglement and attribute-interference candidates: 14 newly
emitted pairs and two Q4 rejections reopened after the GRL claim materially strengthened. Eight
reviewed members were added to the multiattribute-disentanglement broader claim, whose exact member-
derived evidence was refreshed through the Q1 cutoff, and two direct relationships were added for
post-hoc steering and style-timbre control. The speaker theme now has 94 accepted and 1,168 pending
candidates; the full run has 373 accepted, 2,010 rejected, and 2,931 pending candidates. The registry
contains 440 direct relationships and 11 broader claims, and reconciliation validation passes with
zero errors and two expected warnings.

Speaker bundle 3 accepted eight newly emitted reference and representation-transfer candidates:
four non-audio or reference-free identity links, two low-resource or timbre-transfer links, and two
prompt-leakage or pitch-preservation links. Six were recorded as `related`, one as `refines`, and one
as `supports`. The speaker theme now has 102 accepted and 1,160 pending candidates; the full run has
381 accepted, 2,010 rejected, and 2,923 pending candidates. The registry contains 448 direct
relationships and 11 broader claims, and reconciliation validation passes with zero errors and two
expected warnings.

Speaker bundle 5 accepted eight newly emitted identity and perceptual trade-off candidates: five
control-interference or perceptual-cost links, two privacy or metric-validity links, and one style-
timbre evaluation link. Five were recorded as `tradeoff`, one as `supports`, and two as `refines`.
Speaker acceptance review is complete at 118 accepted, with 1,144 categorized rejection candidates
remaining. The full run has 397 accepted, 2,010 rejected, and 2,907 pending candidates. The registry
contains 464 direct relationships and 11 broader claims, and reconciliation validation passes with
zero errors and two expected warnings.

Speaker bundle 6 closed the theme by rejecting 1,144 candidates in one categorized human-review
bundle: 603 unchanged prior scope gaps, 282 prior gaps with added shared evidence, three individually
audited core-claim changes, and 256 newly emitted scope mismatches. Every rejection has a candidate-
specific rationale and reconsideration trigger. The completed theme contains 118 accepted and 1,144
rejected candidates with zero deferred or pending. The full run now has 397 accepted, 3,154 rejected,
and 1,763 pending candidates. Reconciliation validation passes with zero errors and two expected
warnings; the registry remains at 464 direct relationships and 11 broader claims.

Controllability bundle 2 accepted 12 newly emitted factorized and post-hoc control candidates: five
structural-factorization or preservation links, four targeted expressive-control links, and three
post-hoc or signal-level control links. Nine were recorded as `related`, two as `refines`, and one as
`supports`. The controllability theme now has 172 accepted and 775 pending candidates; the full run
has 569 accepted, 3,154 rejected, and 1,591 pending candidates. The registry contains 476 direct
relationships and 11 broader claims, and reconciliation validation passes with zero errors and two
expected warnings.

Controllability bundle 3 accepted ten newly emitted emotion and local-prosody candidates: four
hierarchical emotion or prosody links, three duration, rhythm, or signal-control links, and three
cross-speaker expressive-transfer links. Nine were recorded as `related` and one as `supports`. The
controllability theme now has 182 accepted and 765 pending candidates; the full run has 579 accepted,
3,154 rejected, and 1,581 pending candidates. The registry contains 486 direct relationships and 11
broader claims, and reconciliation validation passes with zero errors and two expected warnings.

Controllability bundle 4 accepted eight newly emitted cross-lingual expressive-control candidates:
two language-sensitive timing or conditioning links, three cross-lingual style or representation-
transfer links, and three low-resource adaptation or leakage-boundary links. Six were recorded as
`related` and two as `refines`. The controllability theme now has 190 accepted and 757 pending
candidates; the full run has 587 accepted, 3,154 rejected, and 1,573 pending candidates. The registry
contains 494 direct relationships and 11 broader claims, and reconciliation validation passes with
zero errors and two expected warnings.

Controllability bundle 5 accepted ten newly emitted control-boundary and evaluation candidates: two
prompt or identity-control boundary links, three attribute-separation or perceptual-cost links, and
five dimension-specific evaluation links. Three were recorded as `related`, two as `refines`, and
five as `supports`. Controllability acceptance review is complete at 200 accepted, with 747
categorized rejection candidates remaining. The full run has 597 accepted, 3,154 rejected, and 1,563
pending candidates. The registry contains 504 direct relationships and 11 broader claims, and
reconciliation validation passes with zero errors and two expected warnings.

Controllability bundle 6 closed the theme by rejecting 747 candidates in one categorized human-
review bundle: 357 unchanged prior scope gaps, 178 prior gaps with added shared evidence, two
individually audited GRL core-claim changes, and 210 newly emitted scope mismatches. Every rejection
has a candidate-specific rationale and reconsideration trigger. The completed theme contains 200
accepted and 747 rejected candidates with zero deferred or pending. The full run now has 597 accepted,
3,901 rejected, and 816 pending candidates. Reconciliation validation passes with zero errors and two
expected warnings; the registry remains at 504 direct relationships and 11 broader claims.

Robustness bundle 1 accepted 40 existing-authority candidates: 21 multilingual coverage or
representation-transfer links, 12 unseen-voice or acoustic-robustness links, four scalable-
supervision links, and three domain-shift evaluation links. Thirty-seven candidates reaffirm existing
human-approved direct relationships and three resolve through the existing training-diversity and
unseen-voice-generalization broader claim. No registry record was created or duplicated. The
robustness theme now has 40 accepted and 178 pending candidates; the full run has 637 accepted, 3,901
rejected, and 776 pending candidates. Reconciliation validation passes with zero errors and two
expected warnings; the registry remains at 504 direct relationships and 11 broader claims.

Robustness bundle 2 accepted 13 newly emitted multilingual coverage and pronunciation candidates:
four multilingual-training or cross-task-transfer links, six pronunciation or language-structure
links, and three scale or balance-boundary links. Eight were recorded as `related`, three as
`supports`, and two as `refines`. The robustness theme now has 53 accepted and 165 pending candidates;
the full run has 650 accepted, 3,901 rejected, and 763 pending candidates. The registry contains 517
direct relationships and 11 broader claims, and reconciliation validation passes with zero errors and
two expected warnings.

Robustness bundle 3 accepted 22 domain-shift and leakage candidates: eight language, accent, or
cloning-leakage links, ten domain-sensitive evaluation links, and four architecture or data-
robustness links. Ten pairs were newly emitted, while 12 Q4 rejections were reopened after added Q1
evidence closed the earlier proposition-scope gap. One was recorded as `related`, 14 as `supports`,
and seven as `refines`. The robustness theme now has 75 accepted and 143 pending candidates; the full
run has 672 accepted, 3,901 rejected, and 741 pending candidates. The registry contains 539 direct
relationships and 11 broader claims, and reconciliation validation passes with zero errors and two
expected warnings.

Robustness bundle 4 accepted three newly emitted conversational-data robustness candidates: one
turn-taking behavior link, one long-context conversation link, and one data-structure-versus-scale
link. Two were recorded as `supports` and one as `refines`. Robustness acceptance review is complete
at 78 accepted, with 140 categorized rejection candidates remaining. The full run has 675 accepted,
3,901 rejected, and 738 pending candidates. The registry contains 542 direct relationships and 11
broader claims, and reconciliation validation passes with zero errors and two expected warnings.

Robustness bundle 5 closed the theme by rejecting 140 candidates in one categorized human-review
bundle: 84 unchanged prior scope gaps, 18 prior gaps with added shared evidence, and 38 newly emitted
scope mismatches. Every rejection has a candidate-specific rationale and reconsideration trigger. The
completed theme contains 78 accepted and 140 rejected candidates with zero deferred or pending. The
full run now has 675 accepted, 4,041 rejected, and 598 pending candidates. Reconciliation validation
passes with zero errors and two expected warnings; the registry remains at 542 direct relationships
and 11 broader claims.

Streaming-and-agents bundle 1 accepted 48 authority candidates: 42 Q4 human-approved decisions were
reaffirmed, five newly emitted pairs resolved through existing broader claims, and one Q4 rejection
was reversed after Q1 broader authority closed the earlier scope gap. Thirty-six candidates use
existing direct relationships and 12 resolve through broader claims; no registry record was created
or duplicated. One legacy agent-proposed equivalent relationship was deliberately bypassed in favor
of the corrective human-approved specialization record for the same backchannel pair. The theme now
has 48 accepted and 171 pending candidates; the full run has 723 accepted, 4,041 rejected, and 550
pending candidates. Reconciliation validation passes with zero errors and two expected warnings; the
registry remains at 542 direct relationships and 11 broader claims.

Streaming-and-agents bundle 2 accepted 14 responsiveness and streaming-policy candidates: five
responsiveness or latency-trade-off links, five interruption or backchannel-policy links, and four
curricula, concurrent-reasoning, or measurement links. Eleven pairs were newly emitted, while three
Q4 rejections were reopened after added Q1 evidence closed the earlier proposition-scope gap. Eleven
were recorded as `related` and three as `supports`. The theme now has 62 accepted and 157 pending
candidates; the full run has 737 accepted, 4,041 rejected, and 536 pending candidates. The registry
contains 556 direct relationships and 11 broader claims, and reconciliation validation passes with
zero errors and two expected warnings.

Streaming-and-agents bundle 3 accepted 14 interaction-evaluation and context candidates: six
backchannel or turn-taking evaluation links, five responsiveness benchmark-coverage links, and three
context or conversational-memory links. Eleven pairs were newly emitted, while three Q4 rejections
were reopened after added Q1 evidence closed the earlier proposition-scope gap. Ten were recorded as
`supports` and four as `related`; one proposed `supports` edge was tightened to `related` to preserve
the acyclic directed registry. The theme now has 76 accepted and 143 pending candidates; the full run
has 751 accepted, 4,041 rejected, and 522 pending candidates. The registry contains 570 direct
relationships and 11 broader claims, and reconciliation validation passes with zero errors and two
expected warnings.

Streaming-and-agents bundle 4 accepted eight streaming-architecture and training candidates: four
system-architecture or concurrent-reasoning links, two simultaneous-interaction or measurement
links, and two curricula, data, or context links. Five pairs were newly emitted, while three Q4
rejections were reopened after added Q1 evidence closed the earlier proposition-scope gap. Five were
recorded as `related` and three as `supports`. Streaming-and-agents acceptance review is complete at
84 accepted, with 135 categorized rejection candidates remaining. The full run has 759 accepted,
4,041 rejected, and 514 pending candidates. The registry contains 578 direct relationships and 11
broader claims, and reconciliation validation passes with zero errors and two expected warnings.

Streaming-and-agents bundle 5 closed the theme by rejecting 135 candidates in one categorized human-
review bundle: 68 unchanged prior scope gaps, 18 prior gaps with added shared evidence, and 49 newly
emitted scope mismatches. Every rejection has a candidate-specific rationale and reconsideration
trigger. The completed theme contains 84 accepted and 135 rejected candidates with zero deferred or
pending. The full run now has 759 accepted, 4,176 rejected, and 379 pending candidates.
Reconciliation validation passes with zero errors and two expected warnings; the registry remains at
578 direct relationships and 11 broader claims.

Efficiency bundle 1 accepted 28 existing-authority candidates: six interactive end-to-end latency
links, 14 parallel or token-efficient decoding links, and eight flow or diffusion acceleration
links. All 28 exactly reaffirm Q4 human-approved direct relationships; no candidate was new or
reopened, and no registry record was created. The efficiency theme now has 28 accepted and 177
pending candidates; the full run has 787 accepted, 4,176 rejected, and 351 pending candidates.
The registry remains at 578 direct relationships and 11 broader claims.

Efficiency bundle 2 accepted 15 interactive end-to-end latency candidates: six system-architecture
or shifting-bottleneck links, four streaming-policy or incremental-generation links, and five
interaction-measurement links. Eleven pairs were newly emitted, while four Q4 rejections were
reopened after Q1 evidence closed the earlier proposition-scope gap. Seven were recorded as
`supports`, five as `related`, two as `tradeoff`, and one as `refines`. The efficiency theme now
has 43 accepted and 162 pending candidates; the full run has 802 accepted, 4,176 rejected, and
336 pending candidates. The registry contains 593 direct relationships and 11 broader claims.

Efficiency bundle 3 accepted 19 token and generation-efficiency candidates: seven token-rate or
compact-representation links, five parallel or non-autoregressive-generation links, five flow or
decoding-acceleration links, and two efficiency-quality validation links. Eleven pairs were newly
emitted, while eight Q4 rejections were reopened after Q1 evidence closed the earlier proposition-
scope gap. Ten were recorded as `supports`, six as `related`, and three as `tradeoff`. The efficiency
theme now has 62 accepted and 143 pending candidates; the full run has 821 accepted, 4,176 rejected,
and 317 pending candidates. The registry contains 612 direct relationships and 11 broader claims.

Efficiency bundle 4 accepted 18 deployment and quality-boundary candidates: two data-efficient-
supervision links, seven streaming or architecture-deployment links, four cross-task or
representation-acceleration links, and five perceptual-quality-boundary links. Three pairs were
newly emitted, while 15 Q4 rejections were reopened after Q1 evidence closed the earlier proposition-
scope gap. Seven were recorded as `supports`, four as `related`, and seven as `tradeoff`. Efficiency
acceptance review is complete at 80 accepted, with 125 categorized rejection candidates remaining.
The full run has 839 accepted, 4,176 rejected, and 299 pending candidates. The registry contains 630
direct relationships and 11 broader claims.

Controllability bundle 1 accepted 160 authority candidates: 111 Q4 human-approved decisions were
reaffirmed, 23 newly emitted pairs resolved through existing reviewed broader claims, and 26 Q4
rejections were explicitly reversed after later Q1 human review established shared broader
authority for both endpoints. No registry record was created or duplicated. The controllability
theme now has 160 accepted and 787 pending candidates; the full run has 557 accepted, 3,154 rejected,
and 1,603 pending candidates. Reconciliation validation passes with zero errors and two expected
warnings; the registry remains at 464 direct relationships and 11 broader claims.

Efficiency bundle 5 closed the theme by rejecting 125 candidates in one categorized human-review
bundle: 90 unchanged prior scope gaps, 13 prior gaps with added shared evidence, and 22 newly
emitted scope mismatches. Every rejection has a candidate-specific rationale and reconsideration
trigger. The completed theme contains 80 accepted and 125 rejected candidates with zero deferred or
pending. The full run now has 839 accepted, 4,301 rejected, and 174 pending candidates. The registry
remains at 630 direct relationships and 11 broader claims.

Post-training bundle 1 accepted 52 authority candidates: 51 Q4 human-approved decisions were
reaffirmed, and one newly emitted pair resolved through the existing preference-post-training broader
claim. Seventeen candidates use existing direct relationships and 35 use the reviewed broader claim;
no registry record was created or duplicated. The post-training theme now has 52 accepted and 122
pending candidates. The full run has 891 accepted, 4,301 rejected, and 122 pending candidates, and the
registry remains at 630 direct relationships and 11 broader claims.

Post-training bundle 2 accepted 16 new reward-design and evaluation relationships on 2026-11-28.
Four cover reward effectiveness and stability, ten cover evaluator limits, and two cover control
and quality failure modes. Eight are `supports`, six are `tradeoff`, and two are `related`.
Post-training now has 68 accepted and 106 pending candidates. The full run has 907 accepted,
4,301 rejected, and 106 pending. The registry contains 646 direct relationships and 11 broader claims.

Post-training bundle 3 accepted 10 new relationships on 2026-11-28. Two cover streaming translation,
three cover timing and alignment, and five cover task adaptation and modality transfer. The registry
adds one specialization, one supports relationship, two refines relationships, and six related links.
Post-training now has 78 accepted and 96 pending candidates. The full run has 917 accepted,
4,301 rejected, and 96 pending. The registry contains 656 direct relationships and 11 broader claims.

Post-training bundle 4 accepted two supports relationships on 2026-11-28. The accent-and-rhythm
pair was new. Q1 evidence on speech reward evaluator collapse reopened the Q4 rejection on proxy
rewards and listener judgment. Post-training now has 80 accepted and 94 pending candidates.
The full run has 919 accepted, 4,301 rejected, and 94 pending. The registry contains 658 direct
relationships and 11 broader claims.

Post-training bundle 5 closed the theme with 94 human-approved rejections: 64 unchanged prior
scope gaps, 12 prior gaps with added evidence, and 18 newly emitted scope mismatches. Each
decision includes a rationale and reconsideration trigger. Post-training closed at 80 accepted
and 94 rejected. Across all eight Q1 themes, 919 were accepted and 4,395 rejected, with zero
pending or deferred. The registry contains 658 direct relationships and 11 broader claims.
The Q1 reconciliation run was finalized on 2026-11-28 with zero errors and the existing warning
for 15 legacy agent proposals.

Speaker bundle 4 accepted eight newly emitted cross-lingual and low-resource transfer candidates:
four adaptation and language-coverage links, two cross-lingual identity or accent links, and two
language-sensitive boundary links. Six were recorded as `related`, one as `supports`, and one as
`refines`. The speaker theme now has 110 accepted and 1,152 pending candidates; the full run has 389
accepted, 2,010 rejected, and 2,915 pending candidates. The registry contains 456 direct
relationships and 11 broader claims, and reconciliation validation passes with zero errors and two
expected warnings.

The review cadence was clarified on 2026-11-15 and promoted to the canonical
`docs/integration-protocol.md` rather than remaining a chat convention. Future integration sessions
must triage a whole theme before decisions, carry forward audited authority in one large bundle,
review likely acceptances in semantic groups of roughly 10–25, and close hundreds of rejections in
one categorized bundle. Review tables must explain what each semantic group covers, its central
claim, candidate count, new-versus-reopened split, and concrete registry effect. Progress is reported
after every approval. Pair-by-pair review is reserved for ambiguity, reversals of human-approved
authority, new broader propositions, and exceptions that cannot safely share a rationale.

No reconciliation commit or push has been made after the initial candidate-generation checkpoint.

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
