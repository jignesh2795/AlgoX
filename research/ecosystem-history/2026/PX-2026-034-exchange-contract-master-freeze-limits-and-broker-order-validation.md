# PX-2026-034 — Exchange contract master, freeze limits and broker order validation

**Research date:** 2026-11-08  
**Status:** official specification and broker API comparison completed; current daily contract file not downloaded  
**AlgoX area:** instrument/contract master / exchange order validation / freeze quantity / provider adapter validation  
**Scope:** NSE equity derivatives and Zerodha Kite Connect, Upstox V3 and DhanHQ API v2  
**Inputs:** PX-025 requirements baseline, PX-026 sliced/compound order recovery, PX-029 expiry/settlement, PX-032 position limits and PX-033 independent admission gates  
**Mode:** research and requirements specification only  
**Non-goals:** no broker or exchange API call, no account/sandbox/production interaction, no order, no implementation, no paid service, no PR or merge to `main`

## Executive finding

An order can pass portfolio, margin and position-limit checks but still be invalid at the exchange or broker boundary. The admission gate G-10 in PX-033 therefore requires a separate, date-effective contract/request validation layer.

This audit identifies five independent sources of order validity:

1. **Exchange contract identity:** exact exchange, segment, instrument token/security ID, symbol, expiry, strike, option type and contract family.
2. **Contract mechanics:** market lot/quantity unit, price tick, freeze quantity, listing/trading status, expiry and price range/operating range.
3. **Exchange session/rule constraints:** trading phase, order type, order variety, operating/price range and product/order restrictions.
4. **Broker API contract:** provider-specific required fields, enums, quantity units, validity, AMO semantics, market protection, slicing and request limits.
5. **Current data provenance:** the effective daily contract master/quantity-freeze file, circular revisions, capture date/hash and parser version.

The current NSE equity-derivatives specification publishes different tick and price-range rules for index futures, index options, stock futures and stock options. NSE Circular NSE/FAOP/74469 (29 May 2026) gives an index-specific quantity-freeze schedule effective 1 June 2026 and instructs members to load the updated `contract.gz` and dated `NSE_FO_contract_ddmmyyyy.csv.gz` files. The actual daily contract file for 8 November 2026 was not downloaded or inspected here. Consequently, the circular's June 2026 index table is a source reference, not a substitute for the current daily file.

The broker APIs are not interchangeable:
- Kite exposes variety, product, validity, market protection and automatic slicing fields.
- Upstox V3 exposes a different order schema, DAY/IOC, session-inferred AMO, automatic slicing and a provider-specific market-protection range.
- Dhan exposes its own product/order type/validity/AMO fields and a separate slicing endpoint. Its reviewed regular placement schema does not document the same market-protection field.

**Decision:** an order request must be validated twice: first against the effective exchange contract/session rules, then against the selected broker API version and account permissions. Neither validation proves broker acceptance or execution. Missing or stale contract data, unsupported enums, ambiguous units or unknown limits must return UNKNOWN/REJECT rather than being silently coerced.

## 1. NSE contract master and source versioning

### 1.1 Contract identity and daily data

NSE's equity-derivatives contract-information page points members to downloadable contract files. NSE Circular NSE/FAOP/74469 specifically requires members to load updated `contract.gz` and `NSE_FO_contract_ddmmyyyy.csv.gz` files for the revised index quantity-freeze limits. The current contract specification page also publishes product-level expiry, lot, tick and price-range information.

A future ingestion component must pin:
- source URL and report/file family;
- exchange, segment and trade date;
- file publication/capture time;
- circular/rule version and effective date;
- file bytes, size and cryptographic hash;
- parser version/schema;
- row count and completeness checks;
- the exact row used for the candidate contract.

A symbol string, broker instrument token or UI display name alone is not a durable contract master. The same underlying may have multiple expiries, strikes, option types and instrument identifiers. Symbols/tokens can be changed or replaced when a contract expires, is introduced, adjusted or removed.

Sources:
- NSE Contract Specifications: https://www.nseindia.com/static/products-services/equity-derivatives-contract-specifications
- NSE Contract Information / Derivatives All Reports: https://betanseapi.nseindia.com/static/products-services/equity-derivatives-contract-information
- NSE Circular NSE/FAOP/74469 (29 May 2026): https://nsearchives.nseindia.com/content/circulars/FAOP74469.pdf
- NSE F&O consolidated circular NSE/FAOP/73928 (28 April 2026): linked from NSE exchange communications / contract information.

### 1.2 Quantity units, lot size and freeze quantity are separate

A contract master can describe a market lot, while a broker API request may expect order quantity in exchange units, contracts, lots or a provider-specific integer representation. These are different quantities.

The adapter must keep distinct:
- user-entered lots;
- exchange market-lot size/contract multiplier;
- resulting exchange units;
- broker API request quantity;
- freeze quantity and any resulting child-order quantity.

The same multiplier must not be applied twice. A position quantity must retain the raw broker/exchange unit and the normalized contract count/underlying unit with its conversion rule and version.

Upstox's V3 placement page says commodity quantity is entered in lots, while other F&O and equity quantity is entered in units. The same documentation then says those units are accepted in “multiples of the tick size”; tick size is a price increment, not a quantity unit. This wording is dimensionally inconsistent in the reviewed page. Do not use that phrase as a quantity conversion rule; validate against the exchange contract's lot size and obtain clarification before treating that sentence as normative.

Source:
- https://upstox.com/developer/api-documentation/v3/place-order/

### 1.3 Index quantity-freeze limits

NSE Circular NSE/FAOP/74469, dated 29 May 2026, sets the following index quantity-freeze limits effective 1 June 2026:

| Index | Quantity freeze limit |
|---|---:|
| BANKNIFTY | 900 |
| NIFTY | 1,800 |
| FINNIFTY | 1,800 |
| MIDCPNIFTY | 2,800 |
| NIFTYNXT50 | 600 |

The circular tells members to load updated `contract.gz` and `NSE_FO_contract_ddmmyyyy.csv.gz` files. The actual dated contract file and any subsequent revision for 8 November 2026 were not inspected in this research environment. These figures must not be hard-coded as an evergreen rule; the current exchange file and effective circular take precedence.

For individual-security F&O, the freeze quantity is security/contract specific and must be read from the effective contract file rather than inferred from a generic lot or a broker-side maximum-order hint.

Sources:
- https://nsearchives.nseindia.com/content/circulars/FAOP74469.pdf
- https://www.nseindia.com/static/products-services/equity-derivatives-contract-specifications

### 1.4 Tick size is product-specific

NSE's current contract-specification page distinguishes these tick-size rules:

- **Index futures:** price steps depend on the level of the underlying index (the published table uses ₹0.05, ₹0.10 and ₹0.20 bands).
- **Index options:** ₹0.05 tick.
- **Individual-security futures:** tick size follows the corresponding cash-market contract.
- **Individual-security options:** the published tick size is ₹0.01 where the underlying is below ₹250 and ₹0.05 where the underlying is ₹250 or above.

The values above describe the current published page; the applicable contract row/circular and any later revisions remain the final effective source. A future implementation must not apply one universal ₹0.05 tick to every F&O product.

All price/trigger-price validation must use exact decimal arithmetic. An off-tick price must be rejected or returned as invalid; the adapter must not silently round a user's limit/trigger price to a different price.

Source:
- https://www.nseindia.com/static/products-services/equity-derivatives-contract-specifications

### 1.5 Price range, operating range and market protection are different controls

The NSE specification describes:
- an operating range for futures contracts as a control against erroneous orders; and
- a dynamic price range for options based on contract delta, refreshed daily under the relevant exchange methodology.

These exchange constraints are distinct from a broker's `market_protection` percentage:
- **Exchange price/operating range:** determines whether a submitted price is permitted for that contract/session.
- **Broker market protection:** controls how far a market/stop-market order may execute from a reference price under the broker/exchange API's protection scheme.
- **Limit price:** the user's execution price cap/floor.
- **Stop trigger price:** the condition that activates a stop order.

A 2% broker market-protection value does not authorize a limit/trigger price outside the exchange's effective price range. Likewise, a valid exchange price range does not prove that a market order's broker-side protection setting satisfies the API rules.

The current range must be sourced from the applicable exchange file/rule and time window. A previous day's option band or a static code percentage must not be used as a fallback.

Source:
- https://www.nseindia.com/static/products-services/equity-derivatives-contract-specifications

## 2. Broker request contracts are provider-specific

### 2.1 Zerodha Kite Connect

The reviewed Kite Orders API documents:
- varieties: `regular`, `amo`, `co`, `iceberg`, `auction`;
- order types: `MARKET`, `LIMIT`, `SL`, `SL-M`;
- product values: `CNC`, `NRML`, `MIS`, `MTF`;
- validity: `DAY`, `IOC`, `TTL`, with `validity_ttl` for TTL;
- market protection for MARKET and SL-M: `-1` for automatic protection, or a custom value greater than zero and up to 100;
- `autoslice` to enable automatic slicing above exchange freeze quantity; it is false by default;
- iceberg legs and per-leg quantity, with a documented 2–50 leg range.

The response may expose broker order ID, exchange order ID, parent order ID, order variety, instrument token, quantities and market-protection data. Exchange order ID can remain null for orders that do not reach the exchange.

The adapter must map Kite-specific variety/product/validity/market-protection choices without exporting those enums as universal broker-neutral values.

Source:
- https://kite.trade/docs/connect/v3/orders/

### 2.2 Upstox V3

The current Upstox V3 Place Order page documents:
- order types: `MARKET`, `LIMIT`, `SL`, `SL-M`;
- products: `I`, `D`, `MTF`;
- validity: `DAY`, `IOC`;
- required instrument token, quantity, product, validity, price, order type, transaction type, disclosed quantity and trigger price fields in the published schema;
- `slice=true` to split using the exchange-assigned freeze quantity;
- a maximum order count for slicing, linked from the page;
- market protection for MARKET and SL-M: `-1` automatic, `1`–`25` custom percentage, `0` no protection (the page says an API market order with no protection is rejected due to exchange restrictions);
- `is_amo` is ignored; the system infers AMO/live handling from the current market session;
- F&O/equity quantity is described as units, while commodity quantity is lots.

The V3 slicing response returns an array of order IDs. A successful parent response therefore creates multiple child order identities.

**Documentation wording issue:** the page's quantity description says F&O/equity units are accepted in multiples of “tick size”. Since tick size is a price increment, the adapter must not treat this sentence as a quantity-unit conversion rule. Contract lot size and the exchange file remain the controlling quantity source.

Source:
- https://upstox.com/developer/api-documentation/v3/place-order/

### 2.3 DhanHQ API v2

The reviewed DhanHQ order page documents provider-specific request fields including:
- exchange segment and security ID;
- transaction type;
- product type;
- order type;
- validity;
- quantity, disclosed quantity, price and trigger price;
- `afterMarketOrder` and AMO time fields;
- correlation ID.

Dhan's order type/product/AMO enums must remain provider-specific. Its `/orders/slicing` endpoint is separate from the ordinary placement endpoint. The reviewed public order page does not publish a complete slicing response schema; PX-026 already records that response/child-grouping limitation as UNKNOWN.

The reviewed regular placement request table does not document a market-protection percentage field equivalent to Kite/Upstox. This is a statement about the reviewed schema only, not proof that no other Dhan product or interface has any slippage protection.

Source:
- https://dhanhq.co/docs/v2/orders/

## 3. Provider validation rules must not be silently normalized

A broker-neutral order intent can represent a logical side, product, order kind, time-in-force, price/trigger and quantity intent. The adapter must map that intent to the selected broker's API and must preserve the exact mapping used.

It must not:
- map unknown provider product/order-type values to a “nearest” enum;
- translate `TTL` into `DAY` or `IOC` without explicit policy;
- infer AMO solely from a UI label when the provider infers it from session time;
- send Kite's variety/product enums to Upstox or Dhan;
- invent market protection where the provider schema does not expose it;
- silently change quantity to meet freeze limits;
- silently round a limit/trigger price to the nearest tick;
- assume a broker acceptance response means exchange validation has succeeded.

An adapter may support an explicit auto-slicing capability only if it preserves:
- parent intent/command ID;
- original requested total quantity;
- exact freeze source/effective date;
- generated child quantities and IDs;
- every child success/error result;
- aggregate accepted, rejected, filled and remaining quantities;
- child-set completeness after lost response.

## 4. Validation pipeline for a future adapter

1. **Load effective contract master.** Require correct exchange, segment, trade date, file/schema version, source and hash.
2. **Resolve exact contract row.** Match stable instrument ID and complete derivative identity: underlying, expiry, strike, option type, contract family and status.
3. **Validate trading eligibility.** Check listed/active/expired/suspended/expiry/market-session and allowed product/order variety for that effective date.
4. **Validate quantity units.** Convert user lots into exchange units once using the market lot/multiplier; preserve input and output units.
5. **Validate lot multiple.** Require quantity in a legal multiple of the contract's effective market lot where that contract requires it.
6. **Load freeze quantity.** Use current contract file/circular for the precise instrument and date. Compare requested quantity with the limit.
7. **Decide slicing explicitly.** If slicing is authorized and supported, produce child quantities under provider/exchange constraints; otherwise reject above-freeze quantity. Do not use a silent fallback.
8. **Validate price/trigger ticks.** Check limit and trigger values against the contract's applicable tick size using exact decimal arithmetic.
9. **Validate exchange price/operating range.** Use current daily/contract-specific price range; do not confuse it with broker market protection.
10. **Validate broker schema.** Validate all required fields, enum values, conditional fields and supported features against the exact API version.
11. **Validate session/validity.** Resolve DAY/IOC/TTL/AMO/auction or provider-specific validity against market phase and provider rules.
12. **Revalidate immediately before dispatch.** If contract master, freeze file, price range, market phase or API capability has changed, invalidate the prior PX-033 admission snapshot.

The output must preserve per-check PASS/FAIL/UNKNOWN/NOT_APPLICABLE and source evidence. A broker's own rejection remains a new observation; it must not cause the domain layer to rewrite the original user request silently.

## 5. Additional requirements for PX-025

### R-119 — Exchange contract master is date-effective and integrity-pinned

A future adapter MUST identify the exact exchange/segment contract file, trade date, publication/effective date, schema version, file hash, capture time and parser version used for each order-validation decision. Missing, stale, corrupt or mismatched-date contract data MUST produce UNKNOWN, not a fallback to the previous day's row.

### R-120 — Complete derivative identity is required

A derivative order MUST resolve a stable contract identity including exchange, segment, underlying/security ID, instrument token, trading symbol, contract family, expiry, strike, option type and active/trading status. Symbol-only, token-only or fuzzy matching MUST NOT authorize an order.

### R-121 — Quantity units and market lot are explicitly converted once

The system MUST keep user lots, exchange units, market lot/multiplier and broker payload quantity as separate typed values. Any conversion MUST identify the effective contract-master version and source unit. The same multiplier MUST NOT be applied twice, and an ambiguous provider quantity unit MUST remain UNKNOWN.

### R-122 — Tick size is contract-specific and exact-decimal

Each limit/trigger price MUST be validated against the effective contract's tick size using exact decimal arithmetic. Off-tick values MUST be rejected or returned as invalid; the adapter MUST NOT silently round/modify a user's requested price or trigger.

### R-123 — Freeze quantity comes from the effective exchange file

Freeze quantity MUST be sourced by exact contract/instrument and effective date from the current NSE circular/contract file. Index and individual-security limits MUST remain distinct. A previously observed circular table or hard-coded constant MUST NOT replace the current daily file.

### R-124 — Exchange price/operating range is distinct from broker market protection

The system MUST validate the effective exchange price/operating range and the broker's market-protection setting as separate controls. A market-protection percentage MUST NOT be treated as permission to submit a price outside the exchange range, and a valid exchange range MUST NOT be treated as satisfying provider market-protection requirements.

### R-125 — Provider order enums are versioned adapter mappings

Order variety, order type, product, validity, AMO, market-protection, iceberg/auto-slice and other provider-specific fields MUST be mapped by broker/API version. Unknown or unsupported enum/field combinations MUST be rejected/UNKNOWN; the adapter MUST NOT silently coerce them to a different order type, product or validity.

### R-126 — Conditional request fields are validated by order type

Price, trigger price, disclosed quantity, auction number, TTL, AMO time, product and other conditional fields MUST be present/absent and validated according to the exact provider schema and selected order type/variety. A nonzero trigger price or market-protection field MUST NOT be sent where the provider says it is ignored or unsupported without an explicit reason.

### R-127 — Market session and AMO semantics are provider-specific

Regular-session, pre-open, auction and after-market order eligibility MUST be resolved against the current exchange session and provider API contract. A client-supplied AMO flag MUST NOT override a provider's documented session inference; AMO acceptance MUST NOT be equated with exchange execution or next-session acceptance.

### R-128 — Above-freeze slicing requires explicit, bounded child construction

A request exceeding the effective freeze quantity MUST be rejected or sliced only through a documented provider/exchange mechanism explicitly enabled by policy. Child quantities MUST comply with freeze/lot limits, child count limits and API schema. The adapter MUST preserve parent/child identity, requested total, each child result and remaining/rejected quantity.

### R-129 — Child-set completeness is mandatory after sliced response loss

When a sliced/multi-child response is lost or partial, the adapter MUST reconcile all possible child orders using provider/exchange evidence and retain UNKNOWN until the child set is established. It MUST NOT resubmit the entire parent quantity merely because some child IDs were not returned.

### R-130 — Contract lifecycle invalidates prior validation

A new expiry, expired contract, strike listing change, corporate-action adjustment, lot/tick/freeze revision, suspension or contract-master update MUST invalidate prior contract/order-validation approval for affected instruments. A cached instrument identity MUST NOT be treated as valid across a known effective contract change.

### R-131 — Exchange and broker rejection semantics are preserved

A rejected request MUST retain the raw broker/exchange code, message, API version, request fingerprint and all validation inputs. The adapter MUST distinguish local validation failure, broker API rejection, exchange rejection and unknown transport outcome. It MUST NOT retry a rejected order with silently altered quantity, price, product or variety.

### R-132 — Dispatch requires a fresh contract-validation snapshot

Immediately before dispatch, the adapter MUST verify that the PX-033 admission snapshot, contract-master row, lot/tick/freeze parameters, exchange price range, market session and provider API capability remain current. Any material change MUST invalidate the admission decision and require revalidation.

## 6. Deterministic acceptance scenarios

These extend AT-001 through AT-220. Use synthetic contract-master files, freeze tables, price ranges and fake broker request validators only.

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
| AT-238 | Kite MARKET/SL-M order uses automatic market protection | Map `-1` to Kite's documented automatic protection and preserve the provider-specific setting |
| AT-239 | Upstox V3 MARKET order sets market protection to zero | Apply the documented API rejection condition; do not treat zero as “unlimited protection” |
| AT-240 | Upstox V3 market protection is outside its documented custom range | Reject invalid provider parameter; do not clamp silently |
| AT-241 | Dhan regular order request is built with an unsupported Kite/Upstox market-protection field | Do not inject an undocumented field; use Dhan's documented schema or return unsupported/UNKNOWN |
| AT-242 | Upstox F&O quantity is entered in lots but API expects units | Convert once using effective market lot and preserve user lots plus payload units; do not use tick size as a quantity multiplier |
| AT-243 | Unsupported broker product/order type/validity enum is supplied | Reject/UNKNOWN; never coerce to the nearest accepted value |
| AT-244 | Upstox request sends `is_amo=true` during active market session | Apply provider rule that session inference overrides the flag; do not represent request as guaranteed AMO |
| AT-245 | Kite TTL is mapped to Upstox or Dhan DAY/IOC without policy | Reject unsupported mapping; no silent validity downgrade |
| AT-246 | Kite autoslice / Upstox slice / Dhan separate slicing endpoint produce child orders | Preserve provider-specific parent/child identities and exact per-child result; no generic response assumption |
| AT-247 | Generated sliced child count exceeds provider/API maximum | Reject or require a separately authorized strategy; do not emit an oversized or partial silent fallback |
| AT-248 | Market protection is within range but exchange dynamic price/operating range rejects the request | Preserve distinct broker/exchange validation reason; market protection does not override exchange price range |
| AT-249 | Contract master, freeze limit or tick changes after PX-033 admission but before dispatch | Invalidate stale admission snapshot and rerun affected gates |
| AT-250 | Provider returns a new/unknown schema field or rejection code | Preserve raw response and classify UNKNOWN/unsupported; do not silently map or retry with altered fields |

PX-025 now contains **132 normative requirements (R-001–R-132) and 250 proposed acceptance scenarios (AT-001–AT-250)**. These are proposed deterministic scenarios; no parser, broker adapter or test implementation was executed.

## 7. Open questions and evidence limitations

1. The daily `contract.gz` and `NSE_FO_contract_ddmmyyyy.csv.gz` file for 8 November 2026 was not downloaded/parsed in this audit. The current per-security freeze/lot/tick rows remain uninspected.
2. NSE Circular FAOP/74469 gives the June 2026 index quantity-freeze values, but any subsequent circular or daily contract-file revision after that date must be checked before operational use.
3. The current contract-information page and linked report formats must be inspected to establish exact row keys, code lists, field definitions, row ordering, checksums and publication time.
4. The Upstox V3 page's “units in multiples of tick size” quantity wording is dimensionally inconsistent; the lot/quantity interpretation should be clarified before implementing the adapter.
5. The exact current maximum number of orders generated by Upstox V3 auto-slicing and its partial child-error response semantics remain provider-specific.
6. Dhan's slicing response schema and child correlation propagation remain unresolved from the reviewed order page.
7. The exact dynamic option-range refresh/cancel process and all instrument-specific price-band exceptions require the current applicable exchange circular/file.
8. The reviewed Dhan regular order schema did not show a market-protection field; a broker-specific support/contract confirmation would be needed before asserting all Dhan order types lack one.

These gaps remain UNKNOWN; no actual API request or broker account was used to probe them.

## 8. Research decisions and non-authorization

- **ACCEPT:** use date-effective NSE contract-master and quantity-freeze files, not hard-coded instrument/lot/tick/freeze values.
- **ACCEPT:** separate market lot, exchange quantity unit, broker payload quantity and freeze quantity.
- **ACCEPT:** validate each contract's tick and exchange price range independently; exact-decimal and no silent rounding.
- **ACCEPT:** keep exchange operating/dynamic price range and broker market protection distinct.
- **ACCEPT:** preserve Kite, Upstox and Dhan provider enums/validity/AMO/slicing differences through versioned adapters.
- **ACCEPT:** parent/child identities and partial slicing outcomes remain explicit.
- **DEFER:** production contract-file parser and provider order-adapter implementation until current daily contract files and unresolved API schemas are available.
- **NOT AUTHORIZED:** broker/exchange calls, sandbox/production operation, real orders, code changes, paid services, credential/IP changes, PR or merge to `main`.

**Final status:** PX-034 exchange contract-master, tick/lot/freeze and provider order-request validation research documented. PX-025 expanded to 132 requirements and 250 proposed acceptance scenarios. The dated 8 November 2026 contract file was not inspected; no broker/exchange API or implementation was used.
