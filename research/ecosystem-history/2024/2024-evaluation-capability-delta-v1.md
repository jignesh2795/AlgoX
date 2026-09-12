# 2024 Evaluation Capability Delta v1

## Purpose

Capture the 2024 shift from demonstrating that an LLM can answer a task toward evaluating complete agent and financial-AI systems under realistic environments, retrieval constraints, and domain-specific metrics.

## Evidence-backed themes

### 1. Agent evaluation became environment-based
AgentBench (ICLR 2024) evaluates LLM agents across eight environments including operating systems, databases, knowledge graphs, web browsing and web shopping. Its failure analysis identifies long-horizon reasoning, decision making and instruction following as major obstacles.

AlgoX implication: an agent capability record should identify the environment, action space, observation model, horizon and failure conditions, not just the model and prompt.

### 2. Open-web research became a measurable systems problem
A September 2024 benchmark evaluated agents on messy, economically valuable open-web research tasks and compared architectures, models and traces. ReAct with delegation performed strongly in that study.

AlgoX implication: research-agent quality must be measured against realistic research tasks and inspectable traces, not answer fluency alone.

### 3. Financial RAG acquired dedicated evaluation
OmniEval (December 2024) introduced a financial RAG benchmark spanning five task classes and 16 financial topics, with separate retrieval/generation evaluation and multidimensional metrics.

AlgoX implication: financial retrieval should be evaluated as a pipeline: query interpretation → retrieval → evidence coverage → reasoning → answer, with provenance preserved.

### 4. Financial LLM evaluation broadened substantially
FinBen (NeurIPS 2024) covers 42 datasets and 24 financial tasks across information extraction, textual analysis, QA, generation, risk management, forecasting, decision making and bilingual tasks. It also includes agent/RAG and stock-trading evaluation.

AlgoX implication: there is no single financial-AI score. Capability-specific benchmarks are required.

### 5. Finance requires heterogeneous metrics
Financial-agent evaluation uses both conventional financial metrics such as Sharpe, Sortino, Calmar, return, volatility and drawdown and non-trading measures for reasoning, retrieval, behavior and user-facing quality.

AlgoX implication: separate task correctness, financial performance, risk, robustness, trace quality and user utility rather than collapsing them into one score.

### 6. Human comparison remains important
Financial research-agent evaluations show that agent outputs can be competitive on particular dimensions while expert-written research can remain stronger in holistic synthesis. Therefore benchmark design should retain expert or high-quality reference baselines where feasible.

## 2023 → 2024 capability delta

| Capability | 2023 tendency | 2024 development | AlgoX consequence |
|---|---|---|---|
| Agent evaluation | task/demo oriented | multi-environment benchmarks | store environment + trace evidence |
| Research agents | answer generation | realistic open-web research | evaluate research process |
| RAG | retrieval + generation | retrieval and generation separately measured | preserve evidence coverage |
| Financial AI | model/task benchmarks | broad multi-task benchmark suites | capability-specific evaluation |
| Trading agents | strategy/backtest claims | broader risk/behavior evaluation | separate alpha from system reliability |
| Agent architecture | prompt/tool loops | explicit environments + delegation + traces | model agent as executable system |
| Quality | model-centric | system/trace/benchmark-centric | evidence maturity becomes central |

## Durable AlgoX extraction

The 2024 ecosystem strengthens this principle:

```text
Capability claim
    ↓
Defined task/environment
    ↓
Reproducible evaluation
    ↓
Trace + evidence
    ↓
Metric-specific result
    ↓
Finding
    ↓
Decision
```

A benchmark result is evidence for a bounded capability, not proof of general intelligence or production readiness.

## Source classification

The 2024 benchmark literature is primarily evidence for evaluation architecture and capability measurement. It should not automatically be treated as evidence that a system is production-ready.

## Next research direction

Continue the 2024 pass into model/inference infrastructure, coding-agent engineering, financial-agent architectures and quant-R&D automation, then freeze the 2023→2024 delta before beginning 2025.
