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

**State as of 2026-07-20** (re-run the commands above before resuming — this will be stale). This
table is now **Q3-scoped directly** (`published_date < 2025-10-01`, non-Tier-2, counted from paper
frontmatter, not the corpus-wide `corpus_summary.py` output) — see the note below on why the
corpus-wide `Covers`-style column was dropped:

| Concept | Q3-scoped papers referencing it | Integrated | % |
|---|---|---|---|
| evaluation-metrics | 286 | 0 | 0% |
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
| rlhf-speech | 29 | 0 | 0% |
| transformer-enc-dec-tts | 28 | 0 | 0% |
| singing | 10 | 0 | 0% |
| fine-tuning | 1 | 0 | 0% |
| **TOTAL** | **2236** | **157** | **7.0%** |

`papers_not_in_any_yaml` (corpus-wide, all quarters, via `health_check.py`): **429** as of
2026-07-20 (down from 548 on 2026-07-19, reflecting the 157 papers integrated this session across
both concepts).

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

**`flow-matching` and `speech-to-speech` are now fully closed for Q3-and-earlier Phase 1 + Phase
2** (97/97 and 60/63 — the 3-paper gap on speech-to-speech is intentional: `2025.acl-long.388`
DiVA, `interspeech-2025-2660` VAP, and `2509.23938` Easy Turn were each evaluated and correctly
excluded for having no speech-generation stage of their own, despite carrying the tag). All other
21 concepts have **no `wiki/_claims/{slug}.yaml` file at all yet**.

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
