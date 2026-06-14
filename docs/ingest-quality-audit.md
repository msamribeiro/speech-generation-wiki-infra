# Ingest Quality Audit — Process and Findings

Document type: operational record  
Last updated: 2026-06-14 (session 46)

---

## Purpose

This document records the quality audit process developed during Tier 1 citation-discovery ingest (sessions 45–46), the recurring failure modes discovered, and the agent spec patches applied to prevent them. It supersedes the grep-based quality checks described in SESSION_NOTE.md.

---

## Core principle: full page read, not grep

During session 46, the audit method was upgraded from grep-based spot checks to **full page reads**. The change was motivated by the observation that grep catches surface-level formatting issues but misses substantive problems — wrong claims, inflated field significance levels, spurious concept slugs, and arguments made in the wrong direction.

**The audit that matters is a human read of the generated page**, checking:

1. Does the abstract callout card accurately describe what the paper does?
2. Are the claims genuinely field-level generalisations (not paper-specific), and do they have section citations?
3. Is the field significance level correct relative to the paper's actual contribution?
4. Are `related_concepts` grounded in what the paper's own method implements — not what it mentions or compares against?
5. Is the Wiki Connections section in bullet format with one descriptive clause per link?
6. Are there adoption claims or citation-verb phrases in Field Significance or Wiki Connections prose?

Grep remains useful for catching the easiest-to-fix issues (em dashes, `[!note]` callouts, `\bSCA\b` in prose) **after** the page read. But it should never substitute for it.

---

## Cadence

- **Standard ingest**: 2 papers per round. Ingest both, then read both pages in full before approving the next pair.
- **Tier 1 CD ingest**: same cadence — 2 at a time, full read before moving on.
- **Tier 2 CD stubs**: 2 at a time, full read. Stubs are shorter but still require the callout, concept slug, and Wiki Connections checks.

---

## Recurring failure modes (13 Tier 1 CD papers, session 46)

The following issues appeared in multiple pages in the session-46 audit and have been patched into the agent specs.

### 1. Wrong abstract callout type

**Issue:** Agent used `[!tip]` or `[!important]` on the abstract card (the top callout). This happened when the same callout type had just been assigned to Field Significance (`[!tip]` for high, `[!important]` for foundational) — the agent then reused it on the card.

**Rule:** The abstract card is **always** `[!abstract]`. No exceptions.

**Papers affected:** 2502.06490 (Discrete Tokens Review), 2504.08528 (SLM Landscape Survey).

**Fix:** Moved the callout warning to immediately before the template's abstract card. Added an explicit "most common mistake" note.

---

### 2. Survey paper frontmatter pollution

**Issue:** Survey papers had `architecture`, `conditioning`, `training` fields filled with what the survey *reviews* — not the survey's own properties. A survey has no architecture, no conditioning mechanism, and no training procedure of its own.

**Rule:**
- `architecture: []`
- `conditioning: []`
- `training: []`
- `datasets_train: ["not applicable (survey)"]`
- `datasets_eval: ["not applicable (survey)"]`

Exception: if the survey includes original controlled experiments with a trained model, list only those datasets.

**Papers affected:** 2410.03751 (Speech LM Survey), 2502.06490 (Discrete Tokens Review), 2504.08528 (SLM Landscape Survey).

**Fix:** Added "Survey paper frontmatter rule" section to the ingest agent spec, immediately before the template.

---

### 3. Wiki Connections format

**Issue:** 11 of 13 Tier 1 CD pages had non-standard Wiki Connections formatting. Common variants:
- Pipe-separated: `[[concept]] | [[paper]] | [[paper]]`
- Dot-separated: `[[concept]] · [[paper]]`
- Inline commas: `[[A]], [[B]], [[C]]`
- Bold section headers with sub-lists
- Wikilinks without any description

**Rule:** One bullet per link, with a descriptive clause:
```
- [[concept-slug]] — {1 sentence: how does this paper relate to this concept?}
- [[paper-id]] (Short title) — {1 sentence: build on / extend / compare against / challenge?}
```

No pipes, no dots, no inline commas, no bold headers. Every `[[wikilink]]` must have a clause after the em dash.

**Papers affected:** All 11 non-survey Tier 1 papers needed at least one correction.

**Fix:** Replaced the generic placeholder in the template with an explicit format block including prohibitions.

---

### 4. Spurious `related_concepts` slugs

**Issue:** Concept slugs were included when the paper merely *mentions*, *evaluates against*, or *compares to* the concept — rather than when the paper's own method directly implements or contributes to it.

Specific recurring errors:

| Slug | Wrong usage | Correct usage |
|------|-------------|---------------|
| `prosody-control` | Paper evaluates F0-RMSE, or has a standard duration predictor | Paper introduces an explicit mechanism to control prosody independently (e.g. phoneme sequence substitution at inference) |
| `disentanglement` | Fast/slow codec streams, separate codebook layers | Training objective explicitly separates speaker identity, content, style into distinct representation spaces |
| `instruction-conditioned-tts` | SCA paper that follows dialogue instructions | Paper's TTS/VC system accepts natural language style instructions as a conditioning signal |
| `prompt-conditioned` (conditioning field) | Paper uses d-vector/x-vector speaker embedding | System is conditioned on a short audio reference clip at inference to control style or speaker |
| `self-supervised-speech` | Paper uses Whisper, or cites SSL in related work | Paper's own system uses HuBERT/WavLM/wav2vec 2.0 as a core component |

**Papers corrected:**
- `prosody-control` removed: 2105.06337 (Grad-TTS), 2502.05512 (IndexTTS)
- `prosody-control` kept: 2406.07855 (VALL-E R — phoneme monotonic alignment genuinely enables prosody cloning via reference sequence substitution)
- `disentanglement` removed: 2411.01156 (Fish-Speech)
- `instruction-conditioned-tts` removed: 2410.11190 (Mini-Omni2), 2504.08528 (SLM Landscape Survey)
- `prompt-conditioned` removed: 2104.00355 (Speech Resynthesis), 2410.17799 (OmniFlatten)

**Fix:** Added explicit grounding rules for each misused slug to the `related_concepts` section of both agent specs.

---

### 5. `training` field missing entries

**Issue:** Papers using supervised training with reconstruction/adversarial losses had `training: [self-supervised]` only, omitting `supervised`.

**Papers affected:** 2104.00355 (Speech Resynthesis — BigVGAN vocoder uses supervised adversarial objectives), 2502.07243 (Vevo — HiFi-GAN is supervised).

**Fix:** Added `supervised` to training fields. No spec change needed — the controlled vocabulary definition already requires listing all applicable paradigms.

---

### 6. Double hyphens in prose

**Issue:** `--` used as em dash substitute in Field Significance prose, violating the em-dash avoidance rule.

**Paper affected:** 2412.15649 (SLAM-Omni).

**Fix:** Replaced with colons and parentheses per the project em-dash rule. No spec change needed — the rule was already in the agent spec.

---

## Tier 2 stub audit (session 46)

12 Tier 2 stubs were audited. The shorter format (frontmatter + abstract callout + Context + Wiki Connections) means fewer failure modes, but three recurring issues appeared:

### Inline Wiki Connections
Same issue as Tier 1: agents wrote inline comma-separated wikilinks or "Related concepts: [[A]], [[B]]" without bullets. All 12 pages were checked; 9 needed corrections.

### Spurious concept slugs on general LLMs
Foundation LM stubs (GPT-3, LLaMA 2, DeepSeekMath) received concept slugs (`instruction-conditioned-tts`, `rlhf-speech`, `autoregressive-codec-tts`) that the paper itself does not implement. The rule: a general-purpose LLM stub should only receive a concept slug if the paper's method directly contributes to a speech generation concept — not because downstream speech papers use it for that purpose.

**Corrections:**
- GPT-3 (2005.14165): removed `autoregressive-codec-tts`, `instruction-conditioned-tts`
- LLaMA 2 (2307.09288): removed `instruction-conditioned-tts`
- DeepSeekMath (2402.03300): removed `rlhf-speech`
- Gemini (2312.11805): removed `multilingual-tts`

### Blank `tags:` field
SpeechBrain (2106.04624) had `tags:` with no value (the field is only for survey papers with `["survey"]`). Removed.

---

## Patches applied to agent specs (2026-06-14)

### `speech-generation-ingest-agent.md` (standard full pages)

| Patch | Location in spec |
|-------|-----------------|
| Survey frontmatter rule | New section before template |
| Abstract card callout warning | Immediately before abstract card in template |
| Wiki Connections bullet format requirement | Replaced generic placeholder in template |
| `related_concepts` grounding rules (5 slugs) | Added after `self-supervised-speech` usage rule |

### `speech-generation-lightweight-ingest-agent.md` (Tier 2 stubs)

| Patch | Location in spec |
|-------|-----------------|
| Abstract card callout warning | Before abstract card in both standard and survey templates |
| Wiki Connections bullet format requirement | Replaced generic placeholders in both templates |
| `related_concepts` grounding rules (3 slugs) | Added after `self-supervised-speech` usage rule |

---

## Quick grep checks (after full page read)

These are fast mechanical checks to run after reading. They catch issues the eye can miss:

```bash
WIKI=/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content

# Wrong callout in first 10 lines (abstract card should be [!abstract])
head -20 $WIKI/papers/{id}.md | grep "\[!tip\]\|\[!important\]"

# Disallowed [!note] callout anywhere
grep -n "\[!note\]" $WIKI/papers/{id}.md

# SCA used as prose (should be "spoken conversational agents")
grep -n '\bSCA\b' $WIKI/papers/{id}.md | grep -v "^[0-9]*:task:\|^[0-9]*:  - SCA"

# Adoption claim phrases
grep -in "de facto\|widely adopted\|the dominant\|has become a standard\|cited by [0-9]" $WIKI/papers/{id}.md

# Em dash doubles (-- substitute)
grep -n ' -- ' $WIKI/papers/{id}.md

# Wiki Connections format check (should have no pipes or dots after [[)
grep -n '\[\[.*\]\].*|' $WIKI/papers/{id}.md
grep -n '\[\[.*\]\] ·' $WIKI/papers/{id}.md
```

---

## What the grep cannot catch

These require reading:

- **Claims that are paper-specific** ("VALL-E R achieves near-ground-truth WER") instead of field-level ("Explicit phoneme alignment in codec LM TTS can close the robustness gap without encoder-decoder architectural changes")
- **Field significance level inflation** (moderate paper called high; high paper missing `[!tip]` callout)
- **`field_significance.type` mismatches** (engineering integration labelled architectural-novelty; survey labelled empirical-benchmark)
- **Context paragraphs with citation-verb phrases** ("TTS papers use this as…", "the community relies on…")
- **Figure selection errors** (figure embedded for an empirical paper with no architectural novelty, or wrong figure selected)
- **Organization field wrong or missing**
