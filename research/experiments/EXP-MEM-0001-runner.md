# EXP-MEM-0001 — Executable Benchmark Runner

Status: **IMPLEMENTED — NOT EXECUTED IN THIS SESSION**

The executable harness is `algox/memory/benchmark.py`. It intentionally depends only on the standard library plus the existing AlgoX memory implementation.

## Current measured workloads

- W1 exact retrieval: evidence recall + latency
- W3 relationship traversal: target recall + latency
- W4 contradiction retrieval: counter-evidence recall + latency
- W5 temporal retrieval: temporal accuracy
- W6 provenance completeness

## Interpretation policy

A passing workload means the expected invariant is satisfied. It does not mean the implementation is production-ready.

Latency numbers are environment-dependent and must only be recorded from an actual run. This repository record therefore does not invent benchmark timings.

## Next benchmark expansion

- W2 semantic recall using a pluggable semantic adapter
- W7 explicit supersession query metric
- W8 decision-chain reconstruction
- W9 experiment-to-decision tracing
- W10 full rebuild verification
- repeated runs with median/p95 latency
- larger synthetic corpus
- PostgreSQL comparison after the in-process baseline is stable
