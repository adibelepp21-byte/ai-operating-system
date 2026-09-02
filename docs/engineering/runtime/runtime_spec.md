# Engineering Specification — Runtime Subsystem

**Phase:** AIOS 2.5 — Engineering Specification. Implementation-neutral. **Immutable basis:** Architecture Freeze v1.0. No architecture/entity/class/API/database/protocol/message-format is added.
**Confidence:** **[E]** ratified/frozen · **[A]** engineering abstraction · **[O]** open / Architect reserved.

## 1. Purpose
[E] Runtime hosts Agent Instances — each Instance instantiates exactly one Agent Definition and is hosted by exactly one Runtime (Freeze INV-3). [A] It binds a definition into execution and drives governed action, a facility rather than an actor.

## 2. Responsibilities
[E] Host/create Agent Instances (INV-3). [A] Drive Workflow-governed execution; ensure each Instance action yields exactly one Trace (INV-4); keep resumable execution state distinct from the immutable Trace.

## 3. Owned Data
[A] Transient hosting/binding state for live Instances; owned centrally (Domain Model §5). [E] Owns no Knowledge; owns no Trace record (Trace is unowned — §5).

## 4. Lifecycle
[A] Invoked-to-host → drives Instance actions → concludes. [E] The Runtime is a facility; it authors no Trace of its own (OQ-2 interpretation).

## 5. Public Interfaces (conceptual only)
[A] Conceptually exposes: (a) host/instantiate an Agent Definition, (b) drive a Workflow's actions, (c) conclude an Instance. [E] Exposes **no** capability to bypass Workflow for agent collaboration (INV-13) or to reach external systems except via Tool (INV-12). *(No signatures/formats.)*

## 6. Internal Responsibilities
[A] Bind Definition→Instance; sequence actions; ensure Trace production per action; separate resumable state from Trace.

## 7. Allowed Dependencies
[E] Depends on Agent Definitions, Workflows, and the Tool boundary. [A] May rely on infrastructure facilities beneath it.

## 8. Forbidden Dependencies
[E] Must not own Knowledge (Freeze §5). [E] Must not become an independent traced actor (OQ-2). [E] Must not enable direct Instance↔Instance collaboration outside Workflow/Knowledge/scoped Memory (INV-13). [E] Must not hold a non-Tool external dependency (INV-12).

## 9. Trace Requirements
[E] Every hosted Agent-Instance action produces exactly one Trace record (INV-4); the Runtime's own hosting operations are audited through the action, not as independent Trace (OQ-2).

## 10. Governance Constraints
[E] Coordination occurs only via Workflow (INV-13); external access only via Tool (INV-12). [A] The Runtime enforces isolation, not policy — it does not decide governance.

## 11. Failure Behaviour
[E] Fail closed (PR-4): if Trace cannot be produced for an action, the action is not accountable and must not be treated as complete. [A] Stuck/hung execution is surfaced (detect), not silently resolved.

## 12. Extension Points
[A] Hosting/scheduling strategy and resumable-state handling are replaceable — none may weaken INV-4/5/12/13. [O] Runtime lifecycle states (e.g., a stuck state, historical evidence) are a candidate governed extension.

## 13. Future Evolution
[O] Scaling, isolation mechanisms, and scheduling are deferred (Freeze §10) and reserved to the Architect; the Native-Core Runtime (Phase 3) implements this spec.

## 14. Open Questions
[O] Runtime state model (which lifecycle states). [O] Resumable-state discipline distinct from Trace. [O] Runtime↔Workflow relationship ratification. **Discharged for the hosting direction:** this entry read *"Runtime↔Workflow relationship ratification (currently Inferred)"* until `FD-P9-001`, whose determination `ACT-CC-P9-001 §8.1` states as *"Runtime MAY depend on and access the Workflow capability for authorized execution hosting, without becoming the owner of Workflow semantics."* That direction is now ratified and no longer Inferred.

> **[D] What this discharge does and does not settle.** It ratifies **Runtime → Workflow as hosting**, which is the direction Blueprint §6 [A] and §7 above already permitted; the prior reservation is why the Runtime conformance suite had listed `workflow` as a forbidden edge, and that prohibition is corrected under the same authority. It does **not** make Runtime the owner of Workflow lifecycle, composition, coordination, or governance — `ACT-CC-P9-001 §8.3` states plainly that *"Hosting is not ownership"* — and it introduces no reverse edge: Workflow still models no Runtime relationship. The two neighbouring reservations are **untouched**: the Runtime state model stays [O] reserved, and resumable-state discipline stays [O] reserved, `ACT-CC-P9-001 §11.5` confirming that Phase 9 *"does not authorize a general resumability engine."*
