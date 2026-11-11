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
| Quarter-specific counts, queue, log | the active session doc (currently `Q3_2026_INGESTION_SESSIONS.md`) |

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
- Apply the peer-reviewed-version rule before selecting the queue. A verified proceedings or
  journal version fully re-dates a paper that is absent from all top-level claim YAMLs. If the
  canonical ID already occurs in a claim YAML, preserve `published_date`, year, and month while
  recording the peer-reviewed venue/date/link and page note. Claim membership, not ingest status,
  is the freeze authority. Never infer acceptance from “submitted to” prose.
- **Proceedings check at pre-flight.** When a candidate's `arxiv_comment` says "accepted to"
  a venue, verify the authoritative proceedings landing page, identity, and venue date. Match
  titles and authors because camera-ready titles can change. An acceptance comment is a discovery
  signal, not sufficient evidence for mutation. Once verified, apply the rule above before the
  paper enters a quarterly queue. A missing proceedings record is not evidence of absence: the
  ISCA fetch keeps only titles that pass the keyword filter, so match against the full proceedings
  index (`isca.scrape_index`), not against fetched records (6 Interspeech 2026 papers, 2026-11-11).
- **Ingest the peer-reviewed version when it is known** (`schemas/metadata.md`, "Source Version at
  Ingest"; user decision 2026-11-11). Decided per paper at ingest time, not in a separate batch:
  for an arXiv-canonical candidate with a verified proceedings or journal version, run
  `scripts/ingest/use_peer_reviewed.py` (dry run, then `--apply`), re-parse with
  `batch_convert.py --ids {id}`, and tell the agent the preprint parse in
  `raw/parsed/{id}/preprint/` is context only. When the peer-reviewed PDF cannot be retrieved
  (OpenReview gate, unpublished proceedings), ingest the preprint. For a proceedings-canonical
  candidate with a known arXiv twin, set `url_preprint`. Pages already written from a preprint get
  the link and note only; never re-ingest them without the user.
- Pre-flight each candidate before it enters the list:
  - **ID/title dedup.** Title-match against the whole corpus, then check authors and abstract
    (retitled versions slip past title matching).
  - **OpenReview records** that duplicate an existing arXiv record: arXiv stays canonical; the
    OpenReview record is flagged `is_duplicate` and `rejected`.
  - **Later versions** (proceedings or journal version of an already-ingested paper): the ingested
    record stays canonical; mark the new record a duplicate and add the peer-reviewed link and
    italic note to the existing page. Re-date only when the canonical ID is absent from every
    top-level claim YAML. Rule: `schemas/metadata.md`, "Duplicates and Later Versions".
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
  - **Prior publication notices** in the PDF itself: skim the first page of `raw/parsed/{id}/paper.md`
    for "preprint of", "published in" or "final authenticated version" notices, which
    `arxiv_comment` often omits. If the paper already appeared in proceedings or a journal, look up
    the date (Crossref via the DOI), set `conference_date` or `journal_date` and re-apply the date
    rule; the paper may leave the quarter (PACC `2605.18001`, ICICC 2025, 2026-10-23).
    Re-date with `lib/paper_dates.apply_date_rule` (never by hand) and log a `review | re-dated`
    line in `raw/pipeline_log.md`; metadata `venue` stays as fetched.
  - **Journal Early Access dates.** `journal_date` is the first online date. For IEEE journals
    Crossref often carries only the print issue (no `published-online`); its record `created`
    date usually matches Early Access but is not proof. IEEE Xplore blocks scripted requests, so
    ask the user to read the article page's "Date of Publication" (TBME `2606.01905`: print
    2026-08, Early Access 2026-05-19, stayed in Q2; user, 2026-10-25). On the page use
    `venue_type: journal` and the card label `Journal`.
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

- Run from the infra ingest worktree: agents start in the session's own working directory, which
  may be a worktree without `raw/` data or `.venv`. Name
  `/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-infra-ingest` as
  the directory for all `raw/` paths and the infra commit in the `generation` block, and
  fast-forward the session worktree to `main` first so the preloaded skill is current (2026-11-11).
- For a record switched to its peer-reviewed version (section 2), spell out the source-version
  block: primary `paper.md`, `preprint/` as context only, `url` and `url_preprint` from metadata,
  no `url_peer_reviewed` and no italic note.
- Write to the content worktree: set
  `SPEECH_WIKI_CONTENT_DIR=/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content-ingest`
  (the resolver otherwise returns the trunk content checkout). Never write through `wiki/`.
- Mitigation B: the agent writes **the paper page only**. Do not update `papers/index.md`,
  `wiki/index.md` counts, `log.md` or metadata; the main session does that (section 5). Paper-page
  assets (0 to 2 architecture figures, only for `architectural-novelty`) are the agent's.
- Quote every date field and the `id` as strings in YAML. Write list fields (`task`,
  `architecture`, `conditioning`, `training`, `field_significance.type`) bracket-unquoted.
- Use piped `[[id|Name]]` paper links in Wiki Connections (the SKILL.md template still shows the
  bare form; the bare form is only for the ID column of `papers/index.md`).
- Match `references.json` citations to corpus pages by hand: its `in_corpus` flags are stale or
  null on most real matches.
- Do not write "internal inconsistencies" on the page unless verified against the source.
- When defining a derived metric (a gap, delta or relative score), check its sign convention
  against the table.
- List every superlative written on the page ("best", "largest", "outperforms") in the closing
  summary, with the table cells that support it across all rows (a tie is not "best").
- Set `organization` from the first-page affiliations, institutions joined with " / ", and quote it.
- Link systems the paper evaluates as baselines when they have pages, even if the reference list
  omits them (OmniVoice on PashtoTTS-Bench; WavTokenizer and SpeechTokenizer on the WER Trap).
- Card label and `venue_type` follow metadata and convention: arXiv preprints and technical
  reports are `Preprint`; a workshop page names the workshop with its year (`SIGUL 2026`,
  `NLPAICS 2026`) when metadata holds the placeholder `workshop`.
- Spell out the callout limit in the prompt: two at most, the abstract card included; only
  `[!abstract]`, `[!tip]`, `[!important]`, `[!warning]`, never `[!note]`.
- Stop and flag, do not write, if the paper is scope-ambiguous. Agents sometimes write the page
  anyway and cite a precedent (`2606.14004`, 2026-10-31); treat that as a flag and confirm with the
  user in the batch summary.
- When Docling garbles a table (split or lost row labels, merged rows, swapped table numbers), read
  the PDF text with `pypdfium2` from `.venv` (`raw/papers/{id}.pdf`) and resolve it; never leave a
  "check against the PDF" note on the page.
- Never link a corpus page on a guess that a product or API is that model (CN-NewsTTS: the
  `mimo-v2.5-tts` API is not evidence of MiMo-Audio `2512.23808`).
- Agent runtimes vary widely: most take 2-7 minutes, some 45 minutes to 3 hours (2026-10-31).
  Wait for the foreground agent; do not relaunch.
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
   - Title hard-cut at 55 characters (`title[:55]`, deliberate; mid-word cuts are expected), never
     the full title.
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
- Single-author or single-language automated benchmarks without human evaluation sit at `low`
  even when their cautions are useful (PSP `2604.25476`; PashtoTTS-Bench `2605.26978` and NLPAICS
  `2026.nlpaics-1.18`, user 2026-10-25). Larger benchmarks with uptake potential stay `moderate`.
  The same applies to system papers whose evaluation is single-language and automatic-only,
  even with released weights (Sarashina2.2-TTS `2606.25369`, user 2026-10-31).
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
  `subjective-evaluation`. Below the cap, a frozen component keeps its slug only when it is on the
  TTS side and central to the evaluated output (a frozen acoustic model or AR backbone that a TTS
  paper adapts or steers), and the page says it is frozen (user, 2026-10-22, Tibetan-TTS
  `2605.02496`; SAE emotion control `2606.01479`). An inherited decoder inside a speech LM or
  dialogue system that the paper never touches does not earn its slug (user, 2026-10-25,
  Sympatheia `2606.00851`: GLM-4-Voice's flow-matching decoder, no `flow-matching`); it can stay
  in `architecture`.
- VITS is tagged `architecture: [VAE, GAN]` with `gan-vocoder` in `related_concepts` when the
  paper trains or fine-tunes it (user, 2026-10-22; older VITS pages are not backfilled).
  Normalizing-flow acoustic models such as Glow-TTS have no architecture term; leave them untagged.
- `gan-vocoder` (user, 2026-10-24): tag it when the paper trains a standalone GAN vocoder (WaveNeXt 2
  `2605.25506`; FMelCodec `2605.25669` retraining HiFi-GAN; CosyEdit2 `2605.25930` training
  BigVGAN), or when a codec/VAE decoder's adversarial training is part of the paper's own
  contribution or is ablated (Target-KL `2605.17085`, CQT discriminator ablated). A codec or VAE
  whose GAN losses are inherited unchanged from a standard recipe (DAC, Stable Audio, Vocos) lists
  `GAN` in `architecture` without the slug (PoDAR, ClariCodec, AffectCodec). Existing codec pages
  (EnCodec, BigCodec and others carry it) are not backfilled.
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
    Resonance `2604.26347`, `emotion-synthesis`; user, 2026-10-21), but only when it actually
    measures that concept's system output: a protocol calibrated on human speech alone does not
    (`2606.31055`, `speech-to-speech` dropped; user, 2026-10-31). A concept also needs evaluated
    evidence: an unevaluated control (ZONOS2 `2606.24320` rate tokens, no `prosody-control`) or a
    benchmark that reuses existing scorers without validating them (no `evaluation-metrics`) does
    not earn the slug (user, 2026-10-31).
  - `spoken-language-model`: an external speech signal consumed by an adapted LLM; benchmarks that
    feed real audio into existing speech LMs and measure them also qualify. AR TTS-LMs consuming
    their own output do not.
  - `speech-to-speech`: must fit a sub-paradigm (dialogue, S2S translation, cascade); codec-level
    audio transforms do not qualify.
  - `multilingual-tts`: the paper's own system trained or adapted across languages, **and** its
    evaluated output spans more than one language (bilingual or pooled training evaluated on each
    language, or code-switched synthesis). Adapting a model pretrained on other languages to a
    single new language does not qualify when each resulting voice is monolingual (user,
    2026-10-22: Central Kurdish `2026.lrec-1.48`, Tibetan `2605.02496`, Creole `2026.sigul-1.11`
    dropped; PS-TTS, JaiTTS and the Quechua/Spanish page kept). One LoRA adapter trained on pooled
    languages and evaluated on each qualifies (`2606.26618`); an inference-only method on a
    pretrained bilingual model does not, since it trains nothing across languages (`2606.25672`).
  - `subjective-evaluation`: real human raters; LLM-judge or automated scoring never qualifies.
    Humans rating actual system output count even when the study exists to validate an automatic
    judge (STEB `2606.25529`); humans checking benchmark labels do not (`2605.27772`; user,
    2026-10-31).
  - `disentanglement`: explicit training mechanism with ablation evidence.
  - `self-supervised-speech`: only when the method itself uses a self-supervised speech model
    (HuBERT, WavLM, wav2vec2, w2v-BERT, data2vec-based models such as emotion2vec; user,
    2026-10-24, AffectCodec `2605.23373`), never Whisper (supervised) and never when SSL appears
    only in an evaluation metric (WavLM speaker similarity). An SSL model applied only to the
    visual stream (AV-HuBERT as a lip encoder) does not count (HoliDubber `2606.09098`; user,
    2026-10-31).
  - `zero-shot-tts`: the paper's own system is evaluated on prompt-based cloning of speakers unseen
    in training. Omit it when the evaluated voices are in the training or fine-tuning data, even if
    the paper says "zero-shot" (user, 2026-10-24: Poly-SVC `2605.12310`, F5-TTS-DPS `2605.23859`),
    and when unseen status cannot be established (base model's training data unknown, targets
    from a common public corpus such as ESD; `2606.05367`, user 2026-10-31).
  - `autoregressive-codec-tts`: neural-codec-token autoregression, not mel-frame AR models.
  - A diffusion transformer trained with a flow-matching objective (VoxCPM2 LocDiT) takes
    `flow-matching`, not also `diffusion-tts` (HoliDubber, `2606.26618`; user, 2026-10-31).
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
| Disallowed `[!note]` / third callout | Agent adds a `[!note]` caveat callout beside abstract and warning (2026-10-25, `2605.25504`) | Step 4 prompt (spell out the limit), `qc.py` callouts check |
| Evaluated baselines left unlinked | Systems scored in the paper's tables but absent from its reference list are linked on some pages, not others (2026-10-25, 2 of 4 in one batch) | Step 4 prompt, step 6 |
| Non-canonical `venue_type` / card label | Agent writes `technical-report` / "Technical Report" against metadata `preprint` (2026-10-25) | Step 4 prompt, step 6 |
| Task/architecture tag missing from `related_concepts` | Health check silent for architecture (2026-10-22, 2 of 4 pages; cured by an explicit per-tag coverage line in the prompt) | Step 6 |
| Concept-tag scope mistag | Tag because the paper discusses it, not performs it | Step 6 |
| Unquoted date or numeric-looking ID | Parsed as date object or float | Step 4 prompt, step 6 |
| False "inconsistency" on page | Agent misreads per-group vs total or different conditions | Step 6 |
| Agent self-report contradicts file | Narrated decision differs from the written frontmatter; or the summary names an error on the page without fixing it (2026-10-25, UNISON KL ordering) | Whole of step 6; act on every defect the summary mentions |
| Batch undercount or list drift | 3 agents launched for a batch of 4, or wrong `#` range | Section 3 |
| Cleanup deferred to batch end | Slipped on 2026-10-18; led to unquoted dates and a skipped log | Section 5 |
| Padding `related_concepts` | Out-of-scope slug added to reach 3 (2026-10-21, before the scope-wins rule) | Step 6 |
| Org mismatch page vs index | `cleanup.py --org` does not sync the page; strings drift (2026-10-21, three of four papers) | Step 5.1 |
| One-sided critique of author framing | Agent cites only the comparisons that go against the authors (2026-10-21) | Step 6; ask for the full comparison in the prompt |
| Docling table numbering | `assets/table-N` does not follow the paper's numbering; labels swapped or garbled; row labels split or lost; values shifted one column or packed several per cell (2026-11-11, three of eight papers) | Step 4 prompt (resolve via `pypdfium2` on the PDF), step 6 |
| Separator swapped to avoid em dashes | Agent writes `- [[id|Name]]: ...` in Wiki Connections (2026-10-22) | Step 4 prompt (spell out the template), step 6 |
| Unquoted numeric `related_papers` | `[2010.05646, ...]` parses as floats (2026-10-22) | Step 4 prompt, `qc.py` unquoted check |
| Dated log section appended at end of `raw/pipeline_log.md` | File is newest-first; 2026-10-23 section landed at the bottom (moved 2026-10-24) | Section 9 |
| Derived-metric sign reversed | Page defines a gap as "speech minus text" while the table is text minus speech (2026-10-23) | Step 4 prompt, step 6 (check against the table) |
| Stale "proceedings not yet published" note | Session doc said Interspeech 2026 was not on ISCA a month after it was; 51 Q2 records were in fact Q3 (2026-10-26) | Section 2, proceedings check |
| Standing prompt drops a protocol exception | Hand-written per-paper prompt omitted the `spoken-language-model` benchmark exception, so the agent excluded it (2026-10-26, COMPASS) | Step 4: copy tagging rules from section 6, not from memory; step 6 |
| Page written despite scope stop | Agent ingests a no-generation paper citing a precedent instead of flagging (2026-10-31, `2606.14004`) | Step 4 prompt, step 6 |
| "Check the PDF" note on page | Agent leaves a reader-facing note about a garbled parse instead of resolving it (2026-10-31, STEB) | Step 4 prompt, step 6 |
| Speculative product-to-model link | A commercial API linked to a research page of the same brand (2026-10-31, MiMo) | Step 4 prompt, step 6 |
| Quoted list fields | Agent writes `task: ["TTS"]` and quoted `architecture`/`type` lists; health check and `qc.py` silent (2026-11-11, `2606.07240`) | Step 4 prompt, step 6 (read the frontmatter) |
| Camera-ready prose quotes preprint numbers | Proceedings table updated but the results prose still quotes the preprint's numbers (2026-11-11, `2604.26136`: fine-tuning results changed sign for French) | Section 2 source version; step 6 (check prose numbers against the primary table) |
| Over-broad "best" claims | "Best MCD" true only among a subset of rows; stronger rows elsewhere in the same table (2026-10-23; three more on 2026-10-24, incl. "best" on a tie) | Step 4 prompt: agents list every superlative with its supporting cells; step 6, read the whole table |

## Known discrepancies to resolve

- `ingest-agent/SKILL.md` and `content.md` still describe the agent updating `papers/index.md`,
  `wiki/index.md`, `log.md` and metadata itself. Under Mitigation B (current practice) the main
  session does this. Either narrow the SKILL.md for the default case or keep stating the override
  in every agent prompt (section 4).
- Older session docs (`docs/records/`) and the Q3/Q4 integration docs may still carry their own
  copy of ingest methodology; this file is canonical.
