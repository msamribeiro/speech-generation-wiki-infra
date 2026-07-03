# Controlled Vocabulary

Use these exact terms throughout the wiki. When a paper uses a different label, map it to the
canonical term and note the original in the paper page.

## Tasks

- `TTS` — text-to-speech, speech synthesis from text
- `VC` — voice conversion, speaker/style transfer (the paper trains and/or evaluates a dedicated VC system with VC-specific metrics — e.g. speaker similarity, EER, WER-on-converted-output — regardless of whether the benchmark is a canonical one like L2-ARCTIC/ESD/VCTK conversion or a custom/paper-specific dataset; zero-shot TTS voice cloning as an incidental capability, with no dedicated VC evaluation, is not VC)
- `SCA` — spoken conversational agent, speech LM dialogue system (frontmatter tag only; in prose always write "spoken conversational agents" or "speech LMs")
- `codec` — neural audio codec (foundational, not a task itself)
- `evaluation` — primarily a benchmark, metric, or listening test methodology paper
- `singing` — singing voice synthesis (include if substantial overlap with TTS methods)

## Architecture Families

- `autoregressive-LM` — token-by-token LM decoding (VALL-E family, SoundStorm, etc.)
- `flow-matching` — continuous normalizing flows, rectified flows (Voicebox family)
- `diffusion` — DDPM / score-based / EDM diffusion
- `GAN` — adversarial vocoder or end-to-end GAN
- `VAE` — variational autoencoder
- `transformer-enc-dec` — non-autoregressive seq2seq (FastSpeech family)
- `hybrid` — combines two or more of the above in a single system

## Conditioning

- `text-conditioned`
- `speaker-conditioned` — requires reference audio or fixed speaker embedding
- `zero-shot` — generalizes to unseen speakers at inference from a short reference clip
- `multilingual`
- `emotion-conditioned`
- `prosody-conditioned`
- `instruction-conditioned` — natural language style or paralinguistic instructions
- `prompt-conditioned` — audio prompt at inference (may overlap with zero-shot)

## Training Paradigm

- `supervised`
- `self-supervised` — uses SSL representations (HuBERT, WavLM, EnCodec, etc.)
- `RLHF` — reinforcement learning from human or AI feedback
- `distillation` — knowledge distillation from a larger model
- `fine-tuning` — adapter or full fine-tuning of a pre-trained foundation model
- `continual-learning` — incremental learning without catastrophic forgetting

## Field Significance

Used in paper page frontmatter and `## Field Significance` prose section.

**level:** `low` | `moderate` | `high` | `foundational`

**type** (one or more):
- `engineering-integration` — applies existing techniques to a new context without architectural novelty
- `architectural-novelty` — introduces a new model structure, training objective, or inference procedure
- `empirical-benchmark` — primary contribution is evaluation at scale or on a new benchmark
- `conceptual-contribution` — reframes how the field thinks about a problem
- `negative-result` — shows that a widely-held belief or approach does not hold
- `evaluation-contribution` — introduces a new metric, test set, or listening test methodology
- `dataset-contribution` — primary contribution is a new dataset

**Callout rules by level:**
- `foundational`: wrap `## Field Significance` prose in `> [!important]`
- `high`: wrap in `> [!tip]`
- `moderate` or `low`: plain prose, no callout

## Evaluation Metrics (canonical names)

- `MOS` — mean opinion score (naturalness)
- `SMOS` — speaker similarity MOS
- `WER` — word error rate (intelligibility via ASR)
- `CER` — character error rate
- `SPK-SIM` — automatic speaker cosine similarity
- `UTMOS` — automatic MOS predictor (Saeki et al.)
- `DNSMOS` — Microsoft DNS MOS
- `EER` — equal error rate (anti-spoofing / speaker verification)
- `MUSHRA` — multiple stimuli with hidden reference and anchor
- `PESQ` — perceptual evaluation of speech quality
- `STOI` — short-time objective intelligibility
- `F0-RMSE` — pitch tracking error

## Concept Page Status Values

`emerging` | `established` | `dominant` | `declining` | `contested` | `mature-infrastructure`
