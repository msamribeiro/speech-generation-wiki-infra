#!/usr/bin/env python3
"""
agent.py — LLM relevance filter for the speech-generation-wiki.

Reads all raw/metadata/*.json with status=pending, scores each paper for
relevance to speech generation research (TTS, VC, SCA, codec, evaluation,
singing), and updates status to accepted / review / rejected.

Borderline papers (score 0.40–0.70) are appended to raw/review_queue.md.
Requires ANTHROPIC_API_KEY in the environment.

Usage:
    python scripts/filter/agent.py
    python scripts/filter/agent.py --dry-run --limit 10
    python scripts/filter/agent.py --model claude-sonnet-4-6 --batch-size 5
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import date
from pathlib import Path

import anthropic

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

# ---------------------------------------------------------------------------
# Paths and constants
# ---------------------------------------------------------------------------

RAW_METADATA = ROOT / "raw" / "metadata"
REVIEW_QUEUE = ROOT / "raw" / "review_queue.md"
WIKI_LOG = ROOT / "wiki" / "log.md"

ACCEPT_THRESHOLD = 0.70
REVIEW_THRESHOLD = 0.40
VALID_TASKS = {"TTS", "VC", "SCA", "codec", "evaluation", "singing"}

DEFAULT_MODEL = "claude-haiku-4-5-20251001"
DEFAULT_BATCH_SIZE = 10

# ---------------------------------------------------------------------------
# System prompt and tool definition
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are a relevance filter for a systematic review of speech generation research.

## In scope — score HIGH

- TTS: text-to-speech — synthesising speech from text input
- VC: voice conversion — transforming one speaker's voice into another's
- SCA: spoken conversational agent — speech language models that conduct spoken dialogue
- codec: neural audio codecs (e.g. EnCodec, SoundStream, DAC) as foundational technology for speech generation
- evaluation: papers primarily about evaluation methodology, benchmarks, or metrics for speech generation systems
- singing: singing voice synthesis

## Out of scope — score LOW

- ASR / automatic speech recognition, unless the paper also makes a synthesis contribution
- Speaker verification, identification, or diarisation
- Speech enhancement or denoising
- Audio source separation
- Music information retrieval (non-singing)
- Papers that only use TTS as a data augmentation tool for a different primary task

## Scoring rubric

0.85–1.0  Primary contribution is generating, converting, or modelling speech for output
0.70–0.85 Closely related: neural codec, speech LM, or evaluation framework for generation
0.40–0.70 Borderline: synthesis present but not primary focus, or abstract is ambiguous
0.10–0.40 Adjacent: mentions synthesis but primary task is recognition, enhancement, or other
0.00–0.10 Not relevant to speech generation

## Instructions

Call the score_papers tool with one entry per paper.
- relevance_note: one concise sentence explaining the score
- task: list of applicable labels from [TTS, VC, SCA, codec, evaluation, singing]; \
empty list if not relevant
"""

SCORE_TOOL = {
    "name": "score_papers",
    "description": "Submit relevance scores for a batch of academic papers.",
    "input_schema": {
        "type": "object",
        "properties": {
            "scores": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "relevance_score": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 1.0,
                        },
                        "relevance_note": {"type": "string"},
                        "task": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": sorted(VALID_TASKS),
                            },
                        },
                    },
                    "required": ["id", "relevance_score", "relevance_note", "task"],
                },
            }
        },
        "required": ["scores"],
    },
}

# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_pending() -> list[dict]:
    papers = []
    for path in sorted(RAW_METADATA.glob("*.json")):
        try:
            data = json.loads(path.read_text())
            if data.get("status") == "pending":
                papers.append(data)
        except Exception as exc:
            print(f"  Warning: could not read {path.name}: {exc}")
    return papers

# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------

def build_user_message(batch: list[dict]) -> str:
    parts = []
    for i, paper in enumerate(batch, 1):
        parts.append(
            f"Paper {i} (ID: {paper['id']})\n"
            f"Title: {paper['title']}\n"
            f"Abstract: {paper.get('abstract', '(no abstract)')}"
        )
    return "\n\n".join(parts)


def call_api(
    client: anthropic.Anthropic,
    model: str,
    batch: list[dict],
    max_retries: int = 3,
) -> list[dict] | None:
    user_msg = build_user_message(batch)
    expected_ids = {p["id"] for p in batch}

    for attempt in range(max_retries):
        try:
            response = client.messages.create(
                model=model,
                max_tokens=1024,
                system=SYSTEM_PROMPT,
                tools=[SCORE_TOOL],
                tool_choice={"type": "tool", "name": "score_papers"},
                messages=[{"role": "user", "content": user_msg}],
            )

            scores = None
            for block in response.content:
                if block.type == "tool_use" and block.name == "score_papers":
                    scores = block.input.get("scores", [])
                    break

            if scores is None:
                raise ValueError("No score_papers tool call in response")

            missing = expected_ids - {s["id"] for s in scores}
            if missing:
                raise ValueError(f"Missing scores for: {missing}")

            for s in scores:
                s["relevance_score"] = max(0.0, min(1.0, float(s["relevance_score"])))
                s["task"] = [t for t in s.get("task", []) if t in VALID_TASKS]

            return scores

        except anthropic.APIError as exc:
            wait = 2 ** attempt
            print(f"    API error (attempt {attempt + 1}/{max_retries}): {exc} — retrying in {wait}s")
            time.sleep(wait)
        except Exception as exc:
            print(f"    Validation error (attempt {attempt + 1}/{max_retries}): {exc}")
            if attempt < max_retries - 1:
                time.sleep(1)

    return None


def score_batch(
    client: anthropic.Anthropic,
    model: str,
    batch: list[dict],
) -> list[dict]:
    """Score a batch, falling back to individual scoring if the batch call fails."""
    result = call_api(client, model, batch)
    if result is not None:
        return result

    if len(batch) == 1:
        # Single paper failed — return a safe placeholder flagged for review
        print(f"    Permanent failure for {batch[0]['id']} — marking for review")
        return [{
            "id": batch[0]["id"],
            "relevance_score": 0.5,
            "relevance_note": "Score unavailable due to API error — requires manual review.",
            "task": [],
        }]

    print(f"    Batch failed — falling back to individual scoring ({len(batch)} papers)")
    all_scores = []
    for paper in batch:
        all_scores.extend(score_batch(client, model, [paper]))
    return all_scores

# ---------------------------------------------------------------------------
# Applying scores
# ---------------------------------------------------------------------------

def status_from_score(score: float) -> str:
    if score > ACCEPT_THRESHOLD:
        return "accepted"
    elif score >= REVIEW_THRESHOLD:
        return "review"
    return "rejected"


def format_review_entry(paper: dict, s: dict) -> str:
    authors = ", ".join(paper.get("authors", []))
    task_str = ", ".join(s["task"]) or "unclear"
    abstract = paper.get("abstract") or ""
    excerpt = abstract[:300] + ("..." if len(abstract) > 300 else "")
    return (
        f"## {paper['id']} | {paper['title']} | arXiv | score: {s['relevance_score']:.2f}\n\n"
        f"**Authors:** {authors}\n"
        f"**Task guess:** {task_str}\n"
        f"**Reason for review:** {s['relevance_note']}\n"
        f"**Abstract excerpt:** {excerpt}\n\n"
        f"**Decision:** [ ] accept  [ ] reject  [ ] accept-partial (note: _________)\n\n"
        f"---\n"
    )


def apply_scores(
    batch: list[dict],
    scores: list[dict],
    dry_run: bool,
    review_entries: list[str],
) -> tuple[int, int, int]:
    score_by_id = {s["id"]: s for s in scores}
    accepted = review = rejected = 0

    for paper in batch:
        s = score_by_id.get(paper["id"])
        if s is None:
            print(f"    Warning: no score for {paper['id']} — skipping")
            continue

        status = status_from_score(s["relevance_score"])
        label = {"accepted": "→ accepted", "review": "→ review  ", "rejected": "→ rejected"}[status]
        task_str = f"[{', '.join(s['task'])}]" if s["task"] else "[]"
        print(f"  {paper['id']}  {s['relevance_score']:.2f}  {task_str:<22}  {label}  {s['relevance_note'][:65]}")

        if status == "accepted":
            accepted += 1
        elif status == "review":
            review += 1
            review_entries.append(format_review_entry(paper, s))
        else:
            rejected += 1

        if not dry_run:
            paper.update({
                "relevance_score": s["relevance_score"],
                "relevance_note": s["relevance_note"],
                "task": s["task"],
                "status": status,
            })
            (RAW_METADATA / f"{paper['id']}.json").write_text(
                json.dumps(paper, indent=2, ensure_ascii=False)
            )

    return accepted, review, rejected

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def filter_papers(
    model: str = DEFAULT_MODEL,
    batch_size: int = DEFAULT_BATCH_SIZE,
    dry_run: bool = False,
    limit: int | None = None,
) -> dict:
    client = anthropic.Anthropic()
    pending = load_pending()
    if limit:
        pending = pending[:limit]

    total = len(pending)
    if total == 0:
        print("No pending papers found.")
        return {"accepted": 0, "review": 0, "rejected": 0}

    print(f"Model     : {model}")
    print(f"Pending   : {total} papers")
    print(f"Batch size: {batch_size}")
    print(f"Dry run   : {dry_run}")
    print()

    batches = [pending[i : i + batch_size] for i in range(0, total, batch_size)]
    n_batches = len(batches)

    total_accepted = total_review = total_rejected = 0
    review_entries: list[str] = []

    for i, batch in enumerate(batches, 1):
        span = f"{batch[0]['id']} – {batch[-1]['id']}" if len(batch) > 1 else batch[0]["id"]
        print(f"[{i}/{n_batches}] {span}")

        scores = score_batch(client, model, batch)
        a, r, rej = apply_scores(batch, scores, dry_run, review_entries)
        total_accepted += a
        total_review += r
        total_rejected += rej
        print(f"  Running: {total_accepted} accepted, {total_review} review, {total_rejected} rejected\n")

    if review_entries and not dry_run:
        with open(REVIEW_QUEUE, "a") as f:
            f.write("\n" + "\n".join(review_entries))
        print(f"Appended {len(review_entries)} entries to {REVIEW_QUEUE.name}")

    log_line = (
        f"\n## [{date.today().isoformat()}] filter | arXiv | "
        f"{total_accepted} accepted, {total_review} review, {total_rejected} rejected"
    )
    if not dry_run:
        with open(WIKI_LOG, "a") as f:
            f.write(log_line)
        print(f"Appended filter entry to {WIKI_LOG.name}")

    prefix = "[DRY RUN] " if dry_run else ""
    print()
    print(f"{prefix}Done.")
    print(f"  Accepted : {total_accepted}")
    print(f"  Review   : {total_review}")
    print(f"  Rejected : {total_rejected}")
    print(f"  Total    : {total_accepted + total_review + total_rejected}")

    return {"accepted": total_accepted, "review": total_review, "rejected": total_rejected}

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--model", default=DEFAULT_MODEL,
                   help=f"Claude model ID (default: {DEFAULT_MODEL})")
    p.add_argument("--batch-size", type=int, default=DEFAULT_BATCH_SIZE,
                   help=f"Papers per API call (default: {DEFAULT_BATCH_SIZE})")
    p.add_argument("--dry-run", action="store_true",
                   help="Score and print but do not write any files")
    p.add_argument("--limit", type=int, default=None,
                   help="Process at most N papers (useful for testing)")
    args = p.parse_args()

    filter_papers(
        model=args.model,
        batch_size=args.batch_size,
        dry_run=args.dry_run,
        limit=args.limit,
    )


if __name__ == "__main__":
    main()
