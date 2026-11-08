# PX-2026-025 — Broker-neutral recovery requirements and acceptance tests

**Research date:** 2026-11-08  
**Status:** requirements baseline proposed; provider contract gaps remain open  
**AlgoX area:** Indian-market broker adapters / order lifecycle / durable recovery  
**Inputs:** PX-2026-024 and official Zerodha Kite Connect, Upstox and DhanHQ documentation  
**Mode:** research and specification only  
**Non-goals:** no adapter implementation, broker connection, sandbox/production API call, order submission, paid service or merge to `main`

## Executive decision

PX-2026-024 established that the three reviewed broker APIs expose different order identifiers, correlation fields, order/trade read APIs and update streams. Their public documentation does not establish a common exactly-once submission contract or a common durable event-stream replay cursor.

This record translates those findings into a **broker-neutral recovery requirements baseline** and a deterministic fake-broker acceptance matrix.

The primary safety rule is:

> Once a command may have left the client process, loss of its acknowledgement is an unknown outcome. AlgoX MUST reconcile before retrying, replacing or declaring that command failed.

The requirements deliberately distinguish:
- logical trading intent;
- one or more command attempts;
- transport/acknowledgement evidence;
- broker OMS order identity;
- exchange order identity;
- individual executions/trades;
- current broker observations;
- AlgoX's derived reconciliation conclusion.

A broker-neutral adapter is not allowed to erase these distinctions to fit a simpler common status enum.

**Recommendation:** accept this document as the research requirements baseline for a future isolated design review. It is not implementation approval and does not select a storage schema, state enum, broker retry policy or production architecture.

## 1. Evidence basis and source-derived constraints

### 1.1 Findings carried forward from PX-024

| Provider | Documented recovery feature | Constraint relevant to the requirements |
|---|---|---|
| Zerodha Kite Connect | `order_id`, optional order `tag`, daily order book/history, daily trade book, per-order trades and WebSocket postbacks | OMS registration is not proof of exchange receipt/execution; `exchange_order_id` may be null; order and trade endpoints are daily views. |
| Upstox | `order_id`, order-history lookup by `tag`, daily/per-order trades and Portfolio Stream Feed | Tag lookup can return all matching orders; documented order history is one-trading-day; stream starts after connection, but the reviewed docs do not establish missed-event replay. |
| DhanHQ | `orderId`, user/partner-generated `correlationId`, lookup by correlation ID, daily order/trade books and Live Order Update WebSocket | The dedicated correlation lookup is explicitly intended for a missed order ID; reviewed docs do not establish idempotent resubmission or a durable replay cursor. |

Official source pages:
- Kite orders: https://kite.trade/docs/connect/v3/orders/
- Kite WebSocket: https://kite.trade/docs/connect/v3/websocket/
- Kite postbacks: https://kite.trade/docs/connect/v3/postbacks/
- Upstox order history: https://upstox.com/developer/api-documentation/get-order-history/
- Upstox daily trades: https://upstox.com/developer/api-documentation/get-trade-history/
- Upstox trades by order: https://upstox.com/developer/api-documentation/get-trades-by-order/
- Upstox Portfolio Stream Feed: https://upstox.com/developer/api-documentation/get-portfolio-stream-feed/
- DhanHQ orders and correlation lookup: https://dhanhq.co/docs/v2/orders/
- DhanHQ Live Order Update: https://dhanhq.co/docs/v2/order-update/
- DhanHQ rate limits: https://dhanhq.co/docs/v2/

### 1.2 What the documents do not establish

The reviewed public pages do not establish a universal answer for:
- duplicate suppression or idempotency when the same placement is submitted again with the same tag/correlation value;
- query read-after-write consistency or an atomic order-plus-trade snapshot;
- uniqueness scope and retention of every provider correlation identifier;
- exactly-once, at-least-once or at-most-once delivery for every update channel;
- replay of a missed stream interval from a durable cursor;
- a common exchange event sequence or timestamp precision sufficient to order every race.

These remain **UNKNOWN provider contracts**. Absence of a statement in public documentation is not proof that a broker's internal system lacks a capability.

### 1.3 Evidence classification

This document uses:
- **SOURCE-DOCUMENTED:** stated in an official provider document.
- **REQUIREMENT:** a proposed AlgoX safety obligation derived from the documented uncertainty.
- **DESIGN CANDIDATE:** one way a later design could satisfy a requirement; not yet selected.
- **UNKNOWN:** a provider behavior or system guarantee that has not been established.

## 2. Scope and terminology

### 2.1 In scope

1. Placement, modification and cancellation commands with uncertain outcomes.
2. Reconnection after WebSocket or network interruption.
3. Recovery of broker order identifiers where the placement acknowledgement was lost.
4. Reconciliation of order state with individual trade executions.
5. Duplicate, delayed, out-of-order and conflicting observations.
6. Account/day retention boundaries.
7. Multi-match, auto-sliced and parent/child order relationships.
8. Deterministic test cases using synthetic broker responses only.

### 2.2 Out of scope

- Broker-specific HTTP/WebSocket implementation.
- Credential, session-token, IP-whitelist or account onboarding.
- Live, paper or sandbox API access.
- Actual order placement, replacement, modification or cancellation.
- Broker-specific execution policy or order-type mapping.
- Market-data recovery and NSE deterministic market replay; PX-023 remains its separate research record.
- Strategy decisions about whether to trade after an unresolved order.
- Selecting a database, message broker, deployment topology or production runtime.

### 2.3 Identity model

The following identities MUST remain distinct:

| Identity | Meaning | Authority |
|---|---|---|
| `IntentId` | One logical AlgoX trading instruction | Created and owned by AlgoX |
| `CommandId` | One requested action: place, modify or cancel | Created and owned by AlgoX |
| `AttemptId` | One transport attempt for a command | Created and owned by AlgoX; a retry is a new attempt |
| `BrokerCorrelationId` | Optional provider-supported tag/correlation value | Provider-specific format and uniqueness are UNKNOWN unless documented |
| `BrokerOrderId` | Broker/OMS identity for an order | Assigned by broker |
| `ExchangeOrderId` | Exchange identity for a routed order | Assigned by exchange; may be absent at an intermediate stage |
| `TradeId` | Identity for one execution/fill record | Provider/exchange-defined; uniqueness scope must be qualified |
| `ObservationId` | One captured API response or stream message | Created and owned by AlgoX |
| `ReconciliationRunId` | One bounded reconciliation pass | Created and owned by AlgoX |

A single intent MAY map to multiple broker orders, for example because a broker or order type slices one logical request into several child orders. A broker order MAY map to multiple individual trade executions. These are explicit one-to-many relationships, not reasons to collapse identifiers.

## 3. Normative requirements

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** are used as requirements language. MUST/MUST NOT describe mandatory safety conditions for any future implementation claiming conformance to this record.

### R-001 — Durable intent before external dispatch

The system MUST durably record the logical intent and its immutable request parameters before it initiates any broker placement command.

At minimum, the record must identify the broker and account scope, instrument/contract identity, side, product, order type, requested quantity, price/trigger/validity fields where applicable, creation time and a stable local intent ID.

It MUST NOT contain broker credentials, access tokens or other authentication secrets.

### R-002 — Append-only command-attempt evidence

Every place/modify/cancel command MUST have a stable command ID and one or more attempt IDs. A retry is a new linked attempt, never an overwrite of the earlier attempt.

The system MUST retain the request fingerprint, dispatch boundary, available transport result, acknowledgement, response evidence and timestamps for each attempt. Sensitive headers and secrets MUST be excluded or redacted before persistence.

### R-003 — Conservative dispatch uncertainty

The transport layer MUST distinguish:
- **PROVEN_NOT_SENT:** reliable local transport evidence establishes that no request bytes or application command could have reached the provider;
- **MAY_HAVE_BEEN_SENT:** dispatch began or the process cannot prove non-dispatch;
- **ACKNOWLEDGED:** a provider response was received and captured;
- **RESPONSE_INVALID_OR_INCOMPLETE:** a response arrived but does not provide sufficient evidence to establish the provider-side outcome.

A timeout, connection reset, generic 5xx, process crash after dispatch began, or lost response MUST NOT be classified as PROVEN_NOT_SENT without specific transport evidence.

### R-004 — Unknown outcome is a first-class result

If a place/modify/cancel command may have reached the provider but its result is not established, the command MUST enter an explicit unknown/reconciliation-required condition.

The implementation MUST NOT silently map that condition to rejected, cancelled, failed, or not placed.

### R-005 — No blind command retry

The system MUST NOT automatically resend a placement, modification or cancellation command whose previous attempt is MAY_HAVE_BEEN_SENT or RESPONSE_INVALID_OR_INCOMPLETE.

A new external command is permitted only when:
1. the prior attempt is proven not sent; or
2. an authoritative provider contract explicitly defines a safe idempotent retry mechanism and the implementation has verified that the exact operation and key semantics satisfy that contract; or
3. a separately governed decision has resolved the prior outcome and approved the next command.

A tag or correlation field by itself is not proof of idempotency.

### R-006 — Broker and exchange identities remain separate

The adapter MUST preserve broker order ID and exchange order ID as distinct optional identities. A missing exchange order ID MUST NOT be interpreted as rejection, non-acceptance or absence of an order.

### R-007 — Provider status is preserved without lossy normalization

The adapter MUST retain the raw provider status, provider message/reason, provider timestamps and raw payload reference. Any normalized lifecycle interpretation MUST be stored separately and MUST preserve unknown/unmapped states.

A provider's interim/pending state MUST NOT be mapped to a terminal state merely to fit a shared enum.

### R-008 — Correlation lookup is not sole proof of non-acceptance

The adapter SHOULD use the provider's correlation/tag lookup where available. However:
- zero matches in one lookup MUST NOT prove that the request was not accepted unless the provider guarantees query completeness and read-after-write semantics for that case;
- multiple matches MUST produce an explicit conflict;
- one match MUST still be checked against account, instrument, side, product, order parameters, timing and order/trade history.

### R-009 — Strict reconciliation scope

Every reconciliation query and observation MUST be scoped by broker, account, trading date/session and relevant segment where the provider API supports these boundaries.

An order from a different account or session MUST NOT be attached to the current intent because its tag or symbol happens to match.

### R-010 — Independent trade reconciliation

Order status and trade executions MUST be reconciled independently.

The implementation MUST preserve each individual execution record, provider trade ID, associated broker order ID, exchange order ID where present, traded quantity, price and timestamps. Partial fills MUST NOT be represented only by a cumulative average-price field.

### R-011 — Trade deduplication is provider-scoped

The system MUST define and test a provider/account/session-scoped execution identity before deduplicating trade observations. It MUST NOT assume a trade ID is globally unique unless the provider says so.

An identical trade observed through two endpoints or repeated stream messages MUST contribute to the economic fill total exactly once, while both raw observations remain available as provenance.

### R-012 — Fill totals must reconcile

The system MUST compare the sum of unique execution quantities with the broker's order-level filled quantity and any available remaining/cancelled quantity.

Any unexplained mismatch, duplicate identity collision, unit mismatch or incomplete trade response MUST leave the affected order in a reconciliation exception/unknown condition. The implementation MUST NOT silently adjust quantities to make totals agree.

For derivatives, raw provider units and normalized contract/underlying units MUST be preserved separately with the date-specific contract-master and lot-size version used for conversion.

### R-013 — Cancellation race is explicitly handled

A cancel request acknowledgement or local timeout MUST NOT be treated as proof that the remaining quantity was cancelled.

Before a replacement order is allowed, the system MUST reconcile final order state and trades, including fills that occurred while cancellation was pending.

### R-014 — Modification outcome is explicitly handled

A modification timeout MUST leave both the last known parameters and the attempted new parameters in the evidence record. The current broker order history MUST be reconciled before another modification is sent.

The implementation MUST NOT assume that the old or new parameters won the race unless the provider's order history establishes it.

### R-015 — Stream reconnect triggers read-side reconciliation

After an update-stream interruption, the adapter MUST record the interruption window and restore the stream without assuming that reconnect replays missed messages.

It MUST perform read-side order and trade reconciliation for the affected account/session and unresolved orders. If the provider lacks a replay cursor or reliable sequence contract, the recovery result MUST state that event-history completeness is not proven.

### R-016 — Observations are immutable evidence

Every captured provider observation MUST preserve:
- provider and API/stream source;
- broker/account/session scope;
- request/query parameters for REST observations, excluding secrets;
- provider event/update timestamp when supplied;
- local receive/capture timestamp;
- raw payload or immutable content reference and content hash;
- parser/adapter version used to interpret it.

A later observation MUST NOT overwrite an earlier raw observation. Derived state can be recomputed from preserved evidence.

### R-017 — Arrival order is not exchange order

The system MUST NOT infer exchange event order solely from local receive order or from timestamps whose ordering guarantee is undocumented.

When ordering cannot be proven, the derived event history MUST preserve ambiguity rather than manufacture a total order. Provider snapshots with no documented atomicity/watermark MUST be treated as observations, not as sequence-aligned replay checkpoints.

### R-018 — Conflicting evidence remains visible

If stream and REST observations disagree, if two broker orders match one intent, if a trade references an unknown order, or if provider status conflicts with execution quantities, the system MUST record the conflict and keep the affected result unresolved until adequate evidence exists.

Last-arrival-wins is prohibited as a reconciliation policy.

### R-019 — External/manual broker activity is represented separately

Account-wide order feeds may include orders submitted outside AlgoX. Such an order MUST first be recorded as an externally observed broker order. It MUST NOT be silently attached to an AlgoX intent based only on matching instrument, side, quantity or approximate time.

Linkage requires the configured correlation identity or sufficiently strong, uniquely verified evidence. Ambiguous linkage remains unmatched.

### R-020 — Parent/child and sliced orders are explicit

Where one intent creates multiple broker order IDs (auto-slicing, multi-leg, bracket/cover/super-order or related child structure), the adapter MUST preserve parent/child and leg relationships where the provider supplies them.

The reconciler MUST account for each child order and each unique trade exactly once. A partially accepted multi-child result MUST NOT be reported as all-or-nothing success.

### R-021 — Session rollover cannot erase audit evidence

Because at least the reviewed Kite and Upstox order views are day-scoped, the implementation MUST persist the broker observations and reconciliation result needed for local audit before those provider views expire.

The local record MUST be sufficient to explain what was observed, which queries were performed, which results were missing, and why any item remained unknown at session close.

### R-022 — Rate limiting and authentication failures do not resolve uncertainty

A rate-limit response, expired token, denied IP, network failure or unavailable API MUST be recorded as a reconciliation obstacle. It MUST NOT be interpreted as an order rejection or proof of non-acceptance.

Read-side retries MUST use provider-specific rate budgets and bounded backoff. They MUST NOT starve other required account/session reconciliation work.

### R-023 — Concurrency is fenced per affected intent/order

Two reconcilers MUST NOT independently issue conflicting external commands for the same unresolved intent or broker order. A future implementation MUST use an explicit lease, version/fencing token or equivalent concurrency control to prevent stale workers from committing derived decisions after ownership has changed.

Read-only duplicate observations may be tolerated and deduplicated without discarding provenance.

### R-024 — Crash recovery replays local evidence first

On process restart, the recovery procedure MUST first load durable intents, command attempts, unresolved outcomes and captured observations. It MUST identify commands that were in flight at crash time and classify them conservatively.

A restart MUST NOT automatically resubmit a command merely because no acknowledgement was durably recorded.

### R-025 — Risk remains fail-closed while exposure is unknown

An unresolved placement or cancellation MUST be treated as potentially creating or retaining exposure until reconciled. A future execution/risk design MUST define conservative exposure reservation and block unsafe replacement or duplicate exposure.

This requirement does not prescribe a universal amount for reserved margin or loss; that depends on product, order type and risk model. The risk engine MUST NOT count an unknown command as zero exposure by default.

### R-026 — Exact units and numeric integrity

Raw broker quantities, prices, average prices and currency values MUST be preserved without lossy conversion. Any normalized values MUST identify the source unit, conversion rule and reference-data version.

Money calculations MUST use exact decimal semantics rather than binary floating-point arithmetic. Contract-lot conversions MUST be date-valid and independently testable.

### R-027 — Time provenance is explicit

The system MUST preserve the original provider timestamp string/value and the local UTC capture timestamp. Where applicable, it SHOULD also preserve the exchange's local timezone interpretation and trading-session date.

Timestamps alone MUST NOT be used to infer causal order when provider precision or clock synchronization is unknown.

### R-028 — Fail closed on unresolved or unsupported semantics

If an adapter encounters an unmapped status, unsupported product/order type, missing identity field, unknown quantity unit, inaccessible history or insufficient provider evidence, it MUST return an explicit unresolved result. It MUST NOT fabricate a default state or silently downgrade the evidence requirement.

### R-029 — Broker-neutral core; provider semantics stay in adapters

The core recovery contract MUST express provider-independent intent, command, observation, execution and reconciliation concepts. Provider-specific statuses, identifiers, lookup endpoints, retention and error semantics MUST remain traceable through adapter mappings.

The core MUST NOT assume that all brokers implement the same retry, event ordering, snapshot or retention behavior.

### R-030 — Recovery evidence must be reproducible

Every reconciliation result MUST reference the exact observations, adapter/parser version, reconciliation policy version and run ID used to derive it. An independent reviewer MUST be able to reconstruct why an order was declared open, partial, filled, cancelled, rejected, expired, conflicting or unknown.

## 4. Candidate lifecycle and reconciliation outcomes

The following is a descriptive model for review. It is not a finalized enum set.

### 4.1 Command-attempt evidence

`PREPARED` → `DISPATCH_POSSIBLE` → one of:
- `PROVEN_NOT_SENT`
- `ACKNOWLEDGEMENT_CAPTURED`
- `OUTCOME_UNKNOWN`

A process crash after `DISPATCH_POSSIBLE` but before an acknowledgement is durably captured MUST recover as `OUTCOME_UNKNOWN` unless stronger transport evidence proves that no request reached the provider.

### 4.2 Broker-order reconciliation result

Candidate derived outcomes:
- `UNMATCHED`
- `MATCHED_UNCONFIRMED`
- `OPEN`
- `PARTIALLY_FILLED`
- `FILLED`
- `CANCELLED`
- `REJECTED`
- `EXPIRED`
- `CONFLICT_MULTIPLE_MATCHES`
- `CONFLICT_ORDER_TRADE_QUANTITY`
- `CONFLICT_OBSERVATION`
- `UNKNOWN`

These values describe reconciliation results, not provider statuses. Raw provider statuses MUST be retained separately.

### 4.3 Resolution is not the same as finality

A reconciliation run can resolve the identity of an order while the order itself remains open or partially filled. Conversely, an order may appear terminal in one response while its trade evidence is incomplete or contradictory.

A future design SHOULD represent separately:
- command outcome resolution;
- broker-order identity resolution;
- current order lifecycle observation;
- execution/trade completeness;
- event-history completeness.

Do not compress those dimensions into one boolean such as `recovered=true`.

## 5. Reconciliation algorithm requirements

The exact algorithm remains a design question, but any conforming design MUST provide the following phases.

1. **Load durable state.** Read the affected intent, commands, attempts, known broker IDs, children, raw observations and outstanding exceptions.
2. **Fence ownership.** Acquire per-intent/order reconciliation ownership with a version/fencing mechanism. Do not issue placement/modify/cancel commands as part of reconciliation.
3. **Restore the observation channel.** Reconnect the broker update stream and begin durable capture. Do not assume it replays the interruption interval.
4. **Read broker order state.** Query the documented correlation/tag route where available, daily order view and individual order histories for each candidate.
5. **Read broker execution state.** Query daily trades and per-order trades. Preserve raw pages/responses and their query scope.
6. **Normalize conservatively.** Map only documented fields/statuses. Keep unknown provider values and missing fields explicit.
7. **Match identities.** Match broker orders to local intents using broker/account scope, correlation value and the immutable order fingerprint. Reject weak or ambiguous matches.
8. **Deduplicate executions.** Use a validated provider-scoped trade identity. Retain all observation provenance while counting each execution once.
9. **Check invariants.** Compare order quantities, remaining/cancelled quantities and unique trades, including parent/child totals and date-valid units.
10. **Classify.** Return a resolved lifecycle observation only when the evidence satisfies the relevant criteria; otherwise return the specific conflict or UNKNOWN.
11. **Persist derivation.** Store the reconciliation run, policy/parser version, observation references, decisions and unresolved reasons.
12. **Re-evaluate before command release.** Any later place/modify/cancel command requires a separate policy decision against the newly reconciled state. The reconciliation process itself MUST NOT issue a replacement command.

A single empty query, one stream reconnect, one successful REST request or a matching correlation value alone is not sufficient to prove non-acceptance or exactly-once recovery.

## 6. Deterministic fake-broker acceptance matrix

All tests in this section MUST execute against deterministic in-process fake providers or recorded synthetic fixtures. No real broker, sandbox, exchange, account or credential is required or permitted by this research task.

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-001 | Intent persistence succeeds; process crashes before dispatch is marked possible | Restart finds the durable intent and no dispatched attempt; no broker command is sent automatically |
| AT-002 | Dispatch may have occurred; broker accepts; acknowledgement is lost | Command becomes UNKNOWN; zero automatic duplicate placements |
| AT-003 | Transport proves request was never sent | Attempt may be classified PROVEN_NOT_SENT; a separately identified retry can be authorized by policy |
| AT-004 | Generic timeout/connection reset after dispatch | UNKNOWN, never REJECTED or NOT_SENT |
| AT-005 | Broker OMS order ID exists but exchange order ID is null | Preserve broker order identity and intermediate state; do not classify as rejected/nonexistent |
| AT-006 | Correlation query returns zero matches once | Remain UNKNOWN unless documented completeness/read-after-write contract is injected as a verified test precondition |
| AT-007 | Correlation/tag query returns one candidate with mismatching instrument/side/account | Reject the match; preserve unmatched/conflict evidence |
| AT-008 | Correlation/tag query returns multiple candidate broker orders | CONFLICT_MULTIPLE_MATCHES; no silent selection and no retry |
| AT-009 | Matching broker order is discovered after delayed visibility | Link the order to the original intent and close the unknown command outcome without a second placement |
| AT-010 | Partial fill exists before disconnect; remaining fill arrives after reconnect | Reconcile every unique fill exactly once; retain partial/final lifecycle accurately |
| AT-011 | Same trade is received from REST and duplicated stream messages | One economic fill contribution; all raw observations retained |
| AT-012 | Two distinct trades have the same apparent price and timestamp but distinct trade IDs | Both executions count; deduplication must not use price/time alone |
| AT-013 | Trade ID collision occurs within a provider scope but instrument/order differs | Raise identity conflict; do not silently merge or discard |
| AT-014 | Unique trade quantity sum disagrees with order filled quantity | CONFLICT_ORDER_TRADE_QUANTITY / UNKNOWN; no forced balancing adjustment |
| AT-015 | Cancel times out, then a fill occurs before the cancel result is observed | Record the fill; do not claim cancellation or submit a replacement before reconciliation |
| AT-016 | Cancel acknowledgement is captured but order remains partially filled/open | Preserve provider state and residual quantity; do not assume full cancellation |
| AT-017 | Modify times out and broker history shows old parameters | Record the outcome and old parameters; no blind second modification |
| AT-018 | Modify times out and broker history shows new parameters | Record the outcome and new parameters; no blind second modification |
| AT-019 | REST snapshot and stream observation disagree | Preserve both observations and conflict; no last-arrival-wins overwrite |
| AT-020 | Stream messages arrive duplicated and out of provider-time order | Preserve raw messages; derived state must not invent a causal order |
| AT-021 | Stream reconnect provides no replay cursor | Record interruption; run REST reconciliation; event-history completeness remains unproven |
| AT-022 | Broker history endpoint is unavailable/rate-limited/auth-expired | Keep UNKNOWN and record obstacle; never infer rejection |
| AT-023 | Trading-day history expires after local evidence is captured | Local audit still reconstructs the last known order/trade evidence and any unresolved gaps |
| AT-024 | Process crashes after broker accepts but before acknowledgement persistence | Restart classifies OUTCOME_UNKNOWN and reconciles before any new command |
| AT-025 | Two workers attempt to reconcile/advance the same intent concurrently | Fencing prevents stale worker from committing over the current owner |
| AT-026 | Account-wide stream reveals a manually placed order | Preserve as external/unmatched; do not attach to an AlgoX intent without sufficient identity evidence |
| AT-027 | One intent is split into multiple child broker orders | Preserve parent/child map; aggregate only unique child fills; incomplete child set remains unresolved |
| AT-028 | One child is rejected while another child is partially filled | Report per-child outcomes and aggregate partial intent; do not report all-or-none success |
| AT-029 | Derivative order quantity uses a different source unit from normalized contract quantity | Preserve raw unit and lot-master version; block normalized quantity reconciliation until conversion is validated |
| AT-030 | Provider returns an unknown status or unsupported order type | Preserve raw value and return UNKNOWN/unsupported; never map to a guessed terminal state |
| AT-031 | Stale REST response arrives after a newer observation | Preserve it as evidence but do not regress derived state solely by arrival order |
| AT-032 | A new submission is attempted while prior intent exposure is UNKNOWN | Risk/command gate blocks unsafe duplicate or replacement exposure |
| AT-033 | Broker lookup returns a single correlation match but tradebook references another broker order | Conflict is explicit; no intent closure |
| AT-034 | A multi-account process sees same tag and same instrument on two accounts | Account scope keeps identities separate |
| AT-035 | A session rolls over with unresolved order/trade evidence | Durable local state remains UNKNOWN with an auditable query history; no implicit reset to zero exposure |

### Test harness requirements

- Fake-provider outcomes MUST be scripted, deterministic and independent of the network.
- Tests MUST control dispatch timing, lost acknowledgements, visibility delays, order-state transitions, partial fills, stream disconnects, response ordering, rate limits and process crashes.
- Tests MUST assert both positive outcomes and prohibited side effects (especially duplicate placement and false rejection).
- Failure injection MUST cover crashes at each persistence/dispatch boundary.
- Repeated test runs with the same fixture/configuration MUST produce the same derived decision and evidence references.
- Property/state-machine tests SHOULD explore permutations of duplicate and out-of-order observations while preserving known causal constraints.
- A test pass validates the implementation against its fake contract; it does not establish that a live provider behaves identically.

## 7. Safety invariants for independent review

Any later implementation review MUST demonstrate these invariants:

1. **No unknown-to-retry transition:** UNKNOWN cannot directly authorize another external command.
2. **No duplicate execution accounting:** each unique trade contributes once to economic fills.
3. **No silent evidence loss:** every raw observation and command attempt remains attributable.
4. **No account/contract cross-linking:** identities are scoped to the right broker account, session, segment and instrument.
5. **No unsupported total order:** ambiguous ordering remains ambiguous.
6. **No order/trade conflation:** order state does not substitute for trade execution records.
7. **No false zero exposure:** unresolved placement/cancellation is not treated as no exposure by default.
8. **No stale worker commit:** reconciliation ownership is fenced.
9. **No lifecycle normalization loss:** raw provider statuses and unknown values are retained.
10. **No implicit session reset:** unresolved evidence survives rollover.

## 8. Proposed exit gates for a future implementation milestone

A future implementation proposal may proceed to detailed design only after these research gates are closed:

| Gate | Required evidence | Current status |
|---|---|---|
| G-01 Provider contract inventory | Per-provider IDs, lookup, order/trade reads, stream behavior, status set, retention, limits and unsupported semantics | PARTIAL — PX-024 comparison exists |
| G-02 Idempotency/retry contract | Official provider statement or explicit decision to operate without safe retry | OPEN |
| G-03 Read consistency and visibility | Provider guarantees or a conservative no-match/visibility policy | OPEN |
| G-04 Event delivery/replay | Provider sequence/cursor/replay guarantees or a documented REST reconciliation fallback | PARTIAL — no common cursor found |
| G-05 Execution identity | Validated trade-ID uniqueness scope and duplicate observations behavior | OPEN |
| G-06 Quantity/unit semantics | Contract/unit mappings and effective dates | OPEN |
| G-07 Parent/child order semantics | Slicing, multi-leg and linked order lifecycle mapping | PARTIAL |
| G-08 Local evidence lifecycle | Retention, crash recovery, immutable evidence and reconciliation audit requirements | REQUIREMENTS PROPOSED — implementation not designed |
| G-09 Risk/exposure behavior | How unknown orders reserve exposure and block unsafe replacement | OPEN |
| G-10 Fake-provider validation plan | Deterministic fault-injection suite and independent review criteria | PROPOSED — not executed |

**No implementation gate is marked PASS by this document.** The test matrix is specified, not executed.

## 9. Open questions for focused provider follow-up

1. Does Kite, Upstox or Dhan document a caller-controlled idempotency key for placement, modify or cancel? If not, is the only valid strategy to reconcile and require a separately authorized new command?
2. Does each correlation/tag field have uniqueness constraints, scope, retention and collision behavior?
3. What are the read-after-write guarantees for correlation lookup, daily order book, order history and tradebook?
4. Are order and trade snapshots atomic or can a read observe a temporarily inconsistent state?
5. What are the event delivery semantics, sequence IDs, replay windows, heartbeat behavior and resubscribe behavior for each update stream?
6. How are trade corrections, trade busts, exchange cancellations and post-trade adjustments represented?
7. What exact relationships are supplied for auto-sliced, bracket, cover, iceberg, multi-leg and child orders?
8. What are the retention periods for each order/trade endpoint and whether historical account export is available?
9. How are broker-local timestamps, exchange timestamps, session boundaries and late updates defined?
10. Which provider statuses are terminal, can terminal statuses be revised, and what is the provider's authoritative resolution endpoint?
11. Can one provider correlation ID return an order from a different session or an earlier command; what uniqueness scope is enforced?
12. Are the documented rate limits shared across read/write endpoints, account/app keys or user identities, and how should recovery polling be budgeted?

Until answered, preserve each as UNKNOWN and do not promote an undocumented guarantee into an adapter contract.

## 10. Recommended next sequence

1. Independently review PX-025 against the three official API specifications and identify any overgeneralized provider claims.
2. Close only the provider questions that have authoritative public answers; retain unresolved items in a capability matrix rather than guessing.
3. Review PX-025 against the existing AlgoX provenance baseline (`ALG-ARCH-001`) to ensure command attempts, observations, derived claims and reconciliation decisions retain traceable provenance.
4. Produce a separate design candidate only after the contract and gap matrix has been reviewed.
5. If a later implementation is authorized, start with deterministic fake providers and persistence/crash tests; real broker access is not a substitute for those tests.

## 11. Research decisions and non-authorization

- **ACCEPT AS REQUIREMENTS BASELINE:** unknown submission outcomes require reconciliation and prohibit blind retry.
- **ACCEPT:** intent, command, attempt, broker order, exchange order and trade identities remain distinct.
- **ACCEPT:** reconcile order views and trade executions independently; preserve raw observations and derived decisions separately.
- **ACCEPT:** account/session scoping, parent/child mapping, duplicate trade protection, crash recovery and fencing are mandatory acceptance topics.
- **DEFER:** final state enums, schema, persistence technology, retry automation, risk reservation arithmetic and broker adapter interface.
- **NOT AUTHORIZED:** code changes, broker connections, sandbox/production API calls, real orders, paid services, credentials/IP changes, PR creation or merging to `main`.

**Current outcome:** PX-025 requirements and acceptance criteria are documented. No tests were run because no implementation exists in this scope; the original 35 cases plus eight provider-specific amendments (43 total) are specified for a future deterministic fake-provider harness.


## 12. Provider-specific slicing, batch and correlation amendment (2026-11-08)

PX-2026-026 found that the 30 requirements and 35 initial acceptance scenarios need more precise child-order/group semantics. The provider audit is recorded in [PX-2026-026 — Provider idempotency, request correlation and compound-order recovery audit](PX-2026-026-provider-idempotency-and-compound-order-recovery.md).

### Additional normative requirements

**R-031 — Command group has per-child outcome accounting.** A batch, sliced placement or compound command MUST preserve each documented child/line/slice/leg outcome independently. Successful child IDs, rejected child lines, provider errors and unresolved children MUST remain attributable to the local command/intent.

**R-032 — Correlation uniqueness is scoped to the provider contract.** The adapter MUST record the documented meaning and uniqueness scope of each correlation field. Within-payload uniqueness MUST NOT be generalized into cross-request idempotency. Provider tags, per-line correlation IDs, Dhan correlation IDs, broker order IDs and local command IDs MUST remain distinct.

**R-033 — Child-set completeness is independently reconciled.** If one command may create multiple broker orders, the system MUST record both observed children and whether the full child set is established. An incomplete child set MUST remain unresolved; expected count or group identity MUST NOT be guessed from quantity alone.

### Additional deterministic acceptance scenarios

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-036 | Kite auto-slice returns successful IDs and per-slice errors | Preserve each success and failure independently; classify group as partial |
| AT-037 | Kite auto-slice acknowledgement is lost and orderbook reveals only some candidate children | Child-set completeness remains UNKNOWN; no full-quantity resubmission |
| AT-038 | Upstox V3 `slice=true` returns multiple `order_ids` | Preserve every ID as an independent child and reconcile each child's status/trades |
| AT-039 | Upstox multi-order returns HTTP 207 / `partial_success` | Correlate per-line successes/errors using `correlation_id`; no all-success/all-failure collapse |
| AT-040 | Upstox multi-order repeats `correlation_id` inside one payload | Model documented whole-payload rejection; do not treat it as cross-request idempotency |
| AT-041 | Dhan slicing response is lost and public page does not define response shape | Keep group outcome and child-set completeness UNKNOWN until full set is established |
| AT-042 | Dhan Super Order has entry, target and stop-loss legs | Preserve parent and leg identity/state; do not flatten into one ordinary order |
| AT-043 | Dhan correlation lookup returns one order after ambiguous sliced request | Treat it as one discovered order only; do not infer every child was found |

The original AT-001 through AT-035 remain unchanged. PX-025 now contains **33 normative requirements and 43 proposed acceptance scenarios**. These tests remain unexecuted; this amendment is documentation only.
