import json
from datetime import datetime, timezone
from pathlib import Path

from algox.memory.store import Evidence, InMemoryStore, MemoryRecord


DATASET = Path(__file__).parents[1] / "research" / "experiments" / "memory-benchmark-dataset.json"


def load_dataset():
    return json.loads(DATASET.read_text())


def build_store():
    data = load_dataset()
    store = InMemoryStore()
    for item in data["records"]:
        store.add_evidence(
            Evidence(
                item["id"],
                item["source_id"],
                item["locator"],
                datetime.fromisoformat(item["observed_at"].replace("Z", "+00:00")),
                item["maturity"],
            )
        )
    for item in data["memories"]:
        store.add_memory(
            MemoryRecord(
                id=item["id"],
                memory_type=item["memory_type"],
                content=item["content"],
                created_at=datetime.fromisoformat(item["created_at"].replace("Z", "+00:00")),
                confidence=item["confidence"],
                valid_from=datetime.fromisoformat(item["valid_from"].replace("Z", "+00:00")) if item.get("valid_from") else None,
                valid_to=datetime.fromisoformat(item["valid_to"].replace("Z", "+00:00")) if item.get("valid_to") else None,
                evidence_ids=item["evidence_ids"],
            )
        )
    for relation in data["relations"]:
        store.link_memory(relation["source"], relation["relation"], relation["target"])
    return store


def test_benchmark_dataset_loads():
    store = build_store()
    assert len(store.evidence) == 6
    assert len(store.memories) == 6


def test_temporal_workload():
    store = build_store()
    before = datetime(2026, 3, 1, tzinfo=timezone.utc)
    after = datetime(2026, 8, 1, tzinfo=timezone.utc)
    assert {m.id for m in store.reconstruct_as_of(before)} == {"M-001", "M-003", "M-004", "M-005", "M-006"}
    assert "M-002" in {m.id for m in store.reconstruct_as_of(after)}
    assert "M-001" not in {m.id for m in store.reconstruct_as_of(after)}


def test_contradiction_workload():
    store = build_store()
    assert [m.id for m in store.find_conflicts("M-004")] == ["M-005"]


def test_provenance_workload():
    store = build_store()
    memory = store.memories["M-003"]
    assert set(memory.evidence_ids) == {"E-001", "E-003"}
    assert all(eid in store.evidence for eid in memory.evidence_ids)
