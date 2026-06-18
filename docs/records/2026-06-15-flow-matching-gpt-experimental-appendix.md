---
title: "Flow Matching Evidence Appendix"
concept: flow-matching
date: 2026-06-15
status: experimental
companion: flow-matching-gpt-experimental-06-15.md
source: "Drafted from wiki/concepts/_evidence/flow-matching.yaml, selected paper pages, and the existing flow-matching concept page"
---

# Flow Matching Evidence Appendix

This appendix is the companion evidence layer for `flow-matching-gpt-experimental-06-15.md`. The concept page should remain short and interpretive; this appendix keeps the supporting paper inventory, claim evidence, caveats, and method-family details.

## Evidence Model

Each paper can contribute to the concept in one or more roles:

- `core evidence` — directly advances the flow-matching method for speech generation.
- `architecture variant` — introduces a new placement or representation for FM.
- `acceleration evidence` — reduces NFE, RTF, or latency.
- `control evidence` — improves speaker, emotion, prosody, language, or dialogue control.
- `historical context` — explains predecessor flow/normalizing-flow work but does not directly validate modern FM-TTS.
- `evaluation caution` — exposes metric, benchmark, or comparison limitations relevant to FM claims.

## Canonical Claim Clusters

| Claim | Status | Supporting papers | Caveats |
|------|--------|-------------------|---------|
| Flow matching can produce high-quality TTS with fewer inference steps than diffusion-style iterative denoising. | strongly supported | [[2025.acl-long.313]], [[2025.acl-long.1043]], [[interspeech-2025-0554]], [[interspeech-2025-0455]], [[interspeech-2025-2449]] | Evidence strongest for mel-spectrogram and latent-mel systems; waveform-latent and discrete-token targets need more validation. |
| Hybrid AR+FM pipelines are a stable design pattern for modern speech systems. | strongly supported | [[2407.05407]], [[2412.10117]], [[2506.21619]], [[2025.acl-long.912]], [[2502.17239]], [[2508.14049]] | Hybrid systems add pipeline complexity and inherit tokenizer/AR-stage limitations. |
| Inference scheduling and trajectory compression are central to practical FM-TTS. | strongly supported | [[2025.acl-long.313]], [[interspeech-2025-2449]], [[interspeech-2025-0455]], [[interspeech-2025-0554]] | Current schedules are often empirical; subjective evaluation is uneven. |
| Learned priors can shorten FM trajectories by starting closer to the target distribution. | emerging | [[2025.acl-long.1043]], [[2510.02848]] | Needs broader validation; current evidence shows trade-offs among WER, naturalness, and speaker similarity. |
| FM can move beyond mel-spectrogram targets into waveform latents, discrete tokens, and vocoder-level generation. | emerging | [[2603.29339]], [[2509.09631]], [[2025.naacl-long.110]], [[2508.16790]] | These are representation-specific findings, not yet one unified family. |
| Speech-specific CFG behavior differs from image-generation CFG behavior. | contested / emerging negative evidence | [[2509.19668]], [[2025.acl-long.313]], [[2412.10117]] | Evidence comes from two main systems; root causes remain unisolated. |
| FM models can support expressive or emotional control through latent/activation structure. | emerging | [[2508.03543]], [[interspeech-2025-0203]], [[2508.07302]], [[2508.16332]] | Evaluation often depends on automatic emotion proxies or narrow subjective tests. |
| PEFT is safer than full fine-tuning for cross-lingual FM-TTS adaptation. | emerging | [[interspeech-2025-1344]] | Single target language and limited data; not yet a general law. |

## Method-Family Evidence

### Pure Non-Autoregressive FM TTS

| Paper | Role | Evidence | Limitation |
|------|------|----------|------------|
| [[2406.18009]] E2 TTS | Establishes alignment-free character-plus-filler FM-TTS. | Reports strong zero-shot WER/SIM on LibriSpeech-PC and argues explicit phoneme alignment can cap naturalness. | Requires target duration estimation; evaluation is English-focused. |
| [[2025.acl-long.313]] F5-TTS | Makes alignment-free FM-TTS robust and open-weight. | Adds ConvNeXt text refinement and Sway Sampling; reports strong WER, SPK-SIM, UTMOS across LibriSpeech-PC and Seed-TTS English/Chinese. | Speaker similarity remains below stronger proprietary systems; mel representation still imposes sequence-length cost. |
| [[2512.04720]] M3-TTS | Replaces pseudo-alignment with multimodal DiT attention. | Uses MMDiT joint text-speech attention and mel-latent training to improve alignment and training speed. | Needs validation beyond its reported benchmark suite. |

### Hybrid AR/LLM + FM

| Paper | Role | Evidence | Limitation |
|------|------|----------|------------|
| [[2407.05407]] CosyVoice | Establishes supervised semantic-token + FM acoustic decoder pattern. | Uses LLM-predicted semantic tokens followed by OT-CFM acoustic synthesis. | Depends on tokenizer and two-stage architecture. |
| [[2412.10117]] CosyVoice 2 | Extends hybrid FM to streaming/non-streaming deployment. | Chunk-aware causal FM supports multiple masking modes in one model. | More complex deployment path than pure NAR FM. |
| [[2506.21619]] IndexTTS2 | Adds emotion/duration control around AR+FM. | Uses an S2M FM module with AR duration and emotion control. | Hybrid complexity and disentanglement assumptions remain. |
| [[2025.acl-long.912]] LLaMA-Omni 2 | Places FM inside a streaming spoken chatbot. | Uses CosyVoice 2-style chunk-aware FM as the acoustic decoder. | Speech-dialogue quality depends on the upstream LLM and latency budget. |
| [[2502.17239]] Baichuan-Audio | Uses FM as post-VQ audio refinement. | FM decoder recovers UTMOS lost in quantization. | Adds inference latency and is evaluated primarily on Chinese. |

### Few-Step and Low-Latency Acceleration

| Paper | Mechanism | Evidence | Limitation |
|------|-----------|----------|------------|
| [[2025.acl-long.1043]] OZSpeech | Learned prior replaces Gaussian initialization. | One-step inference with WER 0.05 on LibriSpeech test-clean using 500h training. | Lower UTMOS and speaker similarity than naturalness-oriented systems. |
| [[interspeech-2025-0554]] RapFlow-TTS | Consistency flow matching. | 2-NFE synthesis with MOS 4.01 on LJSpeech and FastSpeech2-like speed. | Not zero-shot; small model/dataset setting. |
| [[interspeech-2025-0455]] APTTS | Latent FM + adversarial post-training. | 4-step zero-shot synthesis, WER 1.73 on LibriSpeech test-clean full subset. | Speaker similarity lags large-scale systems; hybrid CFG adds complexity. |
| [[interspeech-2025-2449]] EPSS | Training-free non-uniform step pruning. | Reduces F5-TTS from 32 to 7 NFE with WER 1.74 vs. 1.70 on Seed-TTS test-en. | No subjective MOS; validated only on mel FM systems. |
| [[2510.07979]] IntMeanFlow | Average-velocity distillation. | Targets 1-3 NFE speech generation. | Needs comparison under consistent subjective protocols. |
| [[2508.04996]] REF-VC | Shortcut models for voice conversion. | Reduces FM inference from 32 to 4 steps with small quality cost. | VC setting; transfer to TTS unproven. |

### Representation-Shifted FM

| Paper | Target representation | Evidence | Limitation |
|------|----------------------|----------|------------|
| [[2603.29339]] LongCat-AudioDiT | Continuous waveform VAE latent. | Wav-VAE latent improves Seed speaker similarity vs. mel VAE; identifies prompt-region training-inference mismatch. | Proprietary data; limited human listening evidence. |
| [[2509.09631]] DiFlow-TTS | Factorized discrete FACodec token distributions. | Direct discrete FM over prosody/acoustic tokens reaches strong MOS and F0 metrics with compact model. | Automatic speaker similarity is weak; English-only evaluation. |
| [[2025.naacl-long.110]] WaveFM | Waveform/vocoder generation. | Applies FM to mel-conditioned vocoding with consistency distillation. | Vocoder-stage evidence does not directly prove text-to-speech FM claims. |
| [[2510.02848]] Flamed-TTS | Semantically enriched codec prior. | Extends learned-prior FM with attention-free denoising. | Needs broader validation on long utterances and diverse speakers. |
| [[2508.16790]] TaDiCodec | Codec decoder objective. | Uses rectified flow as codec decoder training objective. | Codec-specific result; downstream TTS generalization uncertain. |

### Voice Conversion and Expressive Control

| Paper | Role | Evidence | Limitation |
|------|------|----------|------------|
| [[interspeech-2025-0203]] ClapFM-EVC | Emotional voice conversion with CFM. | CFM decoder conditioned on PPGs and CLAP emotion embeddings supports reference and natural-language emotion control. | Any-to-one evaluation; unseen target speaker generalization untested. |
| [[2508.04996]] REF-VC | Zero-shot VC with DiT-based FM. | Shortcut Models enable 4-step inference; random feature erasure improves noisy-condition robustness. | Small unseen-speaker set; not a TTS result. |
| [[interspeech-2025-1779]] ReFlow-VC | Rectified flow for zero-shot VC. | Uses gated cross-attention fusion of speaker/content/pitch features. | Needs broader evaluation across languages and speakers. |
| [[2508.03543]] EmoSteer-TTS | Training-free emotion control. | Activation steering vectors in FM DiT layers enable emotion conversion/interpolation/erasure. | Early evidence; depends on emotion representations and automatic/subjective evaluation quality. |
| [[2508.07302]] XEmoRAG | Cross-lingual emotion transfer. | Uses FM alignment to bridge codec tokens to mel for Thai emotion transfer. | Thai-only; emotion data limited. |
| [[2508.16332]] Vevo2 | Speech/singing prosody control. | FM acoustic decoder conditioned on chromagram prosody tokens. | Singing/speech unification is related but not central to baseline TTS FM claims. |

### Adaptation and Multilingual Evidence

| Paper | Role | Evidence | Limitation |
|------|------|----------|------------|
| [[interspeech-2025-1344]] PEFT-TTS | Cross-lingual continual adaptation. | LoRA/adapters at 1.72% parameters preserve zero-shot capability better than full fine-tuning for Korean adaptation. | Korean-only, 12h single-speaker setting; multi-speaker WER remains high. |
| [[2508.14049]] MahaTTS | Multilingual Indic TTS with FM acoustic model. | Uses Matcha-TTS-inspired conditional FM for semantic-to-mel generation across Indic languages. | FM stage not independently ablated from the AR text-to-semantic stage. |
| [[2508.08715]] MultiGen | Low-resource child-friendly TTS fine-tuning. | Fine-tunes CosyVoice-300M FM pipeline for child-friendly Southeast Asian languages. | Inherits CosyVoice FM rather than contributing a new FM method. |
| [[interspeech-2025-0762]] Swedish accentedness control | Per-phoneme accentedness conditioning. | Adds accentedness control to Matcha-TTS-style FM. | Narrow perceptual domain. |

## Historical Context Papers

| Paper | Why it matters | Why it is not direct current evidence |
|------|----------------|----------------------------------------|
| [[2106.15561]] A Survey on Neural Speech Synthesis | Summarizes pre-2022 flow, diffusion, GAN, VAE, AR, and NAR TTS families; useful for understanding why parallel generation mattered. | Predates modern flow matching, rectified flow, codec-LM hybrids, and F5/E2/OZSpeech-style systems. |
| [[2210.02747]] Flow Matching for Generative Modeling | Establishes the generic flow-matching objective and OT conditional path used by later TTS systems. | Not a speech paper; supports the mathematical foundation, not speech-specific claims. |
| [[2207.12598]] Classifier-Free Diffusion Guidance | Provides the conditioning-dropout/guidance mechanism later adapted in FM-TTS. | Image/diffusion setting; speech-specific CFG behavior remains contested by [[2509.19668]]. |

## Evidence Strength Notes

### Strong Evidence

- F5-TTS [[2025.acl-long.313]]: large-scale, open-weight, multiple benchmarks, ablations for ConvNeXt text refinement and Sway Sampling.
- RapFlow-TTS [[interspeech-2025-0554]]: clear ablation of consistency FM components and subjective MOS, though not zero-shot.
- APTTS [[interspeech-2025-0455]]: few-step zero-shot FM with subjective and objective evaluation, plus transfer to Matcha-TTS.
- LongCat-AudioDiT [[2603.29339]]: strong representation ablations, especially Wav-VAE vs. Mel-VAE and mismatch correction, though reproducibility is limited by proprietary scale.

### Medium Evidence

- OZSpeech [[2025.acl-long.1043]]: strong speed/intelligibility result, but the naturalness and speaker-similarity trade-off limits broad conclusions.
- EPSS [[interspeech-2025-2449]]: clean practical speedup, but automatic-only evaluation limits confidence.
- DiFlow-TTS [[2509.09631]]: important discrete-FM proof point, but speaker similarity and English-only scope limit generality.
- PEFT-TTS [[interspeech-2025-1344]]: useful adaptation result, but narrow language/data setting.

### Weak or Narrow Evidence

- Low-resource or domain-specific fine-tunes that inherit a CosyVoice/F5/Matcha FM component without isolating the FM mechanism.
- Emotion/VC papers evaluated on narrow speaker-language settings.
- Internal-data-only results without public benchmarks or ablations.

## Current Tensions by Evidence

### Speed vs. Quality

| Evidence | What it supports | What remains unresolved |
|---------|------------------|--------------------------|
| [[2025.acl-long.1043]] | One-step FM can dramatically improve speed and WER. | UTMOS and speaker similarity trail stronger systems. |
| [[interspeech-2025-0554]] | 2-NFE FM can reach strong MOS in non-zero-shot settings. | Does it scale to open-domain zero-shot TTS? |
| [[interspeech-2025-0455]] | 4-step latent FM can compete with 32-step baselines. | SIM-o remains lower than large-scale systems. |
| [[interspeech-2025-2449]] | 7-step training-free pruning is practical. | Does automatic-metric preservation imply perceptual preservation? |

### Representation Choice

| Representation | Evidence | Current reading |
|---------------|----------|-----------------|
| Mel-spectrogram | [[2406.18009]], [[2025.acl-long.313]], [[interspeech-2025-2449]] | Mature and robust, but may inherit vocoder and sequence-length limits. |
| Learned prior / factorized codec | [[2025.acl-long.1043]], [[2510.02848]] | Promising for trajectory shortening, with naturalness/SIM trade-offs still unresolved. |
| Waveform VAE latent | [[2603.29339]] | Strong frontier result; needs independent replication and human listening evidence. |
| Discrete token distribution | [[2509.09631]] | Interesting compact baseline; speaker conditioning is the weak point. |
| Vocoder-level FM | [[2025.naacl-long.110]] | Useful for waveform synthesis, but separate from full TTS system evidence. |

### Pure FM vs. Hybrid FM

| System family | Evidence | Current reading |
|--------------|----------|-----------------|
| Pure NAR FM | [[2406.18009]], [[2025.acl-long.313]], [[2603.29339]] | Best for parallelism and conceptual simplicity. |
| AR/LLM + FM | [[2407.05407]], [[2412.10117]], [[2506.21619]], [[2025.acl-long.912]] | Best current compromise when semantic planning, streaming, or dialogue integration matters. |
| AR + within-chunk FM | [[2507.22746]] | Promising bridge for streaming, but needs standardized benchmarks. |

## Papers to Reassess Later

These papers should be revisited during future integration passes because their long-term importance depends on follow-up adoption or contradiction.

| Paper | Why revisit |
|------|-------------|
| [[2603.29339]] | If waveform-latent FM becomes common, this moves from frontier probe to influential/foundational. |
| [[2509.09631]] | If discrete FM is accelerated and improves speaker similarity, it could become a major alternative to continuous FM. |
| [[2025.acl-long.1043]] | If learned-prior FM scales without naturalness/SIM loss, it becomes a core acceleration family. |
| [[interspeech-2025-2449]] | If EPSS-style schedule pruning becomes a standard inference option, its role increases. |
| [[interspeech-2025-1344]] | If PEFT-first adaptation generalizes to more languages, it becomes a practical guideline for multilingual FM-TTS. |
| [[2509.19668]] | If more systems replicate the CFG language/model-dependence finding, it should move from contested/emerging to strongly supported negative evidence. |

## Suggested Generated Tables

For a production appendix, these sections should be generated from structured data rather than maintained by hand:

- `All Related Papers`: one row per paper with contribution type, relevance, role, key result, limitation.
- `Claim Support Matrix`: canonical claim by paper, with support/contradict/refine/complicate role.
- `Metric Snapshot`: WER, CER, SPK-SIM, UTMOS, MOS, RTF, NFE, dataset, and comparability caveat.
- `Reassessment Queue`: papers whose current role may change due to adoption, contradiction, or lack of follow-up.

## Data Hygiene Notes

The current `wiki/concepts/_evidence/flow-matching.yaml` appears to contain some paper entries after `trend_notes`, rather than under the top-level `papers:` list. Before this appendix is generated automatically, the digest should be validated with a schema and repaired so all paper evidence is structurally accessible.
