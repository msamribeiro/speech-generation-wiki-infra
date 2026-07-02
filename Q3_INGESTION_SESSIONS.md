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

Also check the INGEST_RESULT signal for `review_flags`. If any flags are present, add the paper to the **Manual Verification Queue** above with the flag field and agent's reason. Resolve flagged papers by hand after the batch completes — do not block the next paper on them.

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

### 2026-07-01 — Pre-Q3 + Q3 ACL/arXiv batch (session 3)

**Scope:** 30 papers ingested chronologically — completing the pre-Q3 backlog (papers 1–8, April–June 2025) and starting Q3 2025 (papers 9–30, July 2025 ACL + workshop + arXiv papers).

**Completed:**

1. **New QC feature** — added `review_flags` field to the ingest agent's INGEST_RESULT JSON signal. Agent emits flags only when genuinely uncertain about `claims` role assignment or `field_significance` level (precision gate, not recall gate). Manual Verification Queue added to this session note. No flags raised across all 30 papers.

2. **30-paper ingest batch** (chronological):
   - 2025.naacl-long.591 (VAT length generalisation, NAACL)
   - 2025.naacl-short.65 (kNN-TTS, NAACL)
   - 2025.naacl-short.69 (Indigenous language TTS, NAACL)
   - 2025.iwsds-1.11 (Paralinguistic attitude recognition, IWSDS)
   - 2025.iwsds-1.27 (Turn-taking survey, IWSDS)
   - 2505.15772 (MIKU-PAL emotion annotation benchmark, arXiv)
   - 2507.06235 (Super Kawaii Vocalics, arXiv)
   - 2506.23049 (AURA cascaded SCA, arXiv)
   - 2025.acl-long.681 (SIFT-50M, ACL)
   - 2025.acl-long.790 (Rhythm-Controllable VC, ACL)
   - 2025.acl-long.817 (SimulS2S-LLM, ACL)
   - 2025.acl-long.87 (Takin-VC, ACL)
   - 2025.acl-long.937 (UniCodec, ACL)
   - 2025.acl-long.997 (Align-SLM, ACL)
   - 2025.conll-1.9 (Intonational phrasing in TTS, CoNLL)
   - 2025.findings-acl.101 (Chain-Talker, ACL)
   - 2025.findings-acl.115 (SLAM-Omni, ACL)
   - 2025.findings-acl.1226 (PodAgent, ACL)
   - 2025.findings-acl.470 (Voice assistant context recall, ACL)
   - 2025.findings-acl.534 (Speech instruction query rewriting, ACL)
   - 2025.findings-acl.631 (Slamming, ACL)
   - 2025.findings-acl.687 (TCSinger 2, ACL)
   - 2025.findings-acl.71 (ASK-QA + DAMSEL, ACL)
   - 2025.findings-acl.75 (Unit language guidance S2ST, ACL)
   - 2025.findings-ijcnlp.49 (DST in Japanese full-duplex dialogue, ACL)
   - 2025.iwslt-1.5 (SSR modality connector, IWSLT)
   - 2025.unlp-1.11 (Ukrainian TTS lexical stress, workshop)
   - 2412.18603 (SpeechSSM long-form speech, ICML)
   - 2503.11026 (MAVFlow AV2AV translation, arXiv)
   - 2505.15670 (SALM-Duplex, arXiv)

3. **QC fixes** — 7 bare wikilinks fixed across 6 papers (2506.23049, 2025.acl-long.817, 2025.findings-acl.101 citation format, 2025.findings-acl.470, 2025.findings-ijcnlp.49, 2503.11026 ×2). Index count corrected after each paper (recurring agent off-by-one bug).

**Corpus after session:** 393 ingested pages.

**Late addition (session 3 wrap-up):** 2 more papers ingested to reach 32 total for the session:
   - 2506.09874 (UmbraTTS, arXiv) — environment-aware TTS via flow matching; architecture figure included
   - 2506.18296 (JIS corpus, Interspeech) — Japanese idol speaker corpus; dataset-contribution only

**Corpus after session:** 395 ingested pages.

**Next session:** Continue Q3 2025 chronologically from `2506.23325` (XY-Tokenizer).

---

### 2026-07-02 — Q3 arXiv July batch (session 4)

**Scope:** 28 papers ingested chronologically — July 2025 arXiv papers (2507.xxxxx), covering the backlog that predated XY-Tokenizer and continuing through late July 2025.

**Completed:**

1. **Claims format upgrade** — changed the two-line claims format across all agents, docs, and 80 existing paper pages:
   - Old: `- supports: {claim}\n  Evidence: {detail} *(§N.N)*`
   - New: `- **supports:** {claim}\n  > *Evidence:* {detail} *(§N.N)*`
   - Updated: ingest agent, integration agent, review agent, `docs/writing-style.md`, `docs/content.md`, `scripts/checks/ingest.py` (comment only — logic unchanged). Bulk sed conversion of all 80 existing pages passed corpus-wide health check with 0 errors.

2. **28-paper ingest batch** (chronological):
   - 2507.02176 (Speaker Similarity Assessment, arXiv)
   - 2507.00808 (Multi-interaction TTS, arXiv)
   - 2507.01611 (QHARMA-GAN vocoder, arXiv)
   - 2507.02380 (JoyTTS spoken chatbot, arXiv)
   - 2507.03887 (Traceable TTS, arXiv)
   - 2507.03912 (Prosody Labeling Phoneme-BERT, arXiv)
   - 2507.08012 (RepeaTTS, arXiv)
   - 2507.04349 (TTS-CtrlNet emotion, arXiv)
   - 2507.04598 (Hierarchical Emotion Distribution TTS, arXiv)
   - 2507.04817 (Fast-VGAN VC, arXiv)
   - 2507.01348 (SpeechAccentLLM, arXiv)
   - 2507.06116 (Speech Quality Assessment MoE, arXiv)
   - 2506.23325 (XY-Tokenizer codec, arXiv)
   - 2507.07799 (SecureSpeech, arXiv)
   - 2507.08319 (Active Learning for TTS, arXiv)
   - 2507.09070 (SemAlignVC, arXiv)
   - 2507.09282 (ClaritySpeech dementia obfuscation, arXiv)
   - 2507.09310 (Lombard VC, arXiv)
   - 2507.10985 (Pronunciation Deviation Analysis, arXiv)
   - 2507.12197 (QTTS / QDAC codec, arXiv)
   - 2507.14988 (DMOSpeech 2 RL duration, arXiv)
   - 2507.15272 (A2TTS Indian languages, arXiv)
   - 2507.16875 (Duration Prediction tech report, arXiv)
   - 2507.21138 (TTS-1 Technical Report, arXiv)
   - 2507.18119 (GOAT-SLM paralinguistics, arXiv)
   - 2507.18897 (HH-Codec, arXiv)
   - 2507.17527 (Seed LiveInterpret 2.0, arXiv)
   - 2507.20140 (Do Not Mimic My Voice unlearning, arXiv)

3. **QC fixes** — 22 bare wikilinks fixed across 13 papers. F5-TTS ID corrected from `2410.06885` to canonical `2025.acl-long.313` in 2507.04349. Index count corrected after every paper (recurring agent off-by-one).

**Corpus after session:** 423 ingested pages.

**Next session:** Continue Q3 2025 chronologically from `2507.20731` (Neural Vocoder Range-Null Space).

---

## Manual Verification Queue

Papers where the ingest agent emitted `review_flags` in its INGEST_RESULT signal. Review these after the session batch is complete — check the paper page and resolve each flag by hand.

| Paper ID | Flag | Agent note |
|----------|------|------------|
| _(none yet)_ | | |

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
