# PX-2026-035 — NSE contract-file ingestion, schema variants and integrity controls

**Research date:** 2026-11-08  
**Status:** official circular chronology and file-family audit completed; current daily files and full row schemas not inspected  
**AlgoX area:** reference-data ingestion / contract master / lot and freeze data / exchange admission and routing  
**Scope:** NSE equity-derivatives contract files, MII contract-file variants, daily FO contract CSV, quantity-freeze and market-lot reports  
**Inputs:** PX-023, PX-029, PX-032, PX-034 and PX-025 requirements R-119–R-132  
**Mode:** research and requirements specification only  
**Non-goals:** no current daily NSE file downloaded/parsed, no member extranet access, no broker/exchange API call, no order, no code implementation, paid service, PR or merge to `main`

## Executive finding

PX-034 established that order validation depends on the effective NSE contract master and daily freeze/lot parameters. PX-035 studies the **ingestion contract** for those reference-data artifacts.

The main finding is that AlgoX must not assume one timeless “NSE contract master” file or one stable schema. NSE has published several related file families and variants, and its circular history shows that separately distributed quantity-freeze and market-lot reports have changed status over time.

The source review identifies:

1. **MII contract files:** NSE publishes different contract-file variants, including NSE-exclusive and NSE/BSE interoperability-related contract sets. These variants must remain separately identified.
2. **Dated FO contract CSV:** NSE Circular NSE/FAOP/74469 (29 May 2026) directs members to load updated `contract.gz` and dated `NSE_FO_contract_ddmmyyyy.csv.gz` files for index quantity-freeze changes effective 1 June 2026.
3. **Separate quantity-freeze/market-lot reports:** the 2024 chronology records discontinuation of separate report distribution where the MII contract file carries the information, followed by a later circular re-announcing `Qtyfreeze.csv` and `fo_mktlots.csv` reports. Their presence, precedence and effective date must therefore be resolved from the current circular/report catalogue, not a stale assumption.
4. **Admission type is schema-variant-specific:** NSE Circular NSE/FAOP/73629 (April 2026) describes BSE-exclusive contract identification using a different field number in `contract.gz` and the dated `NSE_FO_contract_ddmmyyyy.csv.gz`. Field 13 is referenced for the first file and field 30 for the second; the relevant value identifies the BSE-listed admission type.
5. **Freeze, market lot and quantity unit are separate values:** the loader must retain raw source values and their meaning. A quantity-freeze report is not a market-lot report, and neither is a user-entered number of lots.
6. **File integrity is part of order safety:** wrong variant, stale date, partial download, unknown field mapping, duplicate contract identity or missing current freeze row must produce UNKNOWN and block an exposure-increasing order.

**Limitations:** the actual daily contract file for 8 November 2026, its full row schema, file hash, record count and the referenced Annexure/sample data were not downloaded or parsed in this audit. The research record describes source file families and identified circular changes; it does not claim a validated parser or complete field dictionary.

## 1. Source and file-family inventory

### 1.1 MII contract-file family

NSE's Derivatives All Reports/contract-information catalogue lists MII contract-file variants. The source/circular material distinguishes at least:
- an F&O MII contract file for NSE-exclusive contracts;
- an F&O MII contract file for NSE/BSE-exclusive or interoperable contract coverage;
- the dated `NSE_FO_contract_ddmmyyyy.csv.gz` file referenced in later circulars;
- the `contract.gz` MII contract file referenced in the 2026 quantity-freeze update.

These are not safe to collapse into one file type merely because each carries instrument/contract data. Variant selection affects which contracts are admitted/routed and which field mapping applies.

The current daily file must be selected based on the exact exchange route and source instructions. A file that includes an instrument row does not by itself prove that the instrument is tradable through the selected venue, member connection or provider.

Sources:
- NSE Contract Information / Derivatives All Reports: https://betanseapi.nseindia.com/static/products-services/equity-derivatives-contract-information
- NSE All Reports – Derivatives: https://www.nseindia.com/all-reports-derivatives
- NSE Circular NSE/FAOP/73629 (April 2026): https://nsearchives.nseindia.com/content/circulars/FAOP73629.pdf
- NSE Circular NSE/FAOP/74469 (29 May 2026): https://nsearchives.nseindia.com/content/circulars/FAOP74469.pdf

### 1.2 Dated FO contract CSV

NSE Circular NSE/FAOP/74469 updates index quantity-freeze limits effective 1 June 2026 and directs members to load the updated:
- `contract.gz`;
- `NSE_FO_contract_ddmmyyyy.csv.gz`.

It also publishes the index-specific quantity-freeze schedule described in PX-034:
- BANKNIFTY 900;
- NIFTY 1,800;
- FINNIFTY 1,800;
- MIDCPNIFTY 2,800;
- NIFTYNXT50 600.

These quantities are a dated circular schedule, not a permanent static table. The circular explicitly directs members to the updated contract files. The actual 8 November 2026 file and any later effective circular were not retrieved in this research pass.

Source:
- https://nsearchives.nseindia.com/content/circulars/FAOP74469.pdf

### 1.3 Separate quantity-freeze and market-lot reports: chronology matters

The NSE circular history shows that standalone quantity-freeze and market-lot report availability has changed:

- **March 2024:** NSE circulars described discontinuation of separate `Qtyfreeze.csv` distribution from the public website/extranet path and directed members to the MII contract file for the corresponding quantity-freeze/market-lot information.
- **December 2024:** a later NSE circular announced separate `Qtyfreeze.csv` and `fo_mktlots.csv` report dissemination from 9 December 2024 EOD.
- **May 2026:** NSE/FAOP/74469 again specifically instructs members to load updated `contract.gz` and dated `NSE_FO_contract_ddmmyyyy.csv.gz` files for the revised index freeze quantities.

This is a source chronology, not a claim that all these artifacts are simultaneously authoritative in every interface. The exact channel, report schedule, use case and latest effective circular must be resolved before any loader chooses a precedence rule. If a separate report is missing, that absence must not be “fixed” by assuming it was discontinued; likewise, an old standalone report must not override a newer contract file.

Sources:
- NSE/FAOP/61157 (March 2024): https://nsearchives.nseindia.com/content/circulars/FAOP61157.pdf
- NSE/FAOP/61372 (March 2024): https://nsearchives.nseindia.com/content/circulars/FAOP61372.pdf
- NSE/FAOP/65435 (5 December 2024): https://nsearchives.nseindia.com/content/circulars/FAOP65435.pdf
- NSE/FAOP/74469 (29 May 2026): https://nsearchives.nseindia.com/content/circulars/FAOP74469.pdf

### 1.4 Admission type and schema variants

NSE Circular NSE/FAOP/73629 (April 2026) introduces/clarifies identification of BSE-exclusive contracts through an **Admission Type** field in the MII contract data:
- in `contract.gz`, the circular references field number **13**;
- in `NSE_FO_contract_ddmmyyyy.csv.gz`, it references field number **30**;
- the specified value identifies the BSE-listed/BSE-exclusive admission type.

The important ingestion lesson is not to hard-code a single numeric field offset across file variants. The same semantic field may occur at a different position in a different contract-file layout. The exact schema profile, circular version, file variant and code list must travel together.

The corresponding venue/alternative-trading-venue treatment must also be read from the applicable circular. A BSE-exclusive contract row must not be treated as a normal NSE-exclusive contract just because a generic instrument parser can decode its underlying, expiry and strike.

Source:
- NSE Circular NSE/FAOP/73629: https://nsearchives.nseindia.com/content/circulars/FAOP73629.pdf

## 2. Data concepts that must remain separate

| Data concept | Meaning | Must not be confused with |
|---|---|---|
| Contract identity | Exact listed derivative contract and venue/segment | Display symbol or broker UI text |
| Market lot | Contract lot multiplier / legal trading unit | User's entered lot count or freeze quantity |
| Quantity unit | Raw exchange/broker payload unit | Underlying shares unless source says so |
| Quantity freeze | Maximum permitted quantity for an applicable order/contract before slicing/rejection | Market lot, position limit or MWPL |
| MWPL/entity position limit | Market-wide/entity holding exposure cap | Single-order freeze quantity |
| Tick size | Minimum permitted price increment | Quantity unit or lot size |
| Operating/dynamic price range | Exchange price admission range | Broker market protection |
| Admission type | Exchange/venue admission classification | Instrument type or option type |
| Contract status | Active, expired, suspended, added/removed or other source state | Presence of an old row in a cached file |
| Effective date/time | When the source row/rule applies | Download/publication timestamp alone |

All raw source fields, original units and effective dates must be preserved. Any normalized value must identify the conversion rule and schema version.

## 3. Schema and artifact provenance model

A future ingestion service should create a source manifest per artifact. The manifest is a research design candidate, not a finalized database schema.

Minimum fields:
- `source_artifact_id`;
- exchange and segment;
- artifact family and variant (`contract.gz`, dated FO contract CSV, quantity-freeze report, market-lot report, delta file, ban list, etc.);
- publication URL/channel and member/public distribution scope;
- source circular/rule references;
- schema profile/version and parser version;
- file date, publication time, capture time and effective date/time;
- compression and encoding;
- byte size and cryptographic hash;
- expected/observed record count where source supplies it;
- primary-key definition and unique-key checks;
- completeness/validation result;
- supersedes/superseded-by relationship;
- promotion status and rejection reason.

The raw bytes must be retained immutably. Parsed rows are a versioned derivative of those bytes, not a replacement for them.

### 3.1 Effective time vs publication time

A circular may be published on one date, direct members to load files at a later time, and apply a parameter from a future effective date. The loader must preserve these separate times:
- circular publication date;
- file publication/dissemination time;
- file capture time;
- row/parameter effective date/time;
- trading session to which the row applies.

Do not make a file effective merely because it is the newest downloaded file. A later-published file can contain future-effective parameters; a delayed download can contain a file whose effective date has already begun.

### 3.2 Schema profiles are source-variant-specific

Field offsets, enum values, row keys and code lists must be keyed by exact artifact variant and schema version. The Admission Type field number 13 in one MII contract file and 30 in another is a concrete reason why positional field maps must not be reused blindly.

The parser must reject:
- unknown schema version;
- file variant inconsistent with the URL/name/source circular;
- missing required fields;
- additional or shifted columns without a documented compatible schema;
- invalid enum values;
- an unknown Admission Type code;
- instrument identity collisions or duplicate primary keys.

A parser that “best-effort” maps a shifted column into a known field can create a valid-looking but wrong tradable instrument. That is a hard data-integrity failure.

## 4. Atomic ingestion and promotion

The ingestion/promotion process should be staged:

1. **Acquire:** fetch the exact artifact through its documented source route without rewriting bytes.
2. **Capture:** record source URL/channel, download time, file size, content hash, response metadata and source circular.
3. **Identify:** resolve artifact family, variant, segment, effective date and schema profile.
4. **Validate container:** gzip integrity, decompression completion, encoding, line/record structure and EOF/truncation.
5. **Parse:** use the exact schema profile; preserve raw columns and row-level source positions.
6. **Validate rows:** required values, enum code lists, unique identity, lot/tick/freeze units, expiry/status dates and venue admission.
7. **Validate set:** duplicates, missing segments, stale records, cross-file mismatches, record-count expectations, and referenced parameter/circular.
8. **Cross-check:** compare related contract, lot, freeze and admission-type records only under documented effective-source rules.
9. **Stage:** build a complete candidate snapshot without making it visible to order admission.
10. **Promote atomically:** promote only if all required artifacts for the target session/effective date pass their checks; otherwise keep the candidate rejected/UNKNOWN.
11. **Audit:** preserve the promoted snapshot ID, file hashes, parser version, source circulars, validation report and promotion decision.
12. **Invalidate:** on a new circular, correction, file replacement, contract change or expiry/corporate action, invalidate only the affected instruments/parameters and require a new complete validated snapshot.

A partially downloaded or partially parsed file must never be mixed with the previous day's file to produce an apparently complete current master. Previous snapshots may remain available for historical research and replay; they must not silently authorize current order admission after their effective period ends.

## 5. Cross-file consistency and conflict handling

The following comparisons are necessary, but a mismatch must be resolved against the current effective source hierarchy rather than automatically choosing a convenient value:

- `contract.gz` vs dated `NSE_FO_contract_ddmmyyyy.csv.gz` instrument/contract identity;
- MII NSE-exclusive vs NSE/BSE-interoperability contract variants;
- contract-file market lot vs separate `fo_mktlots.csv` when that report is applicable;
- contract-file quantity-freeze vs separate `Qtyfreeze.csv` when that report is applicable;
- effective freeze values vs circular-announced index limits;
- admission-type field and selected exchange/venue;
- derivative contract master vs current corporate-action adjustments;
- contract expiry/status vs trading holiday/session calendar;
- contract lot/unit vs broker payload and position/trade quantity unit.

Do not assume every artifact has identical coverage. Some may be segment-specific, route-specific, member-only, effective at different times or intended for a particular product set. The ingestion manifest must state which artifacts are required for which decision.

If two current official sources conflict and no effective hierarchy resolves them, the affected contract/gate remains UNKNOWN. Do not use the maximum/minimum as a default, and do not silently prefer the newest timestamp when the sources have different meanings.

## 6. Special contract admission and venue routing

The Admission Type change documented in FAOP/73629 demonstrates that a contract row can be valid but not necessarily valid through every venue/routing path.

A future order validator must:
- retain Admission Type raw code and normalized meaning;
- bind its enum mapping to the exact contract-file variant and circular;
- know whether the contract is NSE-exclusive, BSE-exclusive or otherwise interoperable;
- check the requested exchange/alternative venue against that admission;
- reject unsupported spread/market-protection/order-type combinations where the circular specifies constraints;
- avoid treating the generic underlying/expiry/strike fields as sufficient venue eligibility.

If the admission code is unknown or the required alternative-trading-venue instruction is not represented in the selected adapter, return UNKNOWN/unsupported. A local broker API being syntactically capable of accepting a symbol does not override exchange contract admission.

## 7. Additional requirements for PX-025

### R-133 — Artifact family and variant are explicit

The loader MUST classify each source artifact by exact family, variant, exchange, segment and distribution channel. NSE-exclusive MII contract files, NSE/BSE-interoperability variants, dated FO contract CSVs, quantity-freeze reports and market-lot reports MUST NOT be treated as interchangeable inputs.

### R-134 — Effective date and publication time are separate

Every artifact and row MUST preserve publication/dissemination time, capture time and effective date/time independently. The newest download MUST NOT automatically be assumed effective for the current trading session.

### R-135 — Schema profile is pinned to artifact variant

The parser MUST bind a schema/profile and field map to the exact artifact variant, version, circular and segment. A field offset from `contract.gz` MUST NOT be reused for `NSE_FO_contract_ddmmyyyy.csv.gz` or another MII/report variant without source evidence.

### R-136 — Raw artifact bytes and provenance are immutable

The system MUST retain the original compressed file bytes, source URL/channel, file size, hash, download time, circular reference, parser version and validation report. Parsed records MUST be traceable to exact source bytes and row/record positions.

### R-137 — Gzip and complete-file validation is mandatory

An artifact MUST pass container/decompression validation through EOF, encoding, record framing and file completeness checks before parsing. Truncated, corrupt, partial or encoding-invalid files MUST be rejected and MUST NOT be promoted as a partial current contract master.

### R-138 — Contract identity keys are unique within their effective scope

The loader MUST define and validate the unique contract key for the artifact's exchange/segment/venue/date, including underlying/security identity, expiry, instrument family, strike, option type and applicable series fields. Duplicate keys, ambiguous aliases or collisions MUST fail validation rather than select an arbitrary row.

### R-139 — Multiple contract-file variants remain separately scoped

NSE-exclusive and NSE/BSE-interoperability MII contract variants MUST retain their own file identity and schema profile. The order validator MUST select the correct variant for the requested venue and member capability, not union all rows into an unqualified universe.

### R-140 — Admission Type is parsed by variant-specific mapping

The Admission Type field MUST use the field number/code mapping for the exact file variant and circular. Unknown codes, shifted fields or a venue mismatch MUST return UNKNOWN/unsupported and block dispatch; the loader MUST NOT reuse the field 13 mapping for the field 30 file or vice versa.

### R-141 — Lot size, quantity unit and freeze quantity remain distinct

The loader MUST store market lot/multiplier, raw quantity unit, broker payload unit and quantity-freeze value separately, each with source/version/effective date. A separate lot/freeze report MUST only be used when the applicable circular/report schedule establishes its coverage and precedence.

### R-142 — Separate quantity-freeze and lot report lifecycle is date-versioned

The loader MUST preserve the circular history for `Qtyfreeze.csv` and `fo_mktlots.csv`, including discontinuation/reintroduction/effective date. Presence or absence of a standalone report MUST NOT be interpreted using an outdated circular; it MUST be resolved against the current report catalogue and contract-file instructions.

### R-143 — Contract snapshots are promoted atomically

A candidate contract-data snapshot MUST remain invisible to order admission until all required artifacts and validations for the target session/effective date have passed. No partial current file may be combined with rows from a previous effective-date snapshot to create a green/complete result.

### R-144 — Related artifact conflicts fail closed

A conflict between the contract master, date-specific freeze/lot report, corporate-action adjustment or circular-announced limit MUST be resolved against an explicit effective-source hierarchy. If unresolved, affected contract fields and order-admission gates MUST remain UNKNOWN; no silent max/min/newest-file fallback is allowed.

### R-145 — Expiry, status and session coverage are complete

Every candidate contract row MUST be checked against the applicable expiry, trading status, suspension/listing/admission and session calendar. A stale contract row remaining in an old file MUST NOT make an expired or suspended instrument tradable.

### R-146 — Venue admission and alternative trading route are enforced

A contract's Admission Type and applicable circular MUST be checked against the requested exchange/venue and member/broker route. BSE-exclusive or otherwise restricted contracts MUST NOT be submitted through a disallowed venue; unsupported alternative-trading-venue handling MUST return UNKNOWN/unsupported.

### R-147 — Promotion and invalidation are auditable

Each promoted or rejected snapshot MUST retain source file hashes, circular/schema versions, exact validation results, rejected rows/reasons, promotion actor/process and effective interval. A later correction, circular or contract change MUST invalidate the affected snapshot/approval and trigger re-ingestion before order admission.

## 8. Additional deterministic acceptance scenarios

These extend AT-001 through AT-250. Use synthetic contract files, circular metadata and fake file-acquisition fixtures only.

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

## 9. Open questions and data limitations

1. The actual NSE MII contract files and dated `NSE_FO_contract_ddmmyyyy.csv.gz` for 8 November 2026 were not downloaded or parsed.
2. The complete current schema and code lists for all MII variants and dated FO CSV are not fully closed by the circulars reviewed here; field-level parser implementation remains deferred.
3. The standalone `Qtyfreeze.csv`/`fo_mktlots.csv` chronology includes discontinuation and later reintroduction notices; the latest current report catalogue and exact route-specific precedence must be rechecked at the time of integration.
4. The exact per-row relation between `contract.gz`, the dated FO CSV, separate freeze/lot reports and provider-specific instrument masters has not been established with real sample files.
5. Admission Type values other than the BSE-listed value documented in FAOP/73629 require a complete current schema/code list before implementation.
6. Whether every member/broker/API route exposes the same NSE/BSE-exclusive variants is not established by the public files reviewed.
7. The current daily MII file publication time, correction/replacement semantics, checksum/manifest availability and expected record counts remain to be verified from the official distribution process.
8. The full freeze/lot file schema, field-level units and code lists in the standalone reports require actual current report documentation/sample rows.

Until these are closed, the current data loader must not issue a tradability PASS based on an inferred or partially parsed contract master.

## 10. Research decisions and non-authorization

- **ACCEPT:** treat contract data as versioned families/variants rather than one timeless file schema.
- **ACCEPT:** bind field maps to exact source variant/circular; preserve the different Admission Type field positions.
- **ACCEPT:** retain publication, capture and effective times separately.
- **ACCEPT:** separate lot, units, freeze, MWPL and position limits.
- **ACCEPT:** use staged validation and atomic snapshot promotion; partial file sets are not current masters.
- **ACCEPT:** BSE-exclusive/alternative venue admission remains a first-class contract-routing condition.
- **DEFER:** field-level parser schema and current-file precedence until the 8 Nov 2026 MII/CSV/auxiliary files and sample records are actually obtained and inspected.
- **NOT AUTHORIZED:** exchange/member portal login, current file acquisition requiring member access, broker/clearing/API calls, sandbox/production interaction, real orders, code changes, paid services, PR or merge to `main`.

**Final status:** PX-035 contract-file ingestion, schema variants and integrity requirements documented. PX-025 expanded to 147 requirements and 280 proposed acceptance scenarios. Current daily files and full row schemas remain uninspected; no parser or broker/exchange interaction was executed.
