# Citation Discovery

One of the most reliable signals for finding missing papers is the corpus itself. Every paper we ingest includes a reference list, and collectively those lists form a citation graph — a map of what the field is actually reading and building on. Papers cited by many corpus papers, but not yet in the corpus themselves, are strong candidates for ingestion. This document describes how we build and maintain that graph.

---

## How the index is built

Every parsed paper produces a `references.json` file (written by the Docling pipeline) containing structured reference entries. Each entry may carry a title, an arXiv ID, a DOI, a publication year, and a raw bibliography string. The `citation_index.py` script scans all of these files and aggregates them into a single index.

For each out-of-corpus reference, the script assigns a canonical key using a priority chain:

```
arxiv:{id}  >  doi:{doi}  >  title:{normalized_title}  >  raw:{raw_prefix}
```

This means that if two corpus papers both cite arXiv:2308.16692, they contribute to the same entry. If a paper is cited by title only (no arXiv ID or DOI), the key falls back to a normalized form of the title — lowercase, alphanumeric only, truncated to 120 characters. The `cited_by` list accumulates the IDs of every corpus paper that references the entry, and `citation_count` is its length.

The output is `raw/citation_index.json` — a sorted list of all out-of-corpus references, with each entry including its citation count, the papers that cite it, a `speech_relevant` flag (based on the same keyword filter used for fetching), and whatever structured metadata was available.

---

## The deduplication problem

In practice, the same paper frequently appears under multiple keys. A bibliography entry in one paper might carry the arXiv ID; a bibliography entry in another paper for the exact same work might cite it by title only, or use a slightly different title form. These end up as separate entries in a naive implementation.

When we first analysed the index (built from 176 parsed papers), the problem was already visible at the top of the list:

| Paper | Entries | Combined count |
|-------|---------|---------------|
| Whisper | `arxiv:2212.04356` (53×) + `title:robustspeech...` (143×) | 196× |
| UTMOS | `arxiv:2204.02152` (83×) + `title:utmosutokyo...` (80×) | 163× |
| LibriTTS | `arxiv:1904.02882` (81×) + `title:libritts...` (68×) + `doi:...` (8×) | 157× |
| HiFi-GAN | `arxiv:2010.05646` (17×) + `title:hifigan...` (105×) | 122× |
| EnCodec | `arxiv:2210.13438` (117×) + `title:highfidelity...` (62×) | 179× |

The root cause: the key is locked in on first encounter. If the first corpus paper to cite Whisper does so with an arXiv ID, the entry is stored under `arxiv:2212.04356`. If another paper cites the same work without an arXiv ID but with the full title, the script sees a new key — `title:robustspeechrecognitionvialargescaleweaksupervision` — and creates a second entry. The two entries accumulate citations independently and neither is aware of the other.

The inline upgrade logic (which already patches in a missing `arxiv_id` when a later sighting of the same key provides one) cannot fix this because the sightings are under different keys and never meet.

---

## The fix: a two-pass approach

### Pass 1 — deterministic title merge

After the full collection pass, the script runs a second pass over all entries grouped by normalized title. Any group with two or more entries is collapsed: the most canonical key wins (same `arxiv: > doi: > title: > raw:` priority), and the `cited_by` sets from all others are unioned into it. If the canonical entry gains an `arxiv_id` through this merge and was stored under a `title:` key, it is re-keyed to `arxiv:{id}`.

This pass is exact — no approximation — and handles every case where the title strings are the same modulo case and punctuation. On the full corpus (875 parsed papers), it collapsed 570 duplicate groups and merged away 602 entries.

### Pass 2 — fuzzy candidate detection

After the deterministic merge, the script computes token Jaccard similarity between titled entries with at least 5 citations. Pairs scoring ≥ 0.85 with different normalized titles are written to a `merge_candidates` field in the output JSON. These are not merged automatically — a high Jaccard score can just as easily indicate genuinely distinct papers (a model family sharing a title template, for example) as a real duplicate.

On the current corpus, 5 candidate pairs were surfaced. All were confirmed as distinct papers — different models in the Qwen and Step-Audio families, and DNSMOS vs DNSMOS P.835 (a later publication, not a variant citation). The fuzzy pass is a human-review aid, not an automatic merge.

### Manual overrides

Some duplicates are neither caught by exact title normalization nor well-described by Jaccard similarity: a reference where the word "large" was dropped from the title in some citations (SpeechTokenizer), or a dataset cited under six different version strings and DOIs (CSTR VCTK). These are handled by `raw/citation_merge_overrides.json`, a small JSON file where each entry specifies a canonical key and the keys to merge into it. The script applies this file as a third pass, after both the deterministic and fuzzy stages. Adding a new override requires editing that file and re-running the script.

---

## What the index enables

With deduplication fixed and the prefilter removed, the index is a usable starting point for two things:

**Citation discovery.** The Citation Discovery Workflow (documented in CLAUDE.md) surfaces out-of-corpus papers cited by three or more corpus papers. The top of the list is predictably the foundational papers — Whisper, VALL-E, HiFi-GAN, WaveNet, VITS — but the middle tiers reveal papers we haven't yet ingested that the community is consistently building on. Running discovery after each major ingest batch keeps the corpus from drifting away from what the field actually cites.

**Quantitative analysis.** Citation counts give a rough signal of a paper's influence within our corpus. This isn't the same as real-world influence (our corpus has biases, papers can be cited negatively, recent papers haven't had time to accumulate citations), but as an internal consistency check — which papers does the field keep returning to? — it's useful. The counts are also a reasonable input for prioritizing Opus quality passes: a paper cited 80× by corpus papers is a stronger candidate for a detailed rewrite than one cited twice.

---

## Current state

The index was last rebuilt on 2026-06-07 from 894 parsed papers (875 in-corpus + some reference-only). Summary:

| Metric | Value |
|--------|-------|
| Total out-of-corpus reference sightings | 36,460 |
| Unique entries (before dedup) | 17,084 |
| Merge groups collapsed | 570 |
| Manual overrides applied | 6 |
| Unique entries (after dedup) | 16,476 |
| Speech-relevant (keyword-filtered) | 1,569 |
| Fuzzy candidates remaining | 5 (all confirmed distinct) |

Top cited out-of-corpus papers (post-dedup):

| Count | Paper |
|-------|-------|
| 208× | Moshi (Défossez et al., 2024) |
| 196× | Whisper (Radford et al., 2022) |
| 179× | EnCodec (Défossez et al., 2022) |
| 163× | UTMOS (Saeki et al., 2022) |
| 157× | LibriTTS (Zen et al., 2019) |
| 123× | HiFi-GAN (Kong et al., 2020) |
| 121× | WavLM (Chen et al., 2021) |
| 107× | HuBERT (Hsu et al., 2021) |
| 107× | VALL-E (Wang et al., 2023) |
| 104× | SpeechTokenizer (Zhang et al., 2023) |

---

## Known limitations

**~11,000 entries have no extractable title.** These are stored under `raw:` keys derived from a normalized prefix of the bibliography string. They cannot be deduplicated against each other or against titled entries. Many are one-off citations of minor works; some are repeated citations where Docling couldn't extract a structured title. The raw string is preserved in `raw_sample` and is readable, but matching across `raw:` entries is not currently attempted.

**Citation counts reflect the parsed corpus, not the full corpus.** Only papers whose `references.json` has been produced contribute to the index. At 894 parsed papers out of 875 total in-corpus (plus some parsed-only), coverage is essentially complete for ingested papers, but papers not yet ingested (699 as of this writing) don't contribute their citations. Running the script after each ingest batch keeps the counts growing.

**The corpus has structural biases.** We skew toward arXiv and proceedings papers, toward recent years (2025–2026), and toward English-language work. Papers that predate our coverage window or were published in venues we don't track will be underrepresented in citation counts regardless of their real-world influence.
