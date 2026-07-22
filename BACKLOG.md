# Backlog

## Ingest [P0 · in-progress]

Resume standard corpus ingest and clear the integration backlog.

- [x] Run dedup pass on 56 OpenReview papers (ICLR 2025: 13, NeurIPS 2025: 16, ICLR 2026: 27) — 8 collisions found (all ingested arXiv copies); arXiv records marked `is_duplicate`, proceedings records marked `ingested` with `wiki_page_id` pointers *(completed 2026-06-29)*
- [x] Pre-Q3 batch — 16 papers (NAACL 2025, ICLR 2025, workshop venues: COLING, CHiPSAL, ComputEL, NoDaLiDa) ingested 2026-06-29; corpus at 354 pages *(completed 2026-06-29)*
- [x] Ingest 2 deferred ICLR 2025 papers: `iclr-2025-hQvX9MBowC` (DiTTo-TTS), `iclr-2025-uxDFlPGRLX` (FlowDec) *(completed 2026-06-30)*
- [x] Continue chronological ingest of remaining accepted papers through end of Q3 2025 — COMPLETE 2026-07-17 (session 13): 364 ingested, 0 remaining, 107 rejected, 471 total in scope; corpus reached 592 pages, 0 errors corpus-wide throughout; full session log archived at `docs/records/2026-07-17-q3-2025-ingestion-sessions.md` *(completed 2026-07-17)*
- [ ] Continue chronological ingest of Q4 2025 (October–December) accepted papers — 51 ingested, 133 remaining, 63 rejected as of 2026-07-18 (session 14); protocol and cadence at `Q4_INGESTION_SESSIONS.md`

## Content Stage Implementation [P0 · in-progress]

Execute the redesigned three-stage pipeline in the wiki content repo. Integration agent spec and schema are complete (2026-06-24); design doc at `docs/design/integration-agent.md`. `_claims/` directory exists; `concepts/_evidence/` removed. YAML validation is covered by the Pipeline Health Suite integrate module (`scripts/checks/integrate.py`, built 2026-07-15).

- [ ] Run integration passes for all supported concepts — per-concept, two-phase model. Dedicated session note at `Q3_INTEGRATION_SESSIONS.md` (scope: all papers published before Q4 2025, across all 23 concepts). **`flow-matching`, `speech-to-speech`, `rlhf-speech`, `evaluation-metrics`, and `disentanglement` fully closed** (Phase 1 + Phase 2) as of 2026-07-22: 97/97, 60/63, 29/29, 285/286, and 100/100 Q3-scoped papers respectively (the 3-paper gap on speech-to-speech and the 1-paper gap on evaluation-metrics are both intentional — papers correctly excluded for lacking a speech-generation stage / being off-topic). `evaluation-metrics` is the largest concept closed so far (285 papers, 17 method_families, 31 claim_clusters); `disentanglement` is the second largest (100 papers, 10 method_families, 17 claim_clusters). 18 other concepts have not started — no `_claims/` YAML exists for them yet. Q3-scoped `papers_not_in_any_yaml`: 157 as of 2026-07-22 (down from 205 on 2026-07-21, 411 on 2026-07-20)
- [x] Run first render pass: generated full concept pages and evidence dossiers for both currently supported `_claims/` concepts (`flow-matching`, 97 papers; `speech-to-speech`, 60 papers), updated the concept catalog and render log, and verified source coverage and provenance *(completed 2026-07-20)*
- [ ] Generate first evidence dossiers for core concepts (flow-matching, autoregressive-codec-tts, neural-codec, zero-shot-tts, evaluation-metrics)

## Wiki Quality Improvements [P1 · planned]

- [x] Run review pass on all papers flagged by `health_check.py --module ingest` — 138 papers reviewed across Interspeech 2025, ACL/EMNLP/NAACL/COLING, and arXiv; 0 errors corpus-wide; record at `docs/records/2026-06-29-health-check-review-pass.md` *(completed 2026-06-29)*
- [ ] Manual verification pass — open PDFs and spot-check the 68 flagged items (metric corrections, causal claims, "first" claims, specific quantitative ranges) recorded in `docs/records/2026-06-29-health-check-review-pass.md`; correct any confirmed errors in the wiki pages; prioritise metric corrections first
- [ ] Run page quality audit — adoption claims in Field Significance, wrong abstract callout types, field_significance.type mismatches, citation verb phrases in Context sections, spurious self-supervised-speech tags; the automatable subset is handled by the Pipeline Health Suite ingest module; this item covers remaining targeted editorial review for foundational and high-significance pages
- [ ] Improve in-corpus citation rendering: (a) wikilinks should render as `[[id|Name]]` so Quartz displays them as bracketed `[Name]` anchors consistent with academic citation style, not bare inline text; (b) named models and systems (WaveNet, VITS, HiFi-GAN, etc.) that have a corpus page should link directly via `[[id|WaveNet]]` rather than appearing as prose followed by a separate paper ID reference ("WaveNet [2609.03499]" → `[[2609.03499|WaveNet]]`); update ingest agent spec and writing style guide, then run a targeted fix pass on high-traffic pages first
- [x] Standardize `related_concepts` frontmatter serialization across all paper pages — found 2026-07-19 while building a Q3-scoped per-concept integration coverage table. Three different YAML serializations coexisted across the 640 pages, with no clean before/after cutover (23 separate ingest days each contained a mix, so it was per-invocation agent drift, not a one-time format change): bracket unquoted `[flow-matching, zero-shot-tts]` (275 pages), bracket quoted `["flow-matching", "zero-shot-tts"]` (348 pages), and YAML block-list (`related_concepts:` / `  - flow-matching`) (6 pages). All three were valid YAML and parsed identically under `yaml.safe_load` — `health_check.py` and `corpus_summary.py` already parsed the frontmatter as real YAML, so pipeline tooling was unaffected; the risk was any future hand-rolled script or manual grep assuming a single format (an ad-hoc script built for the coverage table above undercounted flow-matching's Q3-scoped paper count by roughly half before the bug was found). **Resolved 2026-07-20**: chose bracket-unquoted as canonical, consistent with `task`/`architecture`, which already use unquoted brackets corpus-wide with no drift. (a) Documented under a new "Frontmatter List Formatting" section in `docs/content.md` — the field lives in wiki page frontmatter, not `raw/metadata/` JSON, so the note sits with the page templates rather than `docs/schemas/metadata.md`. (b) `scripts/normalize_related_concepts.py` rewrote the 354 non-canonical pages (348 quoted + 6 block-list) to bracket-unquoted form, touching only the `related_concepts` line(s) per file; verified via `git diff` that no other content changed, and `health_check.py` (all modules) passed with 0 errors before and after. (c) Updated `speech-generation-ingest-agent`, `speech-generation-lightweight-ingest-agent`, and `speech-generation-review-agent` SKILL.md specs with an explicit "never quote, never block-list" instruction next to the allowed-slugs list.
- [x] Repair flow-matching.yaml (malformed YAML: paper entries appear after trend_notes instead of under papers) — verified 2026-07-18: not actually malformed, top-level key order is correct (`concept` → `last_updated` → `paper_count` → `papers` → `claim_clusters` → `method_families` → `reassessment_queue` → `open_questions` → `trend_notes`); this item was stale *(verified resolved 2026-07-18)*
- [ ] Migrate 8 wiki pages from arXiv to canonical conference IDs (dedup pass 2026-06-29; OpenReview metadata already updated with `wiki_page_id` pointers); do after integration pass to avoid broken links:
  - 2411.19842 → iclr-2025-4YpMrGfldX (Scaling Transformers for Low-Bitrate Speech Coding)
  - 2409.00750 → iclr-2025-ExuBFYtCQU (MaskGCT)
  - 2409.06666 → iclr-2025-PYmrUQmMEw (LLaMA-Omni)
  - 2502.07243 → iclr-2025-anQDiQZhDP (Vevo)
  - 2501.01957 → neurips-2025-8PUzLga3lU (VITA-1.5)
  - 2503.14345 → neurips-2025-MVlKSYR7HX (MoonCast)
  - 2510.00981 → iclr-2026-kYkfCs4ZAH (FlexiCodec)
  - 2508.16790 → neurips-2025-wHsFqmM1rp (TaDiCodec)
- [ ] Write wiki/about.md: 3-repo structure, project philosophy, ingest pipeline overview, how to contribute or report errors; link from wiki/index.md

## Infrastructure [P1 · planned]

- [ ] Extend fetch coverage — add ICASSP, ASRU, and SLT fetchers (listed in AGENTS.md coverage but no scripts exist yet)
- [ ] Resolve parse quality review: 8 papers flagged for offline PDF spot-check (raw/parsed/parse_quality_review.md); blocked on user results before --force re-runs

## Pipeline Health Suite [P1 · in-progress]

Single command (`python scripts/health_check.py`) serving two roles: a test suite that validates pipeline outputs at each stage (run post-pass to catch problems before they accumulate), and a health dashboard that tracks overall knowledge base state. One module per stage, each independently runnable via `--module`; a `--report` flag writes `STATUS_DASHBOARD.md` from the combined output, replacing the standalone dashboard script. Serves as the source of truth for corpus counts — static counts in index.md and overview.md should be driven from this output rather than maintained manually.

- [x] Build scripts/health_check.py entry point: runs all modules or a named subset via `--module`; exit 0 on clean, 1 with per-module failure report; `--id` scopes ingest, `--concept`/`--phase` scope integrate, `--wiki-dir` overrides the wiki root *(completed 2026-06-19, extended 2026-07-15)*
- [x] Add agents module (`scripts/checks/agents.py`): validates the shared `AGENTS.md`/`CLAUDE.md` contract, six repository skills, Claude adapters, renderer naming, portable paths, and required references; runs in the default full suite and directly via `--module agents` *(completed 2026-07-20)*
- [ ] Add `--report` flag to the entry point: writes STATUS_DASHBOARD.md with per-module pass/fail summary, corpus counts, and health signals — not yet built; some older docs/backlog text referenced it as if it existed
- [ ] Build fetch module (scripts/checks/fetch.py): metadata JSON parses; required fields present (id, title, published_date, status, venue); status values in allowed set; no duplicate IDs across metadata files; title-based collision detection (canonical priority: proceedings ID > arXiv); absorbs the planned dedup check script
- [ ] Build parse module (scripts/checks/parse.py): accepted papers have local PDF in raw/papers/; parsed entries have paper.md; paper.md not suspiciously short (< 100 lines — flag for manual review); references.json has non-zero count (flag if 0, cross-reference against known exceptions in parse_quality_review.md); assets/ present if figures referenced in paper.md; metadata.json abstract non-null (flag if null)
- [x] Build ingest module (scripts/checks/ingest.py): frontmatter parses; required fields and sections present; controlled vocabulary values valid (field_significance.type, tasks, tags against vocabulary.md); claims have inline source citations (§N.N format); figure links point to existing assets; related_concepts slugs exist; wikilinks use [[id|Name]] format; paper appears in wiki/papers/index.md; Tier 2 stubs have citation stub callout *(completed 2026-06-19)*
- [ ] Extend the ingest module with a `related_concepts` completeness check (distinct from the slug-validity check above): cross-reference each paper's `task`/`architecture` frontmatter tags against `related_concepts` and flag papers missing an expected concept link. This is a known recurring ingest-agent bug (task/architecture tags dropped from `related_concepts` despite repeated prompt fixes — recurred 3x in session 6 alone) that prompting alone hasn't fixed; the integration agent's Phase 1 discovery trusts `related_concepts` with no fallback, so an undetected omission means a paper silently never enters a concept's claim graph
- [x] Build integrate module (scripts/checks/integrate.py): 26 checks across Phase 1 + Phase 2 (25 designed + `paper_id_is_string`, added after testing surfaced a float-coercion hazard on unquoted arXiv IDs); `--concept` (not `--id`) scopes to one YAML, `--phase` forces Phase 1/2; `config/health_check.yaml` added for the canonical concept registry and staleness threshold; `scripts/checks/_base.py` extended (`concept`, `phase` fields) and `health_check.py` output generalized (no longer hardcoded to ingest's `papers_checked` stat key); §2.1/§2.3/§2.5/§6/§8/§10 of `docs/design/pipeline-health-suite.md` reconciled with the actual implementation; tested clean against the real `flow-matching.yaml` and against injected-defect fixtures *(completed 2026-07-15)*
- [ ] Build render module (scripts/checks/render.py): concept pages exist for all _claims/ YAML files; required sections present on concept pages; evidence dossiers exist where expected; paper counts consistent between YAML and rendered page
- [ ] Build corpus module (scripts/checks/corpus.py): metadata status:ingested but missing wiki page; wiki page exists but no metadata (orphaned page); count mismatches across wiki/index.md, overview.md; broken wikilinks across all pages; this module's output is the authoritative source for corpus counts in STATUS_DASHBOARD.md
- [ ] Fix static counts — replace hardcoded paper/concept counts in wiki/index.md, overview.md, and evidence digests with values computed by the corpus module; run as part of `health_check.py --report` after each ingest or integration pass
- [ ] Wire into pre-commit or pre-push hook in wiki content repo

## On-Demand Venue Reports [P2 · deferred]

Venue pages (`wiki/venues/`) were removed from the automated ingest pipeline 2026-07-15 — auto-generated per-venue-year pages were mostly thin paper listings (e.g. "arXiv 2023" as an assortment of unrelated papers), while a handful of hand-enriched pages (e.g. "Interspeech 2025") showed real value once a venue has enough ingested papers to support genuine trend synthesis. Replace with an on-demand generator invoked by request for a specific venue-year, not auto-updated per ingest.

- [ ] Design an on-demand venue report generator (agent or script): input a venue + year, read all ingested papers for that venue-year from `wiki/papers/`, synthesise dominant themes/clusters (not just a paper listing) — similar quality bar to the existing `2025-interspeech.md` write-up
- [ ] Decide the trigger threshold (e.g. only venues with N+ ingested papers) so isolated arXiv preprints don't get a report
- [ ] Decide whether venue pages get linked back into `wiki/index.md` once the generator exists, and where

## Citation Leaderboard [P2 · deferred]

Quarterly snapshot pages ranking the top N most-cited papers in the corpus, updated each quarter to show ranking movement — new entries, risers, and fallers.

- [ ] Decide N (50 vs 100) and page structure: one rolling page (`wiki/reports/top-cited.md`) with historical tables, or one page per quarter (`wiki/reports/top-cited-YYYY-QN.md`) with a summary index
- [ ] Build `scripts/wiki/top_cited.py`: reads `raw/citation_index.json`, counts in-corpus citations per paper, ranks top N, emits a markdown table with columns: Rank, ▲▼ (delta vs previous quarter), Paper, Venue, Year, In-Corpus Citations
- [ ] Define quarterly snapshot format in `raw/citation_snapshots/YYYY-QN.json` so deltas can be computed across quarters without regenerating from scratch
- [ ] Generate first snapshot (label it with the current quarter at time of first run)
- [ ] Add to render pipeline or health_check.py so it can be regenerated on demand

## Dashboard [absorbed into Pipeline Health Suite]

`STATUS_DASHBOARD.md` is generated by `health_check.py --report`. No standalone dashboard script needed.

## Briefs [P2 · deferred]

Short, decision-oriented memos generated from the claim graph. Implement after claim layer is stable.

- [ ] Define brief template (stub in docs/content.md)
- [ ] Create wiki/briefs/ directory in wiki content repo
- [ ] Generate first briefs: flow-matching-vs-ar-codec-tts, tts-evaluation-metrics-that-matter, best-open-weight-zero-shot-tts

## Editorial Quality Pass [P2 · deferred]

Targeted quality upgrades for high-value pages. Blocked on Content Stage Implementation — generation tracking requires rendered concept pages to exist first.

- [ ] Add generation frontmatter tracking to concept pages and overview.md (model, date, infra commit)
- [ ] Run Opus quality pass on foundational paper pages (≥10 in-corpus citations: VITS, VALL-E, HiFi-GAN, Voicebox, EnCodec, WavLM)
- [ ] Run Opus quality pass on mature concept pages (≥15 papers; start with flow-matching, autoregressive-codec-tts)

## Tiered Wiki Pages [P2 · deferred]

Compress incremental papers to a single-paragraph summary as corpus scales; frontmatter retained for search and comparisons; promotable on citation gain. Define trigger criteria before starting.

- [ ] Define promotion/demotion criteria (candidate: 0 in-corpus citations after 6+ months, no concept back-link) and add tier field to wiki/index.md
- [ ] Build pruning agent or script to generate candidate list for user approval before any demotion
- [ ] Run initial tier assignment pass

## Corpus Scope Extension: Spoken Dialog Understanding [P2 · deferred]

Current scope test is subject-matter relevance to TTS/VC/SCA *generation*; this rejects pure understanding/tracking
papers (DST, diarization, ASR) even when they're architecturally part of the same spoken-dialog-agent stack
(2510.09424 DST accepted only via one-off user override, 2026-07-18 — see raw/review_queue.md). User wants to
eventually broaden the controlled vocabulary to cover spoken dialog agents beyond speech generation (e.g. a
`dialog-understanding` or similar concept/task term), so that already-accepted-and-parsed papers in this space can
be let into the corpus on their own terms instead of needing a scope override each time. Not scoped yet — needs a
vocabulary design decision (docs/schemas/vocabulary.md) before any filter/ingest behavior changes.

- [ ] Define the new controlled-vocabulary term(s) for spoken-dialog-understanding tasks (DST, turn-taking, intent
      tracking) distinct from TTS/VC/SCA generation
- [ ] Decide whether this is a new `task` value, a new `concept`, or both
- [ ] Re-review papers previously rejected/flagged under the FAMA/MLC-SLM pattern once the vocabulary exists, to see
      which would now qualify on their own merits (not retroactively, just going forward)
