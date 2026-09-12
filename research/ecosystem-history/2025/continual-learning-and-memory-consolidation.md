# 2025 Continual Learning and Memory Consolidation

## Status
PROVISIONAL.

## Research question
Can an agent improve from experience without turning every past interaction into untrusted memory or causing uncontrolled policy drift?

## Key distinction

2025 work increasingly separates retrieval from learning. A memory system can preserve and retrieve prior experience, while a learning system changes future behavior based on evaluated experience.

```text
Experience
   ↓
Episode record
   ↓
Evaluation
   ├── failure
   ├── success
   └── ambiguous
   ↓
Candidate lesson
   ↓
Applicability / contradiction checks
   ↓
Consolidation
   ↓
Procedure / skill / policy candidate
   ↓
Validation
   ↓
Trusted institutional knowledge
```

## Findings

### 1. Memory should be tiered

Long-running agents benefit from separating immediately useful context from durable semantic knowledge. This supports the existing AlgoX distinction between working, episodic, semantic and procedural memory.

### 2. Consolidation is a governed transformation

A raw episode should not become a permanent fact merely because the model generated a summary. Consolidation should preserve:

- source episode IDs
- evidence
- extraction method
- time of consolidation
- applicability conditions
- confidence
- contradictions
- supersession relationships
- reviewer/policy decision where required

### 3. Experience should produce reusable skills only after evaluation

A repeated successful trajectory can suggest a procedure, but repetition alone does not prove generality. The candidate procedure should be evaluated against held-out tasks or controlled replay before becoming trusted.

### 4. Continual learning creates drift risk

Any mechanism that changes model weights, prompts, routing policy, tool selection or procedural memory can introduce regressions. AlgoX therefore treats learning changes as versioned decisions rather than invisible background adaptation.

```text
Learning change
 ├── before state
 ├── evidence
 ├── experiment
 ├── evaluation
 ├── after state
 ├── regression results
 └── rollback reference
```

### 5. Learning and institutional memory need separate trust levels

Suggested states:

```text
OBSERVED
   ↓
CANDIDATE LESSON
   ↓
REPRODUCED
   ↓
VALIDATED PROCEDURE
   ↓
INSTITUTIONAL KNOWLEDGE
```

The memory layer can preserve lower-confidence observations without presenting them as established procedures.

## AlgoX architecture

Add an explicit **Consolidation Governor** between experience and durable memory:

```text
Agent Runtime
     ↓
Episode Store
     ↓
Evaluator
     ↓
Lesson Extractor
     ↓
Consolidation Governor
     ├── provenance
     ├── temporal validity
     ├── contradiction detection
     ├── confidence
     ├── applicability
     └── governance policy
     ↓
Memory / Knowledge Commit
```

This fits the existing knowledge-delta and governance architecture rather than creating an independent agent-memory authority.

## Financial-system consequence

Continual learning must not silently modify execution behavior. Changes to trading strategy, risk policy, execution rules, broker adapters or regulatory assumptions require explicit versioning and validation.

For a financial platform:

```text
Experience
   ↓
Research lesson
   ↓
Experiment
   ↓
Backtest / replay
   ↓
Risk validation
   ↓
Approval
   ↓
New version
```

No direct:

```text
Live event → autonomous policy mutation
```

## AlgoX decision

**ADOPT:**
- tiered memory
- episode/lesson separation
- governed consolidation
- versioned learning changes
- rollback references
- applicability conditions

**TRIAL:**
- automated lesson extraction
- automatic skill discovery
- continual routing/prompt optimization

**HOLD:**
- unrestricted online weight updates
- autonomous modification of financial execution/risk policy
