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

The Q2 sweep is under way. As of 2026-10-18 (session close), by canonical `published_date`:
**52 ingested + 178 `accepted` remaining** (all downloaded and parsed). The second round of 16
(published 2026-04-17 to 04-24, batches A-D in the Session Log) is done; `2601.11329` (F-Actor) was
rejected as a duplicate of `2026.findings-acl.242` (canonical, Q3, parsed). Corpus: 941 pages.
**The Manual Verification Queue has 13 open items**, deliberately held by the user ("keep these in
mind for now"); bring them up again before or after the next round. Site not yet bumped for this
round.

To resume:

1. Resolve the VoxCPM dedup first: `iclr-2026-h5KLpGoqzC` (04-27) is the ICLR version of ingested
   `2509.24650`; under the OpenReview rule it becomes `is_duplicate` + `rejected` (confirm with the
   user), and `2604.16211`'s `related_papers` switches to `2509.24650`.
2. Pre-select the next 16 by `published_date`. Next candidates start: `2604.22542` (04-24),
   `2604.21164` (04-27), then the ICLR 2026 records dated 04-27 (`iclr-2026-0oXyMbPMtP`,
   `iclr-2026-17DNmdQ9aU`, `iclr-2026-5o0ZvYzh6B`, `iclr-2026-CcmDDh070o`, `iclr-2026-F7GmbfyVg9`,
   ...). Title-match each ICLR record against the whole corpus first (OpenReview dedup rule). Skip
   dedup pointers (`wiki_page_id` set).
3. Main-session cleanup per paper (Mitigation B: agents write the page only): index row with Org
   by hand (`organization` is null on nearly every 2026 record), all 3 `index.md` counts, `log.md`
   entry, metadata `status`/`ingested_date`/`generation_history`, then the scoped health check,
   date/ID quoting, callout, and citation-integrity checks. Run this after each paper, not at batch
   end.
4. Point every ingest agent at the content-ingest worktree:
   `SPEECH_WIKI_CONTENT_DIR=/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content-ingest`
   (the resolver otherwise returns the trunk content checkout). Tell agents to use piped
   `[[id|Name]]` paper links in Wiki Connections: the ingest SKILL.md template still shows the bare
   form.
5. **Extra QC per paper:** `health_check.py --module ingest` now emits a `related_concepts_complete`
   warning when a `task` tag (`singing`, `VC`, `codec`) lacks its concept slug. Treat it as a fix-now
   item. It deliberately does not cover `architecture` tags (about 227 mostly intentional hits in
   the 2026-10-16 baseline), so keep checking those by hand per the standing QC rule.
6. **Recurring issues (2026-10-17, confirmed again 2026-10-18):** `references.json` `in_corpus` flags miss most real
   matches (or come back null), so agents must match citations by hand; agents sometimes write
   false "internal inconsistencies" onto the page (check each against the source: different test
   conditions or per-group vs total counts are not inconsistencies); conference-accepted arXiv
   papers (ICASSP, Speech Prosody, LREC) keep the arXiv date per the user.

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

---

## Manual Verification Queue

Papers where the ingest agent emitted `review_flags` in its INGEST_RESULT signal. Review these
after the session batch is complete — check the paper page and resolve each flag by hand.

| Paper ID | Flag | Agent note |
|----------|------|------------|
| `2026.iwsds-1.16` | field_significance moderate/low boundary | Resolved 2026-09-27: downgraded to low (narrow 20-participant single-model pilot, no comparison group). |
| `2026.propor-1.81` | field_significance low/moderate boundary | Resolved 2026-10-17: kept at moderate (user). |
| `2604.06327` | field_significance low/moderate boundary | Resolved 2026-10-17: kept at low (user); noted as a useful source for objective-metric evidence (`evaluation-metrics`). |
| `2605.27383` | claims (numbers inconsistent across tables) | Resolved 2026-10-17: verified against source; warning callout rewritten (2 of 5 claimed inconsistencies were setting differences or per-language counts). Claims cite single tables. |
| `2604.10065` | field_significance low/moderate boundary | Resolved 2026-10-17: kept at moderate (user). The controlled finding (full-token GRPO degrades content, action-space projection avoids it) carries the level; the page already states the small, mixed gains over delayed Moshi. |
| `2604.10413` | task (vocabulary gap) | Resolved 2026-10-17: not in the gap. The model is text (phoneme) driven FastSpeech 2 with sign-video prosody conditioning, same shape as `interspeech-2025-1494`, so `task: [TTS]` is correct. The real gap (no text input) is tracked in `BACKLOG.md`. |
| `2604.11803` | field_significance / corpus scope | Resolved 2026-10-17: kept (user), on the VietNormalizer precedent at `low`, empty `related_concepts`. |
| `2604.15923` | claims / concept scope | Open: `prosody-control` and `emotion-synthesis` tags (and the facial-emotion-as-prosody-proxy claim) rest on a coarse smoothed emotion-class signal; consider dropping `prosody-control`. |
| `2604.15923` | task (vocabulary gap) | Open: video-to-speech with no text input, tagged `task: [TTS]` as the standing fallback. |
| `2604.16287` | field_significance moderate/low boundary | Open: dataset-plus-benchmark preprint; only 2 `related_concepts` after the tagging rules. |
| `2604.17435` | claims | Open: claim that objective emotion metrics miss non-verbal differences rests on the authors' remark, with no side-by-side objective NV numbers. |
| `2601.04029` | concept scope | Open: `voice-conversion` tag rests on VC systems used to build the benchmark and judges tested on voice-cloning output; the paper has no VC system of its own. Check against the concept-scope mistag pattern. |
| `2604.14548` | corpus scope | Open: speech-LM understanding safety benchmark, no speech-generation output evaluated; kept on the VoiceBench / `2510.02352` precedent pending confirmation. Only `evaluation-metrics` in `related_concepts`. |
| `2604.14548` | metadata | Open: parsed author list has 13 names (adds Luchao Yao), metadata `authors_full` has 12; check the PDF before correcting. |
| `iclr-2026-h5KLpGoqzC` | dedup | Open: ICLR 2026 version of VoxCPM `2509.24650` (ingested). Under the OpenReview dedup rule arXiv stays canonical and the ICLR record becomes `is_duplicate` + `rejected`. In the next pre-selection window (04-27); `2604.16211` lists the ICLR ID in `related_papers` and should switch to `2509.24650` once resolved. |
| `2604.12456` | architecture | Open: `architecture: [GAN]` for an MMDiT-style transformer converter trained with SAC's adversarial losses; no `gan-vocoder` concept. Check whether `GAN` is the right architecture term. |
| `2604.20842` | task | Open: page `task: [SCA, evaluation]` differs from metadata `[TTS, evaluation]`; decide whether to align metadata. |
| `2505.02625` / `2025.acl-long.912` | duplicate pages (pre-existing) | Open: LLaMA-Omni2 has two ingested pages, arXiv and ACL 2025. By the ACL precedent the ACL ID is canonical. Not caused by this session. |
| `2604.21406` / `2604.14548` | concept consistency | Open: `spoken-language-model` is tagged on the HumDial challenge page (directly evaluates Moshi, Freeze-Omni and submitted systems) but excluded on VoxSafeBench (prompting-only evaluation of Qwen3-Omni, Kimi-Audio etc.). Decide one rule for benchmarks that evaluate existing speech LMs and apply it to both. |
| `2604.22225` | concept scope | Open: `zero-shot-tts` rests on six zero-shot TTS systems being scored, not built; dropping it leaves 2 concepts. |

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
