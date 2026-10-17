# PX-2024-014 — RAG Architecture Survey

**Source:** https://arxiv.org/abs/2404.10981
**Historical category:** Retrieval architecture
**Domain:** Retrieval-augmented generation

## 2024 signal
The 2024 RAG literature increasingly treated retrieval as a multi-stage system: pre-retrieval processing, retrieval, post-retrieval processing, and generation.

## Capability observed
Retrieval quality is affected by query preparation, indexing/chunking, candidate retrieval, reranking/context selection, and how the generator uses the resulting context.

## Architectural lesson
AlgoX should not implement a single generic `search()` abstraction and assume it solves evidence retrieval. The research pipeline needs explicit stages and measurable boundaries.

## AlgoX extraction
- Query preparation
- Retrieval
- Reranking/context selection
- Evidence packaging
- Generation/synthesis separation
- Retrieval pipeline evaluation

## Relevance to AlgoX
High. This supports a modular evidence-retrieval architecture capable of comparing different retrieval strategies rather than coupling the knowledge system to one vector database or embedding model.

## Evidence
Huang & Huang, 2024, *A Survey on Retrieval-Augmented Text Generation for Large Language Models*.

**Evidence maturity:** C2
**Status:** RESEARCHED
