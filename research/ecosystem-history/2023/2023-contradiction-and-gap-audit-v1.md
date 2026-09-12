# 2023 Contradiction and Gap Audit v1

## Purpose
This audit prevents the 2023 synthesis from treating current implementations as historical evidence and prevents project popularity from being mistaken for capability evidence.

## Strongly supported capability conclusions

### 1. Event-driven execution state
Supported across mature trading-engine research. Order lifecycle, fills, positions and account state should be represented explicitly rather than inferred from strategy-side CRUD state.

### 2. Reconciliation is a first-class capability
NautilusTrader provides a strong reference: venue reports are reconciled against cached/event-sourced state, with duplicate detection, missing-fill reconstruction and position comparison.

### 3. Instrument identity is not the same as provider token
Broker tokens are provider-specific identifiers. A canonical system needs a stable semantic instrument identity plus provider mappings and validity intervals.

### 4. Corporate actions affect data correctness
Adjusted historical data without provenance is insufficient. Adjustment events and their effective scope need to be reconstructable.

### 5. Options and futures require contract semantics
Underlying, expiry, strike, option right, multiplier/lot size and lifecycle are part of instrument identity. They cannot be reduced to an equity-like symbol string.

### 6. Live execution and backtesting have different evidence sources
Backtests control both sides of the simulation. Live systems must reconcile against an external venue and explicitly handle unknown/missing outcomes.

## Contradictions / qualifications

### Popularity vs quality
No contradiction: popularity remains a discovery signal only. It is not evidence of correctness, reliability or production readiness.

### Current Indian projects vs 2023 history
Current unified broker projects are useful capability references, but they do not establish 2023 existence or maturity. They remain separate until dated evidence is found.

### LEAN vs NautilusTrader
They should not be treated as competing implementations of one identical architecture. LEAN provides a broad algorithmic trading engine with rich security, brokerage and asset-class abstractions; NautilusTrader provides especially strong event-driven execution and reconciliation patterns. The difference is architectural emphasis, not a simple winner.

### Adjusted data vs raw data
These are complementary representations, not alternatives. Institutional memory should retain raw observations and adjustment provenance while allowing derived adjusted series.

## Remaining high-value evidence gaps

1. Indian 2023 corporate-action processing implementations with dated evidence.
2. Indian 2023 canonical/security-master implementations.
3. Indian 2023 F&O contract lifecycle and expiry handling.
4. Indian 2023 margin, charges, taxes and buying-power simulation.
5. Indian 2023 realistic fill/partial-fill simulation.
6. Indian 2023 deterministic tick/order-book replay.
7. Indian 2023 broker disconnect and recovery patterns.
8. Indian 2023 multi-broker normalization with historical evidence.
9. Historical release-level evidence for less prominent projects that may fill the above gaps.

## Gate
Do **not** freeze the 2023 synthesis until these remaining gaps have either:
- acquired sufficient dated evidence,
- been explicitly classified as evidence gaps, or
- been shown to be outside the scope of the 2023 ecosystem.

## Current conclusion
2023 is sufficiently researched to identify durable architectural themes, but not yet sufficiently closed to declare complete historical coverage of the Indian-market ecosystem.
