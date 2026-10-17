from datetime import datetime, timezone

from algox.memory.consolidation import ConsolidationGovernor, Experience


def experience(**overrides):
    values = {
        "id": "EXP-1",
        "trace_id": "TRACE-1",
        "lesson": "Keep venue-specific semantics outside the generic adapter.",
        "evidence_ids": ("E-1",),
        "outcome": "success",
        "created_at": datetime.now(timezone.utc),
        "verified": True,
        "reusable": True,
    }
    values.update(overrides)
    return Experience(**values)


def test_verified_reusable_experience_becomes_proposal():
    proposal = ConsolidationGovernor().propose(experience())
    assert proposal is not None
    assert proposal.memory_type == "procedural"
    assert proposal.evidence_ids == ("E-1",)


def test_unverified_experience_is_not_consolidated():
    assert ConsolidationGovernor().propose(experience(verified=False)) is None


def test_non_reusable_experience_is_not_consolidated():
    assert ConsolidationGovernor().propose(experience(reusable=False)) is None


def test_experience_without_evidence_is_not_consolidated():
    assert ConsolidationGovernor().propose(experience(evidence_ids=())) is None
