# Claims Schema

The claim graph lives in `wiki/_claims/{slug}.yaml` — one file per concept slug. This is the
single source of truth for all rendered wiki output. Concept pages, evidence dossiers, and
overview are all generated from these files; they are never edited directly.

All rendered Markdown carries the version-2 provenance block defined in
`docs/schemas/generation.md`. The claim YAML itself records evidence state and staleness through
`last_updated`; integration-run runtime/model provenance is recorded in `wiki/log.md`.

## Full Schema

```yaml
concept: {slug}
last_updated: YYYY-MM-DD
paper_count: N          # number of entries under papers:

papers:
  - id: {paper_id}
    entry_date: YYYY-MM-DD           # when this entry was written or last force-rewritten
    year: YYYY
    venue: ACL          # cached from paper frontmatter for synthesis efficiency
    task: [TTS]
    architecture: [flow-matching]
    relevance: high | medium | low   # how central this concept is to the paper
    evidence_role:                   # what kind of evidence this paper contributes
      - core_evidence                # see Evidence Role Vocabulary below
    current_role: influential        # concept-scoped; see Current Role Vocabulary below
    method_family: [pure_nar_fm_tts] # links to method_families section
    claims:
      - claim_id: {slug_for_this_claim}
        role: supports               # see Claim Role Vocabulary below
        claim: "..."
        source: "§3.4, Table 2"      # section(s) of source paper where evidence appears
        evidence: "One-sentence supporting fact."
        confidence: high | medium | low
        relevance: high | medium | low  # how central this claim is to this concept
    limitations:
      - "General limitation of this paper relevant to the concept."
    caveats:
      - "Concept-specific caveat, distinct from the paper's general limitations."

claim_clusters:
  - id: {slug}
    claim: "Canonical field-level claim, generalizable across papers."
    status: strongly_supported       # see Claim Status Vocabulary below
    confidence: high | medium | low
    supporting_papers: [{paper_id}, ...]
    contradicting_papers: []
    refining_papers: []
    caveats: [...]
    last_reviewed: YYYY-MM-DD

method_families:
  - id: {slug}
    name: "Human-readable name"
    summary: "1–2 sentence description of what distinguishes this family."
    papers: [{paper_id}, ...]
    open_questions:
      - "Unresolved question specific to this method family."

reassessment_queue:
  - id: {paper_id or claim_id}
    type: paper_role | claim_status | method_family | benchmark_validity
    reason: "Why reassessment is needed."
    trigger: "What evidence would cause reassessment."
    due: YYYY-MM          # calendar fallback if trigger never fires
    current_assessment: {current_role or claim_status value}
    watch_for:
      - "Concrete sign to look for in incoming papers."

open_questions:
  - "Unresolved question surfaced by one or more papers."

trend_notes:
  - "Temporal observation about this concept, e.g. adoption increasing since 2024."
```

## Evidence Role Vocabulary

What kind of evidence this paper contributes to the concept.

| Value | Meaning |
|-------|---------|
| `core_evidence` | Directly advances the concept — new system, method, or result |
| `architecture_variant` | New placement or design variant within the concept |
| `acceleration_evidence` | Speed, NFE, latency, or RTF improvement |
| `control_evidence` | Speaker, prosody, emotion, language, or dialogue control |
| `evaluation_caution` | Exposes metric, benchmark, or comparison limitations |
| `historical_context` | Predecessor or lineage evidence; does not validate current paradigm |
| `negative_evidence` | Contradicts or weakens a claim |
| `infrastructure` | Dataset, codec, benchmark, toolkit, or objective used by others |

## Current Role Vocabulary

The living review's current interpretation of the paper's importance to **this concept**.
This is concept-scoped: the same paper may be `influential` in one concept YAML and `minor`
in another. Updated by the integration agent when reassessment triggers fire.

| Value | Meaning |
|-------|---------|
| `foundational` | Established the concept or a major branch; all later work builds on it |
| `influential` | Substantially shaped the concept; widely adopted or cited |
| `active_evidence` | Directly supports current claims with strong methodology |
| `frontier_probe` | Early or speculative — important if replicated, uncertain if not |
| `historical_context` | Important at publication time; does not validate the current paradigm |
| `minor` | Useful but not central; narrow scope or weak methodology |

## Claim Status Vocabulary

The aggregate status of a canonical concept-level claim across all supporting papers.

| Value | Meaning |
|-------|---------|
| `strongly_supported` | Backed by 3+ independent papers with fair evaluations |
| `emerging` | Backed by 1–2 papers, or with methodological caveats |
| `contested` | Mixed evidence; papers actively disagree |
| `weakened` | Was supported; later evidence reduced confidence |
| `superseded` | Replaced by a stronger or more precise claim |
| `historical` | True at publication time; no longer reflects the current paradigm |

## Claim Role Vocabulary

How a specific paper's evidence relates to a claim.

| Value | Meaning |
|-------|---------|
| `supports` | Provides positive evidence for the claim |
| `contradicts` | Provides evidence against the claim |
| `refines` | Adds nuance, scope limits, or precision to the claim |
| `complicates` | Adds caveats that make the claim harder to apply generally |
| `supersedes` | Replaces the claim with a stronger or more precise version |
| `historical_context` | Relevant to understanding the claim's origins, not its current validity |

## Claim Relevance Field

Every claim entry carries a `relevance` field (distinct from the paper-level `relevance`) that
records how central this specific claim is to the enclosing concept. All claims from the paper's
`## Claims` section are always included — none are dropped during Phase 1 extraction. The
integration agent sets `relevance` based on judgment: a claim about evaluation benchmark design
sitting in `flow-matching.yaml` is `low`; a claim about the flow matching objective is `high`.

Phase 2 synthesis uses this field to weight claim contribution to `claim_clusters`: only `high`
and `medium` relevance claims drive cluster promotion and status changes. `low` relevance claims
are present for completeness and cross-concept traceability but do not count toward thresholds.

The field can be manually edited or revised using full paper context without re-running Phase 1.

## Concept Page Source of Truth Rule

The `wiki/_claims/{slug}.yaml` file is the source of truth. Concept pages and evidence dossiers
are derived from it. Never update claim status, paper roles, or method family membership by
editing a concept page directly — all changes flow through the YAML. The integration agent
writes the YAML; the render agent reads it to produce pages.

## Staleness Detection

Every rendered concept page carries a `source_digest_date` frontmatter field recording the
`last_updated` date of the YAML at generation time. When `last_updated` in the YAML is newer
than `source_digest_date` on the concept page, the page is stale and should be queued for
the next render pass.
