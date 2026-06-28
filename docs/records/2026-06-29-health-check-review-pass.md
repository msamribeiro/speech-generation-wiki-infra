# Health-Check Review Pass — Complete Record

Document type: operational record  
Completed: 2026-06-29  
Sessions: multiple (2026-06-23 start; arXiv batch completed 2026-06-29)

---

## Summary

Full review pass on all 338 ingested Tier 1 wiki pages that failed
`scripts/health_check.py --module ingest`. Two error classes were targeted:

- **`required_fields`** — missing `field_significance` frontmatter block
- **`claims_section`** — missing `## Claims` section, or claim bullets lacking `*(§N.N)*` inline citations

**Total papers reviewed: 138** across all venues.  
**Final state: 0 errors corpus-wide** (confirmed by full ingest health check on 2026-06-29).

Venue breakdown:
- Interspeech 2025: complete (prior sessions)
- ACL / EMNLP / NAACL / COLING: complete (prior sessions)
- arXiv (Oct 2025 – Apr 2026): 16 papers, completed 2026-06-29

---

## Approach

Batches of 4, processed sequentially (never in parallel):

1. Snapshot each file to `/tmp/{ID}.before.md`
2. Run `speech-generation-review-agent` on each paper
3. Diff before/after and critique — flag hallucinated metrics, outrageous claims, wrong types, wikilink violations
4. Fix any issues found in the diff
5. Health check each paper against the standalone content repo (`--wiki-dir`)
6. Report batch summary; add flags to Manual Verification List

---

## Recurring agent failure patterns

These appeared consistently across all batches and should inform future review agent prompts or spec updates.

### 1. F5-TTS canonical ID

The agent repeatedly used the arXiv ID `2410.06885` instead of the canonical ACL ID `2025.acl-long.313`. This affected both `related_papers` frontmatter and Wiki Connections wikilinks. Fixed manually in every occurrence.

**Rule already in REVIEW_SESSION.md helper notes; should be in agent spec.**

### 2. Invalid `field_significance.type` values

The agent invented types outside the controlled vocabulary:
- `evaluation-contribution` (used in 2603.08823) → correct: `empirical-benchmark`
- `dataset-contribution` (used in 2604.00688) → correct: `empirical-benchmark`

Valid types: `architectural-novelty`, `engineering-integration`, `empirical-benchmark`, `conceptual-contribution`.

### 3. Wikilink format violations

Three distinct anti-patterns appeared in preserved prose sections (Wiki Connections written during ingest that the review agent did not rewrite):
- `[[id]] (Name)` — most common; fix to `[[id|Name]]`
- `Name ([[id]])` — name before the link; fix to `[[id|Name]]`
- `[[id]]` bare — acceptable only when no clean system/model name exists

The review agent correctly fixed its own new output but left pre-existing violations in preserved prose. Manual post-diff cleanup was required on most papers.

### 4. Ghost papers in `related_papers`

Several papers had `related_papers` entries referencing arXiv IDs that were never ingested. Removed in review:

| Paper | Ghost IDs removed |
|-------|------------------|
| 2603.18090 (MOSS-TTS) | 2602.10934, 2512.23808, 2509.24650 |
| 2603.29339 (LongCat-AudioDiT) | 2509.24650, 2509.22167 |

`2509.24650` (VoxCPM) appeared as a ghost in multiple papers.

### 5. `field_significance` type/prose inconsistency

In several cases the agent wrote prose in the Field Significance section that described a "training-recipe" or "engineering" contribution, then tagged `type: architectural-novelty`. This occurs because the vocab's definition of `architectural-novelty` includes "training objective", which is broad. The inconsistency is cosmetic but worth watching — if the prose says "primarily a training recipe, not architectural", the type should be `engineering-integration`.

### 6. Causal language in claims

The agent frequently used "because", "primarily because", "eliminating", and "necessary" in claim bullets. These are sometimes accurate (paper states the mechanism directly) but are often the agent's inference. All such claims were added to the Manual Verification List.

### 7. Vocabulary type in `field_significance`

The agent occasionally tagged `field_significance.level: high` for papers that are substantial engineering reports but not paradigm-shifting. Flagged as judgment calls for: 2603.26364 (LLaDA-TTS), 2604.00688 (OmniVoice).

---

## Manual Verification List

51 items spanning all batches, recorded in `REVIEW_SESSION.md` under "Manual Verification List". These require a human to open the PDF and check the specific section/table cited.

Categories of flagged items:
- Specific metric values added or changed by the review agent (e.g. WER corrections)
- "First" claims (field significance or Wiki Connections)
- Causal claims where the paper likely only shows correlation
- Strong language: "eliminates", "necessary", "near-random", "no measurable degradation"
- Specific quantitative ranges that are easy to hallucinate (5–10x, 30K–130K hours)
- Paper-coined terminology that could be fabricated ("tail-first confidence bias")

The manual verification list is the primary remaining deliverable from this pass.

---

## Files changed

- 138 wiki paper pages updated (field_significance, Claims, wikilinks, figures)
- 138 metadata JSONs updated (generation_history)
- Architecture figures added for ~80 papers (where type includes `architectural-novelty`)
- `wiki/log.md` — review entries appended for all 138 papers

Commits:
- Wiki content repo: `9d42a21` (arXiv batch, 2026-06-29); earlier commits for prior venue batches
- Infra repo: `ad149eb` (metadata + REVIEW_SESSION.md, 2026-06-29)
