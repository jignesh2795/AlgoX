# PX-2026-014 — Harness-native agent training and closed-loop improvement

**Research date:** 2026-11-08  
**Covered releases:** 2026-07-23 to 2026-09-30  
**Status:** validated research and product findings; training/evolution architecture input  
**AlgoX area:** agent training / rollouts / environments / experiment lineage / model operations

## Finding

The agent-training stack is expanding beyond training model weights in isolation. Two complementary efforts expose the harness and deployed agent configuration as part of the training/evaluation loop.

### OpenForgeRL

[OpenForgeRL](https://github.com/MSR-Orchard/OpenForge-RL) is an open-source framework for training harness-native agents in diverse environments. Its paper describes a lightweight proxy that serves model calls from a real agent harness while recording them as training data for a conventional RL system such as veRL. A Kubernetes orchestrator runs each rollout in a separate remote container.

The central architectural contribution is the decoupling of **harness inference**, **rollout recording**, and **policy optimization**. The paper reports experiments across tool-based agents and GUI/browser/computer-use agents, and reports that harness choice affects learnability and behavior. Its public repository warns that portions are still being reorganized and may contain incomplete scripts or unpublished assets.

### CoreWeave Forge and RL Rollouts

[CoreWeave Forge](https://www.coreweave.com/news/coreweave-forge-launches-turning-the-ai-loop-production-run-into-a-better-model-and-agent) was announced on September 30, 2026 as a connected environment for running, observing, curating, improving and evaluating models and agents. Its product description includes a registry for versioned checkpoints and agent configurations, serverless post-training/RL, and an RL Rollouts preview that can hot-load checkpoints into a live inference deployment.

CoreWeave's speed and cost comparisons are vendor-reported and are not treated here as independently reproduced findings.

## AlgoX implications

A training run should not be represented by a checkpoint alone. The minimum lineage should connect:

```text
AgentConfiguration
  -> HarnessVersion
  -> EnvironmentVersion
  -> RolloutPolicy
  -> AgentRun / Trajectory
  -> Reward / EvaluatorVersion
  -> TrainingRun
  -> Checkpoint
  -> Independent Evaluation
  -> PromotionDecision
```

Important consequences:

- Record which harness actually executed each trajectory.
- Persist the remote environment/container image and resource envelope for each rollout.
- Separate rollout collection from reward evaluation and policy optimization.
- Record checkpoint hot-swaps and deployment revisions as explicit events.
- Evaluate the resulting checkpoint again in a frozen, independent environment.
- Retain unsuccessful rollouts and failures; they are part of the training/evidence lineage.

## Decision

**ADOPT conceptually.** OpenForgeRL is a technical reference for harness-native rollouts and environment isolation. CoreWeave Forge is a reference for connecting production observations to versioned post-training and deployment workflows. AlgoX should model these contracts and provenance edges, not reproduce a commercial training cloud or a full RL stack.

## Sources

- OpenForgeRL paper: https://arxiv.org/abs/2607.21557
- OpenForgeRL repository: https://github.com/MSR-Orchard/OpenForge-RL
- Microsoft Research publication page: https://www.microsoft.com/en-us/research/publication/openforgerl-train-harness-native-agents-in-any-environment/
- CoreWeave Forge announcement: https://www.coreweave.com/news/coreweave-forge-launches-turning-the-ai-loop-production-run-into-a-better-model-and-agent
