# Engineering Specification — Capability Subsystem

**Phase:** AIOS 2.5 — Engineering Specification. Implementation-neutral. **Immutable basis:** Architecture Freeze v1.0. No architecture/entity/class/API/database/protocol/message-format is added.
**Confidence:** **[E]** ratified/frozen · **[A]** engineering abstraction · **[O]** open / Architect reserved.

## 1. Purpose
[E] Capability is a Department-owned unit of governed ability (Freeze INV-1; Domain Model Spine). [A] It names *what* a Department can do, realized by Agent Definitions.

## 2. Responsibilities
[E] Be owned by exactly one Department (INV-1); be implemented by ≥1 active Agent Definition or be flagged (INV-14). [E] Declare explicit, versioned dependencies (INV-9); keep the dependency graph queryable (INV-11).

## 3. Owned Data
[E] Capability definitions and their explicit versioned dependency contracts, owned by one Department (INV-1/9). [A] Cross-Department dependencies are governed records (INV-10).

## 4. Lifecycle
[A] Defined under a Department → implemented by Agent Definitions → evolved under governance. [E] Zero active implementers is an invalid steady state, flagged for governance review (INV-14).

## 5. Public Interfaces (conceptual only)
[A] Conceptually exposes: (a) be-owned, (b) be-implemented-by Agent Definitions, (c) declare-versioned-dependency-on another Capability (governed). [E] Exposes **no** capability to execute itself (Freeze §4) or to depend cross-Department without governance (INV-10). *(No signatures/formats.)*

## 6. Internal Responsibilities
[A] Maintain explicit versioned dependency references (INV-9); keep dependencies documented and queryable (INV-11).

## 7. Allowed Dependencies
[E] Depends on its Department (ownership) and on other Capabilities *only* via explicit, versioned, governed contracts (INV-9/10).

## 8. Forbidden Dependencies
[E] Must not execute itself (Freeze §4). [E] Must not depend cross-Department without governance (INV-10). [E] Must not carry undocumented dependencies (INV-11). [E] Must not hold an external dependency (INV-12).

## 9. Trace Requirements
[A] Capability *changes* (definition, dependency adoption) are governed actions accountable via their governed-decision path (INV-4 on the acting path). [A] The Capability itself is not an actor and authors no Trace.

## 10. Governance Constraints
[E] Cross-Department dependencies require governance approval — never silent adoption (INV-10). [E] Orphan capabilities are flagged (INV-14). [A] Ownership is accountability (INV-1).

## 11. Failure Behaviour
[E] Fail closed (PR-4): an ungoverned or undocumented dependency is invalid; a zero-implementer capability is an invalid steady state (INV-14) and halts as a governance flag.

## 12. Extension Points
[A] New Capabilities and governed versioned dependencies are the primary extension mechanism. [O] Capability↔**Skill** composition is currently Inferred (reserved). **Partially discharged:** this read *"Capability↔Skill/Workflow"* until `DEC-F03-047` S-2; the **Workflow** half is now the canonical relationship `Workflow realizes Capability` (T-2 ALT-3, `DEC-F03-046`), directed **Workflow→Capability** — this boundary declares no Workflow.

## 13. Future Evolution
[O] Department Architecture (Phase 5) realizes Organization/Department/Capability ownership as a governed structure; reserved to the Architect.

## 14. Open Questions
[O] Capability↔**Skill** relationship ratification — the **Skill** half only. The Workflow half was ratified under `DEC-F03-045`/`DEC-F03-046`; **Capability↔Skill/Workflow is not fully ratified.** [O] Versioned-contract representation (reserved — no format defined here).
