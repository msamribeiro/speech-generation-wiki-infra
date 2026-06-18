# Speech Generation Wiki — Knowledge Architecture, Generation Strategy, and Implementation Notes

## Purpose

The Speech Generation Wiki should be treated as a **living systematic review** of speech-generation research, not merely as a repository of paper summaries.

Its long-term goal is to transform individual papers into field-level understanding across:

- Text-to-speech (TTS)
- Voice conversion (VC)
- Spoken conversational agents (SCA)
- Speech language models
- Speech-to-speech systems
- Evaluation methodology
- Speech generation architectures

The central architecture is:

```text
Evidence
  ↓
Claims
  ↓
Concepts
  ↓
Trends
  ↓
Findings
```

Each layer should have a clear role:

- **Paper pages** capture evidence.
- **Claims** capture reusable propositions supported by papers.
- **Concept pages** synthesize claims and evidence.
- **Reports** capture change over time.
- **Overview pages** summarize field-level understanding.

---

# 1. Core Knowledge Architecture

## 1.1 Paper Pages = Evidence

Paper pages answer:

> What happened in this paper?

They should capture the paper’s problem, method, results, novelty, limitations, and supported claims.

Paper pages are the evidence layer. They should be accurate, grounded, and structured enough to support downstream synthesis.

---

## 1.2 Claims = Reusable Propositions

Claims answer:

> What general proposition does this paper support, weaken, or complicate?

Claims should be extracted independently per paper, but later aggregated across papers.

Claims should not be treated as first-class human-facing pages initially. They are primarily an intermediate representation embedded in paper pages and synthesized into concept pages.

---

## 1.3 Concept Pages = Current Understanding

Concept pages answer:

> What does the field currently know or believe about this topic?

They should aggregate evidence and claims across many papers.

Concept pages should function as **research briefings**, not encyclopedia entries.

---

## 1.4 Reports = Change Over Time

Reports answer:

> What changed?

Reports should be generated periodically or by scope:

- Monthly reports
- Quarterly reports
- Yearly reports
- Venue reports
- Topic-specific reports

Reports are where most trend analysis should live.

---

## 1.5 Overview = Field-Level Understanding

The overview answers:

> What does all of this mean?

It should synthesize concepts, reports, claims, and findings into a coherent state-of-the-field picture.

---

# 2. Recommended Repository Structure

A clean structure could be:

```text
papers/
  One page per ingested paper.

concepts/
  Human-facing synthesis pages for major methods, systems, capabilities, and evaluation topics.

concepts/_evidence/
  Machine-oriented concept evidence digests used to regenerate concept pages.

reports/
  Periodic and scoped reports.

reports/monthly/
  Monthly field reports.

reports/quarterly/
  Quarterly field reports.

reports/yearly/
  Annual state-of-the-field reports.

venues/
  Venue-specific reports and summaries.

comparisons/
  Cross-paper comparison tables generated from structured queries.

overview.md
  High-level synthesis of the state of the field.

index.md
  Master catalog.

log.md
  Append-only operation log.
```

Do not create `claims/` as a top-level directory yet.

Claims should initially live in:

- Paper pages
- Concept evidence digests
- Concept pages
- Reports

Only create first-class claim or finding pages later if claims become a major human-facing product.

---

# 3. Paper Page Design

## 3.1 Purpose

Paper pages should be high-quality structured evidence records.

They should serve both:

- Human readers
- Downstream synthesis agents

A paper page should not try to explain the whole field. It should focus on what this specific paper contributes and what evidence it provides.

---

## 3.2 Recommended Paper Page Sections

Each paper page should contain:

```markdown
---
id:
title:
authors:
organization:
venue:
venue_type:
year:
month:
published_date:
ingested_date:
task:
architecture:
conditioning:
training:
model_size:
codec_used:
datasets_train:
datasets_eval:
metrics:
code_available:
demo_available:
url:
related_concepts:
related_papers:
---

# Title

**Paper:** URL

**One-sentence contribution:** ...

## Problem

## Method

## Key Results

## Novelty Assessment

## Field Significance

## Claims

## Limitations and Open Questions

## Wiki Connections
```

---

## 3.3 What Current Paper Summaries Already Do Well

The example paper summary already has several strengths:

- It starts with the research problem rather than merely listing the method.
- It explains the architectural contribution clearly.
- It separates empirical results from novelty assessment.
- It includes limitations and caveats.
- It links the paper to related concepts.
- It makes qualitative judgments, such as whether the contribution is primarily architectural, empirical, or an engineering integration.

This structure should mostly be preserved.

---

# 4. Claims Extraction

## 4.1 Definition

A claim is a generalized proposition about the field that a paper provides evidence for, against, or complicates.

A claim should be meaningful outside the context of the individual paper.

---

## 4.2 Claims Are Not

A claim is not:

- A metric value
- A benchmark result
- A paper contribution
- A model description
- A dataset description
- A summary of what the authors did

Bad examples:

```markdown
- The model achieves 4.31 MOS.
- The paper introduces a depth-wise decoder.
- The model uses Mimi.
- The authors train on LJSpeech.
```

These are results, methods, or implementation details, not claims.

---

## 4.3 Good Claims

Good examples:

```markdown
- Neural codec representations can reduce streaming latency compared to spectrogram-vocoder pipelines.
- Flow matching enables high-quality speech generation with fewer inference steps than diffusion.
- Speaker similarity remains difficult to preserve in multilingual zero-shot TTS.
- Discrete speech token prediction can replace continuous acoustic regression in modern TTS systems.
- Aggressive codec compression can reduce latency at the cost of perceptual quality.
```

---

## 4.4 Claims Extraction Rules

For each paper, generate 2–5 claims.

Each claim should:

- Be one sentence.
- Be a generalized statement about speech generation.
- Be supported by evidence from the paper.
- Avoid mentioning the paper, authors, or model name.
- Avoid raw metric values unless essential.
- Avoid speculative future predictions.
- Be reusable across multiple papers.
- Be possible to support, contradict, or refine with later evidence.

---

## 4.5 Candidate Claims vs. Canonical Claims

Paper-level claims should be treated as **candidate claims**.

They are extracted independently per paper.

Later, during concept synthesis, similar claims can be clustered into more canonical forms.

Example candidate claims:

```markdown
- Neural codecs enable low-latency speech synthesis.
- Codec representations reduce streaming latency.
- Discrete audio latents improve real-time speech generation.
```

These may later aggregate into a canonical concept-level claim:

```markdown
Neural codec representations enable lower-latency speech generation than traditional spectrogram-vocoder pipelines.
```

---

## 4.6 Do Not Force Claim IDs During Paper Ingestion

Avoid requiring paper ingestion agents to emit canonical claim IDs such as:

```yaml
supports_claims:
  - codec-latents-enable-streaming
```

This is brittle because the claim ontology will evolve.

Instead:

- Extract local candidate claims per paper.
- Normalize and cluster claims later during concept synthesis.

---

# 5. Suggested Prompt for Claims Extraction

Use this instruction inside paper-summary generation:

```markdown
## Claims Extraction Instructions

After writing the paper summary, generate a short `## Claims` section.

A claim is not a metric value, benchmark result, paper contribution, or model description. A claim is a generalized proposition about speech generation that this paper provides evidence for, against, or complicates.

Generate 2–5 claims.

Each claim must:

- Be one sentence.
- Be phrased as a general statement about speech generation.
- Be supported by evidence from the paper.
- Avoid mentioning the paper, authors, or model name.
- Avoid raw metric values unless necessary.
- Avoid speculative future predictions.
- Be meaningful outside the context of this specific paper.
- Be stated at a level where multiple papers could support, contradict, or refine it.

Good examples:

- Neural codec representations can reduce streaming latency compared to spectrogram-vocoder pipelines.
- Flow matching enables high-quality speech generation with fewer inference steps than diffusion.
- Speaker similarity remains difficult to preserve in multilingual zero-shot TTS.
- Discrete speech token prediction can replace continuous acoustic regression in modern TTS systems.

Bad examples:

- The proposed model achieves 48.99 ms latency.
- The paper introduces a depth-wise decoder.
- The model uses Mimi.
- The authors train on LJSpeech.

Output format:

## Claims

- Claim 1.
- Claim 2.
- Claim 3.
```

---

# 6. Field Significance

## 6.1 Purpose

Add a `Field Significance` section to paper pages.

This helps downstream agents distinguish between:

- Foundational papers
- Incremental papers
- Engineering integrations
- Negative or cautionary evidence
- Strong empirical confirmations
- Papers that are interesting but not field-shaping

---

## 6.2 Suggested Labels

Possible field-significance categories:

```yaml
field_significance:
  level: low | moderate | high | foundational
  type:
    - engineering integration
    - architectural novelty
    - empirical benchmark
    - conceptual contribution
    - negative result
    - evaluation contribution
    - dataset contribution
```

---

## 6.3 Human-Readable Section

Example:

```markdown
## Field Significance

Moderate. The paper demonstrates an interesting low-latency codec-native streaming architecture, but quality remains below stronger non-streaming baselines. Its main value is evidence for the latency-quality trade-off in non-autoregressive codec-based TTS.
```

---

# 7. Concept Pages

## 7.1 Purpose

Concept pages should be the main synthesis layer.

They should answer:

> What does the field currently know about this concept?

Concept pages should not simply list papers.

They should interpret the literature.

---

## 7.2 Concept Pages as Research Briefings

Concept pages should function like research briefings.

They should answer:

- What is this concept?
- Why does it matter?
- How important is it today?
- What problems does it solve?
- What papers are representative?
- What claims are strongly supported?
- What claims are emerging?
- What claims are contested?
- What remains unresolved?
- How is this concept changing over time?

---

## 7.3 Recommended Concept Page Structure

```markdown
# Concept Name

## Executive Summary

## Current Status

## Why This Matters

## Problem It Solves

## Core Idea

## Methods and Variants

## Major Claims

### Strongly Supported

### Emerging

### Contested

## Representative Papers

### Foundational

### Influential

### Recent

### Recommended Starting Points

## Relationship to Other Concepts

### Replaces

### Extends

### Competes With

### Commonly Paired With

## Open Questions

## Trend Summary

## Related Papers
```

---

## 7.4 Current Status

Each concept page should include a status classification.

Suggested statuses:

- **Emerging** — growing but not yet dominant.
- **Established** — widely used and stable.
- **Dominant** — central to current frontier systems.
- **Declining** — receiving less attention or being replaced.
- **Contested** — active disagreement or mixed evidence.
- **Mature infrastructure** — no longer novel but still widely used.

Example:

```markdown
## Current Status

Emerging dominant paradigm. Flow matching has rapidly gained adoption in modern TTS and speech generation systems, especially where lower inference cost and simpler sampling are valued.
```

---

## 7.5 Major Claims Section

Concept pages should aggregate candidate claims from paper pages.

Suggested structure:

```markdown
## Major Claims

### Strongly Supported

- Neural codec representations reduce latency in streaming speech generation.
  - Supporting papers: [[2604.12438]], ...

### Emerging

- Codec-native generation may replace spectrogram-vocoder pipelines in latency-sensitive systems.
  - Supporting papers: ...

### Contested

- Codec-native systems can match traditional pipelines in perceptual quality.
  - Supporting evidence: ...
  - Contradicting evidence: ...
```

---

## 7.6 Relationship to Other Concepts

Add explicit graph-like relationships.

Example:

```markdown
## Relationship to Other Concepts

### Commonly Paired With

- [[neural-codec]]
- [[transformer-enc-dec-tts]]

### Competes With

- [[diffusion]]
- [[autoregressive-codec-tts]]

### Replaces

- Continuous mel-spectrogram regression in some low-latency systems.

### Enables

- [[streaming-tts]]
- [[zero-shot-tts]]
```

This turns the wiki into a navigable concept graph rather than a folder tree.

---

## 7.7 Representative Papers

Do not list all papers equally.

Group papers by role:

```markdown
## Representative Papers

### Foundational

### Influential

### Recent

### Recommended Starting Points

### Cautionary / Negative Evidence
```

This helps readers know where to start.

---

## 7.8 Open Questions

Every concept page should include open questions.

Example:

```markdown
## Open Questions

- Can codec-native generation match traditional vocoder pipelines in perceptual quality?
- How much compression is possible before perceptual quality degrades?
- Which codec layers matter most for speaker similarity and prosody?
- Are observed gains due to the codec representation itself or surrounding architectural choices?
```

Open questions are especially valuable for:

- PhD students
- Grant writing
- Research planning
- Identifying genuinely novel work

---

## 7.9 Trend Summary on Concept Pages

Each concept page should include a short trend summary.

Example:

```markdown
## Trend Summary

Neural codec adoption has increased steadily since 2024 and is now central to many streaming and zero-shot TTS systems. The concept has shifted from a representation choice to a foundational architectural component in modern speech generation.
```

This summary should be short and interpretive.

It does not need to contain every statistic.

---

# 8. Concept Evidence Digests

## 8.1 Purpose

Do not regenerate concept pages by loading all relevant paper pages into one context window.

Instead, maintain compact machine-oriented evidence files per concept.

Example:

```text
concepts/_evidence/neural-codec.yaml
concepts/_evidence/flow-matching.yaml
concepts/_evidence/streaming-tts.yaml
```

These are not polished human-facing pages.

They are intermediate synthesis artifacts.

---

## 8.2 Suggested Evidence Digest Contents

A concept evidence digest could contain:

```yaml
concept: neural-codec
last_updated: 2026-06-01

paper_count: 87

papers:
  - id: 2604.12438
    year: 2026
    task: [TTS]
    architecture: [transformer-enc-dec]
    relevance: high
    contribution_type: engineering integration
    claims:
      - Neural codec representations can enable ultra-low-latency streaming speech synthesis.
      - Aggressive codec compression can reduce latency at the cost of perceptual quality.
    evidence:
      - Proposed codec-native streaming TTS using Mimi.
      - Reports sub-50 ms time-to-first-byte.
      - English MOS remains below baseline.
    limitations:
      - Single-speaker only.
      - Quality-latency trade-off remains unresolved.

claim_clusters:
  - claim: Neural codecs reduce latency in streaming speech generation.
    status: strongly_supported
    supporting_papers: [2604.12438, ...]
    contradicting_papers: []
    notes: ...

  - claim: Codec-native generation matches traditional vocoder pipelines in perceptual quality.
    status: contested
    supporting_papers: [...]
    contradicting_papers: [2604.12438]
    notes: ...

open_questions:
  - How much codec compression is possible before perceptual quality degrades?
  - Which RVQ layers matter most for speaker similarity?

trend_notes:
  - Increasing use of codec-native generation in streaming systems.
  - Growing interest in replacing vocoders with neural codec decoders.
```

---

## 8.3 Why Evidence Digests Matter

Evidence digests solve the context-window problem.

Instead of:

```text
800 paper summaries → concept page
```

Use:

```text
paper summaries → concept-specific evidence notes → evidence digest → concept page
```

Each layer is compact.

---

# 9. Generating Concept Pages

## 9.1 Scenario 1: Initial Build from 800 Paper Summaries

Do not load all 800 summaries at once.

Use a staged pipeline:

```text
1. Read paper summaries.
2. Filter papers by related_concepts.
3. For each concept, extract concept-specific notes from each relevant paper.
4. Cluster claims.
5. Build or update concept evidence digest.
6. Generate the human-facing concept page from the digest.
```

---

## 9.2 Concept-Specific Note Extraction

For each paper relevant to a concept, extract a compact note:

```yaml
paper_id:
concept:
relevance: low | medium | high
role:
  - foundational
  - application
  - comparison
  - negative evidence
  - evaluation
claims:
evidence:
limitations:
metrics:
relationships:
```

This makes each paper’s contribution to the concept explicit.

---

## 9.3 Claim Clustering

After extracting concept-specific notes, cluster similar claims.

Example input:

```markdown
- Neural codecs enable low-latency speech synthesis.
- Codec representations reduce streaming latency.
- Discrete audio latents improve real-time speech generation.
```

Clustered canonical claim:

```markdown
Neural codec representations enable lower-latency speech generation than traditional spectrogram-vocoder pipelines.
```

---

## 9.4 Concept Page Generation Inputs

To generate a concept page, use:

- Existing concept evidence digest
- Clustered claims
- Representative papers
- Open questions
- Trend notes
- Existing concept page, if updating

Do not use all paper summaries directly unless the concept has very few papers.

---

## 9.5 Scenario 2: Updating Existing Concept Page with 20 New Papers

Use incremental updates.

Inputs:

- Existing concept page
- Existing concept evidence digest
- New paper summaries
- Concept-specific notes from new papers

Process:

```text
1. Identify which new papers touch the concept.
2. Extract concept-specific notes from those papers.
3. Merge new notes into the concept evidence digest.
4. Update claim clusters.
5. Detect what changed:
   - new claims
   - strengthened claims
   - weakened claims
   - contested claims
   - new limitations
   - new representative papers
6. Update only affected sections of the concept page.
```

---

## 9.6 Concept Update Rules

When updating a concept page, the agent should explicitly determine:

- What is unchanged?
- What has become more strongly supported?
- What has become weaker or contested?
- What is genuinely new?
- What should be promoted to representative status?
- What should be removed or demoted?
- What open questions changed?

Avoid rewriting the entire page unless necessary.

---

# 10. Reports and Trends

## 10.1 Trends Are Not a Separate Page Type

Do not create a top-level `trends/` directory unless there is a clear need.

Trends should live in:

- Concept page trend summaries
- Monthly reports
- Quarterly reports
- Yearly reports
- Venue reports
- Overview pages

---

## 10.2 Definition of a Trend

A trend is a statement of change over time.

Examples:

```markdown
- Flow matching adoption increased between 2024 and 2026.
- Neural codecs displaced mel-spectrogram pipelines in latency-sensitive systems.
- Speech LLM papers became more common than traditional TTS papers.
- MOS reporting decreased while WER reporting increased.
```

Trends are not simply concepts.

They are temporal observations.

---

## 10.3 Four Kinds of Trends

### Concept Trends

Examples:

- Flow Matching
- Neural Codec
- Speech LLM

Question:

> Is usage growing, stable, or declining?

---

### Capability Trends

Examples:

- Zero-shot TTS
- Voice Conversion
- Emotion Control
- Streaming TTS

Question:

> What capabilities are researchers prioritizing?

---

### Architectural Trends

Examples:

- Diffusion
- Flow Matching
- Autoregressive Codec Models
- Transformer Encoder-Decoder

Question:

> What approaches are replacing others?

---

### Claim Trends

Examples:

```markdown
2024: Neural codecs are promising.
2025: Neural codecs outperform traditional pipelines in some settings.
2026: Neural codecs are becoming standard in frontier systems.
```

Question:

> How are the field’s beliefs changing?

---

# 11. Report Design

## 11.1 Purpose

Reports are the temporal synthesis layer.

They should answer:

> What changed during this period or venue?

Reports should not become lists of paper summaries.

---

## 11.2 Report Types

Recommended report types:

```text
reports/monthly/2026-05.md
reports/quarterly/2026-q2.md
reports/yearly/2026.md
venues/interspeech-2026.md
venues/icassp-2026.md
```

Venue pages can be treated as scoped reports.

---

## 11.3 Recommended Report Structure

```markdown
# Speech Generation Report — Month YYYY

## Executive Summary

## Corpus Growth

## Major Developments

## Emerging Concepts

## Declining Concepts

## Architectural Shifts

## Capability Shifts

## Notable Claims

## Open Questions

## Surprises

## Representative Papers

## Forecast

## Appendix: Papers Included
```

---

## 11.4 Report Generation Inputs

A report should be generated from:

- Papers ingested during the period
- Concept evidence deltas
- Existing concept summaries
- Previous report
- Metadata counts
- Claim clusters
- Open questions extracted from new papers

Do not generate reports by reading the entire corpus.

---

## 11.5 Report Generation Rules

Reports should focus on:

- Change
- Direction
- Momentum
- Newly strengthened claims
- Newly contested claims
- Emerging open questions
- Surprises

Avoid:

```markdown
Paper A does X. Paper B does Y. Paper C does Z.
```

Prefer:

```markdown
The field showed increased interest in codec-native streaming architectures, with several new papers bypassing traditional vocoders in favor of neural codec decoders.
```

---

# 12. Overview Page

## 12.1 Purpose

The overview is the highest-level synthesis page.

It should answer:

> What does the literature collectively say about the state and direction of speech generation?

---

## 12.2 Recommended Overview Structure

```markdown
# Overview: State of the Art in Speech Generation

## Executive Summary

## Dominant Paradigms

## Emerging Trends

## Points of Tension

## Gaps

## Key Concept Hubs

## Year-on-Year Perspective

## Findings

## Open Questions

## Forecast
```

---

## 12.3 Overview Generation Inputs

The overview should be generated from:

- Latest concept pages
- Latest yearly reports
- Latest quarterly reports
- Major venue reports
- Established findings
- Major open questions

The overview should not usually read paper summaries directly.

Use papers only for spot checks or citations.

---

## 12.4 Overview Generation Rules

The overview should:

- Synthesize rather than summarize.
- Focus on the field rather than individual papers.
- Identify major shifts.
- Identify unresolved debates.
- Distinguish established findings from emerging evidence.
- Avoid overclaiming beyond available evidence.

---

# 13. Findings Layer

## 13.1 Purpose

A findings layer may eventually be useful.

Findings are high-level conclusions supported by aggregated evidence.

Examples:

```markdown
- Neural codecs have become foundational infrastructure for modern speech generation.
- Flow matching is increasingly replacing diffusion in TTS systems.
- Evaluation remains a bottleneck because subjective metrics are expensive and objective metrics remain imperfect.
```

---

## 13.2 Where Findings Should Live

Initially, findings can live in:

- Overview page
- Yearly reports
- Concept pages

Do not create a `findings/` directory immediately.

Create one later only if findings become a major first-class output.

---

## 13.3 Finding Categories

Possible categories:

```markdown
## Established Findings

## Emerging Findings

## Contested Findings

## Retired Assumptions

## Open Debates
```

---

# 14. Scaling Strategy

## 14.1 Main Constraint

The main generation challenge is that concept pages, reports, and overviews cannot be generated by loading all relevant papers into a single context window.

The solution is not larger context windows.

The solution is layered intermediate artifacts.

---

## 14.2 Layered Synthesis Pipeline

Use:

```text
Full paper
  ↓
Paper summary
  ↓
Concept-specific evidence note
  ↓
Concept evidence digest
  ↓
Concept page
  ↓
Report
  ↓
Overview
```

Each layer consumes the compact output of the layer below.

---

## 14.3 General Rule

Never ask an agent to synthesize from the full corpus when a compact intermediate artifact can be used.

---

# 15. Initial Corpus Build Pipeline

For an initial corpus of approximately 800 paper summaries:

```text
1. Parse all paper summaries.
2. Extract structured metadata.
3. Extract candidate claims from each paper.
4. Map papers to related concepts.
5. For each concept:
   a. Collect relevant papers.
   b. Extract concept-specific evidence notes.
   c. Cluster candidate claims.
   d. Identify representative papers.
   e. Identify open questions.
   f. Generate concept evidence digest.
   g. Generate concept page.
6. Generate venue reports.
7. Generate yearly or state-of-field reports.
8. Generate or update overview.md.
```

---

# 16. Incremental Ingestion Pipeline

For 20 new papers:

```text
1. Generate paper summaries.
2. Extract candidate claims.
3. Assign related concepts.
4. For each affected concept:
   a. Extract concept-specific notes from new papers.
   b. Merge notes into concept evidence digest.
   c. Update claim clusters.
   d. Update trend notes.
   e. Update concept page sections selectively.
5. Generate monthly or batch report.
6. Update overview only if major field-level changes occurred.
```

---

# 17. Machine-Oriented vs Human-Oriented Artifacts

## 17.1 Human-Oriented Artifacts

These are meant to be read:

```text
papers/
concepts/
reports/
venues/
overview.md
comparisons/
```

---

## 17.2 Machine-Oriented Artifacts

These support generation:

```text
concepts/_evidence/
reports/_deltas/
claims_index.yaml
concept_index.yaml
metrics_index.yaml
```

These do not need polished prose.

They should be compact, structured, and stable.

---

# 18. Recommended Intermediate Files

## 18.1 `claims_index.yaml`

Optional global index of candidate claims.

```yaml
claims:
  - claim_text: Neural codec representations can reduce streaming latency.
    paper_id: 2604.12438
    related_concepts: [neural-codec, streaming-tts]
    polarity: supports
    confidence: medium
```

---

## 18.2 `concept_index.yaml`

Global concept registry.

```yaml
concepts:
  - id: neural-codec
    name: Neural Codec
    status: established
    related_concepts:
      - streaming-tts
      - autoregressive-codec-tts
      - speech-language-model
```

---

## 18.3 `metrics_index.yaml`

Structured metrics across papers.

```yaml
metrics:
  - paper_id: 2604.12438
    metric: MOS
    value: 2.51
    system: proposed
    testset: LJSpeech
    task: TTS
```

---

## 18.4 `reports/_deltas/`

Store report-specific deltas.

```yaml
period: 2026-05
new_papers: [...]
concept_changes:
  neural-codec:
    new_papers: [...]
    strengthened_claims: [...]
    contested_claims: [...]
    new_open_questions: [...]
```

---

# 19. Product/Use-Case Direction

The wiki can support multiple downstream products.

## 19.1 RAG-Powered Research Assistant

Use the wiki as a structured retrieval substrate.

Advantages over raw PDFs:

- Controlled vocabulary
- Standardized metrics
- Wikilinks
- YAML frontmatter
- Concept graph
- Claims

Example queries:

```markdown
- Best zero-shot TTS by speaker similarity, excluding proprietary systems?
- Which papers use EnCodec but not autoregressive decoding?
- Open-source flow-matching TTS systems and their WER on LibriSpeech test-clean?
```

---

## 19.2 Living Benchmark Observatory

Use standardized metrics to build dynamic leaderboards.

Important feature:

> Detect metric inflation over time.

Ask:

- Are scores genuinely improving?
- Are papers switching to easier test sets?
- Are evaluation protocols changing?

---

## 19.3 Living Survey Paper

The wiki can support:

- Annual survey papers
- Topic-specific surveys
- Venue-specific reviews
- Long arXiv reports

The living nature of the wiki means it can be updated more easily than a static survey.

---

## 19.4 Research Gap Map

Aggregate:

- Limitations
- Open questions
- Future work
- Contested claims

This may be one of the highest-value outputs for researchers.

---

## 19.5 Organization / Lab Intelligence

Use organization, venue, and year metadata to answer:

```markdown
- What is Google publishing in TTS this year vs. last?
- Is Microsoft shifting from diffusion to flow matching?
- Which academic groups are driving voice conversion research?
```

---

## 19.6 Automated Related-Work Generation

Use a new paper’s abstract and method to retrieve relevant concepts and papers.

Generate related work organized by theme, not chronology.

---

## 19.7 Continuous Monitoring Service

Run ingestion monthly.

New papers update:

- Paper pages
- Concept evidence digests
- Concept pages
- Monthly reports
- Overview if necessary

---

# 20. Writing Style Guidelines

## 20.1 Target Audience

Primary audience:

- Speech researchers
- Applied speech engineers

Secondary audience:

- Research managers
- Technical leads
- Students entering the field

Do not optimize primarily for people interested in the ingestion infrastructure.

---

## 20.2 Write About the Field

Avoid:

```markdown
Paper X proposes...
Paper Y introduces...
Paper Z explores...
```

Prefer:

```markdown
The field has increasingly shifted toward codec-native generation because...
```

Higher-level pages should use field-level subjects.

---

## 20.3 Prefer Synthesis Over Enumeration

The value of the wiki is not that it lists papers.

The value is that it explains what the literature collectively means.

---

## 20.4 Be Explicit About Uncertainty

Distinguish:

- Established evidence
- Emerging evidence
- Mixed evidence
- Speculation
- Open questions

Do not overstate trends from sparse evidence.

---

## 20.5 Surface Trade-Offs

Many papers improve one dimension while weakening another.

For example:

- Lower latency but worse MOS
- Better speaker similarity but worse intelligibility
- Better subjective quality but weaker reproducibility
- Strong benchmark but proprietary model

These trade-offs should be preserved.

---

# 21. Suggested Page-Level Responsibilities

## Paper Page

Question:

> What happened in this paper?

Contains:

- Evidence
- Results
- Claims
- Limitations

---

## Concept Page

Question:

> What do we know about this concept?

Contains:

- Synthesis
- Major claims
- Relationships
- Open questions
- Trend summary

---

## Report

Question:

> What changed?

Contains:

- Trends
- Emerging concepts
- Declining concepts
- Notable claims
- Surprises
- Forecast

---

## Overview

Question:

> What does it all mean?

Contains:

- Dominant paradigms
- Field-level findings
- Tensions
- Gaps
- Forecast

---

# 22. Highest-Leverage Improvements

The five highest-leverage changes are:

1. Add explicit claims extraction to paper ingestion.
2. Add field-significance assessment to paper pages.
3. Turn concept pages into research briefings with status, major claims, open questions, relationships, and trend summaries.
4. Generate periodic reports focused on what changed.
5. Use evidence digests to support scalable incremental synthesis.

---

# 23. Recommended Next Implementation Steps

## Step 1

Add `## Claims` and `## Field Significance` sections to paper page generation.

---

## Step 2

Create concept evidence digest files for each existing concept.

---

## Step 3

Write an agent that extracts concept-specific notes from paper summaries.

---

## Step 4

Write an agent that clusters paper-level claims into concept-level major claims.

---

## Step 5

Update concept page templates to include:

- Current Status
- Major Claims
- Open Questions
- Relationship to Other Concepts
- Trend Summary

---

## Step 6

Create a monthly report template.

---

## Step 7

Generate a first monthly or batch report from recent ingestions.

---

## Step 8

Update `overview.md` using concept pages and reports, not raw papers.

---

# 24. Core Design Principle

The wiki should not be optimized merely for retrieval.

It should be optimized for synthesis.

The long-term opportunity is not:

> Search 800 papers.

It is:

> Understand the current state and direction of speech-generation research.

Paper pages provide evidence.

Claims expose reusable propositions.

Concept pages synthesize understanding.

Reports capture change.

The overview communicates field-level meaning.
