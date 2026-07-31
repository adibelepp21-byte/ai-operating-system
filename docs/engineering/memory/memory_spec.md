# Engineering Specification — Memory Subsystem

**Phase:** AIOS 2.5 — Engineering Specification. Implementation-neutral. **Immutable basis:** Architecture Freeze v1.0. No architecture/entity/class/API/database/protocol/message-format is added.
**Confidence:** **[E]** ratified/frozen · **[A]** engineering abstraction · **[O]** open / Architect reserved.

## 1. Purpose
[E] Memory is a dynamic, provisional, retention-bounded record of what an Agent Instance encountered, **derived from Trace** and **non-authoritative** (Freeze INV-7/8; Domain Model §6.1).

## 2. Responsibilities
[E] Derive Memory from Trace evidence (§6.1). [E] Remain a *candidate source* for promotion — never authoritative, never a source that overrides Knowledge. [E] Honour a bounded retention window (INV-7).

## 3. Owned Data
[E] Derived memory records, scoped by the producing Agent Instance/Department (Domain Model §5). [A] Deliberately without stable identity across derivations (a documented design choice; Vocabulary). [E] Recomputable from Trace.

## 4. Lifecycle
[A] Derived → retained (bounded) → either recomputed, aged out, or *selected as a promotion candidate*. [E] Memory never self-promotes (INV-8).

## 5. Public Interfaces (conceptual only)
[A] Conceptually exposes: (a) derive-from-Trace, (b) read scoped memory, (c) offer candidates to the governed promotion process. [E] Exposes **no** capability to become Knowledge on its own, and **no** capability to write Trace. *(No signatures/formats.)*

## 6. Internal Responsibilities
[A] Recompute from Trace; compute retention/expiry; scope records; surface promotion candidates as *proposals only* (PR-3).

## 7. Allowed Dependencies
[E] May read Trace (derivation). [A] May rely on a storage facility beneath it.

## 8. Forbidden Dependencies
[E] Must not write or rewrite Trace (INV-5). [E] Must not write Knowledge directly (INV-8). [E] Must not hold an external dependency (INV-12).

## 9. Trace Requirements
[E] Memory derivation is itself performed within Agent-Instance actions where applicable; the *derivation facility* is infrastructure, not an independent traced actor (OQ-2). [A] Memory reads Trace; it never authors it.

## 10. Governance Constraints
[E] Promotion to Knowledge occurs **only** through governed human review (INV-8). [E] Ranking/confidence signals may *prioritize* candidates but may never *gate* promotion (PR-3).

## 11. Failure Behaviour
[E] Fail closed (PR-4): if derivation or scoping cannot be guaranteed, Memory is treated as absent, not as authoritative. [A] Loss is acceptable because Trace is permanent and Memory is recomputable.

## 12. Extension Points
[A] Retention policy, derivation heuristics, and candidate-prioritization signals are replaceable — none may cross the promotion boundary. [O] A stable Memory identity, if ever needed, is a governed Domain-Model change.

## 13. Future Evolution
[O] Tiered/working-vs-long-term memory organization is a candidate evolution (DNA Library) — admissible only with the governed promotion boundary intact.

## 14. Open Questions
[O] Whether Memory should ever gain a stable identity. [O] Retention-window policy. [O] Candidate-selection prioritization model (detect-only).
