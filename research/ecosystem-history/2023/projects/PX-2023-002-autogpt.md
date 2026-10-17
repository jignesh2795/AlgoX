# PX-2023-002 — AutoGPT

**Repository:** https://github.com/Significant-Gravitas/AutoGPT
**Historical category:** BREAKOUT / SUSTAINED historical significance
**Domain:** Autonomous agents

## 2023 signal
AutoGPT was one of the defining early open-source agent experiments of 2023. GitHub's 2023 report specifically identified Significant-Gravitas/Auto-GPT among community-driven projects with a surge in first-time contributors and among leading generative-AI projects.

## Capability observed
The project demonstrated an LLM-driven loop intended to pursue a user-defined goal through autonomous task execution, tool use, and iterative reasoning.

## Architectural lesson
The agent loop made planning/execution/tool interaction a first-class software architecture rather than a single model call.

## Failure lessons to investigate
Early autonomous-agent systems exposed reliability, verification, runaway execution, cost, and hallucination problems. These are research targets, not assumptions that the architecture is production-ready.

## AlgoX extraction
- Agent loop
- Task decomposition
- Tool interface
- Iterative execution
- Autonomous workflow concept
- Need for bounded execution and verification

## Evidence
GitHub Octoverse 2023: https://github.blog/news-insights/research/the-state-of-open-source-and-ai/
Repository: https://github.com/Significant-Gravitas/AutoGPT
Historical resource timeline: https://github.com/ScarletPan/awesome-autonomous-gpt

**Evidence maturity:** C1
**Status:** RESEARCHED
