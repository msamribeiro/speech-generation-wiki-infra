# Speech Synthesis Research Wiki

![Speech Generation Wiki](wiki/assets/speech-generation-wiki.png)

A living systematic review of the state of the art in synthetic speech, covering **text-to-speech (TTS)**, **voice conversion (VC)**, and **spoken conversational agents (SCA)**. Papers are ingested on a rolling basis from arXiv, Interspeech, ACL/EMNLP/NAACL, and industry technical reports.

The wiki compiles structured paper pages, concept pages, comparison tables, and periodic field reports under `wiki/`. The raw corpus (metadata, PDFs, parsed text) lives under `raw/` and is never modified by wiki content generation.

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
  index.md            # Landing page — concept navigation and entry points
  overview.md         # Evolving synthesis of dominant paradigms and trends
  log.md              # Reverse-chronological reader-facing changelog
  papers/             # One page per ingested paper
    index.md          # Full paper catalog
  concepts/           # Technology and method concept pages
    index.md          # Concept directory
    _evidence/        # Concept evidence digests (YAML; used for scalable synthesis)
  comparisons/        # Cross-paper comparison tables
  venues/             # Per-conference summaries (named {year}-{venue})
  reports/            # Periodic field reports (monthly, quarterly, yearly)

scripts/
  fetch/              # Fetchers: arXiv, ACL Anthology, Interspeech
  filter/             # Filter agent (assigns relevance scores)
  parse/              # PDF download and parsing pipeline (Docling-based)
  discover/           # Citation discovery (citation index, corpus expansion)

.claude/agents/       # Claude Code subagent specs (ingest, integration, filter)

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
1. FETCH      — scripts/fetch/              → raw/metadata/*.json  (status: pending)
2. FILTER     — scripts/filter/agent.py     → status: accepted | review | rejected
3. REVIEW     — manual (raw/review_queue.md)→ status: accepted | rejected
4. DOWNLOAD   — scripts/parse/download_pdfs.py → raw/papers/*.pdf
5. PARSE      — scripts/parse/batch_convert.py → raw/parsed/{id}/paper.md
6. INGEST     — Claude Code ingest agent    → wiki/papers/{id}.md
7. INTEGRATE  — Claude Code integration agent → concept pages, evidence digests, cross-links
```

Stages 1–5 use Python scripts and are independently resumable — re-running skips work already done. Stages 6–7 use Claude Code subagent specs under `.claude/agents/` and are invoked from a Claude Code session. See `CLAUDE.md` for the full ingest and integration workflow.

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
