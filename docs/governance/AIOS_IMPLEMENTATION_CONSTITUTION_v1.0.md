# AIOS Implementation Constitution v1.0

**Phase:** AIOS 2.9 — Native Implementation Constitution (Final).
**What this document is** [A]: the **highest rule of all AIOS implementation.** From Phase 3 onward, every line of AIOS code is bound by this document.
**What this document is not** [E]: it is **not** architecture, **not** an engineering specification, **not** a technical design. It adds no source code, pseudo-code, API, framework, language, schema, protocol, or database design.
**Its sole function** [A]: to state **how implementation must obey** the Architecture Freeze and the Engineering Specifications. It **does not repeat** the Constitution and **does not repeat** the Architecture Freeze — it only governs conformance to them.
**Confidence tags:** **[E]** ratified / frozen basis · **[A]** governance abstraction · **[O]** open / Architect-reserved. No untagged conclusions.

---

## 1. Purpose

[A] This Implementation Constitution exists so that implementation can **never drift from, weaken, or silently reinterpret** the ratified architecture. Architecture is now frozen; before any code exists, the *rules that bind code to that architecture* must exist first.

[A] It guarantees conformance **by governance, not by goodwill.** Correct implementation is not left to the discipline or memory of whoever writes the code — it is a governed obligation with a defined review path and a fail-closed default.

[E] It is required because (a) the Architecture Freeze is ratified and immutable, (b) the Engineering Specifications and Native Core Blueprint are complete, and (c) Phase 3 (Native Core) would otherwise begin with no binding rule tying its code back to the frozen design.

## 2. Relationship to Architecture Freeze

[E] This document sits inside a fixed governance lineage. Each artifact is derived from, and constrained by, the one above it:

```
Architecture Freeze          (immutable — WHAT AIOS is)
        ↓
Engineering Specification     (per-subsystem responsibilities)
        ↓
Native Core Blueprint         (conceptual structure / boundaries)
        ↓
Implementation Constitution   (THIS document — HOW code must obey the above)
        ↓
Implementation                (Phase 3+ code — obeys this document)
```

[A] Reading the lineage:
- The **Architecture Freeze** is the supreme authority. It is immutable. Nothing below it may alter it.
- The **Engineering Specifications** detail each subsystem within the frozen architecture.
- The **Native Core Blueprint** expresses the conceptual boundaries and dependency directions.
- The **Implementation Constitution** binds implementation to all three above it. It never redefines them.
- **Implementation** obeys this Constitution, and through it, everything above.

[E] This document therefore introduces **no architectural content of its own.** Where it names an invariant, entity, boundary, or principle, it does so **by reference** to the frozen source, never by restating or amending it.

## 3. Implementation Principles

[A] Ten principles govern all AIOS implementation. Each is inherited by reference from the frozen architecture and the Principles Register; none is invented here.

1. **Architecture First** [E] — the frozen architecture is the authority; implementation realizes it and never improves upon or reinterprets it.
2. **Governance First** [E: §6.2 invariant 2] — where implementation touches a governance boundary, governance decides; automation and tooling may propose but never override.
3. **Trace First** [E: INV-4] — every accountable action produces its Trace; accountability is designed in, never bolted on.
4. **Memory Never Self-Promote** [E: INV-8] — Memory becomes Knowledge only through governed human review; no code path promotes automatically.
5. **Knowledge Is Governed** [E: INV-7/INV-8] — Knowledge is durable and changes only by governed addition, never by silent in-place edit.
6. **Human Authority Final** [E: §3.2; §6.2 invariant 2] — final authority over architectural and governance decisions rests with humans; delegation is bounded and documented.
7. **Fail Closed** [E: PR-4] — when conformance is uncertain, implementation does not proceed.
8. **Tool Boundary** [E: INV-12] — external dependency exists only at the Tool boundary; no other entity reaches outside AIOS.
9. **Immutable Trace** [E: INV-5/INV-6] — Trace is append-only and captured at write-time; it is never edited, deleted, or back-filled.
10. **Native AIOS Naming** [E] — implementation uses the Canonical Vocabulary; a name must never imply a capability the architecture forbids.

## 4. Implementation Rules

[A] Normative obligations on all implementation. **SHALL** = mandatory; **MUST NOT** = prohibited; **MAY** = permitted within bounds; **SHALL NEVER** = absolutely and permanently prohibited.

**Implementation SHALL:**
- [E] Trace back every implementation decision to the frozen invariant, entity, or boundary it satisfies.
- [E] Produce exactly one Trace record for each accountable Agent-Instance action (INV-4).
- [E] Confine all external / vendor coupling to the Tool boundary (INV-12).
- [E] Route every Memory→Knowledge transition through governed human review (INV-8).
- [E] Halt accountably when a precondition, authority, or conformance check is unmet (PR-4).

**Implementation MAY:**
- [A] Choose implementation-internal mechanism, ordering, and on-disk layout **within** the frozen rules and the Engineering Specifications.
- [E] Add new Tools, Skills, Workflows, and governed Capabilities at the sanctioned extension points (INV-9/10/12/15).

**Implementation MUST NOT:**
- [E] Introduce any dependency direction the frozen architecture does not permit (Freeze §6).
- [E] Let any non-Tool component hold an external dependency (INV-12).
- [E] Allow direct Agent-Instance-to-Agent-Instance collaboration outside Workflow, Knowledge, or scoped Memory (INV-13).
- [E] Absorb another subsystem's responsibility into a module (Single Responsibility).
- [E] Name or treat anything implementing Trace as a mere "log", "event", "callback", or "checkpoint"; or anything implementing Memory as "Knowledge".

**Implementation SHALL NEVER:**
- [E] Edit or delete a Trace record (INV-5).
- [E] Make Trace production conditional or optional (INV-4; §14.2).
- [E] Auto-promote Memory to Knowledge (INV-8).
- [E] Let automation override or bypass a governance boundary (§6.2 invariant 2).
- [E] Create an entity, subsystem, or boundary with no ratified basis, or rename a canonical entity.

## 5. Dependency Rules

[E] Implementation preserves the frozen dependency directions (Freeze §6; Blueprint §20): authority flows downward, execution flows downward, and Knowledge flows upward **only** through the single governed promotion gate (INV-8).

[E] Forbidden dependencies are forbidden **in code**: Trace depends on nothing above it; only the Tool boundary holds an external dependency (INV-12); Memory never writes Trace (INV-5); execution never writes Knowledge except via promotion (INV-8); the core dependency graph is acyclic.

[A] Any dependency the frozen architecture does not permit is a governance violation, not a design trade-off — it fails closed regardless of convenience or performance benefit.

## 6. Extension Rules

[E] Extension happens **within** frozen rules. A new module is admissible only when it maps to a ratified subsystem or entity and introduces no forbidden dependency, no external coupling outside Tool, and no new governance boundary.

[E] Sanctioned extension points: new **Tools** (external capability, INV-12), new **Skills / Workflows** (INV-15), new governed **Capabilities** (INV-9/10), and new detect-only evaluation signals (PR-3).

[E] Any extension that would require changing a frozen invariant, entity, or boundary is **out of bounds** until governance amends the architecture (Freeze §9). [O] Reserved concepts (Freeze §10) enter only by governed ratification.

## 7. Evolution Rules

[A] AIOS grows by **governed addition, not breaking change.** New capability is added at the boundaries; frozen contracts are not altered to accommodate it.

[E] Evolution is additive and forward: Trace records are never versioned by mutation (INV-5); Knowledge changes only by new governed versions, never in-place edit (INV-8); a version change may never weaken a frozen invariant.

[E] This Implementation Constitution may itself be amended **only** by governance (Constitution §3), never by implementation. [O] Amendments are reserved to the Architect.

## 8. Change Management

[E] Every change is classified by the authority it requires, and routed accordingly:

| Change touches… | Requires |
|---|---|
| Implementation only, within frozen rules and Specs | **Governed implementation review** (§9) — human review; automation proposes only. |
| A frozen architectural item (entity, invariant, layer, boundary, relationship) | **Architecture Review + ADR** under the Constitution's Decision-Making Process (§3). |
| The Canonical Domain Model | **Architect Approval — non-delegable** (§3.2; INV-10). |

[E] Misclassifying an architectural change as an implementation change is itself a violation. [E] Where the required authority is unclear, the change **fails closed** (PR-4) until governance resolves it.

## 9. Implementation Review Checklist

[A] A change is not valid code until **all** items hold (else Fail Closed):

- [ ] Cites the frozen invariant(s), entity, or boundary it satisfies.
- [ ] Introduces no forbidden dependency or import (§5).
- [ ] Confines all external coupling to the Tool boundary (INV-12).
- [ ] Produces exactly one Trace per accountable action; never makes Trace optional (INV-4).
- [ ] Never edits, deletes, or back-fills Trace (INV-5/6).
- [ ] Never auto-promotes Memory to Knowledge (INV-8).
- [ ] Permits no agent-to-agent collaboration outside Workflow / Knowledge / scoped Memory (INV-13).
- [ ] Keeps each module to a single frozen responsibility.
- [ ] Uses canonical vocabulary; carries no false-cognate name (§3.10).
- [ ] Correctly classified and routed to the right authority (§8).
- [ ] Passed governed human review; automation only proposed.
- [ ] Modifies no prior canonical or frozen document.

## 10. Conformance Requirements

[A] Implementation is judged conformant to the Architecture Freeze on two gates, **both** of which must pass:

- **Architectural conformance** [E] — the affected invariants, entity boundaries, ownership, and dependency directions are cited and shown to hold. A change that violates any invariant is non-conformant **by definition** and fails closed.
- **Implementation conformance** [E] — the change satisfies this Constitution's rules (§4–§8) and the relevant Engineering Specification, including its forbidden-dependency and Trace requirements.

[A] Conformance is a **precondition for merge**, not a later audit. [E] Verification is by governed human review; automation may detect and propose but may not approve (PR-3; §6.2 invariant 2).

## 11. Non Goals

[E] This document explicitly does **not**:

- Define or redefine any architecture, entity, invariant, layer, relationship, or boundary (that is frozen — Freeze).
- Specify subsystem behavior (that is the Engineering Specifications).
- Produce source code, pseudo-code, API, interface, framework choice, language choice, schema, protocol, or database design.
- Repeat the content of the Constitution or the Architecture Freeze.
- Decide any reserved or deferred concern (§12).
- Authorize or begin Phase 3.

[A] Its only goal is to govern **how** implementation obeys the frozen architecture and the Engineering Specifications.

## 12. Reserved Future Topics

[O] Deliberately **not** decided here; reserved to the Architect and later governed phases:

- On-disk layout, registry / manifest / bootstrap mechanisms.
- Version-identifier scheme; migration and deprecation workflow.
- Test framework and conformance-enforcement tooling (detect-only, PR-3).
- The deferred concerns (Identity, Authentication, Networking, Database implementation, Deployment, Scaling, Observability implementation — Freeze §10).
- The Inferred relationships (Blueprint §7/§14) and the Knowledge admission model (Freeze §10).
- Formal ratification of this Constitution and the synthesis chain into canon.

---

## Closing

[A] This Implementation Constitution binds all future AIOS code to the frozen architecture **by governance**: architecture is immutable; implementation obeys architecture; engineering obeys architecture; source code obeys engineering; and automation never overrides governance. Every future change has a defined authority, a conformance path, and a Fail-Closed default. [O] All reserved decisions, the enforcement mechanism, and the start of Phase 3 remain reserved to the Architect.

**No source code, pseudo-code, API, interface, framework, language, schema, protocol, or database design was produced. No architectural concept was invented; no canonical entity was renamed. The Architecture Freeze remains immutable. The Constitution, Canonical Domain Model, Principles Register, Architecture Freeze, Engineering Specifications, Native Core Blueprint, and all prior documents were not modified. This is an additive governance document only. Phase 3 has not begun.**
