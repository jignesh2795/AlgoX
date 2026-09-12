# PX-2023-039 — CCXT vs LEAN architectural boundary

## Research question
What should be unified at the exchange-connectivity layer, and what must remain inside the trading engine?

## Finding
CCXT is a unified exchange client rather than a complete trading engine. LEAN provides event-driven backtesting/execution, portfolio construction, risk and execution models. The distinction is architectural: a connector normalizes venue access; the engine owns trading semantics. citeturn0search5

## Implication for AlgoX / future target systems
The broker abstraction should expose a stable canonical contract for connectivity while retaining a venue-specific escape hatch for parameters and behaviors that cannot safely be normalized.

## Proposed boundary
```text
Strategy / AI decision
        ↓
Canonical Order Intent
        ↓
Risk / Portfolio Policy
        ↓
Execution Engine
        ↓
Broker Adapter
        ↓
Venue API
```

Do not allow the broker adapter to become the place where portfolio or strategy semantics are hidden.

## Decision status
ADOPT as an architecture principle for later QuantumTrade-related research.

## Evidence maturity
C2 — comparative official documentation; implementation benchmark still required.
