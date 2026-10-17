# PX-2023-005 — LlamaIndex

**Repository:** https://github.com/run-llama/llama_index
**Historical category:** SUSTAINED
**Domain:** Data / retrieval / LLM applications

## 2023 signal
LlamaIndex emerged in the 2023 wave around connecting LLMs with private and external data. The later project documentation describes its original role as a data framework for ingesting data, structuring it into indexes, and providing retrieval/query interfaces.

## Capability observed
The architecture separates data ingestion/connectors, indexing, retrieval/query engines, and the LLM application layer.

## Architectural lesson
Context/data access should be treated as an explicit subsystem rather than embedding retrieval logic inside every application.

## AlgoX extraction
- Data connector abstraction
- Indexing layer
- Retrieval abstraction
- Context augmentation
- Separation of data access from model/application logic

## Evidence
Repository: https://github.com/run-llama/llama_index
Project documentation: https://github.com/run-llama/llama_index/blob/main/docs/src/content/docs/framework/index.md

**Evidence maturity:** C1
**Status:** RESEARCHED
