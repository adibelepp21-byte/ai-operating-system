# FS-10 — Provider-Side Credential Injection: Founder Decision Package

| Field | Value |
|---|---|
| **Prepared under** | *"AIOS FS-10 — Provider Credential Injection Founder Decision Preparation Gate"* (verbatim: `docs/governance/acts/MI-FS10-PROVIDER-CREDENTIAL-INJECTION-FOUNDER-DECISION-PREPARATION-GATE.md`; Register `§122`) |
| **Evidence** | `../FS-10-PROVIDER-CREDENTIAL-INJECTION-EVIDENCE.md` (Register `§121`), primary source; `../FS-10-FDP012-M1-CUSTODY-VALIDATION.md` (`§120`) |
| **Status** | **PREPARED — NO DECISION MADE.** A decision package, not a Founder Decision Record. The mechanism (here **M-AC**: Claude Code cloud-environment *API credentials*) is **UNSELECTED** |
| **Implementation** | **NOT AUTHORIZED.** No credential, bypass, provider setting, X2, B3 or Production change |
| **FDP-011** | unchanged (sha256 `5a6e5a8b…`, Register `§117`); conflicts are recorded here, not resolved |
| **Release / LIVE** | **PRODUCTION RELEASE = FOUNDER RESERVED · LIVE = FOUNDER RESERVED** — no question below touches either |

Choices are listed in a fixed order that carries no ranking. Evidence classes: **CAN** canonical · **VPD** verified from provider documentation · **DV** directly verified · **UNK** unknown.

## Current state (re-discovered 2026-10-01)

| Item | State |
|---|---|
| `FDP-009` `33fecb97…`, `FDP-010` `fa1d8b12…`, `FDP-011` `5a6e5a8b…`, `AD-FS10-ESC03` `d10a16af…` | in the Register, unchanged (DV) |
| O-A | **AUTHORIZED — NOT IMPLEMENTED** |
| M-AC | **UNSELECTED** |
| M1 (environment variable) | **FAILED** (`§120`) |
| ESC-03 / FDP-010 / FS-10 | NOT RESOLVED / NOT COMPLETE / NOT READY |
| X2 / B3 / Production | SSO on, no bypass, no trusted IPs; B3 unchanged; serving `dpl_s8c6m…`, target `dpl_76CYC…`; `updatedAt` `1790837188645` (DV) |
| Release / LIVE | NOT AUTHORIZED / NOT ACTIVE |

## Known facts about M-AC (from the evidence record, verbatim where quoted)

1. Stored on a cloud **environment**; *"Anthropic's agent proxy adds the key to requests for the hosts you list, after each request leaves the session's VM."* (VPD)
2. *"The key never reaches Claude, the commands it runs, or the session's environment variables."* (VPD)
3. *"The credential applies in every session that runs in the environment, whoever started it, until you delete it."* (VPD)
4. Custom header name; prefix can be cleared; exact hosts or `*.` subdomains. (VPD)
5. *"You can't view the value again after saving."* No edit: *"delete it and add it again."* (VPD)
6. *"API credentials are available on Pro and Max plans."* (VPD)
7. *"Claude Code's telemetry export … doesn't go through the agent proxy."* (VPD)
8. On archiving: *"API credentials on the environment stay attached in its running sessions."* (VPD)
9. X2 accepts `x-vercel-protection-bypass` — the same header as the FDP-009-03 bypass. (VPD + DV)
10. B3 still requires the `aios-operator` bearer. (DV)

**Unknown (kept UNKNOWN; not for the Founder to decide — they need provider evidence):**
- plan entitlement, and whether this account can use API credentials;
- Vercel header logging;
- agent-proxy header logging and provider telemetry;
- whether deletion is immediate;
- proxy caching;
- whether already-running sessions keep the credential after deletion;
- per-request audit.

---

## Q-1 — O-A compatibility

**Question.** Is provider-side credential injection (A) a delivery/custody implementation path for the already-authorized O-A, (B) a materially different X2 access mechanism, or (C) unresolved?

**Canonical evidence:**

| Supports | Provision |
|---|---|
| **A** | `FDP-011` D-1 authorizes *"E-A per-session bypass"*; E-A is defined at X2 as *"an automation-bypass secret created for one operating session, revoked at its end"* (package `§11`). M-AC carries that same secret in the same header. FS-DP-03 `R2.10` admits *"a Founder-authorized, revocable mechanism"*, and X2 sees no difference. T5 itself anticipates *"an authorized secure execution/secret-handling path"*, i.e. a custody path distinct from the mechanism |
| **B** | E-A was evaluated with the credential in the CEO's session (*"per-session secret; transits tool calls"*, package `§12`); M-AC places it with a third party that attaches it for **every** session. D-1: *"The bypass exists only for an explicitly authorized operational session."* AD-FS10-ESC03 S7 treats a new holder of an edge credential as a **new trust boundary** |
| **C** | No canonical text defines whether "mechanism" in D-1 covers custody and delivery, or only the X2 credential type |

**Provider evidence:** facts 1–4, 9 (same header at X2; environment-wide attachment).
**Unknowns:** none decisive for the classification itself; the provider unknowns bear on Q-2 and Q-4.
**Implications:** A treats M-AC as within FDP-011; B treats it as outside FDP-011's authorization.

| Choice | Consequence |
|---|---|
| **Q-1/A** delivery path of O-A | M-AC is assessed under FDP-011 (T1–T9) without a new mechanism decision. Q-2 to Q-4 still apply |
| **Q-1/B** different mechanism | M-AC needs its own authorization (Founder; Architect for the trust boundary); FDP-011's O-A does not cover it |
| **Q-1/C** leave unresolved / defer | M-AC stays unusable; the current state is unchanged |

## Q-2 — T5 custody authorization

**Question.** Does storing the O-A bypass credential in the provider's credential store satisfy FDP-011 T5?

| T5 element | Evidence | Result |
|---|---|---|
| creation | account holder; Vercel dashboard (bypass) and environment dialog (credential) | PASS |
| custody | stored with Anthropic, outside the VM (VPD). T5 requires *"an authorized secure execution/secret-handling path"*; no instrument designates M-AC | **UNKNOWN** (authority) |
| delivery | attached to every request to the listed hosts from any process or session in the environment (VPD). T5: *"used only for the authorized operational session"* | **FAIL** |
| non-disclosure | VM, chat and tool output: none (VPD); provider internals: undocumented | **UNKNOWN** |
| environment visibility | *"never reaches … the session's environment variables"* | PASS |
| tool-output visibility | *"never reaches Claude, the commands it runs"* | PASS |
| repository exclusion | never in the VM or any file | PASS |
| evidence exclusion | T8 fields need no value | PASS |
| logging exclusion | AIOS: none (DV). Vercel and agent proxy: undocumented | **UNKNOWN** |
| telemetry exclusion | Claude Code export bypasses the proxy (VPD); provider-internal: undocumented | **UNKNOWN** |
| rotation | delete and re-add; value never shown | PASS |
| deletion | possible without plaintext (VPD); immediacy, caching and running sessions undocumented | **UNKNOWN** |
| revocation | Vercel bypass revoked in the dashboard; verifiable by a 302 without the value | PASS |
| auditability | credential list and hosts (VPD); per-request undocumented | **UNKNOWN** |
| not retained after the session | *"until you delete it"*; post-deletion behaviour undocumented | **UNKNOWN** |

**Implications:** one FAIL (delivery) and seven UNKNOWN. T5 is not satisfied on the evidence as it stands.

| Choice | Consequence |
|---|---|
| **Q-2/yes** designate M-AC as T5's authorized path | the custody-authority element is settled. The delivery FAIL remains unless Q-4 accepts environment-wide delivery. The UNKNOWNs remain until provider evidence exists (implementation stays hard-stopped on them) |
| **Q-2/no** | M-AC cannot carry the O-A credential under FDP-011 |
| **Q-2/defer** | unchanged |

## Q-3 — FDP-010 §4.2 compatibility

**Question.** Does storing the Vercel O-A bypass in the provider's (Anthropic's) credential store satisfy *"Provider credentials remain stored in the provider's appropriate secret mechanism"*?

**Canonical text (`FDP-010` `§4.2`, *Production Access Ownership*):** *"The Production provider account remains controlled by the account holder. Provider-level credentials, account ownership, billing ownership and provider security controls remain external/account-holder controls. Claude Code MUST NOT require the Founder to paste provider secrets into ChatGPT or another conversational channel. Provider credentials remain stored in the provider's appropriate secret mechanism."*

| | Evidence |
|---|---|
| **For compatibility** | M-AC is a provider-operated secret mechanism built for keys used by sessions: the value is not viewable after saving and never enters the VM (VPD). The account holder creates, holds and deletes it, consistent with *"account-holder controls"*. Entry is through a settings dialog, not a conversational channel |
| **Against compatibility** | In `§4.2`, *"the provider"* is introduced as *"the Production provider account"* (Vercel). M-AC is a different provider's (Anthropic's) store. The bypass is a Vercel protection secret, arguably a *"provider security control"* credential |
| **Unresolved** | (a) whether the automation bypass is a *"provider credential"* within `§4.2`; (b) whether *"the provider's appropriate secret mechanism"* means only the Production provider's own store, or any appropriate store under the account holder's control |

| Choice | Consequence |
|---|---|
| **Q-3/compatible** | `§4.2` is read to admit M-AC; `FDP-010` text unchanged |
| **Q-3/not compatible** | M-AC is excluded for the Vercel bypass unless `§4.2` is changed by a later Founder decision |
| **Q-3/defer** | unchanged |

## Q-4 — Environment-wide lifetime

**Facts.** M-AC:
- applies to the **environment**;
- applies to **every session** using that environment, *"whoever started it"*;
- applies to **every process** in those sessions that calls a listed host;
- **remains until deleted**.

FDP-011 requires:
- D-1: *"per-session automation-bypass mechanism"*; *"exists only for an explicitly authorized operational session and must be revoked at the end of that session"*;
- T4: *"must not become standing access"*;
- T7: explicit revocation and independent verification.

**Procedural per-session use is not technical session isolation.** If the account holder creates, revokes and deletes the credential around each session, its *existence* becomes procedurally session-bounded. It does not stop other sessions or unrelated processes in the environment from receiving it while it exists.

| | Interpretation A — procedural per-session use is acceptable | Interpretation B — environment-wide availability is incompatible with O-A's per-session nature | Interpretation C — additional technical controls are required first |
|---|---|---|---|
| **Canonical basis** | D-1 and T4 concern the bypass's existence and revocation, both controllable by the account holder per session; T7 verification possible | D-1: the bypass *"exists only for an explicitly authorized operational session"*; T5: *"used only for the authorized operational session"*; T4: *"must not become standing access"* | MI rule *"Do not rationalize environment-wide inheritance as session isolation"* (`§120` MI `§12`); AD-FS10-ESC03 S7 (trust boundary) |
| **Security implication** | while it exists, any session and process in the environment can pass X2 (B3 still required); exposure window = the account holder's create-to-delete interval | M-AC excluded; no new exposure | exposure is bounded only after the added controls exist and are evidenced |
| **Operational implication** | account holder acts at the start and end of each session (create, add, revoke, delete) | O-A still has no delivery path; ESC-03 stays open | controls must be identified and evidenced; candidates such as a dedicated environment used only for O-A sessions, no Routines, no concurrent sessions are **listed, not selected**; none is a technical enforcement today |
| **Unresolved evidence** | deletion immediacy; caching; running sessions after deletion | — | whether any provider control limits a credential to one session (none documented) |

| Choice | Consequence |
|---|---|
| **Q-4/A** | environment-wide availability accepted under stated procedure; the delivery FAIL in Q-2 is accepted as procedurally bounded; provider UNKNOWNs still block implementation |
| **Q-4/B** | M-AC incompatible with O-A as authorized |
| **Q-4/C** | M-AC conditional on named controls, whose evidence must exist before implementation |
| **Q-4/defer** | unchanged |

---

## Security impact by Q-4 interpretation (factual)

| Concern | Under A | Under B | Under C |
|---|---|---|---|
| Cross-session access | present while the credential exists | none (not used) | as limited by the added controls |
| Unrelated process access | present (same environment) | none | as limited |
| Routine execution | can receive it if a Routine runs in the environment (none exist now, DV) | none | e.g. excluded if no Routine may use the environment |
| Background execution | inherits X2 passage within the session | none | as limited |
| Credential lifetime | account holder's create-to-delete interval | — | same, plus controls |
| Revocation | Vercel dashboard; verifiable by 302 | — | same |
| Deletion | environment dialog; immediacy UNKNOWN | — | same |
| Replay | any request to a listed host while it exists | — | as limited |
| Provider trust boundary | Anthropic agent proxy and store hold the bypass | none added | same as A |
| Telemetry | VM side none; provider internal UNKNOWN | — | same |
| Logging | AIOS none; Vercel and proxy UNKNOWN | — | same |
| Auditability | credential list; per-request UNKNOWN | — | same |

## Governance impact

| Element | Authority needed | Basis |
|---|---|---|
| Q-1, Q-2, Q-4 (meaning and acceptance under FDP-011) | **Founder Decision** | FDP-011 is a Founder decision; T5's *"authorized"* path is undesignated |
| Q-3 (`FDP-010` `§4.2`) | **Founder Decision** | FDP-010 is a Founder decision |
| New trust boundary at the edge (agent proxy holds an X2 credential) | **Architect Decision** | Engineering Constitution `§3.1`–`§3.2` (architectural tier); `FDP-009-02` `§5.5` (architecture path for deployment protection); AD-FS10-ESC03 S7 |
| Whether one Founder act also carries the Architect decision | **depends on `FD-2`** | `FD-2` (*"Founder ≡ Architect"*) is *"IMPLIED — open"* (Delegation Register), *"open, not relied on"* (P13 exit package). **Founder authority does not automatically resolve the architecture question** while `FD-2` is unratified |

**Result:** both a Founder Decision and an Architect Decision. Whether they can be one instrument depends on `FD-2`.

**Correction (Register `§122`):** earlier FS-10 records described the Architect authority as *"held by the Founder (FD-2 open)"*: ADR `§9`, the complete ESC-03 package `§10`, and evidence record `§19`. That relied on an unratified premise. Those records are preserved; this correction stands beside them.

## Conflicts with FDP-011 (recorded, not resolved)

| Provision | Conflict |
|---|---|
| D-1 *"exists only for an explicitly authorized operational session"* | M-AC attaches the credential environment-wide while it exists |
| T5 *"used only for the authorized operational session"* | same |
| T5 *"authorized secure execution/secret-handling path"* | M-AC not designated |

FDP-011 is unchanged.

## Plan entitlement (not a governance choice)

**PLAN ENTITLEMENT = UNKNOWN. ACCOUNT-HOLDER / PROVIDER VERIFICATION REQUIRED.**

Facts the account holder can supply (no credential, no value, no payment):
1. the subscription plan of the claude.ai account that owns environment `env_01X4j1qVyxMRoTsGvotFpwue` (*"MoriartyContent plan"*): Pro, Max, Team or Enterprise;
2. whether the **API credentials** section appears in that environment's *Update cloud environment* dialog;
3. whether the organization uses customer-managed encryption keys;
4. whether the account holds the organization admin role.

**Provider evidence needed** (statements, not decisions): agent-proxy and Vercel header logging; provider-internal telemetry; deletion immediacy; caching; running-session behaviour after deletion; per-request audit.

## Non-decisions

This package does not:
- select or reject M-AC;
- authorize environment-wide custody;
- amend FDP-011 or FDP-010;
- create FDP-012;
- authorize implementation;
- resolve ESC-03, complete FDP-010 or move FS-10 to READY;
- ratify `FD-2`;
- touch Release or LIVE.

## Founder decision form (unfilled)

- [ ] **Q-1** A · B · C/defer
- [ ] **Q-2** yes · no · defer
- [ ] **Q-3** compatible · not compatible · defer
- [ ] **Q-4** A · B · C (name the controls) · defer
- [ ] Architect decision on the trust boundary, or a statement on `FD-2`
