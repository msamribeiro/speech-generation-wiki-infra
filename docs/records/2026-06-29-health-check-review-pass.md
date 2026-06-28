# Health-Check Review Pass — Complete Record

Document type: operational record  
Completed: 2026-06-29  
Sessions: multiple (2026-06-23 start; arXiv batch completed 2026-06-29)

---

## Summary

Full review pass on all ingested Tier 1 wiki pages that failed
`scripts/health_check.py --module ingest`. Two error classes were targeted:

- **`required_fields`** — missing `field_significance` frontmatter block
- **`claims_section`** — missing `## Claims` section, or claim bullets lacking `*(§N.N)*` inline citations

**Total papers reviewed: 138** across all venues.  
**Final state: 0 errors corpus-wide** (confirmed by full ingest health check on 2026-06-29).

Venue breakdown:
- Interspeech 2025: complete (prior sessions)
- ACL / EMNLP / NAACL / COLING: complete (prior sessions)
- arXiv (Oct 2025 – Apr 2026): 16 papers, completed 2026-06-29

Commits:
- Wiki content repo: `9d42a21` (arXiv batch, 2026-06-29); earlier commits for prior venue batches
- Infra repo: `ad149eb` (metadata + session notes, 2026-06-29)

---

## Approach

Batches of 4, processed sequentially (never in parallel):

1. Snapshot each file to `/tmp/{ID}.before.md`
2. Run `speech-generation-review-agent` on each paper
3. Diff before/after and critique — flag hallucinated metrics, outrageous/exaggerated claims, wrong types, wikilink violations
4. Fix any issues found in the diff
5. Health check each paper against the standalone content repo:
   ```bash
   WIKI=/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content
   .venv/bin/python scripts/health_check.py --module ingest --id {ID} --wiki-dir "$WIKI" -v
   ```
6. Report batch summary; add flags to Manual Verification List

---

## Recurring agent failure patterns

These appeared consistently across all batches and should inform future review agent prompts or spec updates.

### 1. F5-TTS canonical ID

The agent repeatedly used arXiv ID `2410.06885` instead of the canonical ACL ID `2025.acl-long.313`. This affected both `related_papers` frontmatter and Wiki Connections wikilinks. Fixed manually in every occurrence.

### 2. Invalid `field_significance.type` values

The agent invented types outside the controlled vocabulary:
- `evaluation-contribution` (2603.08823) → correct: `empirical-benchmark`
- `dataset-contribution` (2604.00688) → correct: `empirical-benchmark`

Valid types: `architectural-novelty`, `engineering-integration`, `empirical-benchmark`, `conceptual-contribution`.

### 3. Wikilink format violations in preserved prose

Three anti-patterns appeared in Wiki Connections sections the agent did not rewrite:
- `[[id]] (Name)` — most common; fix to `[[id|Name]]`
- `Name ([[id]])` — fix to `[[id|Name]]`
- `[[id]]` bare — acceptable only when no clean system/model name exists

The review agent correctly fixed its own new output but left pre-existing violations in preserved prose. Manual post-diff cleanup was needed on most papers. Grep to check:
```bash
grep "\[\[[0-9]\|interspeech\|acl\|emnlp\|naacl" $WIKI/papers/{ID}.md | grep -v "|"
```

### 4. Ghost papers in `related_papers`

Several papers had `related_papers` entries referencing IDs with no wiki page:

| Paper | Ghost IDs removed |
|-------|------------------|
| 2603.18090 (MOSS-TTS) | 2602.10934, 2512.23808, 2509.24650 |
| 2603.29339 (LongCat-AudioDiT) | 2509.24650, 2509.22167 |

`2509.24650` (VoxCPM) appeared as a ghost in multiple papers.

### 5. Causal language in claims

The agent frequently used "because", "primarily because", "eliminates", and "necessary" in claim bullets — sometimes accurately (paper states the mechanism directly) but often as inference. All such claims were flagged for manual verification.

### 6. `field_significance` type/prose inconsistency

In several cases the agent wrote Field Significance prose describing a "training-recipe" contribution, then tagged `type: architectural-novelty`. The vocab's definition includes "training objective" under architectural-novelty, but when the prose itself contradicts the tag it is worth a second look.

---

## Manual Verification List

68 items requiring a human to open the PDF and check the specific section/table cited. Priority for items marked as metric corrections — those affect structured data.

| Paper ID | Issue | Where to check |
|----------|-------|----------------|
| 2025.acl-long.911 | Claim 3: "peaks at 4–6 dialogue turns, degrades beyond 8" — very specific, easy to hallucinate | Appendix F, Table 3 |
| 2025.acl-long.911 | Claim 2: "codec TTS outperforms prompt-based baselines on most metrics" | §4.4, Table 2 |
| 2507.22746 | Claim 2: "12.5 Hz frame rate — STFT vocoders suffer significant quality degradation" | §4.3.3, Table 4 |
| 2508.00317 | Claim 3: "challenges accelerate progress more reliably than individual papers" — normative editorial claim | §I, §II.E |
| 2508.00317 | field_significance.type: empirical-benchmark — judgment call on a perspective/survey paper | Verify paper framing |
| 2025.acl-long.912 | Field Significance: "orders of magnitude less training data" vs. native SpeechLMs — may overstate | §5 / intro comparison |
| 2025.acl-long.912 | Claim 3: "training from scratch fails to converge" — strong negative finding | §5.2, Table 3 |
| 2025.acl-short.81 | Field Significance: "first large-scale Vietnamese corpus with speaker identity" — "first" claim | §1 / related work |
| 2025.acl-short.81 | Claim 2: "architectural failure modes" on XTTS-v2 — strong characterization of empirical failure | §4 |
| 2508.02013 | Claim 1: "more strongly determined by LLM text reasoning" — strong causal interpretation of correlation data | §5.2 |
| 2508.02013 | Claim 4: "capability gap, not merely a performance gap" — editorial framing unlikely verbatim in paper | §5.2, Table 2 |
| 2025.americasnlp-1.1 | Field Significance: "first speech corpus and TTS system for Shipibo-Konibo" — "first" claim | §1 / related work |
| 2025.americasnlp-1.1 | Claim 3: "pronunciation drift causes natural speech to score lower than synthetic on intelligibility" — counterintuitive | §5.4 |
| 2508.02038 | Claim 5: "male speakers underperform female on emotion recognition across most categories" — specific bias finding | §4.4, Figure 6 |
| 2508.02038 | field_significance includes architectural-novelty — borderline; orthogonality constraint may be engineering-integration only | Judgment call |
| 2508.02849 | Claim 1: "HuBERT/WavLM distillation does not achieve true semantic disentanglement" — strong critique | §II.A, §V.B |
| 2508.02849 | Claim 5: "staged training is necessary for stable convergence" — "necessary" overstates an ablation result | §III.E, §V.C, Table II |
| 2025.coling-main.518 | Claim 3: "flow matching comparable quality to diffusion at lower cost" — requires direct diffusion baseline in paper | §3.4, Table 3 |
| 2508.03543 | **Metric correction**: EI-MOS 4.00 changed from E2-TTS to F5-TTS variant | §4.2, Table 1 |
| 2508.03543 | Claim 4: layer counts 22/8/56 for F5-TTS/E2-TTS/CosyVoice2 — specific numbers | §4.5 |
| 2025.emnlp-demos.70 | Field Significance: "first fully open-source SCA with empathy support" — "first" claim | §1 / related work |
| 2025.emnlp-demos.70 | **Metrics**: VoiceBench commoneval 3.65 and wildvoice 3.66 recovered | Table 2 |
| 2025.emnlp-main.1730 | Claim 3: "4.20M trainable LoRA parameters" — very specific number | §6.3 |
| 2025.emnlp-main.1730 | Claim 4: Vicuna vs LLaMA vs Qwen comparison — verify these are the actual models | §6.3.1, Table 3 |
| 2508.04996 | Claim 4: "order of magnitude" reduction (32→4 steps = 8x, not 10x) — technically overstated | §II.D, Table I |
| 2025.emnlp-main.180 | Claim 3: "necessary... omitting any stage degrades quality" — strong word for an ablation | §4.3, Table 2 |
| 2025.emnlp-main.180 | Wiki Connections: "first large-scale open-source dataset" — pre-existing "first" claim | §1 / related work |
| 2025.emnlp-main.989 | Field Significance: "reduces pronunciation errors by almost half" — no citation | §5.3 |
| 2025.emnlp-main.989 | Claim 3: "ASR and TTS pretraining do not improve spoken QA" — strong negative, ablation result | §5.2, Table 3 |
| 2025.emnlp-main.989 | Claim 4: "two orders of magnitude more data" + "~6,000 hours synthesized speech" — both specific | §5.1, Table 1 |
| 2508.05207 | **Metric correction**: MUSHRA renamed to ViSQOL (subjective→objective) — major category change | Table 1 |
| 2508.05207 | Claim 5: "80 ms latency on desktop CPU at 48 kHz stereo" — specific hardware claim | §1, §2 |
| 2508.05385 | **Metrics**: CLAP-Score 0.187 and IMOS 3.48 recovered | Table 2 |
| 2508.05385 | Claim 3: "NV detection generalises across structurally different languages without retraining" — strong cross-lingual claim | §2.2, §3 |
| 2025.findings-acl.1051 | Claim 2: "end-to-end speech LLMs consistently show degraded language understanding" — "consistently" is strong | §6.4, Table 1 |
| 2025.findings-emnlp.424 | Claim 1: "necessary for classifying conversational events accurately" — "necessary" for a dataset ablation | §4.1, Table 2 |
| 2025.findings-emnlp.424 | Claim 5: "synthetic TTS quality comparable to or exceeding Fisher and Switchboard" — strong comparison | §4.2, Table 3 |
| 2508.06262 | **Metrics**: WER 3.07%→14.37% and SPK-SIM 0.570→0.463 — specific paired values | §V, Table III |
| 2508.06262 | Claim 2: "1.48x" acceleration; Claim 4: "approximately 95%" quality retention — specific numbers | §IV.B Table I; §IV.C Table II |
| 2508.14049 | **Metric correction**: French WER changed 6 → 18 | Table 2 |
| 2510.02848 | **Metric correction**: WER 3s prompt changed 0.05 → 0.04 | Table 1 |
| 2510.05758 | Claim 4: "emphasis on adverbs/adjectives produces stronger intensity than on verbs/nouns" — POS-category ranking | §3.2, Figure 2 |
| 2510.07979 | Claim 4: training instability manifests as degraded subjective quality even when objective metrics appear competitive | §4.3, Table 2 |
| 2510.07979 | Claim 5: larger teacher model during distillation improves smaller student | §4.2.3, Table 1 |
| 2510.12210 | **Metrics**: SPK-SIM 0.66 / UTMOS 4.05 for proposed (medium, 0.3B) on SeedTTS test-en | Table 1 |
| 2510.12210 | Claim 3: "tail-first confidence bias" — paper-coined terminology, verify it appears in the paper | §3.4 |
| 2511.12347 | Claim 1: "near-random and functional output" — strong language for ablation failure | §3.4, §D.1, Table 9 |
| 2511.12347 | Claim 3: "pre-training reducing WER by 5–10x for low-resource languages" — specific range | §4.3, Table 2 |
| 2511.12347 | Claim 5: "larger systems trained on 30K–130K hours" — specific data scale comparison | §4.2, Table 1 |
| 2512.04720 | **Metric correction**: WER 1.36 → 1.48 for M3-TTS-Fbank on Seed-TTS test-en | Table 1 |
| 2512.04720 | Claim 2: "roughly 3x" training acceleration with VAE latents | §2.2, §4.3, Table 2 |
| 2512.13251 | Claim 3: soft vs. hard orthogonality three-way ablation comparison | §3.1.1, Appendix B, Table 6 |
| 2512.14291 | **Metrics**: SPK-SIM 76.4, 67.2, 68.1 and WER 1.91 — multiple new values added | Table 3 |
| 2512.14291 | Claim 1: "reduce phoneme error rate by more than half" with hybrid phoneme-text input | §2.6, §3.4, Table 7 |
| 2512.14291 | Claim 2: "without reward hacking" — design assurance claim, not empirically measured | §2.4, §3.3, Table 4 |
| 2512.14291 | Claim 3: laughter trade-off causation ("because laughter segments resist ASR transcription") | §3.3, Table 6 |
| 2512.14291 | Claim 5: "15% of backbone parameters" for LoRA — specific, weak citation (§2.5 only) | §2.5 |
| 2601.03888 | Claim 1: "no measurable degradation" from halving codec frame rate 50→25 Hz | §3.2, Table 4 |
| 2601.03888 | Claim 2: Japanese-specific finding within multi-language comparison | §4.3, Table 1 |
| 2601.15621 | Claim 2: "reduces sequence length and error accumulation" — "error accumulation" is causal, no table | §4.2.1 |
| 2601.15621 | Claim 5: "open-source systems match or exceed commercial baselines" on instruction-following benchmarks | §4.2.4, Table 8 |
| 2603.08823 | Claim 1: "eliminates the distribution shift" — likely overstates; probably "reduces" or "mitigates" | §3, §4.3 |
| 2603.08823 | Claim 5: "can match or exceed closed-source systems" — broad generalization | §6.1, Tables 1–2 |
| 2603.18090 | Claim 3: "duration control can emerge from paired pretraining format alone" — "emerge" is strong | §6.4, Table 5 |
| 2603.18090 | Claim 4: "cumulative speaker drift is the dominant failure mode in ultra-long AR speech generation" — class-level characterization | §6.5, Table 6, Figure 6 |
| 2603.26364 | field_significance level: high — borderline for a fine-tuning paper; formal theorem may justify it | Judgment call |
| 2603.26364 | Claim 3: "formal bound on the suboptimality of AR predictors" — mathematical claim (ε-forward dependence theorem) | §3.3 |
| 2603.29339 | Claim 1: "primarily because high-frequency acoustic detail is preserved end-to-end" — causal interpretation | §5.3.1, Table 3 |
| 2603.29339 | Claim 3: "increasing VAE fidelity degrades downstream quality" — counterintuitive causal finding | §5.3.2, Figure 3 |
| 2604.00688 | Claim 4: "CER below 5% for languages with fewer than 10 hours" — two specific thresholds | §4.2, Table 4, Figure 4 |
| 2604.00688 | **Metrics**: UTMOS 4.23→4.32 and SIM-o 0.697→0.668 from prompt denoising — four specific values | §4.3, Table 7 |
| 2604.01760 | Claim 4: "cross-lingual generalization stronger for typologically adjacent languages" — no table citation | §5.2 |
| 2604.01760 | Claim 5: "near-complete synthesis failure" from removing duration control at inference | §4.2, §5.3, Table 3 |
| 2604.12438 | Claim 3: "phonetically transparent languages tolerate 12.5 Hz better than deep-orthography languages" — typology framing | §4.3, Table 8 |
