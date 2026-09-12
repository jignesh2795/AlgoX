"""Minimal storage-independent memory engine.

The implementation intentionally keeps authority in structured records. Vector
and graph indexes can later become derived adapters without changing callers.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable


@dataclass(frozen=True)
class Evidence:
    id: str
    source_id: str
    locator: str
    observed_at: datetime
    maturity: str = "C1"


@dataclass
class MemoryRecord:
    id: str
    memory_type: str
    content: str
    created_at: datetime
    confidence: str = "unknown"
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    evidence_ids: list[str] = field(default_factory=list)
    status: str = "active"
    relations: list[tuple[str, str]] = field(default_factory=list)


@dataclass(frozen=True)
class KnowledgeDelta:
    id: str
    operation: str
    entity_type: str
    entity_id: str
    evidence_ids: tuple[str, ...]
    reason: str
    confidence: str = "unknown"


class InMemoryStore:
    """Reference implementation of AlgoX's memory contract."""

    def __init__(self) -> None:
        self.evidence: dict[str, Evidence] = {}
        self.memories: dict[str, MemoryRecord] = {}
        self.deltas: dict[str, KnowledgeDelta] = {}

    def add_evidence(self, evidence: Evidence) -> None:
        if evidence.id in self.evidence:
            raise ValueError(f"evidence already exists: {evidence.id}")
        self.evidence[evidence.id] = evidence

    def add_memory(self, memory: MemoryRecord) -> None:
        if memory.id in self.memories:
            raise ValueError(f"memory already exists: {memory.id}")
        missing = set(memory.evidence_ids) - self.evidence.keys()
        if missing:
            raise ValueError(f"missing evidence: {sorted(missing)}")
        self.memories[memory.id] = memory

    def link_memory(self, source_id: str, relation: str, target_id: str) -> None:
        if source_id not in self.memories or target_id not in self.memories:
            raise KeyError("both memory endpoints must exist")
        self.memories[source_id].relations.append((relation, target_id))

    def retrieve(self, query: str, *, as_of: datetime | None = None) -> list[MemoryRecord]:
        """Deterministic baseline retrieval; semantic retrieval is a later adapter."""
        terms = {term.lower() for term in query.split() if term.strip()}
        candidates: list[MemoryRecord] = []
        for memory in self.memories.values():
            if memory.status != "active":
                continue
            if as_of is not None:
                if memory.valid_from and as_of < memory.valid_from:
                    continue
                if memory.valid_to and as_of >= memory.valid_to:
                    continue
            haystack = f"{memory.content} {' '.join(memory.evidence_ids)}".lower()
            if terms & set(haystack.split()):
                candidates.append(memory)
        return sorted(candidates, key=lambda item: (item.confidence, item.created_at), reverse=True)

    def find_conflicts(self, memory_id: str) -> list[MemoryRecord]:
        memory = self.memories[memory_id]
        targets = {
            target for relation, target in memory.relations if relation == "contradicts"
        }
        return [self.memories[target] for target in targets]

    def propose_delta(self, delta: KnowledgeDelta) -> None:
        if delta.id in self.deltas:
            raise ValueError(f"delta already exists: {delta.id}")
        self.deltas[delta.id] = delta

    def validate_delta(self, delta_id: str) -> tuple[bool, list[str]]:
        delta = self.deltas[delta_id]
        errors: list[str] = []
        if delta.operation not in {"ADD", "UPDATE", "SUPERSEDE", "REFUTE", "QUALIFY"}:
            errors.append("invalid operation")
        if not delta.evidence_ids:
            errors.append("institutional-memory changes require evidence")
        missing = set(delta.evidence_ids) - self.evidence.keys()
        if missing:
            errors.append(f"missing evidence: {sorted(missing)}")
        if delta.operation == "ADD" and delta.entity_id in self.memories:
            errors.append("ADD cannot replace an existing entity")
        return not errors, errors

    def commit_delta(self, delta_id: str) -> None:
        valid, errors = self.validate_delta(delta_id)
        if not valid:
            raise ValueError("delta rejected: " + "; ".join(errors))
        # The reference engine records validated deltas. Entity mutation is
        # deliberately explicit so policy layers can be inserted later.

    def reconstruct_as_of(self, as_of: datetime) -> list[MemoryRecord]:
        return [
            memory
            for memory in self.memories.values()
            if memory.status == "active"
            and (memory.valid_from is None or memory.valid_from <= as_of)
            and (memory.valid_to is None or as_of < memory.valid_to)
        ]
