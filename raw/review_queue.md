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

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________) — user chose to leave `status: accepted` unchanged and skip this paper for now rather than deciding immediately (2026-07-18); not ingested. Revisit when convenient — recommend reject on the FAMA/MLC-SLM pattern absent new information, but flagging rather than deciding unilaterally per the review-queue process. Not part of the "DST/dialog scope expansion" backlog interest ([[future_dst_scope_expansion]] memory) in the same way 2510.09424 is, since this paper has no dialogue-state or dialogue-management output at all — it's pure input-side comprehension analysis.

---
