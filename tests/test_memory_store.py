from datetime import datetime, timezone

import pytest

from algox.memory.store import Evidence, InMemoryStore, KnowledgeDelta, MemoryRecord


def test_memory_requires_existing_evidence():
    store = InMemoryStore()
    with pytest.raises(ValueError, match="missing evidence"):
        store.add_memory(
            MemoryRecord(
                id="M-1",
                memory_type="semantic",
                content="event driven order lifecycle",
                created_at=datetime.now(timezone.utc),
                evidence_ids=["E-1"],
            )
        )


def test_validated_delta_requires_evidence():
    store = InMemoryStore()
    delta = KnowledgeDelta(
        id="D-1",
        operation="ADD",
        entity_type="Claim",
        entity_id="C-1",
        evidence_ids=("E-1",),
        reason="reproduced by experiment",
        confidence="high",
    )
    store.propose_delta(delta)
    ok, errors = store.validate_delta("D-1")
    assert not ok
    assert "missing evidence" in errors[0]


def test_temporal_reconstruction():
    store = InMemoryStore()
    store.add_evidence(Evidence("E-1", "S-1", "doc:p1", datetime(2026, 1, 1, tzinfo=timezone.utc)))
    store.add_memory(
        MemoryRecord(
            id="M-1",
            memory_type="semantic",
            content="broker API version one",
            created_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
            valid_from=datetime(2026, 1, 1, tzinfo=timezone.utc),
            valid_to=datetime(2026, 6, 1, tzinfo=timezone.utc),
            evidence_ids=["E-1"],
        )
    )
    assert len(store.reconstruct_as_of(datetime(2026, 3, 1, tzinfo=timezone.utc))) == 1
    assert len(store.reconstruct_as_of(datetime(2026, 7, 1, tzinfo=timezone.utc))) == 0


def test_relationships_are_explicit():
    store = InMemoryStore()
    evidence = Evidence("E-1", "S-1", "doc:p1", datetime(2026, 1, 1, tzinfo=timezone.utc))
    store.add_evidence(evidence)
    for mid in ("M-1", "M-2"):
        store.add_memory(MemoryRecord(mid, "semantic", mid, evidence.observed_at, evidence_ids=[evidence.id]))
    store.link_memory("M-1", "contradicts", "M-2")
    assert [m.id for m in store.find_conflicts("M-1")] == ["M-2"]
