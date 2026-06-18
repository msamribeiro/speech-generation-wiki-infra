# GPT Suggestions — 2026-06-15

## Content Critique

The wiki is already much more valuable than a paper catalog. Its strongest parts are the field-level synthesis and the way paper pages are designed as reusable evidence objects. The main weakness is consistency drift: counts, citation discipline, and some digest/index hygiene are falling behind the ambition of the system.

## What Works Well

- The core information architecture is strong. Paper pages are not just summaries; they extract problem, method, results, novelty, field significance, claims, limitations, metrics, and concept links. That makes them useful both for humans and downstream synthesis.
- The concept pages are the real asset. Pages like `flow-matching`, `neural-codec`, and `evaluation-metrics` read like living survey sections: they identify method variants, representative papers, claim clusters, contested points, and open questions.
- The wiki is good at distinguishing paper-level contribution from field-level significance. The `Novelty Assessment` and `Field Significance` sections help prevent the usual "every paper is important" summary inflation.
- The overview is effective. It gives a coherent thesis of the field: flow matching vs. AR codec TTS, codec quality as a bottleneck, evaluation fragmentation, and multimodal LLM convergence for spoken conversational agents.
- The controlled vocabulary is doing useful work. Architectures, tasks, metrics, and conditioning tags make the corpus queryable in a way raw markdown usually is not.

## What Does Not Work As Well

- The wiki has visible consistency drift. Different pages report different paper counts: `wiki/index.md`, `wiki/overview.md`, `STATUS.md`, and metadata are not aligned. For a living review, stale counts reduce trust quickly.
- Claim provenance is inconsistent. Some pages have excellent section-cited claims, while others list claims without citations. Since claims are the core reusable evidence unit, missing provenance is more serious than ordinary prose polish.
- Some pages are too long for their role. Concept pages are comprehensive, but several are approaching "monograph chapter" length. That is useful for LLM synthesis, less useful for human scanning.
- The evidence digest layer needs validation. `wiki/concepts/_evidence/flow-matching.yaml` appears structurally suspicious near the end, where paper-like entries appear after `trend_notes`. If this is malformed or semantically misplaced YAML, it risks corrupting future synthesis.
- The paper index has formatting inconsistencies. Some rows are proper wikilinks, others are plain IDs or truncated titles without links.
- Lightweight citation-discovery pages are useful, but their relationship to full paper pages could be clearer. A reader may not immediately understand why one important paper has a stub while another has a full treatment unless they know the ingest tier system.

## Highest-Value Improvements

1. Add a validation script for wiki integrity:
   - paper count consistency
   - every `status: ingested` metadata file has a corresponding `wiki/papers/{id}.md`
   - every paper page has required frontmatter keys
   - every claim bullet has an inline section citation
   - every concept evidence digest parses as YAML
   - every `related_concepts` value points to an existing concept page
   - every wikilink target exists or is intentionally external/missing

2. Split concept pages into two layers:
   - human-readable concept page: summary, claims, tensions, representative papers, open questions
   - exhaustive evidence table: separate appendix or digest-derived page

   In practice, concept pages are currently trying to serve two audiences at once: humans who want a clear synthesis, and agents/scripts that need exhaustive evidence. That creates long pages. The solution is to make concept pages more editorial, while moving exhaustive detail into companion artifacts.

   A practical structure:

   ```text
   wiki/concepts/flow-matching.md
   wiki/concepts/evidence/flow-matching.md
   wiki/concepts/_evidence/flow-matching.yaml
   ```

   `flow-matching.md` would stay human-facing:

   - Executive Summary
   - Current Status
   - Major Claims
   - Contested Claims
   - Methods and Variants
   - Representative Papers
   - Open Questions
   - Trend Summary

   The exhaustive `All Papers` table moves to `wiki/concepts/evidence/flow-matching.md`, generated from the YAML digest or paper frontmatter.

   That evidence page could include:

   - every related paper
   - contribution type
   - claim snippets
   - metric highlights
   - limitations
   - date added
   - relevance level

   The YAML remains the machine layer. The evidence markdown becomes a readable appendix. The main concept page becomes easier to scan and maintain.

   The integration workflow changes from:

   ```text
   update paper page -> update evidence digest -> rewrite concept page
   ```

   to:

   ```text
   update paper page
   -> update evidence digest
   -> regenerate concept evidence appendix
   -> selectively update compact concept synthesis
   ```

   This matters because the concept page should answer: "What should I understand about this concept?" It should not have to show every row of evidence ever attached to the concept.

3. Standardize claim provenance retroactively. Claims without `*(§...)*` citations should be treated as incomplete.

4. Create frontier briefs or decision memos from concept pages, such as:
   - best current open-weight zero-shot TTS systems
   - when to choose flow matching vs. AR codec TTS
   - what metrics are trustworthy for TTS evaluation
   - codec design choices that matter for downstream LM training

   Concept pages explain a topic. Briefs answer a decision-shaped question.

   For example, `flow-matching.md` explains flow matching generally. A brief would answer:

   ```text
   When should I choose flow matching over autoregressive codec TTS?
   ```

   Briefs could live under:

   ```text
   wiki/briefs/flow-matching-vs-ar-codec-tts.md
   wiki/briefs/open-weight-zero-shot-tts.md
   wiki/briefs/trustworthy-tts-evaluation-metrics.md
   wiki/briefs/codec-design-for-speech-lms.md
   ```

   A brief should be short, opinionated, and evidence-backed. Suggested template:

   ```markdown
   ---
   title: "When to Choose Flow Matching vs. AR Codec TTS"
   date: 2026-06-15
   question: "When should a practitioner choose flow matching rather than autoregressive codec TTS?"
   concepts: [flow-matching, autoregressive-codec-tts, zero-shot-tts]
   papers_included: [...]
   status: current
   ---

   ## Short Answer

   Use flow matching when latency, parallel inference, and stable intelligibility matter most. Use AR codec TTS when in-context speaker/prosody modeling and long-form expressiveness matter most. Use hybrid AR+FM when you need both and can afford a two-stage system.

   ## Evidence

   | Claim | Evidence | Caveat |
   |------|----------|--------|
   | Flow matching is faster at inference. | F5-TTS, EPSS, RapFlow-TTS | Mostly tested on mel systems |
   | AR codec TTS scales well with model/data size. | VALL-E, Seed-TTS, Fish Audio S2 | Higher latency |
   | Hybrid AR+FM is becoming dominant in production-like systems. | CosyVoice 2, IndexTTS2, LLaMA-Omni 2 | More complex pipeline |

   ## Recommendation

   For open-weight deployment today...
   ```

   The key difference from concept pages: a brief makes a judgment. It says what the evidence implies for a researcher or engineer.

   Good candidates:

   - `best-open-weight-zero-shot-tts.md`
   - `flow-matching-vs-ar-codec-tts.md`
   - `tts-evaluation-metrics-that-matter.md`
   - `codec-frame-rate-tradeoffs.md`
   - `streaming-tts-state-of-field.md`
   - `spoken-dialogue-evaluation-gaps.md`
   - `preference-alignment-for-tts.md`

   How to generate them in practice:

   1. Pick a decision question.
   2. Load relevant concept pages and evidence digests.
   3. Pull only the strongest supporting and contradicting claims.
   4. Produce a concise memo with:
      - short answer
      - evidence table
      - caveats
      - recommendation
      - papers to read first
   5. Revisit when new papers materially change the answer.

   These briefs are the layer that makes the wiki actionable. Concept pages are "what the field knows"; briefs are "what to do with that knowledge."

5. Add quality/status badges to paper pages:
   - `full`
   - `lightweight`
   - `needs claim citations`
   - `needs integration`
   - `metrics extracted`
   - `figures included`

6. Keep an automatically generated dashboard:
   - total papers
   - ingested vs. integrated
   - concept counts
   - stale concept pages
   - pages missing citations
   - broken wikilinks
   - unintegrated accepted papers

## Strategic Direction

The wiki's best future is not simply "more paper summaries." It is a claim graph: papers support, refute, or complicate reusable propositions about speech generation. The current structure already points there. The highest leverage work is to make claims fully cited, machine-validate the evidence digests, and generate higher-level briefs from the concept layer.

In practical terms, the wiki should treat **claims** as the primary unit of knowledge, not papers.

Right now, each paper page says "this paper claims/shows X." That is useful. But the higher-value version is: "Across the field, what propositions are becoming supported, contested, weakened, or superseded?"

Example:

- Claim: "Flow matching requires fewer inference steps than diffusion for comparable TTS quality."
- Supporting papers: F5-TTS, OZSpeech, RapFlow-TTS, APTTS.
- Caveats: different datasets, different NFE ranges, mostly mel-spectrogram systems.
- Status: strongly supported.
- Concepts: `flow-matching`, `streaming-tts`, `zero-shot-tts`.

That turns the wiki into a structured evidence base. A paper is then not just a page; it is evidence attached to one or more claims.

The practical difference:

- A paper-summary wiki asks: "What did F5-TTS do?"
- A claim-graph wiki asks: "What do we now believe about flow matching, why, which papers support it, and where is the evidence weak?"

This matters because many useful research questions are claim-shaped:

- Is AR codec TTS still necessary, or are NAR systems catching up?
- Do automatic speaker similarity metrics agree with human judgments?
- Does lowering codec frame rate hurt TTS quality?
- Is preference alignment helping naturalness, intelligibility, or just benchmark scores?

To support that, the next improvements would be:

1. Make every paper claim source-cited.
2. Normalize similar claims across papers into canonical concept-level claims.
3. Track each claim's status: `strongly_supported`, `emerging`, `contested`, `weakened`.
4. Generate concept pages, reports, and briefs from those claim clusters.

If those pieces are tightened, this becomes a serious living systematic review rather than a large curated note collection.

## Integration Agent Notes

File reviewed: `.claude/agents/speech-generation-integration-agent.md`

In light of the suggestions above, the integration agent is directionally aligned but still optimized for "update big concept pages" more than for "maintain a claim graph."

### What It Already Does Well

- It explicitly owns cross-paper synthesis, not paper-page writing.
- It updates both human-facing concept pages and machine-oriented evidence digests.
- It has a claim-clustering step in `claim_clusters`, including promotion from `emerging` to `strongly_supported` and marking claims `contested`.
- It updates overview and venue narratives only when warranted, which is the right discipline.
- It processes concept writes sequentially, reducing conflict risk.
- It uses evidence digests to avoid reloading every paper each time.

### Where It Conflicts With These Suggestions

- It still appends every paper to `## All Papers` inside each concept page. That is exactly what makes concept pages grow too long. Under the suggested split, this table should move to a generated evidence appendix.
- It says concept rows in `wiki/concepts/index.md` should not be updated directly, then later instructs the agent to update them. That scope contradiction should be cleaned up.
- It does not require claim bullets on concept pages or paper pages to preserve source-section citations. It only says concept claims need wikilinks. For the claim-graph direction, source provenance should be required at the paper-claim level and ideally retained in digest entries.
- The evidence digest schema stores claim text but not section provenance, quote/evidence location, confidence, or whether the paper supports/contradicts/complicates the claim. That limits its usefulness as a true claim graph.
- It does not validate YAML after editing. Given the suspicious `flow-matching.yaml` structure, this is a real gap.
- It has no concept of decision briefs/frontier briefs. Those would need a new optional step or separate agent.

### Concrete Spec Changes

1. Add a validation step after evidence digest edits:
   - parse every touched YAML file
   - verify top-level keys are correct
   - verify `papers` entries are actually under `papers`
   - verify `paper_count` matches the list length or documented counting policy

2. Change concept page updates so `## All Papers` is no longer the main exhaustive sink:
   - short concept page gets only representative papers
   - exhaustive rows go to `wiki/concepts/evidence/{slug}.md`
   - YAML remains the source of truth

3. Upgrade digest claim entries from:

   ```yaml
   claims:
     - claim text
   ```

   to:

   ```yaml
   claims:
     - claim: claim text
       role: supports | contradicts | complicates
       source: "§4.2, Table 3"
       confidence: high | medium | low
   ```

4. Make claim clusters more explicit:

   ```yaml
   claim_clusters:
     - id: flow-matching-fewer-steps-than-diffusion
       claim: ...
       status: strongly_supported
       supporting_papers: [...]
       contradicting_papers: [...]
       caveats: [...]
       last_reviewed: YYYY-MM-DD
   ```

5. Add an optional "brief candidate" output:
   - if a batch changes a contested claim or strengthens a decision-relevant claim, the agent logs: "Brief candidate: update `flow-matching-vs-ar-codec-tts`."

6. Verify the `WIKI` path policy. The integration agent spec says to use `/speech-generation-wiki-content/`, while this workspace exposes `wiki/` as a submodule. That may be intentional for Claude agents on this machine, but it conflicts with the currently inspected workspace layout and should be checked before relying on it.

The integration agent is already the right place to implement the claim-graph direction. It needs stricter evidence schema, digest validation, concept-page slimming, and either a new brief-generation step or a companion brief agent.

## Ingest Agent Notes

File reviewed: `.claude/agents/speech-generation-ingest-agent.md`

The ingest agent is mostly well designed. It has a tight scope, a strong paper-page template, and much better claim instructions than the integration agent. But it also contains several internal contradictions and a few scripts that likely explain some of the drift seen in the wiki.

### What Works Well

- The scope boundary is good: one paper in, one paper page out. It correctly avoids concept pages, overview, reports, and cross-paper synthesis.
- The paper template is strong. It forces the sections that make the wiki valuable: `Problem`, `Method`, `Key Results`, `Novelty Assessment`, `Field Significance`, `Claims`, `Limitations`, and `Wiki Connections`.
- The claim instructions are especially good. They require field-level claims, prohibit paper-specific trivia, and require inline section citations. This is exactly what the claim-graph direction needs.
- The controlled vocabulary section is useful and more concrete than the general `CLAUDE.md` instructions. The special usage rules for `self-supervised-speech`, `prosody-control`, `disentanglement`, and `instruction-conditioned-tts` are practical and likely reduce noisy concept tagging.
- The figure-selection policy is sensible. It avoids embedding random result plots and reserves images for architectural novelty.

### Main Problems

- There are scope contradictions. The spec says "the only files you write are the five listed above," but the agent writes more than five categories: paper page, assets, `papers/index.md`, venue page, `venues/index.md`, `index.md`, `log.md`, and metadata. The "five listed" language should be corrected.
- There is a metadata contradiction. The `YOU DO` section says update `status` and `ingested_date` only. Step 7 also appends `generation_history`. The invariants again say not to alter metadata except `status` and `ingested_date`. Either `generation_history` is allowed or it is not.
- The paper-index script writes plain IDs, not wikilinks:

  ```python
  new_row = f'| {meta["id"]} | {title} | ... |'
  ```

  That likely explains why some `wiki/papers/index.md` rows are plain IDs instead of `[[id]]` links. It should write:

  ```markdown
  | [[id]] | [Title](papers/id.md) | ... |
  ```

  or at least:

  ```markdown
  | [[id]] | Title | ... |
  ```

- The figure-selection step depends on `field_significance.type` before the page exists. Step 2c says include figures only if the paper's `field_significance.type` includes `architectural-novelty`, but that field is assigned during Step 3. The workflow should either assign significance before figure selection or select figures after drafting frontmatter.
- The procedure says to check `wiki/papers/index.md` before creating a paper page, but the step-by-step procedure does not actually do that before writing. It only appears in the invariants. That should be promoted into Step 1.
- The index/venue update scripts are brittle under parallel ingest. They increment counts by regex and append rows independently. This is exactly where race conditions and count drift can happen. `INGEST_OPT_EXPERIMENT.md` already noted this risk.
- The agent does not validate the generated page. Given how important paper pages are as evidence units, it should run a post-write sanity check: parse YAML, verify required sections, verify claims have section citations, verify selected figure files exist, and verify controlled vocabulary fields.

### Claim-Graph Improvement

This agent is the best place to improve claim provenance because it reads the source paper. The integration agent only sees the paper page later.

Add a machine-readable claim block either in frontmatter or near the `## Claims` section. For example:

```yaml
claim_evidence:
  - claim: "Non-uniform ODE schedules can reduce flow-matching TTS inference with minimal quality loss."
    source: "§3.2, Table 1"
    role: supports
    concepts: [flow-matching, streaming-tts]
    confidence: high
```

The visible markdown claims can remain, but the structured block would make evidence digest updates much more reliable.

### Concrete Fixes

1. Fix the internal scope/metadata contradictions.
2. Add explicit duplicate check before writing `wiki/papers/{id}.md`.
3. Change paper index rows to use wikilinks consistently.
4. Move figure selection after frontmatter/significance assignment.
5. Add a post-write validator.
6. Add structured claim evidence with `claim`, `source`, `role`, `concepts`, and `confidence`.
7. Consider removing shared-file updates from parallel ingest workers and doing `index.md`, `venues/index.md`, and `log.md` in a batch cleanup step.

Overall: the ingest agent is conceptually strong. Its biggest weakness is not the writing instruction; it is operational hygiene around shared indexes, metadata rules, and machine-readable claim extraction.

## Structured Evidence Schema for Concept Appendices

Production concept appendices should be generated primarily from `wiki/concepts/_evidence/{slug}.yaml`, with supplemental canonical metadata pulled from paper-page frontmatter when needed.

The current concept YAML files are close to this, but they are still too prose-oriented and not structured enough for reliable generation. The YAML should become the source of truth for concept-specific evidence: which papers matter for this concept, which claims they support or challenge, how strong the evidence is, and whether the paper should be reassessed later.

The split should be:

```text
paper page/frontmatter = what the paper is
concept evidence YAML = what the paper means for this concept
generated appendix = readable projection of the YAML
concept page = compact synthesis from the YAML
```

### Proposed Top-Level Schema

```yaml
concept: flow-matching
last_updated: 2026-06-15
paper_count: 44

papers:
  - id: 2025.acl-long.313
    title: "F5-TTS: A Fairytaler that Fakes Fluent and Faithful Speech with Flow Matching"
    year: 2025
    venue: ACL
    task: [TTS]
    architecture: [flow-matching]
    relevance: high
    evidence_role:
      - core_evidence
      - acceleration_evidence
    contribution_type:
      - architectural-novelty
    current_role: influential
    publication_role: high
    method_family:
      - pure_nar_fm_tts
    claims:
      - claim_id: fm_alignment_without_phoneme_supervision
        role: supports
        claim: "Flow-matching TTS can learn text-speech alignment without explicit phoneme alignment."
        source: "§3.4, Table 2"
        evidence: "ConvNeXt text refinement fixes E2 TTS alignment failures and improves WER/UTMOS on LibriSpeech-PC."
        confidence: high
      - claim_id: fm_inference_scheduling_matters
        role: supports
        claim: "Non-uniform flow-step scheduling improves FM-TTS faithfulness without retraining."
        source: "§3.5, Figure 4"
        evidence: "Sway Sampling improves WER and UTMOS at matched NFE."
        confidence: high
    metrics:
      - name: WER
        value: 2.42
        system: "F5-TTS 32 NFE"
        testset: "LibriSpeech-PC test-clean"
      - name: UTMOS
        value: 3.89
        system: "F5-TTS 32 NFE"
        testset: "LibriSpeech-PC test-clean"
    limitations:
      - "Speaker similarity remains below Seed-TTS DiT and ground-truth recordings."
    caveats:
      - "Mel-spectrogram system; conclusions may not transfer to waveform-latent FM."
    related_concepts:
      - zero-shot-tts
      - evaluation-metrics
```

Key fields:

- `relevance`: how central the concept is to the paper (`high`, `medium`, `low`).
- `evidence_role`: what kind of evidence this paper contributes for this concept.
- `publication_role`: how important the paper looked at publication/ingest time.
- `current_role`: how the living review currently interprets the paper.
- `method_family`: normalized buckets used to generate appendix sections.
- `claims`: structured claim evidence with role, source location, confidence, and one-sentence evidence.
- `caveats`: concept-specific limits, separate from the paper's general limitations.

### Evidence Roles

Suggested controlled values:

```yaml
evidence_role:
  - core_evidence          # directly advances the concept
  - architecture_variant   # new system placement or design variant
  - acceleration_evidence  # speed, NFE, latency, RTF
  - control_evidence       # speaker/prosody/emotion/language/dialogue control
  - evaluation_caution     # metric or benchmark caution relevant to concept
  - historical_context     # predecessor or lineage evidence
  - negative_evidence      # contradicts or weakens a claim
  - infrastructure         # dataset, codec, benchmark, toolkit, objective
```

### Claim Clusters

Claim clusters should be first-class objects, separate from paper entries. Paper entries record paper-specific claims; claim clusters record canonical concept-level claims.

```yaml
claim_clusters:
  - id: fm_fewer_steps_than_diffusion
    claim: "Flow matching can reach useful speech quality with fewer inference steps than diffusion-style denoising."
    status: strongly_supported
    confidence: high
    supporting_papers:
      - 2025.acl-long.313
      - 2025.acl-long.1043
      - interspeech-2025-0554
      - interspeech-2025-0455
    contradicting_papers: []
    refining_papers:
      - interspeech-2025-2449
    caveats:
      - "Evidence strongest for mel-spectrogram and latent-mel systems."
      - "Subjective evaluation is inconsistent across papers."
    last_reviewed: 2026-06-15
```

Recommended `status` values:

```yaml
status:
  - strongly_supported
  - emerging
  - contested
  - weakened
  - superseded
  - historical
```

Recommended paper-to-claim `role` values:

```yaml
role:
  - supports
  - contradicts
  - refines
  - complicates
  - supersedes
  - historical_context
```

### Method Families

Method families should also be explicit. This lets a generated appendix group papers coherently instead of dumping one long `All Papers` table.

```yaml
method_families:
  - id: pure_nar_fm_tts
    name: "Pure non-autoregressive FM TTS"
    summary: "Text/reference speech are jointly modeled through speech infilling, then FM predicts the target acoustic trajectory."
    papers:
      - 2406.18009
      - 2025.acl-long.313
      - 2512.04720
    open_questions:
      - "How robust is alignment-free FM outside English/Mandarin?"

  - id: hybrid_ar_fm
    name: "AR/LLM-conditioned FM"
    summary: "An AR or LLM stage predicts semantic/prosodic structure, while FM handles acoustic synthesis or refinement."
    papers:
      - 2407.05407
      - 2412.10117
      - 2506.21619
      - 2025.acl-long.912
```

### Reassessment Queue

The `reassessment_queue` is how the living review avoids freezing a paper's importance at ingest time. A new paper may look high-impact when it appears, become minor after a year, or become foundational because later work adopts it. The queue records which papers or claims need to be revisited when enough time or evidence has accumulated.

This should not be a generic TODO list. Each item should have:

- `id`: paper or claim ID.
- `type`: what is being reassessed (`paper_role`, `claim_status`, `method_family`, `benchmark_validity`).
- `reason`: why reassessment is needed.
- `trigger`: what event should cause reassessment.
- `due`: calendar checkpoint if no trigger fires.
- `current_assessment`: current interpretation.
- `possible_outcomes`: what statuses it might move to.
- `watch_for`: concrete signs in future ingests.

Example:

```yaml
reassessment_queue:
  - id: 2603.29339
    type: paper_role
    reason: "Waveform-latent FM may become influential if independently replicated."
    current_assessment: frontier_probe
    trigger: "Reassess after 3+ follow-up papers cite or adopt waveform-latent FM, Wav-VAE-style latents, or the prompt-region mismatch fix."
    due: 2026-12
    possible_outcomes:
      - influential
      - active_evidence
      - minor
    watch_for:
      - "Independent replication on public or semi-public benchmarks."
      - "Use of waveform VAE latents in non-Meituan systems."
      - "Adoption of the prompt-region trajectory correction in F5/E2-style systems."

  - id: 2509.09631
    type: method_family
    reason: "Discrete flow matching could become a major alternative if acceleration and speaker similarity improve."
    current_assessment: frontier_probe
    trigger: "Reassess after a follow-up reaches competitive speaker similarity or sub-16 NFE with subjective validation."
    due: 2026-12
    possible_outcomes:
      - emerging_family
      - minor_variant
      - superseded
    watch_for:
      - "Cross-attention or local timbre conditioning fixes speaker similarity."
      - "Discrete FM used outside FACodec."
      - "Multilingual or large-scale training results."

  - id: fm_cfg_transferability
    type: claim_status
    reason: "Current negative evidence comes mainly from two systems and may be model-specific."
    current_assessment: contested
    trigger: "Reassess after 3+ systems evaluate speech-specific CFG strategies across at least two languages."
    due: 2026-06
    possible_outcomes:
      - strongly_supported
      - contested
      - weakened
    watch_for:
      - "Replication of Mandarin/English behavior gap."
      - "Ablations isolating text encoder, tokenizer, and language effects."
      - "Subjective evaluation of CFG changes, not only WER/SIM."
```

### How Reassessment Works in Practice

During monthly ingest:

1. New papers are mapped to concept claims and method families.
2. The integration pass checks whether any `trigger` conditions are met.
3. If a trigger is met, the agent updates `current_role`, claim `status`, and caveats.
4. If no trigger is met but `due` has passed, the item is surfaced for a periodic review.
5. The concept page only changes when reassessment changes the current synthesis.

This preserves historical context without overreacting to every new paper.

Example interpretation:

```yaml
role_history:
  - date: 2025-09
    role: frontier_probe
    reason: "First direct discrete FM TTS baseline over factorized codec tokens."
  - date: 2026-12
    role: influential
    reason: "Three follow-up systems adopt discrete FM with improved speaker conditioning."
```

Or, in the opposite direction:

```yaml
role_history:
  - date: 2025-12
    role: high
    reason: "Claimed SOTA on a major benchmark."
  - date: 2026-12
    role: minor
    reason: "Later re-evaluation showed gains were benchmark-specific and the method was not adopted."
```

The key principle: paper pages preserve what the paper contributed at publication time; concept YAML preserves the living review's current interpretation.

### Generated Outputs From This Schema

From this one YAML, scripts or agents can generate:

- lightweight concept page: compact synthesis, major claims, tensions, open questions
- evidence appendix: paper tables, method-family tables, claim support matrix
- monthly reports: claims strengthened, weakened, contested, or superseded
- dashboard: stale claims, overdue reassessments, malformed evidence entries
- frontier briefs: decision-oriented memos based on current claim status

This avoids hand-maintaining long markdown tables while keeping the concept page readable.

## Dashboard Proposal

A useful dashboard would be an **operational quality dashboard** for the living review. It should answer: "Is the knowledge base healthy, current, and trustworthy?"

Suggested location:

```text
STATUS_DASHBOARD.md
```

This should probably start in the infra repo because it is mostly operational. Later, a reader-facing version could live under:

```text
wiki/reports/dashboard.md
```

### Example Dashboard Shape

```markdown
# Speech Generation Wiki Dashboard

Generated: 2026-06-16

## Corpus Status

| Metric | Count |
|--------|------:|
| Metadata files | 1326 |
| Accepted, not ingested | 756 |
| Ingested papers | 281 |
| Integrated papers | 276 |
| Concept pages | 24 |
| Evidence digests | 24 |
| Papers missing wiki page | 5 |
| Wiki pages missing metadata | 0 |

## Ingest Health

| Check | Status | Notes |
|------|--------|-------|
| All ingested metadata have paper pages | warning | 5 missing |
| All paper pages parse as YAML | ok | 281/281 |
| Required sections present | warning | 17 missing `## Claims` citations |
| Paper index links valid | warning | 29 plain IDs, not wikilinks |
| Figure references valid | ok | 42/42 assets exist |

## Integration Health

| Check | Status | Notes |
|------|--------|-------|
| Integrated date set | warning | 5 ingested papers not integrated |
| Concept digests parse as YAML | warning | `flow-matching.yaml` malformed |
| Related concepts exist | ok | 100% valid |
| Concept counts match digest counts | warning | 6 mismatches |
| Overview current | warning | Says 225 papers; index says 251 |

## Claim Graph Health

| Metric | Count |
|--------|------:|
| Canonical claim clusters | 184 |
| Strongly supported claims | 62 |
| Emerging claims | 91 |
| Contested claims | 21 |
| Weakened/superseded claims | 10 |
| Claims missing source citations | 38 |
| Claims overdue for reassessment | 7 |

## Reassessment Queue

| Item | Type | Due | Trigger | Status |
|------|------|-----|---------|--------|
| `2603.29339` | paper role | 2026-12 | 3+ follow-ups adopt waveform-latent FM | watching |
| `2509.09631` | method family | 2026-12 | discrete FM improves SIM or NFE | watching |
| `fm_cfg_transferability` | claim status | 2026-06 | 3+ systems evaluate CFG across languages | due |

## Stale Pages

| Page | Last Updated | Reason |
|------|-------------|--------|
| `overview.md` | 2026-06-13 | count mismatch |
| `concepts/flow-matching.md` | 2026-06-13 | digest malformed |
| `concepts/evaluation-metrics.md` | 2026-06-13 | 12 new papers since update |

## Broken Links

| Source | Target | Problem |
|--------|--------|---------|
| `papers/index.md` | `interspeech-2025-2765` | plain ID, not wikilink |
| `concepts/flow-matching.md` | `2510.02848` | target page missing or not ingested |
```

### What It Should Track

The dashboard should have five layers.

#### 1. Corpus State

Basic counts:

- metadata files
- accepted papers
- parsed papers
- ingested papers
- integrated papers
- rejected/review/pending papers
- papers ready to ingest

#### 2. Wiki Integrity

Checks that the markdown graph is structurally valid:

- metadata marked `ingested` but no `wiki/papers/{id}.md`
- paper page exists but metadata missing
- malformed YAML frontmatter
- required sections missing
- missing claim citations
- invalid wikilinks
- missing figure assets
- inconsistent paper counts

#### 3. Concept Evidence Health

Checks for the concept layer:

- all evidence YAML files parse
- `paper_count` matches actual entries
- claim clusters have supporting papers
- supporting paper IDs exist
- related concept slugs are valid
- concept pages stale relative to digest
- digest has malformed sections

#### 4. Claim Graph Health

This is the unique living-review part:

- number of claim clusters
- status distribution
- claims missing citations
- claims with only one supporting paper
- contested claims needing review
- claims not reviewed in 6 or 12 months
- claims affected by new papers this month
- claims weakened or superseded

#### 5. Reassessment Queue

This is how the dashboard prevents old judgments from freezing:

- papers due for reassessment
- claims due for reassessment
- triggers that fired
- overdue items
- role changes since last report

### Implementation

Generate the dashboard with a script:

```text
scripts/wiki/dashboard.py
```

Inputs:

```text
raw/metadata/*.json
wiki/papers/*.md
wiki/concepts/*.md
wiki/concepts/_evidence/*.yaml
wiki/index.md
wiki/overview.md
wiki/papers/index.md
wiki/venues/index.md
```

Output:

```text
STATUS_DASHBOARD.md
```

or later:

```text
wiki/reports/dashboard.md
```

### Most Important Checks To Start With

If building this incrementally, start with:

1. Metadata/wiki consistency.
2. YAML parse validation.
3. Required paper sections.
4. Claims missing `*(§...)*` citations.
5. Concept digest `paper_count` mismatch.
6. Paper-count mismatch across `STATUS.md`, `wiki/index.md`, `wiki/overview.md`, `wiki/papers/index.md`.
7. Broken wikilinks.

These checks would catch most of the issues observed during this review.

## Tier 1 vs. Tier 2 Reader Display

Tier information should be visible but unobtrusive. The reader should immediately know whether they are reading a full evidence page or a context/reference stub.

### Frontmatter

Every paper page should expose tier information structurally:

```yaml
ingest_tier: 1
tier_role: evidence
tier_reason: "Direct evidence for flow-matching zero-shot TTS."
```

or:

```yaml
ingest_tier: 2
tier_role: backbone
tier_reason: "General-purpose LLM backbone cited by speech-generation systems; included for context."
```

This supports filtering, dashboards, generated indexes, and reader-facing labels.

### Page-Level Display

For Tier 1, no special warning is needed. The full paper page structure already signals that it is evidence-bearing.

For Tier 2, add a small plain-text line near the top:

```markdown
_Reference stub: included for context because this paper is cited by speech-generation work; not treated as primary evidence for speech-generation claims._
```

This is preferable to a callout if callout usage should remain sparse.

Tier 2 abstract card example:

```markdown
> [!abstract] arXiv · 2023 · Preprint · Reference Stub
> **OpenAI** · [→ Paper](...)
>
> GPT-4 is included as context because later spoken-language and multimodal systems use GPT-style LLMs as reasoning backbones.

_Reference stub: included for context; not treated as primary evidence for speech-generation claims._
```

### Paper Index Column

Add a `Role` or `Tier` column to `wiki/papers/index.md`:

```markdown
| ID | Title | Role | Org | Venue | Year | Task | Architecture | Ingested |
|----|-------|------|-----|-------|------|------|--------------|---------|
| [[2025.acl-long.313]] | F5-TTS | Evidence | SJTU | ACL | 2025 | TTS | flow-matching | 2026-06-01 |
| [[2303.08774]] | GPT-4 Technical Report | Context: backbone | OpenAI | arXiv | 2023 | — | autoregressive-LM | 2026-06-10 |
```

This is probably the most useful reader-facing display because readers encounter tier information before opening a page.

### Concept Pages

Concept pages should distinguish direct evidence from context/foundation papers:

```markdown
## Representative Papers

### Core Evidence
- [[2025.acl-long.313]] — establishes open-weight flow-matching zero-shot TTS.
- [[2025.acl-long.1043]] — learned-prior FM for one-step inference.

### Context and Foundations
- [[2210.02747]] — generic flow-matching objective.
- [[2207.12598]] — classifier-free guidance mechanism later adapted by FM-TTS.
```

This makes it clear that generic method papers are important but not equivalent to direct speech-generation evidence.

### Appendix Tables

Generated concept evidence appendices should include tier and role:

```markdown
| Paper | Tier | Role | Evidence Role | Current Role | Why Included |
|------|------|------|---------------|--------------|--------------|
| [[2025.acl-long.313]] | 1 | evidence | core_evidence | influential | Direct FM-TTS system |
| [[2210.02747]] | 2 | method_foundation | historical_context | foundational context | Generic FM objective |
| [[2207.12598]] | 2 | method_foundation | historical_context | foundational context | CFG mechanism |
```

### Search and Filter UX

If using Obsidian/Quartz or generated indexes, add tags/frontmatter:

```yaml
tags:
  - paper
  - tier-2
  - context/backbone
```

Scripts can also generate separate indexes:

```text
wiki/papers/evidence.md
wiki/papers/context.md
```

### Reader-Facing Labels

Avoid labels like `minor` or `low-value` in reader-facing pages. Those are internal assessment terms and create bad UX.

Recommended display labels:

- Tier 1: `Evidence`
- Tier 2: `Reference Stub`
- Role examples:
  - `Context: backbone`
  - `Context: dataset`
  - `Context: optimizer`
  - `Foundation: method`
  - `Citation bridge`

Best rule: Tier 2 should not feel like a low-quality page. It should feel like a deliberate citation/context page.

## Survey Paper Handling

Surveys should be handled as **synthesis/context papers**, not as ordinary evidence papers.

They are valuable, but they are a different kind of artifact. A survey usually does not provide new experimental evidence; it organizes prior evidence, proposes a taxonomy, identifies trends, or frames open problems. That means it should not support claims in the same way a primary experimental paper does.

### Recommended Role

Use a distinct role:

```yaml
tier_role: survey
evidence_role:
  - historical_context
  - taxonomy
  - synthesis
```

Reader-facing note:

```markdown
_Reference survey: included for taxonomy, historical framing, and coverage of pre-corpus literature; not treated as primary experimental evidence unless it reports original analyses._
```

### Tier Choice

Surveys can be Tier 1 or Tier 2 depending on their function.

Tier 1 survey:

- central to the field's self-understanding
- introduces a taxonomy used by the wiki
- synthesizes a major area directly in scope
- has original analysis, meta-analysis, benchmark comparison, or systematic review methodology
- materially affects concept pages

Tier 2 survey:

- broad adjacent-field overview
- useful for citation context only
- not central enough to alter current concept claims
- mostly used to explain background

### How Surveys Should Contribute

Surveys should contribute to:

- Historical Context
- Taxonomy
- Terminology
- Open Questions
- Related Work Map
- Concept Boundaries

They should be used carefully in `Major Claims`.

Acceptable survey-derived claim:

```yaml
claims:
  - claim: "By 2021, neural TTS research was organized around acoustic models, vocoders, and end-to-end systems."
    role: historical_context
    source: "§2, §4"
    confidence: high
```

Less acceptable unless the survey performed original systematic analysis:

```yaml
claims:
  - claim: "Diffusion vocoders outperform GAN vocoders."
    role: supports
```

That kind of experimental claim should be supported by primary papers, not repeated survey statements.

### Survey Page Template

Surveys should not necessarily use the same page structure as system papers. Suggested template:

```markdown
## Scope

What literature does the survey cover? What years, tasks, and model families?

## Taxonomy

What organizing framework does it introduce?

## Key Synthesis Points

What field-level patterns does it identify?

## Historical Context

What does it tell us about the state of the field at the time?

## Limitations

What is missing due to publication date, scope, or methodology?

## Wiki Connections

Which concept pages use this survey for taxonomy or history?
```

No `Key Results` unless the survey has original quantitative analysis.

No architecture figure unless the survey introduces a taxonomy diagram worth preserving.

### Survey Frontmatter

```yaml
ingest_tier: 1
tier_role: survey
survey_type: narrative | systematic | meta-analysis | taxonomy | benchmark-survey
evidence_role:
  - taxonomy
  - historical_context
  - synthesis
claim_policy: secondary_only
```

If it has original analysis:

```yaml
claim_policy: primary_for_original_analysis
```

### Concept Evidence YAML for Surveys

```yaml
papers:
  - id: 2106.15561
    tier_role: survey
    survey_type: taxonomy
    evidence_role: [historical_context, taxonomy]
    relevance: medium
    current_role: historical_context
    claims:
      - claim_id: pre_codec_tts_taxonomy
        role: historical_context
        claim: "Pre-2022 neural TTS was commonly organized around acoustic models, neural vocoders, and end-to-end systems."
        source: "§2, §4"
        confidence: high
      - claim_id: explicit_duration_alignment_pre_2022
        role: historical_context
        claim: "Before codec-LM and flow-matching TTS, explicit duration modeling was the dominant solution to robust non-autoregressive alignment."
        source: "§3.4, Table 11"
        confidence: medium
    caveats:
      - "Predates codec language modeling, modern flow matching, and LLM-based TTS."
```

### Reader Display

In paper index:

```markdown
| [[2106.15561]] | A Survey on Neural Speech Synthesis | Survey: taxonomy | arXiv | 2021 |
```

On concept pages:

```markdown
### Context and Surveys
- [[2106.15561]] — useful taxonomy for pre-codec neural TTS; predates modern flow-matching and codec-LM systems.
```

In appendices:

```markdown
| Paper | Tier | Role | Use |
|------|------|------|-----|
| [[2106.15561]] | 1 | Survey: taxonomy | Historical framing for pre-2022 TTS architecture families |
```

### Important Rule

Never let surveys inflate evidence counts for experimental claims.

If three surveys all repeat "diffusion is slow," that is not three independent pieces of primary evidence. It is secondary evidence. The claim should be supported by the original diffusion papers or benchmark papers.

Claim clusters should distinguish:

```yaml
supporting_papers: [...]
secondary_sources: [...]
historical_sources: [...]
```

Example:

```yaml
claim_clusters:
  - id: diffusion_slow_inference
    claim: "Diffusion TTS requires iterative sampling that creates inference latency."
    status: strongly_supported
    supporting_papers:
      - 2105.06337
    secondary_sources:
      - 2106.15561
```

Bottom line: surveys are useful for taxonomy, historical framing, terminology, identifying open problems, and mapping adjacent literature. They should be treated as **secondary synthesis**, not primary experimental evidence, unless they contain original systematic analysis.

## Evidence Dossiers Instead of Appendices

The earlier "appendix" idea should be reframed. The appendix should not be thought of as part of a concept page. It is cleaner to treat it as a separate artifact: an **evidence dossier**.

The hierarchy becomes:

```text
Claim graph
  -> Concept page
  -> Evidence dossier
  -> Trend/report
  -> Brief
  -> Dashboard
```

Each artifact has a different job:

- **Claim graph**: structured source of truth.
- **Concept page**: compact synthesis of what the field currently believes.
- **Evidence dossier**: detailed audit trail behind a concept, claim, benchmark, or debate.
- **Trend/report**: what changed over time.
- **Brief**: decision-oriented answer.
- **Dashboard**: operational health/status.

Instead of:

```text
concept page + appendix
```

think:

```text
concept synthesis + evidence dossier
```

The dossier is related to a concept, but it is its own output type. It should be generated from the claim graph, not manually maintained as an appendix to a page.

Possible paths:

```text
wiki/concepts/flow-matching.md
wiki/evidence/flow-matching.md
wiki/briefs/flow-matching-vs-ar-codec-tts.md
wiki/reports/quarterly/2026-Q2.md
```

or:

```text
wiki/dossiers/flow-matching.md
```

Possible labels:

- Evidence Dossier
- Concept Evidence
- Evidence Ledger
- Claim Support Matrix

Preferred label: **Evidence Dossier**, because it signals "this is where the receipts live."

A concept page can link out:

```markdown
## Evidence

For the full paper-level support matrix, caveats, and reassessment queue, see [[evidence/flow-matching]].
```

The evidence dossier would include:

- canonical claims
- supporting, contradicting, and refining papers
- method-family tables
- metric snapshots
- caveats
- reassessment queue
- historical/context sources
- low-confidence evidence
- papers excluded from direct evidence

This distinction is useful because evidence dossiers do not have to be limited to concepts. Future dossiers could cover:

- a concept: `flow-matching`
- a claim: `fm-fewer-steps-than-diffusion`
- a benchmark: `seed-tts-eval`
- a debate: `automatic-speaker-similarity-validity`
- a system family: `cosyvoice-lineage`

The key shift: dossiers are standalone evidence artifacts generated from the claim graph. They extend concept pages, but they are not subordinate to them.
