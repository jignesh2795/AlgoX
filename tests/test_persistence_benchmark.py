from algox.memory.persistence_benchmark import benchmark_in_memory, benchmark_sqlite


def test_persistence_benchmark_returns_measurements(tmp_path):
    in_memory = benchmark_in_memory(20)
    sqlite = benchmark_sqlite(20, tmp_path)

    assert {r.operation for r in in_memory} == {"retrieve", "temporal_reconstruction"}
    assert {r.operation for r in sqlite} == {"retrieve", "temporal_reconstruction"}
    assert all(r.iterations >= 10 for r in in_memory + sqlite)
    assert all(r.elapsed_seconds > 0 for r in in_memory + sqlite)
    assert all(r.p50_ms >= 0 and r.p95_ms >= 0 for r in in_memory + sqlite)
    assert all(r.ops_per_second > 0 for r in in_memory + sqlite)
