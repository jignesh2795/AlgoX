# PX-2023-037 — Freqtrade

## Historical role
Freqtrade represents a mature open-source crypto trading bot architecture in the 2023 ecosystem. Its exchange layer builds on CCXT while retaining exchange-specific behavior where a unified abstraction is insufficient. Its strategy layer exposes market data, order books, balances and execution state to strategies. citeturn0search0turn0search10

## Architecture observations
- Exchange connectivity is separated from strategy logic.
- CCXT provides a common venue interface, but venue-specific order semantics remain explicit.
- Exchange integration requires testing market/limit orders, cancellation, fees, balances and completed trades.
- Incomplete OHLCV candles are treated as a data-quality hazard and excluded where appropriate.

## AlgoX extraction
**Capability:** exchange adapter + strategy boundary + market-data quality controls.

**Lesson:** normalization must not erase venue-specific semantics. Market-data completeness is part of trading correctness, not merely a data-cleaning concern.

## Decision status
ADOPT as a reference pattern; ADAPT for multi-asset/Indian-market architecture.

## Evidence maturity
C2 — project documentation and implementation evidence; AlgoX reproduction pending.
