# Research Decision Tracing

AlgoX must be able to reconstruct the reasoning behind an institutional decision.

## Canonical chain

```text
Source
  ↓
Evidence
  ↓
Claim / Memory
  ↓
Finding
  ↓
Experiment
  ↓
Result
  ↓
Decision
  ↓
Capability
```

## Rules

1. Every durable decision must have provenance.
2. A decision may have multiple supporting findings.
3. Counter-evidence must remain visible.
4. Superseded knowledge is retained rather than silently overwritten.
5. Temporal validity determines whether a node belongs to an `as_of` reconstruction.
6. Missing links are reported as missing evidence, not filled by model inference.
7. Graph traversal is a derived convenience; authoritative records remain the source of truth.

## Example explanation

```text
Decision D-001
  ← Finding F-001
      ← Experiment EXP-017
          ← Evidence E-006
      ← Claim C-001
          ← Evidence E-004
  ← Counter-evidence E-005
```

The resulting explanation should answer:

- What was decided?
- What evidence supported it?
- What contradicted it?
- Which experiment changed confidence?
- What was the state of knowledge at the decision date?

This is the minimum standard for AlgoX institutional intelligence.
