# PX-2026-041 — Backtest validity, leakage prevention and statistical robustness

**Research date:** 2026-11-08  
**Status:** statistical validation literature and SEBI PaRRVA framework reviewed; no strategy, model or performance series tested  
**AlgoX area:** research protocol / train-validation-test separation / data leakage / model selection / performance statistics / publication provenance  
**Inputs:** PX-025 R-001–R-235; PX-033 order-admission model; PX-037 market-data timing; PX-038 data vintage; PX-039 point-in-time universe; PX-040 execution costs  
**Mode:** research and requirements specification only  
**Non-goals:** no backtest execution, no parameter search, no strategy ranking, no performance claim, no PaRRVA submission, no paid data or verification service, no code implementation, PR or merge to main

## Executive finding

A backtest can be internally consistent and still be statistically invalid. The most common failure modes are not limited to a faulty fill model:
- training and test periods leak through overlapping labels, preprocessing or feature selection;
- repeated parameter/strategy trials select the best noise realisation;
- a final test period is re-used after researchers inspect its results;
- current constituents or revised data are used in a historical period as though they were known then;
- several correlated variants are counted as independent observations, while the actual number of trials is not recorded;
- a large Sharpe ratio is presented without considering non-normal returns, autocorrelation, selection bias or the full trial universe.

The research supports a layered validation protocol:

1. **Chronological protocol:** split by time, keep the final out-of-sample period untouched, and use walk-forward evaluation for repeated model recalibration.
2. **Leakage control:** fit preprocessing/model/feature selection only on each training fold. For labels with multi-period outcomes, purge training labels whose information intervals overlap test labels and apply a justified embargo.
3. **Selection-bias control:** record every strategy and parameter trial, including unsuccessful/manual variants. Use Probability of Backtest Overfitting (PBO/CSCV), Deflated Sharpe Ratio (DSR), or an appropriate data-snooping bootstrap as diagnostics—not as substitutes for sound chronological testing.
4. **Statistical reporting:** report net-of-cost returns, uncertainty, distribution shape, serial dependence, drawdown and capacity alongside any headline performance measure.
5. **Reproducibility and disclosure:** pin the full data, universe, execution/cost and selection history. If risk-return metrics are publicly communicated through a regulated Indian intermediary/Algo-provider route, assess the applicable SEBI/PaRRVA requirements separately from internal research methodology.

**Critical interpretation:** PBO estimates the risk that a strategy selected from a tested family is overfit under the chosen CSCV design; DSR adjusts a Sharpe-ratio significance assessment for multiple trials and non-normality. Neither is a universal probability that a live strategy will fail, and neither can repair look-ahead bias, bad data, unrealistic fills or an unrepresentative sample.

## 1. Chronological evaluation protocol

### 1.1 Separate research roles

Each backtest experiment should separate:
- **Development/training:** feature engineering, model fitting, parameter fitting and initial strategy development.
- **Validation/model selection:** selection among candidate variants, thresholds, features and hyperparameters.
- **Final out-of-sample (OOS):** a later, locked interval used once for final evaluation after the selection protocol is fixed.
- **Forward paper/shadow evaluation:** a later period in which signals and orders are evaluated with the live data/decision pipeline but without claiming fills or returns that were not executed.

A validation interval is not an OOS result if researchers use it to choose parameters or repeatedly modify the strategy. Once the final OOS results are inspected and used to make design changes, that interval has become part of the development history; a new untouched forward interval is needed for an unbiased final claim.

### 1.2 Walk-forward evaluation

For strategies that recalibrate or retrain, use chronological walk-forward folds:
1. fit on an available past window;
2. tune/validate only within the permitted past training/validation area;
3. freeze the fitted strategy and policy;
4. evaluate on the immediately following unseen interval;
5. advance the window and repeat according to the declared retraining schedule.

Preserve every fold's training dates, validation dates, OOS dates, fitted model/parameters, feature pipeline, universe and data manifest. Report both pooled OOS performance and fold-by-fold dispersion; do not hide a failed fold behind a pooled average.

Use expanding-window or rolling-window training only when that choice matches the intended deployment process. The backtest must not train on future data simply because a later fold was available in the dataset.

### 1.3 Final holdout discipline

A final OOS block should be:
- selected before final model tuning is complete;
- stored behind a clear access/approval boundary;
- evaluated only after data, universe, cost, execution and metric definitions are frozen;
- disclosed with its date range and all test decisions;
- marked as consumed once results influence further design choices.

Repeated inspection of the same final holdout turns it into a validation set. Do not call it “unseen OOS” after it has been used for iterative parameter or strategy selection.

## 2. Data leakage and overlapping labels

### 2.1 Fit all transformations inside the training fold

The following must be fitted or selected using only training data inside each fold:
- scaling/normalization and imputation;
- feature selection and dimensionality reduction;
- target/label thresholds;
- model selection and hyperparameters;
- calibration, probability thresholds and ensemble weights;
- strategy rules selected through empirical performance.

Computing a normalization mean, volatility threshold, feature importance, universe filter or PCA basis over the full dataset before splitting exposes information from the validation/test period to training. A pipeline wrapper does not make it safe unless every fitted step is fold-local.

### 2.2 Label interval and information overlap

A financial sample is not always a point observation. A label may depend on a future return path, stop/target outcome, holding period, event window or barrier resolution.

For each labelled observation, preserve:
- feature/decision timestamp;
- label start timestamp;
- label end/resolution timestamp;
- information interval used to compute the target;
- horizon and event/exit rule;
- source and sample identity.

Where a training label interval overlaps a test label interval, that training sample must be purged from the fold. It is not enough to split on the feature row date if the label uses future prices spanning into the test period.

### 2.3 Embargo after test intervals

Purging handles direct label overlap. An embargo can additionally exclude observations immediately following a test interval where serial dependence or feature/label construction can transmit information across the boundary.

The embargo length must be justified by the label horizon, holding period, feature construction and observed dependence—not an arbitrary universal percentage. Record the exact embargo interval and why it was selected. For independent/non-overlapping targets a different policy may be justified, but it must be documented.

The purged K-fold/embargo method described in financial machine-learning literature is a validation design for overlapping labels. It is not interchangeable with forward-only walk-forward testing. The choice depends on whether the experiment is estimating generalisation across dependent samples or simulating deployment through time.

## 3. Repeated trials, data snooping and selection bias

### 3.1 Trial registry

Maintain a permanent trial registry for every tested alternative, including:
- strategy hypothesis and research question;
- parameter set/search space;
- feature set and data transforms;
- universe, market, segment, timeframe and sample period;
- cost/fill model and execution assumptions;
- benchmark and selection metric;
- model/seed/software/environment version;
- data and methodology manifest;
- result, failure reason and researcher decision;
- whether the trial informed a later trial or design change.

Count manual, automated and LLM-generated variants. A discarded experiment still contributed to the selection process if its result influenced what was tried next. Do not record only the final winning strategy.

### 3.2 Probability of Backtest Overfitting (PBO / CSCV)

Bailey, Borwein, López de Prado and Zhu proposed combinatorially symmetric cross-validation (CSCV) as a model-free/non-parametric framework for estimating probability of backtest overfitting from a matrix of candidate strategy returns. The key use is to assess how often the in-sample selected strategy ranks poorly out of sample across the CSCV partitions.

For AlgoX, a PBO report should preserve:
- the full candidate strategy/parameter trial matrix;
- common return dates and missing-data treatment;
- the partition count/design;
- the in-sample selection metric;
- OOS rank calculation;
- estimated PBO and all intermediate results;
- assumptions and limitations.

PBO is sensitive to the tested strategy family and return matrix. It is a diagnostic of selection overfit within that experiment, not a guarantee of future performance. Do not compute PBO from only the final winner or omit unsuccessful trials.

### 3.3 Deflated Sharpe Ratio (DSR)

Bailey and López de Prado's DSR addresses two important sources of inflation in a selected Sharpe ratio:
- selection bias from multiple trials;
- non-normality of returns.

A DSR report should pin:
- observed Sharpe and the return frequency/annualization;
- skewness and kurtosis assumptions/estimates;
- number of trials and effective trial-count assumptions;
- cross-trial dependence/correlation assumptions where used;
- benchmark/selection process and sample length;
- the exact formula/library/version and output.

The raw number of parameter combinations is not necessarily the number of independent trials when strategies are highly correlated. Conversely, counting only a small number of named strategies while omitting many manual variants understates selection. Report the raw trial count and explain any effective-count adjustment.

A high DSR does not cure look-ahead leakage, unrealistic fills, short sample length or a strategy's failure under a forward test.

### 3.4 Data-snooping bootstrap and family-wide tests

White's Reality Check bootstrap was applied by Sullivan, Timmermann and White to evaluate technical trading rules while accounting for the full universe of rules examined. A family-wide bootstrap test can supplement PBO/DSR when testing many related strategies against a benchmark.

The research record should state:
- the complete hypothesis family;
- benchmark/null;
- resampling method and dependence-preserving block choice;
- number of bootstrap replications and random seed;
- test statistic and multiplicity correction;
- p-value/confidence result and limitations.

Do not select the hypothesis family after seeing which members performed well.

## 4. Sample length, dependence and performance reporting

### 4.1 Performance is more than Sharpe

A backtest report should include, as relevant:
- net and gross return, CAGR and cumulative wealth;
- volatility and Sharpe/Sortino with explicit risk-free/benchmark assumptions;
- maximum drawdown, duration and recovery;
- Calmar and downside/tail measures;
- skewness, kurtosis and worst-period losses;
- hit rate, payoff ratio and expectancy;
- turnover, trade count, average holding period and time in market;
- market/sector/contract exposure, gross/net exposure and leverage;
- margin utilisation, liquidity/participation and capacity;
- transaction-cost components and slippage sensitivity;
- fold/subperiod/regime dispersion and benchmark-relative return.

Report the exact return frequency, compounding, annualization factor, missing-session treatment and risk-free rate. Do not annualize intraday Sharpe with an arbitrary square-root multiplier when serial dependence and overlapping returns invalidate the IID assumption.

### 4.2 Uncertainty and effective sample size

Trade count is not the same as independent sample count. Consecutive trades, overlapping holding periods, correlated instruments and common market regimes can create dependence.

Where confidence intervals or bootstrap tests are used, preserve appropriate temporal dependence (for example, a declared block/bootstrap design). Report sample size, effective-observation assumptions and the method. Do not treat thousands of highly correlated intraday trades as thousands of independent experiments.

There is no universal minimum number of trades or years that validates every strategy. Required sample length depends on horizon, turnover, dependence, effect size, market coverage and statistical power. Where evidence is insufficient, label the result inconclusive rather than inventing a universal pass threshold.

### 4.3 Baselines and robustness

Evaluate the candidate against:
- a relevant passive benchmark (price return or TRI as appropriate);
- simple naive/low-complexity strategy baselines;
- cash/zero-exposure baseline where relevant;
- net-of-cost performance at realistic base and adverse cost assumptions.

Robustness checks should be defined before selecting the winner and may include:
- rolling/expanding walk-forward folds;
- distinct market regimes/subperiods defined without looking for favourable breaks;
- parameter perturbations around the selected configuration;
- execution cost and participation stress;
- nearby instruments/segments only when the strategy's hypothesis permits them;
- sensitivity to universe, contract and data-vintage choices.

A strategy that works only under one finely tuned parameter, one instrument or one selected historical interval must be reported as fragile.

## 5. SEBI PaRRVA and performance-claim boundary

### 5.1 PaRRVA operational status

SEBI's 4 April 2025 circular established the Past Risk and Return Verification Agency framework for risk/return metrics of regulated persons, including exchange-empanelled algo providers through stock brokers. SEBI's 29 April 2026 operationalisation announcement says CARE Ratings Limited was recognized as PaRRVA with NSE as PaRRVA Data Centre; following the pilot, regular services began on 4 May 2026.

This is relevant to future external performance communication by regulated/intermediary routes. It is not a statistical method that replaces AlgoX's own internal validation, and it is not evidence that this private research repository or any strategy is PaRRVA-verified.

Sources:
- https://www.sebi.gov.in/legal/circulars/apr-2025/recognition-and-operationalization-of-past-risk-and-return-verification-agency-parrva-_93321.html
- https://www.sebi.gov.in/legal/circulars/apr-2026/operationalisation-of-past-risk-and-return-verification-agency-parrva-_101185.html
- https://www.sebi.gov.in/media-and-notifications/press-releases/apr-2026/sebi-operationalises-past-risk-and-return-verification-agency-parrva-_101187.html

### 5.2 Presentation rules and scope caution

The April 2025 PaRRVA circular's Annexure B prohibits selective display of one specific algo/portfolio when multiple algos/portfolios were submitted for verification, requires the total number and range of positive/negative outcomes and other risk-return metrics to accompany claims, and prohibits arbitrary favourable date windows or selective omission. Its Annexure C requires disclaimers, including that past returns do not assure future returns and verified returns may differ from actual client returns because execution prices and market conditions differ.

The same circular amended the Stock Broker Master Circular so the cited prohibition on references to algorithm performance does not apply where reference is made to PaRRVA-verified risk-return metrics in the manner specified by SEBI. Separate 2026 interim deadlines in the operationalisation circular for IA/RA communication of certified pre-PaRRVA data must not be generalized automatically to every stock broker or algo provider.

Any commercial, client-facing or broker-associated performance claim must be reviewed against the exact current SEBI, exchange, broker and PaRRVA rules and the entity's status. This research note is not legal advice.

Sources:
- https://www.sebi.gov.in/sebi_data/attachdocs/apr-2025/1743761581547.pdf
- https://www.sebi.gov.in/web/?file=https%3A%2F%2Fwww.sebi.gov.in%2Fsebi_data%2Fattachdocs%2Fapr-2026%2F1777473564120.pdf
- https://www.nseindia.com/static/trade/empanelled-algo-providers-exchange

## 6. Experiment protocol for AlgoX

A candidate experiment should proceed through these immutable stages:

1. **Hypothesis:** record economic rationale and falsifiable conditions before search.
2. **Data lock:** pin PX-038/039 data vintage, universe, membership, corporate-action policy and market calendar.
3. **Execution lock:** pin PX-040 fill/cost/settlement assumptions.
4. **Trial plan:** register parameter ranges, features, metrics, model class and permitted search budget.
5. **Chronological split:** create training, validation and a locked final OOS interval before fit/search.
6. **Leakage audit:** record feature availability, label start/end, purging and embargo results for each fold.
7. **Nested walk-forward:** perform model and parameter selection only in the training/validation portions; evaluate each outer OOS segment once.
8. **Trial accounting:** persist all attempted variants, including failed, discarded and manual variants.
9. **Selection-bias diagnostics:** compute PBO/CSCV, DSR and/or an appropriate family-wide bootstrap where their assumptions fit the experiment.
10. **Robustness:** report fold/subperiod variability, parameter sensitivity, market regime and cost stress results.
11. **Final lockbox:** evaluate once after all methodology and parameters are frozen; mark consumed if results drive a change.
12. **Reproducibility:** emit a manifest of source hashes, experiment/trial IDs, code/model versions, splits, metrics, costs, seeds and logs.
13. **Disclosure boundary:** classify output as internal research, paper/shadow observation, actual broker-account record or PaRRVA-verified result. Do not conflate them.

## 7. Additional requirements for PX-025

### R-236 — Research hypothesis and selection criterion are predeclared

Each strategy experiment MUST record its hypothesis, expected mechanism, target, benchmark, selection metric, permitted parameter/search space and evaluation dates before examining validation/final OOS results. Post-hoc changes MUST create a new linked experiment version.

### R-237 — Chronological train/validation/test boundaries are immutable

Every experiment MUST preserve the ordered train, validation and final OOS date intervals. Random shuffling MUST NOT be used for time-dependent financial observations unless a separate statistical justification demonstrates that it is appropriate for the specific target and does not leak future information.

### R-238 — Final OOS is locked and consumed once

The final holdout MUST remain inaccessible to iterative model/strategy selection. Once results are inspected and influence any subsequent change, the interval MUST be marked consumed and cannot be described as untouched OOS for the revised strategy.

### R-239 — All fitted transformations are fold-local

Scaling, imputation, feature selection, dimensionality reduction, calibration, threshold fitting and model parameters MUST be fitted using only the training portion of each fold. A transform fitted on the full history MUST NOT be reused in a test fold.

### R-240 — Walk-forward model selection is nested and chronological

Where model/parameter selection is performed, it MUST occur inside the permitted training/validation window. The outer walk-forward OOS interval MUST remain excluded from fitting, feature selection and candidate ranking until the evaluation step.

### R-241 — Financial labels carry explicit information intervals

Each supervised label MUST retain its feature/decision time, label start and end/resolution time, horizon and information interval. A timestamp on the feature row alone MUST NOT be treated as the complete label interval.

### R-242 — Overlapping train/test labels are purged

Where training and test labels depend on overlapping future return/event intervals, the overlapping training observations MUST be removed from that fold. The purged sample IDs and overlap rule MUST be recorded.

### R-243 — Embargo is explicit and justified

Where residual serial dependence or feature/label construction creates post-test information leakage risk, the validation protocol MUST apply a declared embargo. Its length and justification MUST be based on label horizon, holding period and data-dependence assumptions, not an undocumented fixed default.

### R-244 — Trial registry includes every attempted variant

The experiment registry MUST preserve all tested strategies, parameter combinations, model classes, feature sets, manual changes, prompts and failed/discarded trials that influenced selection. Results MUST NOT report only the winning trial while omitting the search universe.

### R-245 — PBO/CSCV is computed from the full candidate family

Where PBO is reported, the experiment MUST preserve the complete candidate return matrix, common observation dates, CSCV partition design, in-sample selection metric, OOS ranking and calculation version. PBO MUST NOT be estimated from the final winner alone.

### R-246 — DSR records trial count and non-normality inputs

Where DSR is reported, the result MUST preserve observed Sharpe, return frequency/annualization, sample length, skewness, kurtosis, raw trial count, any effective-trial adjustment, dependence assumptions and calculation implementation. A raw Sharpe MUST NOT be presented as deflated or selection-adjusted.

### R-247 — Data-snooping tests preserve the hypothesis family

Where White's Reality Check or another family-wide multiple-testing procedure is used, the experiment MUST pin the full hypothesis family, benchmark/null, bootstrap design, resampling blocks, seed, replications, test statistic and adjusted result. The family MUST NOT be selected after seeing the winner.

### R-248 — Statistical inference accounts for return dependence

Sharpe inference, confidence intervals and bootstrap uncertainty MUST address serial correlation, overlapping holdings/labels, non-normality and cross-instrument dependence as appropriate. Annualization and effective sample assumptions MUST be explicit.

### R-249 — A standard performance panel is reported

A backtest report MUST include gross/net returns, volatility, Sharpe/Sortino assumptions, drawdown depth/duration, tail losses, turnover, trade count, holding period, exposure/leverage, margin use, capacity/participation, cost breakdown and benchmark comparison where relevant. A single headline return or Sharpe MUST NOT stand alone.

### R-250 — Sample adequacy is justified, not hard-coded

A result MUST report sample length, effective observation assumptions, number of independent/overlapping trades and statistical power/uncertainty where estimable. It MUST NOT claim validity from a universal fixed minimum trade count or date span.

### R-251 — Robustness checks are planned and fully reported

The experiment MUST preserve fold/subperiod performance, parameter perturbation, regime and cost-stress tests specified by the protocol. Negative or unstable results MUST remain in the report; they MUST NOT be suppressed in favour of the best interval.

### R-252 — Benchmark and null are appropriate and pinned

Each strategy MUST identify a relevant benchmark and null/baseline consistent with its market, asset, exposure and return convention. Price-return versus total-return benchmarks MUST be distinguished, and benchmark data vintages MUST be pinned.

### R-253 — Adaptive search history is treated as selection

If a researcher changes later experiments after observing prior results, the trial registry MUST retain that adaptive dependency. The subsequent validation/OOS protocol MUST account for the full research path; renaming or branching a strategy MUST NOT reset its trial count.

### R-254 — PaRRVA and public performance status are not self-assigned

Internal backtest metrics MUST be labelled research/simulated unless independently verified under the applicable PaRRVA process. The system MUST retain verification status, scope, entity/algorithm identity, source and effective date if a verified claim is ever imported. A local statistical test MUST NOT be represented as PaRRVA verification.

### R-255 — Performance claims preserve complete selection and disclosure context

Any external risk/return presentation in a regulated broker/IA/RA/algo-provider context MUST be separately checked against the applicable current SEBI/PaRRVA/exchange requirements. The internal experiment record MUST retain all submitted algos/trials, periods, positive/negative result ranges, full risk metrics and required disclaimers so selective winner-only presentation can be detected. Internal research and PaRRVA verification MUST remain distinct statuses.

## 8. Deterministic acceptance scenarios

These extend AT-001 through AT-430. Use synthetic return series, label intervals, trial registries, fake models and deterministic split manifests only.

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-431 | Random shuffle is applied to a chronological price-prediction dataset | Reject split for the time-dependent task unless a justified non-temporal design is explicitly approved |
| AT-432 | Scaler is fitted on the full dataset before train/test split | Detect future-data leakage; require scaler fit independently inside each training fold |
| AT-433 | Feature selection uses OOS performance or future labels | Reject fold; preserve the leakage path and affected sample IDs |
| AT-434 | A rolling label horizon overlaps the test interval | Purge the overlapping training labels and record the overlap decision |
| AT-435 | A label resolves after the test interval starts even though its feature timestamp is earlier | Treat it as overlapping information and purge it from training |
| AT-436 | Embargo is required after a test block due to label horizon/autocorrelation | Apply the configured embargo and preserve its length/rationale |
| AT-437 | Two strategies have the same final OOS but one was changed repeatedly after observing that OOS | Mark the interval consumed for the revised strategy; it is no longer untouched OOS |
| AT-438 | Walk-forward fold trains on a date later than its OOS evaluation date | Reject fold ordering and report temporal leakage |
| AT-439 | Hyperparameters are tuned using outer OOS results | Detect nested-validation breach; invalidate the claimed OOS result |
| AT-440 | Model is retrained on a rolling schedule using only past data | Preserve each fit window, model version and subsequent OOS window |
| AT-441 | Researcher runs 1000 parameter variants but registers only the winning 10 | Fail trial completeness; require all attempted variants and selection dependencies |
| AT-442 | A manual/LLM-prompt change creates a new strategy variant after reviewing prior performance | Record the variant and its parent trial; do not reset trial count |
| AT-443 | PBO is computed from only the winning strategy's return series | Reject PBO result; require the complete candidate strategy matrix |
| AT-444 | CSCV partitions are formed but date gaps/missing rows differ by candidate strategy | Normalize common observation dates under a declared policy or return UNKNOWN; do not compare mismatched trial samples silently |
| AT-445 | DSR is reported without trial count, skewness or kurtosis inputs | Reject as incomplete DSR; preserve only the raw Sharpe with clear label |
| AT-446 | Multiple strategies are strongly correlated | Record raw trial count and effective-count method; do not claim raw count equals independent trial count |
| AT-447 | White Reality Check is applied after the tested rule family was narrowed to winners | Mark family selection as biased; require the original complete hypothesis family |
| AT-448 | Bootstrap resamples individual returns despite strong serial dependence | Require a dependence-appropriate resampling policy or classify inferential result as unsupported |
| AT-449 | Sharpe annualization ignores return frequency and serial correlation | Flag metric as non-comparable; require declared frequency/annualization and dependence treatment |
| AT-450 | Strategy has high CAGR but deep/long drawdown and negative skew | Report the complete risk panel; do not rank on CAGR alone |
| AT-451 | Strategy performs strongly in one selected subperiod and fails other walk-forward folds | Preserve all fold results and report instability; no best-period-only summary |
| AT-452 | Sample contains many overlapping intraday trades with shared return intervals | Report effective observation/overlap treatment; do not count all trades as independent evidence |
| AT-453 | Sample length or trade count is low for the requested inference | Mark evidence inconclusive/low power; do not apply a universal PASS threshold |
| AT-454 | Strategy uses TRI as benchmark but raw price-only portfolio cashflows | Flag return-convention mismatch and require consistent dividend treatment |
| AT-455 | Final OOS results are examined and then parameters are tuned to improve them | Mark OOS consumed and require a new untouched forward evaluation period |
| AT-456 | Current index constituents are used in a historical walk-forward model | Fail point-in-time universe gate and flag survivorship bias |
| AT-457 | Backtest uses corrected historical data unavailable at simulated decision time | Mark data-vintage/lookahead mismatch; require declared latest-corrected versus as-published policy |
| AT-458 | Strategy passes before transaction costs but fails after PX-040 costs | Report net-of-cost failure; do not present gross success as deployable evidence |
| AT-459 | PaRRVA status is set to VERIFIED because internal DSR/PBO tests pass | Reject status; only the applicable external PaRRVA process can establish verification |
| AT-460 | Public claim selects one winning algo from many submitted algos and omits negative-result ranges/date context | Flag selective-presentation risk; require applicable PaRRVA/SEBI review and complete disclosure context |

PX-025 now contains **255 normative requirements (R-001–R-255) and 460 proposed acceptance scenarios (AT-001–AT-460)**. These scenarios are proposed; no backtest, model validation, statistical calculation or PaRRVA submission was executed.

## 9. Open questions and limitations

1. PBO/CSCV and DSR implementations must be validated against the selected return-matrix structure, number and dependence of trials, missing observations and strategy selection process.
2. Purging and embargo require each label's actual information interval; a simple fixed time-series split cannot determine overlap when labels have variable exit times without those intervals.
3. A pure walk-forward out-of-sample evaluation, CSCV/PBO and a final locked holdout answer different questions; no single metric replaces the others.
4. Return distributions, serial dependence, trial correlation and statistical power vary by strategy horizon and market; no universal DSR/PBO cutoff or minimum sample count is imposed here.
5. SEBI PaRRVA operational processes and detailed verification methodologies may be revised. This research does not determine AlgoX's legal status or whether any planned commercial activity requires registration/empanelment.
6. The 2026 PaRRVA operationalisation circular's specific interim deadline extension for IAs/RAs is not generalized to every broker/algo-provider category.
7. No model, return series, backtest, trial matrix or external verification service was used to test these requirements.

## 10. Research decisions and non-authorization

- **ACCEPT:** chronological, nested, walk-forward validation with a truly locked final OOS period.
- **ACCEPT:** fold-local fitting, label-interval purging and justified embargo where overlapping horizons create leakage.
- **ACCEPT:** complete registry of all tried variants, including discarded/manual/LLM-generated trials.
- **ACCEPT:** use PBO/CSCV, DSR and/or family-wide data-snooping bootstrap as complementary diagnostics where their assumptions fit.
- **ACCEPT:** report complete net performance, uncertainty, risk, costs, capacity and fold dispersion—not only the best Sharpe/CAGR.
- **ACCEPT:** separate internal research evidence from SEBI/PaRRVA verification and external performance claims.
- **DEFER:** choose exact split windows, embargo lengths, trial-count estimators, bootstrap design and promotion thresholds per strategy after label/data structure is defined.
- **NOT AUTHORIZED:** strategy performance claims, PaRRVA submission, exchange/broker registration, live trading, code changes, paid service, PR or merge to main.

**Final status:** PX-041 backtest validity, leakage prevention and statistical robustness requirements documented. PX-025 expanded to 255 requirements and 460 proposed acceptance scenarios. No backtest or statistical test was executed.
