# PX-2023-084 — Indian-market corporate actions as a data-correctness capability

## Classification
- Year: 2023 ecosystem evidence
- Domain: Financial data / Indian markets
- Capability: Corporate-action normalization
- Evidence maturity: C1 pending deeper reproduction

## Finding
Corporate actions must be represented as first-class market-data events rather than treated as incidental metadata. Dividends, splits, bonuses, rights issues and symbol/instrument changes can change the economic meaning of historical prices and positions.

## AlgoX implication
A future Indian-market research/trading stack should preserve raw observations and separately maintain adjustment events. Adjusted series must remain traceable to the underlying action and effective dates.

## Boundary
This record does not claim that every current NSE API wrapper existed in 2023. Current repositories are discovery evidence only unless their historical activity is independently established.

## Decision
ADOPT as a capability requirement; implementation deferred to an experiment.
