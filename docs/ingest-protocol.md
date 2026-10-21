# Ingest Protocol

The operating procedure for an ingestion session: what the main session does, what the ingest
agent does, what is verified by hand after every paper, and how a session starts and ends. It is
the canonical reminder of "how we ingest". Read it at the start of every ingest session.

This file orchestrates; it does not duplicate the specifications it points to:

| Concern | Authority |
|---|---|
| Page template, field rules, tagging rules, agent steps | `.agents/skills/speech-generation-ingest-agent/SKILL.md` (Tier 2: `...-lightweight-ingest-agent`) |
| Prose style, claim wording | [writing-style.md](writing-style.md) |
| Frontmatter schema, dates, duplicates and later versions | [schemas/metadata.md](schemas/metadata.md) |
| Controlled vocabulary | [schemas/vocabulary.md](schemas/vocabulary.md) |
| Generation provenance block | [schemas/generation.md](schemas/generation.md) |
| Stage overview and templates | [content.md](content.md) |
| Quarter-specific counts, queue, log | the active session doc (currently `Q2_INGESTION_SESSIONS.md`) |

**Maintenance.** Update this file whenever the procedure changes or a new recurring issue class
is confirmed (see [Recurring issue classes](#recurring-issue-classes)). It is tracked in git and is
part of the session wrap-up: if the session taught us something about the procedure, change it
here before committing. If a rule here conflicts with an unreviewed memory or chat, this file wins;
if it conflicts with a schema or SKILL.md, fix whichever is wrong in the same commit.

---

## 1. Session start

1. `git status` in the infra repo and in the content repo (`python3 scripts/resolve_wiki_dir.py`).
   Preserve unrelated uncommitted changes. If the resolver fails, stop and report.
2. Read `STATUS.md`, the active section of `BACKLOG.md`, and the active session doc's
   "Next Session: Resume Here" and Manual Verification Queue. If `STATUS.md` is stale, say so.
3. Re-derive the counts from files, not from chat or memory (script in the session doc's Progress
   section). Verify the page count with `grep -c '^| \[\[' papers/index.md` in the content repo.
4. If worktrees are in use, check the trunk checkout for unpushed commits from a sibling stream
   (`git log HEAD..origin/main`, `git status`) before any later merge.
5. Activate tooling: use `.venv/bin/python` directly (background shells do not keep `activate`).
6. Pre-select the candidate list (section 2) and confirm it with the user before launching anything.

## 2. Candidate selection

- Select by canonical `published_date` in `raw/metadata/{id}.json`, **never by arXiv ID prefix**.
  Mismatches in both directions are common.
- Only `status: accepted` with a parsed paper (`raw/parsed/{id}/`). Never ingest `pending`,
  `review` or `rejected` without explicit instruction.
- Skip dedup pointers (`wiki_page_id` set) and records marked `is_duplicate`.
- Conference-accepted arXiv papers (ICASSP, Speech Prosody, LREC) keep the arXiv date.
- Pre-flight each candidate before it enters the list:
  - **ID/title dedup.** Title-match against the whole corpus, then check authors and abstract
    (retitled versions slip past title matching).
  - **OpenReview records** that duplicate an existing arXiv record: arXiv stays canonical; the
    OpenReview record is flagged `is_duplicate` and `rejected`.
  - **Later versions** (proceedings or journal version of an already-ingested paper): the ingested
    version stays canonical; mark the new record a duplicate and add an italic note on the existing
    page. Never re-ingest or re-date. Rule: `schemas/metadata.md`, "Duplicates and Later Versions".
    Retitled versions with rewritten abstracts slip past title and abstract matching (VibeVoice ICLR
    2026 vs its tech report, abstract similarity 0.12): screen every candidate's author list against
    ingested records and compare the systems when most authors overlap. Exception: an ingested
    technical report and a later peer-reviewed paper on the same system get separate pages in their
    own quarters, cross-linked, neither a duplicate (VibeVoice precedent; `schemas/metadata.md`).
    Do not enrich an integrated page with a later version's results: integration selects by
    quarter, so the new evidence would never reach the claim YAMLs.
  - **Legacy dedup pointers** are not defects: a proceedings record with `status: ingested` and
    `wiki_page_id` set points to the arXiv page, and that arXiv record carries `is_duplicate` and
    `canonical_id` back to it (MaskGCT, MoonCast, LLaMA-Omni, VITA-1.5 and others). Cite and link
    the `wiki_page_id` target.
  - **Extended/full versions** under an unrelated ID: check `arxiv_comment` for "full version of",
    "extended version", "journal version", especially when the ID prefix disagrees with
    `published_date`. Surface to the user; do not decide alone.
  - **Scope doubt** (ASR/translation/diarization-only, non-speech audio, zero metrics): read the
    paper and apply the precedent chain in the session doc; surface the matching precedent
    explicitly instead of re-deciding from scratch.
  - **Accepted in human triage:** a record whose box is ticked `accept` in `raw/review_queue.md` is
    in scope by the user's decision even when its filter note calls it tangential. Tell the agent
    not to stop on scope; tagging and significance are still judged normally.
- Number the list. Show it to the user and wait for confirmation.

## 3. Cadence

Default, unless the user has most recently asked for something else (follow the latest request and
do not silently revert):

- **Tier 1 pages:** one paper at a time, never in parallel. Cleanup and QC after **each** paper
  (sections 4 to 6). One consolidated batch summary after every 4 papers, then wait for an explicit
  go-ahead.
- **Tier 2 stubs** (`ingest_tier` set; note the field is `ingest_tier`, not `tier`): groups of 4
  in parallel via the lightweight agent, go-ahead between groups, no per-paper quality pass.
- The user may drop to one-paper-with-go-ahead mid-session. Follow it.

Batch bookkeeping (recurring slip): before reporting a batch complete, count the actual agent
launches against the requested size, and compare the **actual IDs** to the numbered list's `#`
column, not just the count. Repeat the check as a sweep at session close.

## 4. Per paper: launch the agent

Spawn `speech-generation-ingest-agent` in the **foreground** (background agents cannot get
Write/Edit approved). The prompt is `Ingest paper {id}` plus these standing instructions:

- Write to the content worktree: set
  `SPEECH_WIKI_CONTENT_DIR=/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content-ingest`
  (the resolver otherwise returns the trunk content checkout). Never write through `wiki/`.
- Mitigation B: the agent writes **the paper page only**. Do not update `papers/index.md`,
  `wiki/index.md` counts, `log.md` or metadata; the main session does that (section 5). Paper-page
  assets (0 to 2 architecture figures, only for `architectural-novelty`) are the agent's.
- Quote every date field and the `id` as strings in YAML.
- Use piped `[[id|Name]]` paper links in Wiki Connections (the SKILL.md template still shows the
  bare form; the bare form is only for the ID column of `papers/index.md`).
- Match `references.json` citations to corpus pages by hand: its `in_corpus` flags are stale or
  null on most real matches.
- Do not write "internal inconsistencies" on the page unless verified against the source.
- Stop and flag, do not write, if the paper is scope-ambiguous.
- Emit `INGEST_RESULT` JSON including `review_flags` only when a precision-gate judgment call
  (claims, `field_significance`, concept scope, vocabulary gap) is genuinely uncertain.

Tell the user which paper is running. Do not start the next paper until section 5 and 6 are done.

## 5. Per paper: main-session cleanup (before the next paper)

All of these target the content worktree. `scripts/ingest/cleanup.py` does steps 1 to 4 in one
idempotent run, taking provenance from the page's `generation` block (it refuses a page without a
version-2 block, which covers step 5):

```bash
.venv/bin/python scripts/ingest/cleanup.py {id} --org "Org A / Org B" --wiki-dir "$WIKI"   # --dry-run to preview
```

What it does, and what to check in its output:

1. **Index row.** Add the row to `papers/index.md`:
   `| [[{id}]] | [{title[:55]}](papers/{id}.md) | {org} | {venue} | {year} | {tasks} | {architectures} | {date} |`
   - ID column is the bare `[[id]]`.
   - Title truncated to about 55 characters (deliberate), not the full title, not cut mid-word.
   - **Org filled by hand** (`organization` is null on nearly every 2026 record; take it from the
     page or PDF first page). Include every task tag. Exactly one row per ID.
2. **Counts.** Fix all three paper-count occurrences in `wiki/index.md` (abstract callout, "Browse
   the Papers" line, "Browse all N papers" link). The sole authority is
   `grep -c '^| \[\[' papers/index.md` (also `ls papers/*.md | grep -v index.md | wc -l`; they should
   match). Agents' counts and the bundled counter script drift in both directions.
3. **Log.** Append to `wiki/log.md` in the correct dated section (regex section insertion, never
   append-to-end-of-file):
   `- ingest | {id} | {title} | {venue} {year} | runtime: {runtime} | provider: {provider} | model: {model}`
4. **Metadata.** `raw/metadata/{id}.json`: `status: ingested`, `ingested_date`, and a
   `generation_history` entry. Pipeline-state fields only; never alter what a paper says.
5. Confirm the page's `generation` block is version 2 with runtime, provider, exact model ID,
   logical agent, date and infra commit.

## 6. Per paper: QC

Run the scoped health check plus the scripted checks below against the content worktree:

```bash
.venv/bin/python scripts/ingest/qc.py {id} --wiki-dir "$WIKI"
```

It prints the health check result, a frontmatter summary to read, and a list per check; an
empty list means nothing was found. It covers quoting, the concept count, callouts, em dashes,
"SCA" in prose, bare links, stray `[[`, citation integrity, adoption language, leaked instructions,
"inconsistency" claims and the index row and counts. Then verify the actual file yourself: the
judgment items below (tag scope, significance, numbers against the source) are not scriptable. Treat every statement in the agent's closing summary
("clean", "not tagged", "count updated") as a hypothesis, including its defence of a format as
intentional. Checks the health check does not (fully) cover:

**Structure and format**
- At most two callouts per page, the abstract card included (`writing-style.md`). A high or
  foundational paper's `[!tip]`/`[!important]` therefore leaves no room for a `[!warning]`; put the
  critical limitation first in Limitations as prose.
- Wiki Connections bullets follow the template exactly: `- [[id|Name]] — description`, with no
  extra parenthetical between the link and the separator.
- No `[[` outside real wikilinks, including inside math: Quartz parses it as a link. Write matrices
  with `\begin{bmatrix}` instead of nested brackets.
- Abstract callout is `[!abstract]`, never the same type as the Field Significance callout
  (`[!tip]` for high, `[!important]` for foundational). Only `[!abstract]`, `[!important]`,
  `[!tip]`, `[!warning]` appear in the body; no `[!note]`.
- No leaked instruction text (e.g. `**Grounding rule:**`) visible in prose.
- YAML: dates and `id` quoted; `task` in bracket-unquoted form (`task: [TTS, evaluation]`).
- Claims: bold role prefix (`**supports:**`, `complicates`, `contradicts`, `refines`) plus a
  `> *Evidence:*` blockquote with a section citation. Named sections need the `§` prefix
  (`*(§Limitations)*`).
- Wikilinks in prose are piped `[[id|Name]]`; fix every `wikilink_format` warning rather than
  suppressing it. No em dashes in page prose (template separators are fine: `- [[link|Name]] — description` in
  Wiki Connections bullets and the `{level} — ` opening of Field Significance). In prose write "spoken conversational
  agents" or "speech LMs", never "SCA" (frontmatter tag only). No "cited by N papers".
- Figures: Interspeech Docling output often picks up the ISCA logo as figure-1; look at the image
  before embedding.

**Citations**
- Every cited paper ID exists on `papers/index.md` (canonical IDs can differ from arXiv IDs, for
  example F5-TTS is `2025.acl-long.313`).
- `accepted`-but-unwritten: keep the ID in `related_papers`, de-link in prose. `rejected`: remove
  entirely (mention unlinked if needed).

**Content judgment**
- No unsupported adoption claims ("de facto", "dominant", "widely adopted", "has become") in Field
  Significance or Wiki Connections.
- `field_significance.type` is plausible (no `empirical-benchmark` on a system paper, no
  `architectural-novelty` on engineering integration).
- Every metric traces to a table or figure; missing values are `"not reported"`.

**Tagging**
- `related_concepts` includes the concept slug for every `task` tag (`singing`, `VC`, `codec`,
  and so on) **and** every architecture-derived tag, in both directions. A
  `related_concepts_complete` warning is a fix-now item; it does not cover architecture tags.
- `related_concepts`: at most 6 slugs (hard cap, user 2026-10-20); 3-6 is the target, but scope
  wins over the minimum (user, 2026-10-21): never pad with an out-of-scope slug, and 1-2 slugs are
  fine when that is all that qualifies (common for benchmarks and narrow system papers). When more
  than 6 qualify, drop slugs that describe frozen or inherited components first (an architecture
  tag can stay in `architecture` without its slug), and keep evidence concepts such as
  `subjective-evaluation`.
- Concept-tag scope: a tag is legitimate only if the paper's own method performs or is evaluated
  on the concept, not merely discusses, contrasts or defers to it. Check the concept's scope note
  and the paper's Limitations section.
- Rules to apply specifically:
  - `VC` task: dedicated VC system plus VC-specific metrics; zero metrics fails the bar. An
    off-the-shelf VC system qualifies when the converted speech itself is the object of measurement
    (acoustic before/after analysis, listeners judging converted audio), not when VC is only a
    preprocessing step (user, 2026-10-21, `2026.dialres-1.18`).
  - Evaluation papers that only score existing systems do not earn those systems' concepts
    (TTS-PRISM, SpeakerSleuth, EchoMind `emotion-synthesis`), except `spoken-language-model` for
    benchmarks of speech LMs. A paper that evaluates how to measure a concept does earn it (The False
    Resonance `2604.26347`, `emotion-synthesis`; user, 2026-10-21).
  - `spoken-language-model`: an external speech signal consumed by an adapted LLM; benchmarks that
    feed real audio into existing speech LMs and measure them also qualify. AR TTS-LMs consuming
    their own output do not.
  - `speech-to-speech`: must fit a sub-paradigm (dialogue, S2S translation, cascade); codec-level
    audio transforms do not qualify.
  - `multilingual-tts`: the paper's own system trained or adapted across languages.
  - `subjective-evaluation`: real human raters; LLM-judge or automated scoring never qualifies.
  - `disentanglement`: explicit training mechanism with ablation evidence.
  - `self-supervised-speech`: only when the method itself uses HuBERT/WavLM/wav2vec2/w2v-BERT,
    never for Whisper.
  - `autoregressive-codec-tts`: neural-codec-token autoregression, not mel-frame AR models.
- Surveys: `## Scope and Coverage` section and `tags: ["survey"]`.
- No text input (lip-to-speech, brain decoding): use `task: [TTS]` as the standing fallback and
  flag it in the verification queue; do not invent a term. Text-driven TTS with non-text
  conditioning is plain TTS.

Fix defects directly (or re-run the agent only when the page needs a rewrite), then re-run the
health check. Add any `review_flags` to the Manual Verification Queue; do not block the next paper
on resolving them.

## 7. Batch summary (after every 4 papers)

Post one summary, and append it to the active session doc's Session Log:

- Paper IDs, with the actual IDs checked against the numbered list.
- QC catches and fixes per paper, and any new recurring issue.
- Corpus page count and updated quarter progress numbers (from the script, not the agent).
- New `review_flags` added to the Manual Verification Queue.

Then wait for the user's go-ahead.

## 8. Interruptions

If an agent is cut off (session limit, API 5xx), inspect the **standalone content worktree**
(never `wiki/`, which can be stale) before retrying. Nothing written: retry directly. Partial
writes (page without index/log/metadata, stray figure assets): complete or reuse by hand, and
check coverage, not just structure. After a retry, also confirm `INGEST_RESULT` was emitted;
agents sometimes omit it.

## 9. Session close

Wrap-up is a single sequence (the user may call it "wrap it up", "close out", and similar):

1. **Session doc.** Append per-batch Session Log entries; rewrite "Next Session: Resume Here"
   (progress counts, last-ingested ID, next candidates, new recurring issues, current cadence);
   update the Manual Verification Queue.
2. **`STATUS.md`.** Refresh "Last updated", the corpus-state table, the quarterly progress table
   and current priorities.
3. **This protocol.** If the session changed the procedure or confirmed a new issue class, update
   this file.
4. **Commit, push, merge, sync every repo touched**, in the order content, then infra (with the
   `wiki` submodule pointer bumped to the new content commit), then site:
   - Edit and commit from the standalone content repo, never via `wiki/` or `site/content/`
     (detached HEAD orphans the work).
   - Before merging `work/ingest` into `main`, check trunk for unpushed commits from a sibling
     stream. Expect a mechanical same-day `log.md` conflict; keep both blocks.
   - After the push, fast-forward the `work/ingest` branch back to `main` in both repos.
   - If the trunk checkout is not on `main`, use a throwaway `git worktree add /tmp/x main` for the
     submodule bump and run `git submodule update --init wiki` there first.
   - `git add -A` can stage symlinked gitignored directories; check `git status` first.
   - Commit messages describe what changed, not when; no session-number prefix.
5. **Site bump.** Ask once per session before bumping the site submodule (it triggers a live
   deploy), unless a durable instruction already covers it.
6. **Memory.** Refresh auto-memory last (corpus status, any genuinely new finding). Memory is a
   convenience copy, never the source of truth; promote durable findings here or to a schema first.

---

## Recurring issue classes

Confirmed repeat offenders; keep this list current (add the date a class was last observed):

| Class | Symptom | Where it is caught |
|---|---|---|
| Index count drift | Three `wiki/index.md` counts stale or mutually inconsistent | Step 5.2 |
| Blank Org / dropped task tag | Row incomplete despite valid frontmatter | Step 5.1 |
| Full title in index row | Agent writes the untruncated title | Step 5.1 |
| Bare wikilinks | `[[id]]` in prose; agent defends it as template-mandated | Step 6 |
| Wrong abstract callout | Abstract uses the Field Significance callout type | Step 6 |
| Task/architecture tag missing from `related_concepts` | Health check silent for architecture | Step 6 |
| Concept-tag scope mistag | Tag because the paper discusses it, not performs it | Step 6 |
| Unquoted date or numeric-looking ID | Parsed as date object or float | Step 4 prompt, step 6 |
| False "inconsistency" on page | Agent misreads per-group vs total or different conditions | Step 6 |
| Agent self-report contradicts file | Narrated decision differs from the written frontmatter | Whole of step 6 |
| Batch undercount or list drift | 3 agents launched for a batch of 4, or wrong `#` range | Section 3 |
| Cleanup deferred to batch end | Slipped on 2026-10-18; led to unquoted dates and a skipped log | Section 5 |
| Padding `related_concepts` | Out-of-scope slug added to reach 3 (2026-10-21, before the scope-wins rule) | Step 6 |
| Org mismatch page vs index | `cleanup.py --org` does not sync the page; strings drift (2026-10-21, three of four papers) | Step 5.1 |
| One-sided critique of author framing | Agent cites only the comparisons that go against the authors (2026-10-21) | Step 6; ask for the full comparison in the prompt |
| Docling table numbering | `assets/table-N` does not follow the paper's numbering; labels swapped or garbled | Step 6; check the table PNG |

## Known discrepancies to resolve

- `ingest-agent/SKILL.md` and `content.md` still describe the agent updating `papers/index.md`,
  `wiki/index.md`, `log.md` and metadata itself. Under Mitigation B (current practice) the main
  session does this. Either narrow the SKILL.md for the default case or keep stating the override
  in every agent prompt (section 4).
- Older session docs (`docs/records/`) and the Q3/Q4 integration docs may still carry their own
  copy of ingest methodology; this file is canonical.
