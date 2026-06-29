"""
Dedup check for the 56 OpenReview papers (ICLR 2025/2026, NeurIPS 2025).

For each OpenReview paper, checks whether a paper with the same normalised title
already exists in the corpus under a different ID (typically an arXiv preprint).

When a collision is found the script:
  - Prints the pair with both IDs, statuses, and titles
  - Optionally updates the OpenReview record to mark it as non-duplicate (if the
    arXiv version is canonical) or marks the arXiv record as duplicate of the
    proceedings ID (correct canonical direction: proceedings > arXiv)

Run:
    python scripts/fetch/dedup_openreview.py [--apply]

Without --apply, the script is read-only and prints a report.
With --apply, it writes is_duplicate/canonical_id into the losing record's JSON.
"""

import argparse
import json
import re
import sys
from pathlib import Path

METADATA_DIR = Path("raw/metadata")
OPENREVIEW_PREFIXES = ("iclr-2025-", "neurips-2025-", "iclr-2026-")


def normalise(title: str) -> str:
    t = title.lower()
    t = re.sub(r"[^a-z0-9 ]", "", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def load_all() -> dict[str, dict]:
    papers = {}
    for f in METADATA_DIR.glob("*.json"):
        try:
            d = json.loads(f.read_text())
            papers[d["id"]] = d
        except Exception as e:
            print(f"  WARN: could not load {f.name}: {e}", file=sys.stderr)
    return papers


def is_openreview(paper_id: str) -> bool:
    return any(paper_id.startswith(p) for p in OPENREVIEW_PREFIXES)


def main():
    parser = argparse.ArgumentParser(description="Dedup OpenReview papers against corpus")
    parser.add_argument("--apply", action="store_true",
                        help="Write is_duplicate/canonical_id changes to metadata files")
    args = parser.parse_args()

    papers = load_all()

    # Build normalised-title → [id, ...] index for the non-OpenReview corpus
    title_index: dict[str, list[str]] = {}
    for pid, p in papers.items():
        if is_openreview(pid):
            continue
        if p.get("status") == "rejected":
            continue
        norm = normalise(p.get("title", ""))
        if norm:
            title_index.setdefault(norm, []).append(pid)

    openreview_papers = {pid: p for pid, p in papers.items() if is_openreview(pid)}
    print(f"OpenReview papers to check: {len(openreview_papers)}")
    print(f"Corpus index size (non-OpenReview, non-rejected): {len(title_index)}\n")

    collisions = []
    for pid, p in sorted(openreview_papers.items()):
        norm = normalise(p.get("title", ""))
        if not norm:
            print(f"  WARN: {pid} has no title")
            continue
        matches = title_index.get(norm, [])
        for match_id in matches:
            collisions.append((pid, match_id, p, papers[match_id]))

    if not collisions:
        print("No title collisions found. All 56 OpenReview papers are unique.")
        return

    print(f"{'='*70}")
    print(f"COLLISIONS FOUND: {len(collisions)}")
    print(f"{'='*70}\n")

    for or_id, corpus_id, or_paper, corpus_paper in collisions:
        or_status = or_paper.get("status", "?")
        corpus_status = corpus_paper.get("status", "?")
        print(f"  PROCEEDINGS: {or_id}  [status: {or_status}]")
        print(f"  CORPUS COPY: {corpus_id}  [status: {corpus_status}]")
        print(f"  TITLE:       {or_paper.get('title', '')}")
        already_flagged = corpus_paper.get("is_duplicate") or or_paper.get("is_duplicate")
        print(f"  Already flagged as duplicate: {already_flagged}")
        print()

    if args.apply:
        print(f"\n{'='*70}")
        print("APPLYING CHANGES")
        print(f"{'='*70}\n")
        for or_id, corpus_id, or_paper, corpus_paper in collisions:
            corpus_status = corpus_paper.get("status", "")
            # Proceedings ID is canonical. Mark the arXiv/non-proceedings record as duplicate.
            # Exception: if the corpus copy is already ingested, flag it but don't change status
            # (wiki migration is a separate manual step).
            corpus_paper["is_duplicate"] = True
            corpus_paper["canonical_id"] = or_id
            corpus_path = METADATA_DIR / f"{corpus_id}.json"
            corpus_path.write_text(json.dumps(corpus_paper, indent=2) + "\n")

            if corpus_status == "ingested":
                print(f"  {corpus_id}: flagged as duplicate of {or_id} — status kept 'ingested' (wiki migration required)")
            else:
                # Also set status to rejected so it doesn't get re-ingested
                corpus_paper["status"] = "rejected"
                corpus_path.write_text(json.dumps(corpus_paper, indent=2) + "\n")
                print(f"  {corpus_id}: flagged as duplicate of {or_id} — status set to 'rejected'")

            # Ensure the OpenReview record is NOT marked as duplicate
            if or_paper.get("is_duplicate"):
                or_paper["is_duplicate"] = False
                or_paper["canonical_id"] = None
                or_path = METADATA_DIR / f"{or_id}.json"
                or_path.write_text(json.dumps(or_paper, indent=2) + "\n")
                print(f"  {or_id}: cleared stale is_duplicate flag")
        print("\nDone.")
    else:
        print(f"Run with --apply to write changes to metadata files.")


if __name__ == "__main__":
    main()
