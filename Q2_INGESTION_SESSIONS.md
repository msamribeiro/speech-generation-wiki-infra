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
| Remaining to ingest (accepted) | 230 |
| Pending human triage (review) | 18 |
| Rejected | 49 |
| **Total Q2 2026 in scope so far** | **302** |

As of 2026-08-23, after the arXiv fetch top-up and ACL Anthology 2026 fetch in this session (see
Session Log). Breakdown by month (`published_date`-derived):

| Month | Accepted | Ingested | Review | Rejected | Total |
|-------|----------|----------|--------|----------|-------|
| April 2026 | 77 | 5 | 0 | 19 | 101 |
| May 2026 | 57 | 0 | 6 | 12 | 75 |
| June 2026 | 96 | 0 | 12 | 18 | 126 |

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
Q2 papers need human triage in `raw/review_queue.md` before the scope count is fully final. The 5
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

Fetch top-up is done (see Session Log below) — Q2 2026 now has a complete, quarter-wide accepted
pool (221 papers, April–June), matching the Q3/Q4/Q1 2026 precedent of not starting ingest until
fetch+filter closes out the full quarter. The user explicitly chose to stop after the fetch+filter
pass this session rather than start ingesting immediately.

To resume:

1. Optionally triage the 15 `review`-status Q2 papers in `raw/review_queue.md` first (not required
   to start ingest — the 221 `accepted` papers are independent of these).
2. Build the first chronological candidate list from the 221 `accepted` Q2 papers (sort by
   `published_date`, not ID prefix — see the ID-prefix note below).
3. ICASSP 2026 (and ASRU/SLT) still have no dedicated fetcher — raised to the user 2026-08-23, not
   yet resolved either way. Worth a decision before or during the sweep on whether to build one.
4. Proceed with the standard batches-of-4 cadence below.

**Cadence:** carried forward unchanged from Q1 2026 — sequential batches of 4, one paper at a time,
health check after each paper, a short batch summary plus explicit go-ahead before the next batch.
The user may drop to one-paper-at-a-time-with-go-ahead mid-session (this happened during Q1 2026);
follow whichever cadence was most recently requested rather than defaulting back silently.

---

## Success Criteria

- All accepted Q2 2026 papers have `status: ingested` in `raw/metadata/`
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

Default (as run throughout Q3/Q4/Q1 2026): pre-select the full remaining list chronologically up
front, then work through it in batches of 4. Within each batch:

1. One paper at a time — no parallel ingest workers.
2. Run the per-paper health check after each paper; fix bare wikilinks and any schema errors
   before moving to the next paper.
3. After all 4 papers in the batch are clean, write a short batch summary (paper IDs, notable
   QC catches, corpus page count, updated Q2 progress numbers) and append it to this file's
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

- **Paper count drift.** `wiki/index.md`'s paper-count callout (3 occurrences: abstract callout,
  "Browse the Papers" section line, "Browse all N papers" link) drifts on most ingests, in both
  directions, with no reliable pattern — including drift that leaves the 3 occurrences mutually
  inconsistent with each other, not just stale. After every paper, independently run
  `ls wiki/papers/*.md | grep -v index.md | wc -l` and `grep -c '^| \[\[' wiki/papers/index.md`
  (these two should always match each other) and fix all 3 `index.md` occurrences directly against
  that number. This is not fixable by prompting — budget for a manual fix on every single paper.
- **Citation integrity.** Before trusting a `[[wikilink]]` the agent added to Wiki Connections,
  confirm the target actually has a wiki page (`ls wiki/papers/{id}.md`) and isn't just
  `status: accepted` or `rejected` in metadata. If it has no page yet, keep the ID in
  `related_papers` frontmatter but remove it from the linked prose (do not cite a page that
  doesn't exist). Agents' own `references.json` `in_corpus` flags are frequently stale in both
  directions — cross-check against the real `wiki/papers/` directory, not the flag.
- **Duplicate / row count.** Confirm exactly one row for the paper ID in `papers/index.md`.
- **Index row completeness.** The Org column sometimes ships blank despite a valid frontmatter
  `organization` field, and Task tags occasionally get truncated relative to the page's own
  `title:`. Compare the index row against the page's own frontmatter directly, in full — don't
  trust the row as written. See [[feedback_index_row_completeness]].
- **Title truncation.** `papers/index.md` rows use a deliberate hard 55-character truncation
  (`title[:55]`) — this is the intended convention, not a bug. Verify every new row's title is
  truncated to (approximately) 55 characters, not the full untruncated title (agents sometimes
  "fix" the truncation they see on neighboring rows) and not cut off mid-word at an unpredictable
  point either. See [[feedback_title_truncation]].
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
- **Concept-tag scope.** A concept tag is only legitimate if the paper actually performs or is
  directly evaluated on that concept, not merely discusses, contrasts, or defers to it (e.g. citing
  another system as background motivation). Check the concept's own scope note and the paper's own
  Limitations section before trusting the tag. See [[feedback_concept_scope_mistag_pattern]] — this
  applies equally to `architecture`-derived concept tags (e.g. `transformer-enc-dec-tts` should be
  present whenever `architecture` includes `transformer-enc-dec` and the paper genuinely trains or
  evaluates that architecture family), not just `task`-derived ones.
- **Agent self-report is not evidence.** An ingest agent's closing summary ("everything checks out",
  "health-check clean") can be flatly wrong even when it sounds confident — always re-run the health
  check and the grep-based checks above yourself rather than trusting the narration. See
  [[feedback_agent_selfreport_unreliable]].

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
  `related_concepts` even when explicitly warned; verify independently every ingest. The same
  omission recurs on `architecture` tags (e.g. `transformer-enc-dec` present but
  `transformer-enc-dec-tts` missing from `related_concepts`) — check both directions. See
  [[feedback_task_related_concepts_mismatch]].
- **`autoregressive-codec-tts` concept tag** — scoped specifically to neural-codec-token
  autoregression (VALL-E-style). Evaluating a classic mel-frame AR acoustic model (e.g. Tacotron 2)
  does not qualify on its own, even in an otherwise legitimate `evaluation-metrics`-tagged paper.
- **YAML date/ID coercion** — unquoted dates parse as YAML date objects, and unquoted numeric-
  looking IDs (e.g. `1412.6980`) parse as floats, dropping trailing zeros. Quote all date fields
  and the `id` field as strings. See [[feedback_yaml_coercion_gotchas]].
- **`task` frontmatter serialization** — canonical form is bracket-unquoted (`task: [TTS, evaluation]`),
  never bracket-quoted (`task: ["TTS", "evaluation"]`). This drift is a known, not-yet-corpus-wide-
  fixed BACKLOG.md item; fix it on sight in any page an ingest agent touches.
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
decoding, lip-to-speech, audio-continuation-only systems). Several Q3/Q4/Q1 2026 papers were tagged
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

**Resume here next session:** re-run `openreview.py --venue ICLR --year 2026 --dry-run` and
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
    if y == '2026' and mo in ('04','05','06'):
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
   its Q2 progress line has gone stale), commit; then bump the `wiki/` submodule pointer to the
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
pushing, fast-forward the `work/ingest` worktree branch back to `main` in both repos. Also note:
a worktree's `wiki/` submodule can appear as an empty, uninitialized directory even when
`.gitmodules` lists it — run `git submodule update --init wiki` before trying to check it out or
bump it, or `git remote -v` inside it will misleadingly report the parent repo's remote.

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
