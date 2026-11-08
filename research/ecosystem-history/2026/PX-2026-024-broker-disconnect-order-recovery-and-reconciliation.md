# PX-2026-024 — Broker disconnect, ambiguous order outcomes and reconciliation

**Research date:** 2026-11-08  
**Status:** official-documentation comparison completed; provider semantics and recovery guarantees remain partially unresolved  
**AlgoX area:** Indian-market broker adapters / order lifecycle / execution recovery  
**Scope:** Zerodha Kite Connect, Upstox Developer API and DhanHQ API v2  
**Mode:** research and documentation only; no broker connection, API request, order, code implementation or paid service

## Executive finding

A broker API response, an OMS order identifier, an exchange order identifier, an order-state update and an executed trade are different evidence objects. A network timeout after a submission may have left the client without an acknowledgement even though the broker accepted or routed the order. It must therefore be represented as **SUBMISSION_UNKNOWN**, not silently converted to rejected/failed and not automatically resubmitted.

The three reviewed brokers provide useful recovery identifiers and read APIs, but they expose different mechanisms:

- **Zerodha Kite:** broker order ID, optional identifying tag, order history/order book, daily trade book and WebSocket order postbacks. An exchange order ID may be null when the order did not reach the exchange.
- **Upstox:** broker order ID, tag-based history lookup, per-order and daily trade queries, and an account-wide portfolio order-update stream. Tag lookup can return all orders associated with that tag.
- **DhanHQ:** user/partner-generated `correlationId`, a dedicated lookup endpoint for the case where the order ID was missed, order/trade books and live WebSocket updates.

The reviewed public documentation does **not** establish a common client-supplied idempotency key, a safe retry contract for repeated submissions, or a durable event-stream replay cursor across all three providers. Correlation/tag identifiers are recovery aids; they must not be treated as proof of exactly-once submission.

**Research conclusion:** a broker-neutral recovery design needs a durable local intent/attempt ledger, an explicit unknown-outcome state, read-side reconciliation across both orders and trades, broker-specific identity mapping, and fail-closed handling when the broker's state cannot be established.

## 1. Evidence model and terminology

Keep these identities and facts separate:

1. **Local intent ID:** AlgoX's durable identifier for the logical order instruction.
2. **Submission attempt ID:** a local identifier for one outbound transport attempt. It is not a broker idempotency key.
3. **Broker correlation/tag:** an optional value sent to the broker to associate or find an order.
4. **Broker order ID:** the broker/OMS identifier returned by the broker.
5. **Exchange order ID:** the exchange-generated identifier, which may be absent while an order is still in a broker-side or validation state.
6. **Trade ID:** the identity of an individual execution/fill record.
7. **Order state:** the current lifecycle state of the order, which can change after submission and can include interim states.
8. **Transport evidence:** whether the client knows a request was not sent, may have been sent, or received a response. This is not the same as the order's broker state.

A successful API call does not necessarily mean an order is executed. Zerodha explicitly says that API placement registers an order with its OMS and does not guarantee exchange receipt; it recommends checking the order book or individual order history for the true state. Its response model distinguishes broker `order_id` from `exchange_order_id`, and the latter can be null.  
Source: https://kite.trade/docs/connect/v3/orders/

## 2. Broker capability comparison

| Capability | Zerodha Kite Connect | Upstox Developer API | DhanHQ API v2 |
|---|---|---|---|
| Broker order ID | Returned after API placement is accepted by the OMS | Returned on successful placement | Returned as `orderId` |
| Client correlation field | Optional `tag`, alphanumeric, max 20 chars | Optional `tag`; order-history lookup accepts tag | User/partner-generated `correlationId`, max 30 chars; allowed characters are alphanumeric, space, underscore and hyphen |
| Lookup when broker ID is known | `GET /orders/{order_id}` and order history | `GET /order/details` and `GET /order/history` | `GET /orders/{order-id}` |
| Lookup when broker ID is missing | Daily order book plus tag-based inspection where available; no dedicated tag endpoint was established in this review | `GET /order/history?tag=...`; returns all matching orders | `GET /orders/external/{correlation-id}`; documentation explicitly describes this for a missed order ID |
| All orders | `GET /orders`, all orders for the day | Order book endpoint; documented order history/details are one-trading-day resources | `GET /orders`, all orders for the day |
| Trade reconciliation | `GET /trades` and `GET /orders/{order_id}/trades` | Daily trades and per-order trades; each partial execution is represented as a trade | Trade book and trades for an order |
| Real-time updates | WebSocket streams order postbacks; a separate postback webhook is available | Portfolio WebSocket stream; webhook option | Live Order Update WebSocket |
| Documented retention qualification | Order book/history is transient and lives for one day | Order history/details remain for one trading day and are removed at session end | The order-book endpoint is described as a day-level book; a longer retention guarantee was not established here |
| Operational constraint found | API rate limits; order modifications capped at 25 per order | Current rate limits vary by algo registration class | Order placement/modification/cancellation requires static-IP whitelisting; order API limits and a 25-modifications-per-order cap are documented |

### 2.1 Zerodha Kite

- `POST /orders/:variety` returns a broker `order_id`; the documentation is explicit that this represents OMS registration and is not proof of exchange receipt or execution.
- `GET /orders` returns the day's orders; `GET /orders/:order_id` retrieves one order's history; `GET /trades` and `GET /orders/:order_id/trades` expose execution records.
- The response separates `order_id` and `exchange_order_id`. The exchange ID and exchange timestamps can be null for orders that have not reached the exchange.
- A client may attach an optional alphanumeric `tag` of up to 20 characters to identify an order. This is a search/correlation aid, not a documented idempotency guarantee.
- The response field `guid` is described as an “Unusable request id to avoid order duplication”; it is not documented as a client-supplied idempotency key that AlgoX can safely reuse.
- Order states include interim stages such as `PUT ORDER REQ RECEIVED`, `VALIDATION PENDING`, `OPEN PENDING`, `MODIFY PENDING` and `CANCEL PENDING`. Do not collapse these into terminal states.
- The order book/history is transient and lives for one day.
- The WebSocket sends order postback messages. Individual developers are directed to WebSocket postbacks for updates on a user's orders across platforms. The HTTP postback webhook is aimed at public/platform apps and only notifies orders placed using that app's API key. Its checksum is SHA-256 over `order_id + order_timestamp + api_secret`; consumers must validate it.

Sources:
- https://kite.trade/docs/connect/v3/orders/
- https://kite.trade/docs/connect/v3/websocket/
- https://kite.trade/docs/connect/v3/postbacks/
- https://kite.trade/docs/connect/v3/exceptions/

### 2.2 Upstox

- Order history accepts either `order_id` or `tag`. When only a tag is supplied, the API returns histories for **all associated orders** matching it. This is useful for detecting multiple matches, but it is not a server-side deduplication promise.
- The documented order history and order-details resources are one-trading-day records and are removed at the end of the session.
- The daily trade endpoint returns separate records for partial executions; the response includes a `trade_id`, `order_id` and `exchange_order_id`. A per-order trade endpoint is also available.
- The Portfolio Stream Feed sends order updates once its WebSocket connection is established. Its documentation says updates include orders placed on other Upstox platforms, not only orders placed through the API.
- The SDK exposes auto-reconnect controls. This is a transport reconnection feature; the reviewed documentation does not describe an event cursor or guarantee that missed updates are replayed after a disconnection.
- The webhook instructions require an endpoint that does not require authentication and that returns a 2XX response. The reviewed webhook page does not establish a signed-event scheme comparable to Kite's documented checksum; do not treat the webhook alone as a durable, independently verified order ledger.

Sources:
- https://upstox.com/developer/api-documentation/get-order-history/
- https://upstox.com/developer/api-documentation/get-order-details/
- https://upstox.com/developer/api-documentation/get-trade-history/
- https://upstox.com/developer/api-documentation/get-trades-by-order/
- https://upstox.com/developer/api-documentation/get-portfolio-stream-feed/
- https://upstox.com/developer/api-documentation/webhook/
- https://upstox.com/developer/api-documentation/streamer-function/

### 2.3 DhanHQ

- Order placement returns a Dhan `orderId` and an `orderStatus`; the order model also carries `correlationId`.
- Dhan describes `correlationId` as a user/partner-generated tracking identifier, with a maximum length of 30 characters.
- The dedicated `GET /orders/external/{correlation-id}` endpoint is specifically documented for the case where the user has missed the order ID due to an unforeseen reason. This is the clearest direct lost-acknowledgement recovery endpoint in this comparison.
- The order response exposes `createTime`, `updateTime`, `exchangeTime`, `remainingQuantity`, `filledQty` and average traded price. The live update message separately exposes Dhan's order number and exchange order number.
- Status values include `TRANSIT`, `PENDING`, `PART_TRADED`, `TRADED`, `REJECTED`, `CANCELLED` and `EXPIRED`.
- Dhan provides a live order-update WebSocket. Its documentation identifies `CorrelationId` in the update payload.
- Placement, modification and cancellation require static-IP whitelisting. The v2 introduction documents a 10-per-second order-API rate limit, with additional minute/hour/day limits, and a maximum of 25 modifications per order.

Sources:
- https://dhanhq.co/docs/v2/orders/
- https://dhanhq.co/docs/v2/order-update/
- https://dhanhq.co/docs/v2/
- https://dhanhq.co/docs/v2/releases/

## 3. Correlation is not idempotency

The current documentation supports these narrower statements:

- Kite's `tag` identifies an order. The documented response `guid` is labelled unusable, not a caller-provided retry token.
- Upstox can find one or more order histories by `tag`; its API explicitly returns all associated orders matching a tag.
- Dhan's `correlationId` is a user/partner-generated tracking value and supports lookup when the order ID is missing.

The reviewed pages do not specify that repeating a placement with the same tag/correlation ID will return the original order, reject a duplicate, or prevent a second order from being created. That is an **unverified provider contract**, not something AlgoX may infer from the existence of the field.

Therefore:
- Generate and persist a unique local intent ID before transmission.
- Populate the broker correlation field where supported, subject to the provider's character/length rules.
- Never blindly resubmit a placement just because the HTTP response was lost.
- Do not reuse a broker tag/correlation ID as an assumed idempotency token unless a separate provider contract explicitly establishes the behavior.
- Keep every submission attempt and every discovered broker order linked to the original local intent. If multiple broker orders match one intent, record a conflict/duplicate exposure; do not discard one as a harmless retry.

## 4. Ambiguous command outcomes

The uncertainty applies to order placement, modification and cancellation.

### Placement

If the request may have left the process but the response is missing, times out, or reports an intermediary/backend failure, the broker-side result is unknown. Zerodha documents `502` for OMS communication failure, `503` for service unavailable and `504` for gateway timeout. Those status codes describe the communication path; they do not, by themselves, prove that the broker created no order.

**Required treatment:** `SUBMISSION_UNKNOWN` / `RECONCILIATION_REQUIRED`.

### Modification

A timed-out modify request may have changed price, quantity, validity or order type even if the client did not receive confirmation. Preserve the last known order version and reconcile the current broker order history before issuing another modification.

### Cancellation

A timed-out cancellation may still be pending, may have been rejected, or may race with a fill. A local timeout is not a cancellation. Reconcile both the order's current remaining/filled/cancelled quantities and its trade records before any replacement order is considered.

### Known rejection vs unknown outcome

An explicit broker rejection with a documented terminal status and matching order evidence can be treated as a rejection. A socket reset, timeout, generic 5xx, connection loss or incomplete response after dispatch began cannot be promoted to rejection without additional evidence.

For conservative transport handling, once the client cannot prove that no request bytes were sent, retain the unknown outcome. A single read that returns no matching order also does not prove non-acceptance unless the provider documents the relevant query's completeness and read-after-write behavior.

## 5. Candidate broker-neutral recovery protocol

This is a research proposal, not an approved implementation design.

1. **Persist intent before transmission.** Store the local intent ID, account/broker identity, instrument/contract identity, side, product, order type, quantity, limit/trigger values, validity, immutable request fingerprint, creation time and broker correlation value. Do not persist credentials in the order record.
2. **Record dispatch before the network call.** Persist the attempt ID and `SUBMISSION_IN_FLIGHT` before sending. Record whether the transport can prove that no bytes were sent; otherwise treat dispatch as potentially delivered.
3. **Separate acknowledgement from execution.** A returned broker order ID means the broker has identified an order; it does not mean the order is filled. Exchange order ID may appear later or remain absent in interim broker-side states.
4. **On ambiguous response, stop resubmission.** Mark the intent `SUBMISSION_UNKNOWN`, retain the correlation value and block any automated replacement that could duplicate or exceed the intended exposure.
5. **Query by broker correlation first.** Use Dhan's correlation endpoint, Upstox tag history, or Kite's daily order book/tag evidence as available. Once the broker order ID is recovered, query its current history/details.
6. **Fetch the complete relevant order view.** Retrieve the broker's day order book and individual histories for all candidate matches. Match using account, segment, instrument/security ID, side, product, order type, quantity, price/trigger, validity, timestamps and correlation/tag. A tag match alone is insufficient if multiple records or external/manual orders exist.
7. **Reconcile trades independently.** Fetch the daily trade book and per-order trade list where available. Deduplicate by a broker-scoped trade identity (at minimum broker, account, trading day and provider trade ID); do not infer fills solely from order status or average price. Sum unique executed quantities and compare them with broker order filled quantities.
8. **Preserve all evidence.** Store raw broker responses and inbound update payloads with source, receive time, provider event/update time, request/response metadata and content hash. Preserve conflicting observations; do not overwrite them with last-arrival-wins logic.
9. **Require convergence or remain unknown.** Repeat read-side reconciliation using bounded, rate-aware backoff. If no candidate is found, multiple candidates conflict, order/trade totals disagree, or provider status remains transitional, retain `UNKNOWN` and escalate. Absence from one query is not proof of absence.
10. **Apply the same rule to modify/cancel.** Reconcile the order history and tradebook after uncertain mutation responses; a cancellation request in a pending state is not a confirmed cancellation.
11. **Reconcile before resuming after reconnect.** Record the disconnect interval, re-establish the update stream, durably buffer new events, fetch order-book and trade-book snapshots, re-fetch specific unresolved orders and their trades, then compare the observations. The reviewed provider docs do not define a common stream sequence cursor or missed-event replay facility, so a reconnect alone cannot close the gap.
12. **Persist before the broker's retention window closes.** Kite and Upstox explicitly document one-day order history/book retention. Persist daily order and trade evidence locally before the session boundary; do not make next-day reconstruction depend only on broker read APIs.

### Candidate state vocabulary

Keep transport/intent state separate from the broker's raw order status. Candidate local states include:

- `INTENT_RECORDED`
- `SUBMISSION_IN_FLIGHT`
- `SUBMISSION_UNKNOWN`
- `BROKER_ORDER_DISCOVERED`
- `RECONCILIATION_REQUIRED`
- `RECONCILED_OPEN`
- `RECONCILED_PARTIAL`
- `RECONCILED_FILLED`
- `RECONCILED_CANCELLED`
- `RECONCILED_REJECTED`
- `RECONCILED_EXPIRED`
- `CONFLICT_MULTIPLE_MATCHES`

These are descriptive research labels only. Do not turn them into code enums until the domain model and provider contracts have been reviewed.

## 6. Reconnection and event-stream semantics

The providers expose useful live update channels:

- Kite WebSocket includes order postbacks. Its postback webhook has a provider-defined checksum. The WebSocket is the recommended path for individual developers who need updates for orders placed through other Kite platforms as well.
- Upstox Portfolio Stream Feed emits order updates after the WebSocket connection is established and includes orders placed through other Upstox platforms. The SDK supports auto-reconnect parameters, but no event cursor or guaranteed missed-message replay was found in the reviewed documentation.
- Dhan Live Order Update provides account order updates and carries order/exchange identifiers, status, timestamps and `CorrelationId`.

None of the reviewed pages establishes a common durable sequence number, replay cursor, or exactly-once delivery promise for order updates. Therefore the event stream should be treated as a low-latency observation channel, not as the sole source of durable truth.

A future adapter should:
- persist the stream interruption interval and every received raw update;
- tolerate duplicates and out-of-order arrival;
- never assume local receive order equals broker/exchange event order;
- use broker timestamps as evidence, not as a substitute for a missing sequence number;
- reconcile current order state and trades through REST after reconnect;
- leave unresolved conflicts in `UNKNOWN` rather than inventing an order sequence.

## 7. Rate limits and operational conditions

Current official pages expose materially different limits. Treat these figures as a documentation snapshot dated 2026-11-08 and re-check before any future integration:

- **Kite:** 10 requests/second per order placement and other endpoints; 400 orders/minute, 10 orders/second and 5,000 orders/day; maximum 25 modifications per order.
- **Upstox:** regular algos are limited to 10 combined placement/modify/cancel requests per second, 500/minute and 2,000 per 30 minutes; registered algos have a higher per-second class. Other standard APIs have separate limits.
- **DhanHQ v2:** order APIs are limited to 10/second, 250/minute, 1,000/hour and 7,000/day; order modification is capped at 25 per order. Placement/modification/cancellation require static-IP whitelisting.

A recovery loop must not poll aggressively or repeatedly retry into rate limits. Use provider-specific budgets, bounded backoff, jitter where appropriate, and explicit rate-limit responses. Exhausted retry budgets do not turn an unknown order into a failed order.

Sources:
- https://kite.trade/docs/connect/v3/exceptions/
- https://upstox.com/developer/api-documentation/rate-limiting/
- https://dhanhq.co/docs/v2/

## 8. Required failure and reconciliation test matrix

Before any implementation can be accepted, a deterministic fake-broker suite should cover at least:

1. Request never leaves the client process; local transport evidence proves non-dispatch.
2. Request reaches broker; broker accepts it; response is lost before the client receives the order ID.
3. Request reaches broker OMS but order never receives an exchange order ID.
4. Explicit broker rejection response vs generic network/5xx failure.
5. Partial fill occurs before the client disconnects; later fills arrive after reconnect.
6. Full fill occurs while the update stream is disconnected.
7. Cancel request times out, then the order fills before the next reconciliation.
8. Modify request times out and the broker retains either the old or new parameters.
9. Update events arrive duplicated, out of order, or after a REST snapshot.
10. Correlation/tag lookup returns no match, one match, or multiple matches.
11. Broker daily orderbook and tradebook disagree temporarily or expose different update times.
12. Auto-sliced or multi-leg submissions produce multiple broker order IDs for one local intent.
13. Orders submitted from broker mobile/web/manual channels appear in the account-wide update stream.
14. Authentication expires or static-IP access is unavailable during recovery.
15. Rate-limit responses interrupt reconciliation.
16. Session rollover removes transient broker history; local evidence remains sufficient to audit the trading day.

Each test must assert that no duplicate order is generated automatically from an unknown outcome, partial fills are counted exactly once, and any unresolved state remains fail-closed.

## 9. Open questions and non-claims

The official documentation reviewed does not settle:

- Whether any of the three providers performs server-side duplicate suppression for repeated requests carrying the same tag/correlation ID.
- Whether Dhan enforces correlation-ID uniqueness, how collisions are resolved, or how long the correlation lookup remains available.
- Whether Upstox tag uniqueness is enforced at placement or merely used as a query attribute.
- Whether broker order/trade read APIs are read-after-write consistent or provide atomic snapshots.
- Whether update delivery is at-most-once, at-least-once or best-effort, and whether a provider can replay an interruption window.
- Whether provider history remains accessible beyond the documented one-day windows or how exact session rollover affects every endpoint.
- Whether timestamps from REST responses and live streams have sufficient precision/ordering guarantees for every race.
- Whether special order types, iceberg/autoslice, multi-leg/bracket orders and child orders require additional identity mappings beyond the examples reviewed.
- Whether a broker offers a documented safe retry procedure for an order request whose response is lost.

These are **UNKNOWN**, not negative claims about undocumented internal broker behavior. No broker account, sandbox or production API was contacted to probe them.

## 10. Research decisions

- **ACCEPT:** represent uncertain placement, modification and cancellation outcomes explicitly; never silently convert a transport failure to rejection.
- **ACCEPT:** distinguish local intent ID, broker correlation/tag, broker order ID, exchange order ID and individual trade ID.
- **ACCEPT:** reconcile orders and trades separately; a final order status alone is insufficient to reconstruct partial executions.
- **ACCEPT:** treat live updates as a fast signal and use REST order/trade reconciliation after disconnection.
- **ACCEPT:** persist local audit evidence before provider day-level history expires.
- **DEFER:** claiming exactly-once submission, automatic retry safety, gap-free event delivery or deterministic recovery until a provider contract and controlled evidence establish them.
- **NOT AUTHORIZED BY THIS RECORD:** broker connection, live/sandbox API calls, real order placement, code changes, paid services or production configuration.

## Source register

All sources below are official provider documentation. URLs were checked for this research record on 2026-11-08; provider documentation and limits may subsequently change.

**Zerodha Kite Connect**
- Orders: https://kite.trade/docs/connect/v3/orders/
- WebSocket streaming: https://kite.trade/docs/connect/v3/websocket/
- Postbacks/WebHooks: https://kite.trade/docs/connect/v3/postbacks/
- Exceptions and rate limits: https://kite.trade/docs/connect/v3/exceptions/

**Upstox**
- Order history: https://upstox.com/developer/api-documentation/get-order-history/
- Order details: https://upstox.com/developer/api-documentation/get-order-details/
- Daily trade book: https://upstox.com/developer/api-documentation/get-trade-history/
- Trades by order: https://upstox.com/developer/api-documentation/get-trades-by-order/
- Portfolio stream feed: https://upstox.com/developer/api-documentation/get-portfolio-stream-feed/
- Webhook: https://upstox.com/developer/api-documentation/webhook/
- Streamer functions/reconnect: https://upstox.com/developer/api-documentation/streamer-function/
- Rate limits: https://upstox.com/developer/api-documentation/rate-limiting/

**DhanHQ**
- Orders: https://dhanhq.co/docs/v2/orders/
- Live Order Update: https://dhanhq.co/docs/v2/order-update/
- Introduction, errors and rate limits: https://dhanhq.co/docs/v2/
- Releases: https://dhanhq.co/docs/v2/releases/
