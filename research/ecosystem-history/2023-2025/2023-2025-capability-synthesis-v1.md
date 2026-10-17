# AlgoX 2023–2025 Capability Synthesis v1

## Purpose

This synthesis converts the historical ecosystem research into capability-level decisions. It is not a popularity ranking and does not treat benchmark performance as production readiness.

## Evolution

### 2023 — foundational capability discovery
- Event-driven execution and stateful order lifecycles became recurring architecture patterns.
- Reconciliation, instrument identity, derivatives semantics, data provenance and execution realism emerged as first-class financial-system concerns.
- LLM/agent ecosystems established tool use, multi-agent orchestration, memory experiments and coding-agent workflows.

### 2024 — systemization and evaluation
- Agent systems increasingly separated model reasoning from state/control flow, tools, execution environments and evaluation.
- Coding agents demonstrated repository-aware edit/execute/test loops.
- Financial AI became layered: financial agents, models, data/LLMOps and domain tools rather than a model-only architecture.
- Benchmarks increasingly evaluated complete environments and traces instead of isolated model answers.

### 2025 — research automation and evidence pressure
- Research/development loops became explicit in quantitative-agent systems.
- Memory and long-horizon agent behavior became benchmarkable capabilities.
- Financial benchmarks exposed substantial gaps between general reasoning and reliable financial research or trading.
- Autonomous experimentation therefore requires validation and provenance gates rather than direct conversion of agent output into institutional knowledge.

## Capability decisions for AlgoX

| Capability | Decision | Rationale |
|---|---|---|
| Evidence/provenance graph | ADOPT | Core institutional-truth mechanism. |
| Knowledge graph | ADOPT | Structured projection of evidence and relationships. |
| Temporal validity | ADOPT | Historical research requires point-in-time correctness. |
| Research trace | ADOPT | Makes agent reasoning/actions auditable without treating traces as truth. |
| Experiment registry | ADOPT | Separates hypothesis, execution, result and conclusion. |
| Benchmark registry | ADOPT | Prevents model/project claims from becoming unqualified decisions. |
| Governance gate | ADOPT | Required before durable knowledge changes. |
| Agent memory | ADAPT | Use evidence-backed semantic/episodic/procedural memory; avoid memory-as-chat-history. |
| Vector retrieval | ADAPT | Candidate generation only; never institutional truth. |
| Multi-agent architecture | ADAPT | Use decomposition only when coordination provides measurable benefit. |
| Autonomous research loop | ADAPT | Proposal → implementation → experiment → validation → evidence. |
| Dedicated graph database | HOLD | Relational graph projection is sufficient until experiments justify migration. |
| Standalone vector database | HOLD | No evidence yet that operational complexity is justified. |
| PostgreSQL persistence | ADOPT LATER | Architectural direction is strong, but persistence should follow local experiments. |
| Production autonomous trading | REJECT FOR NOW | Research-agent competence does not establish execution/risk reliability. |
| GitHub Actions dependency | REJECT | Local verification is the required workflow. |

## Core architectural consequence

AlgoX should optimize for **evidence-governed research**, not autonomous answer generation.

```text
Sources
  ↓
Evidence
  ↓
Research claims
  ↓
Experiments / reproduction
  ↓
Results
  ↓
Findings
  ↓
Governed decisions
  ↓
Capabilities
  ↓
Institutional memory
  ↺
```

An LLM/agent is a proposer and reasoning component. It is not the institutional authority.

## Financial-system consequence

The historical research independently supports keeping these concerns separate:

```text
Market/Data Identity
      ↓
Data Quality + Provenance
      ↓
Strategy / Research
      ↓
Decision
      ↓
Risk
      ↓
Execution
      ↓
Broker/Venue State
      ↓
Reconciliation
```

This separation should inform future QuantumTrade architecture, but AlgoX itself remains the research and capability-intelligence layer.

## Open validation questions

1. Which memory representations provide measurable benefit on AlgoX's own benchmark corpus?
2. When does multi-agent decomposition outperform a strong single-agent workflow after coordination cost?
3. What evidence threshold is sufficient for a research finding to influence architecture?
4. Which financial-agent capabilities can be trusted for research assistance versus live execution?
5. Which capabilities should be reproduced locally before adoption?
6. When does PostgreSQL persistence materially improve research continuity enough to justify implementation cost?

## Decision rule

No ecosystem capability becomes an AlgoX institutional decision merely because a prominent project demonstrates it. The capability must have an identified use case, evidence, provenance, relevant constraints, and—where practical—a reproducible experiment.
