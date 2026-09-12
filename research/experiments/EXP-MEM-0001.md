# EXP-MEM-0001 — Institutional Memory Baseline

Status: **DESIGNED**  
Purpose: establish a reproducible baseline before selecting specialized memory infrastructure.

## Hypothesis

A structured, provenance-first memory model can satisfy AlgoX's initial research-memory workloads without making a vector or graph database authoritative.

## Workloads

| ID | Workload | Success criterion |
|---|---|---|
| W1 | Exact source lookup | correct source/evidence returned |
| W2 | Semantic recall | relevant memories recalled above baseline |
| W3 | Relationship traversal | linked evidence/decision chain reconstructed |
| W4 | Contradiction detection | conflicting claims surfaced, not hidden |
| W5 | Temporal reconstruction | state at requested `as_of` time is correct |
| W6 | Provenance tracing | claim → evidence → source is complete |
| W7 | Supersession | latest valid state selected while history remains |
| W8 | Decision reconstruction | evidence → finding → decision chain recovered |
| W9 | Experiment linkage | experiment result linked to affected decision |
| W10 | Rebuildability | derived indexes can be discarded and recreated |

## Test dataset

The benchmark dataset should contain synthetic but realistic records representing:

- an evolving broker API
- an exchange-rule change
- competing backtesting approaches
- contradictory research findings
- a project architecture that was later revised
- an experiment that invalidated an earlier hypothesis
- a final ADR based on the accumulated evidence

Every record must have provenance and timestamps.

## Implementations to compare

1. In-process relational baseline.
2. PostgreSQL logical model.
3. PostgreSQL + pgvector projection.
4. PostgreSQL + graph projection.
5. Dedicated graph/vector hybrid, only if required by benchmark evidence.

## Metrics

- exact retrieval accuracy
- evidence recall
- contradiction recall
- temporal reconstruction accuracy
- provenance completeness
- multi-hop traversal latency
- write consistency
- rebuild time
- operational complexity
- storage cost
- explainability

## Decision rule

No technology receives an architectural promotion because of popularity, benchmark marketing or embedding-search quality alone. Promotion requires improvement across the relevant workload class without compromising provenance, temporal correctness, auditability and rebuildability.

## Expected result

The current architectural prior is PostgreSQL as the system of record, with vector and graph structures treated as derived projections. EXP-MEM-0001 exists to **challenge that prior**, not to confirm it.
