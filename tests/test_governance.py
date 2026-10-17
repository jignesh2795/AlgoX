from datetime import datetime, timezone

import pytest

from algox.memory.entities import ResearchEntity, ResearchEntityStore
from algox.memory.governance import KnowledgeGovernance
from algox.memory.store import Evidence, InMemoryStore, KnowledgeDelta


def build_governance():
    evidence = InMemoryStore()
    evidence.add_evidence(Evidence("E-1", "S-1", "source", datetime(2026, 1, 1, tzinfo=timezone.utc)))
    return KnowledgeGovernance(ResearchEntityStore(), evidence)


def test_delta_without_evidence_is_rejected():
    gov = build_governance()
    review = gov.review_delta(KnowledgeDelta("K-1", "ADD", "Claim", "C-1", (), "model proposal"))
    assert review.approved is False
    assert review.status == "rejected"
    assert "durable knowledge requires evidence" in review.errors


def test_delta_with_known_evidence_is_approved():
    gov = build_governance()
    review = gov.review_delta(KnowledgeDelta("K-2", "ADD", "Claim", "C-2", ("E-1",), "verified source"))
    assert review.approved is True
    assert review.status == "approved"


def test_truth_changing_operations_require_explicit_review():
    gov = build_governance()
    for operation in ("REFUTE", "QUALIFY", "SUPERSEDE"):
        review = gov.review_delta(KnowledgeDelta(f"K-{operation}", operation, "Claim", f"C-{operation}", ("E-1",), "changes claim status"))
        assert review.approved is False
        assert review.status == "review_required"
        assert "truth-changing proposal requires explicit review" in review.errors[0]


def test_commit_requires_explicit_approval_identity():
    gov = build_governance()
    entity = ResearchEntity("C-3", "Claim", "claim", ("E-1",))
    with pytest.raises(ValueError):
        gov.commit_entity(entity, approved_by="")
    gov.commit_entity(entity, approved_by="human-review")
    assert "C-3" in gov.entities.entities


def test_future_evidence_is_reported_for_historical_review():
    gov = build_governance()
    entity = ResearchEntity("C-4", "Claim", "claim", ("E-1",))
    future = gov.validate_historical_evidence(entity, datetime(2025, 12, 31, tzinfo=timezone.utc))
    assert future == ["E-1"]
