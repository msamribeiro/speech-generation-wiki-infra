# Integration Protocol

The operating procedure for a quarterly or other bounded concept-integration cycle. It defines
how the main session freezes scope, stages Phase 1 and Phase 2, obtains human-reviewed
cross-concept decisions, publishes derived views, merges parallel work, and closes the cycle.
Read it at the start of every integration session.

This file orchestrates; it does not replace the specifications it points to:

| Concern | Authority |
|---|---|
| Phase 1 and Phase 2 behavior, batch limits, run output | `.agents/skills/speech-generation-integration-agent/SKILL.md` |
| Concept claim YAML fields and evidence rules | [schemas/claims.md](schemas/claims.md) |
| Cross-concept candidates, reviewed authority, and run finalization | `.agents/skills/speech-generation-reconciliation-agent/SKILL.md` and [schemas/reconciliation.md](schemas/reconciliation.md) |
| Snapshot boundaries and immutability | [schemas/snapshots.md](schemas/snapshots.md) |
| Concept and field rendering | `.agents/skills/speech-generation-render-agent/SKILL.md` |
| Snapshot-backed quarterly reports | `.agents/skills/speech-generation-report-agent/SKILL.md` |
| Canonical paper dates and later versions | [schemas/metadata.md](schemas/metadata.md) |
| Pipeline ownership and stage overview | [content.md](content.md) |
| Quarter-specific queues, decisions, and resume state | the active integration session record |

**Maintenance.** If an integration cycle reveals a recurring procedural problem, update this
protocol before closing the cycle. Session records preserve what happened once; this file records
what future cycles should do differently. If this protocol conflicts with a schema or skill,
resolve the inconsistency in the same commit.

---

## 1. Start from a stable boundary

1. Inspect the infrastructure, content, and site repositories and every relevant worktree. Preserve
   unrelated or uncommitted work.
2. Merge or otherwise account for all committed ingestion work that can affect the target period
   before creating the integration worktree. Record the starting commits.
3. Use the project interpreter and an explicit content path for validation:

   ```bash
   .venv/bin/python scripts/health_check.py --wiki-dir /absolute/path/to/content
   ```

   Do not rely on the system `python3` or an implicit resolver when multiple content worktrees
   exist.
4. Read `STATUS.md`, `BACKLOG.md`, the previous quarter's archived session record, and the active
   integration record. Recompute counts from files; do not copy counts from chat.
5. Run the full health suite. Integration does not begin with unresolved errors in ingest,
   metadata, integrate, reconcile, or render.

### Canonical-date preflight

The quarter is selected only by canonical `published_date`, inclusive of its first and last day.
Before freezing the candidate set:

- check every accepted or recently ingested paper whose arXiv date is near the boundary for a
  proceedings or journal version;
- resolve page-versus-metadata date disagreements;
- confirm ingest status and the presence of exactly one paper-index row;
- exclude duplicate pointers and Tier 2 pages according to the current schema; and
- apply the peer-reviewed-version and frozen-quarter rules before using the date in integration.

A date is frozen only when the canonical paper ID occurs in the `papers:` list of a top-level
canonical `_claims/*.yaml`. Reconciliation, snapshots, reports, and rendered pages do not create a
freeze. If a known peer-reviewed version has not yet been applied, integration stops at this gate;
Phase 1 must not be used to freeze a provisional preprint date.

A later discovery of an earlier proceedings date can silently move a paper into the quarter. The
Q4 2025 cycle exposed this with `2605.18001` and `2605.25504`; the date audit is therefore a hard
preflight gate, not a closeout cleanup task.

---

## 2. Freeze one deterministic quarter manifest

Create one authoritative manifest in the active session record before Phase 1. It must state:

- evidence cutoff and inclusive date range;
- eligible non-Tier-2 paper IDs;
- intentional exclusions and unassigned pages;
- each paper's canonical `related_concepts` memberships;
- per-concept candidate counts, already-present counts, and Phase 1 queue sizes;
- starting content and infrastructure commits; and
- the exact commands used to reproduce the counts.

The manifest is a set contract, not merely a dashboard estimate. Sort candidates oldest-first by
`published_date` and then stable paper ID. Never infer membership from task or architecture tags
during integration; fix missing `related_concepts` at ingest or review first.

Recompute the exact manifest immediately before the first batch. After that point, newly discovered
papers do not enter ad hoc. Handle them through the bounded corrective procedure in section 8.

---

## 3. Worktree and ownership discipline

Use a dedicated integration worktree created from the latest merged content `main`. Keep these
ownership boundaries:

- integration owns top-level `_claims/{concept}.yaml` and its integration log entries;
- reconciliation owns `_claims/_reconciliation/` and its log entries;
- rendering owns concept pages, the field overview, and navigation it is explicitly instructed to
  refresh;
- ingestion owns paper pages, `papers/index.md`, paper counts, and ingest log entries.

Parallel ingestion may continue only when its effects are visible and bounded. Because ingestion
and integration both historically touched `log.md`, and rendering and ingestion both touched the
homepage, avoid long-lived parallel divergence across shared files. Prefer one of these patterns:

1. pause shared-file ingestion writes until the integration cycle merges; or
2. merge ingestion checkpoints into the integration base before reconciliation and again before
   final rendering, then rerun the manifest and health suite.

Do not wait until closeout to discover months of branch divergence. A completed integration branch
must merge before the next quarterly integration branch starts.

---

## 4. Phase 1 — extract concept-local evidence

Process one concept at a time, top to bottom through the agreed concept order.

1. Recompute the concept's live queue against the frozen manifest.
2. Run oldest-first batches of at most **20 new paper pages** per invocation.
3. Preserve every paper-page claim. Relevance controls synthesis weight; it does not authorize
   dropping claims.
4. Validate the concept with `--phase 1` after every batch.
5. Compare the actual IDs written with the planned batch IDs, not only the count.
6. Update the active session record with cumulative progress, remaining IDs, validation outcome,
   and the exact next starting paper.

Phase 1 is closed only when the exact manifest candidate set equals the concept YAML's bounded set,
after accounting for recorded exclusions. A zero-error health check alone is not an exact-set
closure audit.

---

## 5. Phase 2 — synthesize immediately after concept closure

Run Phase 2 as soon as the target concept's Phase 1 queue closes; do not defer all Phase 2 work to
the end of the quarter.

For each concept:

1. synthesize from the complete YAML `papers:` list, not directly from paper pages;
2. update clusters, method families, reassessments, open questions, and trend notes;
3. verify reciprocal family memberships and high/medium-relevance cluster coverage;
4. run concept-scoped `--phase 2` validation; and
5. finish with the required plain-language paragraph of fewer than 200 words describing the main
   clusters, trade-offs, and established/emerging/contested distinctions.

Append that paragraph to `PHASE2_CLUSTER_SUMMARIES.local.md`. It is a reader-convenience log, not
wiki evidence and not a replacement for the YAML.

After the final concept closes, run the corpus-wide integrate check and the frozen-manifest
candidate-versus-YAML audit. Record accepted warnings explicitly.

---

## 6. Cross-concept reconciliation

Reconciliation begins only after every affected concept has passed Phase 2.

1. Generate one deterministic candidate run from the closed concept graph.
2. Preserve prior human-reviewed authority; generated similarity candidates are advisory.
3. Triage candidates into readable semantic themes and broader bundles before human review.
4. Present the main theme and, for each proposed relationship, explain the category, both claims,
   their relationship, and why the relationship is worth accepting or rejecting.
5. Review bundles rather than individual propositions when they share one defensible rationale.
   Reserve individual review for ambiguous boundaries, reversals of prior authority, and unusual
   rejections.
6. Record every candidate as accepted, rejected, or deferred with rationale and a reconsideration
   trigger. Never label agent triage as human review.
7. Finalize only with zero pending candidates and a passing reconciliation health check.

If late evidence changes only derived support for existing reviewed relationships, run a bounded
corrective refresh. Do not regenerate or silently rewrite the finalized human-review run.

---

## 7. Render, snapshot, and report in gated order

The publication order is fixed:

1. render all stale concept Overview/In Depth pairs;
2. render the field overview from concept YAMLs plus human-approved reconciliation authority;
3. validate render completeness and provenance;
4. freeze the immutable retrospective snapshot;
5. validate its cutoff, source digests, counts, and supersession semantics;
6. generate the quarterly report from the snapshot, never from the live graph; and
7. refresh report and reader-navigation indexes.

The current concept pages and field overview are living views. Snapshots and quarterly reports are
immutable historical views. Keep those roles distinct in prose and metadata.

---

## 8. Bounded late-evidence correction

If a paper that belongs inside the frozen quarter is discovered after nominal integration closure:

1. prove the canonical date and eligibility;
2. add it to the session record as an explicit manifest correction;
3. run targeted Phase 1 only for its canonical concepts;
4. run targeted Phase 2 for every changed concept;
5. audit affected reconciliation relationships and broader claims;
6. refresh only the derived reconciliation evidence that actually changed;
7. rerender affected concepts and the field overview; and
8. freeze or regenerate the snapshot and report only after all earlier gates pass.

Never patch the report alone. The correction must flow through the full source-of-truth chain.

---

## 9. Closeout and publication

Closeout is complete only when all of the following are true:

- the frozen manifest has zero unexplained missing or extra memberships;
- all affected concepts pass Phase 2;
- reconciliation is finalized with zero pending candidates;
- all canonical concept pairs and the field overview are current;
- snapshot and report validation pass;
- the paper catalog has exactly one row per page and homepage counts match it;
- `STATUS.md`, `BACKLOG.md`, the active session record, and both logs agree;
- the full health suite passes with zero errors against an explicit content checkout;
- completed backlog work is moved to `ARCHIVE.md`, never deleted;
- the session record is archived under `docs/records/YYYY-MM-DD-...md`;
- both primary repositories are clean; and
- the integration worktree and branch are removed only after their commits are merged.

Merge and publish in dependency order:

1. merge the integration content branch into content `main`, preserving later ingestion work;
2. run the full health suite against the merged content checkout;
3. push content `main`;
4. update the infrastructure `wiki` submodule to that pushed content commit, merge and push
   infrastructure `main`;
5. update the site `content` submodule, run the production Quartz build, commit, and push the site;
6. verify every local `main` equals `origin/main`.

Do not remove active or dirty ingestion worktrees during integration cleanup. Detached
Codex-managed worktrees also require a separate ownership audit before removal.

---

## 10. Derived state and automation targets

Counts in `STATUS.md`, `BACKLOG.md`, the homepage, and session records drift when maintained by
hand. Until generation is automated, derive them from the health suite, corpus summary, exact
manifest audit, and paper index immediately before writing them.

The highest-value automation targets are:

- `integration preflight`: canonical-date audit, duplicate/index check, frozen manifest, and
  starting health baseline;
- `integration validate`: exact manifest closure plus all stage health modules;
- `integration closeout`: generated status counts, archive checklist, dependency-ordered merge and
  submodule plan; and
- structured per-stream event logs that generate `wiki/log.md`, eliminating long-lived merge
  conflicts in one append-only Markdown file.

Automation may produce candidates and derived counts. It must not accept reconciliation
relationships, decide ambiguous paper scope, or rewrite human-reviewed authority without explicit
review.
