# 2025 — Production Agent Observability and Financial Evaluation

Status: PROVISIONAL

## Research question

How should AlgoX evaluate and observe agents when correctness depends on multi-step tool use, retrieved evidence, environment state, cost, risk and downstream outcomes rather than a single model response?

## Evidence reviewed

- Microsoft Agent Framework production guidance: traces and spans are required to understand multi-step agent behavior, tool calls and failures.
- LangChain State of Agent Engineering 2025: production adoption of observability and tracing is materially higher than offline evaluation adoption.
- Grafana agent observability guidance: production telemetry, replay, evaluations and experiments form a continuous improvement loop.
- AI-Trader (2025): live, data-uncontaminated evaluation across U.S. stocks, A-shares and crypto; reported that general model intelligence did not automatically translate into trading capability and emphasized risk control.
- Agent Market Arena / When Agents Trade (2025): continuous multi-market evaluation of trading-agent behavior; agent architecture can materially affect behavior, not merely model backbone.
- 2025 finance-agent survey: financial deployment spans data analysis, investment research, trading, investment management and risk management, with numerical reasoning, prompt sensitivity and real-time adaptation remaining challenges.

## Finding 1 — Agent evaluation must score trajectories

A model-output score is insufficient for an agent. AlgoX should evaluate:

- tool selection
- tool arguments
- ordering of tool calls
- retrieved evidence quality
- temporal correctness
- grounding
- policy compliance
- cost
- latency
- recovery behavior
- final result
- downstream outcome

The unit of evaluation is therefore an **agent trajectory**, not merely an LLM response.

## Finding 2 — Observability and evaluation are different capabilities

Observability answers:

> What happened?

Evaluation answers:

> Was what happened good, correct and acceptable?

Audit answers:

> What evidence proves what happened and who/what authorized it?

These must remain separate but connected.

## Finding 3 — Financial evaluation must include risk, not only return

Recent live financial-agent benchmarks reinforce the distinction between general intelligence and trading competence. Risk control, market regime, liquidity and execution constraints can materially change outcomes.

Therefore AlgoX must not use raw return as the primary financial-agent metric.

A financial evaluation bundle should include:

- return
- volatility
- drawdown
- Sharpe/Sortino where appropriate
- turnover
- transaction costs
- slippage
- exposure
- concentration
- leverage
- tail loss
- risk-limit violations
- execution quality
- recovery behavior
- reproducibility

## Finding 4 — Live evaluation is a separate evidence domain

Historical backtests, replay, paper trading and live evaluation are not interchangeable.

```text
Historical Dataset
       ↓
Backtest
       ↓
Historical Replay
       ↓
Paper / Sandbox
       ↓
Failure Injection
       ↓
Controlled Live Evaluation
       ↓
Production Evidence
```

A result should retain the evaluation environment and market regime in which it was obtained.

## Finding 5 — Agent architecture is itself an experimental variable

Different agent structures can produce different behavior even when using the same model family. Consequently, AlgoX should benchmark:

- single-agent
- planner/executor
- specialist agents
- critic/verifier
- memory-enabled agents
- tool-routed agents
- deterministic policy-gated agents

Architecture must not be treated as a cosmetic wrapper around a model.

## Proposed AlgoX agent trace

```text
Trace
├── task
├── agent_version
├── model_version
├── policy_version
├── context_version
├── evidence_bundle
├── tool_calls
│   ├── tool
│   ├── arguments
│   ├── result
│   └── latency
├── intermediate decisions
├── verification events
├── approvals
├── final decision
├── downstream outcome
└── audit references
```

## Proposed evaluation graph

```text
Agent Run
   ↓
Trajectory
   ├── Evidence quality
   ├── Tool correctness
   ├── Policy compliance
   ├── Verification
   ├── Cost / latency
   └── Outcome
          ↓
      Evaluation
          ↓
       Finding
          ↓
       Decision
```

## Financial safety boundary

AlgoX research supports agents as research and analysis components. It does **not** establish that an LLM should directly control irreversible execution.

Preferred architecture:

```text
Agent
 ↓
Research / Analysis
 ↓
Recommendation
 ↓
Deterministic Policy Gate
 ↓
Risk Engine
 ↓
Execution Engine
 ↓
Broker / Exchange
```

## Decision status

- ADOPT: trajectory-level observability
- ADOPT: independent evaluation layer
- ADOPT: immutable audit references
- ADOPT: financial risk-aware evaluation
- TRIAL: continuous online evaluation
- TRIAL: architecture-level agent benchmarking
- HOLD: autonomous LLM execution authority

## Remaining questions

1. Which trace schema is sufficient without coupling AlgoX to one observability vendor?
2. How should online evaluation sample production traffic safely?
3. How should evaluation results become durable findings without polluting institutional knowledge with unverified scores?
4. Which financial benchmarks remain robust across market regimes?
5. How should Indian-market constraints be represented in agent evaluations?

## AlgoX implication

The evaluator is part of the intelligence system. A capable agent without an independent evaluator can accumulate confident but incorrect experience. AlgoX should therefore treat traces, evaluation, provenance and governance as first-class capabilities.