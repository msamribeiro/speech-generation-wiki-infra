# Q2 2026 Ingest Session

**Date:** 2026-08-22
**Goal:** Ingest all accepted Q2 2026 (April–June 2026) papers into the wiki.

Bootstrapped from `docs/records/2026-08-22-q1-2026-ingestion-sessions.md`, which holds the full
paper-by-paper Q1 2026 log (8 sessions, 162 papers, complete). This file carries forward the
ingestion protocol and cadence preferences refined during Q3/Q4/Q1 2026, without the historical
narrative.

---

## Scope

| Status | Count |
|--------|-------|
| Already ingested (Q2 2026) | 5 |
| Remaining to ingest (accepted) | 211 |
| Pending human triage (review) | 0 |
| Rejected | 56 |
| **Total Q2 2026 in scope so far** | **272** |

As of 2026-10-04 these counts follow the canonical paper-date rule (`docs/schemas/metadata.md#paper-dates`);
the earlier 241-accepted / 302-total figures used pre-rule dates, and the accepted count fell by a net 30 as papers moved
to other quarters; 5 older papers (2409.18512, 2502.14145, 2507.13563, 2601.04029, 2601.11329) moved in. As of 2026-09-21 (after the triage of the 18 Q2 `review` papers, 11 accepted and 7 rejected; the
counts were 230 / 18 / 49 on 2026-08-23), following the arXiv fetch top-up and ACL Anthology 2026
fetch (see Session Log). Breakdown by month (`published_date`-derived):

| Month | Accepted | Ingested | Review | Rejected | Total |
|-------|----------|----------|--------|----------|-------|
| April 2026 | 63 | 5 | 0 | 19 | 87 |
| May 2026 | 56 | 0 | 0 | 13 | 69 |
| June 2026 | 92 | 0 | 0 | 24 | 116 |

**Download and parse (2026-09-19): complete for the 230 papers `accepted` at that point** (the 11 papers
accepted later from `review`, 5 May and 6 June, still have no PDF or parse) (0 failures; 113 downloaded
and parsed on 2026-09-19, the other 117 were already done). By source: arXiv 181, ICLR 21, ACL 15,
workshop 13. Of the 5 `ingested` records, 4 are real Q2 pages (all arXiv, April); the fifth is the
ICLR record `iclr-2026-kYkfCs4ZAH`, a dedup pointer (`wiki_page_id: 2510.00981`) to a Q4 2025 page.
`2507.09318` is marked `ingested` with an April 2026 `published_date` despite a July 2025 ID prefix
(not investigated; does not change the counts).

**Fetch is now believed complete for all of Q2 2026** (April–June) across both arXiv and ACL
Anthology sources. The arXiv top-up covered `--date-from 2026-05-25` through today (2026-08-23) on
both arXiv fetchers, so June — previously entirely unfetched — is now populated, and any remaining
May gap is closed. A follow-up `acl.py --years 2026 --all-workshops` run added the ACL 2026 main
track plus 21 co-located 2026 workshops, contributing 15 Q2-dated records (1 April, 12 May, 2 June)
after a date-table fix (see below). The arXiv run also incidentally pulled July/August 2026 records
into the corpus (useful head start for the eventual Q3 2026 bootstrap, out of scope for this file).

**EMNLP 2026 and NAACL 2026 are not yet on the ACL Anthology** (no `2026.emnlp`/`2026.naacl` XML
exists yet — confirmed by dry-run, consistent with EMNLP 2026's official Oct 24–29 date and NAACL
2026's date being unconfirmed as of this session). Re-check `acl.py --years 2026 --dry-run` closer
to those dates. ICASSP 2026 still has no dedicated fetcher (`BACKLOG.md` Infrastructure section) —
raised to the user 2026-08-23, not yet resolved; ASRU/SLT are in the same gap. The 18 `review`-status
Q2 papers were triaged by the user (2026-09-20) and the scope count is now final. The 5
already-`ingested` April papers were not part of a chronological Q2 sweep — they were ingested
individually back in late May 2026, before quarterly chronological ingest sessions existed, most
likely via citation-discovery or an early top-up fetch run that happened to overlap April dates.

**Fetcher fix (2026-08-23):** `scripts/fetch/acl.py`'s conference-date table (`_CONF_META`) had no
2026 entries, so every newly-fetched 2026 record (main-track and workshop alike) got a placeholder
`published_date: 2026-01-01`/`month: None` — silently excluding them from any month-based quarter
count. Investigation traced this further back: the *workshop* half of the bug is not 2026-specific —
every co-located-workshop paper in every year gets a hardcoded `canonical_venue = "workshop"` with no
per-workshop date lookup at all, so historically only records that happened to already exist as
dated arXiv preprints (and got "enriched" with a conference ID) kept a real date; freshly-written
workshop records got the placeholder regardless of year. Fixed structurally rather than by adding
more manually-curated table rows: added a confirmed `("ACL", 2026): 2026-07-02` entry (verified
against the official conference site), and `iter_papers` now falls back to the Anthology XML's own
`<meta><month>/<year>` (present on virtually every volume, workshops included — only continuously-
rolling venues like TACL omit it) whenever no curated table entry exists. This closes the gap for
every venue and year going forward, not just ACL 2026. Verified against cached XML: SIGDIAL 2026 →
August 2026 (matches the Anthology's own listed month), ACL 2026 main → July 2026 (matches the
curated table), TACL → correctly still falls back to the placeholder (no month info exists for that
venue). Backfilled all 49 already-written 2026 records in place (`month`/`published_date` fields
only) using the fixed logic — no other fields touched. Pre-2026 years' workshop records (indeterminate
count, corpus-wide) were **not** backfilled this session — that's a larger corpus-wide correction,
worth a dedicated pass rather than folding into a Q2 fetch session.

Counts computed the same way as prior quarters, from `raw/metadata/*.json` where `year == 2026` and
`month in (4, 5, 6)` (derived from `published_date`, not the arXiv ID prefix — see the ID-prefix
note below). Re-run before starting a session, as fetch/filter status will change:

```bash
.venv/bin/python3 -c "
import json, glob
accepted, ingested, rejected = 0, 0, 0
for path in glob.glob('raw/metadata/*.json'):
    m = json.load(open(path))
    y, mo = str(m.get('year','')), str(m.get('month','0')).zfill(2)
    if y == '2026' and mo in ('04','05','06'):
        if m['status'] == 'accepted': accepted += 1
        if m['status'] == 'ingested': ingested += 1
        if m['status'] == 'rejected': rejected += 1
print(f'Ingested: {ingested} | Remaining: {accepted} | Rejected: {rejected}')
"
```

---

## Next Session — Resume Here

The Q2 sweep is under way. As of 2026-10-24 (session close), by canonical `published_date`:
**120 ingested + 104 `accepted` remaining** (all downloaded and parsed; 12 May, 92 June),
61 rejected. April is complete. This session ingested 20 papers in five batches (B-F): the rest of
the sixth round (#5-#16) and a seventh round of 8; see the 2026-10-24 Session Log. Corpus: 1,009
pages. The procedure is `docs/ingest-protocol.md` (canonical over this file's Methodology). The
Manual Verification Queue has no open items (all 14 resolved 2026-10-24; only the legacy
corpus-wide `[!note]` item remains). Content and infra commits are in `git log` (pushed at close).

To resume:

1. **Pre-select the eighth round** and include the two Q4 2025 stragglers the user wants
   ingested (2026-10-24): PACC `2605.18001` (`published_date` 2025-10-01, ICICC 2025) and
   `2605.25504` (2025-11-12, O-COCOSDA 2025). Both are accepted and parsed. They are not part of
   the closed Q4 integration; note them for explicit inclusion in the next integration cycle.
2. Then continue Q2 from 2026-05-26 onward: the next accepted records by date start with
   `2605.26978` PashtoTTS-Bench, `2605.27190`, `2605.27772` (ICML 2026, keeps arXiv date),
   `2605.27258` PilotTTS, `2605.27984`, `2605.29209`, `2605.29859` MELD. Run the full pre-flight
   (title dedup, author overlap with ingested records, `arxiv_comment`, first-page notices,
   Crossref for any proceedings or journal version).
3. Follow `docs/ingest-protocol.md` for the per-paper loop. Point agents at the content-ingest
   worktree
   (`SPEECH_WIKI_CONTENT_DIR=/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content-ingest`)
   and fill the index Org by hand (" / " between institutions; make the page string match).
   New rules from 2026-10-24 are in the protocol: `gan-vocoder` (standalone vocoder, or codec
   decoder adversarial training that is a contribution or ablated), `self-supervised-speech`
   (any SSL speech model the method uses), `zero-shot-tts` (unseen speakers only). Ask agents to
   list every superlative with its supporting table cells (cured the recurring over-broad
   "best" claims). No PDF renderer is installed; agents work from the parse and table PNGs, and
   several runs took 15-100 minutes of wall time with ordinary tool counts.

**OpenReview (side thread, not blocking ingest):** live fetches are blocked by a browser-verification
gate, so use the saved-page path (`openreview.py --from-file`; the user saves the API pages from a
browser). The 20 ICML 2026 candidates (Q3) are written, filtered and, for the 2 accepted, parsed (see
the 2026-09-21 continuation entry); they are ready to ingest whenever Q3 is reached. OpenReview PDF
downloads are behind the same gate, so an OpenReview-only paper needs its PDF saved by hand from
`openreview.net/pdf?id=<forum id>` into `raw/papers/{id}.pdf`. NeurIPS 2026 had no accepted papers
posted on 2026-09-21; re-save its pages later and run the same way.

**Cadence:** see `docs/ingest-protocol.md` section 3; follow whichever cadence the user most
recently requested (this session: one at a time, summary and go-ahead per batch of 4).

---

## Success Criteria

- All accepted Q2 2026 papers have `status: ingested` in `raw/metadata/`
- Health check passes corpus-wide with zero errors:
  ```bash
  .venv/bin/python scripts/health_check.py --module ingest --wiki-dir /Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content
  ```

---

## Methodology

The procedure (cadence, per-paper cleanup and QC, tagging rules, claims format, interruption
recovery, commit workflow) is canonical in `docs/ingest-protocol.md` and the ingest `SKILL.md`.
This section keeps only what is specific to the Q2 2026 sweep: scope precedents and gaps.

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
`2604` prefix) — expect the mirror-image case in Q2 2026 (a `2603.xxxxx`-prefixed paper that is
actually April/May/June by `published_date`) and sort by date every time, never by ID prefix.

### Known open vocabulary gap

No canonical vocabulary term currently covers non-text-input speech generation (brain-signal
decoding, lip-to-speech, audio-continuation-only systems). The gap applies only when there is no
text input: text-driven TTS with visual or other non-text conditioning (e.g. sign-video prosody in
`2604.10413`, video prosody in `interspeech-2025-1494`, face-based voices) is plain `TTS`, not a
fallback. A possible `V2S`-style task term is a deferred `BACKLOG.md` item (2026-10-17). Several Q3/Q4/Q1 2026 papers were tagged
`TTS` as the closest fit pending a user decision on whether to add a dedicated term (e.g.
`2602.11477`, lip-to-speech, applied the standing fallback explicitly in Q1 2026). If this recurs in
Q2 2026, tag `TTS` as the same fallback and flag it in the Manual Verification Queue rather than
inventing a new term unilaterally.

---

## Session Log

### 2026-08-23 — Fetch top-up (no ingest yet)

User asked to top up fetch/filter this session and pause before ingesting. Ran both standard
fetchers with `--date-from 2026-05-25` (default `--date-to` is today, 2026-08-23):

- `arxiv.py` (cs.SD + eess.AS): 1337 discovered, 226 passed filter, 213 written, 13 skipped existing.
- `arxiv_oai.py --set cs.CL`: 10,077 discovered, 125 passed filter, 40 written, 85 skipped existing.

253 new `pending` records total. Ran `speech-generation-filter-agent` on all of them: 185 accepted,
35 review, 33 rejected (73% accept rate); logged to `raw/pipeline_log.md` under `## 2026-08-23`, 35
new entries appended to `raw/review_queue.md`. Verified independently: 0 pending records remain
corpus-wide.

Net effect on Q2 2026 scope: June 2026 went from 0 records to 124 (95 accepted); May grew from 50 to
63 total; April unchanged. The run also incidentally reached into July/August 2026 (out of Q2 scope,
left as-is for a future Q3 2026 bootstrap). ICASSP 2026 fetcher gap confirmed still open in
`BACKLOG.md`, raised to the user, not resolved this session.

Not committed yet — `raw/metadata/*.json` (253 new + all touched), `raw/review_queue.md`,
`raw/pipeline_log.md`, and this file are all modified/untracked pending a commit decision.

### 2026-08-23 (continued) — ACL Anthology 2026 fetch + date-fetcher fix

User asked whether conference/workshop venues needed a separate top-up beyond the arXiv sweep above.
Dry-run survey found: ACL 2026 main track and 2026 workshops already have real content on the
Anthology (unfetched by our last `acl.py` run, which defaulted to years=[2025]); Interspeech 2026
not yet published (404); ICLR 2026 top-up blocked by a 403 from OpenReview's API after retries
(inconclusive, not actionable); NeurIPS 2026 not yet code-configured in `openreview.py`.

Ran `acl.py --years 2026 --all-workshops` for real: 32 new + 53 arXiv→conference enrichments, 0
errors. Filter agent on the 49 new `pending` records: 31 accepted, 8 review, 10 rejected. Verified:
0 pending remain corpus-wide.

While reviewing the new records, found all 49 had a placeholder `published_date: 2026-01-01`/
`month: None` — traced to a genuine fetcher gap (see the Scope section above for the full writeup
and fix). Fixed `scripts/fetch/acl.py` to fall back to the Anthology XML's own `<meta><month>/<year>`
when no curated `_CONF_META` table entry exists, added a verified `("ACL", 2026)` table entry, and
backfilled the 49 already-written records' `month`/`published_date` fields in place. Verified the
fix against cached XML for both a main-track and a workshop volume before backfilling.

Not committed yet — same pending-commit state as the entry above, plus `scripts/fetch/acl.py` and
the 49 backfilled `raw/metadata/2026.*.json` files.

### 2026-08-23 (continued) — NeurIPS 2026 OpenReview: config fixed, fetch blocked

Investigated the ICLR/NeurIPS 2026 issue flagged in the previous entry. Two distinct problems:

1. **NeurIPS 2026 was a real code gap** (same shape as the ACL 2026 date-table gap above):
   `scripts/fetch/openreview.py`'s `_VENUE_TABLE` had no `("NeurIPS", 2026)` entry at all, so the
   script failed immediately with `Unsupported venue/year` before any network call. Looked up the
   real values and added them: venue ID `NeurIPS.cc/2026/Conference` (confirmed live on OpenReview),
   conference start date `2026-12-06` (Sydney, primary venue; satellites in Atlanta and Paris run
   slightly later). **Fixed, not yet committed.**
2. **Both ICLR 2026 and NeurIPS 2026 live fetches are blocked**, and this is not a per-venue problem.
   After the config fix, a NeurIPS 2026 `--dry-run` hit the identical failure as the earlier ICLR 2026
   check: `403 Forbidden` from `api2.openreview.net`, on every one of 5 retries with exponential
   backoff (10s → 160s), then gave up. Two different, independently-configured venues failing
   identically points to OpenReview rate-limiting or blocking this session/IP after the volume of API
   calls made tonight (across arXiv, ACL Anthology, and OpenReview fetchers) — not a broken venue ID
   or a "nothing new yet" signal. Deliberately did not keep retrying, to avoid extending any block.

**Superseded 2026-09-21:** the rate-limiting diagnosis above was wrong (it is a browser-verification
gate; waiting does not help). See the 2026-09-21 entry for the corrected diagnosis and the
`--from-file` workaround.

**Original resume note (obsolete):** re-run `openreview.py --venue ICLR --year 2026 --dry-run` and
`--venue NeurIPS --year 2026 --dry-run` first, before anything else OpenReview-related. If still
403ing, the block hasn't cleared — wait longer rather than retrying repeatedly. If it succeeds,
proceed to a real (non-dry) fetch for both, then run the filter agent on whatever's new, same
pattern as the ACL 2026 batch above.

### 2026-08-23 (continued) — Global fetch status snapshot (corpus-wide, not just Q2)

Requested end-of-session snapshot before committing. Corpus totals: 1,628 metadata records — 908
ingested, 333 accepted (awaiting ingest), 43 in review, 344 rejected, 0 pending.

| Source | Records | Years covered | Notes |
|---|---|---|---|
| arXiv (cs.SD, eess.AS, cs.CL) | 1,191 | 2014–2026 | Continuous through today (2026-08-20 latest), topped up this session |
| Interspeech (ISCA) | 142 | 2025 only | 2026 not yet published (404 confirmed this session) |
| ACL Anthology (ACL/EMNLP/NAACL/Findings + workshops) | 234 | 2024–2026 | 2026 main track + 21 workshops added this session; EMNLP 2026/NAACL 2026 not on Anthology yet |
| ICLR (OpenReview) | 40 | 2025–2026 | 2026 top-up blocked this session (403, likely rate-limit) |
| NeurIPS (OpenReview) | 16 | 2025 only | 2026 fetcher just fixed, but hit the same 403 block before any data came through |
| One-offs (ICASSP, ASRU, NCMMSC, ICML, IJCNLP-AACL) | 5 | scattered | Incidental (citation-discovery or arXiv cross-listed), no dedicated fetcher |

Known gaps, roughly in priority order:
1. ICASSP, ASRU, SLT — no dedicated fetcher exists at all (`BACKLOG.md` P1).
2. ICLR 2026 / NeurIPS 2026 top-up — blocked by OpenReview 403s, see entry above, resume next session.
3. EMNLP 2026 / NAACL 2026 — not yet posted to the Anthology (EMNLP 2026 is Oct 24–29; NAACL 2026 date unconfirmed).
4. 24 pre-2026 workshop records still carry the placeholder-date bug fixed this session — tracked in `BACKLOG.md`, not urgent.
5. 43 total review-queue papers awaiting human triage corpus-wide (18 of these are Q2-scoped).

Next steps for future sessions, roughly in order: retry the OpenReview fetch once unblocked; triage
the review queue (at least the 18 Q2-scoped entries) before treating Q2 scope as final; start the Q2
2026 chronological ingest sweep (230 accepted papers, standard batches-of-4 cadence) — this was
paused pending this session's fetch top-up; whenever convenient, the ICASSP/ASRU/SLT fetcher gap and
the pre-2026 workshop-date backfill are both real but non-blocking.

### 2026-09-19 — Q2 status review, then download + parse of all accepted papers

No ingest, no wiki (content repo) changes. Started as a status review and turned into finishing the
download and parse stage for Q2.

- **Fetch gap analysis (Q2 only):** none for arXiv or ACL Anthology (no weekly holes in arXiv
  coverage April onward). ICLR 2026 is fully in the corpus (27 records). Outside Q2 for reference:
  arXiv is fetched only through 2026-08-20, so late August onward is unfetched for Q3 2026, and
  `isca-archive.org/interspeech_2026/` returned 404.
- **Found:** only 117 of the 230 accepted Q2 papers had a PDF and parse (the 08-23 top-up added
  metadata only); the 98 accepted July–August papers had none.
- **`download_pdfs.py`:** had no way to scope to one quarter (it takes every accepted paper), so
  added `--published-from` / `--published-to` (filters on `published_date`). Used to keep the run to
  Q2 and skip Q3.
- **`acl.py` bug found and fixed:** the first download attempt aborted on 5 consecutive 404s. The
  LREC 2026 volume's Anthology XML lists an external `https://lrec.elra.info/...` `<url>`, and
  `acl.py` prefixed the Anthology base onto it (`https://aclanthology.org/https://lrec...`). Affected
  LREC 2026 main, SIGUL, CAS, DialRES, and PoliticalNLP records. `acl.py` now falls back to the
  canonical Anthology ID (`{collection}-{volume}.{paper}`) when the XML URL is absolute. Repaired
  `pdf_url` (and `url` where it carried the same defect) in place on 17 records (9 accepted, 6
  rejected, 2 review), deriving each canonical ID from the cached XML; diff verified to touch only
  those URL lines. Canonical `aclanthology.org/{id}.pdf` URLs return 200.
- **Download:** 113/113 Q2 PDFs downloaded, 0 failed.
- **Parse:** 113/113 parsed, 0 failed, `--workers 2`, 204 minutes (about 1.8 min per paper; the first
  papers finished much faster than the average, so do not extrapolate from an early rate). Post-parse
  check on all 230 accepted Q2 papers: `paper.md` present, at least 100 lines, non-empty
  `references.json`, 0 flagged. This checks output files, not paper-by-paper content.
- **Citation index** rebuilt: 22,427 entries, 1,169 corpus papers.
- **Review queue:** located the 18 Q2 entries in `raw/review_queue.md` (see Next Session). The user
  will triage offline; nothing applied.
- **Repo state at close:** all of the above committed on infra `work/ingest` (`2729cd2`), one commit
  ahead of `main`, **not merged or pushed** (user's choice). The trunk checkout on `main` had another
  stream's uncommitted work (`BACKLOG.md`, `STATUS.md`, `Q4_INTEGRATION_SESSIONS.md`), which is why
  the merge was held. That work was committed to `main` as `d273f06` before session close, and a
  read-only `git merge-tree` dry run confirmed `work/ingest` merges into it cleanly (both sides
  edited `BACKLOG.md`, in different hunks). Content and site repos untouched. The user was also
  editing `raw/review_queue.md` in this worktree (offline triage ticks, uncommitted) at close: leave
  it alone until they say the decisions are final, then apply them to metadata. Earlier this same session `work/ingest` was
  merged into `main` and pushed (`ab0bfb0`, then a `BACKLOG.md` update `df5176b`), and both ingest
  worktrees were fast-forwarded and their `wiki/` submodule checkout updated.

### 2026-09-20 — Review triage applied, publication dates verified, conference_date repaired

Commit `5f87b1b`. No ingest, no wiki (content repo) changes.

- **The review pool was 43, not 18.** The 18 was the Q2-window count (by `published_date`); the full
  `status: review` pool from the 08-23 filter runs was 43 (35 arXiv/cs.CL, 8 ACL Anthology), 25 of them
  outside Q2 (4 Feb, 14 Jul, 7 Aug). The user ticked all 43 in `raw/review_queue.md`; applied to
  `raw/metadata/` status: **29 accepted, 14 rejected**. By `published_date`: Feb 4A/0R, May 5A/1R,
  Jun 6A/6R, Jul 8A/6R, Aug 6A/1R. Q2 window after triage: 241 accepted, 0 review, 56 rejected.
- **The 29 newly accepted papers have no PDF or parse yet:** 11 in Q2 (5 May, 6 Jun), 14 in Q3
  (8 Jul, 6 Aug), 4 IWSDS 2026 (Q1 stragglers, Q1 is already archived).
- **Dates verified.** The 22 arXiv-sourced accepted papers match the arXiv API `published` date
  exactly (including `2606.27380`, genuinely submitted 2026-05-11 despite its June-style ID). The 7
  Anthology-only papers match their XML volume month (IWSDS 2026 = February 2026, Trento; DialRES and
  LREC = May; NLPAICS = June), with day 01 by convention.
- **`conference_date` repaired.** 65 records carried a placeholder `2026-01-01` / `2025-01-01` (written
  before the date-table fix). Replaced with the Anthology XML volume month, day 01 (ACL and Findings
  2026 -> 2026-07-01, LREC -> 05-01, EACL -> 03-01, IWSDS 2026 -> 02-01). 12 records were XML-confirmed
  January (CHUM, CLTW, COLING 2025, MCG) and left alone. `month` was not touched: on arXiv-sourced
  records it is the arXiv publication month by design. The field has no readers in scripts or the wiki,
  so quarter counts were never affected. The fetcher's curated table has ACL 2026 at 2026-07-02, so
  newly fetched ACL 2026 records read 07-02 while the repaired ones read 07-01 (same month).
- **Left out of the commit:** `.gitignore` and the `openreview.py` change (handled in the 2026-09-21
  entry below).
- **Repo state at close:** committed on infra `work/ingest`, **not merged or pushed** (standing hold,
  see the 2026-09-19 entry).

### 2026-09-21 — OpenReview block: diagnosis, fail-fast, saved-page import, ICML 2026

No ingest, no wiki (content repo) changes. Earlier the same day a separate step (`5f87b1b`) applied the
user's triage of all 43 `review` papers (29 accepted, 14 rejected) and repaired 65 placeholder
`conference_date` values; see `raw/pipeline_log.md` and its commit message. That step left the Q2
window at 241 accepted, 56 rejected, 5 ingested, with **11 newly accepted Q2 papers still lacking a
PDF and parse** (29 across all quarters).

- **Correction to the 2026-08-23 entry above:** the ICLR/NeurIPS 2026 403s are not rate limiting.
  Anonymous scripted `GET /notes` on `api2.openreview.net` returns `403 ChallengeRequiredError`
  ("Challenge verification required", with a `challengeUrl`), a browser-verification gate. The
  rate-limit counter is untouched (179/180), so waiting and retrying cannot help.
- **What was ruled out:** the fetcher (raw `curl` fails identically), the User-Agent, the client
  library (the official `openreview-py` anonymous client gets the same error), the venue year
  (ICLR 2025 and NeurIPS 2025 are gated too), and this network (a phone hotspot is gated too). A real
  browser passes the check in a few seconds, in a normal and an incognito window, with no login.
- **Timing is unknown:** the last successful live OpenReview fetch was **2026-06-05** (all 56
  OpenReview records carry that `fetched_date`; the 06-29 date in `BACKLOG.md` was the local dedup
  pass). The gate appeared sometime between then and 08-23. No announcement was found and the cause is
  not established.
- **`openreview.py` changes:** (1) `or_get` raises `OpenReviewChallengeError` at once on a
  `ChallengeRequiredError` 403 instead of retrying for about 5 minutes; `main` exits with code 2 and
  no `fetch_log.jsonl` entry is written. (2) New `--from-file` mode reads `/notes` pages saved from a
  browser (`limit=1000`, `offset` stepped by 1000, `sort=cdate:asc`) and feeds them through the normal
  parse, keyword filter and skip-existing path. It keeps only notes whose `venueid` matches, drops
  duplicate note IDs, and warns when fewer notes load than the API's `count` (a missing page).
  (3) ICML added to the venue table: `ICML.cc/2026/Conference`, `2026-07-06`, month 7 (ICML 2026 is
  July 6-11, Seoul), which puts it in Q3 2026, not Q2. Workshops are not covered (each has its own
  venue ID; the table and `venue_type` are conference-only).
- **Validation, dry run only:** ICLR 2026 loaded 5,351 notes from 6 saved pages, 27 passed the
  filter, all 27 already in the corpus, so the saved-page path reproduces the June live fetch exactly
  and ICLR 2026 needs nothing more. ICML 2026 loaded 6,341 notes from 7 pages, 20 passed the filter,
  0 existing. Dropping one page correctly triggers the incomplete-coverage warning. NeurIPS 2026's
  first page came back empty as of 2026-09-21 (accepted papers not posted yet).
- **Not done at this point (superseded by the continuation entry below):** the 20 ICML 2026 records
  had not yet been written. A credentialed `openreview-py` login was never tested (no account); it is
  unverified whether a token would pass the gate.
- **Repo state at close:** the `openreview.py` and doc changes are committed on infra `work/ingest`,
  ahead of `main`, **not merged or pushed** (see the standing hold in the 2026-09-19 entry).

### 2026-09-21 (continued) — ICML 2026 written, filtered and deduplicated

- **Written:** 20 ICML 2026 records as `pending` (`openreview.py --venue ICML --year 2026
  --from-file`, `published_date` 2026-07-06, so Q3 2026).
- **17 of the 20 already existed under arXiv IDs** (title match): 7 with an ingested wiki page, 8
  `accepted` but not ingested, 2 `rejected`. Only DropoutTS, AgentSteerTTS and TAC had no arXiv twin.
- **Decision (user, 2026-09-21): the arXiv record stays canonical.** The 17 ICML records were flagged
  `is_duplicate: true`, `canonical_id` set to the arXiv ID, `status: rejected` (the same shape as the
  existing losing-side records), and not re-scored; the arXiv record carries the relevance decision.
  This reverses the proceedings-over-arXiv direction of `scripts/fetch/dedup_openreview.py` for these
  papers, which also does not cover the `icml-2026-` prefix. Reasons: the arXiv copies already have
  PDFs, parses, wiki pages and correct Q2 dates (four of the eight accepted ones are Q2 papers that
  would have moved to Q3), and an OpenReview-canonical record would have needed a hand-saved PDF for
  six of them. There is no precedent in the corpus for an accepted-but-not-ingested arXiv copy meeting
  a proceedings record (the earlier ICLR/NeurIPS collisions were all ingested copies).
- **Scored (3):** AgentSteerTTS `icml-2026-hgKQemfVbS` 0.92 TTS accepted; TAC
  `icml-2026-icMRkTnuU7` 0.88 codec+TTS accepted (general-audio tokenizer with speech results and a
  purely autoregressive TTS model built on it); DropoutTS `icml-2026-7sksHLUvhH` 0.03 rejected
  (time-series forecasting, no audio). Logged in `raw/pipeline_log.md`. Final status of the 20: 2
  accepted, 18 rejected (17 duplicates, 1 off-topic).
- **PDFs:** `openreview.net/pdf?id=...` returns the same 403 challenge page to scripts, and neither
  accepted paper is on arXiv (title search). The user saved both PDFs from a browser; each was checked
  against its first-page text (TAC 22 pages, AgentSteerTTS 19), filed as `raw/papers/{id}.pdf`, and
  `pdf_path` set (`needs_manual_pdf` cleared).
- **Parse:** both done, 0 failed, `--workers 2`, 645 s total. `paper.md` 744 lines / 96 references
  (TAC) and 474 lines / 47 references (AgentSteerTTS). This checks output files, not content. Corpus
  parse status: 232 done, 0 failed, 0 pending.
- **Cleanup:** the scratch directory `tmp/` (13 saved API pages, about 93 MB, plus the two PDFs) was
  removed; the PDFs were verified byte-identical to the filed copies and every record the pages
  produced already exists. To repeat an import, save the pages again (workflow in the entry above).
- **2026 status by quarter, end of session** (by `published_date`; accepted = accepted + ingested; the
  dedup pointer `iclr-2026-kYkfCs4ZAH` is not counted; downloaded and parsed checked on disk):

  | | Q1 | Q2 | Q3 (partial) |
  |---|---|---|---|
  | Records / rejected | 237 / 66 | 302 / 56 | 157 / 43 |
  | Accepted | 171 | 245 | 114 |
  | Downloaded / parsed | 162 / 162 | 234 / 234 | 2 / 2 |
  | Ingested | 162 | 4 | 0 |
  | Awaiting ingest (parsed and ready / need PDF) | 9 (0 / 9) | 241 (230 / 11) | 114 (2 / 112) |

  Total awaiting ingest across 2026: 364, of which 232 are parsed and ready. The parse tool's count of
  accepted papers with no PDF is 132 (9 + 11 + 112), which matches.
- **Finding: Q1 2026 is not fully closed.** It was archived on 2026-08-22 as 162 ingested / 0
  remaining, but the ACL Anthology 2026 fetch of 2026-08-23 added 9 accepted workshop papers dated
  Feb-Mar (5 IWSDS 2026, published 2026-02-01, plus `2026.abjadnlp-1.6`, `2026.africanlp-main.23`,
  `2026.eacl-short.16`, `2026.loreslm-1.54`). None has a PDF. Tracked in `BACKLOG.md`.
- **Q3 is partial on the fetch side:** latest `published_date` is 2026-08-20, nothing from September,
  Interspeech 2026 not yet on ISCA, no ICASSP/ASRU/SLT fetchers. Tracked in `BACKLOG.md`.
- **Known follow-ups, unchanged:** the 7 ingested wiki pages still cite only the arXiv version, not
  ICML acceptance (the deferred venue-migration item in `BACKLOG.md`); `dedup_openreview.py` still
  lacks the `icml-2026-` prefix; the fetcher's keyword filter passed 20 of 6,341 ICML papers and was
  not checked for misses.

### 2026-09-27 — Download + parse of 20 pending papers; Q1 stragglers ingested, Q1 fully closed

- **Download + parse:** ran `download_pdfs.py --published-from 2026-02-01 --published-to 2026-06-30`
  (dry-run confirmed scope first) for the combined set of 9 Q1 stragglers + 11 Q2 review-triage
  papers — 20 downloaded, 0 failed. Then `batch_convert.py --workers 2 --ids ...` for the same 20 —
  20 done, 0 failed, 12.0 min. The 11 Q2 papers are now parked as `accepted`/parsed/ready; only the 9
  Q1 stragglers were ingested this session (see below).
- **Ingested the 9 Q1 stragglers** in three batches (4 / 4 / 1), standard one-paper-at-a-time cadence
  with a health check after each: `2026.iwsds-1.3`, `2026.iwsds-1.4`, `2026.iwsds-1.9`,
  `2026.iwsds-1.10`, `2026.iwsds-1.16`, `2026.abjadnlp-1.6`, `2026.africanlp-main.23`,
  `2026.eacl-short.16`, `2026.loreslm-1.54`. Corpus 900 → 909. Final health check pass on all 9: 0
  errors, 0 warnings.
- **QC catches:** `2026.iwsds-1.10` left 3 bare `[[id]]` wikilinks unfixed by the ingest agent
  (caught by the post-ingest health check, corrected by hand). `2026.abjadnlp-1.6` and
  `2026.eacl-short.16` each self-caught and fixed their own bare-wikilink warnings before reporting
  done. All in-corpus references cited by the 9 pages were spot-checked to confirm the target page
  actually exists.
- **Manual Verification Queue resolved:** `2026.iwsds-1.16` (virtual standardized patient / Nova
  Sonic pilot) came back with a `field_significance` review flag — moderate vs. low boundary, per the
  agent's own note (narrow 20-participant single-model pilot with no comparison group, but its
  role-confusion/over-disclosure failure modes plausibly generalize beyond the specific application).
  Reviewed and downgraded to **low** in both frontmatter and the Field Significance prose section;
  re-ran health check, still 0 errors / 0 warnings.
- **Q1 2026 is now fully closed**, stragglers included: 171 accepted, 171 ingested, 0 remaining.
- **2026 status by quarter, end of session** (by `published_date`; accepted = accepted + ingested):

  | | Q1 | Q2 | Q3 (partial) |
  |---|---|---|---|
  | Accepted | 171 | 245 | 114 |
  | Downloaded / parsed | 171 / 171 | 245 / 245 | 2 / 2 |
  | Ingested | 171 | 4 | 0 |
  | Awaiting ingest | 0 | 241 (all parsed and ready) | 114 (112 need a PDF) |

  Total awaiting ingest across 2026: 355, of which 353 are parsed and ready — Q2's chronological
  ingest sweep (241 papers) is next, per `BACKLOG.md`.

### Session 2026-10-16: paper-date migration and task/related_concepts QC (no ingest)

No papers ingested; this session got the branch ready for the Q2 sweep.

- **Paper-date rule applied from 2026 onward** (decision: leave 2025 and earlier as-is). Added
  `--ingested-from` to `scripts/apply_date_rule.py`; migrated 175 ingested metadata records and synced
  `published_date`/`month` on 39 paper pages. 39 `published_date` changes; 15 papers moved from
  2026-Q1 to Q2. No claim YAML carries 2026 dates. First page-sync rewrote date quoting on 164 pages;
  caught from the diff, reverted, and fixed to preserve each page's quoting style.
- **2026 quarter counts after the rule:** Q1 156 ingested; Q2 19 ingested + 211 accepted; Q3 144
  accepted (only the 2 ICML papers downloaded and parsed).
- **`related_concepts_complete` health check added** (`scripts/checks/ingest.py`, mapping in
  `config/health_check.yaml`). Baseline across 909 pages: 13 task-tag hits plus about 227 architecture-tag
  hits, which were mostly intentional (component-level GAN/diffusion/flow usage), so the config maps
  `task` only.
- **13 task hits resolved.** Slugs added (with Wiki Connections entries): `singing` on
  `2025.findings-acl.687`, `2310.00704`, `2508.01796`, `2508.16332`, `2512.14653`,
  `interspeech-2025-0305`; `voice-conversion` on `2502.06490`; `neural-codec` on `2512.00451`.
  Unsupported tags dropped (frontmatter and index row): `VC` on `2409.00750`, `2304.09116`,
  `2504.18425`, `2509.24650` (demo-only or no VC metrics); `singing` on `2507.12197` (future work
  only). These pages are not yet in the `singing`/VC claim YAML; the next integration pass picks them up.
- **Branch hygiene:** content `work/ingest` was one commit behind `main` (missing the 9 straggler
  pages); rebased before the work above landed.

### Session 2026-10-17: Q2 sweep started

Pre-selected the first 16 candidates by `published_date` (2026-04-01 to 2026-04-14). Wiki writes go
to the `speech-generation-wiki-content-ingest` worktree (`work/ingest`) via `SPEECH_WIKI_CONTENT_DIR`.

**Batch 1** (`2026.propor-1.81`, `2409.18512`, `2604.06327`, `2604.06356`): all four ingested, health
check clean per paper, page count 909 → 913 (index counts verified independently each paper).

- `2026.propor-1.81` (Certas Palavras, PROPOR): dataset paper, in scope (fine-tunes YourTTS/F5-TTS,
  27-rater MOS). Agent caught a σ mismatch in the source (Table 4 1.77 vs §5 1.17), verified.
- `2409.18512` (ExpPro): v1 2024-09, fetched version 2026-04-03, no full-version comment, no title
  duplicate. Fixed page `organization` to match the index row (Kuaishou co-affiliation).
  `autoregressive-codec-tts` kept: consistent with CosyVoice/GPT-SoVITS-based pages.
- `2604.06327` (speaker drift detection): arXiv comment says ICASSP 2026, but `published_date` is
  the arXiv date (no ICASSP fetcher). Left as-is pending a user decision. Only two
  `related_concepts`; `diffusion-tts`/`zero-shot-tts` judged mis-tags (no TTS system trained or
  evaluated).
- `2604.06356` (ICL in SpiritLM): in scope, `spoken-language-model` justified (HuBERT-unit speech
  input). Agent worded the ablation claim to §5.2 ("substantial drop") rather than the abstract's
  "completely removes".
- `references.json` `in_corpus` flags missed most real matches on 3 of 4 papers; agents matched by hand.
- **Pre-existing duplicate found:** MELLE has two ingested pages, `2407.08551` (arXiv) and
  `2025.acl-long.65` (ACL), neither flagged `is_duplicate`. User deferred the fix; tracked in
  `BACKLOG.md` (Wiki Quality Improvements).
- **User decisions:** leave the `2604.06327` ICASSP date as the arXiv date for now; keep both
  flagged `field_significance` levels as set.

**Batch 2** (`2604.07467`, `2604.16456`, `2604.08363`, `2604.08709`): all four ingested, health check
clean per paper, page count 913 → 917. Q2: 27 ingested, 203 accepted remaining.

- `2604.07467` (lexical tone in discrete units, Edinburgh): analysis-of-existing-speech shape (2512.16832
  precedent), no TTS trained; `task: [TTS, codec]` kept as closest terms with `neural-codec`. Arxiv
  comment says Speech Prosody 2026; date left as arXiv (same decision as the ICASSP case). Agent's
  report claimed bare `[[id]] (descriptor)` paper links "per the skill template"; the file actually had
  piped links. The SKILL.md Wiki Connections template still shows the bare form; later prompts
  override it explicitly.
- `2604.16456` (EchoChain, Labelbox): full-duplex benchmark of four closed realtime models, accepted on
  the AURA/VoiceAgentBench precedent. `subjective-evaluation` verified: a real paired human listening
  study (240 ratings) on the cloned user voices.
- `2604.08363` (CapTalk): architecture figure embedded and eyeballed. FlexiVoice
  (`iclr-2026-F7GmbfyVg9`, accepted, no page) kept in `related_papers`, de-linked. Agent reported the
  `references.json` in_corpus step returned null flags for this paper.
- `2604.08709` (Meta, cascaded prompting + online RL): AR semantic-token model + frozen diffusion
  acoustic model; `autoregressive-codec-tts` kept (consistent with CosyVoice tagging), `diffusion-tts`
  omitted (diffusion stage frozen, not trained). CMOS values, 50 crowd / 5 expert raters, and
  the Table 2 CI verified against the source.

**Batch 3** (`2605.27376`, `2605.27383`, `2604.10065`, `2604.10413`): all four ingested, health check
clean per paper, page count 917 → 921. Q2: 31 ingested, 199 accepted remaining.

- `2605.27376`, `2605.27383`: 2605 ID prefix with April dates (`version_estimated: true`); verified
  against the arXiv API (2026-04-09 / 2026-04-10), so the dates stand.
- `2605.27376` (Sungkyunkwan, training-free style interpolation and KV-cache swap on Parler-TTS-mini):
  Figure 5 embedded and eyeballed; 15 human participants verified.
- `2605.27383` (BUPT, synthetic-data scaling + DPO for Thai/Lao on CosyVoice 2): agent wrote 5
  "internal inconsistencies" into the warning callout; 2 were wrong (8,000 total vs 4,000 per language
  is consistent; NMOS differences are across standard-TTS vs zero-shot settings, not "the same test
  set"). Rewrote the callout to keep the real ones (TSynC-2 listed in training vs held out; α=100% 0h
  vs fixed 300h; Figure 2 labels). Metadata `task` still says `[TTS, SCA]`; page and index use `[TTS]`.
- `2604.10065` (ASPIRin, NTU, GRPO on Moshi): text claims a uniform 1-7% TOR reduction but Table 1
  shows synthetic pause-handling TOR rising 0.467 → 0.482; verified, the page avoids the claim.
  `rlhf-speech` for rule-reward GRPO follows `2511.21270` precedent.
- `2604.10413` (Keio, sign-to-speech prosody transfer, ICPR 2026): non-text-input vocabulary gap,
  `task: [TTS]` fallback applied and flagged. Two architecture figures embedded and eyeballed.
- **Second pre-existing duplicate:** SALM-Duplex has pages under both `2505.15670` and
  `interspeech-2025-0874`; added to the deferred `BACKLOG.md` duplicate item alongside MELLE.

**Batch 4** (`2604.10580`, `2604.11424`, `2604.11803`, `2604.12383`): all four ingested, health check
clean per paper, page count 921 → 925. Q2: 35 ingested, 195 accepted remaining. This completes the
first 16 pre-selected papers (published 2026-04-01 to 2026-04-14).

- `2604.10580` (CAST discourse-stress benchmark, HUJI/IBM): `prosody-control` and
  `instruction-conditioned-tts` kept (the benchmark's explicit-markup and instruct modes directly test
  stress control); 3 human listeners and WhiStress κ = 0.32 verified.
- `2604.11424` (SA-SLM, CUHK-Shenzhen/Tencent): `SCA` kept (Whisper-encoded user speech into a
  Qwen2.5-Omni Thinker, empathetic spoken dialogue). `disentanglement` verified against the bar
  (explicit VIB objective §3.1.2, Table 6 ablation, linear probe). No `subjective-evaluation`: all
  "subjective" scores are Gemini-judge. Figure 2 embedded and eyeballed.
- `2604.11803` (Saar-Voice dialect corpus, DialRes-LREC26): trains and evaluates no model; TTS
  experiments are future work. Kept as ingested on the VietNormalizer framing-plus-infrastructure
  precedent (TTS-purposed, released resource), `low`, `related_concepts: []` (16 existing pages
  have the same). Page `task: [TTS]` vs metadata `[TTS, evaluation]`. Raised to the user.
- `2604.12383` (speech VAE distillation, SJTU/ByteDance): `codec` + `neural-codec` for a continuous
  VAE; `TTS` + `flow-matching` kept because the paper trains F5-TTS on each representation. Table 1
  values verified. Agent run took about 3.5 hours wall-clock; no stray writes (git status checked).

**Close:** content `6f330ea` and infra `599e24b` pushed to `main` (both fast-forwards; infra pushed
as `work/ingest:main` because the trunk infra checkout is 16 behind origin with the integrate
stream's uncommitted Q4 edits, left untouched). Site bumped to `6f330ea` at the user's request
(`83734cc`), which also deployed the Q1 stragglers, date-rule sync and task-tag fixes.

### Session 2026-10-18: second round of 16 pre-selected

**Pre-selection** (by `published_date`, 2026-04-17 to 04-24), as 4 batches:

- A: `2604.15923`, `2604.16056`, `2604.16287`, `2604.17435`
- B: `2601.04029`, `2604.14548`, `2604.17958`, `2604.15804`
- C: `2604.16211`, `2605.00861`, `2604.12456`, `2604.20842`
- D: `2604.19055`, `2604.21481`, `2604.21406`, `2604.22225`

**Full-version / dedup check on the two Q1 movers:**

- `2601.11329` (F-Actor) duplicates the Findings of ACL 2026 record `2026.findings-acl.242`
  (same authors, "Behaviour"/"Behavior" title variant). Per the ACL precedent (F5-TTS
  `2025.acl-long.313`), the proceedings record is canonical: `2601.11329` set `rejected`,
  `is_duplicate: true`, `canonical_id: 2026.findings-acl.242` (user approved). The Anthology PDF was
  downloaded and parsed (`raw/parsed/2026.findings-acl.242/`); it is Q3 (published 2026-07-02) and
  will be ingested in the Q3 sweep. `2604.22225` (TTS-PRISM) took its slot.
- `2601.04029` (SpeakerSleuth): no duplicate in metadata, review queue or wiki. `arxiv_comment` says
  "Accepted at ACL 2026 (Main)" but no Anthology record exists yet, so the arXiv ID stays canonical;
  if the Anthology record appears later, it is the same duplicate case.

**Batch A** (`2604.15923`, `2604.16056`, `2604.16287`, `2604.17435`): all four pages clean on the
per-paper health check; page count 925 → 929 (files and index rows agree, all 3 `index.md`
occurrences fixed by hand). Q2: 39 ingested, 191 accepted remaining. Org filled by hand on all four
rows (`organization` null in metadata). All wikilinked and `related_papers` targets have pages and
are `ingested`. Abstract callouts are `[!abstract]`. Unquoted frontmatter dates on three pages (and
the generation `date` on all four) quoted by hand after the batch. Health checks ran at batch end
rather than per paper; follow the per-paper order from batch B.

- `2604.15923` (HiCoDiT video-to-speech, Fudan): text-free video-to-speech is in the known vocabulary
  gap, so `task: [TTS]` is the fallback (flagged). No `codec`/`neural-codec` (uses MaskGCT's
  pretrained codec). Real inconsistencies recorded: text claims UTMOS/WER lead that FTV beats on
  several splits.
- `2604.16056` (AST training-free speech editing, ZJU): `hybrid` (AR semantic LM + DiT flow-matching
  decoder); `evaluation-metrics` for the proposed WDTW metric. Abstract percentages verified against
  Table 2.
- `2604.16287` (NaijaS2ST benchmark, Mila): `speech-to-speech` only (S2S translation +
  cascades); `multilingual-tts` deliberately off (LRL speech output only from un-adapted Gemini
  TTS). `transformer-enc-dec` without `transformer-enc-dec-tts` is intentional (S2ST fine-tuning,
  not TTS). One real table inconsistency recorded (GPT-Audio 1.5 average). The agent opened
  `papers/2026.loreslm-1.54.md` once for frontmatter format only; no content used.
- `2604.17435` (MoVE S2ST with non-verbal vocalizations, NTU/NVIDIA): `spoken-language-model`
  (LoRA-adapted Kimi-Audio consuming source speech), `multilingual-tts` (own en↔zh fine-tuning,
  borderline), `subjective-evaluation` (5 human raters). `disentanglement` off (no training
  mechanism).

**Batch B** (`2601.04029`, `2604.14548`, `2604.17958`, `2604.15804`): run one paper at a time with
the main-session cleanup (index row, counts, log, metadata) and health check after each; all four
clean. Page count 929 → 933 (files and rows agree). Q2: 43 ingested, 187 accepted remaining. From
this batch the agents run as `claude-opus-5-5` (model switched mid-session); generation blocks and
log entries record it. Org filled by hand on all four rows (`organization` null in metadata).

- `2601.04029` (SpeakerSleuth, SNU): meta-evaluation of 12 prompted audio-language models as
  speaker-consistency judges. `subjective-evaluation` kept (3 human annotators ranked 485
  voice-cloning samples as ground truth, Kendall's W 0.860). `voice-conversion` tagged because VC
  systems build the benchmark and §7.4 tests the judges on voice-cloning output; no VC task tag
  (flagged, see queue). ACL 2026 Main acceptance noted on the page; arXiv ID stays canonical.
- `2604.14548` (VoxSafeBench, CUHK-Shenzhen): safety/fairness/privacy benchmark for speech-LM
  understanding; only text responses judged. Kept on the VoiceBench (`2410.17196`) / `2510.02352`
  SCA-benchmark precedent, flagged for confirmation. `related_concepts: [evaluation-metrics]` only
  (`spoken-language-model` off: prompting-only). Parsed author list has 13 names (adds Luchao Yao)
  vs 12 in metadata `authors_full`; not changed.
- `2604.17958` (MINT-Bench, NPU): instruction-following TTS benchmark over 14 systems, 10 languages.
  `instruction-conditioned-tts` and `subjective-evaluation` (native-speaker raters) kept;
  `multilingual-tts` off (no own system). Same-vendor judge caveat recorded.
- `2604.15804` (Qwen3.5-Omni, Qwen Team): page focused on the Talker. `multilingual-tts` kept (own
  Talker trained on 29 languages); no `codec` (tokenizer inherited, no reconstruction results); no
  `subjective-evaluation`. One real inconsistency recorded (text says best in 10 of 12 cross-lingual
  directions, Table 11 bolds 11). Thinker-Talker figure embedded and eyeballed.

**Batch C** (`2604.16211`, `2605.00861`, `2604.12456`, `2604.20842`): one paper at a time with
cleanup and health check after each; all four clean. Page count 933 → 937 (files and rows agree).
Q2: 47 ingested, 183 accepted remaining. Org filled by hand on all four rows.

- `2604.16211` (NVBench, Nanjing University / HKUST): non-verbal vocalization TTS benchmark over 15
  systems; `instruction-conditioned-tts`, `evaluation-metrics`, `subjective-evaluation` (97 Prolific
  raters plus CMOS). Table 3 numbers taken from the table image (parse garbled). The agent found that
  `iclr-2026-h5KLpGoqzC` (accepted, Q2 04-27) is the ICLR 2026 version of VoxCPM `2509.24650`
  (same authors, near-identical abstract); see queue.
- `2605.00861` (TTS voice mapping, KTH): voice-quality metrics (CPPs, spectrum balance, crest
  factor) over six public LJSpeech checkpoints and two vocoders; `low`, no listening test.
  `gan-vocoder` and `transformer-enc-dec-tts` tagged for directly evaluated systems, with
  `architecture: []` (no own model).
- `2604.12456` (X-VC, SJTU): `task: [VC]` + `voice-conversion` (target speaker similarity, WER,
  UTMOS, 15-listener SMOS). No `codec` (frozen pretrained SAC, no reconstruction results);
  `neural-codec` concept kept for codec-latent conversion. `architecture: [GAN]` for an MMDiT-style
  converter trained with SAC's adversarial losses (see queue). Figure embedded and eyeballed. Agent
  run took about 95 minutes wall-clock; no stray writes.
- `2604.20842` (SpeechParaling-Bench, Nanjing University / Xiaomi): scores the generated speech of
  five LALMs, so in scope. Page `task: [SCA, evaluation]` vs metadata `[TTS, evaluation]` (all items
  are spoken instructions to voice assistants answering in speech); index row follows the page.
  One real count inconsistency recorded (104 vs 101 features, Tables 1 and 2).

**Batch D** (`2604.19055`, `2604.21481`, `2604.21406`, `2604.22225`): one paper at a time with
cleanup and health check after each; all four clean. Page count 937 → 941 (files and rows agree).
Q2: 52 ingested, 178 accepted, 57 rejected. This completes the second round of 16 (published
2026-04-17 to 04-24). Org filled by hand on all four rows.

- `2604.19055` (ATRIE persona TTS, GDUT and others; ACM ICMR 2026): `low`. Seven inconsistencies
  recorded on the page; spot-checked four against the source (two CCS definitions, cosine §4.2 vs
  1−EER §4.4; 2,154 utterances attributed to both 3 and 50 characters; characters B/C inside the
  3-character dataset presented as zero-shot; PersonaLLM in the Algorithm 1 inference path despite
  "offline" framing) and all hold. No figure: Figure 1's image does not match its caption.
- `2604.21481` (Indian-language TTS preference study, IIT Madras): 1,915 native raters, 120K
  pairwise judgments over 7 systems; `related_concepts: [subjective-evaluation, evaluation-metrics]`
  only (`multilingual-tts` off: no own system).
- `2604.21406` (ICASSP 2026 HumDial full-duplex challenge, NPU / Nanjing University / AISHELL):
  not a survey despite 5 pages (own dataset, protocol, leaderboard). `spoken-language-model` tagged
  for directly evaluated full-duplex systems (see queue on consistency with `2604.14548`). Real
  inconsistency recorded ("eight scenarios" vs 5 + 4 sub-scenarios); the "L_base set to 60" item
  is closer to ambiguous wording but kept as written.
- `2604.22225` (TTS-PRISM, Tsinghua / Xiaomi): fine-tuned MiMo-Audio as a 12-dimension TTS quality
  judge; `spoken-language-model` off (judge, not dialogue). `subjective-evaluation` rests on the
  expert-annotated gold set; `zero-shot-tts` is borderline (see queue).

**VoxCPM later-version rule:** the user decided that once a page exists, the ingested version stays
canonical. Later proceedings/journal versions are marked duplicates, and the page gets an italic note
linking the published version and stating the page summarises the ingested one. Written into
`docs/schemas/metadata.md` (Duplicates and Later Versions) and applied to `iclr-2026-h5KLpGoqzC`.
The 8 older ICLR/NeurIPS collisions (e.g. MaskGCT, proceedings ID canonical in metadata) predate
the rule and were left as is.

**Close:** content `2e66a35` then `5dc5be9`, infra `b17b59a` then `ca7abc5`, site `3142a48` then
`16c05a4`, all pushed (both `work/ingest` branches match `main`). The 12 open queue items were
held by the user for a later decision.

### Session 2026-10-19: Manual Verification Queue cleared (no ingest)

Worked the 12 held items one at a time, each with a reasoned proposal and a user decision. All
resolved or deferred; per-item outcomes are in the queue table below.

- **Tag scope (mistag pattern):** dropped `prosody-control` from `2604.15923`, `voice-conversion`
  from `2601.04029`, `zero-shot-tts` from `2604.22225`. Rule applied each time: a concept tag needs
  the paper to perform or advance it, not just use or score it. The reachable value stays as a
  clause in the remaining Wiki Connections bullet.
- **`spoken-language-model` on benchmarks:** added to VoxSafeBench (`2604.14548`) so it matches
  HumDial. New usage rule in the ingest `SKILL.md` (benchmarks that feed real audio into existing
  speech LMs qualify; text-only ablations and AR TTS self-context do not). Agents check passes.
- **Fixes:** X-VC architecture `GAN` to `transformer-enc-dec` (page + index row); NaijaS2ST
  significance to `low`; MoVE objective-metric claim narrowed and re-evidenced with Table 1
  (verified against `table-1.png`); VoxSafeBench gains author Luchao Yao (PDF page 1 lists 13), in
  page and metadata (`authors` stays first-10).
- **Kept in scope:** VoxSafeBench (SCA precedent `2510.02352`, VoiceBench).
- **Deferred to `BACKLOG.md`:** no-text-input task term (now five fallback pages), page-vs-metadata
  `task` divergence (210 of 935 ingested records), LLaMA-Omni2 duplicate pair (third pair; ACL ID
  intended canonical; one integration-side pass for all pairs, run the reconcile health check before
  and after), and a mechanism for editing ingested/integrated papers (living wiki).
- **State:** ingest health check passes (941 papers, 0 errors). Content pushed at `088fdc0`; infra
  commit follows. Trunk infra checkout is stale and dirty from the Q4 integration stream; left alone.

### Session 2026-10-20: third round of 16 pre-selected

Protocol moved to the tracked `docs/ingest-protocol.md` (Q2 methodology trimmed to quarter-specific
material). Pre-selected 16 by `published_date`: `2604.22542`, `2604.21164`, then 14 ICLR 2026 records
dated 04-27 (all canonical over `rejected` arXiv twins). VoxPrivacy: arXiv `2601.19956` had been
rejected on relevance rather than as a duplicate; per the user it is now `is_duplicate` with
`canonical_id: iclr-2026-GNo1qMqgPD`, and the ICLR record keeps the paper in scope.

**Batch A** (model `claude-opus-5-5`, cleanup and QC per paper):

| Paper | Outcome | QC catches |
|-------|---------|------------|
| `2604.22542` | Rejected at ingest (user) | Text-only graded-vocabulary LLM dialogue for English learners; no speech anywhere; filter `task: [TTS, SCA]` unsupported. Logged in `raw/pipeline_log.md`. DrVoice (`iclr-2026-h5AiVx0Aiv`) added to the end of the list. |
| `2604.21164` MAGIC-TTS | Ingested | Clean. Warning callout (test utterances drawn from the fine-tuning subset) verified against §5. |
| `iclr-2026-0oXyMbPMtP` MambaVoiceCloning | Ingested | Two recorded table discrepancies verified real (RTF 0.0169 vs 0.0177 on otherwise identical rows; pitch error on three scales); added that Table 8 is long-form. |
| `iclr-2026-17DNmdQ9aU` StableToken | Ingested | `TTS` added to task (Qwen2.5-3B TTS on Seed-TTS, Table 3); no `subjective-evaluation` (MOS protocol unreported). |
| `iclr-2026-5o0ZvYzh6B` UniSS | Ingested | `related_papers` unquoted (`2503.01710` parsed as float); quoted. Retagged to the S2ST precedent: `task: [TTS]` (was `[TTS, VC]`), `voice-conversion` replaced by `multilingual-tts` (en-zh bilingual model; LiveInterpret, Timbre-Aware S2ST, MoVE precedent). Agent misreported LiveInterpret as `[TTS, VC]`. |

Q2: 56 ingested, 172 accepted, 59 rejected. Corpus: 945 pages. Template em dashes (Wiki Connections
separator, Field Significance `{level} — ` opening) clarified as non-defects in the protocol.

**Batch B:**

| Paper | Outcome | QC catches |
|-------|---------|------------|
| `iclr-2026-CcmDDh070o` ParaS2S | Ingested | Clean; human raters confirmed (Table 7). Review flag: field_significance moderate vs high (queue). |
| `iclr-2026-F7GmbfyVg9` FlexiVoice | Ingested | Clean. `disentanglement` kept (PPT stage S2 explicitly trained to separate timbre and style, ablated in Table 5). The SKILL.md 3-6 slug cap pushed out `subjective-evaluation` and `emotion-synthesis`, both of which qualify (queue). |
| `iclr-2026-FihSkzyxdv` VibeVoice (ICLR) | Ingested separately (user, after review) | Initially marked a duplicate of the ingested tech report `2508.19205` and used to enrich that page. Reverted the same day: the tech report is integrated (Q3 2025) and integration selects by quarter, so enrichment would never reach the claim YAMLs. Per the user the two are separate works (tech report vs peer-reviewed paper), each paged in its own quarter and cross-linked; new exception recorded in `docs/schemas/metadata.md`. `2508.19205` left as committed. |
| `iclr-2026-GNo1qMqgPD` VoxPrivacy | Ingested | Emilia's canonical `2407.05361` added to `related_papers` (agent had dropped it because the full-version record `2501.15907` is rejected). |

Q2: 59 ingested, 168 accepted, 60 rejected. Corpus: 948 pages. Batch C starts with SpeechJudge (`iclr-2026-I9ED9VWZq6`).

**Batch C:**

| Paper | Outcome | QC catches |
|-------|---------|------------|
| `iclr-2026-I9ED9VWZq6` SpeechJudge | Ingested | INTP Wiki Connections bullet carried an extra parenthetical before the separator; fixed. No `[!warning]` because of the two-callout limit (`writing-style.md`), limitation kept as prose. Surfaced a new full-page duplicate pair (DualCodec), added to `BACKLOG.md`. |
| `iclr-2026-JbLmIoWwDC` Gogo | Ingested | `TTS` added to task (GogoSpeech trained and evaluated). `rlhf-speech` kept for GRPO with automatic rewards on a codec component (DMOSpeech 2 / F5R-TTS precedent). TFC arXiv citation mapped to `interspeech-2025-1289` (same paper, verified). |
| `iclr-2026-MFrJ3NzA5H` CALM | Ingested | Clean; `[TTS, SCA]` matches the AudioLM page. Review flag: field_significance high vs moderate (queue). |
| `iclr-2026-Pv5l6cvfno` Human or Machine? | Ingested | Clean. Warning (QC experts saw true human/machine labels; revisions lift judge accuracy 0.8791 to 0.9605) verified against §D.3 and Table 14. CUHK-Shenzhen affiliation confirmed from email domains. |

Before batch C, every remaining candidate was screened by author overlap against ingested records (VibeVoice lesson): only same-group, different-system matches. Q2: 63 ingested, 164 accepted, 60 rejected. Corpus: 952 pages.

**Batch D:**

| Paper | Outcome | QC catches |
|-------|---------|------------|
| `iclr-2026-Tf4Lfw85lS` TVTSyn | Ingested | Clean. Page notes the anonymization gain claimed in the abstract does not hold against the semi-informed attacker (EER 14.57 vs DarkStream 20.83); verified against Table 3. `GAN, hybrid` matches DarkStream. |
| `iclr-2026-U4GXPqm3Va` ComVo | Ingested | Matrix written as `$[[W_r, -W_i],...]$` would render as a broken wikilink in Quartz; rewritten as `bmatrix` (no other page affected). Tags match the HiFi-GAN and Vocos pages. |
| `iclr-2026-eLsEjjFODE` SpeechOp | Ingested | Clean. Enhancement and separation have no vocabulary term, so `task: [TTS]` only. Editing scores read from the table image match the parsed row. |
| `iclr-2026-h5AiVx0Aiv` DrVoice | Ingested | Clean. Review flag: field_significance moderate vs high (queue). Agent misread the legacy dedup-pointer convention as an inconsistency (see queue). |

Q2: 67 ingested, 160 accepted, 60 rejected. Corpus: 956 pages.

**VibeVoice follow-up (user):** enrichment of `2508.19205` reverted; `iclr-2026-FihSkzyxdv` ingested
as its own Q2 page (tagged independently: no `spoken-language-model` or `disentanglement`; adds
`subjective-evaluation` and `evaluation-metrics`; records the paper's own 90 vs 30 minute
inconsistency, verified against the abstract, §4.1 and the OpenReview abstract). Both pages
cross-linked; `2508.19205` otherwise unchanged (its 4 legacy bare-wikilink warnings and unquoted
`related_papers` left as committed). Q2: 68 ingested, 160 accepted, 59 rejected. Corpus: 957 pages.

---

### Session 2026-10-21: fourth round of 16 pre-selected

Pre-selection (by `published_date`, 04-27 to 05-01): 16 candidates in four batches. Dedup screen:
`iclr-2026-zjaV5zmlkl` is the ICLR version of ingested MOSS-Speech `2510.00499` (same abstract,
authors and headline numbers; the camera-ready adds a double-blind human evaluation, App. H, and a
split-layer ablation). Marked `is_duplicate`, `rejected`, `canonical_id: 2510.00499`; italic
"Published version" note added to the MOSS-Speech page, which notes the "no human listening test"
limitation applies to the preprint only (user, later-version rule). The ICLR twins of #1-#3 already
carried duplicate flags on their arXiv records; `2601.15668` (EmotionThinker arXiv) now does too.

**Batch 1** (#1-#4, IDs checked against the list): `iclr-2026-l5re5ppqrX` EchoMind,
`iclr-2026-llMfmDtWka` SiTok, `iclr-2026-uGai5lYHlV` TTSDS2, `iclr-2026-wbttgzp7MT` EmotionThinker.
- QC catches: Org strings aligned between page and index on EchoMind (index convention), SiTok
  (page had only Meta; PDF lists CUHK-Shenzhen too) and EmotionThinker. No structural defects; all
  four pass the health check. Metrics spot-checked against source tables on all four. EchoMind's
  UTMOS (text) vs "DNMOS" (Table 4 header) mismatch correctly left off the page.
- EmotionThinker is understanding-only (SER speech LLM); it was accepted by the user in review
  triage, so it was ingested without re-deciding scope.
- Flags added to the Manual Verification Queue: EchoMind `emotion-synthesis` scope; SiTok
  high/moderate; EmotionThinker task term. TTSDS2 moderate/high resolved by the ParaS2S precedent.
- Q2: 72 ingested, 155 accepted, 60 rejected. Corpus: 961 pages.

---

**Batch 2** (#5-#8, IDs checked against the list): `2604.22821` Audio2Tool, `2604.25441` Praxy Voice,
`2604.25476` PSP, `2604.19330` Chain-of-Details.
- Audio2Tool: in scope on the AURA / VoiceAgentBench precedent. QC caught an overstatement: the page
  said §5.3's "Qwen-3-Omni-30B best on Tiers 5-7" holds for Tool Accuracy, but the cascade wins Tool
  Accuracy on Tier 7 (56.2 vs 54.6, checked on the table image); narrowed to Tiers 5 and 6.
- Praxy Voice: the page's Table II note (Config B values equal the Sarvam-Te reference row despite a
  Cartesia-Te caption) verified on the table PNGs and kept. PSP linked from the page once written;
  the cited "~46%" native-Telugu noise floor now notes PSP's own table gives 0.43.
- PSP: `low` and two concepts, both flagged. Companion pages cross-linked.
- Chain-of-Details: agent shipped one concept; `autoregressive-codec-tts` added in QC (masked
  codec-token generator, MaskGCT/SoundStorm precedent, compared directly with MaskGCT).
- New recurring issue: the hard 3-6 `related_concepts` minimum vs strict scope. The first agent
  padded with an out-of-scope slug; later prompts said not to pad, and three of four pages came in
  at two. Queued for a rule decision.
- Q2: 76 ingested, 151 accepted, 60 rejected. Corpus: 965 pages.

---

**Batch 3** (#9-#12, IDs checked against the list): `2604.26281` DiffAnon, `2604.26347` The False
Resonance, `2604.27393` MiniCPM-o 4.5, `2026.dialres-1.18` Speaker Normalization via VC.
- DiffAnon: the page said the authors' "competitive" semi-informed privacy is unsupported, citing
  only the systems that beat it. Checked on the Table 1 image and rebalanced: DiffAnon (14.5-22.8
  test EER) is above B1, B2, B6 and below B3-B5 and T8-T10. Org shortened to the index convention
  (Johns Hopkins University).
- The False Resonance: Table 1 distractor values checked on the image; two retitled references
  (EmoPro, LibriQuote) confirmed as the same arXiv IDs. `emotion-synthesis` joins the EchoMind item.
- MiniCPM-o 4.5: interrupted by a session limit after copying two figures and before the page; stray
  assets removed, clean retry. Verified that the headline SeedTTS numbers are the non-duplex mode
  (Table 10: TAIL 1.04 / 3.93 vs fixed 0.86 / 2.38).
- Speaker Normalization via VC (accepted by the user in triage): the page's five departures from the
  authors' framing (large effect at d = 0.65, "double" dissociation, train-time vs test-time
  comparison, 55.6% size-matched control, F1 shift) checked against the text. Org quoted.
- Recurring: agents now explicitly decline to pad `related_concepts`; one more two-slug page.
  Agents also produce well-founded but one-sided critiques of author framing; the prompt now asks for
  the full comparison.
- Q2: 80 ingested, 147 accepted, 60 rejected. Corpus: 969 pages.

---

**Verification queue cleared** (same session, after Batch 3): user accepted all seven
recommendations (minimum-vs-scope rule; EchoMind drops `emotion-synthesis`, The False Resonance
keeps it; SiTok to moderate; PSP stays low; MiniCPM-o stays moderate; EmotionThinker keeps `[SCA]`
and drops `evaluation-metrics`; `2026.dialres-1.18` keeps `VC`). Pages, protocol, ingest SKILL.md,
vocabulary and `qc.py` updated; agent compatibility check passes. Session closed after Batch 3;
Batch 4 carries over.

---

### Session 2026-10-22: fifth round of 16 pre-selected

Pre-selection (by `published_date`, 05-01 to 05-07): the carried-over LREC Batch 4 as Batch A,
then `2026.lrec-1.48`, `.771`, `.859`, `2026.sigul-1.11`, `2407.15828` J-CHAT, `2604.13288`,
`2605.00777` LASE, `2607.01238` SPARCLE, `2507.13563` Balalaika, `2604.09111` PS-TTS,
`2605.02496` Tibetan-TTS, `2604.27607` JaiTTS. Dedup screen: no title duplicates; Balalaika shares
all six authors with ingested `2604.01247` but is a different paper (cross-link, not a duplicate);
SPARCLE's 2607 ID with a 05-01 date was confirmed against the arXiv API (v1 2026-05-01).

**Batch A** (#1-#4, IDs checked against the list): `2026.lrec-1.184` Probing Discrete Speech
Tokens, `2026.lrec-1.375` TTSVowelViz, `2026.lrec-1.437` Prominence/Boundary Prediction,
`2026.lrec-1.465` IMaSC.
- Probing Discrete Speech Tokens (accepted in triage): all metrics checked against Tables 1-5.
  `spoken-language-model` correctly withheld (probed systems are AR TTS-LMs). Org shortened to the
  index convention (University of Stuttgart).
- TTSVowelViz: not zero-metric (23-listener accent perception test, Figure 4), so no precedent
  needed. QC added `transformer-enc-dec-tts` for the `transformer-enc-dec` architecture tag
  (fine-tuned Tacotron 2 is the object of analysis; corpus tags Tacotron 2 with that slug).
- Prominence/Boundary Prediction: scope surfaced; user ruled it in (TTS front-end prosody
  prediction; label-prediction accuracy only, no synthesis). QC added `transformer-enc-dec-tts`
  (the authors train their own modified FastSpeech2 as one of the three strategies). Docling
  numbers the paper's Tables 4a-4d as 4-7 out of order; the page cites the paper's labels.
- IMaSC: no earlier IMaSC version in the corpus. VITS tagged `[VAE, GAN]` with `gan-vocoder`.
  MOS values checked against Table 3.
- Recurring: architecture tag without its concept slug (2 of 4 pages, 2026-10-22). LREC 2026
  records carry `venue: "workshop"` in metadata (9 records); pages use `LREC 2026` / `conference`.
- Q2: 84 ingested, 143 accepted, 60 rejected. Corpus: 973 pages.

---

**Batch B** (#5-#8, IDs checked against the list): `2026.lrec-1.48` Central Kurdish TTS,
`2026.lrec-1.771` Nos_Brais-GL, `2026.lrec-1.859` URDUTTS, `2026.sigul-1.11` Creole TTS transfer.
- Central Kurdish TTS: two errors caught against the Table 3 PNG and §4.3. Studio-M's PESQ range
  was 3.78 to 4.16, not 4.00 to 4.16. The Table 4 bullet credited the 79.95 BLEU result to real
  speech; it is the all-synthetic run, and 92.42 is the real-speech upper bound. `multilingual-tts`
  (English F5-TTS fine-tuned to Kurdish) flagged to the Manual Verification Queue.
- Nos_Brais-GL: Figures 2 and 3 values verified on the PNGs. QC caught unquoted numeric IDs in
  `related_papers` (`[2010.05646, 2106.15561]`); quoted. Prompts now say to quote `related_papers`.
- URDUTTS: the page's source-side observations verified on the table PNGs: the abstract's 9.6%
  VITS MOS gain does not match Table 5 (13.5%); the VITS-Rm and GlowTTS-Rm rows are identical in
  Tables 6 and 8; the "Romanized" input is a vowelless consonant skeleton (Table 1). Wiki
  Connections bullets used a colon instead of the template separator (the agent over-applied the
  no-em-dash rule); fixed. One `adoption language` QC hit was a false positive ("dominant error").
- Creole TTS transfer: Figures 1, 3 and 4 checked. First SIGUL page: `venue: SIGUL 2026`,
  `venue_type: workshop`. The paper's "informal subjective evaluation" is the authors' own
  impressions, so no `subjective-evaluation`.
- Recurring: an agent replaced the Wiki Connections separator to avoid em dashes (2026-10-22);
  the prompt now spells out the template. Unquoted numeric `related_papers` IDs recurred.
- Q2: 88 ingested, 139 accepted, 60 rejected. Corpus: 977 pages.

---

**Batch C** (#9-#12, IDs checked against the list): `2407.15828` J-CHAT, `2604.13288` Quechua/Spanish
Constitution TTS, `2605.00777` LASE, `2607.01238` SPARCLE.
- J-CHAT: the arXiv record carries the LREC 2026 proceedings (`2026.lrec-1.444`); page keeps the
  arXiv ID with the LREC venue and Anthology URL. Metadata `url_acl` is malformed
  (`https://aclanthology.org/https://lrec.elra.info/...`), as on `2604.13288`. `spoken-language-model`
  for a textless dGSLM-style unit LM kept on the Behavior-SD / Align-SLM precedent. Tables 2 and 3
  and the 68k-vs-57k train-hour confound checked against the source.
- Quechua/Spanish TTS: PoliticalNLP 2026 workshop (co-located with LREC). Table 1 checked; the page
  states that the cross-lingual-transfer conclusion is untested (no Quechua-only baseline).
- LASE: Praxel companion to Praxy Voice and PSP (cross-linked; the paper never evaluates Praxy with
  LASE). Four prose-vs-table mismatches on the page checked against Table I (0.082/0.105 vs
  0.083/0.107; 0.141 vs 0.144; the "2.4-2.7x over both baselines" margin claim is 1.3x against ECAPA
  on Indian voices; ECAPA+GRL has the larger Western margin). `disentanglement` queued.
  `2505.14410` (cited, rejected) replaced by its canonical `interspeech-2025-2283` page.
- SPARCLE: Tables 1 and 2 checked, including the per-budget WER reductions (51%, 72%, 70%, 51%,
  31%) and the small text-vs-table mismatches. ParrotTTS tagged `transformer-enc-dec` from its known
  architecture (not described in the paper; ParrotTTS has no corpus page), with the slug.
- No structural QC defects this batch; the tightened prompt (quoted `related_papers`, explicit
  Wiki Connections separator, architecture-slug coverage) held on all four pages.
- Q2: 92 ingested, 135 accepted, 60 rejected. Corpus: 981 pages.

---

**Batch D** (#13-#16, IDs checked against the list): `2507.13563` Balalaika, `2604.09111` PS-TTS,
`2605.02496` Tibetan-TTS, `2604.27607` JaiTTS.
- Balalaika: companion of ingested `2604.01247` (same six authors), which trains only on
  Balalaika's Yandex Podcasts split; a one-line Wiki Connections back-link was added to that page
  (health check passes). Tables 1 and 2 checked: the "on par with the strongest baselines" CER is
  4th of 12, and the TMR "top" ties M-AILABS. The §4.1 "Table 8" cross-reference is wrong (Table 8
  is the curated-dataset list; the comparison is Table 1). Emilia cited as rejected `2501.15907`;
  canonical `2407.05361` linked.
- PS-TTS: two source mismatches verified on the table PNGs (§4.3 prose UTMOS 2.362 vs Table 2
  2.562; Table 3 baseline LSE-D 11.092 is not the Table 1 average, while the other cells are).
  `speech-to-speech` withheld (only the text-selection and TTS stages are evaluated).
- Tibetan-TTS: proprietary Xingchen AGI Lab AR LM + flow-matching backbone, not CosyVoice 2. The
  flow-matching stage is frozen (Figure 2); slug kept and queued. Org separator normalised to
  " / ". Reference [9] in the source carries placeholder text ("Example venue; please replace"),
  noted on the page. The `inconsistency` QC hit was a false positive ("inconsistent speech data").
- JaiTTS: VoxCPM continually trained on Thai. `autoregressive-codec-tts` for continuous-latent AR
  kept on the VoxCPM / Continuous Audio Language Models precedent. Table 1 (including where JaiTTS
  loses long-form SIM) and Figure 2 (161 + 122 = 283 of 400 wins) checked.
- Round sweep: all 16 IDs have a page, one index row, one log entry and `status: ingested`; the
  full ingest health check passes (0 errors, 985 papers).
- Q2: 96 ingested, 131 accepted, 60 rejected. Corpus: 985 pages.

**Verification queue cleared** (same session, after Batch D): user rulings on six items. New
`multilingual-tts` rule (output must span more than one language), so three pages drop the slug;
the VITS `gan-vocoder` convention is confirmed going forward; frozen components keep their slug
below the cap; `autoregressive-codec-tts` on `2026.lrec-1.184` and `disentanglement` on LASE kept;
LREC metadata (venue, `url_acl`) repaired on 14 records, with the fetcher fix in `BACKLOG.md`.
Health checks re-run on the three edited pages and JaiTTS (pass).

---

### Session 2026-10-23: sixth round of 16 pre-selected

Pre-selection (2026-05-07 onward, re-derived from metadata) and pre-flight screening. Three
decisions, all confirmed by the user:
- `2605.16026` S2ST-Omni 2 extends `2026.findings-acl.1004` S2ST-Omni (accepted, 2026-07-02, Q3;
  4 shared authors). Treated as separate works (new named system, VibeVoice precedent): ingest each
  in its own quarter, cross-link, neither a duplicate.
- `2605.17846` UrduSpeech moved `accepted -> review` (general corpus, no TTS/VC experiment; MOS
  rates the recordings, TTS baselines are future work). `raw/review_queue.md` entry added.
- `2605.18001` PACC re-dated: preprint notice plus Crossref show it in the ICICC 2025 proceedings
  (Springer LNNS, online 2025-10-01); `conference_date` set and the date rule re-applied, so
  `published_date` is 2025-10-01 (Q4 2025 straggler, not in this sweep).
- Replacements: `2605.20946` Thinking-while-speaking and `2605.22083` RobustSpeechFlow (screened
  clean); reserve `2605.26136` (deepfake perception study).
- MoshiRAG (`2604.12928`, ICML 2026) keeps its arXiv date like all 14 arXiv/ICML pairs.

Numbered list: 1 `2605.06407` WavCube, 2 `2605.05927` TextPro-SLM, 3 `2605.05611` X-Voice,
4 `2605.09386` GibbsTTS, 5 `2605.10084` PoDAR, 6 `2605.10199` user-stream routing, 7 `2605.11192`
LATTE, 8 `2604.12928` MoshiRAG, 9 `2605.12310` Poly-SVC, 10 `2605.16026` S2ST-Omni 2,
11 `2605.16964` SemaVoice, 12 `2605.17085` Target-KL VAE, 13 `2605.19541` 300bps RL codec,
14 `2605.20830` Raon-OpenTTS, 15 `2605.20946` Thinking-while-speaking, 16 `2605.22083`
RobustSpeechFlow.

**Batch A** (#1-#4, IDs checked against the list): `2605.06407` WavCube, `2605.05927` TextPro-SLM,
`2605.05611` X-Voice, `2605.09386` GibbsTTS.
- WavCube: Tables 1-3, 5-7 checked. Two Key Results overstatements fixed: the Stage 1 to Stage 2
  loss list omitted ER, and "best MCD" / "highest ASV" on SUPERB-SG VC held only among the final
  latents (Stage 1 and WavLM-Large beat both). Org widened to SJTU / SII / Tencent, page synced.
- TextPro-SLM: task changed `[TTS] -> [SCA]` on the page (no speech output; synthesis is out of
  scope by the authors' Remark 1); metadata `task` left as filter output per precedent. The page
  defined the modality gap with the wrong sign ("speech minus text"); Table 3 shows text minus
  speech, fixed. One slug (`spoken-language-model`), scope over the minimum.
- X-Voice: VC dropped (prompt-based cloning is TTS). Cross-linked to Cross-Lingual F5-TTS
  `2509.14579`. Qwen3-TTS / OmniVoice comparisons verified on Table 5; native-rater IMOS/SMOS
  confirmed. RTF kept as a metric (7 existing pages use it).
- GibbsTTS: frozen MaskGCT codec keeps `neural-codec` below the cap, page says frozen.
  `multilingual-tts` on pooled en/zh training evaluated in both. Tables 2-4 verified; an
  unattributed "first application" novelty claim in Field Significance attributed to the authors.
- Recurring: sign convention of a derived metric written backwards (new; prompt now asks agents
  to check it). Protocol wording "not cut mid-word" for index titles contradicts the hard
  `title[:55]` cut every row uses; fix the protocol text at wrap-up.
- Q2: 100 ingested, 125 accepted, 1 review, 60 rejected. Corpus: 989 pages.
- At close the user rejected UrduSpeech (`review -> rejected`). Q2: 100 ingested, 125 accepted,
  61 rejected.

---

### Session 2026-10-24: sixth round continued

**Batch B** (#5-#8, IDs checked against the list): `2605.10084` PoDAR, `2605.10199` user-stream
routing, `2605.11192` LATTE, `2604.12928` MoshiRAG. Statuses re-verified and the new
prior-publication pre-flight run on all 13 remaining candidates first (no notices).
- PoDAR: Table 2 is scrambled in the markdown; all six comparisons verified on the PNG, Table 1
  on the markdown. `task: [codec, TTS]` on the page (F5-TTS generators trained from scratch,
  all results on TTS benchmarks); metadata `task` left as filter output per precedent.
  `multilingual-tts` kept: the paper's own generator is trained on Emilia ZH-EN and evaluated on
  EN and ZH, which meets the rule, though the bilingual setup is inherited from the F5-TTS recipe
  (agent review flag, surfaced to the user).
- User-stream routing: Table 1 and Table 4 values verified. One omitted comparison added
  (GLM-4-Voice ties CF-Duplex on LLaMA Questions speech and leads on text, 50.7 | 64.7). The
  Table 4 vs Table 10 EN | ZH order swap for stage-1 CF-Duplex TTS WER is real (both PNGs) and
  noted neutrally. Agent noticed SALM-Duplex has two un-linked pages (`interspeech-2025-0874`,
  `2505.15670`, neither marked duplicate); surfaced, not changed.
- LATTE: VC kept (parallel VCTK slot-swap VC measured with target-speaker similarity against
  codec baselines, Table 4), though the authors frame it as an analysis intervention, not a
  conversion system. A speculative Limitations bullet about an unexplained discriminator in
  Figure 1 removed (the text does not describe it; not a verified defect). Agent run took about
  80 minutes of wall time for unclear reasons.
- MoshiRAG: Table 1 verified row by row (Docling scrambled it); every baseline win reported
  (GPT-4o Audio on all sets, Qwen3-Omni over the Gemma config on all four). ICML record
  `icml-2026-4aI2vOyyHH` already a flagged duplicate. Review flags: `evaluation-metrics` scope
  (keyword delay / E2EKD defined and measured across baselines) and moderate vs high
  significance; both left as written and surfaced.
- No new recurring issue class. Cleanup and QC ran clean on all four after each paper.
- Q2: 104 ingested, 121 accepted, 61 rejected. Corpus: 993 pages.

**Batch C** (#9-#12, IDs checked against the list): `2605.12310` Poly-SVC, `2605.16026`
S2ST-Omni 2, `2605.16964` SemaVoice, `2605.17085` Target-KL VAE.
- Poly-SVC: Table 1 verified (subjective only, 12 raters). Fine-tuned Firefly-GAN vocoder earns
  `gan-vocoder`; six slugs. Review flags: `zero-shot-tts` omitted (paper claims zero-shot, but the
  PopBuTFy target singers may be in training data) and `disentanglement` borderline (alignment
  loss plus input perturbation, ablations within about one CI). Both queued.
- S2ST-Omni 2: separate work from `2026.findings-acl.1004` (accepted, no page): kept in
  `related_papers`, mentioned unlinked. `task: [SCA, TTS]` on the SimulS2S-LLM precedent
  (off-the-shelf TTS backends, output speech evaluated with ASR-BLEU and BLASER 2.0). Two slugs.
  Affiliation footnotes verified (seven institutions). Cascade beats it on German to English;
  reported.
- SemaVoice: Table 1 verified; the paper's "consistently outperforms" holds only for English WER,
  and the page gives the full comparison. Continuous sigma-VAE latents, so no
  `autoregressive-codec-tts`; `gan-vocoder` dropped under the 6-slug cap (inherited DAC recipe).
- Target-KL VAE: `task: [TTS, codec]` kept (own 740M DiT TTS trained per VAE and evaluated on
  Seed-TTS test-en). Reconstruction is general-audio only (AudioSet mel loss), stated on the
  page. One overstatement fixed in Key Results and the claim: the 7.65 kbps VAE ties the
  11.56 kbps VAE for best speaker similarity (0.68), not best alone. Review flag: `gan-vocoder`
  from the GAN-trained DAC-VAE decoder; note PoDAR (Batch B) left it off for the same shape
  (GAN discriminator in a retrained VAE recipe), so the two pages are inconsistent pending a
  decision. Queued.
- Agents twice took 80-100 minutes of wall time (LATTE, S2ST-Omni 2) with normal tool counts;
  the S2ST-Omni 2 agent reported missing PDF tools. Later prompts tell agents not to wait on
  unavailable tools. Agents also report the legacy MaskGCT pointer (`2409.00750` /
  `iclr-2025-ExuBFYtCQU`) as inverted; it is the documented legacy convention, no change.
- Q2: 108 ingested, 117 accepted, 61 rejected. Corpus: 997 pages.

**Batch D** (#13-#16, IDs checked against the list; sixth round complete): `2605.19541`
ClariCodec (300bps RL codec), `2605.20830` Raon-OpenTTS, `2605.20946` InterRS
(Thinking-while-speaking), `2605.22083` RobustSpeechFlow.
- ClariCodec: Table 1 verified. GRPO on the encoder plus stochastic FSQ with an ASR-WER reward
  earns `rlhf-speech`; two slugs. Loses to SAC and FlexiCodec on WER, PESQ and SIM at higher
  bitrates; reported. Review flag: `gan-vocoder` left off under the pending GAN-decoder convention,
  although a Vocos vocoder is trained from scratch with the codec (added to that queue row).
- Raon-OpenTTS: agent set `high` with a `[!tip]`; downgraded to moderate on the benchmark/dataset
  precedent (`iclr-2026-CcmDDh070o`, TTSDS2: moderate until uptake is visible) and the callout
  converted to prose. `task: [TTS, evaluation]` (Raon-OpenTTS-Eval is a core contribution).
  Frozen HiFi-GAN vocoder not tagged. DiTTo-TTS cross-linked as related KRAFTON work.
- InterRS: no speech output is evaluated (text metrics, LLM-judge fluency), so no
  `streaming-tts` or `speech-to-speech` (TextPro-SLM precedent); `rlhf-speech` for GRPO with
  new rewards. Fixed a wrong "largest gain on KK-audio" statement (largest over Fast CoT is SMQA;
  on KK-audio InterRS is best overall). Quoted `architecture`/`type` lists normalised.
- RobustSpeechFlow: agent listed every superlative with its supporting cells; spot-checked
  Tables 1-2. Review flag: `multilingual-tts` omitted because the paper trains on about 10k h
  "per language" (English and Korean) without saying whether one joint model was trained.
  VibeVoice cited as the ICLR page `iclr-2026-FihSkzyxdv` (separate-pages precedent).
- Over-broad superlative claims recurred twice in this batch (InterRS) and once in Batch C
  (Target-KL); asking agents to list each superlative with its cells (RobustSpeechFlow) worked.
- Q2: 112 ingested, 113 accepted, 61 rejected. Corpus: 1,001 pages.

---

### Session 2026-10-24 (continued): seventh round of 8 pre-selected

Pre-selection (2026-05-21 onward, re-derived from metadata) and pre-flight screening (title
dedup, author overlap with ingested records, arXiv comments, first-page notices, Crossref for
proceedings/journal versions). `2605.25504` left off (O-COCOSDA 2025, queued); TASLP
`journal_date` precision for #5 and #8 queued. Lineage noted: CORTIS follows `2507.20140`,
CosyEdit2 follows `2601.05329` (separate works, cross-link). #1 ticked `accept` in triage.

Numbered list: 1 `2605.26136` deepfake perception study, 2 `2605.23373` AffectCodec,
3 `2605.23859` F5-TTS-DPS (WildSpoof), 4 `2605.25506` WaveNeXt 2, 5 `2605.25669` ultra-low-bitrate
mel coding, 6 `2605.25962` CORTIS, 7 `2605.25930` CosyEdit2, 8 `2605.26812` CFMDCTCodec.

---

**Batch E** (seventh round #1-#4, IDs checked against the list): `2605.26136` deepfake perception
study, `2605.23373` AffectCodec, `2605.23859` F5-TTS-DPS, `2605.25506` WaveNeXt 2.
- Deepfake study: triage-accepted, so scope not re-opened. `task: [TTS, evaluation]`,
  `subjective-evaluation` only (evaluation-paper rule: no system concepts for stimulus
  families). Review flag: VC dropped although one stimulus family is listener-judged VC output.
- AffectCodec: `task: [codec]` (no TTS or speech LM trained on the tokens). Tables 1-2 checked;
  the two losses to X-Codec / SpeechTokenizer at 3.0 kbps reported. `disentanglement` on the
  block-diagonal projections with a direct ablation. Queued: `self-supervised-speech` for a frozen
  emotion2vec (data2vec-based) teacher, which is outside the rule's model list. GAN decoder from
  the DAC recipe, `gan-vocoder` left off (pending convention).
- F5-TTS-DPS: WildSpoof TTS Track report, low significance, `flow-matching` only. Cross-linked to
  WildSpoof submissions `2512.17293` and `2602.05770` (verified). Rejected WildSpoof evaluation
  plan `2508.16858` removed. Review flag: `zero-shot-tts` omitted (official evaluation is on seen
  speakers in the fine-tuning data).
- WaveNeXt 2: standalone GAN and diffusion vocoders, so `gan-vocoder` and `diffusion-tts` apply.
  Table 1 checked, superlatives listed by the agent hold. The main-session prompt gave a wrong
  title ending ("Sub-band processing"); the agent used the metadata title.
- Agent wall time again long on two runs (AffectCodec about 45 min, WaveNeXt 2 about 14 min) with
  ordinary tool counts; PDF renderers are missing in the environment.
- Q2: 116 ingested, 109 accepted, 61 rejected. Corpus: 1,005 pages.

**Batch F** (seventh round #5-#8, IDs checked against the list; seventh round complete):
`2605.25669` FMelCodec, `2605.25962` CORTIS, `2605.25930` CosyEdit2, `2605.26812` CFMDCTCodec.
- FMelCodec: Tables I-II spot-checked. Retrains a standalone HiFi-GAN v1 vocoder (not a
  contribution), tagged `gan-vocoder`; added to the GAN convention queue row. Journal date left
  unchanged pending the queued decision.
- CORTIS: own page, cross-linked to `2507.20140` with what is new. VoiceBox partly fine-tuned
  (saliency-masked 30%). Review flag: `speaker-adaptation` kept to match `2507.20140`, but
  unlearning removes rather than adapts a speaker.
- CosyEdit2: own page, cross-linked to `2601.05329`. Table 9 spot-checked. `multilingual-tts`
  excluded (editing post-training English only; four-language ability inherited from CosyVoice 2,
  per the 2026-10-22 rule). Trains and separately evaluates a standalone BigVGAN, so
  `gan-vocoder`. Review flag: moderate vs high (CosyEdit was high).
- CFMDCTCodec: the first agent run was cut off by a session limit with nothing written
  (checked: no page, assets, index row, log line or metadata change); retried cleanly. Non-adversarial
  training, so no GAN tag. The abstract's "outperforms" does not hold against BigCodec; the page
  says so.
- Q2: 120 ingested, 105 accepted, 61 rejected. Corpus: 1,009 pages.

---

## Manual Verification Queue

Papers where the ingest agent emitted `review_flags` in its INGEST_RESULT signal. Review these
after the session batch is complete — check the paper page and resolve each flag by hand.

| Paper ID | Flag | Agent note |
|----------|------|------------|
| `2605.25962` | concept scope (`speaker-adaptation`) | Resolved 2026-10-24 (user): kept, consistent with `2507.20140` (speaker-targeted fine-tuning). |
| `2605.25930` | field_significance moderate/high boundary | Resolved 2026-10-24 (user): kept at moderate. |
| `2605.26136` | task (`VC` dropped) | Resolved 2026-10-24 (user): VC stays dropped (one analysis family; evaluation-paper rule). |
| `2605.23373` | concept scope (`self-supervised-speech`) | Resolved 2026-10-24 (user): kept. Any self-supervised speech model the method itself uses counts (emotion2vec, data2vec); never Whisper, never metric-only use. Rule in `docs/ingest-protocol.md` (the ingest SKILL.md already said "or similar"). |
| `2605.23859` | concept scope (`zero-shot-tts` omitted) | Resolved 2026-10-24 (user): stays omitted; evaluated voices seen in training do not earn `zero-shot-tts`. Rule in `docs/ingest-protocol.md`. |
| `2605.25504` | paper date (prior publication) | Resolved 2026-10-24 (user): re-dated (`conference_date` 2025-11-12, `published_date` 2025-11-12; logged in `raw/pipeline_log.md`). Now a Q4 2025 straggler; the user wants it ingested, picked up with PACC `2605.18001` at the next pre-selection (see Resume Here). |
| `2605.25669` / `2605.26812` | paper date (`journal_date` precision) | Resolved 2026-10-24 (user): `journal_date` left unset (Crossref gives the year only; quarter unaffected). |
| `2605.22083` | concept scope (`multilingual-tts` omitted) | Resolved 2026-10-24 (user): stays omitted (joint training not stated). |
| `2605.20830` | field_significance high/moderate | Resolved 2026-10-24 by precedent (`iclr-2026-CcmDDh070o`, TTSDS2): downgraded to moderate, `[!tip]` converted to prose; user did not override. |
| `2605.12310` | concept scope (`zero-shot-tts` omitted) | Resolved 2026-10-24 (user): stays omitted (target singers seen in training). Rule in `docs/ingest-protocol.md`. |
| `2605.12310` | concept scope (`disentanglement`) | Resolved 2026-10-24 (user): kept (explicit mechanism plus ablation meets the rule). |
| `2605.17085` / `2605.10084` | concept scope (`gan-vocoder` for a GAN-trained VAE decoder) | Resolved 2026-10-24 (user): option C. Tag for a standalone GAN vocoder trained in the paper, or when the codec/VAE decoder's adversarial training is the paper's own contribution or is ablated; not for GAN losses inherited unchanged from DAC/Stable Audio/Vocos. Corpus check: 28 of 76 codec+GAN pages carry the slug (EnCodec, BigCodec, HiFi-Codec in the integrated YAML); not backfilled. No page changes: Target-KL keeps it (CQT discriminator ablated, Table 1); PoDAR, ClariCodec, AffectCodec stay without; FMelCodec, CosyEdit2, WaveNeXt 2 keep it. Rule in `docs/ingest-protocol.md`. |
| `2605.10084` | concept scope (`multilingual-tts`) | Resolved 2026-10-24 (user): kept (own generator trained and evaluated on EN and ZH; GibbsTTS precedent). |
| `2604.12928` | concept scope (`evaluation-metrics`) | Resolved 2026-10-24 (user): kept (defines and measures new latency metrics). |
| `2604.12928` | field_significance moderate/high boundary | Resolved 2026-10-24 (user): kept at moderate. |
| `2026.lrec-1.48` | concept scope (`multilingual-tts`) | Resolved 2026-10-22 (user): adaptation to a single new language with monolingual output does not earn `multilingual-tts`; the evaluated output must span more than one language. Dropped from `2026.lrec-1.48`, `2605.02496` and `2026.sigul-1.11`; kept on PS-TTS `2604.09111` (bilingual YourTTS), JaiTTS `2604.27607` (code-switching evaluated, bullet reworded) and `2604.13288` (pooled Spanish+Quechua). Rule in `docs/ingest-protocol.md`. |
| `2026.lrec-1.184` | concept scope (`autoregressive-codec-tts`) | Resolved 2026-10-22 (user): kept. |
| `2605.00777` | concept scope (`disentanglement`) | Resolved 2026-10-22 (user): kept. |
| `2605.02496` | concept scope (frozen `flow-matching`) | Resolved 2026-10-22 (user): below the 6-slug cap a frozen component that is part of the evaluated system keeps its slug, with the page stating it is frozen. Rule in `docs/ingest-protocol.md`. |
| VITS pages | `gan-vocoder` convention | Resolved 2026-10-22 (user): VITS `[VAE, GAN]` carries `gan-vocoder` going forward; older pages not backfilled. Rule in `docs/ingest-protocol.md`. |
| LREC 2026 records | metadata `venue` | Resolved 2026-10-22 (user): fixed now. 13 `2026.lrec-1.*` records set to `LREC` / `conference`; 5 malformed `url_acl` values corrected (14 records in all, logged in `raw/pipeline_log.md`). Fetcher fix tracked in `BACKLOG.md` (Infrastructure). |
| `2026.dialres-1.18` | task (`VC` close call) | Resolved 2026-10-21 (user): `task: [VC]` and `voice-conversion` kept; clarification added to `docs/schemas/vocabulary.md` and the protocol (off-the-shelf VC counts when the converted speech is measured, not when VC is only preprocessing). |
| `2604.27393` | field_significance moderate/high boundary | Resolved 2026-10-21 (user): kept at moderate. |
| `2604.25476` | field_significance low/moderate boundary | Resolved 2026-10-21 (user): kept at low. |
| `2604.22821` | related_concepts minimum vs scope | Resolved 2026-10-21 (user): scope wins over the minimum; cap of 6 stays hard, 1-2 slugs allowed when that is all that qualifies, never pad. Audio2Tool's padded `speech-to-speech` dropped (cascade comparison kept in the `spoken-language-model` bullet). Praxy Voice, PSP, Chain-of-Details and `2026.dialres-1.18` stand at two. Rule updated in `docs/ingest-protocol.md`, the ingest SKILL.md and `scripts/ingest/qc.py`. |
| `iclr-2026-wbttgzp7MT` | task (vocabulary gap: speech understanding) | Resolved 2026-10-21 (user): `task: [SCA]` kept on the `2508.07273` precedent; gap logged in `BACKLOG.md` beside the no-text-input item; `evaluation-metrics` dropped (two slugs remain). |
| `iclr-2026-uGai5lYHlV` | field_significance moderate/high boundary | Resolved 2026-10-21 by precedent (`iclr-2026-CcmDDh070o`: benchmark papers stay moderate until uptake is visible). TTSDS2 kept at moderate; revisit only if the user overrides. |
| `iclr-2026-llMfmDtWka` | field_significance high/moderate boundary | Resolved 2026-10-21 (user): downgraded to moderate (Continuous Audio Language Models precedent); `[!tip]` converted to prose naming the precedents. |
| `iclr-2026-l5re5ppqrX` | concept scope (`emotion-synthesis`) | Resolved 2026-10-21 (user): EchoMind drops `emotion-synthesis` (finding folded into the `evaluation-metrics` bullet); The False Resonance keeps it (evaluates how to measure emotion synthesis). Rule added to `docs/ingest-protocol.md`. |
| `2409.00750` / `iclr-2025-ExuBFYtCQU` | dedup pointer (pre-existing) | Resolved 2026-10-20: not a defect. Legacy dedup-pointer convention: the proceedings record is `ingested` with `wiki_page_id` set to the arXiv page, and the arXiv record carries `is_duplicate` plus `canonical_id` back to it. Eight records follow it consistently (MaskGCT, MoonCast, LLaMA-Omni, VITA-1.5, ...); the page is always the `wiki_page_id` target. Documented in `docs/ingest-protocol.md`. |
| `iclr-2026-CcmDDh070o` | field_significance moderate/high boundary | Resolved 2026-10-20 (user): kept at moderate; benchmark-plus-alignment papers stay moderate until uptake is visible. |
| `iclr-2026-F7GmbfyVg9` | related_concepts cap | Resolved 2026-10-20 (user): hard 3-6 cap kept; swapped `flow-matching` (frozen, inherited decoder; only the LLM is trained) for `subjective-evaluation` (expert-listener Q-MOS/CMOS, App. A.9). `flow-matching` stays in `architecture`. `emotion-synthesis` not added. |
| `2508.19205` | related_concepts | Resolved 2026-10-20 (user): page left as committed (enrichment reverted); the tag recommendation was not applied. The ICLR page is tagged independently under current rules. |
| `iclr-2026-MFrJ3NzA5H` | field_significance high/moderate boundary | Resolved 2026-10-20 (user): downgraded to moderate (continuous AR TTS predates it; speaker similarity lags; the contribution is the domain-general comparison and recipe). `[!tip]` callout converted to prose. |
| `iclr-2026-h5AiVx0Aiv` | field_significance moderate/high boundary | Resolved 2026-10-20 (user): kept at moderate (builds on SLAM-Omni grouping and a Moshi-style parallel design; LLM-judge evaluation). |
| corpus-wide | `[!note]` callouts | 59 other pages carry the disallowed legacy `[!note]` callout (converted on `2508.19205` only). Candidate for a scripted cleanup. |
| `2026.iwsds-1.16` | field_significance moderate/low boundary | Resolved 2026-09-27: downgraded to low (narrow 20-participant single-model pilot, no comparison group). |
| `2026.propor-1.81` | field_significance low/moderate boundary | Resolved 2026-10-17: kept at moderate (user). |
| `2604.06327` | field_significance low/moderate boundary | Resolved 2026-10-17: kept at low (user); noted as a useful source for objective-metric evidence (`evaluation-metrics`). |
| `2605.27383` | claims (numbers inconsistent across tables) | Resolved 2026-10-17: verified against source; warning callout rewritten (2 of 5 claimed inconsistencies were setting differences or per-language counts). Claims cite single tables. |
| `2604.10065` | field_significance low/moderate boundary | Resolved 2026-10-17: kept at moderate (user). The controlled finding (full-token GRPO degrades content, action-space projection avoids it) carries the level; the page already states the small, mixed gains over delayed Moshi. |
| `2604.10413` | task (vocabulary gap) | Resolved 2026-10-17: not in the gap. The model is text (phoneme) driven FastSpeech 2 with sign-video prosody conditioning, same shape as `interspeech-2025-1494`, so `task: [TTS]` is correct. The real gap (no text input) is tracked in `BACKLOG.md`. |
| `2604.11803` | field_significance / corpus scope | Resolved 2026-10-17: kept (user), on the VietNormalizer precedent at `low`, empty `related_concepts`. |
| `2604.15923` | claims / concept scope | Resolved 2026-10-19 (user): dropped `prosody-control` (no explicit pitch/duration/rate control, only a coarse smoothed emotion class); kept `emotion-synthesis`; Wiki Connections bullet reworded. |
| `2604.15923` | task (vocabulary gap) | Resolved 2026-10-19 (user): kept on the `task: [TTS]` fallback; deferred again, now one of five pages in the `BACKLOG.md` no-text-input task-term item. Revisit around ten pages or at Q2 integration. |
| `2604.16287` | field_significance moderate/low boundary | Resolved 2026-10-19 (user): downgraded to low (translation-focused dataset; synthesis is off-the-shelf TTS scored only via ASR, no listening test). Two `related_concepts` stay; `multilingual-tts` does not qualify. |
| `2604.17435` | claims | Resolved 2026-10-19 (user): claim narrowed to the Aro-Val similarity metric and re-evidenced with Table 1 numbers (single-LoRA 0.51 / 26% NV match vs MoVE 0.53 / 76%), checked against the table image; caveats on 5 raters and unreported NV share of the Aro-Val set added. |
| `2601.04029` | concept scope | Resolved 2026-10-19 (user): dropped `voice-conversion` (VC systems only build the benchmark inputs; no VC claim of its own); VC link kept as a clause in the `evaluation-metrics` bullet; VC Quality Ranking claim kept. |
| `2604.14548` | corpus scope | Resolved 2026-10-19 (user): kept in scope as a spoken-conversational-agent benchmark (SCA precedent: `2510.02352`, VoiceBench); now also tagged `spoken-language-model`. |
| `2604.14548` | metadata | Resolved 2026-10-19 (user): PDF page 1 lists 13 authors, adding Luchao Yao (4th); added to the page `authors`, metadata `authors_full` (13) and metadata `authors` (first-10 convention, so Lei Wang falls out of that list). |
| `iclr-2026-h5KLpGoqzC` | dedup | Resolved 2026-10-18 (user): ICLR record marked duplicate of ingested VoxCPM `2509.24650` (`rejected`, `canonical_id`); VoxCPM page notes the ICLR version and states the page summarises the preprint; `2604.16211` repointed. New general rule in `docs/schemas/metadata.md` (Duplicates and Later Versions): once a page exists, the ingested version stays canonical. |
| `2604.12456` | architecture | Resolved 2026-10-19 (user): `architecture: [transformer-enc-dec]` (single-pass non-autoregressive MMDiT-style converter; adversarial losses are inherited SAC training terms, not the architecture); index row updated. |
| `2604.20842` | task | Resolved 2026-10-19 (user): page `[SCA, evaluation]` stays; metadata left as filter output. The page-vs-metadata `task` divergence (210 of 935 ingested records) is tracked as a `BACKLOG.md` item. |
| `2505.02625` / `2025.acl-long.912` | duplicate pages (pre-existing) | Resolved 2026-10-19 (user): deferred; logged as the third pair in the `BACKLOG.md` duplicate-pairs item (ACL ID intended canonical; one integration-side pass for all pairs). |
| `2604.21406` / `2604.14548` | concept consistency | Resolved 2026-10-19 (user): benchmarks that feed real audio into existing speech LMs and measure their behaviour carry `spoken-language-model` (WildSpeech-Bench / ESPnet-SDS precedent). Added to VoxSafeBench with a Wiki Connections bullet; HumDial unchanged; rule added to the ingest SKILL.md. |
| `2604.22225` | concept scope | Resolved 2026-10-19 (user): dropped `zero-shot-tts` (six systems are scored, not built); profiling finding kept as a clause in the `evaluation-metrics` bullet. |

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
    if '2026-04-01' <= str(m.get('published_date') or '') <= '2026-06-30':
        c[m['status']] += 1
print(f\"Ingested: {c['ingested']} | Remaining: {c['accepted']} | Rejected: {c['rejected']}\")
"
```

---

## Commit / Push Workflow

See `docs/ingest-protocol.md` (section 9, Session close) for the commit, push, merge and
site-bump sequence and the worktree notes.
