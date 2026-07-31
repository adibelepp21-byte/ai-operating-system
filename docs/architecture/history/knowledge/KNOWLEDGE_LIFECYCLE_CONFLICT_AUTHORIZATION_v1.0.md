# Architect Authorization Record — Knowledge Lifecycle & Conflict Resolution v1.0

**Status:** Authorization record. Documents architectural direction approved by the Architect. **No implementation, code, schema, API, storage design, or governance-document change is authorized by this record.**
**Version:** v1.0
**Authority:** Architect Authorization, in response to `KNOWLEDGE_LIFECYCLE_CONFLICT_DECISION_PACKAGE_v1.0.md`'s Architect Approval Checklist (4 items).
**Scope of this document:** Records exactly what was approved and how, so this authorization is a permanent, citable reference for every future Knowledge architecture phase — the same durability principle this authorization itself establishes for Knowledge.

---

## Decision 1 — Knowledge Versioned Identity Model

**APPROVED.**

- Knowledge uses a stable identity with an append-only-versioned lifecycle.
- One Knowledge identity may have many versions.
- Old versions are never altered or deleted.
- Revision produces a new version that supersedes the prior one.
- **Supersession and conflict are confirmed as distinct concepts**:
  - **Supersession** = the same Knowledge identity undergoing a controlled change (new version, same identity).
  - **Conflict** = different Knowledge identities holding contradicting claims (no shared identity).

**Rationale on record**: consistent with the Trace immutability pattern, Domain Model §6 lifecycle requirements, and the auditability/explainability principles this arc has proven throughout.

## Decision 2 — Home Department vs. Domain Model §8

**APPROVED WITH INTERPRETATION.**

**Final interpretation, on record**:
- "Home Department" does **not** mean Knowledge is exclusively owned by one Department.
- Knowledge remains a Substrate entity that is cross-cutting, addressable from anywhere in AIOS, and never the private property of any single Department — per Domain Model §8, unchanged.
- Home Department means only: accountability point, curator responsibility, operational ownership, first responder for maintenance/conflict handling.
- Home Department explicitly does **not** grant: exclusive access rights, authority to restrict Knowledge from other Departments, or authority to change Knowledge outside the governed lifecycle process.

**This resolves the tension the integrated review identified**: Domain Model §8 (cross-cutting, non-private) and Domain Model §5 (home Department ownership) are now explicitly reconciled — §8 governs access/addressability, §5 (via Home Department) governs accountability only. Neither is subordinate to the other; they address different questions.

## Decision 3 — Invariant 10 Analogy for Knowledge Conflict Escalation

**ANALOGY REJECTED.**

- Invariant 10 is **not** extended to Knowledge conflict resolution.
- Confirmed reason: invariant 10 explicitly governs Capability dependency handling; applying it to Knowledge conflict would have been a silent governance extension — exactly what the integrated review flagged and what this authorization now formally declines.
- **Status: Deferred.** A cross-Department Knowledge conflict escalation model requires its own future design, grounded in real usage evidence, not an analogy to a differently-scoped invariant.

## Decision 4 — Archived State

**APPROVED:** Archived is **not** a mandatory Knowledge lifecycle state in v1.

- Valid initial lifecycle states: **Active**, **Superseded**.
- **Conflict is confirmed as a condition/status resulting from evaluation, not a lifecycle state in its own right.**
- Archived-as-a-mandatory-state is rejected: no evidence yet demonstrates a need for archival distinct from supersession; adding an unevidenced state increases complexity without proven benefit.

---

## Remaining Open Questions — Explicitly Untouched

No decision was made on any of the following; all five remain exactly as classified in the prior Decision Package:

1. Exact Revision Required trigger.
2. Conflict evidence threshold.
3. Cross-Department escalation authority.
4. Snapshot mechanics.
5. The boundary between a revision signal and an executed revision.

---

## Implementation Boundary

This authorization approves **architectural direction only**. Explicitly forbidden as a consequence of this authorization: writing code, creating a schema, creating an API, creating a storage design, modifying any governance document, or performing any implementation task.

## Next Step (per Architect direction, not yet undertaken)

The Architect has indicated the next phase will be an **Architecture Consistency Review** across the full Knowledge Architecture — Admission Model, Ownership Model, Lifecycle Model, Conflict Resolution Model, Retrieval Boundary, Memory Interaction, and Trace Interaction — to confirm consistency with the Canonical Domain Model before Implementation Planning begins. This is **not** authorized or begun by this document; it awaits a separate future directive.

---

No code, schema, API, storage design, or governance document was created or modified by this authorization record. Documented per instruction; awaiting the next directive.
