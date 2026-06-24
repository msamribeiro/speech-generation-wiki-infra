# CLAUDE.md — Speech Synthesis Research Wiki

This file is the operating contract for this wiki. Read it at the start of every session.
For stage-specific details, read the relevant doc from the tables at the bottom.

---

## Purpose

A living systematic review of the state of the art in synthetic speech, covering TTS, VC,
and spoken conversational agents. Papers are ingested on a rolling basis. The wiki compounds —
every ingested paper enriches existing concept pages, surfaces trends, and flags contradictions.

Coverage: Interspeech, ICASSP, ACL, EMNLP, NAACL, NeurIPS, ICLR, ICML, ASRU, SLT, arXiv,
and technical reports from industry labs.

---

## Environment

```bash
source .venv/bin/activate          # activate before running any script
```

Fresh setup:
```bash
uv venv .venv --python 3.12
uv pip install -r requirements.txt
```

Use `.venv/bin/python` directly in background Bash commands (source activate does not persist).

---

## Directory Structure

```
raw/                  # source documents and pipeline state (not rendered)
  metadata/           # one JSON per paper — the corpus record
  papers/             # downloaded PDFs (gitignored)
  parsed/             # Docling output per paper (gitignored)
  citation_index.json # corpus-wide citation graph
  review_queue.md     # borderline papers awaiting human decision
  pipeline_log.md     # infra-facing operations log

wiki/                 # the knowledge base (git submodule → content repo)
  papers/             # ingest output — one page per paper
  _claims/            # integrate output — one YAML per concept (claim graph)
  concepts/           # render output — concept synthesis pages
  evidence/           # render output — evidence dossiers
  venues/             # render output — venue/org summary pages
  briefs/             # render output — decision memos (deferred)
  reports/            # render output — trend reports (deferred)
  index.md            # master catalog
  log.md              # reader-facing changelog
  overview.md         # evolving field synthesis

docs/                 # stage documentation and design references
scripts/              # pipeline scripts (fetch/, parse/, discover/)
.claude/agents/       # Claude Code subagent specs
config/               # keyword_filter.yaml, parsing.yaml
lib/                  # shared library code
```

---

## Pipeline

Sessions rarely mix stages. Read only the doc for the stage you are running.

```
Fetch → Filter → Parse → Ingest → Integrate → Render
```

- **Fetch / Filter**: discover papers, score relevance, download PDFs → see [docs/fetch.md](docs/fetch.md)
- **Parse**: convert PDFs to markdown via Docling → see [docs/parse.md](docs/parse.md)
- **Ingest → Integrate → Render**: build and maintain wiki content → see [docs/content.md](docs/content.md)

---

## Glossary

| Term | Definition |
|------|-----------|
| **Fetch** | Discover and download paper metadata and PDFs from external sources |
| **Filter** | Assign relevance scores; accept or reject papers for the corpus |
| **Parse** | Convert accepted PDFs to structured markdown via Docling |
| **Ingest** | Write a wiki paper page from a parsed paper; paper-scoped |
| **Integrate** | Extract claims and evidence from paper pages into concept YAML; cross-paper |
| **Render** | Generate human-readable wiki pages from claim YAML; concept-scoped |
| **Claim** | A generalizable proposition about speech generation, traceable to paper evidence |
| **Concept** | A method or capability that groups related claims and papers |
| **Evidence** | Structured support for or against a claim, traceable to a specific paper section |
| **Evidence dossier** | Generated document mapping claims to papers for a given concept |
| **Brief** | Short decision-oriented memo answering a specific research question (deferred) |
| **Corpus** | The full set of papers tracked by the project; defined by `raw/metadata/` files |
| **Tier** | Classification for citation-discovery papers: Tier 1 = full page, Tier 2 = lightweight stub |
| **Method family** | A cluster of papers within a concept sharing a common architectural pattern |
| **Claim graph** | The structured network of claims, evidence, and paper relationships in `wiki/_claims/` |

---

## Invariants

Never violated under any circumstances:

1. **Never alter source documents** — PDFs in `raw/papers/` and substantive content of `raw/metadata/` JSONs are source of truth. Pipeline scripts may update pipeline-state fields (`status`, `pdf_path`, `ingested_date`, `generation_history`) but never alter what a paper says.
2. **Never invent numbers** — if a metric is not in the paper, write `"not reported"`. Never estimate or hallucinate.
3. **Canonical vocabulary only** — map all terms to the controlled vocabulary in [docs/schemas/vocabulary.md](docs/schemas/vocabulary.md). Note authors' original term in parentheses.
4. **One paper, one page** — check the index before creating a new paper page. Deduplicate by arXiv ID first, then by title similarity.
5. **Cite specifically** — use [[wikilinks]] to paper IDs, not just venue or year.
6. **File answers back** — valuable query outputs must be written to the wiki, not left only in chat.
7. **Log everything** — `ingest`, `review`, `integrate`, `render`, and `query` operations log to `wiki/log.md`; `filter`, `parse`, `discover`, `lint`, and `review` (paper triage) operations log to `raw/pipeline_log.md`. Never mix the two.
8. **Respect status** — never ingest a paper with `status: pending`, `review`, or `rejected` without explicit user instruction.
9. **Preserve provenance** — every metric value on a paper page must trace to a specific table or figure in the source PDF.
10. **Claim graph is derived, not authoritative at the page level** — never edit a concept page or evidence dossier directly to change a claim's status; all changes flow through `wiki/_claims/` YAML via the integration agent. The render agent regenerates pages from YAML; pages are always replaceable.

---

## Stage Documentation

| Stage | Doc |
|-------|-----|
| Fetch + Filter | [docs/fetch.md](docs/fetch.md) |
| Parse | [docs/parse.md](docs/parse.md) |
| Ingest + Integrate + Render | [docs/content.md](docs/content.md) |

## Schema Documentation

| Schema | Doc |
|--------|-----|
| Paper metadata JSON (`raw/metadata/`) | [docs/schemas/metadata.md](docs/schemas/metadata.md) |
| Concept claim YAML (`wiki/_claims/`) | [docs/schemas/claims.md](docs/schemas/claims.md) |
| Controlled vocabulary | [docs/schemas/vocabulary.md](docs/schemas/vocabulary.md) |

## Project Tracking

`BACKLOG.md` — prioritised feature list. Items are grouped by area and priority (`P0` active,
`P1` planned, `P2` deferred). Add new work here; remove items only when they are fully done and
moved to the archive. `BACKLOG.md` is the authoritative source for what comes next.

`ARCHIVE.md` — log of completed work. When all tasks in a backlog group are done, move the
entire group here with a completion date and a prose summary of the outcome. Never delete
backlog items without archiving them.
