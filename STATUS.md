# Project Status

Last updated: 2026-06-16 (306 ingested, 276 integrated; passes 1–11 complete; integration pass 12 pending for 30 papers)

---

## Corpus state

| Step | Status | Notes |
|------|--------|-------|
| arXiv fetch (cs.SD + eess.AS) | ✅ Complete | 2025-08-01 → 2026-05-25. 504 + 70 re-scan = 574 written. July 2025 backfill + May tail added 2026-06-05 (+75 written). Full coverage: 2025-07-01 → 2026-05-31. Note: switched to OAI-PMH (search API rate-limited). |
| arXiv fetch (cs.CL) | ✅ Complete | Via OAI-PMH. Aug–Nov: 41; Dec–Feb: 32; Mar–May: 42. Total: 115. Re-scan with expanded keywords done 2026-06-05: Jul backfill +3, Aug–Nov +12, Dec–Feb +5, Mar–May +13 = 33 new. Full coverage: 2025-07-01 → 2026-05-31. |
| ISCA fetch (Interspeech 2025) | ✅ Complete | 128 + 12 re-scan = 140 papers written. |
| Deduplication (arXiv ↔ ISCA) | ✅ Complete | 11 duplicates resolved; ISCA is canonical. |
| ACL Anthology fetch (2025) | ✅ Complete | 14,669 scanned; 113 + 14 re-scan = 127 new written, 136 arXiv records enriched total. |
| Citation discovery fetch (targeted) | ✅ Complete | 5 papers fetched by arXiv ID via `--ids` flag: VALL-E, CosyVoice ×2, Seed-TTS, F5-TTS. |
| ICLR + NeurIPS fetch (OpenReview) | ✅ Complete | New fetcher `scripts/fetch/openreview.py`. ICLR 2025: 13 written. NeurIPS 2025: 16 written. ICLR 2026: 27 written. Total: 56 new pending. Dedup pass pending. |
| Keyword filter expansion | ✅ Complete | +11 terms added to `config/keyword_filter.yaml` (2026-05-25). See Infrastructure section. |
| Filter — batch 1 (May 12) | ✅ Complete | arXiv batch: 404 accepted, 31 review, 69 rejected. |
| Human review — batch 1 (May 19) | ✅ Complete | 31 resolved → 15 accepted, 16 rejected. |
| Filter — batch 2 (May 22) | ✅ Complete | ACL + cs.CL batch: 300 accepted, 39 review, 56 rejected. |
| Human review — batch 2 (May 22) | ✅ Complete | 39 resolved → 25 accepted, 14 rejected. |
| Duplicate resolution (arXiv ↔ ACL) | ✅ Complete | 1 additional duplicate found (2502.19732 → 2025.findings-emnlp.716). |
| Duplicate resolution — full corpus scan (May 28) | ✅ Complete | 15 total arXiv/proceedings duplicates resolved (including F5-TTS 2410.06885). Proceedings ID is canonical throughout. 6 parsed output dirs remapped. |
| Duplicate resolution — top-up fetch (Jun 5) | ✅ Complete | 16 duplicates found in 108 new papers (title match + arXiv ID cross-ref). All arXiv versions marked rejected. 15 source_ids.arxiv backfilled. 1 three-way case: 2505.20868 + 2511.14824 → interspeech-2025-2586. |
| Filter — batch 3 (May 25) | ✅ Complete | Re-scan + citation-discovery: 101 papers, 67 accepted, 7 review, 27 rejected (66% accept rate). |
| Human review — batch 3 | ✅ Complete | 7 resolved → 3 accepted, 4 rejected. Review queue cleared. |
| PDF download | ✅ Complete | 910 PDFs on disk (799 prior + 111 new). 2 new 404s flagged needs_manual_pdf: 2503.20999, 2511.08230 (likely withdrawn from arXiv). |
| Parse (text extraction) | ✅ Complete | 875/875 papers parsed (2026-06-06). Batches 11–13 (111 new papers: arXiv 2409–2605, ICLR 2025/2026, NeurIPS 2025) completed with 0 failures. |
| Citation discovery fetch (bulk) | ✅ Complete | 162 highly-cited out-of-corpus papers written with status=accepted, discovery_source="citation-discovery", corpus_role, and per-quarter citation counts. Bypassed keyword filter. Script: `scripts/fetch/citation_discovery_fetch.py`. PDFs downloaded; parse complete 2026-06-08. |
| Parse (citation-discovery) | ✅ Complete | 162/162 parsed (2026-06-08). Batches 14–18. 0 failures. 1 manual refs fix: 2001.08361 (Scaling Laws, table-layout refs recovered). Quality reports: batch_14–18_cd_quality_report.md. |
| Ingest (wiki pages) | 🔄 In progress | 306/875 ingested (176 standard + 130 CD: 96 T1 full pages + 34 T2 stubs). All 96 Tier 1 CD papers complete. 276/306 integrated (passes 1–11 complete; 30 ingested 2026-06-16 not yet integrated). 24/24 evidence digests seeded. |

---

## Metadata counts (2026-06-16)

```
Total files:  1326
  accepted:    731   ← 699 standard + 0 T1 CD + 32 T2 CD not yet ingested
  ingested:    306   ← 176 standard + 130 CD (96 T1 full pages + 34 T2 stubs)
    integrated: 276  ← passes 1–11 complete; 30 from 2026-06-16 not yet integrated
  pending:       0   ← cleared
  review:        0   ← queue cleared
  rejected:    289   ← includes 2 withdrawn arXiv papers (2503.20999, 2511.08230)

PDFs on disk:  ~1037 ← raw/papers/ (875 standard + 162 citation-discovery)
Parsed:        861   ← all accepted papers parsed (875 standard + 162 citation-discovery; 2026-06-08 complete)
Parse-pending:   0   ← pipeline complete
Ready to ingest: 731 ← parsed + accepted, not yet ingested

Evidence digests: 24/24 seeded (fine-tuning digest created pass 8; singing + fine-tuning below 5-paper threshold but stubs exist)
Missing concept stubs: none — singing and fine-tuning seeded 2026-06-04 (24 total concept pages)
Wiki pages: 306 (as of 2026-06-16)
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
| `scripts/fetch/openreview.py` | OpenReview API v2 fetcher — ICLR and NeurIPS; `--venue ICLR\|NeurIPS --year YYYY` |
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

0. ~~**Parse citation-discovery papers**~~ — ✅ done 2026-06-08. 162/162 parsed (batches 14–18), 0 failures. 1 manual refs fix: 2001.08361 (two-column table layout). Quality reports: `raw/parsed/batch_14–18_cd_quality_report.md`. Citation graph rebuilt: 21,262 entries across 1,056-paper corpus. Ingest strategy documented in `docs/analyses/cd-ingest-strategy.md`.



1. ~~**Parse batches 11–13**~~ — ✅ done 2026-06-06. All 111 new papers parsed, 0 failures. Parse pipeline complete (875/875).

2. ~~**Run integration pass 9**~~ — ✅ done 2026-06-12. 25 papers (15 T1 + 10 T2). 19 concepts updated, 4 evidence digests fully updated, 16 cross-links added. Integration agent spec patched to use correct wiki content repo path (WIKI variable).

2. ~~**Run integration pass 10**~~ — ✅ done 2026-06-13. 25 papers (25 T1: 15 from session 44 + 10 from session 45). 21 concepts updated, 21 evidence digests updated, 133 cross-links added, 6 venue pages updated, overview updated.

2. ~~**Patch ingest agent specs**~~ — ✅ done 2026-06-14. Four fixes to `speech-generation-ingest-agent.md` and three to `speech-generation-lightweight-ingest-agent.md`: survey frontmatter rule (architecture/conditioning/training: []); abstract card callout warning; Wiki Connections bullet format requirement; related_concepts grounding rules (prosody-control, disentanglement, instruction-conditioned-tts, prompt-conditioned, self-supervised-speech).

3. ~~**Run integration pass 11**~~ — ✅ done 2026-06-15. 25 papers (all 25 Tier 1 CD from session 46). 19 concepts updated, 23 digests updated, 8 cross-links added, 2 venue pages updated. All 276 ingested papers now integrated.

3. **Continue ingest** — 746 papers ready to ingest. Chronological strategy: Aug 2025 → Dec 2025 → 2026. Next up: continue Aug 2025 pool from `2509.04093` onwards. Show selection first, ingest 2 at a time.

3. **Run integration pass 12** — ⏸ deferred. 30 papers ingested 2026-06-16 not yet integrated. Run `speech-generation-integration-agent` on these before the next large ingest batch. Papers (session 47): 2301.11325, 2301.12503, 2305.15255, 2312.01479, 2312.15821, 2401.07333, 2402.13236, 2404.03204, 2406.00654, 2406.05551, 2408.02622, 2411.09943, 2411.17607, 2411.18803, 2412.04724. Papers (this session): 2502.18924, 2503.14345, 2504.02407, 2504.10344, 2505.02625, 2505.09558, 2505.13000, 2505.14648, 2506.10274, 2506.13053, 2506.16381, 2507.23159, 2508.04195, 2510.07838, 2511.15848.

3. ~~**Resolve CD ingest strategy open questions**~~ — ✅ done 2026-06-09. (1) `2312.10997` → Tier 2. (2) MusicLM + AudioLDM → confirmed Tier 1. (3) Lightweight stubs → new `speech-generation-lightweight-ingest-agent` spec. (4) Tier 3 eliminated → all 13 papers upgraded to Tier 2. Final counts: Tier 1 = 96, Tier 2 = 66 (22 T2 done, 44 remaining). See `docs/analyses/cd-ingest-strategy.md`.

4. ~~**CD ingest preparation**~~ — ✅ done 2026-06-09. `ingest_tier` field added to schema and bulk-set in all 162 CD metadata files. Citation merge overrides added for CSTR VCTK, AISHELL-3, and GSLM.

5. ~~**Ingest Tier 1 CD papers**~~ — ✅ done 2026-06-16. All 96 Tier 1 CD papers ingested.

6. ~~**Ingest Tier 2 CD papers**~~ — ✅ done 2026-06-17. All 66/66 Tier 2 CD stubs complete. Lightweight stubs via `speech-generation-lightweight-ingest-agent`.

3. ~~**Fetch citation-discovery candidates**~~ — ✅ done 2026-06-08. All 162 arXiv IDs written with `status: accepted`, `discovery_source: "citation-discovery"`, and per-quarter citation counts. Script: `scripts/fetch/citation_discovery_fetch.py`. 57 SR=Y, 101 SR=N, 4 SR=? (titles resolved). These papers bypassed the keyword filter; they are onboarded because they are highly cited by in-corpus papers. Task assignments (TTS/VC/SCA/codec/etc.) and PDF downloads still pending before ingest.

3. ~~**Seed `transformer-enc-dec-tts` and `rlhf-speech` evidence digests**~~ — ✅ done 2026-06-08. transformer-enc-dec-tts (11 papers, 6 claim clusters), rlhf-speech (15 papers, 7 claim clusters). All 23/23 evidence digests seeded.

4. ~~**Seed `singing` and `fine-tuning` concept stubs**~~ — ✅ done 2026-06-04.

5. ~~**Investigate ACL/workshop `published_date` issue**~~ — ✅ done 2026-06-13. 26 metadata files patched: `published_date`, `conference_date`, `month` corrected to actual conference dates; `venue_detail` field added with full name, parent conference, and location. Dates range from COLING Jan 2025 through IWCLUL Dec 2025. Check `scripts/fetch/acl.py` to prevent this from recurring on future fetches.

6. ~~**Corpus top-up fetch (arXiv + cs.CL re-scan)**~~ — ✅ done 2026-06-05. Full coverage 2025-07-01 → 2026-05-31. See `raw/fetch_plan_2026-06.md`. Remaining: citation discovery (Moshi 53×, GLM-4-Voice 35×, VALL-E 2 34×, Llama-omni 28×) → NeurIPS/ICML/ICLR 2025 (~50–150 papers).

7. ~~**Fix "Factor A/B/C" terminology**~~ — ✅ done 2026-06-13. Paper-internal labels replaced with descriptive language across 12 files (5 concept pages, 5 evidence digests, overview.md, 2025.acl-long.1498.md). Missing `[[2412.17048]]` citations added where references lacked one. Source page `2412.17048.md` unchanged.

8. **Generate first field report** — now at 251 ingested, well past the 200-paper threshold. Ready to generate. Use template in CLAUDE.md §5.

9. **Periodic maintenance** — re-run fetchers, filter, and `citation_index.py` monthly.

---

## Backlog

Quick-scan list of improvement ideas. Review at session start; pick up when bandwidth allows.

### Wiki content quality

- **Wiki page quality audit (lint pass)** — Systematic review of all 185 paper pages. Five recurring issue classes found across test ingest of 10 papers (sessions 38–39, 2026-06-09/10):
  1. **Adoption claims** — Field Significance and Wiki Connections contain phrases like "has become the de facto", "dominant", "widely adopted" that require reading citing papers to support; absent from the paper itself. Likely widespread in the 176 pre-session-38 pages. Grounding rule added to both agent specs but does not fully prevent this on foundational papers.
  2. **Abstract callout type** — `[!tip]` used instead of `[!abstract]` on the abstract card. Grep-detectable: `> [!tip]` or `> [!important]` in first 10 lines of paper pages.
  3. **`field_significance.type` mismatches** — e.g., `empirical-benchmark` assigned to survey papers; `architectural-novelty` assigned to engineering integrations. Requires reading each page.
  4. **Leaked instruction text** — `**Grounding rule:**` paragraph appearing as visible prose in Field Significance (only affects pages generated mid-session 38 before the spec was fixed; all patched).
  5. **Spurious `related_concepts` tags** — `self-supervised-speech` appears on papers with no SSL component (EnCodec, FastSpeech 2); agent links it when the paper merely *mentions* or *compares against* SSL work. Similarly, `VAE` in `architecture` for models that use RVQ without a variational objective. Grep-detectable: `self-supervised-speech` in `related_concepts` where `training` does not include `self-supervised`.
  Recommended approach: (a) write a lint script to flag structural issues (wrong callout type, common adoption phrases, leaked instruction labels, spurious `self-supervised-speech` tag) — fast, no LLM; (b) targeted manual review for foundational/high pages; (c) full re-ingest only for the worst offenders.

- ✅ **Claims provenance** — each claim bullet now includes an inline section citation e.g. `*(§4.1, Table 2)*`. Implemented in CLAUDE.md template, ingest agent spec, and WRITING_STYLE.md §3 (2026-06-04). Applies to new ingest only; no backfill needed.
- **Static counts go stale** — paper/concept counts hardcoded in `wiki/index.md`, `overview.md`, venue pages, evidence digests (`paper_count`), and concept page All Papers tables drift after every pass. Fix options: (a) compute at Quartz build time via plugin or pre-build script — single source of truth, never stale; (b) add a post-integration agent checklist to re-derive counts in the key index pages. Option (a) is cleaner long-term.
- **Generation tracking for concept/venue pages** — `generation` frontmatter + `generation_history` implemented for paper pages only. Concept pages, venue pages, and `overview.md` need the same before any Opus quality pass begins. Requires updating integration agent spec and CLAUDE.md template.
- **Opus quality pass** — targeted rewrites for foundational papers (≥10 in-corpus citations) and mature concept pages (≥15 papers). Candidates: VITS, VALL-E, HiFi-GAN, Voicebox, EnCodec. Mark with `quality_pass: opus | YYYY-MM-DD`. Blocked on generation tracking above.
- **Tiered wiki pages** — full vs. summary tiers as corpus scales. Compress low-citation incremental papers to one paragraph; retain frontmatter and URL. Promotable on citation gain. Pruning pass every ~100 ingested.

- **Wiki page migration for 2 ingested arXiv/conference duplicates** — two papers were ingested under arXiv IDs but now have conference versions as canonical (proceedings > arXiv policy). Wiki pages need renaming + re-ingest under conference IDs, then arXiv metadata entries can be fully retired.
  - `wiki/papers/2510.00981.md` → `iclr-2026-kYkfCs4ZAH` (FlexiCodec)
  - `wiki/papers/2508.16790.md` → `neurips-2025-wHsFqmM1rp` (TaDiCodec)
  Both metadata files currently carry `is_duplicate: true` + `canonical_id` as breadcrumbs. Do after concept integration pass to avoid broken links.

### Citation-discovery ingest

- ✅ **Lightweight ingest mode** — done 2026-06-09. `speech-generation-lightweight-ingest-agent` spec built; produces frontmatter + abstract callout + Context section + Wiki Connections. Survey papers use `## Scope and Coverage` instead of Context.
- ✅ **`ingest_tier` metadata field** — done 2026-06-09. All 162 CD metadata files have `ingest_tier` (1 or 2). Final counts: Tier 1 = 94, Tier 2 = 68.
- ✅ **Citation merge candidates** — Added 2026-06-09. All 3 entries in `raw/citation_merge_overrides.json`: CSTR VCTK (~40 raw/title variants), AISHELL-3 (7 variants), GSLM title prefix variant.

### Infrastructure / site

- ✅ **Quartz explorer: exclude `papers/`** — done 2026-06-08. `filterFn` added to `quartz.ts` in site repo (excludes `papers/` and `tags/`; YAML can't express functions).
- **Dedup check at fetch/pre-parse stage** — 15 arXiv/proceedings duplicates resolved manually 2026-05-28. Add `scripts/discover/dedup_check.py` for title-based collision detection after each fetch. Canonical priority: proceedings > arXiv.
- ✅ **Citation index: remove prefilter + fix deduplication** — done 2026-06-07. Post-hoc merge pass collapses 570 groups (602 entries merged away); manual overrides file (`raw/citation_merge_overrides.json`) handles edge cases (SpeechTokenizer title variant, CSTR VCTK versions). Default `--min-citations` lowered to 1 (full index: 16,476 entries, 8.5 MB). 5 fuzzy candidates surfaced in output, all confirmed as genuinely different papers (Qwen family, DNSMOS/DNSMOS P.835, Step-Audio variants). Log target fixed (was writing to `wiki/log.md`, now correctly writes to `raw/pipeline_log.md`).
- **Parse quality review** — 8 papers flagged for offline PDF spot-check; report at `raw/parsed/parse_quality_review.md`. Waiting on user results before any `--force` re-runs.

### Product directions

See `docs/THOUGHTS_FOR_IMPROVEMENTS.md` for extended notes. Key directions: RAG research assistant, living benchmark leaderboards, research gap map, living survey paper, org/lab intelligence, automated related-work generation.

- **Wiki about/documentation page** — write `wiki/about.md` covering: the 3-repo structure (infra, content, site), project philosophy (living systematic review, compounding knowledge base), how the ingest pipeline works, how to contribute or report errors, and FAQs. Link from the wiki landing page (`wiki/index.md`). Should be human-written or lightly assisted — not agent-generated.

---

## Pipeline & codebase improvements

### Completed (2026-06-01, session 22)

- ✅ Writing style guidelines (`docs/WRITING_STYLE.md`)
- ✅ Claims extraction (`## Claims` section, 2–5 generalised propositions)
- ✅ Field significance frontmatter + prose section
- ✅ Concept page redesign (research briefing format)
- ✅ Concept evidence digests (`wiki/concepts/_evidence/{slug}.yaml`)
- ✅ Architecture figures in paper pages (architectural-novelty only, 0–2 per paper)
- ✅ Callout system (4 types with precise trigger rules)
- ✅ Merged paper card (`> [!abstract]` callout)
- ✅ Title deduplication fix (H1 stripped from 121 pages)
- ✅ Log split (`wiki/log.md` reader-facing; `raw/pipeline_log.md` infra-facing)
- ✅ Venue page naming (`{year}-{venue}` for chronological sorting)
- ✅ Quartz display names (frontmatter `title:` on all index pages)
- ✅ Wiki landing page redesign + folder index split
- ✅ `trends/` eliminated (replaced by concept Trend Summary + `wiki/reports/`)

