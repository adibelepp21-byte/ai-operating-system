# Engineering Specification — Optimization Subsystem

**Phase:** AIOS 2.5 — Engineering Specification. Implementation-neutral. **Immutable basis:** Architecture Freeze v1.0. No architecture/entity/class/API/database/protocol/message-format is added.
**Confidence:** **[E]** ratified/frozen · **[A]** engineering abstraction · **[O]** open / Architect reserved.

## 1. Purpose
[E] Optimization is the **governed learning loop** — it detects and proposes improvements from Trace/Memory; humans decide promotion (Freeze §7/§10; PR-3; INV-8). [A] AIOS improves without autonomous self-modification.

## 2. Responsibilities
[A] Observe Trace and Memory; surface candidates, conditions, and quality signals — **as proposals only**. [E] Never decide governance, never auto-promote, never mutate Trace (PR-3; INV-8; INV-5).

## 3. Owned Data
[A] Derived evaluation signals and candidate proposals (conceptual, non-authoritative). [E] Owns no authoritative data; all authority remains with Governance/Knowledge.

## 4. Lifecycle
[A] Observe (Trace/Memory) → detect candidates/conditions → **propose to governed review** → (humans decide). [E] No step promotes or decides (INV-8; §6.2 invariant 2).

## 5. Public Interfaces (conceptual only)
[A] Conceptually exposes: (a) evaluate/observe, (b) propose candidates/conditions to Governance. [E] Exposes **no** capability to promote, decide, or modify Trace/Knowledge. *(No signatures/formats.)*

## 6. Internal Responsibilities
[A] Compute evaluation/quality signals; prioritize candidates (prioritize only, never gate — PR-3); present proposals for human decision.

## 7. Allowed Dependencies
[E] Reads Trace (evidence) and Memory (derivation); submits proposals to Governance.

## 8. Forbidden Dependencies
[E] Must not decide governance (PR-3). [E] Must not auto-promote Memory→Knowledge (INV-8). [E] Must not mutate Trace (INV-5). [E] Must not hold an external dependency (INV-12).

## 9. Trace Requirements
[A] Optimization observes Trace; it never authors or edits it. [A] Any action it triggers occurs through a governed/agent path that itself produces Trace (INV-4).

## 10. Governance Constraints
[E] Detect, Don't Decide (PR-3): Optimization informs; Governance decides. [E] The promotion boundary (INV-8) and human authority (§6.2 invariant 2) are absolute.

## 11. Failure Behaviour
[E] Fail closed (PR-4): if evaluation is uncertain, it proposes nothing rather than deciding. [A] A bad proposal is harmless because humans gate promotion.

## 12. Extension Points
[A] New evaluation/detection signals are extensible — all remain detect-only. [O] Model-level optimization is an external, reserved concern (Freeze §10) — not an AIOS entity.

## 13. Future Evolution
[O] The governed improvement loop (provenance-carrying, human-promoted improvements) is a candidate evolution; model-optimization itself remains reserved/external.

## 14. Open Questions
[O] Candidate-prioritization model (detect-only). [O] Whether/how model-optimization ever attaches to AIOS (reserved). [O] Evaluation-signal catalogue.
