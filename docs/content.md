# Content Stage

The content stage builds and maintains the wiki. It is a three-pass pipeline, each pass having
a single responsibility and clear input/output contract. Passes are independently triggerable
and can be run in any combination.

See also: [docs/schemas/metadata.md](schemas/metadata.md), [docs/schemas/claims.md](schemas/claims.md),
[docs/schemas/vocabulary.md](schemas/vocabulary.md), [docs/writing-style.md](writing-style.md)

---

## Pipeline Overview

| Stage | Agent | Input | Output | Cadence |
|-------|-------|-------|--------|---------|
| **Ingest** | `speech-generation-ingest-agent` | `raw/parsed/{id}/` | `wiki/papers/{id}.md` | per paper |
| **Integrate** | `speech-generation-integration-agent` | `wiki/papers/*.md` | `wiki/_claims/{slug}.yaml` | every ~25 papers |
| **Render** | `speech-generation-render-agent` | `wiki/_claims/{slug}.yaml` | `wiki/concepts/` Overview + In Depth | monthly or on demand |

Data flow:

```
wiki/papers/  →  wiki/_claims/  →  wiki/concepts/{slug}.md
                              →  wiki/concepts/{slug}-in-depth.md
                              →  wiki/overview.md (render)
```

Venue pages (`wiki/venues/`) are not part of the automated pipeline — they are generated
on demand for venues with enough ingested papers to support a real trend synthesis
(e.g. a full conference like Interspeech), rather than auto-updated on every ingest.

**Tier 1 papers** (full standard pages) use `speech-generation-ingest-agent`.
**Tier 2 papers** (lightweight stubs) use `speech-generation-lightweight-ingest-agent`.
Orchestration across batches is handled by `speech-generation-ingest-orchestrator`.

---

## Ingest Workflow

Per-paper, self-contained. No cross-paper knowledge required or produced.

1. **Check status** — only proceed if `status: accepted` in `raw/metadata/{id}.json`. If `status: review`, surface the review queue entry for user decision first.
2. **Check for duplicate** — verify `wiki/papers/{id}.md` does not already exist. Skip if it does.
3. **Read parsed paper** — read `raw/parsed/{id}/paper.md` in full: abstract, introduction, method, experiments, conclusion. Also read `raw/metadata/{id}.json` and `raw/parsed/{id}/references.json` (for in-corpus citation flags).
4. **Draft frontmatter** — fill all fields including `field_significance` (this must come before figure selection; see paper page template).
5. **Select figure** — only if `field_significance.type` includes `architectural-novelty`. Copy 0–2 figures from `raw/parsed/{id}/assets/` to `wiki/papers/assets/{id}/`. Prefer architecture/system diagrams over result plots.
6. **Write paper page** — fill every template field. Use `"not reported"` (never blank, never estimated) for missing values. Claims must each have an inline source citation `*(§N.N)*` or `*(§N.N, Table N)*`.
7. **Update `wiki/papers/index.md`** — add row: `| [[{id}]] | [{title}](papers/{id}.md) | {org} | {venue} | {year} | {tasks} | {architectures} | {date} |`
8. **Update `wiki/index.md`** — increment paper count only.
9. **Update `wiki/log.md`** — append bullet: `- ingest | {id} | {title} | {venue} {year} | runtime: {runtime} | provider: {provider} | model: {model}`
10. **Update metadata** — set `status: ingested`, `ingested_date`, append to `generation_history` in `raw/metadata/{id}.json`.
11. **Emit signal** — output `INGEST_RESULT` JSON on last line for the orchestrator.

The ingest agent writes exactly these files: `wiki/papers/{id}.md`, `wiki/papers/assets/{id}/*`,
`wiki/papers/index.md`, `wiki/index.md`, `wiki/log.md`,
`raw/metadata/{id}.json`. It never touches `wiki/concepts/`, `wiki/_claims/`, `wiki/overview.md`, or `wiki/venues/`.

---

## Integrate Workflow

Cross-paper. Reads paper pages, writes `wiki/_claims/` YAML only. No wiki pages are touched.

**Batch size:** up to 25 papers per pass. Run every ~25 ingested papers.

1. **Discover batch** — find papers with `status: ingested`, ordered by `ingested_date`. Take up to 25.
2. **Read paper pages** — for each paper, read frontmatter + `## Claims` section only (not full page). Collect `related_concepts` and structured claims.
3. **For each concept touched:**
   a. Read existing `wiki/_claims/{slug}.yaml`.
   b. Add or update paper entry: set `evidence_role`, initial `current_role`, `method_family`, structured `claims` (with `role`, `source`, `confidence`), `limitations`, `caveats`.
   c. Update `claim_clusters`: merge new paper claims into canonical clusters; promote `emerging` → `strongly_supported` if ≥3 independent papers support it; mark `contested` if contradicting papers exist; add new clusters for genuinely new claims.
   d. Update `method_families`: add paper to the appropriate family (or create a new family if a distinct architectural pattern emerges).
   e. Check `reassessment_queue`: for each queue item, test whether trigger conditions are met by this batch. If a trigger fires, update `current_role` (paper entry) or `status` (claim cluster) and remove the queue item. If `due` date has passed without a trigger, surface for human review.
4. **Validate YAML** — parse each touched file; verify top-level keys, `paper_count` matches `papers` list length, claim IDs are unique, supporting/contradicting paper IDs exist.
5. **Write updated `wiki/_claims/{slug}.yaml`** files.
6. **Log** — append to `wiki/log.md`: `- integrate | {N} papers | {M} concepts updated | {K} claims updated | {J} reassessments checked`

The integration agent writes exactly these files: `wiki/_claims/*.yaml`, `wiki/log.md`. It never writes wiki pages.

---

## Render Workflow

Page production. Derives all human-readable output from `wiki/_claims/` YAML. Stateless with
respect to history — always regenerates from current YAML state.

**Modes:**
- **Full** — regenerate page from scratch from YAML; produces a more coherent result; safe because YAML is self-contained.
- **Light** — update only sections affected by papers added since last generation; faster and cheaper.

**Invocation targets:**
- `--concept {slug}` — render one concept's Overview and In Depth pages
- `--all-concepts` — render all concept formats whose `source_digest_date` is behind YAML `last_updated`
- `--overview-only` — render only the short Overview format
- `--in-depth-only` — render only the detailed In Depth format
- `--prototype {slug}` — write draft formats to the infra root without changing canonical wiki files
- `--field-overview` — regenerate `wiki/overview.md` from all concept Overviews
- `--force` — render even if not stale

**Staleness check:** compare `source_digest_date` in each rendering's frontmatter against
`last_updated` in YAML. If the YAML is newer, that rendering is stale.

**Steps:**
1. Accept target parameter and mode.
2. For each target: read `wiki/_claims/{slug}.yaml`. Check staleness unless `--force`.
3. Build one shared editorial plan following `docs/design/concept-rendering.md`.
4. Render the Overview and In Depth pages from that plan.
5. Write `wiki/concepts/{slug}.md` and `wiki/concepts/{slug}-in-depth.md` with version-2
   `generation` frontmatter.
6. Update the rendered concept's row in `wiki/concepts/index.md`.
7. Optionally render `wiki/overview.md` from all Concept Overviews + YAML summaries.
8. Log: `- render | {N} concepts | formats: {overview|in-depth|both} | mode: {mode} | runtime: {runtime} | provider: {provider} | model: {model}` to `wiki/log.md`.

The production render agent writes exactly these files: `wiki/concepts/*.md`,
`wiki/concepts/index.md`, `wiki/overview.md`, `wiki/log.md`. Prototype mode writes only
`DRAFT_{SLUG}_OVERVIEW.md` and `DRAFT_{SLUG}_IN_DEPTH.md` in the infra root. It never reads
`raw/parsed/`, never writes `wiki/papers/`, and never writes `wiki/_claims/`.

---

## Page Templates

### Frontmatter List Formatting

List-type frontmatter fields (`task`, `architecture`, `conditioning`, `training`,
`datasets_train`, `datasets_eval`, `related_concepts`, `related_papers`) use YAML flow-sequence
syntax with **unquoted** scalars: `related_concepts: [flow-matching, zero-shot-tts]`, not
`["flow-matching", "zero-shot-tts"]` and not a block list. All slugs and vocabulary values in
this schema are plain kebab-case or alphanumeric tokens, so quoting is never required for valid
YAML. This is the canonical form for every ingest, re-ingest, and review write — pick it even
when writing only a single-element or empty list (`related_concepts: [flow-matching]`,
`task: []`).

`related_concepts` specifically drifted across three coexisting serializations (bracket
unquoted, bracket quoted, YAML block-list) before a 2026-07 normalization pass fixed the
existing corpus and closed the gap in agent specs — see `wiki/log.md` for the normalization
commit. Do not reintroduce quoted or block-list forms for any of these fields.

### Paper Page — Tier 1 (Full)

```markdown
---
id: "{id}"
title: {title}
authors: [{authors}]
organization: {org or null}
venue: {venue}
venue_type: {venue_type}
year: {year}
month: {month}
published_date: {YYYY-MM-DD}
ingested_date: {YYYY-MM-DD}
task: [{task list}]
architecture: [{architecture families}]
conditioning: [{conditioning types}]
training: [{training paradigm}]
model_size: {e.g. "330M params" | "not reported"}
codec_used: {e.g. "EnCodec 75Hz" | "none" | "not reported"}
datasets_train: [{training datasets}]
datasets_eval: [{evaluation/test sets}]
metrics:
  - name: MOS
    value: 4.21
    system: proposed
    testset: LJSpeech
code_available: true | false | null
demo_available: true | false | null
url: {arXiv abstract page or proceedings URL}
related_concepts: [{concept slugs}]
related_papers: [{paper IDs}]
field_significance:
  level: low | moderate | high | foundational
  type: [{one or more from field_significance type vocabulary}]
generation:
  schema_version: 2
  date: {YYYY-MM-DD}
  runtime: claude-code | codex
  provider: anthropic | openai
  agent: speech-generation-ingest-agent
  model: {model-id}
  commit: {7-char infra repo git hash}
---

> [!abstract] {venue} · {year} · {venue_type capitalized}
> **{First Author} et al.** ({organization}) · [→ Paper]({url}) · Demo: ✓/✗/? · Code: ✓/✗/?
>
> {The single most important thing this paper does.}

## Problem

{What gap or limitation does this paper address?}

## Method

{Architecture, conditioning, training objective, inference procedure. Model size and codec if reported.}

{If a figure was selected, embed it here after the first explanatory paragraph:}
![{Caption}](assets/{id}/figure-N.png)

## Key Results

{Headline numbers compared to baselines. Note benchmark conditions.}

## Novelty Assessment

{What is genuinely new vs. incremental?}

## Field Significance

{Use callout for foundational (`> [!important]`) or high (`> [!tip]`); plain prose for moderate/low.}

{level} — {1–3 sentences on field-level contribution.}

## Claims

{2–5 field-level propositions this paper provides evidence for, against, or complicates.
Each claim is one generalised sentence followed by a blockquote Evidence line with paper-local detail and a section citation.}

- **supports:** {Generalized claim sentence.}
  > *Evidence:* {Specific result, mechanism, comparison, dataset, or ablation.} *(§N.N, Table N)*
- **complicates:** {Generalized claim sentence.}
  > *Evidence:* {Specific limitation, failure case, or trade-off.} *(§N.N)*

## Limitations and Open Questions

{What the paper does not address. Critical limitations go in a `> [!warning]` callout first.}

## Wiki Connections

{Which concept pages does this paper most inform? Which prior papers does it build on or challenge? Use [[wikilinks]].}
```

### Paper Page — Tier 2 (Lightweight Stub)

For citation-discovery papers (`ingest_tier: 2`): foundation models, codecs, datasets, ASR systems,
and other non-primary-evidence papers included for context.

Survey papers use `## Scope and Coverage` instead of `## Context in Speech Generation`.

```markdown
---
id: "{id}"
title: {title}
authors: [{authors}]
organization: {org or null}
venue: {venue}
venue_type: {venue_type}
year: {year}
month: {month}
published_date: {YYYY-MM-DD}
ingested_date: {YYYY-MM-DD}
task: [{task list or empty}]
url: {url}
ingest_tier: 2
corpus_role: {corpus_role value}
related_concepts: [{slugs}]
generation:
  schema_version: 2
  date: {YYYY-MM-DD}
  runtime: claude-code | codex
  provider: anthropic | openai
  agent: speech-generation-lightweight-ingest-agent
  model: {model-id}
  commit: {7-char hash}
---

> [!abstract] {venue} · {year} · {venue_type capitalized}
> **{First Author} et al.** ({organization}) · [→ Paper]({url})
>
> {The single most important thing this paper does.}

> [!info] Citation Stub
> This paper is not a speech generation paper but is cited by the corpus. See Context in Speech Generation below for why it is relevant.

## Context in Speech Generation

{4–6 sentences. Why is this paper relevant as a reference? What does it provide to TTS/VC/SCA systems (backbone LLM, codec, dataset, ASR, metric)? Which corpus papers depend on it? Do not perform deep analysis.}

## Wiki Connections

{Which concept pages reference this paper? Which corpus papers cite it? Use [[wikilinks]].}
```

### Concept Overview (`wiki/concepts/{slug}.md`)

The short state-of-the-art rendering. Generated from `wiki/_claims/{slug}.yaml`; do not edit
directly. See `docs/design/concept-rendering.md` for selection and scope rules.

```markdown
---
slug: {slug}
concept: {slug}
render_type: overview
title: {Human-readable title}
aliases: [{alternative names}]
status: emerging | established | dominant | declining | contested | mature-infrastructure
last_reviewed: {YYYY-MM-DD}
source_digest_date: {YYYY-MM-DD}    # last_updated of the _claims YAML used
paper_count: {N}
generation:
  schema_version: 2
  date: {YYYY-MM-DD}
  stage: render
  mode: full | light
  runtime: claude-code | codex
  provider: anthropic | openai
  agent: speech-generation-render-agent
  model: {model-id}
  commit: {7-char hash}
---

> [!abstract]
> {2–3 sentences. What is this concept, where does it stand today, and why does it matter?}

## Current State

{Three to six concise findings that define the current state. Express scope and uncertainty inline.}

## Method Landscape

{At most four or five practically distinct families. Explain how they differ and why the
distinction matters; do not enumerate every variant.}

## Key Trade-offs

- **{Practical choice.}** {What the evidence implies and where it remains conditional.}

## Open Questions

- {Three to five consequential unresolved questions.}

## Go Deeper

Read [[concepts/{slug}-in-depth|{Concept Title}: In Depth]] for the detailed research landscape,
areas of convergence and disagreement, and representative reading path.

## Scope

{One compact paragraph: corpus size and period, important coverage limits, and the narrowest scope
at which the assessment should be read.}

---

_This page is generated from `wiki/_claims/{slug}.yaml` (digest date: {source_digest_date}).
For complete structured claims and paper-level provenance, use the source YAML._
```

### Concept In Depth (`wiki/concepts/{slug}-in-depth.md`)

The detailed reader-oriented rendering. It is comprehensive at the level of important findings,
not exhaustive at the level of YAML records.

```markdown
---
concept: {slug}
render_type: in-depth
title: "{Concept Title}: In Depth"
source_digest_date: {YYYY-MM-DD}
paper_count: {N}
generation:
  schema_version: 2
  date: {YYYY-MM-DD}
  stage: render
  mode: full | light
  runtime: claude-code | codex
  provider: anthropic | openai
  agent: speech-generation-render-agent
  model: {model-id}
  commit: {7-char hash}
---

# {Concept Title}: In Depth

Companion to the [[concepts/{slug}|Overview]]. This page explains what the reviewed research
collectively shows. Citations are representative; complete provenance is in
`wiki/_claims/{slug}.yaml`.

## Findings at a Glance

- **{Six to ten substantive conclusions.}**

## Scope

{Tasks, period, evidence types, coverage limitations, duplicate handling, and the role of surveys.}

## Research Landscape

{A reader-oriented map of the major paradigms or method families and their relationships.}

## What the Research Shows

### {Question- or conclusion-led theme}

**Current assessment:** {Plain-language conclusion at the narrowest supported scope.}

{Narrative explanation of convergence, independence, qualifications, and counterevidence.}

**Most informative evidence:** [[id|Name]], [[id|Name]].

**What remains unresolved:** {Evidence or experiment that would change the assessment.}

## Where Findings Disagree

### {Human-readable research question}

{Explain both sides, their scopes and confounds, and the current interpretation.}

## How the Field Is Changing

{Historical foundations and frontier directions only where they explain the current state.}

## Implications

- **{Design, evaluation, deployment, or research implication.}** {Evidence-bounded explanation.}

## Representative Reading Path

1. [[id|Name]] — {why read it}

## Structured Source

This page selects citations for human readability. The complete claim graph, paper roles, source
sections, caveats, and reassessment state are available in `wiki/_claims/{slug}.yaml`.
```

### Venue Page (`wiki/venues/{year}-{venue-slug}.md`)

Not part of the automated ingest/integrate/render pipeline — generated on demand, by request,
for a venue-year with enough ingested papers to support a real trend synthesis (e.g. a full
conference like Interspeech), not for a bucket of unrelated arXiv preprints. Covers: total
papers ingested, dominant tasks, dominant architectures, standout papers, and trends specific
to that community or organization. Include the version-2 `generation` block from
`docs/schemas/generation.md`.

### Comparison Page (`wiki/comparisons/{slug}.md`)

Generated in response to a query and filed back. Always includes:
- Frontmatter: `question`, `date`, `papers_included`, and the version-2 `generation` block
- A markdown table (one row per system/paper, columns for the dimensions being compared)
- A short interpretive paragraph after the table

---

## Query Workflow

When asked a research question:

1. Read `wiki/index.md` to find relevant pages.
2. Read relevant `wiki/concepts/*.md` and `wiki/_claims/*.yaml` pages.
3. Synthesize with citations using [[wikilinks]].
4. **File valuable answers back**: comparisons → `wiki/comparisons/`, temporal/trend analyses → `wiki/reports/` or the relevant concept page's trend summary.
5. Log: `- query | {question summary} | runtime: {runtime} | provider: {provider} | model: {model}`
   to `wiki/log.md`.

Any overview, brief, report, venue page, comparison page, or other Markdown page created or
substantively regenerated by an agent must use the same version-2 provenance schema. Index and log
files that are only incrementally updated do not receive a new page-level `generation` block; the
operation itself is recorded in `wiki/log.md`.

---

## Health Check Workflow

Run after any ingest pass to catch structural problems before they accumulate.

```bash
# Full ingest module check (all papers + index document)
.venv/bin/python scripts/health_check.py --module ingest

# Single-paper check (fast; skips corpus-wide checks like index validation)
.venv/bin/python scripts/health_check.py --module ingest --id {paper_id}
```

The ingest module checks every `wiki/papers/*.md` for:
- Frontmatter parses as valid YAML; all required fields present and non-null
- `id` field is a quoted string (arXiv float-parse bug: unquoted `1412.6980` → float `1412.698`)
- `field_significance` has `level` and `type` with valid vocabulary values
- Version-2 generation blocks contain runtime, provider, exact model, agent, date, and commit
- Abstract callout (`> [!abstract]`) and `## Wiki Connections` section present
- Tier 2 papers have `> [!info] Citation Stub` callout
- `## Claims` section present with `*(§N.N)*` citations on every bullet
- Figure assets referenced in body exist in `raw/parsed/{id}/assets/`
- `related_concepts` slugs exist in `wiki/concepts/`
- Paper appears in `wiki/papers/index.md` as `[[id]]` wikilink

Corpus-wide (full run only): index table column count, no duplicate IDs, no orphaned entries, no blank rows.

**Errors** must be resolved before continuing ingest. **Warnings** are advisory. Exit code 0 (clean) or 1 (errors).

Log: `- lint | {summary}` to `raw/pipeline_log.md`.

---

## Review Workflow

Use the review agent to fix structural gaps on existing Tier 1 pages without full re-ingest.
Appropriate when `health_check.py` reports errors on pages that already have complete prose
(`## Problem`, `## Method`, `## Key Results`, `## Novelty Assessment`, `## Limitations`, `## Wiki Connections`).

**Use the review agent when:** `field_significance` is missing, `## Claims` is absent or has
uncited bullets, frontmatter values are wrong (task, architecture, related_concepts, metrics),
figures are missing or incorrectly included.

**Re-ingest instead when:** multiple prose sections are absent or the content is fundamentally
wrong — the review agent preserves existing prose.

**Invocation:** one paper at a time, with a health check between papers.

```
Review paper {id}
```

The review agent:
- Audits the page against the full expected Tier 1 template
- Corrects frontmatter, adds missing sections, embeds warranted figures
- Does NOT rewrite prose unless a factual error is traceable to the parsed paper
- Does NOT touch `wiki/papers/index.md`, venue files, or `status`
- Updates `generation_history` in `raw/metadata/{id}.json` with `op: review` or `re-review`
- Logs to `wiki/log.md` with runtime, provider, and exact model provenance
- Emits `REVIEW_RESULT` JSON on last output line

Verify with `health_check.py --module ingest --id {paper_id}` after each review.

---

## Lint Workflow

Manual lint covers what the health check does not yet automate:

- Paper pages with `status: ingested` but no `wiki/papers/{id}.md` (corpus module, planned)
- Orphan paper pages not referenced by any concept's `_claims` YAML (integrate module, planned)
- `wiki/_claims/*.yaml` files that fail YAML parse (integrate module, planned)
- `paper_count` in YAML that does not match the `papers` list length (integrate module, planned)
- Concept pages whose `source_digest_date` is behind the YAML `last_updated` (render module, planned)
- Static count mismatches across `wiki/index.md`, `wiki/overview.md` (corpus module, planned)

Log: `- lint | {summary}` to `raw/pipeline_log.md`.

---

## Concept Page Registry

Canonical slugs for all concept pages in `wiki/concepts/`. Each has a corresponding YAML in
`wiki/_claims/`. The render agent will reject slugs not in this registry.

**Core methods:** `flow-matching` | `diffusion-tts` | `autoregressive-codec-tts` | `transformer-enc-dec-tts` | `gan-vocoder`

**Capabilities:** `zero-shot-tts` | `voice-conversion` | `multilingual-tts` | `emotion-synthesis` | `prosody-control` | `streaming-tts` | `spoken-language-model` | `speech-to-speech` | `instruction-conditioned-tts` | `singing`

**Foundations:** `neural-codec` | `self-supervised-speech` | `disentanglement` | `speaker-adaptation` | `rlhf-speech` | `fine-tuning`

**Evaluation:** `evaluation-metrics` | `subjective-evaluation`

When the integration agent encounters a `related_concepts` slug not in this registry, it flags
it to the user rather than creating an unsanctioned stub.

---

## Index Format (`wiki/index.md`)

```markdown
# Wiki Index

Last updated: {date} | Papers: {N} | Concepts: {N} | Reports: {N}

## Papers

| ID | Title | Org | Venue | Year | Task | Architecture | Ingested |
|----|-------|-----|-------|------|------|--------------|---------|
| [[{id}]] | [{title}](papers/{id}.md) | {org} | {venue} | {year} | {tasks} | {architectures} | {date} |

## Concepts

| Slug | Title | Paper count | Last updated |
|------|-------|-------------|-------------|

## Comparisons

| Slug | Question | Papers | Date |

## Reports

| Page | Type | Period | Papers covered |
```

---

## Log Formats

### `wiki/log.md` — Reader-facing changelog

Records operations that change visible wiki content. Entries in **reverse chronological order**
(newest date section at top). Append to today's section if it exists; otherwise insert a new
`## YYYY-MM-DD` section at the top.

```markdown
## 2026-06-20

- ingest | 2406.18009 | F5-TTS | ACL 2025
- review | 2406.18009 | F5-TTS | ACL 2025
- integrate | 25 papers | 8 concepts updated | 42 claims updated | 3 reassessments checked
- render | 5 concepts | mode: full | runtime: claude-code | provider: anthropic | model: claude-opus-4-8
- query | Comparison of zero-shot TTS systems by SPK-SIM
```

Entry types: `ingest`, `review`, `integrate`, `render`, `query`.

### `raw/pipeline_log.md` — Infra-facing operations log

Records pipeline operations that do not directly change wiki content. Same format. Entry types:
`filter`, `parse`, `discover`, `lint`, `review`.

```markdown
## 2026-06-20

- filter | arXiv cs.SD batch | 41 accepted, 12 review, 28 rejected
- parse | batch 31 | 40 papers | 0 failed
```
