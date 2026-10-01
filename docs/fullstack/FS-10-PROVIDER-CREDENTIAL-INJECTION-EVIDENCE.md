# FS-10 — Provider-Side Credential Injection: Evidence & Compatibility

| Field | Value |
|---|---|
| **Instruction** | *"AIOS FS-10 — Provider-Side Credential Injection Evidence & Compatibility Gate"* (verbatim: `docs/governance/acts/MI-FS10-PROVIDER-CREDENTIAL-INJECTION-EVIDENCE-COMPATIBILITY-GATE.md`; sha256 `258d072d…`; Register `§121`) |
| **Mechanism** | Claude Code cloud environments — **API credentials** (provider: Anthropic). Here called **M-AC** |
| **Selection** | **UNSELECTED.** Not authorized, configured or implemented |
| **Final classification** | **D. FOUNDER DECISION REQUIRED** |
| **Final state** | **STATE D — FOUNDER DECISION REQUIRED** |
| **O-A / M1 / ESC-03 / FDP-010 / FS-10** | authorized, NOT IMPLEMENTED / FAILED (`§120`) / NOT RESOLVED / NOT COMPLETE / NOT READY |
| **Release / LIVE** | **RELEASE NOT AUTHORIZED · LIVE NOT ACTIVE** |
| **Date** | 2026-10-01 |

No credential was created, uploaded, stored, configured, used, rotated or deleted. No provider setting, X2, B3, FDP-011 or Production state changed. No synthetic test was run: a credential can be added only by the account holder in the environment dialog, and adding even a synthetic one would be a provider configuration change (MI `§2`).

Evidence classes, as the MI requires: **VPD** verified from provider documentation · **DV** directly verified · **UNK** unknown · **N/A** not applicable. INF marks a reasoning step, never a fact.

## 1. Scope

Can the provider's API-credential feature carry the FDP-011 O-A bypass value to the Production request? And is doing so a delivery implementation of the already-authorized O-A, or a different mechanism? This is evidence and compatibility analysis only.

## 2. Canonical sources

`FDP-009` (`§107`), incl. `FDP-009-02` `§5.5` and `FDP-009-03` · `FDP-010` (`§109`), incl. `§4.2` and `§11.4` · `FDP-011` (`§117`; O-A; T1–T9) · `AD-FS10-ESC03` (`§113`–`§114`) · FS-DP-03 `R2.5`, `R2.6`, `R2.10` · T5 feasibility record (`§119`) · M1 validation (`§120`). All re-discovered unchanged; FDP-012 still **not received**.

## 3. Provider documentation

**Sources:**
- code.claude.com/docs/en/cloud-environments, *Add API credentials*, *Which requests get the credential*, *Requests that never get the credential*, *Archive an environment*, *Security proxy* (fetched 2026-10-01).
- code.claude.com/docs/en/claude-code-on-the-web, *Security and isolation*.
- `/root/.ccr/README.md` in the session VM.

| # | Item | Finding | Class |
|---|---|---|---|
| 1 | Feature name | *"API credentials"* on a cloud environment | VPD |
| 2 | Supported plans | *"available on Pro and Max plans. They aren't available on Team or Enterprise plans yet"* | VPD |
| 3 | Availability on this account | plan not readable from any tool here | **UNK** |
| 4 | Scope | per **environment**: *"applies in every session that runs in the environment, whoever started it, until you delete it"*. Environments are *"personal to your account"* unless shared by an Owner | VPD |
| 5 | Storage location | on the environment, at Anthropic; outside the session VM | VPD |
| 6 | Visibility | *"You can't view the value again after saving."* The list shows each credential with its hosts | VPD |
| 7 | Reaches Claude? | *"The key never reaches Claude"* | VPD |
| 8 | Reaches shell commands? | *"…the commands it runs"* — no | VPD |
| 9 | Reaches the session environment? | *"…or the session's environment variables"* — no; *"doesn't appear … in any file"* | VPD |
| 10 | Injection behaviour | *"Anthropic's agent proxy adds the key to requests for the hosts you list, after each request leaves the session's VM"* | VPD |
| 11 | Host matching | *"when the request's host matches one you listed"*; *"A leading `*.` matches every subdomain"*; overlapping-but-unequal hosts: *"the agent proxy sends only one of them"* | VPD |
| 12 | Custom headers | a header row with **Name**, **Prefix** and **Value**; *"For a header like `X-Api-Key` that takes the bare value, change the name and clear the prefix"* | VPD |
| 13 | Request methods covered | not stated (matching is by host) | **UNK** |
| 14 | TLS boundary | the session's TLS is re-terminated at the egress proxy (*"TLS is re-terminated there"*) [DV: README]; injection happens at the agent proxy after the request leaves the VM, so the proxy handles the header in clear | DV + VPD; proxy internals **UNK** |
| 15 | Deletion / revocation | delete the credential in the environment editor. *"There's no edit … delete it and add it again."* Deletion needs no plaintext | VPD |
| 16 | Caching | not stated | **UNK** |
| 17 | Persistence across sessions | yes, until deleted (item 4) | VPD |
| 18 | Persistence across Vercel deployments | N/A to the credential store; it matches hosts, so new deployment URLs need new host entries | VPD (host matching) |
| 19 | Persistence across environment rebuilds | stored on the environment, not in the VM | VPD |
| 20 | Auditability | the list shows credentials, their hosts and a **Not sent** marker with a reason. A per-request audit trail of injection is not documented. The security proxy keeps *"a DNS-level audit trail of requested hostnames"* | VPD (partial); per-request **UNK** |
| 21 | Provider logging | whether the agent proxy logs request headers is not documented | **UNK** |
| 22 | Telemetry | *"Claude Code's telemetry export … doesn't go through the agent proxy"* | VPD; provider-internal telemetry **UNK** |
| 23 | Exposure risks | the value never enters the VM (items 7–9). It is held and handled by Anthropic's proxy and storage. **Any** request to a listed host, from any command or session in the environment, receives it | VPD + INF |
| 24 | Multiple credentials | yes, added *"one at a time"* | VPD |
| 25 | Safe rotation | delete and re-add with the new value; the value never shown | VPD; propagation timing **UNK** |

**Requirements to add one [VPD]:**
- an organization admin role (held by the account owner on Pro/Max);
- an existing Anthropic-hosted environment;
- an API reachable from the internet;
- the organization must not use customer-managed encryption keys (otherwise saving is refused).

**Never attached [VPD]:** GitHub, the Anthropic API and the public package registries, setup-script requests, and Claude Code's own telemetry export.

## 4. Plan entitlement

**PLAN ENTITLEMENT = UNKNOWN.** No tool in this session reads the subscription plan. Session metadata shows a seven-day rate-limit window, which does not establish the plan. Whether the **API credentials** section appears in the dialog for environment `env_01X4j1qVyxMRoTsGvotFpwue` is visible only to the account holder. Customer-managed encryption keys: **UNK**. **PROVIDER / ACCOUNT-HOLDER DEPENDENCY.**

## 5. Exact feature behaviour (summary)

The account holder stores a key with a header name, an optional prefix and a host list. For every request **from any process in any session of that environment** to a listed host, the agent proxy adds the header after the request leaves the VM. The key cannot be viewed after saving and stays active until deleted [VPD].

## 6. Target request analysis

| Element | Value | Class |
|---|---|---|
| Hostnames (FDP-011 T2) | Production alias `aios-platform-adibelepp21-bytes-projects.vercel.app`; serving `aios-platform-72l8flelz-adibelepp21-bytes-projects.vercel.app`; designated target `aios-platform-9dhc3bfal-adibelepp21-bytes-projects.vercel.app` | DV |
| Paths | `/api/v1/*`, `/` | DV |
| Protocol | HTTPS (443) | DV |
| Methods | `GET`; `POST /api/v1/runs` | DV |
| Required header | `x-vercel-protection-bypass: <bypass>` | VPD (Vercel) |
| Proxy can attach it? | custom header name with cleared prefix is documented | VPD |
| Vercel accepts it? | yes — documented, and verified under FDP-009-03 | VPD + DV |
| X2 uses it to admit O-A? | the same header as the FDP-009-03 bypass, which X2 admitted | DV |
| B3 receives the request? | yes; B3 then reads the `aios-operator` bearer, sent by the client in `Authorization`, not by the proxy | DV (FDP-010) |
| Interference | B3's `Authorization` header must not be the injected header (header name `x-vercel-protection-bypass`, not the default `Authorization`/`Bearer`). The hosts are reachable from this VM today (302 observed) | VPD + DV |
| Exact-host restriction | possible: three exact hosts, no wildcard | VPD |

Technically, the injected header reaches X2 in the same form as the O-A credential.

## 7. O-A compatibility

| Aspect | Finding |
|---|---|
| X2 contract | **unchanged**: the same Vercel Protection Bypass for Automation, the same header, revoked in the Vercel dashboard. No new trust source, identity provider or header contract at X2 |
| What changes | **custody and delivery**: a third party (the Anthropic agent proxy) holds the bypass value and attaches it on behalf of **every process and session in the environment** that calls the listed hosts, until the account holder deletes it |
| `FDP-011` D-1 | *"The bypass exists only for an explicitly authorized operational session"* — the bypass on Vercel can be session-bounded by the account holder; the proxy attachment is **environment-wide** while it exists |
| `FDP-011` T5 | requires custody *"within an authorized secure execution/secret-handling path"*; **no instrument designates this path** |
| `FDP-010` `§4.2` | *"Provider credentials remain stored in the provider's appropriate secret mechanism."* Storing a Vercel protection secret in another provider's (Anthropic's) credential store is either consistent with this or not, depending on how *"the provider's appropriate secret mechanism"* is read. **The text does not settle it** |
| AD-FS10-ESC03 (S7) | a holder of the edge credential outside the CEO's custody is a **new trust boundary** (the agent proxy), recorded as a security criterion |

**Classification:**
- At X2, the mechanism is the **same** O-A.
- As a custody and delivery path, it is **not designated** by any canonical instrument.
- It depends on a reading of `FDP-010` `§4.2` that the text leaves open.
- It is environment-wide, while D-1 describes a per-session bypass.

Whether this is *"a credential-delivery implementation of O-A"* (A) or *"a materially different mechanism"* (B) **cannot be settled from the canonical texts**: X2 says A; custody, scope and `§4.2` leave B open. Per MI `§6`: **HARD STOP — ARCHITECTURE / AUTHORITY AMBIGUITY.** Not assumed to be O-A.

## 8. T5 compatibility

| T5 requirement | Evidence | Result |
|---|---|---|
| not in chat | value entered in the claude.ai dialog by the account holder; never in conversation | PASS (VPD) |
| not in normal tool output | *"never reaches Claude, the commands it runs"* | PASS (VPD) |
| not in repository / source / documentation / evidence | never in the VM or any file | PASS (VPD) |
| not in logs | VM-side: never in the VM. Agent-proxy and Vercel request logs: undocumented | **UNKNOWN** |
| not in the normal session environment | *"or the session's environment variables"* | PASS (VPD) |
| not retained after the operational session | stays active *"until you delete it"*; whether running sessions keep it after deletion, and whether the proxy caches it, are undocumented | **UNKNOWN** |
| controlled creation | the account holder, in the Vercel dashboard (bypass) and the environment dialog (credential) | PASS (VPD) |
| controlled custody | Anthropic storage and proxy; **not designated** as T5's authorized path; `§4.2` reading open | **UNKNOWN** (authority) |
| controlled delivery | attached to **every** request to the hosts from **any** process or session in the environment | **FAIL** (not limited to the authorized session) |
| controlled use | as above | **FAIL** |
| rotation | delete and re-add; value never shown | PASS (VPD) |
| revocation | Vercel bypass revoked in the dashboard; credential deleted in the dialog; no plaintext needed | PASS (VPD); immediacy **UNKNOWN** |
| evidence without the value | T8 fields need no value | PASS |

## 9. Session / lifetime analysis

| Question | Finding |
|---|---|
| Created for one session only? | **no** — no per-session option documented |
| Environment-wide? | **yes** (VPD) |
| Usable by all sessions? | **yes**, *"whoever started it"* (VPD) |
| Unrelated sessions? | **yes** — any session in the environment that calls a listed host |
| Routine tasks? | **yes** — Routines run in environments (VPD); none exist now (DV) |
| Single execution? | **no** — every request to a listed host |
| Deletion immediate? | **UNK** |
| Running sessions keep access after deletion? | **UNK**. On *archiving*: *"API credentials on the environment stay attached in its running sessions"* (VPD); deletion not stated |
| Proxy caching? | **UNK** |
| Deletion invalidates immediately? | **UNK** |

"The credential does not reach Claude" holds. **"The credential is session-isolated" does not hold:** the mechanism is environment-wide until deleted. Creating and deleting it around a session does not make it per-session.

## 10. Telemetry analysis

- **VM-side telemetry and Claude Code's telemetry export:** the value is never in the VM, and the export *"doesn't go through the agent proxy"* (VPD).
- **Provider-internal telemetry and tracing of proxied requests:** undocumented → **UNKNOWN** (hard stop for implementation).

## 11. Logging analysis

| Channel | Finding |
|---|---|
| Claude transcript, shell, process environment | value absent (VPD) |
| AIOS logs | no header logging (`§120` `§8`; DV: code) |
| Vercel request/runtime logs | header logging undocumented — **UNK** |
| Agent-proxy logs | only *"a DNS-level audit trail of requested hostnames"* documented for the security proxy; header handling **UNK** |
| Error reporting, network debugging | inside the VM the value is absent, so a verbose client cannot print it (VPD); proxy-side **UNK** |

## 12. Revocation analysis

| Question | Finding |
|---|---|
| Who deletes | the account holder (organization admin role) (VPD) |
| How | environment editor, delete the credential (VPD); and revoke the Vercel bypass in Deployment Protection settings (VPD, Vercel) |
| Needs the plaintext? | no (VPD) |
| Dashboard? | yes, for both (VPD) |
| Without exposure? | yes |
| Immediate? | **UNK** |
| Cached copies? | **UNK** |
| Verification | after **revoking the Vercel bypass**, any request to the hosts answers 302 whether or not the proxy still attaches the old value. This is verifiable by the CEO without the value (DV method, FDP-009-03). That the **credential itself** is gone is visible only to the account holder in the list |
| Subsequent request rejected | yes, once the bypass is revoked at Vercel (DV method) |

## 13. Security boundary (facts, not a ranking)

| Property | Finding |
|---|---|
| Least privilege | X2 passage only; B3 still requires the `aios-operator` bearer (unchanged) |
| Host restriction | exact hosts possible (VPD) |
| Header restriction | one named header (VPD) |
| Credential scope | the Production project's bypass (Vercel) |
| Environment scope | the whole environment |
| Session scope | none |
| Rotation | delete and re-add (VPD) |
| Revocation | dashboard, both sides (VPD) |
| Auditability | credential list and hosts; per-request **UNK** |
| Exposure | outside the VM; inside Anthropic's proxy and storage |
| Replay | any process or session in the environment can send requests that receive the header while it exists |
| Cross-session access | yes |
| Unrelated-task access | yes (same environment) |
| Provider-compromise boundary | the bypass is exposed to whoever controls the agent proxy or credential store; B3 still guards the API |

## 14. B3 compatibility

X2 → injected header → request reaches the function → B3 reads the `aios-operator` bearer → existing scopes. B3 unchanged; no scope expansion; `aios.agent.register` still 403; Founder authority unchanged. **Compatible** (DV: FDP-010 controls).

## 15. X2 compatibility

X2 would recognise the injected header exactly as the FDP-009-03 bypass: same Vercel Protection Bypass for Automation, same header contract. No new trust source, identity provider or X2 setting. **Existing O-A at X2** — but see `§7` for custody and scope.

## 16. Account-holder dependency

| Action | Holder |
|---|---|
| Plan (Pro/Max needed) | account holder; **UNK** whether held — no change, no payment requested |
| Enable / see the section | account holder (organization admin role) |
| Create the credential | account holder |
| Delete the credential | account holder |
| Change hosts or header | account holder (delete and re-add) |
| View the credential | nobody (value) · account holder (list) |
| Audit | account holder (list); per-request **UNK** |
| Rotate | account holder (delete and re-add); Vercel bypass also rotated by the account holder |

## 17. Release / LIVE separation

The mechanism carries an X2 header only. It grants no Production Release, Founder Release Authorization, LIVE, public traffic, deployment or governance authority. The application has no such route (tests). **Separated.**

## 18. Decision matrix

| Property | Evidence | Classification |
|---|---|---|
| Provider feature exists | cloud-environments docs | VERIFIED FROM PROVIDER DOCUMENTATION |
| Current plan supports it | no readable plan | **UNKNOWN** |
| Credential never reaches Claude | *"never reaches Claude"* | VERIFIED FROM PROVIDER DOCUMENTATION |
| Credential never reaches shell | *"the commands it runs"* | VERIFIED FROM PROVIDER DOCUMENTATION |
| Credential never enters environment | *"session's environment variables"* | VERIFIED FROM PROVIDER DOCUMENTATION |
| Host restriction | exact hosts / `*.` | VERIFIED FROM PROVIDER DOCUMENTATION |
| Header restriction | custom header row | VERIFIED FROM PROVIDER DOCUMENTATION |
| Session isolation | environment-wide | **FAIL** (VPD) |
| Cross-session isolation | *"whoever started it"* | **FAIL** (VPD) |
| Routine isolation | Routines use environments | **FAIL** (VPD) |
| Lifetime control | until deleted; immediacy unknown | **UNKNOWN** |
| Revocation | dashboard, no plaintext | VERIFIED FROM PROVIDER DOCUMENTATION |
| Deletion verification | bypass revocation → 302 (DV method); credential removal visible to account holder only | PARTIAL — credential side **UNKNOWN** |
| Telemetry safety | VM side safe; provider internal undocumented | **UNKNOWN** |
| Logging safety | proxy and Vercel header logging undocumented | **UNKNOWN** |
| B3 compatibility | unchanged | COMPATIBLE (DV) |
| X2 compatibility | same header contract | COMPATIBLE — existing O-A at X2 (DV + VPD) |
| FDP-011 T5 compatibility | custody path undesignated; delivery not session-bounded | **NOT ESTABLISHED** (FAIL on controlled delivery/use; UNKNOWN on logs, retention, custody authority) |
| O-A compatibility | X2 same; custody/scope/`§4.2` open | **AMBIGUOUS** → hard stop |
| Release/LIVE separation | no such authority | SEPARATED |

Not selected.

## 19. Final classification

**D. FOUNDER DECISION REQUIRED.**

Even with complete evidence and the plan in place, the mechanism could not be used without Founder authority:
- it must be designated as T5's *"authorized secure execution/secret-handling path"*;
- environment-wide attachment must be accepted or rejected against D-1's per-session bypass;
- the open reading of `FDP-010` `§4.2` must be settled.

The new trust boundary (`§7`) is an architecture matter; with `FD-2` open, that authority is the Founder's.

**Concurrent, unresolved:**
- plan entitlement **UNKNOWN** (provider / account-holder dependency);
- proxy and Vercel logging, provider telemetry, deletion immediacy and caching **UNKNOWN** (insufficient evidence; hard stops for implementation).

### 19.1 Founder decision surface (prepared, not decided; options unranked)

| Question | Options (as the evidence allows) |
|---|---|
| Q-1 Is M-AC a delivery implementation of O-A, or a different mechanism? | delivery of O-A · different mechanism · defer |
| Q-2 Is M-AC T5's *"authorized secure execution/secret-handling path"*? | yes · no · defer |
| Q-3 Does storing the Vercel bypass in Anthropic's credential store satisfy `FDP-010` `§4.2`? | yes · no · defer |
| Q-4 Is environment-wide attachment, bounded by account-holder create/revoke/delete around a session, acceptable under D-1? | yes, with stated controls (e.g. a dedicated environment, no Routines) · no · defer |
| Prerequisites for any implementation | plan entitlement confirmed by the account holder; provider statements on proxy logging, telemetry, deletion immediacy and caching |

No decision is made or implied here.

## 20. Remaining unknowns

1. Plan entitlement, and customer-managed encryption keys.
2. Request methods covered.
3. Agent-proxy header logging, provider-internal telemetry and tracing.
4. Vercel header logging.
5. Deletion immediacy, proxy caching, and whether running sessions keep the credential after deletion.
6. Per-request audit of injection.

## 21. Exact next authorized action

None that changes state:
- O-A authorized, **NOT IMPLEMENTED**;
- ESC-03 **NOT RESOLVED**;
- FDP-010 **NOT COMPLETE**;
- FS-10 **NOT READY**;
- **RELEASE NOT AUTHORIZED · LIVE NOT ACTIVE**.

The decision surface (`§19.1`) is prepared for the Founder; nothing is selected, configured or created.
