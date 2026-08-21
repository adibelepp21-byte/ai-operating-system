# Engineering Specification — Skill Subsystem

**Phase:** AIOS 2.5 — Engineering Specification. Implementation-neutral. **Immutable basis:** Architecture Freeze v1.0. No architecture/entity/class/API/database/protocol/message-format is added.
**Confidence:** **[E]** ratified/frozen · **[A]** engineering abstraction · **[O]** open / Architect reserved.

## 1. Purpose
[E] A Skill is a reusable unit of ability, declared by Agent Definitions (0+ per Definition, INV-15) and used within Agent-Instance actions (Domain Model; Freeze §4).

## 2. Responsibilities
[A] Provide a reusable, composable, discoverable ability. [E] Be a facility, not an actor — it authors no independent Trace (INV-4) and holds no external dependency (INV-12).

## 3. Owned Data
[E] Skill definitions, owned centrally (Domain Model §5). [A] Registration/discovery metadata (conceptual), enabling lookup.

## 4. Lifecycle
[A] Registered → discovered → used within actions → reused. [E] Governed centrally.

## 5. Public Interfaces (conceptual only)
[A] Conceptually exposes: (a) register a Skill (facility), (b) discover a Skill, (c) be-used-by an Agent Instance, (d) be-composed-into a Workflow. [E] Exposes **no** external-integration capability (INV-12) and **no** independent Trace authorship (INV-4). *(No signatures/formats.)*

## 6. Internal Responsibilities
[A] Maintain a lookup facility (registry — a facility, not an actor, per P-U8/OQ-2); support composition into Workflows.

## 7. Allowed Dependencies
[E] Used by Agent Instances; composed within Workflows; declared by Agent Definitions (INV-15).

## 8. Forbidden Dependencies
[E] Must not hold an external/vendor dependency (INV-12 — that is Tool's role). [E] Must not author independent Trace (INV-4). [A] Must not own Knowledge or govern.

## 9. Trace Requirements
[E] A Skill's use is accountable through the invoking Agent-Instance action's Trace (INV-4), never a Trace of the Skill itself (OQ-2).

## 10. Governance Constraints
[A] Skills execute ability; they do not decide governance (PR-3). [A] Skill registration/discovery is a facility beneath governance.

## 11. Failure Behaviour
[E] Fail closed (PR-4): a Skill that cannot be resolved/used causes the invoking action to halt accountably, not to proceed silently.

## 12. Extension Points
[A] New Skills registered without core change (registry pattern). [O] Progressive discovery/disclosure is a candidate evolution (historical evidence), admissible under the facility boundary.

## 13. Future Evolution
[O] Skill registry discipline and discovery model reserved to later phases and the Architect.

## 14. Open Questions
[O] Registry facility scope. **Skill↔Capability — RESOLVED:** T-2 Skill half **DETERMINED — derived, no direct edge** (`DEC-F03-053 = S-ALT-1`, reaffirmed against the Canonical Relationship Model under `ACT-CC-F03-055 §4`: `Capability exposes Skill` is **Inferred**, i.e. *"reasoned [A] … but not stated verbatim"*, and "exposes" appears **0 times** in the Domain Model and the Freeze. Declining to ratify it is what S-ALT-1 decides.) Capability and Skill connect only through the two ratified derived paths — via an Agent Definition, or via a Workflow. **No direct edge exists or is pending.** **Skill↔Workflow** is ratified — `§7` above states **[E]** *"composed within Workflows"*, Domain Model §4 carries *"Workflow **contains** Skill"*, and Freeze §4 lists *"compose Skills"*; this entry tracked the Relationship Model's older *Inferred* status and is corrected here.
