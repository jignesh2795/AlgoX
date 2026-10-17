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

INCOMING_REQUIRED = {
    "Decision": {"informs"},
    "Finding": {"supports"},
    "Result": {"produced"},
    "Experiment": {"tested_by"},
}


def validate_decision_chain(entities: ResearchEntityStore, evidence: InMemoryStore, decision_id: str) -> list[str]:
    """Validate Claim→Experiment→Result→Finding→Decision→Capability.

    Decision reconstruction is intentionally backward: a decision must be
    explainable by a finding, result, experiment, and claim. The terminal
    capability is then checked through the decision's forward ``affects`` edge.
    """
    errors: list[str] = []
    decision = entities.entities.get(decision_id)
    if decision is None:
        return [f"missing decision: {decision_id}"]
    if decision.entity_type != "Decision":
        return [f"not a decision: {decision_id}"]

    queue = [decision_id]
    visited: set[str] = set()
    while queue:
        current_id = queue.pop(0)
        if current_id in visited:
            continue
        current = entities.entities.get(current_id)
        if current is None:
            errors.append(f"missing entity: {current_id}")
            continue
        visited.add(current_id)

        outgoing = [edge for edge in entities.edges if edge.source_id == current_id]
        for relation in FORWARD_REQUIRED.get(current.entity_type, set()):
            matches = [edge for edge in outgoing if edge.relation == relation]
            if not matches:
                errors.append(f"{current_id}: missing required relation {relation}")
            elif relation == "affects":
                for edge in matches:
                    target = entities.entities.get(edge.target_id)
                    if target is None:
                        errors.append(f"{current_id}: missing target entity {edge.target_id}")
                    elif target.entity_type != "Capability":
                        errors.append(f"{current_id}: affects must target Capability")

        incoming = [edge for edge in entities.edges if edge.target_id == current_id]
        for relation in INCOMING_REQUIRED.get(current.entity_type, set()):
            matches = [edge for edge in incoming if edge.relation == relation]
            if not matches:
                errors.append(f"{current_id}: missing required incoming relation {relation}")
            queue.extend(edge.source_id for edge in matches)

        if current.entity_type == "Claim":
            if not current.evidence_ids:
                errors.append(f"{current_id}: claim requires evidence")
            for evidence_id in current.evidence_ids:
                if evidence_id not in evidence.evidence:
                    errors.append(f"{current_id}: missing evidence {evidence_id}")

    return sorted(set(errors))
