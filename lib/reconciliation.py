"""Deterministic primitives for cross-concept reconciliation."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import date, datetime
import hashlib
import json
import math
from pathlib import Path
import re
from typing import Iterable

import yaml


TOKEN_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
QUALIFIED_REF_RE = re.compile(r"^(?P<concept>[a-z0-9-]+)#(?P<cluster>[a-z0-9_]+)$")
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "being", "by", "can", "for",
    "from", "has", "have", "in", "into", "is", "it", "its", "may", "more", "of", "on",
    "or", "that", "the", "their", "than", "this", "to", "using", "via", "when", "while",
    "with", "without", "within", "across", "based", "enables", "improves", "models", "model",
    "systems", "system", "speech", "generation", "tts",
}

THEME_KEYWORDS = (
    ("evaluation", {"evaluation", "metric", "metrics", "mos", "mushra", "subjective", "preference", "benchmark", "score", "scores", "intelligibility", "quality", "listener", "human"}),
    ("streaming-agents", {"streaming", "stream", "duplex", "turn-taking", "dialogue", "agent", "agents", "conversation", "interactive", "responsiveness"}),
    ("efficiency", {"latency", "efficient", "efficiency", "decoding", "inference", "nfe", "realtime", "real-time", "throughput", "speed", "compute"}),
    ("speaker", {"speaker", "voice", "identity", "similarity", "adaptation", "cloning", "timbre", "verification"}),
    ("controllability", {"prosody", "emotion", "style", "control", "controllable", "expressive", "expressivity", "conditioning", "disentanglement"}),
    ("post-training", {"rlhf", "reward", "rewards", "preference", "fine-tuning", "finetuning", "adapter", "adapters", "post-training", "alignment"}),
    ("codecs-language-modeling", {"codec", "codecs", "token", "tokens", "semantic", "acoustic", "language", "autoregressive", "quantization", "representation"}),
    ("robustness", {"robust", "robustness", "generalization", "generalisation", "scaling", "diversity", "multilingual", "unseen", "low-resource", "cross-lingual"}),
)


@dataclass(frozen=True)
class ClusterRecord:
    ref: str
    concept: str
    cluster_id: str
    claim: str
    status: str
    supporting_papers: tuple[str, ...]
    contradicting_papers: tuple[str, ...]
    refining_papers: tuple[str, ...]
    tokens: tuple[str, ...]
    technical_terms: tuple[str, ...]


def _jsonable(value):
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def canonical_bytes(value: object, *, omit_digest: bool = False) -> bytes:
    normalized = _jsonable(value)
    if omit_digest and isinstance(normalized, dict):
        normalized = dict(normalized)
        normalized.pop("digest", None)
    text = json.dumps(
        normalized,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return (text + "\n").encode("utf-8")


def canonical_digest(value: object, *, omit_digest: bool = False) -> str:
    return "sha256:" + hashlib.sha256(canonical_bytes(value, omit_digest=omit_digest)).hexdigest()


def load_yaml(path: Path) -> dict:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML: {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ValueError(f"YAML is not a mapping: {path}")
    return data


def load_concept_graphs(wiki_dir: Path) -> dict[str, dict]:
    claims_dir = wiki_dir / "_claims"
    paths = sorted(claims_dir.glob("*.yaml")) if claims_dir.is_dir() else []
    if not paths:
        raise ValueError(f"no concept YAML files found: {claims_dir}")
    graphs: dict[str, dict] = {}
    for path in paths:
        data = load_yaml(path)
        concept = data.get("concept")
        if concept != path.stem:
            raise ValueError(f"concept/path mismatch: {path}: {concept!r}")
        if concept in graphs:
            raise ValueError(f"duplicate concept slug: {concept}")
        graphs[concept] = data
    return graphs


def tokenize(text: str) -> tuple[str, ...]:
    return tuple(TOKEN_RE.findall(text.lower()))


def technical_terms(tokens: Iterable[str]) -> tuple[str, ...]:
    return tuple(sorted({token for token in tokens if token not in STOPWORDS and len(token) > 2}))


def cluster_records(graphs: dict[str, dict]) -> list[ClusterRecord]:
    records: list[ClusterRecord] = []
    for concept, data in sorted(graphs.items()):
        seen_ids: set[str] = set()
        for cluster in data.get("claim_clusters") or []:
            if not isinstance(cluster, dict):
                raise ValueError(f"{concept}: claim cluster is not a mapping")
            cluster_id = cluster.get("id")
            claim = cluster.get("claim")
            if not isinstance(cluster_id, str) or not isinstance(claim, str):
                raise ValueError(f"{concept}: cluster id/claim missing")
            if cluster_id in seen_ids:
                raise ValueError(f"{concept}: duplicate cluster id {cluster_id}")
            seen_ids.add(cluster_id)
            ref = f"{concept}#{cluster_id}"
            tokens = tokenize(claim)
            records.append(ClusterRecord(
                ref=ref,
                concept=concept,
                cluster_id=cluster_id,
                claim=claim,
                status=str(cluster.get("status", "")),
                supporting_papers=tuple(sorted(set(map(str, cluster.get("supporting_papers") or [])))),
                contradicting_papers=tuple(sorted(set(map(str, cluster.get("contradicting_papers") or [])))),
                refining_papers=tuple(sorted(set(map(str, cluster.get("refining_papers") or [])))),
                tokens=tokens,
                technical_terms=technical_terms(tokens),
            ))
    return sorted(records, key=lambda item: item.ref)


def tfidf_vectors(records: list[ClusterRecord]) -> dict[str, dict[str, float]]:
    document_frequency: Counter[str] = Counter()
    for record in records:
        document_frequency.update(set(record.tokens))
    count = len(records)
    vectors: dict[str, dict[str, float]] = {}
    for record in records:
        term_frequency = Counter(record.tokens)
        vector: dict[str, float] = {}
        for token, frequency in term_frequency.items():
            inverse_document_frequency = math.log((1 + count) / (1 + document_frequency[token])) + 1
            vector[token] = (1 + math.log(frequency)) * inverse_document_frequency
        norm = math.sqrt(sum(value * value for value in vector.values()))
        vectors[record.ref] = (
            {token: value / norm for token, value in vector.items()} if norm else {}
        )
    return vectors


def cosine(left: dict[str, float], right: dict[str, float]) -> float:
    if len(left) > len(right):
        left, right = right, left
    return sum(value * right.get(token, 0.0) for token, value in left.items())


def jaccard(left: Iterable[str], right: Iterable[str]) -> float:
    left_set, right_set = set(left), set(right)
    union = left_set | right_set
    return len(left_set & right_set) / len(union) if union else 0.0


def status_compatible(left: ClusterRecord, right: ClusterRecord) -> bool:
    groups = {
        "strongly_supported": "positive",
        "emerging": "positive",
        "contested": "mixed",
        "weakened": "mixed",
        "superseded": "historical",
        "historical": "historical",
    }
    return groups.get(left.status, left.status) == groups.get(right.status, right.status)


def polarity_compatible(left: ClusterRecord, right: ClusterRecord) -> bool:
    left_mixed = bool(left.contradicting_papers)
    right_mixed = bool(right.contradicting_papers)
    return left_mixed == right_mixed


def classify_theme(left: ClusterRecord, right: ClusterRecord) -> str:
    tokens = set(left.tokens) | set(right.tokens) | {left.concept, right.concept}
    best_theme = "robustness"
    best_score = 0
    for theme, keywords in THEME_KEYWORDS:
        score = len(tokens & keywords)
        if score > best_score:
            best_theme, best_score = theme, score
    return best_theme


def stable_candidate_id(left_ref: str, right_ref: str) -> str:
    left_ref, right_ref = sorted((left_ref, right_ref))
    digest = hashlib.sha256(f"{left_ref}\n{right_ref}".encode("utf-8")).hexdigest()[:16]
    return f"cand_{digest}"


def find_cycles(edges: dict[str, set[str]]) -> list[list[str]]:
    cycles: list[list[str]] = []
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(node: str) -> None:
        marker = state.get(node, 0)
        if marker == 2:
            return
        if marker == 1:
            index = stack.index(node)
            cycle = stack[index:] + [node]
            canonical = min(tuple(cycle[i:-1] + cycle[:i] + [cycle[i]]) for i in range(len(cycle) - 1))
            if list(canonical) not in cycles:
                cycles.append(list(canonical))
            return
        state[node] = 1
        stack.append(node)
        for target in sorted(edges.get(node, set())):
            visit(target)
        stack.pop()
        state[node] = 2

    for node in sorted(set(edges) | {target for values in edges.values() for target in values}):
        visit(node)
    return sorted(cycles)
