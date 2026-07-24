# Concept Rendering

Status: production specification  
Decision date: 2026-07-24
Production rollout: 2026-07-24

## Decision

Each `wiki/_claims/{slug}.yaml` file is concept-level data with two human-readable renderings:

1. **Overview** — a short state-of-the-art view for readers surveying many concepts.
2. **In Depth** — a detailed research view for readers who already know the concept and want to
   understand what the reviewed literature collectively shows.

These are not separate knowledge layers. Both are editorial projections of the same claim YAML.
The YAML remains the complete machine-readable representation and the source of truth.

The former Evidence Dossier format is retired for future renders. Human pages do not reproduce the
complete claim graph, paper inventory, reassessment queue, or data-hygiene fields. Readers or agents
that need exhaustive record-level access should use `wiki/_claims/{slug}.yaml`.

## Names and Paths

| Rendering | Reader-facing label | Production path | Internal `render_type` |
|-----------|---------------------|-----------------|------------------------|
| Overview | Overview | `wiki/concepts/{slug}.md` | `overview` |
| In Depth | In Depth | `wiki/concepts/{slug}-in-depth.md` | `in-depth` |

Quartz renders the frontmatter `title` through its Article Title component. Rendered Markdown
therefore contains no body H1; content begins with the abstract or introductory text, followed by
H2 sections.

The flat path scheme preserves existing concept links and avoids relying on directory-index
resolution. Both pages live under the `concepts` information architecture and link to each other.

The concept catalog uses:

```markdown
| Concept | Overview | In Depth | Papers | Last rendered |
```

The Concept cell is plain display text. Overview links to `concepts/{slug}` and In Depth links to
`concepts/{slug}-in-depth`.

## Shared Render Plan

The render agent reads the claim YAML and relevant paper frontmatter once, then prepares one shared
editorial plan before drafting either page. The plan is an execution aid, not a new authoritative
repository artifact.

The plan contains:

- a precise coverage statement;
- claim clusters ranked by concept centrality, decision impact, currentness, breadth, evidence
  strength, independence, and tension value;
- related clusters consolidated into reader-facing themes;
- the practically distinct method-family map;
- support-type and independence notes;
- contested, weakened, or scope-dependent findings;
- historical foundations and frontier directions that change current interpretation;
- representative named citations;
- the open questions most consequential to the concept.

Both renderings must agree on claim strength, scope, method-family relationships, and the direction
of contested evidence. They may differ in detail and citation density, but not in assessment.

## Overview Specification

**Reader question:** What should I know about the current state of this concept?

**Audience:** A speech researcher or engineer surveying the state of the field across 20 or more
concepts.

**Target length:** 700–1,100 words. Do not exceed 1,400 words without explicit user instruction.

**Selection threshold:** Only findings that materially change the reader's high-level mental model,
method choice, evaluation strategy, or interpretation of the field.

Required structure:

1. Abstract — definition, practical purpose, and current importance in two or three sentences.
2. Current State — three to six concise findings, with uncertainty expressed inline.
3. Method Landscape — at most four or five practically distinct families.
4. Key Trade-offs — three to five choices that matter for research or deployment.
5. Open Questions — three to five consequential unresolved questions.
6. Go Deeper — link to the In Depth rendering and optionally three representative papers.
7. Scope note — one compact paragraph stating the evidence boundary.

The Overview omits exhaustive claim coverage, paper inventories, detailed metric tables,
maintenance information, reassessment records, data-hygiene notes, and minor variants.

## In Depth Specification

**Reader question:** What does the reviewed research collectively show, and why?

**Audience:** A researcher already familiar with the concept who wants a detailed understanding
without reading every paper individually.

**Target length:** 2,500–6,000 words. Larger concepts may exceed this only when a coherent
single-page treatment remains usable; otherwise the agent should propose thematic subdivision.

**Selection threshold:** Cover every decision-relevant high- or medium-relevance finding, but
consolidate related claim clusters into coherent themes. Completeness is measured at the level of
important conclusions, not YAML records.

Required structure:

1. Findings at a Glance — six to ten substantive conclusions.
2. Scope — tasks, period, evidence types, coverage limits, duplicate handling, and survey role.
3. Research Landscape — relationships among major paradigms or method families.
4. Major Findings — five to twelve question- or conclusion-led narrative sections.
5. Where Findings Disagree — material contradictions, scope differences, and confounds.
6. How the Field Is Changing — history and frontier work only where they explain the current state.
7. Implications — consequences for system design, evaluation, deployment, or research.
8. Representative Reading Path — a curated route, not a complete bibliography.
9. Structured Source — link to `_claims/{slug}.yaml` for complete machine-readable provenance.

The Representative Reading Path uses a numbered list in an intentional learning sequence. Each
entry begins with a bold reader-oriented step or question, names one to three papers, and explains
why they belong at that point in the route. Do not use a Markdown table: reading-path explanations
need room to wrap on narrow screens, and wikilink pipes make tables fragile.

Quartz builds the right-side table of contents from body headings. Keep H2 labels stable and
structural. H3 labels are short topics or compact research questions, use no numeric prefixes, and
stay at 60 characters or fewer. Put the complete conclusion in the first paragraph—normally as a
bold `Current assessment:` sentence—rather than encoding a claim in the heading.

Use callouts as information hierarchy, not decoration:

- the Overview abstract callout is required;
- a warning callout may surface one critical contested finding or scope limitation;
- In Depth pages normally use prose plus `Findings at a Glance`, not a second decorative abstract;
- keep any generated page to at most two callouts.

Each major-finding section should establish:

- the current assessment in plain language;
- where independent evidence converges;
- the most important qualification or counterevidence;
- a small set of representative citations;
- what remains unresolved or what evidence would change the assessment.

The In Depth rendering must not contain exhaustive paper tables, raw claim IDs, YAML maintenance
fields, generic lists of paper IDs by confidence, or a complete render of the reassessment queue.
Queue items may inform reader-facing open questions when scientifically relevant.

## Citation and Traceability Policy

The Overview normally cites one to three representative papers per conclusion. The In Depth
rendering cites enough papers to demonstrate convergence, independence, and disagreement without
enumerating every supporting record.

Every factual evidence statement must still trace to:

```text
rendered statement
  → YAML claim cluster or method family
    → YAML paper claim entry
      → paper-page claim and source section
```

Selected citations do not imply that uncited supporting papers were ignored. The In Depth scope
note states that complete provenance lives in the YAML.

## Frontmatter and Staleness

Both pages include:

```yaml
concept: {slug}
render_type: overview | in-depth
source_digest_date: {YAML last_updated}
paper_count: {YAML paper_count}
generation:
  schema_version: 2
  stage: render
  mode: full | light
  runtime: claude-code | codex
  provider: anthropic | openai
  agent: speech-generation-render-agent
  model: {exact model ID}
  commit: {infra commit}
```

Each rendering is independently stale when its `source_digest_date` is older than the YAML
`last_updated`. The default concept render produces both from one shared plan.

## Prototype Record

Before production rollout, prototype renders:

- are written only to the infra repository root as
  `DRAFT_{SLUG}_OVERVIEW.md` and `DRAFT_{SLUG}_IN_DEPTH.md`;
- carry `draft: true` and no production generation block;
- do not update content-repository pages, indexes, logs, or YAML;
- do not establish production paths or trigger staleness checks;
- are compared for consistency, readability, length, citation quality, and evidence scope.

Prototype at least:

- one medium concept with clear architectural tensions;
- one large concept with many claim clusters and method families;
- one technically dense method concept.

The completed set was `speech-to-speech`, `evaluation-metrics`, `flow-matching`, and `rlhf-speech`.
After review found no blockers, all four were promoted to canonical pages and the production
catalog was migrated on 2026-07-24.

## Production Acceptance Criteria

Before replacing the existing renderer:

- the Overview can be read alongside 20 or more concept overviews without excessive repetition;
- the In Depth page teaches the concept rather than exposing the YAML structure;
- both pages agree on scope and assessment;
- representative citations are traceable to YAML evidence;
- no important contested or weakened finding disappears through consolidation;
- exact paper counts and digest dates match the YAML;
- the render health module validates both page types and reciprocal links;
- the agent compatibility module passes.
