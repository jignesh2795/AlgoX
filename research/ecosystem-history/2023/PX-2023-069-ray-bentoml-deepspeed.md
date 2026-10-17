# PX-2023-069 — Ray Serve / BentoML / DeepSpeed

## Classification
- Year: 2023
- Domain: model serving / distributed infrastructure
- Research status: comparative discovery record
- Evidence maturity: C1

## Historical relevance
Ray Serve, BentoML and DeepSpeed represent complementary approaches to productionizing ML workloads: distributed serving, packaging/deployment and high-performance distributed model execution/training.

## Capability extraction
- model serving
- batching and scheduling
- distributed execution
- deployment packaging
- hardware-aware optimization
- production observability boundaries

## AlgoX relevance
These systems reinforce that inference is an infrastructure layer separate from reasoning and research semantics. AlgoX's future compute policy should be able to select or replace serving backends.

## Decision
ADAPT — retain the serving/runtime abstraction; assess individual runtimes through later benchmarks.
