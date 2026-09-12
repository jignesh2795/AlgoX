# 2023 AI-Agent Research Map

These papers are research anchors for understanding the architecture behind the 2023 agent ecosystem.

## Tool use

### Toolformer
Language models can learn when and how to call external APIs/tools. Key capability: explicit tool selection, argument construction, and incorporation of tool results.

## Reasoning and action

### ReAct
Interleaves reasoning and action so an agent can use external observations while solving tasks. Key architectural idea: reasoning/action loop rather than one-shot generation.

## Self-improvement / feedback

### Reflexion
Introduces a verbal feedback and memory loop for agent improvement without conventional parameter updates. Key ideas: reflection, episodic memory, feedback-driven iteration.

## Agent memory and simulation

### Generative Agents
Demonstrates agents using memory, reflection, and planning to produce coherent behavior in an interactive environment.

## Embodied / long-horizon agents

### Voyager
Explores an open-ended agent with iterative skill acquisition, memory, and task-driven exploration.

## Agent evaluation

### AgentBench
Treats agent capability as something that should be evaluated across environments and tasks rather than inferred from language-model benchmarks alone.

### WebArena
Provides a realistic environment for evaluating autonomous web agents.

## Software engineering

### Autonomous Agents in Software Development
A 2023 vision paper explicitly extends agentic AI beyond coding into requirements engineering, planning, design, documentation, and software-development workflows.

## AlgoX extraction targets

- Tool abstraction
- Agent loop design
- Planning
- Working/episodic memory
- Reflection
- Skill acquisition
- Environment interfaces
- Evaluation harnesses
- Multi-agent role separation
- Verification and feedback loops
