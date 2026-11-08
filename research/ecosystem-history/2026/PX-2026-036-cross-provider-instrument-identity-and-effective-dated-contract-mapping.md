# PX-2026-036 — Cross-provider instrument identity and effective-dated contract mapping

**Research date:** 2026-11-08  
**Status:** official provider identity documentation reviewed; current daily provider master files not downloaded or parsed  
**AlgoX area:** instrument identity / broker adapters / exchange contract master / order admission / historical replay  
**Providers:** Zerodha Kite Connect, Upstox API, DhanHQ API v2  
**Inputs:** PX-023, PX-028, PX-034, PX-035 and PX-025 requirements R-119–R-147  
**Mode:** research and requirements specification only  
**Non-goals:** no broker/account access, API call, sandbox/production order, provider master download, code implementation, paid service, PR or merge to `main`

## Executive finding

The three provider instrument masters expose different identity models and lifecycle rules. A contract must not be identified by a symbol or numeric token alone.

The key source findings are:

- **Kite:** its consolidated gzipped CSV is generated daily; the `last_price` field in that master is not real-time. Kite explicitly warns that exchange instrument tokens may be reused for different derivative contracts after expiry and recommends exchange + trading symbol rather than numeric token as the storage key.
- **Upstox:** its current documentation recommends JSON over CSV, says `instrument_key` uniquely identifies an instrument, and warns that `exchange_token` may be reused after expiry. Its JSON master is split into BOD instruments and distinct suspended, MTF, MIS, mutual-fund and global-instrument datasets. The files refresh daily at around 6 AM and only refresh intraday when needed; the BOD master for the next trading day excludes delisted stocks and expired contracts.
- **Dhan:** it publishes compact and detailed scrip-master CSVs and a segmentwise instrument-list endpoint. The detailed master exposes exchange, segment, ISIN, underlying security ID/symbol, symbol name, instrument type, series, lot, expiry, strike, option type, tick, expiry flag and trading controls. A Dhan `securityId` must remain scoped by exchange segment and source validity; the documentation does not establish a universal cross-provider or all-time identity.

**Decision:** AlgoX should maintain an immutable internal canonical identity for each underlying and each listed contract, with independent provider aliases scoped by provider, API/schema version, exchange/segment and effective interval. Exact source-supported matches only can create orderable aliases. Historical aliases must remain resolvable for old orders/trades, but stale or expired aliases must not authorize a current order.

**Data limitation:** the actual Kite, Upstox and Dhan daily instrument master files for 8 November 2026 were not acquired or parsed. This document closes several official schema/identity-policy questions but does not claim a validated row-level crosswalk or provider-master parser.

## 1. Provider identity surfaces

### 1.1 Zerodha Kite Connect

Kite documents the following instrument master characteristics:

- `GET /instruments` returns a gzipped CSV dump of instruments across exchanges.
- The dump is generated once daily, and the included `last_price` is not real-time.
- The fields include `instrument_token`, `exchange_token`, `tradingsymbol`, `name`, `expiry`, `strike`, `tick_size`, `lot_size`, `instrument_type`, `segment` and `exchange`.
- Kite says the instrument token is the numerical identifier used for live market-data subscription.
- It expressly warns that exchanges may reuse instrument tokens for different derivative instruments after each expiry and recommends exchange + `tradingsymbol` as the unique storage key instead of the numeric token.
- Quote APIs use the `exchange:tradingsymbol` combination; requested keys can be absent when an instrument has no available data or has expired.

**Implication:** `instrument_token` is a Kite market-data alias, not a durable canonical contract identity. `exchange_token` is a separate exchange-issued value and must not be silently equated to the Kite token. Exchange + trading symbol is the provider's recommended lookup/storage combination, but AlgoX should still retain expiry, strike, option type, segment, lot/tick and source date to detect changes and historical ambiguity.

Sources:
- https://kite.trade/docs/connect/v3/market-quotes/
- https://kite.trade/docs/connect/v3/websocket/

### 1.2 Upstox

Upstox's current Instruments page makes several explicit recommendations:

- use JSON instrument files instead of CSV for enhanced structure and future scalability;
- use `instrument_key` as the unique identifier for an instrument;
- do not use `exchange_token` as a durable unique ID because the exchange may reuse it after expiry;
- BOD JSON contains instruments available at the beginning of the day;
- suspended instruments are supplied in a separate file;
- MTF and MIS eligibility are supplied in separate files;
- mutual-fund and global instruments are also separate data sets;
- instrument files refresh daily at around 6 AM and only refresh intraday when needed;
- the BOD file for the next trading day does not include delisted stocks or expired contracts.

The JSON schema documents relevant attributes including segment, exchange, ISIN, instrument type, `instrument_key`, lot size, freeze quantity, exchange token, tick size, trading symbol, security type and CAS eligibility. Derivative records include expiry, underlying symbol/key, strike price, option type, lot size, freeze quantity and underlying type.

**Implication:** `instrument_key` is the preferred Upstox alias within its documented API contract, but it remains a provider alias, not AlgoX's canonical ID. The separate suspended/MTF/MIS files are meaningful eligibility inputs and must not be discarded after parsing only the BOD master. A file's daily refresh schedule is not proof of an atomic snapshot or that it can never receive an intraday correction.

The current documentation deprecates CSV in favour of JSON. A new adapter should use the JSON master and pin a schema profile; legacy CSV should be read only for historical migration/reconciliation under its own schema.

Source:
- https://upstox.com/developer/api-documentation/instruments/

### 1.3 DhanHQ API v2

Dhan documents two downloadable master files:
- compact: `https://images.dhan.co/api-data/api-scrip-master.csv`;
- detailed: `https://images.dhan.co/api-data/api-scrip-master-detailed.csv`.

It also documents a segmentwise list endpoint:
- `GET /v2/instrument/{exchangeSegment}`.

The detailed master exposes:
- exchange ID and segment;
- ISIN;
- exchange instrument name/type;
- underlying security ID and underlying symbol for derivatives;
- symbol name and display name;
- series;
- lot size;
- expiry date;
- strike price and option type;
- tick size and expiry flag;
- bracket/cover-order capability flags;
- ASM/GSM status and buy/sell indicator;
- cover/bracket margin/range fields.

The documentation defines ISIN as a 12-character alphanumeric identifier for instruments. It does not state that the Dhan `securityId` is globally unique across all segments, all time, providers or derivative contract versions. Therefore an adapter must preserve the raw ID together with the exchange segment and the exact master version/date from which it was obtained.

**Implication:** the detailed master is richer than the compact one for contract/eligibility mapping. The compact master can be retained as a separate source variant, but must not be treated as an identical schema. Dhan's display symbol is not a durable canonical identity; the source also provides underlying and contract attributes which must be used in exact matching.

Source:
- https://dhanhq.co/docs/v2/instruments/

## 2. Canonical identity model

### 2.1 Separate the economic instrument from provider aliases

A proposed canonical model has two separate entities.

**CanonicalUnderlying**
- immutable internal ID;
- asset class and instrument family;
- official exchange/index identity;
- ISIN where applicable and verified;
- source-specific security identifiers and effective intervals;
- historical display-symbol/name aliases;
- corporate-action and successor/predecessor relationships.

**CanonicalContract**
- immutable internal ID;
- exchange, segment and venue/admission type;
- canonical underlying ID;
- equity/index/future/option contract family;
- contract/series type;
- expiry date and expiry flag/type;
- strike as exact decimal for options;
- option type;
- market lot/multiplier and exchange quantity unit;
- tick size and freeze quantity;
- settlement mode and exercise style where applicable;
- contract status and effective interval;
- source master/circular version and provenance;
- predecessor/successor link for adjusted, expired or transformed contracts.

**ProviderInstrumentAlias**
- provider and API version;
- source master family/variant (Kite CSV, Upstox JSON BOD, Upstox suspended/MIS/MTF, Dhan compact/detailed/segmentwise);
- provider identifier (`instrument_token`, `instrument_key`, `securityId`, etc.);
- provider exchange/segment scope;
- provider symbol/display name as observed;
- canonical underlying/contract ID;
- source file hash, schema/parser version and row reference;
- observed/publication/effective timestamps;
- validity interval;
- provider eligibility state and route capability;
- mapping method and evidence;
- status: active, expired, suspended, retired, superseded, ambiguous or quarantined.

A provider alias is not the canonical instrument. Mapping corrections must not rewrite historical trades or past admission decisions that used the earlier alias.

### 2.2 Underlying identity

For listed equity, ISIN is a stronger cross-venue security key than a display symbol where the source provides it and the mapping is verified. It is not sufficient to identify:
- the exchange/segment through which an order is placed;
- the venue/admission route;
- a derivative expiry/strike/option type;
- the contract version before or after a corporate action.

For indices, use an official exchange/index identity; do not invent an ISIN.

Where no verified stable underlying key exists, retain provider/exchange-specific IDs and require a controlled mapping. Company name, index display name or trading symbol alone is not an authoritative crosswalk.

### 2.3 Derivative contract identity

The exact derivative contract identity must include:
- exchange and segment;
- venue/admission type;
- canonical underlying;
- futures/options family and instrument type;
- expiry date and expiry/series type;
- exact strike for options;
- option type;
- source/effective contract-master version;
- quantity unit/lot and other contract attributes used in validation.

A row matching on symbol and expiry but not strike/option type is ambiguous. Matching a strike in one exchange segment to the same strike in another venue is not automatically the same route.

### 2.4 Exact normalization

Strike and other price-like contract terms must be parsed from raw source text into exact decimal semantics. Binary floating-point equality is not suitable for identity resolution. Expiry dates must be interpreted as exchange trading dates in the applicable exchange calendar/timezone; conversion to local machine timezone must not shift the contract date.

Preserve both raw values and normalized values with the parser version.

## 3. Source-master ingestion and crosswalk construction

1. Acquire each provider master independently; do not synthesize one provider's alias from another provider's row.
2. Record provider, API/schema version, file family, URL/channel, capture time, publication/effective time where supplied, byte size and hash.
3. Parse using the exact schema profile for that source variant.
4. Preserve raw IDs, symbols, segment codes, expiry, strike, lot/tick/freeze and status fields.
5. Resolve underlying identity through ISIN or official index/security identity where available; otherwise keep the row unverified.
6. Resolve the complete exchange/segment/venue/contract key.
7. Compare lot, quantity unit, tick, freeze, status, settlement mode and expiry attributes against the effective exchange contract data.
8. Match only if exactly one canonical contract satisfies the required identity and attribute rules.
9. Preserve unmatched, stale, suspended and ambiguous rows; do not drop them or fuzzy-map them.
10. Create a provider-scoped alias record with effective validity and source evidence.
11. Promote the provider-to-canonical crosswalk atomically only after required source masters are complete and validated.
12. Retain prior aliases for historical order/trade/market-data replay; retire them for new orders when the source validity ends.

### 3.1 Matching outcomes

- `EXACT_MATCH`: exact identity attributes agree and exactly one canonical record is valid.
- `MATCH_WITH_VERIFIED_ALIAS`: an official source mapping explicitly links provider alias to the same canonical contract.
- `UNMATCHED`: no canonical record satisfies exact identity.
- `AMBIGUOUS`: more than one possible canonical contract remains.
- `ATTRIBUTE_CONFLICT`: identity candidates appear to match but lot/tick/freeze/units/venue/status conflict.
- `STALE_ALIAS`: provider alias validity has ended or source is superseded.
- `SUSPENDED`: source explicitly marks the instrument unavailable/suspended.
- `UNKNOWN`: source file/schema/effective date or underlying identity is unresolved.

Only EXACT_MATCH or MATCH_WITH_VERIFIED_ALIAS may proceed to the PX-033 admission gates, and those results still do not bypass contract/session/provider validation.

### 3.2 No fuzzy matching for order authorization

The following are not sufficient authorization keys by themselves:
- trading symbol or display name;
- root symbol or option-chain label;
- expiry alone or strike alone;
- numeric equality between provider token/security IDs;
- same lot size or tick size;
- substring/Levenshtein similarity;
- a provider search UI result without a source-master row.

Fuzzy search may help an operator find possible candidates for manual investigation, but it must never auto-create an orderable alias.

## 4. Provider-specific lifecycle and eligibility

### 4.1 Kite

- Ingest the daily instrument dump as a new source snapshot.
- Do not use its `last_price` as live price data.
- Do not retain `instrument_token` as an unscoped forever-key: Kite warns tokens can be reused across expired derivative contracts.
- Use exchange + tradingsymbol as Kite's recommended source lookup key, while still retaining complete contract terms and source date.
- Missing quote keys and expired instrument responses must be handled as absent/unavailable observations, not substituted by another symbol.

### 4.2 Upstox

- Prefer current JSON instrument files; the documentation marks CSV as deprecated.
- Preserve `instrument_key` as the provider's preferred unique API alias.
- Never use `exchange_token` as a durable identity; it may be reused after expiry.
- Include the distinct BOD, suspended, MTF and MIS datasets when the corresponding eligibility question is being answered.
- The daily 6 AM refresh is a documented approximate schedule, not a guarantee that a file is complete, atomic or unchanged for the rest of the day.
- A next-day BOD file omitting expired/delisted rows must not erase historical identity; retain prior aliases for replay and reconciliation.

### 4.3 Dhan

- Keep compact and detailed scrip-master variants separately versioned.
- Prefer detailed records when resolving derivatives, lot/tick/expiry/strike/option and order-eligibility attributes.
- Preserve both underlying security ID and the derivative's own security ID.
- Preserve exchange segment alongside security ID; never query or resolve a raw Dhan ID without its segment/source context.
- Keep ASM/GSM, buy/sell indicator and bracket/cover eligibility as provider observations, not general market-tradability conclusions.

## 5. Corporate action, expiry and alias lifecycle

- An expired contract remains available for historical trades, fills and replay but cannot be selected for current order submission.
- A corporate action that changes strike, lot, multiplier, quantity or contract terms creates an effective-dated adjusted/successor contract relationship; it must not overwrite the predecessor.
- A merger forced-closeout is an exchange-originated lifecycle event, not an alias rename.
- Provider alias changes across daily masters must be recorded as versioned transitions. Old aliases remain valid only for their historical interval.
- If one alias appears to identify two canonical contracts in overlapping validity intervals, quarantine it.
- If the same display symbol later identifies another expiry or venue, do not inherit the older canonical identity merely because the string matches.
- The research model does not assert that any specific provider has reused a Dhan security ID. The reuse guarantee is explicitly documented for Kite instrument tokens and Upstox exchange tokens; other identifier lifecycle guarantees remain provider-specific and must not be assumed.

## 6. Data quality and audit invariants

The crosswalk must answer:
- which canonical contract a strategy/backtest or order referred to;
- which provider identifier was used at that time;
- which provider master and exchange contract row supported the alias;
- which file hashes/schema/parser versions were active;
- when the alias became effective and when it was observed;
- whether it was available, suspended, MTF-only, MIS-eligible or otherwise restricted;
- which exact lot/tick/freeze/underlying/expiry/venue attributes were compared;
- whether the mapping was exact, verified, ambiguous or quarantined.

Required integrity checks include:
- duplicate provider IDs within overlapping provider/segment/effective scopes;
- one alias mapping to multiple canonical contracts;
- one canonical contract mapped to incompatible provider segment/venue;
- underlying ISIN/security ID mismatch;
- expiry/strike/option-type collision;
- lot/tick/freeze/unit mismatch;
- stale BOD/suspended/MTF/MIS state;
- expired alias used for a new order;
- unresolved corporate-action predecessor/successor transition.

Any identity, venue, expiry, option type, quantity unit or lot mismatch must block an order-admission PASS.

## 7. Additional requirements for PX-025

### R-148 — Canonical instrument identity is independent of provider aliases

The system MUST assign an internal immutable canonical identity to each underlying/security and listed contract. Broker tokens, provider keys, symbols and exchange-specific IDs MUST be stored as provider-scoped aliases, not used as a universal canonical ID.

### R-149 — Provider aliases are namespaced by provider, API version and segment

Every provider alias MUST retain provider identity, API/schema version, exchange/segment scope and raw provider identifier. Numeric equality or string equality across providers MUST NOT be treated as evidence that two aliases identify the same contract.

### R-150 — Alias validity is effective-dated

Every alias MUST retain source publication/observation time and its valid-from/valid-to interval. Retired, expired or superseded aliases MUST remain available for historical reconciliation but MUST NOT authorize current order submission.

### R-151 — Underlying identity uses authoritative security/index mapping

Equity underlyings SHOULD be mapped through ISIN where supplied and verified. Indices MUST use an official exchange/index identity. If a stable underlying key is missing or ambiguous, the mapping MUST remain UNKNOWN; display company/index name alone is insufficient.

### R-152 — Derivative identity requires complete contract terms

A derivative canonical identity MUST include exchange, segment, venue/admission type, underlying identity, future/option family, expiry, strike, option type and applicable series/type fields. A match on symbol/root/expiry alone MUST NOT authorize a contract.

### R-153 — Strike, expiry and contract terms use exact normalization

Strike and price-like contract terms MUST use exact-decimal normalization. Expiry must be interpreted using the exchange trading date/calendar without timezone drift. Raw source values and normalized values MUST both be retained with parser version.

### R-154 — Alias mapping requires exact, unique source-supported resolution

A provider alias MAY be linked to a canonical contract only when the exact required identity attributes agree and exactly one candidate is valid for the effective interval. Fuzzy symbol/name/token matching MUST NOT produce an orderable alias.

### R-155 — Contract attributes are cross-checked after identity match

Even when identity keys match, lot/multiplier, quantity unit, tick, freeze, settlement mode, expiry/status and venue attributes MUST be compared. Any unexplained conflict MUST result in ATTRIBUTE_CONFLICT/UNKNOWN and block order admission.

### R-156 — Provider instrument masters are separately versioned inputs

Kite, Upstox and Dhan instrument masters MUST be ingested and versioned independently, with source URL/channel, capture/effective time, hash, schema and parser version. One provider's master MUST NOT be substituted for another provider's alias or capabilities.

### R-157 — Venue and Admission Type are part of the canonical route

A contract's exchange/venue admission type MUST be part of mapping and order-route validation. An otherwise identical underlying/expiry/strike on a different venue or admission path MUST remain a distinct route and MUST NOT be silently substituted.

### R-158 — Corporate-action contract transitions are linked, not overwritten

Changes to strike, lot, multiplier, expiry, quantity or contract terms from a corporate action MUST create an effective-dated successor/adjusted contract relationship with source evidence. The predecessor identity and all historical provider aliases MUST remain immutable for historical reconciliation.

### R-159 — Expired/suspended contracts remain historical but non-tradable

Expired, suspended, delisted or retired contract aliases MUST remain resolvable for old orders/trades but MUST fail current order-admission validity. Presence in a historical source file cannot make the contract currently tradable.

### R-160 — Alias collisions and overlapping validity are quarantined

If one provider alias maps to more than one canonical contract over an overlapping validity interval, or if a provider alias changes identity without a source-supported effective transition, the mapping MUST be quarantined as AMBIGUOUS/CONFLICT. No arbitrary first/last row selection is permitted.

### R-161 — Crosswalk snapshots are atomic and reproducible

A promoted provider-to-canonical crosswalk MUST retain the exact exchange and provider source files, hashes, schema/parser/mapping-policy versions, row references, effective times, validation report and decision trace. A partial provider master set MUST NOT be combined with a previous crosswalk to claim current complete mapping.

### R-162 — Unknown identity blocks order submission

If the underlying, contract, venue, provider alias, lot/unit or effective-date mapping is missing, stale or contradictory, the order-admission gate MUST return UNKNOWN/blocked. It MUST NOT guess a security ID, reuse a stale token or fall back to a similar symbol.

## 8. Deterministic acceptance scenarios

These extend AT-001 through AT-280. Use synthetic exchange/provider instrument masters and fake aliases only.

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

## 9. Open questions and evidence limitations

- The daily Kite, Upstox and Dhan instrument-master files for 8 November 2026 were not downloaded or parsed.
- Upstox's official page provides a unique `instrument_key` recommendation and says `exchange_token` may be reused; its daily refresh schedule is approximate, not proof of atomicity.
- Kite explicitly warns of instrument-token reuse after derivative expiry; its daily `last_price` is not real-time.
- Dhan publishes compact/detailed/segmentwise masters, but a global/all-time uniqueness guarantee for raw `securityId` was not established.
- No provider-to-exchange row-level crosswalk was built because the exact daily source files have not been inspected.

Until these gaps are closed, unverified aliases remain UNKNOWN and cannot authorize new orders.

## 10. Research decisions and non-authorization

- **ACCEPT:** separate canonical underlying/contract identity from provider-specific aliases.
- **ACCEPT:** namespaced provider alias; use Upstox `instrument_key` as its documented preferred alias, but never use `exchange_token` as a durable unique key.
- **ACCEPT:** retain Kite daily master snapshots and do not treat its `last_price` as live; do not use `instrument_token` as an unscoped forever-key.
- **ACCEPT:** keep Upstox BOD, suspended, MTF, MIS, mutual-fund and global files as separate eligibility datasets; use JSON over deprecated CSV.
- **ACCEPT:** preserve Dhan compact/detailed/segmentwise schemas separately; use detailed identity/contract fields for derivatives.
- **ACCEPT:** exact complete contract matching; no fuzzy symbol mapping or cross-provider token equivalence.
- **ACCEPT:** effective-dated aliases and historical retention; expiry/corporate-action transitions do not overwrite old identities.
- **DEFER:** production crosswalk schema/importer and exact provider mapping rows until current provider master files are acquired and validated.
- **NOT AUTHORIZED:** broker API calls, account/sandbox/production access, orders, code changes, paid services, PR or merge to `main`.

**Final status:** PX-036 cross-provider instrument identity and effective-dated contract mapping research documented. PX-025 expanded to 162 requirements and 310 proposed acceptance scenarios. Daily provider master files remain uninspected; no parser or broker integration was implemented.
