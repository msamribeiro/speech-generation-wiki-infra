# Cross-Concept Reconciliation Design

**Status:** Contract approved for implementation
**Stage:** Reconcile, after Integrate and before field-level Render or Snapshot
**Schemas:** [reconciliation.md](../schemas/reconciliation.md),
[claims.md](../schemas/claims.md), [snapshots.md](../schemas/snapshots.md)

## Purpose

Concept integration deliberately produces concept-local claim clusters. The same underlying
proposition can therefore appear in several `_claims/{concept}.yaml` files with different wording,
scope, evidence, confidence, or polarity. Reconciliation reviews those overlaps and records their
relationships without flattening the local graphs.

The stage adds a separate authority layer:

```text
papers -> concept claim YAMLs -> reconciliation registry -> field overview
                                             \-> snapshot -> report
```

Concept YAMLs remain authoritative for local claims, paper evidence, status, confidence, caveats,
and method families. `_claims/_reconciliation/registry.yaml` is downstream authority only for
cross-concept relationships and broader claims marked `human_approved`. Agent-proposed records
remain visible for review but cannot affect rendering or snapshots. Run records are the audit trail
for proposals, agent adjudications, and human decisions.

## Ownership and Paths

The reconciliation workflow reads all `_claims/*.yaml` concept files and writes only:

```text
_claims/_reconciliation/registry.yaml
_claims/_reconciliation/runs/{run-id}.yaml
_claims/_reconciliation/snapshots/{snapshot-id}.yaml
log.md
```

It never rewrites concept-local claims, paper pages, rendered concepts, field overview prose, or
reports. Ordinary integration never writes `_claims/_reconciliation/`.

## Reconciliation Unit

The unit of comparison is a qualified local cluster reference:

```text
{concept-slug}#{cluster-id}
```

Bare cluster IDs are invalid even when globally unique. A qualified reference resolves only when
the concept file exists and contains the named cluster.

Accepted relationships use the vocabulary in `docs/schemas/reconciliation.md`. Direction matters
for `specialization`, `supports`, and `refines`. `equivalent`, `contradicts`, `tradeoff`, and
`related` are symmetric and use lexically ordered endpoints for deterministic serialization.

## Local, Linked, or Broader

Keep clusters concept-local and unlinked when their apparent similarity is merely shared topic or
terminology.

Create a direct relationship when two claims inform one another but a new field-level proposition
would add no explanatory value. Examples include a local claim refining another, two claims
capturing a trade-off, or incompatible assessments at overlapping scope.

Create a broader claim when at least two concepts contribute materially to one field-level
proposition. A broader claim is a reviewed synthesis node, not a replacement cluster. Its members
remain in their local files and retain their own wording and epistemic state.

Accept `equivalent` only when proposition, scope, population, task, metric, threshold, and polarity
are materially the same. Prefer:

- `specialization` when one claim has narrower scope;
- `refines` when one adds a boundary or more precise formulation;
- `supports` when one supplies a compatible mechanism or evidence without identity;
- `contradicts` when assessments are incompatible at overlapping scope;
- `tradeoff` when gains and costs must be interpreted together; or
- `related` when meaningful overlap exists but a stronger relation is not justified.

Different local status or confidence does not itself forbid a relationship. It does forbid
silently replacing those judgments with one manufactured consensus.

## Candidate Generation

Candidate generation is deterministic, read-only, and advisory. It compares clusters from
different concepts using:

- normalized claim-text similarity;
- shared supporting-paper overlap;
- status and polarity compatibility; and
- shared technical vocabulary.

Every candidate records the component signals as well as the aggregate score. For identical
inputs and configuration, output ordering and serialization must be byte-stable.

The initial policy is:

1. exclude same-concept pairs;
2. include the ten highest-scoring cross-concept neighbors per cluster;
3. include every pair with at least two shared supporting papers;
4. deduplicate symmetric pairs using lexical qualified-reference order;
5. collect queue-size and score-distribution diagnostics; and
6. after diagnostics, cap the review queue at 500 while preserving all shared-evidence candidates.

The generator writes candidates with `disposition: pending`. It must not create registry entries,
accept relationships, or rewrite concept YAMLs.

## Agent Proposals and Human Review

An agent may adjudicate candidates and draft registry records, but it must label the run
`review_mode: agent_adjudication` and every resulting registry record
`review_status: agent_proposed`. Do not describe this work as human-reviewed. A corrective or
ordinary human-review run keeps any AI recommendation in a separate candidate `proposal` block
while leaving `disposition: pending` until a person decides.

Review candidates in themed batches, beginning with evaluation and subjective judgment. For every
candidate, record one disposition and a non-empty rationale:

- `accepted` — creates or cites an accepted registry relationship or broader-claim membership;
- `rejected` — the overlap is insufficient or misleading; or
- `deferred` — a named evidence or design condition must be resolved before deciding.

In a human-review run, an accepted decision is incomplete until its registry target exists and is
marked `human_approved`. Rejected candidates never
appear in the registry. Deferred candidates remain warnings and record a concrete reconsideration
trigger.

The reviewer checks evidence scope, polarity, metrics, populations, tasks, architecture context,
and whether shared papers are genuinely independent evidence. Text similarity alone is never a
review rationale.

## Broader-Claim Assessment

A broader claim must have members from at least two distinct concepts. Its supporting,
contradicting, and refining paper lists are derived from member clusters and deduplicated by paper
ID. A paper appearing in several members counts once in each evidence role.

The broader status and confidence are reviewed judgments over the deduplicated evidence, not a
mechanical vote or sum of local statuses. Record the evidence cutoff, assessment date, caveats, and
review rationale. Local members can remain contested or emerging even when the broader
proposition has a different current assessment.

## Cadence and Run Lifecycle

Run reconciliation after each quarterly integration cycle or another large integration round:

1. freeze source concept digests and the evidence cutoff;
2. generate deterministic candidates and diagnostics;
3. review candidates in themed batches;
4. update accepted registry relationships and broader claims;
5. give every candidate a final disposition and rationale, explicitly recording whether the run
   was agent adjudication or human review;
6. validate registry and run together;
7. log concepts, clusters, decisions, deferrals, trigger, runtime, provider, and model; and
8. optionally freeze a snapshot after the run is complete.

Run records are finalized audit artifacts. If review resumes after finalization, create a new run
that references the earlier run rather than silently changing its decisions.

## Validation Contract

The reconciliation health module will treat structural defects as errors and unresolved review
work as warnings. It must validate:

- qualified-reference resolution and canonical endpoint ordering;
- supported relationship and disposition vocabulary;
- unique relationship, broader-claim, candidate, run, and snapshot IDs;
- broader claims spanning at least two concepts;
- reciprocal consistency between broader claims and accepted candidate decisions;
- directed-relationship and broader-membership cycles;
- incompatible equivalent or canonical memberships;
- complete accepted/rejected/deferred rationales;
- accepted candidates pointing to registry state;
- deduplicated evidence paper IDs and canonical publication dates;
- immutable snapshot and supersession rules; and
- unresolved high-similarity or deferred candidates as warnings.

No health command mutates the registry or run records.

## Rendering Contract

Concept Overview and In Depth pages continue to derive their epistemic assessments from their
local YAML. They may use registry relationships for cross-concept navigation and to avoid implying
that linked findings are independent field discoveries.

The current field overview reads all concept YAMLs plus `registry.yaml`. It presents a
`human_approved` broader claim once, deduplicates paper evidence across its members, and preserves material local
qualifications. Unlinked local clusters remain eligible for field synthesis. Candidate and run
files are never rendering authority.

## Initial Pilot

The first run covers the 23 Q3-integrated concepts and starts with the evaluation-themed batch.
The duplicated qualified candidates
`speech-to-speech#semantic_acoustic_token_tradeoff` and
`spoken-language-model#semantic_acoustic_token_tradeoff` seed reference and duplicate-ID fixtures;
their relationship remains undecided until human review.
