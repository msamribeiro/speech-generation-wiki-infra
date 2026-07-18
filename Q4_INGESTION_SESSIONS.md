# Q4 2025 Ingest Session

**Date:** 2026-07-17
**Goal:** Ingest all remaining Q4 2025 (October–December 2025) accepted papers into the wiki.

Bootstrapped from `docs/records/2026-07-17-q3-2025-ingestion-sessions.md`, which holds the full
paper-by-paper Q3 2025 log (13 sessions, 364 papers, complete). This file carries forward the
ingestion protocol and cadence preferences refined during Q3, without the historical narrative.

---

## Scope

| Status | Count |
|--------|-------|
| Already ingested (Q4 2025) | 51 |
| Remaining to ingest | 133 |
| Rejected | 63 |
| **Total Q4 2025 in corpus** | **247** |

As of session 14 close (2026-07-18). Corpus stands at **616 wiki pages**, 0 errors corpus-wide.
Counts computed from `raw/metadata/*.json` where `year == 2025` and `month in (10, 11, 12)`
(these fields are derived from `published_date`, not the arXiv ID prefix — see the ID-prefix
note below). Re-run before starting a session, as fetch/filter may still be adding papers:

```bash
.venv/bin/python3 -c "
import json, glob
accepted, ingested, rejected = 0, 0, 0
for path in glob.glob('raw/metadata/*.json'):
    m = json.load(open(path))
    y, mo = str(m.get('year','')), str(m.get('month','0')).zfill(2)
    if y == '2025' and mo in ('10','11','12'):
        if m['status'] == 'accepted': accepted += 1
        if m['status'] == 'ingested': ingested += 1
        if m['status'] == 'rejected': rejected += 1
print(f'Ingested: {ingested} | Remaining: {accepted} | Rejected: {rejected}')
"
```

---

## Next Session — Resume Here

To continue, just say something like **"Let's continue ingesting"**. Everything needed is below
and in the linked memories (auto-loaded via `MEMORY.md` at session start).

**Before starting:** re-run the progress-count script above — fetch/filter may have added papers
since 2026-07-18, which would shift IDs/counts. If the list below no longer matches
`raw/metadata/`'s current `accepted` set for Q4 2025, re-select fresh candidates chronologically
by `published_date` rather than assuming this list is still accurate.

**Pre-selected candidates (32 papers, 8 batches of 4), chronological by `published_date`,**
starting from the first remaining paper after `2510.08392` (last ingested, session 14):

| # | ID | Date | Venue | Task | Title |
|---|----|----|----|----|----|
| 1 | `2510.09061` | 2025-10-10 | EMNLP | VC | O_O-VC: Synthetic Data-Driven One-to-One Alignment for Voice Conversion |
| 2 | `2510.09016` | 2025-10-10 | arXiv | singing | DiTSinger: Scaling Singing Voice Synthesis with Diffusion Transformers |
| 3 | `2506.12311` | 2025-10-10 | arXiv | TTS | Phonikud: Hebrew Grapheme-to-Phoneme Conversion for Real-Time TTS |
| 4 | `2510.09424` | 2025-10-10 | arXiv | SCA | The Speech-LLM Takes It All: A Truly Fully End-to-End SCA |
| 5 | `2510.09592` | 2025-10-10 | arXiv | SCA | Mind-Paced Speaking: A Dual-Brain Approach to Real-Time Spoken Dialogue |
| 6 | `2510.09245` | 2025-10-10 | arXiv | VC | SynthVC: Leveraging Synthetic Data for End-to-End Low-Latency VC |
| 7 | `2510.10003` | 2025-10-11 | arXiv | TTS, SCA | MTP-S2UT: Enhancing Speech-to-Speech Translation Quality |
| 8 | `2510.10774` | 2025-10-12 | arXiv | TTS | ParsVoice: A Large-Scale Multi-Speaker Persian Speech Corpus |
| 9 | `2510.10785` | 2025-10-12 | arXiv | VC | FAC-FACodec: Controllable Zero-Shot Foreign Accent Conversion |
| 10 | `2510.11646` | 2025-10-13 | arXiv | TTS | BridgeCode: A Dual Speech Representation Paradigm |
| 11 | `2510.11124` | 2025-10-13 | arXiv | TTS | Perturbation Self-Supervised Representations for Cross-Lingual TTS |
| 12 | `2510.12964` | 2025-10-14 | arXiv | VC | VCTR: A Transformer-Based Model for Non-Parallel Voice Conversion |
| 13 | `2510.12116` | 2025-10-14 | EMNLP | SCA | Understanding the Modality Gap: An Empirical Study |
| 14 | `2510.12995` | 2025-10-14 | arXiv | TTS | Continuous-Token Diffusion for Speaker-Referenced TTS |
| 15 | `2510.13221` | 2025-10-15 | arXiv | codec | Acoustic Teleportation via Disentangled Neural Audio Codec |
| 16 | `2510.13293` | 2025-10-15 | arXiv | TTS | Cross-Modal Consistency Guidance for Robust Emotion Control |
| 17 | `2510.13194` | 2025-10-15 | arXiv | TTS | StressTransfer: Stress-Aware Speech-to-Speech Translation |
| 18 | `2510.15364` | 2025-10-17 | arXiv | codec | LDCodec: A High-Quality Neural Audio Codec with Low Complexity |
| 19 | `2510.15227` | 2025-10-17 | arXiv | codec | LongCat-Audio-Codec: An Audio Tokenizer and Detokenizer |
| 20 | `2510.16841` | 2025-10-19 | arXiv | codec | SAC: Neural Speech Codec with Semantic-Acoustic Dual-Stream |
| 21 | `2510.16718` | 2025-10-19 | arXiv | codec | U-Codec: Ultra Low Frame-Rate Neural Speech Codec |
| 22 | `2503.06211` | 2025-10-20 | arXiv | SCA, TTS | Late Fusion and Multi-Level Fission Amplify Cross-Modal Transfer |
| 23 | `2510.18308` | 2025-10-21 | arXiv | TTS | ParaStyleTTS: Toward Efficient and Robust Paralinguistic Control |
| 24 | `2506.23670` | 2025-10-21 | arXiv | TTS, SCA | Efficient Interleaved Speech Modeling through Knowledge Distillation |
| 25 | `2510.19509` | 2025-10-22 | arXiv | evaluation | Which Evaluation for Which Model? A Taxonomy for Speech |
| 26 | `2510.20210` | 2025-10-23 | arXiv | TTS, evaluation | Vox-Evaluator: Enhancing Stability and Fidelity for Zero-Shot TTS |
| 27 | `2510.20513` | 2025-10-23 | arXiv | TTS, evaluation | Decoding the Ear: A Framework for Objectifying Expressiveness |
| 28 | `2510.20677` | 2025-10-23 | arXiv | singing, VC | R2-SVC: Towards Real-World Robust and Expressive Zero-Shot SVC |
| 29 | `2510.21209` | 2025-10-24 | Interspeech | codec | SpecTokenizer: A Lightweight Streaming Codec |
| 30 | `2510.21685` | 2025-10-24 | arXiv | singing, VC | StylePitcher: Generating Style-Following and Expressive Singing |
| 31 | `2510.22241` | 2025-10-25 | arXiv | codec | FOA Tokenizer: Low-Bitrate Neural Codec for First-Order Ambisonics |
| 32 | `2510.22588` | 2025-10-26 | arXiv | TTS, SCA | UltraVoice: Scaling Fine-Grained Style-Controlled Speech |

Batches: 1–4, 5–8, 9–12, 13–16, 17–20, 21–24, 25–28, 29–32 (matching the standard cadence below).

**Pre-flight checks already done for this list (2026-07-18), don't need to be re-run unless the
list changes:**
- No duplicate/full-version signals found — checked `arxiv_comment` on all 3 papers whose arXiv
  ID prefix doesn't match `published_date` (`2506.12311`, `2503.06211`, `2506.23670`); none say
  "full version of" or similar, and none title-match an existing wiki page. See
  [[feedback_arxiv_full_version_dedup]] for what this check looks for and why.
- No exact-title collisions found against `papers/index.md` for any of the 32.
- `2510.07978`-style scope questions may recur among the SCA papers (`2510.09424`, `2510.09592`,
  `2510.10003`, `2510.12116`) — read each carefully before ingesting; see the corpus-scope
  precedent chain below.

---

## Success Criteria

- All accepted Q4 2025 papers have `status: ingested` in `raw/metadata/`
- Health check passes corpus-wide with zero errors:
  ```bash
  .venv/bin/python scripts/health_check.py --module ingest --wiki-dir /Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content
  ```

---

## Methodology

### Claims format

```markdown
## Claims

- **supports:** {Generalized, field-level claim sentence — no paper/model names or raw metrics.}
  > *Evidence:* {Specific result, mechanism, comparison, dataset, or ablation.} *(§N.N, Table N)*
- **complicates:** {Generalized claim sentence.}
  > *Evidence:* {Specific limitation, failure case, or trade-off.} *(§N.N)*
```

Role prefix is one of `supports:`, `complicates:`, `contradicts:`, `refines:`, bolded. The
`Evidence:` line is an italic-led blockquote with paper-local detail and a section citation.
Named-section citations need the `§` prefix even for non-numbered sections (e.g. `*(§Limitations)*`).

### Ingest cadence

Default (as run throughout the back half of Q3, sessions 10–13): pre-select the full remaining
list chronologically up front, then work through it in batches of 4. Within each batch:

1. One paper at a time — no parallel ingest workers.
2. Run the per-paper health check after each paper; fix bare wikilinks and any schema errors
   before moving to the next paper.
3. After all 4 papers in the batch are clean, write a short batch summary (paper IDs, notable
   QC catches, corpus page count, updated Q4 progress numbers) and append it to this file's
   Session Log.
4. Wait for an explicit go-ahead before starting the next batch.

The user may drop to one-paper-at-a-time-with-go-ahead mid-session; follow whichever cadence
was most recently requested rather than defaulting back silently.

### Quality check after each paper

```bash
.venv/bin/python scripts/health_check.py --module ingest --id {ID} --wiki-dir /Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content
```

Do not trust the ingest agent's own closing summary for any of the following — always verify
the actual files independently:

- **Paper count drift.** `wiki/index.md`'s paper-count callout (4 occurrences: abstract callout,
  "Papers" section line, "Browse all N papers" link, "first report is due" line) drifts on most
  ingests, in both directions, with no reliable pattern. After every paper, independently run
  `ls wiki/papers/*.md | grep -v index.md | wc -l` and `grep -c '^| \[\[' wiki/papers/index.md`
  (these two should always match each other) and fix `index.md` directly against that number.
  This is not fixable by prompting — budget for a manual fix on every single paper.
- **Citation integrity.** Before trusting a `[[wikilink]]` the agent added to Wiki Connections,
  confirm the target actually has a wiki page (`ls wiki/papers/{id}.md`) and isn't just
  `status: accepted` or `rejected` in metadata. If it has no page yet, keep the ID in
  `related_papers` frontmatter but remove it from the linked prose (do not cite a page that
  doesn't exist). Agents' own `references.json` `in_corpus` flags are frequently stale in both
  directions — cross-check against the real `wiki/papers/` directory, not the flag.
- **Duplicate / row count.** Confirm exactly one row for the paper ID in `papers/index.md`.
- **Metadata status.** Confirm `status: ingested` and `ingested_date` are actually set in
  `raw/metadata/{id}.json`.
- **Bare wikilinks.** Fix every `wikilink_format` warning the health check reports — pipe to
  `[[id|Display Name]]`, don't just suppress the warning. The `wikilink_format` check's ID regex
  was fixed 2026-07-17/18 to also catch ACL-Anthology-style dotted IDs (`YYYY.venue-track.number`
  e.g. `2025.acl-long.313`) — previously these silently passed even in the exact same bad
  `[[id]] (Name)` pattern the check exists to catch. See [[feedback_health_check_dotted_id_gap]].
  Since the fix is now live in `scripts/checks/ingest.py`, the health check should catch these
  going forward, but it's still worth a manual eyeball on any page with dotted-ID citations.
- **Canonical paper IDs.** Some papers have a canonical wiki ID that differs from their arXiv ID
  (e.g. F5-TTS is `2025.acl-long.313`, not the arXiv `2410.06885`) because the conference/proceedings
  ID took precedence at ingest time. Verify any citation's ID against `wiki/papers/index.md`
  before linking — don't assume the arXiv ID is right just because that's what the source paper's
  own bibliography uses. See [[feedback_f5tts_paper_id]] for the canonical example.

### Tagging rules to apply during ingest (not just structural QC)

These are judgment calls the ingest agent makes per paper — verify independently, don't just
trust the agent's own reasoning in its closing summary:

- **VC task tag** — requires a dedicated VC system + genuine VC-specific metrics (zero metrics of
  any kind fails the bar, even if the system nominally supports voice conversion/editing). See
  [[feedback_vc_task_tagging]].
- **`spoken-language-model` concept tag** — requires an EXTERNAL speech signal consumed by an
  adapted LLM in a real spoken-dialogue context. An autoregressive TTS-LM consuming only its own
  generated output does NOT qualify. See [[feedback_spoken_language_model_tagging]].
- **`multilingual-tts` concept tag** — legitimate if the paper's OWN system was trained/adapted
  across languages, even without full per-language metrics; spurious if it only cites an upstream
  model's claimed multilingual capability. See [[feedback_multilingual_tts_tagging]].
- **`subjective-evaluation` concept tag** — requires real human raters (MOS/listening test);
  LLM-judge/automated scoring never qualifies. See [[feedback_subjective_evaluation_tagging]].
- **Task/`related_concepts` consistency** — a task tag (e.g. `singing`) is frequently omitted from
  `related_concepts` even when explicitly warned; verify independently every ingest. See
  [[feedback_task_related_concepts_mismatch]].
- **YAML date/ID coercion** — unquoted dates parse as YAML date objects, and unquoted numeric-
  looking IDs (e.g. `1412.6980`) parse as floats, dropping trailing zeros. Quote all date fields
  and the `id` field as strings. See [[feedback_yaml_coercion_gotchas]].

### Corpus-scope precedent chain (when a paper's generative-speech connection is unclear)

The test is **subject-matter relevance to TTS/VC/SCA** (including data/tooling/methodology work
squarely in service of speech generation), not literally "does the paper train a model." Read the
actual paper before deciding — task tags and relevance scores are not reliable signals on their
own. See [[feedback_corpus_scope_asr_false_accept]] for the full precedent chain, summarized:

- **Reject** — FAMA, MLC-SLM challenge summary: pure ASR/speech-translation/diarization papers
  whose only connection to "generative" is surface-level terminology ("speech LLM") in the title.
- **Accept** — 2506.04077 (TTS-as-data-augmentation): TTS is not the primary contribution, but the
  paper genuinely and methodologically engages with a TTS system (real claims about its behavior).
- **Accept (scope exception)** — 2510.03111 (TTS preprocessing pipelines): no TTS model trained or
  evaluated, but the paper's entire subject matter IS TTS data curation — it's a different axis
  from FAMA/MLC-SLM entirely, not an exception to that rule.
- **Accept (precedent reapplied)** — AURA, then VoiceAgentBench (2510.07978): agentic tool-use
  benchmarks where TTS/VC is incidental to the voice interface and never evaluated as output.
  Accepted for consistency once the shape was already decided once — when a new paper matches an
  already-decided precedent this closely, surface the match explicitly rather than re-deciding
  the underlying scope question fresh each time.

### arXiv full-version / extended-paper dedup

Some papers get a later arXiv "full version" under a completely different, unrelated-looking ID
(e.g. `2501.15907` was the full version of the already-ingested `2407.05361` Emilia paper). Check
`arxiv_comment` for "full version of X" / "extended version" / "journal version" language whenever
a candidate's arXiv ID prefix doesn't match its `published_date` — this is a stronger and cheaper
signal than assuming it's just the routine chronological-ordering gotcha below. If found and the
referenced ID is already ingested, surface it to the user rather than deciding unilaterally; the
resolution isn't always the same (compare to the plain French/English duplicate case, which was a
straightforward reject-the-non-canonical-version). See [[feedback_arxiv_full_version_dedup]] for
the full resolution procedure (keep canonical ID, re-ingest its content from the fuller paper,
backfill `source_ids`, add an editorial note on the page, log as `misc` not `ingest`).

Also check the INGEST_RESULT signal for `review_flags`; if present, add the paper to the
**Manual Verification Queue** below and resolve by hand after the batch — don't block the next
paper on it (see [[project_review_flags]] for the precision-gate rule agents apply before
flagging). Note: agents sometimes omit the `INGEST_RESULT` signal entirely, especially on a retry
after an interruption — this is not itself an error, just verify the files directly. Also don't
trust an agent's closing summary in general — it sometimes narrates a correct decision while the
actual file contradicts it; always re-read the real file (see [[feedback_agent_selfreport_unreliable]]).

### arXiv ID prefix vs. published date

Some papers carry a misleading arXiv ID prefix (e.g. a `2510.xxxxx` ID for a paper actually
published in September). Always trust `published_date` in `raw/metadata/{id}.json` for
chronological ordering and quarter assignment, not the ID prefix.

### Interruption recovery (session limits, API errors)

If an agent is cut off mid-ingest (session limit, API 5xx, etc.), before retrying: check the
**standalone content repo** (never `infra/wiki/` — that's a submodule pointer and can be stale,
giving a false "nothing written" signal) for whether the page file, index row, or metadata
status actually got written. A clean "nothing written" state is safe to retry directly. A
partial-write state (e.g. a stray copied figure asset with no page yet) needs the retry to
verify and reuse or discard what's there rather than assuming either way. See
[[feedback_session_limit_interruption]] for the full two-case recovery pattern.

Two other long-standing corpus-wide QC bugs to keep verifying manually even though they didn't
recur in session 14: `wiki/index.md`/venue-page count fabrication
(see [[feedback_index_count_drift]]) and mid-string title truncation in `papers/index.md` rows
(see [[feedback_title_truncation]]) — both are "not fixable by prompting," budget for a manual
check on every paper regardless of whether this session's batches stayed clean.

### Known open vocabulary gap

No canonical vocabulary term currently covers non-text-input speech generation (brain-signal
decoding, lip-to-speech, audio-continuation-only systems). Several Q3 papers were tagged `TTS`
as the closest fit pending a user decision on whether to add a dedicated term. If this recurs in
Q4, tag `TTS` as the same fallback and flag it in the Manual Verification Queue rather than
inventing a new term unilaterally.

---

## Session Log

**Session 2026-07-17, session 14 (batch 1 of 4 done):** Pre-selected 16 papers chronologically starting from the first remaining Q4 2025 paper. Before starting, caught a duplicate pair while building the candidate list: `2510.03735` (English, arXiv) and `2510.03741` (French, GRETSI 2025) are the same "Soft Disentanglement in Frequency Bands for Neural Audio Codecs" paper by the same four authors — user confirmed keep English, reject French; `2510.03741` set to `status: rejected`, `is_duplicate: true`, `canonical_id: 2510.03735`, logged to `raw/pipeline_log.md`. Q4 remaining count dropped from 159 to 158 as a result.

Batch 1 (`2510.00499` MOSS-Speech, `2510.00743` MOS-RMBench, `2025.vlsp-1.15` Twinkle-VC, `2025.vlsp-1.14` ViettelRoar) all ingested cleanly, 0 rejected. Corpus 592 → 596 pages, 0 errors, 1178 pre-existing warnings unchanged. Notable QC catches: (1) `2510.00743`'s first draft had unquoted `published_date`/`ingested_date`/`generation.date` — the exact YAML date-coercion bug the corpus has hit before — caught and quoted before it could reach a re-parse; (2) bare wikilinks hit 3 of 4 papers (Moss-Speech 8 links, MOS-RMBench 5, Twinkle-VC 4), all verified against real wiki pages before piping to `[[id|Name]]`; (3) `2025.vlsp-1.14` correctly used the canonical F5-TTS ID (`2025.acl-long.313`) rather than its arXiv ID, unprompted. The three VLSP 2025 shared-task companion papers (2 ingested this batch, 1 overview paper queued for batch 2) were each ingested independently with no fabricated cross-links — confirmed clean by inspection. `wiki/index.md`'s 4 count occurrences were updated directly from actual `ls`/grep counts during the batch cleanup pass (verified 596 pages = 596 index rows before editing), so no drift was possible this batch — workers never touched index.md themselves, per Mitigation B. Q4 progress: 31 ingested / 154 remaining. Nothing committed yet this session.

**Session 2026-07-17, session 14 (batch 2 of 4 done):** Batch 2 (`2025.vlsp-1.13` VLSP task overview, `2510.05150` Chronological Thinking Full-Duplex, `2510.02066` CoT Streaming Full-Duplex, `2510.01722` Emotional TTS/MINE disentanglement) all ingested cleanly, 0 rejected. Corpus 596 → 600 pages, 0 errors, 1178 pre-existing warnings unchanged. Notable QC catches: (1) `2510.02066` was missing a `§N.N` section citation on its 5th claim (had only bare table refs) — a genuine health-check error, not just a warning, fixed by adding `§VII`; (2) confirmed `2510.05150` and `2510.02066` are independent contemporaneous papers on the same topic (chain-of-thought reasoning in full-duplex spoken dialogue) rather than duplicates — different author teams (NTU/StepFun/Mila vs. CMU/Sony), different mechanisms; (3) new health-check gap found: the bare-wikilink `wikilink_format` check does not flag dotted non-arXiv IDs (`2025.vlsp-1.15`, `2025.acl-long.313`, `2025.acl-short.81`) even when they appear in the exact same bad `[[id]] (Name)` pattern it does catch for numeric arXiv IDs — caught by manual inspection on `2025.vlsp-1.13`, all 7 links on that page fixed regardless of whether the health check flagged them. The `spoken-language-model` external-signal rule was applied correctly on both full-duplex dialogue papers (genuine external speech consumed in real dialogue context, tag included). Q4 progress: 35 ingested / 150 remaining. Nothing committed yet this session.

**Session 2026-07-17, health-check tooling fix (between batch 2 and batch 3):** Fixed the dotted-ID gap found during batch 2 by adding a third alternative to `_PAPER_ID_RE` in `scripts/checks/ingest.py`: `^\d{4}\.[a-z][a-z0-9-]*\.\d+$`, covering the ACL Anthology `YYYY.venue-track.number` ID shape. Verified against every dotted ID actually present in `papers/index.md` before committing to the pattern. Re-running the corpus-wide health check with the fix surfaced 20 previously-invisible bare wikilinks across 12 already-ingested pages (all warnings, not errors) — this bug had been silently missing bare wikilinks on ACL/NAACL/EMNLP/Findings/workshop papers since the check was introduced, not just this session's VLSP papers. All 20 fixed by hand the same session, piping in display names derived from each target's title/abstract (reusing existing conventions like "F5-TTS" and "SpeechLM survey" where already established elsewhere). Fixing those lines also cleaned up 6 adjacent bare numeric-ID wikilinks incidentally. Corpus-wide health check after cleanup: 0 errors, 600 papers, 1172 warnings (down from the 1178 pre-fix baseline). See [[feedback_health_check_dotted_id_gap]] (memory) for the full regex diff and affected-paper list. This code fix and the 12 content fixes are uncommitted along with the rest of this session's ingest work.

**Session 2026-07-17, session 14 (batch 3 of 4 done):** Batch 3 (`2510.01903` MelTok, `2510.02044` Stream RAG, `2510.03111` TTS preprocessing pipelines, `2510.03735` Soft Disentanglement in Frequency Bands) all ingested cleanly, 0 rejected, 0 bare wikilinks across the whole batch (first fully clean batch on that front). Corpus 600 → 604 pages, 0 errors, 1172 warnings unchanged. One genuine corpus-scope borderline case: `2510.03111` trains/evaluates no TTS model at all (its own stated contributions are a preprocessing-pipeline evaluation methodology, a low-cost pipeline, and a new raw audio corpus; authors explicitly defer TTS training to future work, §5). Initially flagged using the FAMA/MLC-SLM playbook, but on review that framing was wrong: FAMA and MLC-SLM are fundamentally ASR/speech-translation/diarization papers with no real TTS/VC/SCA connection beyond generative-sounding terminology, whereas this paper's entire subject matter is TTS data curation — it just isn't a modeling paper. Reverted to `status: review`, filed to `review_queue.md`, user confirmed **accept** — not as an exception to the FAMA precedent, but because the paper was never actually FAMA-shaped to begin with (subject-matter relevance to TTS, not "is a model trained," is the right scope test). Ingested with an honest methodology-paper framing: empty `architecture`/`conditioning`/`training`, metrics limited to the paper's actual signal-quality numbers (PESQ), no fabricated TTS results. `2510.03735` is the English canonical paper for the French duplicate (`2510.03741`) rejected earlier this session. Q4 progress: 39 ingested / 146 remaining. Nothing committed yet this session.

**Session 2026-07-17, session 14 (batch 4 of 4 done — 16-paper pre-selected list COMPLETE):** Batch 4 (`2510.04738` Speak/Edit/Repeat (MAVE), `2510.05619` Articulatory Control TTS, `2510.05984` ECTSpeech, `2510.05799` Token-level Preference Optimization (TKTO)) all ingested cleanly, 0 rejected. Corpus 604 → 608 pages, 0 errors, 1172 warnings unchanged. QC catches: (1) `2510.04738`'s metadata tagged both `TTS` and `VC`, but the paper's "voice editing" is text-based masked-span speech editing (not speaker-identity conversion) with zero VC-specific metrics — task narrowed to `[TTS]` only per the VC tagging rule; (2) `2510.05799` had 1 bare wikilink (`2025.acl-long.598`, INTP), fixed. All other papers in the batch were fully clean on first health check. This completes the first 16-paper pre-selected Q4 chronological batch (4 batches of 4) started this session. Q4 progress: 43 ingested / 142 remaining. Nothing committed yet this session.

**Session 2026-07-18 (session 14 continued), extra 4-paper batch:** Pre-selected the next 4 papers chronologically (`2506.15556` PredGen, `2510.07096` Modeling Sarcastic Speech, `2510.06917` SHANKS, `2510.06927` Position: Towards Responsible Evaluation for TTS). Before ingesting, caught a real dedup case while building the candidate list: `2501.15907` ("Emilia: A Large-Scale, Extensive, Multilingual, and Diverse Dataset for Speech Generation") is the arXiv "full version" of the already-ingested `2407.05361` (Emilia, SLT 2024) — same authors, its own `arxiv_comment` says so explicitly, expanding the dataset from 101k to 216k hours ("Emilia-Large") with added scaling-law and multilingual/crosslingual experiments. User decision: keep `2407.05361` canonical (the SLT-published version, already cited by 65+ in-corpus papers), but rewrite its page content to reflect the fuller 2501.15907 paper, with both IDs explicitly linked/clarified on the page. `2501.15907` set to `status: rejected, is_duplicate: true, canonical_id: 2407.05361`; `2407.05361`'s `source_ids` backfilled with `arxiv_full_version: 2501.15907`; page re-ingested with updated dataset scale, new scaling-law/multilingual claims, an explicit editorial note distinguishing the two source papers, and (incidentally) brought up to current template standards — quoted dates, current bold-role-prefix Claims format, bulleted piped Wiki Connections — fixing legacy formatting the original 2026-06-12 ingest had never carried forward. Logged as a `misc` entry in `wiki/log.md` (not `ingest`, since the ID/page already existed) and a `review` entry in `raw/pipeline_log.md`.

Also caught during candidate selection: `2506.15556` has an arXiv ID prefix (June 2025) that doesn't match its actual `published_date` (2025-10-08) — the same ID-prefix-vs-published-date mismatch pattern as Emilia, but in this case NOT a duplicate (checked directly: no "full version of" comment, no existing wiki page match) — just the known chronological-ordering gotcha, handled per the existing rule (trust `published_date`).

All 4 new papers ingested cleanly, 0 rejected. Corpus 608 → 612 pages, 0 errors, 1170 warnings (down slightly from 1172 due to the Emilia legacy-format cleanup). One bare wikilink caught on the Emilia re-ingest itself (6 links, `[[id]] (Name)` pattern recurring even in a careful rewrite) — fixed. Q4 progress: 47 ingested / 137 remaining. Nothing committed yet this session.

**Session 2026-07-18 (session 14 continued), fourth 4-paper batch:** Pre-selected the next 4 papers chronologically (`2510.07881` CS3-Bench, `2510.08373` DialoSpeech, `2510.08392` MeanVC, `2510.07978` VoiceAgentBench). Two genuine corpus-scope checks this batch, both resolved as accept: (1) `2510.07881` (relevance_score 0.60, borderline) — confirmed on full read that it genuinely evaluates and enhances actual speech-to-speech generation output (pronunciation success rate, WER on synthesized code-switched audio, decoder-level Keyword Highlighting conditioning), not just text understanding, so it passes the scope bar cleanly; (2) `2510.07978` (VoiceAgentBench) — a harder case: all four of its evaluation metrics (Tool Selection, Tool Call Structure, Parameter Filling, Refusal Rate) score text/structured tool-call correctness with zero evaluation of generated speech quality anywhere, TTS/VC used only to construct benchmark input audio. Structurally identical to the already-accepted AURA entry in `review_queue.md`. Reverted to review conceptually (flagged, not written) pending user decision; user confirmed **accept**, explicitly for consistency with the AURA precedent, and it was ingested with an honest evaluation-benchmark framing (empty `metrics`, no fabricated speech-quality claims, architecture fields describing the systems under test rather than a proposed model). Both scope decisions and the AURA-precedent reasoning were logged to `review_queue.md` and `raw/pipeline_log.md`. QC: `2510.08373` had 2 bare wikilinks (VALL-E, CosyVoice), fixed; `2510.08373` and `2510.07881` both correctly used canonical wiki IDs (F5-TTS as `2025.acl-long.313`) rather than arXiv IDs, unprompted. Corpus 612 → 616 pages, 0 errors, 1170 warnings unchanged. Q4 progress: 51 ingested / 133 remaining.

**Session 2026-07-17 to 2026-07-18, session 14 close (committed and pushed):** All 6 batches (24 papers total: 27 → 51 ingested, 159 → 133 remaining) committed and pushed. Content repo (`daf328f`): 24 new paper pages + assets, Emilia (2407.05361) re-ingested with expanded content, 12 pages' bare wikilinks fixed, `index.md`/`log.md`/`papers/index.md` updated. Infra repo: metadata status updates for all 24 ingested papers plus the 2 rejected duplicates (2510.03741, 2501.15907) and 2 scope-exception accepts (2510.03111, 2510.07978), the `scripts/checks/ingest.py` dotted-ID regex fix, `raw/pipeline_log.md` and `raw/review_queue.md` entries, and this session log. Corpus at 616 pages, 0 errors corpus-wide. Stray `flow-matching-render-v2-test-2026-06-26.md` file at the infra root again left untouched (still flagged, still unresolved). Next session: continue Q4 2025 chronologically from the next remaining paper after `2510.08392` (re-select the candidate list at session start) — 133 papers remaining.

**Session 2026-07-18, session 15, batch 1 of 8 (32-paper pre-selected list):** Batch 1 (`2510.09061` O_O-VC, `2510.09016` DiTSinger, `2506.12311` Phonikud, `2510.09424` DST/SCA) all ingested, 0 rejected. Corpus 616 → 620 pages, 0 errors. QC caught and fixed on manual verification (not by the ingest agent itself): stale `index.md` paper-count callouts twice (611→617, then 612→618 after the second paper — the ingest agents' own self-reported counts were both wrong even though `papers/index.md` itself was correct), a missing Org column on `2510.09061`'s index row, and a mid-word title truncation on `2510.09016`'s index row ("...Diffusi" → full title). One genuine corpus-scope case: `2510.09424` ("...A Truly Fully End-to-End Spoken Dialog State Tracking Approach") was pre-selected as SCA but is actually a Spoken Dialog State Tracking paper — JSON slot-value output, Joint Goal Accuracy metric, zero speech generation anywhere — a clean structural match to the FAMA/MLC-SLM reject pattern. Flagged to the user before writing anything; user explicitly overrode and accepted it anyway, as a one-off decision (not a new precedent). Ingested with an honest DST framing: explicit scope note under the abstract callout, real DST metrics only (no fabricated speech-quality numbers), `spoken-language-model` tag verified against the external-signal rule. Logged to `raw/review_queue.md` and `raw/pipeline_log.md`, and opened a new P2 backlog item, "Corpus Scope Extension: Spoken Dialog Understanding," for the user's longer-term interest in eventually widening the controlled vocabulary to cover spoken-dialog-understanding tasks (DST, turn-taking, intent tracking) on their own terms rather than via override. Q4 progress: 55 ingested / 129 remaining.

**Session 2026-07-18, session 15, batch 2 of 8:** Batch 2 (`2510.09592` Mind-Paced Speaking, `2510.09245` SynthVC, `2510.10003` MTP-S2UT, `2510.10774` ParsVoice) all ingested cleanly, 0 rejected, 0 fixes needed on any of the four (first fully clean batch this session). Corpus 620 → 624 pages, 0 errors, 1170 warnings unchanged. Two corpus-scope checks this batch, both genuine accepts on read: (1) `2510.09592` confirmed as a real spoken-dialogue architecture (dual-brain: Formulation Brain + Articulation Brain) that consumes external speech input and generates actual spoken output via streaming TTS, evaluated on speech-to-speech conversation (URO-Bench) — not an understanding paper; (2) `2510.10003` (MTP-S2UT) confirmed as genuine speech-to-speech translation with real unit-to-speech resynthesis, not text-only translation. Notable judgment call: `2510.10003` was pre-selected as `TTS, SCA` but the ingest agent tagged `TTS` only, citing clean in-corpus precedent (SeamlessM4T, Seed LiveInterpret 2.0 — both pure S2ST systems tagged TTS-only, never SCA); verified as a reasonable, well-precedented call. `2510.10774` (ParsVoice) correctly treated as a data-curation/fine-tuning-validation paper rather than a novel-architecture paper (XTTS fine-tuned for validation, no architectural-novelty figure), and correctly resolved ManaTTS's canonical wiki ID (`2025.naacl-long.464`, not its arXiv ID `2409.07259`) unprompted. Q4 progress: 59 ingested / 125 remaining.

**Session limit hit and resumed, between batch 2 and batch 3:** Session was interrupted after batch 2's log entry was written but before batch 3 started. On resume, checked both the standalone content repo and infra repo directly per the interruption-recovery protocol — found a clean state, exactly the 8 papers from batches 1–2 present in both repos with no partial writes or orphaned assets, matching what was logged. Re-ran the progress-count script (59 ingested / 125 remaining, confirmed) and a corpus-wide health check (624 pages, 0 errors) before resuming. Nothing needed manual completion; proceeded directly to batch 3.

**Session 2026-07-18, session 15, batch 3 of 8 (3 of 4 pre-selected papers ingested, 1 skipped):** `2510.11646` (BridgeCode), `2510.11124` (Perturbation SSL / EMM-TTS), and `2510.12964` (VCTR) all ingested cleanly, 0 rejected, 0 fixes needed. Notable judgment calls: `2510.11124`'s architecture/codec fields were corrected mid-ingest after the agent viewed the paper's own figure and found an XLSR self-supervised pipeline (not a neural codec) feeding a HiFi-GAN generator; `multilingual-tts` tag verified genuine (own-system Chinese/English cross-lingual evaluation with per-language metrics, not just a title claim). `2510.12964` correctly treated as `field_significance.type: engineering-integration` (architecture adapted from a prior vision-transformer paper, ITTR) with no figure copied, per the no-architectural-novelty rule.

The fourth pre-selected paper, `2510.12116` ("Understanding the Modality Gap..."), was flagged before writing anything: the LSLM under study only ever outputs text (§3.1), and every benchmark (VoiceBench: AdvBench, IFEval, OBQA, MMSU, sd-qa) scores text-QA accuracy — no TTS/VC/spoken-output component anywhere in the paper. This is a cleaner FAMA/MLC-SLM match than `2510.09424` was (no dialogue-state or any spoken-output artifact at all, vs. DST's structured JSON within a spoken-dialogue pipeline). User chose to leave `status: accepted` unchanged and skip it for now rather than deciding immediately — not part of the DST scope-expansion backlog interest in the same way `2510.09424` is, since there's no dialogue-management output here either. Logged to `raw/review_queue.md` (undecided, pending a later explicit call) and `raw/pipeline_log.md`. Corpus 624 → 627 pages (3 papers, not 4), 0 errors, 1170 warnings unchanged. Q4 progress: 62 ingested / 122 remaining (63 rejected). `2510.12116` remains `status: accepted` and is included in that 122 — skip it again when re-selecting the next chronological batch rather than re-ingesting on autopilot, since the scope decision is still pending in `review_queue.md`.

**Session 2026-07-18, session 15, batch 4 of 8:** `2510.12995` (Continuous-Token Diffusion for Speaker-Referenced TTS), `2510.13221` (Acoustic Teleportation codec), `2510.13293` (Cross-Modal Consistency Guidance for emotion control), `2510.13194` (StressTransfer) all ingested, 0 rejected. Corpus 627 → 631 pages, 0 errors, 1170 warnings unchanged. Two spurious concept tags caught and fixed on manual verification (not by the ingest agents themselves): (1) `2510.12995` was tagged `spoken-language-model` despite being a pure TTS-in-MLLM paper whose only conditioning signal is a static 3-second speaker-reference embedding, not a genuine external speech signal consumed in a spoken-dialogue context — exactly the KALL-E/FELLE/DiTAR non-qualifying pattern the tagging rule already excludes; removed from `related_concepts` and Wiki Connections. (2) `2510.13221` was tagged `speech-to-speech` despite being a codec-level room-acoustics/reverb transplantation paper ("acoustic teleportation") with no dialogue or translation component — checked `wiki/concepts/speech-to-speech.md`'s own defined scope (three sub-paradigms: end-to-end spoken dialogue, direct S2S translation, cascade S2S) and confirmed this paper fits none of them; removed. By contrast, `2510.13194` (StressTransfer)'s `speech-to-speech` tag was verified genuine — an explicit cascaded S2TT+TTS pipeline, matching the concept's "Cascade S2S" sub-paradigm exactly. Given the pattern of two spurious tags in the same batch, the third and fourth ingest agents were briefed explicitly on both cases before running, and both came back clean on this front. Q4 progress: 66 ingested / 118 remaining.

**Session 2026-07-18, session 15, batch 5 of 8 (all four codec papers):** `2510.15364` (LDCodec), `2510.15227` (LongCat-Audio-Codec), `2510.16841` (SAC), `2510.16718` (U-Codec) all ingested, 0 rejected. Corpus 631 → 635 pages, 0 errors, 1170 warnings unchanged.

Session-limit interruption occurred mid-write on the first paper (`2510.15364`): the agent was cut off right after starting to write the page, leaving a stray `papers/assets/2510.15364/figure-1.png` with no corresponding page, no index/log/metadata changes anywhere. Confirmed clean per the interruption-recovery protocol (no partial page, no index rows, `raw/metadata` status still `accepted`), discarded the stray asset, and retried from scratch — the retry ingested cleanly with no artifacts from the failed attempt.

New citation-integrity issue caught this batch (not previously seen): `2510.15227` (LongCat-Audio-Codec, a codec paper with an unusually large 18-entry in-corpus reference list) had its `related_papers` frontmatter populated with all 18 IDs the reference-index tool detected as in-corpus, but only 8 were actually cited/linked in the page's prose or Wiki Connections — the other 10 were real in-corpus pages, just never discussed on this particular page. Trimmed `related_papers` to the 8 actually-cited IDs to match established convention (frontmatter should mirror what's genuinely referenced in-page, not the source paper's full in-corpus bibliography overlap). The next two ingest agents in the batch were explicitly briefed on this exact failure mode and both came back with `related_papers` already matching their wikilinks exactly, no fix needed.

Also verified `2510.16718` (U-Codec)'s broadened `task: [codec, TTS]` tag (raw metadata had `codec` only) — genuine, the paper includes a full dedicated zero-shot TTS system with real MOS/SMOS listening tests and SIM/WER benchmarks (§4.2.2, Tables 4–6), not just a codec-reconstruction evaluation. Q4 progress: 70 ingested / 114 remaining.

**Session 2026-07-18, session 15, batch 6 of 8:** `2503.06211` (Late Fusion and Multi-Level Fission), `2510.18308` (ParaStyleTTS), `2506.23670` (Efficient Interleaved Speech Modeling / TinyWave), `2510.19509` (Which Evaluation for Which Model? evaluation taxonomy, survey) all ingested, 0 rejected. Corpus 635 → 639 pages, 0 errors, 1170 warnings unchanged.

`2506.23670` had been sitting as an uningested companion citation (`status: accepted`, no page) since it was first referenced by another paper in an earlier session; confirmed it was still genuinely accepted and un-ingested before proceeding, per the pre-selected chronological list. Double-checked its `spoken-language-model`/`speech-to-speech` concept tags carefully given the two false-positive tags caught in batch 4 — this one held up: TinyWave is a direct distillation of SpiritLM (`2402.05755`, itself already tagged `spoken-language-model`/`speech-to-speech`), consuming real external speech prompts from Libri-Light and continuing them autoregressively in the same interleaved-speech-text token space, matching the concept's own explicitly-scoped "Interleaved speech-text LMs" category rather than the KALL-E/DiTAR-style non-qualifying pattern.

`2510.19509` correctly identified and handled as a survey/taxonomy paper (`## Scope and Coverage` section, `tags: ["survey"]`) with no original model or experiments; citation integrity held clean (only 1 of 4 detected in-corpus refs actually has a wiki page, and only that one was cited/included in `related_papers`). One agent self-report note this batch: the ingest agent's completion message flagged that its own safety classifier was unavailable during review and asked for extra verification — ran the full independent QC pass as usual (page/index/count/citation/health-check) and everything checked out clean regardless. Q4 progress: 74 ingested / 110 remaining.

---

## Manual Verification Queue

Papers where the ingest agent emitted `review_flags` in its INGEST_RESULT signal. Review these
after the session batch is complete — check the paper page and resolve each flag by hand.

| Paper ID | Flag | Agent note |
|----------|------|------------|

---

## Progress

Track with the same script as in the Scope section above (repeated here for convenience):

```bash
.venv/bin/python3 -c "
import json, glob
accepted, ingested, rejected = 0, 0, 0
for path in glob.glob('raw/metadata/*.json'):
    m = json.load(open(path))
    y, mo = str(m.get('year','')), str(m.get('month','0')).zfill(2)
    if y == '2025' and mo in ('10','11','12'):
        if m['status'] == 'accepted': accepted += 1
        if m['status'] == 'ingested': ingested += 1
        if m['status'] == 'rejected': rejected += 1
print(f'Ingested: {ingested} | Remaining: {accepted} | Rejected: {rejected}')
"
```

## Commit / Push Workflow

Not every batch needs a commit — batch within a session freely, commit at natural stopping
points or when explicitly asked. When committing:

1. Content repo: stage new paper pages + assets + `index.md`/`log.md`/`papers/index.md`, commit, push.
2. Infra repo: stage `raw/metadata/*.json` status updates + this session log (and `BACKLOG.md` if
   its Q4 progress line has gone stale), commit; then bump the `wiki/` submodule pointer to the
   new content commit (checkout `main` in `wiki/`, `git pull`, commit the pointer bump in infra), push.
3. Site repo: bump the `content` submodule pointer, commit, push — **ask before this step**
   (though a durable standing instruction to always bump satisfies this too — check for one
   before asking), it triggers a live deploy. Push order is always content → infra → site, since
   site's submodule reference only resolves once content is on GitHub.

Always edit and commit from the **standalone content repo**
(`/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content`), never
via `infra/wiki/` or `site/content/` submodule paths directly — both are detached-HEAD checkouts
of specific commits, and committing there orphans the work. See [[project_repo_structure]] for
the three-repo layout and [[feedback_site_submodule_bump]] for the submodule-bump specifics
(use `git branch` not `git submodule status` to verify branch state). Commit messages: no
`Co-Authored-By` trailers, no session-number prefix — describe what changed, not when (see
[[feedback_commit_messages]]). Wiki prose: avoid em dashes, use comma/colon/parentheses instead
(see [[feedback_em_dashes]]).
