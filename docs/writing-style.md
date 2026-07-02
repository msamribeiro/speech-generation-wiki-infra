# Writing Style Guidelines — Speech Generation Wiki

This guide applies to all content-generating agents: ingest, integration, query, and report. Read it before writing any wiki page. Its rules take precedence over default habits.

---

## 1. Target Audience

**Primary:** Speech researchers and applied speech engineers who read the wiki to stay current with the field, not to learn about this project's infrastructure.

**Secondary:** Research managers, technical leads, and students entering the field.

Write for people who know what a vocoder is, understand MOS, and have read at least a few TTS papers. Do not explain foundational ML concepts unless the paper's contribution is specifically about them.

---

## 2. Write About the Field, Not About the Paper

The most common failure mode in paper summaries and concept pages is turning into a list of "Paper X does Y."

**Avoid:**
> Paper X proposes a depth-wise decoder.
> Paper Y introduces a new conditioning mechanism.
> Paper Z explores streaming inference.

**Prefer (for concept and overview pages):**
> The field has increasingly adopted codec-native generation pipelines, bypassing mel-spectrograms entirely in latency-sensitive applications.

**For paper pages**, subject-of-paper language is appropriate because the page *is* about the paper. But even there, the **Key Results**, **Novelty Assessment**, and **Field Significance** sections should zoom out: what does this result mean for the field, not just for this paper?

The rule of thumb: if the sentence could not appear in a survey paper, it probably belongs only in a paper page, not in a concept page or overview.

---

## 3. Claims

Claims are generalised propositions about speech generation that a paper provides evidence for, against, or complicates. They are the primary mechanism for turning individual paper results into field-level knowledge.

### What a claim is

A claim is one sentence, stated at the field level, reusable across multiple papers. It must be possible for another paper to support, refute, or refine it.

**Good examples:**
- Flow matching enables high-quality speech synthesis with fewer inference steps than diffusion.
- Speaker similarity remains difficult to preserve in zero-shot multilingual TTS.
- Neural codec representations reduce time-to-first-byte in streaming speech generation.
- Aggressive codec quantisation introduces audible artefacts before MOS scores reflect the degradation.
- Subjective preference scores and automatic MOS predictors frequently disagree on voice conversion quality.

**Bad examples (and why):**
- *The model achieves 4.31 MOS.* — This is a metric value, not a claim.
- *The paper introduces a depth-wise decoder.* — This is a contribution description, not a field-level proposition.
- *The model uses Mimi as its codec.* — This is an implementation detail.
- *The authors train on LJSpeech.* — This is a dataset choice, not a claim.
- *Future work should explore multilingual settings.* — This is speculation, not evidence.

### How many claims per paper

2–5 claims per paper page. More than 5 suggests over-granularity; fewer than 2 suggests the paper's field-level contribution hasn't been characterised.

### Section citations (provenance)

Each claim uses a two-line format: a bold role prefix on the bullet line, followed by a blockquote Evidence line carrying the paper-specific detail and an inline section citation:

```markdown
- **supports:** {Generalized claim sentence.}
  > *Evidence:* {Specific result, mechanism, or failure case from this paper.} *(§4.1, Table 2)*
- **complicates:** {Generalized claim sentence.}
  > *Evidence:* {Specific limitation or trade-off.} *(§5.1)*
```

Role prefixes: `**supports:**`, `**complicates:**`, `**contradicts:**`, `**refines:**`.

The section citation `*(§N.N)*` goes at the end of the Evidence line. Use the section number and title if the paper labels them (e.g. `§4.1 "Inference Speed"`). Named sections without numbers are valid: `*(§Limitations)*`, `*(§Appendix B)*`. If evidence spans multiple sections, cite all of them. Do not cite the abstract or introduction alone — find the section where the result or argument is actually presented.

This grounds each claim in the paper and allows readers and future agents to verify it directly in the source PDF.

### What not to force

Do not generate claims that are trivially true, universal, or so hedged that no paper could contradict them. "TTS systems require training data" is not a useful claim.

---

## 4. Field Significance

The `## Field Significance` section and `field_significance` frontmatter together characterise a paper's role in the field, beyond its own results.

### Level guidelines

| Level | When to use |
|-------|-------------|
| `foundational` | Introduces a paradigm, architecture, or benchmark that subsequent work builds on. Rare — fewer than 5% of papers. Examples: VITS, VALL-E, HiFi-GAN, Voicebox. |
| `high` | Strong empirical advance, widely cited architecture change, or first demonstration of a capability. The field's direction is noticeably different because of this paper. |
| `moderate` | Solid incremental contribution. Advances a sub-area, provides useful evidence, or introduces a technique that is adopted but not paradigm-shifting. Most papers fall here. |
| `low` | Confirmatory, minor variant, or narrow application. Still accurate and citable, but primarily adds evidence rather than new understanding. |

### Type guidelines

Use the type tags from the controlled vocabulary. A paper can have multiple types. Assign generously — a paper can simultaneously be `architectural-novelty` and `empirical-benchmark`.

`negative-result` should be used whenever a paper's main contribution is showing that something *doesn't* work, that a widely-used baseline is stronger than believed, or that reported gains don't replicate. These are high-value and should not be marked `low` by default.

### Prose format

```markdown
## Field Significance

Moderate — This paper provides strong evidence that flow matching outperforms diffusion in the low-NFE regime for TTS, reinforcing a trend visible in the prior year's work. Its contribution is primarily empirical rather than architectural; the approach is not novel but the evaluation is thorough and the comparisons are fair.
```

Keep to 1–3 sentences. Do not repeat the contribution description from the One-sentence contribution line.

---

## 5. Novelty Assessment

Be honest. The Novelty Assessment is the place to say that a paper is incremental, that the baseline comparisons are weak, or that the claimed contribution is standard in adjacent fields. Accuracy here is more valuable than generosity.

**Good patterns:**
- "The contribution is primarily engineering integration: [X] and [Y] are established techniques applied here to [domain] for the first time."
- "The architecture is novel, but the evaluation uses proprietary data only, limiting reproducibility."
- "The paper replicates findings from [related work] on a larger scale; the scale itself is the contribution."
- "The claimed gain over the baseline is real but small (0.08 MOS), and the test set is limited to [specific speaker/domain]."

**Avoid:**
- Claiming novelty for standard techniques with different hyperparameters.
- Hedging so much that the assessment is meaningless ("results are promising but more work is needed").
- Endorsing authors' self-assessments without independent evaluation.

---

## 6. Synthesis Over Enumeration

On concept pages and overview pages, prefer interpretive paragraphs over lists of papers.

**Avoid:**
> - Paper A uses flow matching.
> - Paper B uses flow matching.
> - Paper C uses flow matching.

**Prefer:**
> Flow matching has become the dominant training paradigm for continuous-output TTS, appearing in the majority of high-performing systems since 2024. Its advantages over diffusion — fewer inference steps, simpler training objective, and comparable or superior sample quality — have proven robust across system scales and conditioning types.

Lists of papers belong in the **Papers** table of a concept page, not in the synthesis sections.

---

## 7. Explicit Uncertainty

Distinguish these levels clearly:

| Label | Meaning |
|-------|---------|
| **Established** | Supported by multiple independent papers with fair evaluations; no credible contradicting evidence |
| **Emerging** | Supported by 1–2 papers, or supported by more but with methodological caveats |
| **Contested** | Papers disagree; the contradiction is itself informative |
| **Speculation** | Not yet tested; a plausible extrapolation from existing evidence |

Do not write "X is the state of the art" unless X is demonstrably the best-performing system on a standard benchmark with fair comparisons. Prefer "X achieves the strongest reported results on [benchmark] as of [date]."

---

## 8. Surface Trade-offs

Many improvements trade one dimension against another. Make these explicit.

**Good:**
> The system achieves a 60% reduction in time-to-first-byte relative to the non-streaming baseline, at the cost of a 0.3 MOS decrease on naturalness.

**Avoid:**
> The system is faster and maintains high quality.

Trade-offs matter for practitioners choosing systems, for downstream synthesis agents building concept evidence digests, and for claim clustering (where a gain in one system may be a loss in another).

---

## 9. Tense Conventions

- **Paper pages:** present tense for what the paper describes ("the model uses", "results show"). Past tense only for historical context ("prior work relied on").
- **Concept pages:** present tense for current state, past tense for historical trajectory ("diffusion dominated through 2023; flow matching has since displaced it in most frontier systems").
- **Reports:** past tense for what happened during the period; present tense for conclusions that remain valid.

---

## 10. Wikilinks

Use `[[paper_id]]` for in-corpus papers and `[[concept_slug]]` for concept pages. Use wikilinks when a paper or concept is specifically relevant to the sentence — not as a general "see also." Over-linking degrades the signal.

On concept pages, every claim in the Major Claims section (once that section exists) should have at least one wikilink to a supporting paper.

---

## 11. Callout Boxes

Callouts use Obsidian/Quartz syntax: `> [!type]` followed by indented content. Use them sparingly — a page with five callouts has none. Reserve them for information that genuinely warrants visual elevation above surrounding prose.

### Permitted callout types and when to use them

| Type | Syntax | Use when |
|------|--------|----------|
| Abstract | `> [!abstract]` | One-sentence contribution (paper pages); Executive Summary (concept pages). Always. |
| Important | `> [!important]` | Field Significance of a **foundational** paper only. |
| Tip | `> [!tip]` | Field Significance of a **high**-significance paper only. |
| Warning | `> [!warning]` | A critical limitation that restricts claims or reproducibility (paper pages); a Contested claim (concept pages). |
| Note | `> [!note]` | A notable caveat about result interpretation — e.g., comparisons are on different test sets, statistical significance not reported. Use in Key Results only. |

### Rules

- **Maximum 2 callouts per paper page.** The abstract callout for one-sentence contribution counts as one.
- **Moderate and low field significance: no callout.** Plain prose only.
- **Do not use callouts as section decorations.** A heading already provides structure. A callout adds visual weight — use it only when the content itself warrants it.
- **Callout content must be self-contained.** A reader who sees only the callout should understand its point without needing the surrounding paragraph.

### Examples

```markdown
> [!abstract]
> **One-sentence contribution:** Flow matching with a learnable noise schedule matches DDPM sample quality in 10× fewer function evaluations for TTS.

> [!important]
> Foundational — this paper introduced the rectified flow objective that most subsequent flow-matching TTS systems adopt directly.

> [!warning]
> Evaluated on a single proprietary speaker in a controlled studio environment; generalisation to noisy, multi-speaker settings is untested.

> [!note]
> MOS comparisons are not on the same test set as the baseline; direct numerical comparison should be treated with caution.
```

## 12. What to Omit

- Do not restate the abstract. Synthesise from reading the full paper.
- Do not list every experiment or ablation. Focus on the headline results and what they mean.
- Do not include meta-commentary about the wiki or the ingestion process.
- Do not speculate about future work beyond what the paper itself proposes as future directions.
- Do not pad sections. If a section has nothing meaningful to say, write one honest sentence rather than three vague ones.

---

## 13. Citation and Wikilink Format for Concept and Evidence Pages

The general wikilink rule (§10) applies everywhere. Concept and evidence pages additionally follow
these conventions to achieve research-paper citation clarity.

### Syntax

Use `[[id|Name]]` to display a system or model name as the link text:

- `[[2025.acl-long.313|F5-TTS]]` renders as **F5-TTS** (linked to the paper page)
- `[[flow-matching|Flow Matching]]` renders as **Flow Matching** (linked to the concept page)

Use bare `[[id]]` when a paper has no commonly used system or model name.

In markdown table cells, the `|` inside `[[id|Name]]` may conflict with column separators. If the
renderer misparses it, escape with `\|`: `[[2025.acl-long.313\|F5-TTS]]`.

### When to use each form

| Context | Format | Example |
|---------|--------|---------|
| Paper as sentence subject | `[[id\|Name]] achieves...` | `[[2025.acl-long.313\|F5-TTS]] achieves WER 1.83%` |
| Concept named in prose | `[[slug\|Title]]` | `[[flow-matching\|Flow Matching]] has displaced diffusion` |
| Single parenthetical citation | `([[id\|Name]])` | `...in alignment-free TTS ([[2406.18009\|E2 TTS]])` |
| Multiple parenthetical citations | `([[id\|Name]], [[id\|Name]])` | `...([[2025.acl-long.313\|F5-TTS]], [[2025.acl-long.1043\|OZSpeech]])` |
| Paper without a system name | `([[id]])` or `([[id]], [[id]])` | `...([[2210.02747]], [[2312.15821]])` |

### Claim format in Major Claims

Every claim bullet in the `## Major Claims` section uses a three-part format:

```markdown
- **Claim stated at the field level.**  
  Evidence: [[id|Name]], [[id|Name]], [[id]].  
  Caveat: {one sentence on scope limits, if any.}
```

Omit the Caveat line when there are none. The Evidence line lists only papers that directly support
the specific claim — not all papers in the concept. Use `[[id|Name]]` for named systems; bare
`[[id]]` for unnamed papers.

### Traceability invariant

Every claim on a concept page and every evidence cell in a dossier table must be traceable to a
specific entry in `wiki/_claims/{slug}.yaml`. The YAML `claim_clusters` and `papers[].claims`
entries in turn derive from the paper's `## Claims` section, which cites source sections via
`*(§N.N)*`. The full chain is:

```
concept page claim
  → YAML claim_cluster (supporting_papers list)
    → YAML papers[id].claims entry (role, evidence, source)
      → paper page ## Claims bullet
        → paper section *(§N.N)*
```

Render agents never invent evidence — all synthesis derives from YAML entries. If a statement has
no traceable YAML source, it must not appear on the page.
