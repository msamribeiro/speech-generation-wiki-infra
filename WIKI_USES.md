# Wiki — Potential Uses Once Complete

Assumes: ~800 papers parsed and ingested, all concept pages finalized, year-on-year trend pages written.

---

## 1. RAG-powered research assistant

Build a retrieval-augmented system on the wiki to answer structured queries with grounded citations. The controlled vocabulary, standardized metrics, and wikilinks make this unusually good retrieval substrate vs. raw PDFs. The structured YAML frontmatter enables filtered retrieval (e.g., only `code_available: true`, only a specific venue or task).

Example queries:
- *"Best zero-shot TTS by SPK-SIM as of mid-2025, excluding proprietary systems?"*
- *"Which papers use EnCodec but not autoregressive decoding?"*
- *"Open-source flow-matching TTS systems and their WER on LibriSpeech test-clean?"*

---

## 2. Living benchmark leaderboard

Standardized metric fields (MOS, WER, SPK-SIM, etc.) across 800 papers — with test-set attribution already enforced — are enough to build a dynamic leaderboard the field currently lacks.

Key angle: detect **metric inflation over time** — are scores genuinely improving, or are papers switching to easier test sets? The trend pages set this up.

---

## 3. Systematic review / survey paper

The wiki is a systematic review by structure. With 800 papers, controlled vocabulary, trend pages, and a citation graph, the narrative synthesis work is the remaining gap — and that's what a well-prompted LLM on the wiki can produce.

Publishable targets: JMLR, IEEE Signal Processing Magazine, long arXiv survey. The living nature of the wiki means it can be updated annually, unlike a one-shot survey.

---

## 4. Research gap map

The "Open questions" and "Limitations" sections across all concept and paper pages form a **structured map of what the field hasn't solved**. Useful for:
- Framing new research directions
- Grant writing
- Identifying where a paper would be genuinely novel vs. incremental

Probably the highest-leverage output for someone actively doing research in the space.

---

## 5. Org / lab intelligence dashboard

The `organization` field and venue/year pages enable questions like:
- *What is Google publishing in TTS this year vs. last?*
- *Is Microsoft shifting from diffusion to flow-matching?*
- *Which academic groups are driving VC research?*

Useful for competitive intelligence (industry) and collaboration mapping (academia).

---

## 6. Automated related-work generation

Feed a new paper's abstract + method into a retrieval pass over the wiki to get a structured related-work section with proper citations. The concept taxonomy makes it easy to organize by theme rather than chronology — how good related-work sections are actually written.

---

## 7. Continuous ingestion as a monitoring service

Once the pipeline (fetch → filter → parse → ingest) is stable, run it on a monthly schedule. New papers are automatically flagged against existing concept pages. Pairs with the RAG assistant to keep the knowledge base current without manual effort.

---

## Priority / effort notes

| Idea | Buildability now | External impact | Research value |
|------|-----------------|-----------------|----------------|
| RAG assistant | High | Medium | High |
| Benchmark leaderboard | High | High | Medium |
| Survey paper | Medium | Very high | High |
| Research gap map | Low (needs synthesis) | Medium | Very high |
| Org intelligence | High | Medium | Low |
| Related-work gen | High | Medium | High |
| Continuous ingestion | Medium | High | Medium |
