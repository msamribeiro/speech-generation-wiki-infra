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

_(none yet — bootstrapped 2026-07-17)_

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
