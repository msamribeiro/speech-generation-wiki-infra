# Project Status

Last updated: 2026-06-18 (338 ingested, 276 integrated; all CD complete; standard ingest paused for pipeline redesign)

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
| Keyword filter expansion | ✅ Complete | +11 terms added to `config/keyword_filter.yaml` (2026-05-25). |
| Filter — batches 1–3 | ✅ Complete | All batches scored. Total: 732 accepted, 167 rejected, 0 review pending. |
| Human review — batches 1–3 | ✅ Complete | 77 borderline papers resolved. Review queue cleared. |
| Deduplication (arXiv ↔ ACL + full scan) | ✅ Complete | 38 total duplicates resolved; proceedings ID canonical throughout. |
| PDF download | ✅ Complete | ~1,037 PDFs on disk (875 standard + 162 citation-discovery). 2 withdrawn papers flagged `needs_manual_pdf`: 2503.20999, 2511.08230. |
| Parse (standard) | ✅ Complete | 875/875 parsed (2026-06-06). 0 failures. |
| Citation discovery fetch (bulk) | ✅ Complete | 162 highly-cited out-of-corpus papers written with `status=accepted`, `discovery_source="citation-discovery"`. Script: `scripts/fetch/citation_discovery_fetch.py`. |
| Parse (citation-discovery) | ✅ Complete | 162/162 parsed (2026-06-08). 0 failures. |
| Ingest — standard papers | 🔄 In progress | 176/875 ingested. 699 ready. Standard ingest paused (pipeline redesign session 2026-06-18). |
| Ingest — citation-discovery | ✅ Complete | 162/162 ingested (2026-06-17): 96 Tier 1 full pages + 66 Tier 2 stubs. |
| Integrate | 🔄 In progress | 276/338 integrated (passes 1–11). 30 papers from 2026-06-16 pending (pass 12). |

---

## Metadata counts (2026-06-18)

```
Total files:  1326
  accepted:    699   ← standard papers not yet ingested
  ingested:    338   ← 176 standard + 162 CD (96 T1 full pages + 66 T2 stubs)
    integrated: 276  ← passes 1–11 complete; 30 from 2026-06-16 pending pass 12
  pending:       0   ← cleared
  review:        0   ← queue cleared
  rejected:    289   ← includes 2 withdrawn arXiv papers (2503.20999, 2511.08230)

PDFs on disk:  ~1037 ← raw/papers/ (875 standard + 162 citation-discovery)
Parsed:         861  ← all accepted papers parsed (complete 2026-06-08)
Ready to ingest: 699 ← standard papers (parsed + accepted, not yet ingested)

Concept stubs:   24  ← pending migration to wiki/_claims/ schema (see BACKLOG)
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
| `scripts/parse/download_pdfs.py` | Downloads PDFs for all accepted papers; resumable, per-domain rate limiting |
| `scripts/discover/citation_index.py` | Builds `raw/citation_index.json` from all parsed `references.json` files; run after each parse batch |
| `lib/keyword_filter.py` | Shared keyword filter logic used by all fetchers |
| `.claude/agents/speech-generation-filter-agent.md` | Relevance scoring agent; invoke on any new pending batch |

### Extending the corpus

```bash
# Top up cs.SD + eess.AS (run periodically)
python scripts/fetch/arxiv.py --date-from 2026-05-22

# Top up cs.CL
python scripts/fetch/arxiv_oai.py --set cs.CL --date-from 2026-05-22

# Next year's ACL Anthology
python scripts/fetch/acl.py --years 2026 --all-workshops
```
