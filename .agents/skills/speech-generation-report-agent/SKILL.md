---
name: speech-generation-report-agent
description: >-
  Create reproducible quarterly, trend, or on-demand venue research reports from immutable
  reconciliation snapshots while separating publication activity, evidence change, and adoption.
  Use when a bounded temporal or venue synthesis is requested after a valid snapshot exists.
---

# Speech Generation Report Agent

Generate reader-facing reports from immutable reconciliation snapshots. Never reconstruct a
historical report from the living claim graph.

Read before acting:

- `docs/design/temporal-reporting.md`
- `docs/schemas/snapshots.md`
- `docs/schemas/reconciliation.md`
- `docs/schemas/generation.md`
- `docs/writing-style.md`
- `docs/content.md`

## Repository Boundary

Work from the infra repository and resolve the standalone writable content checkout with
`python3 scripts/resolve_wiki_dir.py`. Never write the infra `wiki/` submodule.

Write only:

- `reports/quarterly/*.md`, `reports/trends/*.md`, or approved on-demand venue report paths;
- the reports index; and
- `log.md`.

Never write snapshots, reconciliation registry or runs, concept claim YAML, paper pages, concept
pages, metadata, or parsed sources.

## Inputs

Quarterly and venue reports require one published snapshot. Trend reports require at least two
published snapshots. Validate each snapshot and its digest before drafting.

Paper frontmatter may be read only to resolve human-readable titles, organizations, and links.
Every cited paper must already occur in the snapshot. The snapshot—not the live YAML or paper
page—is evidence authority.

## Quarterly Workflow

1. Validate snapshot ID, digest, source runs, retrospective mode, cutoff, activity window, and
   baseline cutoff.
2. Separate papers published in the activity window from the full eligible evidence set.
3. Compare the pre-quarter and through-quarter assessments encoded by the snapshot.
4. Identify decision-relevant new methods, strengthened or refined claims, contradictions,
   evaluation changes, and negative evidence.
5. Distinguish publication volume from evidence strength and adoption.
6. Draft the required structure in `docs/design/temporal-reporting.md` with representative
   `[[id|Name]]` citations.
7. Record snapshot ID/digest, dates, overlapping concept counts, corpus limits, and version-2
   generation provenance.
8. Validate, update the reports index, and log the operation.

Use explicit wording such as “retrospectively assessed on {date} using evidence published through
{cutoff}.” Never imply contemporaneous reviewer knowledge.

## Trend Workflow

Require at least two snapshots ordered by evidence cutoff. Fail without writing when fewer exist.
Compare like-for-like claim and method-family assessments, and disclose changes in schema, corpus,
or coverage that limit interpretation. Do not infer a trend from publication counts alone.

## Venue Workflow

Select papers by canonical venue and inclusive publication range from one validated snapshot.
Compare venue-specific contributions with the wider snapshot state. If the selection cannot support
theme and evidence synthesis, write no thin inventory page and report the insufficiency.

## Supersession

Do not substantively edit a published report. Produce a versioned successor when its snapshot is
superseded or a factual correction changes meaning. Record the prior report and reason, and add
reciprocal reader-facing navigation without altering the historical source snapshot.

## Provenance and Validation

Every report carries version-2 generation provenance with:

- `stage: report`;
- `mode: quarterly | trend | venue`;
- actual `RUNTIME`, `PROVIDER`, and exact `MODEL`;
- logical agent `speech-generation-report-agent`; and
- the infra commit used.

```yaml
generation:
  schema_version: 2
  date: YYYY-MM-DD
  stage: report
  mode: quarterly | trend | venue
  runtime: {RUNTIME}
  provider: {PROVIDER}
  agent: speech-generation-report-agent
  model: {MODEL}
  commit: {infra commit}
```

Validate that report dates match the snapshot, all citations are included, retrospective labeling
is explicit, required sections exist, supersession references resolve, the reports index is
updated, and `log.md` records the operation.

## Invariants

1. Reports read published snapshots as evidence authority.
2. Reports never edit snapshots or living claim state.
3. Quarterly reports separate activity from changed knowledge.
4. Attention, evidence strength, adoption, and consensus are distinct.
5. Trend reports require at least two comparable snapshots.
6. Venue reports are on demand and must synthesize more than a paper list.
7. Every factual conclusion traces to a snapshot assessment.
8. Published reports use explicit supersession rather than silent substantive edits.
9. All generated pages carry version-2 provenance.
