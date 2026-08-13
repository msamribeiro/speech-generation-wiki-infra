# Temporal Reporting Design

**Status:** Contract approved for implementation
**Inputs:** Immutable reconciliation snapshots
**Schemas:** [snapshots.md](../schemas/snapshots.md),
[reconciliation.md](../schemas/reconciliation.md)

## Purpose

Temporal reports answer bounded questions without rewriting historical assessments when the live
claim graph changes. They distinguish three dates:

- `published_date` determines whether evidence is eligible;
- `evidence_cutoff` bounds the assessed literature; and
- `assessment_as_of` records when reviewers performed the retrospective assessment.

A report must never imply that its assessment was known at the evidence cutoff unless it was
actually assessed then.

## Snapshot First

Every temporal report derives from an immutable snapshot under
`_claims/_reconciliation/snapshots/`. Reports do not read the living registry or concept YAMLs as
evidence authority. They may read paper frontmatter only for human-readable titles and links after
verifying that each paper is included in the snapshot.

For quarterly reporting, the snapshot materializes both the assessment through the pre-quarter
baseline cutoff and the assessment through the quarter cutoff. The report compares those frozen
assessments; it does not recompute historical status from paper counts.

The reconciliation workflow freezes snapshots. The report workflow validates and reads them but
never edits them.

## Report Types

### Quarterly

Path: `reports/quarterly/{YYYY-QN}.md` for the first edition, with versioned filenames for
superseding corrections.

A quarterly report compares:

- activity during the inclusive quarter window;
- the assessed knowledge state at the pre-quarter baseline; and
- the assessed knowledge state through the quarter cutoff.

It separates publication activity from changed knowledge. A paper count can show attention, not
evidence strength, adoption, or consensus. Required coverage includes new or expanded methods,
strengthened/refined/contested claims, evaluation changes, and important negative or limiting
evidence.

### Trend

A trend report requires at least two immutable snapshots. It compares like-for-like assessed
fields and explains schema, corpus, or coverage changes that weaken comparability. With fewer than
two snapshots, the workflow fails clearly and writes no report.

### Venue

Venue reports remain on demand. Selection uses the canonical venue value and an inclusive
publication-date range. A venue report must compare venue-specific activity and evidence with the
wider-field snapshot rather than produce a thin paper inventory. If the selected evidence cannot
support synthesis, write nothing and report the insufficiency.

## Quarterly Structure

Reader-facing quarterly reports contain:

1. Scope and retrospective-assessment statement;
2. Executive synthesis;
3. Publication activity during the quarter;
4. Changes in assessed knowledge;
5. New methods and capability directions;
6. Evaluation and evidence-quality changes;
7. Contested, weakened, or unresolved findings;
8. Attention versus evidence caveat;
9. Representative reading path; and
10. Snapshot and provenance references.

The report cites representative papers with `[[id|Name]]`. Every factual conclusion traces to a
snapshot local-cluster or broader-claim assessment, which in turn traces to concept YAML evidence.

## Current State Versus Historical Reports

`overview.md` is a replaceable current-state synthesis derived from the live concept graphs and
reviewed registry. Reports are immutable bounded accounts derived from snapshots. Updating the
field overview never changes a historical report, and publishing a report never makes its snapshot
the current registry.

## Supersession

Published snapshots and reports are never edited in place for substantive corrections. Create a
versioned successor, record `supersedes` and `supersession_reason`, and add reciprocal reader-facing
links. Typographical changes that do not alter meaning may be corrected without supersession but
must not change snapshot digests or evidence selections.

## Reproducibility

A report records:

- snapshot ID and digest;
- evidence cutoff, activity window, and assessment date;
- included-paper count and overlapping concept counts;
- source infra and content commits;
- version-2 generation provenance; and
- any comparison or coverage limitations.

Rebuilding from the same snapshot and renderer contract must reproduce the same factual
assessments and source set. Prose may vary only before publication; a published report is frozen.

## Validation Contract

Report validation checks:

- the referenced snapshot exists and its digest matches;
- retrospective labeling is explicit;
- every cited paper is included in the snapshot;
- report dates and windows match the snapshot;
- quarterly reports separate activity from knowledge change;
- trend reports reference at least two ordered snapshots;
- venue selection uses canonical venue values and inclusive date bounds;
- supersession references resolve and do not cycle;
- generation provenance is version 2; and
- the reports index and `log.md` contain the operation.
