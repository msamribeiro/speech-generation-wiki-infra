"""Deterministic source projection for the current field overview."""

from __future__ import annotations

from collections.abc import Mapping


EVIDENCE_ROLES = (
    "supporting_papers",
    "contradicting_papers",
    "refining_papers",
)


def _cluster_index(graphs: Mapping[str, dict]) -> dict[str, dict]:
    clusters: dict[str, dict] = {}
    for concept, graph in sorted(graphs.items()):
        for cluster in graph.get("claim_clusters") or []:
            ref = f"{concept}#{cluster['id']}"
            if ref in clusters:
                raise ValueError(f"duplicate qualified cluster reference: {ref}")
            clusters[ref] = cluster
    return clusters


def project_field_conclusions(graphs: Mapping[str, dict], registry: dict) -> dict:
    """Collapse approved broader-claim members and retain all other local clusters.

    The result is an editorial source, not reader-facing prose. Human-approved broader
    claims occur once, evidence IDs are deduplicated, and both broader and member-local
    caveats remain available to the renderer. Agent proposals are ignored.
    """

    clusters = _cluster_index(graphs)
    grouped_refs: set[str] = set()
    broader_conclusions: list[dict] = []

    approved = sorted(
        (
            item
            for item in registry.get("broader_claims") or []
            if item.get("review_status") == "human_approved"
        ),
        key=lambda item: item["id"],
    )
    for broader in approved:
        members: list[dict] = []
        member_refs: set[str] = set()
        evidence = {role: set() for role in EVIDENCE_ROLES}
        for member in broader.get("members") or []:
            ref = member["claim"]
            if ref in member_refs:
                raise ValueError(f"duplicate member in {broader['id']}: {ref}")
            if ref not in clusters:
                raise ValueError(f"missing member in {broader['id']}: {ref}")
            member_refs.add(ref)
            grouped_refs.add(ref)
            cluster = clusters[ref]
            for role in EVIDENCE_ROLES:
                evidence[role].update(str(paper) for paper in cluster.get(role) or [])
            members.append(
                {
                    "ref": ref,
                    "claim": cluster.get("claim"),
                    "status": cluster.get("status"),
                    "confidence": cluster.get("confidence"),
                    "caveats": list(cluster.get("caveats") or []),
                    "relationship": member.get("relationship"),
                    "rationale": member.get("rationale"),
                }
            )

        broader_conclusions.append(
            {
                "id": broader["id"],
                "proposition": broader["proposition"],
                "status": broader["status"],
                "confidence": broader["confidence"],
                "members": members,
                "evidence": {
                    role: sorted(papers) for role, papers in evidence.items()
                },
                "caveats": list(broader.get("caveats") or []),
            }
        )

    local_conclusions = [
        {"ref": ref, **cluster}
        for ref, cluster in sorted(clusters.items())
        if ref not in grouped_refs
    ]
    paper_memberships = [
        str(paper["id"])
        for graph in graphs.values()
        for paper in graph.get("papers") or []
    ]
    return {
        "broader_conclusions": broader_conclusions,
        "local_conclusions": local_conclusions,
        "stats": {
            "concepts": len(graphs),
            "claim_clusters": len(clusters),
            "broader_claims": len(broader_conclusions),
            "concept_paper_memberships": len(paper_memberships),
            "unique_papers": len(set(paper_memberships)),
            "overlapping_memberships": len(paper_memberships) - len(set(paper_memberships)),
        },
    }
