# Q3 2026 Ingest Session

**Date:** 2026-11-01
**Goal:** Ingest all accepted Q3 2026 (July to September 2026) papers into the wiki.

Bootstrapped from `docs/records/2026-11-01-q2-2026-ingestion-sessions.md`, which holds the full
session-by-session Q2 2026 log (sweep closed 2026-10-31). This file carries forward the scope
precedents and gaps without the historical narrative. The procedure (cadence, per-paper cleanup and
QC, commit workflow) is canonical in `docs/ingest-protocol.md`.

---

## Scope

By canonical `published_date` (2026-07-01 to 2026-09-30) as of 2026-11-07:

| Month | Accepted | Ingested | Rejected | Total |
|-------|----------|----------|----------|-------|
| July 2026 | 69 | 0 | 38 | 107 |
| August 2026 | 50 | 0 | 8 | 58 |
| September 2026 | 245 | 34 | 183 | 462 |
| **Total** | **364** | **34** | **229** | **627** |

September is mostly Interspeech 2026 (proceedings date 2026-09-27, first conference day). The 34
ingested pages are arXiv records re-dated to the proceedings date (32 on 2026-10-26, 2 on
2026-11-01). Rejections include the 109 ISCA records and 13 arXiv preprints marked as duplicates.

Accepted papers by source, and download/parse status (every accepted Q3 record now has a PDF):

| Source | Accepted | Parsed | PDF, not parsed |
|--------|---------:|-------:|----------------:|
| Interspeech 2026, ISCA records | 70 | 13 | 57 |
| Interspeech 2026, arXiv records (re-dated) | 65 | 65 | 0 |
| arXiv | 191 | 168 | 23 |
| ACL 2026 | 27 | 27 | 0 |
| Workshops | 9 | 9 | 0 |
| ICML 2026 | 2 | 2 | 0 |
| **Total** | **364** | **284** | **80** |

Not yet in scope: the two Q2-held papers `2606.12940` (ICML 2026) and `2606.13006` (IJCAI 2026),
which move to Q3 under the peer-reviewed-version rule. Q2 also gained one accepted paper on
2026-11-07, `2608.26146` (Vagdhenu, PDF downloaded, not parsed), when its real v1 date (28 Jun 2026)
replaced the fetch-time version date.

**Fetch coverage gaps (pre-flight):**

- **arXiv:** fetched through 2026-09-30 (top-up 2026-11-07, see Session Log). Q3 is complete for
  cs.SD, eess.AS and cs.CL.
- **Interspeech 2026:** fetched from ISCA 2026-11-01 (complete; see Session Log).
- **ICASSP, ASRU, SLT:** no fetcher (`BACKLOG.md`, Infrastructure). ICASSP 2026 is Q2 by its
  conference date (2026-05-03) in any case.
- **ACL 2026:** main track and workshops fetched 2026-08-23. EMNLP 2026 (October) is Q4.

---

## Next Session — Resume Here

**2026-11-13: sweep batches 7-10 done (16 pre-selected papers in four batches A-D), 15 pages
ingested, 1 rejected at the scope check (`2607.01865`, environmental-sound codec).** Last ingested
`2607.03985` NouveauVoice (2026-07-04). Q2 straggler Vagdhenu `2608.26146` ingested; Q2 now has only
the two held records. Q3: 71 ingested, 324 accepted (323 in the sweep; StellarTTS excluded), 232
rejected (incl. `2607.01865`). Corpus 1,099 pages. Manual
Verification Queue: no open items (all 2026-11-13 items resolved). To resume:

**Session order (user, 2026-11-12, confirmed 2026-11-13): ingest oldest first.** The 19 Q4 2026
records were downloaded and parsed at the end of the 2026-11-13 session (step 3).

1. **Continue the sweep with the next oldest accepted, parsed records** (by canonical
   `published_date`, then ID): `2609.04222` GEPARD tech report (07-04), `2607.01345` TurnNat (07-05),
   then 2026-07-06: `2607.02214` SpeechCombine (re-dated to ICML 2026-07-06 on 2026-11-13; ingest the
   arXiv PDF, which is the camera-ready; `url_peer_reviewed` -> OpenReview already set), `2607.04941`
   DuplexChat (SLT demo, "submitted"), `2607.05250` (arXiv comment "Accepted to SPECOM 2026": run the
   proceedings check), `2607.05365` SPEARBench, `icml-2026-hgKQemfVbS` AgentSteerTTS,
   `icml-2026-icMRkTnuU7` (ICML-canonical: search arXiv for a twin and set `url_preprint`), then
   2026-07-07 `2607.06054` BlueMagpie-TTS, `2607.06461` WordVoice, 2026-07-10 `2607.09134` ReGen
   (ICML: proceedings check), 2026-07-15 `2607.06027`, ... Build a numbered list of 16 with the
   per-paper pre-flight from `docs/ingest-protocol.md` section 2, show it and wait for confirmation.
   The two Q2 holds (`2606.12940` ICML, `2606.13006` IJCAI) stay held unless the user lifts the hold.
2. **Ingest the peer-reviewed version when it is known** (rule: `docs/schemas/metadata.md`, "Source
   Version at Ingest"; procedure: `docs/ingest-protocol.md` section 2). Per paper at ingest time:
   - **65 arXiv-canonical Interspeech 2026 records**: switch with `use_peer_reviewed.py`
     (`--from-duplicate` for the 56 with an ISCA duplicate record; explicit flags from the Session
     Log table for the 9 without), then re-parse, just ahead of each batch.
   - **11 ISCA-canonical records with a known arXiv twin**: set `url_preprint` before ingest.
   - **ICML `2607.09134`, ICME `2608.03021`**: check for retrievable proceedings at pre-flight;
     otherwise ingest the preprint. An ICML acceptance confirmed by an OpenReview duplicate record or
     a PMLR line on page 1 re-dates to the ICML date (2026-07-06) with `url_peer_reviewed` set; the
     arXiv PDF stays the source when the OpenReview PDF is gated (SpeechCombine, 2026-11-13).
   - **EMNLP 2026 (8) and SLT 2026 (8)**: ingest the preprint, stay Q3 on arXiv dates.
   - Pages already written from a preprint get link and note only (`migrate_peer_reviewed_versions.py`
     with an overrides YAML in `docs/records/`). The script appends its two log lines to the END of
     `wiki/log.md` and `raw/pipeline_log.md`: move them into the dated section by hand.
   - Check figure-1 of all 70 ISCA papers for the ISCA logo when the sweep reaches 2026-09-27.
3. **Q4 2026 records are ready:** the 6 missing PDFs were downloaded and all 19 Q4 2026 accepted
   records (published 2026-10-05 to 2026-11-02) were parsed on 2026-11-13 (19 done, 0 failed); they
   follow the Q3 sweep in date order.
4. **Excluded from the sweep:** `2607.19859` StellarTTS (ASRU 2025, canonical quarter Q4 2025); it is
   re-dated by the batch, then ingested as a Q4 2025 page. Catch-up Q4 integration with
   `2506.04518` is a `BACKLOG.md` item.
5. **Held papers:** `2606.12940` (ICML) and `2606.13006` (IJCAI) move to Q3 through the
   peer-reviewed-version batch; ingest them as Q3 papers afterwards. Six ingested Q2 pages (four
   ICML, two ICPR) will also move into Q3 then; they need no new pages.

**Side threads (not blocking):** duplicate page pairs in `BACKLOG.md` (LLaMA-Omni 2 `2505.02625` /
`2025.acl-long.912`, intended canonical the ACL one; SLAM-Omni among them); OpenReview live fetches
are blocked by a browser-verification gate, so use the saved-page path (`openreview.py --from-file`).

**Agent prompts (2026-11-13):** keep ONE standing block and copy it verbatim into every prompt;
add only paper-specific notes (source-version block, related pages, scope decisions, the tagging
rules that matter for that paper). Rewriting the block per paper dropped two rules this session (the
`architectural-novelty` definition and the scope stop rule). The block names
`speech-generation-wiki-infra-ingest` as the working directory and infra commit source; card labels
follow existing pages (`ACL · 2026 · Conference`, `ACL 2026 (Findings) · 2026 · Conference`,
`arXiv · 2026 · Preprint`); `field_significance.type` guidance is quoted from the SKILL.md table
(a new training objective is `architectural-novelty`, user 2026-11-13). Agent runtimes this
session: 2.5-30 min typical, 48-67 min for three papers.

**Cadence:** see `docs/ingest-protocol.md` section 3; follow whichever cadence the user most
recently requested (2026-11-13: 16 papers pre-selected chronologically in four batches of 4 with
full pre-flight and one confirmation; papers one at a time with no per-paper go-ahead; batch summary
with one verification item and recommendation, then go-ahead; the user may defer queue items to the
session end).

---

## Success Criteria

- All accepted Q3 2026 papers have `status: ingested` in `raw/metadata/`
- Health check passes corpus-wide with zero errors:
  ```bash
  .venv/bin/python scripts/health_check.py --module ingest --wiki-dir /Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content-ingest
  ```

---

## Methodology

The procedure (cadence, per-paper cleanup and QC, tagging rules, claims format, interruption
recovery, commit workflow) is canonical in `docs/ingest-protocol.md` and the ingest `SKILL.md`.
This section keeps the scope precedents and gaps carried forward from the Q2 2026 sweep, plus
anything specific to Q3 2026.

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
- **Narrow accept (tri-domain audio, genuine speech-reconstruction evidence)** — DashengTokenizer
  (2602.23765): a tri-domain (speech/music/sound) audio tokenizer with no TTS/VC generation
  component, but accepted on `task: [codec]` alone because it reports a genuine SEED-TTS
  speech-reconstruction benchmark against known in-corpus TTS codecs. Distinct from the plain
  reject shape of tri-domain papers with zero speech-specific evaluation (SemanticVocoder,
  TQCodec). See [[feedback_corpus_scope_nonspeech_audio_and_zero_metric]].
- **Framing-plus-infrastructure accept (zero-metric, not a blanket rule)** — VietNormalizer
  (2603.04145): explicitly TTS-pipeline-framed but reports zero quantitative results of any kind.
  Accepted on the strength of genuine open-source infrastructure value, judged case-by-case — this
  is a materially weaker empirical case than the 2510.03111 precedent it invoked, so do not treat it
  as license to accept every zero-metric TTS-adjacent tooling paper.
- **Reject (curiosity papers, user 2026-11-01)** — Interspeech 2026 review: papers worth reading
  but not about generating or evaluating synthetic speech are out. Rejected: perception or
  behaviour studies where a TTS or voice-assistant voice is only a stimulus (voice-cloned emotion
  recognition, phonetic alignment to Siri), speech-LM safety interpretability with no generation
  (consistent with SPIRIT), dialogue interaction-quality modelling from user-side features (left
  to [[future_dst_scope_expansion]]), mechanical vocal-tract synthesis with no metrics, codec
  benchmarks on non-speech health signals, and S2S tutoring demos with TTS as a black box.
  Accepted: listener studies that evaluate TTS output itself with real raters (racial identity in
  TTS voices; robot TTS prosody with a fine-tuned Matcha-TTS and 160 raters), and watermarking
  built into TTS sampling. See [[feedback_corpus_scope_curiosity_papers]].
- **Review-queue decisions, 2026-11-07** (arXiv top-up; full reasons in `raw/review_queue.md`):
  - *Prosody analysis with no system:* the curiosity rule wins over the one-off `2512.16832`
    accept (`2608.30260` syntax-prosody rejected); an analysis framed entirely as design input
    for a generation task is accepted (`2608.27848`, cross-lingual prosody for expressive S2ST).
  - *Brain-signal input:* no standing rule, decide each paper by hand (user). Accepted
    `2609.04455` Brain2Speech-Net (TTS latent-space backbone, the MiSTR shape; `TTS` fallback tag,
    flag at ingest); rejected `2609.37601` SENSE (non-invasive EEG neuroscience, MindVoice shape).
  - *Anti-cloning and detection:* imperceptible protection evaluated against VC/TTS models is
    accepted (Mimic Blocker, NaVo, `2610.00662`); so is work that modifies and evaluates a TTS
    system to study detection evidence (`2609.30983`). Pure detectors, attribution and forensics
    stay rejected.
  - *Full-duplex speech LMs:* memory (`2608.26005`), adversarial robustness with a trained
    defence (`2609.27378`) and an S2S gender-bias audit of the rendered voice (`2609.09263`)
    accepted. `2609.15759` (ASR head in a duplex S2S model) was accepted over a recommended reject
    and is not a precedent: plain ASR-with-speech-LM-framing papers stay rejected (TS-OPD
    `2609.29464`).
  - *Turn-taking detection benchmarks* are accepted (`2608.25218` TurnBench), following Easy Turn
    and DualTurn.

### Interspeech 2026 duplicates and peer-reviewed versions

The ISCA fetch (2026-11-01) marked every proceedings record that duplicates an existing record as
`is_duplicate` with the existing record canonical, and copied the ISCA key and DOI into the
canonical record's `source_ids`. So for the 65 accepted re-dated arXiv records that are
Interspeech papers, ingest the arXiv record (its PDF and parse) as usual. 56 of them have
`source_ids.isca`; the other 9 matched ISCA entries the keyword filter dropped, so look their key up
on the ISCA index when the link is needed. The ISCA URL for the peer-reviewed link is
`https://www.isca-archive.org/interspeech_2026/{source_ids.isca}.html`. The reverse case (from the
2026-11-07 top-up): 13 ISCA records have an arXiv preprint marked as their duplicate, with the
ISCA record canonical; ingest those from the ISCA PDF, and the arXiv ID is in `source_ids.arxiv`. Before writing any Q3 page,
check whether the peer-reviewed-version rule (`BACKLOG.md`) has landed: if it has, the page needs
the `url_peer_reviewed` link and note from the start.

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

Some papers carry a misleading arXiv ID prefix (e.g. a `2604.xxxxx` ID for a paper actually
published in March). Always trust `published_date` in `raw/metadata/{id}.json` for chronological
ordering and quarter assignment, not the ID prefix. This recurred repeatedly across Q1 2026 (e.g.
`2604.03279`, `2604.01247`, `2604.08558`, `2604.08562` were all genuinely Q1 papers despite the
`2604` prefix) — expect the same in Q3 2026, where most Interspeech 2026 papers carry `2601`-`2606` arXiv prefixes but a
`2026-09-27` `published_date` and sort by date every time, never by ID prefix.

### Known open vocabulary gap

No canonical vocabulary term currently covers non-text-input speech generation (brain-signal
decoding, lip-to-speech, audio-continuation-only systems). The gap applies only when there is no
text input: text-driven TTS with visual or other non-text conditioning (e.g. sign-video prosody in
`2604.10413`, video prosody in `interspeech-2025-1494`, face-based voices) is plain `TTS`, not a
fallback. A possible `V2S`-style task term is a deferred `BACKLOG.md` item (2026-10-17). Several Q3/Q4/Q1 2026 papers were tagged
`TTS` as the closest fit pending a user decision on whether to add a dedicated term (e.g.
`2602.11477`, lip-to-speech, applied the standing fallback explicitly in Q1 2026). If this recurs in
Q3 2026, tag `TTS` as the same fallback and flag it in the Manual Verification Queue rather than
inventing a new term unilaterally.

---

## Session Log

### Session 2026-11-01: bootstrap

Created from the Q2 doc after the Q2 sweep closed. The same day's Interspeech 2026 ISCA fetch
(fetcher fixes, 203 records, 109 duplicates, 70 new accepted, two Q2 pages re-dated, PDFs
downloaded) is logged in the archived Q2 doc's Session Log and in `raw/pipeline_log.md`.

### Session 2026-11-07: arXiv top-up, downloads, parse batches 1-3

- **Fetch.** `arxiv.py --date-from 2026-08-20 --date-to 2026-09-30` (cs.SD+eess.AS, 144 written)
  and `arxiv_oai.py --set cs.CL` for the same window (29 written, 53 already in the corpus).
- **Dedup.** Title, author and abstract match of the 173 against the whole corpus: 13 are arXiv
  preprints of Interspeech 2026 ISCA records. Neither version ingested, so the existing ISCA
  record stays canonical (now written into `docs/schemas/metadata.md`); the ISCA records gained
  `source_ids.arxiv` and the arXiv dates (the metadata check requires `preprint_date` and
  `version_date` on any record with an arXiv ID). Kept as separate works: `2609.34052` (extends
  ingested `2603.18359`) and `2609.15184` Cross-Lingual F5-TTS 2.
- **Filter** (filter agent): 160 scored, 110 accepted, 11 review, 39 rejected (14 pure
  deepfake-detection papers rejected per the corpus precedent). User decided the 11 in five
  themed batches: 9 accepted, 2 rejected (see the Methodology precedent list).
- **Downloads.** 224 arXiv PDFs, 0 failures. Re-pinning to the downloaded version changed 37
  `published_date`s: 13 papers moved to Q4 (October/November revisions), and `2608.26146` moved
  to Q2 (arXiv's only version is dated 28 Jun 2026 despite the 2608 ID). Expect this on any
  download run: the version date of what is downloaded is canonical.
- **Parse** batches 1-3 (120 papers, July 1 to September 11), 0 failures. Batch 2 hit the 2 h
  background limit at 38/40 (finished in a second run); batch 3 ran as two runs of 20. LILAC
  `2608.05727` had an empty `references.json` (headless AAAI bibliography after an AI-disclosure
  and an Acknowledgements heading, which stop the after-Conclusion fallback); rebuilt by hand from
  `paper.md` with the converter's `_parse_ref_string` (36 refs). The user declined an extractor
  fix for now.
- Commits: `ac1427c` (fetch, filter, review), `6c4fe03` (downloads), plus the wrap-up commit.

### Session 2026-11-08: parse batches 4-5

- **Batch 4** (40 papers, published 2026-09-11 to 09-24): 40 done, 0 failed, two runs of 20
  (78 min), 0 flagged by the post-parse check.
- **Batch 5** (40 papers, published 2026-09-24 to 09-27, including the first 13 ISCA PDFs): 40 done,
  0 failed, two runs of 20 (48 min), 0 flagged.
- Citation index rebuilt after each batch (now 25,248 entries, 1,392 corpus papers). The
  content-ingest worktree was fast-forwarded to content `main`. The sibling peer-reviewed-version
  stream landed on `main` during the session and was merged into `work/ingest` at wrap-up; no ingest
  pages were written.

### Session 2026-11-11: parse batches 6-7, peer-reviewed-version check

- **Batch 6** (40 ISCA PDFs, 2026-09-27): 40 done, 0 failed, two runs of 20 (49 min), 0 flagged.
- **Batch 7** (17 ISCA + 23 arXiv to 2026-09-30, plus Q2 `2608.26146`): 41 done, 0 failed (68 min).
  `interspeech-2026-kato26_interspeech` and `-pine26_interspeech` are under 100 lines: 2-page
  Show & Tell demos, all sections present, reference counts match the highest in-text citation.
  **All 364 accepted Q3 records are parsed.** Citation index: 25,900 entries, 1,473 corpus papers.
- **Peer-reviewed-version check** (read-only `audit_peer_reviewed_versions.py` against
  content-ingest). The Q1 batch is released (content `844fb57`, infra `8e25555`, both in the ingest
  worktrees); no other venue batch has run. Q3-relevant findings:
  - 50 accepted Interspeech 2026 records carry `conference_date` and ISCA source IDs; they only lack
    `url_peer_reviewed`/peer-reviewed venue (the open Interspeech batch).
  - 9 accepted records were dated 2026-09-27 with no ISCA source ID (6 from the arXiv comment;
    `2606.18072`, `2606.23285`, `2607.14310` found later the same day by querying metadata
    directly, which the audit had grouped differently). Their titles failed the ISCA fetch's keyword
    filter, so no ISCA record existed to match. **Verified 2026-11-11 against the ISCA archive index
    and paper pages**; all stay Q3, no date change. Inputs for `use_peer_reviewed.py` (landing page
    `https://www.isca-archive.org/interspeech_2026/{slug}.html`, PDF `{slug}.pdf`):

    | arXiv ID | ISCA slug | DOI | Match |
    |---|---|---|---|
    | `2606.10591` | `liang26d_interspeech` | 10.21437/Interspeech.2026-3355 | exact title, 4/4 authors |
    | `2606.19951` | `takagi26_interspeech` | 10.21437/Interspeech.2026-1478 | exact title, 4/4 authors |
    | `2606.22009` | `koriyama26_interspeech` | 10.21437/Interspeech.2026-1800 | exact title, 1/1 author |
    | `2606.31365` | `grundhuber26_interspeech` | 10.21437/Interspeech.2026-2406 | exact title, 2/2 authors |
    | `2607.19033` | `wagner26b_interspeech` | 10.21437/Interspeech.2026-2817 | exact title, abstract similarity 0.98; ISCA camera-ready PDF lists only Laurin Wagner, arXiv lists four authors; same work |
    | `2607.22658` | `wang26fa_interspeech` | 10.21437/Interspeech.2026-2938 | exact title; ISCA adds Najim Dehak and Laureano Moro-Velázquez to the 6 arXiv authors |
    | `2606.18072` | `dai26c_interspeech` | 10.21437/Interspeech.2026-791 | exact title, 8/8 authors |
    | `2606.23285` | `kando26_interspeech` | 10.21437/Interspeech.2026-999 | exact title, 4/4 authors |
    | `2607.14310` | `shigabeev26_interspeech` | 10.21437/Interspeech.2026-809 | exact title, 2/2 authors |

  - Acceptance-comment-only Q3 records: EMNLP 2026 (8, incl. non-archival SALMA workshop
    `2609.13413`), SLT 2026 (8), ICML 2026 `2607.09134`, ICME 2026 `2608.03021`, ASRU 2025
    `2607.19859` (would move to Q4 2025 if verified).
  - Would move into Q3 once verified: held `2606.12940` (ICML) and `2606.13006` (IJCAI); ingested
    Q2 pages `2603.17837`, `2604.12928`, `2605.27772`, `2606.01479` (ICML) and `2604.09111`,
    `2604.10413` (ICPR); ACL 2026 pages `2601.04029`, `2603.14432`, `2603.14889` depending on the
    ACL 2026 date; `2605.16026` is a TASLP extension of an ACL Findings paper (full-version check,
    not a re-date).
- **User decisions:** EMNLP and SLT 2026 records stay in Q3 on their arXiv dates and are swept
  now (2026-11-11). ~~The peer-reviewed-version batches run after the Q3 sweep~~ (superseded the
  same day by the next decision).
- **Source version at ingest (user decision 2026-11-11):** when a verified peer-reviewed version is
  known, the page summarizes it, with the preprint as context only and logged as `url_preprint`;
  otherwise the preprint is ingested; pages already written from a preprint get the link and note
  only, no re-ingest. Implemented the same day: `docs/schemas/metadata.md` ("Source Version at
  Ingest", new fields `url_preprint` and `pdf_path_preprint`, parse layout
  `raw/parsed/{id}/preprint/`), `docs/ingest-protocol.md` section 2, the ingest, lightweight-ingest
  and review skills, the metadata health check, and `scripts/ingest/use_peer_reviewed.py` (with
  `tests/test_use_peer_reviewed.py`; 57 tests pass, agents check passes). Dry runs on `2608.00011`
  and `2606.10591` matched expectations; nothing applied yet.
- **ASRU 2025 `2607.19859` StellarTTS:** verified via Crossref (DOI
  10.1109/asru65441.2025.11434642, ASRU 2025 proceedings, conference start 2025-12-06, 9/9
  authors). First posted to arXiv 2026-07-22, months after the conference, so it arrived with the
  Q3 arXiv fetch, but its canonical quarter is Q4 2025. **User decision:** it belongs to Q4 2025
  and is **excluded from the Q3 sweep** (363 remain). Re-date it through the peer-reviewed-version
  batch, then ingest it as a Q4 2025 page; the catch-up Q4 integration for it and `2506.04518` is a
  `BACKLOG.md` item.

### Session 2026-11-11: Q3 sweep batch 1

Numbered list confirmed by the user; actual IDs match #1-#4. All four are ACL Anthology workshop
records (proceedings-canonical, no known arXiv twin, so no `url_preprint`). One paper at a time,
cleanup and QC after each.

| # | ID | Result | QC catches and fixes |
|---|---|---|---|
| 1 | `2026.americasnlp-6.1` Myaamia TTS | low; `transformer-enc-dec-tts`, `gan-vocoder`, `subjective-evaluation` | Clean. Agent restored ± signs Docling dropped from Table 3 (Duration RMSE). Index count line 19 missed by `cleanup.py` (fixed by hand). |
| 2 | `2026.dravidianlangtech-1.3` Dravidian S2ST | low; `speech-to-speech` | **Architecture `transformer-enc-dec` removed** (vocabulary term is FastSpeech-family NAR; the paper's Whisper/IndicTrans2/SeamlessM4T are AR ASR/MT and nothing on the synthesis side is trained; 52 S2S pages use `[]`). Agent rebuilt garbled Table 1 cells from the PDF; cascade-beats-E2E in every cell verified against both tables. Same count miss, fixed by hand. |
| 3 | `2026.iwslt-1.11` HW-TSC cloning | low; `autoregressive-codec-tts` | Task VC dropped on the page (prompt-based TTS cloning, no source speech converted); metadata `task` left as the filter's value (239 pages already differ, the page is authoritative). Text-vs-table note (§4.2 names the wrong lowest Chinese similarity) verified against Table 1. |
| 4 | `2026.iwslt-1.12` four-system cloning benchmark | low; `related_concepts: []` | Garbled Table 1 rebuilt from the PDF text, verified row by row. Figure 2/3 vs Table 1 disagreements in the `[!warning]` verified visually (MOSS-TTS ja, Qwen3-TTS de, CosyVoice3 ja; Qwen3-TTS mean 0.10 vs 0.16). Review flag queued. |

- **New recurring issue, fixed:** `scripts/ingest/cleanup.py` did not update the homepage's
  `> N paper summaries` line (introduced by content commit `416ccd6`); a third pattern was added
  and verified on #3 and #4.
- **Prompt practice:** agents run from the session's own worktree, so the standing prompt now
  names the infra-ingest worktree as the working directory; the session worktree was fast-forwarded
  to `main` first so the preloaded skill is current.
- Corpus at **1,065** pages. Q3: 38 ingested, 360 accepted remaining (359 in the sweep), 229
  rejected.

### Session 2026-11-11: Q3 sweep batch 2

Actual IDs match #5-#8. First use of `use_peer_reviewed.py`: #5-#7 were arXiv-canonical records
with verified ACL Anthology versions (title, authors, DOI, July 2026), switched with `--apply`
(ACL PDF downloaded, arXiv parse moved to `preprint/`, metadata `url`/`url_preprint` updated) and
re-parsed (3 done, 0 failed, 39 s). Their pages link `[→ Paper]` (ACL) and `[→ Preprint]` (arXiv).

| # | ID | Result | QC catches and fixes |
|---|---|---|---|
| 5 | `2604.26136` OmniVoice LoRA cloning (IWSLT) | low; `diffusion-tts` | **The switch mattered:** the camera-ready Table 3 changed the fine-tuning results (French SIM 0.748 → 0.760, Chinese 0.719 → 0.732, Arabic CER 0.071 → 0.060) while §5.1 prose still quotes the preprint numbers; the page uses the proceedings table and says so (verified against both PDFs). VC dropped. Architecture `[diffusion, hybrid]` → `[diffusion]` to match the OmniVoice page's frontmatter (its index row says `diffusion, hybrid`). |
| 6 | `2606.07240` KIT GRPO cloning (IWSLT) | low; `autoregressive-codec-tts`, `multilingual-tts`, `rlhf-speech` | Proceedings and preprint text identical. List fields written in quoted form (`["TTS"]`), unquoted by hand. Table 1 and the Table 2 average misprint (91.64 vs 91.93) verified. |
| 7 | `2606.27380` presentation-coaching survey (BEA) | low; `related_concepts: []` | Accepted in triage. Survey format correct. CosyVoice 2 mis-grouped as non-autoregressive in §2, verified; noted as a factual correction. Review flag queued. |
| 8 | `2607.00946` emotion steering geometry (arXiv) | low; `emotion-synthesis`, `autoregressive-codec-tts`, `flow-matching` | Follow-up to CoCoEmo `2602.03420` by the same authors (separate work, cross-linked). Prior-publication notice (ICML 2026 workshop) found at pre-flight; kept arXiv, flag queued. Docling shifted Table 2 one column; rebuilt table verified against the PDF row by row. |

- Corpus at **1,069** pages. Q3: 42 ingested, 356 accepted remaining (355 in the sweep), 229
  rejected.

### Session 2026-11-12: Q3 sweep batch 3

Pre-selected #9-#24 (four batches, all ACL 2026 on 2026-07-02, ID order) with the full pre-flight;
the user confirmed the list. Actual IDs match #9-#12.

- **Pre-flight finding, later-version duplicate:** `2026.acl-long.863` DisCo_Speech is the ACL
  version of ingested `2512.13251` (exact title, same authors), which is in 6 claim YAMLs (frozen).
  User decision: ACL record -> `is_duplicate`, `canonical_id` 2512.13251, rejected; the page gains
  the ACL link and italic note, date and venue unchanged (`migrate_peer_reviewed_versions.py`,
  overrides `docs/records/2026-11-12-disco-speech-peer-reviewed-version.yaml`). The script appends
  its log lines to the end of both logs; moved by hand into the 2026-11-12 sections.
- **Preprint links:** arXiv twins found by API title+author search and set as `url_preprint` for
  #9 (2604.14920), #11 (2506.11160), #12 (2604.14932), #15 F-Actor (2601.11329, existing duplicate
  record), #16 VoiceStar (2505.19462), #17 Self-EmoQ (2606.09837); none found for #10, #13, #14,
  #18. #19-#24 are arXiv-canonical with ACL IDs and need `use_peer_reviewed.py` with explicit ACL
  URLs (no ACL duplicate record exists; all six ACL pages verified, exact titles, PDFs present).

| # | ID | Result | QC catches and fixes |
|---|---|---|---|
| 9 | `2026.acl-long.6` Dual-Axis Generative Reward Model | moderate; `spoken-language-model`, `evaluation-metrics` | Clean. `training: RLHF` for GRPO on the judge with a rule-based reward, matching WavReward. Agent omitted `rlhf-speech` (reward never used to train a dialogue model, §Limitations), but WavReward and SDiaReward both carry it: queued. Table 1/2 numbers verified. |
| 10 | `2026.acl-long.998` Rectifying the Emotional Flow | moderate (`architectural-novelty`, an inference procedure); `flow-matching`, `emotion-synthesis`, `subjective-evaluation` | Training-free sampler on frozen CosyVoice2/IndexTTS2/F5-TTS, page says frozen. Docling garbled Tables 2, 4, 5 (Expresso row lost), resolved by agent from the PDF; spot-checked Tables 2, 6, 7 against pypdfium2 text. Regressions reported (SMOS, recall, ES). Figure checked. Agent run took 61 min. |
| 11 | `2026.findings-acl.1004` S2ST-Omni | moderate; `speech-to-speech`, `spoken-language-model` | Cascade S2ST with off-the-shelf IndexTTS2 backend; no TTS slugs, no `multilingual-tts` (English output). No evaluated S2ST baseline has a page (verified against the index). VoxCPM1.5 backend linked to the VoxCPM page with the version stated. Figure checked. |
| 12 | `2026.findings-acl.114` WavAlign | moderate; `rlhf-speech`, `spoken-language-model`, `speech-to-speech`, `subjective-evaluation`, `evaluation-metrics` | `evaluation-metrics` from the judge-vs-human agreement study (Tables 5-6). Human-eval item count 80 (Table 4 caption) vs 40 (Appendix G.1, same SBS test): verified, stated neutrally on the page. Losses on BBH/IFEval/AdvBench reported. Figure checked. Agent run took 73 min. |

- Corpus at **1,073** pages. Q3: 46 ingested, 351 accepted remaining (350 in the sweep), 230
  rejected (+1 DisCo_Speech duplicate).

### Session 2026-11-12: Q3 sweep batch 4

`2026.acl-long.6` queue item resolved first (option A, `rlhf-speech` added). Preprint links set
for F-Actor and VoiceStar. Actual IDs match #13-#16.

| # | ID | Result | QC catches and fixes |
|---|---|---|---|
| 13 | `2026.findings-acl.1622` FlowTokenizer (REPA-H codec DiT) | moderate; `neural-codec`, `flow-matching`, `self-supervised-speech`, `gan-vocoder`, `autoregressive-codec-tts`, `subjective-evaluation` (6, at cap) | Page `task: [codec, TTS]` vs metadata `[codec]`: kept, since §3.6/Table 5 trains and evaluates the paper's own codec-token TTS with a new auxiliary loss (index row reads page frontmatter; metadata `task` left as filtered). SSL: MMS (wav2vec 2.0) is the alignment target. `gan-vocoder`: adversarial fine-tuning ablated (Table 3). Docling merged Table 3 UTMOS cells, resolved from the PDF. "Highest UTMOS among 24 kHz systems" checked (ties the single GT row, which is not a system). |
| 14 | `2026.findings-acl.199` Dual-Reasoner | moderate (`architectural-novelty`, `dataset-contribution`); `spoken-language-model`, `speech-to-speech`, `streaming-tts`, `rlhf-speech` | Agent rewrote the Field Significance opening as `**Moderate.**` to avoid an em dash; restored the template `Moderate — `. Five source discrepancies on the page all verified in the parse (MMAR S-M-S cells Table 2 vs 7; "w/o ACR" group described as with-ACR yet 51.88 vs 53.92; VoiceAssistant-400K Fast in text vs Slow in Table 6; "5.17" vs table 6.17; "2.25x over Think" is the Base ratio). Table 3 row recovered from the PDF. Figure checked. |
| 15 | `2026.findings-acl.242` F-Actor | moderate (`engineering-integration`); `spoken-language-model`, `speech-to-speech` | Clean. Human raters judged transcripts, not audio: no `subjective-evaluation`. Closed set of 52 speakers: no `zero-shot-tts`. SALMONN-omni left unlinked (paper cites the 2024 codec-free preprint, the NeurIPS page is a later retitled paper). Table 4 recovered from the PDF. |
| 16 | `2026.findings-acl.570` VoiceStar | moderate; `autoregressive-codec-tts`, `zero-shot-tts`, `transformer-enc-dec-tts`, `prosody-control`, `subjective-evaluation` | Wiki Connections MaskGCT bullet over-broad ("strongest long-form speaker similarity"; false at 40-50 s, where it is lowest on SpkSim); agent named it but did not fix it, reworded to 20-40 s. `transformer-enc-dec-tts` without the `transformer-enc-dec` architecture tag follows T5Gemma-TTS `2604.01760` (encoder-decoder AR codec LM). Short-form losses on Seed-TTS reported. Figures checked. Review flag: significance moderate vs high (queued). |

- Corpus at **1,077** pages. Q3: 50 ingested, 347 accepted remaining (346 in the sweep), 230
  rejected.

### Session 2026-11-12: Q3 sweep batch 5

VoiceStar queue item resolved first (keep moderate). Preprint link set for Self-EmoQ. #19 and #20
switched to their ACL versions with `use_peer_reviewed.py` (explicit `--url/--pdf-url/--venue ACL
--date 2026-07-02 --source acl=... --source doi=10.18653/v1/...`, no trailing slash, matching batch 2),
re-parsed (2 done, 0 failed, 2.1 min); ACL notice confirmed on page 1 of both PDFs. Actual IDs match
#17-#20.

| # | ID | Result | QC catches and fixes |
|---|---|---|---|
| 17 | `2026.findings-acl.740` Self-EmoQ | low (`engineering-integration`); `emotion-synthesis` | Agent tagged `subjective-evaluation` for 10 raters scoring text responses; dropped for consistency with F-Actor (#15, raters judged transcripts) and the protocol (humans must judge system output speech). Four source inconsistencies on the page verified in the PDF text (Table 3 vs 6 full-model row, FSM Effectiveness p < 0.01 with a higher mean, §4.4 overclaim vs Table 4, Table 11 row labels). Docling garbled Tables 3, 4, 6, 7, 11; resolved from the PDF. `emotion-synthesis` queued (emotion of the speech is never measured). |
| 18 | `2026.findings-acl.940` Beyond Sentence-level Labels (Emotional-Context-TTS) | moderate (`dataset-contribution`, `engineering-integration`); `emotion-synthesis`, `instruction-conditioned-tts`, `autoregressive-codec-tts`, `subjective-evaluation` | Fine-tuned CosyVoice 2: `autoregressive-codec-tts` and `[autoregressive-LM, flow-matching, hybrid]` follow the CosyVoice 2 page and CoCoEmo; frozen flow decoder gets no `flow-matching` slug. Warning callout stated the agent's inference (test descriptions derived from target audio) as fact; hedged to what the paper says. |
| 19 | `2503.05085` S2S-Arena (switched to ACL `2026.acl-long.1615`) | moderate; `spoken-language-model`, `speech-to-speech`, `subjective-evaluation`, `evaluation-metrics` | Tags follow VoiceBench `2410.17196` (benchmark measuring generated speech of S2S models, judge validated against humans, Table 3). Text-vs-table mismatches (most wins 140 vs Kimi-Audio 142; Doubao cited as flow-matching evidence with unknown architecture) verified in the PDF; page reports the table values. Docling parse lacks Table 4 values; checked via pypdfium2. |
| 20 | `2503.23439` Speculative End-Turn Detector (switched to ACL `2026.acl-long.2094`) | moderate (`dataset-contribution`, `engineering-integration`); `self-supervised-speech` | In scope by precedent (Phoenix-VAD `2509.20410`; turn-taking benchmark accept 2026-11-07). Fine-tuned wav2vec 2.0 earns `self-supervised-speech`; no LLM consumes speech, so no `spoken-language-model`. GRU size (202K vs 1M) and TTS voice count (2 vs 3) inconsistencies verified in the PDF text. Agent fixed its own over-narrow F1-drop range before finishing. |

- Corpus at **1,081** pages. Q3: 54 ingested, 343 accepted remaining (342 in the sweep), 230
  rejected.

### Session 2026-11-12: Q3 sweep batch 6

Self-EmoQ queue item resolved first (keep `emotion-synthesis`). #21-#24 switched to their ACL
versions with `use_peer_reviewed.py` (explicit ACL URLs as in batch 5) and re-parsed (4 done, 0
failed, 6.5 min); ACL notice confirmed on page 1 of all four PDFs. Actual IDs: #21, #23, #24
ingested; **#22 `2604.06871` held at the scope check, not ingested** (switched and parsed only).

| # | ID | Result | QC catches and fixes |
|---|---|---|---|
| 21 | `2505.22765` StressTest (ACL Findings `2026.findings-acl.64`) | moderate (`evaluation-contribution`, `dataset-contribution`, `empirical-benchmark`); `spoken-language-model` | No `prosody-control`: stress in the synthetic training data comes from an API markup trick checked only as a data filter. Paper error verified in the parse: §5.4 credits StresSLM with SSD 88.3/83.5, which are WhiStress's F1 in Table 3. LLaMA-Omni linked as `2409.06666` (legacy dedup pointer target). Table 10 recovered from the PDF. |
| 22 | `2604.06871` Affinity Pooling (speech-LM token redundancy) | **held: scope** | Input-side token merging for Qwen2-Audio and Kimi-Audio, evaluated only on ASR, spoken QA and speech translation (text output). Matches the FastLongSpeech reject (2026-07-27, input compression for Qwen2-Audio, understanding-only) and the FAMA/MLC-SLM rule. Pending user decision. |
| 23 | `2604.11096` CSLM (ACL Findings `2026.findings-acl.642`) | moderate (`engineering-integration`); `spoken-language-model`, `speech-to-speech`, `multilingual-tts`, `streaming-tts`, `subjective-evaluation` | `multilingual-tts`: own system trained on zh+en, generated speech evaluated in both (Tables 1, 2, 5, 6). `streaming-tts`: chunk-interleaved generation, speedup measured (Table 10); the page uses only the speedup ratios because absolute "Latency(s)" values (hundreds) are undefined, verified in the PDF. Inherited CosyVoice decoder/HiFi-GAN: no slugs. |
| 24 | `2604.15710` VoxMind (ACL `2026.acl-long.459`) | moderate (`engineering-integration`, `dataset-contribution`); `spoken-language-model`, `speech-to-speech` | "Beats Gemini-2.5-Pro" holds on Overall only; per-column wins and losses on the page. Overall formula (mean of 10 columns, FC x20) marked as the page's own arithmetic; verified (745.74/10 = 74.57). SLAM-Omni linked as `2025.findings-acl.115` (the cited version); the pair is already tracked in BACKLOG.md. |

- Corpus at **1,084** pages. Q3: 57 ingested, 339 accepted remaining (338 in the sweep), 231
  rejected (after the #22 rejection). Corpus-wide ingest health: PASS, 0 errors, 1,167 warnings (unchanged baseline).

### Session 2026-11-13: Q3 sweep batch 7 (batch A of 4)

Session order (user): ingest oldest first, parse of the 19 Q4 2026 records deferred. 16 papers
pre-selected chronologically (A: #1-#4 Vagdhenu + three ACL; B: #5-#8 UniSonate, AffectCodec
(Shi), FC-TTS, long-form benchmark; C: #9-#12 ImmersiveTTS, privacy prosody, UniVocal, LuxEmo;
D: #13-#16 IWAENC codec `2607.01865`, GRAFT `2607.02633`, `2609.13150`, NouveauVoice
`2607.03985`). Pre-flight decisions (user, 2026-11-13): `2604.17358` accepted under the turn-taking
precedent; `2607.02214` SpeechCombine re-dated to ICML (2026-07-06, arXiv PDF stays the source,
`url_peer_reviewed` -> OpenReview), so it left the window and NouveauVoice took #16. Pre-flight
notes: UniSonate is InstructAudio's (`2511.18487`) follow-up, not a duplicate; NouveauVoice follows
SpeakerVAE `2511.07135` (same authors, different system); `2607.01865` "Accepted for IWAENC 2026"
is unverified, ingest the preprint. #2-#4 switched with `use_peer_reviewed.py` (explicit ACL flags)
and re-parsed (3 done, 0 failed, 13 min); ACL notice confirmed on page 1 of all three PDFs.
Actual IDs match #1-#4 (4 launches).

| # | ID | Result | QC catches and fixes |
|---|---|---|---|
| 1 | `2608.26146` Vagdhenu (Q2 straggler, arXiv) | low (`engineering-integration`, `negative-result`); `flow-matching`, `prosody-control`, `speaker-adaptation`, `gan-vocoder` | No `subjective-evaluation`: only expert single-listener MOS estimates (Table 1 caption), stated on the page. `gan-vocoder` for the fine-tuned BigVGAN. No `zero-shot-tts` (voice in fine-tuning data), no `multilingual-tts` (many scripts transliterated into one language). Parler-TTS and CosyVoice links verified as the paper's own citations. Clean. |
| 2 | `2604.17358` Still Between Us? (ACL `2026.acl-long.1902`) | moderate (`dataset-contribution`, `empirical-benchmark`, `evaluation-contribution`); `spoken-language-model`, `evaluation-metrics` | Page adds `task: evaluation` (benchmark plus RSF/OH metrics validated against humans, Table 8); index row carries both. No `subjective-evaluation` (humans rated text responses). Card label `ACL · 2026 · Conference` follows existing ACL pages (the prompt's "ACL 2026" was wrong). Tables 2-6, 8 verified in the PDF. Clean. |
| 3 | `2604.17852` LLM-Codec (ACL Findings `2026.findings-acl.1308`) | moderate (`engineering-integration`, flagged); `neural-codec`, `spoken-language-model` | Verified the page's Limitations-vs-ablation note in the PDF (Limitations says per-component learnability is not ablated; Tables 3-4 report it) and the 50.7% random-init SALMon figure. Table 2 headers rebuilt from the PDF. **Prompt error:** my prompt said a new training objective is not `architectural-novelty`, contradicting the SKILL.md type table; corrected for later prompts; type queued. |
| 4 | `2604.18159` FreezeEmpath (ACL Findings `2026.findings-acl.846`) | moderate (`engineering-integration`); 6 slugs (cap): `spoken-language-model`, `speech-to-speech`, `emotion-synthesis`, `autoregressive-codec-tts`, `multilingual-tts`, `subjective-evaluation` | **Fixed:** LLaMA-Omni 2 Wiki Connections link `2505.02625` -> `2025.acl-long.912` (intended canonical per BACKLOG.md). Human raters judged speech responses (5 raters x 20 samples, Figure 4), so `subjective-evaluation` holds. Table 1 VStyle rows rebuilt by the agent and verified cell by cell. Cap flag queued. |

- New recurring-issue candidate: a session prompt line contradicted the SKILL.md type definitions
  (training objective counted as non-architectural). Copy type guidance from the SKILL.md table.
- Corpus at **1,088** pages. Q3: 60 ingested, 336 accepted remaining (335 in the sweep), 231
  rejected. Q2: 175 ingested, 2 accepted (held). Corpus-wide ingest health: PASS, 0 errors,
  1,167 warnings (unchanged baseline).

### Session 2026-11-13: Q3 sweep batch 8 (batch B of 4)

LLM-Codec queue item resolved first (`architectural-novelty`, Figure 1 added). #5-#8 switched to
their ACL versions with `use_peer_reviewed.py` (explicit ACL flags) and re-parsed (4 done, 0
failed, about 22 min); ACL notice, title and authors confirmed on page 1 of all four PDFs. UniSonate's
ACL parse has 48 references vs 59 in the preprint: the camera-ready genuinely trimmed
self-citations (SecoustiCodec, Cui et al. absent from the ACL PDF), not a parse loss. Actual IDs
match #5-#8 (4 launches). Agent runtimes: 67 min (UniSonate), 14, 12 and 5 min.

| # | ID | Result | QC catches and fixes |
|---|---|---|---|
| 5 | `2604.22209` UniSonate (ACL `2026.acl-long.1293`) | moderate (`architectural-novelty`, Figure 2); `flow-matching`, `instruction-conditioned-tts`, `emotion-synthesis`, `multilingual-tts`, `subjective-evaluation` | Predecessor bullet to InstructAudio `2511.18487`. `authors` follow the ACL page (13; metadata `authors_full` lists 14). Warning (token injection and curriculum not ablated; joint-training ablation cannot separate SFX from music data) verified against Tables 6-7. Table 2 cells verified in the PDF. `singing` flag queued. |
| 6 | `2605.11098` AffectCodec, Shi et al. (ACL Findings `2026.findings-acl.442`) | moderate (`architectural-novelty`, Figure 1); `neural-codec`, `emotion-synthesis`, `self-supervised-speech` (frozen HuBERT in the method), `autoregressive-codec-tts`, `subjective-evaluation` | Not linked to Meng et al. `2605.23373` (neither cites the other). Three reporting inconsistencies on the page verified in the PDF (§4.3 WER 5.75->5.18 not in Table 5; "highest UTMOS" on EmoVoice-DB vs CosyVoice 2 4.42; MUSHRA 90.71 vs 90.26). Garbled Table 5 and shifted appendix table numbers resolved by the agent. Task-scope flag queued. |
| 7 | `2605.24618` FC-TTS (ACL `2026.acl-long.173`) | moderate (`architectural-novelty`, Figure 1); `flow-matching`, `zero-shot-tts`, `prosody-control`, `disentanglement`, `subjective-evaluation` | `VC` dropped from the page `task` (no conversion of input speech; index row follows the page, metadata `task` untouched as on #2). Table 3 vs Table 5 RAVDESS gap and the Appendix D.3 ABX question wording verified in the PDF. `disentanglement` flag queued. |
| 8 | `2605.28618` SwanBench-Speech (ACL Findings `2026.findings-acl.112`) | moderate (`empirical-benchmark`, `evaluation-contribution`); `evaluation-metrics` (metrics validated against human ratings, SRCC), `subjective-evaluation` (expert listeners rate output audio) | Three prose-vs-table problems verified in the PDF (F5-TTS hierarchy 2.77 above 4 of 7 open-source AR systems; CosyVoice-3 reverb 2.26 better than CosyVoice-2 2.35; contradictory D.1 timbre thresholds). Commercial systems linked only via the paper's own citations, worded as such. MoonCast `2503.14345` is a legacy dedup pointer (NeurIPS record `wiki_page_id` set), not a defect. |

- Corpus at **1,092** pages. Q3: 64 ingested, 332 accepted remaining (331 in the sweep), 231
  rejected. Corpus-wide ingest health: PASS, 0 errors, 1,167 warnings (unchanged baseline).

### Session 2026-11-13: Q3 sweep batch 9 (batch C of 4)

Batch B queue items resolved first (AffectCodec task scope, FreezeEmpath cap, UniSonate `singing`,
FC-TTS `disentanglement`: all kept). #9-#11 switched to their ACL versions with
`use_peer_reviewed.py` and re-parsed (3 done, 0 failed); ACL notice confirmed on all three PDFs.
#12 LuxEmo (arXiv, no switch) was ingested first while the parse ran (same date, order within
2026-07-02 only). Actual IDs match #9-#12 (4 launches). Agent runtimes: 2.5, 48, 18 and 30 min.

| # | ID | Result | QC catches and fixes |
|---|---|---|---|
| 12 | `2606.31947` LuxEmo (arXiv) | low (`dataset-contribution`, `empirical-benchmark`, flagged); `emotion-synthesis`, `subjective-evaluation`, `speaker-adaptation` | `multilingual` dropped from `task` (single-language adaptation). Off-the-shelf vs author-adapted systems separated (Qwen3 FT, kNN TTS adapted). Figure 2 values checked against the image; the text's "GradTTS (de) highest LuxASR WER" holds only among zero-shot systems (1.72 vs kNN 1.81, Qwen3 FT 13.26), and emotion accuracy / Krippendorff's alpha are announced but never reported: both verified. Qwen3 FT not linked to Qwen3-TTS (no citation). |
| 9 | `2605.30965` ImmersiveTTS (ACL `2026.acl-long.1774`) | moderate (`architectural-novelty`, Figure 1); `flow-matching`, `self-supervised-speech` (WavLM-Large REPA target), `zero-shot-tts` (flagged), `subjective-evaluation` | Table 1 verified in the PDF; Docling dropped the ± signs in Tables 4-5, resolved by the agent. Losses to the CosyVoice2+TangoFlux cascade reported in full. No `instruction-conditioned-tts` (prompt describes only the scene). |
| 10 | `2606.00407` Privacy-preserving prosody (ACL short `2026.acl-short.26`) | low (`architectural-novelty`, Figure 1); `self-supervised-speech`, `disentanglement` (gradient-reversal speaker loss + speaker-normalized targets, 2x2 ablation, Table 2) | Accepted in triage; page states no speech is generated. Tables 1-2 verified in the PDF. Type follows the LLM-Codec decision (new training objective); `task: [TTS]` vocabulary gap queued. |
| 11 | `2606.01677` UniVocal (ACL `2026.acl-long.1452`) | moderate (`architectural-novelty`, `dataset-contribution`, `evaluation-contribution`, Figure 2); 6 slugs: `singing`, `autoregressive-codec-tts`, `flow-matching`, `emotion-synthesis`, `evaluation-metrics`, `subjective-evaluation` | No `multilingual-tts` ("code-switching" is speech/singing mode switching, all English). Gemini mode-switch judge validated against human annotators (verified in the PDF). Cap flag queued. |

- Corpus at **1,096** pages. Q3: 68 ingested, 328 accepted remaining (327 in the sweep), 231
  rejected. Corpus-wide ingest health: PASS, 0 errors, 1,167 warnings (unchanged baseline).

### Session 2026-11-13: Q3 sweep batch 10 (batch D of 4)

Batch C queue items left open by the user until session end. All four papers are arXiv (no
switch, no re-parse); no prior-publication notice on any page 1. Actual IDs match #13-#16 (4
launches); #13 written but held at the scope check. Agent runtimes: 29, 8, 3 and 2.5 min.

| # | ID | Result | QC catches and fixes |
|---|---|---|---|
| 13 | `2607.01865` SFI-layer codec (arXiv; "Accepted for IWAENC 2026" unverified) | **held: scope** | Environmental sound only (CochlScene), confirmed in the parse. Page written because the prompt omitted the stop rule; held without cleanup. Queued with a reject recommendation. |
| 14 | `2607.02633` GRAFT (arXiv) | moderate (`architectural-novelty`, `evaluation-contribution`, Figure 2); `autoregressive-codec-tts`, `multilingual-tts` (5 languages trained and evaluated), `subjective-evaluation` | **Fixed:** removed `evaluation-metrics` (D-PER/WS never validated against human judgment). `zero-shot-tts` and `disentanglement` omitted per rules; vocabulary gap (pronunciation control) queued. |
| 15 | `2609.13150` Reference-free metrics as evaluators and rewards (arXiv) | moderate (`empirical-benchmark`, `evaluation-contribution`, `negative-result`); `evaluation-metrics`, `subjective-evaluation` (own 30-rater Elo test), `rlhf-speech` (own GSPO runs), `autoregressive-codec-tts` (RL-trained Qwen3-TTS policy) | Table II and Table V Elo values verified in the PDF; per-corpus rankings, not a single winner. "De facto" from the abstract not repeated. |
| 16 | `2607.03985` NouveauVoice (arXiv) | low (`engineering-integration`); `voice-conversion` | Linked to SpeakerVAE `2511.07135` as earlier work by the same group (not cited by the paper, stated). GMM baseline wins on FACodec privacy, reported. §IV-A "uninformed" vs §V-A "semi-informed" attacker mismatch verified. Table I verified. |

- **Recurring issue confirmed:** the standing prompt dropped a protocol rule (the scope stop rule
  for #13; earlier today the training-objective type line). Both restored. Copy the standing
  block verbatim, do not rewrite it per paper.
- Corpus at **1,099** pages (index rows; 1,100 page files including the held #13). Q3: 71
  ingested, 325 accepted remaining (324 in the sweep, incl. held #13), 231 rejected.
  Corpus-wide ingest health: PASS, 0 errors, 1,167 warnings (unchanged baseline).

---

## Manual Verification Queue

Papers where the ingest agent emitted `review_flags` in its INGEST_RESULT signal. Review these
after the session batch is complete: check the paper page and resolve each flag by hand.

| Paper ID | Flag | Agent note |
|----------|------|------------|
| `2026.iwslt-1.12` | `related_concepts` empty | Evaluation of four pretrained cross-lingual cloning systems with reused, unvalidated automatic scorers and no human raters; no slug qualifies under the evaluation-paper rules (precedents `2604.11803`, `2606.14004`), so the page will not reach any concept YAML at integration. **Resolved 2026-11-11 (user): add `zero-shot-tts`** (option B over the evaluation-paper rule), **a one-off, not a precedent**: the next benchmark of others' systems is judged under the standing rule. Concept bullet added to Wiki Connections, QC passes. |
| `2606.27380` | `related_concepts` empty | Presentation-coaching survey (accepted in triage); zero-shot cloning (§5.2.2) and tempo/emphasis controls (§5.1.1) are mentioned but not reviewed, so no slug meets the coverage rule. Agent's fallback if a slug is wanted: `zero-shot-tts`. **Resolved 2026-11-11 (user): add `zero-shot-tts`, a one-off, not a precedent** (coverage rule for surveys stands). Concept bullet added, QC passes. |
| `2607.00946` | Workshop notice, venue kept arXiv | First page says "Published at ICML 2026 Workshop on Machine Learning for Audio" (PMLR line is the ICML style default). Treated as a non-archival workshop presentation (`2603.19831` precedent): ingested from arXiv, venue arXiv, no `url_peer_reviewed`; both dates are Q3. **Resolved 2026-11-11 (user): keep as arXiv preprint** (option A); no change. |
| `2026.acl-long.6` | `rlhf-speech` omitted | Generative reward model for full-duplex dialogue, trained with SFT + GRPO (rule-based reward) but never used to train a dialogue model (§Limitations), so the agent left out `rlhf-speech`. Precedent: the sibling reward-model pages WavReward `2505.09558` and SDiaReward `2603.14889` both carry `rlhf-speech`. Recommendation: add it for consistency (reward modelling for speech RL is in the concept's claim graph). **Resolved 2026-11-12 (user): option A, added** (follows the WavReward/SDiaReward precedent: a speech dialogue reward model earns `rlhf-speech` without running RL on a dialogue policy). Concept bullet added, QC passes. |
| `2026.findings-acl.570` | `field_significance` moderate vs high | VoiceStar: PM-RoPE gives an AR codec LM duration control plus length extrapolation (long-form WER 11.91 vs 82.29/52.44 at 40-50 s, Table 5); short-form only on par (Seed-TTS en: baselines ahead on every column). Agent chose moderate. Recommendation: keep moderate (high is reserved for papers whose contribution is clearly ahead on the main benchmarks or field-shaping; the long-form gain is real but rests on one 3-system comparison). **Resolved 2026-11-12 (user): keep moderate.** No change. |
| `2026.findings-acl.740` | `emotion-synthesis` on weak evidence | Self-EmoQ: an RL-trained text LLM plans an emotion label that drives off-the-shelf CosyVoice 2 instruct mode. The synthesized speech is scored only with SpeechBERTScore and PESQ (Table 7); no check that the audio carries the planned emotion and no listening test. Protocol: an unevaluated control does not earn its slug (ZONOS2). Dropping it leaves `related_concepts` empty. Recommendation: keep `emotion-synthesis` (the paper's subject is emotion selection for emotional TTS and the planned-emotion speech is produced and scored end to end; the page's warning states the gap). **Resolved 2026-11-12 (user): keep `emotion-synthesis`.** No change. |
| `2604.06871` | Scope: understanding-only speech-LM efficiency | Training-free token merging (Affinity Pooling) inside Qwen2-Audio and Kimi-Audio; evaluated only on ASR, spoken QA and speech translation with text output, no generated speech. Precedent: FastLongSpeech (input compression for Qwen2-Audio, understanding-only) rejected by the user 2026-07-27 under FAMA/MLC-SLM. Recommendation: reject. Not ingested; the record is already switched to ACL `2026.findings-acl.742` and parsed. **Resolved 2026-11-12 (user): rejected** (status `rejected`, logged in `raw/pipeline_log.md`). |
| `2604.17852` | `field_significance.type` engineering-integration vs architectural-novelty | LLM-Codec adds two LM-facing training objectives (future-token prediction with Medusa heads, memory-bank contrastive semantic alignment, via a Gumbel bridge) to an unchanged AUV codec. The agent chose `engineering-integration` partly because the session prompt wrongly said a new training objective is not `architectural-novelty`; the SKILL.md table says it is. Ablations: either objective alone and any K give the full gain (Tables 3-4). **Resolved 2026-11-13 (user): `architectural-novelty`** (new training objective per the SKILL.md table; level stays moderate). Type, Novelty Assessment opening and Figure 1 (method overview) updated; QC passes. |
| `2604.18159` | `related_concepts` at the 6-slot cap | FreezeEmpath: agent suggests `multilingual-tts` or `autoregressive-codec-tts` could be dropped as secondary. Both meet their rules (zh+en training, VStyle evaluated per language; own trained AR speech-token decoder, as on the LLaMA-Omni 2 page). Recommendation: keep all six. **Resolved 2026-11-13 (user): keep** (recommendation accepted); no change. |
| `2604.22209` | `singing` omitted | UniSonate generates songs from lyrics with evaluated vocal gender/age control (Table 4), but its music evaluation is song-level (SongEval, MMOS, genre/instrument accuracy) with no singing-voice metric. Agent kept `task: [TTS]`, matching the predecessor InstructAudio `2511.18487`. Recommendation: keep without `singing`. **Resolved 2026-11-13 (user): keep** (recommendation accepted); no change. |
| `2605.11098` | `task` codec only, downstream TTS probe | AffectCodec (Shi et al.) trains and evaluates a VALL-E-style AR+NAR TTS on its tokens (Table 4, Appendix E listening test) but frames it as a token probe. Page: `task: [codec]`, `autoregressive-codec-tts` kept, `zero-shot-tts` omitted (the agent's stated reason, avoiding padding, is wrong; the real question is whether a probe TTS earns TTS-side tags). Recommendation: keep as is (the AR codec-LM result is evidence about the codec, which is what `autoregressive-codec-tts` integrates; cloning is not the paper's object). **Resolved 2026-11-13 (user): keep** (recommendation accepted); no change. |
| `2605.24618` | `disentanglement` on frozen FACodec factors | FC-TTS builds on frozen FACodec representations but adds explicit separation mechanisms (cross-conditioned attribute-consistency loss, VQ style bottleneck, timbre-first two-stage decoder), each ablated in Table 5. The rule (explicit mechanism + ablation) is met. `VC` dropped from `task` (no conversion of input speech). Recommendation: keep. **Resolved 2026-11-13 (user): keep** (recommendation accepted); no change. |
| `2606.31947` | `field_significance` low vs moderate | LuxEmo: first expressive Luxembourgish TTS corpus (21 h) with a 20-listener native test, but 4 speakers, weakly supervised emotion labels (38 anger segments), uneven sample counts per system (612 / 53 / 280). Agent chose low. Precedent: single-language datasets/benchmarks sit at low unless uptake potential is clear (PashtoTTS-Bench, NLPAICS). Recommendation: keep low. **Resolved 2026-11-13 (user): keep low.** |
| `2605.30965` | `zero-shot-tts` on an appendix-level speaker prompt | ImmersiveTTS conditions on a WavLM-SV embedding of a speaker prompt (Appendix A) and evaluates speaker similarity on LibriTTS test (SECS, Table 3) and Seed-TTS test-en (S-MOS, Table 6), but never calls itself zero-shot. The rule (own system, prompt-based cloning of unseen speakers, evaluated) is met. Recommendation: keep. **Resolved 2026-11-13 (user): keep.** |
| `2606.00407` | `task: [TTS]` on a no-generation paper | Privacy-preserving prosody SSL encoder (accepted in triage): no speech generated; evaluated only on pitch reconstruction, ToBI prosodic-event probes and speaker ID. No vocabulary task fits; `[TTS]` kept as filter-assigned, as the standing fallback for no-text-input papers does. (The agent's second flag, `architectural-novelty` for a new training objective, follows the 2026-11-13 LLM-Codec decision; not queued.) Recommendation: keep `[TTS]` and note the vocabulary gap. **Resolved 2026-11-13 (user): keep.** |
| `2606.01677` | 6-slot cap: `evaluation-metrics` kept over `zero-shot-tts` | UniVocal: Seed-TTS test-en uses unseen speakers, so `zero-shot-tts` qualifies, but the cloning is inherited from CosyVoice 2; `evaluation-metrics` rests on SCSBench plus a Gemini judge validated against human annotators (rank-consistent, Fleiss' kappa 0.684). Protocol: drop inherited capabilities first at the cap. Recommendation: keep. **Resolved 2026-11-13 (user): keep.** |
| `2607.02633` | Vocabulary gap: pronunciation control | GRAFT: no concept fits per-word pronunciation control (`prosody-control` does not apply). Main session removed the agent's `evaluation-metrics` (D-PER/WS proposed but never validated against human judgment; the listening study is a separate ranking). `zero-shot-tts` omitted (benchmark reference speakers' provenance not stated, so unseen status unverifiable) and `disentanglement` omitted (separation via voice-converted training data, no loss/adversarial mechanism): both per standing rules. Recommendation: no new concept for one paper; note the gap. **Resolved 2026-11-13 (user): no new concept.** |
| `2607.01865` | **Scope: no speech at all** | Codec with adjustable token temporal resolution (SFI layers in DAC): every experiment reconstructs environmental sound (CochlScene); no speech or music test, no listening test, no downstream TTS/speech LM. The narrow tri-domain codec accept requires genuine speech-reconstruction evidence (2026-11-01 precedent), which is absent. The agent wrote the page anyway (the session prompt had dropped the stop rule); page held in the content worktree, **no index row, log or metadata change**. Recommendation: reject (status `rejected`, delete the held page and its figure). **Resolved 2026-11-13 (user): rejected**; page and figure deleted unpublished, logged in `raw/pipeline_log.md`. |

---

## Progress

Count by canonical `published_date` (the protocol's selection basis), not `year`/`month`:

```bash
.venv/bin/python3 -c "
import json, glob
from collections import Counter
c = Counter()
for path in glob.glob('raw/metadata/*.json'):
    m = json.load(open(path))
    if '2026-07-01' <= str(m.get('published_date') or '') <= '2026-09-30':
        c[m['status']] += 1
print(f\"Ingested: {c['ingested']} | Remaining: {c['accepted']} | Rejected: {c['rejected']}\")
"
```

---

## Commit / Push Workflow

See `docs/ingest-protocol.md` (section 9, Session close) for the commit, push, merge and
site-bump sequence and the worktree notes.
