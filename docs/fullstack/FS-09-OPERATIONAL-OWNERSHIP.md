# FS-09 — Operational Ownership Model

| Field | Value |
|---|---|
| **Authority** | `ACT-CC-POST-P13-AIOS-FULL-STACK-004` `§37`: *"Claude may define and implement the operational ownership model required by FS-09 … No new Founder authority is created by this operational model"*; continued under ACT-005 |
| **Register** | `§93` |
| **Scope** | who does what to operate the AIOS Full Stack: the Vercel project `aios-platform`, the Preview store `scfymftfzkpilqbgmfwv`, the Production store `hmljfyqycxcueulhsjae` |
| **Is not** | a governance change, a delegation of Founder authority, a release, or an alerting decision (alerting is unresolved, Register `§93` DG-02) |

This model assigns **operational duties**. Every decision it touches keeps the
authority it already has (runbook `§14`).

## 1. Roles

| Role | Held by | Duties |
|---|---|---|
| **Operator of record** | the Founder (Moriarty) | holds every account and credential (`§2`); performs the steps only an account holder can (setting host variables, dashboard settings); takes every Founder-reserved decision |
| **Delegated executor** | Claude Code, only while an Act authorizes it | builds, verifies, runs drills and backups, investigates incidents, and records evidence, through the connectors the operator has authorized. Never holds a credential in the repository; never bypasses a control except by a temporary, authorized, revoked mechanism |
| **Architect** | the Founder as Architect (`FD-2` open) | architecture decisions; delegated to Claude Code only when an Act says so, and only within it |

## 2. Credentials

| Credential | Custodian | Where it lives | Rules |
|---|---|---|---|
| Vercel team account | operator | Vercel | protection settings are the operator's (EXT-06 showed why a change must be checked) |
| Supabase organization account | operator | Supabase | project creation, pausing and restoring |
| Preview database key (`scfymftfzkpilqbgmfwv`) | operator | Vercel variable `SUPABASE_SECRET_KEY`, **Preview scope only** | never in chat, the repository, logs or evidence |
| Production database key (`hmljfyqycxcueulhsjae`) | operator | **not yet set**: it will be a Vercel variable in **Production scope only**, set at FS-10 | never shared with Preview; a Preview key never serves Production |
| Operator bearer tokens | operator (issued with `python -m fullstack.backend operator-token`) | plaintext only with the holder; the host holds hashes (`AIOS_OPERATOR_TOKENS`, per environment) | rotation per runbook `§2`; one token per person or purpose |
| Temporary access (automation bypass) | created by the executor under an Act, for one suite | never persisted | revoked immediately after use; `protectionBypass: {}` checked after revocation |

## 3. Deployment

* Preview deployments are built from the working branch on every push. The executor verifies them (runbook `§1`) when an Act asks.
* **Production deployment, promotion, alias and variables are the operator's, on a Founder release decision** (`FD-FS-001` D4-A). Nothing in this model deploys to Production.
* The build must show the pinned runtime (*"Using Python 3.12 from .python-version"*).

## 4. Backup and restore

| Item | Rule |
|---|---|
| Method | operator-run logical export (runbook `§7`), per environment; restore only into a fresh store of the **same** environment (runbook `§8`) |
| Cadence | before every release; before any schema change; and weekly while Production serves traffic (from FS-10 onward) |
| Retention | every export and its manifest kept at least until the next release after it; no export ever contains a credential |
| Boundary | a Preview export is never restored into Production, nor the reverse |
| Who | the executor prepares and verifies; the operator keeps the files |

## 5. Rollback

* Preview: the executor may drill it (alias re-pointing), as at FS-09 (`FS-09-ACT-005-EXECUTION-RECORD.md` `§14`).
* Production: the operator, on a Founder decision; never to gain evidence.
* Floors: runbook `§10`.

## 6. Monitoring

* **Logging (L1)** and **metrics (M1)**: the host's function log carries one `fullstack.request/1` line per request; metrics come from `python -m fullstack.backend metrics --log <export>`. The executor reviews them on each verification; the operator can read them in the Vercel dashboard.
* **Readiness (R2)**: `GET /api/v1/health` = 200 means a Runtime started on the store.
* **Alerting: H3, none; manual checks** (Register `§98` `ACT-007-DG-02`, a delegated decision). There is no automatic alert and nobody is paged. Failures are found by the checks in runbook `§12.1`, run by the executor on each verification and before and after any deploy, rollback or restore, and by the operator at will. Who would receive an alert under H1 or H2 is a Founder decision not taken. *History: until ACT-007 this read "unresolved (no H1/H2/H3 selection)".*

## 7. Incidents

* Detect → classify → contain → investigate → recover → record, per runbook `§11`.
* A security incident is recorded even after it is corrected (ACT-004 `§58`); EXT-06 is the precedent.
* The executor investigates and proposes; the operator acts on anything that needs an account or a Founder decision.

## 8. Escalation

As runbook `§14`. In short: Production, spending, protection settings and
release go to the Founder; architecture goes to the Architect unless an Act
delegates it; an execution-permission block is recorded, never bypassed
(ACT-005 `§9`).
