# PX-2024-004 — LlamaIndex

**Repository:** https://github.com/run-llama/llama_index
**Historical category:** SUSTAINED / retrieval infrastructure
**Domain:** RAG / data / agent applications

## Historical signal
LlamaIndex evolved from the 2023 data-framework concept into a broader ecosystem for retrieval, data connectors, indexing, query engines, and agent-oriented workflows.

## Capability observed
The architecture keeps data ingestion, indexing, retrieval, reranking/query logic, and model/application orchestration as separable concerns with an integration ecosystem around the core.

## Architectural lesson
Context engineering is a system layer. Applications should not have to implement every connector, indexing strategy, retrieval mechanism, and provider integration themselves.

## AlgoX extraction
- Connector abstraction
- Indexing layer
- Retrieval/query abstraction
- Context augmentation
- Integration/plugin architecture
- Separation of knowledge access from model reasoning

## Relevance to AlgoX
Directly relevant to AlgoX's evidence and institutional-memory problem: source ingestion, normalization, indexing, retrieval, provenance, and reasoning should remain distinguishable layers.

## Evidence
Repository documentation: https://github.com/run-llama/llama_index

**Evidence maturity:** C2
**Status:** RESEARCHED
