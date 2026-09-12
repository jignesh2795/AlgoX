# PX-2023-052 — Research-to-Live Parity

**Period:** 2023
**Domain:** Trading architecture
**Status:** Historical research record

## Finding

The 2023 ecosystem shows a recurring boundary between research engines and live execution systems. Qlib and vectorbt optimize quantitative research workflows; Freqtrade and LEAN provide stronger paths toward executable trading; broker APIs expose venue-specific connectivity. No single layer should silently assume that research semantics equal broker execution semantics.

## Architectural consequence

The future platform should preserve a common conceptual model while allowing different execution semantics:

```text
Research Model
    ↓
Strategy Intent
    ↓
Portfolio / Risk
    ↓
Execution Model
    ↓
Venue Adapter
    ↓
Broker / Exchange
```

Simulation should consume the same canonical intent where possible, but its fill, latency, liquidity, fee, and market-impact models must remain explicit.

## Validation requirements

- same instrument identity
- same strategy inputs
- same order intent schema
- same portfolio/risk semantics
- explicit simulation assumptions
- explicit live-only constraints
- comparison of simulated and observed events

## Decision

**ADOPT:** shared canonical contracts between research and execution.

**REJECT:** assuming identical behavior between backtest and live broker execution.

**Confidence:** High at architectural level.
