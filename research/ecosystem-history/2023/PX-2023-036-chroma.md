# PX-2023-036 — Chroma

## Historical role
Chroma was publicly presented in April 2023 as an open-source embedding database designed to make knowledge, facts and skills pluggable for LLM applications. Its early positioning illustrates the rapid emergence of retrieval/memory as a dedicated infrastructure layer in 2023. citeturn2search18

## Architecture observations
- Embeddings became a persistent application subsystem rather than an incidental model output.
- The developer experience emphasized simple insertion and semantic retrieval.
- The project targeted LLM memory/knowledge workflows directly, illustrating how retrieval was becoming a reusable infrastructure primitive.

## AlgoX extraction
**Capability:** developer-friendly semantic memory index.

**Lesson:** semantic indexes are useful for candidate retrieval, but an institutional-memory system needs richer provenance, temporal validity, contradiction handling and deterministic reconstruction than an embedding database alone provides.

## Decision
ASSESS as an early retrieval UX/reference implementation; no change to AlgoX's authoritative-storage design.

## Evidence maturity
C2 — contemporaneous project introduction; no AlgoX benchmark yet.
