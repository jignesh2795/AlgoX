"""Validation rules for auditable research decision chains."""

from __future__ import annotations

from .entities import ResearchEntityStore
from .store import InMemoryStore


REQUIRED_CHAIN = {
    "Claim": {"tested_by"},
    "Experiment": {"produced"},
    "Result": {"supports"},
    "Finding": {"informs"},
    "Decision": {"affects"},
}


def validate_decision_chain(
    entities: ResearchEntityStore, evidence: InMemoryStore, decision_id: str
) -> list[str]:
    """Return deterministic errors; an empty list means the chain is admissible."""
    errors: list[str] = []
    decision = entities.entities.get(decision_id)
    if decision is None:
        return [f"missing decision: {decision_id}"]
    if decision.entity_type != "Decision":
        return [f"not a decision: {decision_id}"]

    for evidence_id in decision.evidence_ids:
        if evidence_id not in evidence.evidence:
            errors.append(f"{decision_id}: missing evidence {evidence_id}")

    queue = [decision_id]
    visited = set()
    while queue:
        current_id = queue.pop(0)
        if current_id in visited:
            continue
        visited.add(current_id)
        current = entities.entities[current_id]
        required = REQUIRED_CHAIN.get(current.entity_type, set())
        outgoing = [edge for edge in entities.edges if edge.source_id == current_id]
        for relation in required:
            matches = [edge for edge in outgoing if edge.relation == relation]
            if not matches:
                errors.append(f"{current_id}: missing required relation {relation}")
            queue.extend(edge.target_id for edge in matches)

        for evidence_id in current.evidence_ids:
            if evidence_id not in evidence.evidence:
                errors.append(f"{current_id}: missing evidence {evidence_id}")

    return sorted(set(errors))
