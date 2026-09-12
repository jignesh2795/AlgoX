# Experience Consolidation Boundary

## Purpose

Agent traces and outcomes are experiences, not institutional truth. AlgoX must
convert an experience into durable memory only through an explicit,
evidence-backed consolidation step.

## Lifecycle

```text
Agent Trace
    ↓
Outcome
    ↓
Verification
    ↓
Experience
    ↓
Consolidation Governor
    ↓
Candidate Memory / Knowledge Delta
    ↓
Governance Review
    ↓
Institutional Memory
```

## Conservative admission rules

An experience is eligible to produce a consolidation proposal only when:

1. the experience has independent verification;
2. at least one evidence reference exists;
3. the lesson is non-empty;
4. the lesson is explicitly marked reusable.

A failed or negative experience is still valuable evidence. It should not be
silently discarded; instead it can produce a lesson such as a failure mode,
constraint, or rejected approach after verification.

## Important boundary

The consolidation governor **does not write durable institutional memory**.
It emits a proposal. The existing knowledge-governance layer remains the sole
authority for durable truth changes.

This prevents an agent from learning a rule merely because one trajectory
happened to succeed.

## Future extensions

- repeated-experience support;
- contradiction-aware consolidation;
- confidence decay;
- temporal validity;
- negative-experience memory;
- skill/procedure promotion after repeated validation;
- human review policies by memory type;
- consolidation benchmarks.
