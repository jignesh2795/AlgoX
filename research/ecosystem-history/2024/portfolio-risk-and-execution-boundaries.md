# 2024 Research — Portfolio, Risk, and Execution Boundaries

## Status
PROVISIONAL

## Scope
Determine which boundaries repeatedly appear in mature quantitative systems between forecasts, portfolio construction, risk controls, order decisions, and execution.

## Evidence
Qlib documents a workflow separating forecasts/signals, decision generation, portfolio/orders and execution environments. FinRL separates market environments, agents and applications and models transaction costs, liquidity and risk-aversion. LEAN exposes portfolio management, buying power, fill, slippage and margin models as configurable parts of its event-driven engine.

## Findings

### F1 — A forecast is not an order
A model output such as an alpha score, return forecast or risk estimate should not directly become a broker command. A decision layer must translate forecasts into portfolio targets or execution intents.

### F2 — Portfolio construction is distinct from execution
Position sizing, constraints, exposure limits and portfolio objectives operate at a different semantic level from order routing and fills. Combining them makes independent validation difficult.

### F3 — Risk is a control boundary, not merely a model input
Risk limits must be enforceable independently of the strategy/model that generated an intent. This supports deterministic policy checks and emergency controls.

### F4 — Execution quality is part of realized strategy performance
Transaction costs, liquidity, slippage, fill behavior and market impact can materially change the result of a strategy. They should be explicit model inputs and measured separately from signal quality.

### F5 — Production systems benefit from pluggable domain models
The recurring architecture is not one fixed trading algorithm. It is a set of replaceable components with stable contracts: data, signal, portfolio, risk, execution and analysis.

## Canonical boundary
```text
DATA
 ↓
SIGNAL / FORECAST
 ↓
PORTFOLIO DECISION
 ↓
RISK / POLICY GATE
 ↓
EXECUTION INTENT
 ↓
EXECUTOR / BROKER ADAPTER
 ↓
ORDERS / FILLS
 ↓
RECONCILIATION
 ↓
PORTFOLIO STATE
```

The same structure can support deterministic strategies, ML models and agent-generated research decisions without allowing the model itself to bypass policy and execution controls.

## AlgoX decision
**ADOPT** explicit separation of forecast, portfolio, risk and execution semantics.

**ADOPT** risk as an independently enforceable boundary.

**ADOPT** explicit transaction-cost/fill/slippage modeling in research evaluation.

**ADAPT** framework-specific interfaces rather than importing an entire end-to-end framework as the target architecture.

## Confidence
High for architectural separation; exact module boundaries remain an implementation decision for the target system.
