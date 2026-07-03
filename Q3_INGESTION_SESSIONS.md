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

### 2026-07-02 to 2026-07-03 — Q3 August Interspeech/workshop batch (session 5)

**Scope:** 23 papers ingested chronologically in batches of 4, one paper at a time with a health check after each — continuing from `2507.20731` through the start of the large Interspeech 2025 block (papers dated 2025-08-01 and 2025-08-17).

**Completed:**

1. **23-paper ingest batch** (chronological):
   - 2507.20731 (Neural Vocoder Range-Null Space, arXiv)
   - 2025.ccl-1.77 (HFSD-V2C Visual Voice Cloning, workshop)
   - 2025.icnlsp-1.34 (DPO for TTS on Unlabeled Speech, workshop)
   - 2025.sigdial-1.21 (TRPDformer turn-taking, workshop)
   - 2025.sigdial-1.27 (EmoNews SDS, workshop)
   - 2025.sigdial-1.51 (rrSDS 2.0, workshop)
   - interspeech-2025-0166 (Frozen LLMs Perceive Paralinguistics, Interspeech)
   - interspeech-2025-0305 (DAFMSVC singing VC, Interspeech)
   - interspeech-2025-0347 (PeriodCodec, Interspeech)
   - interspeech-2025-0355 (Codec Robustness Probing, Interspeech)
   - interspeech-2025-0383 (VC for Likability Control, Interspeech)
   - interspeech-2025-0433 (Human-to-Animal VC, Interspeech)
   - interspeech-2025-0438 (LinearVC, Interspeech)
   - interspeech-2025-0464 (Prosody-Adaptable Codecs for Zero-Shot VC, Interspeech)
   - interspeech-2025-0506 (EnCodecMAE, Interspeech)
   - interspeech-2025-0656 (EEG-based VC, Interspeech)
   - interspeech-2025-0706 (Contextual Paralinguistic Data Creation, Interspeech)
   - interspeech-2025-0756 (A-SMiLE affective MoE adapter, Interspeech)
   - interspeech-2025-0998 (Voice-ENHANCE diffusion VC, Interspeech)
   - interspeech-2025-1020 (Prosody Embedding Codebook, Interspeech)
   - interspeech-2025-1081 (Speaker Normalization + Content Restoration VC, Interspeech)
   - interspeech-2025-1084 (Streaming TTS with RVQ/Mamba, Interspeech)
   - interspeech-2025-1098 (GST-BERT-TTS, Interspeech)

2. **Recurring QC issues this session (updated):**
   - **Index count drift got worse, not better** — `wiki/index.md`'s 4-occurrence paper-count prose drifted from the true `wiki/papers/index.md` row count on roughly half of all papers this session, by as much as ±8 (not just off-by-one). This persisted even after adding an explicit "run `grep -c \"^| \\[\\[\" wiki/papers/index.md` after appending your row and use that exact number" instruction to every prompt. Manual `grep -c` verification + correction after every single paper is now mandatory, not optional.
   - **`spoken-language-model`/`subjective-evaluation` tag precision, both directions** — under-tagged `subjective-evaluation` on papers reporting genuine MOS/listening tests (missed 3 times), over-tagged `subjective-evaluation` on papers using only automated/LLM-judge scoring (caught once), and over-tagged `spoken-language-model` on non-generative systems. Established working precedent: speech-in/text-out systems via a frozen or fine-tuned LLM backbone (e.g. DeSTA2, SpeechEmotionLlama-style) DO qualify for `spoken-language-model` in this corpus's actual practice, even though the concept's written definition emphasizes speech-to-speech generation — this is a documented tension worth resolving later (see `docs/content.md` concept registry vs. `wiki/concepts/spoken-language-model.md` abstract).
   - **Agent self-report cannot be trusted** — twice this session an ingest agent's final summary explicitly stated a tag should NOT be applied (with correct reasoning), while the actual file it wrote included that exact tag anyway. Every QC pass now requires re-reading the actual frontmatter/Wiki Connections from the file, never trusting the agent's narrated summary.
   - **Wikilink format is context-dependent and gets confused in both directions** — `wiki/papers/index.md`'s ID column must be a bare `[[id]]` (display title is the next column); everywhere else (Wiki Connections, inline citations) must be piped `[[id|Display Name]]`. Agents mixed these up in both directions this session.
   - **Rejected-duplicate citation trap** — one paper cited a rejected arXiv duplicate ID instead of the canonical ingested ID for the same paper (same title, different ID, exact F5-TTS-style trap from memory). Always verify a cited in-corpus ID has `status: ingested` and an existing wiki page before trusting the citation.
   - **Batch execution undercounting** — three separate times a requested "batch of four" only resulted in 3 ingest agents actually being launched; two were caught via user-visible arithmetic mismatches, one slipped through silently and was only resolved because the next batch happened to start with the missed paper. No papers were permanently lost, but batch launch counts need to be verified against the intended size before reporting completion.
   - **Session-limit interruptions, twice** — one ingest agent was cut off after writing only the paper page and figure assets, before completing index/venue/log/metadata updates; recovered by manually completing the remaining steps. A second agent was cut off before any file writes; a clean retry from scratch was safe.

3. **Date rollover mid-session** — the calendar date changed from 2026-07-02 to 2026-07-03 partway through the batch. Ingest agents handled this correctly on their own (new `## 2026-07-03` section inserted at the top of `wiki/log.md`, `ingested_date`/`generation.date` fields consistent, `Last updated` bumped) — no manual correction needed.

**Corpus after session:** 445 ingested pages. Q3 2025 progress: 220 ingested, 146 remaining.

**Next session:** Continue Q3 2025 chronologically from `interspeech-2025-1106` (LSCodec).

---

### 2026-07-03 — Q3 Interspeech continuation (session 6, in progress)

**Scope:** Continuing Q3 2025 chronologically, one paper at a time with health check + go-ahead between papers.

**Completed so far:**

1. interspeech-2025-1106 (LSCodec, Interspeech) — codec paper, `field_significance: moderate/architectural-novelty`, no `review_flags` raised. Figure-2 (architecture diagram) embedded after confirming figure-1 was the ISCA-logo false positive.

2. **Index count drift recurrence** — the ingest agent reported `wiki/index.md` at 442 papers after this ingest; actual `grep -c "^| \[\[" wiki/papers/index.md` was 446, a 4-paper undercount. Corrected all four occurrences in `wiki/index.md` by hand (abstract callout, "Papers and Venues" section ×2, "Reports" section). This confirms the session-5 finding that manual `grep -c` verification after every paper is required, not optional — the agent's self-reported count cannot be trusted even after the explicit-instruction fix attempted in session 5.

**Batch 1 of 4 (interspeech-2025-1115, -1192, -1210, -1229):**

3. interspeech-2025-1115 (MPE-TTS, Interspeech) — `field_significance: moderate/architectural-novelty`. **review_flag raised**: level sits at moderate/low boundary because the primary baseline (MM-TTS) is a reproduction without an official release, limiting evidential weight of reported gains. Added to Manual Verification Queue below. Also fixed one bare wikilink in Wiki Connections (`[[2301.02111]]` → `[[2301.02111|VALL-E]]`). Index count: agent reported 455, actual was 447 (8-paper overcount) — corrected by hand.

4. interspeech-2025-1192 (Voice Impression Control in Zero-Shot TTS, Interspeech, NTT) — `field_significance: moderate/[architectural-novelty, engineering-integration]`. No review flags; GRL-based control module confirmed as the genuine novel contribution. No wikilink issues. Index count: agent reported 456, actual was 448 (8-paper overcount) — corrected by hand.

5. interspeech-2025-1210 (DiffEmotionVC, Interspeech) — `field_significance: moderate/architectural-novelty`. No review flags. Fixed one bare wikilink in Wiki Connections (`[[2412.10117]]` → `[[2412.10117|CosyVoice 2]]`); reference confirmed as a valid in-corpus citation (CosyVoice 2, ingested). Index count: agent reported 457, actual was 449 (8-paper overcount) — corrected by hand.

6. interspeech-2025-1229 (E2E-BPVC, Interspeech) — `field_significance: moderate/engineering-integration`. No review flags. No wikilink issues (Seed-TTS citation correctly piped). Index count: agent reported 450, actual was 450 — first correct self-report in this session's 4 attempts so far.

**Recurring QC issues this batch:**
- **Index count drift persists at ~8-paper magnitude** — 3 of 4 papers this batch had the agent overcount by exactly 8 (455/456/457 reported vs. 447/448/449 actual); the 4th was correct. Magnitude is consistent enough to suggest the agent may be anchoring on a stale in-context number rather than computing fresh each time, but the fix remains the same: manual `grep -c` verification after every paper, no exceptions.
- **Bare wikilinks in Wiki Connections recurring** — 2 of 4 papers this batch (interspeech-2025-1115, interspeech-2025-1210) had a bare `[[id]]` citation for an in-corpus paper reference despite the explicit piped-format instruction in the prompt; both fixed by hand before health check passed clean.
- Venue page (`2025-interspeech.md`) and `venues/index.md` counts were correct on all 4 papers this batch — no drift observed there.

**Batch 2 of 4 (interspeech-2025-1236, -1334, -1364, -1394):**

7. interspeech-2025-1236 (Accelerating Diffusion-based TTS Training with Dual Modality Alignment / A-DMA, Interspeech) — `field_significance: moderate/architectural-novelty`. No review flags. Four in-corpus citations, all valid and correctly piped, including F5-TTS correctly cited via its canonical ID (2025.acl-long.313, not the arXiv duplicate) — first clean application of that precedent this session. Index count: agent reported 459, actual was 451 (8-paper overcount) — corrected by hand.

8. interspeech-2025-1334 (MiSTR, iEEG-to-speech BCI synthesis, Interspeech) — `field_significance: moderate/architectural-novelty`. No agent-raised review_flags, but **manual flag added**: the agent applied `task: TTS`, though the paper's input is intracranial EEG, not text — no canonical vocabulary term exists for brain-to-speech decoding, and `TTS` (defined as "speech synthesis from text") is a definitional mismatch. Logged to Manual Verification Queue below for a user decision on whether to add a vocabulary term or accept TTS as the closest fit. No wikilink issues. Index count: agent reported 460, actual was 452 (8-paper overcount) — corrected by hand.

9. interspeech-2025-1364 (VS-Singer, Interspeech) — `field_significance: moderate/architectural-novelty`. No agent-raised review_flags, but **caught and fixed directly**: `task: ["singing", "TTS"]` was applied but `related_concepts` omitted the `singing` concept slug (only had diffusion-tts/evaluation-metrics/subjective-evaluation) — added `singing` to `related_concepts` and a corresponding Wiki Connections bullet by hand. No wikilink issues otherwise. Index count: agent reported 461, actual was 453 (8-paper overcount) — corrected by hand.

10. interspeech-2025-1394 (DiEmo-TTS, Interspeech) — `field_significance: moderate/architectural-novelty`. No review flags. First paper this session where the agent's self-reported count (454) matched actual on the first try, and no wikilink issues — prompt addition warning about the task/related_concepts mismatch (from paper 9) may have helped, though this paper didn't have a matching case to test it against.

**Recurring QC issues this batch:**
- **Index count drift continues at exactly 8 on 3 of 4 papers** — same magnitude as batch 1, still resolved only by manual `grep -c` verification.
- **New pattern: task/related_concepts mismatch** — a `task` tag (e.g. `singing`) not mirrored into `related_concepts` even when a matching concept page exists in the registry. Added an explicit instruction about this to the batch's later prompts; one clean paper afterward, but sample size is too small to call it fixed.
- **New pattern: task tag definitional mismatch on edge-domain papers** — MiSTR (brain-to-speech) forced into `task: TTS` for lack of a better vocabulary term. Not an agent error exactly — the controlled vocabulary genuinely has no term for this — but worth a user decision on how to classify future BCI/neural-signal-to-speech papers if more show up in the corpus.

**Corpus so far:** 454 ingested pages.

**Batch 3 of 4 (interspeech-2025-1397, -1434, -1478, -1494):**

11. interspeech-2025-1397 (VibE-SVC, Interspeech) — `field_significance: moderate/architectural-novelty`. No review flags. First clean application of the task/related_concepts precedent from paper 9: tagged `task: ["singing", "VC"]` with `singing` correctly included in `related_concepts` from the start. No wikilink issues. Index count: agent reported 463, actual was 455 (8-paper overcount) — corrected by hand.

12. interspeech-2025-1434 (REWIND, Interspeech) — `field_significance: moderate/architectural-novelty`. No review flags. Fully clean on first try: count (456) matched, VALL-E citation correctly piped, no other issues.

13. interspeech-2025-1478 (LightL2S, Interspeech) — **session-limit interruption on first attempt**: the initial agent run was cut off with no files written at all (confirmed via `raw/metadata` status still `accepted` and no paper page/index/venue/log changes) — a clean retry from scratch was safe, consistent with the "no writes yet" recovery case documented in session 5. On retry: `field_significance: moderate/engineering-integration`. Agent correctly self-flagged the `task: TTS` vocabulary gap this time (lip-to-speech, visual input, no text) as instructed, rather than silently applying it like MiSTR did in batch 2 — added to Manual Verification Queue below. Index count: agent reported 465, actual was 457 (8-paper overcount) — corrected by hand.

14. interspeech-2025-1494 (VisualSpeech, Interspeech) — `field_significance: moderate/[architectural-novelty, engineering-integration]`. No review flags; `task: TTS` correctly justified since text remains the primary input (video is only an auxiliary prosody-conditioning signal) — agent correctly distinguished this from the two prior non-text-input cases (MiSTR, LightL2S) rather than over-flagging. **New QC issue**: health check failed with `claims_section` error — one of four claims had its section citation embedded mid-sentence in parentheses instead of as a trailing `*(§N.N)*` marker, so the health check's citation regex didn't match it. Fixed by hand (moved citation to a proper trailing marker: `*(§3.2, Table 2; §3.3, Table 3)*`). Index count: agent reported 466, actual was 458 (8-paper overcount) — corrected by hand.

**Recurring QC issues this batch:**
- **Index count drift continues at exactly 8** on 3 of 4 papers (all except REWIND) — unchanged from prior batches.
- **Task/related_concepts precedent held** — VibE-SVC applied it correctly on the first try after being added to the prompt in batch 2.
- **Vocabulary-gap self-flagging worked when explicitly instructed** — LightL2S self-flagged the TTS/non-text-input mismatch after being told to do so explicitly in the prompt, unlike MiSTR in batch 2 which silently applied the tag. Suggests this class of issue is promptable when named specifically, unlike the index-count bug.
- **New pattern: malformed claim citations pass the agent's own review but fail health check** — VisualSpeech's citation was embedded inline rather than trailing; this is the first `claims_section` health-check error this session (all prior failures were `wikilink_format`). Worth watching for recurrence.
- **Session-limit interruptions still occur** — one agent this batch was cut off before any file writes; confirmed clean via metadata status and absence of any partial files before retrying.

**Corpus so far:** 458 ingested pages.

**Batch 4 of 3 — final batch, closes out the 16-paper pre-selected queue (interspeech-2025-1531, -1536, -1538):**

15. interspeech-2025-1531 (SVC content encoder via SSL-embedding dimension reduction, Interspeech) — `field_significance: moderate/architectural-novelty`. No review flags. **Recurring gap**: `task: ["singing", "VC"]` applied but `related_concepts` again omitted the `singing` slug, despite an explicit instruction in the prompt (third occurrence this session, after VS-Singer in batch 2) — added `singing` to `related_concepts` and a Wiki Connections bullet by hand. First paper this session with a genuinely correct index-count self-report (459, no drift) and clean trailing citation format throughout.

16. interspeech-2025-1536 (Fairness in Dysarthric Speech Synthesis using F5-TTS, Interspeech) — `field_significance: moderate/[evaluation-contribution, empirical-benchmark]`. No review flags. F5-TTS correctly cited via canonical ID (2025.acl-long.313) — clean application of that precedent. Fully clean: count matched (460), no wikilink issues, all citations properly trailing.

17. interspeech-2025-1538 (StarVC, Interspeech) — `field_significance: moderate/architectural-novelty`. No review flags. `task: VC` confirmed against dedicated VC evaluation (LibriTTS test-clean VC setup vs. TriAAN-VC and CosyVoice baselines). `spoken-language-model` tag verified correct: a Qwen2.5-0.5B LM is adapted to jointly emit text and Mimi codec tokens, matching the "built/adapted LLM emitting discrete speech tokens" precedent exactly. CosyVoice and CosyVoice 2 citations both correct and piped. Index count: agent reported 469, actual was 461 (8-paper overcount) — corrected by hand.

**Recurring QC issues this final batch:**
- **`task`/`related_concepts` singing-slug gap recurred a third time** (interspeech-2025-1531) despite being called out explicitly in the prompt after batches 2 and 3 — this pattern is more persistent than the vocabulary-gap self-flagging fix, which took hold after one explicit correction. Worth a standing note in the ingest agent's base prompt rather than a per-session reminder.
- **Index count drift: final tally for the whole 16-paper queue is 12 of 17 ingest attempts drifted (all but one an exact 8-paper overcount, one earlier a 4-paper undercount), 5 were correct on the first try.** Manual `grep -c` verification caught and corrected every instance; no bad count ever reached a committed file.
- Corpus-wide health check after the full queue: `461 papers, 0 errors, 1178 warnings` — 0 errors confirms the whole 16-paper queue is structurally clean. The 1,178 warnings are accumulated corpus-wide legacy warnings unrelated to this session's papers (not investigated further; out of scope for this ingest pass).

**Queue closed.** All 16 pre-selected papers (interspeech-2025-1106 through interspeech-2025-1538) are ingested. **Corpus: 461 pages.** Q3 2025 progress: 236 ingested, 130 remaining.

**Next session:** Continue Q3 2025 chronologically from `interspeech-2025-1550` (ArVoice, Arabic multi-speaker TTS dataset).

---

## Manual Verification Queue

Papers where the ingest agent emitted `review_flags` in its INGEST_RESULT signal. Review these after the session batch is complete — check the paper page and resolve each flag by hand.

| Paper ID | Flag | Agent note |
|----------|------|------------|
| interspeech-2025-1115 (MPE-TTS) | field_significance | Level sits at moderate/low boundary; primary baseline (MM-TTS) is a reproduction without an official open-source release, limiting the evidential weight of reported gains — could justify low rather than moderate. |
| interspeech-2025-1334 (MiSTR) | task vocabulary gap (caught in manual QC, not agent-raised) | Tagged `task: TTS` for lack of a better term, but input is intracranial EEG, not text — no canonical vocabulary term covers brain-to-speech decoding. Needs a user decision: accept TTS as closest fit, or add a new vocabulary term for future BCI/neural-signal-to-speech papers. |
| interspeech-2025-1478 (LightL2S) | task vocabulary gap (agent self-flagged this time) | Same underlying gap as MiSTR: `task: TTS` applied to lip-to-speech (visual input, no text). Agent flagged it explicitly per this batch's prompt instruction. Same user decision needed — likely resolved together with the MiSTR item once a decision is made (e.g. new vocabulary term, or an explicit documented exception for non-text-input systems). |

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
