# PDF Parsing Pipeline — Design Document

**Project:** Speech Synthesis Research Wiki  
**Scope:** Structured extraction of text, figures, tables, and equations from academic PDFs  
**Depends on:** Fetcher pipeline (`raw/papers/{id}.pdf` must exist)  
**Status:** Partially implemented — see §10 for the adopted Docling-based approach, which supersedes the GROBID+Marker multi-tool stack described in §3–7.

---

## 1. Goals and Non-Goals

### Goals
- Convert each paper PDF into a structured, LLM-readable representation stored in `raw/parsed/{id}/`
- Preserve document structure: title, authors, abstract, sections in order, references
- Extract figures as images with VLM-generated semantic descriptions
- Extract tables in a machine-readable form, with a VLM fallback for complex layouts
- Capture equations in LaTeX where possible, image fallback otherwise
- Produce a single `full_text.md` per paper that the ingest agent can read without touching the PDF
- Be re-runnable and idempotent: re-parsing a paper overwrites the previous output cleanly
- Run primarily locally to avoid per-paper API costs at scale

### Non-Goals
- Perfect equation parsing — understanding the gist is sufficient, exact LaTeX reproduction is not required
- Figure interpretation beyond structured prose description (no metric extraction from graphs)
- OCR of scanned papers — corpus is assumed to be born-digital PDFs
- Real-time or streaming extraction — batch processing is fine

---

## 2. The Extraction Problem in Detail

Academic PDFs in the target corpus (Interspeech, ICASSP, ACL, NeurIPS, arXiv) share a set of structural properties that make naive text extraction unreliable. Understanding these failure modes is prerequisite to designing the right tool chain.

### 2.1 Two-Column Layout

The dominant format at IEEE venues (ICASSP) and ISCA (Interspeech) is two-column. PDF byte order does not respect column boundaries: a naive left-to-right, top-to-bottom text extractor interleaves both columns, producing nonsensical output. The correct reading order requires layout analysis — identifying column boundaries, text blocks, and their spatial relationships — before text is extracted.

ACL-format papers (ACL, EMNLP, NAACL) are also two-column. arXiv preprints vary: some mirror the camera-ready two-column format, others are single-column.

NeurIPS and ICLR use a single-column format with wide margins, which is less problematic but still has footnotes and margin notes to handle.

### 2.2 Equations

Mathematical notation in TTS papers is pervasive: diffusion schedules, flow matching objectives, encoder-decoder attention formulations, loss functions. Equations in PDFs are stored as:
- **Type 1 / TrueType glyphs** — mathematical symbols mapped to font-specific code points, often in private use area Unicode ranges. Extractable as Unicode but often garbled.
- **Vector graphics** — equations rendered as paths, not glyphs. Completely invisible to text extractors.
- **Embedded bitmaps** — scanned or rasterised equations. Require OCR.

The practical result: no text extractor reliably recovers equation content. The best available tool for LaTeX recovery from PDFs is Nougat (Meta, 2023), trained on arXiv source-PDF pairs. Its accuracy degrades on camera-ready proceedings with different typesetting from arXiv defaults.

For the ingest agent's purposes, the surrounding prose context plus an equation image is usually sufficient to understand what a loss function or architecture formula is doing. Exact LaTeX recovery is a nice-to-have, not a requirement.

### 2.3 Figures

Figures are stored as embedded images (JPEG, PNG, PDF sub-streams) or as vector graphics (paths and curves). Text extractors cannot interpret them. For this pipeline, figures are the single highest-value extraction target after section text, because:
- Architecture diagrams communicate system design more efficiently than prose
- Spectrograms and mel-plots are direct evidence of output quality claims
- Ablation and result graphs summarise experimental findings visually

The challenge is not extraction (figures can be identified by their bounding boxes and rasterised) but interpretation. This is where VLMs are uniquely useful.

### 2.4 Tables

Result tables in speech papers typically have:
- Multi-row headers (system name row + metric rows)
- Merged cells (a single system name spanning multiple configuration rows)
- Bold or underlined best results
- Footnote markers (†, ‡) linking to conditions described below the table
- Narrow columns that force line wrapping within cells

Text extractors flatten tables into a sequence of strings, destroying cell structure. Layout-aware tools (GROBID, Marker) do better but still fail on complex merged-cell layouts. A VLM pass on table images is the most reliable fallback.

### 2.5 Headers, Footers, and Boilerplate

Every paper has venue name, page numbers, copyright notices, and author-affiliation blocks. These must be stripped from the extracted text before LLM ingestion — they add noise without signal.

### 2.6 References

The reference list is structured data: author, title, venue, year, for each cited work. GROBID is the best-in-class tool for reference extraction, producing structured BibTeX-compatible output. This is valuable because it enables automatic cross-referencing: if Paper A cites Paper B that is also in the corpus, this can be surfaced in the wiki.

---

## 3. Tool Landscape

| Tool | Type | Layout-aware | Tables | Equations | Figures | Runs locally | Cost |
|------|------|-------------|--------|-----------|---------|-------------|------|
| pdfminer / PyMuPDF | Text extractor | ❌ | ❌ | ❌ | ❌ | ✅ | Free |
| GROBID | ML segmenter | ✅ | Partial | ❌ | Regions only | ✅ | Free |
| Marker | End-to-end MD | ✅ | ✅ | Partial (LaTeX) | Regions only | ✅ | Free |
| Nougat | End-to-end MD | ✅ | ✅ | ✅ (LaTeX) | ❌ | ✅ | Free |
| MinerU | End-to-end MD | ✅ | ✅ | ✅ (LaTeX) | Regions only | ✅ | Free |
| Claude / GPT-4o (VLM) | Vision-language | ✅ | ✅ | ✅ | ✅ | ❌ | Per token |
| Adobe PDF Extract | Cloud API | ✅ | ✅ | Partial | ✅ | ❌ | Per page |

### Recommended tools

**Marker** as the primary full-text extractor. Reasons:
- Trained on academic papers including two-column layouts
- Produces clean Markdown with section headers as `##` headings
- Handles tables as Markdown tables
- Outputs LaTeX for equations it can parse
- Actively maintained, good performance on arXiv and proceedings PDFs
- Runs locally; GPU recommended for throughput, CPU workable for a corpus of a few hundred papers

**PyMuPDF (fitz)** for figure and table region extraction. Reasons:
- Fastest library for page rasterisation and image extraction
- Marker identifies figure bounding boxes; PyMuPDF renders them to PNG
- Used programmatically, not as a text extractor

**GROBID** for reference extraction and header parsing. Reasons:
- Best-in-class structured reference parsing
- TEI XML output is machine-readable
- Header parsing (title, authors, abstract, affiliations) is more reliable than Marker's
- Runs as a local Docker container

**Claude API (claude-sonnet-4-20250514)** for figure description and table fallback. Reasons:
- Already in the stack for the filter and ingest agents
- Handles architecture diagrams, spectrograms, and result graphs with high accuracy
- Used selectively (figures + complex tables only) to control cost

---

## 4. Pipeline Architecture

The parsing pipeline runs per paper and is orchestrated by `scripts/parse/parse_paper.py`. It calls four sub-components in sequence:

```
raw/papers/{id}.pdf
        │
        ▼
┌───────────────────────────────────────────────────────────────┐
│  Stage 1: HEADER + REFERENCE EXTRACTION                       │
│  Tool: GROBID                                                 │
│  Output: header.json, references.json                         │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────────┐
│  Stage 2: FULL-TEXT EXTRACTION                                │
│  Tool: Marker                                                 │
│  Output: full_text_raw.md (with section structure)            │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────────┐
│  Stage 3: FIGURE + TABLE REGION EXTRACTION                    │
│  Tool: PyMuPDF (rasterise) + Marker metadata (bounding boxes) │
│  Output: figures/figN.png, tables/tableN.png                  │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────────┐
│  Stage 4: VLM INTERPRETATION                                  │
│  Tool: Claude API (vision)                                    │
│  Input: figure images, complex table images                   │
│  Output: figures/figN_description.json,                       │
│          tables/tableN_structured.json                        │
└───────────────────────────┬───────────────────────────────────┘
                            │
                            ▼
┌───────────────────────────────────────────────────────────────┐
│  Stage 5: ASSEMBLY                                            │
│  Tool: assemble.py                                            │
│  Input: all stage outputs                                     │
│  Output: full_text.md (final, clean, ingest-ready)            │
│          parse_manifest.json                                  │
└───────────────────────────────────────────────────────────────┘
```

### Output directory structure

```
raw/parsed/{id}/
  full_text.md              # Final assembled Markdown — primary ingest target
  full_text_raw.md          # Marker output before assembly (kept for debugging)
  parse_manifest.json       # Extraction quality report and metadata
  header.json               # GROBID: title, authors, abstract, affiliations
  references.json           # GROBID: structured reference list
  figures/
    fig1.png                # Rasterised figure image (300 DPI)
    fig1_caption.txt        # Caption text extracted from Marker output
    fig1_description.json   # VLM structured description
    fig2.png
    fig2_caption.txt
    fig2_description.json
  tables/
    table1.md               # Marker Markdown table (simple tables)
    table2.png              # Rasterised image (complex tables only)
    table2_structured.json  # VLM extraction for complex tables
  equations/
    eq1.png                 # Equation image
    eq1.tex                 # LaTeX if Marker recovered it (else absent)
```

---

## 5. Stage Designs

### Stage 1: Header and Reference Extraction (GROBID)

GROBID runs as a local REST server (Docker container). Two endpoints are used:

- `/api/processHeaderDocument` — extracts title, authors, abstract, affiliations, venue hint
- `/api/processFulltextDocument` — full segmentation including references

```python
@dataclass
class PaperHeader:
    title: str
    authors: list[str]
    affiliations: list[str]
    abstract: str
    venue_hint: str | None      # e.g. "Interspeech 2025" if present in header
    doi: str | None
    arxiv_id: str | None

@dataclass
class Reference:
    ref_id: str                 # e.g. "b12" (GROBID internal)
    authors: list[str]
    title: str
    venue: str | None
    year: int | None
    doi: str | None
    arxiv_id: str | None        # extracted from URL if present
    in_corpus: bool             # True if this paper is also in raw/metadata/
    corpus_id: str | None       # canonical ID in raw/metadata/ if in_corpus

def extract_header_and_refs(pdf_path: Path, grobid_url: str) -> tuple[PaperHeader, list[Reference]]:
    """
    Calls GROBID REST API.
    Parses TEI XML response.
    For each reference, attempts to match to the corpus via arXiv ID or
    title fingerprint (same fuzzy matching logic as scripts/parse/merge_records.py).
    Returns structured header and reference list.
    """
```

**Known failure modes:**
- GROBID occasionally misparses the abstract boundary on papers with unusual header layouts (e.g. papers that put the abstract in a box or coloured block). In this case, fall back to Marker's abstract extraction.
- Author affiliation parsing is imperfect for papers with complex affiliation footnotes. Store raw affiliation strings; do not attempt structured institution extraction.
- arXiv IDs in references appear as URLs (`arxiv.org/abs/2501.12345`) — extract with a regex after GROBID parsing.

---

### Stage 2: Full-Text Extraction (Marker)

Marker is called via its Python API on the PDF path. It returns a Markdown string and a set of metadata including detected page layouts and element positions.

```python
@dataclass
class MarkerOutput:
    markdown: str               # Full paper as Markdown
    pages: int
    layout: str                 # "single-column" | "two-column" | "mixed"
    figures: list[FigureRegion]
    tables: list[TableRegion]
    equations: list[EquationRegion]

@dataclass
class FigureRegion:
    figure_id: str              # "fig1", "fig2", ...
    page: int
    bbox: tuple[float, float, float, float]   # (x0, y0, x1, y1) in PDF coordinates
    caption: str | None         # Text of figure caption as detected by Marker

@dataclass
class TableRegion:
    table_id: str
    page: int
    bbox: tuple[float, float, float, float]
    markdown: str               # Marker's table as Markdown
    is_complex: bool            # True if merged cells or multi-row header detected

@dataclass
class EquationRegion:
    eq_id: str
    page: int
    bbox: tuple[float, float, float, float]
    latex: str | None           # LaTeX if Marker recovered it
    is_inline: bool             # True if inline equation, False if display equation

def extract_full_text(pdf_path: Path, config: MarkerConfig) -> MarkerOutput:
    """
    Runs Marker on the PDF.
    Post-processes the raw Markdown:
      - Strips page headers/footers (venue name, page number, copyright line)
      - Strips author affiliation block (already captured by GROBID)
      - Normalises section heading levels (## for top-level, ### for subsections)
      - Inserts figure and table placeholders: {{FIGURE:fig1}}, {{TABLE:table1}}
        at the location where Marker detected the element
      - Strips the reference list from the body (already captured by GROBID)
    Returns MarkerOutput with cleaned markdown and region metadata.
    """
```

**Post-processing rules for the raw Marker Markdown:**

Header/footer stripping heuristics:
- Lines matching `^\d+$` (standalone page number) → remove
- Lines matching the venue pattern (e.g. `^Interspeech \d{4}$`) → remove
- Lines matching copyright patterns (`©`, `IEEE`, `ISCA`) → remove
- First N lines if they duplicate content already captured in `header.json` → remove

Section normalisation:
- Marker uses `#` for the paper title and `##` for top-level sections — preserve this mapping
- If Marker emits `#` for sections (not title), re-map to `##`
- Abstract, Introduction, Method/Model, Experiments, Results, Conclusion, References are expected top-level sections — flag if any are missing

Placeholder insertion:
- At the location of each FigureRegion, insert: `{{FIGURE:fig1 | caption: "Caption text here"}}`
- At the location of each TableRegion, insert: `{{TABLE:table1}}` for simple tables (Markdown follows immediately) or `{{TABLE_COMPLEX:table2}}` for complex tables
- At each EquationRegion, insert: `{{EQ:eq1 | latex: "..."}}` or `{{EQ:eq1 | image: true}}` if no LaTeX

**Known failure modes:**
- Marker occasionally merges two adjacent sections if the section heading is in an unusual font or size. Mitigation: post-processing checks for sections longer than 2000 words and flags them in the manifest for human review.
- Two-column papers with figures that span both columns (common for architecture diagrams) may have their figure region incorrectly split. Mitigation: detect split figures by checking for two adjacent FigureRegions on the same page with similar y-coordinates and merge their bounding boxes.
- Papers with coloured section heading backgrounds (common in NeurIPS style) may have headings missed by Marker. Mitigation: secondary pass using regex on capitalised lines after paragraph breaks.

---

### Stage 3: Figure and Table Region Extraction (PyMuPDF)

Using the bounding boxes from `MarkerOutput`, PyMuPDF renders each region to a PNG image at 300 DPI.

```python
def extract_regions(
    pdf_path: Path,
    marker_output: MarkerOutput,
    output_dir: Path,
    dpi: int = 300,
) -> list[ExtractedRegion]:
    """
    Opens PDF with fitz (PyMuPDF).
    For each FigureRegion and TableRegion in marker_output:
      1. Opens the relevant page
      2. Clips to the bounding box (with a small margin: +10pt on each side)
      3. Renders to PNG at specified DPI
      4. Saves to output_dir/figures/figN.png or output_dir/tables/tableN.png
      5. Saves caption to output_dir/figures/figN_caption.txt
    Returns list of ExtractedRegion with local file paths.
    
    Special cases:
      - If a figure bbox spans two pages (rare but occurs with tall figures):
        render both page clips and concatenate vertically
      - If a table is flagged is_complex=True, always save image regardless
        of whether Marker produced a Markdown version
      - Minimum region size: skip regions smaller than 50x50 points (noise)
    """

@dataclass
class ExtractedRegion:
    region_id: str              # "fig1", "table2", "eq3"
    region_type: str            # "figure" | "table" | "equation"
    image_path: Path
    caption: str | None
    marker_markdown: str | None  # Marker's text version if available
    needs_vlm: bool             # True if VLM interpretation is required
```

**`needs_vlm` decision logic:**

For figures: always True. Every figure gets a VLM description.

For tables: True if `is_complex=True` OR if the Marker Markdown has more than 15% empty cells (proxy for extraction failure) OR if the table has more than 8 columns (complex layout likely).

For equations: False (VLM is not used for equations; image fallback is sufficient).

---

### Stage 4: VLM Interpretation (Claude API)

The VLM stage sends figure and complex table images to the Claude API with structured prompts. This is the only stage with external API dependency and per-call cost.

**Cost estimation:** At 300 DPI, a typical architecture diagram is ~800×600px ≈ 150–200K pixels. As a JPEG at moderate quality, this is approximately 50–80KB. Claude's vision API charges by image size. A 10-page paper with 4 figures and 2 complex tables → approximately 6 API calls → roughly $0.02–0.05 per paper. For 300 papers: $6–15 total. Acceptable.

#### 4.1 Figure Description

```python
FIGURE_DESCRIPTION_PROMPT = """
You are analysing a figure from an academic paper on speech synthesis, 
text-to-speech (TTS), voice conversion, or spoken dialogue systems.

Examine this figure carefully and provide a structured description in JSON format:

{
  "figure_type": one of ["architecture_diagram", "result_graph", "spectrogram", 
                          "attention_map", "training_curve", "comparison_table_as_figure",
                          "system_overview", "ablation_plot", "other"],
  "description": "2–4 sentence prose description of what the figure shows. 
                  For architecture diagrams: describe the components and data flow.
                  For graphs: describe axes, what is being measured, and the key result.
                  For spectrograms: describe what speech characteristic is shown and 
                  what the figure demonstrates.",
  "key_components": ["list of named components, modules, or systems shown"],
  "main_finding": "One sentence on what this figure demonstrates or proves, 
                   if it is a results figure. Null if it is a system diagram.",
  "relevance_to_paper": "One sentence on how this figure relates to the paper's 
                          main contribution."
}

Return only valid JSON. No preamble or explanation.

Caption: {caption}
"""

def describe_figure(
    image_path: Path,
    caption: str | None,
    paper_title: str,
    client: anthropic.Anthropic,
) -> FigureDescription:
    """
    Sends figure image to Claude with the structured prompt.
    Parses JSON response.
    Retries up to 3 times on API error or JSON parse failure.
    Returns FigureDescription dataclass.
    """

@dataclass
class FigureDescription:
    figure_id: str
    figure_type: str
    description: str
    key_components: list[str]
    main_finding: str | None
    relevance_to_paper: str
    caption: str | None
    image_path: str             # relative path from raw/parsed/{id}/
```

#### 4.2 Table Extraction

```python
TABLE_EXTRACTION_PROMPT = """
You are extracting data from a results table in an academic paper on speech synthesis.

Extract the table contents as structured JSON:

{
  "headers": ["list of column header strings, in order"],
  "subheaders": ["list of subheader row strings if present, else empty list"],
  "rows": [
    {
      "system": "name of the system or condition in this row",
      "values": {"metric_name": "value", ...},
      "is_proposed": true/false,   // true if this is the paper's proposed system
      "is_baseline": true/false,   // true if explicitly labelled as baseline
      "notes": "any footnote markers or special conditions, else null"
    }
  ],
  "caption": "table caption text",
  "footnotes": ["list of footnote strings if present"],
  "metric_direction": {
    "MOS": "higher_is_better",
    "WER": "lower_is_better"
  }
}

Return only valid JSON. If you cannot read a cell clearly, use null for that value.
Do not invent values. If the table structure is ambiguous, describe the ambiguity 
in a top-level "notes" field.

Caption: {caption}
"""

@dataclass
class TableStructured:
    table_id: str
    headers: list[str]
    subheaders: list[str]
    rows: list[dict]
    caption: str | None
    footnotes: list[str]
    metric_direction: dict[str, str]
    extraction_notes: str | None
```

**Post-extraction validation for tables:**
- Check that all rows have the same number of value keys as headers
- Check that `is_proposed=True` appears at least once (flag if not — may indicate extraction failure)
- Check for numeric plausibility: MOS values should be 1.0–5.0, WER values 0–100

---

### Stage 5: Assembly

The assembly stage combines all stage outputs into the final `full_text.md` and the `parse_manifest.json`.

```python
def assemble(
    paper_id: str,
    header: PaperHeader,
    marker_output: MarkerOutput,
    figure_descriptions: list[FigureDescription],
    table_structured: list[TableStructured],
    references: list[Reference],
    output_dir: Path,
) -> AssemblyResult:
    """
    Builds the final full_text.md by:
    
    1. Writing a structured YAML frontmatter block with fields from header.json
    2. Writing the abstract as the first section
    3. Walking the cleaned Marker Markdown, replacing placeholders:
         {{FIGURE:fig1 | caption: "..."}}
         → replaced with the FigureDescription prose block (see format below)
         
         {{TABLE:table1}}
         → replaced with the Marker Markdown table
         
         {{TABLE_COMPLEX:table2}}
         → replaced with the structured table rendered as Markdown from TableStructured
         
         {{EQ:eq1 | latex: "\\mathcal{L} = ..."}}
         → replaced with LaTeX block: ```math ... ```
         
         {{EQ:eq1 | image: true}}
         → replaced with a note: [Equation eq1 — see raw/parsed/{id}/equations/eq1.png]
    
    4. Appending a ## References section with in-corpus references highlighted
    
    Returns AssemblyResult with path to full_text.md and quality metrics.
    """
```

**Figure block format in `full_text.md`:**

```markdown
> **Figure 1** [architecture_diagram]: The proposed system consists of a text encoder,
> a flow-matching decoder, and a HiFi-GAN vocoder. Text tokens pass through a 
> transformer encoder before being projected into the latent space where the flow 
> matching model operates. The vocoder converts mel spectrograms to waveforms.
> *Key components: text encoder, flow-matching decoder, HiFi-GAN vocoder.*
> *Caption: "Overview of the proposed architecture."*
```

**In-corpus reference format in `## References`:**

```markdown
- [b12] Smith et al. (2024). "VoiceFlow: Flow Matching for TTS." Interspeech 2024.
  → **In corpus:** [[arxiv-2401-12345]]
- [b13] Jones et al. (2023). "FastSpeech 3." arXiv.
  → Not in corpus.
```

---

### 5.1 Parse Manifest (`parse_manifest.json`)

Written after assembly. Records extraction quality metrics and flags issues for human review.

```python
@dataclass
class ParseManifest:
    paper_id: str
    parsed_date: str                # YYYY-MM-DD
    
    # Stage completion
    grobid_success: bool
    marker_success: bool
    vlm_figures_complete: bool
    vlm_tables_complete: bool
    assembly_success: bool
    
    # Quality metrics
    word_count: int                 # words in full_text.md
    section_count: int
    sections_detected: list[str]    # names of top-level sections found
    sections_missing: list[str]     # expected sections not found
    figure_count: int
    figures_with_vlm: int
    table_count: int
    tables_structured: int
    equation_count: int
    equations_with_latex: int
    reference_count: int
    references_in_corpus: int       # how many cited papers are also in raw/metadata/
    
    # Flags
    needs_human_review: bool
    review_reasons: list[str]       # e.g. ["section_count < 3", "abstract_missing"]
    
    # Layout
    layout_detected: str            # "single-column" | "two-column" | "mixed"
    page_count: int
```

**`needs_human_review` triggers:**
- `word_count < 1500` — likely extraction failure
- `section_count < 3` — sections not detected correctly
- `"Abstract" in sections_missing` — abstract not found
- `"Experiments" in sections_missing and "Results" in sections_missing` — experimental section missing
- Any VLM call returned a JSON parse error after 3 retries
- Any table validation failure (row/column mismatch, no proposed system row)

---

## 6. Configuration

```yaml
# config/parsing.yaml

# Tool paths and servers
grobid:
  url: "http://localhost:8070"
  timeout: 60                   # seconds per request
  docker_image: "lfoppiano/grobid:0.8.0"

marker:
  device: "cpu"                 # "cpu" | "cuda" | "mps"
  batch_size: 1                 # increase if GPU available
  langs: ["en"]

# Rasterisation
rasterisation:
  dpi: 300
  figure_margin_pt: 10          # padding around extracted regions
  min_region_size_pt: 50        # ignore regions smaller than this

# VLM
vlm:
  model: "claude-sonnet-4-20250514"
  max_tokens: 1024
  max_retries: 3
  retry_delay: 5                # seconds

# Assembly
assembly:
  include_equations_as_images: true
  include_reference_list: true
  highlight_in_corpus_refs: true

# Quality gates
quality:
  min_word_count: 1500
  min_section_count: 3
  required_sections: ["Abstract", "Introduction"]
```

---

## 7. Running the Pipeline

### Single paper

```bash
python scripts/parse/parse_paper.py --id arxiv-2501-12345
# Output: raw/parsed/arxiv-2501-12345/
```

### Batch (all accepted papers without a parsed directory)

```bash
python scripts/parse/parse_batch.py --status accepted --workers 4
# Processes papers in parallel where safe (GROBID and Marker are CPU-bound;
# VLM calls are I/O-bound and can run concurrently subject to API rate limits)
```

### Review flagged papers

```bash
python scripts/parse/parse_review.py
# Lists all papers where parse_manifest.needs_human_review = True
# with their review_reasons
```

### Re-parse a specific stage

```bash
python scripts/parse/parse_paper.py --id arxiv-2501-12345 --stage vlm
# Re-runs only the VLM stage, useful if a figure description failed
```

---

## 8. What the Ingest Agent Receives

After parsing, the ingest agent reads the following files for each paper. It never opens the PDF.

| File | Purpose |
|------|---------|
| `raw/parsed/{id}/full_text.md` | Full paper text with inline figure descriptions and table data |
| `raw/metadata/{id}.json` | Venue, date, status, task labels from filter agent |
| `raw/parsed/{id}/header.json` | Clean title, authors, abstract (GROBID) |
| `raw/parsed/{id}/references.json` | Structured references with in-corpus flags |
| `raw/parsed/{id}/parse_manifest.json` | Quality report — ingest agent checks `needs_human_review` first |

The ingest agent prompt should explicitly instruct the model to:
- Read `parse_manifest.json` first and flag any quality concerns before extracting information
- Treat `{{EQ:... | image: true}}` placeholders as signals that an equation exists but its content is not textually available
- Weight figure descriptions as primary evidence for architecture understanding
- Use `references_in_corpus` to populate `related_papers` in the wiki paper page

---

## 9. Open Questions

1. **GROBID vs. Marker for abstract extraction:** GROBID is more reliable for header parsing but requires a running server. Marker runs in-process. Should GROBID be optional (fallback to Marker header parsing) to simplify deployment? Recommend: GROBID optional but strongly recommended; document the Docker one-liner to start it.

2. **GPU availability:** Marker runs meaningfully faster on a GPU (10–30x). If a GPU is available, batch processing 300 papers takes ~1 hour. On CPU, estimate 8–15 hours. Is GPU access available, or should the pipeline be designed to run overnight on CPU? This affects whether `batch_size` and parallelism are worth configuring.

3. **VLM for all figures vs. selective:** Currently, all figures get a VLM description. For a paper with 6 figures, this is 6 API calls. Alternatively, limit VLM to figures whose captions mention "architecture", "overview", "model", or "system" — typically the 1–2 most important figures. This would halve API costs but miss result figures. Recommend: all figures for the first run; revisit if costs are higher than estimated.

4. **Equation handling:** For papers where equations are central to understanding the method (e.g. a new diffusion objective), `[Equation — see image]` placeholders in `full_text.md` are a meaningful gap for the ingest agent. Would it be worth adding a Nougat pass specifically for papers tagged with `diffusion` or `flow-matching` architecture? Nougat is slower than Marker but produces much better equation output.

5. **Storage budget:** At 300 DPI, figure images are ~200–500KB each. A 300-paper corpus with ~4 figures per paper → ~600MB for figures alone. With full PDFs already in `raw/papers/`, total `raw/` directory size will be 2–4GB. Is local storage a constraint, or is this acceptable?

---

## 10. Adopted Approach: Docling + Citation Graph

> This section supersedes §3–7 for implementation purposes. The GROBID+Marker design above remains as reference for the problem analysis (§2) and tool landscape (§3).

### 10.1 Primary Tool: Docling

The parsing pipeline is implemented as `scripts/parse/convert_paper.py` (prototyped in `convert_paper_with_docling_tmp.py`), using **Docling** as the single tool for layout analysis, full-text extraction, and figure/table extraction. This replaces the GROBID+Marker+PyMuPDF multi-tool stack.

**Why Docling:**
- Single dependency, no Docker server required
- Handles two-column layouts, produces clean Markdown in reading order
- Exports tables via DataFrame (handles merged cells better than Markdown serialisers)
- Extracts figure and table images with captions
- Optional formula enrichment (LaTeX for display equations) via `docling-ibm-models`
- Accepts local paths and URLs (including arXiv PDF URLs) directly

**Output per paper (`raw/parsed/{id}/`):**

| File | Contents |
|------|----------|
| `paper.md` | LLM-ready Markdown — body text, inline tables, `[FIGURE N]` placeholders |
| `metadata.json` | Title, authors, abstract, figure/table asset registries |
| `references.json` | Structured reference list with in-corpus flags (see §10.2) |
| `docling_native.json` | Docling's full internal document representation (debug/reprocessing) |
| `assets/figure-N.png` | Rasterised figure images (~144 DPI) |
| `assets/table-N.csv` | Table data as CSV (primary structured form) |
| `assets/table-N.png` | Table image (fallback for complex layouts) |

**VLM figure descriptions:** The Docling-based pipeline does not run a VLM pass on figures at parse time. Figures are extracted as images with captions. The ingest agent may optionally describe key figures (architecture diagrams, result graphs) when writing wiki paper pages, using the image files in `assets/`.

---

### 10.2 Reference Extraction

Each paper's reference list is extracted from Docling's document model (items labelled `REFERENCE` in `iterate_items()`) and written to `raw/parsed/{id}/references.json`.

**Extraction strategy (in priority order):**

1. **arXiv ID** — regex match on `arxiv.org/abs/NNNN.NNNNN` or bare `NNNN.NNNNN` patterns in the reference string. Most reliable key for corpus matching.
2. **DOI** — regex match on `doi.org/...` or `10.XXXX/...` patterns. Covers IEEE/ACL proceedings papers without arXiv IDs.
3. **Title fingerprint** — lowercase, punctuation-stripped title string for fuzzy matching against corpus metadata when neither arXiv ID nor DOI is available.

**`references.json` schema:**

```json
[
  {
    "ref_id": "b12",
    "raw": "Smith et al. (2024). VoiceFlow: Flow Matching for TTS. Interspeech 2024.",
    "title": "VoiceFlow: Flow Matching for TTS",
    "authors": ["Smith, J.", "Jones, A."],
    "year": 2024,
    "venue": "Interspeech 2024",
    "arxiv_id": "2401.12345",
    "doi": null,
    "in_corpus": true,
    "corpus_id": "2401.12345"
  }
]
```

`in_corpus` and `corpus_id` are resolved at parse time by checking `raw/metadata/` for a matching arXiv ID, DOI, or title fingerprint.

---

### 10.3 Citation Index

After each parse batch, `scripts/parse/build_citation_index.py` aggregates all `references.json` files into a single corpus-wide citation graph at `raw/citation_index.json`.

**Structure:**

```json
{
  "2401.12345": {
    "title": "VoiceFlow: Flow Matching for TTS",
    "arxiv_id": "2401.12345",
    "doi": null,
    "in_corpus": true,
    "corpus_id": "2401.12345",
    "cited_by": ["2502.00001", "2503.11234", "interspeech-2025-0042"],
    "citation_count": 3
  },
  "vandenOord2016": {
    "title": "WaveNet: A Generative Model for Raw Audio",
    "arxiv_id": "1609.03499",
    "doi": null,
    "in_corpus": false,
    "corpus_id": null,
    "cited_by": ["2501.00112", "2501.33421", "2502.00001", "..."],
    "citation_count": 47
  }
}
```

The index is keyed by arXiv ID where available, otherwise by a stable slug derived from `{first-author-surname}-{year}`.

**Rebuilding:** Run after each parse batch. The script is idempotent — it rebuilds from scratch by scanning all `references.json` files.

```bash
python scripts/parse/build_citation_index.py
# Reads: all raw/parsed/*/references.json
# Writes: raw/citation_index.json
```

---

### 10.4 Citation-Driven Corpus Expansion

The citation index is the primary mechanism for discovering foundational papers that predate the corpus's main collection window (2025) but are essential to understanding the field.

**How it works:**

- Papers cited by many corpus papers are almost certainly foundational works (WaveNet, VITS, HiFi-GAN, VALL-E, FastSpeech, etc.)
- High citation count within the corpus is a strong prior for relevance — these papers will score high through the normal filter agent
- The Citation Discovery Workflow (see `CLAUDE.md`) surfaces the top out-of-corpus candidates for user review and optional addition as `status: pending`

**Threshold guidance:**
- ≥ 3 citations: worth surfacing for review
- ≥ 10 citations: almost certainly worth adding
- ≥ 20 citations: foundational; add without filter review (high confidence)

The discovery workflow is designed to run periodically — after each significant parse batch — as the citation graph grows denser and new hubs emerge.
