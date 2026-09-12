"""Policy gate for committing model-proposed institutional knowledge."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .entities import ResearchEntity, ResearchEntityStore
from .store import Evidence, InMemoryStore, KnowledgeDelta


@dataclass(frozen=True)
class CommitReview:
    delta_id: str
    approved: bool
    errors: tuple[str, ...]
    status: str = "rejected"


class KnowledgeGovernance:
    """Validate proposed knowledge before it becomes durable institutional state."""

    def __init__(self, entities: ResearchEntityStore, evidence: InMemoryStore) -> None:
        self.entities = entities
        self.evidence = evidence

    def review_delta(self, delta: KnowledgeDelta) -> CommitReview:
        errors: list[str] = []
        review_required = False
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

        # A delta backed by evidence can still be unsafe to institutionalize
        # when it conflicts with existing knowledge. It requires an explicit
        # human/policy review rather than being silently rejected or approved.
        if not errors and delta.entity_id in self.entities.entities:
            existing = self.entities.entities[delta.entity_id]
            if existing.status == "disputed":
                review_required = True

        if errors:
            return CommitReview(delta.id, False, tuple(sorted(set(errors))), "rejected")
        if review_required:
            return CommitReview(delta.id, False, ("existing entity is disputed; explicit review required",), "review_required")
        return CommitReview(delta.id, True, (), "approved")

    def commit_entity(self, entity: ResearchEntity, *, approved_by: str) -> None:
        """Commit an already-reviewed entity with explicit approval identity."""
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
