# FS-DP-03 Revision 3 — ESC-03: Operational Edge Access for the Delegated CEO (Architect Decision Package)

| Field | Value |
|---|---|
| **Identifier** | `FS-DP-03-R3` (ESC-03) |
| **Area** | Networking — edge access (Architect-reserved, `FD-FS-001` D2-A; Freeze `§10`) |
| **Status** | **PREPARED — AWAITING ARCHITECT DECISION.** No option is selected or implemented |
| **Decision owner** | the Architect (the Founder acting as Architect, `FD-2` open). Options marked ◆ also need a **Founder** authorization (FS-DP-03 `R2.5`, `R2.10`; `FDP-009-03`; `FDP-010` `§4.2`) |
| **Prepared by** | Claude Code under `ACT-CC-POST-P13-AIOS-FS10-ESC03` `§18` (Register `§111`); evidence: `FS-10-ESC-03-AUTHORITY-RESOLUTION.md` |
| **Not** | a recommendation, a ranking, a release, LIVE, or an implementation (Act `§18`) |

## 1. Problem

The permanent operational principal `aios-operator` (`FDP-010-01`) authenticates at the application, but every request first meets **X2**: Vercel deployment protection on every deployment, Production included. X2 admits *"a Vercel login or a Founder-authorized, revocable mechanism"* (`R2.10`). The delegated CEO has no Vercel login session it can attach an `Authorization` header to, and **no mechanism is authorized for routine operation** (temporary access is for verification only, `FDP-009-03`). So the CEO cannot call the AIOS API for ordinary operation (observe, run workflows, inspect the audit, recovery checks).

## 2. Existing architecture

```text
caller ──HTTPS──▶ Vercel edge: X2 (Vercel Authentication, all_except_custom_domains)
                    │  passes: a Vercel login; a Founder-authorized revocable mechanism
                    ▼
                 api/index.py ── B3: Authorization: Bearer <token> → sha256 → principal + scopes
                    ▼
                 AIOS Runtime (in-process) ── Supabase (server-side key)
```

Two independent layers: X2 decides **who reaches** the function; B3 decides **who the caller is** and **what it may do** (FS-DP-02 rejected the edge as the only gate because the function learns no identity from it).

## 3. Boundary affected

The **edge admission rule of X2**: whether, and how, a non-human operational caller (the delegated CEO) may reach the function. The B3 layer, the scopes, the routes and the store are **not** affected by any option.

## 4. Candidate mechanisms (alphabetical by identifier; not ranked)

| ID | Mechanism | What changes at the edge | Founder authorization also needed |
|---|---|---|---|
| E-A | **Per-session operational bypass**: an automation bypass created for one operating session, revoked and its revocation verified afterwards, as under `FDP-009-03` but for operation | nothing permanent; a time-boxed exception per session | ◆ yes — extends `FDP-009-03` beyond verification |
| E-B | **Standing automation bypass** dedicated to operation, rotated and revocable | a standing exception for any holder of the secret | ◆ yes — `FDP-009-02` created no permanent bypass; ACT-003 `§12` |
| E-C | **Trusted Sources (OIDC)**: admit tokens from a named OIDC issuer the CEO's execution environment can obtain | a standing admission rule for one issuer and subject | — (Architect) |
| E-D | **User-scoped bypass for a CEO provider identity** | a named provider identity admitted | ◆ yes — provider identity and possibly seats are account-holder matters (`FDP-010` `§4.2`; D3-A) |
| E-E | **Operational runtime inside the boundary** (e.g. a scheduled Vercel function invoking AIOS in-process) | none at the edge; a new component inside it | — (Architect), and its trigger and authority need definition |
| E-F | **No new mechanism**: routine API operation only by a human member through a Vercel login; the CEO operates through the provider control plane (deploy, rollback, logs) and read-only store access | none | — |

Options excluded by current authority and listed only for completeness: **X2 → X1** (Production public; conflicts with `FDP-009-02` `§5.5`–`§5.6`); a provider credential (CLI token) in the CEO's environment (`FDP-010` `§4.2`).

## 5. Evidence

`FS-10-ESC-03-AUTHORITY-RESOLUTION.md` `§2` (sources), `§5` (limitations), `§6` (matrix), `§8` (B1–B10, NC-01–NC-10). Provider mechanisms from Vercel documentation (read-only).

## 6. Security implications

| ID | Implication |
|---|---|
| E-A | a secret per session; disclosure window = session length; each creation and revocation needs evidence; as at FS-10 verification, the secret transits the operator's tool calls |
| E-B | a long-lived secret that admits **anyone** holding it to the edge (B3 still required behind it); rotation and leak response become standing duties |
| E-C | no shared secret; short-lived tokens bound to an issuer and subject; correctness depends on the exact trust configuration; **UNKNOWN**: plan entitlement and whether the CEO's environment can obtain such a token |
| E-D | ties edge access to a provider identity for the CEO; provider account governance applies |
| E-E | a new component with its own credentials and trigger surface; must not become an unaudited operator |
| E-F | no new exposure; the CEO cannot run workflows or read the audit through the API |

## 7. Authority implications

All options leave the principal's scopes, Founder authority, Release and LIVE authority unchanged. E-A, E-B and E-D also require a Founder authorization in addition to the Architect decision. E-C and E-E add an architectural element: a trust boundary or component.

## 8. Release / LIVE separation

No option gives access to anything but the existing application, which has no release, promotion, deployment or LIVE operation. The operator's scopes (`aios.observe`, `aios.workflow.run`, `aios.audit`) stay as they are, and B3 stays the identity layer. **Operational access ≠ Release ≠ LIVE** under every option (resolution record `§9`).

## 9. Required architectural change and affected contracts

| ID | Change | Contracts affected |
|---|---|---|
| E-A | none to X2's setting; an operating procedure under a Founder authorization | runbook `§15`; FS-10 current authority |
| E-B | X2 configuration gains a standing exception | FS-DP-03 (X2 meaning), `FDP-009-02` boundary, runbook |
| E-C | X2 configuration gains a trusted issuer | FS-DP-03, provider configuration, CEO environment identity |
| E-D | a provider identity admitted | provider account, FS-DP-03 |
| E-E | a new in-boundary component | FS-DP-03, FS-DP-04 deployment shape, observability |
| E-F | none | runbook (states the limit) |

## 10. Exact decision required

- [ ] Edge access for the delegated CEO: E-A · E-B · E-C · E-D · E-E · E-F · other (stated)
- [ ] Where ◆: the Founder's authorization of that mechanism (scope, duration, revocation, evidence)
- [ ] Decided as: Architect · Founder as Architect
