#!/usr/bin/env python3
"""Freeze a deterministic quarter-integration candidate manifest.

The manifest is a read-only audit of canonical metadata, production paper frontmatter, the paper
catalog, and top-level claim YAMLs.  It never edits content or claims.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ACTIVE_STATUSES = {"accepted", "ingested"}


def _frontmatter(path: Path) -> dict:
    text = path.read_text()
    if not text.startswith("---\n") or "\n---\n" not in text[4:]:
        raise ValueError(f"invalid frontmatter: {path}")
    return yaml.safe_load(text.split("---", 2)[1]) or {}


def _claim_ids(wiki_dir: Path) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for path in sorted((wiki_dir / "_claims").glob("*.yaml")):
        data = yaml.safe_load(path.read_text()) or {}
        result[path.stem] = {
            str(item["id"])
            for item in data.get("papers", [])
            if isinstance(item, dict) and item.get("id") is not None
        }
    return result


def build_manifest(
    metadata_dir: Path,
    wiki_dir: Path,
    *,
    quarter: str,
    start: str,
    end: str,
    infra_commit: str,
    content_commit: str,
) -> dict:
    claims = _claim_ids(wiki_dir)
    canonical_concepts = set(claims)
    index_text = (wiki_dir / "papers" / "index.md").read_text()
    eligible: list[dict] = []
    excluded: list[dict] = []
    errors: list[str] = []

    for path in sorted(metadata_dir.glob("*.json")):
        record = json.loads(path.read_text())
        published_date = str(record.get("published_date") or "")
        if not (start <= published_date <= end):
            continue
        if record.get("status") not in ACTIVE_STATUSES:
            continue
        paper_id = str(record.get("id") or path.stem)
        if record.get("is_duplicate"):
            excluded.append({"id": paper_id, "reason": "duplicate pointer"})
            continue
        page_path = wiki_dir / "papers" / f"{paper_id}.md"
        if not page_path.exists():
            excluded.append({"id": paper_id, "reason": "no production paper page"})
            continue
        frontmatter = _frontmatter(page_path)
        if record.get("ingest_tier") == 2 or frontmatter.get("ingest_tier") == 2:
            excluded.append({"id": paper_id, "reason": "Tier 2 page"})
            continue
        if str(frontmatter.get("id")) != paper_id:
            errors.append(f"{paper_id}: page frontmatter ID is {frontmatter.get('id')!r}")
        if str(frontmatter.get("published_date")) != published_date:
            errors.append(
                f"{paper_id}: page published_date {frontmatter.get('published_date')!r} "
                f"!= metadata {published_date}"
            )
        row_count = index_text.count(f"[[{paper_id}]]")
        if row_count != 1:
            errors.append(f"{paper_id}: expected one paper-index row, found {row_count}")
        related = [str(item) for item in (frontmatter.get("related_concepts") or [])]
        unknown = sorted(set(related) - canonical_concepts)
        if unknown:
            errors.append(f"{paper_id}: unknown related concepts: {', '.join(unknown)}")
        eligible.append(
            {
                "id": paper_id,
                "title": str(record.get("title") or frontmatter.get("title") or ""),
                "published_date": published_date,
                "venue": record.get("venue"),
                "related_concepts": related,
            }
        )

    eligible.sort(key=lambda item: (item["published_date"], item["id"]))
    excluded.sort(key=lambda item: item["id"])
    by_concept: dict[str, list[str]] = defaultdict(list)
    for paper in eligible:
        for concept in paper["related_concepts"]:
            by_concept[concept].append(paper["id"])

    concepts = []
    for concept, ids in sorted(by_concept.items(), key=lambda item: (-len(item[1]), item[0])):
        already = sorted(set(ids) & claims.get(concept, set()))
        queue = [paper_id for paper_id in ids if paper_id not in claims.get(concept, set())]
        concepts.append(
            {
                "concept": concept,
                "candidates": len(ids),
                "already_present": len(already),
                "queue_size": len(queue),
                "candidate_ids": ids,
                "already_present_ids": already,
                "queue_ids": queue,
            }
        )

    unassigned = [paper["id"] for paper in eligible if not paper["related_concepts"]]
    return {
        "schema_version": 1,
        "quarter": quarter,
        "date_range": {"start": start, "end": end, "inclusive": True},
        "evidence_cutoff": end,
        "starting_commits": {"infrastructure": infra_commit, "content": content_commit},
        "summary": {
            "eligible_papers": len(eligible),
            "assigned_papers": len(eligible) - len(unassigned),
            "unassigned_papers": len(unassigned),
            "excluded_active_records": len(excluded),
            "affected_concepts": len(concepts),
            "candidate_memberships": sum(item["candidates"] for item in concepts),
            "already_present_memberships": sum(item["already_present"] for item in concepts),
            "phase_1_queue_memberships": sum(item["queue_size"] for item in concepts),
            "validation_errors": len(errors),
        },
        "intentional_unassigned": unassigned,
        "excluded": excluded,
        "concepts": concepts,
        "papers": eligible,
        "errors": errors,
    }


def render_manifest(manifest: dict) -> str:
    canonical = json.dumps(manifest, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    digest = hashlib.sha256(canonical.encode()).hexdigest()
    return json.dumps(
        {"sha256": digest, **manifest}, indent=2, ensure_ascii=False, sort_keys=True
    ) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wiki-dir", type=Path, required=True)
    parser.add_argument("--quarter", required=True)
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--infra-commit", required=True)
    parser.add_argument("--content-commit", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    manifest = build_manifest(
        ROOT / "raw" / "metadata",
        args.wiki_dir,
        quarter=args.quarter,
        start=args.start,
        end=args.end,
        infra_commit=args.infra_commit,
        content_commit=args.content_commit,
    )
    if manifest["errors"]:
        for error in manifest["errors"]:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    rendered = render_manifest(manifest)
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
