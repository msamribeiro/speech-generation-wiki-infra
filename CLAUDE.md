# CLAUDE.md — Speech Synthesis Research Wiki

This file is the schema and operating contract for this wiki. Read it in full at the start of every session before touching any other file.

---

## Purpose

This wiki is a living systematic review of the state of the art in synthetic speech, covering **text-to-speech (TTS)**, **voice conversion (VC)**, and **spoken conversational agents (SCA)**. It ingests papers on a rolling basis, enabling both current-state snapshots and **year-on-year trend analysis**.

Coverage includes:
- Conference proceedings: Interspeech, ICASSP, ACL, EMNLP, NAACL, NeurIPS, ICLR, ICML, ASRU, SLT
- arXiv preprints (with or without venue acceptance)
- Technical reports from industry labs (Google, Microsoft, Meta, ElevenLabs, Apple, Amazon, etc.)
- Workshop papers at the above venues

The wiki is a **persistent, compounding artifact**. Every ingested paper enriches the existing knowledge base — updating concept pages, surfacing trends, and flagging contradictions. You never re-derive what is already compiled. You build on it.

---

## Environment

The project uses a `uv`-managed Python 3.12 virtual environment. Before running any script, activate it:

```bash
source .venv/bin/activate
```

If the environment does not exist yet (fresh clone), create it:

```bash
uv venv .venv --python 3.12
uv pip install -r requirements.txt
```

`requirements.txt` contains exact pinned versions. See `README.md` for full setup and dependency management instructions.

---

## Directory Structure

```
raw/                          # Source documents — PDFs and metadata are written here by pipeline scripts
  papers/                     # Downloaded PDFs (one per paper; not tracked in git)
  metadata/                   # One JSON file per paper (see schema below)
  parsed/                     # Extracted text and figures per paper (not tracked in git)
    {id}/                     # One directory per parsed paper
      paper.md                # Final LLM-ready Markdown (primary ingest target)
      metadata.json           # Title, authors, abstract, figure/table registries (Docling)
      references.json         # Structured reference list with in-corpus flags
      docling_native.json     # Docling's full internal document representation
      assets/                 # Figures (figure-N.png) and tables (table-N.csv, table-N.png)
  assets/                     # Figures or images extracted from papers
  citation_index.json         # Corpus-wide citation graph (rebuilt after each parse batch)
  review_queue.md             # Borderline papers awaiting manual review decision
  download_log.jsonl          # Append-only log of PDF download attempts (not tracked in git)

wiki/                         # LLM-generated and LLM-maintained markdown
  index.md                    # Master catalog of all wiki pages
  log.md                      # Append-only chronological log
  overview.md                 # Evolving synthesis and thesis (current state)
  papers/                     # One page per ingested paper
    assets/                   # Selected figures copied from raw/parsed/ during ingest
      {id}/                   # One subdirectory per paper that has embedded figures
        figure-N.png          # Architecture/system diagram selected by ingest agent
  concepts/                   # Technology and method concept pages
    _evidence/                # Machine-oriented concept evidence digests (YAML, one per concept slug)
  comparisons/                # Cross-paper comparison tables
  venues/                     # One summary page per conference/venue or org; named {year}-{venue-slug}.md
  reports/                    # Temporal synthesis layer
    monthly/                  # Monthly field reports (reports/monthly/YYYY-MM.md)
    quarterly/                # Quarterly field reports (reports/quarterly/YYYY-QN.md)
    yearly/                   # Annual state-of-field reports (reports/yearly/YYYY.md)

scripts/
  fetch/                      # Fetchers: arxiv.py, arxiv_oai.py, acl.py, isca.py
  filter/                     # Filter agent: agent.py (Anthropic SDK-based)
  parse/                      # PDF pipeline: download_pdfs.py; convert_paper.py (Docling-based); batch_convert.py
  discover/                   # Citation graph tools: citation_index.py
  ingest/                     # Reserved (empty — ingest pipeline runs via Claude Code agents, not scripts)

.claude/
  agents/                     # Claude Code subagent specs
    speech-generation-filter-agent.md
    speech-generation-ingest-agent.md
    speech-generation-ingest-orchestrator.md
    speech-generation-integration-agent.md

lib/                          # Shared library code (keyword_filter.py)
config/                       # keyword_filter.yaml, parsing.yaml
docs/                         # Design documents (FETCHERS_DESIGN.md, PARSING_PIPELINE_DESIGN.md)

README.md                     # Setup guide, script reference, pipeline overview
STATUS.md                     # Current corpus counts and next actions
CLAUDE.md                     # This file — the schema and operating contract
```

---

## Metadata Schema

Every paper in `raw/metadata/` must have a JSON file named `{id}.json`. The ID is the arXiv ID if available, otherwise `{venue-slug}-{year}-{sequence}` (e.g. `interspeech-2025-0412`) or `{org}-{slug}-{year}` for technical reports (e.g. `google-audiopalm2-2025`).

```json
{
  "id": "string",
  "title": "string",
  "authors": ["list of strings"],
  "organization": "string or null — primary affiliated org (e.g. Google, Microsoft, CMU)",
  "venue": "one of the venue values listed below",
  "venue_type": "one of: conference | workshop | preprint | technical-report",
  "year": 2025,
  "month": 11,
  "published_date": "YYYY-MM-DD — date of first public availability",
  "ingested_date": "YYYY-MM-DD or null — set on ingest",
  "integrated_date": "YYYY-MM-DD or null — set by integration agent after first integration pass",
  "url": "string — arXiv or proceedings URL",
  "pdf_path": "raw/papers/filename.pdf",
  "task": ["list — one or more of the task values listed below"],
  "relevance_score": 0.95,
  "relevance_note": "string — brief reason for score, especially for borderline cases",
  "status": "one of: pending | review | accepted | rejected | ingested"
}
```

### `venue` allowed values
`Interspeech` | `ICASSP` | `ACL` | `EMNLP` | `NAACL` | `NeurIPS` | `ICLR` | `ICML` | `ASRU` | `SLT` | `arXiv` | `technical-report` | `workshop` | `other`

### `status` lifecycle
```
pending   → filter agent assigns relevance score
review    → borderline (0.40–0.70): added to review_queue.md for human decision
accepted  → human confirmed relevant (or score > 0.70): ready to ingest
rejected  → human confirmed irrelevant (or score < 0.40): skip
ingested  → wiki paper page written; integration pass pending
integrated_date → set by integration agent after first integration pass (separate from status)
```

---

## Review Queue (`raw/review_queue.md`)

The filter agent appends to this file for every paper with `relevance_score` between 0.40 and 0.70. Format:

```markdown
## {id} | {title} | {venue} | score: {score}

**Authors:** {authors}
**Task guess:** {task}
**Reason for review:** {why the score is uncertain — what is ambiguous about this paper's relevance}
**Abstract excerpt:** {1–2 sentences from the abstract}

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)
```

After you mark a decision, update the metadata JSON `status` field accordingly. The ingest agent checks `status: accepted` before proceeding.

---

## Controlled Vocabulary

Use these exact terms throughout the wiki. When a paper uses a different label, map it to the canonical term and note the original in the paper page.

### Tasks
- `TTS` — text-to-speech, speech synthesis from text
- `VC` — voice conversion, speaker style transfer
- `SCA` — spoken conversational agent, speech LM dialogue system
- `codec` — neural audio codec (foundational, not a task itself)
- `evaluation` — primarily a benchmark, metric, or listening test methodology paper
- `singing` — singing voice synthesis (include if substantial overlap with TTS methods)

### Architecture Families
- `autoregressive-LM` — token-by-token LM decoding (VALL-E family, SoundStorm, etc.)
- `flow-matching` — continuous normalizing flows, rectified flows (Voicebox family)
- `diffusion` — DDPM / score-based / EDM diffusion
- `GAN` — adversarial vocoder or end-to-end GAN
- `VAE` — variational autoencoder
- `transformer-enc-dec` — non-autoregressive seq2seq (FastSpeech family)
- `hybrid` — combines two or more of the above in a single system

### Conditioning
- `text-conditioned`
- `speaker-conditioned` — requires reference audio or fixed speaker embedding
- `zero-shot` — generalizes to unseen speakers at inference from a short reference clip
- `multilingual`
- `emotion-conditioned`
- `prosody-conditioned`
- `instruction-conditioned` — natural language style or paralinguistic instructions
- `prompt-conditioned` — audio prompt at inference (may overlap with zero-shot)

### Training Paradigm
- `supervised`
- `self-supervised` — uses SSL representations (HuBERT, WavLM, EnCodec, etc.)
- `RLHF` — reinforcement learning from human or AI feedback
- `distillation` — knowledge distillation from a larger model
- `fine-tuning` — adapter or full fine-tuning of a pre-trained foundation model
- `continual-learning` — incremental learning without catastrophic forgetting

### Field Significance

Used in paper page frontmatter and `## Field Significance` prose section.

`level`: `low` | `moderate` | `high` | `foundational`

`type` (one or more):
- `engineering-integration` — applies existing techniques to a new context without architectural novelty
- `architectural-novelty` — introduces a new model structure, training objective, or inference procedure
- `empirical-benchmark` — primary contribution is evaluation at scale or on a new benchmark
- `conceptual-contribution` — reframes how the field thinks about a problem
- `negative-result` — shows that a widely-held belief or approach does not hold
- `evaluation-contribution` — introduces a new metric, test set, or listening test methodology
- `dataset-contribution` — primary contribution is a new dataset

### Evaluation Metrics (canonical names)
- `MOS` — mean opinion score (naturalness)
- `SMOS` — speaker similarity MOS
- `WER` — word error rate (intelligibility via ASR)
- `CER` — character error rate
- `SPK-SIM` — automatic speaker cosine similarity
- `UTMOS` — automatic MOS predictor (Saeki et al.)
- `DNSMOS` — Microsoft DNS MOS
- `EER` — equal error rate (anti-spoofing / speaker verification)
- `MUSHRA` — multiple stimuli with hidden reference and anchor
- `PESQ` — perceptual evaluation of speech quality
- `STOI` — short-time objective intelligibility
- `F0-RMSE` — pitch tracking error

---

## Page Types and Templates

### 1. Paper Page (`wiki/papers/{id}.md`)

```markdown
---
id: {id}
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
  - name: MOS
    value: 3.98
    system: baseline
    testset: LJSpeech
code_available: true | false | null
demo_available: true | false | null
url: {original paper URL — arXiv abstract page or proceedings URL}
related_concepts: [{concept slugs}]
related_papers: [{paper IDs}]
field_significance:
  level: low | moderate | high | foundational
  type: [{one or more from the field_significance type vocabulary}]
---

> [!abstract] {venue} · {year} · {venue_type capitalized}
> **{First Author} et al.** ({organization}) · [→ Paper]({url}) · Demo: ✓/✗/? · Code: ✓/✗/?
>
> {The single most important thing this paper does.}

## Problem

{What gap or limitation does this paper address? What did prior work fail to do?}

## Method

{How does the system work? Cover: input representation, architecture, conditioning mechanism, training objective, inference procedure. Include model size and codec choice if reported. Synthesize from reading — do not copy the abstract.}

{If an architecture figure was selected (see figure selection rules), embed it here after the first explanatory paragraph:}
![{Figure N caption from paper.}](assets/{id}/figure-N.png)

## Key Results

{Headline numbers. Compare to baselines. Note which benchmarks were used and whether comparisons are fair (same test set, same conditions).}

## Novelty Assessment

{What is genuinely new vs. incremental? Is the contribution primarily architectural, training-recipe, data-scale, or engineering? Be honest.}

## Field Significance

{For foundational or high papers, wrap the prose in a callout — use `> [!important]` for foundational, `> [!tip]` for high. For moderate or low, write plain prose.}

{level} — {1–3 sentences. What does this paper contribute to the field beyond its own results? Distinguish foundational works, strong empirical evidence, engineering integrations, and incremental variations. Note if this is primarily important as confirmatory evidence or as a cautionary/negative result.}

## Claims

{2–5 generalised propositions about speech generation that this paper provides evidence for, against, or complicates. Each claim must be one sentence, stated at the field level (not about this paper specifically), and reusable across multiple papers. See WRITING_STYLE.md §3 for the full rules.}

- {Claim 1.}
- {Claim 2.}

## Limitations and Open Questions

{What does the paper not address? What would a follow-up need to tackle? If there is a critical limitation that materially restricts the paper's claims or reproducibility, surface it first as a `> [!warning]` callout, then continue with the remaining limitations as prose or a list.}

## Wiki Connections

{Which concept pages does this paper most inform? Which prior papers does it build on, challenge, or confirm? Use [[wikilinks]].}
```

### 2. Concept Page (`wiki/concepts/{slug}.md`)

`status` allowed values: `emerging` | `established` | `dominant` | `declining` | `contested` | `mature-infrastructure`

```markdown
---
slug: {slug}
title: {Human-readable title}
aliases: [{alternative names used in the literature}]
status: emerging | established | dominant | declining | contested | mature-infrastructure
related_concepts: [{slugs of related concept pages}]
last_updated: {YYYY-MM-DD}
---

## Executive Summary

> [!abstract]
> {2–3 sentences. What is this concept, where does it stand today, and why does it matter? Write for a researcher who has 30 seconds. Update whenever the field-level picture changes materially.}

## Current Status

{status-label} — {1–2 sentences on current adoption rate, trajectory, and position relative to competing approaches.}

## Why This Matters

{What problem does this concept solve that alternatives do not? Why did the field develop or adopt it?}

## Core Idea

{Plain-language description. Assume familiarity with TTS/ML fundamentals but not this specific approach.}

## Methods and Variants

{The main sub-families within this concept. For each: what distinguishes it, which papers exemplify it, and its trade-offs. Use [[wikilinks]] for papers.}

## Major Claims

Claims are generalised propositions aggregated from paper evidence. The full claim registry with supporting paper lists is in `wiki/concepts/_evidence/{slug}.yaml`.

### Strongly Supported

- {Claim backed by ≥3 independent papers with fair evaluations.}
  Supporting: [[id]], [[id]]

### Emerging

- {Claim backed by 1–2 papers, or with methodological caveats.}
  Supporting: [[id]]

### Contested

> [!warning]
> {Claim where the evidence is mixed or papers actively disagree.}
> Supporting: [[id]] / Contradicting: [[id]]

## Relationship to Other Concepts

### Replaces or Supersedes
- [[concept_slug]] — {in what context}

### Extends or Builds On
- [[concept_slug]] — {how}

### Competes With
- [[concept_slug]] — {key trade-off between them}

### Commonly Paired With
- [[concept_slug]] — {why they appear together}

## Representative Papers

### Foundational
- [[id]] — {why foundational; 1 sentence}

### Influential
- [[id]] — {key contribution or impact}

### Recent Highlights
- [[id]] — {key contribution}

### Cautionary / Negative Evidence
- [[id]] — {what this paper challenges or complicates}

## Open Questions

- {What is unresolved?}
- {Where do papers disagree?}

## Trend Summary

{Short interpretive paragraph on how this concept has evolved across ingested papers. Note shifts in dominant approach, scale, evaluation standard, and adoption rate. Update as new papers arrive.}

## All Papers

| ID | Title | Venue | Year | Role in this concept |
|----|-------|-------|------|---------------------|
| [[id]] | Title | Venue | 2025 | {1-phrase description} |
```

### 3. Comparison Page (`wiki/comparisons/{slug}.md`)

Generated in response to a query and filed back. Always includes:
- Frontmatter: `question`, `date`, `papers_included`
- A markdown table (one row per system/paper, columns for the dimensions being compared)
- A short interpretive paragraph after the table noting what the comparison reveals

### 4. Concept Evidence Digest (`wiki/concepts/_evidence/{slug}.yaml`)

Machine-oriented intermediate artifact. One YAML file per concept slug. Maintained by the integration agent after each pass. Never shown directly to readers — it is the compact synthesis input for concept page regeneration and report generation. Enables scalable concept synthesis without loading all paper pages into one context window.

```yaml
concept: {slug}
last_updated: YYYY-MM-DD
paper_count: N

papers:
  - id: {paper_id}
    year: YYYY
    task: [TTS]
    architecture: [flow-matching]
    relevance: high | medium | low
    contribution_type: architectural-novelty  # from field_significance type vocabulary
    claims:
      - {Candidate claim extracted from this paper.}
    evidence:
      - {Key supporting fact or result, 1 sentence.}
    limitations:
      - {Limitation relevant to this concept.}

claim_clusters:
  - claim: {Canonical claim at the concept level, synthesised across papers.}
    status: strongly_supported | emerging | contested
    supporting_papers: [{paper_id}, ...]
    contradicting_papers: []
    notes: {Optional nuance.}

open_questions:
  - {Unresolved question surfaced by one or more papers.}

trend_notes:
  - {Temporal observation about this concept, e.g. "adoption increasing since 2024".}
```

**When to create:** when a concept reaches 5+ papers. **When to update:** every integration pass, for each concept touched. **When to use:** as primary input when rewriting a concept page; never load all related paper pages directly.

### 5. Report Page (`wiki/reports/{period}/{slug}.md`)

Temporal synthesis pages. Generated periodically, not after every ingest. Answer: *what changed during this period?* Do not list papers sequentially — synthesise change, direction, and momentum.

```markdown
---
period: YYYY-MM | YYYY-QN | YYYY
type: monthly | quarterly | yearly
concepts_covered: [{slugs}]
papers_included: N
date_generated: YYYY-MM-DD
---

# Speech Generation Report — {Period}

## Executive Summary

## Major Developments

## Emerging Concepts

## Architectural Shifts

## Capability Shifts

## Contested Claims

## Open Questions

## Surprises

## Representative Papers

## Forecast

## Appendix: Papers Included
```

### 6. Venue Page (`wiki/venues/{year}-{venue-slug}.md`)

One page per venue-year (e.g. `2025-interspeech.md`) or per org-year for technical reports (e.g. `2025-google.md`). Named `{year}-{venue-slug}` so that directory listings and the index sort chronologically. Covers: total papers ingested, dominant tasks, dominant architectures, standout papers, and any trends specific to that community or organization.

### 7. Overview (`wiki/overview.md`)

The evolving synthesis. Updated by the integration agent every ~25 ingested papers, or after a significant query that reveals a new pattern. Generated from concept pages, reports, and evidence digests — not directly from paper pages. Sections:

1. **Executive Summary** — 2–3 sentence field-level state
2. **Dominant paradigms** — what architectural approaches dominate each task today
3. **Emerging trends** — what is gaining traction in the most recent papers
4. **Points of tension** — where the literature actively disagrees
5. **Gaps** — what is underexplored relative to adjacent fields
6. **Key concept hubs** — the most-linked concept pages
7. **Year-on-year perspective** — trajectory summary once multiple years are covered
8. **Open questions** — unresolved debates aggregated across concepts

---

## Workflows

### Filter Workflow

When given a batch of candidate papers (from arXiv search, proceedings scrape, or manual addition):

1. Read title and abstract for each.
2. Assign `relevance_score` (0.0–1.0) based on fit to TTS / VC / SCA.
3. Write metadata JSON with `status: accepted` (score > 0.70), `status: review` (0.40–0.70), or `status: rejected` (< 0.40).
4. Append to `raw/review_queue.md` for all `status: review` papers.
5. Log: `- filter | {source} | {N} accepted, {M} review, {K} rejected` under today's `## YYYY-MM-DD` section in `raw/pipeline_log.md`.

### Ingest Workflow

**Running at scale — two-stage pipeline:**

| Stage | Agent | Cadence | Cost |
|-------|-------|---------|------|
| **Ingest** | `speech-generation-ingest-orchestrator` → `speech-generation-ingest-agent` | Every session; 5 papers/call | ~20–25k tokens/paper |
| **Integration** | `speech-generation-integration-agent` | Every ~25 ingested papers | ~60–120k tokens/run |

Ingest is self-contained per paper (writes the paper page + index/log/venue row + metadata). Integration is cross-paper reasoning (updates concept pages, adds back-links between papers, refreshes venue narratives and overview). Run them separately.

```
# Repeat until ingest queue is clear
→ speech-generation-ingest-orchestrator: "Ingest up to 5 papers"

# After every ~25 papers
→ speech-generation-integration-agent: "Run integration pass on last 25 papers"
```

**For a single paper** (by ID, PDF path, or URL):

> **Multi-agent pipeline note:** When using the `speech-generation-ingest-agent` subagent, it performs steps 1–3 and 7–10 only. Steps 4–6 and 11–12 are the **integration agent's** responsibility — they run separately every ~25 papers. Do not instruct the per-paper agent to perform steps 4–6; it will refuse by design. The integration agent also maintains `wiki/concepts/_evidence/` digests (step 12b) — these are not paper-agent territory.

1. **Check `status`** — only proceed if `status: accepted`. If `status: review`, surface the review queue entry for user decision first.
2. **Read the parsed paper** — read `raw/parsed/{id}/paper.md` (Docling output) in full: abstract, introduction, method, experiments, conclusion. Also read `raw/parsed/{id}/metadata.json` for structured fields and `raw/parsed/{id}/references.json` for in-corpus citations. For technical reports, also check appendices on training data and evaluation.
3. **Write the paper page** — fill every template field. Use `"not reported"` (never blank, never estimated) for missing values.
4. **[Integration agent] Update concept pages** — identify 3–6 relevant concept pages. Update each: add the paper to the Papers table, and update "Current state of the art" if this paper advances it.
5. **[Integration agent] Create new concept pages** if the paper uses a concept not yet in the wiki. Seed with what the paper provides; mark `# TODO: expand` on sections needing more papers.
6. **[Integration agent] Cross-link related papers** — for each in-corpus citation, add a `[[wikilink]]` in the Wiki Connections section of both this paper and the cited paper. Out-of-corpus references are noted as plain text; they surface as corpus candidates via the Citation Discovery Workflow.
7. **Update `wiki/index.md`** — add paper entry.
8. **Update `wiki/log.md`** — append a bullet under today's `## YYYY-MM-DD` section: `- ingest | {id} | {title} | {venue} {year}`.
9. **Set `status: ingested`** and `ingested_date` in the metadata JSON.
10. **Update `wiki/venues/{venue-year}.md`**.
11. **[Integration agent] Update `wiki/overview.md`** if a pattern has visibly shifted.
12. **[Integration agent] Update concept evidence digests** (`wiki/concepts/_evidence/{slug}.yaml`) — for each concept touched, merge concept-specific notes (claims, evidence, limitations) from this paper into the digest. Create the digest file if it does not exist and the concept now has ≥5 papers.

### Query Workflow

When asked a research question:

1. Read `wiki/index.md` to find relevant pages.
2. Read those pages.
3. Synthesize with citations using [[wikilinks]].
4. **File valuable answers back**: comparisons → `wiki/comparisons/`, temporal/trend analyses → `wiki/reports/` or the relevant concept page's trend summary section.
5. Log: `- query | {question summary}` under today's `## YYYY-MM-DD` section in `wiki/log.md`.

### Lint Workflow

When asked to lint the wiki:

- Orphan paper pages not linked from any concept page
- Concept pages with fewer than 2 papers (merge candidates)
- Paper pages with `"not reported"` fields that could now be filled from related papers
- Concept "Current state of the art" sections that reference papers no longer the most recent
- Concept evidence digests that are missing for concepts with ≥5 papers
- Concept evidence digests whose `paper_count` is behind the concept page Papers table
- Suggested new concept pages implicit in existing content but not yet created
- Suggested comparison pages based on clusters using the same benchmark
- Out-of-corpus papers cited by ≥ 3 corpus papers (prompt to run Citation Discovery Workflow)
- Log: `- lint | {summary}` under today's `## YYYY-MM-DD` section in `raw/pipeline_log.md`.

### Citation Discovery Workflow

When asked to discover candidate papers via the citation graph:

1. Read `raw/citation_index.json`.
2. Filter to entries with `in_corpus: false`, sorted by `citation_count` descending.
3. Surface candidates cited by ≥ 3 corpus papers (or top 20 if fewer reach that threshold). For each: title (if known), arXiv ID or DOI, citation count, and the corpus papers that cite it.
4. Present the list to the user for approval. Approved candidates get a `raw/metadata/{id}.json` with `status: pending` and are run through the Filter Workflow. The filter agent will assign a relevance score; foundational papers (WaveNet, VITS, HiFi-GAN, VALL-E, etc.) should score high regardless of publication date.
5. Log: `- discover | {N} candidates surfaced, {M} added as pending` under today's `## YYYY-MM-DD` section in `raw/pipeline_log.md`.

---

## Concept Page Registry

All concept stubs in `wiki/concepts/` and their canonical slugs. All stubs were seeded before the first ingest; new ones are added by the integration agent as needed.

**Core methods:** `flow-matching` | `diffusion-tts` | `autoregressive-codec-tts` | `transformer-enc-dec-tts` | `gan-vocoder`

**Capabilities:** `zero-shot-tts` | `voice-conversion` | `multilingual-tts` | `emotion-synthesis` | `prosody-control` | `streaming-tts` | `spoken-language-model` | `speech-to-speech` | `instruction-conditioned-tts`

**Foundations:** `neural-codec` | `self-supervised-speech` | `disentanglement` | `speaker-adaptation` | `rlhf-speech`

**Evaluation:** `evaluation-metrics` | `subjective-evaluation`

When the integration agent encounters a `related_concepts` slug not in this list, it flags it to the user rather than creating an unsanctioned stub.

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
|------|----------|--------|------|

## Reports

| Page | Type | Period | Papers covered |
|------|------|--------|---------------|

## Venues

| Page | Venue | Year | Papers ingested |
|------|-------|------|----------------|
| [[{year}-{venue-slug}]] | {Venue} | {year} | N |
```

---

## Log Format

Two separate logs serve two different audiences.

### `wiki/log.md` — Reader-facing changelog

Rendered on the public wiki site. Records only operations that change visible wiki content. Entry types: `ingest`, `integrate`, `report`, `query`.

```markdown
## 2025-12-01

- ingest | google-audiopalm2-2025 | AudioPaLM 2 | technical-report 2025
- integrate | 25 papers | 8 concepts updated | 3 digests updated | 14 cross-links added

## 2025-12-02

- query | Comparison of zero-shot TTS systems by SPK-SIM
```

### `raw/pipeline_log.md` — Infra-facing operations log

Lives in the infra repo only; never rendered on the site. Records pipeline operations that do not directly change wiki content. Entry types: `filter`, `review`, `parse`, `discover`, `lint`.

```markdown
## 2025-12-01

- filter | Interspeech 2025 | 41 accepted, 12 review, 28 rejected
- parse | batch 7 | 40 papers | 0 failed

## 2025-12-02

- review | Interspeech 2025 | 28 borderline resolved → 15 accepted, 13 rejected
- lint | 2 orphan pages, 1 missing evidence digest (flow-matching)
```

Both logs use the same format: date sections under `## YYYY-MM-DD`, one bullet per operation. When appending: if today's section already exists, add bullets under it; otherwise create a new section at the end.

---

## Invariants

Never violated under any circumstances:

1. **Never alter the content of source documents** — PDFs in `raw/papers/` and the substantive content of `raw/metadata/` JSONs are the source of truth. Pipeline scripts may write new files to `raw/` (PDFs, parsed output, logs) and update pipeline-state fields in metadata (`status`, `pdf_path`, `ingested_date`), but must never alter what a paper says or manually override filter scores without explicit user instruction.
2. **Never invent numbers** — if a metric is not in the paper, write `"not reported"`. Never estimate or hallucinate.
3. **Canonical vocabulary only** — map all terms to the controlled vocabulary. Note the authors' original term in parentheses.
4. **One paper, one page** — check the index before creating a new paper page. Deduplicate by arXiv ID first, then by title similarity.
5. **Cite specifically** — use [[wikilinks]] to paper IDs, not just venue or year.
6. **File answers back** — valuable query outputs must be written to the wiki, not left only in chat.
7. **Log everything** — `ingest`, `integrate`, `report`, and `query` operations log to `wiki/log.md`; `filter`, `parse`, `discover`, `lint`, and `review` operations log to `raw/pipeline_log.md`. Never mix the two.
8. **Respect status** — never ingest a paper with `status: pending`, `review`, or `rejected` without explicit user instruction.
9. **Preserve provenance** — every metric value on a paper page must trace to a specific table or figure in the source PDF, not to another wiki page.
10. **Evidence digests are derived, not authoritative** — never edit a digest directly to change a claim's status; update claim status only through a new integration pass that reads the underlying paper pages. The digest is a cache; the paper pages are the ground truth.
