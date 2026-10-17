# PX-2023-041 — Indian Broker API Contract Patterns

## Historical role
The 2023 Indian broker/API ecosystem provides a useful reference for the canonical adapter boundary AlgoX should preserve. Zerodha Kite Connect exposes order APIs, portfolio APIs, instrument/quote data and WebSocket streaming; its WebSocket stream carries market data plus order updates. citeturn0search2turn0search3 Upstox similarly separates market streaming from order/portfolio updates and supports WebSocket and webhook delivery. citeturn0search1turn0search12 Angel One SmartAPI exposes order operations, postbacks and WebSocket order updates, including explicit connection and heartbeat constraints. citeturn0search0turn0search4

## Architecture observations
- REST/HTTP is used for commands and queries; WebSocket/webhook channels provide asynchronous state changes.
- A broker adapter therefore has at least two planes: command/query and event/update ingestion.
- Broker APIs expose venue-specific fields such as product type, order variety, trigger price, disclosed quantity, symbol token and exchange identifiers.
- Connection limits, heartbeats, authentication expiry and rate limits are part of the adapter contract, not incidental implementation details.
- Order state cannot safely be inferred from the HTTP response alone; asynchronous updates must be reconciled.

## AlgoX extraction
**Capability:** broker integration boundary with asynchronous event reconciliation.

**Canonical model:**

```text
Canonical Order Intent
        ↓
Broker Adapter
   ┌────┴────┐
   ↓         ↓
Commands   Event Stream
   ↓         ↓
Broker     Normalizer
             ↓
       Order State Machine
             ↓
        Reconciliation
```

## Critical lesson
Do not make the canonical order model identical to any broker's schema. Preserve broker-specific evidence at the adapter boundary while translating into a canonical internal representation.

## Decision status
ADOPT as an AlgoX architecture principle for the future trading-platform capability catalog.

## Evidence maturity
C2 — primary broker documentation; no AlgoX implementation/reproduction yet.
