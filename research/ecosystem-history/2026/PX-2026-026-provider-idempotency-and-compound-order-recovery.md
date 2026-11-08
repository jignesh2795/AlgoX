# PX-2026-026 — Provider idempotency, request correlation and compound-order recovery audit

**Research date:** 2026-11-08  
**Status:** official-documentation audit completed; cross-request idempotency remains unproven  
**AlgoX area:** Indian-market broker adapters / order submission / order grouping / recovery  
**Providers:** Zerodha Kite Connect, Upstox Developer API, DhanHQ API v2  
**Inputs:** PX-2026-024 and PX-2026-025  
**Mode:** research and requirements refinement only  
**Non-goals:** no broker connection, account/sandbox/production API call, order placement, code implementation, paid service, PR or merge to `main`

## Executive finding

The deeper audit found that the phrase “one order placement” is too coarse for recovery requirements. Current official documentation describes:
- one placement request producing multiple broker orders through automatic slicing;
- one multi-order request producing separate per-line outcomes, including partial success;
- one compound/super-order request whose entry, target and stop-loss legs have a nested lifecycle;
- one broker correlation lookup returning an order object, without documenting whether it enumerates every child created by a slicing operation.

These behaviors change the unit of reconciliation. A future adapter must preserve **request → logical intent → order group → child broker orders → compound legs → individual trades** as distinct relationships.

The audit also clarifies the limits of correlation identifiers:

- **Kite:** `tag` is an order-identification/filtering field, not a documented deduplication token. `guid` is described as an unusable request ID to avoid duplication; it is not a client-controlled idempotency key. Auto-slicing can return successful slice IDs and per-slice errors in the same response.
- **Upstox:** V3 single-order auto-slicing returns a list of `order_ids`. The separate V2 multi-order API requires a unique `correlation_id` per order line inside one submitted payload and can return HTTP 207 partial success. Duplicate correlation IDs within that payload reject the request. None of those rules documents deduplication across separate repeated HTTP requests.
- **DhanHQ:** `correlationId` is documented as a user/partner-generated tracking value, and the correlation lookup endpoint returns one order object in its published schema. Dhan publishes an order-slicing endpoint but the reviewed page does not include a response structure for it. Dhan Super Orders have a parent order ID and nested target/stop-loss leg details.

**Verdict:** no safe cross-request retry/idempotency contract has been established for these providers from the reviewed public documentation. A repeated request after a lost acknowledgement remains a possible duplicate submission. Correlation identifiers may aid discovery; they are not proof of deduplication.

## 1. Scope and audit method

The audit reviewed current public provider documentation for placement, tags/correlation values, auto-slicing, multi-order placement, order books/history, compound orders, and update streams.

Evidence categories:
- **SOURCE-DOCUMENTED:** directly stated or shown in an official API page.
- **NOT DOCUMENTED IN REVIEWED PAGE:** no such behavior or response contract appears in the reviewed public page. This is not proof that the provider's backend lacks the capability.
- **DERIVED REQUIREMENT:** conservative AlgoX obligation derived from the documented behavior or gap.
- **UNKNOWN:** behavior not established by public documentation and not probed through a broker account or API.

No provider account, sandbox, production endpoint or credential was used. No empirical HTTP retry test was performed.

## 2. Zerodha Kite Connect

### 2.1 Tag and request identity

Kite documents `tag` as an optional field to identify/filter orders and states that the value is returned in the order book. It may be a unique ID or describe an application/context. The reviewed documentation does not state that reusing a tag on a second placement returns the first order, suppresses the second, or rejects it.

The order response also includes `guid`, described as an “Unusable request id to avoid order duplication”. The page does not document this as a caller-supplied idempotency key or provide a client-controlled retry protocol based on it.

**Conclusion:** keep the tag as a correlation/filter attribute. Do not build a retry strategy around tag reuse or the response GUID.

Sources:
- https://kite.trade/docs/connect/v3/orders/

### 2.2 Auto-slicing changes a single request into multiple outcomes

When `autoslice=true` and quantity exceeds exchange freeze limits:
- the response contains an array with one entry per slice;
- a successful slice entry contains its own `order_id`;
- a failed slice is represented by an `error` object containing code/type/message/data;
- successful and failed slices can coexist in the same response;
- each successful slice appears as a separate order in the order book;
- the documented maximum is 10 slices for one auto-slice order.

This is direct evidence that an apparently singular placement can be **partially accepted** at slice level. A single top-level “success” label is not enough to infer that every intended unit was placed.

The published auto-slice example does not document a separate parent-order ID linking all child slice IDs. Kite's `parent_order_id` field is documented for multi-legged/cover-order relationships; it must not be assumed to cover auto-slice children.

**Recovery implication:** if the response is lost, the system may not know the complete slice set. The day order book and tag can provide discovery evidence, but the documentation reviewed does not explicitly guarantee that all auto-slice child orders inherit a common tag or expose a complete parent/child grouping identifier. Child-set completeness must therefore remain UNKNOWN until verified.

Sources:
- https://kite.trade/docs/connect/v3/orders/ (Tagging orders, Auto slice orders, Multi-legged orders)

## 3. Upstox

### 3.1 V3 single-order placement and auto-slicing

The current V3 Place Order page:
- accepts an optional `tag` field;
- documents a 40-character tag limit;
- allows slicing to be enabled using `slice=true`;
- explains that a quantity above freeze limit is split into smaller orders;
- shows a successful response with an array named `data.order_ids`;
- describes each resulting split as a separate order.

The example uses a 10,100 quantity and a 1,000 freeze quantity to show 11 orders. The response schema lists the resulting IDs, but the reviewed page does not describe a parent-order identifier or a per-child failure array for a lost/partial response.

**Recovery implication:** when the response is received, preserve every returned order ID as a child of the local request. When the response is lost, do not infer the intended child count from a partial set of REST or stream observations; use the documented read APIs and keep completeness unresolved unless the full set is established.

The page does not explicitly guarantee that every auto-sliced child inherits a common tag or that a repeated V3 placement with the same tag is deduplicated.

Sources:
- https://upstox.com/developer/api-documentation/v3/place-order/

### 3.2 Multi-order placement is per-line correlated and may partially succeed

Upstox separately documents a multi-order endpoint at `POST /v2/order/multi/place`. The reviewed page states:

- each submitted order line must carry a `correlation_id`;
- the ID length must be between 1 and 20 characters;
- duplicate correlation IDs **within the submitted payload** cause the entire request to be rejected;
- successful responses contain a per-line `correlation_id` and `order_id`;
- HTTP 207 / `partial_success` is supported when some valid order lines encounter errors;
- the response includes successful order lines, per-line errors and a summary of total/success/error counts;
- if one or more lines have payload errors, the page says orders are processed only when the entire batch is free of payload errors;
- documented processing order is all BUY orders first, followed by all SELL orders;
- auto-slicing may be combined with multi-order placement, subject to a maximum order-count limit.

This creates two distinct correlation concepts:
- `correlation_id`: a required per-line key for correlating a multi-order request's response entries to the submitted lines;
- `tag`: an optional order-level field available for order-history retrieval.

The within-payload uniqueness constraint is **not** a cross-request idempotency guarantee. The documentation does not say that resubmitting the same payload and same correlation IDs returns the original results or suppresses duplicate orders.

**Recovery implication:** a multi-order command must be recorded as a batch with independent line outcomes. A 207 result is not a failed batch or an all-success batch. A lost response leaves the batch outcome unknown; per-line correlation IDs are useful for reconstructing which child lines may have succeeded, but must not be used as a retry key without an explicit provider guarantee.

The multi-order page uses the V2 endpoint. It is not described as deprecated on the reviewed page, but the current single-order V3 page is separate. The version difference must remain explicit; do not assume all V2 multi-order features and response contracts transfer unchanged to V3 single-order placement.

Sources:
- https://upstox.com/developer/api-documentation/place-multi-order/
- https://upstox.com/developer/api-documentation/get-order-history/
- https://upstox.com/developer/api-documentation/v3/place-order/

## 4. DhanHQ

### 4.1 Correlation lookup and its documented shape

Dhan describes `correlationId` as a user/partner-generated ID for tracking, with a maximum length of 30 characters. Its `GET /orders/external/{correlation-id}` endpoint is specifically described for a case where the user missed the order ID.

The published response example is a **single order object** containing one `orderId`, one `correlationId`, one order status and the order parameters. The standard day order book returns an array of order objects and includes `correlationId` and `orderId` per row.

The reviewed documentation does not state:
- that `correlationId` is unique across requests or trading sessions;
- that submitting an existing `correlationId` again is suppressed/rejected;
- whether one correlation lookup can return all orders created from a slicing request;
- how collisions are resolved or how long a correlation ID remains searchable.

**Conclusion:** the correlation lookup is a lost-order-ID recovery facility, not a documented idempotency contract. For sliced requests, a single returned order object cannot be treated as proof that the full child-order set has been discovered.

Sources:
- https://dhanhq.co/docs/v2/orders/

### 4.2 Dhan order slicing

Dhan documents `POST /orders/slicing` to split an F&O request above freeze quantity into multiple orders. The request example includes `correlationId`.

The reviewed order page does not publish a response structure after the slicing request parameters; it proceeds to the Order Book section. The public page therefore does not establish the response shape, whether it returns all child order IDs, whether partial slice failure is representable, or how the returned children map back to a single correlation ID.

The day order book does expose a `correlationId` on each order record. However, the reviewed document does not explicitly state that every child created by `/orders/slicing` carries the same value or that searching by that value produces a complete child set.

**Conclusion:** the endpoint exists, but its response and correlation/grouping semantics are insufficiently documented in the reviewed source. Do not fabricate a response type or claim that Dhan slicing recovery is solved.

Source:
- https://dhanhq.co/docs/v2/orders/

### 4.3 Super Orders are a distinct compound-order abstraction

Dhan's Super Order API is documented as a collection containing an entry leg, target leg and stop-loss leg, with optional trailing stop-loss.

The create response supplies one top-level `orderId`. The `GET /super/orders` response lists each Super Order and nests the target/stop-loss leg details under the main entry order. Dhan also states that individual legs can be found in the main order book with their order IDs. Leg names and states include entry, target and stop-loss distinctions.

This is a documented compound-order hierarchy; it is not equivalent to simple quantity slicing. A recovery model must preserve:
- Super Order identity;
- entry/target/stop-loss leg role;
- individual order IDs where exposed;
- leg-specific status, triggered/remaining/filled quantity;
- the parent-to-leg relationship.

Flattening a Super Order into one ordinary order status would lose lifecycle information.

Source:
- https://dhanhq.co/docs/v2/super-order/

## 5. Cross-provider idempotency verdict

| Provider/API | Correlation field | Documented uniqueness scope | Safe repeated-request deduplication documented? | Compound/sliced result |
|---|---|---|---|---|
| Kite regular placement | Optional `tag` (max 20 chars) | Can be a unique ID/filter value; enforcement scope not stated | **NO — not established** | N/A |
| Kite auto-slice | Optional `tag` | Propagation across all child slices not explicitly guaranteed in reviewed page | **NO — not established** | Multiple order IDs; per-slice errors may coexist |
| Upstox V3 placement | Optional `tag` (max 40 chars) | Order identification; no retry uniqueness contract | **NO — not established** | Response returns array of `order_ids` for slicing |
| Upstox V2 multi-order | Required `correlation_id` per order line (1–20 chars), plus optional `tag` | Correlation IDs must be unique within one submitted payload | **NO — within-payload uniqueness is not cross-request idempotency** | Per-line outcomes; HTTP 207 partial success; optional slicing |
| Dhan regular placement | `correlationId` (max 30 chars) | User/partner tracking value; uniqueness/collision scope not stated | **NO — not established** | Single order response |
| Dhan slicing | `correlationId` in request | Child propagation and lookup cardinality not stated | **NO — not established** | Endpoint exists; reviewed page omits response schema |
| Dhan Super Order | `correlationId` (max 30 chars) | Tracking value; uniqueness scope not stated | **NO — not established** | One Super Order ID with nested legs |

“NO — not established” means the reviewed public documentation did not publish the guarantee. It is not a claim that a provider's private implementation necessarily lacks deduplication.

## 6. Required refinements to PX-025

PX-025 already requires identity separation, parent/child modelling and explicit unknown outcomes. The provider audit shows that those requirements need more precise treatment for commands with multiple child outcomes.

### R-031 — Command group has per-child outcome accounting

A batch, sliced placement or compound command MUST preserve the outcome of each documented child/line/slice/leg independently. A group MUST NOT be represented by one success/failure value when the provider can report partial success.

Successful child IDs, rejected child lines, provider errors, missing child results and unresolved children MUST remain separately attributable to the parent local command/intent.

### R-032 — Correlation uniqueness is scoped to the provider contract

The adapter MUST record what a provider correlation field means and its documented uniqueness scope. A provider constraint such as “unique within this request payload” MUST NOT be generalized into global uniqueness, cross-request idempotency or server-side duplicate suppression.

Provider `tag`, multi-order `correlation_id`, Dhan `correlationId`, broker order ID and local command ID MUST remain separate typed fields.

### R-033 — Child-set completeness is independently reconciled

When a command may create multiple broker orders, the system MUST track both:
- which child orders have been positively observed; and
- whether the complete expected child set is known.

An incomplete child set MUST remain unresolved even when one or more child orders are found. The expected count, per-child result or provider-defined group boundary must be supported by the actual response/lookup contract; it MUST NOT be guessed from quantity alone.

### Additional acceptance tests for PX-025

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-036 | Kite auto-slice response has successful order IDs and one or more per-slice error objects | Preserve each success and failure independently; group result is partial, not all-success |
| AT-037 | Kite auto-slice response is lost after possible dispatch and orderbook later shows only some candidate children by tag | Keep child-set completeness UNKNOWN; do not resubmit the full quantity |
| AT-038 | Upstox V3 `slice=true` returns multiple `order_ids` | Preserve every returned ID as an independent child of the command; reconcile each child's status/trades |
| AT-039 | Upstox multi-order endpoint returns HTTP 207 / `partial_success` | Correlate each success and error by its per-line `correlation_id`; never report all-success or all-failure |
| AT-040 | Upstox multi-order payload repeats a `correlation_id` within the same request | Model the documented whole-payload rejection; do not misinterpret this validation rule as cross-request idempotency |
| AT-041 | Dhan slicing request is accepted/response is lost, but the published response schema does not define the child set | Keep group outcome and child-set completeness UNKNOWN until the provider contract/observations establish the full set |
| AT-042 | Dhan Super Order has an entry leg and nested target/stop-loss leg lifecycle | Preserve the parent Super Order and every leg/individual order ID and state; do not flatten it into a single ordinary order |
| AT-043 | Dhan correlation lookup returns one order object after an ambiguous sliced request | Treat that object as one discovered order only; do not infer that all slices/children have been found |

The original PX-025 tests AT-001 through AT-035 remain in force. With this amendment, the proposed specification contains **33 requirements and 43 acceptance scenarios**. These are requirements, not executed tests.

## 7. Consequences for recovery design

1. **Command group is not provider order.** Persist a local command group/intent before sending a batch or slicing request; preserve each provider child order separately.
2. **Request correlation is not idempotency.** Use tags/correlation IDs to find evidence, not to authorize a repeated submission.
3. **Response loss can hide partial acceptance.** A lost response for auto-slicing or a multi-order request may conceal a subset of accepted children. Exposure must be treated conservatively until all children are enumerated/reconciled.
4. **Per-child trades are authoritative execution evidence.** Aggregate fill totals only from deduplicated individual trade records; compare them against each child order's quantities and then the parent intent's aggregate.
5. **Compound legs have distinct transitions.** Super Order/CO/BO/iceberg or other complex structures require provider-specific relationship and leg lifecycle mappings.
6. **No fabricated Dhan slicing contract.** The missing response schema is a provider-documentation gap. Do not invent an array shape or assume a single correlation lookup recovers all resulting orders.
7. **Provider versions remain explicit.** Upstox V3 single placement and V2 multi-order placement are different API endpoints. A future adapter capability matrix must identify the exact endpoint/version used per command.

## 8. Provider contract gaps still open

| Gap | Current evidence | Required closure |
|---|---|---|
| Kite tag reuse across distinct placements | Tag is present for order identification; no dedupe contract reviewed | Official idempotency/retry statement or treat as non-idempotent/unknown |
| Kite tag propagation to every auto-slice child | Each child is a separate order; shared propagation not explicit | Provider confirmation or documented response/orderbook evidence |
| Kite auto-slice child grouping | Successful IDs and errors are returned; no documented parent group identity in example | Explicit group contract or local child ledger from complete response |
| Upstox V3 slice tag propagation | Request has tag and response order_ids; child propagation not explicitly stated | Official confirmation or controlled, separately authorized provider test |
| Upstox repeated multi-order request | Per-line correlation ID uniqueness inside one payload; cross-request behavior absent | Explicit idempotency/retry guarantee |
| Upstox batch read-after-write | Per-line history lookup exists; no atomic snapshot/visibility guarantee reviewed | Provider consistency contract or conservative UNKNOWN window |
| Dhan correlation ID uniqueness and collisions | Tracking field and lookup exist; no uniqueness scope stated | Official contract |
| Dhan correlation lookup cardinality | Published response example is one order object | Explicit statement whether a correlation ID may resolve multiple slice orders |
| Dhan slicing response format | Endpoint/request documented; response schema not shown on reviewed page | Current OpenAPI/schema or official response example |
| Dhan child correlation propagation | Correlation ID appears in request and orderbook objects; slicing propagation not stated | Official contract or verified provider evidence |
| Dhan Super Order post-disconnect completeness | Super Order list exposes nested legs; stream has order updates | Status/replay and REST consistency guarantees |
| Trade bust/correction semantics | Not closed in this audit | Provider-specific post-trade correction and tradebook contract |

No gap is silently considered resolved.

## 9. Recommendation and next sequence

**Accept** R-031 through R-033 and AT-036 through AT-043 as refinements to PX-025.

Then proceed in this order:
1. Build the provider capability matrix around exact endpoint versions, child/group output shapes, correlation semantics, and lookup cardinality.
2. Separate batch/auto-slice/compound-order command groups from ordinary single-order commands in the future domain design.
3. Specify provider-specific reconciliation queries for each child and leg.
4. Design fake-provider tests for lost response with partial child acceptance before any broker connectivity is contemplated.
5. Obtain official answers for unresolved response schemas and idempotency contracts; if not documented, preserve UNKNOWN and require manual/operator resolution rather than automatic retry.

## Source register

**Zerodha Kite Connect**
- Orders, tagging, auto-slice and compound CO details: https://kite.trade/docs/connect/v3/orders/
- Postbacks: https://kite.trade/docs/connect/v3/postbacks/

**Upstox**
- V3 Place Order and auto slicing: https://upstox.com/developer/api-documentation/v3/place-order/
- V2 Place Multi Order: https://upstox.com/developer/api-documentation/place-multi-order/
- V2 Order History: https://upstox.com/developer/api-documentation/get-order-history/
- Order Book: https://upstox.com/developer/api-documentation/get-order-book/
- Portfolio Stream Feed: https://upstox.com/developer/api-documentation/get-portfolio-stream-feed/

**DhanHQ**
- Orders, slicing and correlation lookup: https://dhanhq.co/docs/v2/orders/
- Super Orders: https://dhanhq.co/docs/v2/super-order/
- Live Order Update: https://dhanhq.co/docs/v2/order-update/

**Final status:** provider idempotency and compound-order recovery audit documented. Public documents support correlation and child-order discovery mechanisms, but no provider-wide cross-request exactly-once/idempotent retry guarantee is established. No broker endpoint was called and no trading action occurred.
