# Review Session Context

Temporary working document for the ongoing health-check review pass. Delete when all flagged papers are cleared.

See `memory/project_health_check_review_pass.md` for the durable version of this context.

---

## Task

Fix all pages failing `scripts/health_check.py --module ingest`. Two error classes:

- **`required_fields`** — missing `field_significance` frontmatter block
- **`claims_section`** — missing `## Claims` section, or claim bullets lack `*(§N.N)*` citations

Current scope: all venues — Interspeech 2025, ACL/EMNLP/NAACL/COLING, and arXiv.

---

## Approach

For each batch of 4 papers (process one at a time — never in parallel):

1. **Snapshot** current files before any changes:
   ```bash
   cp /path/to/speech-generation-wiki-content/papers/{ID}.md /tmp/{ID}.before.md
   ```

2. **Run review agent** (`speech-generation-review-agent`) on each paper sequentially. Wait for each to finish before starting the next.

3. **Diff** the before and after to inspect every change:
   ```bash
   diff /tmp/{ID}.before.md /path/to/speech-generation-wiki-content/papers/{ID}.md
   ```

4. **Summarise and critique the diff.** Look for:
   - Hallucinated metric values or section references
   - Wrong `field_significance.type` (common: `architectural-novelty` applied to `engineering-integration` papers)
   - Wrong or missing `related_concepts` additions/removals
   - Bare wikilinks in newly added Wiki Connections prose (see Helper Notes below)
   - Figure embeds on Interspeech papers (see Helper Notes below)

5. **Fix any issues** found in the diff before running the health check. Add contentious topics (ambiguous claims, hard-to-verify metrics, uncertain task tags) to the **Manual Verification List** below.

6. **Health check** against the standalone content repo — no commit or push needed:
   ```bash
   WIKI=/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content
   .venv/bin/python scripts/health_check.py --module ingest --id {ID} --wiki-dir "$WIKI" -v
   ```

7. **Stop and report** — summarise all 4 papers, flag concerns, wait for go-ahead before next batch.

---

## Manual Verification List

Papers with contentious topics flagged during review — require human spot-check before site bump.

| Paper ID | Issue | Notes |
|----------|-------|-------|
| 2025.acl-long.911 | Claim 3: "peaks at 4–6 dialogue turns, degrades beyond 8" — very specific, easy to hallucinate | Check Appendix F, Table 3 |
| 2025.acl-long.911 | Claim 2: "codec TTS outperforms prompt-based baselines on most metrics" | Check §4.4, Table 2 |
| 2507.22746 | Claim 2: "12.5 Hz frame rate — STFT vocoders suffer significant quality degradation" — specific quantitative claim | Check §4.3.3, Table 4 |
| 2508.00317 | Claim 3: "challenges accelerate progress more reliably than individual papers" — normative editorial claim | Check §I, §II.E |
| 2508.00317 | field_significance.type: empirical-benchmark → conceptual-contribution — judgment call on a perspective/survey paper | Verify paper framing |
| 2025.acl-long.912 | Field Significance: "orders of magnitude less training data" vs. native SpeechLMs — no citation, may overstate | Check §5 / intro comparison |
| 2025.acl-long.912 | Claim 3: "training from scratch fails to converge" — strong negative finding | Check §5.2, Table 3 |
| 2025.acl-short.81 | Field Significance: "first large-scale Vietnamese corpus with speaker identity" — "first" claims need verification | Check §1 / related work |
| 2025.acl-short.81 | Claim 2: "architectural failure modes" on XTTS-v2 — strong characterization of empirical failure | Check §4 |
| 2508.02013 | Claim 1: "more strongly determined by LLM text reasoning" — strong causal interpretation of correlation data | Check §5.2 |
| 2508.02013 | Claim 4: "capability gap, not merely a performance gap" — editorial framing unlikely to be in the paper verbatim | Check §5.2, Table 2 |
| 2025.americasnlp-1.1 | Field Significance: "first speech corpus and TTS system for Shipibo-Konibo" — "first" claim | Check §1 / related work |
| 2025.americasnlp-1.1 | Claim 3: "pronunciation drift causes natural speech to score lower than synthetic on intelligibility" — counterintuitive, easy to overstate | Check §5.4 |
| 2508.02038 | Claim 5: "male speakers underperform female on emotion recognition across most categories" — specific bias finding | Check §4.4, Figure 6 |
| 2508.02038 | field_significance includes architectural-novelty — borderline; orthogonality constraint may be engineering-integration only | Judgment call |
| 2508.02849 | Claim 1: "HuBERT/WavLM distillation does not achieve true semantic disentanglement" — strong critique of dominant approach | Check §II.A, §V.B |
| 2508.02849 | Claim 5: "staged training is necessary for stable convergence" — "necessary" overstates an ablation result | Check §III.E, §V.C, Table II |
| 2025.coling-main.518 | Claim 3: "flow matching comparable quality to diffusion at lower cost" — requires a direct diffusion baseline in paper | Check §3.4, Table 3 |
| 2508.03543 | Metric correction: EI-MOS 4.00 changed from E2-TTS to F5-TTS variant | Check §4.2, Table 1 |
| 2508.03543 | Claim 4: layer counts 22/8/56 for F5-TTS/E2-TTS/CosyVoice2 — specific numbers, easy to hallucinate | Check §4.5 |
| 2025.emnlp-demos.70 | Field Significance: "first fully open-source SCA with empathy support" — "first" claim | Check §1 / related work |
| 2025.emnlp-demos.70 | Metrics: VoiceBench commoneval 3.65 and wildvoice 3.66 recovered from Table 2 — verify values | Check Table 2 |
| 2025.emnlp-main.1730 | Claim 3: "4.20M trainable LoRA parameters" — very specific number | Check §6.3 |
| 2025.emnlp-main.1730 | Claim 4: Vicuna vs LLaMA vs Qwen comparison — verify these are the actual models in Table 3 | Check §6.3.1, Table 3 |
| 2508.04996 | Claim 4: "order of magnitude" reduction (32→4 steps = 8x, not 10x) — technically overstated | Check §II.D, Table I |
| 2025.emnlp-main.180 | Claim 3: "necessary... omitting any stage degrades quality" — strong word for an ablation | Check §4.3, Table 2 |
| 2025.emnlp-main.180 | Wiki Connections: "first large-scale open-source dataset" — "first" claim, pre-existing | Check §1 / related work |
| 2025.emnlp-main.989 | Field Significance: "reduces pronunciation errors by almost half" — no citation | Check §5.3 |
| 2025.emnlp-main.989 | Claim 3: "ASR and TTS pretraining do not improve spoken QA" — strong negative, ablation result | Check §5.2, Table 3 |
| 2025.emnlp-main.989 | Claim 4: "two orders of magnitude more data" + "~6,000 hours synthesized speech" — both specific | Check §5.1, Table 1 |
| 2508.05207 | Metrics: MUSHRA renamed to ViSQOL (subjective→objective) — major category change, must verify | Check Table 1 |
| 2508.05207 | Claim 5: "80 ms latency on desktop CPU at 48 kHz stereo" — specific hardware claim | Check §1, §2 |
| 2508.05385 | Metrics: CLAP-Score 0.187 and IMOS 3.48 recovered — verify values | Check Table 2 |
| 2508.05385 | Claim 3: "NV detection generalises across structurally different languages without retraining" — strong cross-lingual claim | Check §2.2, §3 |
| 2025.findings-acl.1051 | Claim 2: "end-to-end speech LLMs consistently show degraded language understanding" — "consistently" is strong | Check §6.4, Table 1 |
| 2025.findings-emnlp.424 | Claim 1: "necessary for classifying conversational events accurately" — "necessary" is strong for a dataset ablation | Check §4.1, Table 2 |
| 2025.findings-emnlp.424 | Claim 5: "synthetic TTS quality comparable to or exceeding Fisher and Switchboard" — strong comparison to classic corpora | Check §4.2, Table 3 |
| 2508.06262 | Claim 1: WER 3.07%→14.37% and SPK-SIM 0.570→0.463 without verification — specific paired values | Check §V, Table III |
| 2508.06262 | Claim 2: "1.48x" acceleration; Claim 4: "approximately 95%" quality retention — specific numbers | Check §IV.B Table I; §IV.C Table II |
| 2508.14049 | Metric correction: French WER changed 6 → 18 | Check Table 2 |
| 2510.02848 | Metric correction: WER 3s prompt changed 0.05 → 0.04 | Check Table 1 |
| 2510.05758 | Claim 4: "Emphasis placement on adverbs and adjectives produces stronger perceived emotional intensity than emphasis on verbs, nouns, or other categories" — granular POS-category ranking | Check §3.2, Figure 2 |
| 2510.07979 | Claim 4: training instability in direct MeanFlow application manifests as degraded subjective quality even when objective metrics appear competitive — specific failure mode | Check §4.3, Table 2 |
| 2510.07979 | Claim 5: larger teacher model during distillation improves smaller student — specific ablation | Check §4.2.3, Table 1 |
| 2510.12210 | Metrics SPK-SIM 0.66 / UTMOS 4.05 for proposed (medium, 0.3B) on SeedTTS test-en | Check Table 1 |
| 2510.12210 | Claim 3: "tail-first confidence bias" — paper-coined terminology, verify it is in the paper | Check §3.4 |
| 2511.12347 | Claim 1: "near-random and functional output" — strong language for ablation failure, may overstate | Check §3.4, §D.1, Table 9 |
| 2511.12347 | Claim 3: "pre-training reducing WER by 5–10x for low-resource languages" — specific quantitative range | Check §4.3, Table 2 |
| 2511.12347 | Claim 5: "larger systems trained on 30K–130K hours" — specific data scale comparison | Check §4.2, Table 1 |
| 2512.04720 | Metric correction: WER 1.36 → 1.48 for M3-TTS-Fbank on Seed-TTS test-en | Check Table 1 |
| 2512.04720 | Claim 2: "roughly 3x" training acceleration with VAE latents | Check §2.2, §4.3, Table 2 |
| 2512.13251 | Claim 3: soft vs. hard orthogonality three-way ablation comparison | Check §3.1.1, Appendix B, Table 6 |
| 2512.14291 | Metrics: SPK-SIM 76.4, 67.2, 68.1 and WER 1.91 — multiple new values added | Check Table 3 |
| 2512.14291 | Claim 1: "reduce phoneme error rate by more than half" with hybrid phoneme-text input | Check §2.6, §3.4, Table 7 |
| 2512.14291 | Claim 2: "without reward hacking" — design assurance claim, not empirically measured | Check §2.4, §3.3, Table 4 |
| 2512.14291 | Claim 3: laughter trade-off causation ("because laughter segments resist ASR transcription") | Check §3.3, Table 6 |
| 2512.14291 | Claim 5: "15% of backbone parameters" for LoRA — specific, weak citation (§2.5 only) | Check §2.5 |
| 2601.03888 | Claim 1: "no measurable degradation" from halving codec frame rate 50→25 Hz | Check §3.2, Table 4 |
| 2601.03888 | Claim 2: Japanese-specific finding within multi-language comparison | Check §4.3, Table 1 |
| 2603.29339 | Claim 1: "primarily because high-frequency acoustic detail... is preserved end-to-end" — causal interpretation | Check §5.3.1, Table 3 |
| 2603.29339 | Claim 3: "increasing VAE fidelity degrades downstream quality" — counterintuitive causal finding | Check §5.3.2, Figure 3 |
| 2604.00688 | Claim 4: "CER below 5% for languages with fewer than 10 hours" — two specific thresholds | Check §4.2, Table 4, Figure 4 |
| 2604.00688 | Claim 5: UTMOS 4.23→4.32 and SIM-o 0.697→0.668 from prompt denoising — four specific values | Check §4.3, Table 7 |
| 2604.01760 | Claim 4: "cross-lingual generalization stronger for typologically adjacent languages" — no table citation | Check §5.2 |
| 2604.01760 | Claim 5: "near-complete synthesis failure" from removing duration control at inference | Check §4.2, §5.3, Table 3 |
| 2604.12438 | Claim 3: "phonetically transparent languages tolerate 12.5 Hz compression better than deep-orthography languages" — linguistic typology framing | Check §4.3, Table 8 |
| 2601.15621 | Claim 2: "reduces sequence length and error accumulation" — "error accumulation" is causal, no table | Check §4.2.1 |
| 2601.15621 | Claim 5: "open-source systems match or exceed commercial baselines" on instruction-following benchmarks | Check §4.2.4, Table 8 |
| 2603.08823 | Claim 1: "eliminates the distribution shift" — likely overstates; probably "reduces" or "mitigates" | Check §3, §4.3 |
| 2603.08823 | Claim 5: "can match or exceed closed-source systems" — broad generalization | Check §6.1, Tables 1–2 |
| 2603.18090 | Claim 3: "Token-level duration control can emerge from paired pretraining format alone, without a dedicated fine-tuning stage" — "emerge" is strong | Check §6.4, Table 5 |
| 2603.18090 | Claim 4: "Cumulative speaker drift... is the dominant failure mode in ultra-long autoregressive speech generation" — class-level characterization | Check §6.5, Table 6, Figure 6 |
| 2603.26364 | field_significance level: high — borderline for a fine-tuning paper; formal theorem may justify it | Judgment call |
| 2603.26364 | Claim 3: "formal bound on the suboptimality of AR predictors" — mathematical claim (ε-forward dependence theorem) | Check §3.3 |

---

## Helper Notes

### Bare wikilinks (recurring agent blind spot)
The review agent adds paper IDs to `related_papers` and writes about them in Wiki Connections prose, but uses bare `[[id]]` or `[[id]] (Name)` format instead of `[[id|Name]]`. After every diff, grep for bare wikilinks in the modified file:
```bash
grep "\[\[[0-9]\|interspeech\|acl\|emnlp\|naacl" /path/to/content/papers/{ID}.md | grep -v "|"
```
**Rule:** use `[[id|Name]]` when a clean display name exists (model name, system name). Bare `[[id]]` is acceptable when no clean name applies. Never write `[[id]] (Name)`.

The agent spec was patched on 2026-06-20 to document this rule. Watch for recurrence.

### Interspeech figure sanity
Docling typically assigns `figure-1.png` to the ISCA logo on Interspeech papers. If the review agent embeds a figure from an Interspeech paper, check file sizes in `raw/parsed/{ID}/assets/` — the logo is the smallest file. Flag for manual visual verify before any site bump.

```bash
ls -lh raw/parsed/{ID}/assets/*.png
```

The smallest file is usually the logo. The agent should embed the largest figure whose caption matches the architectural selection criteria.

### F5-TTS paper ID
F5-TTS's canonical wiki ID is `2025.acl-long.313` (ACL 2025), **not** `2410.06885` (arXiv). Pass this note to the review agent prompt when the paper is likely to cite F5-TTS. Always verify `related_papers` IDs against the wiki index.

### `--wiki-dir` flag
Added to `scripts/health_check.py` on 2026-06-20. Lets you validate changes against the standalone content repo without committing to the submodule or pushing to GitHub.

```bash
WIKI=/Users/sribeiro/Documents/Coding/speech-generation-wiki/speech-generation-wiki-content
.venv/bin/python scripts/health_check.py --module ingest --wiki-dir "$WIKI"
```

---

## Remaining candidates — 16 papers (updated 2026-06-25)

To resume: proceed in batches of 4.

### Interspeech 2025 — 0 papers *(complete)*

### NLP venues (ACL/EMNLP/NAACL/COLING) — 0 papers *(complete)*

### arXiv — 0 papers *(all 16 complete: batches 1–4)*
