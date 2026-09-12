# PX-2023-019 — Qdrant

## Historical role
Qdrant represents the 2023 emergence of purpose-built vector retrieval infrastructure. Its May 2023 1.2 release emphasized vector-search performance, disk-backed collections, and quantization to reduce memory requirements; by December 2023, Qdrant 1.7 added sparse vectors and a Discovery API. citeturn1search2turn1search1

## Architecture observations
- Vector retrieval was becoming an infrastructure layer rather than an application-local utility.
- Storage/indexing choices were exposed as engineering trade-offs involving memory, latency, scale, and search quality.
- Sparse and dense retrieval capabilities increasingly converged, anticipating hybrid retrieval architectures.
- The system demonstrates why semantic retrieval should be treated as a derived capability with measurable operational characteristics.

## Research value
High for retrieval infrastructure, especially when comparing standalone vector systems with relational/vector extensions and hybrid lexical-semantic search.

## AlgoX extraction
**Potential capability:** semantic retrieval index.

**Lesson:** embeddings are an index/projection, not institutional truth. Canonical evidence and provenance must survive independently of the vector store.

## Evidence
- Qdrant 1.2 release, May 2023. citeturn1search2
- Qdrant 1.7 release, December 2023, including sparse vectors and Discovery API. citeturn1search1

## Decision status
ASSESS — retain as a benchmark candidate for semantic retrieval; do not make a standalone vector database authoritative in AlgoX.

## Evidence maturity
C2 — official project release documentation; no AlgoX benchmark yet.
