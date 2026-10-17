# EXP-ALG-005 — Research-Agent Reliability Fixtures

## Status
FIXTURE DESIGN — execution pending.

## Purpose
Test the AlgoX research loop as an evidence-producing system rather than judging an agent by the plausibility of its final answer.

## Canonical pipeline

```text
source
 → hypothesis
 → experiment plan
 → implementation
 → execution
 → result
 → verification
 → finding proposal
 → governance
```

## Fixture classes

### R1 Valid reproduction
A task has known inputs, a deterministic implementation, an expected result and matching verification evidence.

Expected: execution succeeds; result is accepted as evidence candidate.

### R2 Fabricated success
The agent reports success but no execution artifact or verification exists.

Expected: unsupported result is rejected.

### R3 Wrong result
Execution completes but verification disagrees with the claimed result.

Expected: finding is rejected; failure is retained as evidence about the attempt.

### R4 Partial execution
The implementation runs only part of the planned experiment.

Expected: result remains incomplete and cannot become a validated finding.

### R5 Retry recovery
First execution fails; a second attempt succeeds and is independently verified.

Expected: both attempts remain traceable; only the verified result can support a finding.

### R6 Conflicting evidence
Two independent runs produce incompatible results.

Expected: contradiction is surfaced rather than averaged away or silently selected.

## Metrics

- execution success rate;
- reproduction correctness;
- unsupported-result rate;
- verifier catch rate;
- retry recovery rate;
- false acceptance rate;
- human intervention count;
- trace completeness.

## Acceptance gate

No result may become durable institutional knowledge solely because an agent claims success. The evidence chain must contain an execution trace, observed result and verification sufficient for the claimed maturity level.

Local execution only; no GitHub Actions dependency.
