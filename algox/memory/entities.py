"""First-class institutional research entities.

These entities remain storage-independent. They reference the existing memory
and evidence records rather than introducing a second source of truth.
"""

from __future__ import annotations

from dataclasses import dataclass


ENTITY_TYPES = {"Claim", "Finding", "Experiment", "Result", "Decision", "Capability"}


@dataclass(frozen=True)
class ResearchEntity:
    id: str
    entity_type: str
    content: str
    evidence_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.entity_type not in ENTITY_TYPES:
            raise ValueError(f"unsupported research entity type: {self.entity_type}")


@dataclass(frozen=True)
class ResearchEdge:
    source_id: str
    relation: str
    target_id: str


class ResearchEntityStore:
    """Authoritative registry for typed research-chain entities and edges."""

    def __init__(self) -> None:
        self.entities: dict[str, ResearchEntity] = {}
        self.edges: list[ResearchEdge] = []

    def add(self, entity: ResearchEntity) -> None:
        if entity.id in self.entities:
            raise ValueError(f"entity already exists: {entity.id}")
        self.entities[entity.id] = entity

    def link(self, source_id: str, relation: str, target_id: str) -> None:
        if source_id not in self.entities or target_id not in self.entities:
            raise KeyError("both research entity endpoints must exist")
        edge = ResearchEdge(source_id, relation, target_id)
        if edge not in self.edges:
            self.edges.append(edge)

    def neighbors(self, entity_id: str, relation: str | None = None) -> list[ResearchEntity]:
        targets = [
            edge.target_id
            for edge in self.edges
            if edge.source_id == entity_id and (relation is None or edge.relation == relation)
        ]
        return [self.entities[target] for target in targets]

    def evidence_for(self, entity_id: str) -> tuple[str, ...]:
        return self.entities[entity_id].evidence_ids
