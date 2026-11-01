# Archive

Completed features, moved here from BACKLOG.md when all tasks are done.
Each entry records the completion date, a prose summary of the outcome, and the completed task list.

---

## Q4 2025 Content Cycle [completed: 2026-11-01]

Complete the first quarter-over-quarter update after the closed Q3 synthesis program. Scope is
canonical `published_date` from `2025-10-01` through `2025-12-31`, inclusive. The full operating
record is archived at
`docs/records/2026-11-01-q4-2025-integration-and-synthesis-sessions.md`.

- [x] Phase 1 integration — add every eligible Q4 paper to each applicable concept YAML in
  oldest-first batches of at most 20 papers per concept. Baseline: 174 non-Tier-2 Q4 paper pages,
  172 with canonical concept assignments, 22 affected concepts, and approximately 660 missing
  concept-paper entries
- [x] Phase 2 synthesis — after each concept's Q4 Phase 1 queue closes, update claim clusters,
  method families, reassessment items, open questions, and trend notes from the complete YAML
- [x] Validate the completed Q4 claim graphs — concept-scoped checks after every pass, followed by
  the corpus-wide integrate health check and an exact Q4 candidate-versus-YAML closure audit
- [x] Correct late Q4 Phase 1 drift discovered after the original closure — import the two late
  proceedings-dated pages (`2605.18001`, `2605.25504`), sync the later `singing` and `neural-codec`
  concept tags on `2512.14653` and `2512.00451`, add 8 paper-concept entries across 7 concepts,
  and close the current exact audit at 173 eligible non-Tier-2 pages with 0 missing memberships
- [x] Run targeted corrective Phase 2 synthesis for `gan-vocoder`, `voice-conversion`,
  `subjective-evaluation`, `emotion-synthesis`, `diffusion-tts`, `singing`, and `neural-codec`
- [x] Run bounded corrective reconciliation for cluster changes caused by the late Q4 evidence;
  preserve the finalized original Q4 run as the audit trail and refresh derived evidence for the
  automatic-judge, multiattribute-disentanglement, semantic–acoustic-hierarchy, and
  multidimensional-evaluation broader claims
- [x] Run `2025-Q4` cross-concept reconciliation — generate deterministic candidates only after
  all concept integrations close; review in themed batches, obtain explicit human decisions, and
  finalize with no pending candidates before using new relationships downstream
  - [x] Generate the deterministic human-review run: 3,946 pending candidates across eight themes;
    the reviewed Q3 registry remained byte-for-byte unchanged
  - [x] Review all eight themes, beginning with evaluation, and resolve the Q4-induced derived
    evidence drift in existing broader claims through explicit human decisions; evaluation is
    complete with 98 accepted, 624 rejected, and 0 deferred decisions across 722 candidates; seven
    themes and 3,224 candidates remained after evaluation; efficiency is now complete with 28
    accepted, 129 rejected, and 0 deferred decisions across 157 candidates, leaving six themes and
    3,067 candidates; speaker triage is complete with 67 proposed acceptances, 889 proposed
    rejections, and 0 deferrals; the first three speaker bundles approved 47 decisions covering
    reference conditioning, cross-lingual identity/accent, disentanglement/attribute leakage,
    singing timbre/pitch transfer, and speaker trade-offs/robustness/metrics; all 889 audited speaker
    rejections are applied, closing the theme with 67 accepted and 889 rejected decisions and
    leaving five themes and 2,111 candidates pending overall; the complete 677-candidate
    controllability is complete with 111 accepted, 566 rejected, and 0 deferred decisions; its 61
    new direct relationships and 50 carry-forward decisions preserve existing reviewed authority
    without duplicate registry entries; robustness review has started with 3 existing-authority
    carry-forwards, 6 multilingual/generalization relationships, and 6 low-resource/representation
    transfer relationships approved; the text/pronunciation/alignment bundle added 4 acceptances
    and 2 rejections; the remaining 133 robustness candidates are now audited into 21 proposed
    acceptances across four semantic bundles and 112 proposed rejections across two categories;
    robustness is complete with 40 accepted, 114 rejected, and 0 deferred decisions; three themes
    and 1,280 candidates remain; all 1,014 codecs/language-modeling candidates are now audited into
    101 proposed acceptances across nine broad bundles and 913 proposed rejections across two
    categories; all 101 proposed acceptances across the nine broad bundles are approved, including
    20 existing-authority carry-forwards and 81 new direct relationships; all 913 audited
    rejections are applied, closing codecs/language modeling and leaving streaming/agents (138)
    and post-training (128), 266 candidates total; streaming/agents is now audited into 42 proposed
    acceptances across six broad bundles and 96 proposed rejections across two categories; the 9
    existing-authority carry-forwards, 8 incremental-reasoning/latency links, 8 explicit-interaction/
    turn-taking links, 5 unified/low-rate-interface links, 5 interaction-evaluation/context links,
    and 7 Q4-strengthened full-duplex links are approved; the 96 categorized rejections are also
    applied, closing streaming/agents at 42 accepted and 96 rejected; post-training is audited into
    51 proposed acceptances across six broad bundles and 77 proposed rejections across two
    categories; the 28 existing-authority carry-forwards are approved without duplicate registry
    entries; the 5 post-training capability extensions are approved, adding four members to the
    preference-post-training synthesis and one direct supports link; the 4 preference-data and
    reward-control links are approved, adding three unique qualifying members to the synthesis;
    the 9 reward-trade-off and evaluator-limit links are approved as new direct relationships;
    the 4 speech-text capability and instruction-adaptation links are approved as new direct
    relationships; the final guidance/control trade-off link is approved; all 51 proposed
    acceptances are resolved; the final 44 Q3 agent scope-gap reaffirmations and 33 low-semantic-
    overlap rejections are applied, closing post-training at 51 accepted and 77 rejected and the
    complete Q4 run at 538 accepted, 3,408 rejected, 0 deferred, and 0 pending
  - [x] Finalize and validate the run with no pending candidates
- [x] Regenerate every stale concept Overview/In Depth pair from the Q4-updated YAMLs; include the
  still-missing production pairs if their evidence supports useful synthesis. Progress:
  `gan-vocoder`, `voice-conversion`, `subjective-evaluation`, `emotion-synthesis`, `diffusion-tts`,
  `singing`, `neural-codec`, `evaluation-metrics`, `zero-shot-tts`, `spoken-language-model`,
  `speech-to-speech`, `autoregressive-codec-tts`, `multilingual-tts`, and
  `self-supervised-speech`, `flow-matching`, `prosody-control`, `streaming-tts`, and `rlhf-speech`
  plus `speaker-adaptation`, `disentanglement`, `instruction-conditioned-tts`, and
  `transformer-enc-dec-tts` fully regenerated through 2026-11-01. All 22 existing pairs are
  current; `fine-tuning` now has its first evidence-bounded production pair, closing concept
  rendering at 23/23 current pairs.
- [x] Regenerate the field overview from all 23 concept YAMLs and the human-approved reconciliation
  registry, deduplicating linked claims and paper evidence while preserving local caveats
  *(completed 2026-11-01: 668 unique papers, 2,892 memberships, 444 local clusters, 373 approved
  direct relationships, and 11 approved broader claims; render health 0 errors/0 warnings)*
- [x] Freeze the retrospective `2025-Q4` snapshot and publish the Q4 quarterly report; validate
  source digests, cutoff semantics, provenance, indexes, and supersession rules *(completed
  2026-11-01: 668 included papers, 497 baseline, 171 Q4 activity; snapshot and report validators
  pass; digest `sha256:97ebbcfe40a97bc05208e9c8d7209c88a77225485310e425716d83d7f5af3b4c`)*


---

## Cross-Concept Synthesis and Temporal Reporting [completed: 2026-09-13]

Built and validated the first complete cross-concept and temporal-reporting cycle over all 23 Q3
concept graphs. The rollout added canonical publication dates, an advisory reconciliation audit,
explicit human-review authority, a reviewed relationship registry, an immutable retrospective Q3
snapshot, a 23-concept field overview, a snapshot-backed Q3 report, and guarded trend/venue report
foundations. The full record is archived at
`docs/records/2026-09-13-cross-concept-synthesis-and-temporal-reporting.md`.

- [x] Add reconciliation, snapshot, temporal-reporting, and generation-provenance contracts
- [x] Backfill and validate 2,226 canonical publication dates without semantic YAML changes
- [x] Score all 78,475 cross-concept pairs and preserve 2,049 review candidates deterministically
- [x] Correct the initial agent-only adjudication and obtain human dispositions for all 110 proposed acceptances
- [x] Finalize 49 human-approved direct relationships and 11 human-approved broader claims
- [x] Freeze the immutable retrospective `2025-Q3` snapshot over 497 unique papers and 406 local clusters
- [x] Regenerate the field overview from all 23 concepts with deduplicated broader synthesis
- [x] Publish the snapshot-backed Q3 2025 report with activity, evidence change, and adoption separated
- [x] Require at least two ordered snapshots for trend reports and fail clearly with only Q3
- [x] Add canonical inclusive venue selection and an evidence-backed anti-inventory quality gate
- [x] Validate tests, health, compatibility, provenance, snapshot/report binding, and 1,386 synthesis-page wikilinks
- [x] Record future triggers: reconcile after each quarterly integration or other large integration round;
      publish a trend only after a second comparable snapshot; publish venue reports only on explicit
      request when the selected evidence passes the synthesis gate

## Ingest & Integration Pipeline [completed: 2026-06-17]

Built the full multi-agent ingest architecture. Per-paper ingest agent writes one wiki page with
no cross-paper work; integration agent handles concept YAML updates; lightweight stub agent handles
Tier 2 citation-discovery papers. Ingested all 338 papers across sessions 12–47: 176 standard
papers, 96 Tier 1 CD full pages, 66 Tier 2 CD stubs. Ran 11 integration passes covering 276
papers. Architecture since redesigned (2026-06-18) into the three-stage ingest → integrate →
render pipeline documented in docs/content.md.

- [x] Build speech-generation-ingest-agent (per-paper, paper-scoped)
- [x] Build speech-generation-integration-agent (cross-paper, concept YAML)
- [x] Build speech-generation-lightweight-ingest-agent (Tier 2 stubs)
- [x] Build speech-generation-filter-agent (relevance scoring)
- [x] Separate ingest from integration (session 14 — no concept pages during ingest)
- [x] Ingest 176 standard papers (sessions 12–46)
- [x] Ingest 96 Tier 1 CD papers (2026-06-16)
- [x] Ingest 66 Tier 2 CD stubs (2026-06-17)
- [x] Run integration passes 1–11 (276 papers integrated; all 24 concept stubs seeded)

---

## Parse Pipeline Implementation [completed: 2026-06-08]

Built the full PDF-to-markdown parsing pipeline using Docling (chosen over the original
GROBID+Marker stack for better table/figure handling and single-dependency setup). Converted
all 875 standard papers in 30 batches with 0 failures, then all 162 citation-discovery papers
in 5 further batches. Multiple `_REFS_HEADER_RE` patches applied for non-standard reference
headers. Parse design documented in docs/design/parsing-pipeline.md.

- [x] Build convert_paper.py (single-paper Docling converter with MPS/CPU fix)
- [x] Build batch_convert.py (batch orchestrator with --ids, --force, --retry-failed, --status)
- [x] Build make_batch_queue.py (queue generation with --sync flag, --batch-size 40)
- [x] Parse 875 standard papers (batches 1–13, 2026-05-22 → 2026-06-06); 0 failures
- [x] Parse 162 citation-discovery papers (batches 14–18, 2026-06-08); 0 failures
- [x] Apply _REFS_HEADER_RE patches (French headers, numbered Bibliography, letter-prefix headings)
- [x] Rebuild citation index: 21,262 entries, 652+50 merges, 4 override groups

---

## Corpus Cleanup [completed: 2026-06-18]

Reorganised `docs/` into a coherent structure (stage docs at root, `design/`, `schemas/`, `records/`),
moved all one-off session logs and analyses into `docs/records/` with date-prefixed filenames,
deleted the unused `scripts/filter/agent.py` (replaced by the Claude Code filter subagent), and
cleaned the repo root down to five files: `CLAUDE.md`, `README.md`, `STATUS.md`, `BACKLOG.md`, `ARCHIVE.md`.

- [x] Review docs/THOUGHTS_FOR_IMPROVEMENTS.md — archived to docs/records/2026-06-18-thoughts-for-improvements.md
- [x] Move root session files to docs/records/ with date-prefix (GPT suggestions, flow-matching experimental, action plan, schema redesign)
- [x] Archive INGEST_OPT_EXPERIMENT.md → docs/records/2026-05-29-ingest-opt-experiment.md
- [x] Archive WIKI_USES.md → docs/records/2026-05-27-wiki-uses.md
- [x] Delete scripts/filter/agent.py (unused; replaced by speech-generation-filter-agent subagent)
- [x] Update all references to moved/deleted files across docs/, agent specs, and scripts/

---

## Wiki Structural Fixes & Review Agent [completed: 2026-06-19]

Resolved all structural errors surfaced by the Pipeline Health Suite ingest module. Quoted 327
unquoted `id:` fields in paper frontmatter (arXiv float-parse bug). Fixed 191 bare ID cells and
193 plain title cells in `wiki/papers/index.md` to use `[[id]]` wikilinks and `[title](papers/id.md)`
markdown links; removed 1 blank row breaking table rendering. Added `_check_index_document()` to
the ingest health module and patched both ingest agents to strip blank rows from the index table
and always emit quoted IDs going forward. Added `> [!info] Citation Stub` callout to all 65 Tier 2
pages and updated the lightweight ingest agent to emit it on all future writes. Wrote the
`speech-generation-review-agent` spec — a targeted quality review agent that audits any existing
Tier 1 page against the full expected page template, corrects frontmatter, adds missing Field
Significance and Claims sections with `*(§N.N)*` citations, and evaluates figures.

- [x] Quote all `id:` fields in wiki paper frontmatter — 327 files patched; both ingest agents updated to always emit quoted id; blank-line stripping added to index table write in both agents
- [x] Fix paper index wikilink format — 191 ID cells → `[[id]]`, 193 plain titles → `[title](papers/id.md)`, 1 blank row removed; `_check_index_document()` added to health_check ingest module
- [x] Add `[!info] Citation Stub` callout to all Tier 2 paper pages — 65 pages patched retroactively; lightweight ingest agent updated to emit callout on all future writes; health check updated from `[!note]` → `[!info]`
- [x] Write speech-generation-review-agent spec — validates all sections against a complete expected template, corrects frontmatter, adds missing Field Significance and Claims with inline citations, evaluates figures; designed for reuse with any model

---

## Documentation Restructure [completed: 2026-06-18]

Split the monolithic CLAUDE.md (~400 lines mixing contract, templates, and workflows) into a
thin operating contract (~134 lines) plus four stage-specific docs in `docs/`. Introduced
BACKLOG.md and ARCHIVE.md for structured feature tracking. Redesigned the content stage from
a two-pass (ingest + integrate) pipeline to a three-stage pipeline (ingest → integrate → render),
with `wiki/_claims/{slug}.yaml` as the single source of truth for all generated wiki pages.
Wrote the new render agent spec; updated the integration agent to write YAML only; fixed
ingest agent scope statement, duplicate check, figure selection order, and index wikilink format.

- [x] Create BACKLOG.md + ARCHIVE.md
- [x] Write docs/schemas/metadata.md
- [x] Write docs/schemas/vocabulary.md
- [x] Write docs/schemas/claims.md
- [x] Write docs/fetch.md
- [x] Write docs/parse.md
- [x] Write docs/content.md
- [x] Rewrite CLAUDE.md as thin overview (~134 lines)
- [x] Update speech-generation-integration-agent.md (YAML only; removed page-writing steps)
- [x] Fix speech-generation-ingest-agent.md (scope statement, generation_history, figure selection order, duplicate check, index wikilink format)
- [x] Write speech-generation-render-agent.md (new)
