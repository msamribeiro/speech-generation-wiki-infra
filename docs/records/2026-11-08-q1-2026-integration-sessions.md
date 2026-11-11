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

3. Start `subjective-evaluation` Phase 1 with the first 20 IDs listed below.
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

**Progress:** 9/52. Three invocations have written nine entries; 43 remain.

**Batch 1 — next (20 IDs, frozen order):**

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
