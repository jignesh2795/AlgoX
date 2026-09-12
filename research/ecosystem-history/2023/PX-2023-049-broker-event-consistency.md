# PX-2023-049 — Broker Event Consistency and Reconciliation

## Historical evidence
2023 Indian broker API discussions expose an important operational distinction: receiving an order-update event is not necessarily equivalent to having an authoritative final order state. Zerodha documentation describes order updates through WebSockets/postbacks, including partial fills; its developer discussions recommend using the update as an event and then fetching the order book to establish current state. citeturn1search0turn1search9

Upstox similarly exposes a portfolio WebSocket carrying order updates, with fields including order status, filled quantity, pending quantity, timestamps, and exchange identifiers. citeturn1search2turn1search3

## AlgoX finding
A broker adapter should distinguish:

```text
COMMAND
  ↓
ACKNOWLEDGEMENT
  ↓
EVENT STREAM
  ↓
AUTHORITATIVE STATE QUERY
  ↓
CANONICAL ORDER STATE
```

Events are signals for state convergence; they should not automatically be treated as the complete source of truth.

## Required capabilities
- idempotent event processing
- duplicate-event tolerance
- out-of-order-event tolerance
- partial-fill accumulation
- reconciliation against broker state
- reconnect recovery
- startup reconciliation
- canonical internal order state
- immutable raw event retention

## Decision status
ADOPT as a core execution-system requirement for future trading-platform research.

## Evidence maturity
C2 — primary broker documentation plus 2023 practitioner/developer evidence; no production implementation by AlgoX yet.
