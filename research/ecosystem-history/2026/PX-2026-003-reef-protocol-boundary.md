# PX-2026-003 — Reef protocol boundary and agent-skill ecosystem

**Research date:** 2026-09-14
**Status:** validated ecosystem update; architecture input
**AlgoX area:** agent infrastructure / protocol boundaries / skills / parallel execution

## Meaningful developments

The Human-Agent-Society ecosystem has moved beyond a single Reef repository toward explicit protocol and client boundaries. As of September 12, 2026, `reef` depends on a separately maintained `reef-client` package, while `reef-client` provides a stdlib-only implementation of the Reef HTTP wire protocol.

The client exposes receipt/report interactions, harness-version discovery, served-harness retrieval, skill synchronization, trajectory/session capture and an optional local serving sidecar. This makes the agent/harness boundary independently installable and keeps protocol participation possible without importing the full Reef runtime.

Reef itself is now over 1.1k stars and was updated September 12, 2026. Its architecture continues to separate Serve, Observe, Grow and Commit, with SQL-backed interaction state and versioned artifact delivery.

## Architecture implication for AlgoX

This strengthens a principle already identified in AlgoX's provenance model:

**The provenance substrate should expose a stable protocol boundary rather than require every agent runtime to import the core implementation.**

Recommended separation:

```text
Agent / Harness
      |
      | protocol adapter
      v
Interaction + Evidence API
      |
      v
AlgoX provenance core
      |
      +--> Evaluation
      +--> Experiment
      +--> Knowledge
      +--> Promotion
```

A lightweight client/SDK can therefore be treated as a first-class architecture component. The core system owns persistence, identity, provenance and validation; adapters translate agent-specific events into the stable protocol.

## Additional ecosystem signal: skills as portable capability units

The open agent-skills ecosystem is becoming large enough to treat skills as versioned capability artifacts rather than incidental prompt files. K-Dense's scientific-agent-skills repository now reports 165 validated scientific skills and 100+ scientific databases, with compatibility across multiple coding/agent harnesses and the open Agent Skills standard. This is relevant to AlgoX's earlier `SKILL` improvement-source category.

AlgoX should therefore distinguish:

- `SkillDefinition` — reusable capability artifact;
- `SkillVersion` — immutable version;
- `SkillUsage` — evidence that a skill participated in an execution;
- `SkillEvaluation` — measured effect on a task/benchmark;
- `SkillPromotion` — decision to make a version available to future agents.

This avoids treating a successful prompt or skill edit as automatically validated knowledge.

## Parallel-agent execution signal

Stably's Orca is now a large open-source parallel-agent development environment, with activity through September 13, 2026. It is useful as a reference for the execution/orchestration layer: multiple coding-agent sessions can operate concurrently while the higher-level system coordinates the fleet.

AlgoX should catalog parallel execution separately from provenance. Parallelism is an execution capability; provenance must record which agent/session produced which evidence and whether parallel results were independently evaluated.

## Decisions

1. **ADOPT conceptually:** explicit protocol/client boundary for agent integration.
2. **ADOPT conceptually:** skills as versioned, measurable capability artifacts.
3. **CATALOG:** parallel-agent fleet orchestration as an execution-layer capability, not as the AlgoX core.
4. **DO NOT COPY:** Reef's implementation wholesale; reuse the architectural boundary and evidence lifecycle concepts.

## Sources

- Reef: https://github.com/Human-Agent-Society/reef
- Reef client: https://github.com/Human-Agent-Society/reef-client
- K-Dense scientific agent skills: https://github.com/K-Dense-AI/scientific-agent-skills
- Orca: https://github.com/stablyai/orca

## Historical significance

This is a meaningful evolution from the September 13 AlgoX architecture audit: the ecosystem is beginning to standardize the boundary between agent execution and continual-improvement infrastructure. AlgoX should preserve that boundary while making provenance, evidence and validation portable across runtimes.
