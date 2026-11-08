# PX-2026-037 — Market-data identity, timestamp semantics and feed continuity

**Research date:** 2026-11-08  
**Status:** official Kite, Upstox and Dhan market-data documentation reviewed; no live feed or historical dataset was consumed  
**AlgoX area:** market-data adapters / canonical instrument crosswalk / event-time model / quote freshness / historical replay / backtest data quality  
**Inputs:** PX-023, PX-027, PX-034, PX-035, PX-036 and PX-025 requirements R-148–R-162  
**Mode:** research and requirements specification only  
**Non-goals:** no broker/account access, live WebSocket connection, market-data API request, subscription, sandbox/production interaction, order, code implementation, paid data, PR or merge to `main`

## Executive finding

Market data must be attached to the exact canonical contract identity established by PX-036, and its timestamps must retain their distinct meanings. A provider's last-trade time, quote-packet/exchange time, provider message time, and the local process receive time are not interchangeable.

The reviewed providers document materially different market-data envelopes:

- **Kite:** REST quote data distinguishes `timestamp` (exchange timestamp of the quote packet) from `last_trade_time`. Its WebSocket tradable-instrument quote packet includes both last-trade timestamp and exchange timestamp. Its index packet has a different, shorter structure and exposes exchange timestamp but not the same full trade/depth fields.
- **Upstox V3:** the feed begins with a market-status message, then a current-market-data snapshot, then live updates. Per-instrument `ltpc.ltt` is last-trade time; `currentTs` is documented as the timestamp of the received tick. The reviewed schema does not document a separate exchange quote timestamp or replay sequence/cursor.
- **DhanHQ v2:** event-based binary WebSocket packets expose LTT (epoch) for ticker/quote/full packets. The documented packet structures reviewed do not expose a separate exchange quote-update timestamp or sequence/replay cursor. It documents ping every 10 seconds and server-side connection closure after more than 40 seconds without a pong; a disconnect packet carries a reason code.

**Key design decision:** represent event time, last-trade time, provider-message time, local receive time, persistence time, candle bucket time and exchange session date as separate fields. Freshness must be evaluated for the data use case: LTT age measures trade freshness, not necessarily quote/depth freshness. If the provider does not expose a separate quote-update timestamp, the platform must not invent one.

Historical continuity is also provider-specific:
- Kite's continuous-data feature works for **daily candles of expired NFO/MCX futures**, not a general continuous intraday history across every expired contract. Kite notes that expired contract tokens are not available from its live instrument master unless cached.
- Dhan documents daily candles back to instrument inception and intraday intervals of 1/5/15/25/60 minutes for the last five years, with a maximum 90-day intraday request window.
- Provider historical candles are source observations, not automatically interchangeable or perfectly aligned by bucket boundary, adjustment policy or contract identity.

## 1. Timestamp semantics: a typed event-time model

### 1.1 Required time dimensions

Every market-data observation should retain, where supplied:

| Field | Meaning | Source/derivation |
|---|---|---|
| `exchange_event_time` | Exchange-assigned timestamp for the quote/update packet or market event | Provider field only where explicitly documented |
| `last_trade_time` | Time of the trade that produced the current LTP | Provider LTT/last_trade_time |
| `provider_message_time` | Time the provider says it generated or received the enclosing message/tick | Provider timestamp such as Upstox `currentTs` or `market_info.currentTs` |
| `local_received_at_utc` | Wall-clock UTC time when the local adapter received the full message | Captured by AlgoX |
| `local_received_monotonic` | Monotonic clock at local receipt for elapsed-time calculations | Captured by AlgoX; not exchange time |
| `persisted_at_utc` | Time the observation was durably written to the local event store | Captured by AlgoX |
| `candle_bucket_start` / `end` | Start/end of a historical or locally aggregated bar interval | Derived under explicit exchange-session/calendar policy |
| `exchange_session_date` | Trading date to which the event belongs | Effective exchange calendar/session |
| `source_time_semantics` | Documented meaning and unit of each raw timestamp | Provider/API/schema version |

Fields that are not present in a provider payload remain null/UNKNOWN. Do not copy `last_trade_time` into `exchange_event_time`, or local receive time into provider time, merely to fill a schema field.

Store the raw timestamp representation and unit (epoch seconds, epoch milliseconds, ISO 8601 with offset, or protocol-specific integer) alongside the normalized instant and parser/schema version.

### 1.2 Why LTT and quote-update time differ

A security can have an old last-trade time while its bid/ask book or quote packet is receiving new updates. For a thinly traded option, LTT may remain unchanged even while market depth changes; conversely, an instrument can be quiet and have no genuine update at all.

Therefore:
- trade freshness uses age of `last_trade_time`;
- quote/depth freshness uses a quote/update timestamp only if the provider exposes one with clear semantics;
- transport liveness uses most recent packet/heartbeat receipt and connection state;
- provider-message freshness uses the provider's documented message time;
- local processing lag uses local receive/persist timestamps and monotonic elapsed time.

A single `last_updated_at` value is not sufficient to represent all five.

## 2. Provider feed timestamp and continuity findings

### 2.1 Zerodha Kite Connect

The Kite REST quote response documents:
- `timestamp`: exchange timestamp of the quote packet;
- `last_trade_time`: time of the last trade;
- separate market fields such as LTP, volume, OI, OHLC, buy/sell quantity and market depth.

The Kite WebSocket packet for tradable instruments includes:
- the last traded timestamp;
- OI and other quote fields;
- a separate exchange timestamp at bytes 60–64 in the documented full quote packet.

The documented index packet is structurally different: it includes token, index LTP/OHLC/change and exchange timestamp, but not the same full tradable-instrument fields. The parser must choose packet structure by packet/instrument type, not parse an index packet as a regular equity/F&O quote.

Kite's market-data documentation says the WebSocket is the efficient live-hours quote channel, supports up to 3,000 instruments per connection and up to three WebSocket connections per API key. These are provider capacity constraints, not guarantees about sequence completeness or replay after disconnect. The reviewed feed schema does not establish a universal event sequence/cursor for reconstructing missed ticks.

Sources:
- https://kite.trade/docs/connect/v3/market-quotes/
- https://kite.trade/docs/connect/v3/websocket/

### 2.2 Upstox Market Data Feed V3

The V3 WebSocket sequence is explicit:
1. first message is `market_info`, carrying `currentTs` and segment-status values;
2. second tick is a current-market-data snapshot;
3. subsequent messages carry live feed updates.

The market-status message helps determine current status for segments such as NSE_EQ, NSE_FO, BSE_EQ and MCX_FO. It should be retained as a time-scoped provider observation; it does not replace the exchange holiday/session calendar.

For market data:
- per-instrument `ltpc.ltt` is last-trade timestamp;
- `ltpc.ltp`, `ltpc.ltq` and `ltpc.cp` are last price, quantity and close;
- `feeds.currentTs` is documented as the timestamp of the tick received;
- full feeds also include market depth, OI, OHLC and Greeks where subscribed.

The reviewed V3 page does not label `currentTs` as an exchange timestamp and does not document an event-sequence/replay cursor for missed messages. Retain it as provider message/received-tick time, not as exchange event time.

V3 has provider subscription limits across modes and combined subscriptions. These quotas must be respected by a subscription planner; a subscription rejection or omitted feed is a data-coverage gap, not a zero quote.

Source:
- https://upstox.com/developer/api-documentation/v3/get-market-data-feed/

### 2.3 DhanHQ Live Market Feed v2

Dhan describes the WebSocket as tick-by-tick/event-based, with JSON subscription requests and binary responses.

The documented packet fields include:
- an eight-byte response header with response code, packet length, exchange segment and security ID;
- ticker packet LTP and last-trade time (epoch);
- quote/full packets with LTT, LTQ, ATP, volume, buy/sell quantity, OHLC and OI;
- an OI packet supplied with Quote Data;
- previous-close packet sent when instruments are subscribed.

The reviewed packet schemas identify LTT, but do not separately document an exchange quote-update timestamp in the packet. The adapter must therefore retain LTT as trade time, record local receipt time, and leave exchange quote-update time unknown unless a later official schema establishes it.

Connection behaviour:
- up to five WebSocket connections per user;
- up to 5,000 subscribed instruments per connection;
- up to 100 instruments in one subscription message;
- server sends ping every 10 seconds;
- the server closes the connection if no pong is received for more than 40 seconds;
- a server disconnect packet includes a disconnect reason code.

The ping/pong proves transport liveness only. It does not prove every market-data event was delivered, that no sequence gap occurred, or that reconnect replays missed ticks. The reviewed documentation does not define a replay cursor/sequence contract.

Source:
- https://dhanhq.co/docs/v2/live-market-feed/

## 3. Freshness, staleness and missing-data classification

### 3.1 Freshness is use-case-specific

The same observation can be:
- recent as a received packet;
- stale as a last trade;
- unknown as an exchange quote update;
- usable for historical display;
- unsafe for a pre-trade decision.

A freshness policy must be parameterized by:
- provider/feed mode;
- segment and instrument type;
- market state (open, pre-open, closing auction, closed, halt/suspension);
- data component (LTP, bid/ask, depth, OI, Greeks, OHLC);
- strategy decision horizon;
- expected activity/liquidity and documented provider heartbeat/update behaviour.

There is no single universal “tick age” threshold that can validly apply to every liquid equity, thin option, index, auction session and historical candle.

### 3.2 Distinct data-quality states

Candidate observation states:

- `FRESH`: required timestamp and source scope are valid and satisfy the active use-case threshold.
- `TRADE_STALE`: last trade is older than the use-case threshold.
- `QUOTE_STALE`: provider quote/update timestamp is older than the use-case threshold.
- `TRANSPORT_STALE`: connection/heartbeat/packet arrival has exceeded its configured liveness threshold.
- `TIMESTAMP_UNKNOWN`: provider does not expose the timestamp required to prove the requested freshness.
- `GAP_SUSPECTED`: disconnect, malformed packet, subscription gap or local queue overflow may have caused missing observations.
- `GAP_CONFIRMED`: provider/exchange sequence or explicit source evidence establishes missing event range.
- `SESSION_INACTIVE`: segment is closed/holiday/suspended/otherwise not in the active session.
- `NO_TRADE_OBSERVED`: no trade update was observed in the interval; this is not the same as no quote or no subscription.
- `NO_SUBSCRIPTION`: instrument was not subscribed/eligible for the current stream.
- `INVALID`: malformed payload, identity mismatch, future timestamp beyond allowed clock skew, impossible fields or failed decoder.

Do not convert any of these states to a zero price, zero volume, zero OI or a synthetic heartbeat tick.

### 3.3 Last-trade age does not automatically invalidate a book

If the provider supplies a recent quote/update timestamp and the LTT is old, the quote can still be a recent book observation in a no-trade interval. If the provider supplies only LTT (as in the Dhan packet schema reviewed here), the platform cannot prove the precise age of a later depth-only update. It must not claim a fresh book solely because a recent packet arrived unless the packet semantics establish that the book values were refreshed with that packet.

### 3.4 Source conflicts

If two providers disagree:
- preserve each provider observation, raw timestamp and receipt time;
- compare only fields with compatible definitions and scopes;
- do not use last-arrival-wins as universal arbitration;
- do not merge LTP from one provider with depth from another to create an apparently atomic book unless an explicit composite-source policy defines that behaviour;
- classify the observation set as conflicting/UNKNOWN for risk-critical decisions where divergence exceeds policy.

## 4. Feed start, reconnect and continuity

### 4.1 Subscription lifecycle

Every instrument subscription should record:
- canonical instrument ID and provider alias;
- provider connection/session ID;
- subscription request ID/GUID where supported;
- request time, acknowledgement time and subscription mode;
- capacity/limit accounting;
- subscription state, rejection/error and unsubscribe time.

A connected socket is not proof that all requested instruments are subscribed. A subscription failure or capacity rejection must be visible as missing data coverage.

### 4.2 Initial state and reconnect

Provider behaviour differs:
- Upstox V3 sends market status, then a market snapshot, then live updates on connection.
- Dhan sends a previous-close packet when subscribing and documents ping/pong liveness; its disconnect packet includes a reason.
- Kite sends live quote packets and connection-level state, but its reviewed market feed specification does not promise replay of all missed events following a disconnect.

No provider in the reviewed documentation establishes a common cross-provider sequence/replay cursor. Therefore PX-027's rule still applies: reconnect does not prove missed-tick replay.

After reconnect:
1. mark the disconnected interval as a suspected gap;
2. restore subscriptions and capture subscription acknowledgements/state;
3. obtain fresh quote/snapshot data from the same provider where supported;
4. reconcile the current quote state against the last persisted observation;
5. fetch historical candles or other official data where available for backfill/diagnostic comparison;
6. keep event-history completeness UNKNOWN unless a source sequence/replay guarantee proves the missing interval was replayed;
7. never fabricate tick-by-tick events from OHLC bars.

Historical candle backfill can restore bar-level analytical continuity, not the original order-book/quote event stream.

## 5. Historical data, contract roll and bar identity

### 5.1 Kite continuous data is narrowly scoped

Kite explains that exchanges flush instrument tokens for futures contracts at expiry and the live instrument master only provides current live contract tokens; expired tokens are unavailable unless the application cached them.

Kite's `continuous=1` historical-data option works for NFO and MCX **futures daily candles** using a live contract token to retrieve expired contracts' day candles. It is not a general continuous intraday series for all expired options, equities or all derivatives. Preserve the actual contract identity for each constituent expiry even if the provider returns a continuous daily history.

Source:
- https://kite.trade/docs/connect/v3/historical/

### 5.2 Dhan historical data

Dhan documents:
- daily OHLCV data from the instrument's inception;
- daily endpoint uses `fromDate` and non-inclusive `toDate`;
- intraday candles at 1, 5, 15, 25 and 60 minutes;
- intraday historical availability for the last five years for active instruments;
- a maximum 90-day request range per intraday polling call;
- timestamp values are epoch timestamps.

These are provider-specific retention and request semantics. Do not assume they match another provider's date inclusivity, candle boundary or expired-contract coverage. A local backfill process must split requests into valid windows and record every requested range and returned row count.

Source:
- https://dhanhq.co/docs/v2/historical-data/

### 5.3 Bar key and session calendar

A canonical bar key should include:
- canonical instrument/contract ID;
- exchange and segment;
- exchange session date;
- interval length and interval definition;
- bucket start and bucket end;
- timezone/calendar version;
- source provider and source dataset;
- adjustment/continuous-series policy.

The same instrument may have different candles across providers because of different aggregation boundaries, late updates, corrections, missing trades or adjustment policies. Do not deduplicate by timestamp alone.

Missing intervals must be classified:
- exchange holiday/session closed;
- segment inactive/auction/halt;
- no trades occurred;
- provider did not send data;
- local disconnect/queue loss;
- data provider returned incomplete history;
- contract did not exist or had expired.

Do not synthesize flat OHLC candles for missing intervals unless a separately versioned analytical policy explicitly creates a non-market “carry-forward” record and marks it synthetic. Synthetic bars must never be used as actual exchange prices or execution evidence.

### 5.4 Expiry and corporate-action continuity

Continuous futures series and adjusted equity/derivative histories are derived datasets. Preserve the raw contract-level observations. A continuous series must specify:
- roll date/rule;
- old/new contract IDs;
- volume/open-interest or calendar roll criterion;
- any back-adjustment method and factor;
- whether prices are raw or adjusted;
- source provider and source version.

A symbol change, token change, expiry roll or corporate action must not silently splice two different economic contracts into one raw series. The adjusted/continuous view is a derived analytical series, not the identity of a tradable contract.

## 6. Market session and clock handling

- Use the exchange trading calendar and segment status, not local wall-clock time alone, to decide whether market data is expected.
- Retain the provider's segment market-status message where available (Upstox V3 documents `market_info` with per-segment status).
- Keep exchange session date separate from UTC timestamp and host local date.
- Store normalized instants in UTC while preserving original provider timestamp, unit and offset.
- Use a monotonic clock for local elapsed-time/latency measurement; wall-clock UTC is for cross-system audit. Neither local clock replaces provider/exchange time.
- Detect local clock skew using an independently maintained time source; if skew exceeds policy, mark latency and event-time comparisons UNKNOWN.
- Treat pre-open, regular session, closing auction, post-market and closed states separately. A stale-looking quote in a closed session is not automatically an unexpected feed failure; a provider message claiming an inactive segment is open must be investigated rather than blindly trusted.

## 7. Additional requirements for PX-025

### R-163 — Market observations retain distinct timestamp semantics

Every market-data observation MUST preserve exchange event/quote time, last-trade time, provider message time, local receive time, persistence time and candle bucket/session time as separate optional fields. Missing provider timestamps MUST remain null/UNKNOWN; no timestamp may be copied into another semantic field.

### R-164 — Timestamp units and raw values are preserved

The adapter MUST retain raw timestamp value, unit, timezone/offset, schema version and normalized UTC instant. Epoch seconds, epoch milliseconds, ISO timestamps and protocol integers MUST be parsed by an explicit provider/version mapping; ambiguous units or invalid/future values MUST return INVALID/UNKNOWN.

### R-165 — Trade freshness and quote/depth freshness are separate

The system MUST calculate last-trade age independently from quote/depth update age and transport liveness. An old LTT MUST NOT automatically invalidate a demonstrably refreshed quote/depth packet; a recent packet receive time MUST NOT prove quote freshness where the provider has no documented quote-update timestamp.

### R-166 — Local receipt and monotonic timing are captured

Every received market-data message MUST capture local UTC receipt and monotonic receipt time, connection/session ID and ingestion/persistence time. Monotonic time MUST be used for local elapsed/queue-latency measurement; it MUST NOT be represented as exchange or provider time.

### R-167 — Provider timestamp semantics are versioned and explicit

Kite quote `timestamp` and `last_trade_time`, Kite WebSocket LTT/exchange timestamp, Upstox `ltpc.ltt`/`currentTs`, and Dhan LTT MUST map to their documented semantic fields. An undocumented provider timestamp MUST NOT be assumed to be exchange event time.

### R-168 — Instrument/contract identity accompanies every market observation

Every quote, trade tick, depth update, OI update and candle MUST be linked to the canonical instrument/contract ID and the exact provider alias/source version used at receipt. A token/key change MUST not cause historical observations to be remapped to a different contract.

### R-169 — Provider packet variants are parsed by exact schema

Kite index and tradable-instrument packets, Upstox market_info/snapshot/live messages and Dhan ticker/quote/OI/full packets MUST use their distinct packet schemas and versions. Unknown packet lengths, codes or protobuf/binary schema revisions MUST be quarantined rather than best-effort parsed as another packet type.

### R-170 — Market status and exchange session calendar remain separate evidence

Provider segment status messages MUST be retained with provider time and source. Exchange trading calendar/holiday/session schedule MUST be maintained independently. A provider status message or local wall clock alone MUST NOT establish the complete official exchange session state.

### R-171 — Feed liveness does not establish event completeness

Heartbeat/ping/pong, an open WebSocket or a successful reconnect MUST establish at most transport/session liveness. It MUST NOT prove that every tick was received or that missed events were replayed without a documented sequence/replay contract.

### R-172 — Disconnects and subscription gaps create explicit data-gap states

Connection loss, timeout, provider disconnect reason, subscription rejection, capacity overflow, decoder error and local queue overflow MUST create time-bounded gap records scoped to the affected provider/connection/instruments. The event history MUST remain UNKNOWN until reconciled; no missing tick may be fabricated.

### R-173 — Reconnect snapshots and historical backfills do not recreate tick history

After reconnect, the system SHOULD obtain a fresh state snapshot and historical bar backfill where supported, but it MUST distinguish restored current-state/bar completeness from original tick/depth event completeness. OHLC bars MUST NOT be expanded into invented ticks or order-book events.

### R-174 — Freshness thresholds are use-case and market-state specific

Trade, quote, depth, OI, Greeks and candle freshness MUST be evaluated separately using a versioned policy for provider, segment, instrument type, market state, activity/liquidity and decision horizon. A universal stale threshold MUST NOT be assumed valid for every instrument/session.

### R-175 — Historical candles preserve contract, interval and calendar identity

Every historical bar MUST retain canonical contract ID, provider alias, interval definition, exchange session date, bucket start/end, timezone/calendar version, raw source timestamp and adjustment policy. Bars from different contracts or incompatible interval boundaries MUST NOT be deduplicated by timestamp alone.

### R-176 — Continuous/adjusted series are derived views with explicit lineage

Any rolled futures, adjusted equity or continuous derivative series MUST retain original contract-level bars and identify roll rule, old/new contracts, adjustment factor/method, effective date and source data. Continuous series MUST NOT replace the identity of the actual tradable contract.

### R-177 — Missing bars and source conflicts are not silently synthesized or merged

The system MUST distinguish exchange holiday/session closed, no trade, no subscription, provider gap, local loss, incomplete historical response and contract non-existence. Missing bars MUST NOT default to flat OHLC/zero volume; conflicting provider observations MUST remain separately attributable unless an explicit versioned aggregation policy reconciles them.

## 8. Deterministic acceptance scenarios

These extend AT-001 through AT-310. Use synthetic ticks, packet fixtures, calendars, historical bars and fake feed connections only.

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-311 | Kite REST quote has different `timestamp` and `last_trade_time` | Store quote-packet exchange time and LTT separately |
| AT-312 | Kite WebSocket quote packet contains LTT and exchange timestamp | Parse both fields using the exact packet offsets; do not collapse them |
| AT-313 | Kite index packet arrives with its shorter schema | Parse index packet separately; do not expect tradable-instrument depth/LTT fields |
| AT-314 | Upstox market_info message arrives before snapshot/live ticks | Record segment status and provider currentTs before accepting subsequent feed state |
| AT-315 | Upstox snapshot follows market_info | Mark initial state as snapshot, not a replayed event history |
| AT-316 | Upstox `ltpc.ltt` is older than `currentTs` | Preserve last-trade and provider received-tick times separately |
| AT-317 | Upstox currentTs exists but no exchange timestamp is documented | Do not populate exchange_event_time from currentTs; leave it UNKNOWN |
| AT-318 | Dhan quote/full packet supplies LTT but no separate quote timestamp | Store LTT and local receive time; quote-update age remains UNKNOWN unless later schema evidence supports it |
| AT-319 | Dhan ping/pong continues but no instrument packets arrive | Transport liveness PASS does not imply market-data coverage/freshness |
| AT-320 | Dhan misses pong beyond documented timeout and disconnect packet reports reason | Create scoped transport gap with provider reason and time interval |
| AT-321 | LTT is old but quote/depth update time is recent and documented | Trade freshness may be STALE while quote/depth freshness remains FRESH |
| AT-322 | LTT is old and provider exposes no quote-update timestamp | Do not claim current depth freshness solely from local receipt time |
| AT-323 | A liquid instrument has an update gap while exchange segment is NORMAL_OPEN | Mark feed/data gap or stale state; do not convert it to session-inactive |
| AT-324 | Instrument receives no trades during a quiet interval but provider heartbeat is alive | Distinguish NO_TRADE_OBSERVED from TRANSPORT_STALE or NO_SUBSCRIPTION |
| AT-325 | Upstox segment is PRE_OPEN/CLOSED/other status while local clock suggests normal hours | Preserve provider market-status evidence and reconcile with official exchange session calendar |
| AT-326 | Local UTC clock is offset beyond configured skew tolerance | Mark local latency/event-time comparison UNKNOWN; do not rewrite provider timestamps |
| AT-327 | Timestamp parser receives epoch seconds where milliseconds are expected | Detect unit/range mismatch and quarantine rather than silently produce a wrong date |
| AT-328 | Timestamp falls outside session/date beyond allowed skew | Mark invalid/unknown and preserve raw payload; do not shift to nearest session |
| AT-329 | Reconnect occurs after a 30-second stream disconnect with no replay cursor | Record suspected gap and fresh snapshot; tick-history completeness remains UNKNOWN |
| AT-330 | Historical candle backfill covers a disconnected 1-minute interval | Mark bar-level backfill recovered but original tick/depth stream still incomplete |
| AT-331 | Kite continuous=1 is requested for expired NFO futures at minute interval | Do not assume expired intraday continuous history is supported; use only documented daily scope or specific archived contracts |
| AT-332 | Kite expired contract token was not cached before expiry | Mark direct expired-token retrieval unavailable/UNKNOWN; do not infer token from the current master |
| AT-333 | Dhan intraday history request exceeds 90-day window | Split into compliant windows and preserve each range; no dropped date gap |
| AT-334 | Dhan daily query uses non-inclusive toDate | Respect exclusive end boundary and verify returned session dates |
| AT-335 | Historical bars from two providers have same timestamp but different bucket boundary/policy | Retain source-specific bars; do not deduplicate solely by timestamp |
| AT-336 | Continuous futures series rolls to the next contract | Preserve old/new contract IDs, roll date, rule and any adjustment factor; raw contract bars remain available |
| AT-337 | Exchange holiday has no candle for an instrument | Classify session closed/holiday; do not synthesize a zero-volume flat candle |
| AT-338 | Market is open but historical response omits one interval | Mark source/history gap; do not interpret missing interval as no trade without source evidence |
| AT-339 | Two providers report different LTP/depth at nearby but non-identical timestamps | Preserve both values and timestamps; no last-arrival-wins composite quote |
| AT-340 | Provider alias/token changes while the canonical contract remains the same | Link observations through the effective-dated PX-036 alias crosswalk; historical references keep the prior alias |

PX-025 now contains **177 normative requirements (R-001–R-177) and 340 proposed acceptance scenarios (AT-001–AT-340)**. These are proposed deterministic tests only; no live feed or historical API was queried.

## 9. Open questions and evidence limitations

1. The current provider WebSocket documentation does not establish a common event sequence or replay cursor across Kite, Upstox and Dhan; missed-tick completeness remains UNKNOWN without additional source evidence.
2. Dhan's reviewed packet schemas expose LTT but no separately documented exchange quote-update time; quote/depth age semantics require provider clarification if a strategy needs exchange-time freshness.
3. Upstox V3 documents `currentTs` as a tick-received timestamp and LTT separately, but the reviewed page does not identify currentTs as exchange time.
4. Kite's quote and WebSocket fields have distinct timestamps; the exact precision/clock authority of each timestamp should be verified against the applicable API schema revision.
5. Exact candle bucket boundary conventions, corrections/revisions and corporate-action adjustment policies can differ by provider and need current provider-specific specification or fixture tests.
6. Upstox historical-data endpoint retention and contract-expiry continuity need further source closure before claiming parity with Kite or Dhan.
7. No daily provider feed, timestamp or historical dataset was captured in this research pass.

## 10. Research decisions and non-authorization

- **ACCEPT:** keep exchange time, LTT, provider time, local receipt/persistence and candle bucket times as separate semantics.
- **ACCEPT:** separate trade freshness from quote/depth freshness and transport liveness.
- **ACCEPT:** treat the Upstox initial market-info and snapshot messages as distinct startup evidence; preserve segment status.
- **ACCEPT:** treat Dhan's documented LTT-only packet schema as insufficient to prove separate quote-update time; do not invent it.
- **ACCEPT:** reconnect/current snapshot/backfill can recover current state or bars but not reconstruct original tick/depth history without a documented replay contract.
- **ACCEPT:** preserve provider-specific historical and continuous-series scope; Kite continuous expired-futures support is daily-only in the reviewed documentation.
- **ACCEPT:** keep raw contract-level bars and link any adjusted/continuous series to its constituents and transformation policy.
- **DEFER:** exact provider freshness thresholds, event replay, historical correction and bar-boundary semantics until provider contracts and representative real/synthetic fixtures are available.
- **NOT AUTHORIZED:** broker/API connections, live subscriptions, historical API calls, orders, code changes, paid data, credential/IP changes, PR or merge to `main`.

**Final status:** PX-2026-037 market-data identity, timestamp semantics, freshness and historical continuity research documented. PX-025 expanded to 177 requirements and 340 proposed acceptance scenarios. No live market data was collected and no implementation or broker interaction was performed.
