# TTS → SCA Shift Analysis — Working Notes

**Status:** Preliminary / in progress. Not committed. Pick up from here.  
**Started:** 2026-06-07  
**Artifacts:** See end of this document.

---

## Hypothesis

> Within the speech generation literature, are we observing a structural shift from text-to-speech (TTS) as the dominant research direction toward spoken conversational agents (SCA)?

The motivation: the citation comparison between H2 2025 and H1 2026 surfaced Moshi rising from #3 to #1 (citation rate 0.208 → 0.308), VALL-E dropping from #8 to #54, and Qwen2.5-Omni entering the top 3. Moshi, GLM-4-Voice, Spark-TTS, and KimiAudio dominate Q2 2026 citations in a way that has no parallel in Q3 2025. This raised the question: is the field pivoting?

---

## Analytical Approach and Its Evolution

### Step 1 — Half-year citation comparison (H2 2025 vs H1 2026)

**What we did:** Normalised citation rates (citations / papers in window) for the top 100 papers in each half-year, then compared risers and fallers.

**What we found:** Moshi dominates H1 2026, Qwen ecosystem rises sharply, VALL-E family collapses. The narrative is compelling.

**Problem raised:** H2 2025 includes Interspeech (September), H1 2026 does not. Interspeech is TTS-heavy. Comparing half-years across conference seasons may be comparing apples to oranges — TTS citation rates could be elevated in H2 simply because Interspeech papers are doing the citing.

**Resolution:** The citation seasonality concern is real, but the quarterly citation top-10 analysis (step 3) shows the Q3→Q4 transition within H2 2025 itself produces the same pattern. The VALL-E family drops out of the top-10 between Q3 and Q4 2025, before any window boundary. So the half-year comparison was directionally correct even if noisy.

---

### Step 2 — Task distribution by month / quarter (what the corpus produces)

**What we did:** Counted papers tagged TTS / SCA / VC / codec / evaluation per month and quarter from `raw/metadata/*.json`. Also computed a 3-month sliding window SCA/TTS ratio.

**Key concern raised:** The corpus is filtered by keyword. TTS vocabulary ("text-to-speech", "speech synthesis", "TTS") appears in almost every TTS paper title. SCA vocabulary is heterogeneous — "omni", "real-time dialogue", "voice chat" are not in our filter and are documented false-negative patterns (Moshi, Mini-omni, Qwen2.5-Omni title-only). This means TTS papers pass the filter at higher rates than SCA papers, so corpus composition percentages are not reliable proxies for field composition percentages.

**Second concern raised (and corrected):** Whether the keyword filter evolved during the corpus build, which would create temporal artefacts in the task distribution. User confirmed the full time window was re-fetched after keywords were finalised. So the filter is consistent across all quarters — temporal comparisons within the corpus are valid, absolute percentages are not.

**What we found (quarterly task distribution):**

| Quarter   |  N  | TTS  |  SCA  |  VC   |
|-----------|-----|------|-------|-------|
| Q3 2025   | 352 | 63%  | 18.5% | 17.6% |
| Q4 2025   | 172 | 54%  | 26.2% | 13.4% |
| Q1 2026   | 167 | 65%  | 23.4% |  6.0% |
| Q2 2026*  | 122 | 68%  | 31.1% |  9.0% |

VC's decline is the most robust finding: halving from Q3 to Q1. SCA appears to grow from 18.5% to 31%, but this uses all venues mixed.

---

### Step 3 — Quarterly citation top-10 (what the corpus builds on)

**What we did:** For each quarter, computed citation rates across all out-of-corpus references from papers in that window. Top 10 by rate.

**What we found:**

| Quarter  | #1 | #2 | #3 | Classic TTS in top 10? |
|----------|----|----|-----|------------------------|
| Q3 2025  | Moshi (0.159) | CosyVoice 2 | VALL-E orig (0.131) | Yes — VALL-E orig, VALL-E 2, CosyVoice v1, SeedTTS |
| Q4 2025  | Moshi (0.262) | Qwen2.5-Omni | EnCodec | No — replaced by Spark-TTS, GLM-4-Voice, Llama-Omni |
| Q1 2026  | Moshi (0.287) | Qwen2.5-Omni | Spark-TTS | No |
| Q2 2026* | Moshi (0.311) | KimiAudio | Qwen2.5-Omni | No — Gemini 2.5, VoiceBench enter |

The Q3→Q4 2025 boundary is the inflection point: VALL-E family papers disappear from the top-10 citations and the list becomes SCA-infrastructure-anchored. This holds even within H2 2025, so it is not a half-year boundary artefact.

---

### Step 4 — Venue decomposition (is Interspeech skewing Q3?)

**What we did:** Split each quarter into arXiv vs conference papers and computed task distributions separately. Also ran the sliding window analysis on arXiv-only papers.

**What we found:**

Q3 2025 venue breakdown (N=352):
- arXiv: 190 (54%)
- Interspeech: 122 (35%)
- ACL: 34 (10%)

Task distributions within Q3 2025:

| Slice       |  N  | TTS  | SCA  |  VC  |
|-------------|-----|------|------|------|
| arXiv       | 190 | 64.7%| 20.0%| 14.2%|
| Conference  | 162 | 61.7%| 16.7%| 21.6%|

Interspeech is **not** inflating TTS relative to arXiv — TTS rates are similar (62% vs 65%). What Interspeech elevates is **VC** (21.6% vs 14.2%). The SCA suppression at conference venues is modest (16.7% vs 20.0%).

The more notable venue effect is in Q4: EMNLP and NeurIPS papers show **SCA at 41.2%** (vs arXiv's 22.5%). SCA work is appearing at NLP venues, not just speech venues. This inflates Q4's aggregate SCA figure slightly.

**arXiv-only sliding window (3-month, 1-month step):**

| Window           |  N  | TTS% | SCA% |  VC% | SCA/TTS |
|------------------|-----|------|------|------|---------|
| 2025-07–2025-09  | 190 | 64.7%| 20.0%| 14.2%|   0.31  |
| 2025-08–2025-10  | 223 | 59.6%| 22.9%| 12.1%|   0.38  |
| 2025-09–2025-11  | 205 | 58.5%| 22.4%| 12.2%|   0.38  |
| 2025-10–2025-12  | 138 | 54.3%| 22.5%| 13.0%|   0.41  |
| 2025-11–2026-01  | 135 | 60.0%| 23.0%| 11.9%|   0.38  |
| 2025-12–2026-02  | 128 | 64.1%| 22.7%|  7.8%|   0.35  |
| 2026-01–2026-03  | 166 | 65.7%| 23.5%|  6.0%|   0.36  |
| 2026-02–2026-04  | 161 | 68.9%| 28.0%|  4.3%|   0.41  |
| 2026-03–2026-05  | 172 | 68.0%| 27.3%|  7.0%|   0.40  |

In the arXiv-only slice, SCA is a stable 20–24% through most of the window. The SCA/TTS ratio fluctuates between 0.31 and 0.41 with no monotonic trend. A possible uptick appears in the last two windows (Feb–May 2026) at 0.40–0.41, but it is not clearly distinguished from noise given the fluctuation throughout.

---

## Preliminary Conclusions

**What the corpus supports:**

1. **VC is declining robustly.** From ~17–21% (Q3 2025) to ~4–9% (Q1–Q2 2026), consistently across arXiv-only and all-venue slices, and across every window size tried. This is the strongest trend in the data.

2. **SCA is a stable, substantial presence.** Within arXiv-only papers, SCA has been at 20–24% throughout the window. This is already elevated relative to what one would expect if TTS were truly dominant. But it is not clearly growing within our observation window.

3. **The citation landscape turned over at Q3→Q4 2025.** The "what they build on" data is more dramatic than the "what they produce" data. The VALL-E family disappears from the top-10 citation list between Q3 and Q4 2025 and does not return. Moshi's citation rate nearly doubles in a single quarter (0.159 → 0.262). This transition is visible within H2 2025, so it is not a conference-season artefact.

4. **The shift may have already happened before our window opens.** Our corpus starts in July 2025. Moshi was published in 2024 and is already #1 in Q3 2025. VALL-E was 2023. The structural transition in what the community builds on likely occurred in 2023–2024, and we are observing its settled state, not its inflection point.

**What the corpus does not support:**

- Field-wide percentage claims ("X% of speech research is SCA") — the keyword filter has differential sensitivity to TTS vs SCA vocabulary, so corpus composition percentages are lower bounds on SCA presence, not estimates.
- A monotonic production shift from TTS to SCA within this window — the arXiv-only data does not show this clearly.
- Venue-naive quarterly comparisons — Q3 is VC-inflated by Interspeech, Q4 is SCA-inflated by EMNLP/NeurIPS.

---

## Honest Corpus Description (draft)

"Within the papers captured by this corpus's keyword filter (July 2025 – May 2026):

- **Production:** SCA represents 20–25% of arXiv preprints consistently across the window, with a possible uptick to ~27–30% in early 2026. TTS remains the plurality at 55–70%. VC declines from ~14% to ~4–6% and is the clearest directional trend.

- **Citation behaviour:** The reference set that papers build on changed markedly between Q3 and Q4 2025. VALL-E-family papers (the foundational codec-LM TTS papers of 2022–2023) dropped out of the top-10 cited works and have not returned. Moshi (the canonical real-time spoken dialogue model) became the most-cited out-of-corpus work by Q4 2025 and has increased its citation rate each quarter since. By Q2 2026, no classic TTS paper appears in the top-10 citations.

- **Venue signal:** SCA work is splitting across venues — appearing at both speech conferences and NLP conferences (EMNLP, NeurIPS, ICLR). TTS conferences (Interspeech) do not suppress TTS relative to arXiv, but they do concentrate VC work."

---

## Open Questions / Next Steps

1. **Pre-2025 baseline.** The critical missing data point: what was the TTS/SCA split in 2023–2024 arXiv preprints? A metadata-only fetch (no PDFs) for arXiv cs.SD/eess.AS in 2023–2024 with the same keyword filter would establish whether 20% SCA was already the norm, or whether it represents growth.

2. **Keyword filter calibration.** The filter likely undercounts SCA. A calibration experiment: take a random sample of 50 Interspeech 2025 papers that were rejected by the filter, read their abstracts manually, and estimate the false-negative rate for SCA papers specifically. This would bound the undercounting.

3. **Citation analysis by paper task.** Currently we look at what all corpus papers cite. A richer cut: among papers tagged SCA, what fraction of their citations go to other SCA papers vs TTS papers, and how does that fraction change across quarters? A self-citation ratio rising within SCA would indicate the subfield is developing its own citation community.

4. **Task overlap.** Many papers have multiple task tags (e.g., [TTS, SCA]). We've been counting these in both categories. A stricter analysis treating only primary task (or single-task papers only) might reveal a cleaner signal.

5. **Report integration.** When ingestion reaches a sufficient milestone (e.g., 300 papers ingested), this analysis could be written up as the first quarterly field report using the wiki's report template. The current notes are the skeleton for that.

---

## Artifacts

| File | Status | Description |
|------|--------|-------------|
| `docs/analyses/citation-h2-2025-vs-h1-2026.md` | Committed | H2 2025 vs H1 2026 citation rate comparison — top 100, risers, fallers, key findings narrative |
| `docs/analyses/citation-h2-2025-vs-h1-2026.json` | Committed | Machine-readable output of the above |
| `docs/analyses/tts-sca-shift-analysis.md` | Local only | This file — full working notes |
| `docs/analyses/discovery-quarterly-top100.md` | Local only | Union of quarterly top-100 out-of-corpus citations — 168 candidates, per-quarter counts, SR flags |
| `docs/analyses/discovery-quarterly-top100.json` | Local only | Machine-readable version of the above |
| `docs/analyses/discovery-quarterly-arxiv-ids.txt` | Local only | 162 arXiv IDs to fetch (all candidates not yet in metadata, sorted by total citation count) |
| `docs/analyses/discovery-quarterly-fetch-manifest.md` | Local only | Human-readable fetch manifest with SR flags and per-quarter breakdown |
| `scripts/discover/citation_period_compare.py` | Committed | CLI for reproducible citation rate comparisons across any two windows |

**To reproduce the task distribution analyses** (not saved as standalone scripts — run inline):

```bash
# Quarterly task distribution + sliding window + venue split
.venv/bin/python - <<'EOF'
# ... (inline script from session — see conversation history 2026-06-07)
EOF
```

The conversation context for this session is at:
`~/.claude/projects/-Users-sribeiro-Documents-Coding-speech-generation-wiki-speech-generation-wiki-infra/`
(most recent `.jsonl` file)

## Fetch manifest notes

162 arXiv IDs in `discovery-quarterly-arxiv-ids.txt`, split into two tiers:

- **SR=Y (57 papers):** Matched the speech keyword filter — run through normal filter agent → ingest pipeline.
- **SR=N (101 papers) + SR=? (4 papers):** Did not match the keyword filter (foundational LLM/ASR/eval papers: Moshi, Whisper, EnCodec, LLaMA 3, GPT-4, AdamW, Flow Matching, etc.). These need to be added as `status: accepted` manually, bypassing the filter agent, since the filter will reject them again for the same reason it originally missed them.
