# Citation-Discovery Papers: Ingest Strategy

**Date:** 2026-06-09
**Papers classified:** 162
**Decisions finalised:** 2026-06-09

---

## Resolved Decisions

1. **`2312.10997` (RAG for LLMs Survey)** → Tier 2. Only 5 corpus citations; too peripheral for full treatment.
2. **MusicLM (`2301.11325`) and AudioLDM (`2301.12503`)** → confirmed Tier 1. Both are audio-lm papers cited 19× and 14× respectively; foundational to audio generation alongside AudioLM, SoundStorm, and SpeechGPT.
3. **Lightweight stub implementation** → new `speech-generation-lightweight-ingest-agent` agent spec (see `.claude/agents/`). Same procedure skeleton as the standard ingest agent; different page format (no Claims, Key Results, Novelty Assessment, or Field Significance).
4. **Tier 3 eliminated** → all 13 former Tier 3 papers upgraded to Tier 2. All 162 citation-discovery papers receive a wiki stub.

---

## Strategy Overview

| Tier | Format | Count | When to ingest | Agent |
|------|--------|-------|----------------|-------|
| 1 — Full | Standard template (same as 699 standard papers) | 96 | Interleaved with standard corpus, chronologically | `speech-generation-ingest-agent` |
| 2 — Lightweight stub | Frontmatter + abstract callout + Context in Speech Generation + Wiki Connections | 66 | Batch after ~200 standard papers ingested | `speech-generation-lightweight-ingest-agent` |

**Key signal:** `sr_match=Y` (57 papers) means the paper would have been caught by the standard keyword filter. Nearly all land in Tier 1.

---

## Tier 1 — Full Standard Ingest (94 papers)

Same pipeline, same template, same 2-at-a-time cadence. Interleave with standard corpus by `published_date`.

### tts-vc (42 papers)
All TTS/VC papers receive full treatment regardless of `sr_match`.

| ID | Title | Year | Citations |
|----|-------|------|-----------|
| 2010.05646 | HiFi-GAN | 2020 | 123× |
| 2403.03100 | NaturalSpeech 3 | 2024 | 118× |
| 2503.01710 | Spark-TTS | 2025 | 100× |
| 2006.04558 | FastSpeech 2 | 2020 | 95× |
| 2409.00750 | MaskGCT | 2024 | 91× |
| 2505.17589 | CosyVoice 3 | 2025 | 82× |
| 2502.04128 | Llasa | 2025 | 76× |
| 2306.00814 | Vocos | 2023 | 72× |
| 2406.05370 | VALL-E 2 | 2024 | 70× |
| 2206.04658 | BigVGAN | 2022 | 67× |
| 2406.04904 | XTTS | 2024 | 55× |
| 2406.18009 | E2 TTS | 2024 | 55× |
| 2409.03283 | FireRedTTS | 2024 | 55× |
| 2403.16973 | VoiceCraft | 2024 | 49× |
| 2304.09116 | NaturalSpeech 2 | 2023 | 48× |
| 2303.03926 | VALL-E X | 2023 | 47× |
| 1712.05884 | Tacotron 2 | 2017 | 42× |
| 2402.01912 | Natural language guidance of TTS | 2024 | 42× |
| 1609.03499 | WaveNet | 2016 | 41× |
| 2305.07243 | Better speech synthesis through scaling | 2023 | 41× |
| 2407.08551 | Autoregressive Speech Synthesis without VQ | 2024 | 39× |
| 1703.10135 | Tacotron | 2017 | 38× |
| 2402.08093 | BASE TTS | 2024 | 37× |
| 2411.01156 | Fish-Speech | 2024 | 35× |
| 2505.07916 | MiniMax-Speech | 2025 | 34× |
| 2104.00355 | Speech Resynthesis from Discrete Disentangled Units | 2021 | 33× |
| 2105.06337 | Grad-TTS | 2021 | 30× |
| 2502.05512 | IndexTTS | 2025 | 29× |
| 2502.07243 | Vevo | 2025 | 29× |
| 2406.07855 | VALL-E R | 2024 | 28× |
| 2411.09943 | Zero-shot VC with Diffusion Transformers | 2024 | 25× |
| 2401.07333 | ELLA-V | 2024 | 24× |
| 2506.13053 | ZipVoice | 2025 | 24× |
| 2406.05551 | Autoregressive Diffusion Transformer for TTS | 2024 | 21× |
| 2502.18924 | MegaTTS 3 | 2025 | 21× |
| 2412.04724 | StableVC | 2024 | 16× |
| 2404.03204 | RALL-E | 2024 | 15× |
| 2406.00654 | Enhancing Zero-shot TTS with Human Feedback | 2024 | 15× |
| 2503.14345 | MoonCast | 2025 | 14× |
| 2312.01479 | OpenVoice | 2023 | 13× |
| 2508.04195 | NVSpeech | 2025 | 13× |
| 2504.02407 | F5R-TTS | 2025 | 9× |

### codec (9 papers)

| ID | Title | Year | Citations |
|----|-------|------|-----------|
| 2210.13438 | EnCodec | 2022 | 179× |
| 2308.16692 | SpeechTokenizer | 2023 | 104× |
| 2408.16532 | WavTokenizer | 2024 | 65× |
| 2409.05377 | BigCodec | 2024 | 53× |
| 2305.02765 | HiFi-Codec | 2023 | 50× |
| 2411.19842 | Scaling Transformers for Low-Bitrate Codec | 2024 | 40× |
| 2411.18803 | TS3-Codec | 2024 | 25× |
| 2505.13000 | DualCodec | 2025 | 15× |
| 2504.10344 | ALMTokenizer | 2025 | 10× |

### audio-lm (11 papers)

| ID | Title | Year | Citations |
|----|-------|------|-----------|
| 2305.11000 | SpeechGPT | 2023 | 64× |
| 2209.03143 | AudioLM | 2022 | 63× |
| 2305.09636 | SoundStorm | 2023 | 44× |
| 2306.12925 | AudioPaLM | 2023 | 41× |
| 2402.05755 | Spirit LM | 2024 | 37× |
| 2310.00704 | UniAudio | 2023 | 36× |
| 2312.15821 | Audiobox | 2023 | 26× |
| 2301.12503 | AudioLDM | 2023 | 19× |
| 2411.17607 | Scaling Speech-Text Pre-training | 2024 | 19× |
| 2305.15255 | Spoken Question Answering and Speech Continuation | 2023 | 17× |
| 2301.11325 | MusicLM | 2023 | 14× |

### sca (15 papers)

| ID | Title | Year | Citations |
|----|-------|------|-----------|
| 2410.00037 | Moshi | 2024 | 208× |
| 2412.02612 | GLM-4-Voice | 2024 | 113× |
| 2408.16725 | Mini-Omni | 2024 | 77× |
| 2409.06666 | LLaMA-Omni | 2024 | 70× |
| 2411.00774 | Freeze-Omni | 2024 | 66× |
| 2502.11946 | Step-Audio | 2025 | 48× |
| 2501.06282 | MinMo | 2025 | 47× |
| 2502.17239 | Baichuan-Audio | 2025 | 38× |
| 2507.16632 | Step-Audio 2 | 2025 | 37× |
| 2410.11190 | Mini-Omni2 | 2024 | 34× |
| 2412.15649 | SLAM-Omni | 2024 | 32× |
| 2410.17799 | OmniFlatten | 2024 | 28× |
| 2505.02625 | LLaMA-Omni2 | 2025 | 23× |
| 2408.02622 | Language Model Can Listen While Speaking | 2024 | 19× |
| 2511.15848 | Step-Audio-R1 | 2025 | 7× |

### survey (7 papers)
_Note: `2312.10997` (RAG for LLMs) moved to Tier 2 — only 5 corpus citations._

| ID | Title | Year | Citations |
|----|-------|------|-----------|
| 2411.13577 | WavChat: Survey of Spoken Dialogue Models | 2024 | 42× |
| 2106.15561 | A Survey on Neural Speech Synthesis | 2021 | 36× |
| 2410.03751 | Recent Advances in Speech Language Models | 2024 | 33× |
| 2502.06490 | Recent Advances in Discrete Speech Tokens | 2025 | 32× |
| 2504.08528 | On The Landscape of Spoken Language Models | 2025 | 27× |
| 2506.10274 | Discrete Audio Tokens: More Than a Survey! | 2025 | 17× |
| 2402.13236 | Towards audio language modeling — an overview | 2024 | 13× |

### evaluation — sr_match=Y + full-duplex benchmarks (7 papers)

| ID | Title | Year | Citations |
|----|-------|------|-----------|
| 2204.02152 | UTMOS | 2022 | 163× |
| 2410.17196 | VoiceBench | 2024 | 60× |
| 2505.09558 | WavReward | 2025 | 11× |
| 2506.16381 | InstructTTSEval | 2025 | 17× |
| 2505.14648 | Vox-Profile | 2025 | 7× |
| 2507.23159 | Full-Duplex-Bench v1.5 | 2025 | 17× |
| 2510.07838 | Full-Duplex-Bench-v2 | 2025 | 7× |

### asr — Whisper only (1 paper)

| ID | Title | Year | Citations |
|----|-------|------|-----------|
| 2212.04356 | Whisper | 2022 | 196× |

### dataset — sr_match=Y (2 papers)

| ID | Title | Year | Citations |
|----|-------|------|-----------|
| 1904.02882 | LibriTTS | 2019 | 157× |
| 2407.05361 | Emilia | 2024 | 65× |

### ml-method — architecturally central to TTS (2 papers)

| ID | Title | Year | Citations |
|----|-------|------|-----------|
| 2210.02747 | Flow Matching for Generative Modeling | 2022 | 79× |
| 2207.12598 | Classifier-Free Diffusion Guidance | 2022 | 47× |

---

## Tier 2 — Lightweight Stubs (68 papers)

Format: frontmatter + `> [!abstract]` callout + `## Context in Speech Generation` (2–4 sentences) + `## Wiki Connections`. No Claims, no Novelty Assessment, no Key Results, no Field Significance. Goal: wikilinks resolve, readers have context, integration agent can cross-link.

Batch these after ~200 standard papers are ingested. Up to 5 at a time.

### evaluation (11 papers)
_Full-Duplex-Bench v1.5 and v2 promoted to Tier 1 — directly evaluate SCA/S2S systems._

| ID | Title | Year | Citations |
|----|-------|------|-----------|
| 2312.15185 | emotion2vec | 2023 | 64× |
| 2106.04624 | SpeechBrain | 2021 | 21× |
| 2406.14294 | DASB | 2024 | 20× |
| 2402.07729 | AIR-Bench | 2024 | 19× |
| 2410.19168 | MMAU | 2024 | 19× |
| 2502.05139 | Meta Audiobox Aesthetics | 2025 | 25× |
| 2308.05725 | EXPRESSO | 2023 | 15× |
| 2506.02863 | CapSpeech | 2025 | 11× |
| 2508.13992 | MMAU-Pro | 2025 | 9× |
| 2510.14664 | SpeechLLM-as-Judges | 2025 | 9× |
| 2507.12705 | AudioJudge | 2025 | 8× |

### asr (3 papers)

| ID | Title | Year | Citations |
|----|-------|------|-----------|
| 2206.08317 | Paraformer | 2022 | 35× |
| 2509.08753 | Streaming S2S with Delayed Streams | 2025 | 11× |
| 2511.09690 | Omnilingual ASR | 2025 | 6× |

### dataset (7 papers)

| ID | Title | Year | Citations |
|----|-------|------|-----------|
| 1912.06670 | Common Voice | 2019 | 59× |
| 2012.03411 | MLS | 2020 | 43× |
| 2106.06909 | GigaSpeech | 2021 | 36× |
| 1510.08484 | MUSAN | 2015 | 15× |
| 1808.10583 | AISHELL-2 | 2018 | 12× |
| 2007.10310 | CoVoST 2 | 2020 | 12× |
| 1908.06248 | JVS corpus | 2019 | 9× |

### speaker (1 paper)

| ID | Title | Year | Citations |
|----|-------|------|-----------|
| 2005.07143 | ECAPA-TDNN | 2020 | 54× |

### multimodal (15 papers)

| ID | Title | Year | Citations |
|----|-------|------|-----------|
| 2503.20215 | Qwen2.5-Omni | 2025 | 124× |
| 2504.18425 | Kimi-Audio | 2025 | 96× |
| 2407.10759 | Qwen2-Audio | 2024 | 87× |
| 2311.07919 | Qwen-Audio | 2023 | 59× |
| 2407.04051 | FunAudioLLM | 2024 | 42× |
| 2312.05187 | Seamless | 2023 | 38× |
| 2310.13289 | SALMONN | 2023 | 31× |
| 2501.15368 | Baichuan-Omni-1.5 | 2025 | 18× |
| 2507.08128 | Audio Flamingo 3 | 2025 | 18× |
| 2308.11596 | SeamlessM4T | 2023 | 17× |
| 2408.01800 | MiniCPM-V | 2024 | 17× |
| 2408.05211 | VITA | 2024 | 17× |
| 2505.03739 | VITA-Audio | 2025 | 17× |
| 2501.01957 | VITA-1.5 | 2025 | 16× |
| 2501.07246 | Audio-CoT | 2025 | 8× |

### foundation-lm (20 papers)
_13 original Tier 2 + 7 upgraded from former Tier 3._

| ID | Title | Year | Citations | Note |
|----|-------|------|-----------|------|
| 2407.21783 | Llama 3 | 2024 | 89× | |
| 2303.08774 | GPT-4 | 2023 | 81× | |
| 2410.21276 | GPT-4o System Card | 2024 | 70× | |
| 2412.15115 | Qwen2.5 | 2024 | 65× | |
| 2505.09388 | Qwen3 | 2025 | 55× | |
| 2302.13971 | LLaMA | 2023 | 52× | |
| 2501.12948 | DeepSeek-R1 | 2025 | 41× | |
| 2412.19437 | DeepSeek-V3 | 2024 | 34× | |
| 2307.09288 | Llama 2 | 2023 | 23× | |
| 2407.10671 | Qwen2 | 2024 | 21× | |
| 2309.16609 | Qwen (original) | 2023 | 17× | |
| 2312.11805 | Gemini (family) | 2023 | 24× | |
| 2507.06261 | Gemini 2.5 | 2025 | 45× | |
| 1810.04805 | BERT | 2018 | 25× | formerly Tier 3 |
| 2005.14165 | GPT-3 | 2020 | 23× | formerly Tier 3 |
| 2402.03300 | DeepSeekMath | 2024 | 33× | formerly Tier 3 |
| 2503.01743 | Phi-4-Mini | 2025 | 16× | formerly Tier 3 |
| 2503.19786 | Gemma 3 | 2025 | 11× | formerly Tier 3 |
| 2412.08635 | Multimodal Latent LLM | 2024 | 8× | formerly Tier 3 |
| 2506.07900 | MiniCPM4 | 2025 | 4× | formerly Tier 3 |

### ml-method (8 papers)
_2 original Tier 2 + 6 upgraded from former Tier 3._

| ID | Title | Year | Citations | Note |
|----|-------|------|-----------|------|
| 2309.15505 | Finite Scalar Quantization (FSQ) | 2023 | 35× | |
| 2302.00482 | Improving and generalizing flow matching (minibatch OT) | 2023 | 12× | |
| 1412.6980 | Adam optimizer | 2014 | 43× | formerly Tier 3 |
| 1711.05101 | AdamW | 2017 | 72× | formerly Tier 3 |
| 1607.06450 | Layer Normalization | 2016 | 7× | formerly Tier 3 |
| 2002.05202 | GLU Variants | 2020 | 11× | formerly Tier 3 |
| 2001.08361 | Scaling Laws | 2020 | 8× | formerly Tier 3 |
| 2308.10248 | Activation Engineering | 2023 | 4× | formerly Tier 3 |

### survey (1 paper)

| ID | Title | Year | Citations |
|----|-------|------|-----------|
| 2312.10997 | RAG for LLMs: A Survey | 2023 | 5× |

---

## Summary

| Tier | Count | Action |
|------|-------|--------|
| 1 — Full | 96 | Interleave with standard corpus; 2 at a time; chronological; `speech-generation-ingest-agent` |
| 2 — Stub | 66 | Batch after ~200 standard papers; up to 5 at a time; `speech-generation-lightweight-ingest-agent` |
| **Total** | **162** | All papers get a wiki page |
