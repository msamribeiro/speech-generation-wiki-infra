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

Fetch, filter, and review triage are done for Q2 2026 (see Session Log, 2026-08-23, 2026-09-19 and
2026-09-21): 241 `accepted` papers in the window. 230 of them are downloaded, parsed and ready to
ingest; **11 newly accepted ones (from the triage of 2026-09-21) still need a download and parse**.
Ingest itself has not started.

To resume:

1. **Download and parse the newly accepted papers.** 29 papers were accepted from the review queue
   across all quarters: 11 in the Q2 window and 9 in Q1 (`accepted` with no `pdf_path`; the other 9
   are July-August). Run `download_pdfs.py` (scope with `--published-from` / `--published-to`), then
   `batch_convert.py`. Triage is not required to start ingest; the 230 already-parsed papers are
   independent of it. The 9 Q1 papers are stragglers (see the 2026-09-21 continuation entry): ingest
   them as a small closing Q1 batch.
2. Build the first chronological candidate list from the `accepted` Q2 papers (sort by
   `published_date`, not ID prefix; see the ID-prefix note below). April is entirely parsed.
3. Check with the user before starting: the trunk checkout's `BACKLOG.md` (another stream, Q4 2025
   content cycle) marks ingest "P0 · queued" behind that cycle as of 2026-09-19.
4. Proceed with the standard batches-of-4 cadence below.

**OpenReview (side thread, not blocking ingest):** live fetches are blocked by a browser-verification
gate, so use the saved-page path (`openreview.py --from-file`; the user saves the API pages from a
browser). The 20 ICML 2026 candidates (Q3) are written, filtered and, for the 2 accepted, parsed (see
the 2026-09-21 continuation entry); they are ready to ingest whenever Q3 is reached. OpenReview PDF
downloads are behind the same gate, so an OpenReview-only paper needs its PDF saved by hand from
`openreview.net/pdf?id=<forum id>` into `raw/papers/{id}.pdf`. NeurIPS 2026 had no accepted papers
posted on 2026-09-21; re-save its pages later and run the same way.

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

---

## Manual Verification Queue

Papers where the ingest agent emitted `review_flags` in its INGEST_RESULT signal. Review these
after the session batch is complete — check the paper page and resolve each flag by hand.

| Paper ID | Flag | Agent note |
|----------|------|------------|
| `2026.iwsds-1.16` | field_significance moderate/low boundary | Resolved 2026-09-27: downgraded to low (narrow 20-participant single-model pilot, no comparison group). |

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
