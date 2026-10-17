"""Evidence-bundle retrieval over the canonical memory store.

This module is deliberately deterministic. Semantic embeddings and external
indexes are adapters to add later; they must not become authoritative.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .store import InMemoryStore, MemoryRecord


@dataclass(frozen=True)
class EvidenceBundle:
    query: str
    memories: tuple[MemoryRecord, ...]
    supporting_evidence: tuple[str, ...]
    counter_evidence: tuple[str, ...]
    temporal_as_of: datetime | None = None


class EvidenceRetriever:
    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def retrieve(self, query: str, *, as_of: datetime | None = None, limit: int = 10) -> EvidenceBundle:
        memories = self.store.retrieve(query, as_of=as_of)
        memories = memories[:limit]
        selected = {memory.id for memory in memories}
        supporting: list[str] = []
        counter: list[str] = []
        for memory in memories:
            supporting.extend(memory.evidence_ids)
            for relation, target_id in memory.relations:
                if relation == "contradicts" and target_id in self.store.memories:
                    counter.extend(self.store.memories[target_id].evidence_ids)
                elif relation in {"qualifies", "refutes"} and target_id in self.store.memories:
                    counter.extend(self.store.memories[target_id].evidence_ids)
        # Preserve deterministic order while removing duplicates.
        supporting = list(dict.fromkeys(supporting))
        counter = [eid for eid in dict.fromkeys(counter) if eid not in supporting]
        return EvidenceBundle(query, tuple(memories), tuple(supporting), tuple(counter), as_of)

    def related(self, memory_id: str, *, depth: int = 1) -> list[MemoryRecord]:
        """Return deterministic breadth-first relationship traversal."""
        if memory_id not in self.store.memories:
            raise KeyError(memory_id)
        seen = {memory_id}
        frontier = [memory_id]
        result: list[MemoryRecord] = []
        for _ in range(depth):
            next_frontier: list[str] = []
            for current in frontier:
                for _, target in self.store.memories[current].relations:
                    if target not in seen and target in self.store.memories:
                        seen.add(target)
                        next_frontier.append(target)
                        result.append(self.store.memories[target])
            frontier = next_frontier
            if not frontier:
                break
        return result
