# Project Status

Last updated: 2026-11-11

The Q3 and Q4 2025 content cycles are complete through integration, human-reviewed reconciliation,
retrospective snapshots, field rendering, and quarterly reporting. Q2 2026 ingestion is complete
(158 ingested after two pages moved to Q3 on 2026-11-01); the active corpus priority is the Q3 2026
frontier and Q1 integration. The peer-reviewed-version rule and its verified Q1 batch are complete;
Q3 fetch coverage is complete (Interspeech 2026
from ISCA on 2026-11-01; arXiv top-up through 2026-09-30 on 2026-11-07), every accepted Q3 record
has a PDF and is parsed (all 7 parse batches done 2026-11-11).

---

## Current priorities

1. Preserve the published Q4 snapshot and report as immutable historical artifacts.
2. Freeze the 116-paper Q1 2026 integration manifest and begin Phase 1 across its 22 affected
   concepts (453 page-to-concept memberships).
3. Continue the corpus-wide peer-reviewed-version batches, including the two Q2-held ICML/IJCAI
   records and historical frozen records, without duplicating the released migration path. By user
   decision (2026-11-11) the Q3-relevant batches (Interspeech; ICML/IJCAI/ICPR/ICME/ACL) run after
   the Q3 sweep and before Q3 integration.
4. Ingest Q3 2026. Pre-flight is complete (fetch, filter, review, downloads, parse, and the
   peer-reviewed-version check on 2026-11-11); next, the chronological sweep of 363 accepted
   records (StellarTTS `2607.19859` excluded: ASRU 2025, canonical quarter Q4 2025; catch-up Q4
   integration tracked in `BACKLOG.md`). Procedure: `docs/ingest-protocol.md`.

The completed Q2 ingest record is archived at `docs/records/2026-11-01-q2-2026-ingestion-sessions.md`;
the active Q3 operating record is `Q3_2026_INGESTION_SESSIONS.md` (bootstrapped 2026-11-01). The completed Q4 integration record is archived at
`docs/records/2026-11-01-q4-2025-integration-and-synthesis-sessions.md`.

---

## Corpus state

| Measure | Current value | Notes |
|---|---:|---|
| Metadata records | 2,024 | 1,069 ingested, 386 accepted, 0 review, 569 rejected (incl. 109 Interspeech 2026 ISCA duplicates and 13 arXiv preprints of ISCA records) |
| Published paper pages | 1,061 | Unique content pages; canonical-ID pointers explain the difference from metadata marked ingested |
| Active accepted + ingested corpus | 1,455 | Basis of `scripts/corpus_summary.py` |
| Parsed active papers | 1,436 | Includes ingested papers and accepted papers ready for ingest |
| Accepted and parsed, ready to ingest | 367 | 3 Q2 2026 (held ICML/IJCAI records that move to Q3 in a peer-reviewed-version batch, and re-dated `2608.26146`) and 364 Q3 2026 (incl. StellarTTS, which moves to Q4 2025); 19 Q4 2026 records await parse |
| Concept claim YAMLs | 23 | All canonical Q3 concepts represented |
| Concept paper entries | 2,892 | Corrective Phase 1 and Phase 2 are complete for four late Q4 papers across seven concepts |
| Claim clusters | 444 | 342 strongly supported, 85 emerging, and 17 contested |
| Rendered concept pairs | 23/23 present and current for Q4 | Every canonical concept has a current Overview and In Depth page |
| Current field overview | Complete for Q4 | 23 concepts, 668 unique papers, 2,892 memberships, 444 local clusters, and 11 approved broader claims |
| Reconciliation state | 388 relationships, 11 broader claims; 3,946 Q4 decisions finalized, 0 pending | Original run and bounded late-evidence corrective refresh complete |
| Published snapshots | 2 | Retrospective `2025-Q3` and `2025-Q4` snapshots |
| Published quarterly reports | 2 | `reports/quarterly/2025-Q3.md` and `reports/quarterly/2025-Q4.md` |

Live health baseline on 2026-11-01:

```text
agents:    PASS — 0 errors, 0 warnings; 8 workflows checked
ingest:    PASS — 0 errors, 1,167 accepted warnings; 1,061 paper pages checked
integrate: PASS — 0 errors, 324 accepted warnings; 2,892 entries, 444 clusters; papers_not_in_any_yaml=335 against the later ingest frontier
metadata:  PASS — 0 errors, 8 accepted warnings; 1,455 active records checked
reconcile: PASS — 0 errors, 2 expected warnings; 2 published snapshots and finalized decisions remain intact
render:    PASS — 0 errors, 0 warnings; all 23 Q4 concept pairs and the field overview current
```

Integration warnings are non-blocking and primarily reflect accepted method-family outliers. The
bounded corrective reconciliation added exactly four inherited paper references across the
automatic-judge, multiattribute-disentanglement, semantic–acoustic-hierarchy, and
multidimensional-evaluation broader claims. The two remaining warnings reflect one retained
high-similarity rejection and 15 historical agent-proposed registry records that remain
non-authoritative.

---

## Quarterly progress

| Quarter | Ingest | Integrate | Reconcile | Render / report |
|---|---|---|---|---|
| Q3 2025 and earlier | Complete | Complete: 23 concepts, 2,226 entries | Complete: human-reviewed | Complete: field overview, snapshot, and Q3 report; 21/23 concept pairs |
| Q4 2025 | Complete: 173 eligible pages, 2 intentional Tier-2 exclusions | Complete: all affected concepts plus corrective late evidence, 2,892 entries | Complete: 3,946 decisions finalized; bounded corrective evidence refresh passes | Complete: 23/23 concept pairs, field overview, immutable snapshot, and Q4 report |
| Q1 2026 | Complete: 116 ingested, 0 accepted after the verified peer-reviewed-version batch | Not started; manifest-ready (22 concepts, 453 memberships) | Not started | Not started |
| Q2 2026 | Complete: 174 ingested after 16 Q1 pages moved to verified May proceedings dates; 2 accepted held (`2606.12940` ICML, `2606.13006` IJCAI); 1 accepted re-dated into Q2 on 2026-11-07 (`2608.26146` Vagdhenu, parsed 2026-11-11, not yet ingested) | Not started | Not started | Not started |
| Q3 2026 to date | 34 ingested (re-dated Interspeech 2026 pages); 364 accepted (all parsed; 363 in the sweep, StellarTTS moves to Q4 2025) | Not started | Not started | Not started |

Quarter counts above are by canonical `published_date` as of 2026-11-11. Per-quarter ingest
status in `BACKLOG.md` (2026-09-27) predates the paper-date rule and is superseded by these counts.

## Paper dates

Since 2026-10-04 `published_date` follows one rule: the conference date for peer-reviewed
proceedings, else the journal date, else the date of the arXiv version we fetched (`version_date`;
`preprint_date` keeps v1) (`docs/schemas/metadata.md#paper-dates`). All non-ingested records and
all ingested records published from 2026-01-01 are migrated (the latter on 2026-10-16, with their
paper pages). Ingested records from 2025 and earlier are deliberately left on legacy dates so the
frozen 2025 snapshot and claim YAML stay valid; the metadata health check reports them as legacy
warnings.

On 2026-10-26 rule 1 was applied to the published Interspeech 2026 proceedings (ISCA archive): 97
accepted or ingested 2026 records got `conference_date: 2026-09-27` and moved to Q3 (32 ingested pages
synced). Other conference-accepted arXiv records (ICASSP, ICML, ACL, ...) keep the arXiv date for now
by user decision; a one-pass migration is tracked in `BACKLOG.md`.

On 2026-11-01 the full Interspeech 2026 proceedings were fetched from the ISCA archive (203 records
past the keyword filter). 109 duplicated existing records and were marked `is_duplicate` with the
existing record canonical; the canonical records gained `source_ids.isca` and `doi`. Two Q2 pages
missed by the 2026-10-26 title match because they were retitled (`2603.05373`, `2604.16211`) were
re-dated to Q3.

On 2026-11-08 the single-owner migration path was implemented and the verified Q1 batch applied:
20 records gained authoritative peer-reviewed links and dates; 16 moved Q1→Q2, ASRU moved to Q4
2025, SLT moved to Q4 2024, and two AAAI papers stayed in Q1. Claim membership is the sole freeze
authority. Frozen records retain their summarized-version venue and canonical date while recording
the later publication separately. The broader venue backfill remains open in `BACKLOG.md`.


---

## Completed Q4 2025 content cycle

Canonical live audit as of 2026-09-26:

- 174 ingested, non-Tier-2 Q4 paper pages.
- 172 pages carry at least one canonical `related_concepts` assignment.
- 2 pages have no concept assignment and remain intentionally unassigned after audit.
- 2 Tier 2 pages are excluded from integration.
- 169 distinct Q4 papers appear in at least one applicable concept YAML.
- All 22 affected concepts are complete through Phase 2; `fine-tuning` had no Q4 candidate.
- The exact candidate-versus-YAML closure audit reports no missing or extra IDs in any concept.

Largest Q4 queues:

| Concept | Q4 candidates | Already present | Queue |
|---|---:|---:|---:|
| subjective-evaluation | 73 | 73 | 0 |
| evaluation-metrics | 61 | 61 | 0 |
| zero-shot-tts | 59 | 59 | 0 |
| neural-codec | 56 | 56 | 0 |
| spoken-language-model | 46 | 46 | 0 |
| speech-to-speech | 34 | 34 | 0 |
| autoregressive-codec-tts | 31 | 31 | 0 |
| multilingual-tts | 30 | 30 | 0 |
| self-supervised-speech | 30 | 30 | 0 |
| voice-conversion | 29 | 29 | 0 |
| flow-matching | 28 | 28 | 0 |
| emotion-synthesis | 24 | 24 | 0 |

`subjective-evaluation` is complete through Q4 Phase 2. Its remaining 61 concept warnings are
accepted architecture-unspecified evaluation, benchmark, dataset, and metric outliers rather than
missing synthesis work.

`evaluation-metrics` is complete through Q4 Phase 2. Its 20 remaining concept warnings are
accepted method-family outliers: 14 preserved Q3-and-earlier papers plus 6 Q4 architecture,
optimization, or robustness papers whose evaluation claims remain peripheral.

`zero-shot-tts` is complete through Q4 Phase 2. Its 24 remaining concept warnings are intentional
method-family outliers: 16 preserved Q3-and-earlier papers plus 8 Q4 architecture, evaluation,
optimization, or dataset papers whose zero-shot evidence is peripheral to the nine method families.
`neural-codec` is complete through Q4 Phase 2. Its 21 concept warnings are intentional
method-family outliers: 12 preserved Q3-and-earlier papers plus 9 Q4 evaluation, benchmark,
dialogue-context, or peripheral-use papers. The exact live Q4 audit closes at 56/56.

`spoken-language-model` is complete through Q4 Phase 2 at 46/46 live Q4 candidates. Its 39
concept warnings are intentional method-family outliers: 28 preserved Q3-and-earlier survey,
benchmark, dataset, or evaluation papers plus 11 Q4 architecture-unspecified papers. The synthesis
contains 18 strongly supported clusters and 7 method families.

`speech-to-speech` is complete through Q4 Phase 2 at 34/34 live candidates, superseding the
35-paper planning estimate. Its 94-paper graph contains 19 claim clusters and 7 method families;
24/34 Q4 papers have family assignments, and the 28 concept warnings are intentional benchmark,
evaluation, survey, or peripheral-task outliers. All 33 Q4 papers carrying high- or
medium-relevance claims map to at least one cluster.

`autoregressive-codec-tts` is complete through Q4 Phase 2 at 31/31 live candidates, superseding
the 33-candidate planning baseline. Its 196-paper graph contains 19 claim clusters and 14 method
families; 30/31 Q4 papers have family assignments, with one architecture-unspecified survey as an
intentional outlier. All 31 Q4 papers carrying high- or medium-relevance claims map to at least one
cluster.

`multilingual-tts` is complete through Q4 Phase 2 at 30/30 eligible candidates, superseding the
31-candidate dashboard estimate; one additional paper is Tier 2 and excluded. Its 105-paper graph
contains 19 strongly supported claim clusters and seven method families. 28/30 Q4 papers have
family assignments, with two architecture-unspecified orchestration and text-normalization
outliers. All 26 Q4 papers carrying high- or medium-relevance claims map to at least one cluster.

`self-supervised-speech` is complete through Q4 Phase 2 at 30/30 eligible candidates; one Tier 2
paper is excluded. Its 176-paper graph contains 17 clusters (14 strongly supported, two contested,
and one emerging) and seven method families. All 30 Q4 papers have reciprocal family assignments,
and all 24 carrying high- or medium-relevance claims map to at least one cluster. Low-resource
transfer advanced from emerging to strongly supported. The 19 concept warnings are preserved
pre-Q4 architecture-unspecified or peripheral outliers.

`voice-conversion` is complete through Q4 Phase 2 at 29/29 eligible candidates. Its 116-paper graph
contains 19 clusters (17 strongly supported, one contested, and one emerging) and seven method
families. 24/29 Q4 papers have reciprocal family assignments; the five remaining shared-task,
benchmark, dataset, phonation, and survey papers are intentional outliers. All 28 Q4 papers with
high- or medium-relevance claims map to at least one cluster. Q4 added clusters for reference-free
generated speaker identities and synthetic parallel supervision, while non-parallel training and
privacy-oriented conversion advanced to strongly supported.

`flow-matching` is complete through Q4 Phase 2 at 28/28 eligible candidates, superseding the
30-candidate dashboard estimate; no Tier 2 papers were excluded. Its 125-paper graph contains 35
clusters (16 strongly supported, one contested, and 18 emerging) and seven method families. 27/28
Q4 papers have reciprocal family assignments, with one architecture-spanning controllable-TTS
survey retained as an intentional outlier. All 25 Q4 papers with high- or medium-relevance concept
roles map to at least one cluster. Q4 added a strongly supported cluster for causal and chunked
streaming flow matching and promoted seven clusters covering NAR efficiency, RL alignment, codec
refinement, auxiliary attributes, cross-lingual transfer, robustness, and training-time alignment.

`emotion-synthesis` is complete through Q4 Phase 2 at 24/24 eligible candidates, with no Tier 2
exclusions. Its 97-paper graph retains 17 clusters (16 strongly supported and one emerging) and
seven method families. 19/24 Q4 papers have reciprocal family assignments; five evaluation,
dataset, dialogue-benchmark, or survey records are intentional outliers. All 23 Q4 papers with
high- or medium-relevance concept roles map to at least one cluster. Multimodal affect context and
data/taxonomy limitations advanced to strongly supported, and the preference-optimization
reassessment was retired after independent reward-hacking and human-evaluation evidence satisfied
its trigger.

`gan-vocoder` is complete through Q4 Phase 2 at 21/21 eligible candidates, with no Tier 2
exclusions. Its 81-paper graph contains 18 clusters (16 strongly supported and two emerging) and
seven method families. 18/21 Q4 papers have reciprocal family assignments; three peripheral G2P,
voice-quality-control, and endangered-language TTS records are intentional outliers. All 18 Q4
papers with high- or medium-relevance concept roles map to at least one cluster. Q4 added a
strongly supported cluster for frequency-structured representations and promoted causal streaming,
GAN-training stabilization, and objective-metric misranking to strongly supported.

`prosody-control` is complete through Q4 Phase 2 at 21/21 eligible candidates, with no Q4 Tier 2
exclusions. Its 115-paper graph contains 19 clusters (18 strongly
supported and one emerging) and 15 method families. 20/21 Q4 papers have reciprocal family
assignments; the architecture-spanning controllable-TTS survey is an intentional outlier. All 20
Q4 papers with high- or medium-relevance concept roles map to at least one cluster. Q4 added a
strongly supported cluster for cross-attribute interference and an emerging cluster and method
family for reward-optimized prosody control. Diversity–naturalness trade-offs, targeted expressive
data, metric disagreement, and structured control plans advanced to strongly supported.

`streaming-tts` is complete through Q4 Phase 2 at 21/21 eligible candidates, with no Q4 Tier 2
exclusions. Its 75-paper graph contains 19 strongly supported clusters and five method families;
all 21 Q4 papers have reciprocal family assignments. All Q4 contributors also carry high- or
medium-relevance concept roles and map to at least one cluster. Q4 added strongly supported
clusters for concurrent reasoning during listening and migrating end-to-end latency bottlenecks,
while chunk-size trade-offs, shared streaming/offline modes, speech-reasoning gaps, and
interaction-aware evaluation advanced to strongly supported.

`rlhf-speech` is complete through Q4 Phase 2 at 20/20 eligible candidates, with no Q4 Tier 2
exclusions. Its 49-paper graph contains 22 clusters (15 strongly supported, six emerging, and one
contested) and six method families. 19/20 Q4 papers have reciprocal family assignments; the
interaction-corpus paper is an intentional infrastructure outlier. All 19 Q4 papers with high- or
medium-relevance concept roles map to at least one cluster. Q4 added strongly supported clusters
for localized token-level alignment and reward-model brittleness, promoted four existing clusters,
and made the claim that RL-trained reward models outperform supervised training contested.

`speaker-adaptation` is complete through Q4 Phase 2 at 19/19 eligible candidates; one historical
Tier 2 paper is excluded. Its 98-paper graph contains 19 clusters (17 strongly supported and two
emerging) and seven method families. 17/19 Q4 papers have reciprocal family assignments; the
architecture-unspecified shared-task overview and dataset paper are intentional outliers. All 19
Q4 papers with high- or medium-relevance claims map to at least one cluster. Q4 added a strongly
supported cluster for generated or cross-modally inferred speaker identities and an emerging
cluster for location-aware speaker supervision, while codec-prompted in-context cloning advanced
to strongly supported.

`disentanglement` is complete through Q4 Phase 2 at 16/16 eligible candidates, with no Tier 2
exclusions. Its 116-paper graph contains 19 clusters (15 strongly supported, two contested, and two
emerging) and ten method families. All 16 Q4 papers have reciprocal family assignments and map to
at least one cluster. Q4 added strongly supported clusters for architectural stream separation and
cross-source compositional evaluation, promoted incomplete SSL disentanglement to strongly
supported, and retired the mutual-information and prompt-leakage reassessment items after their
triggers were satisfied. The 16 concept warnings are preserved pre-Q4 family outliers.

`instruction-conditioned-tts` is complete through Q4 Phase 2 at 13/13 eligible candidates; five
historical Tier 2 papers are excluded. Its 57-paper graph contains 17 clusters (ten strongly
supported, five emerging, and two contested) and nine method families. All 13 Q4 papers have
reciprocal family assignments and map to at least one cluster. Q4 added a guidance-based control
family and strongly supported clusters for guidance-strength trade-offs and underconstrained
text-only voice control. Stronger-interpreter benefits changed to contested, and the direct-prompt
family reassessment was retired. Two preserved pre-Q4 family outliers remain.

`diffusion-tts` is complete through Q4 Phase 2 at 11/11 eligible candidates, with no Tier 2
exclusions. Its 57-paper graph contains 17 clusters (15 strongly supported and two emerging) and
seven method families. Nine Q4 papers have reciprocal family assignments; the peripheral G2P/TTS
deployment paper and architecture-spanning survey are intentional outliers. All ten Q4 papers with
high- or medium-relevance concept roles map to at least one cluster. Q4 added emerging clusters for
masked discrete diffusion with length control and for structured-surrogate or phase-corrected
diffusion vocoders. Seven family-coverage warnings remain, five from before Q4.

`singing` is complete through Q4 Phase 2 at 10/10 eligible candidates, with no Tier 2 exclusions.
Its 20-paper graph contains 23 clusters (three strongly supported and 20 emerging) and five method
families. Eight Q4 papers have reciprocal family assignments; the generative-feedback evaluator
and field survey are intentional outliers. All ten Q4 papers map to at least one cluster. Q4 added
six emerging directions covering annotation-light alignment, factorized low-resource and
out-of-distribution timbre transfer, real-world conversion robustness, RL post-training,
harmonic-aware vocoding, and data-scale constraints.

`transformer-enc-dec-tts` is complete through Q4 Phase 2 at 5/5 eligible candidates, with no Tier 2
exclusions. Its 33-paper graph contains 19 clusters (six strongly supported and 13 emerging) and
seven method families. All five Q4 papers have reciprocal family memberships and cluster coverage.
Adversarial restoration of acoustic detail advanced to strongly supported, and Q4 added a
strongly supported data-curation cluster plus an emerging spontaneous-speech segmentation cluster.
One preserved pre-Q4 family outlier remains.

Q4 concept integration, reconciliation, rendering, snapshot, and reporting are complete. Active
work has moved to the Q3 2026 ingestion frontier.

---

## Q2 2026 ingestion frontier

Fetch and filter are complete for April-June 2026 across arXiv cs.SD/eess.AS/cs.CL and the
available ACL Anthology 2026 material.

| Status | Count |
|---|---:|
| Ingested | 160 |
| Accepted, held | 2 |
| Accepted, re-dated into Q2 (2026-11-07) | 1 |
| Awaiting human triage | 0 |
| Rejected | 62 |

The Q2 sweep closed on 2026-10-31 with the tenth round (18 papers; counts by canonical
`published_date`). Held by user decision: `2606.12940` (ICML 2026) and `2606.13006` (IJCAI 2026),
which the peer-reviewed-version rule will re-date to Q3. On 2026-10-31 `2606.17126` was re-dated
to its IEEE TASLP Date of Publication (2026-06-19, stays Q2) and ingested as a journal page, and the
ISCSLP challenge proposal `2606.21933` was rejected. The Q4 2025 stragglers PACC `2605.18001` and
`2605.25504` are now included in the completed Q4 integration. ICASSP, ASRU, and SLT remain
fetch-coverage gaps; Interspeech 2026 was fetched from ISCA with dedup on 2026-11-01. The ingest procedure is
`docs/ingest-protocol.md`; quarter-specific state is in `Q3_2026_INGESTION_SESSIONS.md`.

---

## Repository and setup state

- Infrastructure repository: `main` and `work/ingest` in sync at the 2026-11-11 ingest wrap-up
  (see `git log`). The content repository was not touched on 2026-11-07 to 2026-11-11 (no pages
  written); `main` carries the 2026-11-08 peer-reviewed migration (`844fb57`).
- Ingest sessions write to the content-ingest worktree:

```bash
export SPEECH_WIKI_CONTENT_DIR=/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content-ingest
```

  Integration sessions use the `speech-generation-wiki-content-integrate` worktree instead.

Do not write through the infra repository's `wiki/` submodule.

---

## Infrastructure summary

Available fetchers cover arXiv, ACL Anthology, ISCA/Interspeech, and OpenReview. The pipeline
health suite currently implements agent, ingest, integrate, render, and reconciliation checks.
Planned work includes fetch, parse, and corpus modules; generated reporting; computed static
counts; and hook integration. See `BACKLOG.md` for the authoritative task list.
