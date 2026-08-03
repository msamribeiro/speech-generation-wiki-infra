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

All 16 papers from the original preselected chronological candidate list (built 2026-08-03,
`published_date` 2026-01-01 through 2026-01-13) are now ingested: `2601.00217`, `2601.00303`,
`2601.01459`, `2601.01568`, `2601.04233`, `2601.02073`, `2601.02753`, `2601.02776`, `2601.03170`,
`2601.03632`, `2601.03892`, `2601.05329`, `2601.05554`, `2601.05564`, `2505.15727`, `2601.08450`.

To start the next session: re-run the progress-count script first to confirm current counts (159
was the count at bootstrap; 143 remained as of the end of this session, but fetch/filter may have
added more since), then build a fresh chronological candidate list of the next batch(es) starting
from the earliest remaining Q1 2026 `accepted` paper by `published_date`.

**Mandatory before every paper page:** run `grep -n "!tip\]\|!abstract\]\|!important\]"` against
the drafted page and confirm the abstract callout is `[!abstract]` before running the health check.
This mistake (writing `[!tip]` or `[!important]` on the abstract card instead of the Field
Significance callout, reusing the significance-level token) recurred 7 times across this session's
4 batches. A written reminder alone was not sufficient to stop it (it recurred even after being
noted 3 separate times); the mechanical grep check adopted at the end of batch 3 caught it reliably
for the rest of the session (2 more catches in batch 4, both pre-emptive) — keep using the grep
check every time, it is now the confirmed working mitigation, not just a suggestion.

Also check `arxiv_comment` for a named future-conference acceptance (e.g. "ACL 2026", "accepted for
ICASSP 2026") before setting `venue`/`venue_type` — keep `venue: arXiv` / `venue_type: preprint`
until the paper has an actual venue-specific ID, per precedent (`2510.14664`, confirmed again with
`2601.03632` and `2601.03892` in batch 3; no recurrence in batch 4).

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

---

## Manual Verification Queue

Papers where the ingest agent emitted `review_flags` in its INGEST_RESULT signal. Review these
after the session batch is complete — check the paper page and resolve each flag by hand.

| Paper ID | Flag | Agent note |
|----------|------|------------|
| _(none yet)_ | | |

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
