---
slug: flow-matching
title: Flow Matching
aliases: [CFM, OT-CFM, conditional flow matching, rectified flow, flow-based TTS]
status: established
last_reviewed: 2026-06-24
source_digest_date: 2026-06-24
generation:
  date: 2026-06-26
  stage: render-test
  mode: full
  agent: speech-generation-render-agent-v2
  model: claude-sonnet-4-6
  commit: 2d38f07
---

> [!abstract]
> Flow matching is a way to generate speech by learning how to turn noise into a speech representation over a small number of refinement steps. In this reviewed corpus, it is mainly used as the acoustic decoder: the part of a TTS or voice-conversion system that turns text, semantic tokens, or a speaker prompt into mel spectrograms or waveform-ready audio. Its practical appeal is speed: many recent systems use it to get diffusion-like quality with fewer sampling steps.

## Current Assessment

Flow matching is now one of the main continuous-output decoder choices in the papers covered here. The evidence is strongest for zero-shot TTS and voice conversion systems that need good quality without hundreds of sampling steps. The practical question is no longer whether flow matching can produce usable speech; the question is which system shape to choose around it.

Two patterns dominate this corpus. Pure non-autoregressive systems use flow matching directly to generate speech representations, which makes them attractive when latency and simple inference matter. Hybrid systems put an autoregressive language-model stage in front of a flow-matching acoustic decoder, which can improve style control, streaming behavior, or long-form structure, but adds sequential decoding cost.

## Evidence Boundaries

This page is based on 14 flow-matching-related papers, not a systematic survey of all recent TTS, voice conversion, and speech-language-model work. The strongest evidence concerns flow matching as an acoustic decoder in recent speech systems. The corpus is thinner on multilingual spontaneous speech, codec-native pure flow-matching systems, subjective naturalness evaluations, and direct comparisons against the newest non-flow baselines.

Some claims come from different kinds of evidence. The original flow-matching paper ([[2210.02747]]) supports the training objective and why fewer sampling steps are plausible, but it does not test speech. Later speech systems such as [[2406.18009|E2 TTS]], [[2025.acl-long.313|F5-TTS]], [[2412.04724|StableVC]], and [[2412.10117|CosyVoice 2]] show practical adoption and task-level results. Those system papers validate usefulness in speech, not the original theory itself.

## Major Claims

### Strongly Supported

- **Flow matching is a practical replacement for diffusion-style acoustic decoders when the goal is high-quality speech with fewer sampling steps.**
  Evidence: [[2210.02747]], [[2412.04724|StableVC]], [[2025.acl-long.313|F5-TTS]].
  Caveat: The theory comes from non-speech experiments; the speech evidence is mostly from specific TTS and VC systems with their own data, metrics, and decoder choices.

- **Recent speech systems can accelerate flow-matching inference to a small number of refinement steps, but the mechanisms are not interchangeable.**
  Evidence: [[2312.15821|Audiobox]], [[2406.05551|ARDiT]], [[2025.acl-long.1043|OZSpeech]].
  Caveat: Solver optimization, distillation, and learned-prior approaches solve different problems and introduce different quality-speed trade-offs.

- **The basic conditioning pattern used in diffusion models has transferred into flow-matching TTS systems as a standard practical tool.**
  Evidence: [[2207.12598]], [[2406.18009|E2 TTS]], [[2407.05407|CosyVoice]], [[2412.10117|CosyVoice 2]].
  Caveat: The original conditioning paper is image-only and predates flow matching; the speech claim is about successful adoption, not a formal proof that the mechanism is sufficient in all settings.

### Emerging

- **Pure flow-matching TTS can learn text-to-speech alignment with less explicit preprocessing than older alignment-heavy pipelines.**
  Evidence: [[2406.18009|E2 TTS]], [[2025.acl-long.313|F5-TTS]].
  Caveat: The evidence comes from related systems, and failures in complex scripts suggest that some text-processing support is still important.

- **Pure non-autoregressive flow-matching systems are attractive for low-latency generation, while autoregressive-plus-flow systems are attractive for style, control, and long-form behavior.**
  Evidence: [[2025.acl-long.313|F5-TTS]], [[2412.04724|StableVC]], [[2502.07243|Vevo]], [[2412.10117|CosyVoice 2]].
  Caveat: This is a trade-off, not a universal ranking. The best choice depends on whether speed, speaker similarity, style control, or streaming behavior matters most.

- **Some newer work suggests that flow matching can be improved after training, either through preference alignment, better step scheduling, or decoder refinement.**
  Evidence: [[2025.acl-long.313|F5-TTS]], [[2025.acl-long.598]], [[2502.17239|Baichuan-Audio]].
  Caveat: Several of these results are single-paper findings and should be treated as directions to watch rather than settled practice.

- **Learned-prior variants may reduce the data and sampling cost of flow-matching TTS, but current evidence shows a naturalness trade-off.**
  Evidence: [[2025.acl-long.1043|OZSpeech]].
  Caveat: This claim rests on one system, and the comparison changes several factors at once: prior design, codec representation, architecture, and training data.

## Method Families

**Pure flow-matching decoders.**
These systems use flow matching as the main generator for speech representations. They are the cleanest version of the idea and are most compelling when low latency and simple generation are priorities. In this corpus, [[2406.18009|E2 TTS]], [[2025.acl-long.313|F5-TTS]], and [[2412.04724|StableVC]] are the most useful examples for speech researchers. The main unresolved issue is whether these systems can match the strongest style and speaker-control behavior of hybrid systems without adding more pipeline complexity.

**Autoregressive front end plus flow-matching decoder.**
These systems use an autoregressive model to organize content, style, or semantic tokens, then use flow matching for the acoustic detail. This pattern is useful when control, streaming, long context, or style transfer matters more than fully parallel generation. [[2407.05407|CosyVoice]], [[2412.10117|CosyVoice 2]], [[2502.07243|Vevo]], and [[2503.14345|MoonCast]] are the main examples in this corpus. The trade-off is that the autoregressive stage reintroduces sequential latency.

**Accelerated or single-step flow matching.**
This family asks whether flow-matching speech models can be pushed toward very few sampling steps. The corpus includes several routes: better solvers, distillation, and learned starting representations. The headline is promising, but the practical choice depends on which quality dimension is binding: naturalness, intelligibility, speaker similarity, or runtime.

**Conditioning lineage from classifier-free guidance.**
Classifier-free guidance is historical context rather than direct speech evidence. It matters because many flow-matching TTS systems use the same broad conditioning idea, but the original paper does not test audio or flow-matching velocity fields. For current speech decisions, downstream TTS systems are the relevant evidence.

## How to Interpret Older and Newer Evidence

[[2210.02747]] is the theory starting point. Read it to understand why flow matching can train a continuous generator without simulating the full generation process during training, and why simpler generation paths can reduce sampling cost. Do not treat it as speech-quality evidence.

The 2024 systems provide the core speech evidence. [[2406.18009|E2 TTS]] and [[2025.acl-long.313|F5-TTS]] are the clearest pure TTS line; [[2412.04724|StableVC]] extends the case to voice conversion; [[2407.05407|CosyVoice]] and [[2412.10117|CosyVoice 2]] show the hybrid language-model-plus-flow-decoder pattern.

The 2025 papers are useful frontier signals. Preference alignment, learned priors, post-tokenization refinement, and long-form hybrid generation are all plausible directions, but several are supported by one paper each in this corpus.

## Current Tensions

- **Speed vs. control.** Pure flow-matching systems are attractive for fast generation ([[2025.acl-long.313|F5-TTS]], [[2412.04724|StableVC]]), while hybrid systems tend to offer stronger style or long-form control by adding an autoregressive stage ([[2502.07243|Vevo]], [[2503.14345|MoonCast]]). This is the central practical architecture choice in the corpus.
- **Mel spectrograms vs. codec-based representations.** Mel-based systems are simple and well represented in the evidence ([[2406.18009|E2 TTS]], [[2025.acl-long.313|F5-TTS]]), but codec-based or learned-prior systems may improve intelligibility and integration with speech language models ([[2025.acl-long.1043|OZSpeech]], [[2502.17239|Baichuan-Audio]]). The current evidence does not yet settle the naturalness trade-off.
- **Theory vs. speech validation.** The mathematical motivation for flow matching is strong ([[2210.02747]]), but the practical speech claims depend on system-level evidence ([[2406.18009|E2 TTS]], [[2025.acl-long.313|F5-TTS]], [[2412.04724|StableVC]]). A reader should keep those layers separate.
- **Single-paper frontier claims.** Step scheduling ([[2025.acl-long.313|F5-TTS]]), preference alignment in velocity space ([[2025.acl-long.598]]), and learned-prior single-step synthesis ([[2025.acl-long.1043|OZSpeech]]) are promising but not yet broadly replicated in this corpus.

## Decision Implications

- Prefer a pure flow-matching decoder when low latency, simpler inference, and non-autoregressive generation are the main constraints; this is the clearest practical lesson from the pure-system evidence ([[2025.acl-long.313|F5-TTS]], [[2412.04724|StableVC]]).
- Consider a hybrid autoregressive-plus-flow system when style control, streaming behavior, long-form structure, or speaker/style disentanglement matters more than fully parallel generation ([[2412.10117|CosyVoice 2]], [[2502.07243|Vevo]], [[2503.14345|MoonCast]]).
- Treat single-step and learned-prior flow matching as promising but unsettled; current evidence suggests meaningful speed or data-efficiency gains, but with naturalness and reproducibility questions ([[2312.15821|Audiobox]], [[2406.05551|ARDiT]], [[2025.acl-long.1043|OZSpeech]]).
- Do not use the foundational flow-matching paper alone to justify a speech-system design choice. Use [[2210.02747]] for theory, then rely on speech systems for practical expectations ([[2406.18009|E2 TTS]], [[2025.acl-long.313|F5-TTS]], [[2412.10117|CosyVoice 2]]).
- Be cautious when comparing headline numbers across systems: the papers vary in training scale, language coverage, representation type, and evaluation metrics ([[2406.18009|E2 TTS]], [[2025.acl-long.313|F5-TTS]], [[2025.acl-long.1043|OZSpeech]], [[2503.14345|MoonCast]]).

## Open Questions

- Can pure flow-matching systems close the speaker-similarity and style-control gap without adding an autoregressive stage? The question is motivated by the contrast between pure systems and hybrid style-control systems ([[2025.acl-long.313|F5-TTS]], [[2412.04724|StableVC]], [[2502.07243|Vevo]]).
- Are codec-native or learned-prior flow-matching systems a replacement for mel-spectrogram systems, or a separate trade-off point? Current evidence suggests better intelligibility or integration may come with naturalness and infrastructure costs ([[2025.acl-long.313|F5-TTS]], [[2025.acl-long.1043|OZSpeech]], [[2502.17239|Baichuan-Audio]]).
- Do step scheduling, solver optimization, and learned-prior methods stack, or do they solve overlapping parts of the same sampling problem? The corpus has separate evidence for each route but no direct composition study ([[2025.acl-long.313|F5-TTS]], [[2312.15821|Audiobox]], [[2025.acl-long.1043|OZSpeech]]).
- Does preference alignment improve perceptual naturalness, or mainly intelligibility metrics? The current velocity-space alignment evidence is WER-centered and single-system ([[2025.acl-long.598]]).
- How well do current flow-matching systems generalize beyond clean audiobook-style data to spontaneous, noisy, multilingual, or code-switched speech? Several key systems rely heavily on clean or proprietary data, and long-form/generalization evidence remains narrow ([[2406.18009|E2 TTS]], [[2502.07243|Vevo]], [[2503.14345|MoonCast]]).

## Recommended Reader Path

1. [[2210.02747]] — Start here for the core idea and why flow matching is expected to reduce sampling cost; remember that it is not speech evidence.
2. [[2406.18009|E2 TTS]] — Read for the first clear practical version of alignment-light, flow-matching zero-shot TTS in this corpus.
3. [[2025.acl-long.313|F5-TTS]] — Read next for the strongest pure flow-matching TTS recipe represented here and for practical improvements to alignment and sampling.
4. [[2412.04724|StableVC]] — Read for voice conversion evidence and direct comparison against diffusion-style baselines.
5. [[2412.10117|CosyVoice 2]] — Read for the hybrid system pattern, especially streaming and production-style constraints.
6. [[2025.acl-long.1043|OZSpeech]] — Read as a frontier case for learned-prior, single-step generation and the data-efficiency vs. naturalness trade-off.
7. [[2025.acl-long.598]] — Read last for preference alignment applied directly to flow-matching TTS.

## Related Concepts and Pages

- [[evidence/flow-matching|Evidence Dossier]] — full claim matrix, paper inventory, evidence-strength notes, and reassessment candidates for this concept.
- [[autoregressive-codec-tts|Autoregressive Codec TTS]] — relevant for the hybrid autoregressive-plus-flow pattern and the speed/control trade-off.
- [[zero-shot-tts|Zero-Shot TTS]] — most of the current TTS evidence for flow matching is framed around zero-shot speaker prompting and in-context generation.
- [[voice-conversion|Voice Conversion]] — StableVC provides the main voice-conversion evidence in this flow-matching corpus.
- [[neural-codec|Neural Audio Codec]] — relevant for learned-prior and post-tokenization refinement variants that move beyond mel-spectrogram generation.

---

_Temporary render test from `wiki/_claims/flow-matching.yaml` using the V2 render-agent instructions. This file is not part of the generated wiki output._
