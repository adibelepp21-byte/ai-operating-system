# Engineering Specification — Trace Subsystem

**Phase:** AIOS 2.5 — Engineering Specification. Implementation-neutral. Bridges the frozen architecture to future code without implementing it.
**Immutable basis:** Architecture Freeze v1.0. This spec adds **no** architecture, entity, class, API, database, protocol, or message format.
**Confidence:** **[E]** ratified/frozen · **[A]** engineering abstraction · **[O]** open / Architect reserved.

## 1. Purpose
[E] Trace is the immutable, append-only, unconditional record of one Agent-Instance action — the single permanent source of truth (Freeze INV-4/5/6). [A] The subsystem exists to make AIOS auditable *by construction*.

## 2. Responsibilities
[E] Produce exactly one record per Agent-Instance action, unconditionally (INV-4). [E] Guarantee immutability and append-only semantics (INV-5). [E] Capture cited content at write-time so explainability never depends on later existence of Memory/Knowledge (INV-6; PR-5). [A] Serve read access for derivation (Memory, review state).

## 3. Owned Data
[E] Trace records — owned by no one; governed only by retention policy (Domain Model §5). [A] Each record conceptually carries: the acting Agent-Instance reference, the action, and the captured content at write-time. [O] Exact record contents beyond the ratified "required contents" are reserved (Domain Model §2.1).

## 4. Lifecycle
[E] A record is *produced at action time*, *never edited or deleted* (INV-5), and *retained* per policy. [A] There is no update state and no draft state — a record's only transitions are "written" and (eventually, by retention) "aged".

## 5. Public Interfaces (conceptual only)
[A] Conceptually, Trace exposes: (a) an accept-a-completed-action-record capability (write-once), and (b) a read/derive capability for downstream subsystems. [E] It exposes **no** capability to modify or delete an existing record. *(No signatures, protocols, or formats are defined here.)*

## 6. Internal Responsibilities
[A] Enforce write-once semantics; embed captured content (PR-5); ensure production cannot be skipped or made conditional (INV-4). [A] Guarantee ordering/append discipline conceptually.

## 7. Allowed Dependencies
[E] None on higher layers. [A] May rely only on an infrastructure storage *facility* beneath it (audited through the invoking action, not an independent actor — OQ-2).

## 8. Forbidden Dependencies
[E] Must not depend on Memory, Knowledge, or Optimization (they derive from Trace, not vice-versa). [E] Must not hold an external/vendor dependency (INV-12 — that is Tool's role).

## 9. Trace Requirements
[E] Trace *is* the Trace requirement: production is unconditional and one-per-action (INV-4); it does not itself produce a Trace of its own writing (infinite-regress excluded — OQ-2 interpretation).

## 10. Governance Constraints
[E] Immutability is a governance guarantee, not a storage convenience (INV-5). [E] Production cannot be disabled by execution (Constitution §14.2). [A] Governance reads Trace; nothing edits it.

## 11. Failure Behaviour
[E] Fail closed (PR-4): if a Trace record cannot be written, the action must not be treated as completed/accountable. [A] A missing Trace is a governance failure, never a silent success.

## 12. Extension Points
[A] Retention policy is a governed, replaceable parameter. [O] Additional captured fields, if ever needed, enter only by governed Domain-Model change.

## 13. Future Evolution
[O] Retention discipline, storage-facility choice, and export/audit tooling are reserved to later phases and the Architect — none may weaken immutability or unconditionality.

## 14. Open Questions
[O] Exact record schema beyond ratified required contents (reserved). [O] Retention-window governance policy. [O] Whether audit-export is a Trace responsibility or an Infrastructure facility.
