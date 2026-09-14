# ALG-ARCH-001 — AlgoX provenance architecture

**Research date:** 2026-09-14  
**Status:** architecture baseline; design candidate, not implementation  
**Scope:** agent execution, evidence, evaluation, learning, knowledge promotion

## 1. Purpose

AlgoX needs a durable way to explain **why a result, claim, or learned artifact should be trusted**.

The repository research now points to a consistent ecosystem split:

- trading systems provide deterministic domain and execution contracts;
- agent-evolution systems provide experiment isolation and version promotion;
- agent-evaluation systems provide independent scoring and regression measurement;
- agent-retrieval systems optimize context acquisition for the workflow;
- provenance research provides the missing connective tissue between execution, evidence, claims, evaluation and institutional knowledge.

AlgoX should therefore be an **evidence/provenance substrate**, not another autonomous-agent framework.

## 2. Architectural position

```text
                 AGENT / TRADING SYSTEMS
                          |
                          v
                   +--------------+
                   |  Interaction |
                   +--------------+
                          |
                          v
                   +--------------+
                   | ExecutionEvent|
                   +--------------+
                    /      |       \
                   v       v        v
              Retrieval   Tool    Memory
                   |       |        |
                   +-------+--------+
                           |
                           v
                    +-------------+
                    |   Evidence  |
                    +-------------+
                           |
                           v
                    +-------------+
                    |    Claim    |
                    +-------------+
                           |
                           v
                    +-------------+
                    |  Evaluation |
                    +-------------+
                           |
                           v
                    +-------------+
                    |  Experiment |
                    +-------------+
                           |
                           v
                  +-------------------+
                  | PromotionDecision |
                  +-------------------+
                           |
                           v
                     AgentVersion N+1
                           |
                           v
                  Validated Knowledge
```

The important boundary is that **execution produces evidence; evaluation validates evidence/claims; promotion converts validated results into reusable versioned state**.

## 3. Core entities

### 3.1 AgentVersion

Identifies the exact agent configuration used for an interaction or experiment.

```text
AgentVersion
- id
- parent_version
- model
- model_version
- prompt_version
- skills_version
- retriever_version
- memory_policy_version
- tool_policy_version
- environment_version
- created_at
```

A model name alone is insufficient. Changes to prompts, skills, retrieval policy, memory policy, tools or environment can change outcomes and must be attributable.

### 3.2 Interaction

The externally meaningful task/session boundary.

```text
Interaction
- id
- agent_version
- task
- input_ref
- output_ref
- execution_id
- timestamp
```

### 3.3 ExecutionEvent

The ordered provenance stream inside an interaction.

```text
ExecutionEvent
- id
- interaction_id
- sequence
- type
- actor
- input_ref
- output_ref
- timestamp
```

Initial event types should include:

`RETRIEVE`, `TOOL_CALL`, `OBSERVATION`, `MEMORY_READ`, `MEMORY_WRITE`, `ACTION`, `CLAIM`.

The event stream should remain append-oriented. Derived summaries may be regenerated; the underlying event identity should remain stable.

### 3.4 Evidence

An evidence object records the information that can support or challenge a claim.

```text
Evidence
- id
- source
- source_version
- retrieval_event
- content_ref
- authority
- relevance
- sufficiency
- timestamp
```

AlgoX must explicitly distinguish:

```text
Retrieved != Relevant != Sufficient != Authoritative != Validated
```

This prevents a common failure mode where retrieval itself is treated as proof.

### 3.5 Claim

A claim is an assertion made by an agent or derived process.

```text
Claim
- id
- interaction_id
- statement
- evidence_refs[]
- confidence
- status
```

A claim should be promotable only when its supporting evidence and validation state are inspectable.

### 3.6 Evaluation

Evaluation is an independent judgment about a task, claim, candidate, or version.

```text
Evaluation
- id
- subject
- benchmark
- task
- evaluator_version
- score
- metrics
- evidence_refs[]
```

Evaluator identity and version are first-class because evaluation itself can change over time.

### 3.7 Experiment

An experiment links a hypothesis to a controlled comparison.

```text
Experiment
- id
- hypothesis
- baseline_version
- candidate_version
- environment
- budget
- variables
- results
- evaluation_refs[]
```

Experiments should retain enough configuration to distinguish genuine improvement from environment, evaluator, sampling or budget changes.

### 3.8 PromotionDecision

Promotion is a governance event, not an automatic side effect of a good score.

```text
PromotionDecision
- id
- candidate_version
- baseline_version
- evaluation_set
- decision
- reason
- regressions
- confidence
- approved_at
```

Possible decisions:

`PROMOTE`, `REJECT`, `HOLD`, `ROLLBACK`.

## 4. Typed relationships

The initial implementation should use ordinary relational tables with immutable IDs and typed foreign-key relationships rather than introducing a graph database prematurely.

Conceptual edges:

```text
AgentVersion -> Interaction
Interaction -> ExecutionEvent
ExecutionEvent -> Evidence
Evidence -> Claim
Claim -> Evaluation
Experiment -> Evaluation
Experiment -> AgentVersion
Evaluation -> PromotionDecision
PromotionDecision -> AgentVersion
AgentVersion -> ValidatedKnowledge
ValidatedKnowledge -> Evidence
```

A graph projection can be added later without changing the underlying provenance model.

## 5. Retrieval contract

The retrieval layer should eventually accept more than a text query.

Minimum conceptual input:

```text
RetrievalRequest
- interaction_id
- current_event
- task
- agent_state
- previous_events
- candidate_scope
- retrieval_policy_version
```

Output should include both selected and abstained candidates:

```text
RetrievalResult
- evidence_id
- relevance
- authority
- reason
- policy_version
- selected
```

The ability to record **why context was not retrieved** is important for selective retrieval and later policy learning.

## 6. Evaluation contract

AlgoX should support evaluation at multiple levels:

1. **Retrieval** — did the system acquire useful context?
2. **Context construction** — was the right evidence assembled?
3. **Task execution** — did the agent accomplish the task?
4. **Long-horizon improvement** — did repeated experiments improve the baseline?
5. **Experiment efficiency** — how much time/cost/evaluation budget produced improvement?
6. **Knowledge reuse** — did validated knowledge improve future work?
7. **Regression/forgetting** — did improvements damage previously validated capabilities?
8. **Autonomous research** — can the system discover and validate improvements with limited intervention?

These correspond to the benchmark decomposition already recorded in `PX-2026-002`.

## 7. Promotion rule

A candidate should not become institutional knowledge merely because one run succeeded.

Conceptually:

```text
candidate result
      |
      v
independent evaluation
      |
      +---- regression? ---- yes ---> REJECT / HOLD
      |
      no
      v
sufficient evidence?
      |
      +---- no ---------------------> HOLD
      |
      yes
      v
promotion decision
      |
      v
versioned knowledge + provenance
```

Promotion should preserve:

- supporting evidence;
- evaluator/version;
- baseline and candidate versions;
- benchmark/task set;
- observed regressions;
- confidence;
- reproduction information;
- cause taxonomy where known.

## 8. Cause attribution

Every improvement should attempt to classify its cause:

`MODEL`, `PROMPT`, `SKILL`, `RETRIEVAL`, `MEMORY`, `TOOLING`, `ORCHESTRATION`, `EXECUTION`, `COMBINATION`, `UNKNOWN`.

This prevents AlgoX's historical knowledge base from recording a benchmark gain without recording what actually caused it.

## 9. Ecosystem traceability

| External capability | AlgoX architectural destination |
|---|---|
| CORAL experiment isolation and multi-agent evolution | Experiment + ExecutionEvent |
| Reef continual learning/version promotion | AgentVersion + PromotionDecision |
| reef-eval evaluation streams and trusted judges | Evaluation |
| LRAT trajectory-aware retrieval | RetrievalRequest + RetrievalResult |
| Agent Retrieval Bench selective/context retrieval | Evidence + retrieval abstention |
| AutoLab long-horizon research metrics | Experiment + Evaluation |
| Evidence/provenance research | Evidence + Claim + typed provenance edges |
| Mature trading-engine architectures such as LEAN | deterministic execution/domain boundary beneath agent layer |

These are **reference inputs**, not components to copy wholesale.

## 10. Non-goals for the current phase

Do not yet:

- build a full autonomous coding-agent framework;
- build a custom foundation model;
- introduce Neo4j or another graph database solely for provenance;
- implement a production retrieval system before defining its evaluation contract;
- promote memory automatically from successful single interactions;
- couple evidence storage directly to one agent vendor or model provider.

## 11. Phase gate

The next implementation phase should begin only after the following are specified:

- minimal relational schema;
- immutable ID and versioning rules;
- evidence lifecycle and authority policy;
- evaluator isolation/trust model;
- retrieval interface;
- experiment reproducibility contract;
- promotion/regression gates;
- one deterministic end-to-end pilot.

**Decision:** ADOPT as the current AlgoX architecture baseline. Implementation is deliberately deferred until the phase gate is satisfied.

## 12. Research basis

- `PX-2023-038` — LEAN reference architecture.
- `PX-2023-039` — CCXT/LEAN boundary.
- `PX-2023-040` — India-market architecture requirements.
- `PX-2026-001` — agent evolution stack.
- `PX-2026-002` — agent-native retrieval and research evaluation.
- Current ecosystem evidence also includes CORAL's isolated worktrees, grader isolation and multi-island evolution, reinforcing the separation between agent execution and independent evaluation.
