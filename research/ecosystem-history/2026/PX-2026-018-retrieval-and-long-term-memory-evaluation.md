# PX-2026-018 — Retrieval utility and long-term agent-memory evaluation

**Research date:** 2026-11-08  
**Covered releases:** 2026-08-12 to 2026-10-02  
**Status:** validated benchmark/paper findings; retrieval and memory-evaluation input  
**AlgoX area:** coding retrieval / long-term memory / selective context / task utility / evaluation

## Finding

Recent work reinforces that retrieval and memory must be evaluated by what an agent can do with the information, not only by text similarity or final-answer recall.

### CodeGrep

The [CodeGrep paper](https://aclanthology.org/2026.realm-1.80/) introduces a 14B retrieval agent trained with GRPO to perform multi-turn grep, glob and file-reading operations before handing candidate files to a fixed downstream coding agent. On the paper's 500 SWE-Bench Verified instances, CodeGrep preserved the downstream resolution rate while reducing rounds and token use on resolved tasks. The authors report that downstream utility showed a precision threshold: BM25 degraded performance, a Jina retriever was approximately neutral, and CodeGrep's higher precision produced efficiency gains.

The key result is methodological: a retriever should be judged by downstream task utility, not just standalone relevance metrics.

### Agent Memory Leaderboard / Agent Memory Challenge

The [Agent Memory Leaderboard](https://github.com/AML-memory/agent-memory-leaderboard) provides an open evaluation contract for textual, coding and multimodal long-term memory. The first leaderboard cycle was published August 12, 2026. Cycle 2 opened September 20, its submission deadline was October 31, and its formal evaluation closed November 4; the organizers scheduled the official results for mid-November.

The platform separates memory ingestion (`Add`) and retrieval (`Search`) from downstream answer/agent execution and evaluation. It versions data, evaluation contracts, scoring and pipeline configuration. This is particularly useful for comparing memory systems without pretending that all products expose identical internal storage architectures.

### DyadMem

The October 2 paper [DyadMem: A Long-Term Memory Benchmark of How Agents Work with Users](https://arxiv.org/abs/2610.03020) proposes User-conditioned Relational Agent Memory: the memory of how a particular agent should work with a particular user, not only facts about that user. It reports 3,065 episodes, 50,961 sessions and 61,210 QA instances, with capture, update and recall annotations. The paper reports a substantial gap between gold-memory QA and full-pipeline QA, highlighting failures in memory capture, recall and safe deletion.

This helps separate memory quality into multiple lifecycle stages rather than treating the memory store as a passive vector database.

## AlgoX implications

A retrieval/memory evaluation record should include:

- information need and task/workflow state;
- source scope and authority constraints;
- retrieved items and abstentions;
- precision/recall plus downstream task outcome;
- memory capture, update, recall and deletion behavior;
- temporal consistency and user/agent relationship context;
- context/token/latency/cost consumption;
- privacy and policy compliance;
- exact dataset, pipeline, judge and benchmark versions.

Keep these outcomes distinct:

```text
Retrieved != Relevant != Sufficient != Authoritative != Validated
```

Also distinguish a memory benchmark result from a guarantee that a memory system is safe for every agent or user population.

## Decision

**ADOPT conceptually.** CodeGrep is a strong reference for task-aware, agentic code retrieval. Agent Memory Leaderboard supplies a versioned cross-system evaluation contract. DyadMem adds relationship-specific and lifecycle-aware memory dimensions. AlgoX should not equate memory ingestion/retrieval throughput with reliable long-term agent memory.

## Sources

- CodeGrep, ACL Anthology: https://aclanthology.org/2026.realm-1.80/
- Agent Memory Leaderboard: https://github.com/AML-memory/agent-memory-leaderboard
- Leaderboard evaluation status: https://agentmemories.ai/evaluation
- DyadMem paper: https://arxiv.org/abs/2610.03020
