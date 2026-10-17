# 2025 Multimodal Tool Use and Agent Observability

## Status
PROVISIONAL.

## Research question
Did 2025 agent systems make tool use, multimodal interaction, learning from experience, and operational observability sufficiently explicit to become durable architectural capabilities?

## Evidence themes

2025 tool-learning surveys organize agent capability around three recurring problems: selecting the appropriate tool, planning multi-step tool use, and executing tools reliably. Multimodal tools extend this from text-only interfaces to visual and other environment observations.

Recent 2025 work also demonstrates an important training pattern: task synthesis → tool/action sampling → independent verification → preference or policy improvement. This is stronger than simply storing successful trajectories because the verifier becomes part of the learning loop.

## Findings

### 1. Tool use is a first-class subsystem

A production research agent should not expose an undifferentiated tool bag. Tools need:

- typed capabilities
- input/output contracts
- permissions
- cost/latency metadata
- side-effect classification
- provenance of observations
- failure semantics
- retry policy
- verification requirements

### 2. Multimodality should be treated as an observation boundary

Images, PDFs, charts, tables, audio and UI state are observations. They should enter the same evidence pipeline as textual sources rather than creating a separate, ungoverned memory system.

```text
External artifact
      ↓
Observation adapter
      ↓
Normalized evidence
      ↓
Provenance + locator
      ↓
Knowledge / memory
```

The original artifact must remain available when interpretation matters for later audit.

### 3. Verification should operate at trajectory and step level

2025 tool-use research increasingly uses verifiers for generated trajectories and individual actions. This supports an AlgoX design where a long agent run is decomposed into auditable steps rather than being accepted as one opaque answer.

```text
Task
 ↓
Plan
 ↓
Tool action
 ↓
Observation
 ↓
Step verifier
 ↓
Next action
 ↓
Trajectory verifier
 ↓
Outcome
```

### 4. Learning from experience is different from memory storage

Memory answers: "What happened / what is known?"

Learning answers: "What behavior should change because of what happened?"

Therefore AlgoX should preserve both:

```text
Episode
 ├── observations
 ├── actions
 ├── outcome
 ├── evidence
 └── evaluation

Learning artifact
 ├── extracted lesson
 ├── applicable conditions
 ├── confidence
 ├── validation evidence
 └── resulting procedure/policy change
```

A successful trajectory must not automatically become a trusted procedure.

### 5. Observability is part of agent intelligence

Agent runs need structured telemetry for:

- task identity
- model/provider
- model version
- prompt/context version
- tool calls
- tool latency
- token/compute budget
- intermediate observations
- verifier results
- failures/retries
- final outcome
- human interventions
- resulting memory/knowledge changes

This is necessary for debugging, benchmarking, cost attribution and historical reconstruction.

## AlgoX architectural consequence

The brain should evolve from:

```text
Memory + Retrieval + LLM
```

toward:

```text
Memory
 + Evidence
 + Tools
 + Environment observations
 + Verifiers
 + Telemetry
 + Learning artifacts
 + Governance
```

## Financial-system boundary

Multimodal and agentic capabilities should remain on the research/analysis side until independently validated. An agent may inspect a chart, broker document, PDF, dashboard or source repository, but an interpreted observation must not directly authorize an irreversible trading action.

```text
Multimodal observation
        ↓
Evidence
        ↓
Analysis
        ↓
Recommendation
        ↓
Deterministic policy / risk gate
        ↓
Execution
```

## Evidence discipline

The 2025 literature supports the direction of tool selection, multimodal interaction, verification and learning-from-experience. It does not establish that any particular agent framework is production-ready for financial execution. Framework claims remain implementation-specific and require independent reproduction.

## AlgoX decision

**ADOPT as architectural principles:**
- typed tool registry
- observation/evidence adapters
- step-level verification
- trajectory-level verification
- structured agent telemetry
- separate memory from learned procedures
- explicit human/policy intervention records

**TRIAL:**
- automatic learning from trajectories
- multimodal agent control
- verifier-generated feedback

**HOLD:**
- autonomous mutation of production trading policy
- direct agent authorization of irreversible financial actions
