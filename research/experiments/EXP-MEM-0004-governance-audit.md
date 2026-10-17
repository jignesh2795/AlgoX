# EXP-MEM-0004 — Governance and Audit Gate

Status: IMPLEMENTED — execution pending

## Hypothesis

Institutional knowledge should not become authoritative merely because an LLM produced a plausible extraction. Truth-changing proposals need explicit review, and every governance transition should be reconstructable from an append-only audit trail.

## Scope

Validate three controls:

1. Complete decision-chain reconstruction from Decision backward through Finding, Result, Experiment, and Claim, with the Decision affecting a Capability.
2. Evidence-gated governance with distinct `rejected`, `review_required`, and `approved` states.
3. Append-only governance events that preserve actor, time, evidence, reason, and prior-state context.

## Implemented controls

- `validate_decision_chain()` reconstructs the causal chain backward from a Decision.
- Claims on the validated chain must carry known evidence.
- `affects` must terminate at a Capability.
- `REFUTE`, `QUALIFY`, and `SUPERSEDE` proposals require explicit review even with valid evidence.
- Invalid or evidence-deficient proposals are rejected.
- `GovernanceEvent` and `AuditLog` provide an immutable-in-process audit surface.
- Duplicate event IDs are rejected; events cannot be edited in place.

## Test plan

- Complete decision chain passes.
- Missing upstream experiment relation is detected.
- Missing finding-to-decision relation is detected.
- Missing decision-to-capability relation is detected.
- Claim without evidence is detected.
- Evidence-free delta is rejected.
- Truth-changing delta enters `review_required`.
- Explicit approval identity is required before entity commit.
- Duplicate audit events are rejected.
- Invalid event types and empty actors are rejected.

## Evidence standard

This experiment is a software-governance control test. It does not establish that any research claim is true; it establishes that the knowledge system preserves the distinction between model proposals and institutional truth.

## Next measurement

Run the full test suite and then integrate governance events with durable persistence. Measure decision-chain validation latency, audit append latency, and reconstruction correctness on the memory benchmark corpus.
