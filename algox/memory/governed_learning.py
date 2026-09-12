"""Auditable bridge from learning proposals to governance decisions.

The service intentionally stops at the governance boundary. A proposal can be
recorded and reviewed, but no model output is silently promoted to institutional
truth.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from .audit import AuditLog, GovernanceEvent
from .consolidation import ConsolidationProposal
from .governance import CommitReview, KnowledgeGovernance
from .store import KnowledgeDelta


@dataclass(frozen=True)
class GovernanceOutcome:
    proposal_id: str
    delta: KnowledgeDelta
    review: CommitReview
    audit_event_ids: tuple[str, ...]


def govern_proposal(
    proposal: ConsolidationProposal,
    governance: KnowledgeGovernance,
    audit: AuditLog,
    *,
    actor: str = "learning-loop",
    reviewed_at: datetime | None = None,
) -> GovernanceOutcome:
    """Convert a consolidation proposal into a reviewed, auditable delta.

    This function does not mutate canonical research entities. Even an approved
    ADD is only recorded as reviewed here; explicit entity commitment remains a
    separate operation requiring an approval identity.
    """
    if not actor.strip():
        raise ValueError("actor is required")

    occurred_at = reviewed_at or datetime.now(timezone.utc)
    delta = KnowledgeDelta(
        id=f"KD-{proposal.id}",
        operation="ADD",
        entity_type="Finding",
        entity_id=proposal.id,
        evidence_ids=proposal.evidence_ids,
        reason=proposal.reason,
        confidence=proposal.confidence,
    )

    governance.evidence.propose_delta(delta)
    review = governance.review_delta(delta)

    event_type = "APPROVED" if review.approved else "REJECTED"
    if review.status == "review_required":
        event_type = "REVIEWED"

    events = [
        GovernanceEvent(
            event_id=f"AUD-{proposal.id}-PROPOSED",
            event_type="PROPOSED",
            entity_id=proposal.id,
            actor=actor,
            occurred_at=occurred_at,
            evidence_ids=proposal.evidence_ids,
            reason=proposal.reason,
        ),
        GovernanceEvent(
            event_id=f"AUD-{proposal.id}-{event_type}",
            event_type=event_type,
            entity_id=proposal.id,
            actor=actor,
            occurred_at=occurred_at,
            evidence_ids=proposal.evidence_ids,
            reason="; ".join(review.errors) if review.errors else review.status,
        ),
    ]
    for event in events:
        audit.append(event)

    return GovernanceOutcome(
        proposal_id=proposal.id,
        delta=delta,
        review=review,
        audit_event_ids=tuple(event.event_id for event in events),
    )
