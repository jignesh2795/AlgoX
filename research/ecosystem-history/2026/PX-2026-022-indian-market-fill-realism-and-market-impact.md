# PX-2026-022 — Indian-market fill realism, queue reconstruction and market impact

**Research date:** 2026-11-08  
**Status:** research synthesis; source/version and data-entitlement verification still open  
**AlgoX area:** market simulation / execution research / historical market data  
**Scope:** 2023-era capabilities and constraints; no implementation decision

## Executive finding

A credible fill simulator must model several distinct mechanisms rather than treating "partial fills" as a single feature:

1. executable liquidity and book-walking;
2. passive-order queue position and fill probability;
3. latency and the market state changing before an order reaches the matching engine;
4. residual market impact not already represented by displayed depth;
5. brokerage, exchange charges, taxes and other statutory costs.

These components must remain separately observable so the simulator does not double-count spread, depth consumption, slippage or impact.

The research reviewed NautilusTrader, QuantConnect LEAN and Backtrader as reference-engine approaches. The working comparison from this audit is that NautilusTrader's L2 matching path supports partial execution against available depth, while passive partial-fill coverage in the reviewed tests was incomplete/skipped; LEAN's historical default fill assumptions could fill fully even when a volume-share slippage model was configured; and Backtrader requires a custom filler to make volume constrain execution. These are version-specific observations and must be rechecked against pinned 2023 source revisions before being used as definitive historical claims.

## 1. Execution-fidelity ladder

| Level | Required inputs | What can be claimed | What cannot be claimed |
|---|---|---|---|
| L0 — bar approximation | OHLCV bars | Simplified market/limit fill assumptions | Intrabar path, queue priority or executable liquidity |
| L1 — trade/quote aware | Trades and best bid/ask | Spread-aware fills and coarse slippage | Depth consumption or queue position |
| L2 — market-by-price depth | Timestamped aggregated depth levels | Book-walking, visible liquidity constraints and coarse queue proxies | Exact order priority or exact queue position |
| L3 — order-event reconstruction | Sequenced order add/modify/cancel/trade events plus exchange rules | Reconstructed displayed queue state, subject to feed completeness and latency assumptions | Hidden liquidity, unobserved participants or guaranteed real-world fill outcomes |
| L4 — calibrated execution model | L2/L3 data plus broker/exchange acknowledgements and empirical calibration | Probabilistic fills and calibrated residual impact with uncertainty intervals | Certainty outside the calibration domain |

Do not label an engine "realistic" without stating its fidelity level, input data, assumptions and validation period.

## 2. Aggressive orders: depth and partial fills

For a marketable order, consume available opposite-side levels in price-time order until the requested quantity is filled or the configured execution horizon/liquidity is exhausted. Record each fill separately with price, quantity, event time and source level.

- A market order may be partially filled when visible liquidity is insufficient.
- A marketable limit order must never execute beyond its limit price.
- Residual quantity remains open, expires or is cancelled according to the order's time-in-force and simulator policy.
- A bar's traded volume is not proof that a particular order could have filled at the bar's high/low or close.

## 3. Passive orders: queue and fill probability

For a passive order, the simulator needs an estimate of quantity ahead at the same price and subsequent queue depletion through trades and cancellations. Exchange priority rules determine whether an amendment retains or loses priority; these rules are segment-, order-type- and date-specific and must be pinned to the applicable circular/protocol revision.

With only aggregated market-by-price depth, queue position is approximate. Price, displayed quantity and sometimes order count do not reveal the identity and exact priority of individual orders. A probabilistic model can use spread, depth, imbalance, volatility, trade intensity, estimated quantity ahead and order age, but its output must be labelled an estimate and calibrated out of sample.

True event-level reconstruction requires a complete, correctly sequenced order-event feed, stable order identifiers, timestamps, amendment/cancellation/trade messages, recovery/snapshot semantics and documented priority rules. Missing sequence ranges must invalidate or downgrade the reconstructed state; silently continuing would create false queue certainty.

## 4. Latency, slippage and market impact

Keep these effects separate:

- **Spread:** crossing the prevailing bid/ask.
- **Depth cost:** walking displayed book levels for the requested quantity.
- **Latency drift:** price/book movement between decision, submission and exchange arrival.
- **Residual market impact:** the price response not already captured by consuming displayed depth.
- **Fees and taxes:** explicit cost schedules, not market impact.

Almgren–Chriss-style or square-root impact models are candidate residual models, not automatic add-ons. Calibrate them to data and apply only to the component not already represented by book-walking. Report gross execution price, each cost component and net result independently.

## 5. Indian-market data findings and qualifications

The audit found 2023 NSE materials referring to tick-by-tick/order-and-trade feed capabilities across market segments. It also found protocol-version and later-offering differences that prevent a blanket statement that a particular historical F&O payload remains available today or can be obtained freely.

The following distinctions are mandatory:

- Exchange/member-grade event feeds are not equivalent to retail broker market-depth APIs.
- Aggregated broker depth can support book-walking and coarse queue proxies, not exact order-by-order queue reconstruction.
- Historical feed access, segment coverage, protocol revision, licensing, redistribution rights, retention and cost must be verified independently.
- A 2023 circular describing a feed does not establish present-day entitlement or availability.
- Exact F&O packet mapping and protocol continuity remain **unresolved** in this research pass. Do not treat archived protocol documents as proof of current access.

## 6. Acceptance criteria for a future simulator study

A simulator evaluation should include at least:

1. partial fills across multiple price levels;
2. insufficient depth and unfilled residual quantity;
3. marketable-limit price protection;
4. passive queue depletion by trades;
5. cancellation and amendment priority changes under pinned segment rules;
6. sequence gaps, duplicate/out-of-order events, snapshot recovery and stale-book rejection;
7. latency injection between decision, submission and arrival;
8. spread, depth, latency, residual impact, fees and taxes reported separately;
9. calibration/test period separation and out-of-sample evaluation;
10. uncertainty reporting where queue state or impact is inferred rather than observed.

Compare simulated fills with a replayable reference dataset and, where permitted, broker/exchange execution records. Track fill ratio, time-to-fill, adverse selection, implementation shortfall, price improvement, residual quantity and calibration error. Results must be segmented by instrument, liquidity, volatility, order type, size and market regime.

## 7. Research decisions

- **ACCEPT:** use an explicit execution-fidelity ladder; do not collapse all partial-fill behavior into one capability flag.
- **ACCEPT:** separate book-walking, latency drift, residual impact and statutory costs to prevent double counting.
- **ACCEPT WITH LIMITATION:** aggregated depth is sufficient for L2 book-walking and coarse queue estimates, not exact queue reconstruction.
- **INVESTIGATE:** verify the exact NSE 2023 segment-specific circulars, packet schemas, protocol revisions, historical data availability and licensing before claiming L3 coverage.
- **DEFER:** selecting a market-impact formula or claiming a calibrated passive-fill model until suitable data and controlled experiments exist.
- **NOT AUTHORIZED BY THIS RECORD:** implementing a matching engine, connecting a broker, purchasing/licensing data, or changing live/paper execution behavior.

## 8. Follow-up work

1. Build a source register with exact circular numbers, publication dates, protocol versions, segment scope and entitlement terms.
2. Re-verify NautilusTrader, LEAN and Backtrader behavior against pinned 2023 commits/tags; preserve test paths and skipped-test evidence.
3. Identify a legally usable Indian-market dataset for each fidelity level, including a free-data fallback with explicitly lower claims.
4. Specify deterministic replay and data-integrity tests before any queue model is implemented.
5. Design controlled experiments for aggressive fills, passive fills, latency and residual impact separately.

## Evidence discipline

This record captures the research synthesis reached in the 2026-11-08 AlgoX research session. It intentionally distinguishes observed framework behavior, exchange-document leads and unresolved access/protocol questions. The session transcript did not preserve the full bibliography or exact document identifiers; therefore this is not a source-closed historical audit. Add exact primary-source URLs, document IDs and pinned repository revisions during follow-up verification rather than inventing citations.

## Reference starting points

- [NautilusTrader documentation](https://nautilustrader.io/docs/)
- [NautilusTrader source repository](https://github.com/nautechsystems/nautilus_trader)
- [QuantConnect LEAN source repository](https://github.com/QuantConnect/Lean)
- [Backtrader documentation](https://www.backtrader.com/docu/)
- [NSE market data](https://www.nseindia.com/market-data)
