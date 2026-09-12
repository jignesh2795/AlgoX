# 2024 Capability Gap Analysis

## Status
PROVISIONAL — historical capability baseline.

## Purpose
Translate the 2024 research into capabilities that a serious financial research and trading platform must either possess, explicitly delegate, or treat as unresolved.

## Capability matrix

| Capability | 2024 evidence | AlgoX assessment | Target state |
|---|---|---|---|
| Market-data acquisition | Multiple providers and exchange/broker interfaces | Mature concept, provider-specific semantics remain important | ADOPT |
| Market-data normalization | Qlib/LEAN-style abstractions | Valuable but must preserve venue identity and source provenance | ADAPT |
| Data quality validation | Accuracy, completeness, consistency, timeliness and lineage evidence | Core correctness boundary | ADOPT |
| Instrument identity | Financial systems depend on stable security/reference identity | First-class capability | ADOPT |
| Corporate actions | Adjustments materially affect historical research and portfolio state | First-class temporal capability | ADOPT |
| Data lineage | Regulated financial-data evidence requires traceability | Institutional requirement | ADOPT |
| Feature/forecast research | Qlib and similar systems demonstrate modular research workflows | Separate from execution | ADOPT |
| Portfolio construction | Distinct decision capability | Separate policy boundary | ADOPT |
| Risk controls | Trading systems require explicit controls before irreversible actions | Deterministic gate | ADOPT |
| Execution lifecycle | LEAN/broker architectures show event-driven order state | Separate capability | ADOPT |
| Reconciliation | Broker/venue state can diverge from internal state | Runtime core | ADOPT |
| Idempotency | Required for retries and duplicate external events | Safety invariant | ADOPT |
| Recovery/restart | Production correctness includes restoring state after failure | Requires explicit experiments | TRIAL |
| Failure injection | Needed to establish resilience rather than assume it | Research gap | TRIAL |
| Observability | Monitoring is required for production operation and governance | Must cover data, decisions, orders and recovery | ADOPT |
| Historical reconstruction | Evidence and decisions evolve over time | Core institutional-memory capability | ADOPT |
| Experiment reproducibility | Benchmark/evaluation systems increasingly formalized | Required before decisions become durable | ADOPT |
| AI-assisted development | 2024 coding agents demonstrate repository-aware workflows | Useful under controlled verification | ADAPT |
| Autonomous execution | Evidence is insufficient for unconstrained AI control | High-risk unresolved area | HOLD |
| Semantic retrieval | Useful candidate generator | Derived projection only | TRIAL |
| Knowledge graph | Useful for relationships and temporal reasoning | Logical graph first; dedicated DB not yet justified | ADOPT logical / ASSESS physical |
| Vector database as authority | No evidence supports it as institutional truth | Contradicted by provenance/temporal requirements | REJECT |

## Capability boundaries

### Research boundary
Owns:
- datasets;
- feature generation;
- models;
- experiments;
- statistical evaluation;
- reproducibility.

Must not silently own live order lifecycle semantics.

### Decision boundary
Owns:
- portfolio targets;
- position sizing;
- constraints;
- risk overlays;
- policy decisions.

Must produce explainable intent before execution.

### Execution boundary
Owns:
- order lifecycle;
- venue adapters;
- retries;
- idempotency;
- partial fills;
- reconciliation;
- recovery.

Must not infer correctness from strategy output alone.

### Governance boundary
Owns:
- provenance;
- evidence maturity;
- approvals;
- audit;
- temporal validity;
- policy enforcement;
- historical reconstruction.

## Highest-priority gaps for future target systems

1. **Failure/recovery evidence** — normal-path correctness is not enough.
2. **Canonical market-data identity** — source, instrument and effective-time semantics must survive normalization.
3. **Corporate-action temporal model** — research and portfolio state need explicit event history.
4. **Execution reconciliation** — external observations must be reconciled into canonical state.
5. **Decision-to-execution provenance** — every consequential order should be traceable to decision, evidence and policy.
6. **Production observability** — data quality, strategy state, risk decisions, orders and recovery need correlated evidence.
7. **Research/live semantic parity** — share contracts and models where useful without pretending simulation is execution.
8. **Bounded AI integration** — AI may propose or analyze; deterministic controls remain authoritative at irreversible boundaries.

## Roadmap consequence
2024 does not justify immediately choosing a particular database, message broker, service topology or AI framework.

The evidence instead justifies designing the contracts first:

```text
Source
  ↓
Canonical Observation
  ↓
Validated Data
  ↓
Research Artifact
  ↓
Decision Intent
  ↓
Policy / Risk Gate
  ↓
Execution Intent
  ↓
External Event
  ↓
Reconciliation
  ↓
Canonical State
  ↓
Evidence / Audit
```

Technology choices should be experiments against these contracts.
