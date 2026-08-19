# Cross-Concept Synthesis and Temporal Reporting Program

**Started:** 2026-08-02
**Status:** Phase 3 complete; reconciliation infrastructure is next
**Evidence scope:** Q3 2025 and earlier (`published_date <= 2025-09-30`)
**Assessment mode:** Retrospective; the assessment date is the date each reconciliation or
snapshot is completed, not the evidence cutoff

This is the authoritative, resumable implementation note for the first cross-concept
reconciliation and temporal-reporting rollout. Update **Resume Here** and append a dated entry to
**Session Log** at every safe stopping point. Infrastructure and content changes are committed
separately at phase boundaries. No remote push is part of this program unless separately requested.

When the program is complete, archive this file as
`docs/records/{completion-date}-cross-concept-synthesis-sessions.md`.

---

## Goal

Extend the content pipeline from:

```text
Ingest -> Integrate -> Render
```

to:

```text
Ingest -> Integrate -> Reconcile -> Render
                              \-> Snapshot -> Report
```

The reconciliation layer connects semantically overlapping concept-local claim clusters without
deleting or flattening them. Existing paper pages remain authoritative for paper-level evidence;
concept YAMLs remain authoritative for local wording, evidence, confidence, status, caveats, and
method families. The reviewed cross-concept registry becomes authoritative only for relationships
and broader claims.

Rendering remains a current-state synthesis. Reports are explicitly bounded by publication date,
venue, or comparisons between immutable snapshots.

The first rollout will:

1. cover all 23 Q3-integrated concepts and their 406 claim clusters;
2. preserve all existing concept-local clusters;
3. produce a retrospectively assessed Q3 snapshot;
4. regenerate the field overview from all 23 claim graphs plus reviewed relationships; and
5. publish a Q3 2025 quarterly report.

Trend and venue-report workflows will be designed and validated, but no initial trend or venue
report is required.

## Boundaries and Non-Goals

- Do not change source PDFs or substantive metadata content.
- Do not fold Q4 2025 papers into the Q3 evidence set. Q4 papers may exist in the wiki, but report
  inclusion is determined only by canonical `published_date`.
- Do not overload ordinary Phase 2 integration with corpus-wide reconciliation.
- Do not make reports part of ingest.
- Do not allow similarity tooling to mutate accepted relationships.
- Do not delete a concept-local cluster merely because a broader or equivalent claim is accepted.
- Do not use concept Overview pages as evidence authority. They are reader-facing navigation and
  editorial inputs.
- Keep venue reports on demand and prohibit thin paper-list pages.

## Repositories and Ownership

| Concern | Repository | Owned artifacts |
|---|---|---|
| Schemas, designs, agents, checks, migration and report tooling | Infrastructure | `docs/`, `.agents/`, `.claude/`, `scripts/`, tests |
| Local claim graphs and reviewed reconciliation state | Content | `_claims/*.yaml`, `_claims/_reconciliation/` |
| Current field synthesis and bounded reports | Content | `overview.md`, `reports/`, reader-facing indexes |
| Operation history | Content | `log.md` |

The standard wiki resolver in this infrastructure worktree currently points to a missing sibling
clone. Until that setup is repaired, use the explicit content checkout shown in **Resume Here** or
set `SPEECH_WIKI_CONTENT_DIR` to it. Do not write to the `wiki/` submodule.

---

## Reviewed Baseline

Baseline verified on 2026-08-02 against the `work/integrate` content checkout.

| Measure | Live value |
|---|---:|
| Concept YAMLs | 23 |
| Concept paper entries | 2,226 |
| Claim clusters | 406 |
| Strongly supported clusters | 280 |
| Emerging clusters | 112 |
| Contested clusters | 14 |
| Method families | 173 |
| Production concept Overview pages | 21/23 |
| Production concept In Depth pages | 21/23 |
| Current field overview coverage | 5/23 concepts |

The integrate health module passes with 0 errors and 241 warnings. The warnings are primarily
intentional or unresolved empty method-family assignments; they are not reconciliation failures.
The corpus-wide `papers_not_in_any_yaml` value is 190 because Q4 ingestion has advanced beyond the
Q3 claim graphs. It is not a blocker for a Q3-bounded reconciliation.

The render health module passes with 0 errors and 7 warnings. `singing` and `fine-tuning` still
have placeholders rather than full Overview/In Depth pairs; the other warnings are minor word-count
shortfalls. Reconciliation and field synthesis read claim YAMLs directly, so the two missing page
pairs do not reduce the 23-concept audit scope.

`overview.md` is not current: it intentionally represents only `flow-matching`,
`speech-to-speech`, `evaluation-metrics`, `rlhf-speech`, and `disentanglement`. It must be replaced
by an all-concept field view during this program.

### Concrete schema gap found during bootstrap

Cluster IDs are currently checked only within a concept file. Of 406 clusters, 405 IDs are unique
globally. `semantic_acoustic_token_tradeoff` appears independently in:

- `speech-to-speech#semantic_acoustic_token_tradeoff`
- `spoken-language-model#semantic_acoustic_token_tradeoff`

The claims express closely overlapping semantic-versus-acoustic token tradeoffs. This is the first
mandatory review candidate and demonstrates why all registry references must be qualified by both
concept and cluster ID. It is not automatically accepted as equivalent.

An advisory lexical scan also surfaced plausible high-priority pairs involving automatic metrics,
semantic/acoustic hierarchies, speech-text interleaving, unseen-speaker generalization,
disentanglement for control, and full-duplex responsiveness. These findings seed candidate review;
they are not reviewed decisions.

---

## Design Decisions

### 1. Preserve concept-local claims

Keep all concept YAMLs at `_claims/{concept}.yaml`. Local clusters retain their current claim text,
status, confidence, evidence lists, caveats, and review date. Reconciliation adds a separate
reviewed layer and does not rewrite local epistemic judgments to manufacture consistency.

### 2. Use a separate reconciliation registry

Create:

```text
_claims/_reconciliation/
  registry.yaml
  runs/2025-Q3.yaml
  snapshots/2025-Q3.yaml
```

`registry.yaml` is authoritative for accepted cross-concept relationships and broader claims.
`runs/2025-Q3.yaml` preserves every emitted candidate and its `accepted`, `rejected`, or `deferred`
disposition with rationale. `snapshots/2025-Q3.yaml` freezes the time-bounded assessed state.

The subdirectory is intentional: the current integrate checker scans `_claims/*.yaml`, so these
artifacts do not masquerade as concept YAMLs while dedicated reconciliation validation is added.

### 3. Use qualified cluster references

All cross-concept references use:

```text
{concept-slug}#{cluster-id}
```

Never infer a concept from a bare cluster ID, even if the ID is currently globally unique.

### 4. Relationship vocabulary

Supported reviewed relationships:

- `equivalent` — same proposition at materially the same scope and polarity;
- `specialization` — member is a narrower scoped instance of a broader proposition;
- `supports` — one claim supplies compatible evidence or mechanism for another without identity;
- `refines` — one claim adds a boundary, condition, or more precise formulation;
- `contradicts` — claims make incompatible assessments at overlapping scope;
- `tradeoff` — claims capture coupled gains and costs that should be synthesized together; and
- `related` — meaningful overlap exists, but a stronger relationship is not justified.

Do not accept `equivalent` when thresholds, polarity, population, task, metric, or evidence scope
differ materially. Prefer `specialization`, `refines`, `contradicts`, or `related`. A broader claim
requires meaningful membership from at least two concepts.

Each broader claim records:

- a stable ID and proposition;
- current status and confidence;
- qualified member references and their relationships;
- caveats and review rationale;
- evidence cutoff and assessment date; and
- unique supporting, contradicting, and refining paper IDs derived from members.

Evidence counts deduplicate paper IDs across concept memberships. They never sum the same paper
twice merely because it appears in multiple local graphs.

### 5. Temporal semantics

Add required `published_date` to every `papers:` entry in every concept YAML. Source it from the
canonical paper frontmatter or metadata and fail on missing, conflicting, or invalid dates. Never
infer a date from an arXiv ID, paper ID, integration date, or file timestamp.

Existing temporal fields retain their meanings:

- `published_date` — publication eligibility and report-window membership;
- `entry_date` — when a concept paper entry was written or force-rewritten;
- `last_reviewed` — when a local cluster assessment was reviewed; and
- `source_digest_date` — which claim-YAML state a rendered page used.

Q3 boundaries:

- evidence cutoff: `2025-09-30`;
- activity window: `2025-07-01` through `2025-09-30` inclusive;
- pre-quarter baseline: eligible evidence through `2025-06-30`; and
- snapshot `assessment_as_of`: actual reconciliation completion date.

The Q3 snapshot and report must say **retrospective assessment**. They do not claim to reproduce
what reviewers believed on 2025-09-30.

Snapshots record included paper IDs, concept and registry digests, broader-claim assessments,
reconciliation-run reference, cutoff, and assessment date. Published snapshots are immutable;
corrections create a superseding snapshot with an explicit pointer and reason.

### 6. Current-state rendering versus reports

The field overview derives evidence from concept YAMLs and the reviewed reconciliation registry.
Concept Overviews provide terminology and navigation but are not the evidentiary source.

The report workflow has three targets:

- **Quarterly:** publication-window activity and changes in the assessed knowledge state;
- **Trend:** comparison across two or more immutable snapshots; and
- **Venue:** one canonical venue and time range, evaluated against the wider-field baseline.

The field overview is a current-state page. A quarterly report is an immutable bounded account.
Neither substitutes for the other.

---

## Candidate Audit Policy

Implement a deterministic, read-only candidate generator over clusters from different concepts.
Rank using normalized claim-text similarity, shared-paper overlap, status/polarity compatibility,
and shared technical vocabulary. Every emitted score must be accompanied by its component signals
so reviewers can understand why the pair was proposed.

Initial policy:

- exclude same-concept pairs;
- include the ten highest-scoring cross-concept neighbors per cluster;
- include any pair with at least two shared supporting papers;
- deduplicate symmetric pairs with stable qualified-reference ordering;
- cap the initial review queue at the highest-ranked 500 pairs; and
- treat all output as advisory.

Before freezing the 500-pair policy, record queue-size and score-distribution diagnostics. If the
cap excludes any pair with at least two shared supporting papers, shared-evidence candidates take
priority over text-only candidates. Candidate generation must be deterministic for identical
inputs and configuration.

Review in themed batches:

1. evaluation and subjective judgment;
2. efficiency, latency, and decoding;
3. speaker identity, intelligibility, and adaptation;
4. prosody, emotion, style, and controllability;
5. scaling, diversity, robustness, and generalization;
6. codecs, token hierarchies, and language modeling;
7. streaming, duplex interaction, and spoken agents; and
8. post-training, preference optimization, and rewards.

The evaluation batch is the pilot. Validate registry semantics, health checks, and renderer
deduplication on that batch before broadening the review.

---

## Implementation Checklist

### Phase 1 — Bootstrap the session

- [x] Create this root session note from the reviewed program plan.
- [x] Inspect infrastructure and content working trees.
- [x] Record live baseline counts, health results, and repository commits.
- [x] Correct the baseline distinction: 23 integrated concepts, 21 fully rendered concepts, and a
      field overview covering only five concepts.
- [x] Commit the session note independently after authorization *(completed 2026-08-13)*.

**Gate:** The session note is sufficient for a fresh agent to resume without chat history.

### Phase 2 — Designs, schemas, and workflow contracts

- [x] Add focused cross-concept reconciliation and report design documents.
- [x] Extend the claim schema with `published_date`.
- [x] Define schemas for registry, run records, immutable snapshots, and supersession.
- [x] Update pipeline and stage-ownership documentation.
- [x] Add reconciliation and report workflow specifications and compatibility adapters.
- [x] Update integration and rendering contracts without merging stage responsibilities.
- [x] Run `.venv/bin/python scripts/health_check.py --module agents` from a checkout with `.venv`.

**Gate:** Schemas and ownership boundaries are documented, fixtures parse, compatibility checks pass,
and no content data has yet changed.

### Phase 3 — Temporal migration

- [x] Implement an idempotent backfill tool with `--dry-run` and explicit apply mode.
- [x] Resolve dates from canonical sources and report missing or conflicting values.
- [x] Add `published_date` to all 2,226 starting concept paper entries.
- [x] Require it for new Phase 1 integration entries.
- [x] Extend integrate health checks for presence, ISO date validity, and canonical agreement.
- [x] Prove a second migration run produces no diff.
- [x] Prove paper counts, claims, families, evidence roles, and all other fields are unchanged.

**Gate:** Zero missing or conflicting dates across 23 YAMLs; integrate health passes with no new
errors; the migration diff contains only `published_date` additions.

### Phase 4 — Reconciliation infrastructure

- [ ] Implement deterministic candidate generation and tests.
- [ ] Add a dedicated reconciliation health module.
- [ ] Create an empty valid registry and a Q3 run record containing generated candidates.
- [ ] Validate qualified references, vocabulary, unique broader IDs, cycles, decision completeness,
      reciprocal membership, incompatible canonical memberships, and paper deduplication.
- [ ] Report unresolved high-similarity candidates as warnings; broken structure is an error.

**Gate:** Generator output is byte-stable for identical inputs; all references validate; no command
accepts or mutates registry relationships automatically.

### Phase 5 — Q3 pilot and full reconciliation

- [ ] Review the evaluation-focused pilot first.
- [ ] Validate field-render behavior against accepted pilot relationships.
- [ ] Review all remaining thematic batches.
- [ ] Give every emitted candidate an accepted, rejected, or deferred disposition and rationale.
- [ ] Create broader claims only when at least two concepts contribute meaningfully.
- [ ] Preserve local status, scope, polarity, evidence, and caveats.
- [ ] Log each review batch in `log.md` and commit at theme boundaries.

**Gate:** Every Q3 run candidate has a disposition; accepted relationships and broader claims pass
reconciliation health; local cluster count remains 406 unless an independently justified
same-concept cleanup is performed outside this program.

### Phase 6 — Retrospective Q3 snapshot

- [ ] Freeze the reconciled view with cutoff `2025-09-30` and actual assessment date.
- [ ] Include only papers published on or before the cutoff.
- [ ] Record included paper IDs, source digests, and reconciliation run.
- [ ] Validate reproducibility, retrospective labeling, and immutability behavior.

**Gate:** Rebuilding from the same source commits produces the same assessed content and digests;
any later correction must create a superseding snapshot.

### Phase 7 — Current field overview

- [ ] Regenerate `overview.md` from all 23 concept YAMLs and the registry.
- [ ] Rank broader conclusions by decision impact, evidence independence, breadth, recency, and
      disagreement rather than publication volume.
- [ ] Deduplicate linked clusters and papers while preserving local qualifications.
- [ ] State the Q3 cutoff, retrospective assessment date, corpus boundary, and overlapping counts.
- [ ] Preserve traceability: broader claim -> local cluster -> paper claim -> cited source.

**Gate:** All 23 concepts inform the overview; linked clusters appear as one field conclusion where
appropriate; every factual claim remains traceable.

### Phase 8 — Q3 quarterly report

- [ ] Publish `reports/quarterly/2025-Q3.md` and update the reports index.
- [ ] Separate publication activity from changes in knowledge.
- [ ] Compare Q3 contributions with the pre-Q3 baseline.
- [ ] Cover new methods, strengthened/refined/contested claims, evaluation changes, and attention.
- [ ] Label the report as a retrospective assessment.
- [ ] Avoid equating publication volume with evidence strength or adoption.

**Gate:** Cutoff fixtures behave correctly; the report is reproducible from the Q3 snapshot and
distinguishes activity, evidence, and adoption.

### Phase 9 — Report framework completion

- [ ] Require at least two snapshots for trend reports and fail clearly with only Q3 available.
- [ ] Validate venue selection by canonical venue and inclusive publication range.
- [ ] Keep venue generation on demand; do not create an Interspeech report in this rollout.
- [ ] Enforce the existing reader-facing venue quality bar.

**Gate:** Trend failure and venue selection tests pass; no thin venue page is generated.

### Phase 10 — Closeout

- [ ] Run full health, render, reconciliation, report, link, schema, and compatibility checks.
- [ ] Confirm every generated page carries version-2 provenance.
- [ ] Update `BACKLOG.md`, `ARCHIVE.md`, and `log.md` as appropriate.
- [ ] Confirm both repositories are clean and record final commits.
- [ ] Archive this file with `git mv` to the dated `docs/records/` path.
- [ ] Record deliberately deferred candidates and their triggers.

---

## Test Matrix

- Schema fixtures for every relationship, qualified reference, temporal field, decision status,
  and snapshot boundary.
- Negative fixtures for missing clusters, duplicate broader IDs, cycles, conflicting memberships,
  invalid dates, unsupported vocabulary, incomplete dispositions, and improper snapshot mutation.
- Backfill dry-run, apply, and idempotency tests.
- Regression proof that migration changes only `published_date`.
- Candidate-generator determinism and stable ordering tests.
- Paper deduplication tests where one paper supports several member clusters.
- Cutoff fixtures for `2025-06-30`, `2025-07-01`, `2025-09-30`, and `2025-10-01`.
- Retrospective-labeling, snapshot-digest, supersession, and provenance tests.
- Field-overview test proving linked clusters become one conclusion while caveats survive.
- Quarterly-report test separating new publication activity from changed claim status.
- Trend-report failure test with fewer than two snapshots.
- Venue canonicalization and publication-range tests.
- Existing integrate, render, corpus, and agent-compatibility suites remain passing.

## Completion Criteria

- All 23 Q3 concepts participate in the reconciliation audit.
- All 406 starting local clusters remain present unless separately justified outside this program.
- Every emitted candidate has a recorded disposition and rationale.
- Every broader claim is traceable to at least two concept-local clusters.
- Every concept paper entry has an exact canonical `published_date`.
- The Q3 snapshot is reproducible, immutable, and explicitly retrospective.
- The field overview covers all concepts without semantic or paper double-counting.
- The Q3 report uses publication dates and distinguishes attention from evidence.
- Trend and venue workflows are implemented and validated; their first published reports remain
  deferred.
- The session note is archived under `docs/records/`, never in reader-facing reports.
- No source PDF or substantive metadata content is changed.

---

## Resume Here

**Current phase:** Phase 4 — Reconciliation infrastructure.
**Next action:** Implement deterministic advisory candidate generation and the dedicated
reconciliation health module, then create the empty registry and generated Q3 run record.

Baseline commits recorded at bootstrap:

- Infrastructure: `eb6a383` (`Mark Q4 2025 ingest backlog item complete`), detached worktree.
- Content: `5343143` (`Render Q3 concept overviews and in-depth pages`), branch `work/integrate`.

Current working commits after the 2026-08-13 setup refresh:

- Infrastructure: `fd03e29`, branch `work/integrate`, equal to local `main` and one commit ahead
  of freshly fetched `origin/main`.
- Content: `babd6cd`, branch `work/integrate`, equal to local `main` and one commit ahead of
  freshly fetched `origin/main`.

Content checkout:

```bash
export SPEECH_WIKI_CONTENT_DIR=/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content-integrate
```

Resume checks:

```bash
cd /Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-infra
git status --short --branch

cd /Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content-integrate
git status --short --branch

cd /Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-infra
/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-infra/.venv/bin/python \
  scripts/health_check.py --module integrate --wiki-dir "$SPEECH_WIKI_CONTENT_DIR"
/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-infra/.venv/bin/python \
  scripts/health_check.py --module render --wiki-dir "$SPEECH_WIKI_CONTENT_DIR"
```

Known setup issue: `python3 scripts/resolve_wiki_dir.py` currently fails without the environment
override because its default sibling content checkout is not writable in the managed workspace.
Use the explicit checkout above until the resolver setup is corrected.

Known design seed: begin qualified-reference fixtures with the duplicated
`semantic_acoustic_token_tradeoff` cluster ID, and begin human relationship review with the
evaluation-themed candidate batch.

## Session Log

### 2026-08-02 — Bootstrap and plan review

- Read the proposed program plan and reconciled it with tracked project state.
- Confirmed clean starting worktrees before creating this note.
- Confirmed all 23 concepts are integrated: 2,226 concept paper entries, 406 clusters, and 173
  method families.
- Ran integrate health: 0 errors, 241 warnings, 190 currently ingested non-Tier-2 papers absent
  from all YAMLs because Q4 ingest is ahead of integration.
- Ran render health: 0 errors, 7 warnings, 21 production Overview/In Depth pairs.
- Corrected the draft baseline: Q3 integration is complete, but production rendering is 21/23;
  the field overview covers five concepts rather than being “stale at five concepts.”
- Found one globally duplicated cluster ID across `speech-to-speech` and
  `spoken-language-model`, establishing the need for qualified references.
- Recorded the separate-registry, immutable-snapshot, temporal-migration, report-boundary, and
  advisory-candidate decisions.
- Created `CROSS_CONCEPT_SYNTHESIS_SESSIONS.md`; no content-repository files changed.
- Next: Phase 2 design and schema work. No commit or push performed.

### 2026-08-13 — Phase 1 closeout and worktree refresh

- Fetched both infrastructure and content remotes.
- Released the infra `work/integrate` branch from its ephemeral Codex worktree and switched the
  primary writable infra checkout to that branch.
- Fast-forwarded infra `work/integrate` to local `main` at `fd03e29` and content
  `work/integrate` to local `main` at `babd6cd`; both are one commit ahead of freshly fetched
  `origin/main` and zero commits behind.
- Verified the content integration checkout is clean and the explicit wiki resolver override
  targets it successfully.
- Kept this active session note at the repository root; `docs/design/` is reserved for stable
  design contracts and `docs/records/` for the completed program archive.
- Marked Phase 1 complete and authorized this note's standalone commit.
- Next: Phase 2 design and schema work.

### 2026-08-13 — Phase 2 designs, schemas, and workflow contracts

- Added focused reconciliation and temporal-reporting designs and schemas for the living registry,
  finalized run records, dual-boundary immutable snapshots, and supersession.
- Required canonical `published_date` on concept paper entries and removed the integration
  workflow's former missing-date fallback.
- Chose snapshot materialization at both the pre-quarter baseline and quarter cutoff so reports do
  not reassess history from counts or the living graph.
- Added shared reconciliation and report workflow skills, OpenAI metadata, and Claude adapters;
  expanded compatibility validation from six to eight workflows.
- Updated content-stage ownership, integration, rendering, generation provenance, writing style,
  pipeline health design, and the root operating contract.
- Added parseable registry, run, and snapshot fixtures, seeded with the qualified duplicate cluster
  reference, plus focused contract tests.
- Validated both new skills, ran all 15 repository unit tests, and ran the agents health module
  with 0 errors and 0 warnings across 8 workflows.
- Confirmed no content-repository files changed during Phase 2.
- Next: Phase 3 temporal migration.

### 2026-08-19 — Phase 3 temporal migration

- Audited all 2,226 concept paper entries across 23 YAMLs (497 unique papers) against canonical
  metadata and paper frontmatter: zero missing metadata dates, missing pages, missing page dates,
  source conflicts, or pre-existing claim dates.
- Added `scripts/backfill_claim_published_dates.py` with mutually exclusive required `--dry-run`
  and `--apply` modes. The tool inserts one quoted date line after each paper ID and preserves all
  other bytes.
- Added canonical date checks to the integrate health module: required field, exact ISO validity,
  and agreement with metadata.
- Added focused migration and health-check tests; all 24 repository unit tests pass.
- Applied 2,226 date additions across all 23 concept YAMLs. A second apply changed 0 files.
- Compared every migrated YAML with its committed predecessor after removing `published_date`:
  semantic state is identical. The raw diff contains 2,226 additions and zero removals, and every
  addition is a `published_date` line.
- Ran integrate health across all concepts: 0 errors and the same 241 pre-existing warnings;
  counts remain 2,226 paper entries, 406 clusters, 280 strongly supported, and 14 contested.
- Logged the migration in the content changelog with runtime provenance.
- Next: Phase 4 reconciliation infrastructure.
