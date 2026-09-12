# EXP-MEM-0001 — Executable Benchmark Runner

Status: **IMPLEMENTED — NOT EXECUTED IN THIS SESSION**

The executable harness is `algox/memory/benchmark.py`. It intentionally depends only on the standard library plus the existing AlgoX memory implementation.

## Current implemented workloads

- W1 exact retrieval: evidence recall + latency
- W2 semantic retrieval: dependency-free candidate retrieval exists
- W3 relationship traversal: target recall + latency
- W4 contradiction retrieval: counter-evidence recall + latency
- W5 temporal retrieval: temporal accuracy
- W6 provenance completeness
- W8 decision-chain validation and reconstruction primitives
- W9 experiment-to-decision path tracing primitives

## Interpretation policy

A passing workload means the expected invariant is satisfied. It does not mean the implementation is production-ready.

Latency numbers are environment-dependent and must only be recorded from an actual run. This repository record therefore does not invent benchmark timings.

## Next benchmark expansion

- W2 formal Recall@k / Precision@k measurement
- W7 explicit supersession query metric
- W8 executable decision-chain benchmark
- W9 executable experiment-to-decision benchmark
- W10 full rebuild verification
- contradiction-chain and counter-evidence scoring
- temporal path validity at multiple `as_of` timestamps
- repeated runs with median/p95 latency
- larger synthetic corpus
- PostgreSQL comparison after the in-process baseline is stable
