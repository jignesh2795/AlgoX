# 2024 Capability Evolution

## From experimentation to infrastructure

The 2024 evidence indicates a shift from demonstrating what an LLM or agent can do toward engineering reusable systems around models.

### Capability stack

```text
Foundation Model
      ↓
Inference / Runtime
      ↓
Context + Retrieval
      ↓
Tools + Environment
      ↓
Workflow / Agent
      ↓
Evaluation
      ↓
Governance / Application
```

## Capabilities that became stronger

### 1. Inference as infrastructure

Model serving became an explicit systems concern: batching, memory management, latency, throughput and cost matter independently of model quality.

### 2. Context engineering

Retrieval is no longer just an embedding lookup. The system must select, rank, constrain and evaluate context before reasoning.

### 3. Controlled execution

Coding agents demonstrated that environment access, sandboxing, tool permissions and observation loops are architectural components.

### 4. Evaluation infrastructure

Evaluation moved closer to the agent runtime. A benchmark is most useful when the same execution environment can reproduce the evaluated workflow.

### 5. Human control

Approval, checkpoints and bounded execution remain valuable even as autonomy increases.

## AlgoX consequence

The research system should model these as independent capabilities rather than creating one generic `Agent` capability.

```text
Agent
├── Model interface
├── Context selection
├── Memory
├── Tool execution
├── Environment
├── Planning
├── Verification
├── Evaluation
├── Permissions
└── Recovery
```

This decomposition allows individual capabilities to be benchmarked and replaced.

## Trading-system parallel

The same decomposition applies to future financial systems:

```text
Trading Agent / Strategy
├── Market context
├── Portfolio state
├── Risk policy
├── Tool / broker access
├── Execution environment
├── Verification
├── Reconciliation
├── Evaluation
└── Audit
```

## Status

**PROVISIONAL — 2024 capability model.**
