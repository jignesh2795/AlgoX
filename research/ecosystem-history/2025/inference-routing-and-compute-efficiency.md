# 2025 Inference Routing and Compute Efficiency

## Status
PROVISIONAL.

## Research question
How should AlgoX allocate model capacity, reasoning effort, latency budget and inference cost across heterogeneous research tasks?

## Evidence themes

### 1. Test-time compute became an explicit resource
2025 research shows that additional inference-time computation can improve reasoning quality, but the benefit depends on task difficulty and the allocation strategy. Compute-optimal approaches can outperform naive best-of-N or simply choosing a larger model under matched compute.

### 2. More reasoning is not automatically better
Agentic reasoning can improve accuracy while increasing latency variance and infrastructure cost. Reflection depth, parallel rollouts and repeated verification therefore need explicit budgets rather than unlimited recursion.

### 3. Model routing is a capability
Adaptive routing can choose among models and sampling strategies according to task difficulty and quality requirements. This makes model selection part of system architecture rather than a permanent application-level configuration.

### 4. Inference infrastructure is layered
High-throughput serving systems expose scheduling, batching, caching, speculative decoding, distributed execution and serving-layer concerns as distinct capabilities. AlgoX should research these independently rather than treating an inference engine as a monolith.

## AlgoX extraction

The future research brain should have an explicit **Compute Policy** between task planning and model invocation:

```text
Research Task
    ↓
Task Classification
    ↓
Difficulty / Risk Estimate
    ↓
Compute Policy
    ├── model tier
    ├── reasoning budget
    ├── context budget
    ├── number of rollouts
    ├── verification budget
    ├── latency budget
    └── cost budget
    ↓
Model / Runtime
    ↓
Verifier
    ↓
Evidence Bundle
```

## Important consequence
Model choice should be recorded as experimental evidence. A future AlgoX run should be able to answer:

- Which model was used?
- Why was it selected?
- What compute budget was allocated?
- What alternatives were available?
- What did the verification stage cost?
- Did additional reasoning improve the result?
- Was the improvement worth the latency and cost?

## Research decision
**ADOPT as an architectural capability:** explicit compute/resource policy.

**TRIAL:** adaptive model routing and test-time compute allocation.

**HOLD:** assuming one permanently preferred model or unlimited reasoning.

## Boundary
These findings concern research-agent infrastructure, not direct financial execution. Compute optimization must not weaken evidence, verification, governance or audit requirements.
