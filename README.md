# Speech Synthesis Research Wiki

A living systematic review of the state of the art in synthetic speech, covering **text-to-speech (TTS)**, **voice conversion (VC)**, and **spoken conversational agents (SCA)**. Papers are ingested on a rolling basis from arXiv, Interspeech, ACL/EMNLP/NAACL, and industry technical reports.

The wiki compiles structured paper pages, concept pages, comparison tables, and year-on-year trend analyses under `wiki/`. The raw corpus (metadata, PDFs, parsed text) lives under `raw/` and is never modified by wiki content generation.

See `CLAUDE.md` for the full schema and operating contract.

---

## Repository layout

```
raw/                  # Immutable source documents
  metadata/           # One JSON file per paper
  papers/             # Downloaded PDFs (not tracked in git)
  parsed/             # Extracted text and figures (not tracked in git)
  review_queue.md     # Borderline papers awaiting manual review

wiki/                 # LLM-maintained markdown knowledge base
  index.md            # Master catalog
  log.md              # Append-only operation log
  overview.md         # Evolving synthesis
  papers/             # One page per ingested paper
  concepts/           # Technology and method concept pages
  comparisons/        # Cross-paper comparison tables
  venues/             # Per-conference summaries
  trends/             # Longitudinal analysis pages

scripts/
  fetch/              # Fetchers: arXiv, ACL Anthology, Interspeech
  filter/             # Filter agent (assigns relevance scores)
  parse/              # PDF download and parsing pipeline
  discover/           # Citation discovery (citation index, corpus expansion)
  ingest/             # Wiki page generation (planned)

lib/                  # Shared library code
config/               # keyword_filter.yaml and parsing.yaml
docs/                 # Design documents
```

---

## Environment setup

**Prerequisite:** [uv](https://docs.astral.sh/uv/) — install once with:

```bash
brew install uv          # macOS
# or
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**One-time setup:**

```bash
git clone <repo-url>
cd speech-generation-wiki

# Create the virtual environment (uv downloads Python 3.12 automatically)
uv venv .venv --python 3.12

# Install all dependencies
uv pip install -r requirements.txt
```

**Activate the environment** (required at the start of every session):

```bash
source .venv/bin/activate
```

Your prompt will show `(.venv)` when the environment is active. All `python` and `python3` commands will then use the project's Python 3.12 interpreter with the installed packages.

**Deactivate** when done:

```bash
deactivate
```

---

## Adding or updating dependencies

```bash
# Install a new package and update requirements.txt
uv pip install <package-name>
uv pip freeze > requirements.txt

# Sync your environment to match requirements.txt exactly
uv pip install -r requirements.txt
```

Always commit `requirements.txt` after adding a dependency so other sessions reproduce the exact environment.

---

## Running scripts

All scripts are run from the **repository root** with the environment active:

```bash
source .venv/bin/activate   # if not already active
python scripts/fetch/arxiv.py --date-from 2026-05-22
```

### Script reference

| Script | Purpose |
|--------|---------|
| `scripts/fetch/arxiv.py` | Fetch arXiv papers (cs.SD, eess.AS) by date window |
| `scripts/fetch/arxiv_oai.py` | Bulk arXiv fetch via OAI-PMH (use for cs.CL) |
| `scripts/fetch/acl.py` | Fetch ACL Anthology papers (ACL, EMNLP, NAACL, workshops) |
| `scripts/fetch/isca.py` | Scrape Interspeech papers from ISCA Archive |
| `scripts/filter/agent.py` | Run filter agent — scores pending metadata files for relevance |
| `scripts/parse/download_pdfs.py` | Download PDFs for all accepted papers |
| `scripts/discover/citation_index.py` | Build out-of-corpus citation index from parsed references |

### Common fetch flags

```bash
# arXiv: specify date window (defaults to last 6 months)
python scripts/fetch/arxiv.py --date-from 2026-05-22 --date-to 2026-06-01

# arXiv OAI-PMH: specify category and window
python scripts/fetch/arxiv_oai.py --set cs.CL --date-from 2026-05-22

# ACL Anthology: fetch all 2025 venues including workshops
python scripts/fetch/acl.py --years 2025 --all-workshops

# PDF downloader: limit source or paper count
python scripts/parse/download_pdfs.py --source arxiv
python scripts/parse/download_pdfs.py --limit 10 --dry-run

# PDF downloader: adjust consecutive-error failsafe threshold
python scripts/parse/download_pdfs.py --max-errors 3
```

---

## Pipeline overview

```
1. FETCH      — scripts/fetch/          → raw/metadata/*.json  (status: pending)
2. FILTER     — scripts/filter/         → status: accepted | review | rejected
3. REVIEW     — manual (review_queue.md)→ status: accepted | rejected
4. DOWNLOAD   — scripts/parse/download_pdfs.py → raw/papers/*.pdf
5. PARSE      — scripts/parse/          → raw/parsed/*/full_text.md   [planned]
6. INGEST     — scripts/ingest/         → wiki/papers/*.md             [planned]
```

Each stage is independently resumable. Re-running any script skips work that is already done (files that exist, statuses already set).

---

## Corpus status

See `STATUS.md` for current counts and what is ready to run next.

---

## Environment variables

| Variable | Required by | Purpose |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | `scripts/filter/agent.py` | Claude API access for relevance scoring |

Set in your shell profile or a local `.env` file (never commit `.env`).

---

## Keeping the environment reproducible

- `requirements.txt` — exact pinned versions of all packages; commit after every dependency change
- `.python-version` — pins Python 3.12; `uv` reads this automatically when inside the project directory
- `.venv/` — not tracked in git; each environment is rebuilt from `requirements.txt`

To verify your environment matches the pinned versions exactly:

```bash
uv pip install -r requirements.txt
```

`uv` will report any packages that need updating and install them in seconds.
