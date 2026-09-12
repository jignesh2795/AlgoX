# 2025 Coding Agents and Evaluation

## Status
PROVISIONAL.

## Research question
Did 2025 coding-agent progress solve the reliability weaknesses identified in 2024, or mainly increase capability on existing task formulations?

## Evidence reviewed
- SWE-Search (ICLR 2025): search/backtracking over SWE-bench-lite improved results relative to standard open-source agent baselines, indicating that inference-time search can improve repository-level repair rather than relying on one greedy trajectory.
- UTBoost (2025): stronger tests exposed 345 erroneous patches that had been counted as successful by original SWE-bench tests. This demonstrates that benchmark correctness can itself be a moving target.
- SWE-Bench-CL (2025): evaluates coding agents over chronological repository issue streams, introducing forgetting and transfer metrics and explicitly treating accumulated experience as a capability.
- RExBench (2025/2026 review cycle): realistic research-extension tasks remained difficult; evaluated agents failed the majority of extensions, even with additional human hints.
- SWE-Bench Pro (2025): 1,865 long-horizon tasks across 41 repositories; reported Pass@1 below 25% for evaluated models under a unified scaffold, illustrating the remaining gap between issue-level repair and professional-scale engineering.

## Findings

### 1. Agent capability is not equivalent to benchmark success
A coding agent can produce a patch that satisfies an incomplete test suite without actually satisfying the intended behavior. Therefore:

```text
Patch accepted by tests
        !=
Problem correctly solved
```

Evaluation must include regression tests, adversarial/augmented tests, semantic review, and where practical human verification.

### 2. Search became a first-class agent capability
2025 evidence supports explicit search, backtracking, self-assessment and iterative trajectories as useful additions to a simple generate-and-test loop.

```text
Observe
  ↓
Plan
  ↓
Candidate action
  ↓
Test / inspect
  ↓
Evaluate
  ├── success → verify
  └── failure → backtrack / revise
```

This is stronger than treating the agent as a single-pass code generator.

### 3. Long-horizon engineering remains unsolved
The gap between isolated issue repair and multi-file software evolution remains material. Large tasks require repository understanding, architectural consistency, dependency reasoning, migration planning and preservation of unrelated behavior.

### 4. Experience and memory became measurable capabilities
SWE-Bench-CL is important for AlgoX because it turns continual experience into an evaluation dimension: transfer, forgetting and tool-use efficiency can be measured rather than assumed.

This directly supports AlgoX's memory architecture, but does **not** prove that semantic/vector memory is sufficient.

### 5. Benchmark governance is part of the capability
UTBoost demonstrates that improving the evaluator can change the apparent ranking of agents. Therefore AlgoX must version benchmark definitions, test suites, datasets and evaluation policies alongside agent results.

## AlgoX implications

### Capability decomposition
Do not create one capability named `Coding Agent`. Track independently:

- repository discovery
- code understanding
- planning
- tool selection
- patch generation
- test generation
- test execution
- failure diagnosis
- search/backtracking
- multi-file modification
- architecture reasoning
- dependency reasoning
- migration support
- continual learning
- memory retrieval
- regression safety
- human collaboration
- cost/time efficiency

### Required evidence levels
A coding-agent claim should progress through:

```text
Demo
 ↓
Task benchmark
 ↓
Independent evaluator
 ↓
Adversarial tests
 ↓
Long-horizon benchmark
 ↓
Repeated repository evolution
 ↓
Real development evidence
```

## Decision
**ADOPT** the principle that agent evaluation is a system capability, not a model leaderboard.

**ADAPT** search/backtracking and continual-learning concepts into AlgoX's research-agent experiments.

**REJECT** the assumption that a high SWE-bench-style score establishes production engineering autonomy.

## Confidence
High for the evaluation-governance finding; medium for general claims about the relative superiority of individual agent scaffolds because results are benchmark-, model-, scaffold- and evaluator-dependent.
