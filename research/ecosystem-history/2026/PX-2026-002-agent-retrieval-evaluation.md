# PX-2026-002 — Agent-native retrieval and research evaluation

**Research date:** 2026-09-13
**Status:** validated research finding; benchmark/architecture input
**AlgoX area:** retrieval / context engineering / agent evaluation / autoresearch

## Finding

Two 2026 projects clarify that retrieval and evaluation for agents are becoming distinct engineering disciplines rather than simple extensions of conventional RAG and benchmark scoring.

### LRAT — Learning to Retrieve from Agent Trajectories

LRAT trains retrievers from multi-step agent search/browse trajectories rather than relying only on static human relevance labels. The released LRAT-Train set contains 26,482 successful agent trajectories. The repository evaluates both retrieval quality and downstream agent task success.

Repository: https://github.com/Yuqi-Zhou/LRAT

**AlgoX implication:** retrieval should eventually consume agent trajectory/state signals and learn from successful and unsuccessful information-seeking behavior.

### Agent Retrieval Bench (ARB)

ARB evaluates the context-acquisition layer of coding agents. Its relevance definition is based on the coding workflow's next information need, not simply query/file semantic similarity. It includes positive retrieval tasks and selective-retrieval cases where the correct answer is to abstain because useful local context does not exist.

Repository: https://github.com/eyuansu62/agent-retrieval-bench

**AlgoX implication:** retrieval quality should include both:

- finding the right context;
- correctly deciding when not to retrieve local context.

## Autoresearch evaluation

AutoLab evaluates frontier agents on long-horizon research and engineering tasks where agents repeatedly diagnose, modify, execute and benchmark solutions.

Repository: https://github.com/autolabhq/autolab

**AlgoX implication:** research-agent evaluation should measure improvement over time, not only final-answer correctness.

Useful metrics include:

- delta from baseline;
- best score reached;
- improvement per experiment;
- evaluation efficiency;
- regression rate;
- cost/time to improvement;
- reproducibility;
- knowledge reuse.

## Combined architecture lesson

The relevant pipeline is:

```text
Task / workflow signal
        -> agent state / trajectory
        -> retrieval policy
        -> context selection
        -> reasoning / execution
        -> experiment
        -> independent evaluation
        -> evidence
        -> future retrieval / learning
```

This argues against a design in which the entire repository or institutional memory is dumped into the model context.

## AlgoX benchmark direction

The earlier EXP-ALG-005 concept should eventually be decomposed into:

- 005-A Retrieval quality
- 005-B Context construction
- 005-C Agent task completion
- 005-D Long-horizon improvement
- 005-E Experiment efficiency
- 005-F Knowledge reuse
- 005-G Regression/forgetting
- 005-H Autonomous research

## Decision

**Do not implement a custom retrieval or research-agent framework yet.** First use LRAT, ARB and AutoLab as external reference benchmarks and extract the minimum interfaces AlgoX needs for trajectory-aware retrieval, evaluation streams, evidence capture and promotion gates.
