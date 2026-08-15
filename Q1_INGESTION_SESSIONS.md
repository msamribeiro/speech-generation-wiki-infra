# Q1 2026 Ingest Session

**Date:** 2026-08-02
**Goal:** Ingest all accepted Q1 2026 (January–March 2026) papers into the wiki.

Bootstrapped from `docs/records/2026-08-02-q4-2025-ingestion-sessions.md`, which holds the full
paper-by-paper Q4 2025 log (8 sessions, 180 papers, complete). This file carries forward the
ingestion protocol and cadence preferences refined during Q3/Q4, without the historical narrative.

---

## Scope

| Status | Count |
|--------|-------|
| Already ingested (Q1 2026) | 7 |
| Remaining to ingest | 159 |
| Rejected | 58 |
| **Total Q1 2026 in corpus** | **224** |

As of 2026-08-02 (bootstrap, session not yet started). Fetch and filter are fully complete for
this quarter. Counts computed from `raw/metadata/*.json` where `year == 2026` and
`month in (1, 2, 3)` (these fields are derived from `published_date`, not the arXiv ID prefix —
see the ID-prefix note below). Re-run before starting a session, as fetch/filter may still be
adding papers:

```bash
.venv/bin/python3 -c "
import json, glob
accepted, ingested, rejected = 0, 0, 0
for path in glob.glob('raw/metadata/*.json'):
    m = json.load(open(path))
    y, mo = str(m.get('year','')), str(m.get('month','0')).zfill(2)
    if y == '2026' and mo in ('01','02','03'):
        if m['status'] == 'accepted': accepted += 1
        if m['status'] == 'ingested': ingested += 1
        if m['status'] == 'rejected': rejected += 1
print(f'Ingested: {ingested} | Remaining: {accepted} | Rejected: {rejected}')
"
```

---

## Next Session — Resume Here

2026-08-15 was a three-part day: two full 12-paper sessions plus a 2-paper mini-batch appended to
close out the day, totalling **26 papers ingested**. Q1 2026 progress at end of day: 126 ingested,
36 remaining, 62 rejected (224 total in scope, unchanged — no new fetch/filter activity all day).
Corpus 838 → 864 pages, 0 errors / 1171 warnings (unchanged baseline all day) at final health check.

To start the next session: re-run the progress-count script first to confirm current counts, then
build a fresh chronological candidate list starting from the earliest remaining Q1 2026 `accepted`
paper by `published_date`. The last-ingested paper today was `2603.12342` (published_date
2026-03-12); as of day close the next four chronologically are `2603.12565` (Speech-Worthy Alignment
for Japanese SpeechLLMs via Direct Preference Optimization), `2603.13518` (VoXtream2: Full-stream
TTS with dynamic speaking rate control), `2603.14032` (Beyond Two-stage Diffusion TTS: Joint
Structure and Content Refinement via Jump Diffusion), `2603.14035` (Probing neural audio codecs for
distinctions among English nuclear tunes) — verify this list is still current before using it, since
more papers may have been fetched/filtered since.

**Cadence note:** all three parts of today used sequential batches of 4 (or smaller for the closing
mini-batch), no user-requested cadence changes. Default remains batches-of-4 unless told otherwise.

**One clean session-limit interruption in the second full session**, resolved without incident:
`2603.09627` (Speech-Omni-Lite) was cut off with nothing written (verified: no page/assets/
index/log/metadata changes, status still `accepted`) — safe direct retry from scratch, same as the
`2603.04145` precedent.

**One scope pre-check, no issue found**: `2603.16924` (SimulU) had an arXiv ID prefix (16xxx) that
looked out of sequence against neighboring papers' IDs (07xxx-11xxx) despite sharing similar
`published_date`s — checked and confirmed this is normal, since arXiv submission numbers are global
across all categories (~3,000/day) rather than per-category; not a duplicate/full-version case like
the Emilia precedent. Ingested normally.

**Index-count drift remains the dominant recurring issue, all day**: hit on the large majority of
all 26 papers ingested today — essentially every paper needed at least one of the 3
`wiki/index.md` occurrences corrected. Several instances had an ingest agent report a count value
that was flatly wrong by more than 1 (off by exactly 10, three separate times today). Independent
verification via `grep -c '^| \[\[' papers/index.md` against all 3 occurrences after *every single
paper* continues to be mandatory, not optional — this is no longer an occasional catch, it is the
expected steady state of the pipeline; worth considering a script-level fix if it keeps recurring at
this rate. Also caught once (`2603.16924`): an ingest agent's self-reported "0 warnings" that was
actually 5 bare-wikilink warnings — agent self-reports on warning counts, not just error counts or
index counts, need the same independent verification.

Zero `review_flags` entries emitted across all 26 ingested papers today. Manual Verification
Queue below is unchanged from the prior session (still just `2602.11172`, unresolved).

---

## Success Criteria

- All accepted Q1 2026 papers have `status: ingested` in `raw/metadata/`
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

Default (as run throughout Q3/Q4): pre-select the full remaining list chronologically up front,
then work through it in batches of 4. Within each batch:

1. One paper at a time — no parallel ingest workers.
2. Run the per-paper health check after each paper; fix bare wikilinks and any schema errors
   before moving to the next paper.
3. After all 4 papers in the batch are clean, write a short batch summary (paper IDs, notable
   QC catches, corpus page count, updated Q1 progress numbers) and append it to this file's
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
- **Title truncation.** Compare the title in the new `papers/index.md` row against the page's own
  `title:` frontmatter, in full. Agents intermittently cut titles off mid-word with no reliable
  pattern. Not fixable by prompting alone; budget for a manual check on every paper. See
  [[feedback_title_truncation]].
- **Metadata status.** Confirm `status: ingested` and `ingested_date` are actually set in
  `raw/metadata/{id}.json`.
- **Bare wikilinks.** Fix every `wikilink_format` warning the health check reports — pipe to
  `[[id|Display Name]]`, don't just suppress the warning. The check's ID regex covers
  ACL-Anthology-style dotted IDs (`YYYY.venue-track.number` e.g. `2025.acl-long.313`) as well as
  numeric arXiv IDs — still worth a manual eyeball on any page with dotted-ID citations.
- **Canonical paper IDs.** Some papers have a canonical wiki ID that differs from their arXiv ID
  (e.g. F5-TTS is `2025.acl-long.313`, not the arXiv `2410.06885`) because the conference/proceedings
  ID took precedence at ingest time. Verify any citation's ID against `wiki/papers/index.md`
  before linking — don't assume the arXiv ID is right just because that's what the source paper's
  own bibliography uses. See [[feedback_f5tts_paper_id]] for the canonical example.
- **Rejected-paper citations.** Before linking to any in-corpus reference, check its `status` —
  `accepted`-but-unwritten keeps the ID in `related_papers` frontmatter with prose de-linked;
  `rejected` removes it entirely (do not link or cite by ID at all, mention unlinked in prose if
  needed). This recurs even on papers the source paper discusses substantively in its own text.

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
- **Abstract callout.** The abstract card is ALWAYS `[!abstract]`, never the same callout type
  used in that page's own Field Significance section (`[!tip]` for high, `[!important]` for
  foundational). This recurred repeatedly across Q4 — any *elevated* `field_significance.level`
  appears to prime the mistake. Check this specifically before running the health check.

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
- **Accept (one-off override, not a precedent)** — 2510.09424 (Spoken Dialog State Tracking):
  zero TTS/VC/synthesized-speech output, structurally a FAMA/MLC-SLM match, but the user overrode
  explicitly as a one-off. A second same-shape paper (2511.22503) was evaluated fresh afterward
  and rejected — do not treat this override as license to wave through future DST papers.
- **Accept (new precedent shape — analysis-of-existing-speech)** — 2512.16832 (prosody/text
  information-theoretic analysis): no TTS/VC/SCA system built or evaluated, purely a linguistics
  analysis paper, but accepted as directly useful background for prosody-control/expressive-TTS
  research. A genuinely new shape distinct from 2510.03111 (tooling-for-building-speech) — this is
  analysis-of-existing-speech instead. Extended once more by 2512.21706 (full-duplex
  conversational-behavior-reasoning), which is closer to this shape than a genuine generation
  paper despite constructing a real audio training corpus and benchmarking real speech-generation
  systems. Each of these is judged and accepted fresh as its own case, not auto-approved — see
  [[future_dst_scope_expansion]] for the standing P2 backlog item to eventually widen the
  controlled vocabulary so these stop needing one-off calls.

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

Some papers carry a misleading arXiv ID prefix (e.g. a `2601.xxxxx` ID for a paper actually
published in December). Always trust `published_date` in `raw/metadata/{id}.json` for
chronological ordering and quarter assignment, not the ID prefix.

### Interruption recovery (session limits, API errors)

If an agent is cut off mid-ingest (session limit, API 5xx, etc.), before retrying: check the
**standalone content repo** (never `infra/wiki/` — that's a submodule pointer and can be stale,
giving a false "nothing written" signal) for whether the page file, index row, or metadata
status actually got written. A clean "nothing written" state is safe to retry directly. A
partial-write state (e.g. a stray copied figure asset with no page yet, or a page written but
index/log/metadata not yet updated) needs the retry to verify and complete or reuse what's there
rather than assuming either way. See [[feedback_session_limit_interruption]] for the full
two-case recovery pattern.

Two other long-standing corpus-wide QC bugs to keep verifying manually regardless of whether a
given session's batches stay clean: `wiki/index.md`/venue-page count fabrication (see
[[feedback_index_count_drift]]) and mid-string title truncation in `papers/index.md` rows (see
[[feedback_title_truncation]]) — both are "not fixable by prompting."

### Known open vocabulary gap

No canonical vocabulary term currently covers non-text-input speech generation (brain-signal
decoding, lip-to-speech, audio-continuation-only systems). Several Q3/Q4 papers were tagged `TTS`
as the closest fit pending a user decision on whether to add a dedicated term. If this recurs in
Q1 2026, tag `TTS` as the same fallback and flag it in the Manual Verification Queue rather than
inventing a new term unilaterally.

---

## Session Log

### 2026-08-03 — Batch 1 (papers 1-4 of 16 preselected)

Ingested sequentially, one at a time, with a health check after each:

- `2601.00217` — Mitigating Latent Mismatch in cVAE-Based Singing Voice Synthesis via Flow Matching (FM-Singer). Tagged `singing`; note that the ingest skill's embedded `related_concepts` allowed-slugs list is stale (missing `singing` and `fine-tuning`, both closed concepts as of 2026-08-02 per `wiki/_claims/` and `wiki/concepts/`) — used the actual tracked concept set instead of the skill's hardcoded list. Fixed a bare-wikilink health-check warning (WaveNet) before it passed clean. 1 figure embedded (architecture pipeline).
- `2601.00303` — DepFlow: Disentangled Speech Generation to Mitigate Semantic Bias in Depression Detection. Corpus-scope precedent match: TTS-as-methodologically-central-tool for a downstream task (same shape as the 2506.04077 precedent), accepted consistent with prior scope calls. No figure (empirical/engineering-integration contribution, no architectural-novelty type). Manual log.md section-insertion fix needed (today's `## 2026-08-03` section didn't exist yet; the skill's regex assumes a `---\n\n## ` separator pattern not present in the current file).
- `2601.01459` — OV-InstructTTS: Towards Open-Vocabulary Instruct Text-to-Speech. Caught and fixed a real mistake before it reached health check: used `[!tip]` instead of `[!abstract]` on the abstract callout, and omitted the required `[!tip]` wrapper on the Field Significance prose for this `high`-significance paper — both are exactly the callout-type-bleed failure mode the ingest template warns about. Health check initially failed (`required_sections`), fixed, re-ran clean. 1 figure embedded (model architecture).
- `2601.01568` — MM-Sonate: Multimodal Controllable Audio-Video Generation with Zero-Shot Voice Cloning. Confirmed F5-TTS canonical ID is `2025.acl-long.313`, not the `2410.06885` arXiv ID this paper's own bibliography cites (per the standing precedent, see `feedback_f5tts_paper_id`). 1 figure embedded (framework architecture).

QC notes: `wiki/index.md`'s paper-count template has drifted from what the ingest skill's regex expects (it now reads "N paper pages" / "Browse all N papers" in prose rather than the "papers ingested" / "Last updated" pattern the skill script matches), so all 3 occurrences needed a manual fix after every paper rather than being caught by the automated step — consistent with the standing "not fixable by prompting" status of this bug. `papers/index.md` row count and `wiki/papers/*.md` file count were verified to match after each paper (746, 747, 748, 749). No `review_flags` emitted by any of the 4 papers.

Corpus page count: 745 → 749. Q1 2026 progress: 7 → 11 ingested, 159 → 155 remaining (58 rejected, unchanged). Not yet committed/pushed.

### 2026-08-03 — Batch 2 (papers 5-8 of 16 preselected)

Ingested sequentially, one at a time, with a health check after each:

- `2601.04233` — LEMAS: A 150K-Hour Large-scale Extensible Multilingual Audio Suite with Generative Speech Models. Dataset paper (LEMAS-Dataset) validated by two benchmark models (LEMAS-TTS extending F5-TTS, LEMAS-Edit extending VoiceCraft). Fixed the same `[!tip]`-instead-of-`[!abstract]` callout mistake as below (see recurring-mistake note). No figure embedded (the one candidate architecture-style figure sits in the Introduction, not a Method/Model section, so it didn't satisfy the figure-selection criteria).
- `2601.02073` — Towards Prosodically Informed Mizo TTS without Explicit Tone Markings. First reported TTS system for Mizo (low-resource tonal language); genuinely useful methodological finding that DNSMOS and F0-based objective metrics fail to track large, significant differences in tone accuracy and human-rated naturalness. No figure (no architectural-novelty type).
- `2601.02753` — Vclip: Face-based Speaker Generation by Face-voice Association Learning. Zero in-corpus references found (small, disconnected niche literature); flagged an open vocabulary gap (no controlled `conditioning` term for face/image-conditioned generation — used `speaker-conditioned` + `zero-shot` as the closest fit rather than inventing a term). 1 figure embedded (method overview).
- `2601.02776` — UniSRCodec: Unified and Low-Bitrate Single Codebook Codec with Sub-Band Reconstruction. 1 figure embedded (architecture/training diagram).

**Recurring mistake this batch:** made the `[!tip]`-instead-of-`[!abstract]` callout error on 2 of the 4 papers this batch (`2601.04233`, `2601.02776`) — the same mistake caught and fixed once in Batch 1 (`2601.01459`) recurred twice more despite being flagged. Both were caught by the health check (`required_sections` error) before being marked complete, so nothing shipped broken, but this is clearly not a one-off; worth deliberately double-checking the abstract-callout line before running health check on every future paper rather than relying on the check to catch it after the fact.

QC notes: `wiki/index.md` count fix (3 occurrences) still needed manually on every paper, as expected. `papers/index.md` row count and `wiki/papers/*.md` file count verified to match after each paper (750, 751, 752, 753). No `review_flags` emitted by any of the 4 papers.

Corpus page count: 749 → 753. Q1 2026 progress: 11 → 15 ingested, 155 → 151 remaining (58 rejected, unchanged). Not yet committed/pushed.

### 2026-08-03 — Batch 3 (papers 9-12 of 16 preselected)

Ingested sequentially, one at a time, with a health check after each:

- `2601.03170` — TED-TTS: Training-Free Intra-Utterance Emotion and Duration Control. First training-free framework for intra-utterance multi-emotion/duration control on a frozen zero-shot TTS backbone (IndexTTS2-configured); genuinely useful Monotonic Stream Alignment mechanism for driving segment transitions from noisy attention maps. 1 figure embedded. Double-checked the abstract callout before health check per the note left at the end of Batch 2 — passed clean on the first attempt.
- `2601.03632` — ReStyle-TTS: Relative and Continuous Style Control for Zero-Shot Speech Synthesis. First controllable zero-shot TTS to support continuous, reference-relative (not absolute) style control; per-sample regression analysis (slopes ~1, intercepts ~0) is a genuinely rigorous test of the "relative" claim. Caught and fixed a venue-labeling mistake before it shipped: the paper's `arxiv_comment` says "ACL 2026," and I initially set `venue: ACL` / `venue_type: conference`, but a precedent check against an already-ingested paper with the identical situation (`2510.14664`) showed the corpus convention is to keep `venue: arXiv` until the paper has an actual ACL Anthology ID (i.e. until the conference has happened) — reverted to match. Also repeated the `[!tip]`-instead-of-`[!abstract]` callout mistake a **third** time this session despite the explicit note left after Batch 2; caught by health check, fixed. 1 figure embedded.
- `2601.03892` — Lightweight and perceptually-guided voice conversion for electro-laryngeal speech. Clinical-application VC paper (StreamVC adapted for post-laryngectomy speech rehabilitation); useful negative result that adding more than ~2 auxiliary perceptual/intelligibility losses degrades rather than improves a GAN-VC training objective. `arxiv_comment` also flagged "accepted for ICASSP 2026" — applied the same arXiv-venue precedent proactively this time, no fix needed. No figure (engineering-integration, no architectural-novelty type). Correct abstract callout on the first attempt (moderate significance, so no Field Significance callout to conflict with).
- `2601.05329` — CosyEdit: Unlocking End-to-End Speech Editing Capability from Zero-Shot TTS Models. 400M-parameter model fine-tuned on 250h outperforms 3B-16B-parameter end-to-end speech-editing baselines (Step-Audio-EditX, MiMo-Audio, Ming-UniAudio) on RealEdit. Repeated the `[!tip]` mistake a **fourth** time this session. 1 figure embedded.

**The `[!tip]`-instead-of-`[!abstract]` mistake recurred twice more this batch** (`2601.03632`, `2601.05329`), on top of the three prior occurrences from Batches 1-2 — five total across the session, always on `high`-significance papers, always caught by the health check before completion. Explicitly noting it in the session log has not been sufficient to prevent recurrence. Adopted a mechanical fix instead: run `grep -n "!tip\]\|!abstract\]\|!important\]"` against the drafted page before every health check, every paper, no exceptions — verified working for the remainder of this batch.

**New precedent applied:** arXiv-sourced papers whose `arxiv_comment` names a future conference acceptance (e.g. "ACL 2026", "accepted for ICASSP 2026") keep `venue: arXiv` / `venue_type: preprint` until the paper has an actual venue-specific ID (ACL Anthology dotted ID, etc.) — matches existing corpus precedent (`2510.14664`). Worth checking `arxiv_comment` for this pattern on every future paper before setting `venue`.

QC notes: `wiki/index.md` count fix (3 occurrences) needed manually on every paper, as expected. `papers/index.md` row count and `wiki/papers/*.md` file count verified to match after each paper (754, 755, 756, 757). No `review_flags` emitted by any of the 4 papers.

Corpus page count: 753 → 757. Q1 2026 progress: 15 → 19 ingested, 151 → 147 remaining (58 rejected, unchanged). Not yet committed/pushed.

### 2026-08-03 — Batch 4 (papers 13-16 of 16 preselected — list complete)

Ingested sequentially, one at a time, with a health check after each. Session was interrupted mid-write on the first paper of this batch (model temporarily unavailable); recovered cleanly per the standard interruption-recovery procedure (checked the standalone content repo directly — only a stray figure-asset directory existed for `2601.05554`, no page/index-row/log-entry/metadata-update, so it was a safe direct retry).

- `2601.05554` — SPAM: Style Prompt Adherence Metric for Prompt-based TTS. New CLAP-inspired automatic metric for TTS style-prompt adherence, validated for both plausibility (MOS correlation) and faithfulness (paraphrase-invariance via paired t-test) — a genuinely rigorous two-part validation methodology for an evaluation metric. 1 figure embedded (scorer architecture, since the fusion design and multi-positive SupCon loss were judged genuinely novel, not just an applied metric).
- `2601.05564` — The ICASSP 2026 HumDial Challenge. First challenge jointly benchmarking emotional intelligence and full-duplex interaction using authentic professional-actor recordings (not synthetic mixing or concatenation); 100+ registered teams, 15 valid submissions. No figures in the source paper.
- `2505.15727` — VocalBench. Large (~24k instance) bilingual benchmark across 14 capabilities, 27 evaluated models spanning all major SCA paradigms (cascade/SpeechLLM/Omni-LLM/API); rich, genuinely generalizable field-level findings (LLM backbone drives semantic gains without acoustic/empathy gains; E2E models more robust than cascades; paralinguistic control lags semantic instruction-following). Large parsed source file required paginated reading. No figures embedded (benchmark paper, no architectural-novelty type).
- `2601.08450` — Decoding Order Matters in Autoregressive Speech Synthesis. Small, rigorous University of Sheffield paper using a masked-diffusion framework as a controlled instrument to directly challenge the near-universal left-to-right decoding convention in AR speech synthesis; genuinely novel `contradicts`-role claim (rare in this session, most claims have been supports/complicates). Secondary finding that HiFi-GAN can vocode 1-bit-quantized mel-spectrograms without retraining. No figures embedded (all 6 figures are results plots or raw spectrograms, none are architecture diagrams).

**Mechanical abstract-callout check held for the whole batch**: ran `grep -n "!tip\]\|!abstract\]\|!important\]"` against every drafted page before the health check, as adopted at the end of Batch 3. It caught the mistake again on 2 of 4 papers this batch (`2601.05564`, `2505.15727`) before they ever reached the health check — confirming the mechanical check is working as the reliable backstop that written reminders alone were not. Total recurrence count for the full session: 7 (5 caught by health check in batches 1-3, 2 caught pre-emptively by the grep check in batch 4).

QC notes: `wiki/index.md` count fix (3 occurrences) needed manually on every paper, as expected. `papers/index.md` row count and `wiki/papers/*.md` file count verified to match after each paper (758, 759, 760, 761). No `review_flags` emitted by any of the 4 papers. `arxiv_comment` checked for future-conference-acceptance language on every paper this batch (per the batch-3 precedent); none present.

Corpus page count: 757 → 761. Q1 2026 progress: 19 → 23 ingested, 147 → 143 remaining (58 rejected, unchanged). Not yet committed/pushed.

**This completes the original 16-paper preselected candidate list** (built 2026-08-03 at session start, spanning `published_date` 2026-01-01 through 2026-01-13). 143 papers remain in Q1 2026 scope; a fresh chronological candidate list should be built at the start of the next session before continuing.

### 2026-08-03 — Batch 5 (fresh candidate list, papers 1-4)

Ingested sequentially, one at a time, with a health check after each.

- `2601.09239` — DSA-Tokenizer: Disentangled Semantic-Acoustic Tokenization via Flow Matching-based Hierarchical Fusion. 1 figure embedded (framework overview).
- `2602.06053` — PersonaPlex: Voice and Role Control for Full Duplex Conversational Speech Models. Duplex conversational speech model adding role- and voice-conditioning via hybrid text+audio system prompts on top of a Moshi-style backbone; extended Full-Duplex-Bench to multi-role customer-service scenarios. `references.json` in-corpus flag falsely indicated URO-Bench (2502.17810) was in the corpus; verified via direct `ls` and excluded it after confirming it was actually absent. Correctly excluded `instruction-conditioned-tts` from `related_concepts` per the standing SCA-exclusion rule (general-purpose role/persona following in dialogue does not qualify). 1 figure embedded (architecture diagram).
- `2601.10629` — VoiceSculptor: Your Voice, Designed By You. Open-source instruction-based voice design (with RAG-based iterative refinement) unified with zero-shot voice cloning in one framework. Docling figure-numbering mismatch: the placeholder tagged `figure-7.png` but its caption read "Figure 1" (the paper's own numbering); resolved by trusting the caption text over the placeholder number, copied the correct asset file, and labeled it "Figure 1" in the embedded caption to match the source paper.
- `2506.12537` — What Makes a Good Speech Tokenizer for LLM-Centric Speech Generation? A Systematic Study. Controlled, SLM-internal comparison showing decoupled tokenizers (FACodec) outperform coupled/semi-decoupled tokenizers in SLM training despite not always winning on standalone reconstruction quality; introduces multi-token prediction for speech heads (up to 12x faster decoding, WER 6.07→3.01) and RoleTriviaQA, a new speaker-aware role-playing knowledge QA benchmark. `references.json` in-corpus flags were unreliable in the other direction this time — all 46 references flagged `False` even though 10 were actually in-corpus (including NaturalSpeech 3/FACodec, SpeechTokenizer, WavTokenizer, BigCodec, CosyVoice 2, Moshi); verified by direct `ls` lookup against candidate IDs pulled from the reference list rather than trusting the flag. No figure embedded (field_significance.type is empirical-benchmark/engineering-integration/dataset-contribution, no architectural-novelty). Correct `[!abstract]` callout on the first attempt.

**The `[!tip]`/`[!abstract]` callout mistake recurred on all 3 `high`-significance papers this batch** (`2601.09239`, `2602.06053`, `2601.10629`) before being caught by the mandatory `grep -n "!tip\]\|!abstract\]\|!important\]"` check run immediately after drafting each page, per the mechanical mitigation adopted in Batch 3. `2506.12537` (also `high` significance) was the first paper all session to get the callout right on the first attempt. Running session total: 10 recurrences (5 caught by health check in batches 1-3, 2 caught pre-emptively in batch 4, 3 caught pre-emptively in batch 5).

QC notes: `wiki/index.md` count fix needed manually on every paper. On `2506.12537`, the automated count-update script's row-counting logic (filtering out lines containing the substrings `ID`/`Title`) undercounted by 10 (reported 755 against an actual 765 file/row count) — root-caused as the known index-count-drift class of bug, not a one-off; fixed by using the direct `grep -c '^| \[\['` row count as authoritative and manually correcting all 3 occurrences in `wiki/index.md` to 765. `papers/index.md` row count and `wiki/papers/*.md` file count verified to match after each paper (762, 763, 764, 765). No `review_flags` emitted by any of the 4 papers.

Corpus page count: 761 → 765. Q1 2026 progress: 23 → 27 ingested, 143 → 139 remaining (58 rejected, unchanged). Not yet committed/pushed.

### 2026-08-03 — Batch 6 (fresh candidate list continued, papers 5-8)

Ingested sequentially, one at a time, with a health check after each. Continued chronologically by `published_date` from where Batch 5 left off.

- `2601.11141` — FlashLabs Chroma 1.0: A Real-Time End-to-End Spoken Dialogue Model with Personalized Voice Cloning. First open-source system to combine sub-second streaming latency with personalized voice cloning; decouples coarse acoustic-code generation (long-context Backbone) from residual-codebook refinement (frame-local Decoder) to keep both dimensions fast. Zero-shot SIM (0.81) exceeds the human baseline and all compared TTS systems including Seed-TTS. Notable finding: listeners preferred synthesized ElevenLabs audio over ground-truth human recordings 92% of the time, undercutting naturalness-preference as a proxy for speaker-similarity fidelity. 1 figure embedded (overall architecture).
- `2601.16225` — ES4R: Speech Encoding Based on Prepositive Affective Modeling for Empathetic Response Generation. Explicitly models affective context (dual-level intra-turn/inter-turn attention) *before* generic speech encoding rather than relying on the encoder or post-hoc fusion to preserve emotion cues; the largest ablation effect all session (removing this module collapsed BLEU-4 by ~10x). Energy-trajectory-based empathetic prosody strategy selection is a genuinely lightweight, interpretable alternative to explicit emotion supervision. 1 figure embedded (three-stage framework).
- `2601.12205` — Do Neural Codecs Generalize? A Controlled Study Across Unseen Languages and Non-Speech Tasks. Trains NACs from scratch under matched architecture/training configuration (varying only pretraining data coverage) to cleanly isolate three previously confounded generalization questions; counterintuitive finding that non-speech pretraining data does not trade off against speech-task performance, contrary to the authors' own initial hypothesis. No figure embedded (empirical-benchmark/negative-result, no architectural-novelty).
- `2601.12289` — ParaMETA: Towards Learning Disentangled Paralinguistic Speaking Styles Representations from Speech. Two-stage contrastive framework (graded META-space regularization + per-task prototype-anchored subspaces) that cleanly qualifies for the `disentanglement` tag per the standing tagging rule (explicit training mechanism with ablation evidence, not just contrastive framing). `arxiv_comment` flagged "Accepted to AAAI-26"; applied the standing arXiv-venue precedent (venue stays `arXiv`/preprint until a real Anthology-style ID exists) without needing to look it up fresh. Honest negative finding embedded in the results: language-attribute manipulation nearly fails (55% accuracy) since language identity is bound to text/phonetic content rather than a purely acoustic style attribute. 1 figure embedded (framework overview).

**Zero `[!tip]`/`[!abstract]` callout mistakes this batch** — all 4 papers (3 of them `high` significance) got the callout right on the first attempt, verified by the mandatory `grep -n "!tip\]\|!abstract\]\|!important\]"` check before health check. This is the first fully clean batch on this recurring issue; running session total holds at 10 recurrences (unchanged from Batch 5).

QC notes: `wiki/index.md` count fix needed manually on every paper (3 occurrences each), continuing to use the direct `grep -c '^| \[\['` row count as authoritative per the fix adopted in Batch 5. `papers/index.md` row count and `wiki/papers/*.md` file count verified to match after each paper (766, 767, 768, 769). No `review_flags` emitted by any of the 4 papers. `references.json` in-corpus flags continued to be unreliable and were independently verified by direct `ls` lookup on every paper rather than trusted (no false positives or negatives caught this batch, but the check was still run every time).

Corpus page count: 765 → 769. Q1 2026 progress: 27 → 31 ingested, 139 → 135 remaining (58 rejected, unchanged). Not yet committed/pushed.

### 2026-08-11 — Batch 7 (fresh candidate list, papers 1-4 of 12 preselected)

Ingested sequentially, one at a time, with a health check after each. New 12-paper chronological candidate list preselected at session start, `published_date` 2026-01-18 through 2026-01-22.

- `2601.12480` — A Unified Neural Codec Language Model for Selective Editable Text to Speech Generation (SpeechEdit, Microsoft). Unified instruction interface over a VALL-E-style AR/NAR codec-LM backbone covering zero-shot TTS, voice conversion, emotion control, and prosody control as special cases of one editing mechanism. Tagged `[TTS, VC]` (dedicated VC evaluation with subjective CMOS across four speakers). `disentanglement` and `instruction-conditioned-tts` concept tags considered and excluded (disentanglement is implicit/data-driven, not an explicit mechanism; instruction tokens are fixed categorical/ordinal, not natural language). 1 figure embedded. Agent's own draft used bare `[[id]] (Name)` citation format in Wiki Connections against the SKILL.md template's literal text; caught and self-corrected by the agent to piped `[[id|Name]]` format after checking actual corpus convention.
- `2409.16681` — Emotional Dimension Control in Language Model-Based Text-to-Speech: Spanning a Broad Spectrum of Human Emotions. Continuous PAD (pleasure-arousal-dominance) conditioning for LM-based TTS emotion control, avoiding categorical emotion labels. arXiv ID prefix (2409, Sept 2024) doesn't match `published_date` (2026-01-19); checked `arxiv_comment` ("ICASSP 2026") and full paper text for "full version of" / "extended version" language, found none — read as a normal arXiv revision timestamp coinciding with ICASSP 2026 camera-ready, not a duplicate-paper case. **QC catch:** agent left 5 bare `[[id]] (Name)` citations in Wiki Connections unfixed, incorrectly reasoning they matched the skill template; manually corrected to piped format after the fact (health check only warns on this, doesn't error, so it passed before the fix).
- `2601.12966` — Lombard Speech Synthesis for Any Voice with Controllable Style Embeddings. Fine-tunes F5-TTS with FiLM-conditioned style embeddings (replacing in-context reference-audio conditioning) for zero-shot Lombard-speech control; PCA-based mechanism for interpretable loudness/clarity control. F5-TTS citation correctly resolved to canonical ID `2025.acl-long.313` per standing precedent. **QC catches:** (1) Org column left blank in `papers/index.md` despite a valid multi-institution `organization` field (KIT Campus Transfer GmbH, KIT, CMU) — filled in manually as "KIT / CMU"; (2) `wiki/index.md`'s 3 count occurrences were internally inconsistent after the agent's edit (771, 771, 762 — three different wrong numbers, none matching the authoritative `grep -c` count of 772) — corrected all 3 to 772.
- `2601.13055` — VoCodec: An Efficient Lightweight Low-Bitrate Speech Codec. Combines Vocos, DAC-style RVQ, and ConvNeXt/ResNet blocks; correctly classified as `engineering-integration`/`empirical-benchmark` (no architecture figure copied per invariant #10). Zero in-corpus references (0/30 in `references.json`, and none found by manual check either). Table 1's per-condition objective metrics had garbled row alignment in the Docling parse; agent correctly excluded the ambiguous values from frontmatter rather than risk misattribution, and noted this in Limitations. Clean on all counts, including index count and Org field, after explicit instructions incorporating the prior three papers' QC catches.

**Two new recurring-mistake classes surfaced this batch** (distinct from the settled `[!tip]`/`[!abstract]` issue, which had zero recurrences across all 4 papers): (1) bare `[[id]] (Name)` citation format in Wiki Connections instead of piped `[[id|Name]]` — occurred on 2 of the first 2 papers before being explicitly called out in agent instructions, zero recurrence on papers 3-4 once the instruction was explicit; (2) `wiki/index.md` count-fix producing internally inconsistent numbers across its 3 occurrences (not just stale numbers, but 3 different wrong values in the same edit) — worth continuing to verify all 3 occurrences resolve to the same authoritative number, not just that they were "updated."

QC notes: title truncation caught and fixed on paper 1 only (`2601.12480`, cut mid-word as "Selective Edi"); papers 2-4 came through with full titles intact once agents were explicitly told to re-read the line back. `papers/index.md` row count and `wiki/papers/*.md` file count verified to match after each paper (770, 771, 772, 773). No `review_flags` emitted by any of the 4 papers. `references.json` in-corpus flags remained unreliable in both directions (paper 1 undercounted by manual title search; paper 4 correctly reported zero) — independently verified against the real `wiki/papers/` directory on every paper as usual.

Corpus page count: 769 → 773. Q1 2026 progress: 31 → 35 ingested, 135 → 131 remaining (58 rejected, unchanged). Not yet committed/pushed.

### 2026-08-11 — Batch 8 (fresh candidate list continued, papers 5-8 of 12 preselected)

Ingested sequentially, one at a time, with a health check after each. Continued chronologically from where Batch 7 left off.

- `2602.11172` — Synthesizing the Virtual Advocate: A Multi-Persona Speech Generation Framework for Diverse Linguistic Jurisdictions in Indic Languages. Single-author case study prompting closed Gemini 2.5 Flash/Pro TTS models to produce persona-conditioned courtroom speech across five Indic languages; no model trained, Gemini used as a black box (precedent: `2503.04721` Full-Duplex-Bench). Correctly classified `field_significance: low` with `review_flags` emitted (unreported evaluator count/qualifications, no non-Gemini baseline) — added to the Manual Verification Queue. `subjective-evaluation` tag verified legitimate (real human Likert-scale ratings, not LLM-judge). No figure (no architectural-novelty type). Clean on all structural QC.
- `2601.13758` — GOMPSNR: Reflourish the Signal-to-Noise Ratio Metric for Audio Generation Tasks. **Session-limit interruption mid-ingest**, recovered per the standard two-case procedure: checked the standalone content repo directly and found a partial-write state (paper page written and well-formed, but `papers/index.md` title truncated, no `log.md` entry, metadata still `status: accepted`). Completed by hand rather than re-running the agent: fixed the truncated title, filled in the missing `codec` task tag omitted from the row (page frontmatter had `task: [evaluation, codec]`), added the `log.md` entry, and set `status: ingested`/`ingested_date`/`generation_history` in metadata (also backfilled `task: [evaluation, codec]` into the metadata JSON, which had only `["evaluation"]` from the original filter pass). Corrected phase-distance term for SNR (GOMPSNR) plus derived vocoder/codec training losses; validated across 4 vocoders and 2 codecs. Citations independently verified (5/5 in-corpus refs have pages, all `ingested`).
- `2601.13802` — Habibi: Laying the Open-Source Foundation of Unified-Dialectal Arabic Speech Synthesis. F5-TTS fine-tuned for unified multi-dialect Arabic TTS across seven dialects with curriculum training; introduces the first standardized multi-dialect Arabic TTS benchmark. 8 in-corpus citations, all independently verified (pages exist, status `ingested`). Clean on all structural QC first attempt (piped wikilinks, full title, Org/Task columns, count consistency).
- `2601.13835` — The Role of Prosodic and Lexical Cues in Turn-Taking with Self-Supervised Speech Representations. Interpretability/probing paper (not a generative system): uses a WORLD-vocoder resynthesis technique purely as a diagnostic tool to isolate prosodic vs. lexical cues for testing an existing turn-taking model (VAP) built on CPC/wav2vec2.0 representations. **Scope judgment independently re-verified** rather than trusting the agent's self-justification: confirmed against 4 existing in-corpus turn-taking papers (`2025.sigdial-1.21`, `2025.iwsds-1.27`, `2508.07375`, `2509.23938`), two of which are themselves pure timing/survey papers with no synthesis component — this is an established corpus precedent, not a one-off, and turn-taking (deciding *when* to speak) is structurally distinct from the DST/ASR "understanding-only" rejection precedent since it's a core SCA behavior. Accepted the ingest. No in-corpus references (all 24 citations are prior non-corpus work).

**New recurring-issue class confirmed:** the Org/Task column omission from `papers/index.md` seen once in Batch 7 (blank Org) recurred as a blank Org on `2602.11172` initially then caught before health check, and as a dropped secondary task tag on `2601.13758` (only `evaluation` shown in the row despite `task: [evaluation, codec]` in frontmatter) — worth continuing the row-vs-frontmatter cross-check on every multi-tag paper, not just assuming a single task value is complete.

QC notes: `wiki/index.md` count fix needed manually on `2601.13758` only (post-interruption completion); the other 3 papers' agents correctly self-verified all 3 occurrences matched the authoritative `grep -c '^| \[\['` count. `papers/index.md` row count verified after each paper (774, 775, 776, 777). 1 `review_flags` entry (`2602.11172`), added to Manual Verification Queue. All in-corpus citations across the batch independently verified against the real `wiki/papers/` directory and status field, not trusted from agent self-report.

Corpus page count: 773 → 777. Q1 2026 progress: 35 → 39 ingested, 131 → 127 remaining (58 rejected, unchanged). Not yet committed/pushed.

### 2026-08-11 — Batch 9 (cadence dropped to one-paper-at-a-time with go-ahead between each, per user request)

- `2601.13948` — Stream-Voice-Anon: Enhancing Utility of Real-Time Speaker Anonymization via Neural Audio Codec and Language Models. Real-time streaming speaker-anonymization system (autoregressive VC over a frozen FishSpeech neural-codec token space); benchmarked against DarkStream (`2509.04667`, prior SOTA) under the VoicePrivacy 2024 Challenge protocol at matched latency. Tagged `VC` per the standing rule (dedicated VC-style system + genuine metrics: WER, UAR, EER). **QC catch:** `task: ["VC"]` used quoted-list frontmatter syntax instead of the more common unquoted `task: [VC]` — a new instance of the same quoting drift previously resolved for `related_concepts` (213 of ~726 pages currently use quoted `task:`, worth a future normalization pass, not fixed corpus-wide here). Normalized this page only. Citation to DarkStream independently verified (page exists, `status: ingested`). Clean on all other structural QC (callout, piped wikilinks, title, Org, count consistency) on first attempt.

Corpus page count: 777 → 778. Q1 2026 progress: 39 → 40 ingested, 127 → 126 remaining (58 rejected, unchanged). Not yet committed/pushed.

- `2601.14472` — Prosody-Guided Harmonic Attention for Phase-Coherent Neural Vocoding in the Complex Spectrum (ICASSP 2026, BME). Adds an F0-driven harmonic-attention encoder stage plus explicit phase supervision to a complex-spectrum GAN vocoder, contrasted against HiFi-GAN (auxiliary-feature F0 baseline) and Vocos (closest architectural relative). Formal MOS listening study (20 listeners, ITU-T P.800). `references.json` only auto-matched 1 in-corpus reference; agent manually cross-checked `papers/index.md` and correctly recovered the 3 actual Table I baselines (HiFi-GAN, Vocos, BigVGAN) as in-corpus, all independently re-verified here (pages exist, `status: ingested`). Clean on every structural QC check on first attempt: unquoted `task`/`related_concepts`, piped wikilinks, full title, Org filled, count consistency (779 across all 3 occurrences).

Corpus page count: 778 → 779. Q1 2026 progress: 40 → 41 ingested, 126 → 125 remaining (58 rejected, unchanged). Not yet committed/pushed.

- `2601.14960` — VCNAC: A Variable-Channel Neural Audio Codec for Mono, Stereo, and Surround Sound (Amazon AGI). **Scope judgment independently re-verified**: title suggested a general/surround-audio codec possibly out of scope, but the agent's read of the full paper found genuine speech-specific content (LibriTTS/LibriVox training data, a dedicated "Single-Channel Speech Evaluation" modality with PESQ/SI-SDR on LibriTTS) and cited `2508.05207` (SpectroStream, a general-audio codec already accepted on the same basis) as precedent — independently confirmed that precedent's metadata (`status: ingested`, relevance note: "full-band neural codec extending SoundStream to 48kHz stereo") before accepting the ingest. 1 architecture figure embedded (variable-channel design). Citation to SpectroStream independently verified. Clean on all structural QC on first attempt (count, title, Org, unquoted task/related_concepts, piped wikilinks).

Corpus page count: 779 → 780. Q1 2026 progress: 41 → 42 ingested, 125 → 124 remaining (58 rejected, unchanged). Not yet committed/pushed.

- `2601.15596` — DeepASMR: LLM-Based Zero-Shot ASMR Speech Generation for Anyone of Any Voice (SJTU / VUI Labs). Two-stage LLM (Qwen2.5-0.5B over CosyVoice2 S3 tokens) + Voicebox-style flow-matching acoustic decoder, extending zero-shot voice cloning to ASMR style from an ordinary-speech reference; evaluated in English and Mandarin. Sanity-checked as a genuine generative system (not a dataset/analysis paper) before ingest, per instruction. 8 in-corpus citations, all independently verified (pages exist, `status: ingested`). Clean on all structural QC on first attempt.

**This completes both the one-paper-at-a-time cadence (4 papers: `2601.13948`, `2601.14472`, `2601.14960`, `2601.15596`) and the full original 12-paper preselected candidate list** (`published_date` 2026-01-18 through 2026-01-22) built at the start of this session. A fresh chronological candidate list should be built at the start of the next session before continuing. Zero recurring QC issues surfaced on the final 4 papers beyond the single `task:` quoting fix on `2601.13948` — the `[!tip]`/`[!abstract]` callout mistake had zero recurrences across the entire session (8 papers), a first.

Corpus page count: 780 → 781. Q1 2026 progress: 42 → 43 ingested, 124 → 123 remaining (58 rejected, unchanged). Not yet committed/pushed.

### 2026-08-12 — Batch 10 (fresh candidate list, papers 1-4 of 12 preselected; cadence returned to sequential batches of 4)

New 12-paper chronological candidate list preselected at session start, `published_date` 2026-01-22 through 2026-01-28. Ingested sequentially, one at a time, with a health check after each; no per-paper go-ahead this batch per user's explicit cadence choice at session start.

- `2601.16023` — Timbre-Aware LLM-based Direct Speech-to-Speech Translation Extendable to Multiple Language Pairs (DS2ST-LM). Single-stage LLM-based direct S2ST framework adapting the SLAM-Omni architecture (Whisper encoder, Qwen2-0.5B LLM, CosyVoice-style semantic tokenizer + flow-matching + HiFi-GAN vocoder) to speech-to-speech translation; releases GigaS2S-1000, a 1000-hour zh-en corpus built by synthesizing Chinese target speech with XTTS-v2 over GigaST. `field_significance.type` classified as engineering-integration/dataset-contribution/empirical-benchmark (no architectural-novelty), so no figure copied despite the paper having 4 figures. Initial Wiki Connections draft used bare `[[id]] (Name)` format for paper-ID bullets per literal SKILL.md template text; caught against the standing `feedback_wikilink_context_format` memory note (piped `[[id|Name]]` is the actual corpus convention everywhere outside `papers/index.md`) and corrected before health check. 7 in-corpus references independently verified by manual title/ID search (`references.json` in-corpus flag only caught 1 of 7).
- `2601.16618` — PROST-LLM: Progressively Enhancing the Speech-to-Speech Translation Capability in LLMs. First application of preference optimization (DPO/SimPO) to LLM-based S2ST, using back-translation-derived preference pairs constructed without human labeling; tri-task + chain-of-modality SFT on CVSS (en-fr) with a LLaMA-3.2-3B backbone over mHuBERT units. `field_significance` high, `architectural-novelty` (novel training/preference-construction procedure) + `empirical-benchmark`; 1 figure embedded (training system + architecture, Fig. 1). Notable finding: preference-pair scoring metric choice (WER/MCD/BLEU/METEOR) has only a secondary effect once DPO is applied, and monolingual Common Voice speech can substitute for paired CVSS data as a preference-optimization source. 4 in-corpus references verified (`references.json` flagged 0).
- `2601.17086` — SonoEdit: Null-Space Constrained Knowledge Editing for Pronunciation Correction in LLM-Based TTS. First application (per the paper) of null-space-constrained knowledge editing (adapted from ROME/AlphaEdit) to neural TTS; localizes pronunciation to layers 15-21 of Orpheus-TTS's LLaMA-3.2-3B backbone via causal tracing, then applies a closed-form, training-free weight edit constrained orthogonal to a LibriTTS-derived "general speech" subspace. Introduces HardNoun-300, a 300-proper-noun/6-language/3,000-utterance mispronunciation benchmark. `field_significance` high, `architectural-novelty` + `dataset-contribution`; 1 figure embedded (null-space editing illustration, Fig. 2 — Fig. 1 and Fig. 3 excluded as generic background schematic and results/analysis plot respectively, per the figure-selection rule). A role-prefix self-check caught and fixed one claim mislabeled `contradicts:` that should have been `supports:` (the evidence directly confirms the proposition rather than opposing anything) before it reached the page. 7 in-corpus references verified (`references.json` flagged 1 of 7; ROME, AlphaEdit, WavLM, VoiceBox, and SNAC's own papers confirmed absent from corpus, consistent with the corpus's TTS/VC/SCA scope boundary).
- `2601.13742` — Hearing Between the Lines: Unlocking the Reasoning Power of LLMs for Speech Evaluation. Introduces HCoT (Human Chain-of-Thought), a dimension-first (Content/Voice-Quality/Paralinguistics) typed-tie re-annotation protocol for two existing S2S human-preference benchmarks (SpeakBench, S2S-Arena), diagnosing that their original no-tie/untyped-tie labels fabricate winners on both-bad pairs; and TRACE, a training-free text-LLM judge that reasons over a structured textual blueprint of pre-extracted audio signals (ASR, DNSMOS-style quality predictors, prosody/affect descriptors) rather than raw audio, beating both a transcript-only LLM judge and a full audio-language-model judge at ~1/3 the ALM's cost. `field_significance` high, `evaluation-contribution` + `dataset-contribution` (no `architectural-novelty`), so no figure copied despite a clear TRACE-pipeline diagram (Fig. 2) being available. `subjective-evaluation` tag applied on the strength of the genuine human dimension-first rating protocol (inter-rater Cohen's κ reported), not the LLM-judge component itself, consistent with the standing rule that automated/LLM-judge scoring alone never qualifies. 7 in-corpus references verified (`references.json` flagged 4 of 7; the paper's own S2S-Arena dataset source, 2503.05085, confirmed absent from corpus).

QC notes: `wiki/index.md`'s 3 count occurrences verified consistent after every paper (782, 783, 784, 785). `papers/index.md` row count verified to match after each paper. Zero `[!tip]`/`[!abstract]` callout mistakes across all 4 papers. Zero `review_flags` emitted. Health check (`--module ingest --id`) passed clean (0 errors, 0 warnings) on all 4 papers individually; a full corpus-wide `--module ingest` run afterward showed 0 errors but 1170 pre-existing warnings unrelated to this batch (consistent with the known `task:`-quoting and other tracked BACKLOG drift items, not a regression from these 4 papers).

Corpus page count: 781 → 785. Q1 2026 progress: 43 → 47 ingested, 123 → 119 remaining (58 rejected, unchanged). Not yet committed/pushed.

### 2026-08-12 — Batch 11 (fresh candidate list continued, papers 5-8 of 12 preselected)

Ingested sequentially, one at a time, with a health check after each. Continued chronologically from where Batch 10 left off.

- `2601.18094` — OneVoice: One Model, Triple Scenarios-Towards Unified Zero-shot Voice Conversion (China Mobile JIUTIAN Research). Unifies linguistic-preserving, expressive, and singing voice conversion in a single zero-shot model via a Mixture-of-Experts backbone with explicit shared/domain expert specialization, dual-path (global scenario-prior + local dynamic) routing, and per-layer gated prosody fusion; VAE-free next-patch diffusion (DiTAR-derived) with a flow-matching LocalDiT head. Matches or exceeds 6 specialized single-scenario baselines despite a ~250x speech/singing data-scale imbalance, mitigated via two-stage progressive training with LoRA-based domain experts. `field_significance` high, architectural-novelty + empirical-benchmark; 2 figures embedded (overall architecture, MoE/routing detail).
- `2601.18281` — Reflecting Twice before Speaking with Empathy: Self-Reflective Alternating Inference for Empathy-Aware End-to-End Spoken Dialogue (Nankai University / Meituan LongCat). Introduces EmpathyEval (descriptive natural-language empathy evaluator, 18,000-dialogue Mandarin dataset) and ReEmpathy (GLM-4-Voice fine-tuned with a novel mechanism interleaving spoken response chunks with free-form empathetic reflection chunks at inference time). Beats SFT, DPO, and single-step Chain-of-Thought-before-Speaking baselines on every metric; a reflection-disabled ablation and the CoTBS control together isolate the alternating structure itself (not just reasoning content or extra training signal) as the source of the gain. `field_significance` high, architectural-novelty + evaluation-contribution + dataset-contribution; 1 figure embedded (EmpathyEval + ReEmpathy framework overview). **Citation integrity catch:** `references.json` flagged ParaS2S (2511.08723) as in-corpus, but direct verification found it `status: rejected`; excluded from related_papers/Wiki Connections per the standing rejected-paper citation rule, mentioned by name in prose only.
- `2601.18438` — UrgentMOS: Unified Multi-Metric and Preference Learning for Robust Speech Quality Assessment (SJTU / CMU / TU Braunschweig / Meta / Waseda / VUI Labs). Unified speech-quality model jointly predicting 15 objective/perceptual metrics (with an explicit missing-label-tolerant masked loss) plus a naturalness-conditioned cross-attention preference module (CMOS) trained partly on preference pairs derived automatically from existing absolute-MOS datasets via a tunable tie threshold. Notable finding: most existing single-target MOS predictors score worse than random on tie-allowing accuracy against a modern-TTS test set (SpeechJudge), evidencing score-compression/discriminative-sensitivity loss as synthesized speech approaches natural quality. `field_significance` high, architectural-novelty + evaluation-contribution + dataset-contribution; 1 figure embedded (AMPM/NCPM architecture). **Citation integrity catch:** `references.json` flagged TTSDS2 (2506.19441) and SpeechJudge (2511.07931) as in-corpus; both verified `status: rejected` and excluded from links. `related_concepts` scoped to a single tag (`evaluation-metrics`) rather than the usual 3-6, since no other concept's scope genuinely fit a general-purpose cross-domain (TTS/VC/SE) quality-assessment tool rather than a generation system.
- `2601.18694` — Neural Multi-Speaker Voice Cloning for Nepali in Low-Resource Settings (IOE Thapathali Campus, Nepal). Adapts the established SV2TTS-style pipeline (GE2E speaker encoder + Tacotron2 + fine-tuned WaveRNN) to Nepali, a language with no prior multi-speaker voice-cloning system, using two newly collected corpora (235h/833-speaker encoder set, 8.67h/6,046-pair synthesizer set). `field_significance` moderate, engineering-integration + dataset-contribution (no architectural-novelty, so no figure copied despite an available architecture diagram, per the standing figure-selection rule); genuinely useful methodological contrast the paper draws itself: it reports disclosed, quantitative MOS evaluation (55 raters) where the two other surveyed Nepali TTS systems report none. Only 1 in-corpus reference found (Tacotron); all others (SV2TTS, WaveRNN, prior Nepali voice-cloning study) confirmed absent from corpus by manual title search after `references.json` returned zero flags.

QC notes: `wiki/index.md`'s 3 count occurrences verified consistent after every paper (786, 787, 788, 789). `papers/index.md` row count verified to match after each paper. Zero `[!tip]`/`[!abstract]` callout mistakes across all 4 papers. Zero `review_flags` emitted. Two papers this batch (`2601.18281`, `2601.18438`) surfaced `references.json` false positives pointing at since-rejected papers (3 instances total: ParaS2S, TTSDS2, SpeechJudge) — a new variant of the known references.json unreliability pattern, this time flagging rejected rather than merely absent papers; all caught by the standing "verify status, not just page existence" citation-integrity check. Health check (`--module ingest --id`) passed clean (0 errors, 0 warnings) on all 4 papers individually.

Corpus page count: 785 → 789. Q1 2026 progress: 47 → 51 ingested, 119 → 115 remaining (58 rejected, unchanged). Not yet committed/pushed.

### 2026-08-12 — Batch 12 (queue revised mid-session: skipped paper folded back in, then remainder of 12-paper list)

Batch 11's "papers 5-8" label was wrong: it actually processed rows 6-9 of the 12-paper candidate list, silently skipping row 5 (`2601.17761`, AR-Omni), a recurrence of the known batch-numbering-drift class of mistake. Caught when the user asked to see the full 12-paper list with dates; user's resolution: fold the skipped paper into the front of the remaining queue rather than treating it as a separate exception, since ingestion is chronological. Revised queue for this batch: `2601.17761` (2026-01-25, the skipped paper), then `2601.19952`, `2601.19063`, `2601.19781` (the true remaining rows 10-12), completing the original 12-paper list in full.

- `2601.17761` — AR-Omni: A Unified Autoregressive Model for Any-to-Any Generation (HKPolyU / USTC / HIT Shenzhen). Single 7B autoregressive Transformer decoder generating text, image, and streaming speech from one joint discrete vocabulary with no external diffusion or non-AR expert decoder; adopts a single-codebook acoustic speech tokenizer (WavTokenizer) instead of the dual-codebook semantic/acoustic split used by most prior speech-LLM/any-to-any systems, achieving 146ms first-token latency and 0.88 RTF on zero-shot TTS (VCTK) while matching the best token-based baseline's WER. `field_significance` high, architectural-novelty + empirical-benchmark; 1 figure embedded (overall architecture) after resolving a Docling figure-numbering mismatch (placeholder `[FIGURE 2]` vs. caption "Figure 1") by trusting the caption, per established precedent.
- `2601.19952` — LTS-VoiceAgent: A Listen-Think-Speak Framework for Efficient Streaming Voice Interaction via Semantic Triggering and Incremental Reasoning (Meituan / UCAS). Cascaded (ASR-LLM-TTS) streaming voice-agent framework separating *when* to think (a learned Dynamic Semantic Trigger replacing VAD/fixed-chunk triggering) from *how* to reason incrementally (a Dual-Role Stream Orchestrator coordinating a background Thinker and foreground speculative Speaker with selective state-preserving rollback on interruption). Individually-ablated evidence ties the trigger specifically to computational efficiency/interruption-robustness and the orchestrator specifically to reasoning quality/stability. Introduces a Pause-and-Repair benchmark (audio-only, real ASR, synthesized natural disfluencies) rather than simulated text-chunk approximations. `field_significance` high, architectural-novelty + dataset-contribution + empirical-benchmark; 1 figure embedded (framework overview). `related_concepts` scoped to `[speech-to-speech, evaluation-metrics]` since the novelty is reasoning-orchestration architecture, not a TTS/VC-specific mechanism (TTS is off-the-shelf CosyVoice2, used only for benchmark-audio construction).
- `2601.19063` — Optimizing Conversational Quality in Spoken Dialogue Systems with Reinforcement Learning from AI Feedback (CMU / Sony). First multi-reward RLAIF/DPO framework for speech-in/speech-out SDS, jointly optimizing semantic, audio-quality, intelligibility, and emotion-consistency rewards (dataset-level combination, 165.7K preference pairs released); extends utterance-level DPO to blockwise duplex models by aggregating per-block log-probabilities into one sequence-level likelihood, avoiding the need for partial-utterance reward labels. Notable finding: joint semantic+emotion training actively *hurts* emotional alignment relative to single-reward emotion-only training, since strong semantic-judge rewards favor safer/more generic (less expressive) responses — a genuine cross-objective trade-off only a multi-reward study could surface. `field_significance` high, architectural-novelty + dataset-contribution + empirical-benchmark; 1 figure embedded (multi-reward framework overview).
- `2601.19781` — Phonological Tokenizer: Prosody-Aware Phonetic Token via Multi-Objective Fine-Tuning with Differentiable K-Means (U Tokyo / Sony / CMU). Fine-tunes SSL-derived phonetic tokens via differentiable k-means under a joint ASR-and-resynthesis multi-task objective, producing a single-codebook token with genuinely disentangled linguistic/prosodic content vs. speaker identity (auxiliary speaker-embedding-conditioned vocoder), matching multi-codebook hybrid-token designs' property profile without the RVQ multi-stream complexity. Outperforms SpeechTokenizer and WavTokenizer baselines on ASR despite only 44 hours of fine-tuning data (vs. 960h/585h for the baselines) built on a 30h phonetic-token init. `field_significance` high, architectural-novelty + empirical-benchmark; 1 figure embedded (tokenizer architecture). ICASSP 2026 accepted paper (venue kept as `arXiv`/preprint per standing precedent, no Anthology-style ID exists yet).

QC notes: `wiki/index.md`'s 3 count occurrences verified consistent after every paper (790, 791, 792, 793). `papers/index.md` row count verified to match after each paper. Zero `[!tip]`/`[!abstract]` callout mistakes across all 4 papers. Zero `review_flags` emitted. Health check (`--module ingest --id`) passed clean (0 errors, 0 warnings) on all 4 papers individually.

Corpus page count: 789 → 793. Q1 2026 progress: 51 → 55 ingested, 115 → 111 remaining (58 rejected, unchanged). **This completes the full 12-paper candidate list originally built at the start of this session** (`published_date` 2026-01-22 through 2026-01-27, with the mid-session queue correction described above). A fresh chronological candidate list should be built at the start of the next session before continuing. Not yet committed/pushed.

### 2026-08-12 — Batch 13 (fresh candidate list, papers 1-4 of 12 preselected)

New 12-paper chronological candidate list preselected at session start, `published_date` 2026-01-27 through 2026-01-31. Ingested sequentially, one at a time, with a health check after each.

- `2601.19786` — Rethinking Discrete Speech Representation Tokens for Accent Generation (University of Edinburgh). First systematic investigation of accent information in Discrete Speech Representation Tokens (DSRTs); introduces a novel Accent ABX accessibility metric plus a cross-accent voice-conversion recoverability framework. Controlled ablations directly refute two specific published claims: Vevo's codebook-size disentanglement claim and CosyVoice's ASR-supervised token design, both empirically shown not to preserve accent information as claimed. Proposed content/content-accent tokens (selected via the paper's own measurement framework) outperform Vevo's tokens on both objective metrics and subjective Accent SMOS ratings. `field_significance` high, architectural-novelty + evaluation-contribution + empirical-benchmark; 1 figure embedded (evaluation pipeline overview).
- `2601.20094` — T-Mimi: A Transformer-based Mimi Decoder for Real-Time On-Phone TTS (Meta). Replaces the Mimi codec decoder's deconvolution upsampling with a purely transformer-and-linear design (inspired by the authors' own prior TS3-Codec), cutting on-device 80ms-chunk latency from 42.1ms to 4.4ms (9.6x) on a Samsung Galaxy S22 with no significant CMOS quality loss. Quantization-aware-training ablation finds waveform-adjacent decoder layers are disproportionately quantization-sensitive and must stay full-precision. `field_significance` high, engineering-integration + empirical-benchmark (not architectural-novelty, since the transformer-only-codec-decoder concept was already established by TS3-Codec) — no figure copied per the standing figure-selection rule. **QC note:** flagged and corrected a mismatch between `related_papers` (8 entries) and Wiki Connections bullets (7) before finalizing — UniAudio was in frontmatter but had no corresponding bullet; removed from frontmatter to keep the two in sync.
- `2601.14417` — Quantifying Speaker Embedding Phonological Rule Interactions in Accented Speech Synthesis (USC). Introduces phoneme shift rate (PSR), a novel metric measuring how much speaker embeddings in a frozen pretrained TTS model (Kokoro-82M) preserve or override explicit phonological substitution rules (flapping, rhoticity, vowel correspondences) applied to shift American English toward British English targets. PSR never reaches its theoretical floor even under full rule application, demonstrating measurable accent-speaker entanglement; per-embedding analysis shows entanglement degree varies substantially across individual preset voices. `field_significance` high, evaluation-contribution + conceptual-contribution (no architectural-novelty — no TTS model modified, Kokoro used frozen) — no figure copied.
- `2601.20481` — Erasing Your Voice Before It's Heard: Training-free Speaker Unlearning for Zero-shot Text-to-Speech (Ewha Womans University). First training-free, inference-time speaker-unlearning framework for zero-shot TTS (TruS): builds an averaged "ID-prototype" from retain-speaker DiT activations in a frozen F5-TTS backbone, computes a per-target steering vector from the difference between a one-shot opt-out reference and the prototype, and dynamically selects which DiT layers/flow-steps to steer per sample (μ+σ threshold, ablated as best of 4 tested criteria) before projecting out the identity-aligned activation component. Critically generalizes to opt-out speakers never seen in the base model's pretraining data (LibriSpeech, vs. F5-TTS's Emilia pretraining), a capability retraining-based unlearning (SGU/TGU, direct baselines) structurally cannot provide. `field_significance` high, architectural-novelty + empirical-benchmark; 1 figure embedded (framework overview).

QC notes: `wiki/index.md`'s 3 count occurrences verified consistent after every paper (794, 795, 796, 797). `papers/index.md` row count verified to match after each paper. Zero `[!tip]`/`[!abstract]` callout mistakes across all 4 papers. Zero `review_flags` emitted. Health check (`--module ingest --id`) passed clean (0 errors, 0 warnings) on all 4 papers individually. Notable cross-paper pattern this batch: 3 of 4 papers (Rethinking DSRT, PSR, TruS) are accent/identity-disentanglement-adjacent analysis or safety papers rather than new generation architectures — reflects the natural clustering of this chronological slice, not a selection bias.

Corpus page count: 793 → 797. Q1 2026 progress: 55 → 59 ingested, 111 → 107 remaining (58 rejected, unchanged). Not yet committed/pushed.

### 2026-08-12 — Batch 14 (fresh candidate list continued, papers 5-8 of 12 preselected)

Ingested sequentially, one at a time, with a health check after each. Continued chronologically from where Batch 13 left off.

- `2601.20230` — Unit-Based Agent for Semi-Cascaded Full-Duplex Dialogue Systems (Hunan University). Decomposes dialogue into minimal listen/speak "units" controlled by a single MLLM (Qwen3-Omni) reasoning directly over raw audio plus auxiliary ASR context, unifying turn-taking and utterance-completeness signals (previously split across separate categories in EasyTurn) into one continue/switch decision space; train-free, plug-and-play with off-the-shelf VAD/SV/ASR/TTS components. Ranked 2nd in the ICASSP 2026 Human-like Spoken Dialogue Systems Challenge (Track 2: Full-Duplex). `field_significance` moderate, engineering-integration + empirical-benchmark (no architectural-novelty — all components off-the-shelf) — no figure copied. Short 4-page competition-track paper with no ablation study isolating which design choice drives the reported gains.
- `2601.21886` — Speech Quality-Based Localization of Low-Quality Speech and Text-to-Speech Synthesis Artefacts (Paderborn University). Adapts a segment-slice consistency-regularization technique (previously used for neural-codec-token stability) to frame-level speech-quality prediction, resolving a previously identified "smearing" problem where utterance-level-trained SQA models couldn't precisely localize artefacts. Validated on PartialSpoof localization (F1 0.355→0.492) and, more notably, on real TTS output: applies the regularized detector to F5-TTS and StyleTTS2 outputs and confirms via a 9-expert listening test that flagged segments are judged low-quality significantly more often than random controls, with each TTS system showing a distinct dominant artefact type (StyleTTS2: non-speech/low-quality; F5-TTS: speed/pacing artefacts from reference-length misalignment). `field_significance` high, evaluation-contribution + architectural-novelty — no figure copied (all 3 figures are listening-test UI/results plots, excluded per the standing figure-selection rule, not method diagrams).
- `2601.22661` — Evaluating and Rewarding LALMs for Expressive Role-Play TTS via Mean Continuation Log-Probability (unlisted institution). Introduces MCLP, repurposing a pretrained LALM's own in-context-learning likelihood as an interpretable style-consistency metric (validated: >80% pairwise win-rate agreement with human MOS once ΔMCLP > 0.1), then uses it as a GRPO RL reward gated by a CER content-fidelity constraint for role-play TTS. Ablation directly demonstrates reward hacking in both directions when either component is removed alone (style-only → CER collapses above 50%; content-only → style score regresses below the SFT baseline). Releases a new 1,435-hour, 311k-scene RP-TTS dataset built from real drama dialogue (WenetSpeech-derived) rather than synthetic role profiles. `field_significance` high, architectural-novelty + evaluation-contribution + dataset-contribution; 1 figure embedded (framework overview). Organization left `null` in frontmatter — no institution names were legible in the parsed PDF text (only numeric author-affiliation superscripts with no matching footnote captured).
- `2601.22873` — EmoShift: Lightweight Activation Steering for Enhanced Emotion-Aware Speech Synthesis (CUHK-Shenzhen / HK PolyU / Tianjin University). Extends LLM activation-steering to emotion-aware TTS via a dedicated EmoSteer layer (10M trainable params, <1/30 of full fine-tuning) learning one offset vector per emotion in CosyVoice's output embedding space; matches or beats full fine-tuning on both objective emotion accuracy and subjective MOS/Emo-MOS. Inference-time gain factor gives continuous, empirically-characterized (non-monotonic, peaks ~α=3) emotional-intensity control. Explicitly distinguishes itself from the contemporaneous EmoSteer-TTS (few-shot-derived offsets) by learning steering vectors as trainable parameters. `field_significance` high, architectural-novelty + empirical-benchmark; 1 figure embedded (framework overview).

QC notes: `wiki/index.md`'s 3 count occurrences verified consistent after every paper (798, 799, 800, 801). `papers/index.md` row count verified to match after each paper. Zero `[!tip]`/`[!abstract]` callout mistakes across all 4 papers. Zero `review_flags` emitted. Health check (`--module ingest --id`) passed clean (0 errors, 0 warnings) on all 4 papers individually. Two papers this batch (`2601.20230`, `2601.21886`) correctly received no figure despite having figures available, for two different reasons: no architectural-novelty in the first case, and only non-architecture (UI/results) figures available in the second — worth distinguishing these as separate justifications in future batches rather than collapsing them into one rule-of-thumb.

Corpus page count: 797 → 801. Q1 2026 progress: 59 → 63 ingested, 107 → 103 remaining (58 rejected, unchanged). Not yet committed/pushed.

### 2026-08-12 — Batch 15 (final batch of the 12-paper list, papers 9-12 of 12 preselected)

Ingested sequentially, one at a time, with a health check after each. Completes the second 12-paper chronological candidate list in full (`published_date` 2026-01-27 through 2026-01-31).

- `2601.22889` — DiffuSpeech: Silent Thought, Spoken Answer via Unified Speech-Text Diffusion (unlisted institution). Builds a unified speech-text masked-diffusion LLM (LLaDA-8B backbone) that generates a silent "thinking trace" before its spoken answer, replacing the field's exclusively-autoregressive speech-text LMs with bidirectional, parallel-decodable generation; motivated by speech's irreversibility (unlike text, mid-utterance audio errors cannot be backtracked). Trains on a new 26,387-sample/319-hour THINKINGTALK instruction dataset with explicit thinking traces (Stage 2), after a Stage 1 ASR/TTS speech-text alignment phase. `field_significance` high, architectural-novelty + dataset-contribution + empirical-benchmark; 1 figure embedded (architecture + pipeline overview). Organization left `null` — no institution names legible in the parsed PDF text.
- `2601.23174` — Beyond Fixed Frames: Dynamic Character-Aligned Speech Tokenization / DyCAST (unlisted institution). Replaces fixed-rate codec tokenization with character-aligned variable-frame-rate tokenization (~6-18Hz vs. 12.5-80Hz for fixed-rate baselines), driven by boundary/duration predictors trained on a frozen WavLM-large encoder; scalar spherical quantization (32 parallel streams x vocabulary 4) plus a Vocos decoder reconstruct waveforms. Evaluated across resynthesis, ASR, TTS, speaker-ID, emotion-recognition probing, and voice-conversion tasks. `field_significance` high, architectural-novelty + empirical-benchmark; 2 figures embedded (architecture overview, RAD boundary-detection mechanism). Notable finding: FlexiCodec's canonical wiki page is still filed under `2510.00981` (not yet migrated to its ICLR 2026 ID per a pending BACKLOG.md item) — used the currently-live file for citation.
- `2602.00269` — VoxServe: Streaming-Centric Serving System for Speech Language Models (unlisted institution). A serving-infrastructure paper, not a new generation model: introduces a model-execution abstraction decoupling architecture from system-level optimization so one framework can serve 7 architecturally distinct SpeechLMs (Chatterbox, CosyVoice 2, CSM, GLM-4-Voice, Orpheus, Step-Audio 2, Zonos), plus a streaming-aware scheduler and async pipeline achieving 10-20x higher throughput than official per-model serving baselines at comparable latency. Introduces two new streaming-serving metrics (Time-To-First-Audio, Streaming Viability) distinct from text-LLM serving metrics (TTFT/TPOT). `field_significance` high, architectural-novelty (system design, not a generation architecture) + empirical-benchmark + evaluation-contribution; 1 figure embedded (system architecture overview: Scheduler/Worker/Model). Organization left `null`.
- `2602.00443` — RVCBench: Benchmarking the Robustness of Voice Cloning Across Modern Audio Generation Models (unlisted institution). First benchmark to systematically stress-test VC robustness across the full deployment pipeline (input, generation, output, adversarial-perturbation) rather than isolated failure modes; 225 speakers, 14,370 utterances, 10 tasks, 11 evaluated VC models spanning autoregressive-LM, diffusion/flow, and hybrid architectures. Key findings: no model reaches theoretical SIM upper bounds even in-domain; cross-lingual/non-English cloning degrades sharply; deepfake-detector accuracy is independent of generation quality; anti-cloning perturbations (SafeSpeech/SPEC) are only partially neutralized by denoising. `field_significance` high, dataset-contribution + evaluation-contribution + empirical-benchmark — no figure copied (benchmark paper, no proposed architecture). Organization left `null`.

QC notes: `wiki/index.md`'s 3 count occurrences verified consistent after every paper (802, 803, 804, 805). `papers/index.md` row count verified to match after each paper (`grep -c '^| \[\['` = 805 at batch end). Zero `[!tip]`/`[!abstract]` callout mistakes across all 4 papers. Caught and fixed the recurring bare-vs-piped Wiki Connections wikilink format mistake (`[[id]] (Name)` instead of `[[id|Name]]`) on both `2602.00269` and `2602.00443` — health check flagged it as `wikilink_format` warnings (7 and 8 respectively) on first pass; fixed and re-verified 0 warnings on both. Zero `review_flags` emitted. Health check (`--module ingest --id`) passed clean (0 errors, 0 warnings) on all 4 papers after fixes.

Corpus page count: 801 → 805. Q1 2026 progress: 63 → 67 ingested, 103 → 99 remaining (58 rejected, unchanged). This completes the second 12-paper candidate list in full. Not yet committed/pushed.

### 2026-08-13 — Batch 16 (fresh candidate list, papers 1-4 of 12 preselected)

New 12-paper chronological candidate list preselected at session start, `published_date` 2026-01-31
through 2026-02-08. Ingested sequentially, one at a time, with a health check plus independent
manual QC (callout, title match, task/related_concepts cross-check, citation existence/status) after
each.

- `2602.00594` — Kanade: A Simple Disentangled Tokenizer for Spoken Language Modeling. Dual-branch content/global architecture achieving content-speaker disentanglement purely through an information bottleneck (no adversarial/contrastive/supervised loss); `disentanglement` tag independently re-verified legitimate (explicit bottleneck mechanism + ablation evidence in Table 3), not just "by construction." Tagged `[codec, VC, TTS, SCA]`. 1 figure embedded.
- `2602.02591` — VividVoice: A Unified Framework for Scene-Aware Visually-Driven Speech Synthesis. Face-image-conditioned speech synthesis (timbre + environmental acoustics from a visual scene); flagged a genuine vocabulary gap (no dedicated visual-conditioning term). `disentanglement` and `subjective-evaluation` both independently re-verified legitimate (explicit D-MSVA losses + ablation; 25 human MOS raters). 1 figure embedded.
- `2602.03420` — CoCoEmo: Composable and Controllable Human-Like Emotional TTS via Activation Steering. Post-hoc activation-steering technique; `disentanglement` correctly excluded (no training-time mechanism, fails the standing rule despite steering-based framing). Agent self-corrected a leaked instruction-text line before finalizing, independently re-verified removed. 1 figure embedded.
- `2602.09041` — DSFlow: Dual Supervision and Step-Aware Architecture for One-Step Flow Matching Speech Synthesis. One-step flow-matching distillation replacing adaLN-Zero with lightweight step-aware tokens. F5-TTS correctly cited under its canonical ID (`2025.acl-long.313`). 1 figure embedded.

QC notes: `wiki/index.md`'s 3 count occurrences verified consistent after every paper (806, 807, 808, 809). Zero callout mistakes, zero bare-wikilink issues, zero `review_flags`. All citations independently verified via direct `ls`/status lookup, not trusted from agent self-report or `references.json`.

Corpus page count: 805 → 809. Q1 2026 progress: 67 → 71 ingested, 99 → 95 remaining (58 rejected, unchanged).

### 2026-08-13 — Batch 17 (candidate list continued, papers 5-8 of 12; one reject)

- `2602.04160` — PFluxTTS: Hybrid Flow-Matching TTS with Robust Cross-Lingual Voice Cloning and Inference-Time Model Fusion. Dual-decoder (duration-guided + alignment-free) fusion for cross-lingual zero-shot cloning; `voice-conversion` considered and correctly excluded (zero-shot TTS cloning, not a dedicated VC system with VC-specific metrics). `multilingual-tts` and `subjective-evaluation` both independently re-verified legitimate. 1 figure embedded.
- `2602.04683` — UniAudio 2.0: A Unified Audio Language Model with Text-Aligned Factorized Audio Tokenization. **QC catch:** `task: [TTS, VC, SCA, codec, singing]` shipped with `related_concepts` missing `voice-conversion` and `singing` — both independently re-verified legitimate against the raw parsed source (real few-shot VC eval with WER/SIM/DNS-MOS on VCTK; real Song Generation eval with WER/AudioBox-Score against SongGen, confirmed in `raw/parsed/2602.04683/paper.md` even though not detailed in the rendered page prose) before adding the missing `related_concepts` entries and Wiki Connections bullets by hand. 2 figures embedded.
- `2602.04796` — **REJECTED.** LALM-as-a-Judge: Benchmarking Large Audio-Language Models for Safety Evaluation in Multi-Turn Spoken Dialogues. Ingest agent itself caught this before writing any page: benchmarks off-the-shelf LALMs as zero-shot safety judges outputting a scalar `[0,1]` score; Coqui XTTS-v2 used only to synthesize one injected "unsafe" turn for benchmark construction, no TTS quality metric anywhere, studied judges' own output is always a scalar score. Clean match to the FastLongSpeech (`2507.14815`) reject pattern (TTS synthesizes input, never model output) — precedent independently verified in `raw/review_queue.md` before applying. Status flipped `accepted → rejected`; logged to both `raw/review_queue.md` and `raw/pipeline_log.md`.
- `2602.05207` — ARCHI-TTS: A Flow-Matching-Based TTS Model with Self-Supervised Semantic Aligner and Accelerated Inference. `self-supervised-speech` correctly excluded despite the title's framing — the "semantic aligner" is trained end-to-end with the flow-matching objective, not built on a frozen pretrained SSL encoder. 1 figure embedded.

QC notes: `wiki/index.md` count consistent after every paper (810, [reject, no change], 811, 812). Zero callout mistakes. One real task/related_concepts mismatch caught and fixed (`2602.04683`). One corpus-scope reject, precedent-verified independently. Zero `review_flags`.

Corpus page count: 809 → 812 (net +3 across 4 candidate-list slots, one reject). Q1 2026 progress: 71 → 74 ingested, 95 → 90 remaining, 58 → 59 rejected.

### 2026-08-13 — Batch 18 (candidate list continued, papers 9-12 of 12 — completes the list)

- `2602.05443` — Wave-Trainer-Fit: Neural Vocoder with Trainable Prior and Fixed-Point Iteration towards High-Quality Speech Generation from SSL features. WavLM-feature-conditioned vocoder; `task: [TTS]` confirmed consistent with prior vocoder-paper precedent (`2601.14472`). `self-supervised-speech` independently re-verified legitimate. 1 figure embedded.
- `2602.05770` — Zero-Shot TTS With Enhanced Audio Prompts: BSc Submission For The 2026 Wildspoof Challenge TTS Track. Short challenge-submission report; `field_significance: low` correctly held with no inflation (both backbone and enhancement models used off the shelf, fine-tuned only). `subjective-evaluation` correctly excluded — all metrics (UTMOS, DNSMOS Pro, WER, SECS, F0 RMSE) are automated, no human listening test reported. No figure.
- `2602.06180` — STACodec: Semantic Token Assignment for Balancing Acoustic Fidelity and Semantic Information in Audio Codecs. Assigns externally-derived WavLM/HuBERT K-means semantic tokens directly to RVQ layer 1 (rather than an auxiliary distillation loss); `disentanglement` correctly excluded (paper explicitly contrasts itself against HASRD's disentanglement approach rather than performing disentanglement itself). `self-supervised-speech` independently re-verified legitimate. 1 figure embedded.
- `2602.07803` — SoulX-Singer: Towards High-Quality Zero-Shot Singing Voice Synthesis. `VC` task tag added by the agent beyond the raw-metadata `singing` guess (justified — a dedicated SoulX-Singer-SVC variant with its own evaluation table), independently re-verified legitimate. `subjective-evaluation` correctly excluded (SingMOS/Sheet-SSQA are automated proxies, no human MOS). Org filled in from full-text affiliations despite `organization: null` in raw metadata, addressing rather than reproducing the standing blank-Org bug pattern. TCSinger 2 (`2505.14910`, rejected) correctly excluded from citations despite being discussed by name in the paper's own Introduction. 1 figure embedded.

QC notes: `wiki/index.md` count consistent after every paper (813, 814, 815, 816). Zero callout mistakes, zero bare-wikilink issues, zero `review_flags`. This completes the original 12-paper candidate list in full (`2602.00594` through `2602.07803`, published_date 2026-01-31 through 2026-02-08), with one reject (`2602.04796`).

Corpus page count: 812 → 816. Q1 2026 progress: 74 → 78 ingested, 90 → 86 remaining (59 rejected, unchanged).

### 2026-08-13 — Batch 19 (fresh candidate list, papers 1-4 of 12 preselected)

New 12-paper chronological candidate list preselected at session start, `published_date` 2026-02-10
through 2026-02-17.

- `2602.09823` — Covo-Audio Technical Report. Unified TTS/SCA technical report; task/related_concepts cross-checked clean on first attempt (TTS → speaker-adaptation/multilingual-tts/emotion-synthesis, SCA → spoken-language-model/speech-to-speech). Two since-rejected in-corpus references (MMSU `2506.04779`, URO-Bench `2502.17810`) correctly excluded, independently re-verified against metadata status. 2 figures embedded.
- `2602.10164` — Emotion-Coherent Speech Data Augmentation and Self-Supervised Contrastive Style Training for Enhancing Kids's Story Speech Synthesis. `self-supervised-speech` and `disentanglement` both correctly excluded despite the title's "self-supervised contrastive style training" framing — the contrastive loss trains a reference encoder from scratch, not consumption of a frozen SSL representation; no explicit attribute-separation mechanism. Venue kept `arXiv` despite SLT 2024 acceptance (IEEE proceedings, no open anthology ID system) — consistent with the ICASSP/ASRU precedent. No figure (no architecture diagrams in source).
- `2506.04518` — Towards Efficient Speech-Text Jointly Decoding within One Speech Language Model. Old arXiv ID (June 2025) but `published_date` 2026-02-11 (ASRU 2025 camera-ready revision, not a full-version-dedup case — `arxiv_comment` checked, no "full version of" language). `spoken-language-model` independently re-verified legitimate (genuine external spoken question via audio encoder, real dialogue context, not a self-consuming AR TTS-LM). **QC catch:** title truncation in `papers/index.md` (cut off mid-word at "...within O") — fixed by hand. 1 figure embedded.
- `2602.10735` — Calliope: A TTS-based Narrated E-book Creator Ensuring Exact Synchronization, Privacy, and Layout Fidelity. **Session-limit interruption** on the first attempt — verified a clean "nothing written" state (no page, no assets, no index/log entries, metadata still `accepted`) before a direct retry from scratch. `field_significance: moderate/engineering-integration` correctly held with no inflation (integrates two existing TTS backends, no new architecture). No figure (engineering-integration type, not architectural-novelty).

QC notes: `wiki/index.md` count consistent after every paper (817, 818, 819, 820). One title-truncation fix (`2506.04518`), one clean interruption recovery (`2602.10735`). Zero callout mistakes, zero `review_flags`.

Corpus page count: 816 → 820. Q1 2026 progress: 78 → 82 ingested, 86 → 82 remaining (59 rejected, unchanged).

### 2026-08-13 — Batch 20 (candidate list continued, papers 5-8 of 12)

- `2602.10934` — MOSS-Audio-Tokenizer: Scaling Audio Tokenizers for Future Audio Foundation Models. Homogeneous causal-Transformer codec (CAT) jointly optimized with a semantic LLM head. `task: [codec, TTS]` both cross-checked against `related_concepts`. 1 figure embedded.
- `2602.11072` — Simultaneous Speech-to-Speech Translation Without Aligned Data (Kyutai, Hibiki-Zero). `task: [TTS]` confirmed consistent with prior S2ST-paper precedent (`2601.16023`, `2601.16618`) over the raw-metadata `SCA` guess. `subjective-evaluation` independently re-verified legitimate (20 raters/model/language). 1 figure embedded.
- `2602.11477` — SLD-L2S: Hierarchical Subspace Latent Diffusion for High-Fidelity Lip to Speech Synthesis. Non-text-input generation (silent video → speech); applied the standing vocabulary-gap precedent (`TTS` fallback tag, explicit in-page note), cross-referenced against the same-shape prior papers `interspeech-2025-1478`/`interspeech-2025-1334`. `self-supervised-speech` (frozen AV-HuBERT/X-Codec-hubert) and `subjective-evaluation` (15-participant MOS) both independently re-verified legitimate. 1 figure embedded.
- `2602.12135` — WavBench: Benchmarking Reasoning, Colloquialism, and Paralinguistics for End-to-End Spoken Dialogue Models. `subjective-evaluation` correctly excluded — scoring is entirely LLM-judge (Gemini 3 Pro Preview) with no human-correlation validation study, unlike the VStyle precedent which does report one. SCA scope confirmed (5 real end-to-end spoken dialogue models producing actual audio output, not a text-only benchmark). Two since-rejected in-corpus references (MMSU, URO-Bench) correctly excluded again. No figure (dataset/evaluation-contribution type, no proposed architecture).

QC notes: `wiki/index.md` count consistent after every paper (821, 822, 823, 824). Zero callout mistakes, zero `review_flags`. This completes the second 12-paper candidate list (`2602.09823` through `2602.15491`, published_date 2026-02-10 through 2026-02-17) except for its last 4 papers, deferred to batch 21.

Corpus page count: 820 → 824. Q1 2026 progress: 82 → 86 ingested, 82 → 78 remaining (59 rejected, unchanged).

### 2026-08-13 — Batch 21 (5-paper batch, user-requested; finishes the candidate list + 1 more)

User explicitly requested a 5-paper batch (finishing the remaining 4 of the prior 12-paper candidate
list plus the next paper chronologically) with health check plus QC between each paper, rather than
the default batches-of-4.

- `2602.13891` — GSRM: Generative Speech Reward Model for Speech RLHF (Meta Superintelligence Labs). `rlhf-speech` independently re-verified legitimate — GSRM is the actual reward/verifier driving online RLHF that measurably shifts a real speech LLM's generations, not an incidental text reward model. `subjective-evaluation` legitimate (31k expert ratings, human A/B listening tests). 2 figures embedded.
- `2602.14664` — Probing Human Articulatory Constraints in End-to-End TTS with Reverse and Mismatched Speech-Text Directions. Confirmed distinct from the unrelated already-ingested `2510.14664` before starting. Builds and trains real Tacotron-2/VITS-TTS variants with standard WER/CER/MOS evaluation — no scope flag needed (unlike the 2512.16832 analysis-paper precedent, this paper trains and evaluates actual TTS systems). `field_significance: moderate/negative-result` correctly calibrated, not inflated. `gan-vocoder` (VITS-TTS's adversarial decoder) and `subjective-evaluation` (5 real listeners, MOS + preference test) both independently re-verified legitimate. No figure.
- `2602.14686` — Disentangling Pitch and Creak for Speaker Identity Preservation in Speech Synthesis. `disentanglement` tag applied rigorously despite the literal title match — independently re-verified against a real explicit mechanism (TD-PSOLA pitch-shift data augmentation decorrelating pitch/creak) plus 3-way ablation (base-flow/adapted-flow/combined-flow, Table 1/2/Figure 3), not just the title claim. `field_significance: low` correctly held (data-centric fix on an existing published pipeline, no new architecture). No figure.
- `2602.15491` — The Equalizer: Introducing Shape-Gain Decomposition in Neural Audio Codecs. `disentanglement` correctly excluded — decomposes signal-level gain vs. shape, not speech attributes (content/speaker/prosody), so it doesn't match the concept's scope despite having an explicit mechanism and ablation evidence. Zero in-corpus references (verified against `references.json`'s reported 0, consistent). 1 figure embedded.
- `2602.17157` — CC-G2PnP: Streaming Grapheme-to-Phoneme and Prosody with Conformer-CTC for Unsegmented Languages (last paper of batch). Scope-checked explicitly before ingesting: a G2P/prosody-prediction module, but built and evaluated squarely as a TTS front-end (output feeds a downstream TTS model, central evaluation is a subjective MOS test on synthesized speech) — matches the `2510.03111` TTS-preprocessing-tooling precedent, independently re-verified as real (`ingested` status confirmed). 2 figures embedded.

QC notes: `wiki/index.md` count consistent after every paper (825, 826, 827, 828, 829). Zero callout mistakes, zero bare-wikilink issues, zero `review_flags` across all 5 papers.

Corpus page count: 824 → 829. Q1 2026 progress: 86 → 91 ingested, 78 → 74 remaining (59 rejected, unchanged). This completes the second 12-paper candidate list in full plus one additional paper. Full corpus-wide health check re-run at end of session: `[ingest] PASS (0 errors, 1170 warnings | papers_checked=829)` — warning count matches the known pre-existing baseline (unrelated to this session's work, tracked separately in BACKLOG.md).

### 2026-08-14 — Batch 1 (papers 1-4 of a fresh 12-paper candidate list)

Ingested sequentially, one at a time, with a health check plus independent manual QC pass after each:

- `2602.18104` — MeanVoiceFlow: One-step Nonparallel Voice Conversion with Mean Flows. `VC` task tag verified against real reported metrics (MOS, SMOS, CER, SPK-SIM). Agent self-caught and corrected a factual error in its own draft: the paper's "FastVoiceGrad+" Table 2 baseline is built from a different in-corpus paper (Vocoder-Projected Feature Discriminator, `interspeech-2025-1763`) than initially assumed (FasterVoiceGrad, `interspeech-2025-1747`) — reworded the Wiki Connections bullet to avoid mischaracterizing it. 1 figure embedded.
- `2602.19574` — CTC-TTS: LLM-based dual-streaming text-to-speech with CTC alignment. AR codec-token-LM streaming TTS. `spoken-language-model` correctly excluded (self-generated-output AR TTS, no external speech signal consumed) per the standing rule. Found and wikilinked 3 in-corpus baselines the automated reference-matcher missed due to ID-format mismatches (LLMVoX `2025.findings-acl.1051`, ELLA-V `2401.07333`, WavTokenizer `2408.16532`). 2 figures embedded.
- `2602.23068` — TADA: A Generative Framework for Speech Modeling via Text-Acoustic Dual Alignment (Hume AI). `field_significance: high`; `[!tip] High significance` callout correctly present (confirmed convention: elevated levels get the `[!tip]` wrapper, moderate/low are plain prose). `spoken-language-model` tag independently re-verified legitimate — evaluated against Spirit-LM/TWIST on real external-speech story-cloze benchmarks (sSC/tSC), not self-generated audio, satisfying the external-signal rule. 2 figures embedded.
- `2602.23266` — Discourse-Aware Dual-Track Streaming Response for Low-Latency Spoken Dialogue Systems (DDTSR). Cascaded ASR/LLM/TTS spoken-dialogue-latency system; `speech-to-speech` dialogue sub-paradigm confirmed. Includes an honest `[!warning]` in Limitations: quality preservation is assessed only via automated proxies (G-Eval, UTMOSv2), no human listening test reported.

QC notes: `wiki/index.md` count consistent after every paper (830, 831, 832, 833). Zero callout mistakes, zero bare-wikilink issues (all Wiki Connections used piped `[[id|Name]]` correctly after one self-correction on the first paper), zero `review_flags`.

Corpus page count: 829 → 833. Q1 2026 progress: 91 → 95 ingested, 74 → 70 remaining (59 rejected, unchanged).

### 2026-08-14 — Batch 2 (papers 5-8 of the candidate list) — 2 scope rejects, 1 narrowly-scoped accept

This batch surfaced three consecutive corpus-scope boundary cases, all caught by the ingest agent
before writing any page and each resolved via `AskUserQuestion`/direct precedent match rather than
guessed. Full detail in `raw/review_queue.md`; summarized here:

- `2602.23333` — SemanticVocoder: Bridging Audio Generation and Audio Understanding via Semantic Latents. **Rejected.** A genuinely generative system, but of general (non-speech) audio: trained on AudioSet, evaluated on AudioCaps/Clotho/HEAR sound-event benchmarks, baselines all general-TTA systems (EzAudio, AudioLDM2, TangoFlux, StableAudio). Zero speech/speaker/prosody content anywhere; filter's `[TTS, codec]` tag was a keyword false positive (TTA vs. TTS, generic "vocoder" match). New scope-failure shape, distinct from the FAMA/MLC-SLM understanding-wearing-generative-framing pattern — this is genuinely generative, just not of speech. User confirmed reject via `AskUserQuestion`.
- `2602.23765` — DashengTokenizer: One layer is enough for unified audio understanding and generation. **Accepted, narrowly scoped.** A tri-domain (speech/music/environmental-sound) audio tokenizer whose own generative demos (TTA, TTM, speech enhancement) are all non-speech-synthesis — but it runs a genuine SEED-TTS speech-reconstruction benchmark directly against in-corpus TTS codecs (Mimi, XCodec 2.0, SNAC, XY-Tokenizer). User confirmed accept via `AskUserQuestion`, on the reasoning that codec-reconstruction fidelity is genuine neural-codec subject matter even without a TTS/VC generation component. Re-ingested with an explicit scope instruction: `task: [codec]` only (no TTS/VC), `related_concepts: [neural-codec, self-supervised-speech, evaluation-metrics]` only (no TTS-architecture concepts), Claims limited to the SEED-TTS/X-ARES speech-relevant results (TTA/TTM results mentioned in Context only, not as claims). Establishes a precedent: tri-domain/general-audio papers can be accepted narrowly when they include a genuine, directly-comparable speech-codec evaluation, even with zero TTS/VC generation of their own. 1 figure embedded.
- `2603.00958` — S-VoCAL: A Dataset and Evaluation Framework for Inferring Speaking Voice Character Attributes in Literature. **Rejected**, applied directly without a separate user ask (unambiguous case, following established precedent-match practice). Entire pipeline is text-in/text-out: novel text + Wikidata ground truth → RAG (E5-large + Qwen3-8B/Phi-4-14B) predicting 8 categorical character attributes. No audio produced, consumed, or evaluated anywhere; filter's `[TTS, evaluation]` tag was a false positive from TTS-motivation language in the abstract. Cleaner reject than the FAMA/MLC-SLM/2510.12116 precedents it matches, since even the *inputs* are text, not audio.
- `2603.01467` — Conversational Speech Naturalness Predictor (Meta). **Ingested**, confirmed in scope. Trains a dual-channel MOS-style predictor against real human naturalness ratings (≥5 raters/recording) for synthesized (ConvTTS) and full-duplex-agent (FDX-Conv) conversational speech; shows existing single-utterance predictors (NISQA, UTMOSv2) correlate poorly or negatively on this task. Same shape as other automated-MOS-predictor papers already in-corpus (e.g. UTMOS). `metrics: []` (paper reports PCC/SRC/MSE correlation values, not canonical MOS-style values, described in prose per the `2005.07143` precedent). `subjective-evaluation` included (real human-rater data collected and validated against). No figure.

QC notes: `wiki/index.md` count consistent after every ingested paper (834, 835). Zero callout mistakes, zero bare-wikilink issues, zero `review_flags` on the 2 ingested papers.

Corpus page count: 833 → 835 (2 ingested, 2 rejected). Q1 2026 progress: 95 → 97 ingested, 70 → 66 remaining, 59 → 61 rejected.

### 2026-08-14 — Batch 3 (papers 9-12, final batch of the candidate list) — 1 reject, 1 session-limit interruption, 1 retroactive scope flag

- `2603.01476` — Entropy-Guided GRVQ for Ultra-Low Bitrate Neural Speech Codec (Waseda/NTT). Straightforward speech-scoped codec (LibriTTS+VCTK, PESQ/STOI/ViSQOL/SDR + 8-participant MUSHRA). Clean ingest, 0 issues.
- `2603.01592` — TQCodec: Towards neural audio codec for high-fidelity music streaming. **Rejected**, applied directly without a separate user ask (unambiguous case). Trains and evaluates exclusively on music datasets (MusDBHQ, Jamendo, private corpus), LSD/SNR metrics only, no speech-domain data or speech-codec comparison anywhere. Clean match to the MIDI-VALLE/SemanticVocoder reject shape; does not meet the DashengTokenizer narrow-accept bar (no speech-reconstruction benchmark against in-corpus codecs).
- `2603.02022` — CodecFlow: Efficient Bandwidth Extension via Conditional Flow Matching in Neural Codec Latent Space. Confirmed speech-scoped (LibriTTS/VCTK/TIMIT, no music data). Correctly excluded `subjective-evaluation` — the paper's one MOS-labeled value is NISQA-predicted (automated proxy), not real listener ratings.
- `2603.04145` — VietNormalizer: Vietnamese TTS text-normalization library. **Session-limit interruption on first attempt** — verified clean (no page/assets/index/log/metadata changes, `status` still `accepted`) before a safe direct retry. On retry, the ingest agent identified a genuine scope-boundary case (explicit TTS-pipeline framing throughout, but zero quantitative results of any kind — no accuracy, latency, or downstream TTS evaluation, only a qualitative feature-comparison table) but **wrote the page directly instead of stopping to flag first**, a deviation from the explicit instruction given. Caught during independent verification; surfaced via `AskUserQuestion` after the fact. User confirmed **keep** — TTS-pipeline framing plus open-source code judged genuine infrastructure value even without benchmarks, though this is a materially weaker empirical case than the `2510.03111` precedent it invoked (which had real signal-quality metrics across 24 configurations). Logged as a new precedent in `raw/review_queue.md`, explicitly not a blanket exception for future zero-metric papers — re-evaluate each on its own framing strength. `related_concepts: []` (no controlled-vocabulary concept covers TTS text-frontend normalization tooling).

QC notes: `wiki/index.md` count consistent after every ingested paper (836, 837, 838). A corpus-wide health-check re-run at end of session caught 7 bare-wikilink warnings on `2602.23068` (TADA, from batch 1) that had slipped past the earlier per-paper QC pass — fixed by hand (piped `[[id|Name]]` format).

Corpus page count: 835 → 838 (3 ingested, 1 rejected). Q1 2026 progress: 97 → 100 ingested, 66 → 62 remaining, 61 → 62 rejected. This completes the 12-paper candidate list in full. Full corpus-wide health check re-run at end of session: `[ingest] PASS (0 errors, 1170 warnings | papers_checked=838)` — warning count matches the known pre-existing baseline exactly, confirming no new warnings survived across the whole session's 9 ingested papers.

### 2026-08-15 — Batch 1 (papers 1-4 of a fresh 12-paper candidate list)

Ingested sequentially, one at a time, with an independent per-paper health check after each:

- `2603.04219` — ZeSTA: Zero-Shot TTS Augmentation with Domain-Conditioned Training for Data-Efficient Personalized Speech Synthesis. Fine-tunes a VITS-based personalized TTS model on zero-shot-TTS-synthesized augmentation data (Fish-Speech, CosyVoice 2) plus real-data oversampling; base architecture unchanged, so `field_significance.type: engineering-integration` (no figure copied). Health check: 0 errors, 1 informational warning (expected bare-wikilink case, cited paper has no distinctive system name).
- `2603.05299` — WavSLM: Single-Stream Speech Language Modeling via WavLM Distillation. Distills WavLM's upper transformer layers into a causal, single-codebook autoregressive next-chunk predictor on the existing FocalCodec-Stream tokenizer, speech-only training. `field_significance: moderate / architectural-novelty`, 1 figure embedded. Health check: 0 errors, 0 warnings.
- `2603.05373` — Hierarchical Decoding for Discrete Speech Synthesis with Multi-Resolution Spoof Detection (MSpoof-TTS, NUS). Training-free, inference-time framework using multi-resolution spoof detectors to guide autoregressive codec-token decoding of a frozen NeuTTS backbone. `field_significance: moderate / architectural-novelty`, 1 figure embedded. Health check: 0 errors, 0 warnings.
- `2603.05413` — Building Enterprise Realtime Voice Agents from Scratch: A Technical Tutorial (Salesforce AI Research). Judgment call: not pure survey despite a 25+ model / 30+ framework landscape section, since it also contributes original empirical latency benchmarking (own instrumented runs of Qwen2.5-Omni/Qwen3-Omni across 3 deployment configs) and a tested cascaded pipeline — used standard template, not survey handling. `field_significance.type: [engineering-integration, empirical-benchmark, conceptual-contribution]`, no novel architecture (`architecture: []`). Paper's own `references.json` in_corpus flags were unreliable (2/12 correctly flagged); all 12 arXiv references manually cross-checked against the index, 8 selected for Wiki Connections. Health check: 0 errors, 0 warnings.

QC notes: `wiki/index.md` count consistent after every paper (839, 840, 841, 842), verified independently against `grep -c '^| \[\[' papers/index.md` each time. Zero `review_flags` across all 4 papers.

Corpus page count: 838 → 842. Q1 2026 progress: 100 → 104 ingested, 62 → 58 remaining (62 rejected, unchanged). Full corpus-wide health check re-run at batch close: `[ingest] PASS (0 errors, 1171 warnings | papers_checked=842)` — warning count is baseline (1170) + 1 (the expected `2603.04219` informational warning), confirming no new issues.

### 2026-08-15 — Batch 2 (papers 5-8 of the candidate list)

Ingested sequentially, one at a time, with an independent per-paper health check after each:

- `2603.05887` — Reconstruct! Don't Encode: Self-Supervised Representation Reconstruction Loss for High-Intelligibility and Low-Latency Streaming Neural Audio Codec (JHU/USC). Proposes JHCodec (causal Transformer RVQ-VAE streaming codec on TS3-Codec) plus the SSRR loss (reconstructing distilled W2V-BERT 2.0 features from the codec's *decoded* output, not just the encoder as in Mimi's SED); halves WER at matched early training steps. `field_significance: moderate / architectural-novelty`, 1 figure embedded. Health check: 0 errors, 0 warnings.
- `2603.05977` — Activation Steering for Accent-Neutralized Zero-Shot Text-To-Speech (UT Dallas/CRSS). Post-hoc, training-free activation-steering method for Qwen3-TTS that neutralizes accent while preserving speaker timbre, extending the in-corpus activation-steering family (EmoSteer-TTS, TruS, EmoShift) to a new attribute. `field_significance: moderate / architectural-novelty` (narrow scope: one accent pair, one base model). 1 figure embedded. Health check: 0 errors, 0 warnings.
- `2603.06079` — StreamVoiceAnon+: Emotion-Preserving Streaming Speaker Anonymization via Frame-Level Acoustic Distillation. Fixes emotion degradation in streaming neural-codec speaker anonymization via restructured same-speaker neutral/emotional training pairs plus frame-level emotion distillation, 49.2% UAR vs. 39.7% baseline at zero inference-latency cost. `field_significance: moderate / architectural-novelty`, 1 figure embedded. Health check: 0 errors, 0 warnings. **Index count drift caught after this paper**: `wiki/index.md` line 65 prose sentence stayed at 844 while the callout and Browse-link occurrences correctly advanced to 845 — fixed by hand, another instance of the known single-edit-leaves-occurrences-inconsistent pattern.
- `2603.06444` — Prosodic Boundary-Aware Streaming Generation for LLM-Based TTS with Streaming Text Input. Post-training strategy for LLM-based TTS (CosyVoice2 base) inserting a learned prosodic-boundary marker via WhisperX weak alignment plus a bounded sliding-window inference prompt, avoiding the catastrophic long-form collapse (WER 70.97% → 4.77%) seen in interleaved streaming baselines. `field_significance: moderate / architectural-novelty` (single base architecture, author-constructed long-form benchmark). 1 figure embedded. Health check: 0 errors, 0 warnings; all 3 count occurrences already consistent at 846.

QC notes: zero `review_flags` across all 4 papers. One index-count-drift instance caught and fixed (see above); all other counts self-consistent at every step.

Corpus page count: 842 → 846. Q1 2026 progress: 104 → 108 ingested, 58 → 54 remaining (62 rejected, unchanged). Full corpus-wide health check re-run at batch close: `[ingest] PASS (0 errors, 1171 warnings | papers_checked=846)` — warning count unchanged from batch 1 close, confirming no new issues across this batch's 4 papers.

### 2026-08-15 — Batch 3 (papers 9-12, final batch of the candidate list) — 1 session-limit interruption with partial write, 2 index-count-drift catches

- `2603.07513` — Bolbosh: Script-Aware Flow Matching for Kashmiri Text-to-Speech (KAUST / University of Kashmir / Gaash Lab, NIT Srinagar). Cross-lingual fine-tune of a pretrained English Matcha-TTS (OT-CFM) checkpoint with an expanded 272-grapheme vocabulary preserving Perso-Arabic diacritics; first open Kashmiri TTS system, corpus, and benchmark. `field_significance: moderate / engineering-integration, dataset-contribution`. Zero in-corpus references found. No figure (no architectural novelty). Health check: 0 errors, 0 warnings.
- `2603.07534` — Accent Vector: Controllable Accent Manipulation for Multilingual TTS Without Accented Data (USC). **Session-limit interruption with a partial write** — the agent was cut off after writing a fully complete paper page (all sections, generation block finished) but before touching the metadata status, `papers/index.md`, `index.md`, or `log.md`. Verified this was a clean partial (not a corrupted mid-write) by reading the full page end-to-end, then completed the remaining steps by hand: added the index row (title truncated to 55 chars per the skill script's actual `title[:55]` behavior, matching existing convention), bumped `index.md` count (847→848) after also fixing that file's 3 occurrences which had drifted to two different stale values, added the `log.md` entry, set metadata `status: ingested` + `generation_history`, and fixed 5 bare-wikilink warnings the interrupted agent had left in Wiki Connections. Verified all 5 `related_papers` IDs resolve in the index before finishing. Health check: 0 errors, 0 warnings after the fix.
- `2603.07550` — Learning-free L2-Accented Speech Generation using Phonological Rules (USC). Learning-free rule pipeline extending the authors' own prior US-UK phonological accent rules (`2601.14417`) to cross-lingual Spanish/Indian accents over a frozen pretrained TTS model. `field_significance` type excludes architectural-novelty (no figure). Agent self-caught and fixed a 3-way `index.md` count inconsistency (848/848/839) before reporting. Health check: 0 errors, 0 warnings.
- `2603.07551` — Targeted Speaker Poisoning Framework in Zero-Shot Text-to-Speech (USC). **Scope-checked before ingest**: formalizes Speech Generation Speaker Poisoning (SGSP), a privacy/machine-unlearning framing that modifies a trained zero-shot StyleTTS2 model to prevent reproduction of specific forgotten speaker identities while preserving utility for retained ones (adapts Teacher-Guided Poisoning from `2507.20140` to a new backbone, adds a novel Encoder-Guided variant). Confirmed in-scope directly (not deferred to `AskUserQuestion`) since it directly manipulates and evaluates a zero-shot TTS generation model on TTS-relevant metrics (WER utility, AUC/Forget-Speaker-Similarity privacy) rather than attacking an external system — distinct shape from the ASR-false-accept precedents. `field_significance: moderate / conceptual-contribution, evaluation-contribution, engineering-integration`, no figure. Health check on the paper itself: 0 errors, 0 warnings — but caught a fresh 3-way `index.md` count drift afterward (849/849/840 vs. actual 850), fixed by hand.

QC notes: zero `review_flags` across all 4 papers. Two independent index-count-drift instances this batch (one self-caught by the ingest agent on `2603.07550`, one caught by the session's own post-hoc verification on `2603.07551`) plus the `2603.07534` partial-write recovery — the drift pattern and the session-limit-interruption pattern are now both recurring reliably enough to treat independent verification after every single paper (not just at batch close) as mandatory, not optional.

Corpus page count: 846 → 850. Q1 2026 progress: 108 → 112 ingested, 54 → 50 remaining (62 rejected, unchanged). This completes the 12-paper candidate list in full. Full corpus-wide health check re-run at batch close: `[ingest] PASS (0 errors, 1171 warnings | papers_checked=850)` — warning count unchanged from batch 1/2 close, confirming no new issues across the whole session's 12 ingested papers.

### 2026-08-15 — Batch 1 of a fresh 12-paper session (papers 1-4)

Ingested sequentially, one at a time, with an independent per-paper health check after each:

- `2603.07599` — StyleBench: Evaluating Speech Language Models on Conversational Speaking Style Control. Pure-evaluation benchmark paper (no proposed model), evaluating 10 open-source speech/omni LMs on multi-turn conversational speaking-style intensity control (emotion, speed, volume, pitch). `field_significance: moderate / dataset-contribution, evaluation-contribution, empirical-benchmark`; `architecture/conditioning/training: []` per the established pure-evaluation-paper convention (precedent: `2511.10262` MTR-DuplexBench). No figure. Health check: 0 errors, 0 warnings.
- `2603.08216` — DualTurn: Learning Turn-Taking from Dual-Channel Generative Speech Pretraining. Dual-channel generative pretraining (Qwen2.5-0.5B over frozen Mimi codec embeddings) as unsupervised representation learning, fine-tuned into 12 lightweight turn-taking classification heads; beats VAP (wF1 0.633 vs 0.389) and a 3.1B audio-text baseline (AUC 0.930 vs 0.880) with ablations isolating the pretraining objective (not backbone capacity) as the source of the gain. `field_significance: high / architectural-novelty, empirical-benchmark`, 1 figure embedded. Health check: 0 errors, 0 warnings.
- `2603.08574` — Scalable Neural Vocoder from Range-Null Space Decomposition (RNDVoC). GAN vocoder decomposing spectrogram reconstruction into a closed-form linear range-space projection plus a learned null-space residual, with a dual-path sub-band architecture and mel-configuration-agnostic inference (no retraining needed for new mel configs). `field_significance: high / architectural-novelty, conceptual-contribution`, 1 figure embedded. Organization (Chinese Academy of Sciences, Tencent AI Lab) filled in from the PDF text since `raw/metadata` had it null; metadata JSON itself left untouched (pipeline-state fields only) per the never-alter-source invariant. Health check: 0 errors, 0 warnings.
- `2603.08977` — Universal Speech Content Factorization (USCF, JHU). Extends closed-set SCF voice conversion to an open-set/zero-shot setting via a speaker-agnostic linear content mapping (fit once by least-squares/SVD) plus a per-speaker transformation recoverable in closed form from a few seconds of unseen-speaker speech; no gradient-based training required beyond the pretrained WavLM encoder/vocoder. `disentanglement` tag independently re-verified as a genuine explicit factorization mechanism (SVD-based content/speaker separation is the entire method), not an implicit-by-construction case. 1 figure embedded. Health check: 0 errors, 0 warnings.

QC notes: `wiki/index.md` 3-way count drift caught and fixed on **every one of the 4 papers this batch** (851/852/853/854, each time at least one of the three occurrences was stale or an agent-reported wrong value) — independent verification after every paper continues to be necessary, not optional. Zero `review_flags` across all 4 papers.

Corpus page count: 850 → 854. Q1 2026 progress: 112 → 116 ingested, 50 → 46 remaining (62 rejected, unchanged). Full corpus-wide health check re-run at batch close: `[ingest] PASS (0 errors, 1171 warnings | papers_checked=854)` — warning count unchanged from prior session's baseline, confirming no new issues.

### 2026-08-15 — Batch 2 (papers 5-8) — 1 clean session-limit interruption

Ingested sequentially, one at a time, with an independent per-paper health check after each:

- `2603.09120` — Emotion-Aware Prefix: Towards Explicit Emotion Control in Voice Conversion Models. Extends the VEVO two-stage zero-shot VC backbone with an Emotion-Aware Prefix (Temporal-Shuffle Transformer + Perceiver + Emotion Fusion Layer over Emotion2Vec+) injected via Deep-Prefix Prompting (P-Tuning-v2-style KV-cache injection); nearly doubles Emotion Conversion Accuracy (42.40% → 85.50%) on ESD while preserving speaker/content/quality. Stage-isolation and cross-architecture (GenVC) experiments show emotion control is driven by the sequence-modulation stage. `field_significance: moderate / architectural-novelty, conceptual-contribution`, 1 figure embedded. Health check: 0 errors, 0 warnings.
- `2603.09180` — DuplexCascade: Full-Duplex Speech-to-Speech Dialogue with VAD-Free Cascaded ASR-LLM-TTS Pipeline and Micro-Turn Optimization. VAD-free cascaded pipeline converting long turns into chunk-wise micro-turns with dedicated control tokens, LoRA-trained on synthetically-augmented text-only UltraChat dialogues; SOTA turn-taking accuracy on Full-Duplex-Bench, near-parity VoiceBench conversational-intelligence vs. a naive cascade. `field_significance: moderate / architectural-novelty, empirical-benchmark`, 1 figure embedded. Health check: 0 errors, 0 warnings.
- `2603.09627` — Speech-Omni-Lite: Portable Speech Interfaces for Vision-Language Models. **Session-limit interruption on first attempt** — verified clean (no page, no assets, no index/log/metadata changes, `status` still `accepted`) before a safe direct retry. Adds lightweight speech-projector and speech-token-generator adapters to a fully frozen Qwen3-VL-8B backbone, trained partly on a novel LLM-manufactured QTATS spoken-QA dataset built from ASR corpora. `field_significance: moderate / engineering-integration, dataset-contribution`, no figure. Health check: 0 errors, 0 warnings.
- `2603.10371` — Speech Codec Probing from Semantic and Phonetic Perspectives (USC / Dolby Laboratories). Empirical probing study (no new codec proposed) showing four widely-used speech codecs (EnCodec, DAC, MIMI, MIMO) primarily encode phonetic rather than lexical-semantic structure in their "semantic" tokens, via word-pair distance probing, articulatory (rt-MRI) correlation, and cross-modal CKA alignment. `field_significance: moderate / empirical-benchmark, conceptual-contribution, negative-result` (verified `negative-result` is valid controlled vocabulary per `docs/schemas/vocabulary.md`), no figure. Health check: 0 errors, 0 warnings.

QC notes: `wiki/index.md` 3-way count drift caught and fixed on 3 of the 4 papers (855, 857 — corrected from an agent-reported wrong "847" — and 858 all needed manual fixes; only 856 on `2603.09180` was self-consistent). Zero `review_flags` across all 4 papers.

Corpus page count: 854 → 858. Q1 2026 progress: 116 → 120 ingested, 46 → 42 remaining (62 rejected, unchanged). Full corpus-wide health check re-run at batch close: `[ingest] PASS (0 errors, 1171 warnings | papers_checked=858)` — warning count unchanged from baseline.

### 2026-08-15 — Batch 3 (papers 9-12, final batch of the candidate list)

Before this batch, sanity-checked `2603.16924` (SimulU, paper 10): its arXiv ID prefix (16xxx) looked out of sequence against neighboring papers' IDs (07xxx-11xxx) despite all sharing March 8-12 `published_date`s. Confirmed this is normal — arXiv submission numbers are global across all categories (~3,000/day), not per-category, so the jump is consistent with 3 days of full-arXiv volume; no `arxiv_comment` flag either. Proceeded without an `AskUserQuestion`.

Ingested sequentially, one at a time, with an independent per-paper health check after each:

- `2603.10904` — When Fine-Tuning Fails and when it Generalises: Role of Data Diversity and Mixed Training in LLM-based TTS (Sprinklr AI). Empirical LoRA fine-tuning study on the Qwen2.5-0.5B backbone of an AR codec TTS system (NeuTTS); finds training-data acoustic diversity (not dataset size or loss convergence) predicts whether fine-tuning improves or degrades DNS-MOS, documents a loss-quality divergence phenomenon. `field_significance: moderate / empirical-benchmark, negative-result`, no figure. Health check: 0 errors, 0 warnings.
- `2603.16924` — SimulU: Training-free Policy for Long-form Simultaneous Speech-to-Speech Translation. Training-free inference-time policy repurposing SeamlessM4T's internal cross-attention for long-form simultaneous S2S translation without retraining. `field_significance: moderate / architectural-novelty`, 1 figure (correctly selected the true architecture-overview figure over a stray author-affiliation icon mislabeled as figure-1). Caught and fixed 5 bare-wikilink warnings in Wiki Connections that the ingest agent's own reported "0 warnings" claim didn't match — independent health check found them. Health check after fix: 0 errors, 0 warnings.
- `2603.11678` — RAF: Relativistic Adversarial Feedback For Universal Speech Synthesis (KAIST). GAN vocoder training objective pairing SSL-derived (WavLM/HuBERT) quality-gap estimation with relativistic discriminator feedback; notable parameter-efficiency result (14M-param BigVGAN-base+RAF beats 112M-param BigVGAN+LSGAN). `field_significance: moderate / architectural-novelty`, 1 figure embedded, zero in-corpus references. Health check: 0 errors, 0 warnings.
- `2603.11683` — Causal Prosody Mediation for Text-to-Speech: Counterfactual Training of Duration, Pitch, and Energy in FastSpeech2. Augments FastSpeech2 with a structural causal model (emotion→prosody→speech) and two counterfactual training losses (IPC, CPC) keeping emotion's effect routed entirely through duration/pitch/energy. `field_significance` not explicitly reported in agent summary but confirmed via health check; 1 figure (SCM diagram), zero in-corpus references. Health check: 0 errors, 0 warnings.

QC notes: `wiki/index.md` 3-way count drift caught and fixed on 2 of the 4 papers (860 on `2603.16924`, 861 on `2603.11678` — both had agent-reported values off by exactly 10, a new variant of the drift pattern); `2603.10904` and `2603.11683` were self-consistent. Zero `review_flags` across all 4 papers. One instance of an agent's self-reported "0 warnings" being wrong, caught only by the independent post-hoc health check (`2603.16924`) — reinforces that agent self-reports on warnings, not just error counts, need independent verification.

Corpus page count: 858 → 862. Q1 2026 progress: 120 → 124 ingested, 42 → 38 remaining (62 rejected, unchanged). This completes the 12-paper candidate list in full. Full corpus-wide health check re-run at batch close: `[ingest] PASS (0 errors, 1171 warnings | papers_checked=862)` — warning count unchanged from baseline across the whole session's 12 ingested papers.

### 2026-08-15 — Mini-batch (2 papers, appended to close out the day)

- `2603.11947` — Resurfacing Paralinguistic Awareness in Large Audio Language Models (Monash University / UCL). Five layer-wise probing analyses on Qwen2.5-Omni and Kimi-Audio localizing paralinguistic signal (layers 0-6) vs. semantic understanding (layers 7-14); proposes paralinguistic-enhanced fine-tuning (PE-FT, selective-layer LoRA + auxiliary dual-level classification head), two new LLM-judged metrics (PA-score, PA-rate), and a child-safety evaluation dataset showing a 7-8% → 97-99% appropriate-response-rate fix. `field_significance: moderate`, no figure. Citation-integrity check applied correctly: 2 of 4 cited in-corpus papers were `status: rejected` and excluded from `related_papers`/Wiki Connections per the citation-integrity rule. Health check: 0 errors, 0 warnings.
- `2603.12342` — MamTra: A Hybrid Mamba-Transformer Backbone for Speech Synthesis (KAIST / Chung-Ang University). Converts a pretrained CosyVoice 2 attention backbone into a hybrid Mamba-Transformer via structural weight transfer (Q/K/V → Mamba C/B/x projections) plus multi-level distillation (CE + logit-KL + embedding MSE); cuts inference memory up to 34% with only 0.25% absolute WER increase, using under 2% of original training data. `field_significance: moderate / architectural-novelty, empirical-benchmark`, 1 figure embedded. Health check: 0 errors, 0 warnings.

QC notes: `wiki/index.md` 3-way count drift caught and fixed on `2603.11947` (agent-reported "853" vs. correct 863, off by 10 again); `2603.12342` was self-consistent at 864. Zero `review_flags` on both papers.

Corpus page count: 862 → 864. Q1 2026 progress: 124 → 126 ingested, 38 → 36 remaining (62 rejected, unchanged). Full corpus-wide health check re-run at close: `[ingest] PASS (0 errors, 1171 warnings | papers_checked=864)` — warning count unchanged from baseline.

**Day total (both sessions + this mini-batch): 26 papers ingested 2026-08-15.**

---

## Manual Verification Queue

Papers where the ingest agent emitted `review_flags` in its INGEST_RESULT signal. Review these
after the session batch is complete — check the paper page and resolve each flag by hand.

| Paper ID | Flag | Agent note |
|----------|------|------------|
| `2602.11172` | `field_significance` | Single-author closed-model (Gemini 2.5 TTS) case study with no reported evaluator count/qualifications and no non-Gemini baseline; level (`low`) could plausibly be argued lower still if the human-evaluation claims are discounted entirely. |

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
    if y == '2026' and mo in ('01','02','03'):
        if m['status'] == 'accepted': accepted += 1
        if m['status'] == 'ingested': ingested += 1
        if m['status'] == 'rejected': rejected += 1
print(f'Ingested: {ingested} | Remaining: {accepted} | Rejected: {rejected}')
"
```

---

## Commit / Push Workflow

Not every batch needs a commit — batch within a session freely, commit at natural stopping
points or when explicitly asked. When committing:

1. Content repo: stage new paper pages + assets + `index.md`/`log.md`/`papers/index.md`, commit, push.
2. Infra repo: stage `raw/metadata/*.json` status updates + this session log (and `BACKLOG.md` if
   its Q1 progress line has gone stale), commit; then bump the `wiki/` submodule pointer to the
   new content commit (checkout `main` in `wiki/`, `git pull`, commit the pointer bump in infra), push.
3. Site repo: bump the `content` submodule pointer, commit, push — **ask before this step**
   (though a durable standing instruction to always bump satisfies this too — check for one
   before asking), it triggers a live deploy. Push order is always content → infra → site, since
   site's submodule reference only resolves once content is on GitHub.

Parallel-worktree note: if ingest and integrate/render streams are running concurrently (see
[[project_parallel_worktrees]]), check `git log HEAD..origin/main` and `git status` on the trunk
checkout before merging `work/ingest` into `main` — another stream may have already landed
unpushed commits directly on `main`. Expect a single mechanical `log.md` conflict if both streams
appended to the same date section; resolve by keeping both entry blocks. After merging and
pushing, fast-forward the `work/ingest` worktree branch back to `main` in both repos.

---

Always edit and commit from the **standalone content repo**
(`/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content`), never
via `infra/wiki/` or `site/content/` submodule paths directly — both are detached-HEAD checkouts
of specific commits, and committing there orphans the work. See [[project_repo_structure]] for
the three-repo layout and [[feedback_site_submodule_bump]] for the submodule-bump specifics
(use `git branch` not `git submodule status` to verify branch state). Commit messages: no
`Co-Authored-By` trailers, no session-number prefix — describe what changed, not when (see
[[feedback_commit_messages]]). Wiki prose: avoid em dashes, use comma/colon/parentheses instead
(see [[feedback_em_dashes]]).
