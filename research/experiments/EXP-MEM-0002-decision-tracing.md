# EXP-MEM-0002 — Decision Tracing

Status: **DESIGNED / IMPLEMENTED**

## Hypothesis

A provenance-first graph projection can reconstruct a research conclusion and its supporting/counter evidence without storing the graph as the authority.

## Baseline

Memory records plus explicit relations in the in-process store.

## Workloads

- reconstruct all nodes reachable from a research claim
- collect unique evidence IDs across the chain
- expose contradiction and experiment links
- enforce a maximum traversal depth
- produce a deterministic human-auditable explanation

## Acceptance criteria

1. No inferred edge is created.
2. Every returned evidence ID exists in the evidence store.
3. Traversal is bounded.
4. Contradictory evidence remains visible.
5. The same records produce the same explanation.
6. Missing relationships are represented by absence, not hallucinated links.

## Next extension

Add explicit `Claim`, `Finding`, `Experiment`, `Result`, `Decision`, and `Capability` entities so the synthetic benchmark can represent the complete institutional decision chain rather than memory-to-memory links alone.
