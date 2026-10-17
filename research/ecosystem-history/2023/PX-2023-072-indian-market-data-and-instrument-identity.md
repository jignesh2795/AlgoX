# PX-2023-072 — Indian Market Data and Instrument Identity

## Research question

What must a trading platform preserve when normalizing Indian broker/exchange market data?

## Finding

Market data normalization is not merely a field-mapping exercise. A canonical market-data layer needs stable instrument identity, exchange/segment context, contract metadata, temporal validity and provenance before derived bars/features can be trusted.

## Reference evidence

The Zerodha Kite Connect client exposes an instrument-master surface, exchange-specific instrument routes, historical data, quotes, LTP and WebSocket streaming. Its API constants distinguish NSE, BSE, NFO, CDS, BFO, MCX and BCD, demonstrating that venue/segment identity is part of the contract rather than incidental metadata.

## Proposed canonical identity

```text
InstrumentIdentity
├── canonical_security_id
├── venue
├── segment
├── symbol / trading symbol
├── instrument token / provider identity
├── contract type
├── expiry
├── strike
├── option type
├── lot size
├── currency
├── valid_from
└── valid_to
```

## Derived-data boundary

```text
Raw provider observation
        ↓
Provider identity
        ↓
Canonical instrument identity
        ↓
Corporate-action / contract normalization
        ↓
Quality validation
        ↓
Canonical market data
        ↓
Features / backtests
```

## AlgoX decision

**ADOPT** instrument identity as a first-class capability.

**ADOPT** provider provenance and effective-time metadata.

**REJECT** using a display symbol alone as the durable identity of an Indian financial instrument.

## Evidence maturity

C2 — primary client/API inspection, with broader exchange and broker evidence required before production design is finalized.

## Sources

- https://github.com/zerodha/pykiteconnect
- https://github.com/zerodha/pykiteconnect/blob/master/kiteconnect/connect.py
