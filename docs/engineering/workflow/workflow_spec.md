# Engineering Specification — Workflow Subsystem

**Phase:** AIOS 2.5 — Engineering Specification. Implementation-neutral. **Immutable basis:** Architecture Freeze v1.0. No architecture/entity/class/API/database/protocol/message-format is added.
**Confidence:** **[E]** ratified/frozen · **[A]** engineering abstraction · **[O]** open / Architect reserved.

## 1. Purpose
[E] Workflow is the governed composition and the **sole sanctioned channel** for multi-agent coordination (Freeze INV-13; Domain Model).

## 2. Responsibilities
[E] Coordinate Agent Instances (INV-13); compose Skills/actions. [A] Ensure each coordinated step is a Trace-producing Agent-Instance action (INV-4).

## 3. Owned Data
[E] Workflow definitions, owned centrally (Domain Model §5). [A] Composition structure (conceptual), declared by Agent Definitions (0+ per Definition, INV-15).

## 4. Lifecycle
[A] Defined → executed by Runtime as Agent-Instance actions → concluded. [E] Governed centrally.

## 5. Public Interfaces (conceptual only)
[A] Conceptually exposes: (a) define a governed composition, (b) coordinate Agent Instances, (c) compose Skills. [E] Exposes **no** capability for agent collaboration outside itself/Knowledge/scoped Memory (INV-13). *(No signatures/formats.)*

## 6. Internal Responsibilities
[A] Sequence/branch composition; validate that coordination stays within INV-13 and that each step is Trace-producing; keep composition checkable.

## 7. Allowed Dependencies
[E] Executed by Runtime; composes Skills; realizes Capabilities (Inferred, reserved). [A] Coordinates Agent Instances.

## 8. Forbidden Dependencies
[E] Must not permit collaboration outside itself/Knowledge/scoped Memory (INV-13). [E] Must not hold an external dependency (INV-12). [E] Is not the Runtime (Vocabulary — Workflow ≠ Runtime).

## 9. Trace Requirements
[E] Each coordinated step is an Agent-Instance action producing exactly one Trace record (INV-4). [A] Coordination hand-offs are accountable through those actions.

## 10. Governance Constraints
[E] Workflow is the only sanctioned multi-agent channel (INV-13). [A] Free agent-to-agent delegation is a rejected anti-pattern (Freeze AD-9). [E] Validation is a governance property, not a convenience.

## 11. Failure Behaviour
[E] Fail closed (PR-4): on missing authorization or unmet precondition, a Workflow halts rather than proceeds; a step that cannot be Traced is not completed.

## 12. Extension Points
[A] New Workflows and composition patterns without core change. [O] Compile-time/connection validation of governed composition is a candidate evolution (historical evidence), admissible under governance.

## 13. Future Evolution
[O] Workflow validation discipline and failure-recovery semantics reserved to later phases and the Architect.

## 14. Open Questions
[O] Workflow↔Capability/Skill and Runtime↔Workflow relationships (Inferred). [O] Failure-recovery/compensation model (fail-closed baseline holds).
