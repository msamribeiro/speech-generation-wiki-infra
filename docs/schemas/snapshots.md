# Reconciliation Snapshot Schema

Snapshots freeze a publication-bounded, retrospectively assessed projection of the concept claim
graphs and reviewed reconciliation registry. They are report inputs, not backups of
`registry.yaml` and not replacements for concept YAMLs.

## Path and Identity

The first edition uses:

```text
wiki/_claims/_reconciliation/snapshots/{period}.yaml
```

A substantive correction creates `{period}-v2.yaml`, then `-v3`, and so on. Never overwrite a
published snapshot.

## Full Schema

```yaml
schema_version: 1
snapshot_id: 2025-Q3
period: 2025-Q3
evidence_cutoff: 2025-09-30
activity_window:
  start: 2025-07-01
  end: 2025-09-30
baseline_cutoff: 2025-06-30
assessment_as_of: YYYY-MM-DD
assessment_mode: retrospective
status: published
supersedes: null
supersession_reason: null

source:
  infra_commit: abc1234
  content_commit: def5678
  reconciliation_runs: [2025-Q3]
  registry_digest: "sha256:..."
  concept_digests:
    concept-a: "sha256:..."
    concept-b: "sha256:..."

included_papers:
  - id: paper-b
    published_date: 2025-05-10
    venue: ICASSP
    concepts: [concept-a, concept-b]
  - id: paper-a
    published_date: 2025-08-15
    venue: Interspeech
    concepts: [concept-a, concept-b]
baseline_papers: [paper-b]
activity_papers: [paper-a]

concepts:
  - concept: concept-a
    eligible_papers: [paper-a, paper-b]
    claim_clusters:
      - ref: concept-a#cluster-a
        proposition: "Concept-local proposition at snapshot time."
        baseline_assessment:
          status: emerging
          confidence: low
          supporting_papers: [paper-b]
          contradicting_papers: []
          refining_papers: []
        cutoff_assessment:
          status: emerging
          confidence: medium
          supporting_papers: [paper-a, paper-b]
          contradicting_papers: []
          refining_papers: []
        caveats: []
    method_families:
      - id: family-a
        baseline_papers: [paper-b]
        cutoff_papers: [paper-a, paper-b]

broader_claims:
  - id: broader_example
    proposition: "Reviewed broader proposition at snapshot time."
    members: [concept-a#cluster-a, concept-b#cluster-b]
    baseline_assessment:
      status: emerging
      confidence: low
      supporting_papers: [paper-b]
      contradicting_papers: []
      refining_papers: []
    cutoff_assessment:
      status: emerging
      confidence: medium
      supporting_papers: [paper-a, paper-b]
      contradicting_papers: []
      refining_papers: []
    caveats: []

digest: "sha256:..."
```

## Semantics

`included_papers` contains every unique eligible paper used anywhere in the snapshot. Eligibility
requires an exact canonical `published_date` on or before `evidence_cutoff`. The activity window is
inclusive at both ends and is a subset of the evidence window. `baseline_cutoff` immediately
precedes the activity window for quarterly snapshots.

`baseline_papers` contains eligible evidence through `baseline_cutoff`; `activity_papers` contains
papers in the inclusive activity window. Their union forms the unique `included_papers` set through
`evidence_cutoff` for a contiguous quarterly comparison.

Concept clusters materialize both `baseline_assessment` and `cutoff_assessment` after filtering
their evidence to the respective dates. Status and confidence are reassessed at both boundaries;
they are not copied blindly from the live graph. A genuinely new cluster may use `null` for
`baseline_assessment`. Broader claims follow the same rule using eligible, deduplicated member
evidence. A source paper appearing in several concepts occurs once in `included_papers` and once per
evidence-role list in each assessment.

The version-1 materializer applies the claim-schema evidence thresholds at each boundary. A claim
with eligible contradicting evidence is `contested`; otherwise three or more eligible supporting
papers can support `strongly_supported`, while smaller evidence sets remain `emerging`. A live
`emerging` judgment caps the bounded status so paper count cannot erase methodological caveats.
Confidence is `low`, `medium`, or `high` for one, two, or at least three unique eligible evidence
papers respectively, capped by the reviewed live confidence. These deterministic rules make the
retrospective assessment reproducible; they do not treat paper counts as adoption or consensus.

The snapshot records complete local-cluster assessments needed to explain field changes, including
unlinked clusters. It records baseline and cutoff method-family eligibility so reports can
distinguish a new family from an established family gaining more papers.

## Digests

All digests use SHA-256 over canonical UTF-8 serialization with sorted mapping keys, preserved list
order where semantically meaningful, LF newlines, and the artifact's own `digest` field omitted.
Prefix values with `sha256:`. The implementation must publish one canonicalization function and use
it for registry, concept, snapshot, and report-source verification.

`source` digests prove which living inputs were assessed. The top-level snapshot digest protects
the materialized bounded result.

## Immutability and Supersession

`status` is `draft | published | superseded`. Draft snapshots may be rebuilt. Once published, the
file is immutable. A correction creates a new snapshot with:

- a new versioned `snapshot_id` and filename;
- `supersedes` pointing to the immediately previous snapshot;
- a non-empty `supersession_reason`; and
- the previous snapshot marked superseded only through an external index or Git-tracked metadata,
  not by editing the published file.

Supersession chains must resolve, move forward in version order, and contain no cycles.

## Validation Rules

- all dates are exact ISO `YYYY-MM-DD` values and windows are ordered;
- `assessment_mode` is `retrospective` for the initial rollout;
- concept and broader references resolve against the recorded source inputs;
- every evidence paper occurs in `included_papers` and satisfies the cutoff;
- baseline and activity paper partitions obey their inclusive date boundaries;
- every non-null baseline assessment uses only baseline papers and every cutoff assessment uses
  only cutoff-eligible papers;
- every included paper records canonical date, venue, and sorted unique concepts;
- paper and member lists are sorted and unique;
- all 23 concepts are present in the initial Q3 snapshot;
- source run records are finalized and accepted registry targets resolve;
- the stored digest recomputes exactly; and
- published snapshot bytes never change in later commits except through an explicitly approved
  repository-history repair.

## Materialization Command

Use `scripts/freeze_reconciliation_snapshot.py`. Create and validate a draft first, then publish:

```bash
.venv/bin/python scripts/freeze_reconciliation_snapshot.py \
  --wiki-dir "$SPEECH_WIKI_CONTENT_DIR" --snapshot-id 2025-Q3 --period 2025-Q3 \
  --baseline-cutoff 2025-06-30 --activity-start 2025-07-01 --activity-end 2025-09-30 \
  --evidence-cutoff 2025-09-30 --assessment-as-of YYYY-MM-DD \
  --run-id 2025-Q3-corrective-review --apply
```

Repeat with `--check` to prove byte reproducibility. After health validation, repeat with
`--publish`, then `--check` again. The command refuses to overwrite a published snapshot.
