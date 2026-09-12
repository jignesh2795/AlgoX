"""Policy gate for committing model-proposed institutional knowledge."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .chain_validation import validate_decision_chain
from .entities import ResearchEntity, ResearchEntityStore
from .store import Evidence, InMemoryStore, KnowledgeDelta


@dataclass(frozen=True)
class CommitReview:
    delta_id: str
    approved: bool
    errors: tuple[str, ...]


class KnowledgeGovernance:
    """Validate proposed knowledge before it becomes durable institutional state."""

    def __init__(self, entities: ResearchEntityStore, evidence: InMemoryStore) -> None:
        self.entities = entities
        self.evidence = evidence

    def review_delta(self, delta: KnowledgeDelta) -> CommitReview:
        errors: list[str] = []
        if delta.operation not in {"ADD", "UPDATE", "SUPERSEDE", "REFUTE", "QUALIFY"}:
            errors.append("invalid operation")
        if not delta.evidence_ids:
            errors.append("durable knowledge requires evidence")
        errors.extend(
            f"missing evidence: {eid}"
            for eid in delta.evidence_ids
            if eid not in self.evidence.evidence
        )
        if delta.operation == "ADD" and delta.entity_id in self.entities.entities:
            errors.append("ADD cannot replace an existing entity")
        return CommitReview(delta.id, not errors, tuple(sorted(set(errors))))

    def commit_entity(self, entity: ResearchEntity, *, approved_by: str) -> None:
        """Explicitly commit an already-reviewed entity.

        `approved_by` is required so automated extraction cannot silently become
        institutional truth. The reference implementation records the entity;
        production adapters should persist the approval event separately.
        """
        if not approved_by.strip():
            raise ValueError("approved_by is required")
        missing = [eid for eid in entity.evidence_ids if eid not in self.evidence.evidence]
        if missing:
            raise ValueError(f"missing evidence: {missing}")
        self.entities.add(entity)

    def validate_historical_evidence(self, entity: ResearchEntity, as_of: datetime) -> list[str]:
        return [
            eid
            for eid in entity.evidence_ids
            if eid in self.evidence.evidence and self.evidence.evidence[eid].observed_at > as_of
        ]
