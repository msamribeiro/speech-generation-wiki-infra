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
| Already ingested (Q4 2025) | 75 |
| Remaining to ingest | 109 |
| Rejected | 63 |
| **Total Q4 2025 in corpus** | **247** |

As of session 15 close (2026-07-18). Corpus stands at **640 wiki pages**, 0 errors corpus-wide.
One paper (`2510.12116`) remains `status: accepted` but undecided pending a scope call — see
`raw/review_queue.md`; skip it again rather than re-ingesting on autopilot until it's resolved.
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
since 2026-07-19, which would shift IDs/counts. If the list below no longer matches
`raw/metadata/`'s current `accepted` set for Q4 2025, re-select fresh candidates chronologically
by `published_date` rather than assuming this list is still accurate.

**Prior list (session 15, 32 papers) fully consumed as of session 15 close**: items 1–25
processed (24 ingested + `2510.12116` flagged and left `accepted`/undecided), items 26–32
absorbed into this fresh list below (renumbered 1–7), plus 17 new items chronologically after
them. Session 15 also caught and fixed a batch-numbering mistake that silently dropped one list
item without the batch looking short — see [[feedback_batch_execution_undercounting]]. **Always
cross-check the actual committed paper IDs against this table's `#` column at the end of every
batch (not just at session close), not just the running ingested-count.**

**List fully consumed as of session 16 batch 8 close (2026-07-27).** All 16 items resolved: 12
ingested, 2 rejected (`2507.14815`, `2025.findings-emnlp.716`), plus `2510.20210`–`2510.26190`
(the 16 items before this list, session 16 batches 1–4 on 2026-07-26) already closed out earlier.
**Next session: re-run the candidate-selection script fresh** (see Scope section above) rather than
assuming a stale list. Continue chronologically from the first remaining paper after
`2025.findings-emnlp.933`.

**Correction, investigated post-session-close (2026-07-27):** the "9 new EMNLP papers appeared
mid-session" note above (session 16 batch-1 log entry) was wrong about *why* — nothing was newly
fetched. Traced all 9 back to `fetched_date` 2026-05-22–24 and the `filter` entry in
`raw/pipeline_log.md` dated 2026-05-25 ("ACL 2025 + EMNLP 2025 + NAACL 2025 + Interspeech 2025 +
arXiv + workshops pending batch — 300 accepted, 39 review, 56 rejected") — they were `status:
accepted` over two months before this session and simply weren't in session 15's manually-built
candidate list from 2026-07-19. That's a **curation gap in list-building**, not new corpus growth:
the list must have been built by extending a prior list rather than re-running the full accepted-set
query fresh. **Action for next session:** `2511.03080` (PolyNorm, same 2025-11-05 EMNLP date, same
`fetched_date`/filter batch as the 9) is still sitting `status: accepted` and was never picked up —
fold it into the next chronological batch rather than assuming today's list was exhaustive. More
generally, always build the candidate list from a fresh query of the full `accepted` set sorted by
`published_date`, never by extending/renumbering a previous session's list — that's what caught this
gap in the first place.

**Pre-flight checks done for this list (2026-07-27):** no full-version/duplicate `arxiv_comment`
signals on any of the 16 (checked before batch 1), no existing wiki pages, no title collisions.
Items 7 (`2025.emnlp-main.1160`) and 16 (`2025.findings-emnlp.933`) are the proceedings-canonical
versions of two arXiv preprints (`2507.22968` C3-Bench, `2502.17810` URO-Bench) already correctly
rejected as duplicates at fetch time — ingest items 7 and 16 normally, this is not a fresh dedup
decision. `2510.12116` remains pending in `raw/review_queue.md` — do not re-select it.

Corpus-scope precedent chain to keep applying: `2025.emnlp-main.1160` (C3), `2025.emnlp-main.1447`
(MULTIVOX), and `2025.findings-emnlp.933` (URO-Bench) are all SCA/evaluation benchmark papers —
check each against the AURA/VoiceAgentBench-vs-FAMA/MLC-SLM precedent (does the benchmark score the
system's generated *speech* output, or only text/structured output from a system that merely
consumes speech input?) rather than assuming either way from the title. `2025.findings-emnlp.716`
is a general AR-model speculative-decoding survey with only incidental TTS relevance — worth a
second look on whether it clears the corpus bar, similar to the reasoning applied to `2507.14815`.

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
- **Title truncation.** Compare the title in the new `papers/index.md` row against the page's own
  `title:` frontmatter, in full. Agents intermittently cut titles off mid-word (e.g. at ~57
  characters) with no reliable pattern — recurred across all 13 rows added in session 16 before
  being caught. Not fixable by prompting alone; budget for a manual check on every paper. See
  [[feedback_title_truncation]].
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

**Session 2026-07-18, session 15 close — gap found and fixed, then committed and pushed:** While updating this session log after batches 1–6, found that `2510.10785` (FAC-FACodec, item 9 on the pre-selected list) had been silently dropped — batch 3 was mislabeled internally as "items 9–12" when it actually ingested items 10–13 (`2510.11646`, `2510.11124`, `2510.12964`, `2510.12116`), skipping item 9 without anyone noticing since the batch still contained 4 IDs and looked complete. Flagged to the user immediately; user chose to ingest it as a same-session follow-up rather than deferring. Ingested cleanly, 0 errors, genuine VC task tag (real SPK-SIM speaker-similarity metrics on L2-Arctic). Corpus 639 → 640 pages. Final Q4 progress for the session: **75 ingested / 109 remaining** (63 rejected, `2510.12116` still pending a scope call).

All three repos committed and pushed. Content (`dd4eb36`, 23-paper batch commit, then a follow-up commit for `2510.10785`): 24 new paper pages total + assets, `index.md`/`log.md`/`papers/index.md` updated. Infra — three commits: `8aa86f5` (23 metadata files + `BACKLOG.md` + this session log + `review_queue.md` + `pipeline_log.md`), `bd05e7e` (wiki submodule bump to `dd4eb36`), plus a follow-up pair for the `2510.10785` fix. Site: content submodule bump (`e9e0da9`, then a follow-up bump), live deploy triggered — user explicitly authorized both this session. Stray `flow-matching-render-v2-test-2026-06-26.md` again left untouched. Next session: continue Q4 2025 from item 26 (`2510.20210`) of the pre-selected list — 109 papers remaining, plus `2510.12116` pending.

---

**Session 2026-07-26, session 16, batch 1 of ? (list re-verified before starting):** Re-checked the 24-paper pre-selected list from session 15 close against current `raw/metadata/`: items 1–20 (batches 1–5) still hold, but items 21–24 are stale — 9 additional 2025-11-05 EMNLP-related papers (`2025.emnlp-main.1160`, `2025.emnlp-main.1447`, `2025.emnlp-main.1492`, `2025.findings-emnlp.1381`, `2025.findings-emnlp.1394`, `2025.findings-emnlp.524`, `2025.findings-emnlp.716`, `2025.findings-emnlp.933`, `2511.03080`) were added to the accepted set since 2026-07-19, sharing a date with the two originally-selected items and pushing everything after item 22 forward. Will rebuild items 21+ once the session reaches that point. Also surfaced one previously-unchecked ID-prefix/date mismatch inside the still-valid range: `2511.00256` (item 18, Nov arXiv ID vs. Oct 31 `published_date`) — checked `arxiv_comment` ("Under review for IEEE Transactions on Affective Computing", no full-version language) and title against `papers/index.md`, no dedup conflict, clean.

Batch 1 (`2510.20210` Vox-Evaluator, `2510.20513` Decoding the Ear, `2510.20677` R2-SVC, `2510.21209` SpecTokenizer) all ingested cleanly, 0 rejected. Corpus 640 → 644 pages, 0 errors, 1170 warnings unchanged. Notable QC catches: (1) `2510.20513`'s task tag was changed from the pre-assigned `[TTS, evaluation]` to `[SCA, evaluation]` by the ingest agent — verified reasonable (the paper benchmarks 7 SOTA speech-to-speech dialogue systems and fine-tunes one via SFT, matching the FD-Bench precedent rather than a generic TTS-metric paper like UTMOS); (2) `wiki/index.md`'s paper-count callouts drifted on every single paper this batch as usual (one ingest agent's own "fix" undercounted via a substring-match bug, another only updated 1 of 3 occurrences), all caught and corrected manually against real `ls`/grep counts; (3) mid-batch, discovered that a git working-tree-modifying command (likely run by one of the ingest agents, `git checkout`/`restore`/`reset` on `index.md` specifically) silently reverted an in-progress count fix on `index.md` all the way back to the last-committed value (640), while leaving `papers/index.md`, `log.md`, and new page files untouched — confirmed via `git reflog` (`reset: moving to HEAD`). No data was permanently lost since the value is fully re-derivable from `ls`/grep, but flagged explicitly to the user and the 4th ingest agent was briefed to avoid any working-tree-modifying git command for the rest of the session. Q4 progress: 79 ingested / 105 remaining (2510.12116 still pending).

---

**Session 2026-07-26, session 16, batch 2 of ?:** Batch 2 (`2510.21685` StylePitcher, `2510.22241` FOA Tokenizer, `2510.22588` UltraVoice, `2511.05516` Ming-UniAudio) all ingested cleanly, 0 rejected. Corpus 644 → 648 pages, 0 errors, 1170 warnings unchanged. Two corpus-scope/tagging judgment calls this batch, both verified: (1) `2510.22241` (FOA Tokenizer) is a spatial-audio (First Order Ambisonics) codec rather than the usual mono speech codec — accepted as in-scope after confirming it reports genuine speech-domain evaluation (WER, DistillMOS on SpatialVCTK/VCTK speech) and builds directly on in-corpus neural-codec papers, stronger speech relevance than the existing accepted precedent (SpectroStream, a music-only codec with no speech evaluation); (2) `2511.05516` (Ming-UniAudio) was pre-tagged `SCA` but on inspection is a unified understanding/generation/editing speech LLM (ASR, voice cloning, instruction-guided editing) with no spoken-dialogue/conversation setup — confirmed via its own architecture figure showing three task branches (Understanding/Generation/Editing), none of them dialogue; `SCA` and `spoken-language-model` were correctly dropped, `codec` added instead as a second genuine task tag for its separately-evaluated MingTok-Audio tokenizer. Also caught: `2510.22588` (UltraVoice) correctly excluded `subjective-evaluation` despite the paper calling its scores "MOS" — they're actually generated by an audio-LM judge (Gemini-2.5-Flash), not human raters; flagged explicitly on the page via a `complicates:` claim so it isn't later mistaken for genuine listening-test evidence.

Session-limit interruption occurred on the first attempt at `2511.05516` (cut off before any file was written). Verified clean per the interruption-recovery protocol (no page, no index row, no assets, no log entry, metadata still `accepted`, all 7 prior batch papers untouched) and retried from scratch; the retry ingested cleanly. `wiki/index.md`'s paper-count callouts drifted after nearly every paper this batch as usual (agents either don't touch the file per instruction, or partially update it); all corrected manually against real `ls`/grep counts, no further working-tree-modifying git incidents this batch. Q4 progress: 83 ingested / 101 remaining (63 rejected, `2510.12116` still pending).

---

**Session 2026-07-26, session 16, batch 3 of ?:** Batch 3 (`2506.21864` DeepOmni, `2510.23312` LRAC Challenge Description, `2510.23541` SoulX-Podcast, `2510.25178` SFMS-ALR) all ingested cleanly, 0 rejected. Corpus 648 → 652 pages, 0 errors, 1170 warnings unchanged. Notable: (1) `2506.21864`'s own PDF content consistently used the name "DeepOmni" while the source metadata's abstract/GitHub link still referenced an earlier project name, "DeepTalk" — treated the parsed paper body as canonical per the source-of-truth invariant and used DeepOmni throughout; SCA/spoken-language-model tags verified genuine (real speech-to-speech spoken QA evaluation, Table 2); (2) `2510.23312` correctly ingested independently of its companion `2510.00264` (same LRAC challenge, different paper — description vs. baseline systems) with no fabricated cross-links; `subjective-evaluation` verified genuine (large-scale crowdsourced MUSHRA-1S/DCR/ACR/DRT listening tests, not automated proxies); (3) `2510.23541` and `2510.25178` both carried genuine `multilingual-tts` tags verified against their own training data/experiments (Sichuanese/Cantonese/Henanese dialect training data; English-Spanish/English-Chinese/Hindi-English/French-Arabic evaluation respectively), not just title claims.

`wiki/index.md`'s paper-count callouts drifted on 3 of 4 papers this batch (agents overwriting only 1–2 of the 3 occurrences with self-computed, usually-wrong values), all caught and corrected manually against real `ls`/grep counts as usual; no working-tree-modifying git incidents this batch. One agent (item 12, `2510.25178`) flagged that it had touched `index.md` counts despite the standing instruction not to, then found itself unable to cleanly revert — no harm done, the calling session's normal post-paper count reconciliation absorbed it. Q4 progress: 87 ingested / 97 remaining (63 rejected, `2510.12116` still pending).

---

**Session 2026-07-26, session 16, batch 4 of ? — new corpus-wide QC bug found and fixed:** Batch 4 (`2510.24372` Bayesian Speech Synthesizers, `2510.25566` PitchFlower, `2510.25577` Lost in Phonation, `2510.26190` SP-MCQA) all ingested cleanly, 0 rejected. Corpus 652 → 656 pages, 0 errors, 1170 warnings unchanged.

Session-limit interruption hit twice this batch: once mid-`2510.25566` (verified clean per protocol, retried successfully), and earlier at the very start of session 16 mid-`2511.05516` (batch 2, already logged). Both interruptions left a fully clean state with nothing written.

While checking the `2510.25566` retry's clean state, discovered a new title-truncation bug affecting **all 13 rows added earlier this session** (batches 1–3): every title in `papers/index.md` was cut off mid-word at ~57 characters (e.g. "Bayesian Speech Synthesizers Can Learn from Multiple Te" instead of the full title) — this is the same known-unfixable-by-prompting bug documented in [[feedback_title_truncation]] from earlier sessions, recurring here despite not being explicitly checked per-paper this session (a gap in this session's own QC, now corrected). All 13 rows were rewritten with complete titles pulled directly from each page's frontmatter, verified against the existing full-title convention in older rows. The two ingest agents in this batch after the fix (`2510.25577`, `2510.26190`) were briefed explicitly on the bug and both produced correctly untruncated rows on the first try. **Added title-row completeness to the per-paper QC checklist going forward, not just index-count and citation checks.**

Q4 progress: 91 ingested / 93 remaining (63 rejected, `2510.12116` still pending).

---

**Session 2026-07-27, session 16, batch 5 of ? — new 16-paper list pre-selected, 1 reject:** Re-verified progress (91/93/63, matched log) and re-ran the candidate script; items 17–20 of the prior stale list still held, but items 21–24 were stale (9 new 2025-11-05 EMNLP papers added to the accepted set since 2026-07-19, sharing a date with the two originally-selected items). Rebuilt a fresh 16-paper chronological list (items 1–16: `2507.14815`, `2511.00256`, `2511.00850`, `2511.01056`, `2511.01261`, `2511.02104`, then all 10 remaining 2025-11-05 EMNLP papers) for today's session. Pre-flight checks: no full-version/duplicate `arxiv_comment` signals on any of the 16, no existing wiki pages, `2507.14815`'s July-prefix/Oct-31-published-date mismatch confirmed as the routine prefix-lag pattern (NeurIPS 2025 acceptance note, not a dedup case).

First paper, `2507.14815` (FastLongSpeech), was flagged before writing anything: same shape as the FAMA/MLC-SLM/2510.09424/2510.12116 comprehension-only reject pattern — Qwen2-Audio-based long-speech-input compression whose own output is always text (§2 Eq. 1), every benchmark (Spoken QA incl. its own LongSpeech-Eval, AIR-Bench, MELD, ASR WER, SPIRAL-H) scores text/label accuracy, and the only TTS mention (third-party "Orca") synthesizes benchmark input audio rather than being model output. Surfaced to the user; **rejected**, consistent with precedent. Logged to `review_queue.md` and `raw/pipeline_log.md`, `status: rejected` set.

Remaining batch 1 (`2511.00256` NaturalVoices, `2511.00850` MULTI-Bench, `2511.01056` WhisperVC, `2511.01261` Speech-DRAME) all ingested cleanly, 0 further rejects. Corpus 656 → 660 pages, 0 errors, 1170 warnings unchanged (post-fix; briefly 1175 mid-batch, see below). Two corpus-scope AURA/VoiceAgentBench-precedent checks this batch, both genuine accepts on read: (1) `2511.00850` (MULTI-Bench) scores the SDM's generated *speech* directly — an audio-aware Gemini judge plus UTMOS on the acoustic dimension (§2.2, Table 4), not just text; stronger case for inclusion than the incidental-TTS-input AURA/VoiceAgentBench pattern. (2) `2511.01261` (Speech-DRAME) likewise evaluates generated speech directly — real human raters scoring audio clips on Audio Quality/Prosodic Dynamics/Emotional Expressiveness (§4), and its DRAME-Eval judge is a fine-tuned audio-LLM validated against those human ratings (§6); also scores five cascaded TTS pipelines' acoustic output (Tables 5–6). Both tagged `subjective-evaluation` correctly (MULTI-Bench: no, Gemini-judge only; Speech-DRAME: yes, real listening tests).

QC catches (all on manual verification, not agent self-report): (1) `2511.00256`'s `papers/index.md` row title was truncated ("...Spontaneous and Emotional" cutting the rest) despite the session-16-batch-4 title-truncation fix being in place — confirms this bug recurs per-paper regardless of prior fixes, not something that stays fixed; rewritten with the full title. (2) `2511.00850` and `2511.01261` both had bare `[[id]] (Name)` wikilinks in Wiki Connections (5 and 7 respectively) that the ingest agents' own closing summaries incorrectly claimed matched "the skill template's own prescribed format" — verified false by running the health check directly (7 and 5 `wikilink_format` warnings respectively, 0 after piping to `[[id|Display Name]]`); do not trust an agent's claim that a warning is expected without checking the health check output yourself. (3) `wiki/index.md` count-drift recurred as usual (agents cross-checked with `grep -c '^| \[\['` before writing on `2511.00850`/`2511.01261` and got it right unprompted this time, though `2511.00256`'s agent still needed the manual fix). Also confirmed in passing: `references.json` flagged two rejected arXiv preprints (`2502.17810`, `2507.22968`) as `in_corpus` on `2511.00850` — both are pre-existing, correctly-resolved duplicates of two papers later in today's list (`2025.findings-emnlp.933`, `2025.emnlp-main.1160`), not a new issue.

Q4 progress: 95 ingested / 88 remaining (64 rejected, `2510.12116` still pending). Nothing committed yet this session.

---

**Session 2026-07-27, session 16, batch 6 of ? (batch 2 of the fresh 16-paper list):** Batch (`2511.02104` Prosody Evaluation, `2025.emnlp-main.1160` C3, `2025.emnlp-main.1447` MULTIVOX, `2025.emnlp-main.1492` PACHAT) all ingested, 0 rejected. Corpus 660 → 664 pages, 0 errors, 1170 warnings unchanged.

Three AURA/VoiceAgentBench-precedent scope checks this batch, resolved on both sides for the first time (previously every check this session had landed on the accept side): (1) `2025.emnlp-main.1160` (C3) accepted — mostly text/LLM-judge-scored, but its phonological-ambiguity "Generation" subtask has three human experts directly listen to and label the SDM's generated audio (§4.2), explicitly because the phenomenon "cannot be captured by the transcribed text" — a narrow but genuine speech-output evaluation, flagged on the page via a `complicates:` claim for future spot-checking; (2) `2025.emnlp-main.1447` (MULTIVOX) matches the **reject-shaped precedent instead** (AURA/VoiceAgentBench pattern) — the authors' own Limitations section states outright "we limit our evaluation to the content of the speech outputs and not the speech quality," and the only real audio MOS test (Appendix E) validates the benchmark's *input* speech-prompt construction, not any assistant's output; ingested anyway per the established precedent (TTS/VC incidental to input construction is in-scope), no VC/TTS task tag; (3) `2025.emnlp-main.1492` (PACHAT) verified as a genuine architecture paper, not a benchmark — LoRA-tuned Llama 3.1 + Whisper/Q-Former speech-LLM backbone producing real spoken output via CosyVoice2 at inference, with an end-to-end MOS eval (Appendix C.2); `spoken-language-model` and `speech-to-speech` tags both verified genuine (cascade-pattern spoken dialogue, matching the concept's defined cascade sub-paradigm).

Interruption recovery mid-batch: the first attempt at `2025.emnlp-main.1447` was cut off by a session limit before any file was written. Verified clean per protocol (no page, no index row, no log entry, no assets, metadata still `accepted`, all prior batch papers untouched) and retried from scratch; the retry ingested cleanly.

QC notes: `2511.02104` (prosody evaluation methodology paper) correctly excluded the `prosody-control` tag (evaluation metrics, not a control mechanism) and legitimately carries only 2 `related_concepts` (evaluation-metrics, subjective-evaluation) rather than the usual 3–6 — judged acceptable rather than padded with a spurious third tag, since no other vocabulary term genuinely fits a pure prosody-evaluation-methodology paper. `2025.emnlp-main.1160` and `2025.emnlp-main.1492` both needed bare-`[[id]] (Name)`-to-piped-format wikilink fixes (8 each), applied by the agents themselves this time after being briefed explicitly — first batch this session where agents self-corrected the wikilink format issue rather than the main session catching it after the fact.

Q4 progress: 99 ingested / 84 remaining (64 rejected, `2510.12116` still pending). Nothing committed yet this session.

---

**Session 2026-07-27, session 16, batch 7 of ? (batch 3 of the fresh 16-paper list):** Batch (`2025.findings-emnlp.1077` EZ-VC, `2025.findings-emnlp.1381` UniSpeaker, `2025.findings-emnlp.1394` DM-Codec, `2025.findings-emnlp.241` S2S Dialogue RAG) all ingested, 0 rejected. Corpus 664 → 668 pages, 0 errors, 1170 warnings unchanged.

Session-limit interruption occurred mid-verification of `2025.findings-emnlp.1394` (transient classifier-unavailable error, not an actual write-in-progress cutoff); confirmed clean per protocol (state exactly as left: 667/667 rows, single entry, correct title) and resumed verification directly with no retry needed.

New spurious-tag pattern found twice this batch (not previously seen this session): the `disentanglement` tag applied to papers that *discuss or contrast against* disentanglement rather than perform it themselves. (1) `2025.findings-emnlp.1077` (EZ-VC) — page prose explicitly stated content/speaker separation is achieved "implicitly through... input design rather than through dedicated disentanglement modules"; the paper's own novelty framing is built around *avoiding* disentanglement encoders used by prior work (AdaptVC, StableVC, Seed-VC). Removed. (2) `2025.findings-emnlp.1394` (DM-Codec) — Wiki Connections bullet described the paper's design as "holistic," explicitly contrasted against FACodec's "explicit factorized subspace approach"; DM-Codec's actual contribution (confirmed by reading the Method section) is jointly distilling acoustic/semantic/contextual information into a *single* shared RVQ codebook, the opposite of separating attributes into distinct spaces. Removed. By contrast, `2025.findings-emnlp.1381` (UniSpeaker)'s `disentanglement` tag in the same batch held up on inspection — a genuine self-distillation fine-tuning stage with an explicit "negative-disentanglement re-weighting" term and ablation evidence (Table 3: removing it drops SST from 39.37% to 31.07% on VC) — so this is a real per-paper judgment call, not a blanket rule against the tag.

Other QC: `2025.findings-emnlp.241` (S2S Dialogue RAG) verified as a genuine `speech-to-speech`/`spoken-language-model` fit (end-to-end spoken dialogue sub-paradigm, GLM-4-Voice as the unmodified downstream generator) — first paper this batch where the ingest agent avoided the disentanglement trap itself with no tag applied. All citation-integrity spot-checks (in-corpus reference IDs actually have wiki pages) passed across all 4 papers this batch.

Q4 progress: 103 ingested / 80 remaining (64 rejected, `2510.12116` still pending). Nothing committed yet this session.

---

**Session 2026-07-27, session 16, batch 8 of ? (batch 4 of 4, fresh 16-paper list COMPLETE):** Batch (`2025.findings-emnlp.524` Dub-S2ST, `2025.findings-emnlp.716` AR generation-refinement survey, `2025.findings-emnlp.933` URO-Bench) — 2 ingested, 1 rejected. Corpus 668 → 670 pages, 0 errors, 1170 warnings unchanged.

`2025.findings-emnlp.524` (Dub-S2ST) ingested cleanly: `speech-to-speech` tag verified against the direct/textless S2ST translation sub-paradigm; `disentanglement` correctly excluded by the ingest agent itself this time (off-the-shelf pretrained mHuBERT units + speaker embedding, no explicit factorization training objective) — first batch where an agent avoided this trap without being told the specific paper needed it, just from the general standing reminder. Task tag narrowed from the pre-assigned `[TTS, VC]` to `[TTS]` only: VC appears solely as a comparison baseline/ablation, not the paper's own dedicated system, matching the SeamlessM4T precedent for S2ST papers.

`2025.findings-emnlp.716` (AR generation-refinement survey) was flagged before writing anything, per the standing note from this list's initial pre-flight check: confirmed on full read to be a general LLM/AR-model speculative-decoding survey whose substantive content (§3–6) covers text decoding exclusively; speech content is confined to two sentences in §7.2 citing 2 papers out of 100+ total references, no dedicated speech section, no original speech experiment. Surfaced to the user with title/authors/URL on request; user reviewed directly and confirmed **reject**. Logged to `review_queue.md` and `raw/pipeline_log.md`, `status: rejected` set. This is the second reject this session on a genuine-relevance-test basis (distinct from `2507.14815`'s comprehension-vs-generation test) — subject-matter relevance is negligible relative to the survey's actual general-AR-model scope, not a scope exception.

`2025.findings-emnlp.933` (URO-Bench) ingested cleanly: matches the stronger MULTI-Bench/Speech-DRAME/C3 accept pattern rather than the AURA/VoiceAgentBench/MULTIVOX one — UTMOS scores generated audio directly (§3.3, Table 5), audio-aware judges (Gemini 2.0 Flash, GPT-4o-Audio-Preview) score response audio for expressiveness tasks, and a genuine human listening study (§4.3/Appendix B.3) validates the automatic scores against real raters listening to output audio, not transcripts. `subjective-evaluation` tag verified genuine.

This closes out the full 16-paper list pre-selected at the start of this session (2026-07-27): **12 ingested, 2 rejected (`2507.14815`, `2025.findings-emnlp.716`), 2 removed for spurious tags but otherwise clean.** Q4 progress: 105 ingested / 77 remaining (65 rejected, `2510.12116` still pending). Nothing committed yet this session — next step is either a commit/push at this natural stopping point, or re-running the candidate-selection script to pre-select the next batch (re-check for newly-added papers first, as happened at this session's start).

---

## Manual Verification Queue

Papers where the ingest agent emitted `review_flags` in its INGEST_RESULT signal. Review these
after the session batch is complete — check the paper page and resolve each flag by hand.

| Paper ID | Flag | Agent note |
|----------|------|------------|
| `2510.19509` | field_significance | Level sits at moderate/high boundary; comprehensive first-of-its-kind capability-aware evaluation taxonomy, but actual field influence depends on post-publication adoption not visible from the paper alone. Currently set to `moderate` — revisit if the paper gains citations/adoption in later ingests. |
| `2511.18487` | field_significance | Level sits at high/moderate boundary; single industry preprint with no independent validation, and its own results show mixed outcomes (lower NMOS/QMOS than reference-audio-conditioned or dedicated baselines). Currently set to `high` — revisit if independent validation or wider adoption emerges in later ingests. |

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

**Session 2026-07-28, session 17, batch 1 of 4 (fresh 16-paper list, skipping `2510.12116`):** Re-verified progress (105/77/65, matched log) and re-ran the candidate script; confirmed `2511.03080` (PolyNorm) — flagged at session 16 close as never having been picked up — was still sitting `accepted` and is now the first item after `2510.12116`. Rebuilt a fresh 16-paper chronological list. Pre-flight checks: no full-version/duplicate `arxiv_comment` signals on any of the 16, no existing wiki pages, no title collisions, 670=670 page/index parity confirmed before starting. One ID-prefix/date mismatch noted for later in the list: `2508.20916` (SageLM, May-2025 arXiv prefix vs. `published_date` 2025-11-10) — routine prefix-lag, no dedup signal.

Batch 1 (`2511.03080` PolyNorm, `2511.03601` Step-Audio-EditX, `2511.13732` Speculative Decoding in Speech, `2511.14779` Prosodic Segmentation on Spontaneous Speech) all ingested, 0 rejected. Corpus 670 → 674 pages, 0 errors. QC catches (manual verification, not agent self-report): (1) `2511.14779`'s first draft carried a spurious `prosody-control` tag — the paper uses FastSpeech 2 completely unmodified and studies training-data segmentation strategy, not an inference-time prosody control mechanism; the ingest agent's own summary cited the documented exclusion rule ("do NOT include because the paper evaluates prosody metrics... or includes a standard duration predictor") correctly but then talked itself into an unwarranted exception, reasoning that FastSpeech 2's own page carries the tag (true, but FastSpeech 2 itself introduces the duration/pitch/energy predictor mechanism; this paper doesn't introduce anything, it just isolates training-data segmentation as a variable) — removed from `related_concepts` and the Wiki Connections bullet; (2) same page had one bare `[[2006.04558]]` wikilink (FastSpeech 2) in Wiki Connections, piped to `[[2006.04558|FastSpeech 2]]`. All other pages in the batch clean on first health check, all in-corpus references cross-checked to have real wiki pages before trusting agent-reported `related_papers`/Wiki Connections links, index row counts and titles verified against `ls`/grep and frontmatter independently after every paper (no drift this batch). Q4 progress: 109 ingested / 73 remaining (65 rejected, `2510.12116` still pending). Nothing committed yet this session.

---

**Session 2026-07-28, session 17, batch 2 of 4:** Batch (`2025.arabicnlp-main.38` DialG2P, `2511.06150` BSCodec, `2511.06246` IDMap, `2508.20916` SageLM) all ingested, 0 rejected. Corpus 674 → 678 pages, 0 errors.

Session-limit interruption occurred at the very start of `2511.06150` (agent call failed before any file was written, per a transient classifier-unavailable error). Verified clean per protocol (no page, no index row, no log entry, no assets, metadata still `accepted`, counts still 675=675 exactly as left after `2025.arabicnlp-main.38`) and retried from scratch; the retry ingested cleanly.

Three genuine QC catches this batch (all on manual verification, not agent self-report): (1) `2025.arabicnlp-main.38` (DialG2P) was tagged `transformer-enc-dec-tts` despite being a G2P/phonemization front-end, not a TTS acoustic model — the concept's own aliases ("FastSpeech family", "NAR TTS") make clear its scope is non-autoregressive TTS synthesis, and this paper never synthesizes speech; removed from `related_concepts` and Wiki Connections, leaving `evaluation-metrics` as the sole tag (paper is squarely a TTS front-end per its own problem statement, in-scope on the PolyNorm/TTS-preprocessing precedent, just doesn't fit that particular concept). (2) `2511.06150` (BSCodec) was tagged `autoregressive-codec-tts`, but the page's own Limitations section explicitly states the paper leaves untested "whether the band-split token structure is compatible with autoregressive or other generative modeling approaches" — an acknowledged open question, not something the paper demonstrates; same "discussed/contrasted, not performed" mistag pattern seen with `disentanglement` in session 16 batch 7, removed. (3) `2508.20916` (SageLM) cited F5-TTS via its arXiv ID (`2410.06885`, no wiki page) instead of the canonical ACL wiki ID (`2025.acl-long.313`) in both `related_papers` and two in-prose wikilinks — the exact recurring F5-TTS confusion pattern (see [[feedback_f5tts_paper_id]]), fixed both occurrences plus the array entry.

Other notes: `2508.20916`'s audio-native LLM-judge design was verified to genuinely consume external speech (not transcripts), so `subjective-evaluation` was correctly excluded (LLM-judge, no human raters) and `spoken-language-model` correctly included (external speech consumed by an adapted LLM, matching the WavReward precedent); its parsed source also carries an AAAI 2026 copyright footer suggesting a venue update may be warranted later, left as `arXiv` per the invariant against altering substantive metadata without instruction. `2511.06246` (IDMap)'s `VC` task tag verified genuine (dedicated pseudo-speaker/anonymization system with real EER/WER metrics). All index row counts and titles verified against `ls`/grep and frontmatter independently after every paper, no drift this batch. Q4 progress: 113 ingested / 69 remaining (65 rejected, `2510.12116` still pending). Nothing committed yet this session.

---

**Session 2026-07-29, session 18, pre-selection (list ready, batch 1 not yet started):** Re-verified progress (113 ingested / 69 remaining / 65 rejected, matched log) and re-ran the candidate script fresh rather than extending a prior list. Skipped `2510.12116` (still pending its scope call in `review_queue.md`). Built a fresh 16-paper chronological list, the first 16 remaining Q4 2025 papers by `published_date` after `2510.12116`:

1. `2511.05143` — Synthesizing speech with selected perceptual voice qualities (creaky voice case study)
2. `2511.07116` — BridgeVoC: Revitalizing Neural Vocoder from a Restoration Perspective
3. `2511.07135` — Generating Novel and Realistic Speakers for Voice Conversion
4. `2511.08496` — HQ-SVC: High-Quality Zero-Shot Singing Voice Conversion in Low-Resource Scenarios
5. `2511.09995` — Time-Layer Adaptive Alignment for Speaker Similarity in Flow-Matching Based Zero-Shot TTS
6. `2511.10112` — FabasedVC: Voice Conversion with Text Modality Fusion and Phoneme-Level SSL Features
7. `2511.10262` — MTR-DuplexBench: Evaluation of Multi-Round Conversations for Full-Duplex Speech LMs
8. `2511.10913` — Synthetic Voices, Real Threats: Evaluating Large TTS Models in Generating Harmful Audio
9. `2511.11104` — CLARITY: Contextual Linguistic Adaptation and Accent Retrieval for Dual-Bias Mitigation in TTS
10. `2511.11124` — AV-Dialog: Spoken Dialogue Models with Audio-Visual Input
11. `2511.12074` — MF-Speech: Fine-Grained and Compositional Control in Speech Generation via Factor Disentanglement
12. `2511.12690` — Improving Direct Persian-English Speech-to-Speech Translation with Discrete Units and Synthetic Parallel Data
13. `2511.14249` — Towards Authentic Movie Dubbing with Retrieve-Augmented Director-Actor Interaction Learning
14. `2511.16639` — Codec2Vec: Self-Supervised Speech Representation Learning Using Neural Speech Codecs
15. `2511.18487` — InstructAudio: Unified speech and music generation with natural language instruction
16. `2512.05126` — SyncVoice: Towards Video Dubbing with Vision-Augmented Pretrained TTS Model

Pre-flight checks: no full-version/duplicate `arxiv_comment` signals on any of the 16 (checked
each individually — AAAI/ACMMM-Asia/ACL-Findings/ASRU acceptance notes, "under review," or
empty, none reference a prior arXiv ID or "extended version" language); no existing wiki pages
or `papers/index.md` rows for any of the 16; 678=678 page/index parity confirmed before starting
(`ls papers/*.md | grep -v index.md | wc -l` vs. `grep -c '^| \[\[' papers/index.md`). One
ID-prefix/date anomaly flagged for later in the list: `2512.05126` (SyncVoice) carries a
December-prefixed arXiv ID against a `published_date` of 2025-11-23 — the reverse of the usual
lag pattern (ID ahead of the published date rather than behind it). `arxiv_comment` is empty (no
full-version/extended-version language) and no title/author collision was found against the
corpus, so this is being treated as a routine ID-prefix anomaly per the standing rule to trust
`published_date` for ordering, not a dedup signal — worth a second look if a stronger signal
turns up once the paper is actually read during ingest.

Q4 progress unchanged this entry: 113 ingested / 69 remaining / 65 rejected, `2510.12116` still
pending. Nothing ingested yet — list is ready, awaiting go-ahead to start batch 1 of 4.

---

**Session 2026-07-29, session 18, batch 1 of 4:** Batch (`2511.05143` creaky-voice PVQ case study,
`2511.07116` BridgeVoC, `2511.07135` Novel/Realistic Speaker Generation for VC, `2511.08496`
HQ-SVC) all ingested, 0 rejected. Corpus 678 → 682 pages, 0 errors corpus-wide, 1170 warnings
unchanged.

QC catches this batch (all on manual verification, not agent self-report): (1) title truncation
on `papers/index.md` rows recurred on 3 of 4 papers (`2511.05143`, `2511.07116`, `2511.08496`) —
same known unfixable-by-prompting bug, fixed against each page's own frontmatter `title:` every
time; (2) `2511.07116` (BridgeVoC) had 5 bare `[[id]] (Name)` wikilinks in Wiki Connections, piped
to `[[id|Name]]`; (3) `wiki/index.md`'s 3 paper-count occurrences (abstract callout, "Browse the
Papers" prose line, "Browse all N papers" link) drifted after every single paper this batch, in
both directions and sometimes only partially updated (e.g. after `2511.08496` two lines still read
`681` and the link read `675` against an actual count of 682) — corrected against real `ls`/`grep`
counts each time. `2511.07135` was the one fully clean paper this batch (index count, title, and
wikilinks all correct on first health check).

Tagging judgment calls verified: `2511.07135`'s `VC` task tag confirmed genuine (SpeakerVAE
evaluated inside two dedicated VC pipelines with real cosine-similarity/WER/CER/UTMOS metrics).
`2511.08496` (HQ-SVC) correctly carries both `singing` and `VC` task tags with both reflected in
`related_concepts`, per the standing task/related_concepts consistency check; `disentanglement`
correctly excluded (the paper's own training additions aren't ablated as a distinct mechanism,
and the actual disentanglement work belongs to the frozen externally-trained FACodec backbone,
not to this paper). `2511.05143`'s `field_significance.type` was set to
`[engineering-integration, empirical-benchmark]` rather than `architectural-novelty` since its
core manipulation mechanism carries over from the authors' own prior (out-of-corpus) paper —
correctly triggered no figure copy. All in-corpus reference IDs cited by all 4 pages (HiFi-GAN,
BigVGAN, Vocos, PeriodWave, WaveFM, NaturalSpeech 3/FACodec, FastSpeech 2, and others) verified
to have real wiki pages before trusting `related_papers`/Wiki Connections links; no duplicate
index rows found.

Q4 progress: 117 ingested / 65 remaining (65 rejected, `2510.12116` still pending). Nothing
committed yet this session.

---

**Session 2026-07-29, session 18, batch 2 of 4:** Batch (`2511.09995` Time-Layer Adaptive
Alignment for flow-matching zero-shot TTS, `2511.10112` FabasedVC, `2511.10262` MTR-DuplexBench,
`2511.10913` Synthetic Voices, Real Threats) all ingested, 0 rejected. Corpus 682 → 686 pages,
0 errors corpus-wide, 1170 warnings unchanged.

Session-limit interruption occurred on the first attempt at `2511.10262`, cut off right after the
agent announced it was starting to write the page. Verified clean per the interruption-recovery
protocol (no page, no index row, no assets, no log entry, metadata still `accepted`, all 6 prior
batch papers from batches 1–2 untouched, counts still 684=684 exactly as left after `2511.10112`)
and retried from scratch; the retry ingested cleanly.

QC catches this batch (all on manual verification, not agent self-report): title truncation on
`papers/index.md` rows recurred on 3 of 4 papers (`2511.09995`, `2511.10262`, `2511.10913`) —
fixed against each page's own frontmatter `title:` every time; `2511.10112` was the one fully
clean paper this batch. `wiki/index.md`'s 3 paper-count occurrences drifted after every paper
again, sometimes only 1–2 of 3 updated (e.g. after `2511.10262` the abstract callout still read
684 against an actual 685; after `2511.10913` two lines read 685 and the Browse link read 679
against an actual 686) — corrected against real `ls`/`grep` counts each time.

Two scope/tagging judgment calls verified genuine on inspection: (1) `2511.10262`
(MTR-DuplexBench) correctly excluded `subjective-evaluation` — all four evaluation dimensions
are scored by a GPT-4o judge, not real human listeners, with a `complicates:` claim added noting
the automated-judge caveat; `spoken-language-model` correctly included since the systems under
test (Moshi, Freeze-Omni, VocalNet) consume a genuine live external user audio stream in a real
full-duplex spoken-dialogue context, consistent with the sibling Full-Duplex-Bench precedent
already in the corpus. (2) `2511.10913` (Synthetic Voices, Real Threats) correctly excluded
`subjective-evaluation` (all scoring is automated via Detoxify/COLD/moderation APIs, one informal
author aside about listening doesn't count as a controlled test) and correctly included
`spoken-language-model` — verified by reading the full page: the paper's multi-modal attack
family (Read/Spell/Phoneme) genuinely feeds external audio input into the LALM-based TTS system
for it to consume and re-render as speech, satisfying the external-signal rule rather than being
a plain text-to-speech paper wearing the tag. All in-corpus reference IDs across all 4 pages
verified to have real wiki pages before trusting `related_papers`/Wiki Connections links; no
duplicate index rows found.

Q4 progress: 121 ingested / 61 remaining (65 rejected, `2510.12116` still pending). Nothing
committed yet this session.

---

**Session 2026-07-29, session 18, batch 3 of 4:** Batch (`2511.11104` CLARITY, `2511.11124`
AV-Dialog, `2511.12074` MF-Speech, `2511.12690` Persian-English direct S2ST) all ingested, 0
rejected. Corpus 686 → 690 pages, 0 errors corpus-wide, 1170 warnings unchanged.

QC catches this batch (all on manual verification, not agent self-report): title truncation on
`papers/index.md` rows recurred on all 4 papers this time (first fully-100%-affected batch this
session) — fixed against each page's own frontmatter `title:` every time. `wiki/index.md`'s
paper-count occurrences drifted after 3 of 4 papers (correct after `2511.11124` only) in both
directions, including one case (`2511.12074`) where the count reverted all the way back to a
stale `682` across all three occurrences rather than partially updating — corrected against real
`ls`/`grep` counts each time.

Three tagging/scope judgment calls verified genuine on inspection this batch: (1) `2511.11104`
(CLARITY) correctly excluded both `multilingual-tts` (targets English accent varieties, not
multiple languages, and filtered its own training data down to English-dominant utterances only)
and `disentanglement` (bias mitigation is entirely input-side, via LLM text rewriting and
retrieval-based prompt selection, with no explicit factorization/adversarial training mechanism);
(2) `2511.11124` (AV-Dialog) correctly tagged both `spoken-language-model` (LLaMA3-8B genuinely
consumes external live user speech, alongside video, in a real streaming dialogue context — the
added video modality doesn't disqualify the tag) and `speech-to-speech` (fits the end-to-end
spoken-dialogue sub-paradigm, directly comparable to the already-tagged Moshi/SpiRit-LM); (3)
`2511.12074` (MF-Speech) is the strongest catch this batch — despite the title's own "Factor
Disentanglement" framing, the `disentanglement` tag was independently verified against the actual
Method/ablation sections (per-factor contrastive losses + post-discretization MI minimization via
CLUB/MINE, with genuine Table 2 leakage-accuracy and Figure 4 t-SNE ablations) rather than taken
on the title's word; separately, its `task` was reclassified from the pre-assigned `TTS` to `VC`
since the system takes speech (not text) as input and is benchmarked exclusively against VC
baselines on the VC-standard ESD dataset, with the metadata JSON left untouched per the
never-alter-source-metadata invariant and only the page frontmatter corrected. `2511.12690`
(Persian-English S2ST) correctly narrowed `task` to `[TTS]` only, per the established
SeamlessM4T/Dub-S2ST/MTP-S2UT precedent (no dedicated VC system, only a discrete-unit-to-waveform
vocoder). All in-corpus reference IDs across all 4 pages verified to have real wiki pages before
trusting `related_papers`/Wiki Connections links; no duplicate index rows found.

Q4 progress: 125 ingested / 57 remaining (65 rejected, `2510.12116` still pending). Nothing
committed yet this session.

---

**Session 2026-07-29, session 18, batch 4 of 4 (fresh 16-paper list COMPLETE):** Batch (`2511.14249`
movie dubbing, `2511.16639` Codec2Vec, `2511.18487` InstructAudio, `2512.05126` SyncVoice) all
ingested, 0 rejected. Corpus 690 → 694 pages, 0 errors corpus-wide, 1170 warnings unchanged.

Session-limit interruption occurred on the outer session itself (not an individual ingest agent)
right after `2511.14249`'s ingest agent had already returned a complete, successful result.
Verified clean per the interruption-recovery protocol before proceeding: 691=691 page/index
parity, metadata `status: ingested`, log.md entry present, health check 0 errors — the paper was
genuinely fully ingested, only the outer session's own manual-verification pass had been cut off.
No retry was needed, just resumed the normal per-paper QC pass and continued to the next paper.

QC catches this batch (all on manual verification, not agent self-report): title truncation on
`papers/index.md` rows recurred on all 4 papers again; `wiki/index.md`'s paper-count occurrences
drifted after every paper in this batch, in both directions — corrected against real `ls`/`grep`
counts each time. One genuine citation-integrity catch on `2512.05126` (SyncVoice): both the
`related_papers` frontmatter array and a Wiki Connections prose bullet cited F5-TTS via its
arXiv ID (`2410.06885`, no wiki page) instead of the canonical ACL wiki ID (`2025.acl-long.313`)
— the exact recurring F5-TTS confusion pattern (see [[feedback_f5tts_paper_id]]), not caught by
the automated health check since it only validates wikilink *format*, not whether the target page
exists; fixed both occurrences by hand.

Pre-selection's flagged ID-prefix anomaly on `2512.05126` (December-prefixed arXiv ID against a
November `published_date`) was investigated during ingest per the standing instruction: the ingest
agent read the full paper, checked the author list against the corpus, and found four prior
papers from an overlapping Xiamen University author group, all on unrelated topics (endpoint
detection, voice conversion, codec design) with no title/topic overlap and no self-referential
"extended version" language — confirmed as a genuinely new, distinct paper, not a duplicate.

Two scope/tagging judgment calls verified genuine: (1) `2511.14249` (movie dubbing) correctly
excluded `speech-to-speech` (script+video-conditioned TTS, no speech-in/speech-out or dialogue
component, checked against the concept's own scope note) and `multilingual-tts` (single-dataset
training, no cross-language evidence); (2) `2512.05126` (SyncVoice) correctly included
`multilingual-tts` (own bilingual Chinese/English training with a purpose-built Dual Speaker
Encoder and real cross-lingual EN-ZH evaluation) but excluded `speech-to-speech` for the same
reason as the movie-dubbing paper (video+text input, not speech-in/speech-out). `2511.16639`
(Codec2Vec) correctly carries both `neural-codec` and `self-supervised-speech` given an explicit
codec-choice ablation (DAC vs. Encodec) rather than incidental use of an off-the-shelf codec.
`2511.18487` (InstructAudio) correctly scoped its dual speech/music framework to TTS-relevant
prose without inventing music-specific vocabulary terms, and emitted a genuine `review_flags`
entry (field_significance sitting at the high/moderate boundary — added to the Manual
Verification Queue below). All in-corpus reference IDs across all 4 pages verified to have real
wiki pages before trusting `related_papers`/Wiki Connections links (beyond the one F5-TTS catch);
no duplicate index rows found.

**This closes out the full 16-paper list pre-selected at the start of this session (2026-07-29):
16 ingested, 0 rejected.** Q4 progress: 129 ingested / 53 remaining (65 rejected, `2510.12116`
still pending). Nothing committed yet this session — next step is either a commit/push at this
natural stopping point, or re-running the candidate-selection script to pre-select the next batch.

---

**Session 2026-07-29, session 18, pre-selection (5-paper list, batch not yet started):** Re-ran
the candidate script fresh (53 remaining) rather than extending the just-closed 16-paper list.
Skipped `2510.12116` (still pending). Built a fresh 5-paper chronological list:

1. `2511.19734` — Evaluating Objective Speech Quality Metrics for Neural Audio Codecs
2. `2511.20974` — RosettaSpeech: Zero-Shot Speech-to-Speech Translation without Parallel Speech
3. `2511.21045` — CartoonSing: Unifying Human and Nonhuman Timbres in Singing Generation
4. `2511.21229` — Developing an Open Conversational Speech Corpus for the Isan Language
5. `2511.21270` — Multi-Reward GRPO for Stable and Prosodic Single-Codebook TTS LLMs at Scale

Pre-flight checks: no full-version/duplicate `arxiv_comment` signals on any of the 5 (page-count
notes or empty, nothing self-referential); no existing wiki pages or `papers/index.md` rows for
any of the 5; 694=694 page/index parity confirmed before starting; no ID-prefix/published-date
anomalies (all five IDs are `2511.x` against November 2025 dates, consistent). Noted for later in
the queue (not part of this 5-paper list): `2511.22503` ("Joint Speech and Text Training for
LLM-Based End-to-End Spoken Dialogue State Tracking") is the next chronological item after this
batch and looks like another DST paper matching the `2510.09424` precedent (structured
dialogue-state output, not spoken-output generation) — worth checking against that precedent
chain when it comes up rather than assuming either way from the title.

Q4 progress unchanged this entry: 129 ingested / 53 remaining / 65 rejected, `2510.12116` still
pending. Nothing ingested yet — list is ready, awaiting go-ahead.

---

**Session 2026-07-29, session 18, item 1 of 5 (cadence dropped to one-at-a-time-with-go-ahead
per user request):** `2511.19734` (Evaluating Objective Speech Quality Metrics for Neural Audio
Codecs) ingested. Corpus 694 → 695 pages, 0 errors.

Session-limit interruption hit mid-ingest, right as the agent announced it was about to update
`papers/index.md`, `index.md` counts, `log.md`, and metadata — a genuine partial-write case, not
the usual clean-cutoff case. Checked the standalone content repo per the interruption-recovery
protocol and found: the paper page itself (`papers/2511.19734.md`) and its `papers/index.md` row
were both already written and complete (full page, all required sections, clean frontmatter,
`subjective-evaluation` tag correctly applied for a genuine MUSHRA listening test with real human
raters), but `log.md` had no entry and `raw/metadata/2511.19734.json` was still `status:
accepted`. Read the full page to confirm it wasn't a mid-write truncation before deciding to
reuse rather than discard; health check passed 0 errors, 0 warnings on the page as found. Rather
than re-running a fresh ingest agent (which would have re-written the already-correct page),
completed the missing steps by hand: fixed the usual title truncation on the index row, corrected
`wiki/index.md`'s 3 count occurrences (694 → 695), appended the missing `log.md` entry matching
the established format, and set `status: ingested` / `ingested_date` / `generation_history` on
the metadata JSON to match the pattern used by the agent-driven ingests earlier this session.

Q4 progress: 130 ingested / 52 remaining (65 rejected, `2510.12116` still pending). Nothing
committed yet this session.

---

**Session 2026-07-29, session 18, item 2 of 5:** `2511.20974` (RosettaSpeech) ingested. Corpus
695 → 696 pages, 0 errors.

Tagging judgment calls verified genuine: `task` narrowed to `[TTS]` only, per the established
SeamlessM4T/Dub-S2ST/MTP-S2UT/Persian-English-S2ST precedent — speaker preservation runs through
an unmodified, never-fine-tuned off-the-shelf CosyVoice2 CFM component, unlike Dub-S2ST's
synthesizer which the paper does fine-tune as part of its own system. `zero-shot-tts` correctly
excluded from `related_concepts` even though the title says "zero-shot": the voice-preservation
capability is inherited unmodified from a reused external component rather than a dedicated
contribution, and the title's "zero-shot" actually refers to zero-shot S2ST training without
parallel speech data, which the `speech-to-speech` tag and claims already capture.
`spoken-language-model` included since Qwen3 is adapted with a speech encoder to consume an
external source-speech signal, matching the DeSTA2/Qwen3-Omni precedent already in the corpus.

One QC note: the ingest agent flagged what it believed was a "race condition from concurrent
parallel ingest workers" causing inconsistent `wiki/index.md` counts (695 in two places, 689 in
the Browse link) and left the file as-is rather than reconciling it itself. Investigated and
found no evidence of any actual concurrent writer — this session has been running strictly
sequential one-paper-at-a-time ingests all day, and the pattern (partial, inconsistent count
updates) exactly matches the long-standing, already-diagnosed index-count-drift bug rather than a
new race condition. Corrected the usual way (fixed title truncation on the index row and all 3
`wiki/index.md` count occurrences against real `ls`/`grep` counts, 696=696 confirmed). Worth
watching whether this "race condition" misdiagnosis recurs from other agents, since attributing
the drift to a phantom concurrent process could lead a future agent to stop reconciling it
under the (incorrect) assumption that another process will.

Q4 progress: 131 ingested / 51 remaining (65 rejected, `2510.12116` still pending). Nothing
committed yet this session.

---

**Session 2026-07-29, session 18, item 3 of 5:** `2511.21045` (CartoonSing) ingested. Corpus
696 → 697 pages, 0 errors.

Genuine catch this item (manual verification, not agent self-report): the recurring
task/`related_concepts` mismatch bug (see [[feedback_task_related_concepts_mismatch]]) — the
page's `task` frontmatter correctly included `singing` alongside `TTS`/`VC`, but `related_concepts`
and Wiki Connections both omitted the `singing` concept tag entirely despite the paper formally
defining and evaluating both non-human singing voice synthesis and non-human singing voice
conversion as its two core contributions. Added `singing` to `related_concepts` and a
corresponding Wiki Connections bullet by hand. Tagging judgment calls otherwise verified genuine
on inspection: `zero-shot-tts` (unseen timbre embeddings, including non-human, without
per-timbre fine-tuning), `multilingual-tts` (own system trained/evaluated on Chinese and Japanese
singing data with per-language metrics), and `disentanglement` (explicit ablation evidence, §B.2,
that a more timbre-disentangled content representation generalizes better to non-human timbre
transfer) all held up. `task: [singing, TTS, VC]` confirmed reasonable given the paper formally
defines and separately evaluates both an SVS and an SVC task. In-corpus citation correctly
excluded TCSinger 2 (`2505.14910`) since that paper's own `status` is `rejected` in this corpus.

Q4 progress: 132 ingested / 50 remaining (65 rejected, `2510.12116` still pending). Nothing
committed yet this session.

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
