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
