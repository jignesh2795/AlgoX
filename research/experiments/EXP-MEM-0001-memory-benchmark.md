# EXP-MEM-0001 — AlgoX Memory Benchmark

Status: Planned

## Objective

Determine whether a PostgreSQL-first memory architecture is sufficient for AlgoX before introducing a dedicated vector or graph database.

## Hypothesis

A relational authoritative store plus derived semantic retrieval and relational graph traversal can satisfy the first institutional-memory workload without the operational complexity of multiple specialized databases.

## Baselines

A. PostgreSQL relational retrieval only

B. PostgreSQL + pgvector

C. PostgreSQL + pgvector + relational graph tables

D. Dedicated graph database + vector retrieval

E. Hybrid graph + vector architecture

## Workload

1. Find all evidence supporting a capability decision.
2. Answer a point-in-time question about a changing technology.
3. Find contradictions between two projects.
4. Traverse project → capability → algorithm → experiment → decision.
5. Find previous experiments related to a current research question.
6. Retrieve evidence from a specified date range.
7. Identify superseded claims.
8. Resolve multiple project aliases to one canonical entity.
9. Retrieve the most relevant evidence while respecting authority and confidence.
10. Reconstruct what AlgoX believed at a historical point in time.

## Metrics

- exact-answer recall
- evidence precision
- temporal accuracy
- provenance completeness
- contradiction detection accuracy
- graph traversal latency
- semantic retrieval latency
- write latency
- storage size
- operational complexity
- backup/recovery complexity
- query complexity
- reproducibility

## Acceptance principle

A dedicated database is justified only when it produces a material improvement on the actual AlgoX workload that compensates for additional operational complexity.

## Expected first implementation

```text
Object/source artifacts
        ↓
PostgreSQL
  ├── evidence
  ├── claims
  ├── findings
  ├── experiments
  ├── decisions
  ├── entities
  ├── relationships
  └── temporal metadata
        ↓
pgvector projection
        ↓
Hybrid retrieval
```

## Important distinction

This experiment does not attempt to prove that PostgreSQL is universally superior. It tests whether PostgreSQL is the correct **starting authority** for AlgoX.
