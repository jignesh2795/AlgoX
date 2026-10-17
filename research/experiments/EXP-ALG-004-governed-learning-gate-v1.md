# EXP-ALG-004 — Durable Learning Governance Gate

## Status
IMPLEMENTED — local execution pending.

## Question
Can an agent learn from verified experience without silently promoting model output into institutional truth?

## Controlled pipeline

```text
AgentTrace
  ↓
Evaluation
  ↓
Experience
  ↓
ConsolidationProposal
  ↓
KnowledgeDelta
  ↓
Governance review
  ↓
Append-only audit
  ↓
Explicit canonical commit
```

## Controls implemented

- failed or incomplete traces do not produce learning proposals;
- reusable learning requires verification and evidence;
- consolidation produces a proposal rather than mutating canonical state;
- proposals are converted into evidence-backed knowledge deltas;
- rejected and approved review outcomes are audited;
- truth-changing operations remain review-gated;
- explicit approval identity remains required for canonical entity commitment.

## Failure cases

1. No verification → no proposal.
2. Failed verification → no proposal.
3. Missing evidence → rejected governance delta.
4. Truth-changing operation → `review_required`.
5. Missing approval identity → canonical commit rejected.
6. Duplicate audit event → rejected.

## Measurements to run locally

- proposal generation latency;
- governance review latency;
- audit append latency;
- rejected-proposal correctness;
- approved-proposal correctness;
- audit history reconstruction correctness;
- canonical-state mutation absence before explicit commit.

## Acceptance gate

The experiment passes only if every failure case is caught and every durable transition can be reconstructed from proposal, evidence, review state, actor, time and audit history.

No experiment result is claimed until local execution is recorded.
