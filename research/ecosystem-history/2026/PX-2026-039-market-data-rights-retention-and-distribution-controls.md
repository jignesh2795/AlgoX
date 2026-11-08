# PX-2026-039 — Market-data rights, retention and distribution controls

**Research date:** 2026-11-08  
**Status:** public policy/provider terms reviewed; account-specific API agreements remain unverified  
**AlgoX area:** market-data governance / source licensing / storage, retention, display and redistribution controls  
**Inputs:** PX-025, PX-033, PX-035–PX-038  
**Mode:** research and requirements specification only  
**Non-goals:** no legal opinion, account login, agreement acceptance, subscription purchase, feed connection, data download, code implementation, PR or merge to `main`

## Executive finding

Technical access to an API does **not** automatically grant the right to store market data indefinitely, redistribute it, publicly display it, commercialize it, create derived indices or retain it after access terminates.

The public-source review establishes three different levels of evidence:

1. **NSE-originated market data:** NSE's Data Sharing & Usage Policy says a Relevant Agreement defines intended use, transmission, handling and dissemination. It reserves ownership, restricts redistribution except as agreed, and requires separate licensing to create financial indices or instruments/contracts from its data.
2. **Kite Connect:** the published API terms expressly restrict public display of live data, virtual/mock trading uses and redistribution. API content may not, absent permission, be permanently copied or cached with intent to redistribute. Its five-year provision concerns audit logs/records, not a five-year raw-market-data archive licence.
3. **Upstox and Dhan:** public sources do not establish a complete API-feed licence covering all storage, archive, multi-user display, redistribution and commercial uses. Upstox's general website/app terms are not a substitute for API-feed agreement terms. Dhan's Data API subscription provides a paid access mechanism; subscription/payment alone does not prove redistribution or archive rights.

**Decision:** AlgoX must use a source-specific rights manifest and per-operation rights gate. If the source agreement, allowed purpose, retention period, public-display or redistribution right is unknown, the affected operation remains UNKNOWN and is blocked. Do not infer permission from a successful API response, a subscription fee or the technical ability to cache bytes.

This is a requirements record, not a conclusion that all private research or local caching is prohibited. Internal use is permitted only where the governing agreement and applicable rules allow it.

## 1. Scope and source hierarchy

### 1.1 Data categories

The NSE policy defines Market Data broadly: prices, identifiers, volumes and trade-related data, including streaming, real-time, snapshot, delayed, end-of-day, historical and corporate data. It covers equity, debt, equity derivatives, currency derivatives, SLB, commodity derivatives and future segments.

A rights record must distinguish:
- exchange/data vendor and source provider;
- exact product/API/feed, exchange/segment and account/subscriber scope;
- live stream, snapshot, quote, depth, trade, OI, Greeks, EOD, historical candles, contract master and corporate data;
- agreement/licence version and effective period;
- intended purpose, user population and geography;
- transient processing, cache, archive, backup/DR and replay;
- internal display, external/public display, derived use, commercial use, export and onward redistribution.

### 1.2 Rights hierarchy

A rights resolver must preserve—not collapse—these distinct instruments:
1. applicable law, SEBI rules and exchange circulars;
2. exchange/data-vendor licence or Relevant Agreement;
3. broker/API agreement and product-specific conditions;
4. account/end-user terms and platform addenda;
5. internal policy, which can narrow but cannot enlarge rights granted above.

NSE's public policy explicitly says the Relevant Agreement specifies permitted use and end-user restrictions, and the policy is read with the specific agreement. The generic policy is not a complete licence for a particular client or feed.

Sources:
- https://www.nseindia.com/static/market-data/nse-data-policy
- https://www.nseindia.com/static/nse-terms-of-use

## 2. NSE Data Sharing & Usage Policy

The publicly accessible policy states:
- subscribers execute a Relevant Agreement setting subscription terms, intended use and how data is received, transmitted, handled, disseminated or dealt with;
- commercial market-data access is priced under the NSE Data board/delegated policy;
- data is provided online through a designated server; offline removable media requires prior approval of NSE Data's MD & CEO;
- agreements must specify permitted use, transmission, handling, dissemination and end-user restrictions;
- Market Data may not be used to create custom/composite indices or financial instruments/contracts unless separately licensed by the relevant NSE entity;
- reverse engineering or deriving the composition/underlying information, structure or ideas of Market Data is restricted;
- access does not transfer ownership; ownership remains with NSE/NSE Data;
- redistribution is permitted only as agreed in the Relevant Agreement;
- non-commercial/research users may be considered for reduced-fee arrangements or waivers, but must have documented purpose restrictions and confidentiality declarations;
- NSE/NSE Data reserve rights to audit records/systems and conduct spot checks, with details in underlying documentation.

A non-commercial or research label is not a blanket licence. It does not automatically confer a free archive, public-sharing or commercial-output right.

Source:
- https://www.nseindia.com/static/market-data/nse-data-policy (updated 11 December 2025)

## 3. Broker-specific public terms

### 3.1 Zerodha Kite Connect

The published Kite Connect Terms and Conditions state:
- APIs can support a private personal interface or a platform offered to other Zerodha clients subject to required exchange approvals;
- live market data obtained via Kite Connect cannot be displayed to the public at large;
- use of APIs/live market data for virtual/mock-trading apps and trading-related games is prohibited;
- API access is a limited licence for use within India and during the agreement;
- absent express permission or applicable law, returned API content cannot be used to build permanent copies/databases or cached copies intended for redistribution, copied/modified into derivative works, sold, distributed, publicly displayed or sublicensed to third parties;
- credentials such as passwords, API keys/secrets and Client IDs are for the user's use and must be kept confidential;
- complete and accurate API usage trails/books/records/logs must be retained for at least five years or as required by law, with audit rights;
- additional API charges may be communicated separately.

The Zerodha support FAQ separately says Kite Connect data cannot be displayed or redistributed on other platforms and describes Kite Connect as an order-execution platform, not a data-distribution service.

**Critical scope distinction:** the five-year provision is for compliance trails/books/records/logs. It is not a five-year licence to archive raw ticks, depth or candles. The account-specific terms and any written permissions remain controlling.

Sources:
- https://www.kite.trade/terms/
- https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/kite-connect-api-faqs

### 3.2 Upstox

Upstox's public Terms of Use (last updated 15 May 2026) govern its website/mobile application. Its website-content terms state that content on the site or delivered through it is proprietary to Upstox or third parties/partners, and restrict commercial/public use of website materials.

The public general terms reviewed here do **not** settle every API-feed question: long-term cache/archive, multi-user feed display, onward API/data vending, derived outputs, commercial resale or post-termination retention. The website-content clause must not automatically be treated as a complete API-feed licence; equally, the absence of a public API-specific clause is not permission.

**Decision:** obtain the applicable Upstox developer/API and account agreements, including any exchange data restrictions, before enabling those operations.

Sources:
- https://upstox.com/terms-of-use-and-privacy-policy/
- https://upstox.com/developer/api-documentation/

### 3.3 DhanHQ

Dhan's support documentation says Data APIs are subscribed separately through the Dhan Web profile/API area. The current public page reviewed states ₹499 plus applicable taxes per month, auto-debited every 30 days. This establishes a separate Data API access/subscription mechanism; it does not define the complete scope of storage, external display, redistribution, commercial use or archive rights.

The public DhanHQ API documentation describes live market feed, quotes and historical data, but the material reviewed here does not contain a complete rights schedule for multi-user display, onward data distribution, long-term retention or post-termination use.

**Decision:** treat a Data API subscription as access entitlement only unless the current account/API agreement separately grants the intended rights. Dhan-specific rights remain UNKNOWN pending contract review.

Sources:
- https://dhan.co/support/platforms/dhanhq-api/how-to-access-dhan-api/
- https://dhanhq.co/docs/v2/

## 4. Website access is not licensed API data

NSE Website Terms govern NSE website/mobile content and prohibit copying, storing, disseminating or using that website/app content without prior written permission; they also prohibit using website/app content for gaming, virtual trading or simulation.

This must be scoped to the NSE website/mobile application. It is not automatically the full rule for a separately licensed broker feed. Conversely, scraping a public website and labelling the result as an authorized exchange/broker API feed is not acceptable.

The same distinction applies to Upstox website/app content terms: API-feed rights must be established from the relevant API/account agreement rather than inferred solely from website terms.

Sources:
- https://www.nseindia.com/static/nse-terms-of-use
- https://upstox.com/terms-of-use-and-privacy-policy/

## 5. Usage classes and permissions

A future resolver must classify operations separately. This table is a conservative governance model, not a statement that a provider grants any permission by default.

| Use class | Example | Evidence required before enabling |
|---|---|---|
| Private account display | Quotes shown to the authorized account holder in a local terminal | Broker terms permit private account use |
| Internal strategy research | Indicators and strategy experiments run locally | Agreement permits analysis/research and the intended storage |
| Historical backtest/replay | Stored candles/ticks used in a private backtest | Explicit historical access, retention and replay scope |
| Internal derived analytics | Risk metrics, model features, signals and summaries | Transformation/derived-use terms; preserve source lineage |
| Multi-user display | Quotes shown to multiple platform users | Explicit end-user display rights and user/tenant scope |
| Public display | Quotes shown on public websites/social channels | Explicit public-display and redistribution licence |
| Commercial terminal/service | Charge customers for data-bearing dashboards/signals | Written commercial-use rights and required approvals |
| Bulk export/onward API | CSV exports, API endpoints, feed resale | Explicit onward distribution/resale rights |
| Index/instrument creation | Custom index or financial instrument from market data | Separate exchange/data-licensor licence where required |
| Model training/dataset publication | Raw or transformed data used in training or published dataset | Written permission for retention, transformation and disclosure |

Unknown permission never implies permission.

## 6. Storage, caching and deletion

### 6.1 Separate data retention from audit-log retention

Storage classes must remain distinct:
- raw live packets/snapshots;
- historical bars and provider response archives;
- exchange/broker contract and reference masters;
- derived features and indicators;
- user-specific positions/orders/fills and personal data;
- operational/compliance logs;
- agreement metadata and source hashes.

A broker audit-log retention obligation is not a market-data retention licence. In particular, Kite's five-year provision applies to usage trails/books/records/logs, not to raw data payloads.

### 6.2 Rights-aware retention

Before persistent storage, the rights resolver must know:
- which agreement permits storage;
- whether permission covers transient processing, session cache, account cache, long-term archive, backup/DR and replay;
- permitted retention period and deletion trigger;
- whether history can be replayed after subscription/account termination;
- whether derived data can be retained if raw data must be deleted.

If the agreement does not specify a retention term, do not invent an indefinite retention period. Mark UNKNOWN and obtain clarification before persistent archive/replay.

### 6.3 Termination workflow

On licence expiry, API termination, account closure or changed source restrictions:
1. stop ingestion under the expired permission;
2. determine which records must be deleted, quarantined or retained under another valid licence;
3. apply deletion rules to caches, primary storage, derived stores and backups;
4. retain only logs/records with an independent retention basis;
5. produce a deletion/retention evidence record without retaining unauthorized raw payloads.

Downloading data does not transfer ownership or automatically create a perpetual right to keep it.

## 7. Derived analytics and models

Transforming market data into bars, indicators, Greeks, labels, signals, model features, research reports or backtest results does not automatically clear source restrictions.

The rights resolver must evaluate:
- whether the agreement permits transformation and internal analysis;
- whether derived results may be disclosed externally;
- whether a summary still exposes live/recent source prices or reconstructible market data;
- whether the transformation could amount to restricted reverse engineering or derivation of composition;
- whether it creates a custom financial index, benchmark or instrument requiring separate licensing.

Raw observations and derived views must be stored separately with lineage. A derived dataset inherits the strictest applicable restriction unless written terms establish otherwise.

## 8. Security and multi-user scope

- Broker credentials/API keys/client IDs must remain confidential and outside the research repository.
- A subscription tied to one account must not automatically be multiplexed to unrelated users or tenants.
- Every record must retain its allowed account/tenant/user scope.
- UI display, exports, reports and external APIs must check rights in addition to user authentication.
- Audit trails should identify source, user, purpose, destination, time and agreement version.
- A successful login, subscription or WebSocket connection is not proof that every downstream user/use case is licensed.

## 9. Separate retail-algo regulatory compliance

SEBI's retail-algo framework is a different control domain from market-data rights. SEBI Circular 2025/132 (30 September 2025) states that the framework in the 4 February 2025 circular, together with exchange implementation standards/operational modalities, applies to all stock brokers from 1 April 2026. NSE's empanelled-algo-provider page points to NSE/INVG/73992 (30 April 2026) and was updated 3 November 2026.

This is not a market-data redistribution licence. It is a separate deployment/regulatory gate for retail API algo functionality, broker onboarding, exchange registration/empanelment and operational controls. Neither approval substitutes for the other.

Sources:
- https://www.sebi.gov.in/sebi_data/attachdocs/sep-2025/1759232056254.pdf
- https://www.nseindia.com/static/trade/empanelled-algo-providers-exchange
- https://betanseapi.nseindia.com/static/trade/platform-services-non-neat-decision-support-tools-algorithm-trading

## 10. Rights manifest and enforcement model

Each source should have a versioned rights manifest with:
- provider/exchange, exact product/API/feed and account/subscriber/tenant scope;
- agreement/licence ID, version, acceptance date and effective period;
- permitted purpose(s) and geography;
- cache/archive/replay permission and retention deadline;
- internal, multi-user and public display rights;
- derived analytics/model training rights;
- bulk export, onward API, redistribution, commercial use and resale rights;
- index/financial instrument creation permission;
- deletion/termination conditions;
- audit/reporting obligations and legal-review status.

Candidate action outcomes:
- `PERMITTED`;
- `PROHIBITED`;
- `CONDITIONAL`;
- `UNKNOWN_BLOCKED`;
- `NOT_APPLICABLE`.

The rights gate is independent of PX-033 market-risk/order-admission gates. A risk-safe strategy cannot bypass a licensing prohibition; permitted data use does not make an order safe.

## 11. Additional requirements for PX-025

### R-193 — Every market-data source has a rights manifest

Every market-data source/product MUST have a versioned rights manifest identifying provider/exchange, exact API/feed, account/subscriber scope, governing agreement, effective dates, permitted purpose, storage/display/redistribution rights, geography, retention and deletion requirements. Missing agreement evidence MUST result in UNKNOWN.

### R-194 — Technical API access does not imply downstream data rights

The system MUST NOT infer public display, multi-user display, permanent archival, commercial use, onward API, resale or redistribution rights from a successful login, API token, free/paid subscription or ability to retrieve data. Each downstream use MUST be permitted by the applicable agreement.

### R-195 — Internal, research, display and commercial purposes are distinct

The rights resolver MUST distinguish private account use, internal research/backtesting, internal derived analytics, multi-user display, public display, commercial terminal/service, export/resale and index/financial-product creation. Permission for one purpose MUST NOT be generalized to another.

### R-196 — Public display and redistribution are explicit gates

Any operation that exposes raw or reconstructible market data to another person, public website, tenant, customer, API or bulk export MUST require explicit source-specific display/redistribution permission. The default for an unknown or restricted source is BLOCK.

### R-197 — Storage, cache and archive permissions are separate

The system MUST distinguish ephemeral processing, session cache, local account cache, long-term historical archive, backup/DR, replay and derived-data storage. A permission to call an API MUST NOT be interpreted as permission for permanent copies or indefinite caching.

### R-198 — Audit-log retention is not market-data retention

The system MUST store audit-log retention obligations separately from raw market-data retention rights. A requirement to retain access logs/books/records for a stated period MUST NOT be treated as a licence to retain the underlying market-data payload for the same period.

### R-199 — Derived data inherits source restrictions unless cleared

Indicators, OHLC aggregation, Greeks, analytics, signals, model features, training datasets and backtest outputs MUST retain source lineage and restrictions. Transformation, aggregation or removal of direct identifiers MUST NOT automatically be treated as permission to redistribute or commercialize the result.

### R-200 — Exchange and broker terms are separately scoped

The rights resolver MUST preserve exchange/data-vendor licences, broker API terms, account/end-user agreements and website/app terms as distinct sources. Website terms MUST NOT be blindly generalized to a separately licensed API feed; absence of API-specific terms MUST NOT be treated as permission.

### R-201 — Index and financial-instrument creation requires separate rights review

Any custom/composite financial index, benchmark or financial instrument constructed from exchange market data MUST be blocked until the relevant exchange/data licensor's separate licence/approval is recorded where required. A locally computed indicator MUST not be mislabeled as a licensed index.

### R-202 — Non-commercial research permission is documented, not assumed

A research, student, personal or not-for-profit purpose MUST NOT automatically grant a data licence, free archive right or permission to share results containing raw/reconstructible data. Any applicable non-commercial/research permission, confidentiality undertaking, fee waiver and restrictions MUST be recorded.

### R-203 — Termination triggers rights-aware ingestion and deletion workflow

Agreement expiry, API termination, source restriction change or account closure MUST trigger an evaluation of continued ingestion, cached data, archives, derived datasets, backup copies and replay access. The system MUST retain only data whose continued retention is permitted or independently required, and MUST preserve deletion/retention evidence.

### R-204 — Rights checks cover users, tenants, exports and credentials

Every data display/export/replay path MUST enforce authorized account/tenant/user scope. Credentials and client identifiers MUST remain confidential and MUST NOT be shared to multiplex a single-account data subscription to unrelated users. Data access audit records MUST identify source, actor, purpose, destination and time.

### R-205 — Market-data licensing and retail-algo compliance are independent gates

A future deployment review MUST evaluate market-data rights separately from SEBI/exchange retail-algo registration, empanelment and broker operational requirements. Passing a data licence gate MUST NOT imply algo approval; algo approval MUST NOT grant market-data ownership or redistribution rights.

## 12. Deterministic acceptance scenarios

These extend AT-001 through AT-370. Use synthetic agreement manifests, fake data records, export requests and user/tenant contexts only.

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-371 | Source has no identified agreement or account-specific rights record | UNKNOWN_BLOCKED for persistent storage, display, export and commercial use |
| AT-372 | Kite Connect live market data is requested for a public website | PROHIBITED under published Kite terms; block public display |
| AT-373 | Kite Connect data is requested for a virtual/mock-trading app or trading game | PROHIBITED under published Kite API terms |
| AT-374 | Kite API response is cached permanently with intent to redistribute | PROHIBITED unless express permission/applicable law is evidenced |
| AT-375 | Kite audit logs must be retained for five years | Retain audit logs per term, but do not infer five-year raw market-data archive permission |
| AT-376 | NSE market data agreement allows private analysis but not public redistribution | Permit only documented private-analysis scope; block export/public display |
| AT-377 | NSE data is used to construct a custom financial index without separate licence | PROHIBITED/UNKNOWN_BLOCKED; require the separate relevant NSE licence |
| AT-378 | NSE Data subscriber asks to copy feed to offline removable media | Require the policy's prior approval and agreement evidence; otherwise BLOCK |
| AT-379 | NSE Data is redistributed to another subscriber not named/allowed in the Relevant Agreement | Block redistribution; no implied sublicence |
| AT-380 | Non-commercial researcher claims data should be free because the use is academic | Require documented research access/terms/confidentiality; no automatic exemption |
| AT-381 | Upstox website-content terms are available but API-feed licence is not | Do not apply website clause as complete API policy; mark API redistribution/archive rights UNKNOWN |
| AT-382 | Upstox API user requests multi-tenant live quotes through one account | Require explicit API/feed and end-user rights; block while agreement scope is unknown |
| AT-383 | Dhan Data API subscription is active and paid | Treat as API access entitlement only; do not infer commercial redistribution or indefinite archive |
| AT-384 | Dhan feed is exposed through an external user-facing dashboard | Require written display/redistribution permission; subscription alone does not PASS |
| AT-385 | Historical data is stored for internal backtesting | Allow only when the source agreement permits historical retention/replay; record retention scope and dataset provenance |
| AT-386 | Derived technical indicator is published publicly from restricted raw data | Require permission for derived/public use; do not assume transformation removes source restrictions |
| AT-387 | Strategy backtest result embeds reconstructible raw ticks/candles in a downloadable report | Treat as potential data redistribution; block until source rights permit the disclosure |
| AT-388 | Data vendor agreement expires while old raw cache remains | Stop ingestion and evaluate deletion/retention; do not continue replay by default |
| AT-389 | User account closes but compliance logs have a separate retention obligation | Retain only the logs required/permitted; apply distinct raw-data deletion policy |
| AT-390 | Backup/DR copy exists outside the primary data store | Apply the same agreement, geography, access and deletion constraints to backup copies |
| AT-391 | Raw market data is stored in a public GitHub repository | Block; preserve only permitted metadata, source URLs and hashes in research repository |
| AT-392 | One tenant requests another tenant's provider feed cache | Deny cross-tenant access unless the agreement explicitly supports the sharing model |
| AT-393 | Data is displayed to an end user under an agreement with explicit user limits/attribution | Permit only within those exact recorded limits; audit user and source agreement |
| AT-394 | Market-data rights are permitted but SEBI/exchange retail-algo registration is not complete | Data use may be evaluated independently; block live retail-algo deployment on the separate regulatory gate |
| AT-395 | Agreement version changes and narrows permitted display/retention | Invalidate affected rights decisions, stop prohibited operations and re-evaluate stored datasets/exports |

PX-025 now contains **205 normative requirements (R-001–R-205) and 395 proposed acceptance scenarios (AT-001–AT-395)**. These are proposed deterministic tests only; no agreement, account, API feed or data payload was accessed.

### Source and contract limitations

- Kite public API terms and support FAQ explicitly restrict live public display, redistribution and some permanent/cached copies, but the accepted account-specific agreement was not retrieved.
- NSE's Relevant Agreement is subscriber-specific; the generic policy does not replace the signed agreement governing a particular feed.
- Upstox's website/app terms are not treated as a complete API data licence; current API/account terms remain unverified.
- Dhan public support confirms the separate Data API subscription and fee, but not downstream rights; account API terms remain unverified.
- Kite's five-year clause is audit-log retention, not raw-market-data retention permission.


## Final status

PX-2026-039 market-data rights, retention and distribution requirements documented. PX-025 contains 205 requirements and 395 proposed acceptance scenarios. Public Kite terms and NSE policy provide explicit restrictions; Upstox and Dhan API-feed rights remain unverified without the current account/API agreements. No agreement was accepted, no subscription purchased, no market-data feed or historical API was connected, no data payload was downloaded, no code was implemented and no order was submitted.
