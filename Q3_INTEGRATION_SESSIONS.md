# Q3 2025 (and Earlier) Integration Session

**Date:** 2026-07-18
**Goal:** Integrate every ingested paper published before Q4 2025 (`published_date < 2025-10-01`)
into `wiki/_claims/{slug}.yaml`, across all 23 canonical concepts. This is the **integrate**
stage of the three-stage content pipeline (ingest → integrate → render) — distinct from, and a
separate task from, the Q4 2025 ingest work tracked in `Q4_INGESTION_SESSIONS.md`.

This is a large, multi-session undertaking (see Scope below) — expect this note to accumulate a
long session log, the same way `Q4_INGESTION_SESSIONS.md` and the archived Q3 ingest log did.

---

## Scope

**Cutoff:** `published_date < 2025-10-01` — i.e. all of Q3 2025 and every earlier quarter. Q4
2025 papers are intentionally excluded from this task; they're still being ingested (see
`Q4_INGESTION_SESSIONS.md`) and will get their own integration pass later, after that ingest
work completes. Don't fold Q4 papers into an integration batch just because they happen to be
ingested already — keep the two efforts separate so progress in each is easy to reason about.

**Check current status with the two purpose-built tools** (don't hand-roll a script — these
already exist and are the source of truth):

```bash
cd "$(git rev-parse --show-toplevel)"

# Corpus-wide integration coverage per concept (papers referencing each concept vs. papers
# actually integrated into that concept's YAML)
.venv/bin/python scripts/corpus_summary.py --group-before 2025-07

# Structural validation + the single most useful backlog stat: papers_not_in_any_yaml
# (ingested, non-Tier-2 papers with zero concept-YAML entries anywhere)
.venv/bin/python scripts/health_check.py --module integrate --wiki-dir "$(python3 scripts/resolve_wiki_dir.py)" -v
```

**State as of 2026-07-21, after evaluation-metrics batch 14 (Phase 1 closed)** (re-run the commands above before
resuming — this will be stale). This
table is now **Q3-scoped directly** (`published_date < 2025-10-01`, non-Tier-2, counted from paper
frontmatter, not the corpus-wide `corpus_summary.py` output) — see the note below on why the
corpus-wide `Covers`-style column was dropped:

| Concept | Q3-scoped papers referencing it | Integrated | % |
|---|---|---|---|
| **evaluation-metrics** | **286** | **285** | **100%** (Phase 1+2) |
| zero-shot-tts | 204 | 0 | 0% |
| neural-codec | 184 | 0 | 0% |
| subjective-evaluation | 180 | 0 | 0% |
| autoregressive-codec-tts | 166 | 0 | 0% |
| self-supervised-speech | 146 | 0 | 0% |
| spoken-language-model | 127 | 0 | 0% |
| disentanglement | 100 | 0 | 0% |
| **flow-matching** | **97** | **97** | **100%** |
| prosody-control | 94 | 0 | 0% |
| voice-conversion | 87 | 0 | 0% |
| speaker-adaptation | 79 | 0 | 0% |
| multilingual-tts | 76 | 0 | 0% |
| emotion-synthesis | 74 | 0 | 0% |
| **speech-to-speech** | **63** | **60** | **95%** |
| gan-vocoder | 60 | 0 | 0% |
| streaming-tts | 54 | 0 | 0% |
| diffusion-tts | 46 | 0 | 0% |
| instruction-conditioned-tts | 45 | 0 | 0% |
| **rlhf-speech** | **29** | **29** | **100%** (Phase 1+2) |
| transformer-enc-dec-tts | 28 | 0 | 0% |
| singing | 10 | 0 | 0% |
| fine-tuning | 1 | 0 | 0% |
| **TOTAL** | **2236** | **471** | **21.1%** |

`papers_not_in_any_yaml` (corpus-wide, all quarters, via `health_check.py`): **205** as of
2026-07-21 after batch 14 (down from 221 after batch 13, 236 after batch 12, 248 after batch 11,
261 after batch 10, 278 after batch 9, 295 after batch 8, 312 after batch 7, 325 after batch 6,
339 after batch 5, 351 after batch 4, 366 after batches 1-3, 411 earlier, 429 before rlhf-speech
Phase 1, 548 on 2026-07-19).

**Important correction found and fixed 2026-07-20**: the Q3-scoping arithmetic above (and the
2026-07-19 table it replaces) was originally computed by a one-off script that checked a
frontmatter field named `tier` — but the actual field is `ingest_tier`. This silently failed to
exclude any Tier 2 stub pages (65 exist corpus-wide), inflating every concept's "papers
referencing it" denominator. A second bug in the same class: `related_concepts` is serialized
three different ways across paper pages (bracket-unquoted, bracket-quoted, YAML block-list — see
`BACKLOG.md`'s new "Standardize `related_concepts` frontmatter serialization" item), and an
early version of the script only handled one form, silently undercounting further. Both bugs are
now fixed in the ad-hoc scripts used to produce the table above; the two integration agent
invocations that actually wrote `_claims/*.yaml` this session were unaffected (they independently
re-verify `ingest_tier` and `related_concepts` per paper before writing, and in practice caught
4 Tier-2 papers and 3 sub-paradigm-fit exclusions that a naive candidate list would have missed).
**Takeaway for future sessions**: never hand-roll a `related_concepts`/`ingest_tier` scan without
handling both quoting styles and the correct field name — `scripts/corpus_summary.py` and
`scripts/checks/integrate.py` already do this correctly via real YAML frontmatter parsing, so
prefer extending those over writing a new one-off script.

**`flow-matching`, `speech-to-speech`, `rlhf-speech`, and now `evaluation-metrics` are fully
closed for Q3-and-earlier Phase 1 + Phase 2** (97/97, 60/63, 29/29, and 285/286 respectively —
the 3-paper gap on speech-to-speech is intentional: `2025.acl-long.388` DiVA,
`interspeech-2025-2660` VAP, and `2509.23938` Easy Turn were each evaluated and correctly excluded
for having no speech-generation stage of their own, despite carrying the tag; note `2509.23938`
is *not* a contradiction — it's separately and correctly integrated into `evaluation-metrics`,
since exclusion from one concept doesn't imply exclusion from another; evaluation-metrics' one gap
is the permanent `2207.12598` exclusion). `evaluation-metrics` is the largest concept closed so
far by paper count (285 vs. 97/60/29) and its Phase 2 pass required a mid-run course correction
(see Session Log) — the first attempt only covered 59/285 papers (21%) before a session-limit
interruption, and was resumed and reworked around evaluation-methodology *type* rather than TTS
architecture to reach 271/285 (95%) coverage with 14 legitimate outliers. All other 19 concepts
have **no `wiki/_claims/{slug}.yaml` file at all yet**.

**Scale note:** at the Phase 1 cap of 20 new papers per concept per invocation (see Methodology),
fully clearing the Q3-and-before backlog is roughly 463 ÷ 20 ≈ **23+ Phase 1 invocations**, plus
one or more Phase 2 synthesis passes per concept, plus health checks. This will span many
sessions — pace it like the Q4 ingest work (batch, verify, log, repeat), not as a single sitting.

---

## Known process gaps to resolve before/during this task

1. **Two non-registry concept tags found in the corpus**, both outside the 23-slug registry in
   `docs/content.md`:
   - `distillation` — tagged on `2406.05551.md`, `2506.13053.md`
   - `foundation-lm` — tagged on `2001.08361.md`, `2312.10997.md`

   The integration agent's own instructions say: "When the integration agent encounters a
   `related_concepts` slug not in this registry, it flags it to the user rather than creating an
   unsanctioned stub" (`docs/content.md`). Decide before running a broad pass whether these are
   typos that should map to an existing registry slug (e.g. `distillation` → `fine-tuning`?) or
   genuinely need new registry concepts added — don't let the agent silently skip these 4 papers
   for whichever concept they're miscategorized under.

2. **`BACKLOG.md`'s "Content Stage Implementation" section has a stale item**: "Repair
   flow-matching.yaml (malformed YAML: paper entries appear after trend_notes instead of under
   papers)". Verified 2026-07-18 — this is **not** the current state; the file's top-level key
   order is correct (`concept` → `last_updated` → `paper_count` → `papers` → `claim_clusters` →
   `method_families` → `reassessment_queue` → `open_questions` → `trend_notes`). Mark that
   BACKLOG line done/removed rather than re-investigating it.

3. **`2207.12598` (Classifier-Free Diffusion Guidance) is a permanent, never-integrated candidate
   for `evaluation-metrics`** — a Q3 2022 ImageNet diffusion paper tagged `evaluation-metrics`
   only as unrelated CFG background citation, correctly excluded on every re-encounter (batches
   1-5) since it's never written to the YAML. Because it's the oldest paper in the entire
   candidate pool by years, an oldest-first discovery scan will keep resurfacing it as "next"
   forever. Batch 5's agent got this backwards (see 2026-07-20 log entry) and reported it as no
   longer relevant — it always is, until either the paper is re-tagged to drop `evaluation-metrics`
   from `related_concepts` (an ingest-side fix, out of scope for integration) or every session
   explicitly re-confirms and re-excludes it as the standing first candidate. Expect to see this
   again in batch 6+; don't be misled by a "does not resurface" claim.

4. **3 papers in the existing `flow-matching.yaml` have an empty `method_family` after Phase 2**
   synthesis (a warning, not an error, from the health check): `2106.15561`,
   `2025.coling-main.518`, `iclr-2025-uxDFlPGRLX`. Worth a look when next touching flow-matching,
   not urgent.

5. `flow-matching.yaml` is already committed and pushed to `main` in the content repo (commits
   `34af590` prototype, `3847599` round 1) — the "committed locally, not pushed" note in some
   older memory/BACKLOG text is stale as of this session.

---

## Success Criteria

- Every Q3-2025-and-earlier ingested paper (non-Tier-2) that lists a concept in
  `related_concepts` has a corresponding entry in that concept's `wiki/_claims/{slug}.yaml`.
- `.venv/bin/python scripts/health_check.py --module integrate --wiki-dir <content-repo> -v`
  reports 0 errors across all concept YAMLs.
- `papers_not_in_any_yaml`, scoped to Q3-and-before, driven to 0 (Q4 2025 papers will still show
  up in the corpus-wide stat until their own later integration pass — that's expected).

---

## Methodology

### The two-phase model (full detail: `.agents/skills/speech-generation-integration-agent/SKILL.md`,
`docs/schemas/claims.md`, `docs/content.md` Integrate Workflow section)

- **Phase 1 — paper entry extraction.** Reads one paper page, writes one entry to `papers:` in
  the target concept's YAML. No cross-paper reasoning. Idempotent (skips IDs already present
  unless `--force`). **Capped at 20 new paper pages per concept per invocation** — process
  oldest-first by `published_date` (the agent's own discovery script enforces this ordering).
- **Phase 2 — synthesis.** Reads only the `papers:` list already written (no wiki page re-reads).
  Builds/updates `method_families` and `claim_clusters`, checks `reassessment_queue` triggers. No
  paper-count cap, but large YAMLs (50+ entries) can strain context — split `--phase 2` runs
  per-concept if synthesis stalls.
- **Invocation:** `"Run integration pass on concept: {slug}"` (or `concepts: slug1 slug2 ...` for
  several at once) via the `speech-generation-integration-agent`. Both phases run sequentially by
  default; `--phase 1` / `--phase 2` isolate one; `--force [ids]` rewrites existing entries;
  `--regenerate-clusters` rebuilds `claim_clusters`/`method_families` from scratch while
  preserving the human-curated `open_questions`/`trend_notes`/`reassessment_queue`.

### Claims parsing — two formats, both must be supported

Paper pages ingested after 2026-07-02 use the current structured format (bold role prefix +
blockquote Evidence line); pages ingested before that use a legacy bare-sentence format. Since
this task covers the **entire pre-Q4-2025 corpus**, expect a real mix of both — the integration
agent is designed to parse both without requiring paper-page rewrites (see
[[feedback_claims_format]]):

```markdown
Structured (current):
- **supports:** {generalized claim.}
  > *Evidence:* {paper-local detail.} *(§4.2, Table 1)*

Legacy (pre-2026-07-02 pages):
- {generalized claim.} *(§4.2, Table 1)*
```

For legacy claims, the agent infers `role` (defaulting to `supports` unless wording clearly
indicates `complicates`/`contradicts`/`refines`) and writes a one-sentence `evidence` field from
the paper page's own Method/Key Results/Limitations sections — never inventing new facts.

### Suggested cadence

Given the scale, don't try to run all 22 unstarted concepts in parallel or in one session:

1. **Finish `flow-matching` first** (61 papers still queued from round 1, oldest-first,
   continuing from `2503.11026` published 2025-07-30) before starting any new concept — avoids
   context-switching mid-backlog on the one concept already partway done.
2. Then work through the remaining 22 concepts one at a time. No fixed priority order has been
   set — reasonable defaults to propose at session start: largest backlog first (biggest signal
   payoff per pass: `evaluation-metrics` 318, `zero-shot-tts` 230, `neural-codec` 218,
   `subjective-evaluation` 202, `autoregressive-codec-tts` 194), or registry order (Core methods →
   Capabilities → Foundations → Evaluation). Ask the user which they'd prefer if it isn't already
   clear from context.
3. Within a concept: Phase 1 in batches of ≤20 (the hard cap), then Phase 2 once Phase 1 is fully
   caught up for that concept, then the health check, before moving to the next concept. Log each
   completed concept (or each 20-paper Phase 1 batch, if a concept needs multiple rounds) to the
   Session Log below, mirroring the Q4 ingest note's batch-summary style.
4. A paper touching multiple concepts only needs to be *read* once conceptually, but gets a
   separate YAML entry per concept it's integrated into — this is expected duplication, not a bug.

### Health check after each concept (or each Phase 1/2 pass)

```bash
.venv/bin/python3 scripts/health_check.py --module integrate --concept {slug} --wiki-dir "$(python3 scripts/resolve_wiki_dir.py)" -v
```

16 Phase 1 checks (required fields, `entry_date`/vocabulary validity, no duplicate paper/claim
IDs, Tier 2 exclusion, paper IDs exist/ingested, concept-in-registry) + 10 Phase 2 checks
(cluster/method-family required fields and cross-references, `cluster_last_reviewed` staleness).
Phase is auto-detected from the YAML (non-empty `claim_clusters` → Phase 2 checks apply).

Do not trust the agent's own closing summary uncontested — same principle as ingest sessions
(see [[feedback_agent_selfreport_unreliable]]): re-run the health check and spot-check
`paper_count` against `len(papers)` and a couple of claim entries against the actual paper page.

### YAML gotchas (same class of bug as the ingest pipeline)

Unquoted dates (`entry_date`) parse as YAML date objects, and unquoted numeric-looking paper IDs
parse as floats, dropping trailing zeros. Quote both. See [[feedback_yaml_coercion_gotchas]] —
this bit the ingest pipeline repeatedly and the integrate schema uses the same date/ID field
shapes, so it's worth guarding the same way here.

### What this task does NOT include

- **Rendering concept pages or evidence dossiers.** That's the `speech-generation-render-agent`'s
  job, reading from `wiki/_claims/*.yaml` — a separate stage, tracked separately in `BACKLOG.md`
  ("Run first render pass"). Don't conflate the two; a concept can be fully integrated with zero
  rendered output for a long time, and that's fine.
- **Q4 2025 papers.** Excluded by the scope cutoff above.

---

## Relevant memories (auto-loaded via `MEMORY.md` at session start — listed here for completeness)

- [[project_three_stage_pipeline]] — the ingest/integrate/render split, two-phase integration model, current flow-matching progress
- [[project_wiki_check_suite]] — the Pipeline Health Suite, `--module integrate` details, `papers_not_in_any_yaml` stat
- [[feedback_integration_deprioritized]] — don't proactively suggest further integration passes beyond what's explicitly requested (this note itself is the user-requested exception)
- [[project_render_agent]] — the next stage after integration; don't conflate the two
- [[feedback_claims_format]] — structured vs. legacy claim format, and why both must parse
- [[feedback_yaml_coercion_gotchas]] — unquoted dates/IDs in YAML
- [[feedback_agent_selfreport_unreliable]] — verify the agent's own summary against the actual file
- [[project_repo_structure]] — three-repo layout; integration only ever touches the **content**
  repo (`wiki/_claims/*.yaml` and `wiki/log.md`) — never `raw/metadata/`, never infra files except
  this session log
- [[feedback_commit_messages]] / [[feedback_em_dashes]] — same commit-message and prose
  conventions as ingest work

---

## Commit / Push Workflow

Integration work only touches the **content repo** (`wiki/_claims/*.yaml`, `wiki/log.md`) — the
integration agent never writes to `raw/metadata/` or any infra file. This session log
(`Q3_INTEGRATION_SESSIONS.md`) lives in the **infra repo**, so that's the only infra-side commit
needed.

1. Content repo: stage changed/new `_claims/*.yaml` files + `log.md`, commit, push.
2. Infra repo: stage this session log (and `BACKLOG.md` if its integration line needs updating),
   commit, push. **No `wiki/` submodule bump is required for pure integration work** — the
   submodule pointer only needs to move when infra needs to reference a specific content commit,
   and nothing in the integrate stage reads through that submodule path.
3. Site repo: **not needed for integration alone.** The site serves rendered `concepts/` and
   `evidence/` pages; raw `_claims/*.yaml` isn't rendered output and Quartz won't surface it as a
   page. Only bump the site's `content` submodule after a subsequent **render** pass actually
   changes visible content — don't bump it just because `_claims/` changed.

---

## Session Log

### 2026-07-21 — evaluation-metrics Phase 2 synthesis run, concept fully closed

- **First-ever Phase 2 synthesis run for `evaluation-metrics`**, against the full 285-paper set —
  the largest Phase 2 pass to date (vs. 97/60/29 for flow-matching/speech-to-speech/rlhf-speech).
- **Session was interrupted mid-task by an API session limit** partway through synthesis. Per the
  established recovery protocol, file state was checked directly before resuming: the YAML parsed
  validly, `paper_count`/`len(papers)` were intact at 285, and 10 `method_families` + 31
  `claim_clusters` had already been drafted — but the health check revealed this was a genuinely
  incomplete synthesis, not just an unwritten log entry: only 59/285 papers (21%) had a
  non-empty `method_family`, 226 papers triggering the coverage warning. For comparison, the three
  previously-closed concepts left only single-digit legitimate outliers (5/97, 4/29, and similarly
  small for speech-to-speech) — 226 outliers was not a plausible "doesn't fit any family" result.
  The same agent was resumed via `SendMessage` (not restarted from scratch, to preserve the
  legitimate work already done) with explicit instructions to finish classifying the remaining
  papers and reconcile clusters against the fuller picture, rather than accepting the partial
  result.
- **Course correction during the resumed run**: the original 10-family taxonomy was organized
  around TTS/VC architecture, which doesn't fit this concept well since most of its 285 papers are
  system papers from other concepts (TTS/VC/SCA/codec) whose relevance to evaluation-metrics is a
  single incidental `evaluation_caution` finding, not a dedicated methodology contribution. The
  agent reworked the taxonomy around evaluation-methodology *type* instead (which metric/dimension
  a paper's claim concerns: WER/CER, speaker-similarity, MOS/PESQ-style divergence, prosody, codec
  multi-metric suites, LLM-judge reliability, bias/fairness, low-resource/community, clinical/
  accessibility, data curation, watermarking), reaching **17 method_families, 271/285 papers (95%)
  covered, 14 legitimate outliers** (pure architecture/theory/efficiency papers with no
  evaluation-methodology content of their own: Tacotron 2, HiFi-GAN, AudioLDM, GOAT — already a
  documented rlhf-speech outlier too — plus model-quantization/inference-acceleration/G2P-transfer
  papers). Two families are intentionally broad umbrellas by design
  (`objective_perceptual_quality_metric_divergence` 86 papers, `asr_wer_intelligibility_evaluation`
  79 papers) spanning many unrelated architectures sharing one evaluation observation — flagged in
  `reassessment_queue` as future sub-splitting candidates rather than force-fragmented now.
- **31 claim_clusters: 23 strongly_supported, 7 emerging, 1 contested**
  (`llm_audio_judge_reliability_is_contested`: LLM/audio-LM judges approximate human evaluation
  well for instruction-following, style adherence, and checklist-rubric dialogue scoring, but fail
  for fine-grained prosody and non-verbal/raw-waveform cues — independently spot-checked
  `2506.21875` WildSpeech-Bench against its source page, confirmed it genuinely describes the
  query-aware checklist approach the cluster credits it with). While rebuilding families the
  agent cross-checked cluster completeness against the fuller paper set and added 3 previously
  missed supporting papers plus 1 refining paper. Headline cross-cutting finding, replicated
  across unrelated architectures: `wer_cer_unreliable_intelligibility_proxy` (8),
  `embedding_speaker_similarity_diverges_from_human_perception` (11),
  `automatic_mos_predictors_diverge_from_subjective_mos` (8) — together the concept's single
  dominant finding: no automatic objective metric reliably substitutes for targeted human
  perceptual judgment. **7 reassessment_queue items**: 5 `claim_status` (thin-replication
  findings: full-duplex automatic metrics without human raters, automated-annotation-consistency
  possible shared lineage, deception-rate evaluation, reference-free task-specific metrics,
  watermark robustness under realistic transforms) + 2 `method_family` (embedding-distributional-
  distance metrics thin at 4 papers; the two mega-families' internal heterogeneity, worth
  revisiting for sub-splitting).
- Independently re-verified end-to-end (not trusting the agent's closing summary uncontested):
  `paper_count`/`len(papers)` both 285, 0 duplicate IDs, all `id`/`entry_date` string-typed, the
  14 empty-`method_family` IDs matched exactly between the health check output and the agent's
  report, family/cluster/reassessment_queue counts all matched, and one cluster's supporting-paper
  citation was spot-checked against its actual source page. `health_check.py --module integrate
  --concept evaluation-metrics`: 0 errors, 14 warnings (all `method_family_coverage`, all the
  documented legitimate outliers).
- `evaluation-metrics` is now the fourth concept fully closed for Q3-and-earlier Phase 1 + Phase
  2 (after flow-matching, speech-to-speech, rlhf-speech), and by far the largest.
- Held for explicit user go-ahead before committing — everything since batch 9 (Phase 1 batches
  9-14 plus this Phase 2 run) remains uncommitted; batches 5-8 committed locally (`83e78a1`) but
  not yet pushed (content repo 4 commits ahead of `origin/main`).

### 2026-07-21 — evaluation-metrics Phase 1 batch 14 (260 → 285/286), Phase 1 fully closed

- **Final Phase 1 batch for evaluation-metrics.** The standard 20-paper cap was deliberately
  overridden for this single invocation at explicit user request, since only 25 genuine
  candidates remained — processing all of them in one batch to close the concept's Phase 1
  backlog outright. Oldest-first, `2509.17006` through `2510.00264` (2 papers, `2510.02352` and
  `2510.00264`, carry an October-prefixed arXiv ID from a late-September submission rolling over
  the month boundary — verified their actual `published_date` frontmatter is 2025-09-27 and
  2025-09-30 respectively, correctly in-scope despite the misleading ID prefix). The standing
  `2207.12598` exclusion re-confirmed and re-excluded one final time (14th consecutive batch) —
  it remains the sole permanent gap, never written to the YAML.
- **A prior attempt at this same batch was cut off by a session API limit** before any file
  write occurred (confirmed directly: `paper_count` was still 260, diff stat against the last
  commit was byte-identical to the post-batch-13 state). Restarted fresh rather than resuming,
  per the established recovery protocol for the "nothing written yet" case.
- Independently re-verified: `paper_count`/`len(papers)` both 285, 0 duplicate IDs, all
  `id`/`entry_date` string-typed, `2207.12598` absent, health check clean (0 errors, 0 warnings,
  `total_paper_entries=471` corpus-wide, consistent with 97+60+29+285). `papers_not_in_any_yaml`
  dropped 221 → 205. **Independently re-scanned all paper frontmatter matching the
  evaluation-metrics scope criteria (Q3-dated, non-Tier-2, tag present in any serialization) and
  confirmed exactly one gap corpus-wide: the permanent `2207.12598` exclusion** — Phase 1 is
  genuinely, not just nominally, fully closed for this concept.
- `evaluation-metrics` is now the fourth concept to close Phase 1 (after flow-matching,
  speech-to-speech, rlhf-speech), and the largest so far by paper count (285 vs. 97/60/29). Phase
  2 synthesis has not yet been run for this concept — a separate follow-up task.
- Held for explicit user go-ahead before committing — batches 9-14 uncommitted; batches 5-8
  committed locally (`83e78a1`) but not yet pushed (content repo 4 commits ahead of `origin/main`).

### 2026-07-21 — evaluation-metrics Phase 1 batch 13 (240 → 260/286)

- Thirteenth Phase 1 batch, 20 papers, oldest-first continuation from `2509.11425` through
  `2509.20378`. The standing `2207.12598` exclusion (Classifier-Free Diffusion Guidance, an
  off-topic ImageNet diffusion paper with `task: []` and no speech content) was re-derived
  independently from frontmatter and re-confirmed/re-excluded again (thirteenth consecutive
  batch), not counted against the 20-cap or the remaining count. Only 1 of the 20 used the
  legacy bare-claims format (`2509.15969`, VoXtream — evidence synthesized from its Method/Key
  Results/Limitations sections, role inferred from wording rather than defaulted to `supports`);
  the other 19 used the structured bold-prefix/blockquote format. Only 45 in-scope candidates
  remained going in (below the 20-cap headroom for a full second batch), so this does not close
  the concept's backlog; **25/286 remain, next: `2509.17006`, then `2509.17021`, `2509.17988`,
  `2509.18060`, `2509.18470`, ...** — a smaller batch 14 (~25 papers) will finish Phase 1 for this
  concept.
- Independently re-verified: `paper_count`/`len(papers)` both 260, 0 duplicate IDs, all
  `id`/`entry_date` string-typed and properly quoted (spot-checked, including a numeric-looking ID
  `2504.20581`), `2207.12598` absent, health check clean (0 errors, 0 warnings,
  `total_paper_entries=446` corpus-wide, consistent with 97+60+29+260). `papers_not_in_any_yaml`
  dropped 236 → 221 (a smaller drop than 20 because some of this batch's papers already appeared
  in another closed concept's YAML, e.g. flow-matching or speech-to-speech).
- Held for explicit user go-ahead before committing — batches 9-13 uncommitted; batches 5-8
  committed locally (`83e78a1`) but not yet pushed (content repo 4 commits ahead of `origin/main`).

### 2026-07-21 — evaluation-metrics Phase 1 batch 12 (220 → 240/286)

- Twelfth Phase 1 batch, 20 papers, oldest-first continuation from `2508.18006` through
  `2509.11084`. The standing `2207.12598` exclusion re-confirmed and re-excluded again (twelfth
  consecutive batch), not counted against the 20-cap. 9 of the 20 used the legacy bare-claims
  format. **45/286 remain, next: `2509.11425`, then `2508.18240`, `2509.12171`, `2509.14270`, ...**
- Independently re-verified: `paper_count`/`len(papers)` both 240, 0 duplicate IDs, all
  `id`/`entry_date` string-typed, `2207.12598` absent, health check clean (0 errors, 0 warnings,
  `total_paper_entries=426` corpus-wide, consistent with 97+60+29+240). `papers_not_in_any_yaml`
  dropped 248 → 236.
- Held for explicit user go-ahead before committing — batches 9-12 uncommitted; batches 5-8
  committed locally (`83e78a1`) but not yet pushed (content repo 4 commits ahead of `origin/main`).

### 2026-07-21 — evaluation-metrics Phase 1 batch 11 (200 → 220/286)

- Eleventh Phase 1 batch, 20 papers, oldest-first continuation from `interspeech-2025-2449`
  through `2508.17623`, mixing numeric-ID and author-name-ID Interspeech pages (e.g.
  `interspeech-2025-bokkahallisatish25_interspeech`, `interspeech-2025-gourav25_interspeech` —
  independently confirmed these are real pages on disk, not hallucinated IDs) plus a run of
  post-Interspeech `2508.x` arXiv papers. The standing `2207.12598` exclusion re-confirmed and
  re-excluded again (eleventh consecutive batch), not counted against the 20-cap. 10 of the 20
  used the legacy bare-claims format. **65/286 remain, next: `2508.18006`, `2508.20660`,
  `2509.00685`, `2509.01391`, ...**
- Independently re-verified: `paper_count`/`len(papers)` both 220, 0 duplicate IDs, all
  `id`/`entry_date` string-typed, `2207.12598` absent, health check clean (0 errors, 0 warnings,
  `total_paper_entries=406` corpus-wide, consistent with 97+60+29+220). `papers_not_in_any_yaml`
  dropped 261 → 248.
- Held for explicit user go-ahead before committing — batches 9-11 uncommitted; batches 5-8
  committed locally (`83e78a1`) but not yet pushed (content repo 4 commits ahead of `origin/main`).

### 2026-07-21 — evaluation-metrics Phase 1 batch 10 (180 → 200/286)

- Tenth Phase 1 batch, 20 papers, oldest-first continuation from `interspeech-2025-1531` through
  `interspeech-2025-2447`. The standing `2207.12598` exclusion re-confirmed and re-excluded again
  (tenth consecutive batch), not counted against the 20-cap. 4 papers used the legacy bare-claims
  format (`interspeech-2025-1993`, `-2043`, `-2447`, and `-2449` which was read but correctly
  excluded from the write since it falls after the cap), handled per the dual-format compatibility
  rules. **85/286 remain, next: `interspeech-2025-2449`, then `-2536`, `-2573`, `-2595`, `-2660`, ...**
- **Process note**: the agent initially miscounted the remaining-candidate pool by forgetting the
  `published_date < 2025-10-01` scope cutoff in its own discovery query (307/306 instead of 286),
  and over-read 5 papers beyond the 20-cap before catching the mistake. Self-corrected before
  writing; independently confirmed none of the 5 over-read IDs (`interspeech-2025-2449`, `-2536`,
  `-2573`, `-2595`, `-2660`) made it into the YAML — the write itself was clean, only the
  discovery-phase bookkeeping briefly went wrong.
- Independently re-verified: `paper_count`/`len(papers)` both 200, 0 duplicate IDs, all
  `id`/`entry_date` string-typed, `2207.12598` and all 5 over-read IDs correctly absent, health
  check clean (0 errors, 0 warnings, `total_paper_entries=386` corpus-wide, consistent with
  97+60+29+200). `papers_not_in_any_yaml` dropped 278 → 261.
- Held for explicit user go-ahead before committing — batches 9-10 uncommitted; batches 5-8
  committed locally (`83e78a1`) but not yet pushed (content repo 4 commits ahead of `origin/main`).

### 2026-07-21 — evaluation-metrics Phase 1 batch 9 (160 → 180/286)

- Ninth Phase 1 batch, 20 papers, oldest-first continuation from `interspeech-2025-0816` through
  `interspeech-2025-1494` (numeric-ID secondary sort within the shared `2025-08-17` Interspeech
  date cohort, same convention as batches 7-8). The standing `2207.12598` exclusion re-confirmed
  and re-excluded again (ninth consecutive batch), not counted against the 20-cap. **105/286
  remain, next: `interspeech-2025-1531`, `-1536`, `-1550`, `-1726`, ...**
- No interruption this batch; `log.md` entry written immediately after the YAML write as
  instructed, correctly appended under the existing `## 2026-07-21` section without disturbing
  adjacent headers.
- Independently re-verified: `paper_count`/`len(papers)` both 180, 0 duplicate IDs, all
  `id`/`entry_date` string-typed, `2207.12598` absent, health check clean (0 errors, 0 warnings,
  `total_paper_entries=366` corpus-wide, consistent with 97+60+29+180). `papers_not_in_any_yaml`
  dropped 295 → 278 (a smaller drop than the 20 newly-added entries, expected since some of this
  batch's papers were already integrated under other concepts' YAMLs). Spot-checked
  `interspeech-2025-1229` (E2E-BPVC) against its source page: BS-MOS 4.60/4.65, SS-MOS 4.02/4.07,
  ICL-VC BS-MOS 0.70, CER 10.27→7.99/9.22→7.99, SIM 0.849/0.873 all matched exactly.
- Held for explicit user go-ahead before committing — batches 9 (this one) uncommitted; batches
  5-8 committed locally (`83e78a1` in content repo) but not yet pushed (content repo 4 commits
  ahead of `origin/main`).

### 2026-07-21 — evaluation-metrics Phase 1 batch 8 (140 → 160/286)

- Eighth Phase 1 batch, 20 papers, oldest-first continuation from `interspeech-2025-0310` through
  `interspeech-2025-0779` (numeric-ID secondary sort within the shared `2025-08-17` Interspeech
  date cohort, same convention as batch 7). The standing `2207.12598` exclusion re-confirmed and
  re-excluded again, no other exclusions. **125/286 remain, next: `2207.12598` (re-confirm
  again), then `interspeech-2025-0816`, `-0854`, `-0902`, `-0973`, ...**
- No interruption this batch; `log.md` entry written immediately after the YAML write as
  instructed, correctly appended under the existing `## 2026-07-21` section without disturbing
  adjacent headers.
- Independently re-verified: `paper_count`/`len(papers)` both 160, 0 duplicate IDs, all
  `id`/`entry_date` string-typed, `2207.12598` absent, health check clean (0 errors, 0 warnings,
  `total_paper_entries=346` corpus-wide, consistent with 97+60+29+160). Gap-check via numeric
  `interspeech-2025-NNNN` ID ordering: zero numeric IDs below 0816 remain unintegrated; also
  confirmed no non-Interspeech in-scope candidate dated before the shared 2025-08-17 cohort was
  left behind. Spot-checked `interspeech-2025-0656` (EEG-driven zero-shot voice conversion) against
  its source page: all Homogeneity/Consistency/Naturalness-MOS numbers (0.9437/0.9465/0.9371,
  0.8026, 4.00) matched exactly with correct `§3.1.2`/`§4.4`/`§4.4.1` citations.
- Held for explicit user go-ahead before committing — batches 5, 6, 7, and 8 all still uncommitted.

### 2026-07-21 — evaluation-metrics Phase 1 batch 7 (120 → 140/286)

- Seventh Phase 1 batch, 20 papers, oldest-first continuation from `2508.06890` through
  `interspeech-2025-0305`. The standing `2207.12598` exclusion was correctly re-confirmed and
  re-excluded again, no reasoning error this time. No other exclusions. **146/286 remain, next:
  `2207.12598` (re-confirm again), then `interspeech-2025-0310`, `-0347`, `-0355`, `-0383`, ...**
  Includes `interspeech-2025-0063` (DLPO), the paper flagged in the rlhf-speech Phase 2 log for a
  judgment-call `method_family` reclassification — unrelated to this concept's claims about it.
- **No interruption this batch** — the agent was explicitly told upfront to write the `log.md`
  entry immediately after the YAML write, before running any validation, specifically to avoid a
  repeat of batch 6's partial-write gap. `log.md` correctly created a new `## 2026-07-21` section
  header without corrupting the adjacent `## 2026-07-20` header (no recurrence of
  [[feedback_log_insertion_bug]]).
- Independently re-verified: `paper_count`/`len(papers)` both 140, 0 duplicate IDs, all
  `id`/`entry_date` string-typed, `2207.12598` absent, health check clean (0 errors, 0 warnings,
  `total_paper_entries=326` corpus-wide, consistent with 97+60+29+140). Gap-check needed one
  extra step this time: nearly all remaining candidates share the identical nominal
  `published_date: 2025-08-17` (the Interspeech 2025 conference date), so a pure date-sort
  gap-check flags the entire untouched Interspeech cohort as false positives. Re-verified instead
  by numeric `interspeech-2025-NNNN` ID ordering (the tiebreak the agent actually used, consistent
  with a same-date secondary sort): confirmed zero numeric IDs below 0305 remain unintegrated.
  Spot-checked `interspeech-2025-0063` (DLPO) against its source page: all UTMOS/NISQA/WER numbers
  (3.65/3.02/3.18/3.16, 4.02, 1.2%/1.5%/0.99%, 67% human preference) matched the paper's results
  table exactly.
- Held for explicit user go-ahead before committing — batches 5, 6, and 7 all still uncommitted.

### 2026-07-20/21 — evaluation-metrics Phase 1 batch 6 (100 → 120/286)

- Sixth Phase 1 batch, 20 papers, oldest-first continuation from `2025.findings-acl.470` through
  `2508.06870`. The standing `2207.12598` exclusion (Classifier-Free Diffusion Guidance) was
  correctly re-confirmed and re-excluded this time — the agent was explicitly briefed on batch 5's
  reasoning error beforehand. No other exclusions. **166/286 remain, next: `2207.12598` (standing
  exclusion, re-confirm again), then `2508.06890`, `2508.07426`, `2508.07273`, `2508.07375`, ...**
- **Session was interrupted mid-task by an API session limit**, cut off right after the agent's
  last message ("Now let's validate with the Phase 1 inline validation script") — i.e. the YAML
  write had completed but validation and the `log.md` entry had not yet run. Per the established
  recovery protocol ([[feedback_session_limit_interruption]]), checked file state directly rather
  than trusting the interrupted agent: `_claims/evaluation-metrics.yaml` was valid YAML,
  `paper_count`/`len(papers)` both 120, no duplicate IDs, all `id`/`entry_date` fields
  string-typed, and `2207.12598` correctly absent — a clean, complete write. `log.md` however had
  **no batch 6 entry at all** (confirmed via `git diff`) — a genuine partial-write gap, unlike the
  prior interruptions in this session which resolved cleanly on resume. Rather than resuming the
  agent, reconstructed the batch 6 log entry by hand directly from the YAML's actual paper list
  (positions 101–120) and wrote it manually into `log.md`, since all the needed information (paper
  IDs, counts, exclusion) was independently derivable and verifiable from the committed-quality
  YAML itself.
- Independently verified no silent gaps: re-derived the full in-scope candidate list from paper
  frontmatter and confirmed every in-scope paper dated on or before the last-processed paper
  (`2508.06870`, 2025-08-09) is either integrated, or is the standing `2207.12598` exclusion. One
  same-day candidate (`2508.06890`, also 2025-08-09) is simply next-in-line once the 20-cap was
  hit, not a missed paper. Health check clean (0 errors, 0 warnings, `total_paper_entries=306`
  corpus-wide, consistent with 97+60+29+120). Spot-checked `2025.sigdial-1.51` (rrSDS 2.0 robotic
  dialogue demo paper) against its source page: all three claims (modular IU architecture,
  synchronization challenges, engineering-overhead reduction) traced exactly to `§1`-`§4`, and
  `related_concepts` confirmed the `evaluation-metrics` tag.
- Held for explicit user go-ahead before committing — batches 5 and 6 are both still uncommitted
  as of this log entry.

### 2026-07-20 — evaluation-metrics Phase 1 batch 5 (80 → 100/286)

- Fifth Phase 1 batch, 20 papers, oldest-first continuation from `2507.09282` through
  `2025.findings-acl.1226`. No genuine scope-mismatch exclusions this batch (all 20 processed
  papers integrated cleanly). Includes `2025.acl-long.313` (F5-TTS, canonical ACL ID per
  [[feedback_f5tts_paper_id]], correctly not the arXiv `2410.06885` duplicate). **186/286 remain,
  next: `2207.12598` (see reporting-bug note below), then `2025.findings-acl.470`,
  `2025.findings-acl.534`, `2025.findings-acl.71`, `2507.17527`, ...**
- **Reporting bug caught and corrected before commit**: the agent's own report and initial
  `log.md` wording claimed the standing `2207.12598` exclusion (Classifier-Free Diffusion
  Guidance, off-topic ImageNet diffusion paper excluded in batches 1-4) "does not resurface" and
  omitted it from the batch 6 candidate preview, reasoning that its 2022 date put it "before this
  batch's range" — backwards logic, since an oldest-first scan should always resurface the oldest
  unintegrated candidate regardless of how old it is. Independently re-derived the candidate list
  directly from paper frontmatter (not trusting the agent's summary, per
  [[feedback_agent_selfreport_unreliable]]): `2207.12598` is still tagged `evaluation-metrics`,
  still Q3-scoped, still Tier 1, and still absent from the YAML — confirming it remains the true
  oldest unintegrated in-scope candidate, unchanged from batches 1-4. The 186-remaining *count*
  the agent reported was numerically correct by coincidence; only the *reasoning* and the "next
  candidate" pointer were wrong. `log.md` wording corrected to state this accurately and to list
  `2207.12598` first in the batch 6 preview, so a future session isn't misled into skipping the
  re-exclusion step. Data integrity itself was unaffected: 100/100 `paper_count`/`len(papers)`, 0
  duplicate IDs, all `id`/`entry_date` fields string-typed, health check clean (0 errors, 0
  warnings). Spot-checked `2025.acl-long.313` (F5-TTS) against its source page: all 5 claim
  numbers (WER 2.42/2.53/2.84/2.41/18.1%, UTMOS 3.70/3.89, RTF 0.15) matched exactly with correct
  `§3.2`/`§5`/`§5.1`/`§5.2`/`§4` citations.
- Held for explicit user go-ahead before committing (per this session's instruction) — not yet
  committed as of this log entry.

### 2026-07-20 — evaluation-metrics Phase 1 batch 4 (60 → 80/286)

- Fourth Phase 1 batch, 20 papers, oldest-first continuation from `2025.americasnlp-1.1` through
  `2507.08319`. Same standing exclusion re-applied on re-encounter: `2207.12598` (Classifier-Free
  Diffusion Guidance), the oldest unintegrated in-scope candidate on disk since it was never
  written to the YAML in batches 1–3, excluded again for the same reason (off-topic ImageNet
  diffusion paper, no speech content). Not replaced in this batch's 20-cap. No Tier 2 papers
  encountered in this range. **205/286 remain, next oldest `2507.09282`** (followed by
  `2507.09310`, `2506.18296`, `2507.10985`, ...).
- Independently re-verified (not trusting the agent's closing summary uncontested, per
  [[feedback_agent_selfreport_unreliable]]): `paper_count`/`len(papers)` both 80, no duplicate
  IDs, all `id`/`entry_date` fields string-typed (no YAML date/float coercion — see
  [[feedback_yaml_coercion_gotchas]]), health check clean (`--module integrate --concept
  evaluation-metrics`: 0 errors, 0 warnings). Spot-checked `2507.03912` (prosody-labeling SSL
  features paper) against its source page: all four claim numbers (89.8/89.0/82.5% ACC accuracy;
  75.2%/62.9% for melspectrogram/F0 baselines; Japanese-vs-English SSL pretraining comparison)
  matched the paper page's Key Results section and `§5.4`/`§5.6` citations exactly, and
  `related_concepts` frontmatter confirmed the `evaluation-metrics` tag.
- Committed in the content repo (`_claims/evaluation-metrics.yaml` + `log.md`, one commit,
  `f82206d`). Not pushed this session, consistent with the commit-only pattern for prior batches.

### 2026-07-20 — evaluation-metrics Phase 1 started, batches 1–3 (60/286)

- **First-ever integration pass for `evaluation-metrics`**, new `wiki/_claims/evaluation-metrics.yaml`
  created. Three Phase 1 batches, 20 papers each, oldest-first: batch 1 `1703.10135` →
  `2403.16973` (Tacotron-era through VoiceCraft), batch 2 `2404.03204` → `2502.04128` (RALL-E
  through Llasa), batch 3 `2502.06490` → `2025.iwsds-1.27`. 60/286 in-scope candidates processed,
  225 remain, next oldest `2025.americasnlp-1.1`.
- **One consistent exclusion across all three batches**: `2207.12598` (Classifier-Free Diffusion
  Guidance) — a class-conditional ImageNet diffusion-guidance paper with `task: []` and no speech
  content of any kind, wikilinked from `evaluation-metrics` only as background inspiration for
  CFG-style guidance mechanisms elsewhere in the corpus. Excluded independently on each
  re-encounter (batches 1, 2, 3) for the same reason each time — a stable precedent, not
  indecision.
- **Batch 2 was interrupted mid-task by an API session limit**, cut off right after the agent's
  last message ("Now I'll write the Python script that builds all 20 entries and inserts them")
  — i.e. discovery/drafting was done but nothing had been written to disk yet. Checked the file
  directly before resuming: `evaluation-metrics.yaml` was unchanged from batch 1 (still exactly 20
  papers) and `log.md` had no batch-2 entry, confirming a clean pre-write state with no partial or
  corrupted output. The same agent was resumed via `SendMessage` (not restarted) to write the
  already-drafted 20 entries; it was explicitly told to re-verify its draft before committing it to
  disk rather than force a potentially-stale draft through. Result independently re-verified
  afterward: `paper_count`/`len(papers)` (40/40), no duplicate IDs across batches, correct
  re-exclusion of `2207.12598`, health check 0 errors/0 warnings.
- **Batch 3's agent caught and self-corrected its own arithmetic error** before finishing: an
  initial draft log-bullet stated 245 papers remaining (carried over from batch 2's post-batch
  count without subtracting batch 3's 20), corrected to the right figure (225) before the run
  ended. Independently re-verified: the committed log entry and the true remaining-candidate count
  both read 225, consistent with 245 − 20.
- All three batches independently re-verified the same way as prior concepts (never trusting an
  agent's closing summary uncontested — see [[feedback_agent_selfreport_unreliable]]): YAML
  structural checks (`paper_count` vs `len(papers)`, uniqueness, string-typed IDs/dates),
  `health_check.py --module integrate --concept evaluation-metrics` (0 errors/0 warnings after
  every batch), and one claim per batch spot-checked against its source paper page (UTMOS
  listener-dependent MOS modeling, VoiceBench cascade-vs-e2e gap, Landscape-of-SLMs
  content-vs-acoustic-reasoning tradeoff) — all traced cleanly with correct section citations.
- **Committed at end of session**: content repo (`_claims/evaluation-metrics.yaml` new file +
  3 `log.md` entries, one commit) and this infra session log. Not pushed this session (user
  chose commit-only for the prior rlhf-speech work too); push deferred to a later explicit request.

### 2026-07-20 — rlhf-speech Phase 2 synthesis run, concept fully closed

- **Phase 2 synthesis run for `rlhf-speech`** against the full 29-paper set (first Phase 2 run
  for this concept): **5 method_families** (all new — `dpo_style_preference_optimization_discrete_tts`
  11 papers, `rl_policy_gradient_reward_optimization` 9, `differentiable_reward_gradient_backprop`
  3, `continuous_generative_preference_optimization` 3, `reward_model_infrastructure` 2; 3 papers
  have dual family membership by design). **20 claim_clusters** (9 strongly_supported, 11
  emerging, **0 contested** — unlike flow-matching (1) and speech-to-speech (2); read as too few
  independent replications yet to surface real disagreement, not necessarily genuine consensus).
  Headline strongly_supported cluster `rlhf_posttraining_beats_sft_baseline` (11 supporting
  papers): preference/reward-based post-training (DPO/KTO/GRPO/differentiable-reward) consistently
  beats SFT-only baselines on intelligibility/similarity/naturalness. `rlhf_reward_hacking_risk`
  (7 supporting + 2 refining, no disputing paper) recurs across ~7/29 papers regardless of
  architecture or method, read as a structural property of applying verifiable rewards to speech
  rather than a defect of any one technique. **3 reassessment_queue items**: watching for a second
  GFlowNet paper (GOAT family), cross-backbone replication for the continuous-generative-DPO
  cluster (echoes the flow-matching CFG contested-downgrade precedent), and a second primary-research
  SCA/dialogue RLHF paper beyond Step-Audio. **4 method_family outliers** (empty, expected):
  `2025.naacl-demo.12` (ESPnet-SpeechLM, toolkit/demo, no original experiments),
  `2025.acl-long.682` (SpeechLM survey, no original experiments), `2508.15442` (GOAT, genuine
  single-paper GFlowNet paradigm, below the 2-paper family threshold), `2509.19928` (ProsodyEval,
  evaluation-methodology paper, DPO incidental to its core contribution).
- **Session was interrupted mid-task by an API session limit** partway through Phase 2 (after the
  agent had finished and self-verified per-paper `method_family` assignments for all 29 papers,
  before writing the tail `claim_clusters`/`method_families`/`reassessment_queue` sections). Per
  the established recovery protocol (see the 2026-07-19/20 entry below), the file was checked
  directly before resuming rather than trusting the interrupted agent's partial output: `git diff`
  showed a clean, complete 25-insertion/25-deletion change (only `method_family` fields on 25 of
  29 papers, 4 correctly left empty), YAML parsed validly, `paper_count` matched `len(papers)`.
  The same agent was resumed via `SendMessage` (not restarted from scratch) to finish the tail
  sections. After completion, independently re-verified: `paper_count`/`len(papers)` (29/29),
  method_family and claim_cluster counts, cluster status breakdown, and the empty-method_family
  list all matched the agent's report exactly; `health_check.py --module integrate --concept
  rlhf-speech` passed 0 errors / 4 expected warnings (the 4 documented outliers).
- One judgment call worth a second look later: the agent reclassified DLPO
  (`interspeech-2025-0063`) from an initial draft placement in the continuous-generative-DPO
  family into `rl_policy_gradient_reward_optimization`, reasoning that its baselines (DDPO, DPOK,
  KLinR, RWR) are RL methods despite the paper's "DLPO" name suggesting DPO-style preference
  optimization. Not independently re-verified against the source paper this session.
- `rlhf-speech` is now the third concept (after flow-matching and speech-to-speech) fully closed
  for Q3-and-earlier Phase 1 + Phase 2.

### 2026-07-20 — rlhf-speech Phase 1 closed from scratch

- **rlhf-speech started and closed for Phase 1** (Phase 2 deliberately deferred per user
  instruction). Two batches, 20 then 9, 0 in-scope exclusions: 29/29 Q3-scoped papers integrated,
  oldest-first from `2406.00654` (2024-06-02, UNO) through `2509.25416` (2025-09-30). 2 candidates
  correctly skipped as Tier 2 (`2501.12948`, `2307.09288`). All 39+100=139 extracted claims carry
  a real `source` citation; no `"not specified"` fallbacks needed. Both batches independently
  re-verified against the actual YAML (`paper_count`/`len(papers)` match, ID lists match) and a
  spot-checked paper (`2508.15442`, GOAT) against its source page — claim text, section
  citations, and numbers all traced cleanly. `health_check.py --module integrate --concept
  rlhf-speech` passed 0 errors/0 warnings after each batch.
- **Log-insertion bug recurred in a new code path**: the previously-fixed regex-based section
  insertion (see [[feedback_log_insertion_bug]], fixed 2026-06-10 for the append-to-end-of-file
  case) stripped the `## ` heading prefix from the *following* day's section (`## 2026-07-19` →
  `2026-07-19`) when appending an entry within an *existing* day section — a different code path
  than the original bug. Found and repaired by hand during the second batch; verified afterward
  that all section headings in `log.md` are intact. Worth a proper code-level fix rather than
  relying on catching it by inspection each time.
- Two papers integrated with only a nominal/infrastructural connection to rlhf-speech, marked
  `relevance: low` / `current_role: minor` with explicit caveats rather than excluded outright
  (RLHF mentioned as a supported feature or potential future reward-model use, no dedicated RLHF
  experiments in the paper itself) — see Manual Verification Queue below.

### 2026-07-19/20 — flow-matching closed, speech-to-speech done from scratch

- **flow-matching Phase 1 completed**: 3 batches (54→74→94→97 papers), closing the round-1
  backlog. 11 Q4-2025-or-later candidates identified in the same discovery pool and explicitly
  excluded per scope (they'll get their own pass later, per `Q4_INGESTION_SESSIONS.md`).
- **flow-matching Phase 2 run for the first time against the full 97-paper set**: 7
  method_families (2 new: `continuous_ar_fm_head`, `fm_auxiliary_attribute`), 34 claim_clusters
  (8 strongly_supported, 25 emerging, 1 contested), 3 reassessment_queue items. Notable: the
  `cfg_conditioning_mechanism_adopted` cluster was downgraded strongly_supported → contested after
  `2509.19668` found CFG techniques from image generation don't cleanly transfer to flow-matching
  TTS. 5 papers remain legitimate method_family outliers (pre-CFM survey, off-the-shelf-backbone
  usage, theory-only, benchmark-only papers) — expected, not a defect.
- **speech-to-speech started and fully closed** (Phase 1 + Phase 2), the second concept to reach
  this milestone. Phase 1: 4 batches, 60/63 in-scope papers integrated; 3 papers evaluated and
  excluded for having no speech-generation stage of their own despite carrying the tag
  (`2025.acl-long.388` DiVA — speech-in/text-out; `interspeech-2025-2660` VAP turn-taking
  predictor; `2509.23938` Easy Turn detector) — all three independently confirmed against source
  pages, establishing a consistent exclusion precedent for this concept going forward. Phase 2: 5
  method_families, 16 claim_clusters (13 strongly_supported, 2 contested, 1 emerging). Headline
  finding: `cascade_outperforms_e2e_on_benchmarks` turned out much larger than expected (10
  supporting + 5 refining papers) — cascaded ASR+LLM+TTS pipelines still beat end-to-end S2S on
  general instruction-following/reasoning benchmarks, though the gap is concentrated in
  paralinguistic fidelity rather than semantic accuracy. Two duplicate paper pairs discovered and
  handled as single data points for cluster-support counting: `2505.02625`/`2025.acl-long.912`
  (LLaMA-Omni 2, arXiv vs. ACL) and `2412.15649`/`2025.findings-acl.115` (SLAM-Omni, arXiv vs. ACL
  Findings) — both flagged for an eventual ingest-side dedup pass per the existing
  arXiv-full-version-dedup precedent (Emilia case).
- **Two process bugs found and fixed** (see the corrected state table above for detail): (1) an
  ad-hoc scoping script checked frontmatter field `tier` instead of the actual `ingest_tier`,
  silently failing to exclude Tier 2 stubs; (2) `related_concepts` has 3 coexisting YAML
  serializations corpus-wide with no clean chronological cutover, causing a naive single-format
  parser to undercount by roughly half. Neither bug affected the actual `_claims/*.yaml` writes
  (the integration agent invocations independently re-verify both fields per paper), only the
  ad-hoc reporting scripts used to answer "how many Q3 papers per concept" questions. A backlog
  item was added to standardize `related_concepts` serialization.
- **Two agent runs were interrupted mid-task by session API limits** (once during a speech-to-speech
  Phase 1 batch, once during the speech-to-speech Phase 2 run). Both times, the file state was
  checked directly before resuming (valid YAML, correct paper/cluster counts, no partial writes)
  rather than trusting the interrupted agent's own partial output — both resumes were clean,
  no data loss or corruption. A stray `log.md` header corruption (missing `## ` prefix on the
  2026-07-18 and 2026-07-17 section headers, introduced sometime in the uncommitted working tree
  this session) was found and repaired by hand mid-session.
- Everything in this session was independently re-verified against `health_check.py` output and,
  for a sample of claims/clusters each batch, against the actual source paper pages — never taking
  an agent's closing summary at face value (see [[feedback_agent_selfreport_unreliable]]).

---

## Manual Verification Queue

Concept/paper entries worth a second look, flagged during integration passes (health-check
warnings, ambiguous claim roles, or judgment calls noted by the agent).

| Concept | Paper ID | Note |
|---|---|---|
| flow-matching | `2106.15561` | empty `method_family` after Phase 2: pre-2021 survey predating the CFM objective, "flow" refers to normalizing flows not conditional flow matching — intentional outlier |
| flow-matching | `2025.acl-long.1252` | empty `method_family`: F5-TTS used entirely off-the-shelf, no FM methodology contribution |
| flow-matching | `2025.findings-acl.115` | empty `method_family` for flow-matching: AR-LM only, FM present merely as an unrelated pretrained vocoder |
| flow-matching | `interspeech-2025-1066` | empty `method_family`: pure theory paper (SSM↔flow-matching equivalence proof), no TTS/VC system |
| flow-matching | `2509.19928` | empty `method_family`: benchmark/evaluation paper, `architecture: []`, no system of its own |
| flow-matching | `cfg_conditioning_mechanism_adopted` (cluster) | downgraded strongly_supported → contested by `2509.19668`; watch for further evidence either way |
| flow-matching | `2509.09631`, `2509.18470` | `current_role: frontier_probe` — narrow proof-of-concept scope, watch for adoption/replication signal |
| speech-to-speech | `2025.acl-long.388` (DiVA) | excluded from concept: speech-in/text-out only, no speech-generation stage |
| speech-to-speech | `interspeech-2025-2660` (VAP) | excluded from concept: acoustic turn-taking predictor, no speech-generation stage |
| speech-to-speech | `2509.23938` (Easy Turn) | excluded from concept: turn-taking detector, no speech-generation stage — closest call of the three, tightly coupled to S2S systems architecturally despite the exclusion |
| speech-to-speech | `2505.02625` / `2025.acl-long.912` | duplicate pair (LLaMA-Omni 2, arXiv vs. ACL) — both have separate YAML entries but count as one data point for cluster support; candidate for ingest-side dedup |
| speech-to-speech | `2412.15649` / `2025.findings-acl.115` | duplicate pair (SLAM-Omni, arXiv vs. ACL Findings) — same treatment; candidate for ingest-side dedup |
| speech-to-speech | `staged_pretraining_effect_on_instruction_following` (cluster) | contested cluster confounded by model scale (SLAM-Omni 0.5B vs. Baichuan-Audio 7B) — needs a scale-matched ablation to resolve cleanly |
| speech-to-speech | `2025.naacl-long.484` (Behavior-SD) | borderline sub-paradigm fit: generates full-duplex dialogue audio rather than acting as an interactive agent |
| speech-to-speech | `2025.iwsds-1.27` | borderline concept fit: general turn-taking survey, not S2S-specific — consider whether it belongs under `evaluation-metrics`/`subjective-evaluation` instead |
| rlhf-speech | `2025.naacl-demo.12` (ESPnet-SpeechLM) | `relevance: low`, `current_role: minor`: RLHF listed as a supported training feature of the toolkit, no dedicated RLHF experiments in the paper itself |
| rlhf-speech | `2508.08957` (QAMRO) | `relevance: low`, `current_role: minor`: paper discusses potential future use as a reward model for RLHF, does not itself run RLHF training |
| evaluation-metrics | `llm_audio_judge_reliability_is_contested` (cluster) | contested: LLM/audio-LM judges work for instruction-following/style/checklist-rubric scoring but fail on fine-grained prosody and non-verbal/raw-waveform cues; capability-scoped contest, not a blanket rejection |
| evaluation-metrics | `objective_perceptual_quality_metric_divergence` (family, 86 papers), `asr_wer_intelligibility_evaluation` (family, 79 papers) | intentionally broad umbrella families spanning many unrelated architectures sharing one evaluation-methodology observation; flagged as future sub-splitting candidates rather than force-fragmented now |
| evaluation-metrics | `embedding_distributional_distance_metrics` (family) | thin at 4 papers, watch for growth |
| evaluation-metrics | 14 empty-`method_family` papers | legitimate outliers: pure architecture/theory/efficiency papers with no evaluation-methodology content (Tacotron 2 `1712.05884`, HiFi-GAN `2010.05646`, AudioLDM `2301.12503`, GOAT `2508.15442` — also a documented rlhf-speech outlier — plus `2506.09874`, `2509.05359`, `2509.08696`, `2509.23147`, `interspeech-2025-1122/-1364/-1763/-1819/-2031/-2449`) |
