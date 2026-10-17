# PX-2023-053 — Provider Abstraction Must Preserve Venue Semantics

**Period:** 2023
**Domain:** Broker/exchange connectivity
**Status:** Historical research record

## Observation

CCXT and Indian broker APIs demonstrate the value of a normalized interface, while their venue-specific fields and behavior show why normalization cannot erase execution semantics. Kite Connect exposes order varieties, modifications, cancellations, order history, trade history, and WebSocket order updates; these are related but distinct resources.

## Finding

A provider abstraction should normalize common concepts while retaining a deliberate escape hatch for venue-specific capabilities.

## Recommended boundary

```text
Canonical Broker Interface
├── place_order
├── modify_order
├── cancel_order
├── get_orders
├── get_trades
├── get_positions
├── stream_market_data
└── stream_order_events

Venue-specific extension
└── provider capabilities / native parameters
```

The abstraction should not force every venue into the lowest common denominator.

## Decision

**ADOPT:** canonical interface + explicit capability discovery.

**ADAPT:** normalized order/event models.

**REJECT:** abstraction that hides material venue differences.

**Confidence:** High.
