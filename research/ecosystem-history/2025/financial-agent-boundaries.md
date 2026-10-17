# 2025 Financial Agent Boundaries

## Status
PROVISIONAL.

## Core finding
2025 evidence strengthens a boundary already identified in 2023–2024: LLM agents are increasingly useful for **research and knowledge work**, but that does not establish suitability for deterministic, latency-sensitive or irreversible execution.

Financial-agent research covers investment research, portfolio optimization, risk management, information retrieval and strategy generation, but continues to identify numerical reasoning, prompt sensitivity, real-time adaptation and deployment constraints as open problems. [1]

## Capability decomposition

```text
Financial AI
├── Information acquisition
├── Document / market-data analysis
├── Research synthesis
├── Hypothesis generation
├── Strategy research
├── Portfolio analysis
├── Risk analysis
├── Decision support
└── Execution
```

These capabilities should not share one evidence score.

## Proposed AlgoX boundary

```text
AI / Agent Layer
    │
    ├── Research
    ├── Analysis
    ├── Hypothesis generation
    ├── Experiment orchestration
    └── Decision recommendation
            ↓
      Deterministic Policy Gate
            ↓
      Risk / Compliance Gate
            ↓
      Execution Engine
            ↓
        Venue Adapter
```

An agent may propose a decision. A governed deterministic layer must decide whether that proposal is admissible. Execution remains separately observable, auditable and reconcilable.

## 2025 research direction
AlgoX should explicitly investigate:

1. agent-generated financial hypotheses;
2. tool-augmented quantitative research;
3. reflective experiment loops;
4. agent memory and historical reasoning;
5. numerical and temporal reasoning benchmarks;
6. portfolio/risk decision support;
7. bounded execution proposals;
8. human approval and policy gates;
9. reproducibility of agent workflows;
10. failure and adversarial testing.

## Do not infer
The following conclusions are not justified merely from agent benchmark results:

- profitable live trading;
- safe autonomous order submission;
- reliable market prediction;
- robustness across market regimes;
- suitability for high-frequency execution;
- regulatory compliance.

## AlgoX decision
**ADOPT** the architectural separation between agentic research/decision support and deterministic execution governance.

**ASSESS** direct agent-to-exchange execution only through controlled experiments with explicit safety and recovery gates.

**REJECT** any architecture that treats an LLM's generated recommendation as canonical financial state.

## Reference
1. Dong et al., “Large Language Model Agents in Finance: A Survey Bridging Research, Practice, and Real-World Deployment,” Findings of EMNLP 2025.
