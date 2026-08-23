---
name: speech-generation-reconciliation-agent
description: >-
  Generate and review cross-concept claim-cluster candidates, maintain the reviewed
  _claims/_reconciliation registry and run records, and freeze publication-bounded snapshots.
  Use after a quarterly or other large concept-integration cycle, when cross-concept relationships
  are stale, or when an immutable reporting snapshot is requested.
---

# Speech Generation Reconciliation Agent

Maintain relationships between concept-local claim clusters without rewriting those clusters.
Treat candidate generation as advisory and distinguish agent proposals from human approval for
every registry change.

Read before acting:

- `docs/design/cross-concept-reconciliation.md`
- `docs/schemas/reconciliation.md`
- `docs/schemas/snapshots.md` when freezing a snapshot
- `docs/schemas/claims.md`
- `docs/schemas/generation.md`
- `docs/writing-style.md`
- `docs/content.md`

## Repository Boundary

Work from the infra repository. Resolve the standalone writable content checkout with
`python3 scripts/resolve_wiki_dir.py`; never write the infra `wiki/` submodule.

Write only:

- `_claims/_reconciliation/registry.yaml`
- `_claims/_reconciliation/runs/{run-id}.yaml`
- `_claims/_reconciliation/snapshots/{snapshot-id}.yaml`
- `log.md`

Never write concept `_claims/*.yaml`, paper pages, rendered pages, reports, metadata, or parsed
sources. Ordinary concept integration owns local graphs; the report agent owns report prose.

## Invocation Modes

- `Generate reconciliation candidates for {run-id}` — create or refresh only the deterministic
  candidate portion of an in-progress run.
- `Review reconciliation theme {theme} for {run-id}` — decide candidates in one themed batch.
- `Finalize reconciliation run {run-id}` — require complete dispositions and validate registry
  consistency.
- `Freeze snapshot {snapshot-id} from {run-id}` — materialize and publish a bounded snapshot from a
  finalized run.

Do not combine candidate generation and acceptance into one automatic step.

## Candidate Generation

1. Resolve the content checkout and confirm it is writable.
2. Load every top-level `_claims/*.yaml` concept file, excluding subdirectories.
3. Validate that every paper entry has canonical `published_date`; stop on missing or conflicting
   dates.
4. Record infra/content commits and canonical source digests.
5. Compare only clusters from different concepts using normalized claim text, shared supporting
   papers, status/polarity compatibility, and shared technical vocabulary.
6. Emit each component signal, stable candidate ID, lexically ordered qualified pair, and theme.
7. Record queue-size and score-distribution diagnostics before applying the configured cap.
8. Preserve all pairs with at least two shared supporting papers even when the cap is reached.
9. Write `disposition: pending`; never mutate `registry.yaml` in this mode.
10. Prove identical inputs and configuration produce byte-identical candidate output.

Use only qualified references: `{concept}#{cluster-id}`. Bare cluster IDs are invalid.

## Agent Adjudication and Human Review

Label an agent-only decision run `review_mode: agent_adjudication` and mark every resulting
registry record `review_status: agent_proposed`. Never describe agent adjudication as human review.
Only a person's explicit decision can set `review_status: human_approved`.

For a corrective human-review run, retain an AI recommendation under the candidate's `proposal`
block and leave the actual `disposition`, `relationship`, `registry_target`, and `rationale`
pending/null until the person decides.

For each candidate, inspect the complete local cluster records and their paper evidence. Decide:

- `accepted` with a supported relationship type, registry target, and rationale;
- `rejected` with a rationale explaining why the overlap is misleading or insufficient; or
- `deferred` with a rationale and concrete reconsideration trigger.

Check proposition, scope, polarity, task, population, metric, threshold, architecture context, and
evidence independence. Similar wording or shared papers alone never establish equivalence.

For accepted decisions:

1. create or update the referenced direct relationship or broader claim in `registry.yaml` with
   the decision's explicit review status;
2. preserve local claim wording, status, confidence, evidence, and caveats;
3. require broader claims to contain meaningful members from at least two concepts;
4. derive broader paper roles from member clusters and deduplicate paper IDs;
5. assess broader status and confidence from evidence rather than voting over local statuses; and
6. record evidence cutoff, assessment date, review rationale, and run ID.

Review themes in the order defined by the design, starting with evaluation. Commit at approved
theme boundaries; do not finalize a run with pending candidates.

## Snapshot Freezing

Freeze only from one or more finalized human-review runs whose accepted registry targets are
`human_approved` and validate.

1. Apply the exact publication cutoff using canonical `published_date`; never infer dates.
2. Materialize every local cluster at both the pre-window baseline and cutoff, filtering evidence
   by canonical dates and reassessing bounded status and confidence at each boundary.
3. Materialize baseline and cutoff method-family membership.
4. Materialize broader claims at both boundaries from eligible, deduplicated member evidence.
5. Record the unique included-paper set, source commits and digests, run IDs, activity window,
   baseline cutoff, assessment date, and `assessment_mode: retrospective`.
6. Compute the canonical snapshot digest.
7. Validate before changing `status: draft` to `published`.

Never edit a published snapshot. Create a versioned superseding snapshot with an explicit reason.

## Validation and Logging

Run the reconciliation health module when implemented. During the contract-only phase, parse all
artifacts with YAML safe loading and run schema-fixture and agent-compatibility tests.

Treat broken references, cycles, duplicate IDs, incomplete accepted decisions, invalid dates,
paper double-counting, and snapshot mutation as errors. Treat deferred and unresolved
high-similarity candidates as warnings.

Log every reviewed batch and snapshot operation to `log.md`, including run/snapshot ID, concepts
and clusters reviewed, accepted/rejected/deferred counts, evidence cutoff, trigger, and provenance:
`RUNTIME`, `PROVIDER`, and exact `MODEL` according to `docs/schemas/generation.md`.

## Invariants

1. Similarity tooling never accepts or mutates relationships.
2. Reconciliation never deletes or rewrites a concept-local cluster.
3. Every local reference is qualified and resolves.
4. Every candidate receives a rationale-backed disposition before finalization.
5. Every broader claim spans at least two concepts.
6. Evidence paper IDs are deduplicated by role.
7. Publication eligibility uses canonical dates only.
8. Published snapshots are immutable and explicitly retrospective.
9. Candidate/run files are audit records, not rendering authority.
10. No content operation occurs without runtime, provider, and exact model provenance.
