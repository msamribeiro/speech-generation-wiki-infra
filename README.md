# Speech Generation Wiki — Infrastructure

A living systematic review of the state of the art in synthetic speech, covering **text-to-speech (TTS)**, **voice conversion (VC)**, and **spoken conversational agents**. Papers are ingested on a rolling basis from arXiv, Interspeech, ACL/EMNLP/NAACL, NeurIPS, ICLR, and industry technical reports.

This repository contains the data acquisition pipeline, parsing infrastructure, and Claude Code agent specs. It is not the wiki itself — wiki content lives in a separate content repository and is published as a static site.

---

## Three-repo structure

| Repo | Contents |
|------|----------|
| **infra** (this repo) | Pipeline scripts, raw corpus state, Claude Code agent specs |
| **wiki-content** | Paper pages, concept pages, claim graph YAML |
| **site** | Quartz v5 static site → GitHub Pages |

The wiki content repo is included here as a git submodule under `wiki/`.

---

## Directory layout

```
raw/                    # Source documents and pipeline state
  metadata/             # One JSON per paper — the corpus record (tracked)
  papers/               # Downloaded PDFs (gitignored)
  parsed/               # Docling parse output (gitignored)
  citation_index.json   # Corpus-wide citation graph
  review_queue.md       # Borderline papers awaiting manual review
  pipeline_log.md       # Infra-facing operations log

wiki/                   # Knowledge base (git submodule → wiki content repo)
  papers/               # One page per ingested paper
  _claims/              # Claim graph YAML — source of truth for all rendered pages
  concepts/             # Rendered concept synthesis pages
  evidence/             # Rendered evidence dossiers
  venues/               # Rendered venue summary pages
  index.md              # Master paper catalog
  log.md                # Reader-facing changelog
  overview.md           # Evolving field synthesis

docs/                   # Project documentation
  fetch.md              # Fetch + filter stage guide
  parse.md              # Parse stage guide
  content.md            # Ingest + integrate + render stage guide
  writing-style.md      # Prose style guide for content agents
  citation-discovery.md # Citation graph and corpus expansion guide
  schemas/              # Paper metadata schema, claim YAML schema, controlled vocabulary
  design/               # Detailed design documents for fetch and parse stages
  records/              # Date-prefixed session logs, analyses, and archived notes

scripts/
  fetch/                # arXiv, ACL Anthology, Interspeech, OpenReview fetchers
  parse/                # PDF download and Docling conversion pipeline
  discover/             # Citation index and corpus expansion

.claude/agents/         # Claude Code subagent specs
config/                 # keyword_filter.yaml, parsing.yaml
lib/                    # Shared library code

CLAUDE.md               # Operating contract for Claude Code sessions
BACKLOG.md              # Feature backlog (P0/P1/P2 priorities)
ARCHIVE.md              # Completed features with prose summaries
STATUS.md               # Current corpus counts and pipeline state
```

---

## Pipeline

```
Fetch → Filter → Parse → Ingest → Integrate → Render
```

| Stage | Tool | Output |
|-------|------|--------|
| **Fetch** | `scripts/fetch/*.py` | `raw/metadata/*.json` |
| **Filter** | `speech-generation-filter-agent` | status: accepted, review, or rejected |
| **Review** | Manual (`raw/review_queue.md`) | status: accepted or rejected |
| **Parse** | `scripts/parse/batch_convert.py` | `raw/parsed/{id}/paper.md` |
| **Ingest** | `speech-generation-ingest-agent` | `wiki/papers/{id}.md` |
| **Integrate** | `speech-generation-integration-agent` | `wiki/_claims/{slug}.yaml` |
| **Render** | `speech-generation-render-agent` | `wiki/concepts/`, `wiki/evidence/` |

Fetch through Parse use Python scripts and are independently resumable — re-running skips work already done. Ingest, Integrate, and Render use Claude Code subagents invoked from a Claude Code session.

For detailed workflows, see `docs/fetch.md`, `docs/parse.md`, and `docs/content.md`. For the operating contract and invariants, see `CLAUDE.md`.

---

## Environment setup

**Prerequisite:** [uv](https://docs.astral.sh/uv/)

```bash
brew install uv          # macOS
# or
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**One-time setup:**

```bash
git clone <repo-url> --recurse-submodules
cd speech-generation-wiki-infra

uv venv .venv --python 3.12
uv pip install -r requirements.txt
```

**Each session:**

```bash
source .venv/bin/activate
```

---

## Script reference

### Fetch scripts

```bash
# arXiv (cs.SD + eess.AS)
python scripts/fetch/arxiv.py --date-from 2026-05-22

# arXiv cs.CL via OAI-PMH (for large category sweeps)
python scripts/fetch/arxiv_oai.py --set cs.CL --date-from 2026-05-22

# ACL Anthology (main venues + workshops)
python scripts/fetch/acl.py --years 2026 --all-workshops

# Interspeech via ISCA Archive
python scripts/fetch/isca.py --year 2026

# ICLR / NeurIPS via OpenReview
python scripts/fetch/openreview.py --venue ICLR --year 2026
```

### Parse scripts

```bash
# Download PDFs for all accepted papers
python scripts/parse/download_pdfs.py

# Convert PDFs to markdown via Docling
python scripts/parse/batch_convert.py

# Rebuild citation index after each parse batch
python scripts/discover/citation_index.py
```

### Claude Code agents

| Agent | Purpose |
|-------|---------|
| `speech-generation-filter-agent` | Score pending papers for relevance (0.0–1.0); assign status |
| `speech-generation-ingest-agent` | Write a Tier 1 wiki paper page from parsed output |
| `speech-generation-lightweight-ingest-agent` | Write a Tier 2 stub page for citation-discovery papers |
| `speech-generation-integration-agent` | Extract claims from paper pages; update `wiki/_claims/` YAML |
| `speech-generation-render-agent` | Render concept pages and evidence dossiers from claim YAML |

Invoke from a Claude Code session: `"Ingest paper {id}"`, `"Run integration pass on last 25 papers"`, `"Render all stale concepts"`.

---

## Key documents

| Document | Purpose |
|----------|---------|
| `CLAUDE.md` | Operating contract — read at the start of every Claude Code session |
| `STATUS.md` | Current corpus counts and pipeline state |
| `BACKLOG.md` | Prioritised feature backlog |
| `ARCHIVE.md` | Completed features with outcomes |
| `docs/content.md` | Full ingest → integrate → render workflow and page templates |
| `docs/schemas/` | Paper metadata schema, claim YAML schema, controlled vocabulary |

---

## Dependency management

```bash
# Add a package and pin it
uv pip install <package-name>
uv pip freeze > requirements.txt   # commit this

# Sync to pinned versions
uv pip install -r requirements.txt
```
