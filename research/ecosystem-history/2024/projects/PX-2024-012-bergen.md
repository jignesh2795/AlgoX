# PX-2024-012 — BERGEN

**Repository:** https://github.com/naver/bergen
**Historical category:** RAG benchmarking infrastructure
**Domain:** Retrieval / generation research

## 2024 signal
BERGEN addressed a recurring problem in RAG research: inconsistent combinations of datasets, collections, retrievers, rerankers, LLMs, and metrics make results difficult to compare. It proposed a reproducible end-to-end benchmarking library.

## Capability observed
The benchmark configuration itself must be captured as part of evidence. A result without dataset, retriever, reranker, model, metrics, and configuration provenance is weak evidence.

## Architectural lesson
AlgoX experiments should be configuration-addressable and reproducible. Research claims should point to the exact experiment configuration that produced them.

## AlgoX extraction
- Reproducible RAG experiments
- Benchmark configuration provenance
- Retriever/reranker/model comparison
- Standardized evaluation
- Experiment reproducibility

## Relevance to AlgoX
Very high. This directly informs the experiment and benchmark registry and the evidence graph.

## Evidence
BERGEN, Findings of EMNLP 2024: https://aclanthology.org/2024.findings-emnlp.449/

**Evidence maturity:** C2
**Status:** RESEARCHED
