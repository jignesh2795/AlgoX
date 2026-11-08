# PX-2026-043 — Cross-mode conformance testing and replay verification

**Research date:** 2026-11-08  
**Status:** conformance architecture and acceptance specification documented; no harness or engine executed  
**AlgoX area:** deterministic test architecture / scenario fixtures / replay verification / mode conformance / release gates  
**Inputs:** PX-025 R-001–R-275; PX-027 stream and order recovery; PX-033 independent admission gates; PX-037 market-data time semantics; PX-041 statistical validation; PX-042 mode semantics and replay  
**Modes:** BACKTEST, PAPER, SHADOW, LIVE through deterministic fake adapters  
**Mode:** research and requirements specification only  
**Non-goals:** no harness or engine implementation, broker/feed connection, real account, paper/live order, production operation, paid service, PR or merge to main

## Executive finding

PX-042 establishes a shared semantic core with mode-specific clocks, fills, accounts and external evidence. PX-043 defines how to prove that contract through repeatable conformance tests.

The central principle is: **compare common domain invariants exactly; compare mode-specific outcomes against their own explicit contracts.**

It is wrong to require a paper fill price to equal a live brokerage fill price. It is also wrong to excuse a paper/live mode because “fills differ” when their canonical intent, risk-gate outcome, instrument identity or accounting transition diverges without an explained mode-specific reason.

A cross-mode suite must produce:
- one immutable scenario fixture;
- a versioned input/data/policy manifest;
- a canonical expected domain-decision trace;
- a per-mode adapter/fill/evidence expectation;
- a replayable event log;
- explicit invariant assertions;
- a classified divergence report;
- a mode-specific conformance decision.

A single aggregate parity percentage is unsuitable as a release gate. A hard failure such as a paper runtime reaching a live broker adapter, an UNKNOWN risk gate becoming PASS, a duplicate exposure from replay, or a simulated fill being recorded as a live trade must block the mode regardless of benign checks that pass.

## 1. Conformance layers

| Layer | Comparison | Required result |
|---|---|---|
| L0 — Input identity | Instrument/contract, account namespace, data and policy versions | Exact match or explicit source/mode difference |
| L1 — Strategy intent | Signal, action, side, quantity, price/trigger, validity and intent fingerprint | Same when inputs are equivalent |
| L2 — Risk semantics | Applicable gates, input scope, results and reasons | Same domain result where evidence/policy are equivalent; explicit UNKNOWN otherwise |
| L3 — Order lifecycle | Legal transitions, cumulative fill, residual and terminal state | Same invariants, not necessarily same timing or fills |
| L4 — Execution outcome | Fill price/quantity, latency, liquidity and rejection | Mode-specific expected behaviour |
| L5 — Portfolio/accounting | Position roll-forward, cash, fees, margin and settlement | Same accounting rules; model/source differences attributable |
| L6 — Event replay | Event IDs, observed order, clock, scheduler and resulting state | Deterministic for identical replay inputs/version/seed |
| L7 — Mode isolation | Capabilities, credentials, account namespace and routing | Hard security assertions; no cross-mode capability leakage |

Every layer and invariant must be retained separately. L0–L3, L5–L7 carry domain correctness requirements. L4 has mode-specific execution expectations.

### 1.1 Divergence classes

Each comparison should be classified as:
- **EXACT:** identical canonical output expected from equivalent inputs;
- **INVARIANT:** numeric/time result may differ but a shared invariant must hold;
- **MODE_EXPECTED:** difference required by the mode contract;
- **DATA_VARIANCE:** source, vintage or observation timing differs;
- **EXECUTION_VARIANCE:** market/broker fill, partial execution or latency differs;
- **MODEL_VARIANCE:** mode-specific fill/fee/margin/settlement model differs;
- **EXTERNAL_STATE_VARIANCE:** broker/exchange/account evidence differs from simulation;
- **UNEXPLAINED:** no approved rule or evidence explains the difference; conformance fails or is UNKNOWN.

A known difference is not automatically acceptable. It must match an explicit fixture expectation and point to a mode-specific contract/model/source.

### 1.2 Non-compensating release gates

A mode is conformant only if all mandatory hard checks pass. The following always block:
- PAPER or SHADOW has a callable LIVE place/modify/cancel capability;
- LIVE uses virtual balances or fills as actual account state;
- simulated/paper/shadow event is typed as broker/exchange execution;
- mandatory risk-gate UNKNOWN becomes PASS without evidence;
- replay duplicates an intent or economic side effect;
- cumulative filled quantity exceeds requested quantity;
- stale/wrong instrument alias is accepted;
- deterministic replay changes outputs without a declared nondeterministic source;
- simulated and live account namespaces cross-contaminate;
- broker acknowledgement is treated as a trade fill.

## 2. Canonical scenario fixture

### 2.1 Required fixture package

One immutable scenario fixture should contain:
1. stable scenario ID, fixture version, purpose and tags;
2. strategy/config hash, parameters, feature inputs, signal time and intended action;
3. canonical instrument, provider alias, market observation and data manifest;
4. contract-master, lot/tick/freeze/venue, expiry/settlement and session-calendar versions;
5. opening positions, working/child orders, cash, collateral, margin and unresolved attempts;
6. risk policy, required gate set, evidence requirements and expected gate outcomes;
7. canonical order intent and any provider-specific mapping under test;
8. mode-specific fill, fee, slippage, margin and settlement profiles;
9. ordered market, broker, timer, order and settlement events with raw/normalized times;
10. expected shared invariants and per-mode outcomes;
11. virtual clock, scheduler version and deterministic seed;
12. source fixture hashes and test-harness version.

Fixtures must be synthetic or use authorized offline captures. They must not contain real client identifiers, credentials, account secrets or production order data.

### 2.2 Shared assertions and mode expectations

Each fixture defines:
- expected canonical intent/order fingerprint;
- applicable risk gates and expected results;
- legal state-transition constraints;
- position/cash/fee accounting invariants;
- source/mode-specific event types;
- expected fill/no-fill/partial-fill policy;
- known non-equivalence reasons;
- forbidden outcomes.

BACKTEST, PAPER, SHADOW and fake-LIVE runners consume the same scenario identity and shared domain expectations. Each runner uses only its mode-specific adapter/model profile. The fixture must not change the underlying strategy or risk policy silently to make one mode pass.

### 2.3 Golden trace and golden outcome

Preserve both:
- **Golden domain trace:** canonical intent, gate results, legal lifecycle transitions and accounting invariants expected to remain stable across modes.
- **Mode-specific outcome trace:** simulated/hypothetical/external fill events and timing under that mode's contract.

Do not compare final P&L alone. Two modes can coincidentally end with the same P&L despite different instrument identities, duplicate orders, partial fills or incorrect risk gates.

## 3. Replay verification

### 3.1 Deterministic replay manifest

Every deterministic replay must pin:
- scenario/fixture version and content hash;
- market/event input bytes and data-manifest ID;
- canonical contract and provider-alias crosswalk;
- strategy and configuration hash;
- risk policy and reference-parameter versions;
- scheduler, clock, decoder and adapter versions;
- fill/fee/margin/settlement model versions;
- virtual clock origin and ordering policy;
- random seed(s);
- mode/account namespace;
- generated event-log hash.

For BACKTEST/fake-adapter runs, identical manifests and seeds must reproduce identical domain decisions, synthetic fills, portfolio and ledger outputs. If a model uses randomness, all random sources must be seeded and recorded.

### 3.2 Repeated delivery, delays and ordering

Replay must support duplicate delivery, delayed/out-of-order arrival, equal timestamps with different receive sequence, reconnect gaps/snapshot resync, broker events between bar callbacks, late fills after cancel/modify, repeated timer callbacks and process restart at an event boundary.

Idempotency is tested at event and command level. Reprocessing an already-applied event must not create a second fill, fee, position change or side effect. If the provider does not expose a causal sequence, preserve recorded receive order but do not claim exchange causal ordering.

### 3.3 Checkpoint and restart

A checkpoint must preserve mutually consistent:
- strategy state;
- order/child-order and idempotency state;
- positions, cash, fees and margin;
- event offset/last processed event;
- virtual clock and scheduler state;
- policy/config/model versions;
- random-generator state where applicable.

Restart must either resume from a fully consistent checkpoint or replay from a known earlier state. It must not restore strategy variables without matching order, portfolio and event state.

### 3.4 Live-capture replay boundary

Captured LIVE logs can be replayed through fake adapters to test strategy and state-machine response. This verifies handling of recorded evidence; it does not recreate the exchange matching engine, broker internal processing or original market conditions. Replay outputs remain synthetic and must never be recorded as new broker executions.

## 4. Fake adapters and failure injection

Provide deterministic fake interfaces for market data/reconnect, contract master, broker placement/modify/cancel/query, order/trade streams, positions/holdings/funds/ledger, margin/collection, settlement/auction/contract notes and the clock/session calendar.

Inject:
- connect/request timeout and lost acknowledgement;
- duplicate, late and out-of-order messages;
- partial response, partial child set and pagination gap;
- invalid/rejected order or modification;
- partial fill then cancel/reject;
- market-data staleness, queue overflow and reconnect;
- parameter/file mismatch;
- broker position/trade/ledger conflict;
- restart between dispatch and acknowledgement;
- restart between partial and remaining fill;
- settlement failure, auction or delayed margin release.

Each failure must result in a typed expected state and reason, not merely an exception or log line. No fake may fall back to a real endpoint if a fixture is incomplete.

## 5. Property, metamorphic and release tests

In addition to hand-written scenarios, generate event sequences and assert:
- cumulative fills never exceed requested quantity;
- cumulative filled quantity is monotonic and equals the sum of unique fills;
- positions equal opening positions plus signed fills and documented adjustments;
- cash/fees reconcile to unique fills and explicit ledger events;
- duplicate event replay leaves the economic state unchanged;
- terminal orders cannot return to working without a new command lifecycle;
- PAPER/SHADOW cannot emit live-dispatch events;
- simulated events never enter live ledgers;
- deterministic replay is unchanged under transformations declared causally equivalent;
- changing mode does not change canonical identity/intent/risk logic when evidence is equivalent.

Failed random seeds and minimized counterexamples must be retained. A release result must preserve every hard failure and unresolved UNKNOWN. A later successful rerun must not overwrite an earlier failed run.

### 5.1 Conformance outcomes

- **CONFORMANT:** all mandatory common invariants and mode-specific contracts pass.
- **CONFORMANT_WITH_EXPECTED_VARIANCE:** only declared mode/data/execution/model/external-state differences occur.
- **NON_CONFORMANT:** one or more hard invariants or mode-isolation requirements fail.
- **UNKNOWN:** fixture, source, log or expected outcome is incomplete or invalid.

A high pass percentage cannot override a hard failure. Conformance is reported per layer and invariant, not only as one aggregate score.

## 6. Additional requirements for PX-025

### R-276 — Cross-mode conformance is layered

The conformance suite MUST distinguish input/identity, strategy intent, risk semantics, order lifecycle, execution outcome, portfolio/accounting, replay and mode-isolation layers. Exact parity, invariant parity and expected mode variance MUST be specified separately.

### R-277 — Canonical fixtures are immutable and shared

A cross-mode scenario MUST use one immutable versioned fixture containing strategy inputs, market/reference data, portfolio state, risk policy, command input, execution model profiles, event schedule and expected outcomes. Mode runners MUST NOT silently mutate shared inputs to obtain a passing result.

### R-278 — Golden domain trace is separate from mode outcome trace

The harness MUST preserve a common golden trace for canonical intent, risk gates, legal order lifecycle and accounting invariants, plus separate mode-specific outcome traces for fills, timing and external evidence. A matching final P&L MUST NOT substitute for trace conformance.

### R-279 — Divergences are explicitly classified

Every cross-mode mismatch MUST be classified as EXACT, INVARIANT, MODE_EXPECTED, DATA_VARIANCE, EXECUTION_VARIANCE, MODEL_VARIANCE, EXTERNAL_STATE_VARIANCE or UNEXPLAINED. An unexplained divergence MUST prevent a CONFORMANT result.

### R-280 — Conformance layers cannot compensate for hard failure

The suite MUST report results per layer and invariant. A paper/live isolation violation, simulated-as-live fill, risk-gate bypass, duplicate side effect or invalid accounting transition MUST force NON_CONFORMANT regardless of aggregate pass percentage.

### R-281 — Replay manifests pin every deterministic input

Every replay MUST pin fixture/data hashes, strategy/config, risk policy, contract crosswalk, scheduler/clock, decoder, mode adapter, fill/fee/margin/settlement model, seed and event-log version. Missing inputs MUST produce UNKNOWN reproducibility status.

### R-282 — Repeated event delivery is idempotent

The event processor MUST detect and safely handle duplicate/replayed events using source identity and local event provenance. Reprocessing a fill, fee, ledger or settlement event MUST NOT duplicate its economic effect.

### R-283 — Replay supports delay, reordering and gap scenarios

The conformance harness MUST inject delayed, duplicated and out-of-order events, reconnect gaps, snapshots and broker events between bars. It MUST preserve source ordering guarantees and mark unknown causal order rather than manufacturing one.

### R-284 — Checkpoints are transactionally consistent

A replay checkpoint MUST preserve mutually consistent strategy state, order/child-order state, portfolio/ledger state, event offset, clock/scheduler and random generator state. Restart MUST NOT combine state from different event positions.

### R-285 — Fake adapters never fall back to real endpoints

All test and replay adapters MUST be explicit fakes with deterministic fixture-controlled responses. A missing fake capability or injected failure MUST result in an error/UNKNOWN; it MUST NOT route to a real broker, feed, account or exchange endpoint.

### R-286 — Failure injection has explicit expected outcomes

The suite MUST cover transport timeouts, lost acknowledgements, partial responses, order rejection, partial fills, stream gaps, stale data, process restarts, ledger conflict, settlement failure and delayed margin release. Each injected failure MUST have a typed expected state and reason.

### R-287 — Property and metamorphic invariants are tested

The harness MUST test generated event sequences and metamorphic transformations for quantity bounds, unique fill accounting, position roll-forward, ledger arithmetic, idempotent replay, terminal-order rules and mode isolation. Failed seeds and minimized counterexamples MUST be retained.

### R-288 — Mode changes create isolated epochs

Every mode change MUST create a new mode epoch and account namespace after the prior mode is stopped/reconciled. Pending virtual orders MUST NOT be transformed into live commands; external live orders MUST NOT be copied into virtual state as if originated there.

### R-289 — Parity compares semantic outputs and explains execution variance

A parity report MUST compare signal, canonical intent, instrument, gate results, order lifecycle, positions and accounting invariants, while separately recording legitimate mode-specific fill/latency/fee differences. It MUST NOT require identical paper/backtest/live fills.

### R-290 — Conformance outcomes preserve UNKNOWN and NON_CONFORMANT

The suite MUST distinguish CONFORMANT, CONFORMANT_WITH_EXPECTED_VARIANCE, NON_CONFORMANT and UNKNOWN. Missing/incomplete evidence MUST NOT be treated as PASS, and any hard invariant violation MUST force NON_CONFORMANT.

### R-291 — Test run evidence is immutable

Each conformance run MUST retain harness version, fixture hashes, environment, command/configuration, event logs, output traces, seeds, per-assertion results, divergence classifications and final decision. A later successful run MUST NOT delete/overwrite an earlier failed run.

### R-292 — Live capture replay is always synthetic

Replaying captured broker/exchange events through a fake adapter MUST remain labelled replay/synthetic. It MUST NOT create new broker orders, mutate an actual account or be recorded as fresh external trade evidence.

### R-293 — Conformance promotion is hard-gated

A mode or release MUST NOT be promoted by an average test score when any required hard safety, mode-isolation, risk, idempotency, order-state or accounting invariant fails or remains UNKNOWN. Promotion policy and required scenario coverage MUST be versioned.

## 7. Deterministic acceptance scenarios

These extend AT-001 through AT-490. Use synthetic scenario fixtures, fake adapters, captured offline event logs, deterministic clocks and generated state-machine sequences only.

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-491 | Same canonical fixture is run through BACKTEST, PAPER, SHADOW and fake LIVE | Produce one shared domain trace and four mode-specific outcome traces tied to the same fixture hash |
| AT-492 | Strategy intent and risk inputs are equivalent in all four modes | Canonical intent, instrument and mandatory gate outcomes match exactly |
| AT-493 | Paper fill differs from backtest fill because live quote moved before paper execution | Classify as DATA/EXECUTION_VARIANCE with both timestamps and fill policies; semantic gate result remains comparable |
| AT-494 | Same final P&L is reached through different order states or instrument identities | Fail trace conformance; final P&L equality is insufficient |
| AT-495 | A paper adapter tries to call the live order endpoint | Hard NON_CONFORMANT; capability/security test must detect the forbidden route |
| AT-496 | A fake broker fixture is missing a required response | Return typed UNKNOWN/error; no live endpoint fallback |
| AT-497 | Same replay manifest, seed and scheduler are executed twice | Event trace and deterministic simulated outputs match exactly |
| AT-498 | Replay seed changes for a stochastic fill model | Treat as a distinct run; retain seed and do not require output equality |
| AT-499 | A fill event is delivered twice after a restart | Apply one economic fill only; duplicate event retained as replay evidence |
| AT-500 | Broker fill arrives before a delayed cancellation acknowledgement | Preserve actual event sequence and legal lifecycle; no contradictory cancelled/filled state without source evidence |
| AT-501 | Modify request and partial fill race in a fake live adapter | Record fill and modification result independently; never assume modify won |
| AT-502 | Stream disconnect occurs, followed by snapshot without replay cursor | Resync current state while event-history continuity across gap remains UNKNOWN |
| AT-503 | Scheduler checkpoint is taken between partial fill and remaining fill | Restart restores order residual, portfolio and event offset consistently; no lost or duplicated fill |
| AT-504 | Strategy memory is restored but order/portfolio checkpoint is from a different event offset | Reject checkpoint as inconsistent; do not resume strategy on mismatched state |
| AT-505 | Paper mode has no broker credentials but paper fill model is available | Run virtual paper simulation; no credential or live capability required |
| AT-506 | BACKTEST runtime receives a live credential object by configuration error | Fail startup/capability audit; credentials must not be present in backtest runtime |
| AT-507 | Shadow mode is configured with an order-placement adapter | Reject startup or remove the capability through fail-closed policy; no command can be sent |
| AT-508 | User switches PAPER to LIVE while virtual orders remain working | Stop transition; close/reconcile or explicitly abandon virtual state in old epoch; never migrate as live orders |
| AT-509 | User switches LIVE to PAPER while broker orders remain open | Reconcile/carry live orders only in live account epoch; paper account starts separately |
| AT-510 | Simulated backtest settlement event is applied while a live account has a real open position | Keep accounts and event streams separate; actual live position is unchanged |
| AT-511 | A mandatory risk gate is UNKNOWN in the common fixture | All risk-increasing mode runs block or return explicit UNKNOWN; no mode-specific bypass |
| AT-512 | A risk input is simulated in BACKTEST but unavailable in PAPER | Apply explicit paper evidence policy; return UNKNOWN/not-simulated if no valid paper source exists |
| AT-513 | Backtest and paper use different fill models but the same lot/tick/risk policy | Preserve shared domain invariants and classify only declared execution differences |
| AT-514 | Paper fee schedule differs from actual broker contract note | Preserve virtual fee model and actual fee evidence separately; report MODEL/EXTERNAL_STATE_VARIANCE |
| AT-515 | Duplicate intent is replayed after an event-log checkpoint | Idempotency prevents a second command/economic side effect |
| AT-516 | Reordering two events that have no defined causal dependency | Deterministic domain result remains equivalent; otherwise mark ordering dependency explicitly |
| AT-517 | Two same-timestamp events have recorded different receive sequence | Replay in recorded sequence; do not sort by timestamp alone |
| AT-518 | Generated property test creates fills whose cumulative quantity exceeds request | Invariant fails and retains seed/minimized counterexample; run is NON_CONFORMANT |
| AT-519 | Generated property test replays duplicate fees or position adjustments | Accounting invariant detects duplicated economic effect and fails the scenario |
| AT-520 | Conformance report has 99.9% pass but one hard paper-to-live route violation | Overall result NON_CONFORMANT; aggregate pass percentage cannot override the hard failure |

PX-025 now contains **293 normative requirements (R-001–R-293) and 520 proposed acceptance scenarios (AT-001–AT-520)**. These are proposed tests only; no conformance harness, engine, broker, paper account, live account or test was executed.

## 8. Open questions and implementation boundaries

1. Which event-log serialization and content-addressing format should AlgoX standardize for long-lived deterministic fixtures?
2. Which replay scheduler ordering policy should be used when market and broker events share timestamps but no source sequence exists?
3. How should seed and RNG state be recorded for multiple stochastic components and parallel test workers?
4. Which mode-specific fill profiles are appropriate for NSE cash equities, stock/index futures and options at the available historical data resolutions?
5. What numeric conformance tolerances are appropriate for floating market-data fields versus exact decimal money, contract units and order quantities?
6. Which captured live event fields can be retained lawfully and safely for replay under broker/data terms and privacy boundaries?
7. What is the minimum fake-adapter contract needed for all broker-specific features while preserving a single domain order lifecycle?
8. How should parity baselines be recalibrated when a feed schema, broker adapter or fill model changes? Each recalibration must create a new baseline version, not silently overwrite the old one.

These questions are deferred to the design and controlled validation phase. No production or live permission follows from this research.

## 9. Research decisions and non-authorization

- **ACCEPT:** cross-mode conformance is layered; exact/invariant/mode-expected comparisons are separately classified.
- **ACCEPT:** one immutable scenario fixture drives all mode runners; golden domain trace and mode-specific outcome traces are separate.
- **ACCEPT:** deterministic replay pins data, strategy, policy, adapter, model, scheduler, seed and event-log provenance.
- **ACCEPT:** duplicate/reordered/delayed events, checkpoints and injected failures are first-class test scenarios.
- **ACCEPT:** property/metamorphic tests verify domain invariants beyond hand-written examples.
- **ACCEPT:** non-conformant/unknown hard failures cannot be compensated by an aggregate pass percentage.
- **DEFER:** event schema, fixture serialization, scheduler and test harness implementation, exact tolerance policy and conformance release thresholds.
- **NOT AUTHORIZED:** engine or harness code changes, broker/feed connections, paper/live orders, production operation, paid service, PR or merge to main.

**Final status:** PX-043 cross-mode conformance and deterministic replay verification requirements documented. PX-025 expanded to 293 requirements and 520 proposed acceptance scenarios. No harness, engine, broker, paper/live account or test was executed.
