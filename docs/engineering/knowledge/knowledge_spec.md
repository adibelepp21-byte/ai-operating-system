# Engineering Specification — Knowledge Subsystem

**Phase:** AIOS 2.5 — Engineering Specification. Implementation-neutral. **Immutable basis:** Architecture Freeze v1.0. No architecture/entity/class/API/database/protocol/message-format is added.
**Confidence:** **[E]** ratified/frozen · **[A]** engineering abstraction · **[O]** open / Architect reserved.

## 1. Purpose
[E] Knowledge is durable, authoritative, versioned understanding, entered **only** through governed promotion (Freeze INV-7/8), the output of governed review.

## 2. Responsibilities
[E] Hold authoritative Knowledge; accept entries/changes only via governed promotion (INV-8). [E] Be durable — not casually deleted (INV-7). [A] Preserve versioned history (change means a new version, never in-place edit).

## 3. Owned Data
[E] Knowledge items — collectively owned by the Organization, each with a home Department accountable (Domain Model §5). [A] Conceptually versioned; validity is an orthogonal, governed condition.

## 4. Lifecycle
[A] Candidate (from Memory) → governed admission → Active version → (governed revision) → Superseded version. [E] Entry and change happen only through governed review (INV-8). [O] The precise admission model and versioned-repository discipline are reserved (Freeze §10; Architecture Review R-A4).

## 5. Public Interfaces (conceptual only)
[A] Conceptually exposes: (a) be-consumed-by-agents (read), (b) accept-admission/revision *only from the governed review process*. [E] Exposes **no** capability to be written outside governed promotion. *(No signatures/formats.)*

## 6. Internal Responsibilities
[A] Maintain versioned records; record validity conditions set by governed review; preserve prior versions on revision (never overwrite).

## 7. Allowed Dependencies
[E] Depends on the Governance subsystem (promotion authority) and Memory (candidate source). [A] May rely on a storage facility beneath it.

## 8. Forbidden Dependencies
[E] Must not accept entry from execution directly (bypassing promotion — INV-8). [E] Must not be owned by Runtime/Infrastructure. [E] Must not hold an external dependency (INV-12).

## 9. Trace Requirements
[A] Admission/revision are governed decisions; the decision event is accountable through the governed-review action that authors it (INV-4 applies to the acting Instance/reviewer path). [A] Knowledge storage itself is a facility, not an independent traced actor (OQ-2).

## 10. Governance Constraints
[E] Knowledge cannot bypass promotion (INV-8). [E] Change is human-governed; automation may propose candidates and surface conditions but not admit (PR-3; §6.2 invariant 2).

## 11. Failure Behaviour
[E] Fail closed (PR-4): if a promotion decision is absent or unauthorized, no Knowledge is created or changed. [A] An unadmitted candidate remains a candidate, never silently authoritative.

## 12. Extension Points
[A] Validity conditions and versioning discipline are governed, extensible under Domain-Model authority. [O] Retrieval/consumption interfaces are reserved.

## 13. Future Evolution
[O] The admission model, versioned repository, conflict handling, and consumption path are design-open (Freeze §10) — each a governed decision.

## 14. Open Questions
[O] Admission model finalization. [O] Versioned-repository discipline. [O] Governed *read/consumption* path (whether consumption needs governance) — Relationship Model §13.
