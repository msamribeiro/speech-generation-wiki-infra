# Project Status

Last updated: 2026-09-20

The Q3 2025 content cycle is complete through integration, human-reviewed reconciliation,
retrospective snapshot, field rendering, and quarterly reporting. The active content priority is
the Q4 2025 cycle. Q2 2026 ingestion is queued behind that work.

---

## Current priorities

1. Complete Q4 2025 Phase 1 and Phase 2 integration across the affected concept graphs.
2. Validate the updated graphs, run Q4 cross-concept reconciliation, and obtain human decisions
   for accepted relationships.
3. Regenerate stale concept pages and the field overview.
4. If approved, freeze the Q4 snapshot and publish the Q4 retrospective report.
5. Resume Q2 2026 parsing and ingestion after the Q4 content cycle.

The multi-session operating record is `Q4_INTEGRATION_SESSIONS.md`.

---

## Corpus state

| Measure | Current value | Notes |
|---|---:|---|
| Metadata records | 1,628 | 908 ingested, 333 accepted, 43 review, 344 rejected |
| Published paper pages | 900 | Unique content pages; canonical-ID pointers explain the difference from metadata marked ingested |
| Active accepted + ingested corpus | 1,241 | Basis of `scripts/corpus_summary.py` |
| Parsed active papers | 1,025 | Includes ingested papers and accepted papers ready for ingest |
| Accepted and parsed, ready to ingest | 117 | 76 April 2026 and 41 May 2026 papers |
| Concept claim YAMLs | 23 | All canonical Q3 concepts represented |
| Concept paper entries | 2,555 | Includes six Q4 concepts complete through Phase 2 |
| Claim clusters | 413 | 288 strongly supported, 15 contested |
| Rendered concept pairs | 21/23 | `singing` and `fine-tuning` remain unrendered |
| Reconciliation state | 64 relationships, 11 broader claims | Human-approved Q3 authority plus preserved non-authoritative audit history |
| Published snapshots | 1 | Retrospective `2025-Q3` snapshot |
| Published quarterly reports | 1 | `reports/quarterly/2025-Q3.md` |

Live health baseline on 2026-09-20:

```text
integrate: PASS — global check 0 errors, 299 warnings; speech-to-speech Q4 Phase 2 check 0 errors, 28 accepted warnings; papers_not_in_any_yaml=184
render:    PASS — 0 errors, 7 warnings; 21 Overview/In Depth pairs
reconcile: PASS — 0 errors, 1 warning; 2 runs and 1 snapshot
```

Warnings are non-blocking and primarily reflect accepted method-family outliers, the two missing
concept render pairs, and preserved reconciliation audit history.

---

## Quarterly progress

| Quarter | Ingest | Integrate | Reconcile | Render / report |
|---|---|---|---|---|
| Q3 2025 and earlier | Complete | Complete: 23 concepts, 2,226 entries | Complete: human-reviewed | Complete: field overview, snapshot, and Q3 report; 21/23 concept pairs |
| Q4 2025 | Complete | **Active** | Pending integration | Pending reconciliation |
| Q1 2026 | Original chronological sweep complete | Not started | Not started | Not started |
| Q2 2026 | 5 ingested; 230 accepted; 18 review | Not started | Not started | Not started |
| Q3 2026 to date | 98 accepted; 21 review | Not started | Not started | Not started |

Five accepted Q1 2026 records are present in the live metadata after the later corpus top-up and
were not part of the bounded Q1 ingest closeout. Reconcile them when the ingestion frontier resumes.

---

## Active Q4 2025 content cycle

Canonical live audit as of 2026-09-20:

- 174 ingested, non-Tier-2 Q4 paper pages.
- 172 pages carry at least one canonical `related_concepts` assignment.
- 2 pages have no concept assignment and require an audit.
- 2 Tier 2 pages are excluded from integration.
- 161 Q4 papers currently appear in at least one applicable concept YAML.
- 22 concepts have Q4 work queued; `fine-tuning` has no current Q4 candidate.
- The outstanding workload is approximately 329 concept-paper entries. This is larger than the
  unique-paper count because one paper may contribute evidence to several concepts.

Largest Q4 queues:

| Concept | Q4 candidates | Already present | Queue |
|---|---:|---:|---:|
| subjective-evaluation | 73 | 73 | 0 |
| evaluation-metrics | 61 | 61 | 0 |
| zero-shot-tts | 59 | 59 | 0 |
| neural-codec | 56 | 56 | 0 |
| spoken-language-model | 46 | 46 | 0 |
| speech-to-speech | 34 | 34 | 0 |
| autoregressive-codec-tts | 33 | 2 | 31 |
| multilingual-tts | 31 | 1 | 30 |
| self-supervised-speech | 31 | 1 | 30 |
| voice-conversion | 29 | 0 | 29 |
| flow-matching | 30 | 2 | 28 |

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

The remaining 11 affected concepts have queues between 5 and 24 entries. Recompute live discovery
before each concept because canonical IDs, concept tags, or corrective reviews may change the
denominator.

---

## Q2 2026 ingestion frontier

Fetch and filter are complete for April-June 2026 across arXiv cs.SD/eess.AS/cs.CL and the
available ACL Anthology 2026 material.

| Status | Count |
|---|---:|
| Already ingested | 5 |
| Accepted, awaiting ingest | 230 |
| Awaiting human triage | 18 |
| Rejected | 49 |

Of the 230 accepted papers, 117 are currently parsed and ready to ingest; approximately 113 still
need parsing. ICASSP, ASRU, and SLT remain fetch-coverage gaps. The Q2 cadence and paper-level QC
contract remain in `Q2_INGESTION_SESSIONS.md`.

---

## Repository and setup state

- Infrastructure repository: `main` at `df5176b`; clean at the 2026-09-19 baseline inspection.
- Content repository: `work/integrate` at `872959f`; clean at the baseline inspection.
- The default wiki resolver points to a non-writable sibling checkout in the managed workspace.
  Use:

```bash
export SPEECH_WIKI_CONTENT_DIR=/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content-integrate
```

Do not write through the infra repository's `wiki/` submodule.

---

## Infrastructure summary

Available fetchers cover arXiv, ACL Anthology, ISCA/Interspeech, and OpenReview. The pipeline
health suite currently implements agent, ingest, integrate, render, and reconciliation checks.
Planned work includes fetch, parse, and corpus modules; generated reporting; computed static
counts; and hook integration. See `BACKLOG.md` for the authoritative task list.
