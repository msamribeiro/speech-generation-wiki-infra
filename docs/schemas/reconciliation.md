# Cross-Concept Reconciliation Schema

Reconciliation artifacts live below `wiki/_claims/_reconciliation/`. Schema version 1 has two
mutable-to-final artifact types: the living registry and finalized run records. Registry records
explicitly distinguish agent proposals from human-approved decisions. Concept
claims remain in `wiki/_claims/{concept}.yaml` under `docs/schemas/claims.md`.

## Qualified References

Every local cluster reference is a string in this exact form:

```text
{concept-slug}#{cluster-id}
```

Both components must resolve. Bare cluster IDs and references containing more than one `#` are
invalid.

## Relationship Vocabulary

| Value | Direction | Meaning |
|---|---|---|
| `equivalent` | symmetric | Materially the same proposition, scope, and polarity |
| `specialization` | source to target | Source is a narrower instance of target |
| `supports` | source to target | Source supplies compatible evidence or mechanism without identity |
| `refines` | source to target | Source adds a boundary, condition, or more precise formulation |
| `contradicts` | symmetric | Incompatible assessments at overlapping scope |
| `tradeoff` | symmetric | Coupled gains and costs that require joint interpretation |
| `related` | symmetric | Meaningful overlap without a justified stronger relationship |

Symmetric relationship endpoints must be lexically ordered by qualified reference.

## Registry

Path: `wiki/_claims/_reconciliation/registry.yaml`

```yaml
schema_version: 1
last_updated: YYYY-MM-DD

relationships:
  - id: rel_{stable_slug}
    source: concept-a#cluster-a
    target: concept-b#cluster-b
    type: refines
    rationale: "Why this exact relation is justified."
    review_status: agent_proposed | human_approved
    reviewed_on: YYYY-MM-DD
    accepted_in: 2025-Q3

broader_claims:
  - id: broader_{stable_slug}
    proposition: "Reviewed field-level proposition."
    status: strongly_supported
    confidence: high
    review_status: agent_proposed | human_approved
    members:
      - claim: concept-a#cluster-a
        relationship: specialization
        rationale: "How the local claim contributes."
      - claim: concept-b#cluster-b
        relationship: supports
        rationale: "How the local claim contributes."
    supporting_papers: [paper-a, paper-b]
    contradicting_papers: []
    refining_papers: [paper-c]
    caveats:
      - "Material scope qualification."
    review_rationale: "How deduplicated evidence supports the assessment."
    evidence_cutoff: YYYY-MM-DD
    assessment_date: YYYY-MM-DD
    reviewed_in: 2025-Q3
```

Registry rules:

- relationship and broader-claim IDs are globally unique and stable;
- relationship endpoints must come from different concepts;
- a broader claim has at least two members from at least two concepts;
- each member occurs once within a broader claim;
- a local cluster cannot be an `equivalent` member of incompatible broader claims;
- supporting, contradicting, and refining lists contain unique paper IDs derived from members;
- status uses the Claim Status Vocabulary and confidence uses `high | medium | low`;
- `review_status: agent_proposed` records an AI adjudication for human consideration and is not
  rendering or snapshot authority; only `human_approved` records are authoritative downstream;
- every rationale and caveat is evidence-bounded prose, not a similarity score; and
- registry history is recoverable from `accepted_in`/`reviewed_in` run records and Git history.

## Run Record

Path: `wiki/_claims/_reconciliation/runs/{run-id}.yaml`

```yaml
schema_version: 1
run_id: 2025-Q3
trigger: quarterly-integration
evidence_cutoff: 2025-09-30
assessment_as_of: YYYY-MM-DD
status: in_progress
review_mode: agent_adjudication | human_review
supersedes_run: null

source:
  infra_commit: abc1234
  content_commit: def5678
  concept_digests:
    concept-a: "sha256:..."
    concept-b: "sha256:..."

generator:
  version: 1
  neighbors_per_cluster: 10
  review_cap: 500
  shared_support_minimum: 2
  weights:
    text_similarity: 0.40
    shared_evidence: 0.30
    status_polarity: 0.15
    technical_vocabulary: 0.15

diagnostics:
  cross_concept_pairs: 1000
  pre_cap_candidates: 180
  emitted_candidates: 120
  shared_evidence_candidates: 8
  score_distribution:
    minimum: 0.31
    median: 0.56
    maximum: 0.94
  cap_excluded_shared_evidence: false

candidates:
  - id: cand_{first_16_hex_of_pair_sha256}
    left: concept-a#cluster-a
    right: concept-b#cluster-b
    theme: evaluation
    signals:
      text_similarity: 0.82
      shared_evidence_score: 0.50
      shared_supporting_papers: [paper-a, paper-b]
      status_compatible: true
      polarity_compatible: true
      status_polarity_score: 1.0
      technical_vocabulary_score: 0.33
      shared_terms: [speaker-similarity]
      aggregate_score: 0.88
    disposition: accepted
    relationship: refines
    registry_target: rel_{stable_slug}
    rationale: "Reviewed decision rationale."
    reconsideration_trigger: null
    proposal: null

review:
  completed_on: YYYY-MM-DD
  runtime: codex
  provider: openai
  agent: speech-generation-reconciliation-agent
  model: "exact runtime model ID"
  commit: abc1234
```

Run vocabulary:

- `trigger`: `quarterly-integration | large-integration-round | corrective-review`;
- `status`: `in_progress | finalized | superseded`;
- `review_mode`: `agent_adjudication | human_review`;
- `theme`: `evaluation | efficiency | speaker | controllability | robustness | codecs-language-modeling | streaming-agents | post-training`;
- `disposition`: `pending | accepted | rejected | deferred`.

Candidate rules:

- `left` is lexically smaller than `right`, regardless of directed relationship semantics;
- candidate IDs are `cand_` plus the first 16 hexadecimal characters of SHA-256 over the
  lexically ordered qualified-reference pair separated by a newline; ordering is deterministic
  for identical source digests and configuration;
- all component signals are present; shared paper and term lists are sorted and unique;
- `pending` is allowed only while the run is `in_progress`;
- a pending corrective-review candidate may carry an AI recommendation in `proposal`, containing
  `review_status: agent_proposed`, `relationship`, `registry_target`, and a complete `rationale`;
  these fields do not constitute the candidate's disposition;
- `accepted` requires a relationship, registry target, and rationale;
- an accepted candidate in a `human_review` run must target a `human_approved` registry record;
- `rejected` requires a rationale and no registry target;
- `deferred` requires a rationale and non-empty reconsideration trigger;
- a finalized run contains no pending candidates; and
- the review block is required when any candidate has a reviewed disposition.

For directed accepted relationships, the registry target—not `left`/`right` ordering—records source
and target semantics.
