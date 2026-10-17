# PX-2024-013 — RAG Evaluation Survey

**Source:** https://arxiv.org/abs/2405.07437
**Historical category:** Research methodology
**Domain:** RAG evaluation

## 2024 signal
The survey identified the hybrid nature of RAG evaluation: retrieval and generation have distinct measurable properties, while dynamic external knowledge makes evaluation and benchmark design difficult.

## Capability observed
Useful evaluation dimensions include retrieval relevance, generation accuracy, faithfulness, and additional task requirements. Benchmarks need explicit definitions of what constitutes a successful result.

## Architectural lesson
AlgoX must distinguish:

1. source retrieval quality,
2. evidence selection quality,
3. synthesis quality,
4. factual/claim correctness,
5. decision usefulness.

A fluent answer is not sufficient evidence of a successful research run.

## AlgoX extraction
- Layered evaluation model
- Retrieval metrics
- Generation metrics
- Faithfulness checks
- Benchmark-design discipline
- Explicit success criteria

## Relevance to AlgoX
Very high. This becomes part of the design basis for evidence-aware retrieval and research-run evaluation.

## Evidence
Yu et al., 2024, *Evaluation of Retrieval-Augmented Generation: A Survey*.

**Evidence maturity:** C2
**Status:** RESEARCHED
