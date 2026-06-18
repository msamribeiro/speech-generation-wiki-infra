# Fetch Stage

Discover candidate papers, assign relevance scores, and prepare accepted papers for parsing.

**Input:** external sources (arXiv, ACL Anthology, ISCA, OpenReview, citation graph)
**Output:** `raw/metadata/{id}.json` (status: accepted/rejected/review), `raw/papers/{id}.pdf`

See also: [docs/design/fetchers.md](design/fetchers.md), [docs/citation-discovery.md](citation-discovery.md), [docs/schemas/metadata.md](schemas/metadata.md)

---

## Fetch Scripts (`scripts/fetch/`)

| Script | Source | Notes |
|--------|--------|-------|
| `arxiv.py` | arXiv API (keyword search) | cs.SD, eess.AS, cs.CL |
| `arxiv_oai.py` | arXiv OAI-PMH (date range) | bulk harvest |
| `acl.py` | ACL Anthology | proceedings scrape |
| `isca.py` | ISCA archive | Interspeech, ASRU, SLT |
| `openreview.py` | OpenReview API | ICLR, NeurIPS |
| `citation_discovery_fetch.py` | `raw/citation_index.json` | citation-graph candidates |

Each fetcher writes `raw/metadata/{id}.json` with `status: pending` for new papers. Duplicates
(same arXiv ID or near-identical title) are skipped; check before adding to avoid re-ingesting.
Run `uv run scripts/discover/citation_index.py` after parse batches to rebuild `citation_index.json`.

---

## Filter Workflow

Run by the `speech-generation-filter-agent`. Processes all `status: pending` papers.

1. Read title and abstract from `raw/metadata/{id}.json`.
2. Assign `relevance_score` (0.0–1.0) based on fit to TTS / VC / SCA (see [vocabulary](schemas/vocabulary.md) for task definitions).
3. Write updated metadata:
   - `score > 0.70` → `status: accepted`
   - `score 0.40–0.70` → `status: review`; append to `raw/review_queue.md`
   - `score < 0.40` → `status: rejected`
4. Set `relevance_note` and `task` fields.
5. Log: `- filter | {source} | {N} accepted, {M} review, {K} rejected` to `raw/pipeline_log.md`.

**Review queue format** is defined in [docs/schemas/metadata.md](schemas/metadata.md#review-queue-format-rawreview_queuemd).
After marking a decision in the review queue, update the metadata JSON `status` field manually.

---

## Citation Discovery Workflow

Surfaces candidate papers from the corpus citation graph that are not yet in the corpus.

1. Read `raw/citation_index.json`.
2. Filter to `in_corpus: false` entries, sorted by `citation_count` descending.
3. Surface candidates cited by ≥3 corpus papers (or top 20 if fewer reach that threshold).
   For each: title, arXiv ID or DOI, citation count, citing corpus papers.
4. Present to user for approval. Approved candidates get a `raw/metadata/{id}.json` with
   `status: pending` and `discovery_source: citation-discovery`.
5. Run filter workflow on approved candidates. Foundational papers (WaveNet, VITS, HiFi-GAN,
   VALL-E, etc.) should score high regardless of publication date.
6. Set `ingest_tier` (1 = full page, 2 = lightweight stub) based on relevance and corpus role.
7. Log: `- discover | {N} candidates surfaced, {M} added as pending` to `raw/pipeline_log.md`.

---

## PDF Download

After filtering, download PDFs for all `status: accepted` papers that lack `pdf_path`:

```bash
source .venv/bin/activate
python scripts/parse/download_pdfs.py
```

Downloaded PDFs land in `raw/papers/`. The metadata field `pdf_path` is updated on success.
Failed downloads are recorded in `raw/download_log.jsonl`.

---

## pipeline_log.md Entries

All fetch-stage operations log to `raw/pipeline_log.md` (infra-facing, never rendered on site).
Entries go under a `## YYYY-MM-DD` section, newest section at top.

```
- filter | {source} | {N} accepted, {M} review, {K} rejected
- discover | {N} candidates surfaced, {M} added as pending
- review | {source} | {N} borderline resolved → {X} accepted, {Y} rejected
```
