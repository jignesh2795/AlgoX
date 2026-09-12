# EXP-MEM-0006 — Extended Memory and Governance Benchmark

## Status

IMPLEMENTED — NOT EXECUTED IN SESSION

Execution remains a local responsibility because AlgoX deliberately does not depend on GitHub Actions.

## Objective

Extend the first memory benchmark beyond retrieval into the invariants that make institutional memory trustworthy:

- W7: explicit supersession state
- W8: backward decision-chain reconstruction
- W9: experiment-to-decision traceability
- W10: deterministic graph projection rebuild
- G1: governance review correctness
- G2: append-only audit reconstruction

## Workloads

### W7 — Supersession

Verify that a `superseded_by` relation has an existing predecessor marked `superseded` and an existing successor marked `active`.

This tests state-transition integrity rather than merely finding a related record.

### W8 — Decision-chain reconstruction

Validate the canonical chain backward from a Decision:

`Decision ← Finding ← Result ← Experiment ← Claim`

The Claim must retain evidence, and the Decision must pass the typed relation checks.

### W9 — Experiment-to-decision tracing

Verify that a validated chain terminates in the intended Capability through `Decision → affects → Capability`.

### W10 — Graph rebuild

Build the logical graph projection twice from the same authoritative memory store and require identical signatures.

A projection is therefore reproducible from canonical state and is not itself authoritative.

### G1 — Governance review

A valid evidence-backed ADD proposal should be approved. Truth-changing operations remain review-required by policy.

### G2 — Audit append/history

Append a governance event and reconstruct the entity history. Duplicate event IDs remain invalid.

## Metrics

For correctness workloads, the primary metric is a ratio in `[0, 1]`.

For latency, the runner records elapsed milliseconds from the local Python process. These values are empirical and must not be documented as benchmark results until the runner is actually executed.

## Gate

The benchmark is a design/invariant gate, not a performance claim. Before selecting PostgreSQL schema/index strategies, AlgoX should execute this suite locally and preserve the output with:

- Python version
- operating system
- CPU/memory context where useful
- repository commit SHA
- execution timestamp
- full benchmark output

Only then should measured workload characteristics influence the persistence implementation.
