# PX-2023-087 — Corporate Actions and Instrument Identity

**Year:** 2023 evidence / historical capability analysis
**Category:** Data Intelligence / Market Infrastructure
**Status:** Researched

## Finding
Corporate actions and security identity must be modeled as separate, provenance-preserving capabilities. Adjusted historical prices are not sufficient institutional truth: raw observations, adjustment events, effective dates, and affected instruments must remain traceable.

LEAN demonstrates the architectural importance of explicit security/instrument semantics: equity options have contract-specific identity and corporate-action behavior, rather than being treated as generic price series.

## AlgoX implication
A future Indian-market canonical instrument model should distinguish:
- venue/exchange and segment
- underlying instrument
- expiry
- strike
- option right
- contract multiplier/lot size
- broker/provider token
- validity interval
- corporate-action events
- adjustment policy

Provider identifiers are mappings, not canonical identity.

## Evidence
- QuantConnect LEAN option documentation and instrument model.
- Indian-market discovery research retained separately; current repositories are not backdated without dated evidence.

## Decision
**ADOPT** as a capability requirement; implementation remains experiment-gated.
