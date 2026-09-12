"""Structured agent-run traces for evidence-aware research.

The trace layer records what an agent did and what it observed without making
those observations institutional truth. Evaluation and consolidation remain
separate governance steps.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class ToolCall:
    id: str
    tool: str
    arguments: dict[str, Any]
    started_at: datetime
    finished_at: datetime | None = None
    success: bool | None = None
    side_effect: str = "none"


@dataclass(frozen=True)
class Observation:
    id: str
    content: str
    observed_at: datetime
    evidence_ids: tuple[str, ...] = ()
    source: str | None = None


@dataclass(frozen=True)
class Verification:
    id: str
    method: str
    passed: bool
    checked_at: datetime
    evidence_ids: tuple[str, ...] = ()
    details: str = ""


@dataclass
class AgentTrace:
    id: str
    task: str
    started_at: datetime
    ended_at: datetime | None = None
    tool_calls: list[ToolCall] = field(default_factory=list)
    observations: list[Observation] = field(default_factory=list)
    verifications: list[Verification] = field(default_factory=list)
    outcome: str | None = None
    status: str = "running"

    def add_tool_call(self, call: ToolCall) -> None:
        if any(item.id == call.id for item in self.tool_calls):
            raise ValueError(f"duplicate tool call: {call.id}")
        self.tool_calls.append(call)

    def add_observation(self, observation: Observation) -> None:
        if any(item.id == observation.id for item in self.observations):
            raise ValueError(f"duplicate observation: {observation.id}")
        self.observations.append(observation)

    def add_verification(self, verification: Verification) -> None:
        if any(item.id == verification.id for item in self.verifications):
            raise ValueError(f"duplicate verification: {verification.id}")
        self.verifications.append(verification)

    def finish(self, *, outcome: str, ended_at: datetime) -> None:
        if self.status != "running":
            raise ValueError("trace is already finished")
        if ended_at < self.started_at:
            raise ValueError("ended_at cannot precede started_at")
        self.outcome = outcome
        self.ended_at = ended_at
        self.status = "completed"

    @property
    def verified(self) -> bool:
        return bool(self.verifications) and all(item.passed for item in self.verifications)

    def evidence_ids(self) -> set[str]:
        result: set[str] = set()
        for observation in self.observations:
            result.update(observation.evidence_ids)
        for verification in self.verifications:
            result.update(verification.evidence_ids)
        return result
