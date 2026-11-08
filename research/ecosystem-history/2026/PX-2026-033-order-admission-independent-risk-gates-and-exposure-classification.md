# PX-2026-033 — Order admission, exposure classification and independent risk gates

**Research date:** 2026-11-08  
**Status:** cross-record risk-policy synthesis and acceptance specification  
**AlgoX area:** order admission / pre-trade controls / exposure projection / policy evidence / broker command safety  
**Inputs:** PX-2026-024 through PX-2026-032; ALG-ARCH-001 provenance baseline  
**Mode:** research and requirements specification only  
**Non-goals:** no order engine implementation, broker connection, sandbox/production API, live order, paid service, PR, merge or execution-policy deployment

## Executive finding

The preceding research records identify several separate safety systems:
- broker order identity and uncertain submission recovery (PX-024);
- broker-neutral command and reconciliation requirements (PX-025);
- compound/sliced order outcomes (PX-026);
- stream and REST observation gaps (PX-027);
- portfolio, ledger and contract-note reconciliation (PX-028);
- expiry, exercise, physical settlement and corporate actions (PX-029);
- SPAN/ELM, upfront collection, CCO and delivery margin (PX-030);
- clearing reports, client short allocation and member PRISM controls (PX-031);
- MWPL bans, entity position limits and index intraday monitoring (PX-032).

These controls do not answer the same question. An order can have sufficient margin but exceed an entity position limit; a position can be within the permitted limit while margin is not collected; a stock can enter a market-wide ban even when an individual client is below its own cap; a client can have a pending/unknown order which may already have created exposure; and an order can be acknowledged by a broker without having reached the exchange or traded.

**Decision:** the AlgoX order-admission decision must be a conjunction of all applicable independent gates, evaluated against a conservative projected portfolio. It must preserve per-gate results, input versions and evidence. It must not be compressed into a single risk_pass boolean.

The correct control target is the **resulting exposure and obligations**, not the order-side text. A “sell”, “buy to close”, “reduce-only”, “modify” or “cancel” label does not itself prove that a request is risk-reducing. Classification must account for instrument delta, position side, existing orders, partial fills, linked legs, expiry, settlement mode, member/client scope and unresolved commands.

## 1. Evidence and design basis

### 1.1 Source-derived boundaries

The requirements in this record synthesize the following earlier source-backed findings:

- **Broker commands:** Zerodha distinguishes broker OMS order ID from exchange order ID; Upstox tag lookup can return multiple orders; Dhan has a correlation-ID lookup for a missed order ID. The providers do not document a common cross-request idempotency promise. A possibly dispatched command with a lost acknowledgement remains UNKNOWN.
- **Compound order outcomes:** auto-slicing and multi-order requests may return multiple child order IDs, per-child failures or partial success. One parent success flag is insufficient.
- **Market-wide ban:** stock ban state is derived from cross-exchange EOD FutEq OI and MWPL; during ban only position reduction is allowed. A ban is not a client margin shortfall.
- **Entity position limits:** client, TM combined, TM proprietary, FPI and Mutual Fund scopes are distinct. Limits are date-effective and can aggregate a client across different members.
- **Intraday index monitoring:** at least four random snapshots are used. The expiry-day ASD framework for index options is separate from non-expiry-day monitoring.
- **Margin:** equity-derivatives upfront SPAN/ELM and net option premium payable are separate from delivery/CCO collection; actual collection is distinct from a calculator or available-funds snapshot.
- **Expiry and physical settlement:** stock derivatives can generate securities and funds delivery obligations; index derivatives are cash-settled. Delivery/assignment margin is linked to the contract's expiry and settlement stage.
- **Clearing/member risk:** client short allocation, CM/TM collateral allocation and PRISM effective-collateral thresholds operate at different entity levels; PRISM TM alerts are not universal retail-client RMS thresholds.
- **Provenance:** the ALG-ARCH-001 baseline requires attributable execution events, evidence, claims and evaluation decisions. An order-admission decision is a derived claim, and must point to the exact observations/policy versions that support it.

Related records:
- PX-024: broker disconnect and ambiguous outcomes.
- PX-025: requirements R-001–R-101 and AT-001–AT-180.
- PX-026: idempotency, request correlation and child-order recovery.
- PX-027: stream gaps, REST consistency and trade revisions.
- PX-028: positions, holdings, cash ledger, charges and contract notes.
- PX-029: expiry, exercise, delivery and settlement.
- PX-030: margin calculation and collection.
- PX-031: clearing reports, short allocation and PRISM.
- PX-032: position limits, MWPL and intraday monitoring.
- ALG-ARCH-001: provenance architecture.

### 1.2 What this document does not claim

This is a policy-composition proposal, not a broker or exchange implementation contract. It does not prove that any provider exposes every necessary data field in real time, that cross-broker client positions are automatically available, or that all exchanges provide atomic position snapshots. Where the required input is unavailable or its scope cannot be established, the decision is UNKNOWN and cannot clear a risk-increasing action.

The source-derived obligations remain provider-, segment-, product-, account- and effective-date-specific. The proposal does not override the applicable exchange, clearing-corporation, SEBI or broker rule.

## 2. Decision subject and projected exposure

### 2.1 The unit of decision

Every admission decision should identify:
- the logical local intent and command;
- the specific place/modify/cancel/replace action;
- the exact broker/account and client/entity scope;
- the instrument/contract and effective contract-master version;
- the requested order parameters and immutable fingerprint;
- the existing positions, open orders, unresolved attempts and related child/leg orders used in the projection;
- the applicable rule/parameter set and its effective timestamp;
- the current market/contract/settlement state and capture time.

A decision for one child slice or leg is not automatically a decision for the entire parent request. A parent batch or group must be checked for aggregate exposure and each child must retain its own result.

### 2.2 Conservative projected portfolio

The projected post-action portfolio should be derived from:
1. broker-observed current positions;
2. unique reconciled executions/trades;
3. existing working orders and their remaining potential quantity;
4. unresolved placement/modify/cancel outcomes that may have been accepted;
5. the candidate action;
6. linked/compound child orders and legs;
7. the applicable delta/contract/expiry/unit data.

A broker acknowledgement does not remove an order from the working-order set unless the resulting state establishes how much remains executable. A partial fill contributes to the position while its residual quantity remains a potential future execution. An uncertain order contributes conservative potential exposure until reconciled.

Do not net opposing working orders against each other unless the provider/exchange contract and order relationship prove that this is permissible. A pair of opposite orders can fill in different order or not at all.

### 2.3 Exposure is multidimensional

A candidate action may reduce one exposure measure while increasing another. At minimum, future review should keep separate:
- signed net position and gross long/short;
- delta/FutEq exposure where the applicable position-limit framework uses it;
- client/entity and TM/member aggregation;
- margin requirement, available collateral, actual collection and shortfall;
- physical delivery, exercise/assignment and settlement obligations;
- market-wide ban and expiry-specific restrictions;
- maximum potential exposure from working/unknown orders.

An action is not “reduce-only” in all dimensions merely because one of these values falls.

## 3. Independent admission gates

A future implementation should evaluate all applicable gates against one versioned input snapshot. The order below is a review sequence for completeness; it is not a priority ranking that allows one successful gate to compensate for another.

| Gate | Question | Required evidence | Fail/UNKNOWN consequence for a risk-increasing action |
|---|---|---|---|
| G-01 Identity and scope | Is the broker account, client/entity, trading member, product and instrument identity unambiguous? | Verified identity links, UCC/entity category where applicable, contract master, account scope | BLOCK / UNKNOWN |
| G-02 Contract and market eligibility | Is the contract tradable for this session/date/order type and not expired/suspended/restricted? | Effective contract master, exchange session/status and applicable circular | BLOCK / UNKNOWN |
| G-03 Command uniqueness and recovery | Is there any prior attempt whose outcome may already have created the same exposure? | Intent/command/attempt ledger, broker IDs, correlation lookup, order/trade observations | BLOCK / reconcile |
| G-04 Existing and projected exposure | What are the current positions, working orders, partial fills and uncertain residuals after the proposed action? | Orderbook, positions, tradebook, local unresolved exposure and child-order graph | BLOCK / UNKNOWN |
| G-05 MWPL and ban state | Is the security under ban, and if so does the proposed action demonstrably reduce position as allowed? | Effective ban file, cross-exchange FutEq/MWPL, entity Day 1 base and source delta | BLOCK / UNKNOWN |
| G-06 Entity position limit | Does the projected client/TM/proprietary/FPI/MF scope remain within the applicable limit? | Current security-specific limit schedule and complete in-scope entity positions | BLOCK / UNKNOWN |
| G-07 Index intraday/expiry controls | Do applicable index snapshot limits or expiry-day ASD controls permit the action? | Current index rule set, snapshot/delta/price, expiry state and allocated cash evidence | BLOCK / UNKNOWN |
| G-08 Margin and collection | Is the required margin calculated from the full portfolio and is the required client collection actually evidenced? | SPAN/ELM/net premium/CCO/delivery components, client collateral/collection records and parameter versions | BLOCK / shortfall |
| G-09 Expiry and settlement obligation | Could the order create physical delivery, assignment, auction, settlement or delivery-margin exposure? | Contract settlement mode, expiry calendar, current position and settlement/risk evidence | BLOCK / UNKNOWN |
| G-10 Provider/exchange request validation | Are price, quantity, tick, freeze, order variety, product, market session and provider-specific constraints valid? | Current provider API/contract specification and exact request parameters | REJECT / UNKNOWN |
| G-11 Evidence freshness and decision integrity | Are the gate inputs current and internally consistent at dispatch time? | Capture timestamps, source versions, portfolio watermark/consistency scope and policy version | INVALIDATE / recompute |

### 3.1 No compensation between gates

A PASS in one domain never offsets a FAIL or UNKNOWN in another domain. Examples:
- adequate SPAN/margin does not permit an order that would violate a stock position limit;
- position-limit headroom does not establish upfront margin collection;
- a ban-period offset allowance does not override margin or broker order validation;
- a broker's margin calculator does not establish client collateral actually collected;
- a successful broker API response does not establish exchange receipt or execution;
- current position reconciliation does not prove missed WebSocket event history is complete.

### 3.2 Hard blocks, conditional permission and advisory signals

The decision record must distinguish:
- **HARD_BLOCK:** an effective exchange/SEBI/broker or project safety rule forbids the action;
- **CONDITIONAL_REDUCE_ONLY:** the applicable rule permits only demonstrably risk-reducing actions;
- **UNKNOWN_BLOCK:** a required input or state is unavailable, stale, incomplete or contradictory;
- **ADVISORY:** a warning/notification that does not itself establish a hard prohibition;
- **NOT_APPLICABLE:** the gate does not apply, with a recorded reason.

Examples of different scopes:
- a stock already in MWPL ban is a market/position restriction that only permits offsetting reduction;
- the older 60% OI alert listed on NSE's position-limit page is an alert, not the 95% EOD ban trigger, and its migration to FutEq was not established in PX-032;
- PRISM 70/80/90% messages are TM effective-collateral warnings and 100% is a TM facility control—not automatic individual-client square-off rules;
- an actual client short-allocation/collection failure is a separate client/member reporting and margin exception.

A warning must not be elevated into a regulatory hard block without a rule that says so. Conversely, an actual hard block must not be downgraded to an advisory warning because another gate passed.

## 4. Action classification and order lifecycle

### 4.1 PLACE / increase

A new order that increases any applicable risk/exposure measure requires every applicable gate to PASS. An UNKNOWN position, delta file, entity category, current limit, ban list, collection record or unresolved command is not permission to proceed.

### 4.2 OFFSET / reduce

An offsetting order is a conditional action classification, not an order-side property. The engine must calculate the projected post-action vector and establish that the action reduces the measure relevant to the rule:
- during a stock ban, use the prescribed ban-period Day 1/current FutEq comparison, including sign rules and source delta times;
- for client/entity limits, verify the correct cross-member aggregation and that the projected entity position does not increase beyond the allowed state;
- for margin, re-evaluate the full portfolio and recognize that a hedge/spread leg removal can increase margin even when net directional exposure falls;
- for physically settled expiry exposure, a nominally “closing” trade must not be assumed to extinguish already-created delivery or settlement obligations.

If the projected result cannot be established, the action is not proven risk-reducing and remains UNKNOWN.

### 4.3 MODIFY

A modification must be treated as a new risk decision using both the last known parameters and the proposed parameters. It may change remaining executable quantity, price and marketability, instrument/order type or trigger, potential fill/position, spread/hedge status, and margin/risk concentration.

A timed-out modification remains unknown. Do not assume the old or new state won.

### 4.4 CANCEL

A cancel request is an external command, not proof of cancellation. Until the broker confirms the relevant remaining quantity and the tradebook is reconciled, the order may still fill. A timed-out cancel must not be blindly repeated or converted to CANCELLED.

### 4.5 REPLACE

A replace is not one atomic action unless the provider contract explicitly says so. It can create overlap between the old and new orders. The default safe policy is:
1. record the cancel request for the existing order;
2. reconcile the cancellation and fills;
3. establish the true residual/exposure;
4. submit a separately risk-checked replacement only when permitted.

Any provider-native atomic modify/replace behavior must be documented and tested before using a different sequence.

### 4.6 Group, sliced and multi-leg actions

For auto-slice, multi-order, Super Order, bracket/cover or other compound requests:
- evaluate the parent intent and its projected aggregate exposure;
- preserve every child/leg identity and result;
- check each child against its own instrument/contract and provider constraint;
- model partial acceptance and unfilled child quantities;
- do not assume all-or-none acceptance or cross-child atomicity;
- keep group completeness UNKNOWN after a lost response until the full child set is evidenced.

A parent batch passing a single aggregate margin calculation does not replace child-specific position-limit, ban, expiry, quantity and status checks.

## 5. Decision freshness and dispatch fencing

An approval should be attached to a versioned **AdmissionSnapshot** containing:
- all gate results and reasons;
- broker/account/entity/instrument identity;
- projected position/order/child set;
- margin and collection evidence;
- MWPL/position-limit/ban data;
- delta and contract-master versions;
- expiry/settlement and market session state;
- source capture times and file/content hashes;
- policy and adapter versions;
- decision time and expiry/invalidity conditions.

The snapshot must be revalidated immediately before dispatch if any material input can have changed, including position/order/trade state, ban state or per-security limit schedule, delta/market snapshot, margin parameter or collected collateral, expiry/assignment/delivery state, prior uncertain command reconciliation, and broker request constraints or account permissions.

If a material input changed, the prior approval is stale and the gate set must be recomputed. A stale approval must not be reused to send the command.

### 5.1 Separate decision, submission and execution evidence

These events must remain distinct:
1. **Admission decision:** risk policy allowed an attempted command under a particular evidence snapshot.
2. **Dispatch attempt:** the process attempted to send the command.
3. **Broker acknowledgement:** the broker returned an order identifier/response.
4. **Exchange acknowledgement:** exchange order identity/status was observed where available.
5. **Execution:** individual trade evidence was received and reconciled.
6. **Position/ledger result:** actual positions, holdings, funds and settlement records were reconciled.

An ALLOW decision is not evidence that the provider accepted the request. Broker acknowledgement is not proof of execution. An order status is not a replacement for individual trade records.

## 6. Candidate decision result

The following labels are descriptive, not a finalized implementation enum:

- **ALLOW:** all applicable mandatory gates PASS and the admission snapshot is fresh.
- **DENY:** at least one applicable hard rule FAILS.
- **REDUCE_ONLY:** the applicable policy only permits a reduction, and the projected action has been proven to reduce the required exposure measure.
- **UNKNOWN_BLOCKED:** a mandatory input or state is unavailable, stale, incomplete or contradictory.
- **ADVISORY:** warning only; no prohibition established by that source.
- **NOT_APPLICABLE:** gate not relevant to the action with reason captured.

A result must include each gate, not just the summary label. ALLOW and REDUCE_ONLY expire when their evidence snapshot becomes stale.

## 7. Additional requirements for PX-025

### R-102 — Admission is a conjunction of independent mandatory gates

A future order-admission service MUST evaluate every applicable market, contract, command-recovery, exposure, MWPL/ban, entity-limit, index intraday, margin/collection, expiry/settlement and provider-validation gate. A PASS in one dimension MUST NOT compensate for a FAIL or UNKNOWN in another dimension.

### R-103 — Projected exposure includes positions, working orders and unresolved attempts

Projected exposure MUST include broker-observed positions, unique reconciled trades, working-order residuals, partial fills, child orders and any possibly dispatched command whose outcome is unresolved. Opposing working orders MUST NOT be netted away unless an authoritative provider/exchange rule proves such netting is valid.

### R-104 — Action classification is based on projected exposure, not order-side text

PLACE, OFFSET, REDUCE, CLOSE, MODIFY, CANCEL and REPLACE MUST be classified using the projected post-action portfolio across each relevant exposure/risk dimension. A buy/sell string or user-supplied reduce-only label MUST NOT by itself establish that the action reduces exposure.

### R-105 — UNKNOWN blocks exposure-increasing admission

If any mandatory identity, contract, position, ban, entity limit, delta, margin/collection, expiry/settlement or prior-command input is UNKNOWN, the system MUST NOT admit an action that could increase exposure. It MUST retain the reason and the evidence needed to resolve the state.

### R-106 — Cancel, modify and replace are distinct commands

The system MUST retain independent command/attempt identity and outcome for cancellation, modification and replacement. A cancel request MUST NOT be treated as completed cancellation; a replacement MUST NOT be assumed atomic unless the provider contract explicitly establishes it; an unknown outcome MUST be reconciled before issuing a conflicting command.

### R-107 — Ban-period reduction requires rule-specific proof

During a single-stock MWPL ban, the system MUST admit only actions that meet the effective source's offset/reduction rule, including FutEq, Day 1 baseline, current delta and sign constraints. It MUST NOT classify an order as permitted merely because it is opposite-side or labelled reduce-only.

### R-108 — Entity-limit admission uses complete in-scope aggregation

Projected position-limit evaluation MUST use the relevant client/entity/TM/TM-proprietary/FPI/MF category and all required member/exchange positions. If the rule requires cross-member aggregation and the system has only one broker-local subtotal, the gate MUST be UNKNOWN rather than PASS.

### R-109 — Margin admission requires collection evidence, not a calculator

For any rule requiring upfront client margin, the system MUST independently verify the applicable requirement and actual eligible client cash/collateral collection. Margin-calculator output or available-balance snapshot alone MUST NOT clear the gate.

### R-110 — Hedge and basket changes invalidate prior margin/risk approval

Any change to existing positions, working orders, basket legs, option premium, delta, expiry, corporate action or hedge eligibility MUST trigger recalculation of every affected gate. A previous per-order/basket calculation MUST NOT be reused after the supporting portfolio or parameter set changes.

### R-111 — Expiry and settlement risk is part of admission

Before admitting an action that can create or increase an expiring derivative position, the system MUST evaluate contract-specific expiry, exercise style, cash/physical settlement mode, delivery/assignment margin, settlement calendar and available delivery capacity. Missing contract/settlement data MUST block exposure increase.

### R-112 — Compound and sliced orders require parent and child admission

A group request MUST be checked at parent aggregate scope and each child/leg scope. The system MUST preserve partial success/failure and child-set completeness. A parent-level margin result or group approval MUST NOT automatically authorize every child.

### R-113 — Provider/exchange validation is distinct from domain risk approval

Order price, quantity, tick, freeze, order variety, product, market session and provider-specific request validation MUST be evaluated separately from market/portfolio risk gates. A domain-level ALLOW MUST NOT be represented as broker acceptance or proof that the request will pass provider validation.

### R-114 — Warning signals are not automatically hard blocks

The system MUST distinguish advisory alerts from regulatory/clearing hard restrictions. A warning such as a market-wide OI alert or TM-level PRISM utilization message MUST NOT be converted into a retail-client ban unless an applicable source rule establishes that effect. Hard restrictions MUST NOT be downgraded to warnings.

### R-115 — Admission snapshots are immutable and time-bounded

Every admission decision MUST preserve the exact gate outcomes, projected portfolio, data source/hash, effective rule/parameter versions, timestamps, policy/adapter versions and invalidation conditions. The decision MUST be revalidated immediately before dispatch if any material input can change.

### R-116 — Gate outcomes are individually inspectable

The system MUST preserve each applicable gate as PASS, FAIL, UNKNOWN, ADVISORY or NOT_APPLICABLE with its scope, reason and evidence references. A summary ALLOW/DENY/REDUCE_ONLY result MUST NOT erase gate-level results.

### R-117 — Admission, dispatch, acknowledgement and execution are separate evidence events

The system MUST distinguish risk decision, transport dispatch, broker acknowledgement, exchange acknowledgement, trade execution and account/position reconciliation. A successful admission decision MUST NOT be recorded as a successful order submission or fill.

### R-118 — Hard regulatory restrictions cannot be bypassed by a local override

Any manual/emergency override MUST be scoped, authenticated, time-bounded and auditable. It MUST NOT override statutory/exchange/clearing hard restrictions, a market-wide ban, missing client collection required upfront, or an unresolved command that could create duplicate exposure. Where an exception is legally/contractually permitted, its governing authority and evidence MUST be explicit.

## 8. Deterministic acceptance scenarios

These extend AT-001 through AT-180. Use deterministic fake providers, synthetic portfolios, parameter files and market/settlement fixtures only.

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-181 | Every applicable gate passes and all evidence is fresh | ALLOW with a complete immutable gate trace; no claim of broker acceptance |
| AT-182 | Position-limit gate FAILS while margin gate PASSes | DENY; margin sufficiency cannot compensate for position-limit breach |
| AT-183 | Margin/collection gate FAILS while entity position-limit gate PASSes | DENY; position-limit headroom cannot compensate for short collection |
| AT-184 | A mandatory gate lacks current source data | UNKNOWN_BLOCKED; no risk-increasing dispatch |
| AT-185 | A gate is genuinely not applicable to the instrument/product/action | Record NOT_APPLICABLE with the rule-based reason; do not silently omit the gate |
| AT-186 | An order is labelled SELL but projected delta/gross/physical exposure increases | Classify by projected exposure; do not accept a reduce-only label |
| AT-187 | An opposite-side order decreases signed delta but increases gross short, margin or delivery obligation | Preserve each dimension; apply all relevant gates and deny if a hard requirement fails |
| AT-188 | Existing working orders could fill alongside the candidate order | Include working residuals in projected exposure; do not use position-only subtotal |
| AT-189 | Two opposing working orders exist without guaranteed atomic/OCO semantics | Do not net them as mutually exclusive; include conservative potential exposure |
| AT-190 | A previous placement may have reached the broker but acknowledgement was lost | Block duplicate risk-increasing placement; reconcile before any new command |
| AT-191 | Cancel request times out while the order may still be executable | Keep residual exposure; cancel remains UNKNOWN until broker/order/trade reconciliation |
| AT-192 | Modify request changes price/quantity/trigger and times out | Preserve old and proposed parameters; reconcile actual broker state before another modification |
| AT-193 | Replace is attempted before old order cancellation is confirmed | Block unsafe overlap unless a documented provider-atomic replacement contract applies |
| AT-194 | A reduce-only order during single-stock ban increases FutEq or violates the Day 1 sign rule | DENY; opposite-side label is insufficient |
| AT-195 | A ban-period offset reduces FutEq using the effective baseline/delta rule | REDUCE_ONLY/ALLOW according to applicable gates; preserve baseline and current delta evidence |
| AT-196 | Client's broker-local position is within limit but aggregated cross-member position exceeds limit | DENY or UNKNOWN as applicable; do not use broker-local subtotal |
| AT-197 | Cross-member client position data is unavailable | UNKNOWN_BLOCKED; no false PASS from incomplete identity scope |
| AT-198 | Basket hedge leg is removed after admission approval but before dispatch | Invalidate snapshot and recompute margin/position/expiry gates |
| AT-199 | Client has sufficient nominal balance but verified eligible upfront collateral is below requirement | DENY; available funds do not substitute for actual collection |
| AT-200 | SPAN/ELM and net option premium change after the admission snapshot | Mark approval stale; recalculate before dispatch |
| AT-201 | Stock derivative will create physical delivery near expiry but contract/lot/settlement data is missing | UNKNOWN_BLOCKED; do not admit exposure increase |
| AT-202 | Index derivative is cash-settled while stock derivative is physically settled | Apply correct product settlement mode; do not apply one generic expiry gate |
| AT-203 | A compound order passes parent margin but one child exceeds a position limit | Block the affected child/group as required; parent margin PASS does not authorize that child |
| AT-204 | Auto-sliced group returns partial success and per-slice errors | Preserve each child result and recompute remaining group exposure; do not report all-success |
| AT-205 | Group response is lost and only some child orders are discovered | Child-set completeness UNKNOWN; no full group resubmission |
| AT-206 | Provider accepts a request and returns broker order ID, but exchange order ID is null | Record broker acknowledgement/intermediate state; do not infer exchange acceptance or execution |
| AT-207 | Broker order reaches OPEN status but no trade record exists | Record open order, not execution; positions/fills remain based on unique trade evidence |
| AT-208 | A 60% OI alert or 70/80/90% TM PRISM warning is received | Record scoped ADVISORY; do not automatically treat as a retail-client hard block |
| AT-209 | Effective stock MWPL ban or client position limit is breached | HARD_BLOCK/REDUCE_ONLY as the specific source rule requires; do not downgrade to advisory |
| AT-210 | Index option expiry-day ASD conditions are met | Apply expiry-day ASD only under the current applicable 2025/122 and NSE implementation rules |
| AT-211 | Non-expiry-day index intraday snapshot shows a threshold breach but no applicable ASD rule | Record surveillance outcome/advisory according to effective policy; do not apply expiry-day ASD automatically |
| AT-212 | Admission snapshot uses a delta file or position report that changes before dispatch | Snapshot invalidated; rerun all affected gates |
| AT-213 | Market/contract session changes to closed/expired/suspended after risk approval | Invalidate admission and reject dispatch under the new state |
| AT-214 | A partial fill arrives between admission and dispatch of a second related command | Recompute projected positions and all dependent gates before second dispatch |
| AT-215 | A prior unknown cancellation is resolved as FILLED rather than CANCELLED | Reconcile fill into positions/margin and deny any duplicate replacement |
| AT-216 | A child leg of a multi-leg order is rejected while another leg is accepted | Preserve unhedged residual risk; re-evaluate exposure and risk controls for the surviving leg |
| AT-217 | Parent request passes aggregate risk but child order uses a different instrument/expiry/contract master | Re-run child identity, limit, margin and expiry gates independently |
| AT-218 | Manual override requests permission to breach an active market-wide ban | Reject override; hard regulatory/exchange restriction is non-bypassable |
| AT-219 | A manual exception is permitted by a documented non-regulatory local policy | Require authorized principal, scope, expiry, reason and audit; do not relax hard source rules |
| AT-220 | Admission decision is ALLOW but broker submit later times out | Preserve ALLOW + SUBMISSION_UNKNOWN as separate facts; reconcile, do not rewrite the decision as a fill or blindly retry |

PX-025 now contains **118 normative requirements (R-001–R-118) and 220 proposed acceptance scenarios (AT-001–AT-220)**. The new scenarios are not executed tests.

## 9. Decision and implementation boundary

- **ACCEPT AS REQUIREMENTS BASELINE:** all applicable independent risk gates must pass; no single margin/position/ban state substitutes for the others.
- **ACCEPT:** projected exposure includes positions, working residuals, partial fills, compound children and unresolved command outcomes.
- **ACCEPT:** risk-reducing classification is based on projected exposure and effective source rules, not order-side text.
- **ACCEPT:** cancel/modify/replace, dispatch, broker acknowledgement, exchange acknowledgement and fill are separate lifecycle/evidence states.
- **ACCEPT:** warning-only controls and hard restrictions are distinct; regulatory/clearing restrictions are not locally overridable.
- **DEFER:** final gate ordering/engine API, exact data freshness thresholds, position/risk vector schema, per-broker order validation mapping and override workflow.
- **NOT AUTHORIZED:** production risk engine implementation, broker connection, sandbox/production API, real order submission, live execution, paid services, credentials/IP changes, PR or merge to main.

**Final status:** PX-033 order-admission and independent risk-gate composition research documented. PX-025 expanded to 118 requirements and 220 proposed acceptance scenarios. No code, broker/API interaction, order or test execution was performed.
