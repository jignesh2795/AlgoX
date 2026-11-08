# PX-2026-037 — Market-data time semantics, feed integrity and historical contract continuity

**Research date:** 2026-11-08  
**Status:** official provider documentation reviewed; no live feed or historical data requests made  
**AlgoX area:** market-data adapters / timestamp and clock model / feed-health / historical replay / contract continuity  
**Providers:** Zerodha Kite Connect, Upstox Market Data Feed V3, DhanHQ Market Feed v2  
**Inputs:** PX-025 R-001–R-162; PX-027 stream-gap semantics; PX-034/035 contract master; PX-036 canonical identity and provider-alias crosswalk  
**Mode:** research and requirements specification only  
**Non-goals:** no credentials, broker API connection, market-feed subscription, historical data request, account/sandbox/production call, code implementation, paid service, order, PR or merge to `main`

## Executive finding

Market data from a broker feed is not one undifferentiated “tick with a timestamp”. The official provider schemas expose different time domains, snapshot semantics, binary encodings, heartbeat behaviour, subscription limits and historical-candle coverage.

The core distinction is between:

1. **Last-trade/event time:** when the represented trade or last-traded-price event occurred, where the provider supplies it.
2. **Exchange timestamp:** a timestamp explicitly labelled as such in a provider packet.
3. **Provider message/generated/received time:** when the provider says a feed message was generated or received by the feed service.
4. **Local receive time:** when AlgoX's process actually received the frame.
5. **Local processing time:** when the decoder and downstream pipeline processed it.
6. **Candle interval time:** the interval start or label attached to an OHLC candle, not necessarily the time of the final trade inside that candle.
7. **Session/calendar time:** the exchange trading date and market phase that contextualize the observation.

These timestamps are not interchangeable. A last traded time may remain old for an illiquid instrument even while bid/ask depth changes; an open WebSocket heartbeat shows connection liveness but does not prove that each subscribed instrument has a fresh quote; and a local receive timestamp does not prove that no earlier provider event was missed.

**Design decision:** AlgoX should store raw provider event fields, provider message timestamps, local UTC receive time, local monotonic receive/process timing, connection/subscription epoch, canonical instrument identity at event time, and decoder/schema provenance independently. It should publish a field-specific freshness/completeness state and refuse to infer exchange sequence or replay guarantees that a provider has not documented.

**Historical-data decision:** preserve actual dated contract identity and provider alias for every observation/candle. Continuous-futures convenience endpoints are not a substitute for a transparent roll policy and actual contract-level history. A historical series must record whether it is an actual contract, continuous vendor series, locally rolled series, or adjusted synthetic series.

## 1. Official provider market-feed findings

### 1.1 Zerodha Kite Connect

The current Kite WebSocket documentation states:
- up to 3,000 instruments per WebSocket connection;
- up to three WebSocket connections per API key;
- requests/subscriptions use numerical `instrument_token` values from the instrument list;
- quote packets are binary; postbacks and other non-quote updates are text;
- feed modes are `ltp`, `quote` and `full`;
- if no data is to be streamed over an open socket, a one-byte heartbeat is sent every couple of seconds.

For the normal tradable-instrument quote packet, the documented fields include:
- instrument token;
- last traded price and quantity;
- average traded price;
- volume and aggregate buy/sell quantity;
- open/high/low/close;
- last-traded timestamp;
- open interest and OI day high/low;
- a separate **exchange timestamp**;
- market-depth entries.

The distinction between bytes 44–48 (last-traded timestamp) and 60–64 (exchange timestamp) is explicitly documented. Index packets have a different, shorter structure and include an exchange timestamp; do not parse index packets using the full tradable-instrument layout.

Kite states that all prices in the binary packet are in paise, with a separate divisor for currencies. The decoder must therefore preserve raw integer values and apply the correct segment-specific scale exactly once. A generic float or one universal price divisor is unsafe.

Sources:
- https://kite.trade/docs/connect/v3/websocket/
- https://kite.trade/docs/connect/v3/market-quotes/#instruments

### 1.2 Upstox Market Data Feed V3

The legacy Upstox Market Data Feed page is marked discontinued. This research uses **Market Data Feed V3**, which is a Protobuf WebSocket feed and requires the supplied V3 `.proto` schema.

The V3 connection bootstrap has three ordered semantic messages:
1. a `market_info` message containing market-segment status and a `currentTs` timestamp documented as the time the message was generated;
2. a current market-data snapshot at connection time;
3. subsequent live-feed updates.

For live feed messages:
- `ltpc.ltt` is documented as last-traded time;
- `feeds.currentTs` is documented as the timestamp of the received tick;
- the V3 page's examples show these as 13-digit timestamp strings;
- full mode includes market levels, extended metadata and option Greeks.

The `currentTs` value must not be re-labelled as exchange event time or trade time; the documentation describes it as the received-tick timestamp. The market-info `currentTs` is specifically described as message generation time. Keep those contexts separate even though the field name is the same.

Normal V3 connection/subscription limits on the reviewed page:
- 2 connections per user;
- LTPC: up to 5,000 instrument keys individually, 2,000 combined across modes;
- Option Greeks: up to 3,000 individually, 2,000 combined;
- Full: up to 2,000 individually, 1,500 combined.
Upstox Plus has different additional limits; any deployed adapter must pin the subscription entitlement/limit profile.

The V3 page also says the first message reports segment status, the second supplies a snapshot, and subsequent messages stream live updates. This is a startup synchronization aid. It is not a documented replay cursor for messages missed before or during a disconnect.

Sources:
- https://upstox.com/developer/api-documentation/v3/get-market-data-feed/
- https://upstox.com/developer/api-documentation/get-market-data-feed/ (legacy page marked discontinued; not used as the current contract)

### 1.3 DhanHQ Live Market Feed v2

DhanHQ documents its v2 feed as tick-by-tick, WebSocket-based, and binary:
- up to five WebSocket connections per user;
- up to 5,000 instruments per connection;
- up to 100 instruments in each subscription JSON message, with multiple messages allowed on the connection;
- server Ping every 10 seconds;
- if the client fails to respond for more than 40 seconds, the server closes the connection;
- binary packets use little-endian encoding.

The common response header carries feed response code, payload message length, exchange segment and security ID. The ticker/quote/full packet definitions expose an LTT field described as Last Trade Time (EPOCH), stored as a 32-bit integer in the documented layouts. The reviewed v2 packet layout does not document a second per-message exchange-timestamp field comparable to Kite's exchange timestamp or Upstox's currentTs.

Do not infer that Dhan's LTT is a local receive timestamp. Preserve it as provider LTT with the exact feed schema/unit profile. A local receiver timestamp must be added by AlgoX when the frame arrives.

Sources:
- https://dhanhq.co/docs/v2/live-market-feed/
- https://dhanhq.co/docs/v2/annexure/

### 1.4 Cross-provider comparison

| Time/data field | Kite | Upstox V3 | DhanHQ v2 |
|---|---|---|---|
| Last-trade time | Dedicated last-traded timestamp in binary quote packet | `ltpc.ltt` documented as last traded time | LTT field documented as Last Trade Time (EPOCH) |
| Exchange timestamp | Separate field in normal quote and index packet | No equivalent separate exchange timestamp identified in the reviewed V3 packet schema | No separate field identified in the reviewed v2 packet layout |
| Provider message/receive timestamp | Not identified as a general per-packet receive-time field in the reviewed quote layout | `currentTs` is timestamp of received tick; market-info `currentTs` is message generation time | No equivalent per-message timestamp identified in the reviewed packet layout |
| Local receive time | Must be captured by the client | Must be captured by the client | Must be captured by the client |
| Encoding | Binary packet; integer prices in paise with currency scale exception | Protobuf using supplied V3 proto | Binary little-endian |
| Liveness | One-byte heartbeat every couple seconds when no data to stream | Periodic WebSocket ping/pong | Server ping every 10 seconds; closes after more than 40 seconds without response |
| Startup snapshot | The reviewed page describes stream connection/subscription but not a replay cursor | Explicit market_info, current snapshot, then live updates | Previous-close packet sent when subscribed; no replay cursor documented |
| Per-stream sequence/replay | No per-message sequence/replay guarantee identified in reviewed public schema | No sequence/replay cursor identified in reviewed V3 public schema | No sequence/replay cursor identified in reviewed v2 public schema |

This comparison is limited to the reviewed public market-feed pages and schemas. Absence of a field in the reviewed packet page is not a claim that the provider has no other product, exchange feed or private member interface with sequencing.

## 2. Canonical timestamp and clock model

### 2.1 Preserve distinct time domains

A future normalized market-data observation should retain, where available:

- `provider_event_time_raw`;
- `provider_last_trade_time_raw`;
- `provider_exchange_time_raw`;
- `provider_message_time_raw`;
- `provider_timestamp_unit` and epoch/scale profile;
- `local_received_at_utc`;
- `local_received_monotonic_ns`;
- `local_decoded_at_utc`;
- `local_processed_monotonic_ns`;
- `market_session_id` / exchange trading date;
- `connection_epoch_id` and `subscription_epoch_id`;
- provider, API/feed version, schema/protobuf hash and decoder version;
- raw frame hash/reference and packet/message offset where retained.

Raw source timestamps must not be overwritten by a converted datetime. Keep the raw value, normalized UTC instant, unit/epoch assumption and conversion version. Use exchange timezone (Asia/Kolkata for NSE/BSE sessions) only for session/calendar interpretation and rendering; do not convert a date-only expiry/session key through a timezone and accidentally shift it.

The machine's local UTC wall clock is useful for cross-process observability but can jump due to time adjustment. A local monotonic clock is required for elapsed time, queue latency and processing duration. Record clock synchronization state/offset/uncertainty where available. Do not compare monotonic values across process restarts or machines as if they were a shared epoch.

### 2.2 Event time and receive time answer different questions

- **Last-trade time** answers when the represented last trade occurred, not necessarily when the current quote/depth changed.
- **Exchange timestamp** is used only where the provider explicitly identifies it as such.
- **Provider currentTs/message time** follows the provider documentation's meaning; do not relabel it.
- **Local receive time** answers when AlgoX observed the message, not when the exchange event happened.
- **Local processing time** measures internal pipeline delay, not market latency.

A thinly traded instrument can have a stale last-trade time while its order book or indicative price changes. Conversely, an old exchange timestamp arriving now can represent stale market data delivered late. Freshness must be evaluated per field and use case, not by one generic `timestamp_age`.

### 2.3 Timestamp units and binary precision

The providers use different representations:
- Kite quote packet timestamps are 32-bit integers in its binary layout; the schema gives field meaning but its unit/profile must be pinned and validated by API version/decoder.
- Upstox V3 uses timestamp strings in its examples, with millisecond-scale values; preserve the raw string and use the current protobuf field definition as the unit contract.
- Dhan v2 documents an int32 EPOCH LTT field; preserve raw bytes/value and apply the documented/verified epoch unit profile rather than blindly treating it as milliseconds.

Do not infer unit from a numeric value alone when the provider schema version is unknown. A seconds-vs-milliseconds mistake creates dates thousands of years apart or silently shifts observations. Range sanity checks must reject invalid timestamps and keep the raw value.

Prices and Greeks may arrive as fixed-point integers, float32 or Protobuf numeric fields. Preserve raw bytes/bit values and source scale where practical. Convert into AlgoX's exact internal decimal representation only once under the source decoder's documented scale. The provider's floating-point encoding does not become exact exchange decimal merely by parsing it into a binary float again.

## 3. Snapshot, live updates and feed completeness

### 3.1 Connection liveness is not per-instrument freshness

Provider heartbeats are connection-management signals:
- Kite sends a one-byte heartbeat every couple seconds when no data is streamed;
- Dhan sends server ping every 10 seconds and closes if no pong is received for more than 40 seconds;
- Upstox's V3 WebSocket uses ping/pong for the connection.

A healthy heartbeat does not prove that:
- every subscribed instrument has received a current quote;
- the provider delivered every underlying market event;
- the last-trade value changed;
- a quote/depth snapshot is fresh enough for a particular strategy;
- the client did not drop frames after receive due to local backpressure.

Maintain separate health dimensions for socket state, ping/pong state, subscription acknowledgements, received bytes/frames, per-instrument update/observation age, local queue backlog, decoder errors and strategy-consumer lag.

### 3.2 Startup and reconnect resynchronization

Upstox V3 explicitly sends market status, then a snapshot, then live updates at connection start. Treat the snapshot as a current-state observation with its own timestamp and connection epoch. Do not interpret it as a replay of events since the last connection.

Kite and Dhan public feed pages describe binary subscriptions and liveness but do not establish a general replay cursor or missed-event replay guarantee in the reviewed schema. PX-027 already requires event-history completeness to remain UNKNOWN after an undocumented stream gap.

A safe reconnect sequence:
1. mark the old connection epoch closed and record the disconnect interval;
2. mark event-history continuity across the interval UNKNOWN unless provider replay semantics exist;
3. create a new connection/subscription epoch;
4. decode market status/session state where supplied;
5. obtain/record the provider's current snapshot and a REST snapshot where appropriate;
6. begin applying live observations under the new epoch;
7. compare snapshots for current-state reconciliation, not fabricated event replay;
8. retain a gap record and any source differences;
9. allow downstream current-state use only when its field freshness/quality gate passes;
10. keep historical event completeness UNKNOWN if the missed event sequence cannot be proven complete.

### 3.3 Ordering, duplicates and no documented sequence

The reviewed provider schemas do not expose a common event sequence number for these retail broker WebSocket feeds. Therefore:
- local arrival order is not proof of exchange causal order;
- timestamps can collide or have coarse resolution;
- two packets can carry the same LTT while depth or other fields differ;
- identical price/quantity/time values can be separate observations;
- deduplicating by timestamp + LTP can discard real data;
- a later-arriving older event must not silently overwrite a newer accepted observation without a quality/order policy.

Persist raw observations and derive a current-state projection using an explicit provider-specific ordering policy. When event ordering cannot be established, mark the affected field/history as ordering-uncertain rather than inventing a sequence.

## 4. Historical candles and replay continuity

### 4.1 Candle start time and interval semantics

Upstox Historical Candle Data V3 explicitly defines the candle timestamp as the **start time of the candle's timeframe**. Dhan's historical data API returns an epoch timestamp for each OHLC candle but the reviewed page does not explicitly define whether the timestamp is interval start or end. Kite's historical page gives ISO-8601 timestamps with an Asia/Kolkata offset in examples, but the reviewed page does not explicitly define all interval-boundary and finalization semantics.

Therefore a normalized candle must retain:
- source provider/API version;
- canonical contract identity and provider alias used for retrieval;
- interval/unit and source timestamp raw value;
- timestamp meaning (start/end/label/unknown) as documented for that source;
- exchange session/date and timezone/calendar;
- source retrieval time and request range;
- candle completeness/finality status if available;
- OHLCV/OI raw values and units;
- source correction/revision identity if exposed.

Do not assume candles from different providers align just because their interval labels both say “1 minute”. Compare exact time boundaries and session alignment first. Never shift a candle silently to make the providers agree.

### 4.2 Historical availability and retrieval limits are source-specific

The reviewed public docs state:
- **Kite:** historical candle data spans back several years; available intervals include minute, 3/5/10/15/30/60-minute and day. It has a `continuous=1` option for day candles for NFO/MCX futures.
- **Upstox V3:** minute data is listed from January 2022; 1–15 minute intervals have a one-month maximum retrieval range per call, larger minute intervals up to a quarter, hour data up to a quarter, day data from January 2000 with up to a decade range, and weekly/monthly from January 2000 with no listed range cap.
- **Dhan v2:** daily data is documented back to instrument inception; intraday data covers the last five years, with only 90 days polled per request.

These are provider/API availability limits at the time of the reviewed documentation. They are not a guarantee that all instruments have uninterrupted history or that broker histories are identical. Store the returned coverage and page/request ranges per data acquisition.

Sources:
- https://kite.trade/docs/connect/v3/historical/
- https://upstox.com/developer/api-documentation/v3/get-historical-candle-data/
- https://dhanhq.co/docs/v2/historical-data/

### 4.3 Expiry and continuous-futures identity

Kite explicitly says exchanges flush futures/options instrument tokens at each expiry; the live instrument master returns live contracts and expired token history is unavailable from that live master unless the client regularly caches it. Its continuous API returns daily candles for expired NFO/MCX futures contracts when queried with a live contract token.

This does not establish that:
- expired contract tokens are globally stable without a cached historical master;
- the continuous endpoint supplies intraday candles or tick history for expired futures;
- the series is adjusted/back-adjusted for price gaps;
- a universal roll date or roll-price policy is applied;
- the continuous series is suitable as an execution-grade contract record.

The platform should retain the exact contract alias and master version for each actual contract observation. A separate continuous-series builder must declare:
- eligible contract chain;
- roll trigger/date/time;
- roll execution price or reference;
- gap handling (unadjusted, ratio-adjusted, difference-adjusted or other);
- corporate-action handling;
- expiry-day/holiday rule;
- volume/OI selection and rollover;
- source and adjustment version.

Backtests should be able to use actual dated contracts. A continuous series is a derived analytical view, not an exchange-listed instrument or a broker orderable token.

### 4.4 No synthetic tick replay from candles

OHLCV candles cannot reconstruct:
- exact trade sequence;
- bid/ask depth changes;
- intrabar path;
- event order within a bar;
- queue position or order-book liquidity;
- provider stream gaps and receipt latency.

A backtest using bars must declare the resolution and execution assumptions. It must not claim tick-level, queue-aware or exchange-event replay. When a strategy requires intrabar sequence that candles do not preserve, the result is an approximation or UNKNOWN for that requirement.

## 5. Field-specific freshness and strategy/risk admission

A single feed-health boolean is insufficient. Keep at least:
- connection liveness;
- subscription completeness;
- last raw frame receive age;
- last per-instrument market observation receive age;
- provider event/last-trade time age;
- exchange timestamp age where present;
- book/depth observation age;
- OI observation age;
- Greek observation age;
- source snapshot age;
- decoder/queue/consumer lag;
- stream-gap/history-continuity state.

For example:
- an instrument's last-trade time can be old while the best bid/ask has been recently updated;
- an active heartbeat with no per-instrument observation is not evidence of fresh depth;
- a recent local receive time with an old provider event time indicates delayed data;
- a recent LTP update does not prove option Greeks/OI were recalculated at the same time unless the provider timestamp semantics establish that;
- a REST quote snapshot and WebSocket quote are separately timed, non-atomic observations.

Freshness thresholds must be configured by product, segment, session phase, field and use-case. Liquid index futures during continuous session, an illiquid stock option, pre-open indicative equilibrium price and post-close reference data have different expected update patterns. Do not impose one global timeout that flags illiquid contracts as disconnected or treats an old price as current.

For order admission:
- a risk-increasing action must not rely on stale/unavailable fields required for pricing, margin, delta or position controls;
- a risk-reducing/cancel request may have a different safe path, but its actual result and residual exposure remain unknown until broker/order/trade reconciliation;
- if no reliable freshness/completeness bound exists for a field required by the rule, the relevant gate is UNKNOWN;
- a stale provider quote must not be silently replaced by another provider's quote without recording the separate source and time, and without a defined cross-provider selection policy.

## 6. Raw data and decoder integrity

Kite binary packets, Upstox V3 Protobuf messages and Dhan little-endian packets require provider-specific decoders.

A market-data capture record should preserve:
- raw WebSocket frame/packet bytes (or immutable object/hash and storage pointer);
- frame length and provider packet/message type;
- provider/API/feed schema version;
- Protobuf file hash or binary layout profile;
- provider instrument alias and canonical identity crosswalk version;
- connection and subscription epoch;
- local receive wall time and monotonic time;
- decoder version and parsed field values;
- decode errors/unknown fields and packet offsets;
- backpressure, queue overflow, drop and reconnect metrics.

Unknown feed types, short/oversized packets, invalid length headers, unknown Protobuf fields that change required semantics, invalid timestamp ranges, unknown segment/security IDs and unsupported schema versions must be preserved and rejected/quarantined, not parsed with a best-effort old layout.

## 7. Additional requirements for PX-025

### R-163 — Market time domains remain distinct

Every market-data record MUST distinguish provider last-trade/event time, explicit exchange timestamp, provider message/generated/received time, local receive time, local processing time and candle interval time where each is available. One generic timestamp field MUST NOT substitute for these domains.

### R-164 — Raw and normalized timestamps are both preserved

The system MUST preserve the raw timestamp bytes/value/string, provider unit/epoch profile, normalized UTC instant, conversion/version and timezone/calendar interpretation. Invalid, ambiguous or unknown timestamp units MUST remain UNKNOWN; no seconds/milliseconds guess may be used to authorize a risk-sensitive decision.

### R-165 — Local wall and monotonic clock observations are separate

The ingest service MUST capture local UTC receive time and local monotonic receive/process durations separately. Clock synchronization state/offset/uncertainty SHOULD be recorded. Monotonic clock values MUST NOT be compared across hosts or process restarts as a shared timebase.

### R-166 — Field-specific timestamp meaning is preserved

Last trade time, exchange timestamp, feed-message timestamp, quote/depth observation, OI, Greeks and market-status timestamp MUST retain their source-defined meanings. A timestamp for one field MUST NOT be copied to another field unless the provider schema explicitly says they share the same observation time.

### R-167 — Candle timestamp semantics are provider-specific

Historical candle records MUST preserve interval size, timestamp raw value, timestamp meaning (start/end/label/UNKNOWN), exchange session/calendar and source API version. A candle timestamp MUST NOT be shifted or assumed to mean the same boundary across providers without documented evidence.

### R-168 — Connection heartbeat is not instrument-data freshness

The system MUST represent socket liveness, heartbeat/ping-pong health, subscription status and per-instrument/per-field observation freshness separately. A heartbeat MUST NOT be interpreted as proof that every instrument or required field is current.

### R-169 — Reconnect snapshot is not missed-event replay

A new connection/snapshot MUST be recorded under a new connection/subscription epoch. Unless the provider documents a replay cursor and completion guarantee, the stream gap's event-history completeness MUST remain UNKNOWN even after current state is resynchronized.

### R-170 — Feed event ordering is not inferred from local arrival order

The adapter MUST preserve packet order as received locally but MUST NOT claim this is exchange causal order without a provider sequence or documented ordering contract. Timestamp collisions, out-of-order arrival and duplicate values MUST not be deduplicated solely by timestamp/price/quantity.

### R-171 — Decoder schema, binary encoding and price scale are pinned

Every decoded frame MUST retain provider/feed version, Protobuf or binary-layout version/hash, endianness, field scale, decoder version and raw frame provenance. Unknown/short/malformed packets MUST be quarantined; no best-effort old decoder fallback may promote a risk-sensitive quote.

### R-172 — Historical coverage and retrieval limits are recorded

Every historical-data acquisition MUST preserve provider/API version, instrument identity/alias, interval, requested and returned date ranges, documented retention/retrieval limits, missing periods and response provenance. An empty/partial response MUST NOT be represented as a complete history without validation.

### R-173 — Expiry-specific instrument identity is preserved in history

Historical market observations MUST retain the actual dated futures/options contract identity and provider alias used at the time. Expired tokens/aliases MUST remain available in the historical crosswalk; a current contract token MUST NOT be substituted for an expired contract without an explicit historical continuous-data rule.

### R-174 — Continuous-series construction is explicit and reproducible

Any continuous futures series MUST be a derived dataset with declared contract chain, roll trigger/time, roll reference price, gap/adjustment method, expiry/calendar rule, volume/OI treatment, corporate-action handling and builder version. A provider continuous endpoint MUST NOT be presumed to implement a universal adjusted roll methodology.

### R-175 — OHLCV candles do not claim tick-event completeness

A bar-based dataset or backtest MUST declare its resolution and intrabar assumptions. OHLCV data MUST NOT be represented as full trade sequence, order-book, queue-position or tick-level replay.

### R-176 — Data pipeline loss and completeness are observable

The ingest pipeline MUST measure frame/packet count, bytes, decode failures, subscription gaps, queue depth, processing lag, overflow/dropped messages, reconnect gaps and consumer lag. A locally detected loss MUST invalidate affected event-history completeness and relevant downstream decisions until repaired/reconciled.

### R-177 — Freshness policy is field, product and session specific

Freshness thresholds MUST be configured for the required data field, product/segment, market phase and decision use-case. Old last-trade time alone MUST NOT classify a recently updated book as stale; a recent heartbeat alone MUST NOT classify an old/missing book as fresh.

### R-178 — Cross-provider quotes remain asynchronous observations

Quote snapshots from different providers MUST retain separate source, event/message/receive timestamps and instrument aliases. They MUST NOT be treated as an atomic cross-provider market snapshot or averaged/merged without a documented selection and timestamp-alignment policy. Material unexplained disagreement MUST produce a quality exception for risk-sensitive use.

## 8. Deterministic acceptance scenarios

These extend AT-001 through AT-310. Use synthetic feed frames, Protobuf messages, historical candle fixtures, fake clocks and deterministic connection events only.

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-311 | Kite quote packet has different last-traded and exchange timestamps | Preserve both raw fields and normalize under the Kite schema; do not collapse them |
| AT-312 | Kite index packet arrives | Parse the index-specific shorter layout and exchange timestamp; do not use tradable-instrument offsets |
| AT-313 | Kite price is encoded as int32 paise for equities and currency uses the documented different divisor | Apply segment-specific scale once; preserve raw integer and scale version |
| AT-314 | Upstox V3 message has old `ltpc.ltt` but recent `currentTs` | Represent old last-trade time and recent received-tick time separately; freshness is field-specific |
| AT-315 | Upstox `market_info` message has generated `currentTs` and segment status | Preserve message-generation time and market-status scope separately from live tick time |
| AT-316 | Upstox V3 connection emits market_info, then snapshot, then live update | Record bootstrap ordering and connection epoch; snapshot is not replay of missed historical messages |
| AT-317 | Dhan v2 LTT integer arrives with little-endian binary header | Decode under pinned Dhan v2 layout; preserve raw LTT/unit and local receive time separately |
| AT-318 | Provider has no documented separate exchange timestamp in the reviewed packet layout | Leave exchange timestamp absent/UNKNOWN; do not copy local receive time or LTT into that field |
| AT-319 | Kite sends heartbeat while no instrument quote has changed | Mark connection alive; per-instrument freshness remains based on actual observations |
| AT-320 | Dhan ping arrives every 10 seconds and pong is not returned for more than 40 seconds | Record disconnect per provider contract; mark affected feed epoch gap and resubscribe/resynchronize |
| AT-321 | Upstox periodic ping/pong maintains socket while one requested instrument has no feed observation | Keep socket alive but instrument field quality is independently stale/UNKNOWN according to configured policy |
| AT-322 | Illiquid instrument's last trade is old but its bid/ask book updates recently | Do not label whole instrument stale solely from LTT; assess book freshness separately |
| AT-323 | Active instrument receives a delayed packet with older provider event time after a newer packet | Preserve both; do not overwrite newer accepted state blindly or invent causal order |
| AT-324 | Two valid updates share same timestamp, LTP and quantity but differ in depth | Retain both observations; no timestamp-price deduplication |
| AT-325 | Two opposing provider observations arrive at different times and disagree on LTP/depth | Preserve provider/source/time; do not merge into an atomic best quote |
| AT-326 | WebSocket disconnects and reconnects with a current snapshot but no replay cursor | Current-state resync may pass its freshness gate; missed event history remains UNKNOWN |
| AT-327 | Local receive queue overflows and frames are dropped while socket remains connected | Record local data loss, invalidate event continuity and mark dependent feed quality UNKNOWN |
| AT-328 | Decoder receives unknown packet type or unexpected Protobuf schema revision | Preserve raw bytes and decoder error; quarantine rather than parse with old field map |
| AT-329 | Timestamp numeric value is ambiguous between seconds and milliseconds due unknown provider schema | Keep raw value, mark unit UNKNOWN and block timestamp-dependent risk decision |
| AT-330 | Local wall clock jumps but monotonic timer advances correctly | Use monotonic duration for processing latency; record clock anomaly and do not reorder events by wall clock alone |
| AT-331 | Upstox historical candle timestamp is returned for a one-minute interval | Treat it as the documented candle start time; preserve timezone offset/source interval |
| AT-332 | Dhan historical candle returns epoch timestamp with no explicit start/end semantic in the reviewed contract | Preserve raw epoch and mark candle-boundary semantic according to verified source profile; do not assume Upstox meaning |
| AT-333 | Kite historical candle uses an ISO timestamp with +0530 offset | Preserve explicit offset and exchange session date; do not strip timezone into machine-local time |
| AT-334 | Kite continuous=1 returns daily data across expired NFO/MCX futures contracts | Record provider continuous-series source and exact query contract; do not infer an adjusted/back-adjusted series or intraday expired-token history |
| AT-335 | Expired derivative token is missing from the current provider master but exists in a cached historical master | Resolve historical observations using the effective historical alias; do not substitute current expiry token |
| AT-336 | Historical request hits Upstox one-month intraday retrieval limit or Dhan 90-day per-request limit | Split/record date windows and coverage; do not claim requested full history if pages are missing |
| AT-337 | Historical response omits one trading session or has duplicate candle timestamps | Create gap/duplicate quality exception; no complete-history PASS |
| AT-338 | Candle OHLC matches but provider interval boundaries differ | Keep distinct time buckets; no silent shift or false cross-provider equality |
| AT-339 | Strategy asks for tick/order-book replay but only minute candles are stored | Mark requirement unsupported/approximate; do not generate fictitious intrabar sequence |
| AT-340 | Option LTP updates but OI/Greeks have no documented matching observation time | Keep LTP and OI/Greeks freshness separate; do not stamp all fields with LTT |

PX-025 now contains **178 normative requirements (R-001–R-178) and 340 proposed acceptance scenarios (AT-001–AT-340)**. These are proposed tests only; no market feed, data request, decoder, time-series store or backtest engine was executed.

## 9. Open questions and evidence limitations

1. No current broker feed was connected, so actual delivery jitter, packet reordering, reconnect behaviour, local queue pressure and field update cadence were not measured.
2. No official provider feed schema guarantees an exchange sequence/replay cursor in the reviewed retail feed pages. Other licensed/exchange-native feeds may have different transport contracts.
3. The exact timestamp units/epoch representation for every provider/API version must be pinned to the current Protobuf/binary schema and validated with official test fixtures; this report does not normalize by numeric-guessing.
4. Dhan's packet layout labels LTT as EPOCH but the reviewed public page does not expose a second per-message exchange timestamp field. Field-level update times for every quote/depth/OI value remain provider-specific/open.
5. Kite's historical page does not fully define candle start/end semantics for every interval in the text inspected. Do not transfer Upstox's explicitly documented start-time definition to Kite.
6. Dhan's historical page documents epoch candle timestamps but does not explicitly specify interval start/end semantics in the reviewed section.
7. Provider history retention/range limits are documented per API but actual coverage may differ by instrument, expiry, segment, entitlement or provider-side retention changes.
8. No actual OHLCV, tick or depth datasets were requested or compared. Provider values, correction policy, auction treatment and final candle-close timing remain unmeasured.
9. Exact current market-session/holiday schedules must be source-versioned from NSE/BSE circulars and calendars; local wall-clock assumptions are not sufficient.
10. A strategy-specific staleness threshold cannot be fixed from provider documentation alone; it must be derived from the decision use-case, instrument liquidity, session phase and empirical validation.

## 10. Research decisions and non-authorization

- **ACCEPT:** separate exchange/event, last-trade, provider message, local receive, local processing and candle interval times.
- **ACCEPT:** preserve raw frame and timestamp provenance; provider-specific binary/Protobuf decoder versions and price scales are pinned.
- **ACCEPT:** heartbeat/connection liveness and per-instrument/per-field freshness are independent.
- **ACCEPT:** reconnect snapshots restore current state only; absent a documented replay cursor, event-history completeness remains UNKNOWN.
- **ACCEPT:** exact contract identity/alias at observation time is part of every market-data record.
- **ACCEPT:** actual contract-level futures history and continuous derived series remain separate; continuous roll methodology must be reproducible.
- **ACCEPT:** OHLCV bars do not claim tick/order-book/queue-level replay.
- **DEFER:** production feed connectors, binary/protobuf decoders, persistent tick store, clock monitor, freshness policy and continuous-series builder until current schemas and sample payloads can be safely obtained and tested.
- **NOT AUTHORIZED:** broker credentials, data-feed subscriptions, market-data API calls, sandbox/production orders, code changes, paid services, PR or merge to `main`.

**Final status:** PX-037 market-data time semantics, feed integrity, historical candles and contract continuity research documented. PX-025 expanded to 178 requirements and 340 proposed acceptance scenarios. No market data was fetched from a broker; no parser or integration was implemented.
