# Engineering Specification — Agent Subsystem

**Phase:** AIOS 2.5 — Engineering Specification. Implementation-neutral. **Immutable basis:** Architecture Freeze v1.0. No architecture/entity/class/API/database/protocol/message-format is added.
**Confidence:** **[E]** ratified/frozen · **[A]** engineering abstraction · **[O]** open / Architect reserved.

## 1. Purpose
[E] The Agent subsystem covers Agent Definition (the governed template) and Agent Instance (a runtime execution of exactly one Definition — the only actor) (Freeze INV-2/3; Domain Model §6).

## 2. Responsibilities
[E] An Agent Definition implements ≥1 Capability (INV-2) and may declare 0+ Skills and 0+ Workflows (INV-15). [E] An Agent Instance acts, and every action produces exactly one Trace record (INV-4). [A] Instances use Skills/Tools, consume Knowledge, write scoped Memory.

## 3. Owned Data
[E] Agent Definitions owned by exactly one Department (INV-2). [E] Agent Instances not owned — transient, accountable to the Department owning the Definition (Domain Model §5).

## 4. Lifecycle
[E] Definition (governed, persistent) → Runtime creates Instance (INV-3) → governed action(s) each producing Trace (INV-4) → conclusion. [A] The Definition persists; the Instance is ephemeral; the Trace is permanent.

## 5. Public Interfaces (conceptual only)
[A] Conceptually exposes: (a) define an agent (as a governed template), (b) instantiate (via Runtime), (c) act (producing Trace). [E] Exposes **no** capability for direct Instance↔Instance collaboration outside Workflow/Knowledge/scoped Memory (INV-13), nor to modify Trace (INV-5), nor to self-promote Memory (INV-8). *(No signatures/formats.)*

## 6. Internal Responsibilities
[A] Bind a Definition to its Capabilities/Skills/Workflows; ensure each Instance action is Trace-producing; keep the actor boundary (only Instances act).

## 7. Allowed Dependencies
[E] Depends on Runtime (to be instantiated), Capabilities (implemented), Skills/Workflows (declared), Tools (used), Knowledge (consumed), scoped Memory (written).

## 8. Forbidden Dependencies
[E] Must not modify Trace (INV-5). [E] Must not collaborate directly agent-to-agent outside sanctioned channels (INV-13). [E] Must not redefine a Capability (Freeze §4). [E] Must not hold a non-Tool external dependency (INV-12).

## 9. Trace Requirements
[E] Every Agent-Instance action → exactly one Trace record, unconditionally (INV-4). [A] This is the subsystem's central obligation.

## 10. Governance Constraints
[E] Agents execute; they do not govern (PR-3). [E] An Agent may propose (e.g., surface a Memory candidate) but may not decide promotion (INV-8). [E] Capability implementation counts toward INV-14 (no orphan capabilities).

## 11. Failure Behaviour
[E] Fail closed (PR-4): if an action cannot produce Trace, it is not accountable and must not be treated as done. [A] Definition without an implemented Capability is invalid (INV-2/14) and flagged for governance.

## 12. Extension Points
[A] Agent Definitions are extensible (new Skills/Workflows declared, INV-15). [O] Agent construction discipline is the subject of Phase 4 (Agent Factory).

## 13. Future Evolution
[O] The Agent Factory (Phase 4) will define governed construction of Definitions/Instances atop the Native Core; reserved to the Architect.

## 14. Open Questions
[O] Agent-Instance↔Skill/Knowledge relationships (currently Inferred). [O] Instance identity/attribution details beyond ratified rules.
