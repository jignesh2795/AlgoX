# 2025 Research-Agent Evidence and Reliability v1

## Purpose

This record extends the 2025 research from research automation toward the reliability boundary: can an agent actually execute novel research, reproduce experiments, maintain memory, and produce evidence that can safely enter institutional knowledge?

## Evidence anchors

### R&D-Agent-Quant

R&D-Agent(Q) represents a full-stack quantitative research loop. Its Research stage formulates hypotheses and maps them to tasks; its Development stage implements those tasks; execution runs real-market backtests; a feedback stage evaluates results and informs subsequent iterations. A multi-armed-bandit scheduler selects research directions adaptively.

AlgoX interpretation: this is strong evidence for treating research direction selection, implementation, experiment execution and feedback as separate capabilities connected by explicit evidence-producing transitions.

Historical boundary: the paper was submitted in May 2025. Do not backdate its architecture into 2024.

### RExBench

RExBench evaluates whether coding agents can implement novel extensions to existing research papers and codebases. It uses 12 research-extension tasks and automatic execution-based evaluation. The 2025 results reported that the evaluated agents failed on the majority of extensions; even with additional human-written hints, the best reported success rate remained below 40%.

AlgoX interpretation: research automation must not be equated with research autonomy. Implementation capability remains a major bottleneck.

### AutoExperiment

AutoExperiment evaluates a continuum from reproducing existing research code to implementing experiments from increasingly incomplete code starting points. This establishes a useful capability axis between reproduction and independent replication.

AlgoX interpretation: research-agent maturity should be measured by how much missing implementation context the agent can reliably bridge, not simply whether it can run an existing repository.

### MLR-Bench

MLR-Bench evaluates open-ended machine-learning research across idea generation, proposal formulation, experimentation and paper writing. Its reported evaluation found that coding agents frequently generated fabricated or invalidated experimental results.

AlgoX interpretation: executable experiment provenance and result validation must be first-class controls. A plausible research report is not evidence.

### Agent Laboratory

Agent Laboratory demonstrates an end-to-end research-assistant workflow spanning literature review, experimentation and report writing, while retaining opportunities for human feedback.

AlgoX interpretation: human guidance should be represented as an explicit control/evidence channel rather than hidden intervention.

### Memory benchmarks

MemBench evaluates agent memory across factual and reflective memory, multiple interaction scenarios, effectiveness, efficiency and capacity. Letta's 2025 memory benchmarks separately evaluate memory read, write and update behavior.

AlgoX interpretation: memory must have measurable operations and should not be reduced to retrieval similarity.

## 2025 capability model

```text
Research question
      ↓
Literature / prior evidence
      ↓
Hypothesis
      ↓
Task decomposition
      ↓
Implementation
      ↓
Controlled execution
      ↓
Observed result
      ↓
Validation / reproduction
      ↓
Evidence package
      ↓
Finding
      ↓
Decision
      ↓
Memory update
      ↓
Next research direction
```

## Reliability boundary

The 2025 evidence produces an important negative finding:

> Autonomous research is not yet equivalent to trustworthy autonomous research.

Failure modes include:

- invalid experimental implementation;
- fabricated or unsupported results;
- inadequate reproduction;
- incorrect interpretation of prior work;
- memory errors;
- inappropriate research-direction selection;
- hidden human intervention;
- benchmark contamination or shortcutting.

Therefore AlgoX must preserve the distinction:

```text
Agent output
    ≠
Evidence

Experiment execution
    ≠
Validated result

Research report
    ≠
Institutional truth
```

## Implications for AlgoX

1. Research agents should produce structured traces.
2. Every durable claim should reference evidence.
3. Experiment results should be independently checkable where practical.
4. Human intervention should be recorded explicitly.
5. Failed research attempts are valuable evidence and should remain auditable.
6. Memory updates should pass governance rather than being automatic.
7. Research-direction selection should be measurable and reversible.
8. Benchmarks should test the entire research loop, not only language quality.

## 2023 → 2024 → 2025 progression

```text
2023: agent experimentation
      ↓
2024: agent systemization + evaluation
      ↓
2025: research automation + measurable memory
      ↓
2025 finding: autonomy still requires evidence governance
```

## Provisional maturity assessment

- Agent task execution: advanced but heterogeneous
- Multi-step coding: improving, not reliable for arbitrary research extensions
- Research automation: demonstrated
- Autonomous experimentation: demonstrated in constrained settings
- Scientific reliability: unresolved
- Agent memory: measurable capability, still evolving
- Quant research automation: demonstrated experimentally
- Institutional-quality autonomous research: not established

## AlgoX decision

**ADOPT** the research-loop abstraction.

**ADOPT** structured experiment/evidence traces.

**ADOPT** explicit memory operation benchmarks.

**ADAPT** autonomous research agents behind AlgoX governance and verification.

**REJECT** any architecture that treats generated research output as truth without evidence validation.
