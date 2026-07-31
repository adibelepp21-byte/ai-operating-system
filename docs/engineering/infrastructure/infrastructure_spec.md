# Engineering Specification — Infrastructure Subsystem

**Phase:** AIOS 2.5 — Engineering Specification. Implementation-neutral. **Immutable basis:** Architecture Freeze v1.0. No architecture/entity/class/API/database/protocol/message-format is added.
**Confidence:** **[E]** ratified/frozen · **[A]** engineering abstraction · **[O]** open / Architect reserved.

## 1. Purpose
[E] Infrastructure provides facilities *beneath* the entities — storage under substrate, the execution substrate, and the **single external boundary (Tool)** — audited through the invoking actions, never as independent actors (Freeze §5; INV-12; OQ-2 interpretation).

## 2. Responsibilities
[E] Confine all external/vendor coupling to the Tool boundary (INV-12). [A] Provide persistence facilities under Trace/Memory/Knowledge; provide the execution substrate. [E] Own no governance and no Knowledge.

## 3. Owned Data
[A] Facility-level state (storage handles, substrate) — non-entity. [E] Tool holds the only direct external dependency (INV-12); owned centrally (Domain Model §5).

## 4. Lifecycle
[A] Facilities are provisioned, used within actions, and released — always subordinate to the invoking action. [E] Facilities author no independent Trace (OQ-2).

## 5. Public Interfaces (conceptual only)
[A] Conceptually exposes: (a) storage facilities to substrate subsystems, (b) the Tool boundary for external access, (c) the execution substrate to Runtime. [E] Exposes **no** external access outside Tool (INV-12) and **no** governance capability. *(No signatures/formats.)*

## 6. Internal Responsibilities
[A] Keep facilities beneath entities; ensure external coupling flows only through Tool; keep facilities audited through invoking actions.

## 7. Allowed Dependencies
[E] Used by Trace/Memory/Knowledge (storage), Runtime (substrate), and Agent Instances (Tool). [A] May integrate outward **only** as a Tool.

## 8. Forbidden Dependencies
[E] Any non-Tool entity holding an external dependency (INV-12). [E] Owning Knowledge (Freeze §5). [E] Becoming an independent traced actor (OQ-2).

## 9. Trace Requirements
[E] Facility operations are accountable through the Agent-Instance action that invokes them (INV-4), never as independent Trace (OQ-2).

## 10. Governance Constraints
[A] Infrastructure serves; it does not govern. [E] External access is bounded to Tool (INV-12); governance and Knowledge ownership are excluded here.

## 11. Failure Behaviour
[E] Fail closed (PR-4): a failed facility causes the invoking action to halt accountably; external failures surface through the Tool boundary, not silently.

## 12. Extension Points
[A] New Tools (external integrations) are the sanctioned extension for external capability. [O] Storage/substrate backends are replaceable beneath the entities.

## 13. Future Evolution
[O] **Reserved / deferred (Freeze §10):** Identity, Authentication, Networking, Database implementation, Deployment, Scaling, Observability implementation — each named as a boundary, **not defined**, reserved to the Architect.

## 14. Open Questions
[O] Which reserved concerns (Identity/Auth/Networking/Deployment/Scaling) ever become ratified entities. [O] Storage-facility discipline under substrate.
