"""First-class institutional research entities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


ENTITY_TYPES = {"Claim", "Finding", "Experiment", "Result", "Decision", "Capability"}


@dataclass(frozen=True)
class ResearchEntity:
    id: str
    entity_type: str
    content: str
    evidence_ids: tuple[str, ...] = ()
    valid_from: datetime | None = None
    valid_to: datetime | None = None
    status: str = "active"

    def __post_init__(self) -> None:
        if self.entity_type not in ENTITY_TYPES:
            raise ValueError(f"unsupported research entity type: {self.entity_type}")
        if self.valid_from and self.valid_to and self.valid_from >= self.valid_to:
            raise ValueError("valid_from must precede valid_to")
        if self.status not in {"active", "superseded", "disputed", "retracted"}:
            raise ValueError(f"unsupported research entity status: {self.status}")

    def is_valid_at(self, at: datetime) -> bool:
        return (
            self.status == "active"
            and (self.valid_from is None or self.valid_from <= at)
            and (self.valid_to is None or at < self.valid_to)
        )


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

    def valid_entities_at(self, at: datetime) -> list[ResearchEntity]:
        return [entity for entity in self.entities.values() if entity.is_valid_at(at)]
