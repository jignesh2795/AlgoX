"""Deterministic benchmark harness for the memory and research layers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from time import perf_counter

from .audit import AuditLog, GovernanceEvent
from .chain_validation import validate_decision_chain
from .entities import ResearchEntity, ResearchEntityStore
from .graph import MemoryGraph
from .governance import KnowledgeGovernance
from .retrieval import EvidenceRetriever
from .store import InMemoryStore, KnowledgeDelta


@dataclass(frozen=True)
class BenchmarkResult:
    workload: str
    passed: bool
    metric: str
    value: float
    unit: str


def _ratio(passed: bool) -> float:
    return 1.0 if passed else 0.0


def benchmark_retrieval(store: InMemoryStore) -> list[BenchmarkResult]:
    """Run deterministic retrieval, temporal, provenance, and graph workloads."""
    retriever = EvidenceRetriever(store)
    results: list[BenchmarkResult] = []

    start = perf_counter()
    bundle = retriever.retrieve("broker API asynchronous order", limit=10)
    elapsed_ms = (perf_counter() - start) * 1000
    found = "E-002" in bundle.supporting_evidence
    results.append(BenchmarkResult("W1 exact retrieval", found, "evidence_recall", _ratio(found), "ratio"))
    results.append(BenchmarkResult("W1 exact retrieval", True, "latency", elapsed_ms, "ms"))

    start = perf_counter()
    related = retriever.related("M-004", depth=2)
    elapsed_ms = (perf_counter() - start) * 1000
    ids = {memory.id for memory in related}
    traversal_ok = {"M-005", "M-006"}.issubset(ids)
    results.append(BenchmarkResult("W3 relationship traversal", traversal_ok, "target_recall", _ratio(traversal_ok), "ratio"))
    results.append(BenchmarkResult("W3 relationship traversal", True, "latency", elapsed_ms, "ms"))

    start = perf_counter()
    bundle = retriever.retrieve("method X", limit=10)
    elapsed_ms = (perf_counter() - start) * 1000
    contradiction_found = "E-005" in bundle.counter_evidence or "E-006" in bundle.counter_evidence
    results.append(BenchmarkResult("W4 contradiction retrieval", contradiction_found, "counter_evidence_recall", _ratio(contradiction_found), "ratio"))
    results.append(BenchmarkResult("W4 contradiction retrieval", True, "latency", elapsed_ms, "ms"))

    as_of = datetime(2026, 3, 1, tzinfo=timezone.utc)
    bundle = retriever.retrieve("broker API", as_of=as_of)
    ids = {memory.id for memory in bundle.memories}
    temporal_ok = "M-001" in ids and "M-002" not in ids
    results.append(BenchmarkResult("W5 temporal retrieval", temporal_ok, "temporal_accuracy", _ratio(temporal_ok), "ratio"))

    provenance_ok = bool(bundle.supporting_evidence) and all(eid in store.evidence for eid in bundle.supporting_evidence)
    results.append(BenchmarkResult("W6 provenance completeness", provenance_ok, "provenance_completeness", _ratio(provenance_ok), "ratio"))

    supersession_ok = _supersession_invariant(store)
    results.append(BenchmarkResult("W7 supersession", supersession_ok, "supersession_accuracy", _ratio(supersession_ok), "ratio"))

    graph = MemoryGraph(store)
    start = perf_counter()
    signature_before = graph.rebuild_signature()
    signature_after = MemoryGraph(store).rebuild_signature()
    elapsed_ms = (perf_counter() - start) * 1000
    rebuild_ok = signature_before == signature_after
    results.append(BenchmarkResult("W10 graph rebuild", rebuild_ok, "rebuild_signature_equality", _ratio(rebuild_ok), "ratio"))
    results.append(BenchmarkResult("W10 graph rebuild", True, "latency", elapsed_ms, "ms"))
    return results


def _supersession_invariant(store: InMemoryStore) -> bool:
    """Check that an active memory is not silently replaced by its successor."""
    successor_pairs = []
    for memory in store.memories.values():
        for relation, target in memory.relations:
            if relation == "superseded_by":
                successor_pairs.append((memory.id, target))
    return bool(successor_pairs) and all(
        old in store.memories and new in store.memories
        and store.memories[old].status == "superseded"
        and store.memories[new].status == "active"
        for old, new in successor_pairs
    )


def benchmark_decision_chain(entities: ResearchEntityStore, evidence: InMemoryStore, decision_id: str) -> list[BenchmarkResult]:
    """Measure auditable decision-chain reconstruction and terminal tracing."""
    start = perf_counter()
    errors = validate_decision_chain(entities, evidence, decision_id)
    elapsed_ms = (perf_counter() - start) * 1000
    chain_ok = not errors
    results = [
        BenchmarkResult("W8 decision-chain reconstruction", chain_ok, "chain_validity", _ratio(chain_ok), "ratio"),
        BenchmarkResult("W8 decision-chain reconstruction", True, "latency", elapsed_ms, "ms"),
    ]
    decision_to_capability = any(
        edge.source_id == decision_id and edge.relation == "affects"
        and entities.entities.get(edge.target_id) is not None
        and entities.entities[edge.target_id].entity_type == "Capability"
        for edge in entities.edges
    )
    results.append(BenchmarkResult("W9 experiment-to-decision tracing", chain_ok and decision_to_capability, "traceability", _ratio(chain_ok and decision_to_capability), "ratio"))
    return results


def benchmark_governance(entities: ResearchEntityStore, evidence: InMemoryStore) -> list[BenchmarkResult]:
    """Benchmark governance decisions and append-only audit reconstruction."""
    governance = KnowledgeGovernance(entities, evidence)
    audit = AuditLog()
    results: list[BenchmarkResult] = []

    valid_delta = KnowledgeDelta(
        id="BM-DELTA-001", operation="ADD", entity_type="Finding", entity_id="BM-F-001",
        evidence_ids=("E-001",), reason="benchmark governance proposal", confidence="high",
    )
    start = perf_counter()
    review = governance.review_delta(valid_delta)
    review_ms = (perf_counter() - start) * 1000
    review_ok = review.approved and review.status == "approved"
    results.append(BenchmarkResult("G1 governance review", review_ok, "approval_correctness", _ratio(review_ok), "ratio"))
    results.append(BenchmarkResult("G1 governance review", True, "latency", review_ms, "ms"))

    start = perf_counter()
    audit.append(GovernanceEvent(
        event_id="BM-EVENT-001", event_type="REVIEWED", entity_id="BM-F-001", actor="benchmark",
        occurred_at=datetime.now(timezone.utc), evidence_ids=("E-001",), reason="approved benchmark proposal",
    ))
    history = audit.history("BM-F-001")
    audit_ms = (perf_counter() - start) * 1000
    audit_ok = len(history) == 1 and history[0].event_id == "BM-EVENT-001"
    results.append(BenchmarkResult("G2 audit append", audit_ok, "append_correctness", _ratio(audit_ok), "ratio"))
    results.append(BenchmarkResult("G2 audit append", True, "latency", audit_ms, "ms"))
    return results
