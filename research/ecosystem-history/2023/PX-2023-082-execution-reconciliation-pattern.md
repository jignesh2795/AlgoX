# PX-2023-082 — Execution reconciliation as a first-class capability

## Finding
Execution correctness requires reconciliation between internal state and external venue state. A robust architecture treats orders, fills, and positions as independently reconcilable evidence rather than assuming internal event processing is complete.

## Evidence
NautilusTrader's reconciliation architecture provides a concrete reference: venue reports are generated for orders, fills, and positions; reports are deduplicated; missing events can be reconstructed; positions are compared against venue state.

## Capability extraction
- startup reconciliation
- order reconciliation
- fill reconciliation
- position reconciliation
- duplicate detection
- missing-event reconstruction
- explicit degraded-state handling

## AlgoX relevance
High. This capability belongs in the canonical execution/reliability model and should be benchmarked independently of strategy alpha.

## Decision
ADOPT as an architectural requirement; implementation remains an experiment question.
