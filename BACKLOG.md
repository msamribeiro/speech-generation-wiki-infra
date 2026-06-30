# Backlog

## Ingest [P0 · in-progress]

Resume standard corpus ingest and clear the integration backlog.

- [x] Run dedup pass on 56 OpenReview papers (ICLR 2025: 13, NeurIPS 2025: 16, ICLR 2026: 27) — 8 collisions found (all ingested arXiv copies); arXiv records marked `is_duplicate`, proceedings records marked `ingested` with `wiki_page_id` pointers *(completed 2026-06-29)*
- [x] Pre-Q3 batch — 16 papers (NAACL 2025, ICLR 2025, workshop venues: COLING, CHiPSAL, ComputEL, NoDaLiDa) ingested 2026-06-29; corpus at 354 pages *(completed 2026-06-29)*
- [x] Ingest 2 deferred ICLR 2025 papers: `iclr-2025-hQvX9MBowC` (DiTTo-TTS), `iclr-2025-uxDFlPGRLX` (FlowDec) *(completed 2026-06-30)*
- [ ] Continue chronological ingest of remaining accepted papers through end of Q3 2025 (232 remaining as of 2026-06-30) — 8 ingested 2026-06-30 (DiVISe, BnTTS, Prompt-Guided Selective Masking Loss, ESPnet-SpeechLM, ESPnet-SDS, Behavior-SD + the 2 ICLR papers above); next: `2025.iwsds-1.11`, `2025.iwsds-1.27`, `2507.06235`, `2505.15772`, then remaining pre-Q3, then Q3 2025 (Jul–Sep) proper

## Content Stage Implementation [P0 · planned]

Execute the redesigned three-stage pipeline in the wiki content repo. Integration agent spec and schema are complete (2026-06-24); design doc at `docs/design/integration-agent.md`. `_claims/` directory exists; `concepts/_evidence/` removed. YAML validation is covered by the Pipeline Health Suite integrate module (`docs/records/2026-06-24-integrate-health-check-design.md`).

- [ ] Run integration passes for all supported concepts — per-concept, two-phase model; flow-matching prototype exists, all others start from scratch; run Phase 1 across all ingested Tier 1 papers for each concept, then Phase 2 per concept
- [ ] Run first render pass: generate concept pages and evidence dossiers from `_claims/` YAML
- [ ] Generate first evidence dossiers for core concepts (flow-matching, autoregressive-codec-tts, neural-codec, zero-shot-tts, evaluation-metrics)

## Wiki Quality Improvements [P1 · planned]

- [x] Run review pass on all papers flagged by `health_check.py --module ingest` — 138 papers reviewed across Interspeech 2025, ACL/EMNLP/NAACL/COLING, and arXiv; 0 errors corpus-wide; record at `docs/records/2026-06-29-health-check-review-pass.md` *(completed 2026-06-29)*
- [ ] Manual verification pass — open PDFs and spot-check the 68 flagged items (metric corrections, causal claims, "first" claims, specific quantitative ranges) recorded in `docs/records/2026-06-29-health-check-review-pass.md`; correct any confirmed errors in the wiki pages; prioritise metric corrections first
- [ ] Run page quality audit — adoption claims in Field Significance, wrong abstract callout types, field_significance.type mismatches, citation verb phrases in Context sections, spurious self-supervised-speech tags; the automatable subset is handled by the Pipeline Health Suite ingest module; this item covers remaining targeted editorial review for foundational and high-significance pages
- [ ] Improve in-corpus citation rendering: (a) wikilinks should render as `[[id|Name]]` so Quartz displays them as bracketed `[Name]` anchors consistent with academic citation style, not bare inline text; (b) named models and systems (WaveNet, VITS, HiFi-GAN, etc.) that have a corpus page should link directly via `[[id|WaveNet]]` rather than appearing as prose followed by a separate paper ID reference ("WaveNet [2609.03499]" → `[[2609.03499|WaveNet]]`); update ingest agent spec and writing style guide, then run a targeted fix pass on high-traffic pages first
- [ ] Repair flow-matching.yaml (malformed YAML: paper entries appear after trend_notes instead of under papers)
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

- [ ] Extend fetch coverage — add ICASSP, ASRU, and SLT fetchers (listed in CLAUDE.md coverage but no scripts exist yet)
- [ ] Resolve parse quality review: 8 papers flagged for offline PDF spot-check (raw/parsed/parse_quality_review.md); blocked on user results before --force re-runs

## Pipeline Health Suite [P1 · planned]

Single command (`python scripts/health_check.py`) serving two roles: a test suite that validates pipeline outputs at each stage (run post-pass to catch problems before they accumulate), and a health dashboard that tracks overall knowledge base state. One module per stage, each independently runnable via `--module`; a `--report` flag writes `STATUS_DASHBOARD.md` from the combined output, replacing the standalone dashboard script. Serves as the source of truth for corpus counts — static counts in index.md, overview.md, and venue pages should be driven from this output rather than maintained manually.

- [ ] Build scripts/health_check.py: entry point; runs all modules or a named subset via `--module`; exit 0 on clean, 1 with per-module failure report; `--id <paper_id>` to scope fetch/parse/ingest checks to a single paper; `--report` flag writes STATUS_DASHBOARD.md with per-module pass/fail summary, corpus counts, and health signals
- [ ] Build fetch module (scripts/checks/fetch.py): metadata JSON parses; required fields present (id, title, published_date, status, venue); status values in allowed set; no duplicate IDs across metadata files; title-based collision detection (canonical priority: proceedings ID > arXiv); absorbs the planned dedup check script
- [ ] Build parse module (scripts/checks/parse.py): accepted papers have local PDF in raw/papers/; parsed entries have paper.md; paper.md not suspiciously short (< 100 lines — flag for manual review); references.json has non-zero count (flag if 0, cross-reference against known exceptions in parse_quality_review.md); assets/ present if figures referenced in paper.md; metadata.json abstract non-null (flag if null)
- [ ] Build ingest module (scripts/checks/ingest.py): frontmatter parses; required fields and sections present; controlled vocabulary values valid (field_significance.type, tasks, tags against vocabulary.md); claims have inline source citations (§N.N format); figure links point to existing assets; related_concepts slugs exist; wikilinks use [[id|Name]] format; paper appears in wiki/papers/index.md; Tier 2 stubs have citation stub callout
- [ ] Build integrate module (scripts/checks/integrate.py): full check set designed (25 checks across Phase 1 + Phase 2) — read `docs/records/2026-06-24-integrate-health-check-design.md` before implementing; uses `--concept` (not `--id`) to scope to one YAML; also update §6 of `docs/design/pipeline-health-suite.md` to replace the old thin stub; absorbs validate_concept_evidence.py from Content Stage Implementation
- [ ] Build render module (scripts/checks/render.py): concept pages exist for all _claims/ YAML files; required sections present on concept pages; evidence dossiers exist where expected; paper counts consistent between YAML and rendered page
- [ ] Build corpus module (scripts/checks/corpus.py): metadata status:ingested but missing wiki page; wiki page exists but no metadata (orphaned page); count mismatches across wiki/index.md, overview.md, venue pages; broken wikilinks across all pages; this module's output is the authoritative source for corpus counts in STATUS_DASHBOARD.md
- [ ] Fix static counts — replace hardcoded paper/concept counts in wiki/index.md, overview.md, venue pages, and evidence digests with values computed by the corpus module; run as part of `health_check.py --report` after each ingest or integration pass
- [ ] Wire into pre-commit or pre-push hook in wiki content repo

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

- [ ] Add generation frontmatter tracking to concept pages, venue pages, and overview.md (model, date, infra commit)
- [ ] Run Opus quality pass on foundational paper pages (≥10 in-corpus citations: VITS, VALL-E, HiFi-GAN, Voicebox, EnCodec, WavLM)
- [ ] Run Opus quality pass on mature concept pages (≥15 papers; start with flow-matching, autoregressive-codec-tts)

## Tiered Wiki Pages [P2 · deferred]

Compress incremental papers to a single-paragraph summary as corpus scales; frontmatter retained for search and comparisons; promotable on citation gain. Define trigger criteria before starting.

- [ ] Define promotion/demotion criteria (candidate: 0 in-corpus citations after 6+ months, no concept back-link) and add tier field to wiki/index.md
- [ ] Build pruning agent or script to generate candidate list for user approval before any demotion
- [ ] Run initial tier assignment pass
