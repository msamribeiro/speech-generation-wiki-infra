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

**State as of 2026-07-26, after diffusion-tts Phase 2 closed** (re-run the commands
above before resuming — this will be stale). This
table is now **Q3-scoped directly** (`published_date < 2025-10-01`, non-Tier-2, counted from paper
frontmatter, not the corpus-wide `corpus_summary.py` output) — see the note below on why the
corpus-wide `Covers`-style column was dropped:

| Concept | Q3-scoped papers referencing it | Integrated | % |
|---|---|---|---|
| **evaluation-metrics** | **286** | **285** | **100%** (Phase 1+2) |
| **zero-shot-tts** | **203** | **203** | **100%** (Phase 1+2) |
| neural-codec | 184 | 0 | 0% |
| subjective-evaluation | 180 | 0 | 0% |
| **autoregressive-codec-tts** | **165** | **165** | **100%** (Phase 1+2) |
| self-supervised-speech | 146 | 0 | 0% |
| spoken-language-model | 127 | 0 | 0% |
| **disentanglement** | **100** | **100** | **100%** (Phase 1+2) |
| **flow-matching** | **97** | **97** | **100%** |
| **prosody-control** | **94** | **94** | **100%** (Phase 1+2) |
| voice-conversion | 87 | 0 | 0% |
| speaker-adaptation | 79 | 0 | 0% |
| multilingual-tts | 76 | 0 | 0% |
| emotion-synthesis | 74 | 0 | 0% |
| **speech-to-speech** | **63** | **60** | **95%** |
| gan-vocoder | 60 | 0 | 0% |
| streaming-tts | 54 | 0 | 0% |
| **diffusion-tts** | **46** | **46** | **100%** (Phase 1+2) |
| **instruction-conditioned-tts** | **44** | **44** | **100%** (Phase 1+2) |
| **rlhf-speech** | **29** | **29** | **100%** (Phase 1+2) |
| transformer-enc-dec-tts | 28 | 0 | 0% |
| singing | 10 | 0 | 0% |
| fine-tuning | 1 | 0 | 0% |
| **TOTAL** | **2233** | **1123** | **50.3%** |

`papers_not_in_any_yaml` (corpus-wide, all quarters, via `health_check.py`): **93** as of
2026-07-26 after zero-shot-tts Phase 1 closed. This is a unique-paper corpus-wide
coverage statistic, so it does not decrease by one for every per-concept YAML entry.

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

**`flow-matching`, `speech-to-speech`, `rlhf-speech`, `evaluation-metrics`, `disentanglement`,
`autoregressive-codec-tts`, `instruction-conditioned-tts`, `prosody-control`, `zero-shot-tts`,
and `diffusion-tts` are fully closed
for Q3-and-earlier Phase 1 + Phase 2** (97/97, 60/63, 29/29, 285/286, 100/100, 165/165, 44/44,
94/94, 203/203, and 46/46 respectively —
the 3-paper gap on speech-to-speech is intentional: `2025.acl-long.388` DiVA,
`interspeech-2025-2660` VAP, and `2509.23938` Easy Turn were each evaluated and correctly excluded
for having no speech-generation stage of their own, despite carrying the tag; note `2509.23938`
is *not* a contradiction — it's separately and correctly integrated into `evaluation-metrics`,
since exclusion from one concept doesn't imply exclusion from another; evaluation-metrics' one gap
is the permanent `2207.12598` exclusion). `evaluation-metrics` is the largest concept closed so
far by paper count (285 vs. 97/60/29/100) and its Phase 2 pass required a mid-run course correction
(see Session Log) — the first attempt only covered 59/285 papers (21%) before a session-limit
interruption, and was resumed and reworked around evaluation-methodology *type* rather than TTS
architecture to reach 271/285 (95%) coverage with 14 legitimate outliers. `disentanglement`'s
Phase 2 pass hit a similar (smaller-scale) pattern: a session-limit interruption left per-paper
`method_family` assignment at 77/100 with 23 empty, and the resumed run reconciled 7 of those 23
against the same evidentiary standard already used elsewhere, landing at 16/100 legitimate
outliers, 10 method_families, 17 claim_clusters (12 strongly_supported, 3 emerging, 2 contested).
`autoregressive-codec-tts` is fully closed at 165/165 after nine Phase 1 batches and one Phase 2
synthesis pass. The live
YAML-frontmatter discovery on 2026-07-25 found 165 candidates rather than the 166 recorded on
2026-07-22; the current live count is used here. `instruction-conditioned-tts` is fully closed
at 44/44 after three Phase 1 batches and one Phase 2 synthesis pass. `prosody-control` is fully
closed at 94/94 after five Phase 1 batches and one Phase 2 synthesis pass. As of 2026-07-26,
`zero-shot-tts` is fully closed at 203/203 after eleven Phase 1 batches and one Phase 2 synthesis
pass. `diffusion-tts` is fully closed at 46/46 after three Phase 1 batches and one Phase 2
synthesis pass, leaving 13 concepts with no `wiki/_claims/{slug}.yaml` file yet.

**Scale note:** at the Phase 1 cap of 20 new papers per concept per invocation (see Methodology),
and with `papers_not_in_any_yaml` (corpus-wide, unique papers) at 93, fully clearing the
Q3-and-before backlog for the remaining 13 unstarted concepts is at minimum 93 ÷ 20 ≈ **5+ Phase 1
invocations** if every remaining paper needed only one concept entry — in practice higher, since a
paper touching multiple unstarted concepts needs a separate YAML entry per concept (the per-concept
"Q3-scoped papers referencing it" column above sums to far more than 157 for exactly this reason,
so summing that column directly overstates the invocation count). Plus one or more Phase 2
synthesis passes per concept, plus health checks. This will span many sessions — pace it like the
Q4 ingest work (batch, verify, log, repeat), not as a single sitting.

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

### 2026-07-26 — diffusion-tts Phase 2 synthesis run, concept fully closed

- Ran the first Phase 2 synthesis pass against all 46 Phase 1 entries and 199 extracted claims,
  reading only `_claims/diffusion-tts.yaml` as required. No reassessment items were pending.
- Created 7 architecture-based `method_families` and assigned 41/46 papers reciprocally. The
  largest families are `score_based_diffusion_synthesis` (14 papers),
  `flow_and_consistency_alternatives` (7), and `autoregressive_diffusion_hybrids` and
  `adversarial_and_distilled_diffusion` (5 each). Five architecture-unspecified or
  diffusion-adjacent papers remain legitimate outliers rather than being forced into a family.
- Created 15 `claim_clusters`, all `strongly_supported`, spanning diffusion fidelity and sampling
  cost; acceleration, latent targets, guidance, and transformer scaling; zero-shot transfer,
  factorized and expressive control, robustness, and preference optimization; flow/consistency
  alternatives, alignment supervision, representation choice, and evaluation limitations. Added
  5 open questions and 5 trend notes.
- Phase 2 health validation passed with 0 errors and 5 expected method-family coverage warnings.
  Corpus-wide totals are now 1,123 paper entries and 200 claim clusters across 10 concept YAMLs;
  `papers_not_in_any_yaml` remains 93. `diffusion-tts` is now fully closed for Q3-and-earlier.

### 2026-07-26 — diffusion-tts Phase 1 batches 2–3, Phase 1 complete (20 → 46/46)

- Continued `diffusion-tts` with exactly two sequential oldest-first Phase 1 batches. Batch 2
  integrated 20 papers from `interspeech-2025-0554` through `2509.08696`; batch 3 integrated the
  final 6 from `2509.09748` through `2509.25416`. Authoritative discovery now finds all 46
  eligible Q3-and-earlier papers integrated, with 0 remaining.
- Batch 2 preserved 86 claims from 17 structured and 3 legacy pages; batch 3 preserved 25 claims
  from 6 structured pages. All 111 claims retain source citations, with no empty claims lists and
  no `source: "not specified"` fallbacks. Each entry received fresh diffusion-TTS-specific
  relevance, evidence-role, current-role, claim-relevance, caveat, and empty `method_family`
  judgments.
- The concept-scoped Phase 1 health check passed after each batch with 0 errors and 0 warnings.
  Corpus-wide `papers_not_in_any_yaml` remained 93. Phase 2 was not run; `method_families` and
  `claim_clusters` remain empty pending explicit go-ahead.

### 2026-07-26 — diffusion-tts Phase 1 batch 1 (0 → 20/46)

- Started `diffusion-tts` with the standard Q3-and-earlier Phase 1 protocol. Authoritative
  discovery found 46 eligible papers, no Tier 2 exclusions, and no pre-existing concept YAML.
  Processed the 20 oldest papers from `2105.06337` through `interspeech-2025-0063`; 26 remain.
- Preserved all 88 claims from 4 structured and 16 legacy pages. Every paper-level extraction was
  already validated in another concept YAML, then received fresh diffusion-TTS-specific paper
  relevance, evidence roles, current role, claim relevance, caveat, and empty `method_family`
  judgments. All claims retain source citations; there are no empty claim lists or
  `source: "not specified"` fallbacks.
- The concept-scoped Phase 1 health check passed with 0 errors and 0 warnings
  (`total_paper_entries=1097`, `papers_not_in_any_yaml=93`). Phase 2 was not run, and
  `method_families` and `claim_clusters` remain empty.

### 2026-07-26 — zero-shot-tts Phase 2 synthesis run, concept fully closed

- Ran the first Phase 2 synthesis pass against all 203 Phase 1 entries and 903 extracted claims,
  reading only `_claims/zero-shot-tts.yaml` as required. No reassessment items were pending.
- Created 9 architecture-based `method_families` and assigned 187/203 papers reciprocally. The
  largest families are `autoregressive_speech_token_lm` (64 papers),
  `nonautoregressive_flow_matching` (38), and `hybrid_ar_semantic_nar_acoustic` (25). The 16
  unassigned papers have empty Phase 1 architecture fields and contribute primarily
  infrastructure, evaluation, historical-context, or architecture-comparison evidence, so they
  remain legitimate outliers rather than being forced into a method family.
- Created 18 `claim_clusters`: 16 `strongly_supported` and 2 `contested`. The contested clusters
  cover whether cross-lingual cloning necessarily leaks language or prosody and whether automatic
  metrics consistently fail to capture perceived cloning quality. Added 5 open questions and 5
  trend notes covering prompt robustness, representation choice, evaluation validity, data scale,
  long-form generation, and cloning safeguards.
- Phase 2 health validation passed with 0 errors and 16 expected method-family coverage warnings.
  Corpus-wide totals are now 1,077 paper entries and 185 claim clusters across 9 concept YAMLs;
  `papers_not_in_any_yaml` remains 93. `zero-shot-tts` is now fully closed for Q3-and-earlier.

### 2026-07-26 — zero-shot-tts Phase 1 batch 11, Phase 1 complete (200 → 203/203)

- Completed the final oldest-first Phase 1 batch with `2509.22167`, `2509.24650`, and
  `2509.25131`. Authoritative metadata discovery now finds all 203 eligible Q3-and-earlier papers
  integrated, with 0 remaining after excluding 3 Tier 2 records. The closure audit specifically
  rechecked `2407.04051`: its page frontmatter omits `ingest_tier`, but its authoritative raw
  metadata records `ingest_tier: 2`, so the health check correctly requires its exclusion.
- Extracted all 14 claims directly from the three structured paper pages. Every claim retains a
  source citation; there are no empty claims lists and no `source: "not specified"` fallbacks.
- The concept-scoped Phase 1 health check passed with 0 errors and 0 warnings
  (`total_paper_entries=1077`, `papers_not_in_any_yaml=93`). Phase 2 was not run:
  `method_families` and `claim_clusters` remain empty pending explicit go-ahead.

### 2026-07-26 — zero-shot-tts Phase 1 batches 9–10 (160 → 200/203)

- Continued `zero-shot-tts` with exactly two sequential oldest-first Phase 1 batches. Batch 9
  integrated 20 papers from `2509.02020` through `2509.14579`; batch 10 integrated 20 papers from
  `2509.14684` through `2509.22062`. The concept now has 200/203 entries, with exactly 3 remaining.
- Batch 9 preserved 89 claims from 15 structured and 5 legacy pages; batch 10 preserved 86 claims
  from 18 structured and 2 legacy pages. All 175 claims retain source citations, with no empty
  claims lists and no `source: "not specified"` fallbacks. `2509.12831` was the only paper without
  an existing entry in another claim YAML and was extracted directly from its paper page.
- The concept-scoped Phase 1 health check passed after each batch with 0 errors and 0 warnings.
  Phase 2 was not run. Corpus-wide `papers_not_in_any_yaml` decreased from 94 to 93 in batch 9
  and remained 93 after batch 10.

### 2026-07-26 — zero-shot-tts Phase 1 batches 7–8 (120 → 160/203)

- Continued `zero-shot-tts` with exactly two sequential oldest-first Phase 1 batches. Batch 7
  integrated 20 papers from `interspeech-2025-0596` through `interspeech-2025-1726`; batch 8
  integrated 20 papers from `interspeech-2025-1779` through `2507.14534`. The concept now has
  160/203 entries, with 43 remaining.
- Batch 7 preserved 83 claims from 12 structured and 8 legacy pages; batch 8 preserved 83 claims
  from 8 structured and 12 legacy pages. All 166 claims retain source citations, with no empty
  claims lists and no `source: "not specified"` fallbacks. Two papers without an existing entry
  in another claim YAML (`interspeech-2025-0787`, `interspeech-2025-2815`) were extracted directly
  from their legacy claim blocks; the first batch-7 attempt detected the unsupported-format case
  and stopped before writing, after which the legacy compatibility path was applied from a clean
  120-paper state.
- The concept-scoped Phase 1 health check passed after each completed batch with 0 errors and
  0 warnings. Phase 2 was not run. Corpus-wide `papers_not_in_any_yaml` decreased from 96 to 94.

### 2026-07-26 — zero-shot-tts Phase 1 batches 5–6 (80 → 120/203)

- Continued `zero-shot-tts` with exactly two sequential oldest-first Phase 1 batches. Batch 5
  integrated 20 papers from `2025.acl-long.1043` through `2508.02038`; batch 6 integrated 20
  papers from `2504.10352` through `interspeech-2025-0575`. The concept now has 120/203 entries,
  with 83 remaining.
- Batch 5 preserved 93 claims from 9 structured and 11 legacy pages; batch 6 preserved 91 claims
  from 2 structured and 18 legacy pages. All 184 claims retain source citations, with no empty
  claims lists and no `source: "not specified"` fallbacks. Every paper had an existing validated
  paper-level extraction in another concept YAML; each received fresh zero-shot-TTS-specific
  relevance, evidence-role, current-role, claim-relevance, caveat, and empty `method_family`
  judgments.
- The concept-scoped Phase 1 health check passed after each batch with 0 errors and 0 warnings.
  Phase 2 was not run. Corpus-wide `papers_not_in_any_yaml` remains 96.

### 2026-07-26 — zero-shot-tts Phase 1 batches 3–4 (40 → 80/203)

- Continued `zero-shot-tts` with exactly two sequential oldest-first Phase 1 batches. Batch 3
  integrated 20 papers from `2501.06282` through `2505.13000`; batch 4 integrated 20 papers from
  `2505.17589` through `2025.acl-industry.42`. The concept now has 80/203 entries, with 123
  remaining.
- Batch 3 preserved 93 claims from 9 structured and 11 legacy pages; batch 4 preserved 84 claims
  from 16 structured and 4 legacy pages. All 177 claims retain source citations, with no empty
  claims lists and no `source: "not specified"` fallbacks. Three pages without an existing entry
  in another claim YAML (`iclr-2025-hQvX9MBowC`, `2025.naacl-short.65`, `2507.15272`) were
  extracted directly from their structured claim blocks; all other entries reused validated
  paper-level extractions and received fresh zero-shot-TTS-specific judgments.
- The concept-scoped Phase 1 health check passed after each batch with 0 errors and 0 warnings.
  Phase 2 was not run. Corpus-wide `papers_not_in_any_yaml` decreased from 99 before batch 3 to
  96 after batch 4.

### 2026-07-26 — zero-shot-tts Phase 1 batches 1–2 (0 → 40/203)

- Started `zero-shot-tts` from scratch and ran exactly two sequential oldest-first Phase 1 batches.
  Live discovery found 203 Q3-and-earlier non-Tier-2 candidates, correcting the prior 204-paper
  estimate, and skipped 3 Tier 2 pages. Batch 1 integrated the first 20 papers from `1712.05884`
  through `2403.03100`; batch 2 integrated the next 20 from `2403.16973` through `2409.09098`.
  The concept now has 40/203 entries, with 163 remaining.
- The 40 paper-level extractions reused already validated entries from other concept YAMLs while
  applying fresh zero-shot-TTS-specific paper relevance, evidence roles, current roles, claim
  relevance, caveats, and empty Phase 1 `method_family` assignments. Claim counts were checked
  against each complete paper page before writing: batch 1 preserved 93 claims from 20 legacy
  pages; batch 2 preserved 94 claims from 2 structured and 18 legacy pages. All 187 claims retain
  source citations; no `source: "not specified"` fallback was needed.
- The concept-scoped Phase 1 health check passed after each batch with 0 errors and 0 warnings.
  Phase 2 was not run. Corpus-wide `papers_not_in_any_yaml` remains 99 because all 40 papers
  already participated in at least one of the eight previously integrated concepts.

### 2026-07-25 — repository checkpoint after instruction-conditioned-tts and prosody-control closure

- Saved the accumulated content-repository integration work in commit `1adc40f`
  (`Integrate three Q3 speech generation concepts`): the completed
  `autoregressive-codec-tts`, `instruction-conditioned-tts`, and `prosody-control` claim graphs,
  plus their reader-facing integration log entries.
- The checkpoint leaves eight Q3 concepts with Phase 1 + Phase 2 closed and 15 concepts not yet
  started. The Q3 coverage table remains at 874/2,234 concept-paper entries (39.1%), with
  `papers_not_in_any_yaml` at 99.
- The infrastructure checkpoint includes this session note, the current integration backlog
  status, and the post-Q3 recurring cross-concept claim-cluster reconciliation design item.

### 2026-07-25 — prosody-control Phase 2 synthesis run, concept fully closed

- Synthesized the 94-paper Phase 1 graph entirely from YAML without re-reading paper pages.
  Built **14 method families** with 179 reciprocal memberships. The largest are
  `explicit_acoustic_variance_control` (42 papers), `emotion_expressive_prosody_control` (28),
  `latent_reference_prosody_transfer` (23), and `disentangled_prosody_content_timbre` (17).
- The first pass left 23/94 papers without family membership. A consistency reconciliation added
  evidence-backed implicit-scale, language/domain, analysis/evaluation, and voice-quality
  families and corrected missed disentanglement, context, latent-control, and language-mediated
  assignments. Final coverage is **82/94**, with 12 legitimate low-relevance or contextual
  outliers rather than forced architectural assignments.
- Built **17 claim clusters**: 13 `strongly_supported` and 4 `emerging`. Strong convergence
  covers explicit pitch/energy/duration control, stochastic one-to-many modeling, prosody
  disentanglement, reference transfer and leakage, linguistic context, duration/alignment,
  local-control difficulty, SSL representation trade-offs, multimodal conditioning, hierarchical
  emotion, language-specific structure, shared speech–singing learning, and scale-driven implicit
  prosody.
- Added 7 reassessment items, including future subdivision watches for the two largest families
  and evidence watches for diversity–naturalness trade-offs, metric validity, SSL entanglement,
  structured control plans, and reference-prompt leakage. Added 6 open questions and 5 trend notes.
- Final `health_check.py --module integrate --concept prosody-control --phase 2` passed with
  **0 errors and 12 expected method-family coverage warnings** for the outliers.
  **The concept is fully closed for Q3 and earlier.**

### 2026-07-25 — prosody-control Phase 1 closed, batches 1–5 (0 → 94/94)

- Re-derived the Q3-and-earlier queue before each sequential invocation. Live discovery confirmed
  **94** eligible non-Tier-2 papers, matching the session-table estimate, and excluded one Tier 2
  page (`2312.05187`).
- **Batch 1:** 20 papers, `1609.03499` through `2025.naacl-long.484`; 89 claims
  (4 structured pages, 16 legacy). **Batch 2:** 20 papers, `2507.06235` through `2508.08399`;
  85 claims (11 structured, 9 legacy). **Batch 3:** 20 papers, `2508.09702` through
  `interspeech-2025-1020`; 87 claims (5 structured, 15 legacy).
- The three batches added **60 papers and 261 claims** (20 structured pages, 40 legacy).
  Every paper has claims, all claims have source citations, there are no duplicate IDs, and all
  `method_family` lists and top-level `claim_clusters` remain empty as required for Phase 1.
- **Batch 4:** 20 papers, `interspeech-2025-1098` through `2509.03940`; 84 claims
  (12 structured pages, 8 legacy). **Batch 5:** the final 14 papers, `2509.04072` through
  `2509.26514`; 59 claims (13 structured, 1 legacy).
- Across all five batches, Phase 1 produced **404 claims from 94 papers** (45 structured pages,
  49 legacy). Every paper has claims, all citations are specified, there are no duplicate or
  extraneous paper IDs, and all Phase 2 structures remain empty.
- Live discovery confirmed **0 unintegrated IDs**. Every batch's concept-scoped Phase 1 health
  check passed with **0 errors and 0 warnings**. Phase 1 completed here; Phase 2 was subsequently
  run and is recorded above.

### 2026-07-25 — instruction-conditioned-tts Phase 2 synthesis run, concept fully closed

- Synthesized the 44-paper Phase 1 graph entirely from the YAML, without re-reading paper pages.
  Built **8 method families** with 57 total memberships and reciprocal paper assignments.
  The largest are `direct_prompt_conditioned_speech_lm` (11 papers),
  `description_embedding_style_control` (9), `instruction_data_and_annotation_pipeline` (8),
  and `instruction_following_benchmark_and_audit` (8).
- Assigned 42/44 papers to at least one family. `2310.00704` and `2502.11946` remain deliberate
  outliers: both contribute contextual general-purpose audio-language-model evidence, but neither
  justifies forced membership in an instruction-conditioning method family.
- Built **15 claim clusters**: 8 `strongly_supported`, 6 `emerging`, and 1 `contested`.
  Strong convergence appears around multidimensional natural-language control, small-data
  instruction adaptation, instruction diversity, automatic supervision construction, structured
  intermediate control, the open-versus-closed capability gap, demographic bias, and bounded
  benefits from situated context.
- The contested cluster `automatic_judges_do_not_fully_replace_human_evaluation` preserves both
  sides of the evidence: several studies report strong judge-human agreement, while others expose
  blind spots in fine-grained alignment, naturalness, and atypical-speech evaluation.
- Added 5 reassessment items, 5 cross-cutting open questions, and 4 temporal trend notes. Final
  `health_check.py --module integrate --concept instruction-conditioned-tts --phase 2` passed
  with **0 errors and 2 expected method-family coverage warnings** for the two outliers.
  **The concept is fully closed for Q3 and earlier.**

### 2026-07-25 — instruction-conditioned-tts Phase 1 closed, batches 1–3 (0 → 44/44)

- Re-derived the Q3-and-earlier queue before each sequential invocation. Live YAML-frontmatter
  discovery found **44** eligible non-Tier-2 papers rather than the session table's prior estimate
  of 45; 5 Tier 2 pages were excluded by protocol.
- **Batch 1:** 20 papers, `2305.11000` through `2025.acl-long.681`; 90 claims
  (6 structured pages, 14 legacy). **Batch 2:** 20 papers, `2025.acl-long.911` through
  `2505.17093`; 85 claims (10 structured, 10 legacy). **Batch 3:** the final 4 papers
  (`2509.15845`, `2509.17516`, `2509.24570`, `2509.26514`); 17 claims, all structured.
- Phase 1 produced **192 claims across 44 papers** (20 structured pages, 24 legacy). Every paper
  has claims; all citations are specified; there are no duplicate paper IDs; all per-paper
  `method_family` lists and top-level `claim_clusters` remain empty as required before Phase 2.
- Validation caught and corrected an initial empty-list YAML skeleton formatting error after
  batch 1 and four punctuation-obscured source citations on `2509.24570`. The final
  `health_check.py --module integrate --concept instruction-conditioned-tts --phase 1` passed
  with **0 errors and 0 warnings**; live discovery found **0 unintegrated IDs**.
- Phase 1 completed here; Phase 2 was subsequently run and is recorded above.

### 2026-07-25 — autoregressive-codec-tts Phase 2 synthesis run, concept fully closed

- Synthesized the 165-paper Phase 1 evidence graph without re-reading paper pages. Assigned
  13 method families with 264 total memberships; every paper has at least one reciprocal family
  assignment, including `interspeech-2025-1538`, which was retained as a low-relevance
  speech-text autoregressive VC variant and reassessed from `active_evidence` to `minor`.
- Largest families are `hybrid_ar_token_continuous_renderer` (52 papers),
  `semantic_acoustic_token_cascade` (43), `unified_speech_text_language_model` (39),
  `codec_tokenizer_infrastructure` (36), and `scaled_general_ar_codec_tts` (24).
  The first two were explicitly queued for future sub-splitting rather than fragmented without
  a stable evidentiary boundary.
- Built 17 claim clusters: 15 `strongly_supported`, 1 `contested`, and 1 `emerging`.
  The contested cluster, `parallel_and_masked_models_challenge_full_autoregression`, was
  corrected during polarity audit: 4 papers support quality-preserving parallel/masked decoding,
  3 provide contrary latency/quality evidence, and 1 refines the trade-off. The emerging
  `continuous_representations_avoid_quantization_tradeoffs` cluster has only 2 supporting papers.
- Added 5 reassessment items: the contested causal-versus-parallel comparison, the thin
  continuous-token claim, the broad general autoregressive family, and the two largest
  mega-families. Added 5 open questions and 5 temporal trend notes.
- Final `health_check.py --module integrate --concept autoregressive-codec-tts --phase 2`
  passed with **0 errors and 0 warnings**. **The concept is fully closed for Q3 and earlier.**

### 2026-07-25 — autoregressive-codec-tts Phase 1 closed, batches 7–9 (120 → 165/165)

- Ran the final three Phase 1 invocations sequentially, independently re-deriving the queue and
  running the full concept-scoped health check after each.
- **Batch 7:** integrated 20 papers from `interspeech-2025-1993` through `2509.09174`;
  90 claims across 7 structured-format and 13 legacy-format pages. Validation passed with
  0 errors and 0 warnings; 25 remained.
- **Batch 8:** integrated 20 papers from `2509.09550` through `2509.21968`;
  89 claims across 19 structured-format and 1 legacy-format page. Validation passed with
  0 errors and 0 warnings; 5 remained.
- **Batch 9:** integrated the final 5 papers (`2509.22062`, `2509.24570`, `2509.24650`,
  `2509.25131`, `2509.26514`), extracting 21 claims from 5 structured-format pages.
  Four Evidence citations on `2509.24570` ended with punctuation after the italic citation
  marker and initially parsed as unspecified; all four were recovered from the page and corrected
  before final validation.
- Across the three batches: **45 papers, 200 claims, 31 structured pages, 14 legacy pages,
  0 empty claim lists, and 0 unspecified sources**. Live discovery confirmed 165 Q3-scoped
  non-Tier-2 candidates and zero unintegrated IDs. The final Phase 1 health check passed with
  0 errors and 0 warnings. `papers_not_in_any_yaml` fell from 122 to 112.
  **Phase 1 is closed at 165/165; Phase 2 synthesis remains pending.**

### 2026-07-25 — autoregressive-codec-tts Phase 1 batches 5–6 (80 → 120/165)

- Ran two complete 20-paper invocations sequentially, with independent oldest-first discovery
  and a full concept-scoped Phase 1 health check after each batch.
- **Batch 5:** integrated 20 papers from `2025.acl-long.1498` through `2508.06262`;
  92 claims across 5 structured-format and 15 legacy-format pages, all with source citations.
  Validation passed with 0 errors and 0 warnings; 65 remained.
- **Batch 6:** re-derived the queue at 100/165, then integrated 20 papers from `2508.08715`
  through `interspeech-2025-1776`; 85 claims across 5 structured-format and 15 legacy-format
  pages, all with source citations. Final validation passed with 0 errors and 0 warnings.
- Across both batches: **40 papers, 177 claims, 10 structured pages, 30 legacy pages, 0 empty
  claim lists, and 0 unspecified sources**. No Phase 2 synthesis was performed.
  `papers_not_in_any_yaml` fell from 136 to 122. **45 in-scope papers remain.**

### 2026-07-25 — autoregressive-codec-tts Phase 1 batches 3–4 (40 → 80/165)

- Ran two complete 20-paper invocations sequentially, re-deriving the oldest-first queue and
  running the full concept-scoped Phase 1 health check between them.
- **Batch 3:** integrated the next 20 papers from `2410.17799` through
  `iclr-2025-cuFzE8Jlvb`; 96 claims across 2 structured-format and 18 legacy-format pages,
  all with source citations. Validation passed with 0 errors and 0 warnings; 105 remained.
- **Batch 4:** independently re-derived the queue at 60/165, then integrated the next 20 from
  `iclr-2025-dGSOn7sdWg` through `2025.acl-long.1043`; 94 claims across 12 structured-format
  and 8 legacy-format pages. One structured Evidence citation on `2025.naacl-demo.12` ended
  with punctuation after the italic citation and initially parsed as unspecified; it was
  corrected to `§3.3` before final validation. Final health check passed with 0 errors and
  0 warnings.
- Across both batches: **40 papers, 190 claims, 14 structured pages, 26 legacy pages, 0 empty
  claim lists, and 0 unspecified sources**. No Phase 2 synthesis was performed.
  `papers_not_in_any_yaml` fell from 145 to 136. **85 in-scope papers remain.**

### 2026-07-25 — autoregressive-codec-tts Phase 1 batch 2 (20 → 40/165)

- Re-derived the queue before writing: 165 Q3-scoped non-Tier-2 candidates, 20 already in YAML,
  145 queued, and 9 Tier 2 pages skipped. Processed the next 20 oldest:
  `2402.13236`, `2403.16973`, `2404.03204`, `2406.00654`, `2406.02430`, `2406.04904`,
  `2406.05370`, `2406.07855`, `2406.18009`, `2407.05407`, `2407.08551`, `2408.02622`,
  `2408.16532`, `2408.16725`, `2409.00750`, `2409.03283`, `2409.05377`, `2410.00037`,
  `2410.03751`, `2410.11190`.
- All 20 pages use the legacy bare-claims format. Extracted all 93 claims with real source
  citations; no empty-claims pages and no `source: "not specified"` fallbacks. Phase 1 left
  `method_family: []` throughout and did not synthesize clusters.
- QC also repaired sentence-boundary truncation in several batch-1 evidence fields caused by
  decimal values following `vs.` and normalized the affected batch-2 evidence sentences before
  validation. The concept-scoped Phase 1 health check passed with 0 errors and 0 warnings.
  Corpus-wide `papers_not_in_any_yaml` fell from 149 to 145. **125 in-scope papers remain.**

### 2026-07-25 — autoregressive-codec-tts Phase 1 batch 1 (0 → 20/165)

- Re-derived the Q3 scope from live paper frontmatter and metadata before writing:
  `published_date < 2025-10-01`, `related_concepts` containing
  `autoregressive-codec-tts`, and `ingest_tier != 2`. This produced 165 in-scope candidates,
  one fewer than the 166 recorded in the 2026-07-22 table; 9 Tier 2 pages were skipped.
- Created `wiki/_claims/autoregressive-codec-tts.yaml` and integrated the 20 oldest candidates,
  from `1609.03499` (WaveNet, 2016-09-12) through `2402.08093` (BASE TTS, 2024-02-12):
  `1609.03499`, `1703.10135`, `2106.15561`, `2209.03143`, `2210.13438`, `2301.02111`,
  `2301.11325`, `2303.03926`, `2305.02765`, `2305.07243`, `2305.09636`, `2305.11000`,
  `2306.00814`, `2306.12925`, `2308.16692`, `2310.00704`, `2401.07333`, `2402.01912`,
  `2402.05755`, `2402.08093`.
- All 20 pages use the legacy bare-claims format. Extracted all 93 claims and retained a real
  source citation for every claim, including the two appendix-form citations on
  `2308.16692`. Phase 1 left `method_family: []` throughout and did not synthesize clusters.
- Inline validation confirmed 20 unique paper IDs, `paper_count == len(papers)`, 93 claims, and
  no null sources. The concept-scoped Phase 1 health check passed with 0 errors and 0 warnings.
  Corpus-wide `papers_not_in_any_yaml` fell from 157 to 149 because 8 of the 20 papers had not
  previously appeared in another concept YAML. **145 in-scope papers remain.**

### 2026-07-22 — disentanglement Phase 2 synthesis run, concept fully closed

- **First-ever Phase 2 synthesis run for `disentanglement`**, against the full 100-paper set
  (larger than flow-matching's 97 and rlhf-speech's 29, smaller than evaluation-metrics' 285 and
  speech-to-speech's 60). Used a metadata-first + relevance-filtered-claims condensation strategy
  rather than reading the full ~4900-line YAML at once, per the evaluation-metrics Phase 2
  precedent.
- **Session was interrupted mid-task by an API session limit**, cut off right after the agent said
  "Now I'll build the complete Phase 2 synthesis content programmatically to ensure correctness,
  then validate before writing." Per the established recovery protocol, file state was checked
  directly before resuming rather than trusting the interrupted agent: `paper_count`/`len(papers)`
  were intact at 100, 77/100 papers already had a non-empty `method_family` assigned across 10
  family labels, but the top-level `claim_clusters`/`method_families`/`reassessment_queue` lists
  were still empty and no `log.md` entry existed yet — a genuine partial write, not a clean
  pre-write state. **Process error caught and corrected during this recovery**: the first resume
  attempt mistakenly launched a brand-new `Agent` call (in an isolated git worktree) instead of
  using `SendMessage` to resume the original interrupted agent by its agent ID — this would have
  lost all prior context and, worse, isolated the write from the actual content repo. Caught before
  any work was done in the worktree; that agent was stopped cleanly via `TaskStop` and the correct
  agent was resumed via `SendMessage` with a full brief on the file state. See
  [[feedback_session_limit_interruption]] for the update to this recovery protocol.
- **Course correction during the resumed run**: the initial per-paper classification pass had left
  23/100 papers (23%) with an empty `method_family`, a noticeably higher outlier rate than the
  other closed concepts (5/97, 4/29, ~14/285). The coordinator flagged this before accepting the
  result (same class of check as the evaluation-metrics 226/285 false start); the resumed agent
  reconciled 7 of those 23 against the same evidentiary standard already applied to similar
  included papers (e.g. FreeCodec's self-reported incomplete separation was already included in
  the RVQ-distillation family, so DiffStyleTTS's self-reported prosody/timbre non-separation,
  VibeVoice's and PerformSinger's inherited-not-novel codec splits, and ChiReSSD's/Conan's
  inherited-mechanism applications were brought in on the same basis), landing at a final 16/100
  (16%) legitimate-outlier rate.
- **10 method_families**: `explicit_multiencoder_factorization` (30, largest/most heterogeneous,
  flagged as a reassessment_queue mega-family watch), `rvq_semantic_acoustic_distillation` (19),
  `data_training_recipe_disentanglement` (11), `adversarial_grl_disentanglement` (7),
  `asr_text_alignment_disentanglement` (7), `discrete_bottleneck_disentanglement` (7),
  `signal_level_prosody_decomposition` (6), `orthogonality_constraint_disentanglement` (5),
  `ssl_statistical_normalization_disentanglement` (4), `mutual_information_minimization` (2, thin,
  flagged). 14 papers hold dual family membership.
- **17 claim_clusters: 12 strongly_supported, 3 emerging, 2 contested.** Headline
  strongly_supported clusters: `disentanglement_reconstruction_fidelity_tradeoff` (10 supporting,
  incorporating DeCodec's explicit reconstruction-quality trade-off),
  `explicit_disentanglement_enables_independent_multiattribute_control` (12),
  `emotion_speaker_disentanglement_enables_crossspeaker_transfer` (7). The 2 contested clusters
  directly surface complicating evidence flagged during Phase 1:
  `grl_disentanglement_leakage_vs_quality_tradeoff` (GRL reduces leakage per 5 supporting papers,
  but PeriodCodec reports a GRL-induced MOS regression — 3.28→2.44 — and DiEmoTTS directly critiques
  GRL/VQ-based disentanglement) and `disentanglement_oriented_codecs_fail_on_pitch`
  (`interspeech-2025-0115`/AnCoGen's finding that SpeechTokenizer- and Mimi-style codecs fail to
  cleanly separate pitch, contradicted by 3 papers using dedicated signal-level F0 mechanisms rather
  than generic representation-level disentanglement, with FreeCodec's self-reported incomplete
  t-SNE separation as a refining data point). Independently spot-checked the PeriodCodec claim
  numbers against its source page (`interspeech-2025-0347`): MOS 3.28→2.44 and 3.55→3.33 both
  matched exactly.
- **7 reassessment_queue items**: 2 method_family threshold-watches (the mega-family risk;
  `mutual_information_minimization`'s 2-paper thinness), 3 contested/thin claim_status watches (the
  2 contested clusters above, plus a 3-paper emerging claim on objective metrics not predicting
  subjective disentanglement quality), 1 fast-emerging 3-paper claim
  (`prompt_based_conditioning_causes_attribute_leakage`), 1 paper_role watch (Vevo2's un-ablated
  bottleneck tokenizer).
- Independently re-verified end-to-end: `paper_count`/`len(papers)` both 100, 0 duplicate IDs, all
  `id`/`entry_date`/`last_reviewed` fields string-typed, every `claim_cluster` and `method_family`
  paper reference resolves to a real entry in `papers:`, cluster status counts (12/3/2) matched the
  agent's report exactly, the 16 empty-`method_family` IDs matched exactly between the health check
  output and the agent's report. `health_check.py --module integrate --concept disentanglement`:
  0 errors, 16 warnings (all `method_family_coverage`, all documented legitimate outliers).
- `disentanglement` is now the fifth concept fully closed for Q3-and-earlier Phase 1 + Phase 2
  (after flow-matching, speech-to-speech, rlhf-speech, evaluation-metrics).
- Committed to the content repo (`_claims/disentanglement.yaml` new file + `log.md`, one commit,
  `f01eff1`) alongside a fix for a pre-existing, unrelated bare `2026-07-19` log.md section header
  (confirmed via `git diff` to predate this session, not introduced by it). Pushed to `origin/main`.

### 2026-07-22 — disentanglement Phase 1 closed from scratch (batches 1-5, 100/100)

- **First-ever integration pass for `disentanglement`**, new `wiki/_claims/disentanglement.yaml`
  created. 110 total candidates found (papers with `disentanglement` in `related_concepts`), 10
  Q4-2025-or-later excluded per scope, 0 Tier 2 stubs, leaving 100 in-scope Q3-and-earlier
  candidates — all 100 integrated across 5 batches, oldest-first, 0 genuine scope-mismatch
  exclusions.
- Batch 1 (20, `2010.05646` HiFi-GAN → `2505.07916` MiniMax-Speech): first-ever batch, 18/20 legacy
  claims format. Batch 2 (20, `2506.10274` → `interspeech-2025-0115`): 6/20 structured format;
  surfaced `interspeech-2025-0115`'s finding that SpeechTokenizer/Mimi fail to cleanly separate
  pitch. Batch 3 (20, `interspeech-2025-0196` → `-1106`): 8/20 structured format; surfaced
  PeriodCodec's GRL-induced MOS regression and LinearVC's clean SVD evidence for orthogonal
  content-speaker subspaces (independently spot-checked against source pages, both exact matches).
  Batch 4 (20, `interspeech-2025-1115` → `2508.16332`): 14/20 structured format; independently
  spot-checked FreeCodec (`interspeech-2025-1440`) against its source page, exact match on all 4
  claims. Batch 5 / final (20, `2508.17031` → `2509.24650`): confirmed exactly 20 remaining
  in-scope candidates going in (no scope miscount), closing Phase 1 at 100/100; independently
  spot-checked DeCodec (`2509.09201`) against its source page, exact match on all 5 claims.
- **One session-limit interruption during batch 4**: cut off right after the agent's last message
  ("Now I'll construct the 20 YAML entries and insert them into the file") — confirmed via direct
  file check to be a clean pre-write state (`paper_count`/`len(papers)` unchanged at 60, no batch 4
  `log.md` entry). Restarted fresh rather than resuming, since no drafting had occurred yet to
  preserve.
- **Two log-insertion issues surfaced**: batch 5's agent introduced and self-corrected a header
  corruption mid-write (recurrence of the known log-insertion bug class, see
  [[feedback_log_insertion_bug]]) before it was ever visible outside the write; independently
  confirmed all `## YYYY-MM-DD` headers intact afterward. Separately, a pre-existing bare
  `2026-07-19` header (missing its `## ` prefix, predating this session per `git diff` against the
  last commit) was manually fixed as its own small edit at the user's request.
- Independently re-verified every batch the same way as prior concepts (never trusting an agent's
  closing summary uncontested, see [[feedback_agent_selfreport_unreliable]]): `paper_count`/
  `len(papers)` match after each batch (20/40/60/80/100), 0 duplicate IDs throughout, all
  `id`/`entry_date` fields string-typed, `health_check.py --module integrate --concept
  disentanglement --phase 1` clean (0 errors, 0 warnings) after every batch, `papers_not_in_any_yaml`
  dropped 205 → 198 → 188 → 180 → 169 → 157 across the 5 batches, and one claim spot-checked per
  batch against its actual source page (SpeechTokenizer, `interspeech-2025-0115` AnCoGen, LinearVC,
  FreeCodec, DeCodec) — all traced cleanly with correct section citations.

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
| disentanglement | `grl_disentanglement_leakage_vs_quality_tradeoff` (cluster) | contested: GRL-based adversarial disentanglement reduces leakage per 5 supporting papers, but PeriodCodec (`interspeech-2025-0347`) reports a GRL-induced MOS regression (3.28→2.44) and DiEmoTTS (`interspeech-2025-1394`) directly critiques GRL/VQ-based disentanglement as introducing a separation-vs-quality tension |
| disentanglement | `disentanglement_oriented_codecs_fail_on_pitch` (cluster) | contested: AnCoGen (`interspeech-2025-0115`) finds SpeechTokenizer- and Mimi-style disentanglement-oriented codecs fail to cleanly separate pitch, contradicted by 3 papers using dedicated signal-level F0 mechanisms rather than generic representation-level disentanglement — may be two different mechanisms rather than a direct conflict |
| disentanglement | `explicit_multiencoder_factorization` (family, 30 papers) | intentionally broad mega-family spanning many distinct multi-encoder disentanglement architectures; flagged as a future sub-splitting candidate |
| disentanglement | `mutual_information_minimization` (family) | thin at 2 papers, watch for growth |
| disentanglement | 16 empty-`method_family` papers | legitimate outliers: evaluation/diagnostic-side contributions, out-of-scope modality, or tangential/analogical use of disentanglement (`2010.05646` HiFi-GAN, `2304.09116` NaturalSpeech 2, `2508.11224`, `interspeech-2025-0196/-0455/-0575/-0656/-0723/-0816`, `2508.15565`, `2508.15931`, `2508.16188`, `2508.17031`, `2509.00503`, `2509.18060`, `2505.10599`) |
