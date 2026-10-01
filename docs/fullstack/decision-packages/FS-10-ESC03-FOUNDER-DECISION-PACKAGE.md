# FS-10 — ESC-03 Founder Decision Package (Production Operational Edge Access)

| Field | Value |
|---|---|
| **Prepared under** | `AD-FS10-ESC03` `§22`, `§23`, `§30` (Register `§113`); record `FS-10-ESC03-ARCHITECTURE-DECISION.md`; evidence `evidence/FS-10-ESC03-ARCHITECTURE-EVIDENCE.json` |
| **Status** | **PREPARED — AWAITING FOUNDER.** Nothing is selected, recommended, ranked or implemented. This package is not a Founder Decision Record |
| **Why the Founder** | edge access is Founder-held configuration (FS-DP-03 `R2.5`); X2 admits only *"a Vercel login or a Founder-authorized, revocable mechanism"* (`R2.10`); deployment-protection changes go through the architecture authority path (`FDP-009-02` `§5.5`), which the Founder holds as Architect (`FD-2` open); temporary access is verification-only by Founder decision (`FDP-009-03`); provider identities and credentials are account-holder controls (`FDP-010` `§4.2`). Existing delegation (`FDP-009` `§8`, `FDP-010` `§13`) does not reach any of these |
| **Release / LIVE** | **unaffected by every option: PRODUCTION RELEASE = FOUNDER RESERVED · LIVE = FOUNDER RESERVED** |

## 1. Exact decision question

> Which edge-access mechanism, if any, may the delegated CEO use to reach the protected Production AIOS API for routine operation — and, if one is chosen, on what scope, duration, revocation and evidence terms?

A second, related question surfaced by the evidence:

> Is a **human** Production principal to exist for the Founder? Today nobody can use the Production API: the Founder passes X2 but holds no principal, and the CEO holds `aios-operator` but cannot pass X2.

## 2. Evidence (summary; full record in the ADR)

- B3 and `aios-operator` work once a request reaches the function [DV]; X2 stops the CEO's requests (302/401) [DV].
- The limitation is the connector (no header parameter; stops at SSO) and the configuration (no authorized mechanism). It is not AIOS architecture [DV].
- The CEO's environment can send any header [DV], but holds no OIDC token from a documented issuer [DV].
- The team has one member and the plan is unknown [CO/UNK]. No in-boundary runtime exists [DV].
- Through the control plane the CEO can deploy, roll back, configure, read logs and metrics, and read the store. The CEO **cannot** run active health checks, post-rollback or post-deploy verification (runbook `§1`, `§9`, `§12.1`), or workflows [DV].

## 3. Current architecture

```text
caller ─▶ X2 (Vercel Authentication; Founder-held) ─▶ api/index.py ─▶ B3 (bearer → principal, scopes) ─▶ AIOS ─▶ store
```

## 4. Options and their effects (not ranked)

| Option | Proposed architectural effect | Security effect | Authority effect | Implementation boundary if chosen | Rollback / recovery effect |
|---|---|---|---|---|---|
| **E-A** per-session bypass | none permanent; a time-boxed X2 exception per operating session | per-session secret; it transits the executor's tool calls; revoked and verified each time | extends `FDP-009-03` from verification to operation | create → use → revoke → verify revocation → evidence, per session; scopes unchanged | sessions also allow post-rollback verification |
| **E-B** standing bypass | a persistent X2 exception | long-lived secret admits any holder to the edge (B3 behind it); rotation and leak response become standing duties | a permanent mechanism at the Founder-held edge | dedicated secret, rotation schedule, revocation procedure | always available for verification |
| **E-C** Trusted Sources OIDC | X2 trusts a named external issuer and subject | no shared secret; short-lived tokens; correctness rests on trust configuration | a new trust relationship at the edge | **evidence incomplete**: plan, project support, X2 acceptance unknown; no issuer available to the CEO's environment — an external runtime (e.g. CI) would be needed | available while the issuer works |
| **E-D** Vercel identity for the CEO | a provider user admitted by X2 | provider login credentials in the CEO's session (`FDP-010` `§4.2`) | provider identity for the CEO; seats per plan (unknown; spending D3-A) | member or user-scoped access; login custody | available while the identity is valid |
| **E-E** runtime inside the boundary | a scheduled or triggered component inside the deployment | a credential in the function environment, or B3 sidestepped; the cron header collides with B3's | a new operational surface; Architect redesign (`FDP-009` `§8`) | **evidence incomplete**: cron passage of X2 unknown | scheduled verification only, unless a trigger is added |
| **E-F** no new mechanism | none | none added | none | the CEO operates through the control plane and read-only store; routine API use only by a human with a Vercel login **and** a principal (none exists today) | post-rollback API verification needs a human |

## 5. Release / LIVE non-effect

No option adds or changes a release, promotion, deployment or LIVE operation. The application has none (tested). The scopes stay `aios.observe`, `aios.workflow.run`, `aios.audit`. Resolving ESC-03 is neither Release nor LIVE authorization.

## 6. Exact decisions required

- [ ] **As Architect:** E-A · E-B · E-C · E-D · E-E · E-F · other (stated) · defer
- [ ] **As Founder**, for the option chosen where needed: the authorization of the mechanism (scope, duration, revocation, evidence), or of the provider identity or configuration change
- [ ] **As Founder (related):** whether a human Production principal exists for the Founder, and under what scopes
