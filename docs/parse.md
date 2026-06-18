# Parse Stage

Convert accepted paper PDFs to structured markdown for use by the ingest stage.

**Input:** `raw/papers/{id}.pdf` (for papers with `status: accepted` and a valid `pdf_path`)
**Output:** `raw/parsed/{id}/paper.md`, `metadata.json`, `references.json`, `assets/`

See also: [docs/design/parsing-pipeline.md](design/parsing-pipeline.md), [docs/schemas/metadata.md](schemas/metadata.md)

---

## Parse Pipeline Scripts (`scripts/parse/`)

| Script | Purpose |
|--------|---------|
| `download_pdfs.py` | Download PDFs for accepted papers lacking `pdf_path` |
| `convert_paper.py` | Convert a single PDF to markdown via Docling |
| `batch_convert.py` | Batch convert with parallelism and resume support |
| `make_batch_queue.py` | Build the list of papers needing parse |

### Standard batch run

```bash
source .venv/bin/activate

# Build queue of accepted papers not yet parsed
python scripts/parse/make_batch_queue.py --sync --batch-size 40

# Run batch conversion
python scripts/parse/batch_convert.py
```

`--sync` ensures the queue reflects current metadata status. Use `--batch-size 40` as the
default; smaller batches (10–20) for spotting Docling errors early.

### Single paper

```bash
python scripts/parse/convert_paper.py --id 2406.18009
```

---

## Parse Output (`raw/parsed/{id}/`)

| File | Contents |
|------|---------|
| `paper.md` | LLM-ready markdown — primary ingest target |
| `metadata.json` | Title, authors, abstract, figure/table registries (Docling output) |
| `references.json` | Structured reference list with `in_corpus` flags |
| `docling_native.json` | Docling's full internal document representation |
| `assets/` | Figures (`figure-N.png`) and tables (`table-N.csv`, `table-N.png`) |

`paper.md` and `assets/` are the files the ingest agent reads. The others are intermediate
artifacts and are not tracked in git.

---

## Docling Gotchas

- **MPS/CPU fix**: If Docling crashes on Apple Silicon GPU, set `DOCLING_DEVICE=cpu` before running.
- **REFERENCE label fallback**: Docling sometimes labels reference sections with uppercase `REFERENCES`; the parser handles this via a fallback regex — patch `_REFS_HEADER_RE` in `convert_paper.py` if you see reference sections missing from `references.json`.
- **Label names**: Docling uses uppercase label names internally; do not lowercase them in matching logic.
- **Re-parse rule**: Never re-run `convert_paper.py --force` on a paper without first applying a code fix. Re-running without a fix produces identical output.

---

## Parse Quality Review

Spot-check parsed output when:
- A paper has an unusual PDF structure (scanned, two-column with complex figures, non-standard section headers)
- `references.json` is empty or has fewer entries than expected
- `paper.md` is very short relative to the paper's known length

Flagged papers are tracked in `raw/parsed/parse_quality_review.md`. Do not force-reparse until
the user has confirmed the PDF looks correct offline.

---

## Citation Index Rebuild

After each parse batch, rebuild the corpus-wide citation graph:

```bash
python scripts/discover/citation_index.py
```

This updates `raw/citation_index.json`, which is used by the citation discovery workflow.

---

## pipeline_log.md Entries

Parse-stage operations log to `raw/pipeline_log.md`.

```
- parse | batch {N} | {M} papers | {K} failed
```
