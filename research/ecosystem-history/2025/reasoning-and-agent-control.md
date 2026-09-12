# 2025 Reasoning and Agent Control

## Status
PROVISIONAL.

## Research question
What changed in 2025 from the 2024 controlled-workflow architecture: better reasoning, better search, better environments, or genuinely safer autonomy?

## Findings

### 1. Reasoning became an execution-time resource
2025 coding-agent research increasingly treats reasoning as a process that can search, branch, inspect intermediate state and backtrack. SWE-Search is representative: Monte-Carlo-tree-search-style exploration improved repository-level repair performance over simpler trajectories.

The architectural consequence is:

```text
Model
  ↓
Reasoning / Search Controller
  ↓
Candidate actions
  ↓
Environment
  ↓
Observations / tests
  ↓
Evaluation
  ↓
Continue / backtrack / stop
```

The model should therefore not be equated with the whole agent runtime.

### 2. Verification remains outside the model
The 2025 benchmark corrections are strong evidence that self-reported or test-only success is insufficient. The environment and evaluator must independently determine whether an action achieved its objective.

For AlgoX:

```text
Agent claim
    ↓
Independent verifier
    ↓
Evidence
    ↓
Institutional knowledge
```

Not:

```text
Agent claim → truth
```

### 3. More autonomy increases the need for policy boundaries
An agent that can browse, edit files, execute programs, install dependencies and modify durable state has a larger failure surface. 2025 agent-security research also evaluates privacy/data-minimization failures in realistic end-to-end environments, showing that model-level prompting alone is not a sufficient control boundary.

Therefore permissions should be explicit:

- read-only
- sandbox write
- execute
- network access
- credential access
- durable knowledge proposal
- durable knowledge commit
- irreversible external action

### 4. Human collaboration is a capability, not merely a fallback
RExBench's results indicate that realistic research-extension tasks still require substantial human guidance. AlgoX should therefore optimize for **human-agent research throughput**, not maximum unattended autonomy.

A productive workflow is:

```text
Human objective
      ↓
Agent research
      ↓
Candidate findings
      ↓
Evidence / experiments
      ↓
Human or policy review
      ↓
Knowledge commit
```

### 5. Cost and time belong in evaluation
A more capable agent can spend substantially more inference, tool and execution resources. Therefore AlgoX should record:

- wall-clock time
- model/tool calls
- compute cost where measurable
- retries
- search depth
- human interventions
- successful outcome
- failure mode

Capability should be measured as value per resource, not success rate alone.

## 2023 → 2024 → 2025 evolution

```text
2023
Agent loop + tools + memory
        ↓
2024
Controlled workflows + environments + evaluation
        ↓
2025
Search + verification + long-horizon evaluation + continual experience
```

The evolution is real, but it is not evidence that autonomous production engineering has been solved.

## AlgoX architectural decision
The research-agent runtime should expose separate components for:

1. Model provider
2. Context/evidence retrieval
3. Planning/reasoning controller
4. Tool policy
5. Execution environment
6. Verifier/evaluator
7. Memory/consolidation
8. Governance/approval
9. Audit trail

No component should silently absorb another component's authority.

## Financial-system implication
For financial workflows, reasoning agents may assist with research, diagnostics, reconciliation analysis, scenario generation and engineering tasks. They should not receive unrestricted authority over irreversible execution merely because their reasoning benchmark improves.

The deterministic execution/risk boundary remains authoritative.

## Decision
**ADOPT** explicit reasoning/search control as a capability.

**ADOPT** independent verification and policy-controlled environments.

**ADAPT** human-agent collaboration as the default operating model for high-impact research.

**HOLD** autonomous irreversible financial execution until independent production evidence exists.

## Confidence
High for the verification and control-boundary findings; medium for claims about the superiority of particular reasoning/search techniques because benchmark and scaffold effects remain significant.
