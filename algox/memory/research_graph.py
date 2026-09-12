"""Validated institutional research graph over first-class research entities."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .entities import ResearchEdge, ResearchEntity, ResearchEntityStore
from .store import Evidence, InMemoryStore


@dataclass(frozen=True)
class ResearchGraphNode:
    entity: ResearchEntity
    evidence: tuple[Evidence, ...]


@dataclass(frozen=True)
class ResearchPath:
    node_ids: tuple[str, ...]
    edge_relations: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    missing_evidence: tuple[str, ...] = ()


class ValidatedResearchGraph:
    """Combines typed entities with the authoritative evidence registry."""

    def __init__(self, entities: ResearchEntityStore, evidence: InMemoryStore) -> None:
        self.entities = entities
        self.evidence = evidence

    def validate(self) -> list[str]:
        errors: list[str] = []
        for entity in self.entities.entities.values():
            for evidence_id in entity.evidence_ids:
                if evidence_id not in self.evidence.evidence:
                    errors.append(f"{entity.id}: missing evidence {evidence_id}")
        for edge in self.entities.edges:
            if edge.source_id not in self.entities.entities:
                errors.append(f"edge: missing source {edge.source_id}")
            if edge.target_id not in self.entities.entities:
                errors.append(f"edge: missing target {edge.target_id}")
        return errors

    def path(self, start_id: str, target_id: str, *, max_depth: int = 8) -> ResearchPath | None:
        if start_id not in self.entities.entities or target_id not in self.entities.entities:
            raise KeyError("both path endpoints must exist")
        queue: list[tuple[str, tuple[str, ...], tuple[str, ...]]] = [(start_id, (start_id,), ())]
        seen = {start_id}
        while queue:
            current, nodes, relations = queue.pop(0)
            if current == target_id:
                evidence_ids = tuple(dict.fromkeys(
                    eid for node_id in nodes for eid in self.entities.entities[node_id].evidence_ids
                ))
                missing = tuple(eid for eid in evidence_ids if eid not in self.evidence.evidence)
                return ResearchPath(nodes, relations, evidence_ids, missing)
            if len(relations) >= max_depth:
                continue
            for edge in self.entities.edges:
                if edge.source_id != current or edge.target_id in seen:
                    continue
                seen.add(edge.target_id)
                queue.append((edge.target_id, nodes + (edge.target_id,), relations + (edge.relation,)))
        return None

    def path_is_valid_as_of(self, path: ResearchPath, as_of: datetime) -> bool:
        for node_id in path.node_ids:
            entity = self.entities.entities[node_id]
            for evidence_id in entity.evidence_ids:
                evidence = self.evidence.evidence.get(evidence_id)
                if evidence is not None and evidence.observed_at > as_of:
                    return False
        return True
