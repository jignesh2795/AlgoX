# EXP-ALG-001 — Persistence Baseline

## Status
DESIGNED — execution pending.

## Objective
Measure the actual workload that AlgoX memory persistence must support before selecting a durable backend.

## Baseline
The current reference implementation is `InMemoryStore`. It keeps evidence, memory records and knowledge deltas in structured dictionaries; retrieval is deterministic and temporal reconstruction is explicit. See `algox/memory/store.py`.

## Workloads

1. Sequential evidence inserts.
2. Sequential memory inserts with provenance validation.
3. Evidence-backed delta insertion and validation.
4. Exact/term retrieval.
5. Temporal reconstruction (`reconstruct_as_of`).
6. Relation traversal/conflict lookup.
7. Restart/reload durability test for the candidate persistent adapter.

## Dataset
Use the existing `research/experiments/memory-benchmark-dataset.json` as the correctness fixture. The existing benchmark tests cover six evidence records, six memories, temporal reconstruction, contradiction lookup and provenance checks.

## Candidate
First durable candidate: PostgreSQL. Do not add a production dependency until the benchmark establishes a requirement for it.

## Metrics

- insert operations/second
- p50/p95 retrieval latency
- temporal reconstruction latency
- relation lookup latency
- storage size
- restart/reload correctness
- provenance validation correctness
- implementation complexity

## Acceptance gates

A persistent adapter is justified only if:

- it preserves all required memory semantics;
- restart/reload is lossless for accepted records;
- provenance and temporal constraints remain enforceable;
- measured workload exceeds practical in-memory limits or durability becomes a concrete requirement;
- benchmark results and environment are recorded as evidence.

## Execution

Local only. No GitHub Actions dependency.

Suggested command once the adapter and benchmark runner exist:

```bash
python tools/local_verify.py --pytest
```

Then run the dedicated persistence benchmark and record raw results in this experiment file. Do not mark the experiment passed until it has actually been executed.

## Current conclusion
The repository already has a useful storage-independent contract. The next engineering task is a measured persistence adapter, not a premature database migration.
