# 2024 — RAG / Evidence Research Synthesis

**Status:** PROVISIONAL
**Evidence maturity:** C2

## Executive finding

2024 RAG research establishes that retrieval is not a single operation and that retrieval-augmented research must be evaluated as a pipeline.

```text
Research Question
      ↓
Query Preparation
      ↓
Candidate Retrieval
      ↓
Reranking / Selection
      ↓
Evidence Packaging
      ↓
Reasoning / Synthesis
      ↓
Claim Verification
      ↓
Decision
```

## What AlgoX should learn

### 1. Retrieval and generation are separate failure domains
A system can retrieve poor evidence and generate fluent text, or retrieve strong evidence and still synthesize an incorrect claim.

### 2. Evidence quality needs its own metrics
At minimum AlgoX should distinguish:
- retrieval relevance
- evidence coverage
- source authority
- freshness
- citation/provenance completeness
- claim faithfulness
- synthesis correctness
- decision usefulness

### 3. Experiment configuration is evidence
A benchmark result should preserve its dataset, corpus, retriever, reranker, model, prompt/configuration, metrics, and version identifiers. BERGEN's reproducibility work strongly supports this principle.

### 4. Reference-free evaluation is useful but insufficient
RAGAs demonstrates that automated signals can accelerate evaluation, but AlgoX should not promote a finding solely because an LLM-based evaluator gives it a high score.

### 5. Dynamic knowledge requires temporal provenance
Research sources change. AlgoX therefore needs source retrieval timestamps, source versions where available, publication/update dates, and supersession relationships.

## Proposed AlgoX evidence object

```text
Evidence
├── source_id
├── source_locator
├── retrieved_at
├── published_at
├── updated_at
├── source_version
├── excerpt / artifact reference
├── authority
├── relevance
├── freshness
├── provenance
├── claims_supported[]
└── verification_status
```

## Proposed claim flow

```text
SOURCE
  ↓
EVIDENCE
  ↓
CLAIM
  ↓
COUNTER-CLAIM SEARCH
  ↓
VERIFICATION
  ↓
FINDING
  ↓
DECISION
```

## Strategic conclusion

AlgoX should build an **evidence system**, not merely a RAG system.

RAG is an implementation capability. Evidence provenance, claim verification, temporal validity, contradiction handling, and decision traceability are the institutional capabilities AlgoX actually needs.

## Research basis

- RAGAs, EACL 2024
- BERGEN, Findings of EMNLP 2024
- Evaluation of Retrieval-Augmented Generation: A Survey, 2024
- A Survey on Retrieval-Augmented Text Generation for Large Language Models, 2024

**Next research target:** knowledge graphs, temporal knowledge, contradiction detection, provenance systems, and source lifecycle management.
