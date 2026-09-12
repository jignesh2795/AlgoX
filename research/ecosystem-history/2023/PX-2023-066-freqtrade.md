# PX-2023-066 — Freqtrade

## Classification
- Year: 2023
- Domain: algorithmic trading / crypto execution
- Research status: discovery record
- Evidence maturity: C1

## Historical relevance
Freqtrade is a mature open-source trading framework combining strategy development, backtesting, dry-run and exchange-connected execution. Its value for AlgoX is the explicit relationship between research/simulation and operational execution.

## Capability extraction
- strategy interface
- backtesting
- dry-run/paper execution
- exchange adapter boundary
- position and order management
- configurable risk controls

## AlgoX relevance
Provides another implementation to compare against LEAN, Hummingbot, NautilusTrader and broker APIs. Particular focus should be placed on simulation/live parity, exchange semantics and failure handling.

## Decision
ADAPT — extract lifecycle and validation patterns; do not treat the framework as a universal trading-engine answer.
