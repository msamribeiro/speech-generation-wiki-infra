# Review Queue

Borderline papers (relevance_score 0.40–0.70) awaiting manual decision.

After marking a decision below, update `status` in `raw/metadata/{id}.json`.

---

## 2409.07151 | Zero-Shot Text-to-Speech as Golden Speech Generator: A Systematic Framework and its Applicability in Automatic Pronunciation Assessment | arXiv | score: 0.45

**Authors:** Tien-Hong Lo, Meng-Ting Tsai, Yao-Ting Sung et al.
**Task guess:** [TTS]
**Reason for review:** ZS-TTS is used as a tool to generate learner-specific "golden speech" for L2 pronunciation assessment, but the paper's primary contribution is the pronunciation assessment framework, not advancement of TTS methods. It is ambiguous whether the systematic evaluation of ZS-TTS quality for this downstream use is a synthesis contribution.
**Abstract excerpt:** Second language (L2) learners can improve their pronunciation by imitating golden speech, especially when the speech that aligns with their respective speech characteristics. This study explores the hypothesis that learner-specific golden speech generated with zero-shot text-to-speech (ZS-TTS) techniques can be harnessed as an effective metric for measuring the pronunciation proficiency of L2 learners.

**Decision:** [ ] accept  [x] reject  [ ] accept-partial (note: _________)

---

## 2505.06671 | RADE: A Neural Codec for Transmitting Speech over HF Radio Channels | arXiv | score: 0.40

**Authors:** David Rowe, Jean-Marc Valin
**Task guess:** [codec]
**Reason for review:** Technically a neural codec that encodes/decodes speech, but the application is HF radio channel transmission rather than speech synthesis infrastructure. The codec design objectives (robustness to channel errors, low-bitrate transmission) are quite different from speech-generation codecs (reconstruction quality, semantic richness). Relevance depends on scope interpretation.
**Abstract excerpt:** Speech compression is commonly used to send voice over radio channels in applications such as mobile telephony and two-way push-to-talk (PTT) radio. In classical systems, the speech codec is combined with forward error correction, modulation and radio hardware.

**Decision:** [ ] accept  [x] reject  [ ] accept-partial (note: _________)

---

## 2506.23049 | AURA: Agent for Understanding, Reasoning, and Automated Tool Use in Voice-Driven Tasks | arXiv | score: 0.48

**Authors:** Leander Melroy Maben, Gayathri Ganesh Lakshmy, Srijith Radhakrishnan et al.
**Task guess:** [SCA]
**Reason for review:** Introduces an open-source speech-native agentic assistant (AURA) using a cascaded ASR+LLM+TTS pipeline with multi-turn dialogue and tool use. The primary contribution is agentic reasoning and tool invocation, not speech synthesis; TTS is a black-box component. Whether this qualifies as advancing SCA systems depends on scope — it is a full-duplex speech interface but does not study synthesis quality.
**Abstract excerpt:** Despite advances in language and speech technologies, no open-source system enables full speech-to-speech, multi-turn dialogue with integrated tool use and agentic reasoning. We introduce AURA (Agent for Understanding, Reasoning, and Automated Tool Use), the first open-source, speech-native assistant capable of completing complex, goal-driven tasks through dynamic tool invocation and multi-turn conversation.

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2507.03887 | Traceable TTS: Toward Watermark-Free TTS with Strong Traceability | arXiv | score: 0.45

**Authors:** Yuxiang Zhao, Yunchong Xiao, Yushen Chen et al.
**Task guess:** [TTS]
**Reason for review:** Proposes a TTS system with built-in traceability (fingerprinting at generation time) to track synthesized speech without explicit watermarks. The paper builds a full TTS model but the primary novelty is the traceability/security mechanism. It is ambiguous whether the synthesis quality contributions are substantial enough to warrant inclusion.
**Abstract excerpt:** Recent advances in Text-To-Speech (TTS) technology have enabled synthetic speech to mimic human voices with remarkable realism, raising significant security concerns. This underscores the need for traceable TTS models-systems capable of tracing their synthesized speech without compromising quality or security.

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2507.06235 | Super Kawaii Vocalics: Amplifying the "Cute" Factor in Computer Voice | arXiv | score: 0.50

**Authors:** Yuto Mandai, Katie Seaborn, Tomoyasu Nakano et al.
**Task guess:** [TTS]
**Reason for review:** Studies what acoustic elements constitute "kawaii" (cute) voice and explores both manual and automatic voice manipulation to amplify these properties. Advances understanding of voice style and automatic voice transformation, but the primary framing is perceptual/HCI research. Whether automatic kawaii voice manipulation counts as VC/TTS prosody research is ambiguous.
**Abstract excerpt:** "Kawaii" is the Japanese concept of cute, which carries sociocultural connotations related to social identities and emotional responses. Yet, virtually all work to date has focused on the visual side of kawaii, including in studies of computer agents and social robots.

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2507.08530 | MIDI-VALLE: Improving Expressive Piano Performance Synthesis Through Neural Codec Language Modelling | arXiv | score: 0.45

**Authors:** Jingjing Tang, Xin Wang, Zhe Zhang et al.
**Task guess:** [TTS]
**Reason for review:** Directly applies VALL-E-style neural codec language modeling (a core TTS architecture) to piano performance synthesis. The method transfer is direct and technically relevant, but the domain is music (piano audio), not speech. Relevance depends on whether the wiki scope includes music synthesis that uses speech-generation architectures.
**Abstract excerpt:** Generating expressive audio performances from music scores requires models to capture both instrument acoustics and human interpretation. Traditional music performance synthesis pipelines follow a two-stage approach, first generating expressive performance MIDI from a score, then synthesising the MIDI into audio.

**Decision:** [ ] accept  [x] reject  [ ] accept-partial (note: _________)

---

## 2507.09282 | ClaritySpeech: Dementia Obfuscation in Speech | arXiv | score: 0.55

**Authors:** Dominika Woszczyk, Ranya Aloufi, Soteris Demetriou
**Task guess:** [TTS]
**Reason for review:** Integrates ZS-TTS to correct dementia-affected speech while preserving speaker identity — the TTS component is central to the pipeline and must preserve naturalness and speaker similarity. However, the primary contribution is dementia obfuscation/privacy, not TTS advancement. The paper does evaluate TTS quality for atypical speech, which could contribute to evaluation methodology.
**Abstract excerpt:** Dementia, a neurodegenerative disease, alters speech patterns, creating communication barriers and raising privacy concerns. Current speech technologies, such as automatic speech transcription (ASR), struggle with dementia and atypical speech, further challenging accessibility.

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2507.10985 | Pronunciation Deviation Analysis Through Voice Cloning and Acoustic Comparison | arXiv | score: 0.45

**Authors:** Andrew Valdivia, Yueming Zhang, Hailu Xu et al.
**Task guess:** [TTS]
**Reason for review:** Uses voice cloning to generate a correctly-pronounced reference utterance in the user's own voice, then detects mispronunciations by comparing acoustic deviation. Voice cloning is an enabling component but the paper's contribution is mispronunciation detection methodology, not synthesis. The voice cloning evaluation could have incidental TTS relevance.
**Abstract excerpt:** This paper presents a novel approach for detecting mispronunciations by analyzing deviations between a user's original speech and their voice-cloned counterpart with corrected pronunciation. We hypothesize that regions with maximal acoustic deviation between the original and cloned utterances indicate potential mispronunciations.

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2507.19202 | Latent Granular Resynthesis using Neural Audio Codecs | arXiv | score: 0.45

**Authors:** Nao Tokui, Tom Baker
**Task guess:** [codec]
**Reason for review:** Uses neural audio codecs for creative audio resynthesis (granular synthesis in latent space); the technique is novel and codec-adjacent, but the primary application domain is creative music/audio art rather than TTS, VC, or foundational codec design for speech synthesis pipelines.
**Abstract excerpt:** We introduce a novel technique for creative audio resynthesis that operates by reworking the concept of granular synthesis at the latent vector level. Our approach creates a "granular codebook" by encoding a source audio corpus into latent vector segments, then matches each latent grain of a target audio signal to its closest counterpart in the codebook.

**Decision:** [ ] accept  [x] reject  [ ] accept-partial (note: _________)

---

## 2510.07881 | CS3-Bench: Evaluating and Enhancing Speech-to-Speech LLMs for Mandarin-English Code-Switching | arXiv | score: 0.60

**Authors:** Heyang Liu, Yuhao Wang, Ziyang Cheng et al.
**Task guess:** [SCA, evaluation]
**Reason for review:** CS3-Bench evaluates Mandarin-English code-switching in speech-to-speech LLMs and covers speech output quality, but the primary focus is language alignment and code-switching behaviour rather than advancing speech synthesis methodology per se.
**Abstract excerpt:** The advancement of multimodal large language models has accelerated the development of speech-to-speech interaction systems. While natural monolingual interaction has been achieved, we find existing models exhibit deficiencies in language alignment.

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2511.08230 | VocalBench-zh: Decomposing and Benchmarking the Speech Conversational Abilities in Mandarin Context | arXiv | score: 0.65

**Authors:** Heyang Liu, Ziyang Cheng, Yuhao Wang et al.
**Task guess:** [SCA, evaluation]
**Reason for review:** VocalBench-zh introduces a Mandarin S2S evaluation benchmark covering speech conversational abilities — relevant as evaluation infrastructure for systems that generate speech, but it is ambiguous whether the decomposition of speech conversational abilities primarily advances synthesis evaluation or broader speech understanding evaluation.
**Abstract excerpt:** The development of multi-modal large language models (LLMs) leads to intelligent approaches capable of speech interactions. As one of the most widely spoken languages globally, Mandarin is supported by most models to enhance their applicability and reach.

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2601.13742 | Hearing Between the Lines: Unlocking the Reasoning Power of LLMs for Speech Evaluation | arXiv | score: 0.68

**Authors:** Arjun Chandra, Kevin Miller, Venkatesh Ravichandran et al.
**Task guess:** [SCA, evaluation]
**Reason for review:** TRACE proposes a framework enabling LLM judges to reason over audio cues for S2S evaluation — the evaluation methodology is relevant to assessing speech output quality, but the core contribution is about LLM judging infrastructure rather than advancing synthesis itself. The boundary between evaluation-of-synthesis and evaluation-of-understanding is ambiguous here.
**Abstract excerpt:** Large Language Model (LLM) judges exhibit strong reasoning capabilities but are limited to textual content. This leaves current automatic Speech-to-Speech (S2S) evaluation methods reliant on opaque and expensive Audio Language Models (ALMs).

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2605.27190 | Learning When to Think While Listening in Large Audio-Language Models | arXiv | score: 0.42

**Authors:** Zhiyuan Song, Weici Zhao, Yang Xiao et al.
**Task guess:** [SCA]
**Reason for review:** Introduces a wait-think-answer control mechanism for streaming audio LLMs — this is relevant to real-time SCA responsiveness but the primary contribution is reasoning latency control in audio LLMs rather than advancing speech synthesis or generation quality.
**Abstract excerpt:** Recent advances in Large Audio-Language Models (LALMs) have made real-time, streaming spoken interaction increasingly practical. In this setting, reasoning quality and responsiveness are tightly coupled: delaying reasoning until the speech endpoint can improve answer quality but moves deliberation into user-visible response delay.

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2605.27772 | Do Audio LLMs Listen or Read? Analyzing and Mitigating Paralinguistic Failures with VoxParadox | arXiv | score: 0.50

**Authors:** Jiacheng Pang, Ashutosh Chaubey, Mohammad Soleymani
**Task guess:** [evaluation]
**Reason for review:** VoxParadox uses controlled TTS synthesis to construct adversarial examples testing paralinguistic understanding in audio LLMs — TTS is a construction tool rather than the object of study; the question is whether paralinguistic evaluation benchmarks that depend on TTS methodology count as synthesis-adjacent contributions.
**Abstract excerpt:** Audio large language models (Audio LLMs) demonstrate strong performance on speech understanding tasks, yet their ability to understand paralinguistic information remains limited. To systematically quantify this issue, we introduce VoxParadox, an adversarial benchmark with 2,000 verified examples, spanning 10 paralinguistic tasks, created with controlled speech synthesis.

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2605.27984 | KVoiceBench, KOpenAudioBench, and KMMAU: Agent-Driven Korean Speech Benchmarks for Evaluating SpeechLMs | arXiv | score: 0.58

**Authors:** Haechan Kim, Seungjun Chung, Inkyu Park et al.
**Task guess:** [evaluation]
**Reason for review:** Introduces Korean-language speech benchmarks for SpeechLMs using TTS for benchmark construction — the primary contribution is multilingual SpeechLM evaluation infrastructure; relevance depends on whether SpeechLM evaluation benchmarks that explicitly address speech output quality are in scope.
**Abstract excerpt:** Speech language models (SpeechLMs) have achieved substantial progress by extending large language models (LLMs) to the speech modality. However, SpeechLM evaluation remains heavily centered on English, limiting reliable assessment of multilingual speech capabilities.

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2605.30107 | Dial HEALTHDIAL for Advice: A Multilingual and Multi-Parallel Spoken Dialogue Dataset for Knowledge-Grounded Information Seeking | arXiv | score: 0.40

**Authors:** Songbo Hu, Yinhong Liu, Ej Zhou et al.
**Task guess:** [SCA]
**Reason for review:** HEALTHDIAL is a multilingual spoken dialogue dataset where TTS was used for data construction — borderline because the dataset could serve as training/evaluation data for spoken dialogue systems that generate speech, but the paper's contribution is the dataset methodology and RAG framework, not synthesis advancement.
**Abstract excerpt:** Creating spoken dialogue datasets is methodologically challenging, and these challenges are amplified when the goal is to build multilingual, multi-parallel datasets at scale. This work introduces HEALTHDIAL, a large-scale, multilingual, and multi-parallel dataset for developing and evaluating retrieval-augmented generation (RAG)-based spoken dialogue systems.

**Decision:** [ ] accept  [x] reject  [ ] accept-partial (note: _________)

---

## 2605.26136 | Eroding Trust in Real Speech: A Large-Scale Study of Human Audio Deepfake Perception | arXiv | score: 0.65

**Authors:** Nicolas M. Müller, Wei Herng Choong
**Task guess:** evaluation
**Reason for review:** TTS systems used to generate deepfake stimuli; contribution is human perception/detection study, not synthesis methodology. Borderline — accept if perception of synthesised speech quality is considered in-scope evaluation.
**Abstract excerpt:** Audio deepfakes have improved rapidly recently, yet their effect on human trust in real speech remains unstudied. We present the largest listening study on audio deepfake perception to date, collecting 35,532 judgments from 1,768 participants across ...

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________)

---
## iclr-2026-GNo1qMqgPD | VoxPrivacy: A Benchmark for Evaluating Interactional Privacy of Speech Language Models | ICLR | score: 0.55

**Authors:** Yuxiang Wang, HongYu Liu, Dekun Chen et al.
**Task guess:** ['SCA', 'evaluation']
**Reason for review:** VoxPrivacy evaluates whether SLMs can distinguish between users and manage information flow appropriately in shared environments. The benchmark indirectly requires speaker-aware response generation, but the primary contribution is SLM safety/privacy evaluation — it is ambiguous whether this qualifies as a synthesis evaluation contribution under the wiki scope.
**Abstract excerpt:** As Speech Language Models (SLMs) transition from personal devices to shared, multi-user environments such as smart homes, a new challenge emerges: the model is expected to distinguish between users to manage information flow appropriately.

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## iclr-2026-l5re5ppqrX | EchoMind: An Interrelated Multi-level Benchmark for Evaluating Empathetic Speech Language Models | ICLR | score: 0.65

**Authors:** Li Zhou, Lutong Yu, You Lyu et al.
**Task guess:** ['SCA', 'evaluation']
**Reason for review:** EchoMind is a multi-level SLM benchmark that evaluates both perception and response generation (including expressive spoken response quality). The benchmark does include evaluation of generated speech responses, but it is unclear whether the synthesis evaluation dimension is substantial enough to qualify as an evaluation-contribution in scope.
**Abstract excerpt:** Speech Language Models (SLMs) have made significant progress in spoken language understanding. Yet it remains unclear whether they can fully perceive non-lexical vocal cues alongside spoken words, and respond with empathy that aligns with both emotional and contextual factors.

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## iclr-2026-wbttgzp7MT | EmotionThinker: Prosody-Aware Reinforcement Learning for Explainable Speech Emotion Reasoning | ICLR | score: 0.45

**Authors:** Dingdong WANG, Shujie LIU, Tianhua Zhang et al.
**Task guess:** []
**Reason for review:** EmotionThinker reformulates speech emotion recognition as a reasoning problem using RL with prosody-aware rewards. The prosody awareness and use of SpeechLLMs creates a tangential connection to synthesis, but the primary contribution is to SER/emotion understanding — ambiguous whether it informs emotion-conditioned TTS.
**Abstract excerpt:** Emotional information in speech plays a unique role in multimodal perception. However, current Speech Large Language Models (SpeechLLMs), similar to conventional speech emotion recognition (SER) systems, still treat emotion understanding as a simple classification problem.

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## neurips-2025-8PUzLga3lU | VITA-1.5: Towards GPT-4o Level Real-Time Vision and Speech Interaction | NeurIPS | score: 0.48

**Authors:** Chaoyou Fu, Haojia Lin, Xiong Wang et al.
**Task guess:** ['SCA']
**Reason for review:** VITA-1.5 integrates vision and speech in a real-time multimodal LLM and includes speech output generation. However, the speech synthesis method is not the primary focus — it is one capability among several, and the contribution is primarily about multi-stage vision-language-speech alignment. Borderline because real-time speech interaction output is architecturally non-trivial.
**Abstract excerpt:** Recent Multimodal Large Language Models (MLLMs) have typically focused on integrating visual and textual modalities, with less emphasis placed on the role of speech in enhancing interaction. However, speech plays a crucial role in multimodal dialogue systems.

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2025.clicit-1.81 | FAMA: The First Large-Scale Open-Science Speech Foundation Model for English and Italian | workshop (CLiC-it 2025) | score: 0.50

**Authors:** Sara Papi, Marco Gaido, Luisa Bentivogli et al.
**Task guess:** []
**Reason for review:** Was ingested by mistake this session (2026-07-05) before full-text review caught the scope issue; ingest was reverted and status reset to `review`. FAMA is a pure open-science ASR/speech-translation foundation model (trained and evaluated only on WER/COMET); its own keywords list is "automatic speech recognition, speech translation, ASR, ST" with no mention of TTS, VC, or SCA. No generative speech component of any kind. Almost certainly out of scope for a TTS/VC/SCA-focused wiki, but flagging for an explicit reject decision rather than assuming, since the corpus does track some adjacent infrastructure (codecs, evaluation tooling) that isn't itself generative.
**Abstract excerpt:** The development of speech foundation models (SFMs) like Whisper and SeamlessM4T has significantly advanced the field of speech processing. However, their closed nature—with inaccessible training data and code—poses major reproducibility and fair evaluation challenges. ... we introduce FAMA, the first family of open science SFMs for English and Italian, trained on 150k+ hours of OS speech data.

**Decision:** [ ] accept  [x] reject  [ ] accept-partial (note: _________)

---

## neurips-2025-vhPy3NMsO5 | OmniResponse: Online Multimodal Conversational Response Generation in Dyadic Interactions | NeurIPS | score: 0.58

**Authors:** Cheng Luo, Jianghui Wang, Bing Li et al.
**Task guess:** ['SCA']
**Reason for review:** OmniResponse generates synchronized verbal (audio) and non-verbal (facial) listener responses online; the spoken audio generation component is real and architecturally described, but the primary novelty is the multimodal dyadic interaction task framing rather than advancing speech synthesis methods specifically.
**Abstract excerpt:** In this paper, we introduce Online Multimodal Conversational Response Generation (OMCRG), a novel task designed to produce synchronized verbal and non-verbal listener feedback online, based on the speaker's multimodal inputs.

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2509.13785 | Summary on The Multilingual Conversational Speech Language Model Challenge: Datasets, Tasks, Baselines, and Methods | arXiv | score: 0.85

**Authors:** Bingshen Mu, Pengcheng Guo, Zhaokai Sun et al.
**Task guess:** []
**Reason for review:** Was ingested this session (2026-07-13) before full-text review caught the scope issue; ingest was reverted and status reset directly to `rejected` (user read the PDF and confirmed the same session). This is a pure multilingual ASR + speaker-diarization challenge summary (MLC-SLM): both defined tasks (Task 1 ASR, Task 2 joint diarization+recognition) are evaluated only on MER/tcpMER, WER/CER variants. No TTS, VC, or any speech-generation component anywhere in the paper — the "speech LLM" baselines only transcribe, they never synthesize audio. Same scope pattern as FAMA (2025.clicit-1.81): a filter-stage false accept (relevance_score 0.85) on a paper whose "speech LLM"/"SLLM" framing reads as generative but is comprehension-only.
**Abstract excerpt:** This paper summarizes the Interspeech2025 Multilingual Conversational Speech Language Model (MLC-SLM) challenge, which aims to advance the exploration of building effective multilingual conversational speech LLMs (SLLMs). We provide a detailed description of the task settings for the MLC-SLM challenge, the released real-world multilingual conversational speech dataset totaling approximately 1,604 hours, and the baseline systems for participants.

**Decision:** [ ] accept  [x] reject  [ ] accept-partial (note: _________)

---

## 2510.03111 | Evaluation of preprocessing pipelines in the creation of in-the-wild TTS datasets | arXiv | score: 0.65

**Authors:** Matías Di Bernardo, Emmanuel Misley, Ignacio Correa, Mateo García Iacovelli, Simón Mellino, Gala Lucía Gonzalez Barrios
**Task guess:** [TTS, evaluation]
**Reason for review:** Caught at ingest time (2026-07-17, Q4 session 14 batch 3) before any page was written. The paper's own three stated contributions (§1) are: a preprocessing-pipeline evaluation methodology "independent of any specific TTS system," a low-cost CPU-friendly preprocessing chain (VAD, denoising, quality filtering, STT), and a new raw Argentine Spanish audio collection. No TTS model is trained or evaluated anywhere in the paper — all reported metrics (PESQ, SI-SDR, SNR, T30, C50, F0-STD, MCD) are signal/audio-quality metrics computed on raw vs. processed recordings, not on synthesized speech. The authors explicitly defer TTS training/evaluation to future work (§5, Limitations and Future Work: "We plan to measure the correlation between the composite score and TTS outcomes by training representative TTS models..."). Same scope pattern as FAMA and the MLC-SLM challenge summary: "TTS" in the title/task tag is not itself evidence of a generative component. The original `relevance_note` at filter time already flagged this ambiguity ("synthesis is the end goal but pipeline evaluation is primary").
**Abstract excerpt:** This work introduces a reproducible, metric-driven methodology to evaluate preprocessing pipelines for in-the-wild TTS corpora generation. We apply a custom low-cost pipeline to the first in-the-wild Argentine Spanish collection and compare 24 pipeline configurations combining different denoising and quality filtering variants. Evaluation relies on complementary objective measures (PESQ, SI-SDR, SNR), acoustic descriptors (T30, C50), and speech-preservation metrics (F0-STD, MCD). Results expose trade-offs between dataset size, signal quality, and voice preservation; where denoising variants with permissive filtering provide the best overall compromise for our testbed. The proposed methodology allows selecting pipeline configurations without training TTS models for each subset, accelerating and reducing the cost of preprocessing development for low-resource settings.

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________) — user accepted despite no trained TTS model; preprocessing methodology judged valuable infrastructure for the field (2026-07-17)

---

## 2510.07978 | VoiceAgentBench: Are Voice Assistants ready for agentic tasks? | arXiv | score: 0.72

**Authors:** Dhruv Jain, Harshit Shukla, Gautam Rajeev, Ashish Kulkarni, Chandra Khatri, Shubham Agarwal
**Task guess:** [SCA, evaluation]
**Reason for review:** Caught at ingest time (2026-07-18, Q4 session 14). All four evaluation metrics (Tool Selection, Tool Call Structure, Parameter Filling, Refusal Rate — §3.2, Tables 2-4) score text/structured tool-call correctness against the model's spoken query; none evaluate generated speech quality, naturalness, or any acoustic characteristic. TTS/VC (ElevenLabs, Coqui-TTS, Krutrim-TTS) is used only to construct the benchmark's input audio, including a speaker-diversity sampling ablation (§3.1.2) and a vendor-selection MOS pilot (Appendix I) — neither is evaluated as a research contribution in its own right. Structurally identical in scope-relevance to the AURA entry above (agentic reasoning/tool-use primary, TTS/VC incidental to the voice interface).
**Abstract excerpt:** Large scale Speech Language Models have enabled voice assistants capable of understanding natural spoken queries and performing complex tasks. However, existing speech benchmarks largely focus on isolated capabilities such as transcription or question answering and do not systematically evaluate agentic behavior or adversarial robustness. To address this, we introduce VOICEAGENTBENCH, a comprehensive benchmark for evaluating SpeechLMs in realistic spoken agentic settings, comprising 6,000+ synthetic spoken queries spanning single-tool invocations, multi-tool workflows, multi-turn dialogue, and safety evaluations across English and six Indic languages.

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________) — user accepted following the AURA precedent (2026-07-18): same shape (agentic tool-use primary, TTS/VC incidental), treated consistently as in-scope SCA-adjacent evaluation work

---

## 2510.09424 | The Speech-LLM Takes It All: A Truly Fully End-to-End Spoken Dialogue State Tracking Approach | arXiv | score: 0.55

**Authors:** Nizar El Ghazal, Antoine Caubrière, Valentin Vielzeuf
**Task guess:** [SCA]
**Reason for review:** Caught at ingest time (2026-07-18). This is a Spoken Dialog State Tracking (DST) paper: a speech encoder + connector + LLM (with optional attention-pooling context-compression module) consumes a full spoken multi-turn dialogue and autoregressively emits a structured JSON of slot-value pairs, evaluated via Joint Goal Accuracy on SpokenWOZ. There is no TTS, no VC, no synthesized spoken output anywhere in the paper — the sole generative step is the LLM emitting a JSON string. Structurally matches the FAMA (2025.clicit-1.81) / MLC-SLM (2509.13785) reject pattern: an "understanding task wearing speech-LLM terminology," where "speechLLM"/"E2E" framing reads as generative but the task itself is comprehension/tracking, not generation. This is a distinct pattern from the AURA/VoiceAgentBench precedent above, which involved incidental TTS/VC used to construct a benchmark's input audio for an agentic tool-use task; here there is no TTS/VC component anywhere in the pipeline, incidental or otherwise.
**Abstract excerpt:** This paper presents a comparative study of context management strategies for end-to-end Spoken Dialog State Tracking using Speech-LLMs. We systematically evaluate traditional multimodal context (combining text history and spoken current turn), full spoken history, and compressed spoken history approaches. Our experiments on the SpokenWOZ corpus demonstrate that providing the full spoken conversation as input yields the highest performance among models of similar size, significantly surpassing prior methods.

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________) — user explicitly overrode the scope concern and accepted anyway (2026-07-18), citing architectural/methodological relevance (context management for long spoken multi-turn input into an LLM) despite the paper having no generative speech output. Logged as a one-off scope-override decision, not a new precedent: does not authorize accepting future DST/understanding-only papers by default; each should still be evaluated against the FAMA/MLC-SLM pattern on its own merits.

---

## 2510.12116 | Understanding the Modality Gap: An Empirical Study on the Speech-Text Alignment Mechanism of Large Speech Language Models | EMNLP | score: 0.82

**Authors:** (see raw/metadata/2510.12116.json)
**Task guess:** [SCA]
**Reason for review:** Caught at ingest time (2026-07-18, Q4 session 15, batch 3), before any page was written. The LSLM under study only ever outputs text — §3.1 states it "enabl[es] autoregressive generation of textual responses," and all evaluation is on VoiceBench QA-accuracy subsets (AdvBench, IFEval, OBQA, MMSU, sd-qa). No TTS, VC, speech-to-speech, or any spoken-output quality metric appears anywhere in the paper (checked Table 1, §3–§5, Limitations). The paper's actual contribution is a representation-similarity analysis of why speech-input QA accuracy lags text-input QA accuracy in speech-text LLMs, plus inference-time embedding interventions to close that gap — pure speech *comprehension* research. This is a cleaner match to the FAMA/MLC-SLM reject pattern than 2510.09424 was: unlike that DST case (which at least produces a structured dialogue-state output as part of a spoken-dialogue-agent pipeline), this paper has no spoken-output component of any kind, incidental or otherwise.
**Abstract excerpt:** (see raw/metadata/2510.12116.json for full abstract)

**Decision:** [ ] accept  [x] reject  [ ] accept-partial (note: _________) — user confirmed reject (2026-08-02), consistent with the FAMA/MLC-SLM/2507.14815/2511.22503 precedent: pure speech-comprehension representation analysis with no TTS/VC/spoken-output component anywhere in the paper. Left pending since 2026-07-18 before this final decision.

---

## 2507.14815 | FastLongSpeech: Enhancing Large Speech-Language Models for Efficient Long-Speech Processing | arXiv (NeurIPS 2025) | score: 0.72

**Authors:** Shoutao Guo, Shaolei Zhang, Qingkai Fang, Zhengrui Ma, Min Zhang, Yang Feng
**Task guess:** [SCA]
**Reason for review:** Caught at ingest time (2026-07-27, Q4 session 16), before any page was written. FastLongSpeech extends Qwen2-Audio with a speech extractor ("iterative fusion" compression, §3.2) and a two-stage training recipe (CTC content-density training + dynamic compression training, §3.3) so the LLM can consume long audio inputs more cheaply, but the system's own output is always text (§2 Eq. 1, reused unchanged in §3.1). Every benchmark scores text or label outputs — Short/Long-Speech Spoken QA (including the paper's own LongSpeech-Eval, §3.4), Spoken Dialogue Understanding (AIR-Bench), Emotion Recognition (MELD), ASR (LibriSpeech/GigaSpeech WER), and Speech Information Retrieval (SPIRAL-H) — never generated speech. The only TTS mention (the third-party "Orca" model, §3.4/Appendix A) synthesizes input audio for constructing the LongSpeech-Eval benchmark, not model output. Clean match to the FAMA/MLC-SLM/2510.12116 reject pattern — no spoken output anywhere, not even incidental.
**Abstract excerpt:** (see raw/metadata/2507.14815.json for full abstract)

**Decision:** [ ] accept  [x] reject  [ ] accept-partial (note: _________) — user confirmed reject (2026-07-27), consistent with the FAMA/MLC-SLM/2510.12116 precedent.

---

## 2511.22503 | Joint Speech and Text Training for LLM-Based End-to-End Spoken Dialogue State Tracking | arXiv (submitted to ICASSP 2026) | score: 0.55

**Authors:** Katia Vendrame, Bolaji Yusuf, Santosh Kesiraju, Šimon Sedláček, Oldřich Plchot, Jan Černocký
**Task guess:** [SCA]
**Reason for review:** Caught at ingest time (2026-07-30, Q4 session 18 continuation), before any page was written. A second instance of the exact 2510.09424 DST shape: a speech encoder (WavLM) + Transformer connector + LLM (Gemma-3/OLMo-1B) with LoRA adapters consumes the current spoken turn plus text dialogue history and emits a single JSON string (ASR transcript + dialogue-state slot-value pairs). This paper's own contribution is a parallel text encoder (sharing the connector/LoRA parameters) so the model can also train on unpaired written DST data for domains with no paired speech, discarded at inference — inference remains speech-in/JSON-out, identical to the baseline it builds on (Sedláček et al. 2025, likely the same Brno University of Technology research line as 2510.09424). Sole metric is Joint Goal Accuracy (SpokenWOZ/MultiWOZ-style fuzzy slot matching) — no speech-quality metric anywhere, since nothing is generated in the speech modality. Structurally identical to the FAMA/MLC-SLM/2510.09424 reject pattern.
**Abstract excerpt:** End-to-end spoken dialogue state tracking (DST) is made difficult by the tandem of having to handle speech input and data scarcity. Combining speech foundation encoders and large language models has been proposed in recent work as to alleviate some of this difficulty... in this work, we propose jointly training on available spoken DST data and written textual data from other domains as a way to achieve cross-domain generalization.

**Decision:** [ ] accept  [x] reject  [ ] accept-partial (note: _________) — user confirmed reject (2026-07-30). The 2510.09424 accept was explicitly logged as a one-off override, not a new precedent, so this second same-shape paper was evaluated fresh against the FAMA/MLC-SLM pattern rather than auto-accepted; no speech generation anywhere in the pipeline.

---

## 2025.findings-emnlp.716 | Mitigating Sequential Dependencies: A Survey of Algorithms and Systems for Generation-Refinement Frameworks in Autoregressive Models | EMNLP | score: 0.45

**Authors:** Yunhai Hu, Zining Liu, Zhenyuan Dong, Tianfan Peng, Bradley McDanel, Sai Qian Zhang
**Task guess:** [TTS]
**Reason for review:** Caught at ingest time (2026-07-27, Q4 session 16), before any page was written. This is a general survey of speculative decoding / generation-refinement frameworks for autoregressive models. Its substantive content (§3–6, the bulk of the survey) covers text/LLM decoding techniques exclusively (draft-model taxonomy, tree-based verification, iterative Jacobi/Gauss-Seidel decoding, distributed/hardware system optimizations). Speech-domain content is confined to two sentences in §7.2 ("Speculative Decoding for Multimodal Output Generation"), citing only two speech papers (VADUSA, a speech-LLaMA multi-token-prediction paper) out of 100+ total references. No dedicated speech section, no speech-specific taxonomy branch, no original speech experiment. Subject-matter relevance to TTS/VC/SCA is negligible relative to the survey's actual scope (general AR-model inference acceleration), not a scope exception like the TTS-preprocessing or AURA/VoiceAgentBench precedents.
**Abstract excerpt:** (see raw/metadata/2025.findings-emnlp.716.json for full abstract)

**Decision:** [ ] accept  [x] reject  [ ] accept-partial (note: _________) — user reviewed the paper directly (title/authors/URL provided) and confirmed reject (2026-07-27).

---

## 2512.16832 | What Do Prosody and Text Convey? Characterizing How Meaningful Information is Distributed Across Multiple Channels | arXiv | score: 0.55

**Authors:** Aditya Yadavalli, Tiago Pimentel, Tamar I Regev, Ethan Wilcox, Alex Warstadt
**Task guess:** [evaluation]
**Reason for review:** Caught at ingest time (2026-08-02, Q4 session 20 continuation), before any page was written. This is an information-theoretic linguistics paper: it fine-tunes existing classifiers (GPT-2 on text, Whisper/wav2vec2 on audio) to predict discrete labels (sarcasm, emotion, questionhood) from natural TV/podcast speech, then uses mutual-information estimates to quantify how much of that signal lives in audio vs. text. No TTS, VC, or SCA system is built, trained, or evaluated anywhere in the paper, it is purely about speech *understanding*/classification, structurally closer to the FAMA/MLC-SLM reject shape than to the TTS-preprocessing (2510.03111) or AURA/VoiceAgentBench accept shapes, just without generative-sounding title language to obscure it. The paper's own relevance_note flagged it as "primarily a speech analysis paper."
**Abstract excerpt:** Prosody -- the melody of speech -- conveys critical information often not captured by the words or text of a message. In this paper, we propose an information-theoretic approach to quantify how much information is expressed by prosody alone and not by text, and crucially, what that information is about... We find that for sarcasm and emotion the audio channel -- and by implication the prosodic channel -- transmits over an order of magnitude more information about these features than the text channel alone.

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________) — user confirmed accept as a scope exception (2026-08-02), reasoning that its findings on prosody's informational content are directly useful background for prosody-control/expressive-TTS research, similar in spirit to the 2510.03111 precedent (accepted for being squarely relevant methodology/analysis work even without training a generative model). Ingested with an honest analysis-paper framing: empty `architecture`/`conditioning` fields, no fabricated TTS results, empty `related_concepts` since no tracked concept's usage rule is actually satisfied by this paper's own content.

---

## 2512.21706 | Enabling Conversational Behavior Reasoning Capabilities in Full-Duplex Speech | arXiv | score: 0.83

**Authors:** Shuchang Pan, Siddharth Banerjee, Dhruv Hebbar, Siddhant Patel, Akshaj Gupta, Kan Jen Cheng, Hanjo Kim, Zeyi Austin Li, Martin Q. Ma, Tingle Li, Gopala Anumanchipalli, Jiachen Lian
**Task guess:** [SCA]
**Reason for review:** Caught at ingest time (2026-08-02, Q4 session 20 continuation), before any page was written. The paper's own system is a spoken-dialogue *understanding/reasoning* pipeline: a hierarchical speech-act detector (HuBERT + Whisper features, causal Transformer) followed by a Graph-of-Thoughts reasoning module that predicts the next conversational behavior and generates a text rationale explaining it. It never generates speech itself — CosyVoice2 is used only as an off-the-shelf tool to synthesize its synthetic training corpus (with a genuinely novel overlap-based TTS dialogue-stitching mechanism), and Moshi/dGSLM are used only as benchmarked existing full-duplex speech-generation systems, not extended or improved. Structurally closer to the DST (2510.09424) and prosody-analysis (2512.16832) shapes than to a speech-generation accept, but with more genuine audio/speech-corpus content than either (real two-channel overlapped speech input, a novel full-duplex TTS corpus-construction method, and direct benchmarking of real full-duplex speech-generation systems on turn-taking statistics).
**Abstract excerpt:** Human conversation is organized by an implicit chain of thoughts that manifests as timed speech acts... We introduce a framework that enables reasoning over conversational behaviors by modeling this process as causal inference within a Graph-of-Thoughts (GoT)... Experiments on both synthetic and real duplex dialogues show that the framework delivers robust behavior detection, produces interpretable reasoning chains, and establishes a foundation for benchmarking conversational reasoning in full duplex spoken dialogue systems.

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________) — user confirmed accept as a scope exception (2026-08-02), extending the 2510.09424/2512.16832 precedent to full-duplex behavior-reasoning research with genuine audio/corpus content, even though the system itself does not generate speech. Ingested with an honest scope note under the abstract callout, empty `conditioning` field, real metrics only (F1/AUC/BLEU/ROUGE are not canonical TTS/VC metrics so `metrics: []`), and a flagged internal inconsistency in the paper's own human-evaluation numbers (Section 6.3 text vs. Table 6 report different rankings) surfaced via a `[!warning]` callout rather than silently picking one.

---

## 2602.04796 | LALM-as-a-Judge: Benchmarking Large Audio-Language Models for Safety Evaluation in Multi-Turn Spoken Dialogues | arXiv | score: 0.45

**Authors:** Amir Ivry, Shinji Watanabe
**Task guess:** [evaluation]
**Reason for review:** Caught at ingest time (2026-08-13, Q1 2026 session batch 17), before any page was written. The paper benchmarks three off-the-shelf large audio-language models (Qwen2-Audio, Audio Flamingo 3, MERaLiON) plus a text-only LLaMA baseline as zero-shot safety judges that output a scalar `[0,1]` safety score for multi-turn spoken dialogues. Coqui XTTS-v2 is used only to synthesize one replaced "unsafe" turn per dialogue, purely to construct the benchmark's synthetic input corpus (DEEPDIALOGUE-derived) — no TTS quality metric (MOS, WER, naturalness, speaker similarity) is reported anywhere, and the studied judges' own output is always a scalar score, never speech. Clean match to the FastLongSpeech (2507.14815) reject pattern: TTS synthesizes benchmark *input*, never model *output*. Also structurally matches the broader FAMA/MLC-SLM/2510.12116 reject shape (pure audio-understanding/classification system, no spoken-output component anywhere). The paper's own `relevance_note` from the filter pass had already flagged "evaluation not generation."
**Abstract excerpt:** Spoken dialogues with and between voice agents are becoming increasingly common, yet assessing them for their socially harmful content such as violence, harassment, and hate remains text-centric... We present LALM-as-a-Judge, the first controlled benchmark and systematic study of large audio-language models (LALMs) as safety judges for multi-turn spoken dialogues.

**Decision:** [ ] accept  [x] reject  [ ] accept-partial (note: _________) — rejected per the FastLongSpeech precedent match (2026-08-13); TTS is incidental benchmark-construction tooling, not a studied generation contribution.

---

## 2602.23333 | SemanticVocoder: Bridging Audio Generation and Audio Understanding via Semantic Latents | arXiv | score: 0.82

**Authors:** Zeyu Xie, Chenxing Li, Qiao Jin, Xuenan Xu, Guanrou Yang, Wenfu Wang, Mengyue Wu, Dong Yu, Yuexian Zou
**Task guess:** [TTS, codec] (filter-assigned; disputed — see below)
**Reason for review:** Caught at ingest time (2026-08-14, Q1 2026 session batch 2), before any page was written. This is a new scope-failure shape, distinct from the established FAMA/MLC-SLM (understanding-wearing-generative-framing) pattern: SemanticVocoder is a genuinely generative system, but it generates general (non-speech) audio, not human speech. The paper's own scope is text-to-audio (TTA) generation of sound events ("a dog barking") and environmental/YouTube audio: trained on AudioSet, evaluated on AudioCaps/Clotho/WavCaps/HEAR (audio event classification, DCASE2016/ESC50/FSD50k), with baselines EzAudio, AudioLDM2, TangoFlux, MakeAnAudio, StableAudio, MMAudio — all general TTA systems, none speech-specific. No mention anywhere in the paper (Abstract, Introduction, Method, Results, Limitations, references) of speech, speaker, prosody, phonemes, linguistic content, or spoken dialogue; the sole "speech" reference is a citation to the HiFi-GAN paper's title (used as a generic vocoder baseline concept, not applied to speech in this work). The filter's `task: [TTS, codec]` tag appears to be a false positive from generic "vocoder"/"text-to-X generation" keyword matching (TTA vs. TTS confusion), not genuine subject-matter overlap with speech synthesis. Flagging for an explicit decision rather than auto-rejecting, since this is a new pattern not previously logged (prior scope precedents in this queue are all speech-*understanding* papers, not non-speech generation papers) and the wiki has an adjacent `neural-codec`/vocoder concept scope that could plausibly extend to general-audio vocoders if the project wants that reach.
**Abstract excerpt:** Recent audio generation models typically rely on Variational Autoencoders (VAEs) and perform generation within the VAE latent space... To address these issues, we discard VAE acoustic latents and introduce semantic encoder latents, thereby proposing SemanticVocoder, a generative vocoder that directly synthesizes waveforms from semantic latents. Equipped with SemanticVocoder, our text-to-audio generation model achieves a Frechet Distance of 12.823 and a Frechet Audio Distance of 1.709 on the AudioCaps test set... Beyond improved generation performance, it also serves as a promising attempt towards unifying audio understanding and generation within a shared semantic space.

**Decision:** [ ] accept  [x] reject  [ ] accept-partial (note: _________) — user confirmed reject (2026-08-14): out of corpus scope, general (non-speech) text-to-audio generation with no speech-specific content anywhere; establishes a new precedent shape distinct from the FAMA/MLC-SLM understanding-wearing-generative-framing pattern (this is genuinely generative, just not of speech).

---

## 2602.23765 | DashengTokenizer: One layer is enough for unified audio understanding and generation | arXiv | score: 0.88

**Authors:** Heinrich Dinkel, Xingwei Sun, Gang Li, Jiahao Mei, Yadong Niu, Jizhong Liu, Xiyang Li, Yifan Liao, Jiahao Zhou, Junbo Zhang, Jian Luan
**Task guess:** [codec] (filter-assigned)
**Reason for review:** Caught at ingest time (2026-08-14, Q1 2026 session batch 2, immediately after the adjacent 2602.23333/SemanticVocoder reject), before any page was written. Distinct shape from that precedent: this paper does have substantial genuine speech content — training data is ~71% speech (English 21% + Chinese 40% + other languages 10%, vs. 21% music / 26% general sound), and it reports a dedicated speech reconstruction benchmark on SEED-TTS (ZH/EN) comparing directly against TTS-community codecs (Mimi, XCodec 2.0, SNAC, XY-Tokenizer), plus a speech enhancement experiment (Valentini/DNS1) and speech-domain understanding tasks (emotion, ASR, speaker ID, gender, language ID via X-ARES). However, the paper's own explicit self-framing is a tri-domain general-purpose audio tokenizer: "a unified continuous audio tokenizer designed for both understanding and generation across speech, music, and environmental sound domains" (§1), and every one of its *generative* demonstrations is non-speech: text-to-audio (AudioCaps, general sound events), text-to-music (MusicCaps), and speech enhancement (a denoising/restoration task, not text-to-speech). The paper never performs TTS or VC generation anywhere — its "generation" results section (§5.4) is entirely TTA/TTM using a flow-matching DiT that replaces a VAE baseline from UniFlow-Audio, a general-audio system. Speech is one of three co-equal evaluation domains (alongside music and environmental/general sound) rather than the paper's subject. This is a new pattern relative to the clean SemanticVocoder reject (which had zero speech content) — flagging for an explicit scope decision rather than assuming either way, since the corpus does track codec/vocoder infrastructure papers and this one's speech-reconstruction table is directly comparable to codecs used elsewhere in the wiki's `neural-codec`/`autoregressive-codec-tts`/`spoken-language-model` concepts.
**Abstract excerpt:** This paper introduces DashengTokenizer, a continuous audio tokenizer engineered for joint use in both understanding and generation tasks... we leverage frozen semantic features and inject acoustic information... We further evaluate the tokenizer's generative performance on text-to-audio (TTA), text-to-music (TTM), and speech enhancement (SE). Our approach surpasses standard variational autoencoder (VAE)-based methods on TTA and TTM tasks... Finally, our results challenge the prevailing assumption that VAE-based architectures are a prerequisite for audio synthesis.

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________) — user confirmed accept (2026-08-14): the SEED-TTS speech-reconstruction benchmark against known in-corpus TTS codecs (Mimi, XCodec 2.0, SNAC, XY-Tokenizer) is genuine neural-codec subject matter even without a TTS/VC generation component of its own; ingest with `task: [codec]` only (no TTS/VC), scoped to the speech-reconstruction contribution, with an explicit note that the paper's own framing and generative demos are tri-domain/non-speech.

---

## 2603.00958 | S-VoCAL: A Dataset and Evaluation Framework for Inferring Speaking Voice Character Attributes in Literature | arXiv (accepted to LREC 2026) | score: 0.80

**Authors:** Abigail Berthe-Pardo, Gaspard Michel, Elena V. Epure, Christophe Cerisara
**Task guess:** [TTS, evaluation] (filter-assigned; disputed — see below)
**Reason for review:** Caught at ingest time (2026-08-14, Q1 2026 session batch 2, third candidate in batch), before any page was written. This is a pure text-based NLP/digital-humanities paper, not a speech-generation paper: the "Attribute Inference" task is entirely text-in/text-out — given a novel's full text (from Project Gutenberg) and a character's identifiers, a RAG pipeline (E5-large retrieval + Qwen3-8B/Phi-4-14B LLM inference) predicts 8 categorical/text attributes (Age, Gender, Origin, Residence, Occupation, Spoken Languages, Physical Health, Type) sourced and ground-truthed from Wikidata. No audio is ever produced, consumed, or evaluated anywhere in the paper; there is no TTS or VC system trained, fine-tuned, or benchmarked, and no speech-quality metric of any kind (the reported metrics are Weighted F1, soft-F1, Cohen's kappa, Krippendorff's alpha, and a Qwen3-embedding cosine-similarity/Human-Aligned-Score for text attribute matching). The paper's own Conclusion frames the contribution correctly: a "standardized benchmark for evaluating systems designed to infer voice-relevant character attributes from novels," motivated by (but not performing) downstream synthetic audiobook narration/character-voice assignment. Structurally this is an even cleaner reject than the FAMA/MLC-SLM/2510.12116/2512.16832 precedents (those at least study audio inputs); here the entire pipeline, including its inputs, is text. The filter's `task: [TTS, evaluation]` tag is a false positive from TTS-motivation language in the abstract ("With recent advances in Text-to-Speech (TTS) systems...") rather than genuine subject-matter overlap with speech generation.
**Abstract excerpt:** With recent advances in Text-to-Speech (TTS) systems, synthetic audiobook narration has seen increased interest... We present S-VoCAL (Speaking Voice Character Attributes in Literature), the first dataset and evaluation framework dedicated to evaluate the inference of voice-related fictional character attributes. S-VoCAL entails 8 attributes grounded in sociophonetic studies, and 952 character-book pairs derived from Project Gutenberg... We demonstrate the applicability of S-VoCAL by applying a simple Retrieval-Augmented Generation (RAG) pipeline to the task of inferring character attributes.

**Decision:** [ ] accept  [x] reject  [ ] accept-partial (note: _________) — rejected (2026-08-14): pure text-in/text-out NLP benchmark, no audio anywhere in the pipeline, cleaner reject than the FAMA/MLC-SLM precedent it matches.

---

## 2603.01592 | TQCodec: Towards neural audio codec for high-fidelity music streaming | arXiv | score: 0.75

**Authors:** Lixing He, Zhouxuan Chen, Mingshuai Liu, Xinran Sun, Wucheng Wang, Minfu Li, Lingcheng Kong, Weifeng Zhao, Wenjiang Zhou
**Task guess:** [codec] (filter-assigned)
**Reason for review:** Caught at ingest time (2026-08-14, Q1 2026 session batch 3, second candidate in batch), before any page was written. Clean corpus-scope reject: TQCodec is a neural audio codec explicitly designed for high-bitrate (32-128 kbps), 44.1 kHz music streaming, targeting the gap left by ultra-low-bitrate speech-oriented codecs (§1: "a significant portion of codec research focuses on speech, where low bandwidth is critical and sufficient" — TQCodec is framed as the non-speech complement to that line of work). Training data is exclusively music: MusDBHQ (150 tracks), Jamendo (55,609 tracks), and a 100k+-track private music dataset (Table 2); evaluation metrics are LSD and SNR computed only on these music datasets, with no speech-domain data, no speech intelligibility/MOS/WER metric, and no comparison to any speech codec (in-corpus or otherwise) anywhere in the paper. Unlike the 2602.23765 (DashengTokenizer) accept, which had ~71% speech training data and a dedicated SEED-TTS speech-reconstruction benchmark against known in-corpus speech codecs, TQCodec has zero speech-domain training or evaluation content — its only relation to speech is that SEANet (its encoder/decoder backbone, borrowed from a speech-enhancement paper) and DAC/EnCodec (its architectural baselines) originated in speech/general-audio codec research. This matches the clean MIDI-VALLE (2507.08530) and SemanticVocoder (2602.23333) reject shape: a real, well-executed generative-audio system with no speech-domain content anywhere in training or evaluation.
**Abstract excerpt:** We propose TQCodec, a neural audio codec designed for high-bitrate, high-fidelity music streaming. Unlike existing neural codecs that primarily target ultra-low bitrates (<= 16kbps), TQCodec operates at 44.1 kHz and supports bitrates from 32 kbps to 128 kbps, aligning with the standard quality of modern music streaming platforms... Evaluations on diverse music datasets demonstrate that TQCodec achieves superior audio quality at target bitrates, making it well-suited for high-quality audio applications.

**Decision:** [ ] accept  [x] reject  [ ] accept-partial (note: _________) — rejected (2026-08-14): trains and evaluates exclusively on music datasets (MusDBHQ, Jamendo, private music corpus) with no speech-domain data, no speech-quality metric, and no comparison to any speech codec anywhere in the paper; matches the clean MIDI-VALLE/SemanticVocoder reject shape, does not meet the DashengTokenizer narrow-accept bar.

---

## 2603.04145 | VietNormalizer: An Open-Source, Dependency-Free Python Library for Vietnamese Text Normalization in TTS and NLP Applications | arXiv | score: 0.60

**Authors:** Hung Vu Nguyen, Loan Do, Thanh Ngoc Nguyen, Ushik Shrestha Khwakhali, Thanh Pham, Vinh Do, Charlotte Nguyen, Hien Nguyen
**Task guess:** [TTS] (filter-assigned)
**Reason for review:** Caught retroactively (2026-08-14, Q1 2026 session batch 3, final candidate). The ingest agent wrote the page directly rather than stopping to flag first (a deviation from instructions), citing the paper's explicit TTS-pipeline framing (title, abstract, §1, §4, and §5.3 "Integration with Multilingual TTS Pipelines") as sufficient scope justification. However, unlike the `2510.03111` preprocessing-pipeline precedent it invoked, this paper reports **zero quantitative results of any kind**: no normalization accuracy, no latency benchmark, no downstream TTS evaluation (MOS/WER), only a qualitative feature-comparison table (Table 1) against four prior Vietnamese text-normalization tools. `2510.03111` by contrast had real signal-quality metrics (PESQ, SI-SDR, SNR, T30, C50, F0-STD, MCD across 24 pipeline configurations) — it just never trained/evaluated a TTS model. This is a materially weaker empirical case, flagged for an explicit decision after the fact rather than left silently accepted.
**Abstract excerpt:** (Vietnamese text normalization library for TTS front-end preprocessing; rule-based, dependency-free, open-source; no empirical evaluation reported.)

**Decision:** [x] accept  [ ] reject  [ ] accept-partial (note: _________) — user confirmed keep (2026-08-14): TTS-pipeline framing plus open-source code availability judged genuine infrastructure value even without benchmarks, in the same spirit as `2510.03111` despite the weaker empirical case; `field_significance: low` / `related_concepts: []` (no controlled-vocabulary concept covers TTS text-frontend normalization tooling) already reflects the limited evidentiary weight. New precedent: TTS-pipeline-framed tooling papers can be kept on framing + infrastructure value alone when zero quantitative validation is reported, provided this is stated honestly in the page's Field Significance section — not a blanket exception for future zero-metric papers, re-evaluate each on its own framing strength.

---
