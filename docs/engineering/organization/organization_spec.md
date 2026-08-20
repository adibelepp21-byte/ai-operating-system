# Engineering Specification — Organization Subsystem

**Phase:** AIOS 5 — Engineering Specification. Implementation-neutral. **Immutable basis:** Architecture Freeze v1.0. No architecture/entity/class/API/database/protocol/message-format is added.
**Confidence:** **[E]** ratified/frozen · **[A]** engineering abstraction · **[O]** open / Architect reserved.
**Authority:** FOUNDER · `ACT-CC-F03-035` `DEC-DEPT-REALIZATION = AUTHORIZE` (R-2). Realizes the already-ratified Freeze §4 entity; ratifies nothing.

## 1. Purpose
[E] Organization is the **hierarchy root** and the **accountability root** (Freeze §4 Spine). [A] It names the whole under which Departments are accountable; it is not itself an actor.

## 2. Responsibilities
[E] Own Departments. [E] Be the accountability root. [A] Provide the single root against which Department parentage is resolved.

## 3. Owned Data
[E] Organization identity and the set of Departments it owns (Freeze §4). [A] Nothing else; membership is by Department reference, not by embedded Department state.

## 4. Lifecycle
[E] **Governed** (Freeze §4). [A] Created and changed only through the governed decision path; this boundary defines no lifecycle *states* — Freeze §4 says "governed" and stops there, and so does this specification.

## 5. Public Interfaces (conceptual only)
[A] Conceptually exposes: (a) be identified, (b) own Departments, (c) be queried for the Departments it owns. [E] Exposes **no** execution surface — Freeze §4 forbids Organization *"acting as an executor"*. *(No signatures/formats.)*

## 6. Internal Responsibilities
[A] Maintain its identity and the ownership set. [A] Nothing computed, nothing executed.

## 7. Allowed Dependencies
[E] None above it — Freeze §4: *"Dependencies: none above it."* [A] It may be referenced by Department (its children); it references nothing upward.

## 8. Forbidden Dependencies
[E] Must not act as an executor (Freeze §4). [E] Must not mutate Trace (Freeze §4; INV-5). [E] Must not hold an external dependency (INV-12).

## 9. Trace Requirements
[A] Organization is not an actor and authors no Trace. [A] Changes to an Organization are governed actions accountable via their governed-decision path (INV-4 on the acting path).

## 10. Governance Constraints
[E] Lifecycle is governed (Freeze §4). [A] Ownership is accountability: the Organization is where Department accountability terminates.

## 11. Failure Behaviour
[A] Fail closed (PR-4): an Organization without identity is invalid; a Department naming an unknown Organization is an unresolvable parent and fails closed.

## 12. Extension Points
[A] New Organizations and new Department memberships are the extension mechanism. [O] Multi-Organization topology beyond a single root is **not** established by Freeze §4 and is reserved.

## 13. Future Evolution
[O] Organization-level policy, budget, workforce and reporting structures are **not** in Freeze §4 and are reserved to the Architect.

## 14. Open Questions
[O] Whether more than one Organization may coexist. [O] Organization lifecycle *states*, which Freeze §4 does not enumerate.
