from datetime import datetime, timedelta, timezone

from algox.memory.agent_trace import AgentTrace, Observation, ToolCall, Verification
from algox.memory.evaluation import evaluate_trace


def test_trace_requires_independent_verification():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    trace = AgentTrace(id="AR-1", task="research", started_at=start)
    trace.add_tool_call(
        ToolCall(
            id="TC-1",
            tool="search",
            arguments={"q": "claim"},
            started_at=start,
            finished_at=start + timedelta(seconds=1),
            success=True,
        )
    )
    trace.add_observation(
        Observation(id="OBS-1", content="claim", observed_at=start, evidence_ids=("E-1",))
    )
    trace.finish(outcome="candidate", ended_at=start + timedelta(seconds=2))

    result = evaluate_trace(trace)
    assert not result.passed
    assert "trace has no independent verification" in result.reasons


def test_verified_trace_passes():
    start = datetime(2026, 1, 1, tzinfo=timezone.utc)
    trace = AgentTrace(id="AR-2", task="research", started_at=start)
    trace.add_observation(
        Observation(id="OBS-2", content="verified fact", observed_at=start, evidence_ids=("E-2",))
    )
    trace.add_verification(
        Verification(
            id="V-1",
            method="independent-check",
            passed=True,
            checked_at=start + timedelta(seconds=1),
            evidence_ids=("E-2",),
        )
    )
    trace.finish(outcome="accepted", ended_at=start + timedelta(seconds=2))

    result = evaluate_trace(trace)
    assert result.passed
    assert result.score == 1.0
