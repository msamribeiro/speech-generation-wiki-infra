---
slug: flow-matching
title: "Flow Matching"
status: dominant
last_reviewed: 2026-06-15
source: "Experimental GPT rewrite based on wiki/concepts/_evidence/flow-matching.yaml and selected paper pages"
---

# Flow Matching

> [!abstract]
> Flow matching is now the leading non-autoregressive paradigm for modern TTS: it offers parallel inference, a simpler transport objective than diffusion, and strong compatibility with zero-shot prompting and LLM-conditioned acoustic decoding. The evidence base is strongest for mel-spectrogram TTS and hybrid AR+FM pipelines; newer work is testing whether the same advantages hold in waveform latents, discrete token spaces, voice conversion, and dialogue generation.

## Current Assessment

Flow matching should be treated as **dominant but still actively diversifying**. The core claim that it can produce high-quality speech with fewer inference steps than diffusion is well supported across F5-TTS [[2025.acl-long.313]], OZSpeech [[2025.acl-long.1043]], RapFlow-TTS [[interspeech-2025-0554]], and APTTS [[interspeech-2025-0455]]. The field has moved beyond asking whether flow matching works for TTS; the live questions are now about where to place it in a system, how far inference can be compressed, and which representation it should operate over.

The strongest current pattern is not "pure flow matching replaces everything." It is **flow matching as the acoustic synthesis workhorse**: pure non-autoregressive systems use it directly ([[2406.18009]], [[2025.acl-long.313]]), while hybrid systems use autoregressive or LLM stages for semantic planning and flow matching for acoustic realization ([[2412.10117]], [[2506.21619]], [[2025.acl-long.912]], [[2502.17239]]).

## Major Claims

### Strongly Supported

- **Flow matching can reach useful TTS quality with fewer inference steps than diffusion-style denoising.**  
  Evidence: [[2025.acl-long.313]] establishes large-scale zero-shot FM TTS; [[2025.acl-long.1043]] achieves one-step inference by replacing Gaussian noise with a learned prior; [[interspeech-2025-0554]] reaches 2-NFE synthesis through consistency flow matching; [[interspeech-2025-0455]] reaches 4-step zero-shot synthesis through adversarial post-training.  
  Caveat: the evidence is strongest for mel-spectrogram or latent-mel systems. Waveform-latent and discrete-token flow matching are promising but thinner.

- **Hybrid AR+FM systems are a stable design pattern.**  
  Evidence: CosyVoice-style systems [[2407.05407]], [[2412.10117]], IndexTTS2 [[2506.21619]], LLaMA-Omni 2 [[2025.acl-long.912]], Baichuan-Audio [[2502.17239]], and other hybrid architectures use an autoregressive or LLM stage for semantic/prosodic structure and a flow-matching decoder for acoustic synthesis or refinement.  
  Caveat: hybrid systems inherit complexity from both sides: AR latency, tokenizer dependence, and FM/vocoder tuning.

- **Inference-time scheduling matters for flow-matching TTS.**  
  Evidence: F5-TTS [[2025.acl-long.313]] introduces Sway Sampling; EPSS [[interspeech-2025-2449]] shows that non-uniform step pruning can reduce F5-TTS from 32 to 7 NFE with little automatic-metric degradation; APTTS [[interspeech-2025-0455]] also uses early-biased fixed ODE steps.  
  Caveat: current schedules are often hand-designed or empirically inspected rather than learned or globally optimized.

- **Classifier-free guidance is not a solved transfer from image generation to speech.**  
  Evidence: F5-TTS [[2025.acl-long.313]] and CosyVoice-style systems [[2412.10117]] depend on CFG-like conditioning, but [[2509.19668]] reports that image-domain CFG tricks do not transfer cleanly and that behavior differs across languages.  
  Caveat: this should be treated as contested rather than settled; speech-specific conditioning structure, tokenization, text encoders, and language effects are confounded.

### Emerging

- **Learned priors can replace Gaussian initialization and substantially shorten FM trajectories.**  
  Evidence: OZSpeech [[2025.acl-long.1043]] shows one-step inference with a prior codes generator; Flamed-TTS [[2510.02848]] extends the learned-prior idea with semantically enriched codec priors.  
  Caveat: OZSpeech trades off naturalness and speaker similarity against intelligibility and speed; learned-prior methods need stronger validation across datasets, languages, and prompt conditions.

- **Flow matching may generalize beyond mel-spectrogram generation.**  
  Evidence: LongCat-AudioDiT [[2603.29339]] moves FM into waveform VAE latent space; DiFlow-TTS [[2509.09631]] applies discrete flow matching to factorized codec tokens; WaveFM [[2025.naacl-long.110]] applies flow matching to the vocoder stage; ReFlow-VC [[interspeech-2025-1779]] applies rectified flow to voice conversion.  
  Caveat: these are not yet a single consolidated family. Each representation changes the bottleneck: vocoder error, codec quantization, VAE compression, or token convergence.

- **Flow-matching models contain steerable paralinguistic structure.**  
  Evidence: EmoSteer-TTS [[2508.03543]] reports training-free emotion control through activation steering in pre-trained FM DiT layers. ClapFM-EVC [[interspeech-2025-0203]] shows dual reference/text emotion control in a CFM voice-conversion decoder.  
  Caveat: emotional control evidence is early, and evaluation often depends on subjective emotion judgments or automatic emotion proxies.

- **Parameter-efficient adaptation is likely the safer default for cross-lingual FM TTS adaptation.**  
  Evidence: PEFT-TTS [[interspeech-2025-1344]] reports that adapter-based tuning preserves zero-shot capability while full fine-tuning damages it.  
  Caveat: current evidence is narrow: one target language, limited data, and smaller-scale adaptation compared with frontier multilingual systems.

## Method Families

**Pure non-autoregressive FM TTS.**  
E2 TTS [[2406.18009]] and F5-TTS [[2025.acl-long.313]] are the reference family: text and reference speech are jointly modeled through speech infilling, then a flow-matching model predicts the target acoustic trajectory. This family is attractive for parallel inference and architectural simplicity, but it still depends heavily on alignment robustness, text representation quality, and ODE scheduling. E2 TTS establishes the character-plus-filler alignment-free formulation; F5-TTS adds ConvNeXt text refinement and Sway Sampling to improve robustness.

**LLM-conditioned or AR-conditioned FM.**  
CosyVoice-style systems [[2407.05407]], [[2412.10117]], IndexTTS2 [[2506.21619]], and LLaMA-Omni 2 [[2025.acl-long.912]] separate semantic planning from acoustic realization. The AR/LLM component improves language modeling and text adherence; flow matching then handles acoustic synthesis. Baichuan-Audio [[2502.17239]] also uses flow matching as a post-VQ refinement stage, reinforcing FM's role as an acoustic repair/synthesis component in larger speech systems.

**Few-step acceleration.**  
The 2025 acceleration cluster is now large enough to be a subfield: consistency flow matching in RapFlow-TTS [[interspeech-2025-0554]], adversarial post-training in APTTS [[interspeech-2025-0455]], non-uniform schedule pruning in EPSS [[interspeech-2025-2449]], learned priors in OZSpeech [[2025.acl-long.1043]], shortcut models for VC in REF-VC [[2508.04996]], and distillation-style methods such as IntMeanFlow [[2510.07979]] all target the same bottleneck. The common signal is that early FM trajectory regions are disproportionately important, while late regions often permit pruning or compression.

**Representation-shifted FM.**  
Newer systems move the flow target away from standard mel-spectrograms: waveform VAE latents in LongCat-AudioDiT [[2603.29339]], discrete factorized codec tokens in DiFlow-TTS [[2509.09631]], semantically enriched codec priors in Flamed-TTS [[2510.02848]], and vocoder-level waveform generation in WaveFM [[2025.naacl-long.110]]. This is where the next meaningful paradigm shift may happen, because the representation determines whether FM inherits vocoder errors, codec errors, or VAE compression errors.

**Flow matching for VC and expressive control.**  
Voice conversion and emotion conversion papers show that FM is not limited to TTS: ClapFM-EVC [[interspeech-2025-0203]] uses CFM for emotional VC, REF-VC [[2508.04996]] applies DiT-based FM with shortcut models to zero-shot VC, ReFlow-VC [[interspeech-2025-1779]] applies rectified flow to VC, and EmoSteer-TTS [[2508.03543]] uses activation steering for emotion control in FM TTS. The evidence is promising but thinner than for TTS, and many systems are evaluated on narrower speaker/language settings.

## How to Interpret Older and Newer Evidence

Early flow-based TTS evidence from surveys and normalizing-flow systems should be treated as **historical context**, not direct support for the current FM paradigm. The 2021 neural speech synthesis survey [[2106.15561]] covers normalizing-flow TTS and diffusion-era predecessors, but explicitly predates the modern codec-LM, rectified-flow, and OT-CFM systems that dominate the current concept page. Those older works establish that parallel invertible generation was a meaningful alternative to autoregression; they do not by themselves validate the current F5-TTS/OZSpeech/RapFlow-style formulation.

F5-TTS [[2025.acl-long.313]] remains **highly influential** even if later systems beat it on some metrics. Its lasting contribution is not just a score: it made alignment-free, open-weight, large-scale flow-matching TTS a credible baseline and introduced practical inference scheduling. E2 TTS [[2406.18009]] is the more direct predecessor for the character-plus-filler alignment-free formulation, while F5-TTS made that lineage more robust through ConvNeXt text refinement.

OZSpeech [[2025.acl-long.1043]], RapFlow-TTS [[interspeech-2025-0554]], APTTS [[interspeech-2025-0455]], and EPSS [[interspeech-2025-2449]] should be treated as **active evidence for acceleration**, not independent paradigms yet. They point toward a shared conclusion: FM trajectories can be compressed aggressively. The unresolved question is which compression mechanism survives scale, multilingual use, and subjective evaluation.

LongCat-AudioDiT [[2603.29339]] and DiFlow-TTS [[2509.09631]] should be treated as **frontier probes**. They may become important if later papers validate their representation choices, but at present they primarily show that the mel-spectrogram assumption is no longer fixed.

## Current Tensions

- **Speed vs. naturalness.** OZSpeech [[2025.acl-long.1043]] reaches one-step inference and extremely low WER, but with lower UTMOS and speaker similarity than stronger naturalness-oriented systems. APTTS [[interspeech-2025-0455]] and RapFlow-TTS [[interspeech-2025-0554]] include subjective MOS evidence, while EPSS [[interspeech-2025-2449]] relies on automatic metrics; few-step methods still need more consistent subjective evaluation to determine whether automatic metrics hide perceptual degradation.

- **Pure FM vs. hybrid AR+FM.** Pure FM offers parallelism and simpler inference ([[2406.18009]], [[2025.acl-long.313]]); hybrid systems offer stronger semantic planning and in-context behavior through AR or LLM components ([[2412.10117]], [[2506.21619]], [[2025.acl-long.912]]). Current evidence favors hybrids for production-like generality and pure FM for efficient open-weight zero-shot synthesis.

- **Mel-spectrogram vs. latent/token targets.** Mel targets are mature and easy to vocode, as in E2 TTS and F5-TTS ([[2406.18009]], [[2025.acl-long.313]]), but they may bake in sequence-length and vocoder bottlenecks. LongCat-AudioDiT [[2603.29339]] argues for waveform VAE latents to avoid mel-vocoder compounding errors; DiFlow-TTS [[2509.09631]] argues for direct discrete flow over factorized codec tokens. These alternatives promise efficiency but introduce new compression or convergence failure modes.

- **CFG transferability.** Guidance is essential in many conditional FM systems, including F5-TTS [[2025.acl-long.313]] and CosyVoice 2 [[2412.10117]], but speech-specific CFG behavior remains under-theorized. The systematic negative evidence in [[2509.19668]] shows image-generation intuitions are not reliable enough to serve as default design rules.

- **Benchmark comparability.** Many FM papers report WER, SPK-SIM, UTMOS, RTF, and sometimes MOS, but comparisons are often across different datasets, prompt lengths, ASR backends, and training scales. This is visible in the heterogeneous comparisons across F5-TTS [[2025.acl-long.313]], OZSpeech [[2025.acl-long.1043]], APTTS [[interspeech-2025-0455]], and DiFlow-TTS [[2509.09631]].

## Open Questions

- Can few-step FM TTS below 5 NFE preserve subjective naturalness, not just WER, SPK-SIM, or UTMOS? Current evidence comes from RapFlow-TTS [[interspeech-2025-0554]], APTTS [[interspeech-2025-0455]], and EPSS [[interspeech-2025-2449]], but the evaluation protocols are not uniform.
- Does learned-prior FM scale beyond narrow or medium-resource settings without sacrificing naturalness and speaker similarity? OZSpeech [[2025.acl-long.1043]] is the key evidence, with Flamed-TTS [[2510.02848]] as a follow-up direction.
- Which representation is the best FM target for speech: mel-spectrograms ([[2406.18009]], [[2025.acl-long.313]]), waveform VAE latents ([[2603.29339]]), discrete codec tokens ([[2509.09631]]), or factorized codec priors ([[2025.acl-long.1043]], [[2510.02848]])?
- Can speech-specific CFG be formalized enough to replace current empirical schedule/weight tuning? [[2509.19668]] shows the problem, while F5-TTS [[2025.acl-long.313]] and CosyVoice 2 [[2412.10117]] are the main testbeds.
- Does the training-inference mismatch identified by LongCat-AudioDiT [[2603.29339]] apply broadly to existing Voicebox/F5-TTS-style systems, and can it be corrected without full retraining?
- Can PEFT adaptation findings from [[interspeech-2025-1344]] generalize across typologically distant languages and multi-speaker settings?
- Are FM-based dialogue generation systems competitive beyond two-speaker controlled dialogue, especially under interruption and long-context conditions? ZipVoice-Dialog [[2507.09318]] is the primary current evidence.

## Recommended Reader Path

1. [[2210.02747]] for the generic flow-matching objective.
2. [[2025.acl-long.313]] for the modern open-weight zero-shot FM TTS baseline.
3. [[2025.acl-long.1043]] for learned-prior one-step inference and the speed/intelligibility/naturalness trade-off.
4. [[interspeech-2025-0554]] and [[interspeech-2025-0455]] for two complementary few-step acceleration strategies.
5. [[interspeech-2025-2449]] for training-free step pruning.
6. [[2603.29339]] and [[2509.09631]] for representation-shifted frontier directions.

## Maintenance Notes

This lightweight page intentionally omits the exhaustive `All Papers` table. That table should live in a generated evidence appendix derived from `wiki/concepts/_evidence/flow-matching.yaml` and paper frontmatter.

The current evidence digest appears to contain some paper entries after `trend_notes`, which should be validated before using it as a source of truth. A future claim-graph schema should preserve each paper claim with `role`, `source`, `confidence`, and `concepts`, then aggregate those into canonical claim clusters.
