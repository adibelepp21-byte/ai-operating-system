# FS-DP-02 — Identity and Authentication

| Field | Value |
|---|---|
| **Identifier** | `FS-DP-02` (provisional) |
| **Area** | Identity (as a general/auth concept), Authentication — Freeze `§10`, Architect-reserved (*"no ratified entity"*) |
| **Status** | **PROPOSED — NOT RATIFIED** |
| **Decision owner** | Holder of Architect authority (`FD-FS-001` D2-A; `FD-2` open) |
| **Founder constraints** | No spending (D3-A). Supabase is named for the **database** only; using its authentication service is a further choice this package asks for |
| **Prepared by** | Claude Code, 2026-09-26 |

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
