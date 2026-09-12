# PX-2023-035 — Milvus

## Historical role
Milvus 2.3 was a major 2023 vector-database release. It added GPU indexing, Arm64 support, upsert, change-data-capture, ScaNN, MMap, improved query performance, load balancing, scheduling, observability and operational tooling. citeturn2search3turn2search5

## Architecture observations
- Vector search was becoming production infrastructure rather than a notebook-only component.
- Indexing, storage, scheduling, consistency, observability and recovery became first-class concerns.
- GPU acceleration exposed an explicit cost/latency/throughput trade-off.
- Data lifecycle operations such as upsert and CDC matter when embeddings are continuously updated.

## AlgoX extraction
**Capability:** scalable semantic retrieval infrastructure.

**Lesson:** retrieval architecture must account for lifecycle, updates, observability and consistency—not only nearest-neighbor search quality.

## Decision
ASSESS as a retrieval benchmark candidate. It does not change the current AlgoX decision that canonical evidence remains outside vector infrastructure.

## Evidence maturity
C2 — official Milvus 2.3 release evidence; no AlgoX workload benchmark yet.
