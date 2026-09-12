"""Closed-loop bridge from agent experience to governed memory proposals."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .agent_trace import AgentTrace
from .consolidation import ConsolidationGovernor, ConsolidationProposal, Experience
from .evaluation import EvaluationResult, evaluate_trace


@dataclass(frozen=True)
class LearningLoopResult:
    evaluation: EvaluationResult
    proposal: ConsolidationProposal | None


def process_trace(
    trace: AgentTrace,
    *,
    lesson: str,
    reusable: bool,
    governor: ConsolidationGovernor | None = None,
) -> LearningLoopResult:
    """Evaluate a completed trace and, only when eligible, propose learning."""
    evaluation = evaluate_trace(trace)
    if not evaluation.passed:
        return LearningLoopResult(evaluation=evaluation, proposal=None)

    if trace.ended_at is None or trace.outcome is None:
        raise ValueError("a passed trace must have an outcome and end time")

    experience = Experience(
        id=f"EX-{trace.id}",
        trace_id=trace.id,
        lesson=lesson,
        evidence_ids=tuple(sorted(trace.evidence_ids())),
        outcome=trace.outcome,
        created_at=trace.ended_at,
        verified=trace.verified,
        reusable=reusable,
    )
    proposal = (governor or ConsolidationGovernor()).propose(experience)
    return LearningLoopResult(evaluation=evaluation, proposal=proposal)
