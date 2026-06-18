# Fetcher Pipeline — Design Document

**Project:** Speech Synthesis Research Wiki  
**Scope:** Data acquisition layer — discovery, retrieval, deduplication, and PDF resolution  
**Status:** Implemented (arXiv cs.SD/eess.AS, arXiv cs.CL via OAI-PMH, ACL Anthology, Interspeech) — OpenReview and IEEE Xplore remain at design stage

---

## 1. Goals and Non-Goals

### Goals
- Automatically discover and retrieve metadata and PDFs for papers relevant to TTS, VC, and SCA published in the last 6 months (rolling window)
- Cover all primary target venues: Interspeech, ICASSP, ACL/EMNLP/NAACL, NeurIPS, ICLR, ICML, and arXiv preprints including technical reports
- Produce one well-formed `raw/metadata/{id}.json` per paper, ready for the filter agent
- Minimise manual effort while respecting source terms of service and rate limits
- Be re-runnable: safe to execute again after a week to pick up new papers without creating duplicates

### Non-Goals
- Full-text indexing or search (that is the wiki layer's job)
- Paying for or circumventing paywalled access (IEEE full-text)
- Automated ingestion into the wiki (fetchers only populate `raw/`, ingestion is a separate step)
- Scraping author homepages or project pages

---

## 2. Source Landscape and Challenges

Each source has a different access model, data quality, and set of constraints. The table below summarises the key dimensions:

| Source | Metadata API | Full-text access | Rate limits | ToS sensitivity | Coverage of target domain |
|--------|-------------|-----------------|-------------|-----------------|--------------------------|
| arXiv | ✅ Official API | ✅ Open PDFs | Moderate (3 req/s) | Low | Very high (cs.SD, eess.AS) |
| ACL Anthology | ✅ Bulk JSON | ✅ Open PDFs | None (bulk download) | Low | High (ACL, EMNLP, NAACL) |
| OpenReview | ✅ Official API | ✅ Open PDFs | Low | Low | Medium (NeurIPS, ICLR, ICML) |
| ISCA Archive (Interspeech) | ❌ HTML only | ⚠️ Gated per-click | Low-medium | Medium | Very high |
| IEEE Xplore (ICASSP) | ⚠️ Metadata API only | ❌ Institutional only | Strict | High | Very high |
| Semantic Scholar | ✅ Official API | ⚠️ Open access only | 100 req/5 min | Low | Cross-venue, useful for dedup |

### 2.1 arXiv

**Challenge — no venue tags in metadata:** arXiv does not record conference acceptance. A paper submitted to Interspeech 2025 may list `cs.SD` as its category but there is no structured `venue` field. Venue must be inferred from the paper's `comment` field (authors often write "Accepted at Interspeech 2025") or from cross-referencing against proceedings metadata from other sources.

**Challenge — category breadth:** `cs.SD` and `eess.AS` contain audio source separation, music, acoustic modelling, and speech recognition papers alongside TTS/VC. Filtering by category alone gives high recall but low precision. Keyword filtering on title and abstract is required as a second pass.

**Challenge — version drift:** arXiv papers are versioned. A paper posted as v1 in June may have a substantially different v3 by December. The fetcher must always retrieve the latest version's metadata while preserving the original submission date for timeline accuracy.

**Solution:** Use the arXiv API with category + date filters for discovery, then apply a keyword filter on title/abstract. Store arXiv ID as the canonical identifier. Record `published_date` from the `submitted` field (v1 date) and note the latest version separately.

### 2.2 ACL Anthology

**Challenge — none significant:** The Anthology publishes a bulk JSON dump of all proceedings at `https://aclanthology.org/anthology+abstracts.json.gz`. It is updated regularly, covers all ACL venues, and includes abstracts, author lists, PDFs, and DOIs. This is the cleanest source in the pipeline.

**Challenge — scope creep:** The Anthology includes speech recognition, parsing, summarisation, and many other NLP tasks. Filtering to TTS/VC/SCA requires a keyword pass on title and abstract.

**Solution:** Download the bulk JSON, filter by venue code (ACL, EMNLP, NAACL, and their workshops prefixed with `W-`) and publication year, then apply keyword filter. PDF URLs are embedded in the JSON.

### 2.3 OpenReview (NeurIPS, ICLR, ICML)

**Challenge — venue and track structure:** OpenReview organises submissions by invitation ID, which encodes the venue and year (e.g. `NeurIPS.cc/2025/Conference`). Accepted papers have a `decision` note with value `Accept`. Withdrawn and rejected papers are also present and must be excluded.

**Challenge — NeurIPS workshop papers:** NeurIPS has many workshops, some of which (e.g. NeurIPS 2025 Workshop on Machine Learning for Audio) are highly relevant. These have separate invitation IDs and must be opted into explicitly.

**Solution:** Use the OpenReview Python client with venue-specific invitation IDs. Filter for `decision: Accept`. Retrieve abstract and PDF URL from the forum notes.

### 2.4 ISCA Archive (Interspeech)

**Challenge — no API:** The ISCA archive (`isca-speech.org/archive`) serves proceedings as HTML pages, one per paper, with a consistent but non-machine-readable structure. There is no bulk metadata endpoint.

**Challenge — PDF access:** PDFs are served from the ISCA server and require a click-through per paper. There is no bulk download facility. Aggressive downloading would strain a small academic server and is contrary to good practice.

**Solution — two-stage:**
1. Scrape the proceedings index page (one HTML page listing all papers with title, authors, and abstract) to build metadata records. This is a single lightweight request per proceedings volume.
2. For PDFs: attempt to resolve each paper to an arXiv preprint via title matching (Semantic Scholar API or direct arXiv search). If found, use the arXiv PDF. If not, flag the paper in a `needs_manual_pdf` list for a single batch download session. Estimate: 60–70% of relevant Interspeech TTS papers have arXiv preprints.

### 2.5 IEEE Xplore (ICASSP)

**Challenge — full-text paywall:** IEEE Xplore requires institutional credentials for PDF access. This is a hard constraint. The IEEE Xplore API allows metadata retrieval (title, authors, abstract, DOI) for up to 200 results per query with a free API key, but explicitly prohibits bulk downloading in its ToS.

**Challenge — API result limits:** The free IEEE Xplore API returns at most 200 records per query and has a rate limit of 200 requests per day. ICASSP 2025 had approximately 4,000 accepted papers total; the relevant subset (TTS/VC/SCA) is perhaps 80–150 papers, comfortably within limits if queries are well-targeted.

**Solution — two-stage:**
1. Use the IEEE Xplore metadata API with targeted keyword queries (e.g. `"text-to-speech" OR "voice conversion" OR "speech synthesis"`) scoped to the ICASSP publication code. Retrieve metadata only.
2. For PDFs: same arXiv resolution strategy as Interspeech. ICASSP authors in the TTS field are very likely to post arXiv preprints. Flag non-resolved papers for manual collection.

### 2.6 Deduplication

**Challenge:** The same paper typically appears in multiple sources. A paper accepted at Interspeech 2025 may exist as: an arXiv preprint (with arXiv ID), an ISCA proceedings entry (with ISCA ID), and a Semantic Scholar record (with S2 ID). Without deduplication, the same paper gets multiple metadata files and potentially multiple wiki pages.

**Solution — deduplication key hierarchy:**
1. **arXiv ID** — if a paper has an arXiv ID, that is the canonical ID. All other source records for the same paper should be merged into this record, enriching it with venue information.
2. **DOI** — if no arXiv ID, use the DOI as the merge key.
3. **Title fingerprint** — if neither, compute a normalised title (lowercase, strip punctuation, strip stop words) and use fuzzy matching (token sort ratio ≥ 0.92) to detect duplicates.

The deduplication step runs after all fetchers have completed but before the filter agent. It merges records and sets the canonical `id`.

---

## 3. Generic Fetcher Workflow

All four fetchers share a common structure. Each is an independent Python script that:

1. **Discovers** papers matching venue + date criteria
2. **Filters** by relevance keywords on title and abstract (coarse pass)
3. **Resolves** PDFs where possible
4. **Writes** one metadata JSON per paper to `raw/metadata/`
5. **Logs** a summary to stdout and to `raw/fetch_log.jsonl`

```
┌─────────────────────────────────────────────────────────┐
│                    Fetcher (per source)                  │
│                                                         │
│  1. DISCOVER       Query API / scrape index             │
│       │            → list of (title, authors, url, ...)  │
│       ▼                                                 │
│  2. COARSE FILTER  Keyword match on title + abstract    │
│       │            → discard clearly irrelevant papers  │
│       ▼                                                 │
│  3. RESOLVE PDF    arXiv ID → arXiv PDF                 │
│       │            DOI → Unpaywall → open PDF           │
│       │            title → arXiv search → PDF           │
│       │            else → flag as needs_manual_pdf      │
│       ▼                                                 │
│  4. WRITE          raw/metadata/{id}.json               │
│       │            status: pending                      │
│       ▼                                                 │
│  5. LOG            raw/fetch_log.jsonl                  │
└─────────────────────────────────────────────────────────┘
```

After all fetchers run:

```
┌─────────────────────────────────────────────────────────┐
│                  Post-fetch Pipeline                     │
│                                                         │
│  6. DEDUPLICATE    scripts/parse/merge_records.py        │
│       │            → canonical ID assignment            │
│       │            → duplicate metadata files removed   │
│       ▼                                                 │
│  7. PDF RESOLUTION scripts/parse/resolve_pdfs.py        │
│       │            → fills pdf_path where missing       │
│       │            → outputs needs_manual_pdf.txt       │
│       ▼                                                 │
│  8. FILTER AGENT   LLM relevance scoring                │
│       │            → status: accepted / review / rejected│
│       │            → appends to review_queue.md         │
│       ▼                                                 │
│  9. HUMAN REVIEW   review_queue.md                      │
│       │            → marks decisions                    │
│       ▼                                                 │
│ 10. INGEST AGENT   wiki population (separate pipeline)  │
└─────────────────────────────────────────────────────────┘
```

---

## 3.5 Repository Structure

Scripts live under `scripts/` grouped by pipeline stage. Shared logic lives in `lib/`.

```
scripts/
  fetch/          # One script per data source
    arxiv.py      # arXiv search API (cs.SD, eess.AS)
    arxiv_oai.py  # arXiv OAI-PMH bulk harvest (cs.CL and large categories)
    acl.py        # ACL Anthology via GitHub XML
    isca.py       # Interspeech via ISCA HTML scraper
    openreview.py # NeurIPS / ICLR / ICML (design stage)
    ieee.py       # ICASSP via IEEE Xplore API (design stage)
  filter/
    agent.py      # Standalone LLM filter (requires ANTHROPIC_API_KEY)
  parse/          # Planned: PDF download, parsing, assembly
  ingest/         # Planned: wiki page generation

lib/
  keyword_filter.py  # load_keyword_filter(), passes_filter() — shared by all fetchers
```

All scripts resolve paths relative to `Path(__file__).parent.parent.parent` (the project root) and prepend the project root to `sys.path` so that `from lib.keyword_filter import ...` works when invoked as `python scripts/fetch/arxiv.py` from the project root.

---

## 4. Preliminary Data Structures

### 4.1 Raw Metadata Record (`raw/metadata/{id}.json`)

```python
@dataclass
class PaperMetadata:
    # Identity
    id: str                     # canonical ID (arXiv ID preferred)
    source_ids: dict            # {"arxiv": "2501.12345", "isca": "interspeech25-0412", "doi": "10.21437/..."}
    title: str
    authors: list[str]
    organization: str | None    # primary affiliation if detectable

    # Venue
    venue: str                  # controlled vocabulary (see CLAUDE.md)
    venue_type: str             # conference | workshop | preprint | technical-report
    year: int
    month: int
    published_date: str         # YYYY-MM-DD (arXiv v1 date or proceedings date)

    # Access
    url: str                    # canonical URL (arXiv abstract page or proceedings page)
    pdf_url: str | None         # direct PDF URL if resolved
    pdf_path: str | None        # local path after download (raw/papers/{id}.pdf)
    pdf_source: str | None      # "arxiv" | "anthology" | "openreview" | "manual"

    # Content
    abstract: str | None
    task: list[str]             # filled by filter agent; empty at fetch time
    relevance_score: float | None  # filled by filter agent
    relevance_note: str | None

    # Lifecycle
    status: str                 # pending | review | accepted | rejected | ingested
    fetched_date: str           # YYYY-MM-DD
    ingested_date: str | None   # YYYY-MM-DD, set on wiki ingest

    # Flags
    needs_manual_pdf: bool      # True if PDF could not be auto-resolved
    is_duplicate: bool          # True if merged into another record
    canonical_id: str | None    # set if is_duplicate, points to the primary record
```

### 4.2 Fetch Log Entry (`raw/fetch_log.jsonl`)

One JSON line per fetch run per source:

```python
@dataclass
class FetchLogEntry:
    timestamp: str              # ISO 8601
    source: str                 # "arxiv" | "acl" | "openreview" | "isca" | "ieee"
    venue: str | None           # e.g. "Interspeech 2025"
    query: str | None           # the query or filter used
    discovered: int             # papers found before keyword filter
    after_keyword_filter: int   # papers remaining after coarse keyword pass
    written: int                # new metadata files written
    skipped_existing: int       # already had a metadata file
    errors: list[str]           # any retrieval errors
    needs_manual_pdf_count: int
```

### 4.3 Keyword Filter Configuration (`config/keyword_filter.yaml`)

```yaml
# Coarse keyword filter applied at fetch time (title + abstract)
# A paper passes if it matches at least one term in any include group
# and none of the terms in the exclude list

include:
  core:
    - "text-to-speech"
    - "speech synthesis"
    - "voice conversion"
    - "speech generation"
    - "TTS"
    - "neural vocoder"
    - "voice cloning"
  conversational:
    - "spoken dialogue"
    - "conversational speech"
    - "speech language model"
    - "spoken language model"
    - "speech LM"
  codec:
    - "neural audio codec"
    - "speech codec"
    - "audio tokenizer"
    - "EnCodec"
    - "SoundStream"
  related:
    - "zero-shot speaker"
    - "speaker adaptation"
    - "prosody"
    - "paralinguistic"
    - "singing voice synthesis"

exclude:
  # Terms that indicate a paper is primarily about something else
  - "speech recognition"       # ASR-only papers
  - "automatic speech recognition"
  - "speaker diarization"
  - "source separation"
  - "music transcription"
  - "keyword spotting"

# Minimum: title must match at least one include term
# OR abstract must match at least two include terms (looser for abstract)
title_min_matches: 1
abstract_min_matches: 2
```

### 4.4 PDF Resolution Chain (`scripts/parse/resolve_pdfs.py`)

```python
def resolve_pdf(record: PaperMetadata) -> tuple[str | None, str]:
    """
    Attempts to find an open PDF for a paper.
    Returns (pdf_url, source) or (None, "unresolved").
    
    Resolution order:
    1. arXiv ID already known → use arXiv PDF directly
    2. DOI known → try Unpaywall API (free, no auth required)
    3. Title search on arXiv → fuzzy match, use if confidence > 0.92
    4. Semantic Scholar open access link
    5. Give up → flag needs_manual_pdf = True
    """
    
    # 1. arXiv
    if arxiv_id := record.source_ids.get("arxiv"):
        url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        return url, "arxiv"

    # 2. Unpaywall (uses DOI, returns open access PDF URL if available)
    if doi := record.source_ids.get("doi"):
        url = unpaywall_lookup(doi)   # calls api.unpaywall.org/v2/{doi}
        if url:
            return url, "unpaywall"

    # 3. arXiv title search
    candidates = arxiv_title_search(record.title)
    for candidate in candidates:
        score = token_sort_ratio(normalise(record.title), normalise(candidate.title))
        if score >= 92 and authors_overlap(record.authors, candidate.authors):
            record.source_ids["arxiv"] = candidate.arxiv_id
            return f"https://arxiv.org/pdf/{candidate.arxiv_id}.pdf", "arxiv_via_title"

    # 4. Semantic Scholar
    s2_url = semantic_scholar_oa_lookup(record.title, record.authors)
    if s2_url:
        return s2_url, "semantic_scholar"

    # 5. Unresolved
    record.needs_manual_pdf = True
    return None, "unresolved"
```

---

## 5. Per-Fetcher Design

### 5.1 `scripts/fetch/arxiv.py`

**Status: Implemented and run.**

**API:** `http://export.arxiv.org/api/query` (Atom feed, no auth required)  
**Rate limit:** 1 request per 3 seconds (enforced by `time.sleep`)  
**Coverage:** arXiv preprints in `cs.SD` and `eess.AS` (audio/speech-focused categories)

**Note — cs.CL:** The search API throttles aggressively on large category queries. Use `scripts/fetch/arxiv_oai.py` (§5.2) for cs.CL harvesting instead.

**CLI:**
```
python scripts/fetch/arxiv.py
python scripts/fetch/arxiv.py --date-from 2025-08-01
python scripts/fetch/arxiv.py --date-from 2026-05-22 --dry-run
```

**First run results (anchored at 2025-08-01, run May 2026):**
- 3,566 papers discovered across cs.SD and eess.AS
- 504 papers passed the keyword filter
- 0 fetch errors

**Known edge cases:**
- Papers with very long author lists (some Google papers have 20+ authors) — truncate to first 10, store full list in `authors_full`
- arXiv API occasionally returns malformed Atom — each record parse is wrapped in try/except

### 5.2 `scripts/fetch/arxiv_oai.py`

**Status: Implemented and run.**

**API:** `https://export.arxiv.org/oai2` (OAI-PMH bulk harvest, no auth required)  
**Rate limit:** Minimum 5 seconds between requests (arXiv OAI-PMH policy, enforced by `time.sleep`)  
**Coverage:** Any arXiv category via OAI-PMH set identifiers; designed for large categories like `cs.CL` where the search API hits aggressive rate limits

**Key differences from `arxiv.py`:** Uses resumption tokens instead of offset pagination — no large-query timeouts, no 429 storms. OAI-PMH set identifiers use colon-separated hierarchy (`cs:cs:CL`); the CLI accepts the familiar dot notation (`cs.CL`) and converts automatically.

**CLI:**
```
python scripts/fetch/arxiv_oai.py --set cs.CL --date-from 2026-05-22
python scripts/fetch/arxiv_oai.py --set cs.CL --date-from 2025-12-01 --date-to 2026-02-28 --dry-run
python scripts/fetch/arxiv_oai.py --set cs.CL --resume-token <token>   # resume interrupted run
```

**cs.CL harvest results (Aug 2025 – May 2026, run May 2026):**

| Window | Records scanned | Passed filter | Written | Skipped (existing) |
|--------|----------------|--------------|---------|-------------------|
| 2025-08-01 → 2025-11-30 | 9,461 | 119 | 41 | 78 |
| 2025-12-01 → 2026-02-28 | 6,857 | 65 | 32 | 33 |
| 2026-03-01 → 2026-05-22 | 9,752 | 96 | 42 | 54 |
| **Total** | **26,070** | **280** | **115** | **165** |

**Known edge cases:**
- Deleted records (OAI-PMH `status=deleted`) are silently skipped
- Some records have `created` date missing; falls back to OAI-PMH datestamp for year/month

### 5.3 `scripts/fetch/acl.py`

**Status: Implemented and run.** See `scripts/fetch/acl.py`.

**API:** Per-venue XML files from the ACL Anthology GitHub repository  
**Rate limit:** 0.5 s between XML downloads; GitHub tree API for workshop discovery  
**Coverage:** ACL, EMNLP, NAACL (main + findings + all co-located workshops)  
**Cache:** `raw/anthology_xml_cache/`, refreshed if >7 days old

**Key design decisions:**
- **XML not bulk JSON** — the historical `anthology+abstracts.json.gz` endpoint no longer exists; this fetcher uses per-venue XML files at `https://raw.githubusercontent.com/acl-org/acl-anthology/master/data/xml/{year}.{venue}.xml`. Workshop XMLs are discovered via the GitHub git-tree API in a single call.
- **Findings papers included** — `findings-acl`, `findings-emnlp`, `findings-naacl` are peer-reviewed and treated as `venue_type: conference`.
- **Prefer peer-reviewed over preprint** — when an Anthology title matches an existing arXiv record by normalised title, the arXiv record is enriched in place: `venue`, `venue_type`, `doi`, and `pdf_url` (camera-ready) are updated. The arXiv ID remains the canonical ID. Records with `status: ingested` are skipped with a warning.

**CLI:**
```
python scripts/fetch/acl.py
python scripts/fetch/acl.py --years 2024 2025
python scripts/fetch/acl.py --all-workshops
python scripts/fetch/acl.py --dry-run
python scripts/fetch/acl.py --no-cache   # force re-download of all XML files
```

**2025 run results (May 2026):**
- 14,669 papers scanned (main venues + 182 workshops)
- 129 passed keyword filter; 113 written as new records, 16 enriched existing arXiv records

**Known edge cases:**
- Some entries have no abstract — title-only filter check falls back to `abstract_min_matches` ≥ 2
- Workshop XMLs not yet published return 404 and are silently skipped

### 5.4 `scripts/fetch/openreview.py`

**API:** OpenReview Python client (`pip install openreview-py`)  
**Rate limit:** Generous; 1 req/s is safe  
**Coverage:** NeurIPS, ICLR, ICML and their workshops

```python
def fetch_openreview(
    venues: list[dict],             # [{"id": "NeurIPS.cc/2025/Conference", "year": 2025, "name": "NeurIPS"}, ...]
    output_dir: Path = RAW_METADATA,
) -> FetchLogEntry:
    """
    Uses openreview.Client (no auth needed for public venues).
    Retrieves all submissions, then filters to accepted papers only
    by checking for an Accept decision note.
    Applies keyword filter. PDF URLs are embedded in notes.
    
    Notes:
    - Decision notes are separate from submission notes; must join on forum ID
    - Some venues use "Accept (Poster)" / "Accept (Oral)" — treat all Accept variants as accepted
    - Workshop invitation IDs vary by year; maintain a lookup table in config
    - OpenReview PDFs are served at openreview.net/pdf?id={forum_id}
    """
```

**Known edge cases:**
- NeurIPS 2025 workshop for ML+Audio may not be on OpenReview — check ISCA or the workshop website
- Withdrawn papers still appear in the API with a Withdraw note — exclude explicitly
- ICLR has "Spotlight" and "Oral" decision values in addition to "Poster" — all are accepted

### 5.5 `scripts/fetch/isca.py`

**Status: Implemented and run.**

**Source:** HTML at `https://www.isca-archive.org/interspeech_{year}/`  
**Rate limit:** 2 s between individual paper page fetches  
**Coverage:** Interspeech proceedings metadata

**Two-stage strategy:**
1. Scrape the proceedings index (one page) to collect all paper slugs, titles, and authors.
2. For papers passing the *title-only* keyword pre-filter, fetch each individual paper page to retrieve the abstract and DOI. Apply the full title+abstract filter only at this stage.

**CLI:**
```
python scripts/fetch/isca.py --year 2025
python scripts/fetch/isca.py --year 2025 --dry-run
```

**2025 run results:** 128 papers written.

**Known edge cases:**
- DOI extraction uses regex on full page text (`10.21437/Interspeech.{year}-{seq}`); papers without a DOI get a slug-based ID
- `pdf_url` is stored from the ISCA server for later resolution via `scripts/parse/resolve_pdfs.py`
- ISCA ID stored in `source_ids["isca"]`

### 5.6 `scripts/fetch/ieee.py` *(design stage)*

**API:** `https://ieeexploreapi.ieee.org/api/v1/search/articles`  
**Auth:** Free API key (register at developer.ieee.org)  
**Rate limit:** 200 requests/day, 200 results/request  
**Coverage:** ICASSP proceedings metadata only; PDFs resolved separately

```python
def fetch_icassp(
    years: list[int],
    api_key: str,                   # from environment variable IEEE_API_KEY
    output_dir: Path = RAW_METADATA,
) -> FetchLogEntry:
    """
    Queries IEEE Xplore with targeted keyword searches scoped to ICASSP.
    Uses publication_title="ICASSP" as a filter parameter.
    Retrieves: title, authors, abstract, DOI, article number.
    Applies keyword filter. Does NOT download PDFs.
    
    Query strategy:
    - Run separate queries per keyword cluster to stay within 200-result pages:
        "text-to-speech OR speech synthesis OR neural vocoder"
        "voice conversion OR speaker adaptation OR zero-shot speaker"
        "speech generation OR spoken language model"
    - Deduplicate results across queries by DOI before writing
    
    Notes:
    - IEEE article numbers become source_ids["ieee"]
    - DOI stored in source_ids["doi"] for Unpaywall resolution
    - ToS: metadata retrieval is permitted; bulk PDF downloading is not
    """
```

---

## 6. Post-Fetch Scripts

### 6.1 `scripts/parse/merge_records.py`

Runs after all fetchers. Deduplicates across sources using the key hierarchy defined in Section 2.6.

```python
def merge_records(metadata_dir: Path) -> MergeReport:
    """
    Loads all metadata JSON files.
    Groups by arXiv ID → DOI → title fingerprint.
    For each group with >1 record:
      - Selects the record with the most complete information as primary
      - Merges source_ids from all records into the primary
      - Sets is_duplicate=True and canonical_id on secondary records
      - Enriches primary with venue info from secondary (e.g. adds venue="Interspeech"
        to an arXiv record that was also found in the ISCA scrape)
    Returns a MergeReport with counts and a list of merged pairs.
    """
```

### 6.2 `scripts/parse/resolve_pdfs.py`

Attempts to fill `pdf_url` for all records where `pdf_path` is None, using the resolution chain in Section 4.4. Downloads confirmed PDFs to `raw/papers/`.

```python
def resolve_and_download(
    metadata_dir: Path,
    papers_dir: Path,
    email: str,              # required by Unpaywall API (identifies requester)
    dry_run: bool = False,   # if True, resolve URLs but do not download
) -> ResolutionReport:
    """
    For each accepted/pending record without a pdf_path:
      1. Run resolve_pdf() to get a URL
      2. Download the PDF to raw/papers/{id}.pdf
      3. Update the metadata JSON with pdf_path and pdf_source
    Outputs needs_manual_pdf.txt listing all unresolved papers.
    """
```

### 6.3 `needs_manual_pdf.txt` (output)

A plain text file listing papers that could not be auto-resolved, formatted for a human batch download session:

```
# Papers requiring manual PDF download
# For each: visit the URL, download the PDF, save to raw/papers/{id}.pdf,
# then run: python scripts/parse/update_pdf_path.py {id} raw/papers/{id}.pdf

[interspeech-2025-0198]
Title: Some Paper Without arXiv Preprint
URL: https://www.isca-archive.org/interspeech_2025/...
DOI: 10.21437/Interspeech.2025-198
Save as: raw/papers/interspeech-2025-0198.pdf

[icassp-2025-0471]
Title: Another Paper
URL: https://ieeexplore.ieee.org/document/...
DOI: 10.1109/ICASSP.2025...
Save as: raw/papers/icassp-2025-0471.pdf
```

---

## 7. Configuration and Environment

All fetchers read from a shared `config/pipeline.yaml`:

```yaml
# Date window (rolling — update date_from periodically)
date_from: "2024-11-01"
date_to: null               # null = today

# Target venues per fetcher
arxiv:
  categories: ["cs.SD", "eess.AS", "cs.CL"]

acl:
  venues: ["ACL", "EMNLP", "NAACL", "findings-ACL", "findings-EMNLP"]
  years: [2024, 2025]

openreview:
  venues:
    - id: "NeurIPS.cc/2025/Conference"
      name: "NeurIPS"
      year: 2025
    - id: "ICLR.cc/2025/Conference"
      name: "ICLR"
      year: 2025
    - id: "ICML.cc/2025/Conference"
      name: "ICML"
      year: 2025

interspeech:
  years: [2024, 2025]

icassp:
  years: [2024, 2025]

# PDF resolution
unpaywall_email: "your@email.com"   # required by Unpaywall ToS

# Paths
raw_dir: "raw"
metadata_dir: "raw/metadata"
papers_dir: "raw/papers"

# Rate limiting (seconds between requests)
rate_limits:
  arxiv: 3.0
  isca: 2.0
  ieee: 1.0
  openreview: 1.0
  semantic_scholar: 1.0
```

Environment variables (never stored in config files):
```
IEEE_API_KEY=...
SEMANTIC_SCHOLAR_API_KEY=...   # optional; raises rate limits substantially
```

---

## 8. Running Order and Estimated Output

For an initial window across all target venues, running the full pipeline once:

| Step | Script | Status | Est. runtime | Actual (Aug 2025 – May 2026) |
|------|--------|--------|-------------|-------------------------------|
| Fetch arXiv cs.SD/eess.AS | `scripts/fetch/arxiv.py` | ✅ Done | 10–20 min | 3,566 → 504 after filter |
| Fetch arXiv cs.CL (OAI-PMH) | `scripts/fetch/arxiv_oai.py` | ✅ Done | 20–40 min | 26,070 scanned → 115 written |
| Fetch ACL Anthology | `scripts/fetch/acl.py` | ✅ Done | 2–5 min | 14,669 → 113 written, 16 enriched |
| Fetch Interspeech | `scripts/fetch/isca.py` | ✅ Done | 5–10 min | 128 written |
| Fetch OpenReview | `scripts/fetch/openreview.py` | ⏳ Not started | 5–10 min | — |
| Fetch ICASSP | `scripts/fetch/ieee.py` | ⏳ Not started | 5–10 min | — |
| Merge/deduplicate | `scripts/parse/merge_records.py` | ⏳ Not started | < 1 min | — |
| Resolve PDFs | `scripts/parse/resolve_pdfs.py` | ⏳ Not started | 20–40 min | — |
| Manual PDF session | human | ⏳ Not started | 1–2 hours | — |
| Filter agent | `speech-generation-filter-agent` (Claude Code subagent) | ✅ Done | 30–90 min | 732 accepted, 167 rejected |
| Human review | human | ✅ Done | 60–90 min | 70 borderline resolved → 40 accepted, 30 rejected |

**Corpus status (May 2026):** 732 papers accepted, 167 rejected, 0 pending. Ready for PDF resolution and ingest.

### Filter agent note

Filtering is done via the `speech-generation-filter-agent` Claude Code subagent (`.claude/agents/speech-generation-filter-agent.md`). Invoke it from a Claude Code session whenever papers with `status: pending` need scoring. No separate API key required beyond the Claude Code subscription.

---

## 9. Open Questions

The following decisions are deferred pending feedback:

1. **Semantic Scholar API key:** Registration is free and raises the rate limit from 100 req/5min to ~1 req/s. Worth the 5-minute sign-up given its role in PDF resolution. Recommend: yes.

2. **ASRU / SLT coverage:** These IEEE speech conferences are smaller and more focused on recognition than synthesis. Worth including for VC and evaluation papers. The same `scripts/fetch/ieee.py` IEEE Xplore approach covers them.

3. **Workshop granularity:** Should workshops at NeurIPS/ICLR be included by default, or only if a paper fails to appear in the main proceedings? Recommend: include ICASSP-SPGC, Interspeech satellite workshops, and NeurIPS ML4Audio by default; others on request.

4. **Re-run cadence:** How often to re-run the fetchers for new arXiv preprints? Weekly is reasonable for a rolling review. A simple cron job or GitHub Action could automate this.

5. **Version pinning for arXiv:** Should the fetcher always pull the latest version of an arXiv paper, or pin to v1 to preserve the state at time of discovery? Recommend: store v1 date in `published_date`, always download latest PDF, and store latest version number in metadata.
