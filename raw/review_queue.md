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

## 2605.31173 | MindVoice: Reconstructing Intelligible Speech from Non-invasive Neural Signals with Pretrained Priors | arXiv | score: 0.45

**Authors:** Guangyin Bao, Taiping Zeng, Jianfeng Feng, et al.
**Task guess:** [TTS] (filter-assigned)
**Reason for review:** MindVoice reconstructs intelligible speech from non-invasive neural (EEG-like) signals using pretrained speech-generation priors; input modality is brain signals rather than text, so fit with the TTS/VC/SCA scope is ambiguous - it uses speech synthesis technology for a brain-computer-interface task, not text-to-speech or voice conversion per the controlled vocabulary.
**Abstract excerpt:** Reconstructing continuous speech from non-invasive neural recordings is a fundamental problem for probing human auditory perception and building safe, scalable speech brain-computer interfaces. Despite recent progress, intelligible reconstruction remains elusive, as non-invasive recordings are inherently noisy, spatially blurred, and only partially preserve information about perceived speech.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2605.31530 | UNISON: A Unified Sound Generation and Editing Framework via Deep LLM Fusion | arXiv | score: 0.62

**Authors:** Zhaoqing Li, Haoning Xu, Jingran Su, et al.
**Task guess:** [TTS] (filter-assigned)
**Reason for review:** UNISON is primarily a unified general-audio generation/editing framework (text-to-audio, text-to-music, scene editing) with TTS and zero-shot speaker cloning as one of several capabilities; unclear how much of the paper's evidence specifically advances speech synthesis versus general audio generation.
**Abstract excerpt:** We present UNISON, a latent diffusion framework that unifies speech generation, sound generation, and audio editing within a single model. A single model handles text-to-audio, text-to-speech, zero-shot speaker cloning, mixed speech-and-sound generation, scene-level audio editing, speech-in-scene editing, and timed temporal composition, all of which share a single set of weights.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2606.00407 | Privacy-preserving Prosody Representation Learning | arXiv | score: 0.55

**Authors:** Kevin Everson, Mari Ostendorf
**Task guess:** [TTS] (filter-assigned)
**Reason for review:** Proposes self-supervised privacy-preserving prosody representation learning with speaker disentanglement; useful for generation but the paper trains no TTS/VC system and reports no synthesis-quality evaluation.
**Abstract excerpt:** Speech representations that capture prosodic information can be useful for both understanding and generation. However, speaker characteristics are reflected in acoustic-prosodic features (e.g., pitch).

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2606.07397 | Audio-Oscar: A Multi-Agent System for Complex Audio Scene Generation, Orchestration, and Refinement | arXiv | score: 0.55

**Authors:** Yifan Duan, Qixiang Xu, Hengtao Wu, et al.
**Task guess:** [TTS] (filter-assigned)
**Reason for review:** Audio-Oscar is a multi-agent system orchestrating complex audio scene generation across TTS, text-to-audio, and text-to-music; TTS is one of several generation types and the primary contribution is scene-level orchestration rather than speech synthesis quality.
**Abstract excerpt:** In recent years, audio generation has made significant progress in tasks such as text-to-speech (TTS), text-to-audio (TTA) and text-to-music (TTM). However, generating long-form and controllable audio from complex audio scene descriptions remains a significant challenge, as such scenes often require coordinated speech, sound effects, music, songs, temporal structure, and post-production.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2606.09098 | HoliDubber: Holistic Video Dubbing for Complex Acoustic Scenes via Text-Guided Audio Synthesis | arXiv | score: 0.62

**Authors:** Wenhao Guan, Yifan Duan, Junxi Liu, et al.
**Task guess:** [TTS] (filter-assigned)
**Reason for review:** HoliDubber proposes holistic video dubbing combining text-guided speech and ambient-audio synthesis; core speech synthesis is one part of a broader dubbing/audio-scene system, similar to the UNISON/Audio-Oscar borderline pattern.
**Abstract excerpt:** Video dubbing is a cornerstone of multimedia content creation, aiming to synthesize synchronized acoustic sequences for visual streams. While Text-to-Speech (TTS) and Text-to-Audio (TTA) generation have each achieved remarkable progress, existing dubbing systems remain confined to isolated speech synthesis without incorporating sound effects and ambient audio, forcing practitioners to rely on fragmented workflows and laborious manual post-mixing.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2606.09667 | Cross-Modal Masking for Robust Silent Speech Synthesis Using sEMG and Lipreading | arXiv | score: 0.48

**Authors:** Eder del Blanco, David Gimeno-Gómez, Eva Navas, et al.
**Task guess:** [TTS] (filter-assigned)
**Reason for review:** Proposes cross-modal masking for silent speech synthesis from sEMG and lipreading signals; generates speech from non-text, non-acoustic input modalities, so fit with the text-to-speech/voice-conversion scope is ambiguous, similar to MindVoice (2605.31173).
**Abstract excerpt:** Speech restoration through silent speech interfaces (SSIs) has emerged as a promising assistive technology for individuals with impaired or absent laryngeal voice production. Among non-invasive SSI modalities, surface electromyography (sEMG) and video-based lipreading provide complementary articulatory information, yet their integration for continuous speech synthesis remains underexplored.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2606.09717 | What Makes Synthetic Speech Sound Sarcastic? A Prosody-Controlled Perception Study | arXiv | score: 0.55

**Authors:** Zhu Li, Shekhar Nayak, Matt Coler
**Task guess:** [TTS, evaluation] (filter-assigned)
**Reason for review:** Uses prompt-conditioned neural TTS as an experimental tool in a perception study of sarcasm; primary contribution is a human-perception finding about prosodic cues rather than a TTS system or evaluation-methodology advance.
**Abstract excerpt:** Prosody plays an important role in sarcasm perception, yet previous studies have relied on naturally produced speech that lacks fine-grained control over individual acoustic dimensions. As prosodic cues co-vary in natural data, isolating their independent contributions remains challenging.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2606.12812 | Vocal Identity Under Siege by AI Voice Cloning Technologies | arXiv | score: 0.4

**Authors:** Jyh-An Lee, Xuan Sun
**Task guess:** [] (filter-assigned)
**Reason for review:** A legal/ethical commentary on AI voice cloning and vocal identity rights (prompted by the ChatGPT-4o/Scarlett Johansson controversy); relevant to TTS/VC ecosystem policy but unclear if it is an empirical ML contribution versus a law/ethics article.
**Abstract excerpt:** The advent of sophisticated AI-driven voice cloning has brought to the fore critical legal and ethical challenges regarding the protection of vocal identity. Prompted by recent controversies - including the striking resemblance between OpenAI's ChatGPT-4o voice and that of Scarlett Johansson - this article examines how generative AI technologies undermine the unique value of the human voice and further complicate the legal questions surrounding personality right.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2606.13630 | From Tokens to Faces: Investigating Discrete Speech Representations for 3D Facial Animation | arXiv | score: 0.4

**Authors:** Pedro Correa, Olivier Perrotin, Samir Sadok, et al.
**Task guess:** [] (filter-assigned)
**Reason for review:** Evaluates discrete speech representations (SSL, codec, ASR-style) for driving 3D facial animation; the target task is facial animation, not speech generation, though the representations studied are the same ones used in TTS/codec research.
**Abstract excerpt:** The choice of speech representation is critical in speech-driven 3D facial animation. Representations differ in what they encode: SSL features emphasize segmental and semantic cues, neural codecs yield latents optimized for acoustic reconstruction, and ASR-style objectives produce label-based spaces.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2606.14004 | Unsupervised Approaches for Global Prosodic Embedding Extraction | arXiv | score: 0.55

**Authors:** Martin Meza, Luciana Ferrer, Pablo Riera
**Task guess:** [TTS] (filter-assigned)
**Reason for review:** Studies unsupervised extraction of global prosodic embeddings disentangled from linguistic/speaker information; a representation-learning contribution useful for TTS but the paper trains no synthesis system.
**Abstract excerpt:** Prosody is central to oral communication, conveying information like the emotional state of the speaker and cues needed for meaning disambiguation. Many self-supervised models of speech produce embeddings that encode prosodic as well as linguistic, and speaker information.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2606.16464 | Towards Robust Generative Speech Enhancement Using Vector Quantisation-Based Neural Audio Codec | arXiv | score: 0.42

**Authors:** Haixin Zhao, Nilesh Madhu
**Task guess:** [] (filter-assigned)
**Reason for review:** Investigates generative speech enhancement using a VQ-based neural audio codec; speech enhancement is adjacent to but outside the TTS/VC/SCA/codec-generation scope, though it reuses codec/generative-modeling techniques.
**Abstract excerpt:** This work investigates modelling strategies in continuous and discrete latent spaces in the vector quantisation (VQ)-based neural audio codec (NAC) speech enhancement (SE), along with the role of VQ regularisation. We propose cNAC-SE and dNAC-SE frameworks that predict continuous representations and discrete tokens in latent space, respectively.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2606.17806 | PhASE-Flow: Phonetic-Conditioned Acoustic Flow Matching in SSL Representation Domain for Speech Enhancement | arXiv | score: 0.42

**Authors:** Jun Gao, Xiaobin Rong, Yu Sun, et al.
**Task guess:** [] (filter-assigned)
**Reason for review:** PhASE-Flow applies phonetic-conditioned flow matching in SSL representation space for speech enhancement; speech enhancement is adjacent to but outside the TTS/VC/SCA/codec-generation scope, though the flow-matching/SSL techniques are directly relevant.
**Abstract excerpt:** Flow matching (FM) enables high-fidelity generation, while self-supervised learning (SSL) speech models provide hierarchical representations spanning acoustic and phonetic levels. However, existing FM-based speech enhancement (SE) methods operate primarily in the spectral domain, treating SSL features only as external conditions rather than modeling directly in the SSL latent space.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2606.21215 | Speaker Identity in Non-Verbal Vocalizations: Conditional Distillation and Mixture of Experts Approach | arXiv | score: 0.5

**Authors:** Tzu-Chieh Wei, Yi-Cheng Lin, Huang-Cheng Chou, et al.
**Task guess:** [evaluation] (filter-assigned)
**Reason for review:** Studies speaker verification robustness on non-verbal vocalizations (motivated by expressive TTS/VC systems increasingly generating NVVs); primarily an SV-system contribution rather than a TTS/VC/SCA generation or dedicated evaluation-methodology paper.
**Abstract excerpt:** As expressive text-to-speech (TTS) and voice conversion (VC) systems increasingly generate non-verbal vocalizations (NVVs) to enhance naturalness, reliable speaker verification (SV) becomes essential to objectively assess identity consistency across both verbal and non-verbal segments. Yet current SV systems generalize poorly to NVVs, and fine-tuning on NVV data causes catastrophic forgetting of speech performance.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2606.23052 | CAAD: Contrastive Audio-Aware Distillation for Efficient Speech Language Models | arXiv | score: 0.5

**Authors:** Chun-Wei Chen, Tzu-Quan Lin, Ke-Han Lu, et al.
**Task guess:** [SCA] (filter-assigned)
**Reason for review:** CAAD proposes contrastive audio-aware distillation for efficient speech language models to improve acoustic grounding over linguistic priors; relevant to SCA/speech-LM infrastructure, but unclear from the abstract whether the target SLM performs speech generation or is a speech-understanding/reasoning model only.
**Abstract excerpt:** Speech Language Models achieve reasoning capabilities, but are often hindered by massive parameter counts and a tendency to prioritize linguistic priors over acoustic features. While contrastive decoding enhances grounding by contrasting audio-aware and text-only logits, it increases inference latency.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2606.27380 | A Survey of Automated Presentation Coaching: Systems, Methods, and Open Challenges | arXiv | score: 0.5

**Authors:** Wen Liang, Li Siyan, Zackary Rackauckas, et al.
**Task guess:** [] (filter-assigned)
**Reason for review:** Surveys automated presentation-coaching systems spanning pronunciation training, prosody/fluency coaching, and speech synthesis; speech synthesis is one of several dimensions covered rather than the survey's primary focus.
**Abstract excerpt:** Automated coaching for oral presentations sits at the intersection of computer-assisted pronunciation training (CAPT), prosody modeling, and speech synthesis, yet no prior work has systematically surveyed and compared existing systems along these dimensions. This survey reviews and categorizes automated presentation coaching systems, spanning pronunciation tutors, fluency and prosody coaches, multimodal trainers, and conference Q&A practice tools.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2607.02763 | LuxSQA: Ask Me in Luxembourgish with TTS-Augmented Spoken Question Answering | arXiv | score: 0.6

**Authors:** Nina Hosseini-Kivanani, Marco Matassoni, Alessio Brutti
**Task guess:** [TTS] (filter-assigned)
**Reason for review:** LuxSQA investigates whether TTS can generate task-specific training data for low-resource Luxembourgish spoken question answering; TTS is used as a data-augmentation tool for a downstream QA task rather than the paper's primary object of study.
**Abstract excerpt:** Spoken Question Answering (SQA) remains largely focused on high-resource languages and carefully recorded speech, limiting the reach of speech-LLM methods in low-resource settings. This paper investigates whether text-to-speech (TTS) can provide task-specific training data for Luxembourgish SQA without requiring a large human-recorded QA corpus.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2607.06014 | Escaping the Procrustean Bed: Groupwise Orthogonal Connectors for Audio-Language Models | arXiv | score: 0.45

**Authors:** Ho-Lam Chung, Ke-Han Lu, Yi-Cheng Lin, et al.
**Task guess:** [] (filter-assigned)
**Reason for review:** Studies representation collapse in Q-Former audio-language connectors that lose paralinguistic cues (speaker, gender, prosody); relevant to audio-LLM understanding architecture, but unclear from the abstract whether the target system performs speech generation or is an understanding-only audio-language model.
**Abstract excerpt:** Audio-language models compress a speech encoder's output through a Querying Transformer (Q-Former) connector before feeding it to a large language model. We identify two failures in this compression.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2607.07579 | Text-Independent Speaker Verification Using Discrete Audio Tokens | arXiv | score: 0.4

**Authors:** Zheng Liang, Junjie Li, Kong Aik Lee
**Task guess:** [codec] (filter-assigned)
**Reason for review:** Studies whether discrete neural-audio-codec tokens (originally developed for speech synthesis) can be used for text-independent automatic speaker verification; primarily an ASV-system contribution using codec representations as a feature source, not a TTS/VC/SCA generation or codec-design paper itself.
**Abstract excerpt:** Neural audio codecs (NACs) enable efficient audio compression and have achieved success in downstream tasks such as speech synthesis. However, their discrete representations consistently underperform traditional spectral features in automatic speaker verification (ASV).

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2607.08409 | When Synthetic Speech Is All You Have: Better Call GRPO | arXiv | score: 0.45

**Authors:** Shashi Kumar, Yanis Labrak, Hasindri Watawana, et al.
**Task guess:** [TTS] (filter-assigned)
**Reason for review:** Applies reinforcement learning (GRPO) to close the synthetic-real acoustic gap for LLM-based ASR trained on TTS-generated speech in privacy-constrained domains; primarily an ASR-adaptation paper that uses synthetic TTS speech as its training substrate rather than advancing TTS itself.
**Abstract excerpt:** LLM-based ASR adapted to regulated domains such as banking is bottlenecked by privacy: real speech is costly and legally constrained to collect, making synthetic text-to-speech (TTS) an attractive substitute. Yet synthetic speech stays acoustically mismatched with real recordings, and work on this gap has stayed within supervised fine-tuning (SFT).

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2607.09134 | ReGen: Hierarchical Multi-Prompt Representation Generation for Efficient Waveform Diffusion Models | arXiv | score: 0.5

**Authors:** Sang-Hoon Lee, Ha-Yeong Choi
**Task guess:** [] (filter-assigned)
**Reason for review:** ReGen proposes a hierarchical multi-prompt representation-generation framework to accelerate waveform diffusion model training; the abstract does not specify whether the target domain is speech or general audio, leaving TTS/VC/SCA relevance ambiguous.
**Abstract excerpt:** Representation alignment (REPA) has been investigated to accelerate diffusion training, but we observe that regularizing intermediate representations in diffusion Transformers (DiT) may implicitly entangle latents and limit generative capacity. To address this issue, we propose ReGen, a hierarchical multi-prompt representation generation framework that jointly estimates multiple vector fields for both representations and data within a single diffusion model.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2607.10162 | Hearing Like Humans? Sound Symbolism and Perceptual Alignment in Speech Language Models | arXiv | score: 0.55

**Authors:** Yun-Shao Tsai, Chun-Wei Chen, Chee-En Yu, et al.
**Task guess:** [SCA] (filter-assigned)
**Reason for review:** Studies whether speech language models exhibit human-like sound symbolism using genuine human speech recordings; a perceptual-alignment analysis of SLM representations rather than a TTS/VC/SCA generation or evaluation-methodology contribution.
**Abstract excerpt:** Sound symbolism, the human tendency to map speech sounds to perceptual qualities such as roundness or sharpness, arises primarily from the acoustics of speech rather than spelling. Whether Speech Language Models (SLMs) share this tendency remains open, as prior evaluations rely on text or images rather than real speech.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2607.10790 | Data Augmentation for L2 English Speaking Assessment using TTS | arXiv | score: 0.45

**Authors:** Stefano Bannò, Penny Karanasou, Mengjie Qian, et al.
**Task guess:** [TTS] (filter-assigned)
**Reason for review:** Investigates using TTS and voice cloning to convert written L2 English text into synthetic speech for augmenting L2 speaking-proficiency assessment training data; TTS is used as a data-augmentation tool for a downstream assessment task rather than the paper's primary object of study.
**Abstract excerpt:** Automated assessment of second language (L2) speaking proficiency relies on large-scale annotated speech data, which remains scarce compared to widely available written learner corpora. A promising direction for addressing this imbalance is to use text-to-speech (TTS) and voice cloning to convert written L2 production into synthetic speech.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2607.16870 | Do Speech Tokens Leak Voiceprints? Speaker Inversion Attacks Against End-to-End Speech Language Models | arXiv | score: 0.62

**Authors:** Ye Lu, Yihan Yan, Zhaoyang Zhang, et al.
**Task guess:** [] (filter-assigned)
**Reason for review:** Investigates whether speech tokens used in end-to-end speech language models leak speaker voiceprints via speaker-inversion attacks; a privacy/security analysis of speech-token representations used in SCA systems.
**Abstract excerpt:** End-to-end speech language models increasingly represent user speech with speech tokens rather than relying exclusively on cascaded ASR--LLM--TTS pipelines. Although these tokens support expressive and low-latency spoken interaction, they may also preserve sensitive speaker characteristics.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2607.18629 | CS-ETS: Chaos-Inspired Samba-Based EMG-To-Speech Synthesis with Nonlinear Chaotic Losses | arXiv | score: 0.48

**Authors:** Sajid Fardin Dipto, Tarikul Islam Tamiti, David Vergano, et al.
**Task guess:** [TTS] (filter-assigned)
**Reason for review:** CS-ETS proposes a chaos-inspired architecture for EMG-to-speech synthesis; generates speech from a non-text, non-acoustic input modality (surface EMG), so fit with the text-to-speech/voice-conversion scope is ambiguous, similar to other silent-speech-interface papers.
**Abstract excerpt:** We propose a chaos-inspired new architecture for EMG-to-Speech (ETS) synthesis called CS-ETS, which combines a Samba-based encoder with two novel chaos-inspired loss functions -- Lyapunov Exponent Regularization (LER) and Multi-Scale Detrended Fluctuation Analysis (MSDFA). LER is designed based on Lyapunov exponents to capture nonlinear fluctuations and sensitivity to initial conditions.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2607.21132 | Investigating Codec-Internal Latent Audio Watermarking for Neural Codec Robustness | arXiv | score: 0.45

**Authors:** Zi Hu, Houmin Sun, Linxi Li, et al.
**Task guess:** [codec] (filter-assigned)
**Reason for review:** Investigates continuous latent-space audio watermarking robust to neural codec re-encoding; a traceability/security contribution for codec-processed audio rather than an advance in codec reconstruction or speech generation quality.
**Abstract excerpt:** Neural audio codecs are challenging transformations for audio watermarking because they re-encode, quantize, and resynthesize speech. This paper investigates continuous latent-space watermarking for codec robustness.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2607.22304 | Synthetic Speech, Real Signal: Paralinguistic Preservation and Cross-Lingual Augmentation via Voice Cloning | arXiv | score: 0.55

**Authors:** Roseline Polle, Owen Parsons, George Fairs, et al.
**Task guess:** [VC] (filter-assigned)
**Reason for review:** Studies voice cloning as a data-augmentation approach for clinical paralinguistic tasks, evaluating downstream task performance rather than voice-cloning intelligibility/similarity metrics; VC used as one tool for an application study rather than the paper's primary object of study.
**Abstract excerpt:** Synthetic data augmentation in speech is common practice for linguistic tasks like ASR, but has seen far less work for paralinguistic ones, especially clinical tasks where labelled data is expensive and some patient groups are underrepresented. Voice cloning is one such augmentation approach, but is typically evaluated on speech intelligibility (WER) or speaker similarity (SS) rather than on downstream performance, and it remains unclear whether these preserve the paralinguistic signal such tasks depend on.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2607.26350 | Dissecting Sensitivity to Training Language in Self-Supervised Speech Learning Using Neural Audio Codec Tokens | arXiv | score: 0.55

**Authors:** Daigo Takizawa, Tomohiko Nakamura, Samuele Cornell, et al.
**Task guess:** [codec] (filter-assigned)
**Reason for review:** Investigates language sensitivity of self-supervised learning models trained on neural-audio-codec discrete tokens; a codec-based SSL representation-robustness study relevant to but not centrally about TTS/VC/SCA generation.
**Abstract excerpt:** Neural audio codecs (NACs) have become popular for obtaining speech representations as discrete tokens. Beyond compression, discrete tokens can be used to train self-supervised learning (SSL) models.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2607.26541 | Prosody-driven Jailbreaks in Audio LLMs: A Controlled Study and Mechanistic Analysis | arXiv | score: 0.5

**Authors:** Jiachen Qian, Junyu Li
**Task guess:** [SCA] (filter-assigned)
**Reason for review:** Studies how prosodic delivery variation (holding transcript text fixed) affects jailbreak susceptibility in audio-capable foundation models; a safety/robustness analysis of spoken interaction models rather than a TTS/VC/SCA generation or evaluation-methodology contribution.
**Abstract excerpt:** Audio-capable foundation models enable end-to-end spoken interaction, but they also introduce safety risks beyond transcript content. It remains unclear how much jailbreak capability can arise from matched-text variation in speech delivery rather than from lexical rewriting or broader style transfer.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2608.06409 | Separating Decision-Rule Misalignment from Readout-Coverage Limitations in Speech Language Models | arXiv | score: 0.55

**Authors:** Linkai Peng, Baorian Nuchged
**Task guess:** [SCA] (filter-assigned)
**Reason for review:** Introduces a generation-aligned diagnostic ladder separating decision-rule misalignment from readout-coverage limitations when evaluating paralinguistic-task accuracy in speech language models; an evaluation-methodology contribution for SLM understanding capability rather than a TTS/VC/SCA generation or synthesis-quality-evaluation paper.
**Abstract excerpt:** Speech language models are increasingly evaluated on paralinguistic tasks by the accuracy of prompted answers, but answer accuracy combines failures at different stages of the audio-to-answer computation. We introduce a generation-aligned diagnostic ladder that compares the emitted answer, the option logits, an affine readout of those logits, and a linear readout of the hidden state at the same answer token.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2608.10405 | Never Stop Speaking: a Denial-of-Service Attack on End-to-End Speech Language Models | arXiv | score: 0.45

**Authors:** Shuozhe Cheng, Kunlan Xiang, Mingxuan Li, et al.
**Task guess:** [SCA] (filter-assigned)
**Reason for review:** Studies a denial-of-service attack that induces end-to-end speech language models to generate excessively long outputs; a security/robustness study of speech-LM systems rather than a TTS/VC/SCA generation, control, or evaluation-methodology contribution.
**Abstract excerpt:** Many studies have shown that specially crafted inputs can induce large language models (LLMs) to generate excessively long outputs, resulting in significant computational overhead and resource consumption. While most existing denial-of-service (DoS) attacks target text-only LLMs, end-to-end (E2E) speech LLMs are rapidly emerging.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2608.11804 | MiDashengLM-Gen: Unified Audio Scene Generation via LLM-Driven Autoregressive Flow Matching | arXiv | score: 0.6

**Authors:** Xingwei Sun, Heinrich Dinkel, Gang Li, et al.
**Task guess:** [TTS] (filter-assigned)
**Reason for review:** MiDashengLM-Gen proposes end-to-end unified audio scene generation blending speech, music, and sound effects via LLM-driven autoregressive flow matching; speech intelligibility is a stated motivation, but the paper's primary contribution is general audio-scene generation rather than speech synthesis specifically, similar to the UNISON/Audio-Oscar/HoliDubber borderline pattern.
**Abstract excerpt:** Generating coherent audio scenes that simultaneously blend speech, music, and sound effects remains a significant challenge. Current approaches typically rely on a disjointed pipeline where a frozen, decoupled text encoder feeds a separate audio decoder, limiting cross-modal optimization and leading to poor speech intelligibility.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2608.12082 | Rethinking Language Model-Based Generative Speech Enhancement in the Latent Space of a Neural Audio Codec | arXiv | score: 0.42

**Authors:** Yihui Fu, Zhengyang Li, Tim Fingscheidt
**Task guess:** [] (filter-assigned)
**Reason for review:** Presents a unified framework covering six LM-based generative speech-enhancement modeling paradigms in neural-audio-codec latent space; speech enhancement is adjacent to but outside the TTS/VC/SCA/codec-generation scope, though it directly reuses codec/generative-modeling techniques from speech synthesis research.
**Abstract excerpt:** Language model (LM)-based speech enhancement (SE) has recently emerged rapidly using latent space features of neural audio codecs (NACs). In this paper, first, we present a unified framework covering six popular LM-based generative SE modeling paradigms based on discrete/continuous latent NAC features: discrete or continuous autoregressive (D/CAR) SE, discrete or continuous non-autoregressive (D/CNAR) SE, discrete diffusion (DDiff) SE, and continuous flow matching (CFM) SE.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2608.14029 | S2Dialog: Multimodal Dialogue Retrieval with Semantic and Acoustic-Style Modeling | arXiv | score: 0.4

**Authors:** Xueqi Wang, Zhigang Wang, Runqing Zhang, et al.
**Task guess:** [] (filter-assigned)
**Reason for review:** S2Dialog studies multimodal dialogue retrieval (retrieving similar dialogues by semantic and acoustic-conversational style) as an auxiliary resource for downstream dialogue tasks; a retrieval-system contribution rather than TTS/VC/SCA generation itself, though motivated by conversational speech synthesis applications.
**Abstract excerpt:** Multimodal dialogue retrieval aims to retrieve dialogues from multimodal dialogue banks that are similar to a target dialogue in terms of both textual semantics and acoustic conversational styles. Such dialogue-level retrieval is crucial for many dialogue-related tasks, including Emotion Recognition in Conversation, Spoken Dialogue Systems, and Conversational Speech Synthesis, where external dialogue examples can provide valuable semantic and stylistic references.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2608.15369 | AudioTQ: A Data-Oblivious 6-Bit CPU Audio Codec via Randomized Hadamard Rotation and Lloyd-Max Quantization | arXiv | score: 0.4

**Authors:** Sahil Gangurde
**Task guess:** [] (filter-assigned)
**Reason for review:** AudioTQ proposes a data-oblivious, psychoacoustic-free lossy audio compression scheme (randomized Hadamard rotation plus Lloyd-Max quantization) as a general alternative to MP3/AAC/Opus; unclear whether this is a learned neural speech codec in the sense used by TTS/VC/SCA generation research or a general-purpose classical audio-compression technique.
**Abstract excerpt:** Lossy audio compression algorithms traditionally rely on psychoacoustic modeling and frequency-domain representations (e.g., MP3, AAC, and Opus) to discard information that is imperceptible to the human auditory system. While highly effective, these approaches are computationally complex and domain-specific.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2608.19959 | Tracking the Trend in How Speech Synthesizers Deceive People | arXiv | score: 0.6

**Authors:** Milan Šalko, Anton Firc, Kamil Malinka, et al.
**Task guess:** [evaluation] (filter-assigned)
**Reason for review:** Compares human deepfake-audio detection accuracy against pretrained detectors across TTS synthesizers released in 2019, 2022, and 2024, tracking how perceptually deceptive synthetic speech has become over time; a human-perception trend study of TTS realism, evaluation-adjacent but framed primarily around deepfake detection rather than TTS methodology.
**Abstract excerpt:** Advances in speech synthesis have made deepfake audio highly realistic. Earlier studies reported 70-80% human detection accuracy, but relied primarily on older synthesizers.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---
## 2026.dialres-1.18 | Speaker Normalization via Voice Conversion Reveals a Human-Machine Dissociation in Dialect Classification | workshop | score: 0.45

**Authors:** Caroline Kleen, Lea Fischbach, Akbar Karimi, et al.
**Task guess:** [VC]
**Reason for review:** Uses off-the-shelf Retrieval-based Voice Conversion (RVC) purely as a speaker-normalization instrument to study human vs. machine dialect classification; VC is a black-box tool for a perception study, not the paper's own method or evaluation contribution to VC itself.
**Abstract excerpt:** This study evaluates whether Retrieval-based Voice Conversion (RVC) can be used to normalize speaker-specific variability while preserving dialect-relevant acoustic cues, and what the response of human and machine systems to this manipulation reveals about the architecture of dialect recognition.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2026.findings-acl.1245 | A Unified Feature Mixture Framework for Joint Speech and Singing Deepfake Detection | ACL | score: 0.42

**Authors:** Aastha Sharma, Guangjing Wang
**Task guess:** []
**Reason for review:** GenuVoice is a deepfake detector for voice-conversion and singing-synthesis audio; it engages directly with synthetic speech/singing artifacts but the contribution is detection, not generation or a synthesis quality/evaluation methodology, so it sits outside the controlled task vocabulary.
**Abstract excerpt:** High-fidelity audio generation techniques, such as voice conversion and singing voice synthesis, have significantly increased the risk of audio deepfakes. Although existing methods perform well on conversational speech deepfake detection, they fail severely under the speech-to-singing domain shift.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2026.iwsds-1.16 | Conversational AI for Virtual Standardized Patients using a Speech-to-Speech LLM | workshop | score: 0.45

**Authors:** Andrew Emerson, Keelan Evanini, Su Somay, et al.
**Task guess:** [SCA]
**Reason for review:** Uses an existing speech-to-speech LLM as a black-box component to build a medical-education application (virtual standardized patients); an application/deployment paper rather than a method contribution advancing S2S or SCA generation itself.
**Abstract excerpt:** To develop clinical reasoning skills, medical students are often tasked with interacting with trained standardized patients (SPs). Human SPs enable real conversations that can resemble authentic clinical scenarios.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2026.iwsds-1.3 | Personality Expression in Spoken Dialogue Systems: From Text to Speech | workshop | score: 0.5

**Authors:** Kenta Yamamoto, Kazunori Komatani
**Task guess:** [TTS]
**Reason for review:** Studies which personality traits are reliably perceived when expressed through a text-to-speech-realized spoken dialogue system; ambiguous whether the paper's core contribution is a synthesis/control method or a corpus-based perception analysis.
**Abstract excerpt:** A consistent personality in a spoken dialogue system enhances the naturalness and friendliness of interactions. However, users may not accurately perceive all the personality traits that the system attempts to express.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2026.iwsds-1.4 | Reproducing Proficiency-Conditioned Dialogue Features with Full-duplex Spoken Dialogue Models | workshop | score: 0.58

**Authors:** Takao Obi, Sadahiro Yoshikawa, Mao Saeki, et al.
**Task guess:** [SCA]
**Reason for review:** Adapts and empirically evaluates an existing full-duplex spoken dialogue model's ability to reproduce proficiency-conditioned human dialogue features; a capability/behavior study of SCA rather than a new generation method.
**Abstract excerpt:** Real-time, human-centered conversational AI requires systems that handle spoken dialogue with overlap and rapid turn-taking. Although full-duplex models promise these capabilities, empirical work applying them to conversational AI is still nascent.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2026.iwsds-1.9 | Exploring Emotional Nuances in Spoken Dialogue: Dataset Construction and Prediction of Emotional Dialogue Breakdown | workshop | score: 0.4

**Authors:** Hyuga Nakaguro, Koichiro Yoshino
**Task guess:** []
**Reason for review:** Constructs a "paraling-dial" dataset pairing fixed utterance text with five distinct emotional speech renditions, but the paper's own contribution is predicting emotional dialogue breakdown (a classification task) rather than synthesis; the paired-audio resource has latent emotional-TTS relevance.
**Abstract excerpt:** In spoken dialogue systems, even when the utterance text is the same, speaking style or tone differences can change its nuance. To respond appropriately in such cases, systems must accurately interpret paralinguistic information.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2026.lrec-1.184 | Probing Discrete Speech Tokens of Spoken Language Models | workshop | score: 0.55

**Authors:** Sven Naber, Julia Koch, Pranav Singh, et al.
**Task guess:** [codec]
**Reason for review:** Presents a probing framework analyzing what phonetic/paralinguistic attributes are recoverable from discrete speech tokens used by spoken language models; a representation-analysis study relevant to codec/SLM design but not itself a new generation or codec method.
**Abstract excerpt:** This paper presents a framework for systematic probing of discrete speech token representations in spoken language models (SLMs). We propose three complementary components: a distributional divergence analysis testing whether an attribute is reflected in token usage, token-based classifiers to quantify recoverability and an attribute-conditioned representation analysis.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---

## 2026.nlpaics-1.18 | How Well Do Commodity Text-to-Speech Systems Evade Acoustic Perturbation Detection? A Multi-Engine Evaluation Across 21 Languages | workshop | score: 0.68

**Authors:** Anatoly Marchenko
**Task guess:** [TTS, evaluation]
**Reason for review:** Empirically characterizes commodity TTS engines' acoustic properties (jitter, shimmer, HNR) across 21 languages against deepfake-detection biomarkers; substantial synthesis-quality characterization content, but framed primarily around detection-evasion rather than TTS methodology or standard listening-test evaluation.
**Abstract excerpt:** Jitter, shimmer, and harmonics-to-noise ratio (HNR) are often used to detect voice deepfakes, since these features capture biomechanical irregularities of vocal fold vibration that synthetic speech supposedly lacks. We test this assumption on three commodity TTS engines.

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)

---
