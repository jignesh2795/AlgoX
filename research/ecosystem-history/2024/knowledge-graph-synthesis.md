# 2024 — Knowledge Graph, Provenance, and Temporal Research Synthesis

**Status:** PROVISIONAL

## Executive finding

A useful institutional knowledge system cannot be modeled as a static graph of entities and relationships. Research knowledge changes: sources are updated, projects evolve, claims are superseded, experiments change confidence, and competing findings may coexist under different assumptions.

2024 temporal-knowledge-graph research reinforces the need to represent validity intervals and evolving relationships rather than treating every fact as timeless. Provenance research likewise shows that traceability of changes is a first-class requirement when knowledge must be audited or reproduced.

## AlgoX principle

> **The knowledge graph stores claims and relationships; the evidence system stores why those claims are believed, when they were valid, where they came from, and how they changed.**

## Proposed research knowledge model

```text
Source
  ↓ supports
Evidence
  ↓ supports
Claim
  ↓ interpreted_as
Finding
  ↓ tested_by
Experiment
  ↓ produces
Result
  ↓ informs
Decision
  ↓ affects
Capability
```

Temporal dimensions should exist on claims, evidence, source versions, project observations, and decisions.

## Temporal model

Each knowledge assertion should distinguish at least:

- `observed_at` — when AlgoX observed the information
- `published_at` — when the source was published
- `valid_from` — when the assertion became applicable
- `valid_to` — when it stopped being applicable, if known
- `superseded_at` — when a later assertion replaced it
- `source_version` — version, commit, release, or document revision

This prevents historical research from silently replacing past truth with today's state.

## Provenance model

Every material claim should be traceable to one or more evidence objects.

```text
Claim C-001
├── Evidence E-001
│   ├── source: paper
│   ├── locator: page/section
│   ├── retrieved_at
│   └── source_version
├── Evidence E-002
│   └── implementation/test
└── Verification V-001
    └── experiment EXP-001
```

A claim without provenance may remain a hypothesis, but should not silently become an institutional fact.

## Contradiction model

AlgoX should preserve disagreement rather than flattening it.

```text
Claim A: technique improves latency
  ├── Evidence A1: benchmark under workload X
  └── Evidence A2: implementation test

Claim B: technique increases latency
  ├── Evidence B1: workload Y
  └── Evidence B2: production report

Resolution
  └── conditional finding:
      improvement depends on workload, hardware, and configuration
```

Contradictions should therefore be classified as:

- direct contradiction
- different time period
- different implementation
- different dataset
- different market regime
- different metric definition
- different assumptions
- incomplete evidence
- genuine unresolved disagreement

## Revisions and supersession

Never delete an old claim merely because a newer claim exists.

Use:

```text
SUPERSEDES
REFUTES
QUALIFIES
EXTENDS
CORRECTS
DUPLICATES
```

This creates institutional memory instead of a constantly rewritten summary.

## Knowledge graph boundary

The graph should not attempt to contain every document or every token. It should contain durable research entities and relationships:

- projects
- algorithms
- capabilities
- technologies
- architectures
- requirements
- findings
- claims
- evidence
- experiments
- benchmarks
- decisions
- failures
- dependencies
- source versions

Raw documents and extracted passages belong in the source/evidence store and can be indexed for retrieval.

## Retrieval architecture

```text
Research Question
       ↓
Query Planner
       ↓
Hybrid Retrieval
 ┌─────┼─────┐
 │     │     │
Text  Graph  Metadata
 │     │     │
 └─────┼─────┘
       ↓
Temporal / Provenance Filtering
       ↓
Evidence Ranking
       ↓
Evidence Bundle
       ↓
Reasoning
       ↓
Claim Extraction
       ↓
Contradiction Check
       ↓
Verification
```

Vector search is therefore only one retrieval mechanism. Exact metadata, graph traversal, temporal filters, source authority, and provenance are equally important.

## Decision implications for AlgoX

1. Build an evidence registry before optimizing semantic retrieval.
2. Treat temporal validity as a core data property.
3. Preserve superseded claims and source versions.
4. Store contradictions explicitly.
5. Link decisions to the evidence and experiments that justified them.
6. Keep raw source artifacts separate from derived knowledge.
7. Make every generated finding auditable.
8. Do not allow an LLM to silently overwrite institutional knowledge.

## Relevance to finance

The temporal model is especially important for financial research. Broker APIs, exchange rules, fees, order types, instrument definitions, market hours, regulations, and software behavior change over time. A statement can be correct for one date and wrong for another.

AlgoX should therefore answer both:

- "What is true now?"
- "What did we believe, and what evidence supported it, at time T?"

## Evidence base

- 2024 survey work on temporal knowledge graph representation and applications
- 2024 survey work on temporal knowledge graph embeddings
- 2024 work on full traceability and provenance for knowledge graphs
- 2024 work on time-aware retrieval for temporal knowledge graph QA

**Evidence maturity:** C1–C2
