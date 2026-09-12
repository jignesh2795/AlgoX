# PX-2023-043 — Asynchronous Order-State Reconciliation

## Historical role
Indian broker APIs provide multiple representations of an order lifecycle: synchronous command responses, order books, trade books, postbacks/webhooks and WebSocket updates. Kite Connect exposes order history and trades separately and streams order updates over WebSocket. citeturn0search15turn0search2 Upstox documents order-update streams and webhooks, while Angel One documents WebSocket order-status events with fields for filled and unfilled quantities. citeturn0search9turn0search12turn0search0

## Architecture observations
- An order command acknowledgement is not equivalent to execution.
- One order can produce multiple lifecycle events and multiple trades/fills.
- Partial fills require accumulation and reconciliation.
- Polling and push channels can coexist; duplicate or out-of-order observations must be tolerated.
- Broker reconnects and missed events imply the need for authoritative reconciliation queries.

## AlgoX extraction
**Capability:** evidence-aware order state machine with reconciliation.

```text
Intent
  ↓
Submitted
  ↓
Accepted / Rejected
  ↓
Partially Filled
  ↓
Filled / Cancelled
  ↓
Reconciled
```

The state machine must preserve raw broker observations and derive canonical state rather than overwriting history.

## Critical lesson
The execution engine must be **event-sourced enough to reconstruct what happened**, even if the eventual production implementation does not use full event sourcing.

## Decision status
ADOPT as a design requirement for future execution-system research.

## Evidence maturity
C2 — primary broker documentation; production implementation not yet built or benchmarked by AlgoX.
