# PX-2023-044 — Exchange Data Governance

## Historical role
Exchange market data is subject to explicit usage and distribution policies. NSE's market-data policy describes rules governing data usage and distribution by market participants and subscribers. citeturn0search10

## Architecture observations
- Market data is not merely a technical feed; licensing and permitted use are part of system requirements.
- Data provenance must include source, entitlement/context, observation time and transformation history.
- A research archive should distinguish raw market data from derived indicators and internally generated datasets.
- Data retention and redistribution decisions can affect architecture before storage technology is selected.

## AlgoX extraction
**Capability:** data-provenance and entitlement metadata.

```text
Source
  ↓
Entitlement / Usage Terms
  ↓
Raw Dataset
  ↓
Transformation
  ↓
Derived Dataset
  ↓
Experiment / Finding
```

## Critical lesson
For financial research, data provenance is partly a legal/commercial property. AlgoX must not treat a technically accessible dataset as automatically reusable or redistributable.

## Decision status
ADOPT as a research-governance requirement; investigate exact licensing before any future dataset ingestion or publication.

## Evidence maturity
C2 — exchange policy evidence; specific licensing decisions remain context-dependent.
