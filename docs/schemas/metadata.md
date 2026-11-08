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
  "venue_type": "one of: conference | journal | workshop | preprint | technical-report",
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
  "url_peer_reviewed": "string or null — landing page for a later peer-reviewed version when url identifies the version summarized by the wiki page",
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
| `published_date` | **Canonical quarter date.** Before integration: `conference_date` if set, then `journal_date`, then `version_date`, otherwise `preprint_date`. After integration it is frozen at the value already copied into claim YAMLs. |

Rules:

1. **Peer-reviewed venues win before integration.** If the paper appeared at a conference or workshop,
   `published_date = conference_date`; if it appeared in a peer-reviewed journal,
   `published_date = journal_date`, even when an earlier preprint exists. A paper in both uses
   the conference date. This rule applies fully until the paper enters a canonical claim YAML.
2. **Claim membership freezes the quarter.** A paper is integrated when its canonical ID occurs
   in the `papers:` list of any top-level canonical `_claims/*.yaml` file. Once integrated,
   `published_date`, `year`, and `month` remain unchanged when a later peer-reviewed version is
   found. Still record `conference_date` or `journal_date`, update the venue fields, add
   `url_peer_reviewed`, and add the page note defined under “Duplicates and Later Versions.”
   Reconciliation runs, snapshots, reports, and rendered pages do not independently create a
   freeze. There is no `date_frozen` metadata field; claim membership is the authority.
3. **Otherwise the date of the version we ingest.** A preprint's content can change after v1
   (new evidence, rewrites), and snapshots must not credit later evidence to an earlier date, so
   `published_date = version_date`. Journal acceptance noted in `arxiv_comment` is a cue to look
   up the journal date (for example via Crossref).
4. **Only the version we hold counts.** Never use the arXiv "latest revision" date of a version we
   have not fetched, and never derive the date from the arXiv ID (IDs can lag the submission
   month). When we re-fetch or re-ingest a newer version, the new version is the one that counts:
   the date moves, and any frozen snapshot is corrected by explicit supersession, not edited.
5. **Pinning.** Fetchers record the version they harvest (`version_estimated: false`).
   `scripts/parse/download_pdfs.py` re-pins to the latest version at download. Records predating
   pinning were estimated by `scripts/apply_date_rule.py` as the latest version submitted on or
   before the local PDF's modification date, else `fetched_date` (`version_estimated: true`).
6. **Keep `year` and `month` in sync** with `published_date`.
7. **Precision.** A `-01` day means month-only precision (an Anthology volume month) unless the
   venue table in `scripts/fetch/acl.py` (`_CONF_META`) supplies the exact conference date, in
   which case the fetcher upgrades it.
8. **Do not edit by hand.** Set the supporting dates, then call the shared date-rule API with an
   explicit preserve-date decision from the migration or checking layer. Fetchers use the normal
   pre-integration path; only claim-membership-aware workflows may preserve an integrated date.
   `lib/arxiv_versions.pin_version` pins versions.
9. **Never changes the paper's content.** These are pipeline fields: correcting them is allowed
   under the "never alter source documents" invariant.

Ingested but not integrated records are migrated together with their paper pages and catalog rows.
Integrated records retain their claim-graph date while gaining the verified venue metadata and
peer-reviewed link. Health validation resolves claim membership from the explicit content checkout:
a mismatch with the normal date priority is valid only for an integrated record whose retained
`published_date`, `year`, and `month` agree with its paper page and claim entries.

## Status Lifecycle

```
pending   → filter agent assigns relevance score
review    → borderline (0.40–0.70): added to raw/review_queue.md for human decision
accepted  → score > 0.70 or human confirmed relevant: ready to ingest
rejected  → score < 0.40 or human confirmed irrelevant: skip
ingested  → wiki paper page written
```

## Duplicates and Later Versions

One paper has one page (AGENTS.md invariant 4). When two records describe the same work (an arXiv
preprint and its proceedings or journal version, possibly under a different title), the
non-canonical record gets:

- `is_duplicate: true`
- `canonical_id`: the canonical record's ID
- `status: rejected`
- a `relevance_note` sentence naming the version it duplicates

The canonical record keeps the relevance decision. Its `source_ids` may gain the duplicate's source
ID (for example `"openreview": "h5KLpGoqzC"`).

**Once a page exists, the ingested record stays canonical.** A later proceedings or journal record
is marked as a duplicate of the ingested record, whatever its venue, and the canonical record gains
the later source identifiers. The existing `url` continues to identify the version summarized by
the page; `url_peer_reviewed` points to the later version's authoritative landing page.

- **Before integration:** record the peer-reviewed venue and date, reapply the canonical date rule,
  and update the paper page and catalog. The paper may move quarters.
- **After integration:** record the same venue, date, source IDs, and link, but preserve
  `published_date`, `year`, and `month`. Claim YAMLs, reconciliation state, snapshots, and reports
  remain unchanged.

In both cases, add one short italic editorial note after the abstract callout. It names and links
the peer-reviewed version and states that the page, its metrics, and its claims summarize the
ingested version. The abstract card keeps `[→ Paper]({url})` and adds a separate
`[→ Peer-reviewed version]({url_peer_reviewed})` link. Log the change to `wiki/log.md` as `misc`.
Re-ingesting from the later version is a separate, explicit user decision.

**Exception: technical report and peer-reviewed paper.** When the ingested record is an industry
technical report and the later version is a peer-reviewed paper on the same system (same authors,
but substantially rewritten and extended), the two are treated as separate works: each gets its own
page dated by its own `published_date`, so each sits in its own quarter, neither is marked
`is_duplicate`, and each page's Wiki Connections links the other with a bullet that names the
relationship (technical report vs peer-reviewed version). Precedent: VibeVoice Technical Report
`2508.19205` (Q3 2025) and the ICLR 2026 paper `iclr-2026-FihSkzyxdv` (Q2 2026), user decision
2026-10-20. A plain camera-ready of an arXiv preprint is not an exception (VoxCPM).

**Before either version is ingested**, the existing source rules apply:

- ACL Anthology: the proceedings record is canonical (e.g. F5-TTS `2025.acl-long.313`, F-Actor
  `2026.findings-acl.242`).
- OpenReview (ICLR, NeurIPS, ICML): the arXiv record stays canonical, and the proceedings record is
  the duplicate.
- ISCA (Interspeech): the record already in the corpus stays canonical, whichever source it came
  from. The 2026-11-01 ISCA fetch kept existing arXiv records canonical; the 2026-11-07 arXiv top-up
  kept existing ISCA records canonical. The canonical record gains the duplicate's source ID; when
  an ISCA record gains `source_ids.arxiv`, also copy the arXiv `preprint_date`, `arxiv_version`,
  `version_date` and `version_estimated` (the metadata check requires them, and `published_date`
  stays on the conference date).

Detection: title-match every new batch against the whole corpus, then also check author overlap and
abstract similarity, because camera-ready versions are sometimes retitled (VoxCPM `2509.24650` was
published at ICLR 2026 as "Hierarchical Semantic-Acoustic Modeling via Semi-Discrete Residual
Representations ...").

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
