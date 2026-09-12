# PX-2023-029 — Weaviate

## Historical role
Weaviate was an established vector database before 2023, but its 2023 evolution is important to the historical research because it increasingly positioned vector search as infrastructure for RAG and long-term AI memory. Its 2023 archive shows work on HNSW, product quantization, hybrid search, production monitoring, RAG evaluation, and multimodal retrieval. citeturn0search2turn0search0

## Architecture observations
- Vector search was moving from a standalone similarity primitive toward a broader retrieval platform.
- Hybrid search combined semantic and lexical signals.
- Quantization demonstrated that retrieval quality, memory footprint, and cost are coupled engineering variables.
- RAG externalized model knowledge into an updateable retrieval layer; multimodal RAG extended the same principle beyond text. citeturn0search0

## AlgoX extraction
**Capability:** hybrid semantic/lexical retrieval with derived indexes.

**Lesson:** retrieval should expose multiple evidence paths. AlgoX should retain exact/lexical, semantic, graph, temporal and provenance retrieval rather than depending on one embedding representation.

## Decision
ASSESS — strong historical reference for retrieval architecture; use as a benchmark candidate, not as the authoritative knowledge store.

## Evidence maturity
C2 — official 2023 archive and technical material; AlgoX benchmark pending.
