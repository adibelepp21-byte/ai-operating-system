# Engineering Specification — Governance Subsystem

**Phase:** AIOS 2.5 — Engineering Specification. Implementation-neutral. **Immutable basis:** Architecture Freeze v1.0. No architecture/entity/class/API/database/protocol/message-format is added.
**Confidence:** **[E]** ratified/frozen · **[A]** engineering abstraction · **[O]** open / Architect reserved.

## 1. Purpose
[E] Governance holds authority over decisions, accountability, and the promotion of derived Memory into authoritative Knowledge (Freeze §8; Constitution; INV-8). [A] It is the layer that makes execution accountable, never overridable by automation.

## 2. Responsibilities
[E] Decision authority (Constitution §3 tiers); promotion authority (INV-8); review authority (human decisions); accountability via Trace (INV-4/5). [A] Detect-and-surface for humans; decide nothing automatically (PR-3).

## 3. Owned Data
[A] Governed decision records and review outcomes (conceptually), each accountable via Trace. [E] Governance owns no execution entity; it governs the Memory→Knowledge edge and authority (Mapping §5).

## 4. Lifecycle
[A] A governed decision is *proposed (by detection)* → *reviewed (by a human authority)* → *recorded* (accountable). [E] No automatic decision path exists (§6.2 invariant 2).

## 5. Public Interfaces (conceptual only)
[A] Conceptually exposes: (a) accept human review decisions, (b) authorize/deny promotion, (c) read Trace/Memory for evidence, (d) publish decision outcomes. [E] Exposes **no** capability for automation to decide or to override a decision. *(No signatures/formats.)*

## 6. Internal Responsibilities
[A] Enforce authority tiers; gate the promotion boundary; ensure detection proposes but never decides; fail closed on missing authority.

## 7. Allowed Dependencies
[E] Reads Trace (evidence) and Memory (candidates). [A] Directs the Knowledge subsystem's admission/revision.

## 8. Forbidden Dependencies
[E] Must not be overridable by, or dependent on, execution authority (§6.2 invariant 2). [E] Must not mutate Trace (INV-5). [E] Must not hold an external dependency (INV-12).

## 9. Trace Requirements
[E] Governed decisions are accountable actions — each produces Trace via its acting path (INV-4). [A] Governance reads Trace; it never edits it.

## 10. Governance Constraints
[E] Automation may request/recommend/detect; it may not decide (Constitution §6.2 invariant 2; PR-3). [E] Cross-Department and Domain-Model changes follow the Decision-Making Process; some are non-delegable (§3.2; INV-10).

## 11. Failure Behaviour
[E] Fail closed (PR-4): absence of authorization means no promotion, no decision, no change. [A] Ambiguous authority halts rather than proceeds.

## 12. Extension Points
[A] Authority tiers, review workflows, and detection signals are governed and extensible under Constitutional authority. [O] Delegation-documentation discipline (ADR framework) is reserved.

## 13. Future Evolution
[O] Formal decision-record/ADR handling, delegation scopes, and conflict-escalation are reserved to the Architect (Constitution §3; ADR framework).

## 14. Open Questions
[O] Whether Governance is an entity-with-relationships or strictly a layer (Architecture Review R-A7). [O] Authority's ontological status. [O] Admission decision packaging.
