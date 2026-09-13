# PX-2026-001 — Agent evolution stack: CORAL, Reef, reef-eval

**Research date:** 2026-09-13
**Status:** validated research finding; architecture input, not implementation
**AlgoX area:** agent architecture / evaluation / continual improvement / provenance

## Finding

The 2026 open-source agent ecosystem is converging on a stack in which autonomous improvement is separated into execution, observation, experimentation, evaluation, and versioned promotion.

Three projects are especially complementary:

- **CORAL** — autonomous multi-agent research infrastructure with isolated workspaces, grading, persistent shared state, and multi-island exploration.
- **Reef** — continual-learning infrastructure that can evolve either agent harnesses or model artifacts and publish accepted versions while rejected candidates leave the serving release unchanged.
- **reef-eval** — evaluation infrastructure for self-evolving agents, adding judges, task streams, persistent result storage, budgets, and metrics on top of Harbor.

## Architecture implications for AlgoX

AlgoX should not become another monolithic coding-agent framework. The stronger opportunity is an evidence-governed substrate underneath multiple agents.

Recommended conceptual loop:

```text
SERVE
  -> OBSERVE
  -> HYPOTHESIZE
  -> EXPERIMENT
  -> INDEPENDENT EVALUATION
  -> EVIDENCE
  -> CANDIDATE VERSION
  -> REGRESSION GATES
  -> PROMOTE / REJECT
```

### Primitives to adopt

1. **Experiment isolation** — separate workspaces and execution environments.
2. **Evaluator isolation** — the agent must not be able to read private grader state or answer keys.
3. **Receipt-linked interactions** — every important interaction should have a stable ID that later feedback/evaluation can reference.
4. **Versioned agent state** — model, prompt, skills, retrieval policy, tools, evaluator set and policy configuration should form an identifiable agent version.
5. **Candidate promotion** — improvements should be candidates until independently evaluated.
6. **Evaluation streams** — repeated/ordered tasks should measure retention and regression, not just one-shot benchmark accuracy.
7. **Reproducible learning records** — a claimed improvement needs pinned configuration, raw per-version results, an explicit acceptance criterion, and a reproducible command.

## AlgoX-specific extension

AlgoX should add an explicit provenance layer between evaluation and institutional knowledge:

```text
Interaction
  -> Experiment
  -> Evaluation
  -> Evidence
  -> Claim
  -> Validated Knowledge
```

Knowledge must not be promoted merely because an agent used it successfully once. Promotion should retain evidence, validation history, confidence, and the agent versions that depended on it.

## Improvement-source taxonomy

Every promoted improvement should identify its primary cause where possible:

- MODEL
- PROMPT
- SKILL
- RETRIEVAL
- MEMORY
- TOOLING
- ORCHESTRATION
- EXECUTION
- COMBINATION
- UNKNOWN

This is important for historical ecosystem analysis because benchmark gains otherwise cannot be attributed correctly.

## Key external evidence

- CORAL: https://github.com/Human-Agent-Society/Coral
- Reef: https://github.com/Human-Agent-Society/reef
- reef-eval: https://github.com/Human-Agent-Society/reef-eval
- Reef roadmap: https://github.com/Human-Agent-Society/reef/issues/25

## AlgoX decision

**Adopt conceptually, do not copy wholesale.** CORAL provides strong experiment/isolation primitives; Reef provides versioned continual-improvement mechanics; reef-eval provides the evaluation substrate. AlgoX's differentiation should remain evidence provenance and controlled knowledge promotion.
