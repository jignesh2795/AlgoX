# AlgoX Persistence Contract

**Status:** Design contract before PostgreSQL implementation

## Purpose

Define the persistence behavior that every durable AlgoX memory backend must satisfy. This prevents the database schema from becoming the architecture by accident.

## Authority model

```text
Source artifacts
      ↓
Evidence / provenance
      ↓
Canonical research entities
      ↓
Governance events
      ↓
Derived indexes / graph projections
```

The canonical records are authoritative. Semantic vectors, search indexes, caches, summaries, and graph projections are rebuildable derivatives.

## Required durable records

The first persistent implementation must support:

- sources and source versions;
- evidence with source locator, observation time, and maturity;
- research entities: Claim, Finding, Experiment, Result, Decision, Capability;
- typed research edges;
- memory records and memory relations;
- knowledge deltas;
- governance/audit events;
- temporal validity;
- confidence and status;
- provenance links.

## Transactional invariants

A persistence adapter must enforce these invariants atomically:

1. An evidence reference cannot point to an unknown evidence record.
2. An entity cannot be committed without required evidence.
3. An edge cannot reference an unknown endpoint.
4. Duplicate canonical IDs are rejected.
5. Duplicate audit event IDs are rejected.
6. Governance state transitions are represented by events; history is not silently overwritten.
7. A derived index failure cannot destroy canonical knowledge.
8. A failed transaction leaves no partial knowledge commit.
9. Historical reconstruction never uses evidence observed after the requested time.
10. A projection can be deleted and rebuilt without changing canonical knowledge.

## Commit protocol

```text
BEGIN TRANSACTION
       ↓
validate delta
       ↓
validate evidence
       ↓
validate temporal constraints
       ↓
validate entity/edge references
       ↓
apply approved canonical mutation
       ↓
append governance event
       ↓
COMMIT
       ↓
refresh derived projections asynchronously
```

Projection refresh must not be required for canonical correctness.

## Concurrency

The future PostgreSQL adapter must define behavior for:

- two researchers updating the same entity;
- two agents proposing competing deltas;
- simultaneous supersession/refutation;
- duplicate retries;
- interrupted commits;
- stale approval decisions.

The preferred design is optimistic concurrency using an entity/version revision plus an atomic transaction. Idempotency keys should protect retried writes.

## Audit requirements

Every truth-changing transition should retain:

- event ID;
- entity or delta ID;
- event type;
- actor or policy identity;
- event time;
- supporting evidence IDs;
- reason;
- previous-state reference/hash where applicable.

Audit history is append-only from the application's perspective.

## Temporal requirements

Store both **valid time** and **observation time** where applicable.

Example:

```text
valid_from  = when the broker rule became effective
observed_at = when AlgoX verified the rule
```

These must not be collapsed into one timestamp. A historical query must be able to answer what AlgoX could legitimately have known at time T.

## Graph projection

Relational edge tables are sufficient as the initial graph representation. The projection must support deterministic rebuild and preserve relation type, provenance, and temporal metadata.

A dedicated graph database remains an optimization decision and must pass the graph workload gate first.

## Semantic projection

Embedding rows are disposable. Each vector record must identify the canonical entity/chunk and the embedding/model version. Re-embedding must not change canonical content.

## PostgreSQL implementation gate

Before implementation, the local benchmark suite should establish baseline measurements for:

- exact retrieval;
- relationship traversal;
- contradiction retrieval;
- temporal reconstruction;
- provenance completeness;
- decision-chain reconstruction;
- experiment-to-decision tracing;
- audit append and history reconstruction;
- graph rebuild;
- repeated p50/p95 latency.

The PostgreSQL implementation is then compared against those workloads rather than adopted merely because it is a conventional choice.
