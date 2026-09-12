"""Validation rules for auditable research decision chains."""

from __future__ import annotations

from .entities import ResearchEntityStore
from .store import InMemoryStore


FORWARD_REQUIRED = {
    "Claim": {"tested_by"},
    "Experiment": {"produced"},
    "Result": {"supports"},
    "Finding": {"informs"},
    "Decision": {"affects"},
}


def validate_decision_chain(entities: ResearchEntityStore, evidence: InMemoryStore, decision_id: str) -> list[str]:
    """Validate the causal Claim→Experiment→Result→Finding→Decision→Capability chain."""
    errors: list[str] = []
    decision = entities.entities.get(decision_id)
    if decision is None:
        return [f"missing decision: {decision_id}"]
    if decision.entity_type != "Decision":
        return [f"not a decision: {decision_id}"]

    for entity in entities.entities.values():
        for evidence_id in entity.evidence_ids:
            if evidence_id not in evidence.evidence:
                errors.append(f"{entity.id}: missing evidence {evidence_id}")

    # Decision tracing runs backward through causal edges; each discovered
    # node is then checked for its required forward edge.
    incoming_required = {
        "Decision": {"informs"},
        "Finding": {"supports"},
        "Result": {"produced"},
        "Experiment": {"tested_by"},
    }
    queue = [decision_id]
    visited: set[str] = set()
    while queue:
        current_id = queue.pop(0)
        if current_id in visited:
            continue
        visited.add(current_id)
        current = entities.entities[current_id]
        outgoing = [edge for edge in entities.edges if edge.source_id == current_id]
        for relation in FORWARD_REQUIRED.get(current.entity_type, set()):
            if not any(edge.relation == relation for edge in outgoing):
                errors.append(f"{current_id}: missing required relation {relation}")
        incoming = [edge for edge in entities.edges if edge.target_id == current_id]
        for relation in incoming_required.get(current.entity_type, set()):
            matches = [edge for edge in incoming if edge.relation == relation]
            if not matches:
                errors.append(f"{current_id}: missing required incoming relation {relation}")
            queue.extend(edge.source_id for edge in matches)

    return sorted(set(errors))
