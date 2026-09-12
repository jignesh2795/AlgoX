# PX-2023-075 — NautilusTrader

## Historical relevance
NautilusTrader is directly evidenced as an active algorithmic-trading platform in 2023. Its 2023 beta releases show a strongly event-driven architecture with explicit market-data, order, execution, actor and risk concepts, while progressively moving performance-sensitive components into Rust.

## 2023 evidence
- v1.175.0 beta was released June 16, 2023.
- That release integrated a Rust order book, OrderBookDelta, Rust HTTP/WebSocket/socket clients and an Interactive Brokers adapter v2.
- v1.177.0 beta in August 2023 added actor execution facilities, emulated/released order events and execution-engine fixes.
- v1.179.0 beta in October 2023 added ParquetDataCatalog v2, strategy/execution event handlers, RiskEngine notional limits, dynamic controllers, fill reporting and WebSocket improvements.

## AlgoX classification
- Domain: financial / quantitative infrastructure
- Type: event-driven trading platform / backtester / execution runtime
- Historical year: 2023
- Evidence maturity: C2 — release/source inspection
- Research maturity: M2 — understood provisionally

## Architectural lessons
1. Model market data, orders, execution and risk as explicit event-driven domains.
2. Use precise domain types such as QuoteTick, TradeTick, OrderBookDelta and explicit order states.
3. Separate strategy/event handling from execution infrastructure.
4. Performance-critical paths can be implemented in a lower-level language while preserving a higher-level research interface.
5. Data catalogs and persistence formats are part of trading-system architecture, not merely research utilities.

## AlgoX caution
The 2023 API was still beta and subject to breaking changes. AlgoX should therefore extract concepts and evidence-backed patterns rather than copying the API wholesale.

## Sources
- https://newreleases.io/project/github/nautechsystems/nautilus_trader/release/v1.175.0
- https://newreleases.io/project/github/nautechsystems/nautilus_trader/release/v1.177.0
- https://newreleases.io/project/github/nautechsystems/nautilus_trader/release/v1.179.0
- https://github.com/nautechsystems/nautilus_trader
