# Backlog

## Ingest [P0 · in-progress]

Resume standard corpus ingest and clear the integration backlog.

- [ ] Run dedup pass on 56 OpenReview papers (ICLR 2025: 13, NeurIPS 2025: 16, ICLR 2026: 27) — check title collisions against existing corpus before filtering; proceedings ID is canonical over arXiv
- [ ] Run integration pass 12 — 30 papers pending from 2026-06-16: 2301.11325, 2301.12503, 2305.15255, 2312.01479, 2312.15821, 2401.07333, 2402.13236, 2404.03204, 2406.00654, 2406.05551, 2408.02622, 2411.09943, 2411.17607, 2411.18803, 2412.04724, 2502.18924, 2503.14345, 2504.02407, 2504.10344, 2505.02625, 2505.09558, 2505.13000, 2505.14648, 2506.10274, 2506.13053, 2506.16381, 2507.23159, 2508.04195, 2510.07838, 2511.15848
- [ ] Resume standard ingest from 2509.04093 — 699 papers ready; chronological order (Aug 2025 → Dec 2025 → 2026); show selection, ingest 2 at a time with quality check

## Content Stage Implementation [P0 · planned]

Execute the redesigned three-stage pipeline in the wiki content repo.

- [ ] Migrate wiki/concepts/_evidence/ → wiki/_claims/ (wiki content repo filesystem change)
- [ ] Migrate existing 24 YAML digests to new rich schema (structural: add evidence_role, current_role, method_family; convert flat claim strings to objects with role/source/confidence)
- [ ] Build YAML validation script (scripts/wiki/validate_concept_evidence.py): required keys present, paper IDs cross-referenced against metadata, claim IDs unique within file, paper_count matches entry count; will be absorbed into the wiki check suite YAML module once that exists
- [ ] Run first render pass: regenerate all 24 concept pages with new template
- [ ] Generate first evidence dossiers for core concepts (flow-matching, autoregressive-codec-tts, neural-codec, zero-shot-tts, evaluation-metrics)

## Wiki Quality Improvements [P1 · planned]

- [ ] Fix paper index wikilink format (wiki/papers/index.md: inconsistent plain IDs → [[id]] links)
- [ ] Run page quality audit — 5 issue classes across 225+ pages: adoption claims in Field Significance, wrong abstract callout types, field_significance.type mismatches, citation verb phrases in Context sections, spurious self-supervised-speech tags; wiki check suite lint module handles the automatable subset, targeted editorial review for foundational and high-significance pages
- [ ] Repair flow-matching.yaml (malformed YAML: paper entries appear after trend_notes instead of under papers)
- [ ] Backfill missing claim section citations (*(§N.N)* format); prioritize foundational and high-significance papers; track completion status per page (complete / partial / missing)
- [ ] Migrate 2 wiki pages from arXiv to canonical conference IDs: 2510.00981 → iclr-2026-kYkfCs4ZAH (FlexiCodec), 2508.16790 → neurips-2025-wHsFqmM1rp (TaDiCodec); do after integration pass to avoid broken links
- [ ] Write wiki/about.md: 3-repo structure, project philosophy, ingest pipeline overview, how to contribute or report errors; link from wiki/index.md

## Infrastructure [P1 · planned]

- [ ] Build dedup check script (scripts/discover/dedup_check.py): title-based collision detection after each fetch; canonical priority proceedings > arXiv
- [ ] Fix static counts — hardcoded paper/concept counts in wiki/index.md, overview.md, venue pages, and evidence digests go stale each ingest pass; decide approach (computed-at-build vs. integration-pass checklist) and implement
- [ ] Extend fetch coverage — add ICASSP, ASRU, and SLT fetchers (listed in CLAUDE.md coverage but no scripts exist yet)
- [ ] Resolve parse quality review: 8 papers flagged for offline PDF spot-check (raw/parsed/parse_quality_review.md); blocked on user results before --force re-runs

## Wiki Check Suite [P1 · planned]

Single command (`python scripts/wiki/check.py`) that runs all wiki correctness checks — the equivalent of a test suite for the wiki content repo. Each check category is a module; they compose into one exit-0-or-1 result suitable for a pre-commit or pre-push hook.

- [ ] Build scripts/wiki/check.py: entry point; discovers and runs all check modules; exit 0 on clean, 1 with per-module failure report; --module flag to run a subset
- [ ] Build integrity module (scripts/wiki/checks/integrity.py): metadata↔page consistency, ingested-but-missing-page, required sections present, broken wikilinks, count mismatches across wiki/index.md, wiki/overview.md, venue pages
- [ ] Build YAML schema module (scripts/wiki/checks/yaml_schema.py): _claims/ keys, paper ID cross-ref against metadata, claim ID uniqueness, paper_count match; absorbs validate_concept_evidence.py from Content Stage Implementation
- [ ] Build lint module (scripts/wiki/checks/lint.py): adoption claims in Field Significance, wrong callout types, citation verb phrases in Context sections, spurious self-supervised-speech tags, field_significance.type red flags
- [ ] Wire into pre-commit or pre-push hook in wiki content repo

## Dashboard [P2 · deferred]

Operational health checks for the living review.

- [ ] Build scripts/wiki/dashboard.py (checks: corpus state, wiki integrity, concept evidence health, claim graph health, reassessment queue)
- [ ] Output to STATUS_DASHBOARD.md

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
