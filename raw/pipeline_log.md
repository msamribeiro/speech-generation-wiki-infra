# Pipeline Log

Infra-only operations (filter, parse, discover, lint, review). Not rendered on the wiki site.

## 2026-05-12

- filter | arXiv | 404 accepted, 31 review, 69 rejected

## 2026-05-19

- review | arXiv | 31 borderline resolved → 15 accepted, 16 rejected | final corpus: 419 accepted, 85 rejected

## 2026-05-22

- filter | ACL 2025 + EMNLP 2025 + NAACL 2025 + Interspeech 2025 + arXiv + workshops pending batch | 300 accepted, 39 review, 56 rejected
- review | ACL 2025 + cs.CL batch | 39 borderline resolved → 25 accepted, 14 rejected | final corpus: 733 accepted, 166 rejected

## 2026-05-23

- parse | batch queue created | 36 batches × 20 papers (718 total) | batch 1 partial: 8/20 done | workflow: conversion in main session, quality inspection via lightweight sub-agent

## 2026-05-24

- discover | 450 candidates surfaced (86 speech-relevant), 264 corpus papers
- discover | 458 candidates surfaced (112 speech-relevant), 270 corpus papers

## 2026-05-25

- filter | keyword filter expanded (+11 terms: text to speech, speech-to-speech, speech interaction, voice interaction, spoken chatbot, speech foundation model, audio codec, speech tokenizer, voice assistant, voicemos, speech synthesizer) | re-scan triggered
- filter | ISCA 2025 re-scan | 1179 papers, 140 passed title filter, 12 new written
- filter | ACL Anthology 2025 re-scan | 14669 papers, 134 passed filter, 14 new written, 120 arXiv records enriched
- filter | arXiv cs.SD+eess.AS re-scan (2025-08-01→2026-05-25) | 3604 discovered, 555 passed filter, 70 new written
- filter | arxiv.py --ids 2301.02111 2407.05407 2412.10117 2406.02430 2410.06885 | 5 citation-discovery papers fetched (VALL-E, CosyVoice, CosyVoice 2, Seed-TTS, F5-TTS)
- filter | citation-discovery + re-scan batch | 101 papers scored in-conversation | 67 accepted, 7 review, 27 rejected | accept rate 66%

## 2026-05-26

- review | citation-discovery + re-scan batch | 7 borderline resolved → 3 accepted (2025.clicit-1.81, 2025.coling-industry.29, 2603.02022), 4 rejected | review queue cleared
- parse | batch 21 (queue batch 1) | 40 papers (2025.acl-long.388 … 2512.18706) | 40/40 done | Patched _REFS_HEADER_RE: added French "Références" and modifier-word prefix (e.g. "Bibliographical References"); 2510.03741 + 2510.25577 re-parsed, refs recovered
- parse | batch 22 (queue batch 2) | 40 papers (2512.20156 … 2601.19952) | 40/40 done | Clean run
- parse | batch 23 (queue batch 3) | 40 papers (2601.20094 … 2602.23068) | 40/40 done | Patched _REFS_HEADER_RE: added letter-prefix headings (e.g. "B. REFERENCES"); 2602.06053 re-parsed, 33 refs recovered | total parsed: 531/798

## 2026-05-27

- parse | batch 24 (queue batch 4) | 40 papers (2602.23266 … 2603.14032) | 40/40 done | RapidOCR: 2602.23765, 2603.08574, 2603.08823, 2603.09120, 2603.11589 (non-fatal) | total parsed: 571/798

## 2026-05-28

- lint | duplicate detected: 2410.06885 is arXiv preprint of 2025.acl-long.313 (ACL canonical) — wiki page and index entry removed, metadata set to rejected
- lint | full corpus duplicate scan — 14 arXiv/proceedings pairs resolved; arXiv IDs rejected, proceedings IDs canonical; 6 parsed output directories remapped from arXiv to proceedings IDs; corpus: 754 accepted, 29 ingested, 217 rejected
- parse | batch 25 (queue batch 5) | 40 papers (2603.14035 … 2604.06356) | 40/40 done | RapidOCR: 2603.14853, 2603.22252, 2603.23938, 2603.24144 (non-fatal) | total parsed: 611/783
- parse | batch 26 (queue batch 6) | 40 papers (2604.06871 … 2604.22821) | 40/40 done | RapidOCR: 2604.11424 (×4, non-fatal) | 0 refs: 2604.13288 (no References header, refs in body text, non-blocking) | total parsed: 651/783

## 2026-05-29

- parse | batch 27 (queue batch 7) | 40 papers (2604.25441 … interspeech-2025-0355) | 40/40 done | RapidOCR: 2605.05611 (×1), 2605.20946 (×2), interspeech-2025-0115 (×2) (non-fatal) | total in-corpus parsed: 681/783
- parse | batch 28 (queue batch 8) | 40 papers (interspeech-2025-0383 … interspeech-2025-1081) | 40/40 done | RapidOCR: 0408, 0433, 0669, 0756 (non-fatal) | total in-corpus parsed: 721/783

## 2026-05-30

- parse | batch 9 | 38 Interspeech 2025 papers (interspeech-2025-1084 … interspeech-2025-2031) | 38 done, 0 failed | RapidOCR warnings: 1531, 1595, 1641, 1684 (non-fatal) | parsed total: 759/783
- parse | batch 10 | 24 Interspeech 2025 papers (interspeech-2025-2032 … interspeech-2025-raju25_interspeech) | 24 done, 0 failed | RapidOCR warnings: 2032, 2586, 2739, 2815, cho25c, raju25 (non-fatal) | 4 slug-named papers are 2-page demos (short/few-refs expected) | parsed total: 783/783 — parse pipeline complete

## 2026-06-01

- schema | paper page template: added claims, field_significance, architecture figures, merged callout card
- schema | concept page template: research briefing redesign (Executive Summary, Major Claims, Relationship to Other Concepts, Representative Papers, Trend Summary)
- schema | evidence digest schema defined; wiki/concepts/_evidence/ created; integration agent Step 3 added
- schema | WRITING_STYLE.md created; callout system defined and applied to 100 paper pages
- schema | log split: wiki/log.md reader-only; raw/pipeline_log.md for infra ops; 26 entries migrated
- schema | venue page naming: {venue}-{year} → {year}-{venue}; 9 files renamed
- schema | Quartz display names: title frontmatter added to top-level files and folder index pages
- schema | wiki landing page redesigned; paper/concept/venue tables migrated to folder index pages
- schema | trends/ directory eliminated; replaced by reports/ and concept page Trend Summary sections
