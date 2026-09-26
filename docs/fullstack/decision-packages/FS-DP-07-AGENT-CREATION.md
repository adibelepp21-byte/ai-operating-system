# FS-DP-07 — Agent Creation Through the Application Surface

| Field | Value |
|---|---|
| **Identifier** | `FS-DP-07` (provisional) |
| **Area** | Governed construction of Agent Definitions and Instances (the Agent Factory) — Architect-reserved (Freeze `§13`; Blueprint `§3`; `agent_spec §12–§13`) |
| **Status** | **PROPOSED — NOT RATIFIED** |
| **Decision owner** | Holder of Architect authority. Authority over Definitions sits with the owning Platform Division (Domain Model `§6`, via the Agent Definition Framework `§3`) |
| **Blocks** | Act FS-07 Scenario A: *User → Create Agent → Backend → AIOS Agent Capability → Persist → Result* |
| **Prepared by** | Claude Code, 2026-09-26 |

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
