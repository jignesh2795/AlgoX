# PX-2023-078 — Indian NSE/BSE Data Projects

## Classification
- Year: 2023
- Domain: Financial / Quantitative / Indian Market Data
- Type: Ecosystem capability record
- Status: historical evidence confirmed

## Evidence
GitHub topic and repository evidence shows multiple Indian-market data projects with activity during 2023. NSEDownload was updated in December 2023; NSEazy was updated in June 2023; NSE-Py was updated in July 2023; and NSE_TRADER was updated in November 2023.

These projects expose programmatic access to NSE data, historical prices, indices, bhavcopy-style data and strategy research. They are smaller ecosystem components rather than full trading engines.

## Capability signals
- exchange-data acquisition
- historical-data download
- bhavcopy ingestion
- NSE index/security data
- basic research pipelines
- local/open-source access to Indian market data

## Architectural lesson
Indian-market infrastructure should treat exchange-data acquisition as a separate capability from broker execution. A broker API is not a substitute for an independent historical-data and reference-data layer.

## AlgoX interpretation
The 2023 Indian ecosystem was fragmented: small data libraries, broker APIs and strategy projects existed independently. This is useful evidence for designing canonical data/reference-data boundaries rather than assuming one provider can supply the complete institutional data model.

## Sources
- GitHub NSE stock-data topic: https://github.com/topics/nse-stock-data
- GitHub national-stock-exchange topic: https://github.com/topics/national-stock-exchange

## Confidence
Medium-high for ecosystem activity; low for production-readiness. Repository activity demonstrates existence and use cases, not institutional data quality.