# 2023 Final Targeted Evidence Hunt v1

## Purpose

This pass targets the remaining Indian-market evidence gaps identified by the 2023 contradiction/gap audit. The rule is strict: current implementations are capability references, not historical 2023 evidence unless a dated release, commit, paper, archived documentation, or other contemporaneous artifact establishes the capability in 2023.

## Evidence status

| Capability gap | 2023 status | Evidence strength | AlgoX interpretation |
|---|---|---:|---|
| Broker API boundary | Evidence found | C2 | Adopt as a core boundary pattern |
| Instrument master / provider identity | Evidence found | C2 | Adopt canonical identity + provider mapping pattern |
| F&O contract semantics / expiry | Partial evidence | C1-C2 | Treat as required capability; historical implementation coverage remains incomplete |
| Margin / buying power | Partial evidence | C1-C2 | Capability clearly existed at broker/API boundary; simulation methodology remains a gap |
| Charges / taxes | Partial evidence | C1-C2 | Broker charge calculation existed; historical cross-broker normalization remains incomplete |
| Corporate-action processing | Partial evidence | C1 | Historical Indian implementations found, but provenance/adjustment architecture is not sufficiently closed |
| Realistic fills / partial fills | Insufficient dated Indian evidence | C0-C1 | Keep as explicit gap; use mature non-Indian engines for architectural reference |
| Deterministic tick / order-book replay | Partial evidence | C1-C2 | Indian tick/order-book collection exists; deterministic replay evidence is insufficient |
| Broker disconnect / recovery | Partial evidence | C1 | Operational problem is visible, but dated 2023 recovery implementations are not sufficiently evidenced |
| Multi-broker normalization | Insufficient dated 2023 evidence | C0-C1 | Do not backdate current unified broker projects |

## 1. Broker API boundary — CLOSED FOR CORE PATTERN

Zerodha's Python Kite Connect client has dated July 31, 2023 repository evidence and exposes distinct routes for orders, trades, positions, instruments, historical data, margins, order-margin calculation and contract-note/charge calculation. Its instrument parser also explicitly carries expiry, strike, tick size and lot size fields. This is strong contemporaneous evidence that the broker/API boundary must expose both execution and instrument semantics rather than being treated as a thin order-placement wrapper.

Primary evidence: https://github.com/zerodha/pykiteconnect/blob/master/kiteconnect/connect.py

AlgoX conclusion: **ADOPT** the boundary pattern, but do not treat the Zerodha schema as the canonical internal schema.

## 2. Instrument identity / security master — STRONG CORE PATTERN, HISTORICAL CROSS-BROKER GAP

The 2023-era Kite client provides an instrument dump and parses provider token, exchange, trading symbol, expiry, strike, tick size and lot size. This demonstrates the need for a provider instrument registry. The important architectural distinction is that a provider token is an external identifier; a research/trading platform needs a semantic instrument identity plus provider mappings.

The historical evidence is strong enough for the capability, but not enough to prove that a standardized cross-broker Indian security master was widely established in 2023.

AlgoX conclusion: **ADOPT** canonical instrument identity + provider mapping + validity interval as a design requirement; classify cross-broker normalization as an evidence gap.

## 3. F&O lifecycle and expiry — PARTIAL

Kite's 2023 client explicitly models NFO/BFO/CDS/MCX exchanges and parses derivative expiry, strike and lot size. Historical Indian option-chain projects also show daily instrument synchronization and expiry-specific subscriptions. This is enough to establish that expiry and contract metadata were operational concerns, not merely theoretical fields.

However, the research has not yet found sufficient dated 2023 evidence for a complete Indian contract-lifecycle model covering listing, rollover, expiry, exercise/assignment, settlement and canonical contract lineage.

AlgoX conclusion: **ADAPT** mature trading-engine contract models to Indian exchange semantics; do not claim a complete 2023 Indian lifecycle implementation was found.

## 4. Margin / buying power — PARTIAL

Kite's dated 2023 client exposes account margins, segment margins, order margin and basket margin endpoints. This proves that broker-side margin was an explicit machine-readable capability. It does not by itself prove a correct local buying-power simulator or historical cross-broker margin model.

AlgoX conclusion: separate `broker_margin_observation` from `local_margin_model`; benchmark any local model against broker/exchange evidence before treating it as authoritative.

## 5. Charges / taxes — PARTIAL

The same 2023 Kite client exposes a contract-note/charges calculation route. Paytm Money's client also exposes charge calculation as an API capability. These establish the need to model transaction costs as structured execution evidence rather than hard-coded strategy constants.

The remaining gap is a dated, normalized Indian 2023 cost model spanning brokers, segments, statutory levies, taxes, and product-specific rules.

AlgoX conclusion: **ADAPT** a cost ledger abstraction; retain broker-provided and regulatory evidence separately from derived estimates.

## 6. Corporate actions — NOT CLOSED

A dedicated Indian GitHub project exists for collecting NSE corporate actions, including dividends, bulk/block deals and related market data. This establishes practitioner demand for a separate corporate-action ingestion path. Other Indian market-data projects expose corporate-action retrieval as part of a broader data library.

The evidence found is not sufficient to establish a mature 2023 canonical adjustment/provenance architecture. In particular, AlgoX still lacks dated evidence showing how an Indian 2023 system represented event scope, effective dates, adjustment factors, instrument lineage and reproducible reconstruction of adjusted versus raw series.

AlgoX conclusion: keep this as an explicit research gap. **Do not freeze the corporate-action architecture yet.**

## 7. Realistic fills / partial fills — OPEN GAP

No sufficiently strong dated Indian 2023 implementation was found in this pass that demonstrates a complete realistic fill simulator including partial fills, queue position, market depth, latency, order-type semantics and cancellation races.

This does not mean the capability did not exist. It means the current evidence set does not justify claiming historical coverage.

AlgoX conclusion: use mature execution engines such as NautilusTrader/LEAN as architectural references, but keep Indian-specific realism as an experiment target.

## 8. Tick / order-book collection and replay — PARTIAL

Indian projects around Zerodha demonstrate continuous tick capture, order-book support and option-chain streaming. Kinetick documents a continuously running blotter, MongoDB storage for tick/bar/trade data, ZeroMQ pub/sub, and order-book strategy resolutions. These demonstrate the collection and event-distribution side of the capability.

The missing evidence is a dated 2023 deterministic replay specification with explicit ordering, timestamps, duplicate handling, gap detection, snapshot/delta semantics and reproducibility guarantees.

AlgoX conclusion: **ADAPT** the event-log/replay concept; require a deterministic replay experiment before production adoption.

## 9. Broker disconnect / recovery — OPEN GAP

Broker APIs and long-running tick collectors make connection lifecycle an obvious operational boundary, but the evidence collected here is insufficient to establish a complete 2023 Indian recovery pattern. A production-quality design still needs reconnect policy, resubscription, sequence/gap detection, state reconciliation and safe handling of unknown order outcomes.

AlgoX conclusion: keep this as a high-priority experiment rather than assuming reconnect equals recovery.

## 10. Multi-broker normalization — OPEN HISTORICAL GAP

Current Indian projects clearly demonstrate the value of broker adapters and normalized symbols, but they must not be backdated into 2023. The 2023 evidence set contains multiple individual broker APIs, but not yet sufficient contemporaneous evidence for a mature common normalization layer across brokers.

AlgoX conclusion: **BUILD/ADAPT experimentally** rather than claiming the 2023 ecosystem already solved it.

## 11. Historical classification rule

The following must remain separated:

```text
2023 evidence
    ≠
current implementation
    ≠
capability that probably existed
```

A current project can be used as a **capability reference** while its historical status remains unknown. A dated commit/release/document can upgrade it to historical evidence.

## 12. 2023 gate result

The targeted hunt closes several capability questions enough to support architectural direction:

- broker API boundary — supported;
- provider instrument metadata — supported;
- derivatives contract metadata — supported;
- broker-side margin/charge APIs — supported;
- tick/order-book collection — supported.

The following remain explicitly open:

- canonical corporate-action provenance and adjustment;
- complete Indian F&O lifecycle model;
- realistic Indian fill/partial-fill simulation;
- deterministic replay specification;
- broker disconnect/recovery evidence;
- historically proven multi-broker normalization;
- comprehensive 2023 Indian cost/margin normalization.

Therefore the 2023 synthesis may proceed as a **qualified architectural synthesis**, but it must not be labelled exhaustive historical coverage of the Indian-market implementation ecosystem.

## Decision summary

| Area | Decision |
|---|---|
| Broker boundary | ADOPT |
| Canonical instrument identity | ADOPT |
| Provider-token mapping | ADOPT |
| Contract metadata | ADOPT |
| Local margin model | EXPERIMENT |
| Cost ledger | ADAPT |
| Corporate-action engine | RESEARCH / EXPERIMENT |
| Fill simulator | EXPERIMENT |
| Deterministic replay | EXPERIMENT |
| Recovery/reconciliation | ADOPT as requirement; EXPERIMENT implementation |
| Multi-broker normalization | EXPERIMENT; do not backdate |
