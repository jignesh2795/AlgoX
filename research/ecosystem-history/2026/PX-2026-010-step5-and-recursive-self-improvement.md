# PX-2026-010 — Step 5 Preview and recursive self-improvement

**Research date:** 2026-09-21
**Status:** validated research finding; model/evolution architecture input
**AlgoX area:** inference / agent models / continual improvement / provenance / evaluation

## Finding

Two September 2026 developments materially extend the AlgoX ecosystem model.

### Step 5 Preview

StepFun launched Step 5 Preview on 2026-09-20 as a hosted sparse-MoE model with 600B total parameters, 27B active parameters per token and a 1M-token context window. Open weights are announced for 2026-10-15; as of this research date the weights are not yet available.

The immediate architectural lesson is that agent-model capability catalogs must distinguish total parameters from active parameters, memory footprint, context/cache behavior, serving constraints, modality, cost and deployment status. A hosted preview must not be classified as open-weight merely because an open-weight release is promised.

**AlgoX decision:** ADOPT a deployment-aware model capability schema and track `availability_status`, `open_weight_status`, `active_parameters`, `total_parameters`, `context_limit`, `cache_characteristics`, `serving_requirements`, `cost_profile` and `independent_evaluation_status`.

### RSIAgent

The September 2026 RSIAgent research proposes a training-free multi-agent framework for recursive self-improvement through autonomous memory construction. It separates curriculum, actor and verifier roles and retains environment-specific causal relationships between actions, conditions and consequences.

**AlgoX implication:** persistent improvement should not be modeled only as model-weight changes. Agent improvement can occur through structured memory and environment-specific knowledge. Therefore an agent lineage should track changes to model, harness, skills, retrieval, memory and policy independently.

A useful abstraction is:

```text
AgentVersion
  -> ModelVersion
  -> HarnessVersion
  -> SkillSetVersion
  -> RetrievalPolicyVersion
  -> MemoryPolicyVersion
  -> CapabilityPolicyVersion
  -> EnvironmentVersion
```

The verifier/evaluator remains independent from the actor's improvement process.

## Combined architecture lesson

The ecosystem is increasingly separating **capability acquisition** from **capability promotion**:

```text
Explore / Modify
      -> Observe
      -> Verify
      -> Record evidence
      -> Compare against baseline
      -> Promote a versioned component
```

AlgoX should therefore treat recursive improvement as a graph of independently versioned components rather than a single mutable agent state.

## Evidence boundary

Step 5's benchmark and pricing claims should be treated as vendor claims until independently reproduced. RSIAgent's reported gains should likewise remain research evidence until reproduced under AlgoX's evaluation protocol.

## Decision status

**ADOPT conceptually; monitor implementation evidence.**

Do not add Step 5 to the local-model deployment catalog until the promised weights, license and independent evaluations are available.

## External references

- StepFun Step 5 Preview announcement/documentation — announced 2026-09-20; open-weight release announced for 2026-10-15.
- RSIAgent, arXiv:2609.15364 — published 2026-09-14.
