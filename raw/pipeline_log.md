## 2026-07-18

- review | 2510.07978 (VoiceAgentBench: Are Voice Assistants ready for agentic tasks?) | 1 paper | accepted (scope exception) | caught at ingest time before any page was written; all four evaluation metrics (Tool Selection, Tool Call Structure, Parameter Filling, Refusal Rate) score text tool-call correctness, zero evaluation of generated speech quality; TTS/VC used only to construct benchmark input audio (speaker-diversity sampling, vendor MOS selection in Appendix I); structurally identical to the already-accepted AURA entry in review_queue.md (agentic reasoning primary, TTS/VC incidental to voice interface) — user confirmed accept, following that precedent for consistency | status: accepted → review → accepted, review_queue.md decision recorded
- review | 2501.15907 (Emilia: A Large-Scale, Extensive, Multilingual, and Diverse Dataset for Speech Generation) | 1 paper | rejected as duplicate, content merged | caught while pre-selecting the next Q4 batch; own arxiv_comment states "Full version of arXiv:2407.05361" (already-ingested SLT 2024 Emilia paper), same authors, expanded to Emilia-Large (216k vs 101k hours) with additional scaling-law and multilingual/crosslingual experiments; user decided to keep 2407.05361 as canonical (the SLT-published version) but replace its page content with the fuller arXiv version's material, explicitly linking both papers on the canonical page | status: accepted → rejected, is_duplicate: true, canonical_id: 2407.05361; 2407.05361 re-ingested same session (see wiki/log.md misc entry) with source_ids.arxiv_full_version backfilled

## 2026-07-17

- review | 2510.03111 (Evaluation of preprocessing pipelines in the creation of in-the-wild TTS datasets) | 1 paper | accepted (scope exception) | caught at ingest time (Q4 session 14 batch 3) before any page was written; paper's own stated contributions are a preprocessing-pipeline evaluation methodology, a low-cost pipeline, and a new raw audio corpus, with zero TTS model trained or evaluated (all metrics are signal-quality metrics on raw vs. processed recordings); authors explicitly defer TTS training to future work (§5); same scope pattern as FAMA and MLC-SLM challenge summary, but unlike those cases user confirmed accept — preprocessing methodology judged valuable field infrastructure despite no synthesis evaluation | status: accepted → review → accepted, review_queue.md decision recorded
- review | 2510.03741 (Désentrelacement Fréquentiel Doux pour les Codecs Audio Neuronaux) | 1 paper | rejected as duplicate | French-language version (GRETSI 2025) of 2510.03735 "Soft Disentanglement in Frequency Bands for Neural Audio Codecs", same authors and abstract, arXiv English preprint kept as canonical | status: accepted → rejected, is_duplicate: true, canonical_id: 2510.03735

## 2026-07-14

- review | 2509.13785 (MLC-SLM Challenge Summary) | 1 paper | rejected | pure multilingual ASR + speaker-diarization challenge summary (MER/tcpMER only), no TTS/VC/SCA component; filter-stage false accept (relevance_score 0.85) caught mid-batch during ingest QC, ingest reverted, sent to review_queue.md, user confirmed reject after reading the PDF; same scope pattern as FAMA (2025.clicit-1.81) | status: accepted → ingested → rejected

## 2026-07-06

- review | 2025.clicit-1.81 (FAMA) | 1 paper | rejected | pure ASR/speech-translation foundation model (WER/COMET only), no TTS/VC/SCA component; filter-stage false accept (relevance_score 0.50) caught at ingest time, ingest reverted, sent to review_queue.md, user confirmed reject | status: accepted → review → rejected

## 2026-07-03

- lint | health check ingest module (full corpus, post session-6 ingest) | 461 papers checked | 0 errors, 1178 warnings (pre-existing corpus-wide, not investigated this pass) | health check: scripts/health_check.py --module ingest --wiki-dir speech-generation-wiki-content

## 2026-06-23

- review | health-check review pass (NLP + arXiv batch) | 28 papers | field_significance added, ## Claims with §-section citations added, bare wikilinks fixed to [[id|Name]] format, F5-TTS ID corrected (2410.06885 → 2025.acl-long.313), architecture figures embedded for 6 papers | 14 NLP: 2025.acl-long.682/.911/.912, acl-short.81, americasnlp-1.1, ccl-1.80, coling-main.352/.518, emnlp-demos.70, emnlp-main.1730/.180/.989, findings-acl.1051, findings-emnlp.424 | 14 arXiv: 2507.22746, 2508.00317/.01796/.02013/.02038/.02849/.03543/.04141/.04585/.04996/.05207/.05385/.06262/.06870 | 44 papers remaining (3 NLP, 41 arXiv) | wiki commit: 7ddf224

## 2026-06-19

- lint | health check ingest module | 338 papers checked | 327 id fields quoted (arXiv float-parse bug), 191 index IDs → [[wikilinks]], 193 index titles → [title](papers/id.md) links, 1 blank row removed from index table, 65 Tier 2 pages → [!info] Citation Stub callout | health check: scripts/health_check.py --module ingest

## 2026-06-13

- review | ACL workshop venue dates | 26 metadata files patched | published_date, conference_date, month corrected; venue_detail field added | covers COLING (Jan), NoDaLiDa/ComputEL (Mar), AmericasNLP/IWSDS (May), CoNLL/IWSLT/UNLP (Jul–Aug), CCL/ICNLSP/SIGDIAL (Aug), CLiC-IT (Sep), VLSP (Oct), ArabicNLP (Nov), IWCLUL (Dec)
- quality-pass | Factor A/B/C label cleanup | 12 files edited (5 concept pages, 5 evidence digests, overview.md, papers/2025.acl-long.1498.md) | paper-internal labels from 2412.17048 replaced with descriptive language; missing [[2412.17048]] citations added | source paper page unchanged
- lint | paper set cross-verification | 4 sets checked (metadata, files, papers/index, wiki/log) | counts reconciled at 251 | log has 1 stale entry (2410.06885, arXiv F5-TTS superseded by ACL canonical) — expected | 0 orphans (all 251 in venue pages) | 4 standard papers missed by integration added to concept pages: interspeech-2025-0253, interspeech-2025-0408, interspeech-2025-0902, 2025.americasnlp-1.1 | 12 remaining Tier 2 stubs (ml-method, dataset, foundation-lm, multimodal) have no concept page by design

## 2026-06-12
- integrate | pass 9 | 25 papers (15 T1 + 10 T2) | 19 concepts updated | 4 evidence digests fully updated (neural-codec, autoregressive-codec-tts, zero-shot-tts, spoken-language-model) | 16 cross-links added | integrated_date set for all 25 | integration agent spec patched: WIKI variable + two-repo working directory (was writing to detached-HEAD submodule)
- ingest | 10 Tier 2 stubs (session 43) | Qwen-Audio (2311.07919), Qwen3 (2505.09388), ECAPA-TDNN (2005.07143), LLaMA (2302.13971), Gemini 2.5 (2507.06261), MLS (2012.03411), DeepSeek-R1 (2501.12948), Seamless (2312.05187), GigaSpeech (2106.06909), FSQ (2309.15505) | wiki now 225 pages | 23 quality fixes applied across both batches (adoption claims, SCA prose, spurious SSL tags, field_significance.type mismatches, task tag errors, wikilink formatting) | agent specs strengthened: litmus test + citation-verb failure mode added to both ingest agent specs; SCA prose rule added

## 2026-06-10
- ingest | 15 papers (session 40, 2-batch) | UTMOS (2204.02152), LibriTTS (1904.02882), NaturalSpeech 3 (2403.03100), GLM-4-Voice (2412.02612), Flow Matching (2210.02747), AudioLM (2209.03143), BigVGAN (2206.04658), CFG (2207.12598) [T1]; Kimi-Audio (2504.18425), Qwen2-Audio (2407.10759), GPT-4 TR (2303.08774), AdamW (1711.05101), GPT-4o (2410.21276), Qwen2.5 (2412.15115), Adam (1412.6980) [T2] | wiki now 200 pages | 8 quality fixes applied in-session | agent spec patches: log insertion bug fixed in standard ingest agent (same append-to-end pattern as lightweight; now regex-based section insertion)
- ingest | 10 papers (session 39, 2026-06-09) | Moshi (2410.00037), WavChat (2411.13577), Whisper (2212.04356), HiFi-GAN (2010.05646), EnCodec (2210.13438), FastSpeech 2 (2006.04558), Qwen2.5-Omni (2503.20215), Llama 3 (2407.21783), Common Voice (1912.06670), emotion2vec (2312.15185) | wiki now 185 pages | 5 quality issue classes identified; both agent specs tightened (SSL rule, callout type restriction, log insertion fix in lightweight agent)

## 2026-06-09
- discover | citation merge overrides | added AISHELL-3 (arxiv:2010.11567, 40×) and GSLM (arxiv:2102.01192, 30×) groups; fixed VCTK canonical to title: entry (131×, was doi: not in index); 50 override_entries_merged total | rebuilt index: 21,253 entries, 652 standard merge groups + 50 overrides, 5 fuzzy candidates (none actionable)


## 2026-06-08
- discover | 21262 entries (652 merge groups collapsed, 8 fuzzy candidates), 1056 corpus papers

- parse | citation-discovery batch 18 | 2/2 done, 0 failures | ~7 min | quality report: raw/parsed/batch_18_cd_quality_report.md | clean | PARSE PIPELINE COMPLETE: 861/861 accepted papers parsed (699 standard + 162 citation-discovery)
- parse | citation-discovery batch 17 | 40/40 done, 0 failures | ~79 min | quality report: raw/parsed/batch_17_cd_quality_report.md | RapidOCR warnings on 4 papers, PIL warnings on 2 (all non-fatal) | clean
- parse | citation-discovery batch 16 | 40/40 done, 0 failures | ~93 min | quality report: raw/parsed/batch_16_cd_quality_report.md | RapidOCR warnings on 6 papers, PIL warning on 1 (all non-fatal) | clean
- parse | citation-discovery batch 15 | 40/40 done, 0 failures | ~128 min | quality report: raw/parsed/batch_15_cd_quality_report.md | RapidOCR warnings on 2 papers (non-fatal) | clean
- parse | citation-discovery batch 14 | 40/40 done, 0 failures | ~206 min | quality report: raw/parsed/batch_14_cd_quality_report.md | RapidOCR warnings on 3 papers (non-fatal) | 2001.08361 refs manually recovered (50 refs, Docling rendered ref section as table)
- integrate | seeded evidence digests | transformer-enc-dec-tts (11 papers) | rlhf-speech (15 papers)
- parse | citation-discovery PDFs | 162/162 downloaded, 0 failures | all arxiv source | batches 14–18 added to raw/parsed/batch_queue.json (pending parse)
- discover | citation-discovery corpus_role patch | 162 metadata files patched with corpus_role field | 12-value vocabulary (tts-vc 42, foundation-lm 20, evaluation 18, sca 15, multimodal 15, audio-lm 11, ml-method 10, codec 9, dataset 9, survey 8, asr 4, speaker 1)
- discover | citation-discovery fetch | 162 papers written with status=accepted | source: docs/analyses/discovery-quarterly-fetch-manifest.md | bypassed filter; discovery_source="citation-discovery" field set | 57 SR=Y, 101 SR=N, 4 SR=? (titles resolved via arXiv API)

## 2026-06-07

- discover | 16476 entries (570 merge groups collapsed, 5 fuzzy candidates), 894 corpus papers


# Pipeline Log

Infra-only operations (filter, parse, discover, lint, review). Not rendered on the wiki site.

## 2026-06-06

- parse | batch 13 | 31 papers | 0 failed | RapidOCR warnings (non-fatal): iclr-2026-JbLmIoWwDC (×4), iclr-2026-U4GXPqm3Va (×6), iclr-2026-wbttgzp7MT (×1), neurips-2025-AsRB5nmlOD (×2), neurips-2025-vhPy3NMsO5 (×1)
- parse | batch 12 | 40 papers | 0 failed | RapidOCR warnings (non-fatal): 2510.07881, 2605.25962 (×5), 2605.27190, iclr-2025-dGSOn7sdWg (×3), iclr-2025-tQ1PmLfPBL
- parse | batch 11 | 40 papers | 0 failed | RapidOCR warnings (non-fatal): 2506.23325, 2507.04349, 2507.20140

## 2026-06-05

- fetch | cs.SD (OAI-PMH) | 2025-07-01→2025-07-31 | 353 discovered, 52 written | July backfill; arXiv search API rate-limited (all retries), switched permanently to OAI-PMH for cs.SD + eess.AS
- fetch | eess.AS (OAI-PMH) | 2025-07-01→2025-07-31 | 401 discovered, 9 written, 50 skipped (cross-listed with cs.SD)
- fetch | cs.CL (OAI-PMH) | 2025-07-01→2025-07-31 | 1867 discovered, 3 written, 18 skipped | July backfill (new window, never previously scanned)
- fetch | cs.CL (OAI-PMH) | 2025-08-01→2025-11-30 | 9330 discovered, 12 written, 115 skipped | re-scan with expanded keyword list (+11 terms added 2026-05-25)
- fetch | cs.CL (OAI-PMH) | 2025-12-01→2026-02-28 | 6579 discovered, 5 written, 68 skipped | re-scan
- fetch | cs.CL (OAI-PMH) | 2026-03-01→2026-05-31 | 10571 discovered, 13 written, 97 skipped | re-scan + new top-up to 2026-05-31
- fetch | cs.SD (OAI-PMH) | 2026-05-25→2026-05-31 | 94 discovered, 6 written, 7 skipped | May tail (prev fetch ended 2026-05-25)
- fetch | eess.AS (OAI-PMH) | 2026-05-25→2026-05-31 | 60 discovered, 8 written, 5 skipped | May tail
- fetch | total | 108 new pending papers written across all batches; corpus now fully covers 2025-07-01→2026-05-31
- dedup | 108 new pending papers checked (arXiv ID cross-ref + normalized title match) | 16 duplicates found: all arXiv preprints of existing Interspeech/ACL/EMNLP proceedings entries | 16 arXiv versions marked rejected/is_duplicate; 15 source_ids.arxiv backfilled on proceedings side; 1 three-way case (2505.20868 + 2511.14824 → interspeech-2025-2586) | 92 net-new pending papers remain
- fetch | ICLR 2025 (OpenReview API) | 3703 discovered, 13 written | new fetcher: scripts/fetch/openreview.py; conference ID canonical (iclr-2025-{forum_id}); arXiv extraction best-effort
- fetch | NeurIPS 2025 (OpenReview API) | 5286 discovered, 16 written
- fetch | ICLR 2026 (OpenReview API) | 5352 discovered, 27 written
- fetch | total | 56 new pending papers written (ICLR 2025 + NeurIPS 2025 + ICLR 2026); dedup pass pending
- dedup | 148 pending papers checked (title match; arXiv ID where available) | 22 duplicates found | 20 arXiv papers marked rejected/is_duplicate (19 accepted + 1 pending); 22 source_ids.arxiv backfilled on conference papers | 2 ingested arXiv papers (2510.00981, 2508.16790) marked is_duplicate but status kept ingested — wiki page migration deferred | net pending: 147
- filter | arXiv batch 1 (2409–2507, 49 papers) | 32 accepted, 8 review, 9 rejected
- filter | arXiv batch 2 + ICLR 2025 (49 papers) | 31 accepted, 8 review, 10 rejected
- filter | ICLR 2025 + ICLR 2026 + NeurIPS 2025 batch 3 (49 papers) | 34 accepted, 5 review, 10 rejected
- review | arXiv + ICLR + NeurIPS batch (22 borderline) | 17 accepted, 5 rejected (incl. 2409.07151) | review queue cleared | corpus: 698 accepted, 289 rejected
- download | 113 new PDFs | 111 downloaded (69 arXiv, 42 OpenReview) | 2 confirmed withdrawn → rejected (2503.20999, 2511.08230) | 3 OpenReview 429s recovered via retry
- parse | batch queue updated | batches 11–13 appended (40+40+31 = 111 papers) | --sync run: batches 1–10 marked done, batch 1 partial (39/40)

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
