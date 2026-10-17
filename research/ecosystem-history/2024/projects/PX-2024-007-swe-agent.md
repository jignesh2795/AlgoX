# PX-2024-007 — SWE-agent

**Repository:** https://github.com/SWE-agent/SWE-agent
**Historical category:** AI-development / software-engineering agent
**Domain:** Autonomous software engineering

## 2024 signal
SWE-agent demonstrated that repository-level software engineering required more than code generation: the agent needed an environment, repository navigation, file editing, shell/test execution, and an interaction policy designed around software-engineering tasks. The 2024 SWE-bench release reported SWE-agent as the first agent-based system and a major step beyond direct patch generation.

## Capability observed
The system couples an LLM with an engineered agent-computer interface so the model can inspect repositories, edit files, execute commands, observe results, and iterate toward an issue resolution.

## Architectural lesson
Agent capability depends strongly on the interface between model and environment. Tool affordances, context presentation, action space, feedback, and verification are part of the system architecture rather than incidental prompt details.

## AlgoX extraction
- Repository-aware agent environment
- Explicit action/tool interface
- Iterative execution loop
- Software-engineering-specific context
- Test-driven feedback
- Benchmark-first agent evaluation
- Reproducible task environments

## Relevance to AlgoX
Directly relevant to research-agent architecture. AlgoX should treat its research environment, source retrieval, evidence capture, experiment execution, and validation tools as a deliberate capability surface.

## Evidence
SWE-bench project history and SWE-agent release evidence: https://www.swebench.com/original.html
SWE-agent repository: https://github.com/SWE-agent/SWE-agent

**Evidence maturity:** C2
**Status:** RESEARCHED
