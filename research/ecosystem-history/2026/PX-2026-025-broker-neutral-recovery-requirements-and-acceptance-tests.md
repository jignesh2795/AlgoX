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

PX-029 adds R-049 through R-061 and AT-076 through AT-100. The consolidated requirements baseline now contains **61 normative requirements (R-001–R-061) and 100 proposed acceptance scenarios (AT-001–AT-100)**. The new expiry/settlement scenarios are specified only; no test was executed and no settlement code was implemented.
