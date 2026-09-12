from datetime import datetime, timezone

from algox.memory.persistence import SQLiteMemoryStore
from algox.memory.store import Evidence, MemoryRecord


def _fixture(path):
    store = SQLiteMemoryStore(path)
    evidence = Evidence(
        id="E-PERSIST-001",
        source_id="SRC-001",
        locator="fixture://persistence",
        observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    store.add_evidence(evidence)
    store.add_memory(
        MemoryRecord(
            id="M-PERSIST-001",
            memory_type="semantic",
            content="persistence preserves provenance",
            created_at=datetime(2026, 1, 2, tzinfo=timezone.utc),
            confidence="high",
            evidence_ids=[evidence.id],
        )
    )
    return store


def test_sqlite_round_trip(tmp_path):
    db_path = tmp_path / "memory.sqlite3"
    store = _fixture(db_path)
    store.close()

    reopened = SQLiteMemoryStore(db_path)
    memory = reopened.get_memory("M-PERSIST-001")
    assert memory.content == "persistence preserves provenance"
    assert memory.evidence_ids == ["E-PERSIST-001"]
    reopened.close()


def test_temporal_reconstruction_survives_restart(tmp_path):
    db_path = tmp_path / "memory.sqlite3"
    store = SQLiteMemoryStore(db_path)
    evidence = Evidence(
        id="E-PERSIST-002",
        source_id="SRC-002",
        locator="fixture://temporal",
        observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    store.add_evidence(evidence)
    store.add_memory(
        MemoryRecord(
            id="M-PERSIST-002",
            memory_type="semantic",
            content="temporally valid",
            created_at=datetime(2026, 1, 2, tzinfo=timezone.utc),
            evidence_ids=[evidence.id],
            valid_from=datetime(2026, 2, 1, tzinfo=timezone.utc),
            valid_to=datetime(2026, 3, 1, tzinfo=timezone.utc),
        )
    )
    store.close()

    reopened = SQLiteMemoryStore(db_path)
    before = datetime(2026, 1, 31, tzinfo=timezone.utc)
    during = datetime(2026, 2, 15, tzinfo=timezone.utc)
    assert reopened.reconstruct_as_of(before) == []
    assert [m.id for m in reopened.reconstruct_as_of(during)] == ["M-PERSIST-002"]
    reopened.close()


def test_persisted_relations_round_trip(tmp_path):
    db_path = tmp_path / "memory.sqlite3"
    store = SQLiteMemoryStore(db_path)
    evidence = Evidence(
        id="E-PERSIST-003",
        source_id="SRC-003",
        locator="fixture://relations",
        observed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    store.add_evidence(evidence)
    store.add_memory(
        MemoryRecord(
            id="M-PERSIST-003-A",
            memory_type="finding",
            content="candidate approach",
            created_at=datetime(2026, 1, 2, tzinfo=timezone.utc),
            evidence_ids=[evidence.id],
        )
    )
    store.add_memory(
        MemoryRecord(
            id="M-PERSIST-003-B",
            memory_type="finding",
            content="contradicting approach",
            created_at=datetime(2026, 1, 3, tzinfo=timezone.utc),
            evidence_ids=[evidence.id],
        )
    )
    store.link_memory(
        "M-PERSIST-003-A", "contradicts", "M-PERSIST-003-B"
    )
    store.close()

    reopened = SQLiteMemoryStore(db_path)
    memory = reopened.get_memory("M-PERSIST-003-A")
    assert memory.relations == [("contradicts", "M-PERSIST-003-B")]
    reopened.close()
