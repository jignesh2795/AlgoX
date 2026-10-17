"""Local benchmark harness for EXP-ALG-001.

This module deliberately produces measurements without deciding whether SQLite
or PostgreSQL is the correct durable backend. It compares the storage contract
against the in-memory reference using the same deterministic fixture.

Run locally with:
    python -m algox.memory.persistence_benchmark
"""

from __future__ import annotations

import argparse
import statistics
import tempfile
import time
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .persistence import SQLiteMemoryStore
from .store import Evidence, InMemoryStore, MemoryRecord


@dataclass(frozen=True)
class BenchmarkResult:
    backend: str
    operation: str
    iterations: int
    elapsed_seconds: float
    p50_ms: float
    p95_ms: float
    ops_per_second: float


def _fixture(count: int):
    base = datetime(2026, 1, 1, tzinfo=timezone.utc)
    evidence = [
        Evidence(
            id=f"E-BM-{i:06d}",
            source_id="SRC-BENCH",
            locator=f"fixture://evidence/{i}",
            observed_at=base + timedelta(seconds=i),
        )
        for i in range(count)
    ]
    memories = [
        MemoryRecord(
            id=f"M-BM-{i:06d}",
            memory_type="semantic",
            content=f"benchmark memory item {i}",
            created_at=base + timedelta(seconds=i),
            confidence="high",
            evidence_ids=[evidence[i].id],
            valid_from=base + timedelta(seconds=i),
        )
        for i in range(count)
    ]
    return evidence, memories


def _timed(fn, iterations: int) -> BenchmarkResult:
    samples = []
    start = time.perf_counter()
    for _ in range(iterations):
        t0 = time.perf_counter_ns()
        fn()
        samples.append((time.perf_counter_ns() - t0) / 1_000_000)
    elapsed = time.perf_counter() - start
    ordered = sorted(samples)
    p50 = statistics.median(ordered)
    p95 = ordered[max(0, int(len(ordered) * 0.95) - 1)]
    return BenchmarkResult("unknown", "unknown", iterations, elapsed, p50, p95, iterations / elapsed)


def benchmark_in_memory(count: int) -> list[BenchmarkResult]:
    evidence, memories = _fixture(count)
    store = InMemoryStore()
    for item in evidence:
        store.add_evidence(item)
    for item in memories:
        store.add_memory(item)

    def retrieve():
        store.retrieve("benchmark memory")

    def temporal():
        store.reconstruct_as_of(evidence[count // 2].observed_at)

    results = []
    for operation, fn in (("retrieve", retrieve), ("temporal_reconstruction", temporal)):
        r = _timed(fn, max(10, min(count, 1000)))
        results.append(BenchmarkResult("in_memory", operation, r.iterations, r.elapsed_seconds, r.p50_ms, r.p95_ms, r.ops_per_second))
    return results


def benchmark_sqlite(count: int, directory: Path) -> list[BenchmarkResult]:
    evidence, memories = _fixture(count)
    path = directory / "persistence-benchmark.sqlite3"
    store = SQLiteMemoryStore(path)
    for item in evidence:
        store.add_evidence(item)
    for item in memories:
        store.add_memory(item)

    def retrieve():
        store.get_memory(memories[count // 2].id)

    def temporal():
        store.reconstruct_as_of(evidence[count // 2].observed_at)

    results = []
    for operation, fn in (("retrieve", retrieve), ("temporal_reconstruction", temporal)):
        r = _timed(fn, max(10, min(count, 1000)))
        results.append(BenchmarkResult("sqlite", operation, r.iterations, r.elapsed_seconds, r.p50_ms, r.p95_ms, r.ops_per_second))
    store.close()
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=1000)
    args = parser.parse_args()
    if args.count < 10:
        parser.error("--count must be at least 10")

    with tempfile.TemporaryDirectory(prefix="algox-exp-alg-001-") as tmp:
        results = benchmark_in_memory(args.count) + benchmark_sqlite(args.count, Path(tmp))
    print("backend,operation,iterations,elapsed_seconds,p50_ms,p95_ms,ops_per_second")
    for r in results:
        print(f"{r.backend},{r.operation},{r.iterations},{r.elapsed_seconds:.6f},{r.p50_ms:.4f},{r.p95_ms:.4f},{r.ops_per_second:.2f}")


if __name__ == "__main__":
    main()
