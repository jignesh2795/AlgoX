"""Evaluation gate for agent traces.

A completed trace is not automatically trustworthy. This module provides a
small deterministic gate that can later be replaced by richer evaluators.
"""

from __future__ import annotations

from dataclasses import dataclass

from .agent_trace import AgentTrace


@dataclass(frozen=True)
class EvaluationResult:
    trace_id: str
    passed: bool
    score: float
    reasons: tuple[str, ...]


def evaluate_trace(trace: AgentTrace) -> EvaluationResult:
    reasons: list[str] = []
    if trace.status != "completed":
        reasons.append("trace is not completed")
    if not trace.observations:
        reasons.append("trace has no observations")
    if not trace.verifications:
        reasons.append("trace has no independent verification")
    elif not trace.verified:
        reasons.append("at least one verification failed")

    total = 3
    satisfied = total - min(len(reasons), total)
    score = satisfied / total
    return EvaluationResult(
        trace_id=trace.id,
        passed=not reasons,
        score=score,
        reasons=tuple(reasons),
    )
