# Project Status

Last updated: 2026-05-28 (session 16)

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
| Parse (text extraction) | 🔄 In progress | 611/783 done (after dedup). Queue batches 6–10 pending; 6 remapped from arXiv to proceedings IDs. |
| Ingest (wiki pages) | 🔄 In progress | 39/783 ingested. 5 ingested today (Vevo2, Marco-Voice, OmniVoice, EmoSteer-TTS, Flamed-TTS). ~491 more ready. |

---

## Metadata counts (2026-05-28)

```
Total files:  1000
  accepted:    744   ← after dedup (783 unique papers - 39 ingested)
  ingested:     39   ← wiki page written
    integrated: 25   ← integrated_date set (integration pass run 2026-05-27)
    pending:    14   ← awaiting integration pass (next due after 11 more papers)
  review:        0   ← queue cleared
  rejected:    217   ← 202 + 15 arXiv/proceedings duplicates resolved

PDFs on disk:  ~784  ← raw/papers/ (accepted + ingested; 15 duplicate arXiv PDFs may remain)
Parsed:        577   ← raw/parsed/ (571 original + 6 remapped from arXiv to proceedings IDs)
Parse-pending: 206   ← queue batches 6–10 pending
Ready to ingest: ~491 ← parsed but not yet ingested
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
| 6 | 40 | 2604.06871 … 2604.22821 | pending |
| 7 | 40 | 2604.25441 … interspeech-2025-0355 | pending |
| 8 | 40 | interspeech-2025-0383 … interspeech-2025-1081 | pending |
| 9 | 40 | interspeech-2025-1084 … interspeech-2025-2031 | pending |
| 10 | 27 | interspeech-2025-2032 … interspeech-2025-raju25_interspeech | pending |

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

### Ingest progress (session 13 — 2026-05-27)

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

1. ~~**Integration pass (catch-up)**~~ ✅ Complete — integration pass run on all 25 ingested papers (15-paper pass on 2026-05-27: 16 concepts updated, 3 cross-links added, overview.md written, arxiv-2025 venue page updated).
2. **Continue ingest** — ~491 papers ready. Repeat `speech-generation-ingest-orchestrator: "Ingest up to 5 papers"`; run `speech-generation-integration-agent: "Run integration pass on last 25 papers"` every ~25 papers. Next integration pass due after 11 more papers (25 - 14 pending).
3. **Continue batch parse** — queue batches 5–10 pending (~206 papers; 6 already remapped from arXiv IDs). Workflow: `source .venv/bin/activate && python scripts/parse/batch_convert.py --ids <ids> 2>&1 | tee /tmp/batch_N.log` → spawn quality subagent → save report → update STATUS.md. Get batch IDs from `raw/parsed/batch_queue.json`. Can run in parallel with ingest.
4. **Citation discovery — next candidates** — Top unactioned speech-relevant entries: Moshi (53x, 2410.00037), GLM-4-Voice (35x, 2412.02612), VALL-E 2 (34x, 2406.05370), Llama-omni (28x, 2409.06666). Fetch with `python scripts/fetch/arxiv.py --ids <ids>`, then filter + download. Re-run `scripts/discover/citation_index.py` after each parse batch.
5. **cs.CL re-scan (deferred)** — ~15–30 marginal papers expected; low priority given current backlog.
6. **Periodic maintenance** — re-run fetchers, filter, and `citation_index.py` monthly.

---

## Pipeline & codebase improvements

1. **Ingest agent: image and table reasoning** — The ingest agent currently reads only `paper.md`. Extend it to enumerate `raw/parsed/{id}/assets/` (figure-N.png, table-N.csv) and incorporate key figures/tables into the wiki paper page — link architecture diagrams, extract result tables into the Metrics section, and surface any figures that clarify the method.
2. **Writing style guidelines** — Define a shared style guide for all content-generating agents (ingest, integration, query). Write `docs/WRITING_STYLE.md` covering: tense conventions, how to introduce a contribution, how to write Novelty Assessments honestly, how to write cross-paper comparisons without overclaiming, and handling uncertainty. Reference it explicitly in each agent spec under `.claude/agents/`.
3. **Deduplication check at fetch/pre-parse stage** — 15 arXiv/proceedings duplicate pairs were found and resolved manually on 2026-05-28. Add a title-based dedup gate so this is caught automatically. Options: (a) a `scripts/discover/dedup_check.py` script that scans all non-rejected metadata for normalised-title collisions and can be run after each fetch batch; (b) a `--dedup-check` flag on `batch_convert.py` that refuses to parse a paper whose title already exists under a proceedings ID. Canonical priority rule: proceedings ID (ACL, EMNLP, Interspeech, etc.) > arXiv ID. When swapping, remap `raw/parsed/{arxiv_id}/` → `raw/parsed/{proc_id}/` rather than re-parsing.

