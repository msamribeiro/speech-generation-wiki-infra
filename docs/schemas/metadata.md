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
  "published_date": "YYYY-MM-DD — canonical wiki date; conference_date, else journal_date, else version_date, else preprint_date (see Paper Dates)",
  "preprint_date": "YYYY-MM-DD or null — arXiv v1 submission date; null if no preprint",
  "arxiv_version": "int or null — arXiv version number of the content we fetched/downloaded",
  "version_date": "YYYY-MM-DD or null — submission date of that arXiv version (equals preprint_date for v1)",
  "version_estimated": "bool — true if the version was inferred from file/fetch dates, false if pinned at fetch or download",
  "conference_date": "YYYY-MM-DD or null — date of the peer-reviewed proceedings; null if not peer-reviewed or unknown",
  "journal_date": "YYYY-MM-DD — optional; first online publication date in a peer-reviewed journal (omit if not a journal paper)",
  "ingested_date": "YYYY-MM-DD or null — set on ingest",
  "generation_history": [
    {
      "schema_version": 2,
      "date": "YYYY-MM-DD",
      "op": "ingest | re-ingest | review | re-review | quality-pass",
      "agent": "speech-generation-ingest-agent | speech-generation-lightweight-ingest-agent | speech-generation-review-agent",
      "runtime": "claude-code | codex — execution surface",
      "provider": "anthropic | openai — model provider",
      "model": "string — exact model ID exposed by the runtime, or unknown",
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

Entries without `schema_version` are legacy version-1 provenance and remain valid. All new ingest,
re-ingest, review, and re-review entries use version 2. See
[generation.md](generation.md) for field semantics.

## Paper Dates

Each record logs supporting dates and one canonical date. Every date-dependent feature of the
wiki (quarter assignment, paper-page and claim-YAML `published_date`, snapshot eligibility,
temporal reports, corpus summaries) uses the canonical `published_date`.

| Field | Meaning |
|-------|---------|
| `preprint_date` | arXiv **v1** submission date. Null when the paper has no preprint. The priority date: when the idea first appeared. |
| `arxiv_version`, `version_date` | The arXiv version whose content we fetched and downloaded, and that version's submission date. Equal to v1 (`preprint_date`) when we have the original. `arxiv_version` is null when the fetch source does not expose it (OAI harvests). |
| `version_estimated` | `false` when the version was pinned at fetch or PDF download; `true` when inferred (see rule 4). |
| `conference_date` | Date of the peer-reviewed proceedings (conference or workshop) in which the paper appeared. Null when not peer reviewed, or when the date is unknown. |
| `journal_date` | Optional. First online publication date (Crossref `published-online`, or the journal site) in a peer-reviewed journal. Omit for non-journal papers. |
| `published_date` | **Canonical.** `conference_date` if set, then `journal_date`, then `version_date`, otherwise `preprint_date`. |

Rules:

1. **Peer-reviewed venues win.** If the paper appeared at a conference or workshop,
   `published_date = conference_date`; if it appeared in a peer-reviewed journal,
   `published_date = journal_date`, even when an earlier preprint exists. A paper in both uses
   the conference date.
2. **Otherwise the date of the version we ingest.** A preprint's content can change after v1
   (new evidence, rewrites), and snapshots must not credit later evidence to an earlier date, so
   `published_date = version_date`. Journal acceptance noted in `arxiv_comment` is a cue to look
   up the journal date (for example via Crossref).
3. **Only the version we hold counts.** Never use the arXiv "latest revision" date of a version we
   have not fetched, and never derive the date from the arXiv ID (IDs can lag the submission
   month). When we re-fetch or re-ingest a newer version, the new version is the one that counts:
   the date moves, and any frozen snapshot is corrected by explicit supersession, not edited.
4. **Pinning.** Fetchers record the version they harvest (`version_estimated: false`).
   `scripts/parse/download_pdfs.py` re-pins to the latest version at download. Records predating
   pinning were estimated by `scripts/apply_date_rule.py` as the latest version submitted on or
   before the local PDF's modification date, else `fetched_date` (`version_estimated: true`).
5. **Keep `year` and `month` in sync** with `published_date`.
6. **Precision.** A `-01` day means month-only precision (an Anthology volume month) unless the
   venue table in `scripts/fetch/acl.py` (`_CONF_META`) supplies the exact conference date, in
   which case the fetcher upgrades it.
7. **Do not edit by hand.** Set the supporting dates, then call
   `lib/paper_dates.apply_date_rule(record)`, which derives `published_date`, `year`, and `month`.
   Fetchers do this; `lib/arxiv_versions.pin_version` pins versions;
   `scripts/apply_date_rule.py` is the batch migration.
8. **Never changes the paper's content.** These are pipeline fields: correcting them is allowed
   under the "never alter source documents" invariant.

Ingested records: wiki paper pages and claim YAML copy `published_date`, and frozen snapshots
depend on it, so ingested records are migrated only together with their pages (tracked in
`BACKLOG.md`). Until then `scripts/health_check.py --module metadata` counts them as legacy and
reports rule deviations as warnings; non-ingested records (`pending`, `review`, `accepted`)
violating the rule are errors.

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
