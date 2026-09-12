"""Governed conversion of evaluated agent experience into candidate memory.

This module deliberately produces proposals rather than mutating institutional
memory. A separate governance layer must approve durable knowledge changes.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Experience:
    id: str
    trace_id: str
    lesson: str
    evidence_ids: tuple[str, ...]
    outcome: str
    created_at: datetime
    verified: bool = False
    reusable: bool = False


@dataclass(frozen=True)
class ConsolidationProposal:
    id: str
    experience_id: str
    memory_type: str
    content: str
    evidence_ids: tuple[str, ...]
    reason: str
    confidence: str


class ConsolidationGovernor:
    """Apply conservative rules before proposing durable memory."""

    def propose(self, experience: Experience) -> ConsolidationProposal | None:
        if not experience.verified:
            return None
        if not experience.evidence_ids:
            return None
        if not experience.lesson.strip():
            return None
        if not experience.reusable:
            return None

        confidence = "high" if experience.outcome == "success" else "medium"
        return ConsolidationProposal(
            id=f"CP-{experience.id}",
            experience_id=experience.id,
            memory_type="procedural",
            content=experience.lesson.strip(),
            evidence_ids=experience.evidence_ids,
            reason="verified reusable experience",
            confidence=confidence,
        )
