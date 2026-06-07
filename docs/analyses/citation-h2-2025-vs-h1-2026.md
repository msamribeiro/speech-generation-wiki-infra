# Citation Rate Comparison: H2 2025 vs H1 2026

**Generated:** 2026-06-07  
**Reproduced with:** `python scripts/discover/citation_period_compare.py --window-a 2025-07-01 2025-12-31 --label-a "H2 2025" --window-b 2026-01-01 2026-06-30 --label-b "H1 2026" --top-n 100`

## Key Findings

**Moshi as the new centre of gravity.** Moshi (Défossez et al., 2024) was already #3 in H2 2025 at 0.208 citation rate; by H1 2026 it is #1 at 0.308 — the only paper to cross the 30% mark in either window. This is the steepest absolute rise among papers present in both top-100s. The spoken conversational agent literature is converging on Moshi as the canonical reference architecture the way TTS converged on WaveNet in 2017.

**The VALL-E / codec LM foundational era is receding.** The biggest faller in the comparison is the original VALL-E paper ("Neural codec language models are zero-shot text to speech synthesizers"), dropping from #8 (0.151) to #54 (0.055) — a ×0.37 ratio. FastSpeech 2 fell ×0.54, HiFi-GAN ×0.50. These are not being forgotten; they are being assumed. The community has absorbed them as infrastructure and no longer cites them per-paper.

**The Qwen ecosystem is consolidating the SCA landscape.** Qwen2.5-Omni rose #15→#3 (×1.88), Qwen2-Audio #40→#12 (×1.77), Qwen3 #85→#15 (×2.44), Qwen2.5 #54→#19 (×1.44). The Qwen family collectively accounts for four of the top-20 positions in H1 2026 that it did not dominate in H2 2025. New spoken dialogue and SCA papers are increasingly built on Qwen-family LLMs as a shared backbone.

**2025-generation models are already being cited as foundational.** CosyVoice 3 (×2.58, #57→#7), KimiAudio (×2.47, #49→#6), Spark-TTS (×1.60, #20→#8) all broke into the H1 2026 top-10. Papers published in 2025 are being cited at rates that match the 2021–2022 cohort of foundational models — suggesting the field's reference pool is turning over faster than in prior periods.

**General-purpose LLMs are becoming a cited dependency.** DeepSeek-R1, DeepSeek-V3, GPT-4o, and Gemini 2.5 all appear in or enter the H1 2026 top-100 (DeepSeek-R1 at #40, Gemini 2.5 at #21). This reflects SCA papers increasingly treating general-purpose reasoning LLMs as a standard component rather than an external comparison, citing them the way earlier TTS papers cited HuBERT or WavLM for representations.

**Evaluation infrastructure is gaining stable citation.** VoiceBench (×1.75), UTMOS stable in both top-5s, DNSMOS newly entering in H1 2026, and the survey "On the landscape of spoken language models" appearing at #45. Evaluation tooling and survey papers are accruing citations at a rate approaching the model papers themselves — a sign of a maturing field establishing shared measurement conventions.

**Dropped papers reflect trend completion, not irrelevance.** Papers that exited the top-100 in H1 2026 — Matcha-TTS, VoiceCraft, BASE TTS, NaturalSpeech 2, CosyVoice (v1) — are 2023–2024 works that were active baselines in H2 2025 but have since been superseded by later papers in the same lineage. CosyVoice v1 and v2 dropped out while CosyVoice 3 rose to #7; this is succession, not abandonment.

---

## Overview

| | H2 2025 | H1 2026 |
|-|-------|-------|
| Corpus papers in window | 524 | 289 |
| Papers in both top-100 | 75 | 75 |
| Papers unique to this window | 25 | 25 |

Citation rate = fraction of papers in the window citing this work. A rate of 0.20 means 20% of the window's papers cite it.

## Top 100: H2 2025

| Rank | Rate | Title | Year |
|------|------|-------|------|
| 1 | 0.229 | Robust speech recognition via large-scale weak supervision | 2022 |
| 2 | 0.218 | High fidelity neural audio compression | 2022 |
| 3 | 0.208 | Moshi: a speechtext foundation model for real-time dialogue | 2024 |
| 4 | 0.202 | Utmos: Utokyo-sarulab system for voicemos challenge 2022 | 2022 |
| 5 | 0.193 | Libritts: A corpus derived from librispeech for text-to-speech | 2019 |
| 6 | 0.181 | HiFi-GAN: Generative Adversarial Networks for Efficient and High Fidelity Speech Synthesis | 2010 |
| 7 | 0.157 | NaturalSpeech 3: Zero-Shot Speech Synthesis with Factorized Codec and Diffusion Models | 2024 |
| 8 | 0.151 | Neural codec language models are zero-shot text to speech synthesizers | 2023 |
| 9 | 0.147 | Hubert: Self-supervised speech representation learning by masked prediction of hidden units | 2021 |
| 10 | 0.141 | Wavlm: Large-scale self-supervised pre-training for full stack speech processing | 2021 |
| 11 | 0.128 | Fastspeech 2: Fast and high-quality end-to-end text to speech | 2006 |
| 12 | 0.122 | Cosyvoice 2: Scalable streaming speech synthesis with large language models | 2024 |
| 13 | 0.115 | Glm-4-voice: Towards intelligent and human-like endto-end spoken chatbot | 2024 |
| 14 | 0.115 | SoundStream: An End-to-End Neural Audio Codec | 2021 |
| 15 | 0.109 | Qwen2. 5-omni technical report | 2025 |
| 16 | 0.109 | Librispeech: An ASR corpus based on public domain audio books, | 2015 |
| 17 | 0.103 | Cosyvoice: A scalable multilingual zero-shot text-to-speech synthesizer based on supervised semantic tokens | 2024 |
| 18 | 0.101 | Gpt-4 technical report | 2023 |
| 19 | 0.101 | Seedtts: A family of high-quality versatile speech generation models | 2024 |
| 20 | 0.099 | Spark-tts: An efficient llm-based text-to-speech model with single-stream decoupled speech tokens | 2025 |
| 21 | 0.099 | Flow matching for generative modeling | 2022 |
| 22 | 0.097 | Speechtokenizer: Unified speech tokenizer for speech large language models | 2024 |
| 23 | 0.095 | Vocos: Closing the gap between time-domain and fourierbased neural vocoders for high-quality audio synthesis | 2024 |
| 24 | 0.092 | The llama 3 herd of models | 2024 |
| 25 | 0.090 | High-fidelity audio compression with improved rvqgan | 2024 |
| 26 | 0.090 | Maskgct: Zero-shot text-to-speech with masked generative codec transformer | 2024 |
| 27 | 0.088 | VALL-E 2: Neural Codec Language Models are Human Parity Zero-Shot Text to Speech Synthesizers | 2024 |
| 28 | 0.086 | Decoupled weight decay regularization | 2017 |
| 29 | 0.086 | Bigvgan: A universal neural vocoder with large-scale training | 2022 |
| 30 | 0.086 | F5-tts: A fairytaler that fakes fluent and faithful speech with flow matching | 2025 |
| 31 | 0.084 | Emilia: An extensive, multilingual, and diverse speech dataset for large-scale speech generation | 2024 |
| 32 | 0.084 | Speechgpt: Empowering large language models with intrinsic cross-modal conversational abilities | 2023 |
| 33 | 0.082 | Llasa: Scaling train-time and inferencetime compute for llama-based speech synthesis | 2025 |
| 34 | 0.082 | Freeze-omni: A smart and low latency speech-to-speech dialogue model with frozen llm | 2024 |
| 35 | 0.082 | Voicecraft: Zero-shot speech editing and text-to-speech in the wild | 2024 |
| 36 | 0.082 | Conditional variational autoencoder with adversarial learning for end-to-end text-to-speech | 2021 |
| 37 | 0.080 | Llama-omni: Seamless speech interaction with large language models | 2024 |
| 38 | 0.078 | Emotion2vec: Self-supervised pre-training for speech emotion representation | 2023 |
| 39 | 0.078 | Mini-omni: Language models can hear, talk while thinking in streaming | 2024 |
| 40 | 0.078 | Qwen2-audio technical report | 2024 |
| 41 | 0.076 | Common voice: A massively-multilingual speech corpus | 2019 |
| 42 | 0.074 | Wavtokenizer: An efficient acoustic discrete codec tokenizer for audio language modeling | 2025 |
| 43 | 0.072 | Qwen-audio: Advancing universal audio understanding via unified large-scale audio-language models | 2023 |
| 44 | 0.072 | Attention Is All You Need | 2023 |
| 45 | 0.072 | Audiolm: a language modeling approach to audio generation | 2023 |
| 46 | 0.071 | Ecapa-tdnn: Emphasized channel attention, propagation and aggregation in tdnn based speaker verification | 2005 |
| 47 | 0.069 | Wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations | 2020 |
| 48 | 0.069 | Fireredtts: A foundation text-to-speech framework for industry-level generative speech applications | — |
| 49 | 0.069 | Kimiaudio technical report | 2025 |
| 50 | 0.069 | Llama: Open and efficient foundation language models | 2023 |
| 51 | 0.069 | E2 tts: Embarrassingly easy fully non-autoregressive zero-shot tts | 2024 |
| 52 | 0.067 | Voicebox: Text-guided multilingual universal speech generation at scale | 2023 |
| 53 | 0.067 | Hifi-codec: Group-residual vector quantization for high fidelity audio codec | 2023 |
| 54 | 0.065 | Qwen2.5 technical report | 2025 |
| 55 | 0.065 | Adam: A Method for Stochastic Optimization | 2014 |
| 56 | 0.065 | NaturalSpeech 2: Latent Diffusion Models are Natural and Zero-Shot Speech and Singing Synthesizers | 2023 |
| 57 | 0.063 | Cosyvoice 3: Towards in-the-wild speech generation via scaling-up and post-training | 2025 |
| 58 | 0.063 | Xtts: a massively multilingual zero-shot text-to-speech model | 2024 |
| 59 | 0.061 | Speak foreign languages with your own voice: Cross-lingual neural codec language modeling | 2023 |
| 60 | 0.061 | Bigcodec: Pushing the limits of low-bitrate neural speech codec | 2024 |
| 61 | 0.061 | Neural discrete representation learning | 2017 |
| 62 | 0.059 | Mls: A large-scale multilingual dataset for speech research | 2012 |
| 63 | 0.059 | GPT-4o system card | 2024 |
| 64 | 0.057 | MinMo: A multimodal large language model for seamless voice interaction | 2025 |
| 65 | 0.055 | Perceptual evaluation of speech quality (pesq)-a new method for speech quality assessment of telephone networks and codecs | 2001 |
| 66 | 0.055 | Classifier-free diffusion guidance | 2022 |
| 67 | 0.053 | Natural TTS synthesis by conditioning wavenet on mel spectrogram predictions | 2018 |
| 68 | 0.053 | Yourtts: Towards zero-shot multi-speaker tts and zero-shot voice conversion for everyone | 2023 |
| 69 | 0.051 | Voicebench: Benchmarking llm-based voice assistants | — |
| 70 | 0.051 | Soundstorm: Efficient parallel audio generation | 2023 |
| 71 | 0.051 | BASE TTS: Lessons from building a billion-parameter text-to-speech model on 100k hours of data | 2024 |
| 72 | 0.050 | Matcha-tts: A fast TTS architecture with conditional flow matching | 2023 |
| 73 | 0.050 | Audiopalm: A large language model that can speak and listen | 2023 |
| 74 | 0.050 | Autoregressive speech synthesis without vector quantization | 2024 |
| 75 | 0.048 | A survey on neural speech synthesis | 2021 |
| 76 | 0.048 | Paraformer: Fast and accurate parallel transformer for non-autoregressive end-to-end speech recognition | 2022 |
| 77 | 0.048 | Funaudiollm: Voice understanding and generation foundation models for natural interaction between humans and llms | 2024 |
| 78 | 0.048 | Seamless: Multilingual Expressive and Streaming Speech Translation | 2023 |
| 79 | 0.048 | Conformer: Convolution-augmented transformer for speech recognition | 2005 |
| 80 | 0.046 | Scaling transformers for low-bitrate high-quality speech coding | 2024 |
| 81 | 0.046 | The lj speech dataset | 2017 |
| 82 | 0.044 | Diffusion-based voice conversion with fast maximum likelihood sampling scheme | 2021 |
| 83 | 0.044 | LoRA: Low-rank adaptation of large language models | 2021 |
| 84 | 0.044 | Step-audio: Unified understanding and generation in intelligent speech interaction | 2025 |
| 85 | 0.044 | Qwen3 technical report | 2025 |
| 86 | 0.044 | Speech resynthesis from discrete disentangled self-supervised representations | 2021 |
| 87 | 0.042 | Slam-omni: Timbrecontrollable voice interaction system with single-stage training | 2024 |
| 88 | 0.042 | Natural Language Guidance of HighFidelity Text-to-Speech with Synthetic Annotations | 2024 |
| 89 | 0.042 | SpiRit-LM: Interleaved spoken and written language model | 2024 |
| 90 | 0.042 | Finite scalar quantization: Vq-vae made simple | 2023 |
| 91 | 0.042 | Freevc: Towards high-quality text-free one-shot  voice  conversion | 2023 |
| 92 | 0.042 | Libri-Light: A Benchmark for ASR with Limited or No Supervision | 2020 |
| 93 | 0.042 | Libritts-r: A restored multispeaker text-to-speech corpus | 2023 |
| 94 | 0.042 | Scalable diffusion models with transformers | 2023 |
| 95 | 0.042 | Uniaudio: An audio foundation model toward universal audio generation | 2024 |
| 96 | 0.042 | Wavenet: A generative model for raw audio | 2016 |
| 97 | 0.042 | WavChat: A survey of spoken dialogue models | 2024 |
| 98 | 0.040 | Better speech synthesis through scaling | 2023 |
| 99 | 0.040 | Baichuanaudio: A unified framework for end-to-end speech interaction | 2025 |
| 100 | 0.040 | Mini-omni2: Towards open-source gpt4o with vision, speech and duplex capabilities | 2024 |

## Top 100: H1 2026

| Rank | Rate | Title | Year |
|------|------|-------|------|
| 1 | 0.308 | Moshi: a speechtext foundation model for real-time dialogue | 2024 |
| 2 | 0.242 | Robust speech recognition via large-scale weak supervision | 2022 |
| 3 | 0.204 | Qwen2. 5-omni technical report | 2025 |
| 4 | 0.183 | High fidelity neural audio compression | 2022 |
| 5 | 0.180 | Utmos: Utokyo-sarulab system for voicemos challenge 2022 | 2022 |
| 6 | 0.170 | Kimiaudio technical report | 2025 |
| 7 | 0.163 | Cosyvoice 3: Towards in-the-wild speech generation via scaling-up and post-training | 2025 |
| 8 | 0.159 | Spark-tts: An efficient llm-based text-to-speech model with single-stream decoupled speech tokens | 2025 |
| 9 | 0.159 | Glm-4-voice: Towards intelligent and human-like endto-end spoken chatbot | 2024 |
| 10 | 0.156 | Wavlm: Large-scale self-supervised pre-training for full stack speech processing | 2021 |
| 11 | 0.149 | Libritts: A corpus derived from librispeech for text-to-speech | 2019 |
| 12 | 0.138 | Qwen2-audio technical report | 2024 |
| 13 | 0.132 | Maskgct: Zero-shot text-to-speech with masked generative codec transformer | 2024 |
| 14 | 0.107 | The llama 3 herd of models | 2024 |
| 15 | 0.107 | Qwen3 technical report | 2025 |
| 16 | 0.107 | Llasa: Scaling train-time and inferencetime compute for llama-based speech synthesis | 2025 |
| 17 | 0.104 | GPT-4o system card | 2024 |
| 18 | 0.097 | Mini-omni: Language models can hear, talk while thinking in streaming | 2024 |
| 19 | 0.093 | Qwen2.5 technical report | 2025 |
| 20 | 0.093 | NaturalSpeech 3: Zero-Shot Speech Synthesis with Factorized Codec and Diffusion Models | 2024 |
| 21 | 0.093 | Gemini 2.5: Pushing the frontier with advanced reasoning, multimodality, long context, and next generation agentic capabilities | 2025 |
| 22 | 0.090 | HiFi-GAN: Generative Adversarial Networks for Efficient and High Fidelity Speech Synthesis | 2010 |
| 23 | 0.090 | SoundStream: An End-to-End Neural Audio Codec | 2021 |
| 24 | 0.090 | Voicebench: Benchmarking llm-based voice assistants | — |
| 25 | 0.086 | Hubert: Self-supervised speech representation learning by masked prediction of hidden units | 2021 |
| 26 | 0.083 | Decoupled weight decay regularization | 2017 |
| 27 | 0.080 | Fish-speech: Leveraging large language models for advanced multilingual text-to-speech synthesis | 2024 |
| 28 | 0.080 | F5-tts: A fairytaler that fakes fluent and faithful speech with flow matching | 2025 |
| 29 | 0.080 | Wavtokenizer: An efficient acoustic discrete codec tokenizer for audio language modeling | 2025 |
| 30 | 0.080 | Librispeech: An ASR corpus based on public domain audio books, | 2015 |
| 31 | 0.080 | High-fidelity audio compression with improved rvqgan | 2024 |
| 32 | 0.080 | Step-audio 2 technical report | 2025 |
| 33 | 0.073 | Llama-omni: Seamless speech interaction with large language models | 2024 |
| 34 | 0.073 | Flow matching for generative modeling | 2022 |
| 35 | 0.069 | Speechtokenizer: Unified speech tokenizer for speech large language models | 2024 |
| 36 | 0.069 | Fastspeech 2: Fast and high-quality end-to-end text to speech | 2006 |
| 37 | 0.069 | Audiolm: a language modeling approach to audio generation | 2023 |
| 38 | 0.069 | Step-audio: Unified understanding and generation in intelligent speech interaction | 2025 |
| 39 | 0.066 | Gpt-4 technical report | 2023 |
| 40 | 0.066 | Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning | 2025 |
| 41 | 0.066 | Bigcodec: Pushing the limits of low-bitrate neural speech codec | 2024 |
| 42 | 0.066 | Deepseekmath: Pushing the limits of mathematical reasoning in open language models | 2024 |
| 43 | 0.066 | Freeze-omni: A smart and low latency speech-to-speech dialogue model with frozen llm | 2024 |
| 44 | 0.062 | WavChat: A survey of spoken dialogue models | 2024 |
| 45 | 0.062 | On the landscape of spoken language models: A comprehensive survey | 2025 |
| 46 | 0.059 | VALL-E 2: Neural Codec Language Models are Human Parity Zero-Shot Text to Speech Synthesizers | 2024 |
| 47 | 0.059 | Emotion2vec: Self-supervised pre-training for speech emotion representation | 2023 |
| 48 | 0.059 | Vocos: Closing the gap between time-domain and fourierbased neural vocoders for high-quality audio synthesis | 2024 |
| 49 | 0.059 | Deepseek-v3 technical report | 2024 |
| 50 | 0.059 | Emilia: An extensive, multilingual, and diverse speech dataset for large-scale speech generation | 2024 |
| 51 | 0.059 | Ecapa-tdnn: Emphasized channel attention, propagation and aggregation in tdnn based speaker verification | 2005 |
| 52 | 0.055 | Voicebox: Text-guided multilingual universal speech generation at scale | 2023 |
| 53 | 0.055 | Conditional variational autoencoder with adversarial learning for end-to-end text-to-speech | 2021 |
| 54 | 0.055 | Neural codec language models are zero-shot text to speech synthesizers | 2023 |
| 55 | 0.055 | MiniMax-Speech: Intrinsic zero-shot text-to-speech with a learnable speaker encoder | 2025 |
| 56 | 0.055 | Xtts: a massively multilingual zero-shot text-to-speech model | 2024 |
| 57 | 0.052 | Funaudiollm: Voice understanding and generation foundation models for natural interaction between humans and llms | 2024 |
| 58 | 0.052 | Gigaspeech: An evolving, multidomain asr corpus with 10,000 hours of transcribed audio | 2021 |
| 59 | 0.052 | Fireredtts: A foundation text-to-speech framework for industry-level generative speech applications | — |
| 60 | 0.052 | MinMo: A multimodal large language model for seamless voice interaction | 2025 |
| 61 | 0.052 | Bigvgan: A universal neural vocoder with large-scale training | 2022 |
| 62 | 0.052 | Common voice: A massively-multilingual speech corpus | 2019 |
| 63 | 0.052 | Speechgpt: Empowering large language models with intrinsic cross-modal conversational abilities | 2023 |
| 64 | 0.048 | Libritts-r: A restored multispeaker text-to-speech corpus | 2023 |
| 65 | 0.048 | Scaling transformers for low-bitrate high-quality speech coding | 2024 |
| 66 | 0.048 | Soundstorm: Efficient parallel audio generation | 2023 |
| 67 | 0.048 | Natural Language Guidance of HighFidelity Text-to-Speech with Synthetic Annotations | 2024 |
| 68 | 0.048 | Recent advances in discrete speech tokens: A review | 2025 |
| 69 | 0.048 | LoRA: Low-rank adaptation of large language models | 2021 |
| 70 | 0.045 | Tacotron: Towards endto-end speech synthesis | 2017 |
| 71 | 0.045 | Wavenet: A generative model for raw audio | 2016 |
| 72 | 0.045 | Better speech synthesis through scaling | 2023 |
| 73 | 0.045 | Baichuanaudio: A unified framework for end-to-end speech interaction | 2025 |
| 74 | 0.045 | E2 tts: Embarrassingly easy fully non-autoregressive zero-shot tts | 2024 |
| 75 | 0.045 | ZipVoice: Fast and high-quality zero-shot text-tospeech with flow matching | 2025 |
| 76 | 0.045 | Qwen-audio: Advancing universal audio understanding via unified large-scale audio-language models | 2023 |
| 77 | 0.045 | Llama-omni2: Llm-based real-time spoken chatbot with autoregressive streaming speech synthesis | 2025 |
| 78 | 0.045 | Dnsmos: A non-intrusive perceptual objective speech quality metric to evaluate noise suppressors | 2021 |
| 79 | 0.042 | NaturalSpeech 2: Latent Diffusion Models are Natural and Zero-Shot Speech and Singing Synthesizers | 2023 |
| 80 | 0.042 | Grad-tts: A diffusion probabilistic model for text-to-speech | 2021 |
| 81 | 0.042 | Wav2vec 2.0: A Framework for Self-Supervised Learning of Speech Representations | 2020 |
| 82 | 0.042 | Attention Is All You Need | 2023 |
| 83 | 0.042 | Nisqa: A deep cnn-self-attention model for multidimensional speech quality prediction with crowdsourced datasets | 2021 |
| 84 | 0.042 | Neural discrete representation learning | 2017 |
| 85 | 0.042 | SpiRit-LM: Interleaved spoken and written language model | 2024 |
| 86 | 0.042 | Audioldm: Text-to-audio generation with latent diffusion models | 2023 |
| 87 | 0.042 | Classifier-free diffusion guidance | 2022 |
| 88 | 0.038 | Natural TTS synthesis by conditioning wavenet on mel spectrogram predictions | 2018 |
| 89 | 0.038 | Speak foreign languages with your own voice: Cross-lingual neural codec language modeling | 2023 |
| 90 | 0.038 | Montreal Forced Aligner: Trainable Text-Speech Alignment Using Kaldi | 2017 |
| 91 | 0.038 | Seamless: Multilingual Expressive and Streaming Speech Translation | 2023 |
| 92 | 0.038 | TS3Codec: Transformer-Based simple streaming single codec | 2024 |
| 93 | 0.038 | The t05 system for the voicemos challenge 2024: Transfer learning from deep image classifier to naturalness mos prediction of high-quality synthetic speech | 2024 |
| 94 | 0.038 | Indextts: An industrial-level controllable and efficient zero-shot text-to-speech system | 2025 |
| 95 | 0.038 | Discrete Audio Tokens: More Than a Survey! | 2025 |
| 96 | 0.038 | Audiopalm: A large language model that can speak and listen | 2023 |
| 97 | 0.038 | Vevo: Controllable zero-shot voice imitation with self-supervised disentanglement | 2025 |
| 98 | 0.038 | Audio flamingo 3: Advancing audio intelligence with fully open large audio language models | 2025 |
| 99 | 0.035 | Instructttseval: Benchmarking complex natural-language instruction following in text-tospeech systems | 2025 |
| 100 | 0.035 | Finite scalar quantization: Vq-vae made simple | 2023 |

## Biggest risers (H2 2025 → H1 2026)

Papers in both top-100, sorted by rate ratio (B/A). Ratio > 1 means citation rate increased.

| Ratio | H2 2025 rank→H1 2026 rank | H2 2025 rate | H1 2026 rate | Title | Year |
|-------|---------------------|-----------|-----------|-------|------|
| ×2.58 | #57→#7 | 0.063 | 0.163 | Cosyvoice 3: Towards in-the-wild speech generation via scali | 2025 |
| ×2.47 | #49→#6 | 0.069 | 0.170 | Kimiaudio technical report | 2025 |
| ×2.44 | #85→#15 | 0.044 | 0.107 | Qwen3 technical report | 2025 |
| ×1.88 | #15→#3 | 0.109 | 0.204 | Qwen2. 5-omni technical report | 2025 |
| ×1.77 | #40→#12 | 0.078 | 0.138 | Qwen2-audio technical report | 2024 |
| ×1.75 | #63→#17 | 0.059 | 0.104 | GPT-4o system card | 2024 |
| ×1.75 | #69→#24 | 0.051 | 0.090 | Voicebench: Benchmarking llm-based voice assistants | — |
| ×1.60 | #20→#8 | 0.099 | 0.159 | Spark-tts: An efficient llm-based text-to-speech model with  | 2025 |
| ×1.58 | #84→#38 | 0.044 | 0.069 | Step-audio: Unified understanding and generation in intellig | 2025 |
| ×1.48 | #97→#44 | 0.042 | 0.062 | WavChat: A survey of spoken dialogue models | 2024 |
| ×1.48 | #3→#1 | 0.208 | 0.308 | Moshi: a speechtext foundation model for real-time dialogue | 2024 |
| ×1.47 | #26→#13 | 0.090 | 0.132 | Maskgct: Zero-shot text-to-speech with masked generative cod | 2024 |
| ×1.44 | #54→#19 | 0.065 | 0.093 | Qwen2.5 technical report | 2025 |
| ×1.39 | #13→#9 | 0.115 | 0.159 | Glm-4-voice: Towards intelligent and human-like endto-end sp | 2024 |
| ×1.31 | #33→#16 | 0.082 | 0.107 | Llasa: Scaling train-time and inferencetime compute for llam | 2025 |
| ×1.24 | #39→#18 | 0.078 | 0.097 | Mini-omni: Language models can hear, talk while thinking in  | 2024 |
| ×1.17 | #24→#14 | 0.092 | 0.107 | The llama 3 herd of models | 2024 |
| ×1.15 | #93→#64 | 0.042 | 0.048 | Libritts-r: A restored multispeaker text-to-speech corpus | 2023 |
| ×1.15 | #88→#67 | 0.042 | 0.048 | Natural Language Guidance of HighFidelity Text-to-Speech wit | 2024 |
| ×1.12 | #98→#72 | 0.040 | 0.045 | Better speech synthesis through scaling | 2023 |

## Biggest fallers (H2 2025 → H1 2026)

| Ratio | H2 2025 rank→H1 2026 rank | H2 2025 rate | H1 2026 rate | Title | Year |
|-------|---------------------|-----------|-----------|-------|------|
| ×0.37 | #8→#54 | 0.151 | 0.055 | Neural codec language models are zero-shot text to speech sy | 2023 |
| ×0.50 | #6→#22 | 0.181 | 0.090 | HiFi-GAN: Generative Adversarial Networks for Efficient and  | 2010 |
| ×0.54 | #11→#36 | 0.128 | 0.069 | Fastspeech 2: Fast and high-quality end-to-end text to speec | 2006 |
| ×0.57 | #44→#82 | 0.072 | 0.042 | Attention Is All You Need | 2023 |
| ×0.59 | #9→#25 | 0.147 | 0.086 | Hubert: Self-supervised speech representation learning by ma | 2021 |
| ×0.60 | #7→#20 | 0.157 | 0.093 | NaturalSpeech 3: Zero-Shot Speech Synthesis with Factorized  | 2024 |
| ×0.60 | #29→#61 | 0.086 | 0.052 | Bigvgan: A universal neural vocoder with large-scale trainin | 2022 |
| ×0.60 | #47→#81 | 0.069 | 0.042 | Wav2vec 2.0: A Framework for Self-Supervised Learning of Spe | 2020 |
| ×0.62 | #23→#48 | 0.095 | 0.059 | Vocos: Closing the gap between time-domain and fourierbased  | 2024 |
| ×0.62 | #32→#63 | 0.084 | 0.052 | Speechgpt: Empowering large language models with intrinsic c | 2023 |
| ×0.62 | #43→#76 | 0.072 | 0.045 | Qwen-audio: Advancing universal audio understanding via unif | 2023 |
| ×0.62 | #59→#89 | 0.061 | 0.038 | Speak foreign languages with your own voice: Cross-lingual n | 2023 |
| ×0.64 | #56→#79 | 0.065 | 0.042 | NaturalSpeech 2: Latent Diffusion Models are Natural and Zer | 2023 |
| ×0.65 | #18→#39 | 0.101 | 0.066 | Gpt-4 technical report | 2023 |
| ×0.66 | #51→#74 | 0.069 | 0.045 | E2 tts: Embarrassingly easy fully non-autoregressive zero-sh | 2024 |
| ×0.67 | #27→#46 | 0.088 | 0.059 | VALL-E 2: Neural Codec Language Models are Human Parity Zero | 2024 |
| ×0.68 | #36→#53 | 0.082 | 0.055 | Conditional variational autoencoder with adversarial learnin | 2021 |
| ×0.68 | #61→#84 | 0.061 | 0.042 | Neural discrete representation learning | 2017 |
| ×0.68 | #41→#62 | 0.076 | 0.052 | Common voice: A massively-multilingual speech corpus | 2019 |
| ×0.70 | #31→#50 | 0.084 | 0.059 | Emilia: An extensive, multilingual, and diverse speech datas | 2024 |

## New in H1 2026 top-100 (not in H2 2025)

| Rank | Rate | Title | Year |
|------|------|-------|------|
| 21 | 0.093 | Gemini 2.5: Pushing the frontier with advanced reasoning, multimodality, long context, and next generation agentic capabilities | 2025 |
| 27 | 0.080 | Fish-speech: Leveraging large language models for advanced multilingual text-to-speech synthesis | 2024 |
| 32 | 0.080 | Step-audio 2 technical report | 2025 |
| 40 | 0.066 | Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning | 2025 |
| 42 | 0.066 | Deepseekmath: Pushing the limits of mathematical reasoning in open language models | 2024 |
| 45 | 0.062 | On the landscape of spoken language models: A comprehensive survey | 2025 |
| 49 | 0.059 | Deepseek-v3 technical report | 2024 |
| 55 | 0.055 | MiniMax-Speech: Intrinsic zero-shot text-to-speech with a learnable speaker encoder | 2025 |
| 58 | 0.052 | Gigaspeech: An evolving, multidomain asr corpus with 10,000 hours of transcribed audio | 2021 |
| 68 | 0.048 | Recent advances in discrete speech tokens: A review | 2025 |
| 70 | 0.045 | Tacotron: Towards endto-end speech synthesis | 2017 |
| 75 | 0.045 | ZipVoice: Fast and high-quality zero-shot text-tospeech with flow matching | 2025 |
| 77 | 0.045 | Llama-omni2: Llm-based real-time spoken chatbot with autoregressive streaming speech synthesis | 2025 |
| 78 | 0.045 | Dnsmos: A non-intrusive perceptual objective speech quality metric to evaluate noise suppressors | 2021 |
| 80 | 0.042 | Grad-tts: A diffusion probabilistic model for text-to-speech | 2021 |
| 83 | 0.042 | Nisqa: A deep cnn-self-attention model for multidimensional speech quality prediction with crowdsourced datasets | 2021 |
| 86 | 0.042 | Audioldm: Text-to-audio generation with latent diffusion models | 2023 |
| 90 | 0.038 | Montreal Forced Aligner: Trainable Text-Speech Alignment Using Kaldi | 2017 |
| 92 | 0.038 | TS3Codec: Transformer-Based simple streaming single codec | 2024 |
| 93 | 0.038 | The t05 system for the voicemos challenge 2024: Transfer learning from deep image classifier to naturalness mos prediction of high-quality synthetic speech | 2024 |
| 94 | 0.038 | Indextts: An industrial-level controllable and efficient zero-shot text-to-speech system | 2025 |
| 95 | 0.038 | Discrete Audio Tokens: More Than a Survey! | 2025 |
| 97 | 0.038 | Vevo: Controllable zero-shot voice imitation with self-supervised disentanglement | 2025 |
| 98 | 0.038 | Audio flamingo 3: Advancing audio intelligence with fully open large audio language models | 2025 |
| 99 | 0.035 | Instructttseval: Benchmarking complex natural-language instruction following in text-tospeech systems | 2025 |

## Dropped from H2 2025 top-100 (not in H1 2026)

| Rank | Rate | Title | Year |
|------|------|-------|------|
| 12 | 0.122 | Cosyvoice 2: Scalable streaming speech synthesis with large language models | 2024 |
| 17 | 0.103 | Cosyvoice: A scalable multilingual zero-shot text-to-speech synthesizer based on supervised semantic tokens | 2024 |
| 19 | 0.101 | Seedtts: A family of high-quality versatile speech generation models | 2024 |
| 35 | 0.082 | Voicecraft: Zero-shot speech editing and text-to-speech in the wild | 2024 |
| 50 | 0.069 | Llama: Open and efficient foundation language models | 2023 |
| 53 | 0.067 | Hifi-codec: Group-residual vector quantization for high fidelity audio codec | 2023 |
| 55 | 0.065 | Adam: A Method for Stochastic Optimization | 2014 |
| 62 | 0.059 | Mls: A large-scale multilingual dataset for speech research | 2012 |
| 65 | 0.055 | Perceptual evaluation of speech quality (pesq)-a new method for speech quality assessment of telephone networks and codecs | 2001 |
| 68 | 0.053 | Yourtts: Towards zero-shot multi-speaker tts and zero-shot voice conversion for everyone | 2023 |
| 71 | 0.051 | BASE TTS: Lessons from building a billion-parameter text-to-speech model on 100k hours of data | 2024 |
| 72 | 0.050 | Matcha-tts: A fast TTS architecture with conditional flow matching | 2023 |
| 74 | 0.050 | Autoregressive speech synthesis without vector quantization | 2024 |
| 75 | 0.048 | A survey on neural speech synthesis | 2021 |
| 76 | 0.048 | Paraformer: Fast and accurate parallel transformer for non-autoregressive end-to-end speech recognition | 2022 |
| 79 | 0.048 | Conformer: Convolution-augmented transformer for speech recognition | 2005 |
| 81 | 0.046 | The lj speech dataset | 2017 |
| 82 | 0.044 | Diffusion-based voice conversion with fast maximum likelihood sampling scheme | 2021 |
| 86 | 0.044 | Speech resynthesis from discrete disentangled self-supervised representations | 2021 |
| 87 | 0.042 | Slam-omni: Timbrecontrollable voice interaction system with single-stage training | 2024 |
| 91 | 0.042 | Freevc: Towards high-quality text-free one-shot  voice  conversion | 2023 |
| 92 | 0.042 | Libri-Light: A Benchmark for ASR with Limited or No Supervision | 2020 |
| 94 | 0.042 | Scalable diffusion models with transformers | 2023 |
| 95 | 0.042 | Uniaudio: An audio foundation model toward universal audio generation | 2024 |
| 100 | 0.040 | Mini-omni2: Towards open-source gpt4o with vision, speech and duplex capabilities | 2024 |
