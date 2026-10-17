# Semantic Retrieval Gate

## Objective

Determine whether semantic retrieval materially improves AlgoX research retrieval over the deterministic lexical baseline without weakening provenance, temporal correctness, contradiction visibility, or rebuildability.

## Candidates

1. Lexical baseline
2. Dependency-free token-vector baseline
3. External embedding adapter + pgvector
4. Alternative vector backend only if benchmark evidence justifies it

## Required metrics

- Recall@k
- Precision@k
- evidence recall
- contradiction recall
- temporal accuracy
- provenance completeness
- ranking stability
- p50/p95 latency
- rebuild time
- operational complexity

## Gate

Semantic retrieval is promoted only when it demonstrates meaningful workload improvement on the same corpus and query set. A higher similarity score or vendor benchmark alone is insufficient.

## Safety invariant

Semantic search returns candidate memories. It never establishes truth. Evidence, provenance, temporal validity and contradiction state remain authoritative.
