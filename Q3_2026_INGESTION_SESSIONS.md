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
| Interspeech 2026, ISCA records | 70 | 0 | 70 |
| Interspeech 2026, arXiv records (re-dated) | 65 | 52 | 13 |
| arXiv | 191 | 114 | 77 |
| ACL 2026 | 27 | 27 | 0 |
| Workshops | 9 | 9 | 0 |
| ICML 2026 | 2 | 2 | 0 |
| **Total** | **364** | **204** | **160** |

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

Q3 2026 pre-flight is in progress; no Q3 page has been written by a sweep yet. Done on 2026-11-07:
arXiv top-up, dedup and filter, review queue cleared, all 224 missing PDFs downloaded, parse
batches 1-3 of 7. To resume:

1. **Finish parsing: batches 4-7** (160 papers, every accepted Q3 record with a PDF and no
   `paper.md`, ordered by `published_date`; batch 4 starts at 2026-09-11). Regenerate the list
   from metadata (the batch files lived in the session scratchpad). The user reviews one batch at a
   time: run each batch of 40 as two background runs of 20 (`batch_convert.py --workers 2 --ids
   ...`, about 40 min each), since a single run of 40 can exceed the 2 h background-task limit
   (batch 2 did). After each batch: post-parse check (paper.md < 100 lines or empty
   references.json), `citation_index.py`, one log line, then report. Most of batches 5-7 are the
   70 ISCA PDFs: check their figure-1 for the ISCA logo at ingest
   ([[feedback_interspeech_figure_sanity]]). Also parse `2608.26146` (now Q2).
2. *(done 2026-11-07)* arXiv top-up 2026-08-20 to 2026-09-30.
3. *(done 2026-11-07)* Download every Q3 accepted record without a PDF.
4. **Peer-reviewed-version rule** (`BACKLOG.md` "Peer-reviewed versions after ingest"): implement
   before the sweep so Q3 pages are written with the peer-reviewed link. Inputs confirmed: field
   `url_peer_reviewed`; ICASSP 2026 `conference_date: 2026-05-03`. Still pinned: frozen-date
   detection by claim-YAML presence (recommended) vs an explicit `date_frozen` flag. Backfill: the
   34 re-dated Interspeech pages (ISCA keys now in `source_ids.isca`) and the 10 frozen 2025 pages
   that are Interspeech 2026 papers (`2509.09631`, `2509.13068`, `2509.15626`, `2509.17516`,
   `2509.22167`, `2510.13293`, `2510.16718`, `2510.25577`, `2511.01056`, `2511.19734`).
5. **Held papers:** `2606.12940` and `2606.13006` move to Q3 under the rule; ingest them as Q3
   papers. `2606.13006` is already cited (accepted, no page) by `2606.28249` HPRO.
6. **Start the sweep:** pre-flight per `docs/ingest-protocol.md` section 2, then chronological
   selection by `published_date`.

**Side threads (not blocking):** duplicate page pairs in `BACKLOG.md`; OpenReview live fetches are
blocked by a browser-verification gate, so use the saved-page path (`openreview.py --from-file`).

**Cadence:** see `docs/ingest-protocol.md` section 3; follow whichever cadence the user most
recently requested (2026-10-31: decisions walked through one at a time first, then batches of 4,
one paper at a time, summary and go-ahead per batch, queue reviewed one item at a time at round
end; 2026-11-01: full-text details on request before the user overrides a recommendation;
2026-11-07: review-queue decisions in themed batches, each paper with precedents and a
recommendation; parse one batch of 40 at a time with a go-ahead between batches).

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

---

## Manual Verification Queue

Papers where the ingest agent emitted `review_flags` in its INGEST_RESULT signal. Review these
after the session batch is complete: check the paper page and resolve each flag by hand.

| Paper ID | Flag | Agent note |
|----------|------|------------|

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
