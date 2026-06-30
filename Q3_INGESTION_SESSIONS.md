# Q3 2025 Ingest Session

**Date:** 2026-06-29
**Goal:** Ingest all remaining Q3 2025 (July–September 2025) accepted papers into the wiki.

---

## Scope

| Status | Count |
|--------|-------|
| Already ingested (Q3 2025) | 145 |
| Remaining to ingest | 221 |
| Rejected | 105 |
| **Total Q3 2025 in corpus** | **471** |

All 221 remaining papers are Tier 1. No Tier 2 stubs needed for this quarter.

---

## Success Criteria

- All 221 accepted Q3 2025 papers have status `ingested` in `raw/metadata/`
- Health check passes corpus-wide with zero errors:
  ```bash
  python3 scripts/health_check.py --ingest --wiki-dir /Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content
  ```

---

## Methodology

### Claims format

All new paper pages use the structured claims format introduced in this session:

```markdown
## Claims

- supports: {Generalized claim sentence.}
  Evidence: {Specific result, mechanism, comparison, dataset, or ablation.} *(§N.N, Table N)*
- complicates: {Generalized claim sentence.}
  Evidence: {Specific limitation, failure case, or trade-off.} *(§N.N)*
```

Each claim must carry:
- a **role prefix** (`supports:`, `complicates:`, `contradicts:`, or `refines:`)
- a **field-level proposition** (no paper names, model names, or raw metrics)
- an `Evidence:` continuation line with the paper-local concrete detail and a section citation

### Ingest cadence

- One paper at a time
- Run health check after each paper; fix any error before proceeding
- No parallel ingest workers

### Quality check after each paper

```bash
python3 scripts/health_check.py --ingest {ID} --wiki-dir /path/to/wiki-content
```

Fix bare wikilinks and any schema errors before marking the paper done.

---

## Session Log

### 2026-06-29 — Pre-Q3 batch + dedup (session 1)

**Scope:** Preparatory work before starting Q3 ingest — dedup pass + 16 earliest remaining accepted papers (pre-Q3, chronological).

**Completed:**

1. **OpenReview dedup pass** — 8 collisions found among 56 OpenReview papers (ICLR 2025: 13, NeurIPS 2025: 16, ICLR 2026: 27). ArXiv records marked `is_duplicate`, proceedings records marked `ingested` with `wiki_page_id`. 8-paper migration list added to BACKLOG (deferred until after integration pass). `scripts/fetch/dedup_openreview.py` created.

2. **16-paper ingest batch** — all NAACL 2025, ICLR 2025, and workshop papers:
   - 2409.09098 (AccentBox, arXiv 2024)
   - 2025.coling-industry.29 (CarMem, COLING Industry)
   - 2025.chipsal-1.18 (Nepali TTS, CHiPSAL)
   - 2025.coling-main.685 (VoxpopuliTTS, COLING)
   - 2409.20007 (DeSTA2, arXiv 2024)
   - 2025.computel-main.6 (Ojibwe TTS, ComputEL)
   - 2025.nodalida-1.32 (Estonian TTS, NoDaLiDa)
   - 2025.naacl-srw.6 (Codec-LM Co-design, NAACL)
   - 2025.findings-naacl.298 (Gender Bias in TTS, NAACL)
   - 2025.findings-naacl.471 (Prosody/SQA, NAACL)
   - 2025.naacl-long.464 (ManaTTS Persian, NAACL)
   - 2025.naacl-long.619 (ProSE, NAACL)
   - iclr-2025-tQ1PmLfPBL (PeriodWave, ICLR)
   - iclr-2025-cuFzE8Jlvb (Continuous Autoregressive Modeling, ICLR)
   - iclr-2025-dGSOn7sdWg (SyllableLM, ICLR)
   - iclr-2025-868masI331 (HALL-E, ICLR)

**Corpus after session:** 354 ingested pages.

**Two ICLR 2025 papers deferred to next session:**
- `iclr-2025-hQvX9MBowC` (DiTTo-TTS)
- `iclr-2025-uxDFlPGRLX` (FlowDec)

**Recurring QC issues to watch:**
- Agent writes unquoted YAML scalars for `published_date`, `ingested_date`, `generation.date`, `field_significance.type` — fix manually in QC
- Agent uses array `["architectural-novelty"]` for single `field_significance.type` — should be quoted string `"architectural-novelty"`
- Agent sometimes uses unquoted strings inside `task`/`architecture`/`conditioning`/`training` arrays
- Spurious `multilingual-tts` on single-language papers (any language — remove if only one language)
- Spurious `VC` on cross-accent/voice-cloning papers not evaluated on L2-ARCTIC/ESD/VCTK conversion

**Q3 2025 status after session:** 221 Q3 papers remaining, ingest not yet started. Next: DiTTo-TTS + FlowDec (two deferred ICLR papers), then Q3 ingest chronologically.

---

### 2026-06-30 — Pre-Q3 ICLR + remaining NAACL batch (session 2)

**Scope:** Ingested 8 accepted papers chronologically (pre-Q3 backlog, through 2025-04-29), completing the deferred ICLR papers and the remaining NAACL 2025 Findings/Demo/Long papers not covered in session 1.

**Completed:**

1. **Scope correction** — broadened ingest scope from "Q3 2025 only (Jul–Sep)" to "all accepted papers chronologically through end of Q3 2025," surfacing 17 pre-Q3 papers still uningested. Fixed `raw/metadata/2601.13910.json` conference date (IJCNLP-AACL 2025 met Dec 20–24 2025, not Jan 2025).

2. **8-paper ingest batch** (two batches of 4, with cross-paper critique round after each):
   - iclr-2025-hQvX9MBowC (DiTTo-TTS, ICLR)
   - iclr-2025-uxDFlPGRLX (FlowDec, ICLR)
   - 2025.findings-naacl.130 (DiVISe, NAACL Findings)
   - 2025.findings-naacl.279 (BnTTS, NAACL Findings)
   - 2025.findings-naacl.38 (Prompt-Guided Selective Masking Loss, NAACL Findings)
   - 2025.naacl-demo.12 (ESPnet-SpeechLM, NAACL Demo)
   - 2025.naacl-demo.21 (ESPnet-SDS, NAACL Demo)
   - 2025.naacl-long.484 (Behavior-SD, NAACL)

3. **Infrastructure fix** — `scripts/checks/ingest.py` claims-citation check was a false positive: it only scanned `- ` bullet lines, missing the `Evidence:` continuation line where `*(§N.N)*` actually lives in the two-line claims format. Fixed to group each bullet with its continuation lines before checking.

4. **Corpus-wide venue drift fix** — `venues/index.md` had stale paper counts across most active venue rows (years of blind +1 increments). Synced all rows to authoritative venue-page frontmatter values in one pass.

**Corpus after session:** 363 ingested pages.

**Recurring QC issues to watch (updated):**
- Spurious `multilingual-tts` on single-language papers — remove if paper covers only one language, even if it adapts a multilingual framework
- Spurious `spoken-language-model` on papers that merely use a text LLM as an upstream conditioning module — concept requires discrete speech tokens, no text intermediate
- Ingest agents count `index.md` paper count before finishing their own write (off by one) — add "count as the very last step after all files written" to ingest prompt; verify and correct in QC
- Bare wikilinks `[[id]]` instead of `[[id|Name]]` still occur occasionally in Wiki Connections; now caught by health check (wikilink_format warning)
- `field_significance.type` is correctly a list (array) per docs/content.md schema — the prior note saying "should be string not array" was incorrect

**Next session:** Continue chronologically — 2025.iwsds-1.11 (Paralinguistic Attitude Recognition), 2025.iwsds-1.27 (Turn-taking Survey), 2507.06235 (Super Kawaii Vocalics), 2505.15772 (MIKU-PAL), then remaining pre-Q3 papers, then Q3 2025 (Jul–Sep) papers.

---

## Progress

Track by running:

```bash
python3 -c "
import json, glob
accepted, ingested = 0, 0
for path in glob.glob('raw/metadata/*.json'):
    m = json.load(open(path))
    y, mo = str(m.get('year','')), str(m.get('month','0')).zfill(2)
    if y == '2025' and mo in ('07','08','09'):
        if m['status'] == 'accepted': accepted += 1
        if m['status'] == 'ingested': ingested += 1
print(f'Ingested: {ingested} | Remaining: {accepted}')
"
```
