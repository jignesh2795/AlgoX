"""Append-only audit events for institutional knowledge governance."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


EVENT_TYPES = {
    "PROPOSED",
    "REVIEWED",
    "APPROVED",
    "REJECTED",
    "SUPERSEDED",
    "REFUTED",
    "QUALIFIED",
}


@dataclass(frozen=True)
class GovernanceEvent:
    event_id: str
    event_type: str
    entity_id: str
    actor: str
    occurred_at: datetime
    evidence_ids: tuple[str, ...] = ()
    reason: str = ""
    previous_state_hash: str | None = None

    def __post_init__(self) -> None:
        if self.event_type not in EVENT_TYPES:
            raise ValueError(f"unsupported governance event type: {self.event_type}")
        if not self.event_id.strip() or not self.entity_id.strip() or not self.actor.strip():
            raise ValueError("event_id, entity_id, and actor are required")


class AuditLog:
    """In-memory append-only event log; persistence is a future adapter concern."""

    def __init__(self) -> None:
        self._events: tuple[GovernanceEvent, ...] = ()

    def append(self, event: GovernanceEvent) -> None:
        if any(existing.event_id == event.event_id for existing in self._events):
            raise ValueError(f"audit event already exists: {event.event_id}")
        self._events = (*self._events, event)

    def events(self, entity_id: str | None = None) -> tuple[GovernanceEvent, ...]:
        if entity_id is None:
            return self._events
        return tuple(event for event in self._events if event.entity_id == entity_id)

    def history(self, entity_id: str) -> tuple[GovernanceEvent, ...]:
        return self.events(entity_id)
