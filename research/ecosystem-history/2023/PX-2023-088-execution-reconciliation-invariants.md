# PX-2023-088 — Execution Reconciliation Invariants

**Year:** 2023 evidence / historical capability analysis
**Category:** Execution / Reliability / Risk
**Status:** Researched

## Finding
Execution correctness requires reconciliation between external venue state and internal event-sourced state. Order status, fills, and positions cannot be assumed complete merely because a local order request succeeded.

NautilusTrader provides a strong reference architecture: reconciliation consumes order-status, fill, and position reports; detects duplicates; reconstructs missing fills; and compares venue positions with internal state.

## Invariants to preserve
1. Venue state is authoritative for live reconciliation.
2. Missing history must not silently become fabricated economic history.
3. Duplicate reports must be detectable and idempotent.
4. Partial fills must remain explicit.
5. Position reconciliation must be downstream of order/fill reconciliation.
6. Unknown outcomes must remain unknown until sufficient evidence arrives.

## AlgoX implication
These become capability requirements for any future Indian-market execution system and benchmark dimensions for broker adapters.

## Decision
**ADOPT** as an architectural requirement; implementation remains experiment-gated.
