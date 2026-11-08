# PX-2026-044 — Operational observability, incident response and safe recovery

**Research date:** 2026-11-08  
**Status:** SEBI technical-glitch framework reviewed; operational observability and recovery requirements specified  
**AlgoX area:** operations / telemetry / audit trail / incident management / risk containment / broker recovery / business continuity  
**Inputs:** PX-025 R-001–R-293; PX-024–PX-027 broker recovery and stream gaps; PX-030/031 margin monitoring; PX-033 independent risk gates; PX-037 market-data quality; PX-042/043 mode isolation and replay  
**Mode:** research and requirements specification only  
**Non-goals:** no broker connection, no market-feed subscription, no account access, no order, no incident in a production system, no code implementation, no paid service, PR or merge to main

## Executive finding

A trading platform is unsafe when its operational state is less observable than its financial state. A green dashboard or healthy WebSocket does not prove that every subscribed instrument is current, that every broker command is reconciled, that the kill switch actually stopped new risk, or that the account ledger is complete.

PX-044 defines a layered operating model:
1. **Telemetry:** metrics, structured logs, traces and health signals.
2. **Durable audit/event evidence:** append-only records of commands, gate decisions, external responses, fills, reconciliations and operator actions.
3. **Detection:** alerts for feed degradation, command uncertainty, risk-gate state, reconciliation age, resource saturation and infrastructure failure.
4. **Incident command:** severity, owner, timeline, escalation, runbooks, customer/broker/exchange communications where applicable and evidence preservation.
5. **Safe containment and recovery:** stop risk-increasing actions, preserve potentially working orders, reconcile actual broker state and confirm each protective action independently.
6. **Resilience:** capacity planning, tested software changes, backup/restore, failover fencing, disaster recovery and explicit RTO/RPO.

**Core decision:** operational observability is not merely a dashboard feature. It is a control plane whose failure must itself be detectable. Telemetry may explain a state but is not a substitute for authoritative broker/exchange/ledger evidence. If the platform cannot establish whether an order, kill-switch action, feed gap or recovery step succeeded, the state remains UNKNOWN and new risk-increasing activity is blocked.

## 1. SEBI technical-glitch framework — scope and obligations

### 1.1 Regulatory scope

SEBI circular **HO/38/44/12(1)2026-MIRSD-TPD1**, dated 9 January 2026, reviews the framework for technical glitches in stock brokers' electronic trading systems and supersedes the 25 November 2022 framework.

The circular states that the framework applies to stock brokers:
- providing Internet Based Trading (IBT) or Securities Trading using Wireless Technology (STWT) platforms; and
- having more than 10,000 registered clients (excluding closed accounts) as at 31 March of the previous financial year.

This is a scoped stock-broker framework. PX-044 does not assert that AlgoX as a private research/platform project is itself a covered stock broker. Applicability must be assessed against the actual regulated entity, its services/platforms, client count and current exchange guidelines.

### 1.2 Technical-glitch definition

The circular defines a technical glitch as a malfunction in the stock broker's electronic system, including hardware, software, networks/bandwidth, processes or products/services directly or indirectly related to trading and risk management, occurring during the exchange trading session and causing stoppage, slowing or variance in functions such as:
- login;
- order placement, modification, cancellation, execution, confirmation or status;
- allocation; and
- viewing margin, collateral or funds,

for a **contiguous period of five minutes or more**.

This definition is specific to the covered regulatory framework. AlgoX should use it as a broker-incident classification input where relevant, but its internal engineering incident thresholds can be shorter and may cover more failure classes.

### 1.3 Explicit exclusions and disincentive exceptions

The circular says the following are not considered technical glitches irrespective of duration for this framework:
- global issues such as cloud-service-provider or other global technology-provider disruption causing widespread outage;
- technology disruption at a Market Infrastructure Institution (MII);
- technical issues during new-account/KYC processing;
- back-office issues that do not impact client trading and settlement;
- payment-gateway issues originating at banks, service providers or payment aggregators;
- decision-support tools such as charts, P&L statements and back-office reports.

It separately says the financial disincentive structure does not apply to:
- a technical glitch affecting one of two trading modes (mobile or web) while the other mode functions properly; and
- a glitch that is minor or has minor impact on seamless broker operations.

These are regulatory classification/disincentive conditions. They do not mean AlgoX should ignore such incidents operationally. For example, a payment gateway may be outside the technical-glitch definition but a failed pay-in can still create a funds/settlement risk for the user.

### 1.4 Reporting timelines for covered brokers

The circular states that covered stock brokers must:
- inform the stock exchanges and their clients regarding the technical glitch within **two hours** of occurrence;
- notify clients through their website and another mode such as SMS, email or an application pop-up;
- submit a Preliminary Incident Report (PIR) within **T+1 day**, where T is the incident date; if T+1 is a trading holiday, the next trading day may be used;
- submit a Root Cause Analysis (RCA) within **14 working days** from the incident date;
- submit the reports through the common **Samuhik Prativedan Manch** portal.

The circular also states that reported and independently monitored incidents are examined by stock exchanges for suitable action.

These are regulatory timelines for entities within scope. Internal AlgoX incident response should detect and escalate much earlier; the statutory outer limits must not be used as an operational response-time target.

### 1.5 Capacity planning, software testing and monitoring

The circular calls for:
- capacity planning across servers, network availability and trading application serving capacity;
- monitoring peak load in trading applications, servers and network architecture;
- rigorous testing of application/software changes before production use;
- traceability matrices, change-management processes and periodic asset updates;
- continued exchange monitoring of broker trading systems through the API-based Logging and Monitoring Mechanism (LAMA), with detailed guidance on applicability, key parameters and log preservation.

This supports a broader engineering rule: monitoring, software change control and evidence retention are part of market-operational safety, not optional post-incident tasks.

### 1.6 Business continuity and disaster recovery

The circular references exchange review of BCP/DR applicability based on broker size and technology dependence, including:
- DR site in a different seismic zone;
- frequency of DR drills and trading from DR site;
- Recovery Time Objective (RTO);
- Recovery Point Objective (RPO);
- definition of a disaster for DR implementation;
- BCP/DR coverage in system audits and ISO certification requirements.

It notes that BCP/DR shall not apply to small-sized stock brokers under the revised framework, subject to exchange guidance. The precise requirements for a specific entity must be checked against the applicable exchange circulars and current BCP/DR rules; this note does not define the legal DR obligations for every broker.

Official sources:
- SEBI Circular, 9 January 2026: https://www.sebi.gov.in/sebi_data/attachdocs/jan-2026/1767957683485.pdf
- SEBI press release: https://www.sebi.gov.in/sebi_data/attachdocs/jan-2026/1767956378858.pdf

## 2. Operational observability architecture

### 2.1 Separate telemetry from durable evidence

AlgoX should distinguish:

| Evidence plane | Purpose | Examples | Authority |
|---|---|---|---|
| Metrics | Aggregate health and trends | latency, queue depth, error rate, reconnect count | Diagnostic |
| Structured logs | Explain a specific operation | command validation, adapter response, error reason | Diagnostic/audit support |
| Distributed traces | Follow a request across components | strategy → risk → adapter → persistence | Diagnostic |
| Durable domain event ledger | Record economic/control state transitions | intent, admission, dispatch, fill, cancel, reconciliation | Domain evidence |
| External broker/exchange evidence | Establish actual external state | broker order/trade IDs, positions, contract note, settlement report | Authoritative for corresponding provider/account assertion |
| Incident record | Timeline, impact, cause, response and recovery | incident ID, owner, status, actions, RCA | Operational governance |

A metric that says “order accepted” is not proof that the broker accepted it. A log line that says “kill switch invoked” is not proof that working orders were cancelled or that new entries were blocked. The durable domain event and external evidence remain distinct.

### 2.2 Structured event fields

A structured operational event should preserve, where applicable:
- event ID and event schema version;
- correlation ID, causation ID, intent/command/attempt ID;
- mode and run/mode epoch;
- pseudonymized account/client namespace and provider;
- canonical instrument ID and provider alias;
- component/service and deployment/build version;
- event type, severity, result and reason code;
- event time, source/provider time, UTC receive time and monotonic processing time;
- connection/subscription epoch and broker/exchange IDs where supplied;
- risk-policy and admission-snapshot reference;
- source artifact/hash and data/model/config versions;
- retry count and idempotency scope;
- trace/span reference;
- operator/service identity for manual or automated actions.

Do not log credentials, API secrets, auth tokens, session cookies, private keys or full sensitive client identifiers. Redaction must happen before telemetry leaves the trusted process; error/debug logging must not accidentally serialize request headers or secret-bearing configuration.

### 2.3 Metrics, logs and traces are not interchangeable

- Use **metrics** for SLOs, rates, saturation, freshness distributions and alerting.
- Use **logs** for event-specific context and fault investigation.
- Use **traces** to identify where latency or failure occurred through the service graph.
- Use the **domain event ledger** for replay, idempotency and state reconstruction.
- Use **external statements/responses** to resolve what the broker/exchange/account actually did.

Telemetry sampling or loss must not drop a legally or economically material order/fill/audit event. High-volume market-data traces may be sampled under policy, but the system must retain sufficient raw/event evidence to detect and quantify drops, gaps and sequence uncertainty.

### 2.4 Observability pipeline health is itself observable

Track:
- exporter/collector availability;
- local durable buffer queue depth;
- dropped/overflowed records;
- telemetry send failures and retries;
- clock offset/synchronization;
- storage write/read latency;
- retention and replication lag;
- audit-ledger sequence gaps and integrity-check results;
- alert delivery/acknowledgement status.

If the central telemetry backend is unavailable, a bounded local durable buffer should preserve critical event records. If the durable audit buffer itself fills or fails, the system must generate a local high-severity condition and block new risk-increasing actions that require an auditable admission/command trail.

## 3. Service health, SLOs and alert design

### 3.1 Service-level indicators

Define service-level indicators by subsystem, mode and decision use-case:

**Market data**
- socket/connection liveness;
- subscription acknowledgement/completeness;
- per-instrument and per-field update age;
- stale/out-of-order observation count;
- decode failure and unknown-schema count;
- frame/byte rate, drops, queue depth and consumer lag;
- reconnect duration and unresolved gap duration.

**Order command path**
- validation/admission latency;
- dispatch latency;
- broker acknowledgement latency;
- UNKNOWN command count and oldest age;
- order/trade stream lag;
- duplicate/ambiguous command count;
- open-order reconciliation age;
- cancel/modify uncertainty.

**Risk and account**
- risk-gate PASS/FAIL/UNKNOWN counts;
- margin parameter age and calculation duration;
- actual collection-evidence age and shortfall;
- position-limit/MWPL file age;
- broker-vs-computed position variance;
- ledger/contract-note reconciliation age;
- unsettled delivery/expiry obligation age;
- kill-switch state and verification status.

**Platform**
- CPU, memory, disk, I/O and network;
- queue depth/backpressure;
- worker lag, dead-letter count and retry storm;
- database connection/pool and transaction errors;
- failover/replication lag and checkpoint age;
- build/config/reference-data version mismatches.

### 3.2 SLO design

SLOs must be specified by:
- component;
- operating mode;
- market phase/session;
- instrument/product and required data field;
- severity and customer impact;
- measurement window and exclusion rules.

There is no universal “all feeds must update within X ms” threshold suitable for every illiquid option, benchmark index, EOD report or after-market process. PX-037 requires field/product/session-specific freshness policies. PX-044 requires each SLO to state its source and rationale and to be monitored against actual observations.

### 3.3 Alert priority

A candidate alert priority model:

- **P0 / Critical:** risk-increasing commands may be dispatched despite an UNKNOWN/hard-block gate; paper/shadow reaches live adapter; duplicate live exposure; audit ledger corruption; confirmed kill-switch failure; wrong account/instrument mapping affecting orders.
- **P1 / High:** broker connectivity lost during active orders; growing order-state UNKNOWN; feed loss affecting live risk decisions; position/ledger divergence; margin shortfall or expiry/delivery obligation unresolved.
- **P2 / Medium:** degraded quote field, stale non-critical reference data, rising latency/queue, single component failure with safe redundancy still functioning.
- **P3 / Low:** informational, expected maintenance or non-trading research job failure without risk impact.

Each alert should include incident key, deduplication fingerprint, affected mode/account/instrument scope, first/last occurrence, severity, owner, runbook link and the evidence required to resolve it. Deduplicating repeated alerts must not hide the fact that the incident is ongoing or increasing in scope.

## 4. Incident classification and response

### 4.1 Incident record

Every incident record should preserve:
- incident ID, severity and classification;
- first detection, actual/estimated start, acknowledgement and resolution times;
- affected service/mode/provider/account/instrument scope;
- market/session/settlement phase;
- customer/order/position/ledger impact;
- relevant source events, traces, logs and file hashes;
- alert and escalation history;
- incident commander/owner and responders;
- actions taken, approvals and exact command/evidence;
- containment and recovery state;
- broker/exchange/customer communication records where applicable;
- root cause, contributing factors and detection gap;
- corrective/preventive actions, owners and due dates;
- regulatory applicability assessment and reporting deadlines if the entity is covered.

An incident must not be marked RESOLVED while a potentially working order, unresolved fill, unknown position, unexplained ledger variance or unconfirmed kill-switch action remains open. Operational service restoration and account-risk reconciliation are two distinct closure conditions.

### 4.2 Incident response state machine

Candidate states:
- DETECTED;
- TRIAGED;
- DECLARED;
- CONTAINMENT_IN_PROGRESS;
- CONTAINED;
- RECOVERY_IN_PROGRESS;
- SERVICE_RESTORED;
- ACCOUNT_RECONCILIATION_PENDING;
- RESOLVED;
- POSTMORTEM_COMPLETE;
- REGULATORY_REPORTING_COMPLETE / NOT_APPLICABLE.

The state machine must retain previous state transitions and actor/evidence. “Service restored” does not imply “account reconciled”. “Broker connection restored” does not imply “all missed events recovered”.

### 4.3 Regulatory scope tagging

For a potential stock-broker technical glitch, record:
- whether the affected entity is a stock broker;
- whether it provides IBT/STWT;
- registered client count (excluding closed accounts) as at 31 March of previous FY;
- exchange(s) and client platform(s) affected;
- duration and continuity of the impairment;
- function affected (login/order/modify/cancel/execution/status/allocation/margin/funds etc.);
- applicability/exclusion rationale under the current SEBI circular;
- notification/PIR/RCA deadlines and completion evidence.

Do not trigger a legal filing purely from a generic internal alert without a scoped applicability assessment; do not ignore reporting obligations when the regulated entity is covered. Legal/compliance owner confirms regulatory classification.

## 5. Safe containment and recovery

### 5.1 Containment objective

During an operational incident, the default safe objective is to prevent new unverified exposure while preserving enough capability and evidence to reconcile existing orders and positions.

Containment should be granular:
1. stop new risk-increasing intent/admission;
2. prevent dispatch of commands that fail or have UNKNOWN required gates;
3. preserve read-only broker/feed/position/ledger channels if available;
4. maintain the ability to observe and reconcile existing orders;
5. decide separately whether cancellation, risk reduction or flattening is permitted and safe;
6. verify every protective action through independent evidence.

Do not automatically disable every network path if doing so would remove the only way to observe existing orders. Avoid turning an entry kill switch into a blanket blind disconnect.

### 5.2 Kill-switch semantics

Keep distinct controls and results:
- **ENTRY_BLOCK:** no new exposure-increasing orders;
- **COMMAND_FREEZE:** no new order/modify/replace commands except explicitly allowed containment actions;
- **CANCEL_WORKING:** request cancellation of identified working orders; each cancellation remains pending until independently confirmed;
- **REDUCE_ONLY:** permit only actions proven risk-reducing under the relevant rules;
- **FLATTEN:** an explicitly approved procedure to reduce/close existing exposure; not inherently safe under bans, physical delivery, price limits, margin or stale data;
- **CONNECTOR_DISABLE:** disable a command capability after order state has been captured/reconciled or when required by security containment.

An operator invoking a control is only an intent/action event. The control state must be VERIFIED only after checking the actual command gate and relevant broker/order state. If the verification channel is unavailable, the outcome is UNKNOWN, not SUCCESS.

### 5.3 Recovery order

A safe recovery sequence:
1. freeze new risk-increasing actions;
2. persist incident timeline and local critical event buffer;
3. determine which processes/adapters/data sources failed and the affected time interval;
4. restore read-only connectivity/monitoring first where safe;
5. reconcile all broker open orders and recent order history;
6. reconcile individual trades/fills and child orders;
7. recover positions, holdings, funds/margin, cash ledger and settlement obligations;
8. compare broker observations and local state; preserve source conflicts and UNKNOWN;
9. verify kill-switch/entry-block state and permissions;
10. validate reference files, clocks, feed subscriptions and data freshness;
11. rerun risk/admission readiness against reconciled state;
12. resume only the permitted mode/actions under a recorded operator/system decision.

Never blindly resubmit a timed-out place/modify/cancel request. Never infer that no order exists because the local UI or database has no record. Never mark startup ready until required recovery reports meet the defined completeness rule.

### 5.4 Failover and split-brain prevention

For multi-process/DR failover, the system must ensure:
- a single fenced command authority per broker account/strategy scope;
- leader/lease or equivalent fencing token with monotonic generation;
- old writer cannot continue dispatching after failover;
- shared idempotency/command state is durable and consistent;
- checkpoint/event offset consistency;
- outstanding broker orders are reconciled after failover before new exposure;
- recovery is blocked if ownership/lease status is ambiguous.

A DNS/load-balancer switch alone is not a safe trading failover if both old and new workers can dispatch.

## 6. Capacity, change management and BCP/DR

### 6.1 Capacity and backpressure

Monitor peak as well as average usage for:
- feed ingest, decoding and per-instrument fan-out;
- strategy/risk decision workers;
- order/ack/trade stream consumers;
- persistent store, event log and telemetry buffers;
- broker/API rate limits and retry queues;
- UI/CLI/API serving and concurrent sessions.

Queues must be bounded with explicit backpressure. Silent dropping of market/order/risk events is prohibited. Under saturation, degrade optional analytics/chart/report functions before critical order-state, risk and audit paths. If safe operation cannot be maintained, block risk-increasing actions.

### 6.2 Change management

Every deployment/config/reference-data change should record:
- change request, owner, reviewer and approval;
- build/artifact/config hash;
- dependency and broker API schema versions;
- tests and traceability to affected requirements;
- staged rollout/canary and health criteria;
- rollback procedure and compatibility;
- data/schema migration plan;
- effective time and deployment event;
- post-change validation and incident linkage.

High-risk changes should be tested against deterministic conformance fixtures (PX-043), replay, failure injection and relevant broker-adapter contracts. A successful unit test does not establish live readiness.

### 6.3 RTO/RPO and disaster recovery

Define:
- **RTO:** maximum acceptable time to restore the service or the clearly scoped capability;
- **RPO:** maximum acceptable loss of persisted state/event history;
- recovery scope: market data, strategy, order command, order/trade event log, account ledger, configuration, audit and incident evidence;
- source of truth for each recovered state;
- failover fencing and split-brain test;
- recovery drill schedule and results;
- degraded-mode policy and explicit no-trade conditions.

Do not claim an RTO/RPO without a tested drill. A database backup alone is insufficient if command idempotency, broker open orders and event offsets cannot be reconciled after restore.

## 7. Additional requirements for PX-025

### R-294 — Operational state is observable by subsystem and mode

The system MUST expose health for market data, strategy, risk gates, order command, broker adapter, persistence, accounting, UI/API and observability pipeline independently. A single aggregate green health flag MUST NOT conceal a degraded critical subsystem.

### R-295 — Telemetry and authoritative domain evidence are distinct

Metrics, logs and traces MUST be treated as diagnostic telemetry, not substitutes for durable command/order/trade/ledger events or external broker/exchange evidence. A dashboard or log message MUST NOT prove an order/fill/kill-switch action succeeded.

### R-296 — Structured operational events carry correlation and provenance

Critical operational events MUST retain event ID/version, correlation/causation IDs, intent/command/attempt IDs, mode/epoch, pseudonymized account/provider scope, canonical instrument, component/build, reason/result, source/provider time, UTC receive and monotonic time, policy/adapter version and source reference where applicable.

### R-297 — Secrets and sensitive identifiers are excluded from telemetry

Logs, traces, metrics labels and incident exports MUST NOT expose credentials, API secrets, access tokens, session cookies, private keys or unnecessary full client identifiers. Redaction MUST occur before sensitive payloads leave the trusted process; secret-bearing configuration and request headers MUST NOT be dumped by debug logging.

### R-298 — Observability pipeline loss is itself monitored

The system MUST monitor exporter/collector availability, local buffer depth, telemetry drops, send retries, storage lag, retention, clock skew and audit-event sequence gaps. If critical durable audit buffering fails or fills, a high-severity local condition MUST be raised and new risk-increasing actions MUST be blocked where admission/command evidence can no longer be preserved.

### R-299 — Feed and command SLOs are field/use-case specific

Freshness, latency and availability SLOs MUST be scoped by subsystem, mode, market phase, instrument/product and required data field. A single global heartbeat or latency threshold MUST NOT declare every feed/order path healthy.

### R-300 — Critical alerts are deduplicated without hiding continuing impact

Alert deduplication MUST preserve first/last occurrence, duration, scope growth, severity, owner and acknowledgement history. An alert storm MUST be grouped without suppressing a continuing incident or an increase in affected accounts/instruments/services.

### R-301 — Incident records preserve timeline and evidence append-only

Every incident MUST retain detection, start/acknowledgement, severity, affected scope, market/session phase, customer/order/position/ledger impact, source event references, actions, approvals, recovery results, root cause and corrective actions. Later updates MUST append rather than overwrite the original timeline.

### R-302 — Service restoration and account reconciliation are separate closure states

An incident MUST NOT be marked fully resolved solely because the service is reachable. Potentially working orders, unresolved fills, position/ledger variance, unsettled obligations or unverified protective actions MUST remain open until reconciled or explicitly classified UNKNOWN with approved handling.

### R-303 — Regulatory technical-glitch applicability is explicitly assessed

Where a stock-broker entity is involved, the system/compliance workflow MUST record whether the entity and platform are within the current SEBI technical-glitch framework, including IBT/STWT scope and registered client threshold. A generic platform incident MUST NOT be automatically labelled a reportable SEBI technical glitch without this scope assessment.

### R-304 — Covered-broker technical-glitch threshold and exclusions are versioned

For entities within scope, regulatory classification MUST evaluate the circular's contiguous five-minute trading-session impact definition and explicit excluded issue categories, including global provider/MII disruptions, KYC, non-trading back-office, payment gateway and decision-support tool issues. The current circular/exchange interpretation MUST be referenced by version.

### R-305 — Covered-broker reporting deadlines are tracked independently

Where the SEBI technical-glitch framework applies, the incident workflow MUST track exchange/client notification within two hours, PIR by T+1 (next trading day where T+1 is a trading holiday) and RCA within 14 working days, using the applicable exchange format and reporting portal. These statutory outer deadlines MUST NOT be substituted for internal faster response SLOs.

### R-306 — Capacity planning includes peak loads and critical paths

The system MUST measure peak server, network, application, database, queue and provider/API load. Capacity tests MUST cover high-concurrency market open/close, reconnect storms and incident recovery. Averages alone MUST NOT establish sufficient capacity.

### R-307 — Queue backpressure cannot silently drop critical events

Critical market, broker order/trade, risk, accounting and audit streams MUST use bounded queues with observable backpressure and explicit drop/failure states. If reliable processing cannot be maintained, dependent risk-increasing actions MUST be blocked and event-history completeness marked UNKNOWN.

### R-308 — Software and configuration changes are traceable and tested

Every production-bound code/config/schema/reference-data change MUST retain owner/reviewer, artifact/config hash, affected requirements, test evidence, deployment time, canary/health criteria, rollback plan and post-deployment validation. Unverified changes MUST NOT be silently promoted to live operation.

### R-309 — Incident response has ownership, escalation and typed state

Incidents MUST have severity, commander/owner, affected scope, runbook, acknowledgement/escalation history and typed states from detection through containment, service restoration, account reconciliation and postmortem. Alert acknowledgement MUST NOT be treated as issue resolution.

### R-310 — Kill-switch invocation is not verified containment

ENTRY_BLOCK, COMMAND_FREEZE, CANCEL_WORKING, REDUCE_ONLY, FLATTEN and CONNECTOR_DISABLE MUST be separate, scoped actions. A control MUST only be marked VERIFIED after its actual effect is independently checked; lost control-channel response or missing broker evidence MUST remain UNKNOWN. A kill switch MUST NOT blindly disconnect the only order-observation/reconciliation path.

### R-311 — Recovery preserves ambiguous commands and reconciles external state

After incident/restart, the system MUST recover broker open orders, recent order history, trades, child orders, positions, holdings, funds/margin, cash ledger and settlement obligations before resuming risk-increasing activity. Possibly dispatched commands MUST NOT be blindly retried or considered absent because local state is missing.

### R-312 — Failover uses fencing and one command authority

A failover MUST establish one active command authority per broker/account/strategy scope using a durable lease/generation/fencing mechanism. An old writer MUST be unable to dispatch after failover. Ambiguous lease/ownership, event offset or idempotency state MUST block new exposure until reconciled.

### R-313 — RTO/RPO and disaster recovery are tested and scoped

The system MUST define RTO/RPO per critical capability and preserved data class, including event log, idempotency state, account ledger, configuration and audit. Recovery drills MUST verify backups, restore, fencing, broker reconciliation and degraded-mode policy. Untested objectives MUST NOT be reported as achieved.

## 8. Deterministic acceptance scenarios

These extend AT-001 through AT-520. Use synthetic metrics/logs/traces, fake incident events, local buffers, fake broker recovery and simulated failover only.

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-521 | Order service is healthy while market-data consumer is stalled | Aggregate health must show the feed/consumer degradation; risk gate using affected data is UNKNOWN/blocked |
| AT-522 | WebSocket heartbeat continues but one subscribed instrument has no updates | Socket can remain healthy while per-instrument freshness alert fires |
| AT-523 | Central telemetry backend becomes unavailable while trading services remain up | Local durable critical-event buffer records the outage; buffer depth/send retries are visible; no event silently discarded |
| AT-524 | Local critical audit buffer reaches capacity | Raise critical local incident and block risk-increasing dispatch where evidence cannot be durably recorded |
| AT-525 | Debug logger attempts to serialize authorization headers/API token | Redaction prevents secret emission; test searches logs/traces for secret canaries and fails on leakage |
| AT-526 | Queue overflow drops market-data frames | Record drop count and affected subscriptions; invalidate event completeness and dependent risk admission |
| AT-527 | Broker order event queue lags while socket is connected | Alert on processing/consumer lag; do not declare broker-order subsystem healthy from socket state alone |
| AT-528 | Duplicate critical alerts occur during one ongoing incident | Deduplicate into one incident while retaining first/last time, count, growing scope and acknowledgement history |
| AT-529 | Same failure spreads from one account to multiple instruments/accounts | Incident scope and severity update; deduplication must not hide scope growth |
| AT-530 | Alert is acknowledged but underlying order-state UNKNOWN persists | Incident remains open; acknowledgement is not resolution |
| AT-531 | Service endpoint recovers but one broker order may still be working | Mark SERVICE_RESTORED and ACCOUNT_RECONCILIATION_PENDING; do not close the incident |
| AT-532 | Potential kill-switch command times out after invocation | Mark containment UNKNOWN; verify entry gate and broker working orders independently; no success claim |
| AT-533 | ENTRY_BLOCK succeeds but CANCEL_WORKING has not been confirmed | Record new entries blocked and working-order cancellation pending as separate states |
| AT-534 | Kill switch disconnects the broker adapter before open orders are queried | Flag loss of observability; do not mark working orders cancelled or account safe |
| AT-535 | Operator selects FLATTEN during a stock MWPL ban or physical-delivery constraint | Re-evaluate rule-specific risk; do not assume flatten is always permitted or safe |
| AT-536 | Incident occurs for a covered broker with IBT/STWT and more than 10,000 eligible registered clients | Regulatory applicability is marked IN_SCOPE and reporting deadlines are created |
| AT-537 | Covered-broker trading-related malfunction lasts four contiguous minutes | Internal incident/alert still exists; do not classify solely under the five-minute SEBI threshold as the defined glitch |
| AT-538 | Covered-broker trading-related malfunction lasts five contiguous minutes | Trigger the defined technical-glitch threshold and applicability/reporting workflow |
| AT-539 | Global cloud/MII disruption or payment-gateway/KYC/back-office issue matches an explicit exclusion | Retain operational incident but classify the relevant SEBI technical-glitch exclusion accurately |
| AT-540 | Only mobile app is affected while web trading remains functional | Preserve incident; apply the circular's stated disincentive exception only when conditions are satisfied |
| AT-541 | Covered-broker glitch notification is not sent within two hours | Raise regulatory deadline breach and preserve evidence/timeline; do not reset timer on incident acknowledgement |
| AT-542 | PIR is due T+1 but that day is a trading holiday | Resolve deadline to next trading day under the circular; preserve calendar and computation |
| AT-543 | RCA is still incomplete at the 14-working-day deadline | Escalate deadline risk/breach, retain draft and evidence; do not mark reporting complete |
| AT-544 | Peak load at market open saturates order/event queues while average daily utilization is low | Capacity alert uses peak data; block unsafe risk-increasing paths if critical queues cannot preserve events |
| AT-545 | Deployment changes order adapter schema without linked tests/rollback evidence | Change-management gate fails; live promotion blocked |
| AT-546 | Canary deployment causes error/latency regression | Trigger rollback criteria and preserve deployment/version/incident association |
| AT-547 | New and old failover workers both believe they own broker command authority | Fencing token permits one writer only; old writer dispatch rejected |
| AT-548 | DR restore recovers database but event log/idempotency state is behind | Recovery state UNKNOWN; no order dispatch until state/ broker orders reconciled |
| AT-549 | RTO/RPO targets are documented but no drill has tested them | Mark objective DEFINED/UNVERIFIED, not ACHIEVED |
| AT-550 | Incident recovery report says service is healthy but cash ledger/positions still diverge | Keep ACCOUNT_RECONCILIATION_PENDING; overall recovery is not complete |

PX-025 now contains **313 normative requirements (R-001–R-313) and 550 proposed acceptance scenarios (AT-001–AT-550)**. These are proposed tests only; no production system, broker, market feed, paper/live account or incident was exercised.

## 9. Open questions and boundaries

1. Which exact exchange circulars and operational guidelines implement the January 2026 SEBI technical-glitch framework for each broker class and platform?
2. Which logging and monitoring parameters must covered brokers expose through NSE LAMA, and what log retention/preservation rules apply to each system?
3. What are the actual exchange formats and service interfaces for the PIR, RCA and Samuhik Prativedan Manch submissions?
4. What incident/severity mapping and SLO thresholds should AlgoX adopt by mode, product, market phase and customer impact?
5. Which durable audit store and replication design best fit AlgoX's local-first/single-node initial architecture while preserving event integrity?
6. What fencing/lease design will be used if AlgoX later runs more than one process/host capable of broker dispatch?
7. What are the exact tested RTO/RPO values for data, command state, account ledger and observability? None are asserted by this research.
8. What notification/incident duties arise for a future AlgoX entity depending on whether it is an internal tool, technology vendor, broker-integrated algo provider or regulated stock broker? This requires entity-specific legal/compliance review.
9. How can telemetry retention, client privacy, broker data terms and regulatory evidence preservation be reconciled in a versioned retention/redaction policy?

These are implementation/compliance closure items, not permission to connect to a broker or production system.

## 10. Research decisions and non-authorization

- **ACCEPT:** observability is split into metrics/logs/traces, durable domain events, external evidence and incident records.
- **ACCEPT:** observability pipeline health and event drops are monitored; inability to preserve critical admission/command evidence blocks new risk.
- **ACCEPT:** incident resolution separates service restoration from account/order/ledger reconciliation.
- **ACCEPT:** kill-switch invocation is not proof of containment; actions are scoped and independently verified.
- **ACCEPT:** recovery reconciles open orders, trades, positions, funds, ledgers and settlement before resuming risk-increasing actions.
- **ACCEPT:** failover requires fencing and a single broker-command authority; RTO/RPO are only achieved after drills.
- **ACCEPT:** SEBI technical-glitch applicability and reporting are tracked only for entities/platforms within the circular's scope; internal engineering incident thresholds can be broader.
- **DEFER:** production telemetry stack, audit storage, alert thresholds, incident integrations, reporting portal integration, BCP/DR design and numeric RTO/RPO until architecture and entity role are confirmed.
- **NOT AUTHORIZED:** broker/feed connection, production control changes, live/paper orders, credentials, paid service, code implementation, PR or merge to main.

**Final status:** PX-2026-044 operational observability, incident response and safe recovery requirements documented. PX-025 expanded to 313 requirements and 550 proposed acceptance scenarios. No system, broker, feed, account, order or incident was exercised.
