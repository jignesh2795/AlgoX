"""Pluggable semantic-retrieval contract.

The default implementation is intentionally dependency-free. It provides a
small token-vector baseline so semantic retrieval can be benchmarked without
making a particular embedding model or vector database an architectural
requirement.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from dataclasses import dataclass

from .store import InMemoryStore, MemoryRecord

_TOKEN = re.compile(r"[a-z0-9]+")


def _tokens(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


def _cosine(a: Counter[str], b: Counter[str]) -> float:
    if not a or not b:
        return 0.0
    dot = sum(a[k] * b[k] for k in a.keys() & b.keys())
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


@dataclass(frozen=True)
class SemanticMatch:
    memory: MemoryRecord
    score: float


class SemanticRetriever:
    """Embedding-provider-shaped interface with a deterministic baseline."""

    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def search(self, query: str, *, limit: int = 10, min_score: float = 0.0) -> list[SemanticMatch]:
        query_vector = Counter(_tokens(query))
        matches = []
        for memory in self.store.memories.values():
            if memory.status != "active":
                continue
            score = _cosine(query_vector, Counter(_tokens(memory.content)))
            if score >= min_score:
                matches.append(SemanticMatch(memory, score))
        return sorted(matches, key=lambda item: (-item.score, item.memory.id))[:limit]


class SemanticAdapter:
    """Protocol-like base contract for future embedding/vector implementations."""

    def search(self, query: str, *, limit: int = 10) -> list[SemanticMatch]:
        raise NotImplementedError
