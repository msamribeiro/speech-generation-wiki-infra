# Project Status

Last updated: 2026-06-01 (session 22, schema and wiki design pass)

---

## Corpus state

| Step | Status | Notes |
|------|--------|-------|
| arXiv fetch (cs.SD + eess.AS) | ✅ Complete | 2025-08-01 → 2026-05-25. 504 + 70 re-scan = 574 written. |
| arXiv fetch (cs.CL) | ✅ Complete | Via OAI-PMH. Aug–Nov: 41; Dec–Feb: 32; Mar–May: 42. Total: 115 new. cs.CL re-scan deferred (low marginal yield vs. cost). |
| ISCA fetch (Interspeech 2025) | ✅ Complete | 128 + 12 re-scan = 140 papers written. |
| Deduplication (arXiv ↔ ISCA) | ✅ Complete | 11 duplicates resolved; ISCA is canonical. |
| ACL Anthology fetch (2025) | ✅ Complete | 14,669 scanned; 113 + 14 re-scan = 127 new written, 136 arXiv records enriched total. |
| Citation discovery fetch (targeted) | ✅ Complete | 5 papers fetched by arXiv ID via `--ids` flag: VALL-E, CosyVoice ×2, Seed-TTS, F5-TTS. |
| Keyword filter expansion | ✅ Complete | +11 terms added to `config/keyword_filter.yaml` (2026-05-25). See Infrastructure section. |
| Filter — batch 1 (May 12) | ✅ Complete | arXiv batch: 404 accepted, 31 review, 69 rejected. |
| Human review — batch 1 (May 19) | ✅ Complete | 31 resolved → 15 accepted, 16 rejected. |
| Filter — batch 2 (May 22) | ✅ Complete | ACL + cs.CL batch: 300 accepted, 39 review, 56 rejected. |
| Human review — batch 2 (May 22) | ✅ Complete | 39 resolved → 25 accepted, 14 rejected. |
| Duplicate resolution (arXiv ↔ ACL) | ✅ Complete | 1 additional duplicate found (2502.19732 → 2025.findings-emnlp.716). |
| Duplicate resolution — full corpus scan (May 28) | ✅ Complete | 15 total arXiv/proceedings duplicates resolved (including F5-TTS 2410.06885). Proceedings ID is canonical throughout. 6 parsed output dirs remapped. |
| Filter — batch 3 (May 25) | ✅ Complete | Re-scan + citation-discovery: 101 papers, 67 accepted, 7 review, 27 rejected (66% accept rate). |
| Human review — batch 3 | ✅ Complete | 7 resolved → 3 accepted, 4 rejected. Review queue cleared. |
| PDF download | ✅ Complete | 799 PDFs on disk (799 accepted; 1 withdrawn/404: 2601.20362 → rejected). |
| Parse (text extraction) | ✅ Complete | 783/783 done (in-corpus). All queue batches 1–10 finished. Quality reports saved in `raw/parsed/`. |
| Ingest (wiki pages) | 🔄 In progress | 100/783 ingested. +30 this session (6 batches of 5 TTS papers across Interspeech, NAACL, ACL, EMNLP, arXiv, COLING). **Integration threshold exceeded (30 pending).** ~621 more ready. |

---

## Metadata counts (2026-05-30)

```
Total files:  1000
  accepted:    683   ← after dedup (783 unique papers - 100 ingested)
  ingested:    100   ← wiki page written
    integrated: 70   ← all 70 pre-session papers integrated
    pending:    30   ← integration backlog; threshold exceeded — run integration pass now
  review:        0   ← queue cleared
  rejected:    217   ← 202 + 15 arXiv/proceedings duplicates resolved

PDFs on disk:  ~784  ← raw/papers/ (accepted + ingested; 15 duplicate arXiv PDFs may remain)
Parsed:        783   ← in-corpus paper.md files (parse complete, 2026-05-30)
Parse-pending:   0   ← all queue batches done
Ready to ingest: ~693 ← parsed but not yet ingested
```

---

## cs.CL fetch detail

The arXiv search API (`export.arxiv.org/api/query`) is unreliable for cs.CL due to
aggressive rate-limiting on large result sets. Switched to the OAI-PMH bulk-harvest
endpoint (`export.arxiv.org/oai2`), implemented in `fetch_arxiv_oai.py`.

**OAI-PMH set identifier:** `cs:cs:CL` (the familiar `cs.CL` notation is accepted by
the CLI and converted automatically).

### Final harvest results

| Window | Records scanned | Matched filter | Written | Skipped (existing) |
|--------|----------------|----------------|---------|-------------------|
| 2025-08-01 → 2025-11-30 | 9,461 | 119 | 41 | 78 |
| 2025-12-01 → 2026-02-28 | 6,857 | 65 | 32 | 33 |
| 2026-03-01 → 2026-05-22 | 9,752 | 96 | 42 | 54 |
| **Total** | **26,070** | **280** | **115** | **165** |

"Skipped (existing)" = paper already in corpus from cs.SD/eess.AS or ACL fetches.

---

## ACL Anthology fetch detail

`fetch_acl.py` completed on 2026-05-22. Fetches per-venue XML from the ACL Anthology
GitHub repository (`acl-org/acl-anthology`).

**Scope:** 2025 main proceedings (EMNLP, ACL, NAACL, Findings) + 182 co-located workshops.

### Final results (2026-05-22)

| Venue group | Papers scanned | Passed filter | Written (new) | Enriched existing |
|-------------|---------------|--------------|---------------|-------------------|
| Main venues (EMNLP, Findings, ACL, NAACL) | 8,369 | 80 | 67 | 16 |
| Workshops (182 files) | 6,300 | 49 | 46 | 0 |
| **Total** | **14,669** | **129** | **113** | **16** |

---

## Infrastructure

| Tool | Purpose |
|------|---------|
| `scripts/fetch/arxiv.py` | arXiv search API fetcher (cs.SD, eess.AS; avoid for large cs.CL queries) |
| `scripts/fetch/arxiv_oai.py` | OAI-PMH bulk fetcher — use for cs.CL and future large-category sweeps |
| `scripts/fetch/acl.py` | ACL Anthology fetcher via GitHub XML; supports `--all-workshops` |
| `scripts/fetch/isca.py` | ISCA/Interspeech HTML scraper |
| `scripts/filter/agent.py` | Standalone Anthropic SDK filter; requires `ANTHROPIC_API_KEY` |
| `scripts/parse/download_pdfs.py` | Downloads PDFs for all accepted papers; resumable, per-domain rate limiting |
| `scripts/discover/citation_index.py` | Builds `raw/citation_index.json` from all parsed `references.json` files; flags speech-relevant candidates; run periodically after parse batches |
| `lib/keyword_filter.py` | Shared keyword filter logic used by all fetchers |
| `.claude/agents/speech-generation-filter-agent.md` | Reusable Sonnet filter agent; invoke on any new pending batch |

### Extending the corpus

```bash
# Top up cs.SD + eess.AS (run periodically)
python scripts/fetch/arxiv.py --date-from 2026-05-22

# Top up cs.CL
python scripts/fetch/arxiv_oai.py --set cs.CL --date-from 2026-05-22

# Next year's ACL Anthology
python scripts/fetch/acl.py --years 2026 --all-workshops
```

---

## Parse pipeline progress (session 3 — 2026-05-22)

Tool choice: **Docling** (replaces the GROBID+Marker multi-tool stack from the original design). See `docs/PARSING_PIPELINE_DESIGN.md` §10 for rationale.

### Scripts

| Script | Status | Purpose |
|--------|--------|---------|
| `scripts/parse/convert_paper.py` | ✅ Built & tested | Single-paper converter |
| `scripts/parse/batch_convert.py` | ✅ Built & tested | Batch orchestrator (`--ids`, `--force`, `--retry-failed`, `--status`) |
| `scripts/parse/make_batch_queue.py` | ✅ Built | Generates/refreshes `raw/parsed/batch_queue.json` |
| `scripts/parse/build_citation_index.py` | 🔜 Phase 5 | Post-batch citation aggregator |

### Batch conversion queue (session 9 — 2026-05-26)

Queue rebuilt with 40-paper batches. 411 papers done (batches 1–20 at 20-paper size); 387 remaining across 10 new batches.
Queue file: `raw/parsed/batch_queue.json`. Managed by `scripts/parse/make_batch_queue.py`.

**Workflow per batch:**
1. Main session runs: `source .venv/bin/activate && python scripts/parse/batch_convert.py --ids <ids> 2>&1 | tee /tmp/batch_N.log`
2. Once complete, a lightweight sub-agent reads the output files and returns a quality table.
3. Any failures are re-run with `--force --ids <failed_ids>` before proceeding to the next batch.

**Completed batches (old 20-paper size):**

| Batch | Papers | Status | Done | Failed | Notes |
|-------|--------|--------|------|--------|-------|
| 1 | 20 | complete | 20 | 0 | Quality report: `raw/parsed/batch_1_quality_report.md` |
| 2 | 20 | complete | 20 | 0 | Quality report: `raw/parsed/batch_2_quality_report.md`. Warnings: RapidOCR (3 papers), PIL DecompressionBomb (emnlp-main.989) |
| 3 | 20 | complete | 20 | 0 | Quality report: `raw/parsed/batch_3_quality_report.md`. Clean run, no warnings. |
| 4 | 20 | complete | 20 | 0 | Quality report: `raw/parsed/batch_4_quality_report.md`. RapidOCR: naacl-long.110 (×2), sigdial-1.51 (×1). |
| 5 | 20 | complete | 20 | 0 | Quality report: `raw/parsed/batch_5_quality_report.md`. RapidOCR: 2501.15907. Quality issue: 2407.15828 (0 refs extracted). |
| 6 | 20 | complete | 20 | 0 | Quality report: `raw/parsed/batch_6_quality_report.md`. Clean run, no warnings. |
| 7 | 20 | complete | 20 | 0 | Quality report: `raw/parsed/batch_7_quality_report.md`. RapidOCR: 2507.07518, 2508.02013 (non-fatal). |
| 8 | 20 | complete | 20 | 0 | Quality report: `raw/parsed/batch_8_quality_report.md`. 2 quality issues resolved: 2508.06262 and 2508.08961 refs recovered via patched third fallback. |
| 9 | 20 | complete | 20 | 0 | Quality report: `raw/parsed/batch_9_quality_report.md`. Clean run, no issues. |
| 10 | 20 | complete | 20 | 0 | Quality report: `raw/parsed/batch_10_quality_report.md`. 1 quality issue: 2509.04702 has 2 false-positive figure captions in references.json (non-blocking). All flagged papers manually verified by user. |
| 11 | 20 | complete | 20 | 0 | Quality report: `raw/parsed/batch_11_quality_report.md`. Clean run, no issues. |
| 12 | 20 | complete | 20 | 0 | Quality report: `raw/parsed/batch_12_quality_report.md`. Patched _REFS_HEADER_RE for "N References" headings (no period); 2509.15462 re-run gave 16 refs. |
| 13 | 20 | complete | 20 | 0 | Quality report: `raw/parsed/batch_13_quality_report.md`. Clean run, no warnings. |
| 14 | 20 | complete | 20 | 0 | Quality report: `raw/parsed/batch_14_quality_report.md`. 5 thin (legitimate). RapidOCR: 2510.01903 (×1), 2510.04738 (×2). |
| 15 | 20 | complete | 20 | 0 | Quality report: `raw/parsed/batch_15_quality_report.md`. 2510.09424 0 refs fixed (patched _REFS_HEADER_RE for numbered "Bibliography" headings). RapidOCR: 2510.05984 (×1), 2510.09245 (×4). |
| 16 | 20 | complete | 20 | 0 | Quality report: `raw/parsed/batch_16_quality_report.md`. Null abstracts: 2510.15364, 2510.21685 (fixed in abstract re-run). Short: 2510.20677 (165 lines). |
| 17 | 20 | complete | 20 | 0 | Quality report: `raw/parsed/batch_17_quality_report.md`. Null abstracts: 2510.25178, 2511.05516, 2511.06246 (fixed). RapidOCR: 2511.00256, 2511.07116, 2511.08496 (non-fatal). |
| 18 | 20 | complete | 20 | 0 | Quality report: `raw/parsed/batch_18_quality_report.md`. Null abstracts: 6 papers (fixed). 0 refs: 2511.21229 (727-line paper, refs unrecovered). RapidOCR: 2511.14249, 2511.21270. |
| 19 | 20 | complete | 20 | 0 | Quality report: `raw/parsed/batch_19_quality_report.md`. Clean run. Minor OCR spacing artifacts: 2512.13251 (non-blocking). All abstracts populated. |
| 20 | 20 | complete | 20 | 0 | Quality report: `raw/parsed/batch_20_quality_report.md`. Short: 2512.17293 (117 lines, 3 refs). PIL DecompressionBomb: 2601.03170 (non-fatal). All abstracts populated. |

**Pending batches (new 40-paper size — queue IDs 1–10):**

| Queue batch | Papers | Range | Status |
|-------------|--------|-------|--------|
| 1 | 40 | 2025.acl-long.388 … 2512.18706 | complete | Quality report: `raw/parsed/batch_21_quality_report.md`. Patched `_REFS_HEADER_RE` for French "Références" and "Bibliographical/Language Resource References" headings; both re-parsed, all refs recovered. RapidOCR: 2025.coling-industry.29 (non-fatal). |
| 2 | 40 | 2512.20156 … 2601.19952 | complete | Quality report: `raw/parsed/batch_22_quality_report.md`. RapidOCR warnings on 6 papers (non-fatal). PIL DecompressionBomb: 2601.15621 (non-fatal). Low refs: 2601.18694 (16, legitimate). |
| 3 | 40 | 2601.20094 … 2602.23068 | complete | Quality report: `raw/parsed/batch_23_quality_report.md`. Patched `_REFS_HEADER_RE` for letter-prefix headings (e.g. "B. REFERENCES"); re-parsed 2602.06053, 33 refs recovered. RapidOCR: 2602.04683, 2602.13891 (non-fatal). |
| 4 | 40 | 2602.23266 … 2603.14032 | complete | Quality report: `raw/parsed/batch_24_quality_report.md`. RapidOCR: 2602.23765, 2603.08574, 2603.08823, 2603.09120, 2603.11589 (non-fatal). Spot-check recommended: 2603.08574, 2603.11589 (4–6 consecutive OCR failures). |
| 5 | 40 | 2603.14035 … 2604.06356 | complete | Quality report: `raw/parsed/batch_25_quality_report.md`. RapidOCR: 2603.14853 (×4), 2603.22252 (×2), 2603.23938 (×5), 2603.24144 (×1) (non-fatal). Low refs: 2603.19798 (16), 2604.03279 (17) (legitimate). |
| 6 | 40 | 2604.06871 … 2604.22821 | complete | Quality report: `raw/parsed/batch_26_quality_report.md`. RapidOCR: 2604.11424 (×4, non-fatal). 0 refs: 2604.13288 (no References header, non-blocking). |
| 7 | 40 | 2604.25441 … interspeech-2025-0355 | complete | Quality report: `raw/parsed/batch_27_quality_report.md`. RapidOCR: 2605.05611 (×1), 2605.20946 (×2), interspeech-2025-0115 (×2) (non-fatal). Clean run. |
| 8 | 40 | interspeech-2025-0383 … interspeech-2025-1081 | complete | Quality report: `raw/parsed/batch_8_quality_report.md`. RapidOCR: 0408, 0433, 0669, 0756 (non-fatal). Clean run. |
| 9 | 40 | interspeech-2025-1084 … interspeech-2025-2031 | complete | Quality report: `raw/parsed/batch9_quality_report.md`. RapidOCR: 1531, 1595, 1641, 1684 (non-fatal). Clean run. |
| 10 | 27 | interspeech-2025-2032 … interspeech-2025-raju25_interspeech | complete | Quality report: `raw/parsed/batch10_quality_report.md`. RapidOCR: 2032, 2586, 2739, 2815, cho25c, raju25 (non-fatal). 4 slug-named papers are legitimate 2-page demos (short/few-refs expected). |

**Known issues (cosmetic, do not block ingest):**
1. Title heading appears twice (YAML frontmatter `# Title` + Docling body `## Title`)
2. Floating figure captions sometimes appear as loose text lines after `[FIGURE N — see assets/]`
3. Occasional reference list bleed into body without clean separator

### `convert_paper.py` — output per paper

```
raw/parsed/{id}/
  paper.md              LLM-ready Markdown (DONE sentinel — atomic write)
  metadata.json         Title, authors, abstract, asset registries
  references.json       Structured references with in-corpus flags
  docling_native.json   Docling's full internal representation
  assets/               figure-N.png, table-N.csv, table-N.png
```

### State model (filesystem-based)

| State | Condition |
|-------|-----------|
| DONE | `paper.md` exists, no `error.json` |
| FAILED | `error.json` exists (includes error type, message, traceback, attempt count) |
| PENDING | neither exists |

### Known issues / fixes applied

- **MPS float64 crash**: Docling defaults to MPS on Apple Silicon; forced to CPU via `AcceleratorOptions(device=AcceleratorDevice.CPU)`. MPS doesn't support float64, which the layout model requires.
- **Reference label fallback**: Docling doesn't always label reference entries as `REFERENCE`. Fallback collects `TEXT`/`LIST_ITEM` items that follow a "References" section header.
- **Duplicate abstract**: Abstract body items are labeled `TEXT`, not `ABSTRACT`. Fixed with `in_abstract_section` flag that suppresses body items following the abstract section header.

### Batch orchestrator design (Phase 2 — to build)

- `--workers N` — parallel ProcessPoolExecutor workers (default 1; Docling loads ~3–5 GB ML models per worker)
- `--limit N`, `--offset N` — manual batching
- `--ids id1 id2` — targeted conversion
- `--force` — re-extract DONE papers
- `--retry-failed` — only process FAILED papers
- `--dry-run` — print queue, do nothing
- `--status` — print DONE/FAILED/PENDING counts and exit
- Worker initializer loads `DocumentConverter` once per process and caches it module-globally
- SIGINT handled gracefully: finishes current paper(s), then stops
- Progress log: one JSON line per paper to `raw/parsed/batch_convert.log`

---

## Ingest pipeline (session 14 — 2026-05-27)

Architecture: native Claude Code multi-agent pattern (no Anthropic SDK calls). Two distinct stages — **ingest** (per-paper, cheap, parallel) and **integration** (cross-paper, expensive, sequential).

### Agents

| Agent | Status | Purpose |
|-------|--------|---------|
| `.claude/agents/speech-generation-ingest-agent.md` | ✅ Built | Per-paper worker — reads paper.md, writes wiki page, index row, venue row, log bullet, metadata status. Paper-scoped only. |
| `.claude/agents/speech-generation-ingest-orchestrator.md` | ✅ Built | Ingest coordinator — discovers ready papers, spawns ingest agents in parallel batches of 5, logs batch summary. No cross-paper work. |
| `.claude/agents/speech-generation-integration-agent.md` | ✅ Built | Cross-paper integration — updates concept pages, adds back-links between papers, refreshes venue narratives, overview.md. Run every ~25 papers. |

### Invocation

```
# Stage 1 — Ingest (repeat until queue is clear)
→ speech-generation-ingest-orchestrator: "Ingest up to 5 papers"

# Stage 2 — Integration (run every ~25 ingested papers)
→ speech-generation-integration-agent: "Run integration pass on last 25 papers"

# Single paper (ingest worker directly)
→ speech-generation-ingest-agent: "Ingest paper {id}"
```

### Ingest progress (session 18 — 2026-05-29)

| Batch | Papers | Method | Per-paper concepts | Orchestrator concept pass | Notes |
|-------|--------|--------|-------------------|--------------------------|-------|
| 1 | 5 | orchestrator | yes (by design) | yes | 2509.02020, 2507.14534, 2509.19668, 2510.00981, 2412.17048; 9 concept pages updated |
| 2 | 5 | orchestrator | yes (by design) | **skipped** | 2025.findings-emnlp.424, 2025.acl-demo.37, 2025.acl-industry.42, 2025.acl-long.1043, 2025.acl-long.1252, 2025.acl-long.1471 |
| 3 | 5 | direct agents (sequential) | yes (not suppressed — see note) | n/a | 2025.acl-long.1498, .313, .346, .388, .598; ~379k tokens total |

**Session 12 note (historical):** Prior to session 14, the orchestrator included an in-built concept pass that caused scope creep — ingest agents were also updating concept pages, doubling per-paper token cost (~75k instead of ~35–40k). Resolved in session 14 by separating ingest and integration into distinct agents.

**Batch 3 verified (session 13):** All 5 papers confirmed fully ingested — `status: ingested`, `ingested_date: 2026-05-26`, wiki pages 90–153 lines, index entries present. No data loss.

**Pending:** Run integration pass on all 16 ingested papers to catch up on concept page updates (batches 1–3 had varying/incomplete concept coverage under the old architecture).

### Context budget (empirically measured — 2026-05-26, updated session 14)

**Ingest stage:**

| Mode | Papers | Tokens (subagent) | Tool uses | Time |
|------|--------|-------------------|-----------|------|
| Orchestrator (ingest only) | 5 | ~130k (orchestrator) | ~30 | ~7 min |
| Direct ingest agent (paper page only) | 1 | ~35–40k | ~25 | ~4 min |

**Integration stage (estimated):**

| Mode | Papers | Tokens (subagent) |
|------|--------|-------------------|
| Concepts + cross-links | 25 | ~60–80k |
| Full pass (+ venue + overview) | 15 | ~80–120k |

- **5 papers per orchestrator call** is the validated safe limit (context overflow risk beyond 7).
- The main session context does **not** accumulate between orchestrator calls — each is a fresh subagent.
- Do **not** use "Ingest all ready papers" — hundreds of papers will overflow the context window.

### State model

| State | Condition |
|-------|-----------|
| Ready to ingest | `status: accepted` AND `raw/parsed/{id}/paper.md` exists |
| Ingested | `status: ingested` in `raw/metadata/{id}.json` |
| Failed | `status: accepted` + error in `raw/parsed/ingest.log` (retryable) |
| Blocked | `status: accepted` AND no parsed output (waiting on parse pipeline) |

---

## Next actions

1. **Re-ingest ~10 representative papers** — The new template (claims, field_significance, merged callout card, architecture figures) requires a re-ingest pass on papers that exemplify different paper types (foundational, architectural, empirical, engineering integration). Existing 100 pages have the structural changes applied (H1 stripped, callout format updated) but lack claims and field_significance fields.
2. **Continue ingest** — ~683 papers ready. Use parallel direct subagents (Mitigation B). Workers write paper pages only; main session does batch cleanup. Run integration every ~25 papers. Next up: `interspeech-2025-0469` then `interspeech-2025-0854` onwards.
3. **Integration pass** — 0 pending (all 100 integrated after pass 4). Next pass after 25 more ingested; first pass to also create concept evidence digests.
4. **Citation discovery — next candidates** — Moshi (53x, 2410.00037), GLM-4-Voice (35x, 2412.02612), VALL-E 2 (34x, 2406.05370), Llama-omni (28x, 2409.06666). Fetch, filter, download. Re-run `scripts/discover/citation_index.py` after each parse batch.
5. **Exclude `papers/` from Quartz explorer sidebar** — one-line `filterFn` change in site repo's `quartz.config.yaml`; prevents 800+ paper list from flooding the sidebar.
6. **cs.CL re-scan (deferred)** — ~15–30 marginal papers expected; low priority.
7. **Periodic maintenance** — re-run fetchers, filter, and `citation_index.py` monthly.

---

## Pipeline & codebase improvements

### Completed (2026-06-01, session 22)

- ✅ **Writing style guidelines** — `docs/WRITING_STYLE.md` created; covers claims, field significance, synthesis vs enumeration, callouts, tense, uncertainty. Referenced in ingest and integration agent specs.
- ✅ **Claims extraction** — `## Claims` section (2–5 generalised propositions) added to paper page template and ingest agent spec. Controlled vocabulary for claim style in WRITING_STYLE.md §3.
- ✅ **Field significance** — `field_significance.level` + `field_significance.type` frontmatter + `## Field Significance` prose section added to paper page template and ingest agent.
- ✅ **Concept page redesign** — Research briefing format: Executive Summary, Current Status (with status vocab), Methods and Variants, Major Claims (Strongly Supported / Emerging / Contested), Relationship to Other Concepts (typed), Representative Papers (tiered), Open Questions, Trend Summary, All Papers table.
- ✅ **Concept evidence digests** — Schema defined (`wiki/concepts/_evidence/{slug}.yaml`); integration agent Step 3 writes/updates digests after each pass; directory created.
- ✅ **Architecture figures in paper pages** — Ingest agent Step 2b selects 0–2 architecture figures per paper (only for `architectural-novelty` papers); copies to `wiki/papers/assets/{id}/`; embeds in `## Method`.
- ✅ **Callout system** — Quartz callout support confirmed. 4 callout types defined with precise trigger rules in WRITING_STYLE.md §11. Applied retroactively to 100 paper pages; concept page template updated.
- ✅ **Merged paper card** — `> [!abstract]` callout combining venue badge, authors, paper link, availability flags, and one-sentence contribution. Applied to all 100 existing pages.
- ✅ **Title deduplication fix** — `article-title` Quartz plugin caused double titles. Stripped H1 from 121 pages (100 papers + 21 concepts); templates updated to omit H1 going forward.
- ✅ **Log split** — `wiki/log.md` is now reader-facing only (ingest, integrate, report, query). Infra operations (filter, parse, discover, lint, review) go to `raw/pipeline_log.md`. 26 entries migrated.
- ✅ **Venue page naming** — Renamed `{venue}-{year}` → `{year}-{venue}` for chronological sorting. 9 files renamed; index updated; agent specs updated.
- ✅ **Quartz display names** — Frontmatter `title:` added to top-level wiki files and all folder `index.md` pages so Quartz explorer shows clean names instead of slugs.
- ✅ **Wiki landing page** — `wiki/index.md` redesigned: banner image, `> [!abstract]` callout, concept navigation by category, links to All Concepts / Venues / Reports / Papers. Paper/concept/venue tables migrated to `wiki/papers/index.md`, `wiki/concepts/index.md`, `wiki/venues/index.md`. Agent specs updated to write to folder indexes.
- ✅ **`trends/` eliminated** — Replaced by: concept page Trend Summary sections + `wiki/reports/` (monthly/quarterly/yearly). No files to migrate (directory was empty).

### Pending

- **Deduplication check at fetch/pre-parse stage** — 15 arXiv/proceedings duplicates resolved manually 2026-05-28. Add `scripts/discover/dedup_check.py` for title-based collision detection after each fetch batch. Canonical priority: proceedings > arXiv.
- **Tiered wiki pages** — Full vs. summary tiers as corpus scales. Low-citation incremental papers compressed to one paragraph; promotable on in-corpus citation gain. Pruning pass every ~100 ingested.
- **Opus quality pass** — Targeted rewrites for papers with ≥10 in-corpus citations and concept pages with ≥15 entries. Mark with `quality_pass: opus | YYYY-MM-DD`. Candidates: VITS, VALL-E, HiFi-GAN, Voicebox, EnCodec.
- **Quartz explorer: exclude `papers/`** — One-line `filterFn` change in site repo prevents 800+ paper list flooding sidebar. Discovery via concepts, venues, search, and `papers/index.md`.

