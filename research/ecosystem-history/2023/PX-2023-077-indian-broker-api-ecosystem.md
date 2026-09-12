# PX-2023-077 — Indian Broker API Ecosystem

## Historical relevance
The 2023 Indian-market research pass confirms that broker APIs were already exposing the primitives required for automated trading: authentication, order placement/modification/cancellation, portfolio state, historical data and real-time WebSocket feeds. This is ecosystem evidence rather than endorsement of a single broker.

## Evidence
- Zerodha's Kite Connect ecosystem provides REST-style trading and data APIs plus WebSocket streaming and instrument metadata.
- Upstox API v2 is evidenced in 2023 through developer materials and contemporaneous community API collections covering real-time orders, portfolio access and WebSocket market data.
- FYERS has public API/sample-code activity predating 2023 and 2023 ecosystem usage evidence.
- Angel One SmartAPI exposes REST-like trading APIs and WebSocket market-data/order-stream capabilities.

## AlgoX classification
- Domain: Indian financial infrastructure
- Type: broker/API ecosystem
- Historical year: 2023 ecosystem state
- Evidence maturity: C2 — public SDK/API and historical evidence inspection
- Research maturity: M2 — understood provisionally

## Architectural lessons
1. Broker adapters must preserve broker-specific authentication and order semantics.
2. A canonical internal model should not assume that all brokers expose identical event or order-state behavior.
3. WebSocket market data and order updates must be treated as asynchronous event streams.
4. Instrument identity and exchange/segment metadata are foundational dependencies for an Indian-market execution layer.
5. Multi-broker abstractions should normalize common semantics while retaining provider-specific capabilities and constraints.

## AlgoX caution
Current broker SDKs may differ substantially from their 2023 versions. Historical classification must therefore reference the version/evidence date instead of using today's API as a proxy for the 2023 system.

## Sources
- https://github.com/zerodha/pykiteconnect
- https://github.com/upstox/upstox-python
- https://github.com/angel-one/smartapi-python
- https://github.com/FyersDev/fyers-api-sample-code
