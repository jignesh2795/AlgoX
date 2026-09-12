# PX-2023-071 — Indian Broker API Boundary Pattern

## Scope

Cross-project research record for the Indian broker-integration layer, using official broker SDK/API implementations as primary evidence rather than treating any single broker as the canonical architecture.

## Historical observation

The 2023 Indian retail-algo ecosystem exposed a recurring split between broker-specific APIs and strategy/application code. Zerodha Kite Connect is a representative example: the official client provides authentication, orders, portfolio, instruments, quotes, historical data and WebSocket streaming while retaining broker-specific order/product/exchange semantics.

## Capability decomposition

```text
Broker API
├── Authentication / session
├── Instrument identity
├── Market data REST
├── Market data streaming
├── Order commands
├── Order/trade queries
├── Portfolio / funds
└── Venue-specific semantics
```

## AlgoX finding

A multi-broker trading platform should not normalize away all broker semantics. The correct abstraction is:

```text
Strategy / Portfolio / Risk
          ↓
Canonical intent / execution contract
          ↓
Broker adapter
          ↓
Venue-specific request
          ↓
Broker events
          ↓
Reconciliation
          ↓
Canonical state
```

## Important distinction

`API response`, `broker event`, and `canonical order state` are different evidence domains. A successful order-command response does not by itself prove execution. A broker event does not automatically become authoritative internal state without reconciliation and identity checks.

## Indian-market requirements to preserve

- exchange and segment identity
- instrument identity and contract metadata
- order variety and product type
- validity
- quantity/lot-size constraints
- broker/exchange-specific errors
- authentication/session expiry
- market-data subscription semantics
- asynchronous order/trade events
- rate limits and operational constraints
- corporate-action/instrument-master effects

## Decision

**ADOPT** the boundary principle.

**ADAPT** broker-specific APIs behind a canonical contract.

**REJECT** a universal abstraction that erases venue semantics.

## Evidence maturity

C2 — synthesized from primary broker API/client evidence. This record is a research finding, not a claim that every Indian broker implements the same protocol.

## Sources

- https://github.com/zerodha/pykiteconnect
- https://github.com/zerodha/pykiteconnect/blob/master/kiteconnect/connect.py
