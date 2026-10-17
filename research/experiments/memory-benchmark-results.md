# EXP-MEM-0001 — Baseline Results

Status: **INITIAL BASELINE**

## Scope

This document records the deterministic in-process baseline only. No claim is made yet about PostgreSQL, pgvector, a dedicated graph database, or a vector database.

## Dataset

Six evidence records, six memories and five explicit relationship types are included in the first fixture. The fixture contains temporal supersession, contradictory research claims, an experiment result and provenance chains.

## Results

| Workload | Baseline result |
|---|---|
| W1 Exact lookup | PASS at unit-test level |
| W2 Semantic recall | NOT IMPLEMENTED — requires semantic adapter |
| W3 Relationship traversal | PASS for explicit one-hop relations |
| W4 Contradiction detection | PASS for explicit contradiction relation |
| W5 Temporal reconstruction | PASS for validity intervals |
| W6 Provenance tracing | PASS for evidence-backed records |
| W7 Supersession | PASS for validity-window reconstruction |
| W8 Decision reconstruction | NOT IMPLEMENTED — next graph-chain workload |
| W9 Experiment linkage | PASS at explicit relation level |
| W10 Rebuildability | ARCHITECTURALLY SUPPORTED; derived indexes not yet implemented |

## Interpretation

The baseline validates the core invariants, not retrieval intelligence. The next experiment must add ranking and multi-hop traversal before comparing specialized storage technologies.

## Next gate

Implement:

1. evidence-bundle retrieval API
2. relation-aware multi-hop traversal
3. deterministic ranking
4. contradiction-aware retrieval
5. `as_of` query support in retrieval
6. benchmark timing instrumentation

Only after that should PostgreSQL/pgvector and dedicated graph/vector implementations be compared.
