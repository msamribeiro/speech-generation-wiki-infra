# Metadata Schema

Every paper in `raw/metadata/` has a JSON file named `{id}.json`.

## ID Naming Convention

- arXiv papers: use the arXiv ID (e.g. `2406.18009`)
- Proceedings papers without arXiv: `{venue-slug}-{year}-{sequence}` (e.g. `interspeech-2025-0412`)
- Technical reports: `{org}-{slug}-{year}` (e.g. `google-audiopalm2-2025`)

## JSON Schema

```json
{
  "id": "string",
  "title": "string",
  "authors": ["list of strings"],
  "organization": "string or null — primary affiliated org (e.g. Google, Microsoft, CMU)",
  "venue": "one of the venue values listed below",
  "venue_type": "one of: conference | workshop | preprint | technical-report",
  "year": 2025,
  "month": 11,
  "published_date": "YYYY-MM-DD — date of first public availability",
  "ingested_date": "YYYY-MM-DD or null — set on ingest",
  "generation_history": [
    {
      "date": "YYYY-MM-DD",
      "op": "ingest | re-ingest | quality-pass",
      "agent": "speech-generation-ingest-agent | speech-generation-lightweight-ingest-agent | speech-generation-integration-agent",
      "model": "string — the model ID that actually performed this operation, e.g. claude-sonnet-5",
      "commit": "abc1234"
    }
  ],
  "url": "string — arXiv or proceedings URL",
  "pdf_path": "raw/papers/filename.pdf",
  "task": ["list — one or more task values; see docs/schemas/vocabulary.md"],
  "relevance_score": 0.95,
  "relevance_note": "string — brief reason for score, especially for borderline cases",
  "status": "one of: pending | review | accepted | rejected | ingested",

  "discovery_source": "citation-discovery — only present for CD papers",
  "corpus_role": "one of the corpus_role values below — null for standard filter papers",
  "corpus_citation_count": 208,
  "citation_counts_by_quarter": {"Q3_2025": 56, "Q4_2025": 45},
  "sr_match": "true | false | null — whether the paper matched the keyword filter",
  "ingest_tier": "1 | 2 | null — Tier 1 = full page; Tier 2 = lightweight stub; null for standard papers"
}
```

## Status Lifecycle

```
pending   → filter agent assigns relevance score
review    → borderline (0.40–0.70): added to raw/review_queue.md for human decision
accepted  → score > 0.70 or human confirmed relevant: ready to ingest
rejected  → score < 0.40 or human confirmed irrelevant: skip
ingested  → wiki paper page written
```

## Venue Allowed Values

`Interspeech` | `ICASSP` | `ACL` | `EMNLP` | `NAACL` | `NeurIPS` | `ICLR` | `ICML` | `ASRU` | `SLT` | `arXiv` | `technical-report` | `workshop` | `other`

## corpus_role Allowed Values

Classifies citation-discovery papers by functional role in the speech synthesis ecosystem.

| Value | Description | Examples |
|-------|-------------|---------|
| `tts-vc` | TTS or voice conversion system | HiFi-GAN, FastSpeech 2, VALL-E 2 |
| `sca` | Spoken conversational agent / full-duplex speech LM | Moshi, LLaMA-Omni |
| `codec` | Neural audio codec | EnCodec, SpeechTokenizer, BigCodec |
| `audio-lm` | Audio/speech LM not primarily TTS | AudioLM, SoundStorm, SpeechGPT |
| `foundation-lm` | General-purpose LLM used as TTS/SCA backbone | LLaMA, GPT-4, Qwen |
| `asr` | Automatic speech recognition system | Whisper, Paraformer |
| `speaker` | Speaker verification or recognition model | ECAPA-TDNN |
| `dataset` | Training or evaluation corpus | LibriTTS, Common Voice, Emilia |
| `evaluation` | Benchmark, metric, or evaluation toolkit | UTMOS, VoiceBench, MMAU |
| `ml-method` | General ML technique | Adam, flow matching, layer norm, FSQ |
| `survey` | Survey or overview paper | WavChat, "A Survey on Neural Speech Synthesis" |
| `multimodal` | Vision+speech or multi-task audio-language model | Qwen-Audio, SeamlessM4T |

`corpus_role` is `null` for standard keyword-filter papers.

## Review Queue Format (`raw/review_queue.md`)

The filter agent appends to this file for every paper with `relevance_score` between 0.40 and 0.70.

```markdown
## {id} | {title} | {venue} | score: {score}

**Authors:** {authors}
**Task guess:** {task}
**Reason for review:** {why the score is uncertain}
**Abstract excerpt:** {1–2 sentences}

**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)
```

After marking a decision, update the metadata JSON `status` field accordingly.
