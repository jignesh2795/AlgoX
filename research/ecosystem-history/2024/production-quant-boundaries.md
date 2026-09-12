# 2024 Production Quantitative Boundaries

## Status
PROVISIONAL.

## Core finding
The 2024 cross-check strengthens a separation that should remain fundamental in AlgoX: **research capability, decision capability and execution capability are different evidence domains.**

A quantitative framework can be excellent for feature research while being unsuitable as an execution engine. Conversely, an execution engine can model order lifecycle and corporate actions well without being the best environment for ML experimentation.

## Capability boundaries

### Research
- datasets and feature generation
- model training
- signal evaluation
- experiment tracking
- parameter studies
- statistical analysis

### Decision
- portfolio construction
- position sizing
- risk overlays
- target holdings/orders
- policy constraints

### Execution
- order lifecycle
- broker/exchange adapters
- retries and idempotency
- partial fills
- reconciliation
- market-session constraints

### Governance
- provenance
- evidence
- approvals
- audit
- historical reconstruction
- policy enforcement

## Important contradiction
A single framework may advertise an end-to-end workflow, but end-to-end availability does not imply that every component has equal maturity.

AlgoX therefore evaluates capabilities independently instead of assigning a single quality score to a project.

## Decision rule
When comparing a framework:

```text
Project quality
    ≠
Research quality + execution quality + production quality as one score
```

Instead:

```text
Project
 ├── research capability score
 ├── simulation capability score
 ├── execution capability score
 ├── reliability score
 ├── reproducibility score
 └── evidence maturity
```

## Consequence for future target systems
A future QuantumTrade architecture should be able to reuse a research framework without inheriting its execution assumptions, and reuse an execution framework without coupling the research layer to it.

## Evidence discipline
Current documentation of Qlib, LEAN and FinRL supports the architectural decomposition, but current implementations must not be treated as proof of historical 2024 behavior without version-specific source inspection.
