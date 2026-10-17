# PX-2023-070 — Zerodha Kite Connect / pykiteconnect

## Historical role

Official Indian broker API client and one of the clearest reference implementations for a broker-facing trading interface in the 2023 ecosystem. The repository exposes REST-style trading, portfolio, instrument, quote and historical-data APIs plus WebSocket market-data streaming.

## Evidence

Primary implementation: `zerodha/pykiteconnect`.
The repository describes Kite Connect as APIs for real-time order execution, portfolio management and live market data, with Python client abstractions and examples. The client uses an explicit login/session flow, typed constants for products/order types/exchanges, REST route mappings, and a separate WebSocket client.

A repository file shows a July 2023 implementation state and a 7-second default HTTP timeout, explicit order/product/exchange constants, REST route mappings, and session-token endpoints.

## Architecture observations

- Broker API wrapper rather than a complete trading engine.
- Authentication/session lifecycle is explicit.
- REST and streaming surfaces are distinct.
- Broker/venue semantics remain visible through product, order-type, exchange and variety constants.
- Instrument identity is exposed through broker-provided instrument data.
- Order placement returns broker identifiers; downstream lifecycle handling belongs to the application using the client.

## AlgoX extraction

### Capabilities

- broker connectivity
- authentication/session management
- order command surface
- portfolio/account queries
- historical market-data access
- WebSocket market-data streaming
- instrument-master acquisition
- explicit venue/product semantics

### Architectural lesson

A broker adapter should not pretend to be a trading engine. It should expose a stable integration boundary while retaining venue-specific semantics required for correct execution.

### Reliability lesson

The client abstraction alone does not establish canonical order state. Command responses and asynchronous order/trade events remain observations that a higher-level OMS/reconciliation layer must interpret.

## AlgoX decision

**ADOPT architectural boundary; ADAPT broker-specific contract patterns.**

Do not copy the broker API as the canonical trading model. Build a canonical internal contract plus an explicit venue-specific escape hatch.

## Evidence maturity

C2 — primary source-code/documentation inspection. Production usage is not inferred from repository popularity.

## License

MIT according to the repository metadata.

## Temporal note

The repository predates 2023; this record is included in the 2023 historical ecosystem because the client and its architecture were active/relevant during the period studied. Historical year is therefore the ecosystem-observation year, not the original project creation year.

## Sources

- https://github.com/zerodha/pykiteconnect
- https://github.com/zerodha/pykiteconnect/blob/master/kiteconnect/connect.py
