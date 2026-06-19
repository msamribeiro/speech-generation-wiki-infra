# Archive

Completed features, moved here from BACKLOG.md when all tasks are done.
Each entry records the completion date, a prose summary of the outcome, and the completed task list.

---

## Ingest & Integration Pipeline [completed: 2026-06-17]

Built the full multi-agent ingest architecture. Per-paper ingest agent writes one wiki page with
no cross-paper work; integration agent handles concept YAML updates; lightweight stub agent handles
Tier 2 citation-discovery papers. Ingested all 338 papers across sessions 12–47: 176 standard
papers, 96 Tier 1 CD full pages, 66 Tier 2 CD stubs. Ran 11 integration passes covering 276
papers. Architecture since redesigned (2026-06-18) into the three-stage ingest → integrate →
render pipeline documented in docs/content.md.

- [x] Build speech-generation-ingest-agent (per-paper, paper-scoped)
- [x] Build speech-generation-integration-agent (cross-paper, concept YAML)
- [x] Build speech-generation-lightweight-ingest-agent (Tier 2 stubs)
- [x] Build speech-generation-filter-agent (relevance scoring)
- [x] Separate ingest from integration (session 14 — no concept pages during ingest)
- [x] Ingest 176 standard papers (sessions 12–46)
- [x] Ingest 96 Tier 1 CD papers (2026-06-16)
- [x] Ingest 66 Tier 2 CD stubs (2026-06-17)
- [x] Run integration passes 1–11 (276 papers integrated; all 24 concept stubs seeded)

---

## Parse Pipeline Implementation [completed: 2026-06-08]

Built the full PDF-to-markdown parsing pipeline using Docling (chosen over the original
GROBID+Marker stack for better table/figure handling and single-dependency setup). Converted
all 875 standard papers in 30 batches with 0 failures, then all 162 citation-discovery papers
in 5 further batches. Multiple `_REFS_HEADER_RE` patches applied for non-standard reference
headers. Parse design documented in docs/design/parsing-pipeline.md.

- [x] Build convert_paper.py (single-paper Docling converter with MPS/CPU fix)
- [x] Build batch_convert.py (batch orchestrator with --ids, --force, --retry-failed, --status)
- [x] Build make_batch_queue.py (queue generation with --sync flag, --batch-size 40)
- [x] Parse 875 standard papers (batches 1–13, 2026-05-22 → 2026-06-06); 0 failures
- [x] Parse 162 citation-discovery papers (batches 14–18, 2026-06-08); 0 failures
- [x] Apply _REFS_HEADER_RE patches (French headers, numbered Bibliography, letter-prefix headings)
- [x] Rebuild citation index: 21,262 entries, 652+50 merges, 4 override groups

---

## Corpus Cleanup [completed: 2026-06-18]

Reorganised `docs/` into a coherent structure (stage docs at root, `design/`, `schemas/`, `records/`),
moved all one-off session logs and analyses into `docs/records/` with date-prefixed filenames,
deleted the unused `scripts/filter/agent.py` (replaced by the Claude Code filter subagent), and
cleaned the repo root down to five files: `CLAUDE.md`, `README.md`, `STATUS.md`, `BACKLOG.md`, `ARCHIVE.md`.

- [x] Review docs/THOUGHTS_FOR_IMPROVEMENTS.md — archived to docs/records/2026-06-18-thoughts-for-improvements.md
- [x] Move root session files to docs/records/ with date-prefix (GPT suggestions, flow-matching experimental, action plan, schema redesign)
- [x] Archive INGEST_OPT_EXPERIMENT.md → docs/records/2026-05-29-ingest-opt-experiment.md
- [x] Archive WIKI_USES.md → docs/records/2026-05-27-wiki-uses.md
- [x] Delete scripts/filter/agent.py (unused; replaced by speech-generation-filter-agent subagent)
- [x] Update all references to moved/deleted files across docs/, agent specs, and scripts/

---

## Wiki Structural Fixes & Review Agent [completed: 2026-06-19]

Resolved all structural errors surfaced by the Pipeline Health Suite ingest module. Quoted 327
unquoted `id:` fields in paper frontmatter (arXiv float-parse bug). Fixed 191 bare ID cells and
193 plain title cells in `wiki/papers/index.md` to use `[[id]]` wikilinks and `[title](papers/id.md)`
markdown links; removed 1 blank row breaking table rendering. Added `_check_index_document()` to
the ingest health module and patched both ingest agents to strip blank rows from the index table
and always emit quoted IDs going forward. Added `> [!info] Citation Stub` callout to all 65 Tier 2
pages and updated the lightweight ingest agent to emit it on all future writes. Wrote the
`speech-generation-review-agent` spec — a targeted quality review agent that audits any existing
Tier 1 page against the full expected page template, corrects frontmatter, adds missing Field
Significance and Claims sections with `*(§N.N)*` citations, and evaluates figures.

- [x] Quote all `id:` fields in wiki paper frontmatter — 327 files patched; both ingest agents updated to always emit quoted id; blank-line stripping added to index table write in both agents
- [x] Fix paper index wikilink format — 191 ID cells → `[[id]]`, 193 plain titles → `[title](papers/id.md)`, 1 blank row removed; `_check_index_document()` added to health_check ingest module
- [x] Add `[!info] Citation Stub` callout to all Tier 2 paper pages — 65 pages patched retroactively; lightweight ingest agent updated to emit callout on all future writes; health check updated from `[!note]` → `[!info]`
- [x] Write speech-generation-review-agent spec — validates all sections against a complete expected template, corrects frontmatter, adds missing Field Significance and Claims with inline citations, evaluates figures; designed for reuse with any model

---

## Documentation Restructure [completed: 2026-06-18]

Split the monolithic CLAUDE.md (~400 lines mixing contract, templates, and workflows) into a
thin operating contract (~134 lines) plus four stage-specific docs in `docs/`. Introduced
BACKLOG.md and ARCHIVE.md for structured feature tracking. Redesigned the content stage from
a two-pass (ingest + integrate) pipeline to a three-stage pipeline (ingest → integrate → render),
with `wiki/_claims/{slug}.yaml` as the single source of truth for all generated wiki pages.
Wrote the new render agent spec; updated the integration agent to write YAML only; fixed
ingest agent scope statement, duplicate check, figure selection order, and index wikilink format.

- [x] Create BACKLOG.md + ARCHIVE.md
- [x] Write docs/schemas/metadata.md
- [x] Write docs/schemas/vocabulary.md
- [x] Write docs/schemas/claims.md
- [x] Write docs/fetch.md
- [x] Write docs/parse.md
- [x] Write docs/content.md
- [x] Rewrite CLAUDE.md as thin overview (~134 lines)
- [x] Update speech-generation-integration-agent.md (YAML only; removed page-writing steps)
- [x] Fix speech-generation-ingest-agent.md (scope statement, generation_history, figure selection order, duplicate check, index wikilink format)
- [x] Write speech-generation-render-agent.md (new)
