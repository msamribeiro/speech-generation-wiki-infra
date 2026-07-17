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
cd /Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-infra

# Corpus-wide integration coverage per concept (papers referencing each concept vs. papers
# actually integrated into that concept's YAML)
.venv/bin/python scripts/corpus_summary.py --group-before 2025-07

# Structural validation + the single most useful backlog stat: papers_not_in_any_yaml
# (ingested, non-Tier-2 papers with zero concept-YAML entries anywhere)
.venv/bin/python scripts/health_check.py --module integrate --wiki-dir /Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content -v
```

**State as of 2026-07-18** (re-run the commands above before resuming — this will be stale):

| Concept | Papers referencing it (all time) | Integrated | % |
|---|---|---|---|
| flow-matching | 112 | 34 | 30% |
| zero-shot-tts | 230 | 0 | 0% |
| evaluation-metrics | 318 | 0 | 0% |
| subjective-evaluation | 202 | 0 | 0% |
| neural-codec | 218 | 0 | 0% |
| autoregressive-codec-tts | 194 | 0 | 0% |
| spoken-language-model | 176 | 0 | 0% |
| self-supervised-speech | 159 | 0 | 0% |
| disentanglement | 104 | 0 | 0% |
| prosody-control | 103 | 0 | 0% |
| multilingual-tts | 102 | 0 | 0% |
| voice-conversion | 94 | 0 | 0% |
| emotion-synthesis | 85 | 0 | 0% |
| speaker-adaptation | 84 | 0 | 0% |
| speech-to-speech | 81 | 0 | 0% |
| streaming-tts | 70 | 0 | 0% |
| gan-vocoder | 64 | 0 | 0% |
| instruction-conditioned-tts | 54 | 0 | 0% |
| diffusion-tts | 53 | 0 | 0% |
| rlhf-speech | 40 | 0 | 0% |
| transformer-enc-dec-tts | 32 | 0 | 0% |
| singing | 10 | 0 | 0% |
| fine-tuning | 1 | 0 | 0% |
| **TOTAL** | **2590** | **34** | **1%** |

`papers_not_in_any_yaml` (corpus-wide, all quarters): **524**. Scoped to Q3-2025-and-earlier only
(the actual target of this task, excluding Tier 2 stubs): **463** as of 2026-07-18.

**Only `flow-matching` has started** — 34 of 112 papers integrated (round 1 of a production run
begun 2026-07-15, prototype-tested 2026-06-24 on an initial 14 papers). All other 22 concepts
have **no `wiki/_claims/{slug}.yaml` file at all yet** — every paper touching them is unintegrated.

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

3. **3 papers in the existing `flow-matching.yaml` have an empty `method_family` after Phase 2**
   synthesis (a warning, not an error, from the health check): `2106.15561`,
   `2025.coling-main.518`, `iclr-2025-uxDFlPGRLX`. Worth a look when next touching flow-matching,
   not urgent.

4. `flow-matching.yaml` is already committed and pushed to `main` in the content repo (commits
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

### The two-phase model (full detail: `.claude/agents/speech-generation-integration-agent.md`,
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
.venv/bin/python3 scripts/health_check.py --module integrate --concept {slug} --wiki-dir /Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content -v
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

_(none yet — bootstrapped 2026-07-18)_

---

## Manual Verification Queue

Concept/paper entries worth a second look, flagged during integration passes (health-check
warnings, ambiguous claim roles, or judgment calls noted by the agent).

| Concept | Paper ID | Note |
|---|---|---|
| flow-matching | `2106.15561` | empty `method_family` after Phase 2 (pre-existing, session 2026-07-15) |
| flow-matching | `2025.coling-main.518` | empty `method_family` after Phase 2 (pre-existing, session 2026-07-15) |
| flow-matching | `iclr-2025-uxDFlPGRLX` | empty `method_family` after Phase 2 (pre-existing, session 2026-07-15) |
