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

The original AT-001 through AT-035 remain unchanged. PX-025 now contains **36 normative requirements and 49 proposed acceptance scenarios**. These tests remain unexecuted; this amendment is documentation only.


## 13. Provider stream continuity, REST consistency and trade-revision amendment (2026-11-08)

PX-2026-027 reviewed current official provider documentation for WebSocket order updates, reconnect behavior, order/trade REST reads, message identifiers and trade corrections. See [PX-2026-027 — Broker observation consistency, stream gaps and trade-revision semantics](PX-2026-027-broker-observation-consistency-stream-recovery-and-trade-revisions.md).

### Additional normative requirements

**R-034 — Stream-gap completeness requires a documented continuity contract.** Reconnecting a stream MUST NOT be treated as proof that missed messages were replayed. Without documented sequence/cursor and replay/resume semantics, event-history completeness for the gap remains UNKNOWN even if current state can later be reconciled.

**R-035 — Separate REST reads are not an atomic snapshot by default.** Unless a provider documents a shared atomic snapshot/watermark or read-after-write guarantee, order and trade responses fetched separately MUST be treated as independently timed observations. Do not force quantity/status agreement by overwriting evidence.

**R-036 — Trade corrections are append-only and provider-defined.** Preserve original trade observations and later correction/bust/reversal records as separate linked evidence. Apply economic reversal/replacement only when authoritative provider/exchange semantics define it. Missing documentation remains UNKNOWN.

### Additional deterministic acceptance scenarios

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-044 | WebSocket disconnects/reconnects without documented replay cursor | Record gap; reconcile current orders/trades; event-history completeness remains UNKNOWN |
| AT-045 | Orderbook and tradebook reads at different cutoffs temporarily disagree | Preserve both observations/times; do not invent atomicity or force balance |
| AT-046 | Upstox `order_request_id` and `order_ref_id` appear in an update | Preserve as request/order metadata; do not treat as event sequence or replay offset |
| AT-047 | Duplicate/out-of-order updates arrive with equal/coarse timestamps | Retain raw observations; do not infer uniqueness or causal order from timestamps |
| AT-048 | Synthetic trade correction/bust carries an explicit authoritative link | Preserve original and correction; derive net execution only under documented correction rule |
| AT-049 | Trade endpoints expose executions but no correction/bust contract is documented | Correction capability remains UNKNOWN; do not delete/rewrite original trade or claim finality |

The original AT-001 through AT-043 remain in force. The requirements baseline now contains **48 normative requirements and 75 proposed acceptance scenarios**. The scenarios are not executed tests.

### Scope clarification

Kite checksums can authenticate a received HTTP postback but do not establish message completeness. Upstox `order_request_id` and `order_ref_id` are described as request-count/order metadata, not stream cursors. Dhan order IDs and last-updated timestamps identify an order/update but are not documented as a sequence or replay cursor. See PX-027 for source details and limits.

No provider stream was connected and no broker endpoint was called. This amendment is requirements documentation only.


## 14. Portfolio, cash-ledger, charges and contract-note amendment (2026-11-08)

PX-2026-028 reviewed the official broker portfolio, statement, cash-ledger, charges and funds/margin documentation and the NSE investor advisory. See [PX-2026-028 — Portfolio, cash-ledger, charge and contract-note reconciliation](PX-2026-028-portfolio-cash-ledger-charge-and-contract-note-reconciliation.md).

### Additional normative requirements

- **R-037:** keep orders, trades, positions, demat holdings, cash ledger, charges/contract notes, funds/margin and independent evidence as distinct but linkable layers.
- **R-038:** scope accounting records by broker/account/exchange/segment/stable instrument/product and trade/settlement dates; symbols alone are insufficient.
- **R-039:** reconcile position roll-forward from opening quantity plus signed executions plus documented non-trade adjustments; never create balancing plugs.
- **R-040:** preserve settled/DP, T+1, available, used/authorised and collateral/pledged holding buckets independently.
- **R-041:** reconcile cash from signed posted ledger entries with voucher identity and running balance; pending/blocked amounts are not posted cash.
- **R-042:** broker-issued contract notes/statements are evidence for posted charges; virtual/estimated calculators are not substitutes.
- **R-043:** preserve date/segment/side-specific charge components and tariff version; aggregate charges cannot be allocated to individual trades without an authoritative rule.
- **R-044:** available-to-trade, blocked/used margin, collateral, receivables, blocked payouts, ledger cash and withdrawable cash remain distinct.
- **R-045:** keep realised/unrealised/day/carry-forward/MTM/settlement P&L and cash movements separate.
- **R-046:** historical report pagination, period, segment, financial-year and retention completeness are mandatory.
- **R-047:** cross-check holdings/settlement against depository and exchange/bank evidence where available; preserve settlement dates and buckets.
- **R-048:** preserve raw numeric representations and source units; derived money uses exact decimal arithmetic and explicit rounding.

### Additional acceptance scenarios

AT-050 through AT-075 now cover position roll-forward, unsettled/overnight holdings, Dhan ledger vouchers and charges, payment pending state, funds snapshots, Kite virtual contract note, Upstox aggregate charges, issued note variances/missing notes, nullable trade IDs, pagination gaps, settlement boundaries, corporate actions/expiry/pledges, cash running-balance mismatch, duplicate source appearances, exact-decimal parsing, unlike P&L/funds scopes, depository conflicts, non-atomic capture times, dated charge schedules and downstream reconciliation of late-recovered fills.

PX-025 now contains **48 normative requirements and 75 proposed acceptance scenarios** (AT-001 through AT-075). All remain proposed; none was executed in this research work.

### Detailed acceptance matrix — portfolio, ledger and contract-note reconciliation

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-050 | Opening position plus signed trades matches broker closing net position | Reconciliation PASS for that instrument/product/session with all source references retained |
| AT-051 | Broker position differs from computed roll-forward with no adjustment evidence | POSITION_ROLL_FORWARD_VARIANCE; no balancing event fabricated |
| AT-052 | Overnight equity moves from positions view to holdings view | Model the provider's documented portfolio transition; do not interpret it as a missing sell or zero quantity |
| AT-053 | Holdings show T+1, delivered/DP, available and collateral quantities | Preserve separate buckets; do not collapse into one settled/available quantity |
| AT-054 | Derivatives carry forward while day activity is flat/closed | Keep opening/overnight position and day activity distinct |
| AT-055 | Dhan ledger has debit/credit entries and voucher numbers | Verify per-entry signed amounts and running-balance arithmetic; retain voucher identity |
| AT-056 | Dhan trade record includes per-trade tax/charge fields | Preserve raw fields separately and reconcile against actual statement/contract note |
| AT-057 | A pay-in is PENDING or FAILED | Do not count it as posted cash credit; retain transaction ID/status |
| AT-058 | Funds snapshot has available, collateral, utilised and withdrawable values that differ | Preserve each provider-defined component; do not flag a mismatch by comparing unlike buckets |
| AT-059 | Kite virtual contract-note calculator produces a charge total | Label as calculated/virtual estimate; do not substitute for an issued contract note |
| AT-060 | Upstox charge report returns aggregate charges without per-trade allocation | Reconcile at its documented aggregate scope; do not invent per-trade charge splits |
| AT-061 | Actual contract note arrives with a charge total different from the earlier calculator estimate | Keep the issued note as posted-charge evidence; retain estimate and record the variance |
| AT-062 | Contract note is missing after the applicable delivery window | CONTRACT_NOTE_MISSING; no synthetic note generated |
| AT-063 | Contract note total agrees but one individual execution line is missing/mismatched | CONTRACT_NOTE_TRADE_LINE_MISMATCH; total agreement does not close line-level completeness |
| AT-064 | Upstox historical trades have a nullable/empty trade ID for a segment | Preserve record; use a separately validated composite/statement identity or remain UNKNOWN; do not use empty ID as dedupe key |
| AT-065 | Historical trade endpoint uses multiple pages and a middle page is unavailable | SOURCE_PAGINATION_INCOMPLETE; no period-level PASS |
| AT-066 | Trade date and settlement date straddle a calendar/session boundary | Apply date-valid settlement rules and keep both dates; no blanket same-day settlement assumption |
| AT-067 | Corporate action, exercise/assignment, expiry, pledge or settlement changes position without an ordinary trade | Require explicit non-trade adjustment evidence; otherwise UNEXPLAINED_POSITION_ADJUSTMENT |
| AT-068 | Cash ledger running balance does not equal opening plus signed posted entries | LEDGER_RUNNING_BALANCE_VARIANCE; preserve original amounts and source evidence |
| AT-069 | Same trade appears in tradebook, P&L report and contract note | Deduplicate economic execution by validated identity while retaining all source observations |
| AT-070 | API numerics arrive as binary floating values or decimal strings with different scale | Preserve raw input/scale and exact decimal result; no binary-float contamination |
| AT-071 | Broker P&L, trade charges, cash ledger and margin snapshot show different totals because scopes differ | Keep each measure separately typed and explain scope; do not force one total to equal another |
| AT-072 | Depository statement or exchange balance message conflicts with broker holdings/ledger | Raise external-evidence variance; retain both versions and require review |
| AT-073 | Funds snapshot is fetched at a different time from ledger/position data | Store each capture timestamp; do not treat snapshots as one atomic account state |
| AT-074 | Charge tariff/rate changes across effective dates or segments | Calculate using the applicable dated schedule; do not back-apply current rate to historical trades |
| AT-075 | Unresolved order from PX-024/025 later creates a fill that changes the account position/ledger | Link the recovered fill into execution, position and cash reconciliation; preserve the original UNKNOWN interval and resolution provenance |


### Scope clarification

- Kite distinguishes net/day positions and holdings, and its `/charges/orders` page calls the output a **Virtual contract note**.
- Upstox separates historical trades, trade-wise realised P&L, aggregate segment/FY charges and pay-in/payout records.
- Dhan exposes a voucher-based cash ledger, paginated historical trades with exchangeTradeId and charge fields, holdings quantity buckets, positions and a separate fund-limit snapshot.
- NSE's investor advisory asks investors to receive contract notes within 24 hours and account statements at least quarterly, and to verify demat/exchange balance evidence.

No account, broker endpoint, sandbox, real order, code implementation or paid service was used. This amendment is requirements documentation only.


## 15. Derivatives expiry, exercise, delivery and net-settlement requirements amendment

PX-2026-029 identified that order/trade reconciliation must continue through derivatives expiry, exercise/assignment and cash or securities settlement. The provider/clearing rule must be effective-date and product-family scoped.

**R-049 — Contract identity and expiry calendar are effective-dated.** Every derivative contract and expiry event MUST retain the exchange/segment, product family, underlying/security identity, expiry date, holiday calendar, contract-master version, lot/multiplier, tick size, exercise style and settlement-mode source/version. A generic weekday rule MUST NOT override the published contract-specific expiry and holiday schedule.

**R-050 — Settlement mode is explicit per product and date.** The domain MUST distinguish index futures/options from individual-security futures/options and preserve the effective cash/physical settlement mode for the contract date. An unresolved or conflicting mode MUST remain UNKNOWN and block automatic settlement classification.

**R-051 — Automatic exercise and assignment are evidence-backed.** For contracts whose applicable rule specifies automatic exercise, the system MUST retain the expiry reference, ITM decision, series, eligible long quantity, assignment result and clearing/client allocation evidence. Random allocation of long ITM positions to shorts MUST NOT be fabricated or deterministically assigned by AlgoX.

**R-052 — Physical delivery direction is modelled by position and option side.** Stock futures and physically settled stock options MUST produce explicit securities-give/receive and funds-pay/receive obligations with the originating contract, position and trade references. Long/short stock futures and call/put positions MUST NOT be collapsed into one signed cash P&L.

**R-053 — Expiry and settlement are separate lifecycle stages.** The implementation MUST distinguish last-trading/expiry observation, daily MTM/premium settlement, exercise/assignment, obligation generation, delivery/funds pay-in, early pay-in, payout, shortage/auction and final settlement confirmation. An expired order/contract MUST NOT be assumed to mean all resulting obligations are settled.

**R-054 — Delivery and assignment margins are time-bounded obligations.** Delivery/assignment margin MUST retain amount, rule/parameter version, valuation input, assessed time, expiry-to-settlement window and release evidence. Early-pay-in initiation MUST NOT be treated as confirmed delivery or automatic margin release.

**R-055 — Cash/F&O net-settlement eligibility is explicit.** Cross-segment netting MUST be applied only where the applicable SEBI/exchange rules establish eligibility, including the same TM-CM combination and participant-class restrictions. Different clearing-member/corporation routes and excluded institutional categories MUST NOT receive inferred netting benefits.

**R-056 — Client and clearing-member aggregation remain distinct.** Preserve client-level originating obligations, TM/CM mapping, custodial participant category, eligibility decision and clearing-member net settlement output separately. Clearing-member netting MUST NOT overwrite client-level source obligations or imply arbitrary cross-client margin set-off.

**R-057 — Settlement obligations are append-only and linked to source trades.** Exercise, assignment, physical delivery, funds settlement, early pay-in, margin, netting, closeout and payout MUST be recorded as linked settlement events. They MUST NOT mutate/delete the original order or trade evidence. Reconciliation MUST connect those events to PX-028 holdings, ledger, charges and contract-note evidence.

**R-058 — Corporate-action adjustments are versioned and effective-dated.** Bonus, split, consolidation, rights, dividend and other contract adjustments MUST retain the source circular/rule, ex-date/last cum-date, adjustment factor, rounding/tick/lot methodology and old/new contract/position values. No approximate adjustment factor may be inferred from the corporate-action label alone.

**R-059 — Merger closeout is a distinct exchange-originated event.** Where the applicable NSE rule requires forced settlement on a last cum-date, the system MUST preserve the last-cum-date, closing-price reference, affected outstanding contracts, forced settlement obligation and GTC/GTD cancellation event separately from client-initiated orders.

**R-060 — Taxes and charges retain segment-specific settlement provenance.** STT, stamp duty, brokerage and other applicable charges MUST retain the relevant transaction/settlement segment, event type, tariff/rule version and original trade/settlement reference. Cross-segment delivery netting MUST NOT collapse or erase segment-wise STT/stamp-duty computation.

**R-061 — Delivery shortage and default are explicit settlement exceptions.** Missing securities/funds, failed early pay-in, auction, auction failure, closeout, penalty and default handling MUST be explicit evidence-backed states. A generated delivery obligation MUST NOT be marked settled until authoritative pay-in/payout/closeout evidence is captured.



### Acceptance matrix — derivatives expiry, exercise and settlement

The following deterministic tests extend AT-001 through AT-075. Use synthetic contract masters, exchange files and fake clearing results only.

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-076 | Current listed Tuesday expiry falls on a trading holiday | Resolve the previous trading day from the effective holiday calendar and preserve the calendar/version reference |
| AT-077 | Historical contract has a different expiry rule or the applicable master/circular is missing | Do not apply the current Tuesday rule; return UNKNOWN and block automatic expiry classification |
| AT-078 | An index option reaches expiry and is ITM | Create the appropriate cash-exercise settlement event; do not create underlying-share delivery |
| AT-079 | A stock future is open at expiry after daily MTM settlements | Preserve daily MTM history and create separate physical share/funds delivery obligations for the long/short positions |
| AT-080 | An ITM physically settled stock call is long | Create share-receipt and strike-funds-pay obligation linked to the option series and source trades |
| AT-081 | An ITM physically settled stock call is short and assigned | Create share-delivery and strike-funds-receivable obligation only for the assigned quantity |
| AT-082 | An ITM physically settled stock put is long | Create share-delivery and strike-funds-receivable obligation linked to the option position |
| AT-083 | An ITM physically settled stock put is short and assigned | Create share-receipt and strike-funds-pay obligation only for the assigned quantity |
| AT-084 | Short option position is not assigned in the exchange's random allocation | Preserve the exchange assignment result; do not assume every short ITM position is assigned |
| AT-085 | Long ITM option is automatically exercised under the effective rule | Create an exercise result even without a client-initiated close order; preserve the expiry reference and clearing allocation |
| AT-086 | Clearing member allocates exercised positions to clients | Preserve client-level allocation evidence and link each result to the original option position |
| AT-087 | Delivery margin is assessed from expiry until settlement | Retain margin amount/parameter version and due window; do not treat margin as a trade expense |
| AT-088 | Early pay-in is initiated but not confirmed | Keep delivery obligation open and margin unreleased until authoritative confirmation |
| AT-089 | Expiry+1 settlement date crosses a clearing/bank holiday | Resolve the actual date from the published settlement schedule; do not use a fixed 24-hour offset |
| AT-090 | Cash and physical F&O expiry obligations use the same eligible TM-CM combination | Apply only the documented eligible net-settlement process and preserve pre-net cash/F&O obligations |
| AT-091 | Cash and F&O trades clear through different clearing members/corporations | Do not net the obligations; keep both settlement routes separate |
| AT-092 | Institutional/FPI account is presented for cross-segment netting | Reject the netting eligibility under the SEBI 2022 exclusion; preserve original gross obligations |
| AT-093 | Eligible physical F&O delivery is netted with cash-market delivery | Keep STT and stamp duty computed/reported segment-wise; do not collapse tax provenance |
| AT-094 | Clearing-member net obligations differ from one client's gross obligations | Retain client, TM, CM and clearing output layers; never substitute the CM net figure for the client obligation |
| AT-095 | Bonus or split adjustment affects open contracts | Apply the date-effective official adjustment factor, tick/lot rounding and revised position; retain original and adjusted contract identities |
| AT-096 | Rights issue adjusts strike, futures base price, lot and position | Use the official event-specific factor and preserve old/new values and formula version |
| AT-097 | Extraordinary dividend meets the effective adjustment threshold | Apply the correct dated NSE method; an ordinary dividend below the threshold must not receive the extraordinary adjustment |
| AT-098 | Merger imposes compulsory settlement on last cum-date | Create a forced-closeout event at the official reference price and preserve the affected contracts |
| AT-099 | GTC/GTD orders remain open on merger last cum-date | Record exchange-originated cancellation separately; do not represent it as a user cancel request |
| AT-100 | Securities/funds delivery fails or auction/closeout occurs | Keep settlement exception states and authoritative auction/closeout evidence; never mark ordinary settlement PASS without it |


### Latest requirements baseline status — PX-029

PX-029 adds R-049 through R-061 and AT-076 through AT-100. The consolidated requirements baseline now contains **76 normative requirements (R-001–R-076) and 130 proposed acceptance scenarios (AT-001–AT-130)**. The new expiry/settlement scenarios are specified only; no test was executed and no settlement code was implemented.

## 16. Equity-derivatives margin calculation, collection and risk controls (2026-11-08)

PX-2026-030 adds the source-derived margin requirements from NSE Clearing, SEBI and the Kite/Upstox/Dhan broker API surfaces. It distinguishes portfolio margin calculation, client collection, peak/EOD verification, actual collected collateral, member-level margin, shortfall and release.

### Additional normative requirements

**R-062 — Margin parameters are source-versioned and effective-dated.** Every margin calculation MUST retain the exact exchange/clearing parameter-set identity, source/reference file, effective timestamp/date, market snapshot and applicable contract-master version. A current SPAN/ELM rate MUST NOT be applied retrospectively to historical positions.

**R-063 — Portfolio-based margin is not per-order isolation.** Margin calculation MUST account for all in-scope positions and eligible open orders of the same client, product and account. It MUST preserve per-client netting and the resulting member-level gross total separately. A standalone per-order estimate MUST NOT be represented as the client's complete portfolio margin unless the source calculation explicitly includes the relevant portfolio.

**R-064 — Upfront collection includes applicable client net option premium.** For equity-derivatives trades on and after 1 February 2025, the upfront collection/verification requirement MUST include net options premium payable at client level in addition to IM and ELM, using the effective SEBI/exchange definition. Historical trades MUST use the rule effective on their date.

**R-065 — BOD verification parameters differ from live clearing parameters.** The system MUST distinguish the fixed BOD parameters used for client upfront-margin verification/shortfall assessment from the refreshed intraday/EOD parameters used by Clearing Corporations for actual clearing obligations. It MUST NOT treat a BOD verification snapshot as the live clearing requirement or assume clearing requirements remain static during the day.

**R-066 — No cross-client or client/proprietary margin set-off.** The margin core MUST net positions only within the permitted individual-client scope and MUST NOT offset one client's excess margin against another client's requirement. Proprietary positions MUST remain separate from client positions. Any cross-margin benefit MUST be traceable to the applicable approved framework, client and eligible position set.

**R-067 — Margin components remain separately attributable.** SPAN/initial, ELM, net option premium, CCO, delivery, assignment, tender, additional/special, cross-margin benefit, collected collateral, utilization, shortfall and release MUST be represented separately. A single total may be derived, but the component inputs and source rules MUST remain auditable.

**R-068 — Basket/hedge benefits are conditional and revocable.** A spread or hedge benefit MUST be calculated from the complete eligible portfolio using the effective exchange rules. Closing, expiry, exercise, corporate action or other loss of a hedge leg MUST trigger a fresh margin evaluation. The previous basket result MUST NOT be carried forward after its supporting position set changes.

**R-069 — Expiry and delivery margin link to settlement lifecycle.** Delivery, tender and assignment margin MUST retain the expiry/settlement date, applicable contract family, delivery mode, assessment/release period and source rule. Margin must be recalculated when a contract enters the tender/delivery/assignment window. This requirement links to PX-029 physical-settlement obligations.

**R-070 — CCO is distinct intraday and EOD evidence.** Intraday CCO MUST use the documented client-level closed-futures crystallized P&L and payable/receivable premium inputs. EOD CCO MUST preserve the additional futures MTM, options premium, option exercise/assignment and futures final-settlement inputs. The two calculations MUST NOT be collapsed into an unexplained daily total.

**R-071 — F&O collection deadline is segment-specific.** For the reviewed NSE F&O member FAQ, SPAN/ELM MUST be collected before trade; delivery margin and CCO MUST be collected by T+1 day. The cash-segment settlement-day change in SEBI Circular 2025/57 MUST NOT be generalized into an F&O collection rule. The exact current effective rule and trading/settlement calendar must be checked for the relevant segment and date.

**R-072 — Required margin and actual collected margin are separate records.** The system MUST retain the amount required, amount available, amount actually collected/blocked, amount reported, collection timestamp, collection instrument/source and any shortfall separately. It MUST NOT derive “collected” from “required” or a margin calculator response.

**R-073 — Peak-margin snapshots are preserved with purpose and parameters.** Every intraday snapshot MUST retain its capture window/time, client scope, reported component values and verification parameter set. The system MUST preserve EOD and peak-across-snapshot values separately. Snapshot count/selection and reporting rules must be date-versioned.

**R-074 — Margin release follows confirmed obligation settlement.** Delivery/CCO/assignment/other margin MUST remain allocated until the effective release condition has been met and confirmed by authoritative settlement/clearing/broker evidence. Order cancellation, position flattening, early-pay-in initiation or a broker display change alone MUST NOT prove the corresponding margin release.

**R-075 — Collateral eligibility and member-level liquidity remain distinct.** Collateral type, ownership/client allocation, encumbrance, applicable haircut, eligible value and liquid-cash classification MUST be preserved independently. Clearing-member deposit composition requirements (including the published 50% cash-component rule) MUST NOT be misapplied as a universal client cash percentage. Client collateral segregation/eligibility must follow its own effective rules.

**R-076 — Margin shortfall and reporting conflict fail closed.** An unmet upfront requirement, a T+1 shortfall, unavailable collateral, missing client allocation, stale calculation or mismatch between actual collections and reported collections MUST remain an explicit risk exception. The system MUST NOT permit a new position on the assumption that an uncollected or unverified amount is available, and MUST NOT fabricate a collection record to satisfy reporting.

### Additional deterministic acceptance scenarios

The following use synthetic portfolio, parameter, collection and fake clearing/broker fixtures only.

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-101 | SPAN/ELM input parameter set is missing or stale | Margin result UNKNOWN; no zero/default margin or order clearance |
| AT-102 | Existing same-client positions and open orders affect a new order's SPAN | Compute against the complete supplied portfolio context; record exactly which positions/orders were included |
| AT-103 | A two-leg spread receives a documented eligible hedge benefit | Record gross leg margins, eligible benefit and net requirement separately with the rule version |
| AT-104 | One hedge leg is closed, expired or becomes ineligible | Recompute the remaining portfolio margin; revoke unsupported prior hedge benefit |
| AT-105 | Client submits an order without upfront SPAN/IM and ELM collected | Block/reject pre-trade authorization; do not rely on post-trade collection |
| AT-106 | Equity-derivatives option buyer has net premium payable on/after 1 February 2025 | Include client-level net option premium in upfront collection and verification |
| AT-107 | Multiple option trades create offsetting premiums within one client | Calculate net payable premium at the client scope under the effective rule; do not sum all gross buy premiums |
| AT-108 | Client verification snapshot uses fixed BOD parameters while Clearing Corporation updates live parameters intraday | Preserve both values with purpose; do not label them contradictory or substitute one for the other |
| AT-109 | Four or more randomly selected intraday snapshots and an EOD margin report are supplied | Preserve each timestamped snapshot and independently derive peak and EOD verification requirements |
| AT-110 | Two clients have opposite/surplus margin positions | Do not set off one client's surplus against the other's requirement |
| AT-111 | Proprietary positions hedge client positions at member level | Keep proprietary and client risk/offset ledgers separate; no proprietary-to-client set-off |
| AT-112 | Basket margin estimate changes after a position or open order is added | Recalculate complete portfolio margin; preserve request context and before/after deltas |
| AT-113 | Kite margin API order response considers existing positions/open orders and basket API evaluates a spread | Preserve broker estimate and input scope; do not treat it as Clearing Corporation or collection evidence |
| AT-114 | Upstox margin response contains SPAN, ELM/exposure, net buy premium and tender-margin fields | Preserve each field separately; apply tender margin only according to its provider/effective contract definition |
| AT-115 | Dhan multi-order margin request includes existing positions and open orders | Record inclusion flags and complete scrip list; do not compare with a calculation that omits these inputs |
| AT-116 | Contract approaches expiry and delivery/tender/assignment margin becomes applicable | Recompute with date-effective expiry rules and link margin to settlement obligation |
| AT-117 | F&O upfront and T+1 collection timelines are evaluated | Require SPAN/ELM before trade; enforce current F&O T+1 collection for delivery/CCO; do not apply cash-segment 2025/57 settlement-day rule to F&O |
| AT-118 | Cash-segment non-upfront margin falls under SEBI Circular 2025/57 | Use settlement-day rule for the cash segment only; retain segment scope in the rule reference |
| AT-119 | Intraday CCO contains premium payable and crystallized futures loss | Compute/record intraday payable CCO at client level from the two documented inputs |
| AT-120 | EOD CCO includes futures MTM, premiums, expired option exercise/assignment and futures final settlement | Reconcile each component before classifying EOD CCO payable/receivable |
| AT-121 | Short index option due to expire incurs additional expiry-day ELM under the effective parameter set | Apply the dated rule to all eligible open and newly initiated due-to-expire positions; never hard-code it across all historical dates |
| AT-122 | Member reports required margin as collected but collection ledger has no matching client cash/collateral evidence | FALSE_COLLECTION_REPORTING_CONFLICT; block PASS and preserve the missing/short collection evidence |
| AT-123 | Approved collateral is present but after haircut/encumbrance its eligible value is below requirement | Calculate eligible value using dated haircut/eligibility; record shortfall rather than nominal face value |
| AT-124 | Delivery/CCO margin remains blocked after order cancellation but settlement is not complete | Keep margin allocated until the documented settlement/release condition is evidenced |
| AT-125 | Clearing member satisfies its 50% cash-component effective-deposit rule using CM-level deposits | Validate at CM level only; do not translate it into a blanket 50% retail-client cash requirement |
| AT-126 | SPAN parameters update intraday while a broker calculator returns a value from an earlier timestamp | Store both parameter timestamps; classify stale estimate and recalculate before risk clearance |
| AT-127 | Current published ELM rates differ from the rate applicable to a historical trade date | Use the historical effective parameter file; never back-apply the current website table |
| AT-128 | Expiry-day calendar-spread benefit is withdrawn under the applicable rule | Recalculate margin without the expired benefit and preserve the triggering expiry/rule evidence |
| AT-129 | A margin shortfall is detected but the collection/reporting API is unavailable | Keep shortfall unresolved and fail closed; do not assume collection or emit a synthetic success |
| AT-130 | Settlement is completed and clearing/broker evidence confirms margin release | Release only the confirmed amount; retain the release event, linked obligation, timestamp and source reference |

PX-025 now contains **162 normative requirements (R-001–R-162) and 310 proposed acceptance scenarios (AT-001–AT-310)**. The new margin scenarios are proposed for future fake-provider/fake-clearing tests only; no test was executed.


## 17. Clearing margin reports, collateral short allocation and PRISM enforcement (2026-11-08)

PX-2026-031 reviews the official UDiFF catalogue, client margin/short-allocation reporting page, PRISM/violations page and payment-of-margin page. See [PX-2026-031 — Clearing margin reports, short allocation and risk enforcement](PX-2026-031-clearing-margin-reports-short-allocation-and-risk-enforcement.md).

### Additional normative requirements

**R-077 — Clearing-report parser is UDiFF-versioned.** A future report-ingestion component MUST pin the UDiFF standard/workbook version, applicable circular, report name, segment and effective date for every parsed file. It MUST preserve the original file/hash and parser version. It MUST NOT infer field positions, codes or semantics from an older report or from a filename alone.

**R-078 — Intraday margin snapshots are individually preserved.** Every client-wise snapshot MUST retain its original report identity, snapshot time/window, client/TM/CP/member scope, segment, parameter version and raw margin components. The implementation MUST support the minimum-four-random-snapshot framework without assuming fixed snapshot times.

**R-079 — EOD, peak and short-allocation measures remain distinct.** The system MUST preserve EOD requirement, each intraday snapshot requirement, peak-across-snapshots requirement, reported collection, available margin and short allocation separately. It MUST NOT replace them with one daily total or assume that agreement in one comparison proves all other comparisons pass.

**R-080 — Collateral allocation is explicitly scoped.** Collateral allocation MUST be tracked by Clearing Member, Trading Member, Custodial Participant, client/proprietary flag, segment and collateral source. Allocated collateral and securities re-pledged to the Clearing Corporation MUST be separately identifiable and must not be attributed to the wrong client or segment.

**R-081 — Deemed member-proprietary allocation is not client collection.** Where member proprietary collateral is blocked/deemed allocated to cover a TM Prop/CP/client margin requirement, the system MUST preserve the provider-deemed allocation, supplying member, supported beneficiary and segment as a separate evidence event. It MUST NOT represent the blocked member collateral as cash or collateral actually paid by the client.

**R-082 — Short allocation uses the published minimum-upfront definition.** The short-allocation calculation MUST use the applicable published minimum client upfront collection requirement (including BOD SPAN/ELM and net option premium where effective) less the defined eligible client collateral value in that segment. It MUST respect the source's specific exclusions for margins permitted to be collected by T+1/T+2. The resulting short-allocation metric MUST NOT be substituted for total margin liability.

**R-083 — Shortfall penalty comparison preserves all three tests.** The calculation MUST preserve the separate EOD shortfall, peak-across-snapshots shortfall and highest intraday/EOD short-allocation amount after permitted excess collateral/reason codes. Where the applicable rule uses the higher amount, the source inputs and selected maximum MUST remain reproducible.

**R-084 — Report upload/sign-off deadlines are distinct from collection deadlines.** The system MUST record report upload and sign-off status against the applicable reporting calendar (including the published T+5 upload/sixth-working-day sign-off procedure where effective). It MUST NOT interpret this reporting window as permission to delay upfront client collection.

**R-085 — Non-reporting is an explicit full short-reporting exception.** Missing or incomplete client-margin reporting MUST be recorded as a separate non-reporting exception and processed according to the applicable rule (the reviewed page treats it similarly to 100% short reporting). An absent file MUST NOT be treated as a zero-margin/zero-shortfall report.

**R-086 — Member-level risk utilization thresholds remain scoped to the member.** Any implementation of the published PRISM 70%/80%/90% warnings and 100% Trading Member facility withdrawal MUST bind them to the TM effective-collateral scope and effective rule version. It MUST NOT apply those values as universal retail-client RMS thresholds or automatically square off a client solely from this member-level page.

**R-087 — CM/TM violations and client short allocation remain distinct.** The system MUST separately classify client short allocation, TM effective-collateral utilization/limit violation, CM effective-deposit/liquid-net-worth violation and position-limit violation. A violation at one layer MUST NOT be misreported as a client shortfall at another layer without source-supported allocation.

**R-088 — Risk-enforcement response is evidence-backed.** A member-level margin violation response (additional collateral, member limit change, facility disablement, closeout or other action) MUST retain the triggering requirement, effective collateral, utilization, threshold, member scope, source event/time and observed enforcement result. A warning message alone MUST NOT be recorded as a completed closeout or as proof that collateral was deposited.

### Additional deterministic acceptance scenarios

The following extend AT-001 through AT-130. All use deterministic synthetic UDiFF/report/clearing fixtures; no membership portal or live clearing file is needed.

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-131 | Margin report is parsed without a known UDiFF version/circular | Reject semantic parsing or return UNKNOWN; preserve original file/hash and do not guess fields |
| AT-132 | UDiFF margin file changes to include net option premium under NCL/CMPT/65315 | Apply only the date-effective schema; retain premium as a separate component |
| AT-133 | T+0 settlement report schema revision is encountered | Select the applicable report/version/segment; do not parse it as an unchanged prior UDiFF file |
| AT-134 | Only three intraday snapshots are present where the effective framework requires at least four | Snapshot-set completeness exception; no peak-verification PASS |
| AT-135 | Four snapshots have different client SPAN/ELM/net-premium values | Preserve each timestamp and calculate peak across the actual provided snapshots |
| AT-136 | EOD margin file uses EOD positions and BOD parameters | Retain both effective parameter purpose and EOD position scope; do not compare it as live intraday clearing margin |
| AT-137 | MG09/10 CM/TM totals and MG13 client details are ingested together | Preserve report scope and reconcile aggregates without substituting CM totals for a client amount |
| AT-138 | Same instrument/client appears in two segments with separately allocated collateral | Maintain segment-specific collateral allocation; no silent cross-segment or cross-client reuse |
| AT-139 | Client allocated collateral is short and CM proprietary collateral is blocked as deemed allocation | Record the deemed allocation and supplying member separately; do not mark client-paid collateral as increased |
| AT-140 | Re-pledged securities collateral is part of client collateral value | Apply the source-defined segment/client scope and collateral value basis; preserve raw and eligible values |
| AT-141 | Short-allocation calculation has upfront SPAN/ELM/net premium plus other T+1 collection items | Include the prescribed upfront components and exclude only the margins the short-allocation definition permits to be collected later |
| AT-142 | One client's collateral exceeds requirement while another client is short | No cross-client offset; short allocation remains client-specific |
| AT-143 | Report file is uploaded on T+5 and signed off on sixth working day | Record as reporting timeliness only; upfront collection deadline remains unchanged |
| AT-144 | Client margin report is not submitted | NON_REPORTING exception with the published 100%-short-reporting treatment; no zero-filled file |
| AT-145 | EOD shortfall, peak shortfall and short-allocation metrics differ | Preserve all three and select the rule-defined higher amount for penalty; keep calculation trace |
| AT-146 | TM effective collateral reaches 70% utilization in PRISM | Record TM-level warning only; do not apply an automatic retail-client square-off |
| AT-147 | TM effective collateral reaches 80% utilization | Record the correct TM-level warning and utilization evidence |
| AT-148 | TM effective collateral reaches 90% utilization | Record the correct TM-level warning and utilization evidence |
| AT-149 | TM effective collateral reaches 100% utilization | Record facility withdrawal for the TM scope; do not assume every client account has been individually disabled unless separately evidenced |
| AT-150 | CM liability exceeds effective deposit less minimum liquid net worth, or TM liability exceeds CM-set limit | Record member-level margin violation and enforcement evidence separately from client short allocation |

PX-025 now contains **88 normative requirements (R-001–R-088) and 150 proposed acceptance scenarios (AT-001–AT-150)**. The new report/short-allocation scenarios are proposed only; no parser, fake provider or risk-enforcement implementation exists in this research work.

### UDiFF inspection limitation

The official UDiFF catalogue and its report-family/change history were reviewed. The linked Annexure B XLSX workbook could not be parsed by the research connector, and the related ZIP downloads were unavailable. Therefore the field-level schema, code lists and actual sample rows remain uninspected. No field-level parser contract is claimed.

## 18. Position limits, MWPL ban period and intraday index risk monitoring (2026-11-08)

PX-2026-032 adds the current FutEq-based single-stock MWPL/ban process, entity position limits, index intraday snapshots and expiry-day ASD. See [PX-2026-032 — Position limits, MWPL ban period and intraday risk monitoring](PX-2026-032-position-limits-mwpl-ban-period-and-intraday-risk-monitoring.md).

### Additional normative requirements

**R-089 — Position-limit sources are effective-dated and versioned.** Every position-limit decision MUST retain the exchange/segment, underlying/security, entity category, member/client scope, applicable MWPL, individual/entity cap, source circular/annexure, effective period, retrieved file/hash and parameter version. A historical or stale HTML table MUST NOT be treated as the current limit schedule.

**R-090 — Client limits aggregate across relevant trading members.** Where the applicable rule defines a client limit across different members, the calculation MUST aggregate all relevant positions for the same client/entity identity across those members and the applicable exchange/clearing scope. A broker-local account subtotal MUST NOT be represented as the full entity exposure. If client identity mapping or cross-member data is incomplete, the total is UNKNOWN.

**R-091 — FutEq uses contract-specific delta evidence.** The system MUST preserve raw contracts/open positions and compute/ingest FutEq using the applicable contract delta factor for symbol, expiry, strike, option type and timestamp. The delta source file/version and parameter snapshot MUST be retained. Raw OI, notional OI and FutEq OI MUST remain distinct measures.

**R-092 — MWPL calculation is quarterly, source-based and corporate-action adjusted.** For the rule introduced by SEBI 2025/79, the MWPL calculation MUST use the lower of 15% free float and 65 times market-wide ADDV in quantity, subject to the 10% free-float floor, and the preceding three-month ADDV window. It MUST preserve the calculation inputs, reference period and quarterly effective date. Applicable corporate-action factors MUST be applied only from the effective source; no stale monthly limit may be carried forward.

**R-093 — MWPL ban activation and resumption are cross-exchange EOD conditions.** Under the current FutEq framework, the ban MUST be activated only after the EOD market-wide FutEq OI for the stock exceeds 95% of the applicable MWPL, with the ban effective from the next trading day. Normal trading MUST remain restricted until combined FutEq OI across exchanges is 80% or below MWPL. An intraday alert MUST NOT be converted into next-day ban status without the prescribed EOD test.

**R-094 — Ban-period Day 1 baseline is immutable.** The system MUST preserve the entity's Day 1 baseline positions when a security enters ban and the exact delta snapshot used to create the base FutEq value. Subsequent daily comparisons MUST use the source-prescribed position and delta times (including the specified 2 PM snapshot) and must be reproducible from raw position and delta files.

**R-095 — Passive delta movement and expiry roll-off are not fabricated as active increases.** The ban reconciler MUST distinguish actual position changes from FutEq changes caused only by a delta-factor movement. It MUST apply the official Day 1/current-day comparison and sign rule. An expiry-related passive change that the applicable exchange rule excludes MUST NOT be penalized as an active increase. The system MUST retain enough evidence to show why a change was active or passive.

**R-096 — Entity-level stock limits use the latest applicable category and security schedule.** The implementation MUST distinguish client/NRI/scheme, TM combined, TM proprietary, FPI Category I/II and Mutual Fund scopes. It MUST load the latest applicable per-security MWPL and entity cap for the effective period (including any 1 October 2026 schedule only after the official NCL/CMPT/76459 circular and Annexure I are independently retrieved; secondary metadata alone is insufficient). It MUST NOT hard-code category percentages from the September 2025 schedule as current October 2026 values without verifying the operative Annexure I.

**R-097 — Intraday index monitoring retains every required snapshot.** For equity-index derivatives, the system MUST retain at least four randomly timed snapshots in the prescribed windows, with client/entity identity, raw positions, applicable limit, underlying price, delta/FutEq factor, snapshot time and source/report identity. It MUST NOT assume fixed snapshot times or use a daily bar to reconstruct an actual snapshot.

**R-098 — Index-option expiry ASD is limited to the effective expiry-day framework.** For the applicable index-option expiry-day intraday breach framework effective from 8 December 2025, the system MUST preserve the breach snapshot, cure-period snapshot, EOD comparison, cash/cash-equivalent allocation and ASD calculation. It MUST apply the source-defined 1.5x intraday ASD and one-month block only where applicable. It MUST NOT apply this expiry-day ASD to non-expiry-day intraday alerts.

**R-099 — Existing-limit intraday monitoring and expiry-day ASD are separate rule states.** The system MUST preserve the 2025/41 rule that existing notional-limit intraday breaches were not treated as violations/penalties until further directions, alongside the later 2025/122 and NSE implementation of expiry-day index-option ASD. It MUST apply the effective rule by product, entity, date and expiry status; it MUST NOT generalize either statement to every index intraday or stock MWPL case.

**R-100 — Ban files, delta files and violation files are completeness-gated inputs.** A position-limit decision MUST retain and validate the daily ban-period security list, combined cross-exchange MWPL/OI data, contract delta file, member/entity FutEq files and any applicable violation report. Missing, stale, partial, corrupt or mismatched-date inputs MUST result in UNKNOWN, not a pass or zero exposure.

**R-101 — Position limits, margin and member PRISM controls remain distinct.** The system MUST model position-limit utilization, MWPL ban state, margin requirement/shortfall, client collateral availability and member-level effective-collateral/PRISM utilization as separate risk dimensions. One dimension MUST NOT be inferred from another. Any automated block or warning MUST carry the scope and source rule that authorizes that control.

### Additional deterministic acceptance scenarios

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-151 | Position-limit parameter set is missing, stale or effective date does not cover the trade date | UNKNOWN; no position-limit clearance or invented default |
| AT-152 | Same client's stock-derivative position is split across two brokers/trading members | Aggregate under the applicable client identity/rule; do not assess each broker account independently |
| AT-153 | Client identity mapping across trading members is incomplete | Cross-member total remains UNKNOWN; do not assume broker-local exposure is the client total |
| AT-154 | Option contract delta file is missing for one expiry/strike | FutEq calculation UNKNOWN for affected positions; do not substitute delta 1 or stale delta |
| AT-155 | Futures and options on the same stock have different delta factors | Compute FutEq with the correct factor per contract and retain raw OI separately |
| AT-156 | MWPL inputs provide 15% free-float quantity and 65x ADDV quantity | Select the lower, enforce the 10% free-float floor and record the calculation trace |
| AT-157 | Quarter boundary changes the ADDV reference window and MWPL | Use the rolling preceding three-month period and the new effective date; do not apply monthly/stale limits |
| AT-158 | Corporate action changes the applicable MWPL from an ex-date | Apply only the published adjustment factor from that date and retain pre/post limits |
| AT-159 | Market-wide FutEq OI closes at 94.99% of MWPL | Do not activate ban; retain the EOD ratio and source inputs |
| AT-160 | Market-wide FutEq OI closes above 95% of MWPL | Mark stock for ban beginning the next trading day, not immediately during the current session |
| AT-161 | NSE-only OI exceeds a warning threshold but cross-exchange FutEq has not reached ban trigger | Preserve the warning and market-wide test separately; do not enter ban solely from the alert |
| AT-162 | Market-wide FutEq OI falls to 80% or below across exchanges | Resume normal trading only after the applicable source-confirmed EOD condition is met |
| AT-163 | Market-wide OI remains between 80% and 95% after ban | Keep ban active; do not resume early |
| AT-164 | Day 1 ban baseline is captured and Day 2 uses new delta factors | Recompute current FutEq using the prescribed 2 PM delta and EOD positions; retain raw positions and comparison values |
| AT-165 | Day 2 contract delta changes while raw entity positions are unchanged | Classify passive FutEq change according to the official baseline comparison; no false active-increase violation |
| AT-166 | Position reduction crosses through zero and changes FutEq sign | Apply the source sign rule; do not call it a valid reduction merely because absolute magnitude is lower |
| AT-167 | Entity increases raw contracts during ban but delta-weighted EOD FutEq remains at/below base without sign change | Apply the effective FutEq rule and source evidence; do not use raw contract count alone to decide |
| AT-168 | Near-month expiry causes passive open-interest/FutEq movement during ban | Apply the documented expiry-passive treatment; do not levy an active-increase penalty without the triggering evidence |
| AT-169 | Ban-period trade creates new exposure rather than offsetting an existing position | Flag violation and compute the applicable ban-increase penalty basis |
| AT-170 | Ban begins next day after EOD 95% trigger | Enforce offset-only trading for the next trade date; do not restrict the trigger day retrospectively |
| AT-171 | Security returns to normal only after combined all-exchange FutEq reaches 80% | Keep restriction until the cross-exchange condition is met; one exchange's local OI is insufficient |
| AT-172 | Current entity-limit annexure is the 1 October 2026 NCL/CMPT/76459 schedule | Require the actual applicable annexure/security row; if unavailable, return UNKNOWN instead of using 2025 category table |
| AT-173 | TM combined proprietary+client, TM proprietary-only and client limits are assessed together | Preserve each limit scope separately; do not substitute TM combined cap for client cap |
| AT-174 | FPI Category I, FPI Category II subcategories, MF scheme and NRI client have different applicable limits | Apply the correctly classified entity rule and date-specific schedule; ambiguous category remains UNKNOWN |
| AT-175 | Index-derivative intraday monitoring supplies four random snapshots | Preserve each snapshot and calculate applicable peak/breach state; do not assume snapshots occur at fixed times |
| AT-176 | Intraday index position snapshot has an underlying price different from EOD close | Use the price/time input prescribed for that snapshot; do not value the intraday exposure with stale close |
| AT-177 | Intraday breach occurs on a non-expiry day under the 2025/41 / 2025/122 framework | Preserve the intraday observation and applicable surveillance rule; do not apply the expiry-day ASD automatically |
| AT-178 | Intraday breach occurs on an index-option expiry day after 8 December 2025 | Apply the current expiry-day ASD process, including cure-period/EOD comparison, 1.5x intraday ASD and one-month block where the source conditions are met |
| AT-179 | Missing delta/ban file or incomplete exchange snapshot set prevents a reliable breach calculation | Position state UNKNOWN; do not clear order or manufacture a pass |
| AT-180 | Position-limit alert exists while SPAN margin is sufficient; or margin shortfall exists while position limit is within bounds | Preserve the two separate risk dimensions and trigger only the rule-specific control |

PX-025 now contains **101 normative requirements (R-001–R-101) and 180 proposed acceptance scenarios (AT-001–AT-180)**. These are proposed deterministic scenarios, not executed tests.

## 19. Order admission, exposure classification and independent risk gates (2026-11-08)

PX-2026-033 composes the broker recovery, margin, position limit, MWPL ban, expiry/settlement and member-risk controls into a single admission policy model. See [PX-2026-033 — Order admission, exposure classification and independent risk gates](PX-2026-033-order-admission-independent-risk-gates-and-exposure-classification.md).

### Additional normative requirements

**R-102 — Admission is a conjunction of independent mandatory gates.** A future order-admission service MUST evaluate every applicable market, contract, command-recovery, exposure, MWPL/ban, entity-limit, index intraday, margin/collection, expiry/settlement and provider-validation gate. A PASS in one dimension MUST NOT compensate for a FAIL or UNKNOWN in another dimension.

**R-103 — Projected exposure includes positions, working orders and unresolved attempts.** Projected exposure MUST include broker-observed positions, unique reconciled trades, working-order residuals, partial fills, child orders and any possibly dispatched command whose outcome is unresolved. Opposing working orders MUST NOT be netted away unless an authoritative provider/exchange rule proves such netting is valid.

**R-104 — Action classification is based on projected exposure, not order-side text.** PLACE, OFFSET, REDUCE, CLOSE, MODIFY, CANCEL and REPLACE MUST be classified using the projected post-action portfolio across each relevant exposure/risk dimension. A buy/sell string or user-supplied reduce-only label MUST NOT by itself establish that the action reduces exposure.

**R-105 — UNKNOWN blocks exposure-increasing admission.** If any mandatory identity, contract, position, ban, entity limit, delta, margin/collection, expiry/settlement or prior-command input is UNKNOWN, the system MUST NOT admit an action that could increase exposure. It MUST retain the reason and evidence needed to resolve the state.

**R-106 — Cancel, modify and replace are distinct commands.** The system MUST retain independent command/attempt identity and outcome for cancellation, modification and replacement. A cancel request MUST NOT be treated as completed cancellation; a replacement MUST NOT be assumed atomic unless the provider contract explicitly establishes it; an unknown outcome MUST be reconciled before issuing a conflicting command.

**R-107 — Ban-period reduction requires rule-specific proof.** During a single-stock MWPL ban, the system MUST admit only actions that meet the effective source's offset/reduction rule, including FutEq, Day 1 baseline, current delta and sign constraints. It MUST NOT classify an order as permitted merely because it is opposite-side or labelled reduce-only.

**R-108 — Entity-limit admission uses complete in-scope aggregation.** Projected position-limit evaluation MUST use the relevant client/entity/TM/TM-proprietary/FPI/MF category and all required member/exchange positions. If the rule requires cross-member aggregation and the system has only one broker-local subtotal, the gate MUST be UNKNOWN rather than PASS.

**R-109 — Margin admission requires collection evidence, not a calculator.** For any rule requiring upfront client margin, the system MUST independently verify the applicable requirement and actual eligible client cash/collateral collection. Margin-calculator output or available-balance snapshot alone MUST NOT clear the gate.

**R-110 — Hedge and basket changes invalidate prior margin/risk approval.** Any change to existing positions, working orders, basket legs, option premium, delta, expiry, corporate action or hedge eligibility MUST trigger recalculation of every affected gate. A previous per-order/basket calculation MUST NOT be reused after the supporting portfolio or parameter set changes.

**R-111 — Expiry and settlement risk is part of admission.** Before admitting an action that can create or increase an expiring derivative position, the system MUST evaluate contract-specific expiry, exercise style, cash/physical settlement mode, delivery/assignment margin, settlement calendar and available delivery capacity. Missing contract/settlement data MUST block exposure increase.

**R-112 — Compound and sliced orders require parent and child admission.** A group request MUST be checked at parent aggregate scope and each child/leg scope. The system MUST preserve partial success/failure and child-set completeness. A parent-level margin result or group approval MUST NOT automatically authorize every child.

**R-113 — Provider/exchange validation is distinct from domain risk approval.** Order price, quantity, tick, freeze, order variety, product, market session and provider-specific request validation MUST be evaluated separately from market/portfolio risk gates. A domain-level ALLOW MUST NOT be represented as broker acceptance or proof that the request will pass provider validation.

**R-114 — Warning signals are not automatically hard blocks.** The system MUST distinguish advisory alerts from regulatory/clearing hard restrictions. A warning such as a market-wide OI alert or TM-level PRISM utilization message MUST NOT be converted into a retail-client ban unless an applicable source rule establishes that effect. Hard restrictions MUST NOT be downgraded to warnings.

**R-115 — Admission snapshots are immutable and time-bounded.** Every admission decision MUST preserve the exact gate outcomes, projected portfolio, data source/hash, effective rule/parameter versions, timestamps, policy/adapter versions and invalidation conditions. The decision MUST be revalidated immediately before dispatch if any material input can change.

**R-116 — Gate outcomes are individually inspectable.** The system MUST preserve each applicable gate as PASS, FAIL, UNKNOWN, ADVISORY or NOT_APPLICABLE with its scope, reason and evidence references. A summary ALLOW/DENY/REDUCE_ONLY result MUST NOT erase gate-level results.

**R-117 — Admission, dispatch, acknowledgement and execution are separate evidence events.** The system MUST distinguish risk decision, transport dispatch, broker acknowledgement, exchange acknowledgement, trade execution and account/position reconciliation. A successful admission decision MUST NOT be recorded as a successful order submission or fill.

**R-118 — Hard regulatory restrictions cannot be bypassed by a local override.** Any manual/emergency override MUST be scoped, authenticated, time-bounded and auditable. It MUST NOT override statutory/exchange/clearing hard restrictions, a market-wide ban, missing client collection required upfront, or an unresolved command that could create duplicate exposure. Where an exception is legally/contractually permitted, its governing authority and evidence MUST be explicit.

### Additional deterministic acceptance scenarios

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

## 20. Exchange contract master, freeze limits and broker order validation (2026-11-08)

PX-2026-034 audits NSE contract-master, quantity-freeze, lot/tick/price-range rules and the broker request schemas for Kite, Upstox V3 and DhanHQ v2. See [PX-2026-034 — Exchange contract master, freeze limits and broker order validation](PX-2026-034-exchange-contract-master-freeze-limits-and-broker-order-validation.md).

### Additional normative requirements

**R-119 — Exchange contract master is date-effective and integrity-pinned.** A future adapter MUST identify the exact exchange/segment contract file, trade date, publication/effective date, schema version, file hash, capture time and parser version used for each order-validation decision. Missing, stale, corrupt or mismatched-date contract data MUST produce UNKNOWN, not a fallback to the previous day's row.

**R-120 — Complete derivative identity is required.** A derivative order MUST resolve a stable contract identity including exchange, segment, underlying/security ID, instrument token, trading symbol, contract family, expiry, strike, option type and active/trading status. Symbol-only, token-only or fuzzy matching MUST NOT authorize an order.

**R-121 — Quantity units and market lot are explicitly converted once.** The system MUST keep user lots, exchange units, market lot/multiplier and broker payload quantity as separate typed values. Any conversion MUST identify the effective contract-master version and source unit. The same multiplier MUST NOT be applied twice, and an ambiguous provider quantity unit MUST remain UNKNOWN.

**R-122 — Tick size is contract-specific and exact-decimal.** Each limit/trigger price MUST be validated against the effective contract's tick size using exact decimal arithmetic. Off-tick values MUST be rejected or returned as invalid; the adapter MUST NOT silently round/modify a user's requested price or trigger.

**R-123 — Freeze quantity comes from the effective exchange file.** Freeze quantity MUST be sourced by exact contract/instrument and effective date from the current NSE circular/contract file. Index and individual-security limits MUST remain distinct. A previously observed circular table or hard-coded constant MUST NOT replace the current daily file.

**R-124 — Exchange price/operating range is distinct from broker market protection.** The system MUST validate the effective exchange price/operating range and the broker's market-protection setting as separate controls. A market-protection percentage MUST NOT be treated as permission to submit a price outside the exchange range, and a valid exchange range MUST NOT be treated as satisfying provider market-protection requirements.

**R-125 — Provider order enums are versioned adapter mappings.** Order variety, order type, product, validity, AMO, market-protection, iceberg/auto-slice and other provider-specific fields MUST be mapped by broker/API version. Unknown or unsupported enum/field combinations MUST be rejected/UNKNOWN; the adapter MUST NOT silently coerce them to a different order type, product or validity.

**R-126 — Conditional request fields are validated by order type.** Price, trigger price, disclosed quantity, auction number, TTL, AMO time, product and other conditional fields MUST be present/absent and validated according to the exact provider schema and selected order type/variety. A nonzero trigger price or market-protection field MUST NOT be sent where the provider says it is ignored or unsupported without an explicit reason.

**R-127 — Market session and AMO semantics are provider-specific.** Regular-session, pre-open, auction and after-market order eligibility MUST be resolved against the current exchange session and provider API contract. A client-supplied AMO flag MUST NOT override a provider's documented session inference; AMO acceptance MUST NOT be equated with exchange execution or next-session acceptance.

**R-128 — Above-freeze slicing requires explicit, bounded child construction.** A request exceeding the effective freeze quantity MUST be rejected or sliced only through a documented provider/exchange mechanism explicitly enabled by policy. Child quantities MUST comply with freeze/lot limits, child count limits and API schema. The adapter MUST preserve parent/child identity, requested total, each child result and remaining/rejected quantity.

**R-129 — Child-set completeness is mandatory after sliced response loss.** When a sliced/multi-child response is lost or partial, the adapter MUST reconcile all possible child orders using provider/exchange evidence and retain UNKNOWN until the child set is established. It MUST NOT resubmit the entire parent quantity merely because some child IDs were not returned.

**R-130 — Contract lifecycle invalidates prior validation.** A new expiry, expired contract, strike listing change, corporate-action adjustment, lot/tick/freeze revision, suspension or contract-master update MUST invalidate prior contract/order-validation approval for affected instruments. A cached instrument identity MUST NOT be treated as valid across a known effective contract change.

**R-131 — Exchange and broker rejection semantics are preserved.** A rejected request MUST retain the raw broker/exchange code, message, API version, request fingerprint and all validation inputs. The adapter MUST distinguish local validation failure, broker API rejection, exchange rejection and unknown transport outcome. It MUST NOT retry a rejected order with silently altered quantity, price, product or variety.

**R-132 — Dispatch requires a fresh contract-validation snapshot.** Immediately before dispatch, the adapter MUST verify that the PX-033 admission snapshot, contract-master row, lot/tick/freeze parameters, exchange price range, market session and provider API capability remain current. Any material change MUST invalidate the admission decision and require revalidation.

### Additional deterministic acceptance scenarios

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-221 | Contract master for the target trading date is missing | UNKNOWN; no contract resolution or order admission |
| AT-222 | Only the previous trading day's contract file is available | Mark stale; do not reuse it as current without an explicit source rule |
| AT-223 | Instrument token resolves to a different symbol/expiry/strike from the requested instrument | Reject identity mismatch; no fuzzy substitution |
| AT-224 | Contract is expired, suspended, not yet active or not tradable in the current session | Reject/UNKNOWN with the exact source status |
| AT-225 | User quantity is not a legal multiple of the effective market lot | Reject quantity; do not silently round to a lot multiple |
| AT-226 | Lots are converted to exchange units and adapter applies the multiplier again | Detect double conversion; preserve original and normalized units and reject the request |
| AT-227 | Index-futures tick size changes across the published index-level bands; index options use their separate tick | Validate each exact contract against its own current tick; reject off-tick prices |
| AT-228 | Individual-stock future and option have different applicable tick rules | Use the cash-market tick for stock futures and the current underlying-price option tick rule for stock options |
| AT-229 | Stop-loss trigger price is not aligned to the effective contract tick | Reject; do not silently adjust trigger price |
| AT-230 | Limit price lies outside the effective exchange operating/dynamic price range | Reject on exchange-range validation even when broker market-protection value is valid |
| AT-231 | Option dynamic price range changes for the current day | Use current dated range; do not use yesterday's range or a static percentage |
| AT-232 | Futures order lies outside its published operating range | Reject/UNKNOWN using the effective futures range; do not use option delta range |
| AT-233 | Quantity equals the effective freeze limit exactly | Permit quantity check if all other gates pass; preserve source row and effective date |
| AT-234 | Quantity exceeds the effective index freeze limit by one unit | Reject or use explicitly authorized provider slicing; no single over-freeze child |
| AT-235 | Individual-stock freeze quantity differs from another stock's freeze quantity | Use the target security's own daily contract-file row; no generic stock freeze constant |
| AT-236 | Circular index-freeze table and current daily contract file differ | Retain both sources and resolve by effective hierarchy/current file; UNKNOWN if the discrepancy cannot be reconciled |
| AT-237 | Contract file is truncated, duplicate-keyed, malformed or fails hash/completeness checks | Reject semantic use; mark contract data UNKNOWN |
| AT-238 | Kite MARKET/SL-M order uses automatic market protection | Map -1 to Kite's documented automatic protection and preserve the provider-specific setting |
| AT-239 | Upstox V3 MARKET order sets market protection to zero | Apply the documented API rejection condition; do not treat zero as “unlimited protection” |
| AT-240 | Upstox V3 market protection is outside its documented custom range | Reject invalid provider parameter; do not clamp silently |
| AT-241 | Dhan regular order request is built with an unsupported Kite/Upstox market-protection field | Do not inject an undocumented field; use Dhan's documented schema or return unsupported/UNKNOWN |
| AT-242 | Upstox F&O quantity is entered in lots but API expects units | Convert once using effective market lot and preserve user lots plus payload units; do not use tick size as a quantity multiplier |
| AT-243 | Unsupported broker product/order type/validity enum is supplied | Reject/UNKNOWN; never coerce to the nearest accepted value |
| AT-244 | Upstox request sends is_amo=true during active market session | Apply provider rule that session inference overrides the flag; do not represent request as guaranteed AMO |
| AT-245 | Kite TTL is mapped to Upstox or Dhan DAY/IOC without policy | Reject unsupported mapping; no silent validity downgrade |
| AT-246 | Kite autoslice / Upstox slice / Dhan separate slicing endpoint produce child orders | Preserve provider-specific parent/child identities and exact per-child result; no generic response assumption |
| AT-247 | Generated sliced child count exceeds provider/API maximum | Reject or require a separately authorized strategy; do not emit an oversized or partial silent fallback |
| AT-248 | Market protection is within range but exchange dynamic price/operating range rejects the request | Preserve distinct broker/exchange validation reason; market protection does not override exchange price range |
| AT-249 | Contract master, freeze limit or tick changes after PX-033 admission but before dispatch | Invalidate stale admission snapshot and rerun affected gates |
| AT-250 | Provider returns a new/unknown schema field or rejection code | Preserve raw response and classify UNKNOWN/unsupported; do not silently map or retry with altered fields |

PX-025 now contains **132 normative requirements (R-001–R-132) and 250 proposed acceptance scenarios (AT-001–AT-250)**. These are proposed deterministic scenarios; no parser, broker adapter or test implementation was executed.

### Data limitations

The daily NSE `contract.gz` and `NSE_FO_contract_ddmmyyyy.csv.gz` file for 8 November 2026 was not downloaded or parsed. The June 2026 quantity-freeze circular is a dated source, not a substitute for the current daily file. Upstox's “units in multiples of tick size” quantity wording is dimensionally inconsistent and must not be used as a conversion rule. Dhan slicing response details remain incomplete in the reviewed public order page.

## 21. NSE contract-file ingestion, schema variants and integrity (2026-11-08)

PX-2026-035 audits NSE MII contract-file variants, dated F&O contract CSVs, quantity-freeze/market-lot report chronology and contract Admission Type. See [PX-2026-035 — NSE contract-file ingestion, schema variants and integrity](PX-2026-035-nse-contract-file-ingestion-schema-variants-and-integrity.md).

### Additional normative requirements

**R-133 — Artifact family and variant are explicit.** The loader MUST classify each source artifact by exact family, variant, exchange, segment and distribution channel. NSE-exclusive MII contract files, NSE/BSE-interoperability variants, dated FO contract CSVs, quantity-freeze reports and market-lot reports MUST NOT be treated as interchangeable inputs.

**R-134 — Effective date and publication time are separate.** Every artifact and row MUST preserve publication/dissemination time, capture time and effective date/time independently. The newest download MUST NOT automatically be assumed effective for the current trading session.

**R-135 — Schema profile is pinned to artifact variant.** The parser MUST bind a schema/profile and field map to the exact artifact variant, version, circular and segment. A field offset from `contract.gz` MUST NOT be reused for `NSE_FO_contract_ddmmyyyy.csv.gz` or another MII/report variant without source evidence.

**R-136 — Raw artifact bytes and provenance are immutable.** The system MUST retain the original compressed file bytes, source URL/channel, file size, hash, download time, circular reference, parser version and validation report. Parsed records MUST be traceable to exact source bytes and row/record positions.

**R-137 — Gzip and complete-file validation is mandatory.** An artifact MUST pass container/decompression validation through EOF, encoding, record framing and file completeness checks before parsing. Truncated, corrupt, partial or encoding-invalid files MUST be rejected and MUST NOT be promoted as a partial current contract master.

**R-138 — Contract identity keys are unique within their effective scope.** The loader MUST define and validate the unique contract key for the artifact's exchange/segment/venue/date, including underlying/security identity, expiry, instrument family, strike, option type and applicable series fields. Duplicate keys, ambiguous aliases or collisions MUST fail validation rather than select an arbitrary row.

**R-139 — Multiple contract-file variants remain separately scoped.** NSE-exclusive and NSE/BSE-interoperability MII contract variants MUST retain their own file identity and schema profile. The order validator MUST select the correct variant for the requested venue and member capability, not union all rows into an unqualified universe.

**R-140 — Admission Type is parsed by variant-specific mapping.** The Admission Type field MUST use the field number/code mapping for the exact file variant and circular. Unknown codes, shifted fields or a venue mismatch MUST return UNKNOWN/unsupported and block dispatch; the loader MUST NOT reuse the field 13 mapping for the field 30 file or vice versa.

**R-141 — Lot size, quantity unit and freeze quantity remain distinct.** The loader MUST store market lot/multiplier, raw quantity unit, broker payload unit and quantity-freeze value separately, each with source/version/effective date. A separate lot/freeze report MUST only be used when the applicable circular/report schedule establishes its coverage and precedence.

**R-142 — Separate quantity-freeze and lot report lifecycle is date-versioned.** The loader MUST preserve the circular history for `Qtyfreeze.csv` and `fo_mktlots.csv`, including discontinuation/reintroduction/effective date. Presence or absence of a standalone report MUST NOT be interpreted using an outdated circular; it MUST be resolved against the current report catalogue and contract-file instructions.

**R-143 — Contract snapshots are promoted atomically.** A candidate contract-data snapshot MUST remain invisible to order admission until all required artifacts and validations for the target session/effective date have passed. No partial current file may be combined with rows from a previous effective-date snapshot to create a green/complete result.

**R-144 — Related artifact conflicts fail closed.** A conflict between the contract master, date-specific freeze/lot report, corporate-action adjustment or circular-announced limit MUST be resolved against an explicit effective-source hierarchy. If unresolved, affected contract fields and order-admission gates MUST remain UNKNOWN; no silent max/min/newest-file fallback is allowed.

**R-145 — Expiry, status and session coverage are complete.** Every candidate contract row MUST be checked against the applicable expiry, trading status, suspension/listing/admission and session calendar. A stale contract row remaining in an old file MUST NOT make an expired or suspended instrument tradable.

**R-146 — Venue admission and alternative trading route are enforced.** A contract's Admission Type and applicable circular MUST be checked against the requested exchange/venue and member/broker route. BSE-exclusive or otherwise restricted contracts MUST NOT be submitted through a disallowed venue; unsupported alternative-trading-venue handling MUST return UNKNOWN/unsupported.

**R-147 — Promotion and invalidation are auditable.** Each promoted or rejected snapshot MUST retain source file hashes, circular/schema versions, exact validation results, rejected rows/reasons, promotion actor/process and effective interval. A later correction, circular or contract change MUST invalidate the affected snapshot/approval and trigger re-ingestion before order admission.

### Additional deterministic acceptance scenarios

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-251 | Loader receives an NSE-exclusive MII contract file | Classify the exact file variant and apply its own schema profile |
| AT-252 | Loader receives the NSE/BSE-interoperability contract-file variant | Keep it separate from NSE-exclusive file; do not union variants without route rules |
| AT-253 | Dated `NSE_FO_contract_ddmmyyyy.csv.gz` is received with a schema profile for another file | Reject schema/variant mismatch; do not parse with wrong field map |
| AT-254 | Contract.gz Admission Type field is at field 13 | Parse using the contract.gz mapping and preserve raw value/source position |
| AT-255 | Dated FO CSV Admission Type field is at field 30 | Parse using that file's mapping; do not reuse field 13 offset |
| AT-256 | Admission Type contains an unknown value or field shifts unexpectedly | Reject/UNKNOWN; do not infer NSE/BSE venue from symbol alone |
| AT-257 | BSE-exclusive contract is requested through a venue/route not permitted by its Admission Type | Block order validation and retain the exact admission/routing reason |
| AT-258 | BSE-exclusive contract requires an alternative trading venue that the adapter cannot select | UNKNOWN/unsupported; no fallback to the default exchange route |
| AT-259 | Contract file contains two rows with same effective unique contract key but differing lot/expiry/status | Reject duplicate-key conflict; do not choose first/last row |
| AT-260 | Contract file is for a future effective date but is published today | Keep it staged for its future effective date; do not apply early |
| AT-261 | Contract file was published earlier but is downloaded after the effective date begins | Preserve publication/capture/effective times; verify whether the file is still authoritative for the session |
| AT-262 | Gzip stream is truncated before EOF | Reject artifact; do not promote parsed prefix rows |
| AT-263 | File hash changes between download and staged parse | Integrity failure; quarantine artifact and reacquire |
| AT-264 | One required segment/variant file is missing from a multi-file contract set | Candidate snapshot incomplete; no atomic promotion |
| AT-265 | A row has blank or malformed underlying/security/expiry/strike/option-type identity | Reject row or whole snapshot according to the pinned schema completeness policy; no fuzzy identity |
| AT-266 | Expired contract row is present alongside active contract rows | Preserve historical row for audit but mark expired/non-tradable for current session |
| AT-267 | Current contract file is partial while previous-day file is complete | Do not merge them into one current snapshot; return UNKNOWN for affected current contracts |
| AT-268 | Standalone `Qtyfreeze.csv` is absent after a circular said it was discontinued | Resolve the current circular/file hierarchy; absence alone is not a missing-data failure if the MII contract has the complete required field |
| AT-269 | Standalone `Qtyfreeze.csv` is present under a later report schedule | Apply only if the applicable circular says it is current and authoritative for the target decision |
| AT-270 | `fo_mktlots.csv` and contract-file lot values differ | Keep both observations and resolve using effective source/variant instructions; UNKNOWN if no hierarchy |
| AT-271 | 2026 circular changes index freeze quantity while a cached file retains prior quantity | Invalidate cache and require the effective dated contract file; no hard-coded/cached approval |
| AT-272 | Index freeze value in the daily file differs from the circular summary | Preserve both and resolve whether the file reflects later effective data; fail closed if the discrepancy is unexplained |
| AT-273 | Same instrument appears in NSE-exclusive and NSE/BSE variants with different Admission Type/route | Preserve variant scope and validate against requested venue; no automatic cross-variant alias |
| AT-274 | Parser is upgraded but source bytes/schema version are unchanged | Retain old parser provenance and compare/revalidate new output before promoting the new parser profile |
| AT-275 | Schema circular shifts a field position but parser continues with previous mapping | Reject schema mismatch; do not silently read the wrong field into Admission Type/lot/freeze |
| AT-276 | Contract file uses unknown enum for market status or instrument family | Preserve raw code and return UNKNOWN/unsupported; no default active/tradable mapping |
| AT-277 | Contract row exists but selected broker/provider does not support the required exchange/venue/product | Exchange contract identity PASS is not enough; provider capability gate rejects/UNKNOWN |
| AT-278 | Contract and freeze/lot artifacts are individually valid but refer to different effective sessions | Do not combine; stage remains incomplete/UNKNOWN |
| AT-279 | All required artifacts pass schema, hash, identity, status and effective-date validation | Promote one immutable atomic snapshot with complete provenance |
| AT-280 | A later circular/file correction changes a promoted lot, tick, freeze or Admission Type | Invalidate affected instrument/admission snapshots and require re-ingestion/revalidation before dispatch |

PX-025 now contains **147 normative requirements (R-001–R-147) and 280 proposed acceptance scenarios (AT-001–AT-280)**. These are proposed tests only; no daily 8 November 2026 file or parser was executed.

### Source and schema limitations

- The actual daily 8 November 2026 MII/FO contract files were not downloaded or parsed.
- The complete current schema and code lists for all variants are not closed by the documents reviewed.
- The standalone `Qtyfreeze.csv`/`fo_mktlots.csv` lifecycle includes discontinuation and later reintroduction notices; the current report catalogue and route-specific precedence must be verified at integration time.
- Field-level parser implementation remains deferred; no inferred mapping is to be promoted as authoritative.

## 22. Cross-provider instrument identity and effective-dated contract mapping (2026-11-08)

PX-2026-036 distinguishes canonical exchange contract identity from provider aliases for Kite, Upstox and Dhan. Official provider master documentation was reviewed; daily files were not downloaded. See [PX-2026-036 — Cross-provider instrument identity and effective-dated contract mapping](PX-2026-036-cross-provider-instrument-identity-and-effective-dated-contract-mapping.md).

### Additional normative requirements

**R-148 — Canonical instrument identity is independent of provider aliases.** The system MUST assign an internal immutable canonical identity to each underlying/security and listed contract. Broker tokens, provider keys, symbols and exchange-specific IDs MUST be stored as provider-scoped aliases, not used as a universal canonical ID.

**R-149 — Provider aliases are namespaced by provider, API version and segment.** Every provider alias MUST retain provider identity, API/schema version, exchange/segment scope and raw provider identifier. Numeric equality or string equality across providers MUST NOT be treated as evidence that two aliases identify the same contract.

**R-150 — Alias validity is effective-dated.** Every alias MUST retain source publication/observation time and its valid-from/valid-to interval. Retired, expired or superseded aliases MUST remain available for historical reconciliation but MUST NOT authorize current order submission.

**R-151 — Underlying identity uses authoritative security/index mapping.** Equity underlyings SHOULD be mapped through ISIN where supplied and verified. Indices MUST use an official exchange/index identity. If a stable underlying key is missing or ambiguous, the mapping MUST remain UNKNOWN; display company/index name alone is insufficient.

**R-152 — Derivative identity requires complete contract terms.** A derivative canonical identity MUST include exchange, segment, venue/admission type, underlying identity, future/option family, expiry, strike, option type and applicable series/type fields. A match on symbol/root/expiry alone MUST NOT authorize a contract.

**R-153 — Strike, expiry and contract terms use exact normalization.** Strike and price-like contract terms MUST use exact-decimal normalization. Expiry must be interpreted using the exchange trading date/calendar without timezone drift. Raw source values and normalized values MUST both be retained with parser version.

**R-154 — Alias mapping requires exact, unique source-supported resolution.** A provider alias MAY be linked to a canonical contract only when the exact required identity attributes agree and exactly one candidate is valid for the effective interval. Fuzzy symbol/name/token matching MUST NOT produce an orderable alias.

**R-155 — Contract attributes are cross-checked after identity match.** Even when identity keys match, lot/multiplier, quantity unit, tick, freeze, settlement mode, expiry/status and venue attributes MUST be compared. Any unexplained conflict MUST result in ATTRIBUTE_CONFLICT/UNKNOWN and block order admission.

**R-156 — Provider instrument masters are separately versioned inputs.** Kite, Upstox and Dhan instrument masters MUST be ingested and versioned independently, with source URL/channel, capture/effective time, hash, schema and parser version. One provider's master MUST NOT be substituted for another provider's alias or capabilities.

**R-157 — Venue and Admission Type are part of the canonical route.** A contract's exchange/venue admission type MUST be part of mapping and order-route validation. An otherwise identical underlying/expiry/strike on a different venue or admission path MUST remain a distinct route and MUST NOT be silently substituted.

**R-158 — Corporate-action contract transitions are linked, not overwritten.** Changes to strike, lot, multiplier, expiry, quantity or contract terms from a corporate action MUST create an effective-dated successor/adjusted contract relationship with source evidence. The predecessor identity and all historical provider aliases MUST remain immutable for historical reconciliation.

**R-159 — Expired/suspended contracts remain historical but non-tradable.** Expired, suspended, delisted or retired contract aliases MUST remain resolvable for old orders/trades but MUST fail current order-admission validity. Presence in a historical source file cannot make the contract currently tradable.

**R-160 — Alias collisions and overlapping validity are quarantined.** If one provider alias maps to more than one canonical contract over an overlapping validity interval, or if a provider alias changes identity without a source-supported effective transition, the mapping MUST be quarantined as AMBIGUOUS/CONFLICT. No arbitrary first/last row selection is permitted.

**R-161 — Crosswalk snapshots are atomic and reproducible.** A promoted provider-to-canonical crosswalk MUST retain the exact exchange and provider source files, hashes, schema/parser/mapping-policy versions, row references, effective times, validation report and decision trace. A partial provider master set MUST NOT be combined with a previous crosswalk to claim current complete mapping.

**R-162 — Unknown identity blocks order submission.** If the underlying, contract, venue, provider alias, lot/unit or effective-date mapping is missing, stale or contradictory, the order-admission gate MUST return UNKNOWN/blocked. It MUST NOT guess a security ID, reuse a stale token or fall back to a similar symbol.

### Additional deterministic acceptance scenarios

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-281 | Same listed contract appears in NSE, Kite, Upstox and Dhan masters with different provider identifiers | Map each exact source alias to one canonical contract; preserve identifiers separately |
| AT-282 | Numeric Kite instrument token equals a numeric Dhan security ID by coincidence | Keep provider namespaces separate; no identity match from numeric equality |
| AT-283 | Same trading symbol exists for current and next expiry | Resolve using full expiry/contract terms; no symbol-only selection |
| AT-284 | Same underlying/expiry has multiple option strikes | Resolve exact decimal strike; reject ambiguous root/expiry match |
| AT-285 | Same strike/expiry has CE and PE contracts | Resolve option type separately; no call/put alias collision |
| AT-286 | Equity underlying has same display symbol on two venues but a verified same ISIN | Preserve venue route separately while linking the underlying security identity |
| AT-287 | Underlying display symbol changed but ISIN/security identity remains the same | Preserve historical symbol aliases and map only through the authoritative underlying crosswalk |
| AT-288 | Index underlyings have no ISIN | Use official index identity; do not invent an ISIN or use display name alone |
| AT-289 | Provider master contains a contract absent from the current exchange contract universe | Quarantine as unmatched/unsupported; do not auto-create an exchange-listed canonical contract |
| AT-290 | Exchange master contains a valid contract absent from one provider master | Preserve canonical contract with no alias for that provider; do not reuse another provider's token |
| AT-291 | Provider aliases match contract terms but lot size differs | ATTRIBUTE_CONFLICT/UNKNOWN; no orderable mapping |
| AT-292 | Provider aliases match but tick size/freeze value differs | Preserve both observations and resolve source/effective scope; no silent selection |
| AT-293 | Broker master has quantity in lots while exchange file has quantity units | Preserve raw units and apply only a verified one-time conversion; otherwise UNKNOWN |
| AT-294 | Option strike is parsed as binary float and produces a precision mismatch | Reject unsafe normalization; use exact decimal source representation |
| AT-295 | Expiry date from provider uses a timestamp that shifts to previous date under local timezone conversion | Preserve exchange date semantics; reject timezone-drifted contract mapping |
| AT-296 | Same provider alias appears mapped to two contracts with overlapping validity intervals | Quarantine alias as AMBIGUOUS; block dispatch |
| AT-297 | Provider alias changes on a new daily master with a documented effective transition | Retire old alias for new orders but retain historical mapping and link to current alias |
| AT-298 | Old expired alias is used in a current order request | Reject current tradability while keeping it available for historical trade reconciliation |
| AT-299 | Corporate action changes contract strike and lot size | Create linked predecessor/successor canonical contracts with effective date; do not overwrite old terms |
| AT-300 | Merger forces closeout and a successor security is listed | Preserve forced-closeout event and new underlying identity; do not alias old derivative contract to new one |
| AT-301 | NSE and BSE rows share underlying/expiry/strike but have different Admission Type | Keep venue-specific canonical routes and reject unsupported route substitution |
| AT-302 | BSE-exclusive provider alias is offered to an adapter/session configured only for NSE | Reject venue mismatch despite matching underlying and contract terms |
| AT-303 | Provider API version changes instrument alias schema | Create a new source schema profile; do not parse with previous API/master mapping |
| AT-304 | Provider master file is stale while exchange contract master is current | Alias freshness UNKNOWN; no new order even if prior crosswalk once matched |
| AT-305 | Symbol/name fuzzy match finds a single apparent candidate but ISIN/security ID is missing | Keep UNKNOWN; fuzzy search result cannot authorize mapping |
| AT-306 | Provider master has duplicate identical key rows with differing status/effective time | Preserve both rows and resolve by explicit source effective rules; otherwise quarantine |
| AT-307 | Provider instrument ID is reused or collides in a different segment/date scope | Scope alias by provider, API version, segment and effective interval; never global lookup |
| AT-308 | Lot/multiplier changes after a contract adjustment | Invalidate old alias/contract approval and create a date-effective adjusted contract mapping |
| AT-309 | One provider alias maps to two canonical contracts because option type was omitted | Reject ambiguous mapping; require option type in the complete contract identity |
| AT-310 | A crosswalk snapshot contains missing provider master, duplicate key or unresolved venue mapping | Do not promote partial crosswalk; retain UNKNOWN/quarantine report and block order admission |

PX-025 now contains **162 normative requirements (R-001–R-162) and 310 proposed acceptance scenarios (AT-001–AT-310)**. These are proposed tests only; no provider master files, live API calls, parser or crosswalk implementation were executed.

### Provider-master source clarifications

- Kite's daily CSV master includes token/contract attributes but its `last_price` is not real-time; its docs warn instrument tokens can be reused after derivative expiry.
- Upstox recommends JSON, marks CSV as deprecated, identifies `instrument_key` as unique for each instrument, warns exchange_token may be reused, and provides separate BOD/suspended/MTF/MIS files.
- Dhan publishes compact/detailed/segmentwise master surfaces; the detailed file includes underlying security ID and derivative attributes. A global all-time uniqueness guarantee for raw Dhan securityId was not established.
