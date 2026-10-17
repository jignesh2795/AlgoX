# Closed Learning Loop

AlgoX now has an explicit bridge from an agent run to a candidate institutional-memory change.

```text
AgentTrace
   ↓
Evaluation
   ↓
Experience
   ↓
Consolidation Governor
   ↓
Consolidation Proposal
   ↓
Knowledge Governance
   ↓
Institutional Memory
```

## Invariants

- A running or incomplete trace cannot produce learning.
- A trace without observations cannot pass evaluation.
- A trace without independent verification cannot pass evaluation.
- Failed verification cannot produce a consolidation proposal.
- A consolidation proposal must carry evidence IDs inherited from the trace.
- The consolidation layer never commits durable truth.
- Governance remains responsible for approval and audit.

## Negative experience

Failure is not equivalent to uselessness. A verified failure can later become a
failure-mode memory, constraint, rejected approach, or qualification. The first
implementation deliberately keeps consolidation conservative and requires the
caller to mark a lesson reusable.

## Financial boundary

This loop is a research-learning mechanism. It must not silently promote an
agent observation into trading, risk, broker, exchange, or regulatory policy.
Those domains require their own evidence, approval and temporal validity rules.

## Next integration target

Connect accepted consolidation proposals to the existing `KnowledgeGovernance`
and `AuditLog` APIs so every durable learning event has an auditable state
transition. Only after that integration should persistence adapters be designed.
