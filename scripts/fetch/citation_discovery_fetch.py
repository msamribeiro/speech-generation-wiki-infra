#!/usr/bin/env python3
"""
citation_discovery_fetch.py — Fetch metadata for highly-cited out-of-corpus papers.

Reads the quarterly citation discovery manifest, fetches arXiv metadata from the
API, and writes metadata JSON files with status=accepted, bypassing the standard
keyword filter. Papers are onboarded because they are frequently cited by
in-corpus papers, not because they passed the filter.

Three provenance fields are added to each metadata file:
  discovery_source        : "citation-discovery"
  corpus_citation_count   : total in-corpus citation count from the analysis
  citation_counts_by_quarter : per-quarter breakdown (Q3 2025 – Q2 2026)
  sr_match                : whether the paper matched the keyword filter (True/False/null)

Usage:
    python scripts/fetch/citation_discovery_fetch.py
    python scripts/fetch/citation_discovery_fetch.py --dry-run
    python scripts/fetch/citation_discovery_fetch.py --ids 2410.00037 2212.04356
    python scripts/fetch/citation_discovery_fetch.py --manifest docs/analyses/discovery-quarterly-fetch-manifest.md
"""

import argparse
import json
import re
import sys
import time
from datetime import date, datetime
from pathlib import Path

import feedparser
import requests

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

RAW_METADATA = ROOT / "raw" / "metadata"
FETCH_LOG = ROOT / "raw" / "fetch_log.jsonl"
DEFAULT_MANIFEST = ROOT / "docs" / "analyses" / "discovery-quarterly-fetch-manifest.md"

ARXIV_API_URL = "https://export.arxiv.org/api/query"
RATE_LIMIT_SECONDS = 3.0
CHUNK = 50  # arXiv API handles up to 100 per id_list request; 50 is safe


# ---------------------------------------------------------------------------
# corpus_role lookup table
#
# Classifies each citation-discovered paper by its functional role in the
# speech synthesis ecosystem. Distinct from the task field (TTS/VC/SCA/…),
# which is speech-task-specific and populated at ingest. corpus_role is a
# coarser, ecosystem-level classification used to track trend shifts over time.
#
# Vocabulary:
#   tts-vc          TTS or voice conversion system
#   sca             spoken conversational agent / full-duplex speech LM
#   codec           neural audio codec
#   audio-lm        audio/speech language model not primarily TTS (AudioLM, etc.)
#   foundation-lm   general-purpose LLM used as TTS/SCA backbone
#   asr             automatic speech recognition system
#   speaker         speaker verification or recognition model
#   dataset         training or evaluation corpus
#   evaluation      benchmark, metric, or evaluation toolkit
#   ml-method       general ML technique (optimizer, normalization, diffusion, etc.)
#   survey          survey or overview paper
#   multimodal      vision+speech or multi-task audio-language model
# ---------------------------------------------------------------------------

CORPUS_ROLE: dict[str, str] = {
    # TTS / voice conversion systems
    "1609.03499": "tts-vc",   # WaveNet
    "1703.10135": "tts-vc",   # Tacotron
    "1712.05884": "tts-vc",   # Tacotron 2
    "2006.04558": "tts-vc",   # FastSpeech 2
    "2010.05646": "tts-vc",   # HiFi-GAN
    "2105.06337": "tts-vc",   # Grad-TTS
    "2104.00355": "tts-vc",   # Speech Resynthesis from Discrete Disentangled SSL Reps
    "2206.04658": "tts-vc",   # BigVGAN
    "2303.03926": "tts-vc",   # Cross-lingual neural voice cloning
    "2304.09116": "tts-vc",   # NaturalSpeech 2
    # HiFi-Codec classified under codec below
    "2305.07243": "tts-vc",   # Better speech synthesis through scaling
    "2306.00814": "tts-vc",   # Vocos
    "2312.01479": "tts-vc",   # OpenVoice
    "2401.07333": "tts-vc",   # ELLA-V
    "2402.01912": "tts-vc",   # Natural Language Guidance of High-Fidelity TTS
    "2402.08093": "tts-vc",   # BASE TTS
    "2403.03100": "tts-vc",   # NaturalSpeech 3
    "2403.16973": "tts-vc",   # VoiceCraft
    "2404.03204": "tts-vc",   # RALL-E
    "2406.00654": "tts-vc",   # Enhancing Zero-shot TTS with Human Feedback
    "2406.04904": "tts-vc",   # XTTS
    "2406.05370": "tts-vc",   # VALL-E 2
    "2406.05551": "tts-vc",   # Autoregressive Diffusion Transformer for TTS
    "2406.07855": "tts-vc",   # VALL-E R
    "2406.18009": "tts-vc",   # E2 TTS
    "2407.08551": "tts-vc",   # Autoregressive Speech Synthesis without VQ
    "2409.00750": "tts-vc",   # MaskGCT
    "2409.03283": "tts-vc",   # FireRedTTS
    "2411.01156": "tts-vc",   # Fish-Speech
    "2411.09943": "tts-vc",   # Zero-shot Voice Conversion with Diffusion Transformers
    "2412.04724": "tts-vc",   # StableVC
    "2502.04128": "tts-vc",   # Llasa
    "2502.05512": "tts-vc",   # IndexTTS
    "2502.07243": "tts-vc",   # Vevo
    "2502.18924": "tts-vc",   # MegaTTS 3
    "2503.01710": "tts-vc",   # Spark-TTS
    "2503.14345": "tts-vc",   # MoonCast (podcast generation = TTS)
    "2504.02407": "tts-vc",   # F5R-TTS
    "2505.07916": "tts-vc",   # MiniMax-Speech
    "2505.13000": "codec",    # DualCodec — codec, not a TTS front-end
    "2505.17589": "tts-vc",   # CosyVoice 3
    "2506.13053": "tts-vc",   # ZipVoice
    "2508.04195": "tts-vc",   # NVSpeech

    # Spoken conversational agents / full-duplex speech LMs
    "2408.02622": "sca",      # Language Model Can Listen While Speaking
    "2408.16725": "sca",      # Mini-Omni
    "2409.06666": "sca",      # LLaMA-Omni
    "2410.00037": "sca",      # Moshi
    "2410.11190": "sca",      # Mini-Omni2
    "2410.17799": "sca",      # OmniFlatten
    "2411.00774": "sca",      # Freeze-Omni
    "2412.02612": "sca",      # GLM-4-Voice
    "2412.15649": "sca",      # SLAM-Omni
    "2501.06282": "sca",      # MinMo
    "2502.11946": "sca",      # Step-Audio
    "2502.17239": "sca",      # Baichuan-Audio
    "2505.02625": "sca",      # LLaMA-Omni2
    # VITA-Audio classified under multimodal below
    "2507.16632": "sca",      # Step-Audio 2
    "2511.15848": "sca",      # Step-Audio-R1

    # Neural audio codecs
    "2210.13438": "codec",    # EnCodec
    "2305.02765": "codec",    # HiFi-Codec — already listed under tts-vc; keeping codec wins
    "2308.16692": "codec",    # SpeechTokenizer
    "2408.16532": "codec",    # WavTokenizer
    "2409.05377": "codec",    # BigCodec
    "2411.18803": "codec",    # TS3-Codec
    "2411.19842": "codec",    # Scaling Transformers for Low-Bitrate Speech Coding
    "2504.10344": "codec",    # ALMTokenizer

    # Audio / speech language models (not primarily TTS)
    "2209.03143": "audio-lm", # AudioLM
    "2301.11325": "audio-lm", # MusicLM
    "2301.12503": "audio-lm", # AudioLDM
    "2305.09636": "audio-lm", # SoundStorm
    "2305.11000": "audio-lm", # SpeechGPT
    "2305.15255": "audio-lm", # Spoken QA and Speech Continuation Using Spectrograms
    "2306.12925": "audio-lm", # AudioPaLM
    "2310.00704": "audio-lm", # UniAudio
    "2312.15821": "audio-lm", # Audiobox
    "2402.05755": "audio-lm", # SpiRit-LM
    "2411.17607": "audio-lm", # Scaling Speech-Text Pre-training with Synthetic Interleaved Data

    # Foundation LLMs used as TTS/SCA backbone
    "1810.04805": "foundation-lm",  # BERT
    "2005.14165": "foundation-lm",  # GPT-3
    "2302.13971": "foundation-lm",  # LLaMA
    "2303.08774": "foundation-lm",  # GPT-4
    "2307.09288": "foundation-lm",  # LLaMA 2
    "2309.16609": "foundation-lm",  # Qwen
    "2402.03300": "foundation-lm",  # DeepSeekMath
    "2407.10671": "foundation-lm",  # Qwen2
    "2407.21783": "foundation-lm",  # LLaMA 3
    "2410.21276": "foundation-lm",  # GPT-4o System Card
    "2312.11805": "foundation-lm",  # Gemini
    "2412.15115": "foundation-lm",  # Qwen2.5
    "2412.19437": "foundation-lm",  # DeepSeek-V3
    "2501.12948": "foundation-lm",  # DeepSeek-R1
    "2503.01743": "foundation-lm",  # Phi-4-Mini
    "2503.19786": "foundation-lm",  # Gemma 3
    "2505.09388": "foundation-lm",  # Qwen3
    "2506.07900": "foundation-lm",  # MiniCPM4
    "2507.06261": "foundation-lm",  # Gemini 2.5
    "2412.08635": "foundation-lm",  # Multimodal Latent LM with Next-Token Diffusion

    # ASR systems
    "2005.07143": "speaker",  # ECAPA-TDNN (speaker verification, not ASR)
    "2206.08317": "asr",      # Paraformer
    "2212.04356": "asr",      # Whisper
    "2509.08753": "asr",      # Streaming Seq2Seq with Delayed Streams
    "2511.09690": "asr",      # Omnilingual ASR

    # Speaker verification / recognition
    # (ECAPA-TDNN above)

    # Datasets
    "1808.10583": "dataset",  # AISHELL-2
    "1904.02882": "dataset",  # LibriTTS
    "1908.06248": "dataset",  # JVS corpus
    "1912.06670": "dataset",  # Common Voice
    "1510.08484": "dataset",  # MUSAN
    "2007.10310": "dataset",  # CoVoST 2
    "2012.03411": "dataset",  # MLS
    "2106.06909": "dataset",  # GigaSpeech
    "2407.05361": "dataset",  # Emilia

    # Evaluation metrics, benchmarks, toolkits
    "2106.04624": "evaluation",  # SpeechBrain
    "2204.02152": "evaluation",  # UTMOS
    "2312.15185": "evaluation",  # emotion2vec
    "2308.05725": "evaluation",  # EXPRESSO
    "2402.07729": "evaluation",  # AIR-Bench
    "2406.14294": "evaluation",  # DASB
    "2410.17196": "evaluation",  # VoiceBench
    "2410.19168": "evaluation",  # MMAU
    "2502.05139": "evaluation",  # Meta Audiobox Aesthetics
    "2505.09558": "evaluation",  # WavReward
    "2505.14648": "evaluation",  # Vox-Profile
    "2506.02863": "evaluation",  # CapSpeech
    "2506.16381": "evaluation",  # InstructTTSEval
    "2507.12705": "evaluation",  # AudioJudge
    "2507.23159": "evaluation",  # Full-Duplex-Bench v1.5
    "2508.13992": "evaluation",  # MMAU-Pro
    "2510.07838": "evaluation",  # Full-Duplex-Bench-v2
    "2510.14664": "evaluation",  # SpeechLLM-as-Judges

    # General ML methods
    "1412.6980":  "ml-method",  # Adam
    "1607.06450": "ml-method",  # Layer Normalization
    "1711.05101": "ml-method",  # AdamW
    "2001.08361": "ml-method",  # Scaling Laws for Neural Language Models
    "2002.05202": "ml-method",  # GLU Variants Improve Transformer
    "2207.12598": "ml-method",  # Classifier-Free Diffusion Guidance
    "2210.02747": "ml-method",  # Flow Matching for Generative Modeling
    "2302.00482": "ml-method",  # Conditional Flow Matching
    "2308.10248": "ml-method",  # Steering Language Models With Activation Engineering
    "2309.15505": "ml-method",  # Finite Scalar Quantization

    # Survey / overview papers
    "2106.15561": "survey",   # A Survey on Neural Speech Synthesis
    "2312.10997": "survey",   # RAG for LLMs: A Survey
    "2402.13236": "survey",   # Towards Audio Language Modeling — An Overview
    "2410.03751": "survey",   # Recent Advances in Speech Language Models
    "2411.13577": "survey",   # WavChat: A Survey of Spoken Dialogue Models
    "2502.06490": "survey",   # Recent Advances in Discrete Speech Tokens
    "2504.08528": "survey",   # On the Landscape of Spoken Language Models
    "2506.10274": "survey",   # Discrete Audio Tokens: More Than a Survey!

    # Multimodal (vision+speech or general audio-language) models
    "2310.13289": "multimodal",  # SALMONN
    "2311.07919": "multimodal",  # Qwen-Audio
    "2312.05187": "multimodal",  # Seamless
    "2308.11596": "multimodal",  # SeamlessM4T
    "2407.04051": "multimodal",  # FunAudioLLM
    "2407.10759": "multimodal",  # Qwen2-Audio
    "2408.01800": "multimodal",  # MiniCPM-V
    "2408.05211": "multimodal",  # VITA
    "2501.01957": "multimodal",  # VITA-1.5
    "2501.07246": "multimodal",  # Audio-CoT
    "2501.15368": "multimodal",  # Baichuan-Omni-1.5
    "2503.20215": "multimodal",  # Qwen2.5-Omni
    "2504.18425": "multimodal",  # Kimi-Audio
    "2505.03739": "multimodal",  # VITA-Audio (also sca; multimodal is primary role)
    "2507.08128": "multimodal",  # Audio Flamingo 3
}


# ---------------------------------------------------------------------------
# Manifest parsing
# ---------------------------------------------------------------------------

def parse_manifest(manifest_path: Path) -> dict[str, dict]:
    """
    Parse the markdown manifest table.

    Expected columns (pipe-separated):
        # | arXiv ID | Title | Year | SR | Total | Q3'25 | Q4'25 | Q1'26 | Q2'26

    Returns: dict of arxiv_id -> {sr, total, q3_2025, q4_2025, q1_2026, q2_2026}
    """
    result = {}
    for line in manifest_path.read_text().splitlines():
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")]
        # Drop only the leading and trailing empty tokens from "| ... |"
        if parts and parts[0] == "":
            parts = parts[1:]
        if parts and parts[-1] == "":
            parts = parts[:-1]
        if len(parts) < 10:
            continue
        # Skip header / separator rows
        if not parts[0].isdigit():
            continue

        arxiv_id = parts[1].strip()
        sr = parts[4].strip()  # Y / N / ?

        def _int(s: str) -> int:
            s = s.replace("—", "0").replace("-", "0").strip()
            try:
                return int(s)
            except ValueError:
                return 0

        result[arxiv_id] = {
            "sr": sr,
            "total": _int(parts[5]),
            "q3_2025": _int(parts[6]),
            "q4_2025": _int(parts[7]),
            "q1_2026": _int(parts[8]),
            "q2_2026": _int(parts[9]),
        }
    return result


# ---------------------------------------------------------------------------
# arXiv helpers
# ---------------------------------------------------------------------------

def arxiv_id_from_url(url: str) -> str:
    m = re.search(r"abs/([^v\s/]+?)(?:v\d+)?$", url)
    return m.group(1) if m else url.rstrip("/").split("/")[-1]


def build_metadata(entry, arxiv_id: str, manifest_data: dict) -> dict:
    tp = entry.get("published_parsed")
    if tp:
        published_date = f"{tp.tm_year}-{tp.tm_mon:02d}-{tp.tm_mday:02d}"
        year, month = tp.tm_year, tp.tm_mon
    else:
        published_date, year, month = None, None, None

    authors_all = [a["name"] for a in entry.get("authors", [])]
    authors = authors_all[:10]

    info = manifest_data.get(arxiv_id, {})
    total = info.get("total", 0)
    sr = info.get("sr", "?")

    sr_match = {"Y": True, "N": False}.get(sr, None)

    relevance_note = (
        f"Citation-discovered: cited {total}× by in-corpus papers "
        f"(Q3 2025–Q2 2026 quarterly analysis). "
        f"Accepted without filter scoring."
    )

    return {
        "id": arxiv_id,
        "source_ids": {"arxiv": arxiv_id},
        "title": entry.title.replace("\n", " ").strip(),
        "authors": authors,
        "authors_full": authors_all if len(authors_all) > 10 else None,
        "organization": None,
        "venue": "arXiv",
        "venue_type": "preprint",
        "year": year,
        "month": month,
        "published_date": published_date,
        "ingested_date": None,
        "integrated_date": None,
        "url": f"https://arxiv.org/abs/{arxiv_id}",
        "pdf_url": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
        "pdf_path": None,
        "pdf_source": "arxiv",
        "abstract": entry.get("summary", "").replace("\n", " ").strip(),
        "arxiv_comment": getattr(entry, "arxiv_comment", None),
        "task": [],
        "relevance_score": None,
        "relevance_note": relevance_note,
        "status": "accepted",
        "fetched_date": date.today().isoformat(),
        "needs_manual_pdf": False,
        "is_duplicate": False,
        "canonical_id": None,
        "generation_history": [],
        # Discovery provenance
        "discovery_source": "citation-discovery",
        "corpus_role": CORPUS_ROLE.get(arxiv_id),
        "corpus_citation_count": total,
        "citation_counts_by_quarter": {
            "Q3_2025": info.get("q3_2025", 0),
            "Q4_2025": info.get("q4_2025", 0),
            "Q1_2026": info.get("q1_2026", 0),
            "Q2_2026": info.get("q2_2026", 0),
        },
        "sr_match": sr_match,
    }


# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------

def fetch_discovery_ids(ids_with_data: dict[str, dict], dry_run: bool = False) -> dict:
    """Fetch arXiv metadata for the given IDs and write metadata files."""
    RAW_METADATA.mkdir(parents=True, exist_ok=True)

    all_ids = list(ids_with_data.keys())

    to_fetch, skipped = [], []
    for arxiv_id in all_ids:
        if (RAW_METADATA / f"{arxiv_id}.json").exists():
            skipped.append(arxiv_id)
        else:
            to_fetch.append(arxiv_id)

    print(f"Total IDs     : {len(all_ids)}")
    print(f"Already exist : {len(skipped)} (skipped)")
    if skipped:
        print(f"  {', '.join(skipped[:8])}{'...' if len(skipped) > 8 else ''}")
    print(f"To fetch      : {len(to_fetch)}")
    print(f"Dry run       : {dry_run}")
    print()

    if not to_fetch:
        print("Nothing to fetch.")
        return {"written": 0, "skipped_existing": len(skipped), "errors": []}

    session = requests.Session()
    session.headers["User-Agent"] = "speech-generation-wiki/1.0"

    fetched_entries = []
    errors = []

    for i in range(0, len(to_fetch), CHUNK):
        chunk = to_fetch[i : i + CHUNK]
        chunk_num = i // CHUNK + 1
        total_chunks = (len(to_fetch) + CHUNK - 1) // CHUNK
        print(f"Chunk {chunk_num}/{total_chunks}: fetching {len(chunk)} IDs...")

        for attempt in range(5):
            wait = 30 * (2 ** attempt)
            try:
                resp = session.get(
                    ARXIV_API_URL,
                    params={"id_list": ",".join(chunk), "max_results": len(chunk)},
                    timeout=60,
                )
                resp.raise_for_status()
                feed = feedparser.parse(resp.text)
                fetched_entries.extend(feed.entries)
                print(f"  → {len(feed.entries)} entries returned")
                break
            except requests.exceptions.HTTPError as exc:
                code = exc.response.status_code if exc.response is not None else 0
                if code in (429, 500, 502, 503, 504):
                    print(f"  HTTP {code} — waiting {wait}s before retry {attempt + 1}/5...")
                    time.sleep(wait)
                else:
                    errors.append(str(exc))
                    print(f"  HTTP error: {exc}")
                    break
            except Exception as exc:
                print(f"  Request error (attempt {attempt + 1}/5): {exc} — waiting {wait}s...")
                time.sleep(wait)
        else:
            errors.append(f"Chunk {chunk_num}: all retries exhausted")

        if i + CHUNK < len(to_fetch):
            time.sleep(RATE_LIMIT_SECONDS)

    print()
    print("Writing metadata files...")
    written = 0
    for entry in fetched_entries:
        try:
            arxiv_id = arxiv_id_from_url(entry.id)
            title = entry.title.replace("\n", " ").strip()
            out_path = RAW_METADATA / f"{arxiv_id}.json"

            metadata = build_metadata(entry, arxiv_id, ids_with_data)
            if not dry_run:
                out_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))
            written += 1

            info = ids_with_data.get(arxiv_id, {})
            sr_label = info.get("sr", "?")
            total = info.get("total", 0)
            print(f"  + {arxiv_id} [{total:>3}× cited, SR={sr_label}]: {title[:65]}")

        except Exception as exc:
            msg = f"{getattr(entry, 'id', '?')}: {exc}"
            errors.append(msg)
            print(f"  ERROR: {msg}")

    # Flag IDs that arXiv didn't return (withdrawn, invalid, etc.)
    returned_ids = {arxiv_id_from_url(e.id) for e in fetched_entries}
    for rid in to_fetch:
        if rid not in returned_ids:
            errors.append(f"{rid}: not returned by arXiv (withdrawn or invalid?)")
            print(f"  ! {rid}: not returned by arXiv")

    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": "citation-discovery",
        "ids_requested": len(to_fetch),
        "written": written,
        "skipped_existing": len(skipped),
        "errors": errors,
    }

    if not dry_run:
        with open(FETCH_LOG, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    prefix = "[DRY RUN] " if dry_run else ""
    print()
    print(f"{prefix}Summary")
    print(f"  Requested  : {len(to_fetch)}")
    print(f"  Written    : {written}")
    print(f"  Skipped    : {len(skipped)}")
    print(f"  Errors     : {len(errors)}")
    if errors:
        for e in errors[:10]:
            print(f"    {e}")

    return log_entry


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument(
        "--manifest",
        default=str(DEFAULT_MANIFEST),
        metavar="PATH",
        help="Path to the discovery manifest markdown file (default: docs/analyses/discovery-quarterly-fetch-manifest.md)",
    )
    p.add_argument(
        "--ids",
        nargs="+",
        metavar="ARXIV_ID",
        help="Fetch only these specific IDs (overrides manifest selection, but still reads citation counts from manifest)",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Fetch from arXiv but do not write any files",
    )
    args = p.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"ERROR: manifest not found: {manifest_path}", file=sys.stderr)
        sys.exit(1)

    manifest_data = parse_manifest(manifest_path)
    print(f"Manifest      : {manifest_path}")
    print(f"Entries parsed: {len(manifest_data)}")
    print()

    if args.ids:
        # Restrict to the specified IDs; use manifest data for citation counts if available
        ids_subset = {
            arxiv_id: manifest_data.get(
                arxiv_id,
                {"sr": "?", "total": 0, "q3_2025": 0, "q4_2025": 0, "q1_2026": 0, "q2_2026": 0},
            )
            for arxiv_id in args.ids
        }
        fetch_discovery_ids(ids_subset, dry_run=args.dry_run)
    else:
        fetch_discovery_ids(manifest_data, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
