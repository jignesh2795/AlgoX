# PX-2023-050 — Backtesting Validation Boundary

**Period:** 2023
**Domain:** Quant research / backtesting
**Status:** Historical research record

## Observation

2023-era open-source trading systems demonstrate that backtesting is a research accelerator, not proof of live profitability. Freqtrade explicitly separates historical backtesting from dry-run/forward testing and warns that backtests can distort results. Vectorized systems such as vectorbt optimize research throughput and large-scale idea exploration, but throughput does not itself establish execution fidelity.

## Evidence

- Freqtrade documentation describes historical-data backtesting and separate real-time dry-run/forward testing.
- Vectorbt emphasizes rapid exploration of large numbers of trading ideas.
- Trading-system research generally requires explicit treatment of fees, slippage, liquidity, data quality, and execution assumptions.

## Finding

Backtesting must be treated as a simulation layer with explicit assumptions rather than as an authoritative statement about future trading performance.

## AlgoX implication

A future capability model should distinguish:

1. research-speed backtesting;
2. event-driven execution simulation;
3. market-impact/fill modeling;
4. walk-forward/forward testing;
5. live-vs-simulation parity;
6. post-trade attribution and reconciliation.

## Decision

**ADOPT:** explicit simulation assumptions and validation stages.

**ADAPT:** high-throughput vectorized research where useful.

**REJECT:** treating a single backtest result as production evidence.

## Confidence

High for the architectural boundary; individual performance claims remain strategy- and dataset-dependent.
