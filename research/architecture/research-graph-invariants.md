# Research Graph Invariants

The typed research graph is a structured projection over evidence-backed institutional records.

## Invariants

1. **Evidence-first:** every durable Claim, Finding, Experiment result, or Decision that asserts a factual conclusion carries evidence references.
2. **No phantom edges:** relationships are explicit records; traversal never invents missing links.
3. **Temporal correctness:** a reconstruction at time `T` cannot use evidence observed after `T`.
4. **Contradiction visibility:** supporting and contradicting evidence remain separately traversable.
5. **Rebuildability:** graph structures can be rebuilt from authoritative records.
6. **Determinism:** identical records and query constraints produce the same path.
7. **Separation of concerns:** the LLM proposes interpretations; structured validation decides whether a knowledge change is admissible.

## Storage direction

The initial implementation deliberately remains storage-independent. PostgreSQL remains the intended system of record; graph and semantic indexes are derived projections. A dedicated graph database is not justified until graph workloads demonstrate material benefit.

## Financial-system implication

For broker APIs, exchange rules, fees, instrument metadata, market hours, corporate actions, and regulatory constraints, every material assertion should carry an effective/observation time. AlgoX must be able to reconstruct both current truth and historical institutional belief.
