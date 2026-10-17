# 2024 Capability Evolution Map v1

## Purpose

Convert the 2024 project research into capability evolution rather than a project list.

## 2023 -> 2024 evolution

| Capability | 2023 emphasis | 2024 evolution | AlgoX implication |
|---|---|---|---|
| Agent control | prompts, loops, roles | explicit state, graphs, execution control | model control flow explicitly |
| Tool use | function/tool calls | agent-computer interfaces and environments | tools are architectural interfaces |
| Memory | context/RAG experiments | persistent, temporal, evaluated memory | provenance and validity are first-class |
| Evaluation | model/task benchmarks | environment + trace + task outcome evaluation | evaluate complete systems |
| Coding agents | code generation | repository navigation, editing, tests, execution | development is an executable workflow |
| Finance agents | financial LLMs and task agents | multi-component financial workflows | separate research, data, reasoning and execution |
| Quant research automation | isolated alpha/model experiments | iterative research-development-feedback loops | experiment loop becomes a capability |
| Infrastructure | model/vector infrastructure | execution environments and evaluation infrastructure | reproducibility requires controlled environments |

## Strong findings

### 1. Interface design is capability
SWE-agent demonstrated that a purpose-built agent-computer interface can materially affect agent performance. Its 2024 research evaluated repository navigation, code editing and program execution on SWE-bench and HumanEvalFix. This supports treating the action interface as an architectural component rather than an implementation detail.

### 2. Evaluation must include the environment
Agent performance cannot be reduced to model quality. The environment, available tools, state transitions, execution traces and task definition influence measured capability.

### 3. Memory is more than retrieval
Retrieval is a mechanism for obtaining information. Institutional memory additionally requires provenance, temporal validity, relationships, review state and durable decisions.

### 4. Financial AI is layered
Financial-agent architectures increasingly separate model reasoning from financial data, quantitative analytics, orchestration and execution. AlgoX should preserve these boundaries.

### 5. Multi-agent is a design choice, not a default
Decomposition can improve specialization but introduces coordination, latency, state synchronization and evaluation costs. AlgoX must require evidence before recommending multi-agent decomposition.

### 6. Research automation is converging on closed loops
The later R&D-Agent(Q) work is a useful validation target: research hypothesis -> implementation -> real-market experiment -> evaluation -> next direction. It is intentionally recorded as later evidence rather than backdated to 2024.

## Architecture pattern emerging from 2024

```text
MODEL
  |
REASONING / PLANNING
  |
STATE + CONTROL FLOW
  |
TOOLS / ACTION INTERFACE
  |
EXECUTION ENVIRONMENT
  |
OBSERVATION / TRACE
  |
EVALUATION
  |
EVIDENCE
  |
MEMORY / LEARNING
  |
NEXT DECISION
```

## AlgoX decision

ADOPT the capability model, not any individual project's architecture wholesale.

The durable lesson is that intelligent systems need explicit boundaries between reasoning, action, environment, observation, evaluation and institutional memory.

## Evidence discipline

SWE-agent is direct 2024 evidence. R&D-Agent(Q) is later evidence and must not be used to claim a 2024 release or 2024 capability. Later systems may validate, qualify or refute the provisional 2024 synthesis.
