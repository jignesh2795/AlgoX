"""Deterministic benchmark harness for the memory engine."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from time import perf_counter

from .retrieval import EvidenceRetriever
from .store import InMemoryStore


@dataclass(frozen=True)
class BenchmarkResult:
    workload: str
    passed: bool
    metric: str
    value: float
    unit: str


def benchmark_retrieval(store: InMemoryStore) -> list[BenchmarkResult]:
    retriever = EvidenceRetriever(store)
    results: list[BenchmarkResult] = []

    start = perf_counter()
    bundle = retriever.retrieve("broker API asynchronous order", limit=10)
    elapsed_ms = (perf_counter() - start) * 1000
    results.append(BenchmarkResult("W1 exact retrieval", "E-002" in bundle.supporting_evidence, "evidence_recall", 1.0 if "E-002" in bundle.supporting_evidence else 0.0, "ratio"))
    results.append(BenchmarkResult("W1 exact retrieval", True, "latency", elapsed_ms, "ms"))

    start = perf_counter()
    related = retriever.related("M-004", depth=2)
    elapsed_ms = (perf_counter() - start) * 1000
    ids = {memory.id for memory in related}
    results.append(BenchmarkResult("W3 relationship traversal", {"M-005", "M-006"}.issubset(ids), "target_recall", 1.0 if {"M-005", "M-006"}.issubset(ids) else 0.0, "ratio"))
    results.append(BenchmarkResult("W3 relationship traversal", True, "latency", elapsed_ms, "ms"))

    start = perf_counter()
    bundle = retriever.retrieve("method X", limit=10)
    elapsed_ms = (perf_counter() - start) * 1000
    contradiction_found = "E-005" in bundle.counter_evidence or "E-006" in bundle.counter_evidence
    results.append(BenchmarkResult("W4 contradiction retrieval", contradiction_found, "counter_evidence_recall", 1.0 if contradiction_found else 0.0, "ratio"))
    results.append(BenchmarkResult("W4 contradiction retrieval", True, "latency", elapsed_ms, "ms"))

    as_of = datetime(2026, 3, 1, tzinfo=timezone.utc)
    bundle = retriever.retrieve("broker API", as_of=as_of)
    ids = {memory.id for memory in bundle.memories}
    temporal_ok = "M-001" in ids and "M-002" not in ids
    results.append(BenchmarkResult("W5 temporal retrieval", temporal_ok, "temporal_accuracy", 1.0 if temporal_ok else 0.0, "ratio"))

    provenance_ok = bool(bundle.supporting_evidence) and all(eid in store.evidence for eid in bundle.supporting_evidence)
    results.append(BenchmarkResult("W6 provenance completeness", provenance_ok, "provenance_completeness", 1.0 if provenance_ok else 0.0, "ratio"))

    return results
