# FS-DP-02 — Identity and Authentication

| Field | Value |
|---|---|
| **Identifier** | `FS-DP-02` (provisional) |
| **Area** | Identity (as a general/auth concept), Authentication — Freeze `§10`, Architect-reserved (*"no ratified entity"*) |
| **Status** | **PROPOSED — ROUTED TO THE ARCHITECT** (Register `§71`, 2026-09-27); **AWAITING ARCHITECT DECISION**. Not ratified |
| **Decision owner** | Holder of Architect authority (`FD-FS-001` D2-A; `FD-2` open) |
| **Founder constraints** | No spending (D3-A). Supabase is named for the **database** only; using its authentication service is a further choice this package asks for |
| **Prepared by** | Claude Code, 2026-09-26; **Revision 2** 2026-09-27 (below), under `ACT-CC-POST-P13-AIOS-FULL-STACK-002` `§11` |

## Context

- The Act's FS-06 flow: *User → Identity → Authentication → Authorization →
  Capability → AIOS*, and *User → Role → Permission → Policy → Action →
  Audit*. *"Frontend shall never become the final authority source."*
- AIOS already has authority concepts, all internal: Governance review with
  `HumanAuthority`; Tool caller classes; P13 envelopes. None is a person
  signing in.
- The backend ships an **authenticator port** that refuses everyone
  (`NoAuthenticator`), **scope** authorization per route, and an audit ledger
  (`fullstack/backend/security.py`). The scopes are `aios.observe`,
  `aios.workflow.run`, `aios.audit`.

## Part A — Architectural decision (ADR-eligible)

**Question.** Does human identity enter the AIOS Domain Model?

| Option | Statement | Assessment |
|---|---|---|
| **A1** | **No.** A signed-in person is a *principal of the application layer*. The application maps a principal to scopes; AIOS authority stays where it is (Governance, Tool governance, envelopes). A principal is not an Agent Instance and holds no AIOS authority by existing | No Domain Model change; nothing delegable is exceeded |
| A2 | Yes: add an Identity entity and relationships to the Domain Model | A Domain Model semantic change: not delegable (Constitution `§3.2`); needs its own ADR and Architect approval |

**Recommendation: A1.** Revisit only if AIOS itself must reason about who a
human is.

## Part B — Implementation decision (Freeze `§10`; not ADR-eligible)

| Option | Mechanism | Cost | Notes |
|---|---|---|---|
| **B1** | **Supabase Auth**: sign-in by email link or GitHub OAuth; the backend verifies the JWT against the project's published keys; scopes read from `app_metadata.aios_scopes`, which only the operator can set | free-plan limits to confirm | Same provider already named; scopes never come from the browser |
| B2 | WorkOS AuthKit (a connector exists in this environment) | to confirm | A provider the Founder has **not** named; needs a Founder naming first |
| B3 | Operator bearer tokens: random secrets stored hashed in the host's secret store, each mapped to scopes | none | Single-operator only; no self-service identity; simplest to audit |

**Recommendation: B1** for a multi-user console, **or B3** if the first
release is operator-only. Either is a drop-in `Authenticator`; nothing else
in the backend changes.

Whichever is chosen:

- **least privilege**: default grant is `aios.observe` only; `aios.workflow.run`
  and `aios.audit` are granted explicitly;
- tokens and keys live in the host's secret store, never in the repository,
  logs, frontend bundle or evidence (NC-10);
- the audit ledger keeps recording every decision.

## Until decided

Every route except `/api/v1/health` answers **401**. Tests inject a test-only
authenticator; the production composition has none.

## Exact decision required

- [ ] Part A: A1 · A2
- [ ] Part B: B1 · B2 (with a Founder naming) · B3 · other
- [ ] Initial grants for the Founder's own principal
- [ ] Decided as: Architect · Founder as Architect

---

## Revision 2 (2026-09-27): after the deployment was ratified and built

FS-DP-01 and FS-DP-04 are now ratified and implemented (Register `§68`,
`§69`). That fixes facts the first revision could only assume. This revision
is **proposed; Claude does not ratify it** (Act NC-01, NC-06).

### R2.1 Evidence

| Fact | Class | Source |
|---|---|---|
| The backend has an authenticator **port**; the shipped one refuses everyone (`NoAuthenticator`). Every route but health answers 401, locally and in the deployed function | Observed | `fullstack/backend/security.py`; `fullstack/deploy/vercel.py`; `test_the_shipped_function_authenticates_nobody` |
| Authorization is by three scopes, one per route, decided in the backend only | Observed | `security.authorize`; `fullstack/backend/contract.py` |
| Every allowed or refused decision is audited with the subject, never the credential | Observed | `AuditLedger` |
| The console sends `Authorization: Bearer <credential>`, keeping the credential in `sessionStorage` | Observed | `fullstack/frontend/api.js` |
| The console's CSP allows network calls to its own origin only (`connect-src 'self'`) | Observed | `fullstack/backend/api.py` `PAGE_CSP`; `vercel.json` |
| Deployed, each request has its own Runtime and nothing survives in memory (FS-DP-04 A1). A server-side session would need durable storage | Observed | `fullstack/deploy/vercel.py` |
| The Supabase project's Auth signs tokens with **ES256** (EC P-256), from its public key set | Observed, 2026-09-27 | `https://scfymftfzkpilqbgmfwv.supabase.co/auth/v1/.well-known/jwks.json` |
| Python's standard library has no ECDSA verification. The backend so far has **no third-party dependency** | Observed | stdlib; repository |
| Vercel Authentication (SSO) protects every preview URL for team members. It does not hand the member's identity to the function, and it does not cover custom domains | Observed (protection); **Inferred** (no identity passed) | `get_project`; `FS-08-DEPLOYMENT-EVIDENCE.md` `§4` |
| A WorkOS connector exists in this environment | Observed | session tools; not a Founder-named provider |

### R2.2 Requirements

From the Act's FS-06 flows and the backend as built:

1. The backend alone decides; the frontend never holds authority.
2. Least privilege: `aios.observe` by default, the other scopes explicitly.
3. Every decision audited with a stable subject; no credential recorded.
4. Stateless per request (A1): the credential is verified on each request,
   without in-memory sessions.
5. No secret in the repository, the frontend bundle, logs, Trace, audit or
   responses.
6. Fail closed: a verifier error authenticates nobody.
7. No spending (D3-A).

### R2.3 Part A: unchanged

A1 recommended: a signed-in person is a principal of the application layer,
not an AIOS entity. Nothing in the deployment changes this.

### R2.4 Part B: options, revised with the evidence

| # | Mechanism | Backend | Frontend | New dependency or secret | Fit |
|---|---|---|---|---|---|
| **B3** | **Operator bearer tokens.** The Founder generates each token offline; the host stores only its SHA-256 hash with a subject and scopes (`AIOS_OPERATOR_TOKENS`); the backend hashes the presented token and compares in constant time | a drop-in `Authenticator`, stdlib | **none**: the console already sends a bearer credential | a host environment variable set by the Founder; Claude never sees a token | operator-only; revocation by editing the variable and redeploying; no self-service |
| B1a | Supabase Auth, token verified locally (ES256 against the public key set) | an `Authenticator` plus a JWT/ECDSA library | a sign-in flow; CSP `connect-src` widened to the Supabase origin, or sign-in proxied through the backend | the **first third-party dependency** in the backend | multi-user; scopes in `app_metadata`, set by the operator |
| B1b | Supabase Auth, token verified by calling Supabase's user endpoint on each request | stdlib; one extra HTTPS call per request | as B1a | none new | multi-user; adds latency and a runtime dependency on Supabase Auth |
| B2 | WorkOS AuthKit | an SDK or JWT library | a hosted sign-in | a provider **not named by the Founder** | needs a Founder naming first |
| B4 | Vercel Authentication as the only gate | none | none | none | **Rejected**: the function learns no identity, so there is no subject for audit and no scopes; it does not cover custom domains |

**Recommendation: B3 first**, for the operator-only surface FS-08 and FS-09
need, with B1a or B1b as the step to multiple users when that becomes a
requirement. B3 changes one class and nothing else; its tokens never pass
through Claude. The recommendation is not a decision.

### R2.5 Implications

| | B3 | B1a / B1b |
|---|---|---|
| Security | tokens are bearer secrets: the console holds one in `sessionStorage`, as today's tests do. Only hashes are on the host. HTTPS only | standard JWTs, expiring; a sign-in surface to secure; B1b trusts Supabase Auth on every request |
| State | none (stateless) | none in the backend; sessions live in Supabase Auth |
| Deployment | one environment variable per environment; Preview and Production may hold different principals | Auth settings in the Supabase project; redirect URLs per deployment URL |
| Compatibility | the `Authenticator` port, scopes, audit and console unchanged | port, scopes and audit unchanged; console gains sign-in; CSP changes |
| Concurrency | opens run creation: **FS-DP-05 must be decided before or with it** | same |

### R2.6 Unresolved decisions (for the Architect, or the Founder where marked)

- Initial principals and grants, e.g. the Founder's own principal with all three scopes.
- Token lifetime and rotation (B3), or token expiry and sign-in methods (B1).
- Whether Preview and Production share principals.
- Naming WorkOS as a provider (**Founder**, only if B2 is wanted).

### R2.7 Negative controls for implementation, whichever is chosen

- No credential accepted by any code path before ratification (today's
  `NoAuthenticator` stays the shipped default until then).
- No token, key or hash in the repository, tests' fixtures excepted as
  obviously fake values.
- No credential in audit, Trace, logs or responses.
- A verifier error authenticates nobody.
- The frontend never decides a scope.
- No Supabase or WorkOS feature becomes an AIOS entity (Part A1).

### R2.8 After ratification

Implementation is one `Authenticator` and its tests, then the composition in
`fullstack/deploy/vercel.py`. For B3 the Founder then sets
`AIOS_OPERATOR_TOKENS` for Preview (a new external dependency, like EXT-05)
and gives the console a token. The live success path of FS-08 becomes
testable.

### R2.9 Exact decision required

- [ ] Part A: A1 · A2
- [ ] Part B: B3 · B1a · B1b · B2 (with a Founder naming) · other
- [ ] Initial principals and grants
- [ ] Token lifetime / rotation
- [ ] Preview and Production principals: shared · separate
- [ ] Decided as: Architect · Founder as Architect

### R2.10 Routing record (2026-09-27)

Routed to the Architect by the Founder's authorization of
`ACT-CC-POST-P13-AIOS-FULL-STACK-002` (Register `§71`). That authorization
**does not ratify** this package. The elements its `§9` requires, and where
they are:

| Element | Where |
|---|---|
| Current evidence | `§R2.1` |
| Architectural question | Part A: *does human identity enter the AIOS Domain Model?* Part B: *by what mechanism does the backend learn who is calling?* |
| Current implementation | `§R2.1`: the port with `NoAuthenticator`; scopes; audit; the console's bearer header |
| Options | `§R2.4` |
| Implications | `§R2.5` |
| Proposed recommendation | `§R2.4`: A1 + B3 first |
| Negative controls | `§R2.7` |
| Implementation boundary | `§R2.11` |
| Verification requirements | `§R2.12` |
| Architect decision block | `§R2.13` |

**Order** (authorization `§10`): FS-DP-05 is implemented before, or together
with, whatever is ratified here, because an authenticator admits run
requests.

### R2.11 Implementation boundary (if B3 is ratified)

In: one `Authenticator` in `fullstack/backend/security.py` reading token
hashes from the host environment; its composition in
`fullstack/deploy/vercel.py` and `fullstack/backend/__main__.py`; tests.
Out: the scopes, `authorize`, the audit format, the console, the CSP,
`native_core/`, `consumers/`, `tools/`, any certified root. Tokens are
generated and set by the Founder; Claude never generates, sees or stores one.

### R2.12 Verification requirements

1. Unit: a valid token maps to its subject and scopes; unknown, malformed,
   empty and near-miss tokens authenticate nobody; comparison is constant
   time; a malformed configuration authenticates nobody.
2. No token or hash in responses, audit, Trace or logs (scan, as the
   security suite does today).
3. Integration: 401 without a token, 403 without the scope, 201 with it;
   audit subject recorded.
4. Live, once EXT-03, EXT-05 and the token configuration exist: the success
   path, the failure path, a refusal, Trace and audit on the preview.
5. Full regression.

### R2.13 Architect decision

| Field | Value |
|---|---|
| Architect | *(to complete)* |
| Date | *(to complete)* |
| Part A | [ ] A1 · [ ] A2 |
| Decision (Part B) | [ ] RATIFY B3 — operator bearer tokens · [ ] SELECT ANOTHER DOCUMENTED OPTION: ______ · [ ] REQUEST REVISION · [ ] DEFER · [ ] REJECT |
| Initial principals and grants | *(to complete)* |
| Token lifetime / rotation | *(to complete)* |
| Preview and Production principals | [ ] shared · [ ] separate |
| Conditions | *(Architect to complete)* |
| Rationale | *(Architect to complete)* |
| Status | **AWAITING ARCHITECT DECISION** |

A decision takes effect when recorded in the Register, not in this file.
