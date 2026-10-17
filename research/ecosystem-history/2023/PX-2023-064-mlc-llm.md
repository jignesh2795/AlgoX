# PX-2023-064 — MLC LLM

## Classification
- Year: 2023
- Domain: local inference / compiler infrastructure
- Research status: discovery record
- Evidence maturity: C1

## Historical relevance
MLC LLM demonstrated the importance of compiling and deploying language models across heterogeneous hardware and runtimes rather than coupling applications to one inference backend.

## Capability extraction
- model compilation
- heterogeneous hardware deployment
- runtime portability
- local inference
- performance-aware deployment

## AlgoX relevance
Supports the separation of model logic from inference runtime. Future AlgoX agents should be able to route tasks across local and remote inference backends without changing research semantics.

## Decision
ADAPT — preserve runtime/provider abstraction as a first-class boundary.
