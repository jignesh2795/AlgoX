# PX-2023-042 — Indian Market-Data Architecture

## Historical role
Indian broker APIs demonstrate that live trading applications commonly consume both normalized quote streams and instrument metadata through provider-specific contracts. Kite Connect provides instrument tokens and WebSocket quote streaming, including LTP, OHLC and market depth; the stream also carries order updates. citeturn0search2turn0search3 Angel One exposes exchange-specific symbol tokens and subscription limits in its streaming contract. citeturn0search0turn0search4

## Architecture observations
- Instrument identity is a first-class domain problem; broker identifiers such as instrument tokens are not universal identifiers.
- Market data contains multiple temporal granularities and evidence levels: LTP, quote, depth, OHLC and order events.
- Subscription limits and connection limits require explicit capacity management.
- Data acquisition and trading decisions should be separated so a broker-feed outage does not silently become a strategy/data-quality failure.

## AlgoX extraction
**Capability:** canonical instrument master + market-data normalization + feed health monitoring.

**Required lineage:**

```text
Exchange / Broker Identifier
        ↓
Instrument Master
        ↓
Canonical Instrument ID
        ↓
Raw Market Event
        ↓
Normalized Event
        ↓
Quality / Timestamp Checks
        ↓
Research / Strategy / Execution
```

## Critical lesson
Never let a broker's symbol token become the canonical instrument identity. Preserve the provider identifier as provenance and map it through a versioned instrument master.

## Decision status
ADOPT as a future financial capability requirement.

## Evidence maturity
C2 — primary broker API documentation; no AlgoX benchmark yet.
