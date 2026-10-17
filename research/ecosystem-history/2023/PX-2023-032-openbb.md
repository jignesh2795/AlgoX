# PX-2023-032 — OpenBB Terminal

## Historical role
OpenBB Terminal was an open-source investment-research workstation with 2023 releases covering market data, filings, forecasting, economics, technical analysis and quantitative workflows. The January 2023 v2.3 release added stock filings and forecasting functionality, while the July 2023 v3.2 release continued modular data/analysis development. citeturn1search12turn1search14

## Architecture observations
- A research workstation can unify heterogeneous financial data and analytical functions behind a common user interface.
- Provider/data-source changes are an architectural concern, not merely configuration.
- The later OpenBB Platform direction explicitly separated core infrastructure, providers and toolkits; this is useful as an evolution signal, but should not be projected backward into the 2023 Terminal architecture. citeturn2search1turn2search4

## AlgoX extraction
**Capability:** provider abstraction and financial research-tool composition.

**Lesson:** data providers should be replaceable modules with standardized contracts. AlgoX should preserve source identity and provenance instead of treating normalized data as source-less truth.

## Decision
ADOPT as a reference pattern for provider abstraction; ASSESS individual OpenBB components rather than adopting the whole platform.

## Evidence maturity
C2 — historical releases and architecture documentation; no AlgoX reproduction yet.
