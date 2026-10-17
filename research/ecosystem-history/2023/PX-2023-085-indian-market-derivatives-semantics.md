# PX-2023-085 — Indian derivatives semantics

## Classification
- Year: 2023 ecosystem evidence
- Domain: Indian F&O
- Capability: Contract identity, expiry, strike, option type, lot size and margin semantics
- Evidence maturity: C1

## Finding
Indian derivatives cannot be modeled as ordinary equity symbols. A canonical contract identity needs underlying, instrument type, expiry, strike, option type, exchange/segment and effective instrument metadata. Historical research must also account for expired contracts and changing contract specifications.

## AlgoX implication
Instrument-master ingestion and derivative-contract lifecycle should be independent capabilities from broker connectivity. Broker adapters should resolve provider tokens to canonical contracts rather than becoming the canonical identity store.

## Decision
ADOPT as an architectural requirement; benchmark and reproduction required before implementation selection.
