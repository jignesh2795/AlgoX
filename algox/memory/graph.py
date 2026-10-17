"""Derived logical knowledge-graph projection over memory relations."""

from __future__ import annotations

from dataclasses import dataclass

from .store import InMemoryStore


@dataclass(frozen=True)
class GraphEdge:
    source: str
    relation: str
    target: str


class MemoryGraph:
    """Graph projection rebuilt from the authoritative memory store."""

    def __init__(self, store: InMemoryStore) -> None:
        self.store = store

    def edges(self) -> list[GraphEdge]:
        result: list[GraphEdge] = []
        for memory in self.store.memories.values():
            for relation, target in memory.relations:
                result.append(GraphEdge(memory.id, relation, target))
        return result

    def neighbors(self, memory_id: str, *, relation: str | None = None) -> list[str]:
        if memory_id not in self.store.memories:
            raise KeyError(memory_id)
        return [
            target
            for rel, target in self.store.memories[memory_id].relations
            if relation is None or rel == relation
        ]

    def path(self, source_id: str, target_id: str, *, max_depth: int = 5) -> list[str] | None:
        if source_id not in self.store.memories or target_id not in self.store.memories:
            raise KeyError("both graph endpoints must exist")
        queue: list[list[str]] = [[source_id]]
        visited = {source_id}
        while queue:
            current = queue.pop(0)
            if current[-1] == target_id:
                return current
            if len(current) - 1 >= max_depth:
                continue
            for neighbor in self.neighbors(current[-1]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(current + [neighbor])
        return None

    def rebuild_signature(self) -> tuple[tuple[str, str, str], ...]:
        return tuple(sorted((e.source, e.relation, e.target) for e in self.edges()))
