"""CLI entry point for memory-engine benchmark workloads.

Usage from the repository root:
    python experiments/memory_benchmark.py
"""

import json
from datetime import datetime
from pathlib import Path

from algox.memory import Evidence, InMemoryStore, MemoryRecord, benchmark_decision_chain, benchmark_governance, benchmark_retrieval
from algox.memory.entities import ResearchEntity, ResearchEntityStore


ROOT = Path(__file__).parents[1]
DATASET = ROOT / "research" / "experiments" / "memory-benchmark-dataset.json"
CHAIN_FIXTURE = ROOT / "research" / "experiments" / "memory-chain-fixture.json"


def load_store() -> InMemoryStore:
    data = json.loads(DATASET.read_text(encoding="utf-8"))
    store = InMemoryStore()
    for item in data["records"]:
        store.add_evidence(Evidence(
            item["id"], item["source_id"], item["locator"],
            datetime.fromisoformat(item["observed_at"].replace("Z", "+00:00")),
            item["maturity"],
        ))
    for item in data["memories"]:
        store.add_memory(MemoryRecord(
            id=item["id"], memory_type=item["memory_type"], content=item["content"],
            created_at=datetime.fromisoformat(item["created_at"].replace("Z", "+00:00")),
            confidence=item["confidence"],
            valid_from=datetime.fromisoformat(item["valid_from"].replace("Z", "+00:00")) if item.get("valid_from") else None,
            valid_to=datetime.fromisoformat(item["valid_to"].replace("Z", "+00:00")) if item.get("valid_to") else None,
            evidence_ids=item["evidence_ids"],
        ))
    for relation in data["relations"]:
        store.link_memory(relation["source"], relation["relation"], relation["target"])
    return store


def load_chain(evidence: InMemoryStore) -> ResearchEntityStore:
    """Build the typed research graph from the canonical chain fixture."""
    data = json.loads(CHAIN_FIXTURE.read_text(encoding="utf-8"))
    entities = ResearchEntityStore()
    for item in data["entities"]:
        evidence_ids = ()
        if item["id"] == "C-001":
            evidence_ids = ("E-004",)
        entities.add(ResearchEntity(item["id"], item["type"], item["content"], evidence_ids))
    for source, relation, target in data["edges"]:
        if relation in {"tested_by", "produced", "supports", "informs", "affects"}:
            entities.link(source, relation, target)
    return entities


def main() -> int:
    store = load_store()
    results = benchmark_retrieval(store)

    entities = load_chain(store)
    results.extend(benchmark_decision_chain(entities, store, "D-001"))
    results.extend(benchmark_governance(entities, store))

    print("EXP-MEM-0001")
    failed = False
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        failed |= not result.passed
        print(f"{status}\t{result.workload}\t{result.metric}={result.value:.6f}{result.unit}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
