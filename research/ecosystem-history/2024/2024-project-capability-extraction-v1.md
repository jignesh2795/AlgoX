# 2024 Project Capability Extraction v1

## Purpose

Move the 2024 research from a project list into reusable capabilities, architectural patterns, evidence, and decisions. A project is evidence; it is not automatically a recommendation.

## 1. OpenHands / OpenDevin

### Evidence
The July 2024 OpenHands paper describes a generalist software-development agent that can write code, use a command line, browse the web, operate in sandboxed execution environments, coordinate multiple agents, and incorporate evaluation benchmarks. It evaluates across software-engineering and web tasks.

### Extracted capabilities
- sandboxed tool execution
- explicit agent/environment boundary
- code + shell + browser action space
- extensible agent implementations
- multi-agent coordination
- benchmark-integrated evaluation
- reproducible task execution

### AlgoX finding
A useful agent architecture requires more than an LLM and prompt. The execution environment and action interface are first-class system components.

### Decision
ADOPT as an architectural reference. Do not copy the whole runtime.

## 2. SWE-agent

### Capability contribution
SWE-agent established the importance of an agent-computer interface tailored to software engineering: controlled file viewing/editing, command execution, repository context, and iterative issue resolution.

### AlgoX finding
Tool design can materially affect agent performance. The interface between reasoning and environment should therefore be benchmarked independently from model selection.

### Decision
ADAPT the principle of explicit, constrained action interfaces.

## 3. AutoGen

### Evidence
The 2024 AutoGen paper describes composition of multiple customizable, conversable agents using LLMs, human input and tools, with flexible conversation patterns.

### Extracted capabilities
- multi-agent composition
- explicit agent roles
- human-in-the-loop interaction
- tool-enabled agents
- conversation/state orchestration

### AlgoX finding
Multi-agent systems are orchestration systems, not simply collections of prompts. State, control flow and termination conditions must be explicit.

### Qualification
Multi-agent does not automatically mean better. OpenHands published a 2024 analysis arguing that strong single-agent systems can be preferable for some tasks.

### Decision
ASSESS; do not universally adopt multi-agent decomposition.

## 4. LangGraph

### Capability contribution
2024 LangGraph work emphasized graph/state-oriented agent execution, persistence, local development and interoperability. Its November 2024 Agent Protocol announcement attempted to standardize framework-agnostic agent communication and demonstrated wrapping AutoGen/CrewAI agents as graph nodes.

### Extracted capabilities
- explicit state graph
- durable execution concepts
- persistence boundary
- human-in-the-loop control
- framework interoperability
- agent protocol abstraction

### AlgoX finding
Agent interoperability is easier when execution state and interfaces are explicit rather than hidden inside framework-specific conversation abstractions.

### Decision
ADOPT graph/state concepts for AlgoX's research-agent architecture; WRAP external agent frameworks where useful.

## 5. FinRobot

### Evidence
The May 2024 FinRobot paper describes a financial AI-agent platform with four layers: financial AI agents, financial LLM algorithms, LLMOps/DataOps, and multi-source foundation models.

### Extracted capabilities
- finance-specialized agent roles
- financial reasoning workflows
- model-selection/application strategies
- LLMOps/DataOps boundary
- multi-model foundation layer

### AlgoX finding
Financial AI should separate domain workflows from model providers and from data/training operations.

### Decision
ADOPT the layered separation as an architectural pattern; do not assume its financial reasoning outputs are trading evidence.

## 6. TradingAgents

### Capability contribution
The 2024 multi-agent trading research direction decomposes financial research into specialized roles such as fundamental, sentiment, technical, trader and risk agents.

### Extracted capabilities
- specialized research roles
- debate/collaboration between agents
- explicit risk role
- financial research workflow decomposition

### AlgoX qualification
Agent-generated trading decisions remain hypotheses until independently backtested, stress-tested and validated against realistic execution/data assumptions.

### Decision
ADAPT for research orchestration, not direct autonomous execution.

## 7. SWE-bench and evaluation infrastructure

### Capability contribution
2024 made real repository issues a benchmark target for software-engineering agents. SWE-bench evaluates whether generated patches resolve real GitHub issues.

### AlgoX finding
Evaluation must use task outcomes rather than model capability claims. Agent evaluation should retain the task, environment, model, tools, trajectory and result.

### Decision
ADOPT trajectory-aware evaluation provenance.

## Cross-project 2024 capability map

| Capability | OpenHands | SWE-agent | AutoGen | LangGraph | FinRobot | TradingAgents |
|---|---|---|---|---|---|---|
| Stateful execution | Strong | Medium | Medium | Strong | Medium | Medium |
| Tool execution | Strong | Strong | Strong | Strong | Strong | Strong |
| Sandboxing | Strong | Strong | Optional | Deployment-dependent | Deployment-dependent | Deployment-dependent |
| Multi-agent orchestration | Supported | Limited | Strong | Strong | Strong | Strong |
| Human-in-loop | Supported | Possible | Strong | Strong | Workflow-dependent | Workflow-dependent |
| Domain specialization | Software | Software | General | General | Finance | Finance |
| Evaluation integration | Strong | Strong | Research-oriented | Strong | Research-oriented | Research-oriented |
| Persistent state | Architecture-level | Task-level | Conversation-level | Strong | Layer-dependent | Workflow-dependent |

These ratings are comparative research judgments, not benchmark scores.

## 2023 → 2024 delta

### 2023 emphasis
- prompt/tool experimentation
- early autonomous-agent loops
- memory experiments
- multi-agent role experimentation
- initial agent benchmarks
- local-model and RAG infrastructure

### 2024 emphasis
- explicit state machines/graphs
- sandboxed execution
- agent-computer interfaces
- reproducible evaluation environments
- production-oriented persistence
- interoperability
- finance-specific agent layers
- benchmark-driven development

## Architectural lesson for AlgoX

The ecosystem is converging on a layered system:

```text
Model
  ↓
Reasoning / Planning
  ↓
State + Control Flow
  ↓
Tools / Action Interface
  ↓
Sandbox / Environment
  ↓
Observation / Result
  ↓
Evaluation
  ↓
Trace / Evidence
  ↓
Learning / Memory
```

AlgoX's institutional-memory architecture already contains several of these boundaries. The 2024 research therefore strengthens the decision to treat traces, evidence, experiments and governance as first-class objects rather than storing only final agent answers.

## Important non-conclusion

2024 does **not** establish that multi-agent systems outperform single-agent systems in general. It establishes that multi-agent orchestration became a major architectural pattern and that its value must be evaluated task-by-task.
