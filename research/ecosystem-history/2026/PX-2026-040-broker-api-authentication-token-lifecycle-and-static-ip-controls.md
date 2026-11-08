# PX-2026-040 — Broker API authentication, token lifecycle and static-IP controls

**Research date:** 2026-11-08  
**Status:** current official broker authentication/static-IP documentation and NSE implementation standards reviewed; no account-specific authentication was performed  
**AlgoX area:** broker adapter security / authentication lifecycle / credential custody / token expiry and revocation / static-IP enforcement / dispatch fencing  
**Providers:** Zerodha Kite Connect, Upstox API V2/V3 and DhanHQ API v2  
**Inputs:** PX-025, PX-033, PX-034, PX-039  
**Mode:** research and requirements specification only  
**Non-goals:** no broker account login, token issuance, static-IP registration/modification, subscription, API call to broker, sandbox/production request, order, code implementation, paid infrastructure, PR or merge to main

## Executive finding

Broker API security is not one credential check. It is the conjunction of separate, provider-scoped facts:

1. **App credentials:** API key/client ID and API secret identify an application; they are not the user's short-lived access token.
2. **User authorization:** interactive login, consent or one-time authorization code binds a specific user/account to an app.
3. **Access token:** a time-limited bearer/session credential authorizes subsequent API requests.
4. **Token revocation/renewal:** providers expose different logout/renewal semantics; no universal OAuth refresh-token contract can be assumed.
5. **Static egress IP:** for order APIs, the actual public IP/NAT egress may need to match a provider/exchange-registered primary/secondary IP.
6. **Order/API scope:** the static-IP requirement applies to different endpoint families by provider; read-only quote/portfolio endpoints are not necessarily covered by the order-placement rule.
7. **Account, app and environment identity:** credentials/tokens/IPs must remain bound to the intended broker, client, API app, segment and deployment environment.
8. **Dispatch freshness:** token expiry, account permissions, API app status, IP registration and actual outbound route must be valid immediately before an authenticated order command.

A valid access token does not prove the request uses a registered static IP. A registered static IP does not prove the token is valid. A token that can read a profile does not by itself prove the account has a particular exchange/product/order permission.

**Decision:** represent app-secret validity, user authorization, access-token lifetime, revocation, IP-registration scope, egress verification and endpoint policy as separate security claims. Unknown, expired, revoked, mismatched or stale credentials/IP state must block order dispatch. The system must never store live credentials in the repository, logs, prompts, client-side bundles or research artefacts.

## 1. NSE static-IP and retail API framework

NSE Circular NSE/INVG/67858, dated 5 May 2025, encloses implementation standards for safer participation of retail investors in algorithmic trading. It says stockbrokers may provide clients API access, and clients must provide static IP address(es) mapped to the API keys connecting to the broker's trading platform. It allows one primary IP and an optional secondary IP for connectivity redundancy. Where clients have multiple API keys, each key can be mapped to the same or separate primary/secondary IPs according to the stated rules.

SEBI Circular 2025/132 extended the implementation milestones and states that the framework in the 4 February 2025 circular, together with exchange implementation standards/operational modalities, applies to all stock brokers from 1 April 2026. NSE's current algo/trading page references NSE/INVG/73992 (30 April 2026) and carries registration/empanelment processes.

These are regulatory implementation standards, not provider-specific OAuth specifications. Broker docs describe how each provider implements the network allowlist and token lifecycle.

Sources:
- NSE Circular NSE/INVG/67858 (5 May 2025): https://nsearchives.nseindia.com/content/circulars/INVG67858.pdf
- SEBI Circular 2025/132: https://www.sebi.gov.in/sebi_data/attachdocs/sep-2025/1759232056254.pdf
- NSE algo framework / implementation page: https://www.nseindia.com/static/trade/platform-services-non-neat-decision-support-tools-algorithm-trading
- NSE empanelled algo providers: https://www.nseindia.com/static/trade/empanelled-algo-providers-exchange

## 2. Provider authentication and token lifecycle

### 2.1 Zerodha Kite Connect

Kite documents an interactive login/token exchange:

1. The user is directed to the Kite Connect login page with the API key.
2. Successful login redirects to the registered redirect URL with a request_token.
3. The application submits the request_token and a SHA-256 checksum derived from api_key + request_token + api_secret to POST /session/token.
4. The returned access_token is used to sign subsequent API calls.

Kite support documents the request token as temporary, valid for only a few minutes and single-use. If it expires or is consumed, it must not be blindly resubmitted as though it were still valid.

The Kite user API documents:
- the access token expires at **6:00 AM the following day**, unless it is invalidated earlier;
- a master logout from the Kite Web trading terminal also invalidates the token;
- DELETE /session/token logs out and invalidates the API session/access token;
- refresh_token is returned only to certain approved platforms for long-standing read permissions; it is not a general refresh-token entitlement for every API client.

Kite explicitly warns never to embed api_secret in a mobile app or client-side application and never to expose the session access_token publicly.

#### Kite static IP

Kite's current static-IP support article states that from **1 April 2026**, a registered static IP is required for API-based order placement. It explicitly says the WebSocket market-data stream and other APIs such as orderbook and positions can continue from any IP address. The support FAQ gives:
- primary IP mandatory and secondary IP optional, up to two IP addresses;
- one change per calendar week;
- configuration at the Kite Connect developer-account level;
- sharing only within the specified immediate-family rules;
- IPv4 and IPv6 support;
- order requests can be rejected when the actual public egress IP does not exactly match the registered IP.

**Documentation chronology:** an older Kite FAQ page still states 1 April 2025, whereas the newer dedicated static-IP support article states 1 April 2026. This report uses the newer dedicated page for the effective date and records the older page as stale documentation; operational verification should use the current Developer Console and applicable exchange standard.

Sources:
- https://kite.trade/docs/connect/v3/user/
- https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/kite-connect-api-faqs
- https://support.zerodha.com/category/trading-and-markets/general-kite/kite-api/articles/static-ip

### 2.2 Upstox API

Upstox documents a standard OAuth 2.0 authorization-code flow:
1. Create an app and register an exact redirect URI.
2. Redirect the user to Upstox login with the client ID, redirect URI and optional state.
3. Receive a single-use authorization code.
4. Exchange the code server-to-server using client_id, client_secret, exact redirect_uri and grant_type=authorization_code.
5. Store the returned access token securely for API calls.

The documentation states:
- customer credentials are entered on Upstox, not collected directly by the integrating application;
- client_secret is confidential and should be known only to the application and Upstox;
- redirect URI must exactly match the registered URI;
- state is returned unchanged when provided, allowing the application to correlate the authorization callback and defend the login transaction;
- the authorization code is **single-use even if token generation fails**;
- the access token expires at **3:30 AM the following day**, irrespective of the generation time;
- the dedicated DELETE /logout endpoint logs out the active user session, making the current session invalid and requiring login again.

Upstox also documents a semi-automated access-token request route where the user approves through a notifier/approval mechanism. The authorization request itself expires at 3:30 AM the following day unless the user approves it earlier. The notifier endpoint must be protected; do not expose token delivery to an unauthenticated webhook.

#### Upstox static IP

Upstox's static-IP management announcement, dated 10 April 2026, documents:
- user-level registration: the same primary/optional secondary IPs apply across API usage regardless of which OAuth client issued the token;
- one update per calendar week;
- successful IP update invalidates existing access tokens and requires the OAuth flow again;
- once enforcement is active, orders may be rejected from an unregistered IP;
- standard IPv4 or IPv6 notation;
- primary IP required; secondary optional.

The update API returns registered IPs, update timestamps and an access_tokens_invalidated flag. This flag is an explicit revocation side effect and must be persisted as a token-state transition.

Sources:
- https://upstox.com/developer/api-documentation/authentication/
- https://upstox.com/developer/api-documentation/get-token/
- https://upstox.com/developer/api-documentation/access-token-request/
- https://upstox.com/developer/api-documentation/logout/
- https://upstox.com/developer/api-documentation/announcements/static-ip-apis/
- https://upstox.com/developer/api-documentation/update-app-static-ips/
- https://upstox.com/developer/api-documentation/get-app-static-ips/

### 2.3 DhanHQ API v2

Dhan documents two individual-trader access-token routes:
- manually generate an access token in Dhan Web;
- generate an access token through an API endpoint when TOTP is enabled.

The documented access token is valid for **24 hours**. The RenewToken endpoint replaces the active token with another 24-hour token, but Dhan specifically says this renewal works only for tokens generated from Dhan Web and fails for an already-expired token.

Dhan also documents an individual user-specific API key/secret flow:
1. Create a user-specific app key/secret and register its app name, redirect URL and optional postback URL.
2. Generate a consent session using app_id and app_secret.
3. The user completes a browser-based login/2FA flow and receives a tokenId.
4. Consume consent using the app key/secret and tokenId to obtain the user JWT/access token.

The API key and secret are documented as valid for **12 months** from generation. The consent endpoint allows up to 25 consentAppId entries per day, but the docs say only one token is generated at any given point. The partner authentication path uses distinct partner_id/partner_secret credentials and must not be mixed with individual account API credentials.

**Important renewal distinction:** RenewToken is explicitly documented for active tokens generated from Dhan Web. The reviewed docs do not establish that an API-key/consent-generated token can use the same renewal path. Do not assume that it can.

#### Dhan static IP

Dhan's authentication page states:
- primary and secondary static IPs can be configured;
- each individual needs a unique static IP;
- after whitelisting, the IP cannot be modified for the next **7 days** (or as recommended by the exchange);
- static IP is required for order placement APIs including normal Orders, Super Order and Forever Order;
- fetching order details or trade details does not require the same IP whitelisting;
- both IPv4 and IPv6 are supported;
- Set IP, Modify IP and Get IP APIs expose the registered values and the next modification date.

The seven-day change limit must be enforced as a policy cooldown, not bypassed with retries or alternate API credentials.

**Revocation limitation:** the reviewed Dhan authentication page documents 24-hour expiry and the restricted renewal behavior above, but this review did not establish a general logout/revoke endpoint for every Dhan token type. Treat explicit revocation capability as UNKNOWN until confirmed in the account/API contract; do not invent an endpoint.

Sources:
- https://dhanhq.co/docs/v2/authentication/
- https://dhanhq.co/docs/v2/

## 3. Authentication, network identity and order admission are independent

A future AlgoX authentication gate should evaluate these separately:

| Gate | Evidence | Failure consequence |
|---|---|---|
| App credential | Correct provider/app/client ID and secret version, valid app status | Block token exchange |
| User authorization | Completed login/consent, verified callback/state, correct client/account identity | Block token issuance/use |
| Access token | Token exists, provider, scope, issue/expiry time, status active | Block authenticated request |
| Revocation state | No logout, master logout, static-IP invalidation, app disablement or incident revocation | Block request |
| Account/API permissions | Exchanges, products, order types and API capability enabled | Block unsupported operation |
| Static IP | Correct account/user/app mapping, registered primary/secondary, actual egress match | Block order endpoints when enforced |
| Session freshness | Token valid through request window; clock and expiry policy valid | Re-authenticate/re-authorize |
| Dispatch fencing | Current auth/IP state still matches immediately before order dispatch | Invalidate admission snapshot |

A successful read request is not proof of permission to place an order. A successful login is not proof that static-IP mapping is complete. A static-IP registration is not proof that a token remains valid after an IP update.

## 4. Provider-scope differences for static IP

| Provider | Registration scope | Primary/secondary | Change cooldown | Documented endpoint scope |
|---|---|---|---|---|
| Kite | Kite Connect developer-account scope; current support article says order-placement IP check only | Primary mandatory, secondary optional; FAQ says up to two | One modification per calendar week | API orders require registered static IP; WebSocket market data, orderbook and positions can be accessed from any IP |
| Upstox | User-level, applies across all OAuth clients | Primary required, secondary optional | Once per calendar week | API order traffic must originate from registered IP when enforcement is active; exact read-endpoint scope should not be generalized without further documentation |
| Dhan | Individual account | Primary and secondary supported | Seven days after registration/change | Order placement endpoints require registered IP; documented order/trade detail reads do not require that IP check |

These differences are provider policy, not one broker-neutral static-IP model. A generic static_ip boolean cannot express the actual requirement.

## 5. Secret custody and credential security model

A future adapter must keep the following credential classes separate:
- app API key/client ID;
- app API secret/client secret;
- one-time authorization request token/code;
- short-lived access token/JWT;
- partner ID/partner secret where applicable;
- TOTP seed/recovery materials (if a provider flow requires local TOTP);
- redirect URI/state/callback configuration;
- static-IP registration metadata (not a secret, but a sensitive security control).

Required security boundaries:
- Secrets are stored only in a dedicated local secret store/OS credential vault or approved secrets manager, not in repository files, committed .env files, source code, logs, screenshots or prompts.
- Access tokens are not embedded in browser/mobile/client-side bundles or user-facing logs.
- Token values and one-time codes must be redacted from exception bodies, HTTP traces, crash dumps and telemetry.
- Use least-privilege app permissions/account scope where the provider exposes them; never assume all provider accounts have identical enabled exchanges, products or order types.
- Use separate credential namespaces for provider, user/account, API app, environment and purpose. Do not share one user's credentials to multiplex other users.
- Authentication callbacks must bind to the initiating session, registered redirect URI and unpredictable state/nonce where supported.
- Authorization codes/request tokens are one-time secrets; process once, record success/failure metadata, then discard the raw code.
- Rotate/revoke on exposure, suspicious activity, account closure or provider instruction. Do not invent an API key-rotation or global-revocation endpoint where the provider docs do not establish one.
- Never automatically create a new user authorization session in a loop when a token is invalidated; require the documented user approval/login path.

## 6. Token lifecycle and dispatch policy

Candidate states:
- NOT_CONFIGURED;
- AUTHORIZATION_PENDING;
- TOKEN_ACTIVE;
- TOKEN_EXPIRING;
- TOKEN_EXPIRED;
- TOKEN_REVOKED;
- APP_SECRET_EXPIRED;
- IP_MISMATCH;
- IP_UPDATE_COOLDOWN;
- ACCOUNT_OR_APP_DISABLED;
- PERMISSION_INSUFFICIENT;
- UNKNOWN.

A token record should preserve:
- provider, account/client ID, API app ID and environment;
- auth flow/version and authorization evidence ID;
- issue time, expiry time and timezone;
- token type/fingerprint (never raw token in ordinary persistence);
- revocation/logout source/time;
- static-IP registration version and actual egress check result;
- API permissions/capability snapshot;
- last authentication validation and last successful API use;
- any rotation/reissue/cooldown metadata.

Before dispatch:
1. Verify correct provider/account/app binding.
2. Verify app key/secret is current and not known exposed/revoked.
3. Verify access token is active and will remain valid for the request window.
4. Verify no logout, master logout, static-IP update/token invalidation or security incident has revoked it.
5. Verify account permissions and app state.
6. Verify the actual public egress address matches the provider's registered address for order calls when required.
7. Revalidate immediately before dispatch if token/IP/app state may have changed.
8. If auth state is unknown/expired/revoked/mismatched, block the order and start only the provider's documented reauthorization path.

Do not blindly retry an order after 401/403/IP rejection. The rejection may happen after an uncertain network/command stage; use PX-024/PX-025 command-recovery rules before sending a new risk-increasing order. An authentication error does not automatically prove that a prior order command never reached the broker.

## 7. Static-IP planning, NAT and failover

The registered address must be the public egress IP actually observed by the broker, not:
- a private RFC1918 address on the local laptop;
- an interface IP inside a container/VM;
- a VPN tunnel address that is not the final public egress;
- an IPv4 address when the request exits via IPv6, or vice versa;
- a developer workstation address if requests are sent through a cloud server/NAT gateway.

A future deployment must:
- pin a fixed public egress IP for each broker/account scope;
- verify primary and optional secondary addresses before use;
- keep route/NAT configuration and provider registration in sync;
- test failover only in an approved non-production validation context;
- maintain the provider's update cooldown calendar;
- plan IP migration before infrastructure replacement;
- treat a static-IP change as a security-state change; where Upstox explicitly invalidates access tokens on update, re-authenticate before order dispatch;
- never use a residential dynamic IP or assume a cloud instance's IP is static unless its public egress is actually reserved.

A secondary address is a backup path only when the provider has registered it and the infrastructure's failover route actually exits through that address.

## 8. Documentation mismatches and open provider semantics

- **Kite static-IP date:** an older FAQ says 1 April 2025, but its newer dedicated static-IP article says 1 April 2026. This report follows the newer dedicated page and records the older page as stale documentation. The current Developer Console configuration and effective exchange standard must still be checked for an actual account.
- **Kite scope:** its current dedicated article expressly separates order placement from WebSocket/orderbook/position reads. Do not generalize the IP check to every request.
- **Upstox scope:** static IP is registered at user level across OAuth clients, and a successful IP update invalidates existing access tokens. The reviewed announcement explains order rejection under enforcement; it does not establish every read endpoint's IP scope.
- **Dhan renewal:** RenewToken is only documented for active tokens generated from Dhan Web. API-key/consent token renewal is not established.
- **Dhan revocation:** a general logout/revoke API for every token type was not identified in the reviewed public docs. Do not infer none exists; mark as unresolved.
- **API key rotation:** the providers' public pages do not provide a common rotation contract or cross-provider secret version semantics. App deactivation/reissue steps must be confirmed provider by provider before implementation.
- **NSE scope:** the NSE static-IP circular maps addresses to API keys; each broker's account/user/app scoping and endpoint enforcement are provider-specific implementations.

## 9. Additional requirements for PX-025

### R-206 — App credentials and user access tokens are separate credential classes

The system MUST distinguish API key/client ID, API secret/client secret, one-time request token/authorization code, access token/JWT and partner credentials. Their issuer, purpose, validity and revocation semantics MUST remain separate. An access token MUST NOT be treated as an app secret or vice versa.

### R-207 — Authentication flow is provider- and version-specific

Kite request-token/checksum exchange, Upstox OAuth authorization-code flow and Dhan individual/partner consent flows MUST be implemented as distinct adapter contracts. The system MUST NOT impose a fictitious common refresh-token or user-login flow on all providers.

### R-208 — One-time authorization tokens are single-use and expiry-aware

Kite request tokens and Upstox authorization codes MUST be treated as one-time credentials with provider-specific expiry semantics. A consumed/failed/expired code MUST NOT be blindly reused; a new documented user authorization flow is required.

### R-209 — API secrets and session tokens are never exposed to clients or logs

API secrets, partner secrets, access tokens, TOTP seeds and authorization codes MUST remain out of source repositories, client-side bundles, prompts, user-visible logs, crash dumps and telemetry. Kite api_secret and Upstox client_secret MUST be stored only in an approved secret store/backend boundary.

### R-210 — Token lifetime and renewal rules are provider-specific

The token manager MUST preserve exact provider expiry time, timezone, issue time and permitted renewal method. Kite next-day 6 AM expiry, Upstox next-day 3:30 AM expiry and Dhan 24-hour validity MUST not be normalized to one fixed duration or assumed refresh policy.

### R-211 — Revocation and logout state must be explicit

Kite DELETE /session/token, Kite master logout, Upstox DELETE /logout and any documented static-IP-triggered token invalidation MUST create explicit revoked-session evidence. Dhan token revocation semantics remain UNKNOWN unless provider documentation or account contract establishes them; expiry is not the same as verified revocation.

### R-212 — Dhan API key and secret expiry are distinct from access-token expiry

Dhan individual API key/secret (documented 12-month validity) MUST have a separate lifecycle from its 24-hour access token. RenewToken MUST be used only for the active Dhan Web-generated tokens explicitly supported by the docs; the system MUST NOT assume the same renewal path works for API-key/consent-generated tokens.

### R-213 — Static IP is a provider-scoped order-access control

The system MUST model static-IP requirement by provider, account/user/app/API key, endpoint family and effective date. A read-only market-data or portfolio API MUST NOT be blocked solely because an order-endpoint rule applies elsewhere, and an order request MUST NOT bypass a required registered IP.

### R-214 — Primary and secondary egress addresses are explicit

The system MUST retain primary and optional secondary registered public IPv4/IPv6 addresses, provider registration scope, effective/cooldown timestamps and actual egress routing evidence. Private interface/container IPs MUST NOT be submitted as though they were the public address seen by the broker.

### R-215 — Static-IP cooldown and token-invalidation side effects are enforced

IP changes MUST observe the applicable provider cooldown (Kite/Upstox one calendar-week update; Dhan seven-day lock as documented). An Upstox successful IP update MUST mark existing tokens invalid and require fresh OAuth. No request may use a stale IP/token combination after an IP change.

### R-216 — Dispatch checks actual egress identity

Immediately before an order API call, the adapter MUST verify that the actual public egress route corresponds to a registered primary/secondary address under that provider's rules. If NAT, IPv4/IPv6 routing, VPN, proxy or failover changes the egress, order dispatch MUST remain blocked until the provider registration matches.

### R-217 — Authentication failure does not authorize blind command retry

Expired/revoked token, invalid IP, 401/403, API-app disablement or permission errors MUST transition auth state explicitly. The system MUST preserve the associated command/attempt status and apply PX-024/PX-025 uncertain-submission reconciliation before retrying any placement/modification that may already have reached the broker.

### R-218 — Credential compromise and rotation are auditable security incidents

A suspected leak, unauthorized token use, account closure, app deactivation or provider revocation MUST trigger a security incident: stop affected dispatch, quarantine credentials, perform only documented revocation/rotation, reauthenticate with user approval and retain non-secret audit evidence. The system MUST NOT invent undocumented global revoke/rotate operations.

## 10. Deterministic acceptance scenarios

These extend AT-001 through AT-395. Use synthetic credential metadata, fake auth callbacks, token timestamps, static-IP state and fake broker responses only.

| Test ID | Scenario | Required observable result |
|---|---|---|
| AT-396 | Kite login returns a request_token that is older than the provider's few-minute window | Reject as expired; require a new user login; do not exchange stale token |
| AT-397 | Kite request_token has already been consumed once | Reject reuse; require fresh login and a new one-time request_token |
| AT-398 | Kite access token reaches 6 AM next day or master logout occurs | Mark token EXPIRED/REVOKED and block authenticated dispatch |
| AT-399 | Kite api_secret is present in client/mobile bundle, Git or logs | Treat as compromised; stop affected integration, redact evidence and require documented secret remediation |
| AT-400 | Kite API order is sent from unregistered egress after 1 April 2026 enforcement | Block/reject order placement; preserve actual public egress and registered-IP mismatch |
| AT-401 | Kite market-data WebSocket/read-only orderbook call originates from a non-whitelisted IP | Apply current provider rule: read-only endpoints remain available from any IP; do not incorrectly treat it as an order-placement violation |
| AT-402 | Kite static IP changes a second time within the same calendar week | Reject/hold update according to cooldown; do not attempt alternate API-key workaround |
| AT-403 | Upstox authorization redirect_uri differs from the registered app URI | Reject authorization/token exchange; do not accept a near-match |
| AT-404 | Upstox callback returns a state value different from the initiating session | Reject callback as uncorrelated/possible CSRF; do not exchange code |
| AT-405 | Upstox authorization code exchange fails once and the same code is retried | Reject reuse because the code is single-use even after failure; initiate fresh user approval |
| AT-406 | Upstox access token reaches 3:30 AM following day | Mark EXPIRED using provider timezone/time semantics and require a new authorization/token flow |
| AT-407 | Upstox DELETE /logout succeeds | Mark the active user session/token REVOKED; subsequent calls require login again |
| AT-408 | Upstox primary/secondary IP is updated successfully | Mark existing access tokens invalid, read response flag, and complete OAuth again before use |
| AT-409 | Upstox IP update is attempted twice within a calendar week | Enforce provider cooldown; do not rotate OAuth clients to bypass user-level limit |
| AT-410 | Upstox two OAuth clients are registered but user-level IP differs for only one | Apply the same user-level registered IP to all OAuth clients; flag any route mismatch |
| AT-411 | Dhan API key/secret reaches 12 months from generation | Mark app credentials expired; require new documented credential/consent flow |
| AT-412 | Dhan access token reaches 24-hour expiry | Mark token EXPIRED and block use; do not assume silent refresh |
| AT-413 | Dhan RenewToken is called for an active token generated from Dhan Web | Replace the old token, record old-token invalidation and store the new 24-hour expiry |
| AT-414 | Dhan RenewToken is attempted after token expiry | Preserve failure; require new supported token-generation flow; do not loop renewal |
| AT-415 | Dhan RenewToken is attempted for API-key/consent-generated token without documented support | Mark operation unsupported/UNKNOWN; do not assume Dhan Web renewal semantics apply |
| AT-416 | Dhan consent flow creates multiple consentAppIds or attempts parallel tokens | Enforce the documented 25-per-day limit and one-token-at-a-time behavior; do not create parallel live sessions |
| AT-417 | Dhan order-placement API call originates from unregistered public IP | Block order placement; compare account's registered primary/secondary with actual egress |
| AT-418 | Dhan order/trade detail read endpoint originates from a different IP | Apply documented endpoint scope; do not misclassify the read call as an order-placement IP violation |
| AT-419 | Dhan static IP was changed within the previous seven days | Block further modification until the provider's next allowed date; preserve cooldown evidence |
| AT-420 | Broker returns 401/403/IP mismatch after a placement attempt times out | Mark auth/network state separately from command outcome; reconcile uncertain order state before retrying placement |

PX-025 now contains **218 normative requirements (R-001–R-218) and 420 proposed acceptance scenarios (AT-001–AT-420)**. These are proposed deterministic scenarios; no credentials, tokens, account sessions, IP registrations, broker APIs or orders were used.

## 11. Open questions and evidence limitations

1. The current accepted Kite Connect agreement and developer-console configuration for any actual account were not inspected; the report relies on current public support/API documentation.
2. Kite's older FAQ still contains a 1 April 2025 static-IP date, while its newer dedicated page says effective 1 April 2026. Current dedicated page and exchange implementation standards are used; actual Developer Console state remains account-specific.
3. Upstox documentation specifies user-level IP updates and token invalidation, but exact read-only endpoint enforcement scope should be confirmed before enforcing a universal IP gate for every API request.
4. Dhan documents RenewToken only for active tokens generated from Dhan Web; it does not establish the same renewal for API-key/consent tokens in this review.
5. A general Dhan logout/revoke API for every token type was not identified in the reviewed public docs. Do not infer none exists; mark as unresolved.
6. A common provider API-key rotation/revocation contract was not identified. Exact key reissue/deactivation procedures remain provider/account specific.
7. Actual public egress may differ from VM/container/private interface addresses due to NAT, VPN, dual-stack routing, proxies or failover. No live environment was inspected.
8. The NSE implementation standards and provider pages must be checked for revisions before any future production deployment; no static IP or algo registration was performed in this research.

## 12. Research decisions and non-authorization

- **ACCEPT:** app secret/client ID, user authorization code/request token, access token/JWT and partner credentials are separate classes with distinct lifecycle.
- **ACCEPT:** token expiry and renewal are provider-specific; Kite 6 AM, Upstox 3:30 AM and Dhan 24-hour validity are not normalized.
- **ACCEPT:** explicit logout/revocation evidence is retained; unknown revocation semantics remain UNKNOWN.
- **ACCEPT:** static IP is a separate endpoint/account/user/app scoped network gate, not authentication and not a universal read-API requirement.
- **ACCEPT:** provider IP cooldowns and Upstox token invalidation after IP update are enforced.
- **ACCEPT:** secrets and tokens remain out of repository/client-side bundles/logs; leaked credentials trigger documented incident response.
- **DEFER:** Dhan consent-token revoke/renew behaviour for API-key flow, Upstox read endpoint IP scope and provider key rotation details pending account/API contract confirmation.
- **NOT AUTHORIZED:** account login, token generation/renewal, credential rotation, static IP registration/modification, broker API calls, sandbox/production use, real orders, paid infrastructure, code changes, PR or merge to main.

**Final status:** PX-2026-040 broker API authentication, token lifecycle, static-IP scope and credential security research documented. PX-025 expanded to 218 requirements and 420 proposed acceptance scenarios. No account, token, IP or broker API was accessed; no code was implemented.
