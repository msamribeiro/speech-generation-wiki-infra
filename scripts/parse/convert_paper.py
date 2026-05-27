#!/usr/bin/env python3
"""
convert_paper.py — Single-paper PDF-to-Markdown converter using Docling.

Produces:
  raw/parsed/{id}/paper.md              LLM-ready Markdown (primary ingest target)
  raw/parsed/{id}/metadata.json         Title, authors, abstract, asset registries
  raw/parsed/{id}/references.json       Structured reference list with in-corpus flags
  raw/parsed/{id}/docling_native.json   Docling internal document representation
  raw/parsed/{id}/assets/               Figure PNGs, table CSVs and PNGs

Filesystem state semantics:
  DONE    — paper.md exists AND error.json absent
  FAILED  — error.json exists
  PENDING — neither exists

Usage (standalone):
    python scripts/parse/convert_paper.py --id 2501.12345
    python scripts/parse/convert_paper.py --pdf raw/papers/2501.12345.pdf
    python scripts/parse/convert_paper.py --id 2501.12345 --force

Importable API (used by batch_convert.py):
    from scripts.parse.convert_paper import convert_paper, build_corpus_index
    index  = build_corpus_index(RAW_METADATA)
    result = convert_paper(paper_id, pdf_path, output_dir, force, index)
"""

import argparse
import json
import logging
import re
import time
import traceback as tb_module
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    AcceleratorDevice,
    AcceleratorOptions,
    PdfPipelineOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling_core.types.doc import PictureItem, TableItem

_log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

ROOT         = Path(__file__).parent.parent.parent
RAW_METADATA = ROOT / "raw" / "metadata"
RAW_PAPERS   = ROOT / "raw" / "papers"
RAW_PARSED   = ROOT / "raw" / "parsed"

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

IMAGE_RESOLUTION_SCALE = 2.0   # ~144 DPI — good balance of quality and file size
FORMULA_ENRICHMENT     = True  # requires docling-ibm-models; adds ~30–60s/paper on CPU


# ---------------------------------------------------------------------------
# Result type
# ---------------------------------------------------------------------------

@dataclass
class ConversionResult:
    paper_id:      str
    success:       bool
    elapsed_s:     float
    output_dir:    Path
    md_path:       Optional[Path] = None
    skipped:       bool           = False   # already DONE and force=False
    error_type:    Optional[str]  = None
    error_message: Optional[str]  = None
    traceback:     Optional[str]  = None
    attempt_count: int            = 1


# ---------------------------------------------------------------------------
# Corpus index
# ---------------------------------------------------------------------------

def _normalise_doi(doi: str) -> str:
    return doi.lower().rstrip(".,;:/")


def build_corpus_index(metadata_dir: Path) -> dict:
    """
    Scan all metadata JSONs and build fast-lookup tables for in-corpus matching.

    Returns:
        {
            "arxiv": {arxiv_id: corpus_id, ...},
            "doi":   {normalised_doi: corpus_id, ...},
        }
    """
    arxiv_lookup: dict[str, str] = {}
    doi_lookup:   dict[str, str] = {}

    for f in metadata_dir.glob("*.json"):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except Exception:
            continue

        corpus_id = d.get("id")
        if not corpus_id:
            continue

        source_ids = d.get("source_ids") or {}

        # arXiv ID — prefer source_ids.arxiv; fall back to bare ID if it looks like one
        arxiv_id = source_ids.get("arxiv")
        if not arxiv_id and re.match(r"^\d{4}\.\d{4,5}$", corpus_id):
            arxiv_id = corpus_id
        if arxiv_id:
            arxiv_lookup[arxiv_id] = corpus_id

        doi = source_ids.get("doi")
        if doi:
            doi_lookup[_normalise_doi(doi)] = corpus_id

    return {"arxiv": arxiv_lookup, "doi": doi_lookup}


# ---------------------------------------------------------------------------
# Reference extraction helpers
# ---------------------------------------------------------------------------

_ARXIV_URL_RE    = re.compile(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?", re.I)
_ARXIV_PREFIX_RE = re.compile(r"\barxiv[:\s]+(\d{4}\.\d{4,5})(?:v\d+)?", re.I)
# Bare arXiv IDs: require 5-digit sequence to reduce false positives (years look like NNNN.N)
_ARXIV_BARE_RE   = re.compile(r"\b((?:1[2-9]|2[0-9])\d{2}\.\d{5})\b")
_DOI_RE          = re.compile(r"\b(10\.\d{4,9}/\S+)")
_YEAR_RE         = re.compile(r"\b((?:19|20)\d{2})\b")
# Matches text in straight or curly double quotes — common for paper titles in IEEE/ACM style
_QUOTED_TITLE_RE = re.compile(r'[“"](.{15,200}?)[”"]')


def _extract_arxiv_id(text: str) -> Optional[str]:
    for pattern in (_ARXIV_URL_RE, _ARXIV_PREFIX_RE, _ARXIV_BARE_RE):
        m = pattern.search(text)
        if m:
            return m.group(1)
    return None


def _extract_doi(text: str) -> Optional[str]:
    m = _DOI_RE.search(text)
    if not m:
        return None
    return m.group(1).rstrip(".,;:)")


def _extract_year(text: str) -> Optional[int]:
    for y in reversed(_YEAR_RE.findall(text)):
        y_int = int(y)
        if 1950 <= y_int <= 2030:
            return y_int
    return None


def _extract_title(text: str) -> tuple[Optional[str], str]:
    """Return (title, confidence). Confidence is 'high' (from quotes) or 'low' (absent)."""
    m = _QUOTED_TITLE_RE.search(text)
    if m:
        return m.group(1).strip(), "high"
    return None, "low"


def _parse_ref_string(ref_id: str, raw: str, arxiv_lookup: dict, doi_lookup: dict) -> dict:
    arxiv_id         = _extract_arxiv_id(raw)
    doi              = _extract_doi(raw)
    doi_norm         = _normalise_doi(doi) if doi else None
    title, title_conf = _extract_title(raw)

    corpus_id = None
    if arxiv_id and arxiv_id in arxiv_lookup:
        corpus_id = arxiv_lookup[arxiv_id]
    elif doi_norm and doi_norm in doi_lookup:
        corpus_id = doi_lookup[doi_norm]

    return {
        "ref_id":           ref_id,
        "raw":              raw,
        "title":            title,
        "title_confidence": title_conf,
        "authors":          [],
        "year":             _extract_year(raw),
        "venue":            None,
        "arxiv_id":         arxiv_id,
        "doi":              doi,
        "in_corpus":        corpus_id is not None,
        "corpus_id":        corpus_id,
    }


_REFS_HEADER_RE = re.compile(
    r"^(?:\d+\.?\s*|[ivxlcdm]+\.\s*|[A-Z]\.\s*)(?:\w+\s+)*(?:references?|bibliography|références?)$"
    r"|^(?:\w+\s+)*(?:references?|bibliography|références?)$",
    re.IGNORECASE,
)

# Matches conclusion section headers (with optional numeric/roman prefix).
# Used by the third reference-extraction fallback for papers that place their
# reference list immediately after the conclusion with no "References" heading.
_CONCLUSION_HEADER_RE = re.compile(
    r"^(?:(?:\d+\.?\s+|[ivxlcdm]+\.\s+)?)"
    r"(?:concluding\s+remarks|conclusions?(?:\s+and\s+[\w\s]+)?)$",
    re.IGNORECASE,
)

# Venue/format signals that distinguish a reference string from narrative body text.
_REF_SIGNAL_RE = re.compile(
    r"arxiv|corr\b|doi:|proceedings|conference|workshop|journal|preprint|transactions|"
    r"vol\.\s*(?:abs/)?\d|\bpp\.\s*\d|\bpages?\s+\d",
    re.IGNORECASE,
)

# Author-name patterns (case-sensitive): AAAI style "Lastname, F." and IEEE style "F. Lastname,".
# These appear in virtually every reference string but not in conclusion body paragraphs.
_AUTHOR_RE = re.compile(
    r"et al\.|[A-Z][a-z]{1,15},\s+[A-Z]\.|[A-Z]\.\s+[A-Z][a-z]{1,15},"
)

# Loose year match for the third fallback — no trailing \b so it also matches
# AAAI disambiguation suffixes like "2024a" and "2024b".
_YEAR_LOOSE_RE = re.compile(r"(?:19|20)\d{2}")


def extract_references(doc, corpus_index: dict) -> list[dict]:
    """
    Harvest reference items from a Docling document and resolve each against
    the corpus index.

    Primary path: items explicitly labelled REFERENCE.
    Second fallback: items (text / list_item) that follow a "References" section
    header — used for papers where Docling labels the reference list as body text.
    Third fallback: items after a Conclusion section header that pass a year +
    venue-signal heuristic — used for papers (IEEE, AAAI style) that place the
    reference list immediately after the conclusion with no "References" heading.
    """
    arxiv_lookup = corpus_index.get("arxiv", {})
    doi_lookup   = corpus_index.get("doi",   {})

    refs    = []
    counter = 0

    # Primary: explicitly labelled REFERENCE items
    for item, _ in doc.iterate_items():
        if not hasattr(item, "label") or not hasattr(item, "text"):
            continue
        label_name = item.label.name if hasattr(item.label, "name") else str(item.label)
        if label_name != "REFERENCE":
            continue
        raw = item.text.strip()
        if raw:
            counter += 1
            refs.append(_parse_ref_string(f"b{counter}", raw, arxiv_lookup, doi_lookup))

    if refs:
        return refs

    # Fallback: collect text/list_item items after the References section header
    in_refs = False
    for item, _ in doc.iterate_items():
        if not hasattr(item, "label") or not hasattr(item, "text"):
            continue
        label_name = item.label.name if hasattr(item.label, "name") else str(item.label)
        text       = item.text.strip()
        if not text:
            continue

        if label_name == "SECTION_HEADER":
            if _REFS_HEADER_RE.match(text.strip()):
                in_refs = True
            else:
                in_refs = False  # new section started — stop collecting
            continue

        if in_refs and label_name in ("TEXT", "LIST_ITEM", "REFERENCE") and len(text) >= 20:
            counter += 1
            refs.append(_parse_ref_string(f"b{counter}", text, arxiv_lookup, doi_lookup))

    if refs:
        return refs

    # Third fallback: items after a Conclusion section header that look like references.
    # Handles papers where the reference list appears inline after the conclusion with
    # no "References" heading (seen in IEEE and AAAI formatted papers).
    after_conclusion = False
    for item, _ in doc.iterate_items():
        if not hasattr(item, "label") or not hasattr(item, "text"):
            continue
        label_name = item.label.name if hasattr(item.label, "name") else str(item.label)
        text       = item.text.strip()
        if not text:
            continue

        if label_name == "SECTION_HEADER":
            if _CONCLUSION_HEADER_RE.match(text):
                after_conclusion = True
            elif after_conclusion:
                after_conclusion = False  # appendix or next major section — stop
            continue

        if (after_conclusion
                and label_name in ("TEXT", "LIST_ITEM")
                and len(text) >= 20
                and _YEAR_LOOSE_RE.search(text)
                and (_REF_SIGNAL_RE.search(text) or _AUTHOR_RE.search(text))):
            counter += 1
            refs.append(_parse_ref_string(f"b{counter}", text, arxiv_lookup, doi_lookup))

    return refs


# ---------------------------------------------------------------------------
# Docling pipeline
# ---------------------------------------------------------------------------

def _build_pipeline_options() -> PdfPipelineOptions:
    opts = PdfPipelineOptions()
    opts.images_scale            = IMAGE_RESOLUTION_SCALE
    opts.generate_page_images    = False
    opts.generate_picture_images = True
    opts.generate_table_images   = True

    # Force CPU — MPS (Apple Silicon GPU) does not support float64, which Docling
    # requires in its layout model. CPU is slower but universally compatible.
    opts.accelerator_options = AcceleratorOptions(device=AcceleratorDevice.CPU)

    if FORMULA_ENRICHMENT:
        try:
            opts.do_formula_enrichment = True
            _log.debug("Formula enrichment enabled.")
        except AttributeError:
            _log.warning("Formula enrichment unavailable in this Docling version.")

    return opts


def _make_converter() -> DocumentConverter:
    return DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=_build_pipeline_options())
        }
    )


# ---------------------------------------------------------------------------
# Helpers (from convert_paper_with_docling_tmp.py)
# ---------------------------------------------------------------------------

def _slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:60]


def _extract_metadata(doc) -> dict:
    metadata = {"title": None, "authors": [], "abstract": None}

    for item, _ in doc.iterate_items():
        if not hasattr(item, "label") or not hasattr(item, "text"):
            continue
        label_name = item.label.name if hasattr(item.label, "name") else str(item.label)
        if label_name == "TITLE":
            metadata["title"] = item.text.strip()
            break

    # Build a flat list of (label_name, text) for all items with text
    labelled = []
    for item, _ in doc.iterate_items():
        if not hasattr(item, "text") or not item.text.strip():
            continue
        label_name = item.label.name if hasattr(item.label, "name") else str(item.label)
        labelled.append((label_name, item.text.strip()))

    # Abstract extraction — four strategies in priority order:
    # 1. Standalone "abstract" / "abstract." text item → grab next text/list item
    # 2. "Abstract - ..." or "Abstract— ..." merged item (IEEE style)
    # 3. section_header whose text contains "abstract" → grab next text/list item
    # 4. Fallback: first substantial text item (>80 chars) before any Introduction heading
    prev_was_abstract_heading = False
    for label, text in labelled:
        text_lower = text.lower()

        # Strategy 2: merged "Abstract - body" item
        m = re.match(r'^abstract\s*[-—]\s*(.+)', text, re.IGNORECASE | re.DOTALL)
        if m:
            metadata["abstract"] = m.group(1).strip()
            break

        # Strategy 1: standalone heading in a text item
        if label == "TEXT" and text_lower in ("abstract", "abstract."):
            prev_was_abstract_heading = True
            continue

        # Strategy 3: numbered/section heading containing "abstract"
        if label == "SECTION_HEADER" and re.search(r'\babstract\b', text_lower):
            prev_was_abstract_heading = True
            continue

        if prev_was_abstract_heading and label in ("TEXT", "LIST_ITEM"):
            metadata["abstract"] = text
            break

        # Reset on any other section heading
        if label == "SECTION_HEADER":
            prev_was_abstract_heading = False

    # Strategy 4: fallback for tech reports with no abstract heading
    if metadata["abstract"] is None:
        for label, text in labelled:
            if label == "SECTION_HEADER" and re.search(r'\bintroduction\b', text.lower()):
                break
            if label == "TEXT" and len(text) > 80:
                metadata["abstract"] = text
                break

    return metadata


def _table_to_clean_markdown(df: pd.DataFrame) -> str:
    df = df.copy()
    if not df.empty:
        df.iloc[:, 0] = df.iloc[:, 0].ffill()
    df = df.fillna("")
    # pandas ≥2.1 deprecates applymap in favour of map
    try:
        df = df.applymap(lambda x: str(x).strip() if x != "" else "")
    except AttributeError:
        df = df.map(lambda x: str(x).strip() if x != "" else "")
    return df.to_markdown(index=False)


def _get_caption(item, doc) -> str:
    caption = ""
    try:
        if hasattr(item, "captions") and item.captions:
            caption = " ".join(c.text for c in item.captions if hasattr(c, "text"))
        elif hasattr(item, "caption_text"):
            caption = item.caption_text(doc)
    except Exception:
        pass
    return caption.strip()


def _looks_garbled(text: str) -> bool:
    if not text:
        return True
    non_ascii = sum(1 for c in text if ord(c) > 127)
    pua       = sum(1 for c in text if 0xE000 <= ord(c) <= 0xF8FF)
    return (pua / max(len(text), 1)) > 0.1 or (non_ascii / max(len(text), 1)) > 0.6


# ---------------------------------------------------------------------------
# Markdown assembly
# ---------------------------------------------------------------------------

_SKIP_LABELS = {"PAGE_HEADER", "PAGE_FOOTER", "FOOTNOTE", "REFERENCE"}


def _assemble_markdown(conv_res, assets_dir: Path, title_override: Optional[str] = None) -> tuple[str, dict]:
    """
    Walk the Docling document in reading order and produce a single clean
    Markdown string suitable for LLM ingestion.

    Returns (markdown_text, docling_metadata_dict).
    REFERENCE items are skipped here — they are captured in references.json.
    """
    doc      = conv_res.document
    metadata = _extract_metadata(doc)

    # Corpus metadata title is more reliable than Docling's extraction
    # (Docling often labels the title as SECTION_HEADER, not TITLE)
    if title_override:
        metadata["title"] = title_override

    lines            = []
    table_counter    = 0
    picture_counter  = 0
    table_registry   = {}
    figure_registry  = {}

    lines += ["---",
              f"title: {json.dumps(metadata['title'] or 'Unknown')}",
              "---", ""]

    if metadata["title"]:
        lines += [f"# {metadata['title']}", ""]

    if metadata["abstract"]:
        lines += ["## Abstract", "", metadata["abstract"], ""]

    abstract_emitted      = metadata["abstract"] is not None
    in_abstract_section   = False   # True while iterating the abstract body

    for item, level in doc.iterate_items():

        # --- Tables ---
        if isinstance(item, TableItem):
            table_counter += 1
            caption  = _get_caption(item, doc)
            png_path = assets_dir / f"table-{table_counter}.png"
            csv_path = assets_dir / f"table-{table_counter}.csv"

            try:
                img = item.get_image(doc)
                if img:
                    img.save(png_path, "PNG")
                else:
                    png_path = None
            except Exception as e:
                _log.debug(f"table {table_counter} image: {e}")
                png_path = None

            md_table = None
            try:
                df = item.export_to_dataframe(doc)
                if df is not None and not df.empty:
                    df.to_csv(csv_path, index=False)
                    md_table = _table_to_clean_markdown(df)
            except Exception as e:
                _log.debug(f"table {table_counter} dataframe: {e}")

            table_registry[table_counter] = {
                "csv_path": str(csv_path) if csv_path.exists() else None,
                "png_path": str(png_path) if png_path and Path(png_path).exists() else None,
                "caption":  caption,
            }

            lines.append(f"### Table {table_counter}")
            if caption:
                lines += [f"*{caption}*", ""]
            if md_table:
                lines.append(md_table)
            else:
                lines.append(f"*[Table {table_counter} could not be parsed — see assets/table-{table_counter}.png]*")
            lines.append("")
            continue

        # --- Figures ---
        if isinstance(item, PictureItem):
            picture_counter += 1
            caption  = _get_caption(item, doc)
            png_path = assets_dir / f"figure-{picture_counter}.png"

            try:
                img = item.get_image(doc)
                if img:
                    img.save(png_path, "PNG")
                else:
                    png_path = None
            except Exception as e:
                _log.debug(f"figure {picture_counter} image: {e}")
                png_path = None

            figure_registry[picture_counter] = {
                "png_path": str(png_path) if png_path and Path(png_path).exists() else None,
                "caption":  caption,
            }

            lines.append(
                f"[FIGURE {picture_counter}"
                + (f": {caption}" if caption else "")
                + f" — see assets/figure-{picture_counter}.png]"
            )
            lines.append("")
            continue

        # --- Text items ---
        if not hasattr(item, "label") or not hasattr(item, "text"):
            continue

        label_name = item.label.name if hasattr(item.label, "name") else str(item.label)

        if label_name in _SKIP_LABELS:
            continue

        text = item.text.strip()
        if not text:
            continue

        if label_name == "SECTION_HEADER":
            in_abstract_section = False  # reset: we're leaving any prior section
            # Skip reference/bibliography heading — content goes to references.json
            if _REFS_HEADER_RE.match(text.strip()):
                continue
            # Skip abstract heading and mark its body for skipping
            if abstract_emitted and text.lower().strip() in ("abstract", "abstract."):
                in_abstract_section = True
                continue
            depth          = max(1, level) if level else 2
            heading_hashes = "#" * min(depth + 1, 4)
            lines += [f"{heading_hashes} {text}", ""]
            continue

        if in_abstract_section:
            continue  # body text already emitted in frontmatter

        if label_name == "TITLE":
            continue  # already emitted in frontmatter

        if label_name == "FORMULA":
            if FORMULA_ENRICHMENT and text and not _looks_garbled(text):
                lines += [f"```math\n{text}\n```", ""]
            else:
                lines += ["*[Equation — see original PDF]*", ""]
            continue

        if label_name == "CODE":
            lines += [f"```\n{text}\n```", ""]
            continue

        if label_name == "LIST_ITEM":
            lines.append(f"- {text}")
            continue

        lines += [text, ""]

    metadata["figures"] = figure_registry
    metadata["tables"]  = table_registry
    return "\n".join(lines), metadata


# ---------------------------------------------------------------------------
# Error state helpers
# ---------------------------------------------------------------------------

def _read_attempt_count(output_dir: Path) -> int:
    error_file = output_dir / "error.json"
    if not error_file.exists():
        return 0
    try:
        return json.loads(error_file.read_text()).get("attempt_count", 0)
    except Exception:
        return 0


def _write_error(output_dir: Path, paper_id: str, exc: Exception, attempt_count: int) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    record = {
        "id":            paper_id,
        "error_type":    type(exc).__name__,
        "error_message": str(exc),
        "traceback":     tb_module.format_exc(),
        "timestamp":     datetime.now().isoformat(),
        "attempt_count": attempt_count,
    }
    (output_dir / "error.json").write_text(
        json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8"
    )


def _is_done(output_dir: Path) -> bool:
    return (output_dir / "paper.md").exists() and not (output_dir / "error.json").exists()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def convert_paper(
    paper_id:     str,
    pdf_path:     Path,
    output_dir:   Path,
    force:        bool                      = False,
    corpus_index: Optional[dict]            = None,
    converter:    Optional[DocumentConverter] = None,
) -> ConversionResult:
    """
    Convert a single paper PDF to LLM-ready Markdown and supporting files.

    Args:
        paper_id:     Corpus ID (used for filenames and error records).
        pdf_path:     Absolute path to the source PDF.
        output_dir:   Destination directory (raw/parsed/{id}/).
        force:        Re-extract even if already DONE.
        corpus_index: Pre-built index from build_corpus_index(); built on demand if None.
        converter:    Docling DocumentConverter; created on demand if None (slow — ~30s).

    Returns:
        ConversionResult with success flag and timing.
    """
    t0 = time.monotonic()

    if _is_done(output_dir) and not force:
        return ConversionResult(
            paper_id=paper_id,
            success=True,
            elapsed_s=time.monotonic() - t0,
            output_dir=output_dir,
            md_path=output_dir / "paper.md",
            skipped=True,
        )

    attempt_count = _read_attempt_count(output_dir) + 1
    assets_dir    = output_dir / "assets"

    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        assets_dir.mkdir(exist_ok=True)

        if corpus_index is None:
            corpus_index = build_corpus_index(RAW_METADATA)

        if converter is None:
            converter = _make_converter()

        _log.info(f"[{paper_id}] converting…")
        conv_res = converter.convert(str(pdf_path))

        _log.debug(f"[{paper_id}] assembling markdown…")
        corpus_title = None
        meta_path = RAW_METADATA / f"{paper_id}.json"
        if meta_path.exists():
            try:
                corpus_title = json.loads(meta_path.read_text(encoding="utf-8")).get("title")
            except Exception:
                pass
        markdown, doc_metadata = _assemble_markdown(conv_res, assets_dir, title_override=corpus_title)

        _log.debug(f"[{paper_id}] extracting references…")
        refs = extract_references(conv_res.document, corpus_index)

        # Write supporting files first (non-atomic — failures here are caught and
        # will prevent paper.md from being written, so state stays FAILED/PENDING)
        (output_dir / "metadata.json").write_text(
            json.dumps(doc_metadata, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        (output_dir / "references.json").write_text(
            json.dumps(refs, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        _log.debug(f"[{paper_id}] saving docling native JSON…")
        conv_res.document.save_as_json(output_dir / "docling_native.json")

        # paper.md is the DONE sentinel — write atomically via tmp → rename
        tmp_md = output_dir / "paper.md.tmp"
        tmp_md.write_text(markdown, encoding="utf-8")
        tmp_md.replace(output_dir / "paper.md")

        # Clean up any prior error record now that we succeeded
        error_file = output_dir / "error.json"
        if error_file.exists():
            error_file.unlink()

        n_figs   = len(doc_metadata.get("figures") or {})
        n_tables = len(doc_metadata.get("tables")  or {})
        n_refs   = len(refs)
        _log.info(
            f"[{paper_id}] done — {n_figs} figures, {n_tables} tables, "
            f"{n_refs} refs ({sum(r['in_corpus'] for r in refs)} in corpus)"
        )

        return ConversionResult(
            paper_id=paper_id,
            success=True,
            elapsed_s=time.monotonic() - t0,
            output_dir=output_dir,
            md_path=output_dir / "paper.md",
            attempt_count=attempt_count,
        )

    except Exception as exc:
        _write_error(output_dir, paper_id, exc, attempt_count)
        return ConversionResult(
            paper_id=paper_id,
            success=False,
            elapsed_s=time.monotonic() - t0,
            output_dir=output_dir,
            error_type=type(exc).__name__,
            error_message=str(exc),
            traceback=tb_module.format_exc(),
            attempt_count=attempt_count,
        )


# ---------------------------------------------------------------------------
# CLI (standalone use)
# ---------------------------------------------------------------------------

def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--id",
        metavar="ID",
        help="Corpus paper ID — looks up pdf_path from raw/metadata/{id}.json",
    )
    group.add_argument(
        "--pdf",
        metavar="PATH",
        type=Path,
        help="Direct path to a PDF file",
    )
    parser.add_argument(
        "--output",
        metavar="DIR",
        type=Path,
        help="Output directory (default: raw/parsed/{id}/)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-extract even if output already exists (DONE state)",
    )
    args = parser.parse_args()

    if args.id:
        meta_path = RAW_METADATA / f"{args.id}.json"
        if not meta_path.exists():
            parser.error(f"Metadata not found: {meta_path}")
        meta       = json.loads(meta_path.read_text())
        paper_id   = meta["id"]
        pdf_path   = ROOT / meta["pdf_path"]
        output_dir = args.output or (RAW_PARSED / paper_id)
    else:
        pdf_path   = args.pdf.resolve()
        paper_id   = pdf_path.stem
        output_dir = args.output or (RAW_PARSED / paper_id)

    if not pdf_path.exists():
        parser.error(f"PDF not found: {pdf_path}")

    corpus_index = build_corpus_index(RAW_METADATA)
    result       = convert_paper(paper_id, pdf_path, output_dir, args.force, corpus_index)

    if result.skipped:
        print(f"Skipped (already done): {output_dir / 'paper.md'}")
        print("Use --force to re-extract.")
    elif result.success:
        print(f"Done in {result.elapsed_s:.1f}s")
        print(f"  paper.md:       {result.md_path}")
        print(f"  metadata.json:  {output_dir / 'metadata.json'}")
        print(f"  references.json:{output_dir / 'references.json'}")
    else:
        print(f"FAILED after {result.elapsed_s:.1f}s: {result.error_type}: {result.error_message}")
        print(f"  error.json: {output_dir / 'error.json'}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
