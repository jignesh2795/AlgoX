from datetime import datetime, timedelta, timezone

from algox.memory.agent_trace import AgentTrace, Observation, Verification
from algox.memory.learning_loop import process_trace


def completed_trace(*, verification_passed=True):
    now = datetime.now(timezone.utc)
    trace = AgentTrace(id="TRACE-1", task="research", started_at=now)
    trace.add_observation(
        Observation(id="OBS-1", content="found evidence", observed_at=now, evidence_ids=("E-1",))
    )
    trace.add_verification(
        Verification(
            id="VER-1",
            method="independent test",
            passed=verification_passed,
            checked_at=now + timedelta(seconds=1),
            evidence_ids=("E-1",),
        )
    )
    trace.finish(outcome="success", ended_at=now + timedelta(seconds=2))
    return trace


def test_learning_loop_produces_proposal_after_verification():
    result = process_trace(
        completed_trace(),
        lesson="Preserve venue semantics.",
        reusable=True,
    )
    assert result.evaluation.passed
    assert result.proposal is not None
    assert result.proposal.evidence_ids == ("E-1",)


def test_learning_loop_does_not_consolidate_failed_verification():
    result = process_trace(
        completed_trace(verification_passed=False),
        lesson="Do not trust an unverified result.",
        reusable=True,
    )
    assert not result.evaluation.passed
    assert result.proposal is None
