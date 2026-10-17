# 2025 Capability Gap Analysis

Status: PROVISIONAL

## Objective

Compare the current AlgoX architecture with the capabilities evidenced by 2025 research.

## Capability matrix

| Capability | Current AlgoX | 2025 evidence | Gap | Priority |
|---|---|---|---|---|
| Evidence/provenance | Strong foundation | Required for reliable agents | Extend into agent traces | High |
| Temporal knowledge | Implemented conceptually | Dynamic financial environments require time-aware state | Integrate trace/event time | High |
| Memory types | Working/episodic/semantic/procedural/source/meta | Modern memory systems use differentiated memory | Consolidation policy needed | High |
| Memory consolidation | Designed conceptually | Continual-learning agents need controlled accumulation | Implement governor | High |
| Tool registry | Not yet first-class | Tool use is central to agent capability | Add typed registry and permissions | High |
| Tool verification | Partial governance | Agent benchmarks show action-level failure | Add tool-result verification | High |
| Context compiler | Architecture defined | Context must be bounded and provenance-preserving | Implement | High |
| Compute policy | Research finding only | Adaptive compute/routing is increasingly important | Implement policy interface | Medium |
| Model routing | Not implemented | Different tasks have different cost/quality needs | Experiment | Medium |
| Agent traces | Not implemented | Production agents require trace/span visibility | Implement vendor-neutral schema | High |
| Agent evaluation | Benchmark foundation exists | Trajectory-level evaluation needed | Add trajectory evaluator | High |
| Online evaluation | Not implemented | Production quality needs live sampling | Trial after trace layer | Medium |
| Financial agent evaluation | Research evidence only | Live multi-market benchmarks emerging | Build reproducible finance suite | High |
| Risk-aware evaluation | Financial architecture exists | Risk control strongly affects agent robustness | Connect evaluation to risk metrics | High |
| Replay | Conceptually supported | Live-agent reproducibility needs replay | Implement event replay model | High |
| Failure injection | Planned | Production reliability requires adversarial testing | Build experiment harness | High |
| Audit | Implemented | Financial agents need durable action history | Connect to agent traces | High |
| Human approval | Governance foundation | High-impact actions require explicit boundaries | Add action-policy gate | High |
| Multimodal evidence | Not first-class | Agents increasingly operate on charts/docs/screens | Add observation adapters | Medium |
| Production SLOs | Not implemented | Serving systems require latency/cost/resource controls | Add measurement model | Medium |

## Priority 1 — Agent execution evidence

AlgoX should next implement a vendor-neutral trajectory model:

```text
AgentRun
├── task
├── versions
├── context
├── evidence
├── tool calls
├── observations
├── decisions
├── verification
├── approvals
├── outcome
└── audit references
```

Every step should have timestamps and stable IDs.

## Priority 2 — Consolidation Governor

The current memory system can store knowledge, but institutional learning needs a controlled promotion path:

```text
Episode
  ↓
Evaluation
  ↓
Candidate Lesson
  ↓
Evidence Check
  ↓
Contradiction Check
  ↓
Temporal Check
  ↓
Approval Policy
  ↓
Institutional Memory
```

The governor must be able to reject a lesson.

## Priority 3 — Financial agent evaluation

Create a benchmark layer capable of evaluating agents without allowing the agent to redefine its own metrics.

Minimum domains:

1. market research
2. financial data analysis
3. portfolio recommendation
4. risk analysis
5. trading simulation
6. execution planning

Metrics should include task correctness plus financial/risk metrics where applicable.

## Priority 4 — Replay and causal debugging

Agent traces should be replayable against the same evidence/context versions.

```text
Original Run
   ↓
Trace
   ↓
Frozen Evidence
   ↓
Frozen Tool Results
   ↓
Replay
   ↓
Compare
```

This allows AlgoX to distinguish model drift, retrieval drift, tool drift, policy drift and environment drift.

## Priority 5 — Multimodal observation

Do not store raw multimodal observations only inside prompts. Convert them into evidence objects with:

- source artifact
- modality
- locator
- extraction method
- timestamp
- confidence
- derived claims

## Technology decision

No database change is justified by this research alone.

The current PostgreSQL-first direction remains appropriate because the missing capabilities are primarily **data contracts, evaluation semantics, governance and traceability**, not a particular database engine.

## 2025 architectural gap

The major missing layer is now:

```text
                    AGENT RUNTIME
                         ↓
             ┌──────────────────────┐
             │  TRACE / OBSERVE     │
             └──────────┬───────────┘
                        ↓
             ┌──────────────────────┐
             │   EVALUATE / VERIFY  │
             └──────────┬───────────┘
                        ↓
             ┌──────────────────────┐
             │ CONSOLIDATE / GOVERN │
             └──────────┬───────────┘
                        ↓
                 INSTITUTIONAL
                    KNOWLEDGE
```

This closes the loop between agent execution and AlgoX's existing evidence/memory architecture.