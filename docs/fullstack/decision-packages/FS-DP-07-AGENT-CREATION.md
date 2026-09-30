# FS-DP-07 — Agent Creation Through the Application Surface

| Field | Value |
|---|---|
| **Identifier** | `FS-DP-07` (provisional) |
| **Area** | Governed construction of Agent Definitions and Instances (the Agent Factory) — Architect-reserved (Freeze `§13`; Blueprint `§3`; `agent_spec §12–§13`) |
| **Status** | **CURRENT: A2** (Agent Instance registration only), selected by the delegated decision `ACT-008-DG-01` under `ACT-CC-POST-P13-AIOS-FULL-STACK-008` `§7.2` (Register `§101`, 2026-09-30); A3 (Agent Factory) is not built. *History, kept as recorded:* **RATIFIED — A1**, by the Founder as Architect in `ACT-CC-POST-P13-AIOS-FULL-STACK-004` `§12` (Register `§93`, `ACT-004-DG-03`); ACT-007 classified Scenario A as a residual under A1 (`ACT-007-DG-01`, `§98`), which ACT-008 superseded because Scenario A is mandatory and A1 cannot execute it. *The A1 text that follows is the package as it stood.* The Scenario A residual classification under A1 (`R2.5`) was not decided by ACT-004; it is classified outside the present FS-09 envelope, not executed, by the delegated decision `ACT-007-DG-01` (Register `§98`, 2026-09-30). Revision 2 (below) is the package as reviewed (`§89`) |
| **Decision owner** | Holder of Architect authority. Authority over Definitions sits with the owning Platform Division (Domain Model `§6`, via the Agent Definition Framework `§3`) |
| **Blocks** | Act FS-07 Scenario A: *User → Create Agent → Backend → AIOS Agent Capability → Persist → Result* |
| **Prepared by** | Claude Code, 2026-09-26; **Revision 2** 2026-09-27 (below), on the Founder's *"FS-09 — DECISION PACKAGE PREPARATION"* |

## Context

- The `agent` boundary exports the contract only. `AgentDefinition` and
  `AgentInstance` are immutable data contracts; how they are *"governed,
  validated against Capabilities, created, or registered"* is reserved.
- Agent Definitions exist as governed documents
  (`docs/architecture/organization/*/agent-definitions/`), owned by Platform
  Divisions.
- `tools/agent_instance_registry.py` registers Agent Instances, but its
  authority is `FD-P11-001 §7`, scoped to P11-W4. Reusing it from the
  application would extend that authority without a decision.

## Part A — Architectural decision (ADR-eligible)

| Option | Statement | Assessment |
|---|---|---|
| **A1** | **Keep reserved.** The application shows the Agent Instances that act (from Workflow steps and Trace) and creates none | Scenario A stays blocked; nothing else is |
| A2 | **Instance registration only.** An operator holding a new scope `aios.agent.register` registers an Agent Instance of an **existing** governed Definition through the canonical mechanism. Definitions stay governed documents | Needs an authority instrument extending `FD-P11-001 §7`-style registration to the application |
| A3 | **Full Agent Factory.** Definitions authored through the application | Crosses Platform Division authority over Definitions; the largest change; not recommended as a first step |

**Recommendation: A1 now; A2 when a use needs it.** A2 is the smallest
change that makes Scenario A meaningful without the application authoring
Definitions.

## Part B — Implementation decision

None needed for A1. For A2: one route, `POST /api/v1/agent-instances`, over
the canonical `AgentInstance` contract; registration persisted as an
append-only record; audited.

## Until decided

No route creates an Agent. `GET /api/v1/runs/{id}` shows which Agent
Instances acted.

## Exact decision required

- [ ] Part A: A1 · A2 (with its authority instrument) · A3
- [ ] Decided as: Architect · Founder as Architect

## Revision 2 (2026-09-27): FS-09 Architect review package

Revision 1 above is unchanged. **A1, A2 and A3 are preserved exactly as stated
there.** No Agent Factory is built, or proposed to be built, merely to satisfy
Scenario A.

### R2.1 Decision ID

`FS-DP-07` (provisional), revision 2. Register `§89`.

### R2.2 Exact architectural question

May the AIOS Full Stack application create Agents and, if it may, what it may
create: nothing (A1), an Agent **Instance** of an existing governed Definition
(A2), or Agent **Definitions** themselves (A3).

### R2.3 Canonical sources

| Source | What it says |
|---|---|
| ACT-001 `§18` (FS-07) | *"Mandatory End-to-End Classes. Scenario A — Agent: User → Create Agent → Backend → AIOS Agent Capability → Persist → Result"* |
| ACT-001 `§20` exit | *"residual non-blocking findings classified"* |
| Freeze `§13`; Blueprint `§3`; `agent_spec §12–§13` | how Definitions and Instances are *"governed, validated against Capabilities, created, or registered"* is reserved |
| Domain Model `§6`; Agent Definition Framework `§3` | Definitions belong to the owning Platform Division |
| `FD-P11-001 §7` | Agent Instance registration, authorized for P11-W4 only |

### R2.4 Current implementation state

* The application runs **one** catalog Workflow (`document-conformance-review`) with three fixed Agent Instance keys: `tool-proposing-agent`, `engineering-intelligence-agent` and `workflow-participating-agent` (`consumers` agents, composed in `fullstack/backend/aios.py`).
* **No route creates, registers or edits an Agent.** `GET /api/v1/runs/{id}` shows which Agent Instances acted, and Trace records each one's actions.
* `tools/agent_instance_registry.py` registers Instances under `FD-P11-001 §7` (P11-W4 scope). The application does not import it (`aios.py` *"imports nothing from `tools/`"*).
* Agent Definitions exist as governed documents under `docs/architecture/organization/*/agent-definitions/`.
* Readiness gate: *Functionality: agent creation (Scenario A)* **BLOCKED** on this package.

### R2.5 Authority required

**Architect** (or the Founder acting as Architect) decides A1, A2 or A3.
Authority over Definitions sits with the owning Platform Division. A2 also
needs an **authority instrument** extending `FD-P11-001 §7`-style
registration to the application; A3 would reach into Platform Division
authority. If A1: the **Founder** decides whether mandatory Scenario A may
stand as a classified non-blocking residual.

### R2.6 Available options (verbatim from revision 1)

| Option | Statement |
|---|---|
| **A1** | **Keep reserved.** The application shows the Agent Instances that act (from Workflow steps and Trace) and creates none |
| **A2** | **Instance registration only.** An operator holding a new scope `aios.agent.register` registers an Agent Instance of an **existing** governed Definition through the canonical mechanism. Definitions stay governed documents |
| **A3** | **Full Agent Factory.** Definitions authored through the application |

### R2.7 Architectural consequences

| Option | Consequence |
|---|---|
| A1 | none. Scenario A stays impossible, contrary to its mandatory status, unless classified (`R2.5`) |
| A2 | one new route over the canonical `AgentInstance` contract (identity only, one Definition, INV-3); an organizational registration record beside it, as P11-W4 did. Definitions stay documents |
| A3 | the application becomes an authoring surface for governed Definitions: a new path into Platform Division authority, validation against Capabilities in the application, and the largest change to the frozen boundaries |

### R2.8 Data and state consequences

| Option | Consequence |
|---|---|
| A1 | none |
| A2 | a new append-only partition of registrations. **A registration can never be deleted**: a wrong one stays and needs a later revocation record, whose design is part of A2 |
| A3 | Definitions would exist both as governed documents and as application records: two sources of truth unless one is designated. Records are append-only, as in A2 |

All three persist in the shared store until `FS-09-ENV` is decided.

### R2.9 Security consequences

| Option | Consequence |
|---|---|
| A1 | no new capability exposed |
| A2 | a new scope, `aios.agent.register`, issued to named operators only (B3). Every registration audited by subject. A registered Instance does not grant authority (`§17`, *"AGENT INSTANCE ≠ AUTHORITY"*) |
| A3 | authoring Definitions through a network API: the most powerful capability the application would hold; compromise of a token with that scope alters what agents may be |

### R2.10 Operational consequences

* A1: nothing to operate.
* A2: token issuance for the new scope; runbook entries for registration and revocation; review of registrations.
* A3: a Definition review workflow in the application, and Platform Division involvement in operations.

### R2.11 Verification requirements

* A1: the gate row becomes *classified residual* only on a recorded Founder decision (`R2.5`); a test that no route creates an Agent (the existing surface map test).
* A2: the authority instrument recorded first. Then tests: registration of an existing Definition succeeds; an unknown Definition, a missing scope and a duplicate are refused; the record is append-only and audited. Then a live Scenario A on a Preview (needs access).
* A3: its own package; not verifiable within FS-09.

### R2.12 Rollback implications

* A1: none.
* A2: a rollback below the route leaves registration records in the store, unread but intact; a later roll-forward reads them again. The record format must be readable by later versions (successor rule, FS-04 `§4`).
* A3: Definitions created through the application would outlive a rollback and conflict with the governed documents.

### R2.13 Explicit non-scope

**No Agent Factory is built to satisfy Scenario A.** No Definition is authored.
The P11-W4 registry authority is not reused. No scope is added and no route
is created by this package.

### R2.14 Dependencies

| On | Why |
|---|---|
| an authority instrument (A2) | extends `FD-P11-001 §7`-style registration beyond P11-W4 |
| Platform Divisions (A2, A3) | Definitions' owners |
| `FS-DP-02` B3 (ratified) | the new scope for A2 |
| `FS-09-ENV` | where registrations persist |
| Founder (A1) | the residual classification |

### R2.15 Whether it blocks FS-09

**Yes.** Scenario A is a mandatory class (ACT-001 `§18`). Gate row
*Functionality: agent creation (Scenario A)* is BLOCKED. Under A1, FS-09 can
pass only if the Founder classifies Scenario A as a non-blocking residual.

### R2.16 Analytical recommendation (**UNRATIFIED**)

> *Not a decision. Stands only as analysis until the Architect decides.*
> Revision 1's recommendation, unchanged: *"A1 now; A2 when a use needs it."*
> Under A1, the path to FS-09 PASS requires the Founder's residual
> classification. A2 requires its authority instrument before any construction.

### R2.17 Exact decision required

- [ ] Part A: A1 · A2 (with its authority instrument) · A3
- [ ] If A1: Founder classification of Scenario A (residual · not accepted)
- [ ] Decided as: Architect · Founder as Architect

