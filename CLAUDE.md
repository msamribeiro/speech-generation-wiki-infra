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
  concepts/                   # Technology and method concept pages
  comparisons/                # Cross-paper comparison tables
  venues/                     # One summary page per conference/venue or org
  trends/                     # Year-on-year longitudinal analysis pages

scripts/
  fetch/                      # Fetchers: arxiv.py, arxiv_oai.py, acl.py, isca.py
  filter/                     # Filter agent: agent.py
  parse/                      # PDF pipeline: download_pdfs.py; convert_paper.py (Docling-based)
  ingest/                     # Wiki page generation (planned)

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
ingested  → wiki paper page written and all cross-references updated
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
---

# {Title}

**Paper:** [{url}]({url})

**One-sentence contribution:** {The single most important thing this paper does.}

## Problem

{What gap or limitation does this paper address? What did prior work fail to do?}

## Method

{How does the system work? Cover: input representation, architecture, conditioning mechanism, training objective, inference procedure. Include model size and codec choice if reported. Synthesize from reading — do not copy the abstract.}

## Key Results

{Headline numbers. Compare to baselines. Note which benchmarks were used and whether comparisons are fair (same test set, same conditions).}

## Novelty Assessment

{What is genuinely new vs. incremental? Is the contribution primarily architectural, training-recipe, data-scale, or engineering? Be honest.}

## Limitations and Open Questions

{What does the paper not address? What would a follow-up need to tackle?}

## Wiki Connections

{Which concept pages does this paper most inform? Which prior papers does it build on, challenge, or confirm? Use [[wikilinks]].}
```

### 2. Concept Page (`wiki/concepts/{slug}.md`)

```markdown
---
slug: {slug}
title: {Human-readable title}
aliases: [{alternative names used in the literature}]
related_concepts: [{slugs of related concept pages}]
last_updated: {YYYY-MM-DD}
---

# {Title}

## What it is

{Plain-language description of the concept and its role in speech synthesis.}

## Why it matters

{Why is this important in TTS/VC/SCA specifically? What problem does it solve that alternatives do not?}

## Current state of the art

{The leading approaches as of the most recently ingested papers. Cite specific papers with [[wikilinks]].}

## Key variants and sub-approaches

{The main sub-families. For each: what distinguishes it, which papers use it, and its trade-offs.}

## Comparison to alternatives

{How does this compare to competing paradigms? Trade-offs in quality, speed, data efficiency, controllability.}

## Year-on-year trajectory

{How has this concept evolved across the ingested papers? Note shifts in dominant approach, scale, or evaluation standard. Update as new papers arrive.}

## Open questions

{What is unresolved? Where do ingested papers disagree?}

## Papers

| ID | Title | Venue | Year | Key use of this concept |
|----|-------|-------|------|------------------------|
| [[id]] | Title | Venue | 2025 | Description |
```

### 3. Comparison Page (`wiki/comparisons/{slug}.md`)

Generated in response to a query and filed back. Always includes:
- Frontmatter: `question`, `date`, `papers_included`
- A markdown table (one row per system/paper, columns for the dimensions being compared)
- A short interpretive paragraph after the table noting what the comparison reveals

### 4. Venue Page (`wiki/venues/{venue-year}.md`)

One page per venue-year (e.g. `interspeech-2025.md`) or per org-year for technical reports (e.g. `google-2025.md`). Covers: total papers ingested, dominant tasks, dominant architectures, standout papers, and any trends specific to that community or organization.

### 5. Trend Page (`wiki/trends/{slug}.md`)

For longitudinal analysis across multiple years. Created when enough papers span 2+ years to support a meaningful comparison.

```markdown
---
slug: {slug}
title: {e.g. "Architecture trends in TTS 2023–2025"}
concepts: [{related concept slugs}]
years_covered: [2023, 2024, 2025]
last_updated: {date}
---

# {Title}

## Summary

{1–2 paragraph narrative of how this dimension has evolved.}

## Year-by-year breakdown

### {Year}
{What was dominant, what was emerging, what key papers defined the year.}

## Metric progression

{If measurable: how did benchmark numbers move year over year.}

## What drove the change

{Architectural shifts, dataset availability, compute scale, influence of adjacent fields.}
```

### 6. Overview (`wiki/overview.md`)

The evolving synthesis. Updated after every 10 ingests or after a significant query. Sections:

1. **Dominant paradigms** — what architectural approaches dominate each task today
2. **Emerging trends** — what is gaining traction in the most recent papers
3. **Points of tension** — where the literature actively disagrees
4. **Gaps** — what is underexplored relative to adjacent fields
5. **Key concept hubs** — the most-linked concept pages
6. **Year-on-year perspective** — trajectory summary once multiple years are covered

---

## Workflows

### Filter Workflow

When given a batch of candidate papers (from arXiv search, proceedings scrape, or manual addition):

1. Read title and abstract for each.
2. Assign `relevance_score` (0.0–1.0) based on fit to TTS / VC / SCA.
3. Write metadata JSON with `status: accepted` (score > 0.70), `status: review` (0.40–0.70), or `status: rejected` (< 0.40).
4. Append to `raw/review_queue.md` for all `status: review` papers.
5. Log: `## [YYYY-MM-DD] filter | {source} | {N} accepted, {M} review, {K} rejected`.

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

> **Multi-agent pipeline note:** When using the `speech-generation-ingest-agent` subagent, it performs steps 1–3 and 7–10 only. Steps 4–6 and 11–12 are the **integration agent's** responsibility — they run separately every ~25 papers. Do not instruct the per-paper agent to perform steps 4–6; it will refuse by design.

1. **Check `status`** — only proceed if `status: accepted`. If `status: review`, surface the review queue entry for user decision first.
2. **Read the PDF** — full text: abstract, introduction, method, experiments, conclusion. For technical reports, also read appendices on training data and evaluation.
3. **Write the paper page** — fill every template field. Use `"not reported"` (never blank, never estimated) for missing values.
4. **[Concept pass] Update concept pages** — identify 3–6 relevant concept pages. Update each: add the paper to the Papers table, and update "Current state of the art" if this paper advances it.
5. **[Concept pass] Create new concept pages** if the paper uses a concept not yet in the wiki. Seed with what the paper provides; mark `# TODO: expand` on sections needing more papers.
6. **[Concept pass] Update related paper pages** — read `raw/parsed/{id}/references.json`. For each reference with `in_corpus: true`, add a `[[wikilink]]` in the Wiki Connections section of both this paper and the cited paper. Out-of-corpus references are noted as plain text; they surface as corpus candidates via the Citation Discovery Workflow.
7. **Update `wiki/index.md`** — add paper entry and any new concept or trend pages.
8. **Update `wiki/log.md`** — append a bullet under today's `## YYYY-MM-DD` section: `- ingest | {id} | {title} | {venue} {year}`.
9. **Set `status: ingested`** and `ingested_date` in the metadata JSON.
10. **Update `wiki/venues/{venue-year}.md`**.
11. **[Concept pass] Update `wiki/overview.md`** if a pattern has visibly shifted.
12. **[Concept pass] Update relevant trend pages** if the paper extends a longitudinal analysis.

### Query Workflow

When asked a research question:

1. Read `wiki/index.md` to find relevant pages.
2. Read those pages.
3. Synthesize with citations using [[wikilinks]].
4. **File valuable answers back**: comparisons → `wiki/comparisons/`, trend insights → `wiki/trends/` or `overview.md`.
5. Log: `## [YYYY-MM-DD] query | {question summary}`.

### Lint Workflow

When asked to lint the wiki:

- Orphan paper pages not linked from any concept page
- Concept pages with fewer than 2 papers (merge candidates)
- Paper pages with `"not reported"` fields that could now be filled from related papers
- Concept "Current state of the art" sections that reference papers no longer the most recent
- Missing trend pages for concepts with papers spanning 2+ years
- Suggested new concept pages implicit in existing content but not yet created
- Suggested comparison pages based on clusters using the same benchmark
- Out-of-corpus papers cited by ≥ 3 corpus papers (prompt to run Citation Discovery Workflow)
- Log: `## [YYYY-MM-DD] lint | {summary}`.

### Citation Discovery Workflow

When asked to discover candidate papers via the citation graph:

1. Read `raw/citation_index.json`.
2. Filter to entries with `in_corpus: false`, sorted by `citation_count` descending.
3. Surface candidates cited by ≥ 3 corpus papers (or top 20 if fewer reach that threshold). For each: title (if known), arXiv ID or DOI, citation count, and the corpus papers that cite it.
4. Present the list to the user for approval. Approved candidates get a `raw/metadata/{id}.json` with `status: pending` and are run through the Filter Workflow. The filter agent will assign a relevance score; foundational papers (WaveNet, VITS, HiFi-GAN, VALL-E, etc.) should score high regardless of publication date.
5. Log: `## [YYYY-MM-DD] discover | {N} candidates surfaced, {M} added as pending`.

---

## Concept Pages to Seed Before First Ingest

Create these stubs before ingesting any paper so cross-references resolve immediately:

**Core methods:** `flow-matching.md`, `diffusion-tts.md`, `autoregressive-codec-tts.md`, `transformer-enc-dec-tts.md`, `gan-vocoder.md`

**Capabilities:** `zero-shot-tts.md`, `voice-conversion.md`, `multilingual-tts.md`, `emotion-synthesis.md`, `prosody-control.md`, `streaming-tts.md`, `spoken-language-model.md`, `instruction-conditioned-tts.md`

**Foundations:** `neural-codec.md`, `self-supervised-speech.md`, `disentanglement.md`, `speaker-adaptation.md`, `rlhf-speech.md`

**Evaluation:** `evaluation-metrics.md`, `subjective-evaluation.md`

---

## Index Format (`wiki/index.md`)

```markdown
# Wiki Index

Last updated: {date} | Papers: {N} | Concepts: {N} | Trends: {N}

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

## Trends

| Slug | Title | Years | Last updated |
|------|-------|-------|-------------|

## Venues

| Page | Venue | Year | Papers ingested |
|------|-------|------|----------------|
```

---

## Log Format (`wiki/log.md`)

Entries are grouped by date under `##` headings. Each entry is a bullet whose first token must be `ingest`, `integrate`, `filter`, `review`, `query`, `lint`, `discover`, or `parse`.

```markdown
## 2025-12-01

- ingest | google-audiopalm2-2025 | AudioPaLM 2 | technical-report 2025
- filter | Interspeech 2025 | 41 accepted, 12 review, 28 rejected

## 2025-12-02

- review | Interspeech 2025 | 28 borderline resolved → 15 accepted, 13 rejected
- query | Comparison of zero-shot TTS systems by SPK-SIM

## 2025-12-05

- lint | 2 orphan pages, 1 new concept suggested (streaming-inference)
```

When appending: if the current date already has a `##` section, add bullets under it. If not, create a new `## YYYY-MM-DD` section at the end of the file.

`filter` records the automated LLM pass output. `review` records the human decision on the borderline papers from `raw/review_queue.md`. Log both whenever the review queue is processed. `discover` records a Citation Discovery run. `parse` records a batch parse run.

---

## Invariants

Never violated under any circumstances:

1. **Never alter the content of source documents** — PDFs in `raw/papers/` and the substantive content of `raw/metadata/` JSONs are the source of truth. Pipeline scripts may write new files to `raw/` (PDFs, parsed output, logs) and update pipeline-state fields in metadata (`status`, `pdf_path`, `ingested_date`), but must never alter what a paper says or manually override filter scores without explicit user instruction.
2. **Never invent numbers** — if a metric is not in the paper, write `"not reported"`. Never estimate or hallucinate.
3. **Canonical vocabulary only** — map all terms to the controlled vocabulary. Note the authors' original term in parentheses.
4. **One paper, one page** — check the index before creating a new paper page. Deduplicate by arXiv ID first, then by title similarity.
5. **Cite specifically** — use [[wikilinks]] to paper IDs, not just venue or year.
6. **File answers back** — valuable query outputs must be written to the wiki, not left only in chat.
7. **Log everything** — every filter, ingest, query, and lint produces a log entry.
8. **Respect status** — never ingest a paper with `status: pending`, `review`, or `rejected` without explicit user instruction.
9. **Preserve provenance** — every metric value on a paper page must trace to a specific table or figure in the source PDF, not to another wiki page.
