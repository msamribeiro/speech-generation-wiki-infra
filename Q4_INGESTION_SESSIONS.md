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
| Already ingested (Q4 2025) | 27 |
| Remaining to ingest | 159 |
| Rejected | 61 |
| **Total Q4 2025 in corpus** | **247** |

Counts computed from `raw/metadata/*.json` where `year == 2025` and `month in (10, 11, 12)`
(these fields are derived from `published_date`, not the arXiv ID prefix — see the ID-prefix
note below). Re-run before starting a session, as fetch/filter may still be adding papers.

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
  `[[id|Display Name]]`, don't just suppress the warning.

Also check the INGEST_RESULT signal for `review_flags`; if present, add the paper to the
**Manual Verification Queue** below and resolve by hand after the batch — don't block the next
paper on it. Note: agents sometimes omit the `INGEST_RESULT` signal entirely, especially on a
retry after an interruption — this is not itself an error, just verify the files directly.

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
verify and reuse or discard what's there rather than assuming either way.

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

---

## Manual Verification Queue

Papers where the ingest agent emitted `review_flags` in its INGEST_RESULT signal. Review these
after the session batch is complete — check the paper page and resolve each flag by hand.

| Paper ID | Flag | Agent note |
|----------|------|------------|

---

## Progress

Track by running:

```bash
.venv/bin/python3 -c "
import json, glob
accepted, ingested = 0, 0
for path in glob.glob('raw/metadata/*.json'):
    m = json.load(open(path))
    y, mo = str(m.get('year','')), str(m.get('month','0')).zfill(2)
    if y == '2025' and mo in ('10','11','12'):
        if m['status'] == 'accepted': accepted += 1
        if m['status'] == 'ingested': ingested += 1
print(f'Ingested: {ingested} | Remaining: {accepted}')
"
```

## Commit / Push Workflow

Not every batch needs a commit — batch within a session freely, commit at natural stopping
points or when explicitly asked. When committing:

1. Content repo: stage new paper pages + assets + `index.md`/`log.md`/`papers/index.md`, commit, push.
2. Infra repo: stage `raw/metadata/*.json` status updates + this session log, commit; then bump
   the `wiki/` submodule pointer to the new content commit (checkout `main` in `wiki/`, `git pull`,
   commit the pointer bump in infra), push.
3. Site repo: bump the `content` submodule pointer, commit, push — **ask before this step**, it
   triggers a live deploy. Push order is always content → infra → site, since site's submodule
   reference only resolves once content is on GitHub.
