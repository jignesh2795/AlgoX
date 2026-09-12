# 2024 Research — Data Quality and Corporate Actions

## Status
PROVISIONAL

## Scope
Cross-check 2024-era quant platforms and production-finance evidence for market-data correctness, corporate actions, survivorship, identity, and derived-data governance.

## Evidence
- LEAN documents explicit handling of splits, dividends, mergers, listings/delistings and other corporate actions, and provides configurable slippage, fill and margin models.
- Qlib separates its data infrastructure from learning and workflow layers and warns that public datasets may be imperfect; users with higher-quality data should prepare their own datasets.
- FinRL's environment model explicitly incorporates transaction costs, liquidity and risk constraints.
- Production finance literature treats corporate-action processing as a material operational problem for multi-asset and multi-broker portfolios.

## Findings

### F1 — Raw market data and adjusted research data are different artifacts
A historical price used for research may be transformed by corporate actions, survivorship treatment, or normalization. The raw observation must remain recoverable rather than being overwritten by a derived adjustment.

### F2 — Corporate actions are part of market-data correctness
Splits, dividends, mergers, delistings and symbol/instrument changes can alter the meaning of historical observations. They belong in the data model and evidence chain, not in an ad-hoc preprocessing script.

### F3 — Instrument identity is temporal
A symbol or broker identifier is not sufficient as a permanent identity. AlgoX should preserve canonical identity plus effective intervals and source-specific identifiers.

### F4 — Data quality must be measurable
At minimum, a production-grade research dataset needs gap detection, duplicate detection, timestamp validation, stale-feed detection, corporate-action reconciliation, and provenance.

### F5 — Backtest correctness depends on data semantics
A fast backtest on incorrectly adjusted or incomplete data can produce a highly reproducible but invalid result. Reproducibility does not compensate for invalid source data.

## Architectural implication
```text
RAW OBSERVATIONS
      ↓
SOURCE / VENUE PROVENANCE
      ↓
IDENTITY + CORPORATE ACTIONS
      ↓
QUALITY VALIDATION
      ↓
DERIVED / ADJUSTED DATASETS
      ↓
RESEARCH FEATURES
      ↓
MODEL / BACKTEST
```

Raw observations and derived views must not be collapsed into one mutable representation.

## AlgoX decision
**ADOPT** the separation of raw evidence from derived market-data views.

**ADOPT** temporal instrument identity and corporate actions as first-class research entities.

**ADOPT** explicit data-quality evidence before a dataset can be used for a high-confidence benchmark.

**HOLD** any specific database/streaming technology choice until workload benchmarking.

## Confidence
High for architectural principle; implementation details remain domain and venue specific.
