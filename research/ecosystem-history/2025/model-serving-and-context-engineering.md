# 2025 Model Serving and Context Engineering

## Status
PROVISIONAL.

## Research question
What changed in 2025 around serving models and constructing context for long-running research agents?

## Serving findings
Modern inference infrastructure increasingly separates:

- model execution
- scheduling
- batching
- KV/cache management
- speculative decoding
- distributed execution
- request routing
- autoscaling
- observability
- service-level objectives

This reinforces the 2024 conclusion that the model itself is only one layer of the AI system.

## Context findings
Context should be treated as a managed resource rather than an unlimited prompt. A research agent may need to combine:

```text
Task
 + source evidence
 + prior findings
 + counter-evidence
 + temporal constraints
 + experiment results
 + current policy
 + tool observations
```

The retrieval system therefore needs to decide not merely **what is relevant**, but what evidence is sufficiently authoritative, current, non-contradictory and within the task's temporal scope.

## AlgoX architecture implication

```text
                RESEARCH REQUEST
                       ↓
                 Query Planner
                       ↓
                Context Policy
          ┌────────────┼────────────┐
          ↓            ↓            ↓
       Evidence     Memory       Graph
       Retrieval    Retrieval   Traversal
          └────────────┼────────────┘
                       ↓
                Context Compiler
                       ↓
              Compute / Model Policy
                       ↓
                  Inference
                       ↓
                  Verifier
```

The **Context Compiler** is a useful new conceptual boundary. It converts heterogeneous evidence into a bounded reasoning context while preserving provenance and temporal constraints.

## Institutional-memory consequence
A raw retrieved chunk, embedding, generated summary or cached context must never become the authoritative representation of a research fact. Canonical evidence and knowledge remain authoritative; context is a disposable projection.

## Decision
**ADOPT:** explicit context-management boundary.

**ADOPT:** provenance-preserving context assembly.

**TRIAL:** cache/prefix reuse and specialized retrieval optimization.

**HOLD:** treating the context window as the institutional memory itself.

## Relationship to financial systems
The same principle applies to financial research. A model should receive market data, instrument identity, rules, fees, corporate-action state and historical evidence through explicit context contracts rather than relying on an implicit long prompt.
