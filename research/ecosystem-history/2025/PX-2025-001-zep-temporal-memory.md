# PX-2025-001 — Zep / Graphiti: Temporal Agent Memory

**Status:** PROVISIONAL
**Research period:** 2025
**Domain:** agent memory / temporal knowledge graphs

## Why it matters

Zep's 2025 architecture is an important evolution from flat semantic memory toward a temporal knowledge graph. The paper describes Graphiti as a temporally aware graph that integrates conversational and structured business data while preserving historical relationships. It reports 94.8% vs 93.4% on DMR and substantial gains on LongMemEval; these are reported benchmark results from the authors and should not be treated as universal superiority. citeturn0search7

Zep Community Edition had already open-sourced a Graphiti-backed memory layer in September 2024, progressively building and updating a temporal graph from chat, tool use, and structured/unstructured data. citeturn0search4

## Architectural lesson

The important pattern is:

```text
experience / source
        ↓
entity + relationship + fact extraction
        ↓
temporal + provenance-aware graph
        ↓
retrieval using multiple signals
        ↓
compact context for reasoning
```

Zep documentation describes episodic nodes, entity nodes, and relationship/fact edges as distinct graph primitives. citeturn0search2

## AlgoX adaptation

AlgoX should use the same **conceptual model**, without committing to Zep, Graphiti, or a graph database as the primary storage technology.

Every important knowledge item should support:

- source/evidence provenance;
- observed/ingested time;
- valid-from / valid-to where applicable;
- supersession rather than destructive overwrite;
- contradiction relationships;
- confidence/evidence maturity;
- point-in-time reconstruction.

This is especially important for finance because broker APIs, exchange rules, fees, taxes, instrument metadata, and regulatory constraints change.

## Decision

**ADAPT:** temporal knowledge-graph semantics.

**DO NOT YET ADOPT:** a dedicated graph database as AlgoX's system of record.

Reason: the semantics are required now; the specialized storage engine is an implementation hypothesis that should be earned through workload evidence.

**Confidence:** High on temporal/provenance requirements; medium on the eventual graph-storage choice.
