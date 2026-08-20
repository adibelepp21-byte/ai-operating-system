# Phase 5 Construction Cycle — Status, Eligibility, Target, Construction

**Prepared under:** FOUNDER · `ACT-CC-F03-037 §8`–`§16`, `§22` · **Date:** 2026-08-20
**Predecessor:** `ACT-CC-F03-036` (Department realization — COMPLETE)
**Decision basis:** `DEC-PHASE5-SEMANTICS = OPTION B`, canonicalized at
`AIOS_PHASE5_SEMANTIC_RECONCILIATION_v1.0.md §6`

> **This artifact is not canonical architecture.** It records status, an
> eligibility assessment and an engineering result. It ratifies nothing.

---

## D-02. Phase 5 Status Reconciliation (`§8`)

### D-02.1 Occurrences of the decision identifier, classified

Repository-wide scan for `DEC-PHASE5-SEMANTICS` — **six** occurrences, all
in `docs/program/`. No occurrence exists anywhere else in the repository.

| # | Location | Text in substance | Class (`§8`) | Action |
|---|---|---|---|---|
| 1 | `AIOS_PHASE5_SEMANTIC_RECONCILIATION_v1.0.md:110` | *"= **OPEN — FOUNDER DECISION REQUIRED**"* | **A — governance status** | **RECONCILED.** Preserved verbatim as quoted provenance in the new §5; superseded by the canonical record in §6. |
| 2 | `…RECONCILIATION_v1.0.md:1` | document title | — | none |
| 3 | `…RECONCILIATION_v1.0.md:53` | §4 heading, "Founder Decision Package" | **B — historical** | unchanged |
| 4 | `AIOS_DEPARTMENT_DECISION_PACKAGE_v1.0.md:134` | *"unblocks category instantiation, **if** `DEC-PHASE5-SEMANTICS` also resolves"* | **B — historical** | unchanged. A conditional written before the decision; it asserts no status. |
| 5 | `AIOS_DEPARTMENT_DECISION_PACKAGE_v1.0.md:179` | *"…are independent of this decision and **are not resolved here**"* | **B — historical** | unchanged. Accurate then and now — that document did not resolve it. |
| 6 | `AIOS_DEPARTMENT_ARCHITECTURE_PROPOSAL_v0.1.md:115` | *"Related but **separate** … This proposal decides neither"* | **B — historical** | unchanged. Document carries `PROPOSED — NOT CANONICAL` and is superseded. |

**Class C — stale implementation status: none found for this decision.**

**[E]** No historical record was rewritten to remove evidence of the previous
OPEN state (`§8` final clause). The OPEN text survives verbatim, quoted, in the
artifact that issued it.

### D-02.2 Phase 5 status after canonicalization

| Item | Before | After |
|---|---|---|
| `DEC-PHASE5-SEMANTICS` | OPEN — Founder decision required | **CANONICAL — OPTION B** |
| Phase 5 construction interpretation | undetermined | work against the **existing ratified Capability architecture** and its Capability-category surface |
| Intelligence as an entity | not ratified | **still not ratified** — explicitly excluded by the decision |
| Planner / Scheduler / Orchestrator | not authorized | **still not authorized** (`§17`) |
| Architecture Freeze entity count | twelve | **twelve** |
| Native Core core-region boundaries | eleven | **eleven** |
| `capability_spec §13` Department blocker | discharged by `ACT-CC-F03-036` | discharged |
| PD-02 activation | not executed | **not executed** (`§20`) |

---

## D-03. Construction Eligibility Matrix (`§11`, `§22`)

Four conditions, all of which must pass: **Architecture RATIFIED · Specification
SUFFICIENT · Dependency SATISFIED · Construction Authority PRESENT.**

| # | Candidate target | Architecture | Spec | Dependency | Authority | Eligibility |
|---|---|---|---|---|---|---|
| **T-1** | **Ownership reconciliation — make INV-1 checkable across both representations** | **RATIFIED** — Capability + Freeze §4 Organization/Department | **SUFFICIENT** — INV-1, INV-10, INV-11, `capability_spec §1/2/7/10/11`, PR-3/PR-4 | **SATISFIED** — Department realization COMPLETE (`-036`) | **PRESENT** — Option B track; `§11`, `§12` | **ELIGIBLE** |
| T-2 | Capability↔Skill/Workflow composition | RATIFIED (entities) | **RESERVED** — `capability_spec §12` *"Inferred (reserved)"*, `§14` *"relationship ratification"* **[O]** | satisfied | **ABSENT** — Architect-reserved | **NOT ELIGIBLE** — escalation path, not construction |
| T-3 | Versioned-contract representation format | RATIFIED | **RESERVED** — `capability_spec §14` **[O]** *"no format defined here"* | satisfied | **ABSENT** — Architect-reserved | **NOT ELIGIBLE** |
| T-4 | Capability Catalog category instantiation | RATIFIED | sufficient | satisfied | **ABSENT** — assigning a category to an owning Department is an INV-1 ownership decision (governance data), and `OB-01` is unresolved | **CONDITIONALLY ELIGIBLE — blocked on ownership-assignment authority** |
| T-5 | Intelligence as an entity | **NOT RATIFIED** — 0 occurrences in Freeze and Domain Model | none | — | **EXCLUDED by `DEC-PHASE5-SEMANTICS`** | **NOT AUTHORIZED** |
| T-6 | Planner | **NOT RATIFIED** | none | — | **ABSENT** | **NOT AUTHORIZED** (`§17`) |
| T-7 | Scheduler | **NOT RATIFIED** | none | — | **ABSENT** | **NOT AUTHORIZED** (`§17`) |
| T-8 | Execution Orchestrator | **NOT RATIFIED** | none | — | **ABSENT** | **NOT AUTHORIZED** (`§17`) |

**[A]** T-6/T-7/T-8 appear in the Master Roadmap's **Phase 3** exit criteria.
Per `§17`/`§18` that is a historical planning scope and is **not** construction
authorization; the historical roadmap text was left intact.

---

## D-04. Next Construction Target — **T-1**

**Target.** Reconcile the two representations of Capability ownership so that
INV-1 is *checkable* rather than merely *asserted*.

**Rationale — the gap was created by the `-036` landing, and is real.** Before
realization, ownership existed only as `DepartmentRef`, an unverifiable string.
Realization added a second representation — `Department.owned_capabilities` —
and the two were never connected. Three defects were confirmed **empirically**,
not inferred:

| ID | Confirmed behaviour before the fix |
|---|---|
| **G-1** | `CapabilityGraph` accepts a Capability whose `department_key` names **no existing Department**. INV-1 says *exactly one*; zero passed. |
| **G-2** | Department `platform` claims `cap.b`; `cap.b` names `research`. `resolve()` silently returned `research`, `unresolved_ownership()` returned empty — **no query detected the contradiction.** |
| **G-3** | INV-10 decides "crosses Department ownership" by comparing unverified strings, so a **typo** (`platfrom`) silently became a cross-Department edge and demanded a governance record that the architecture does not require. |

**Dependency position.** Priority 1 — *unblock critical dependency*
(roadmap §7). Every downstream Phase-5 activity under Option B instantiates
Capabilities under Departments; an unverifiable ownership edge makes INV-1,
and the INV-10 check built on it, unsound.

**Expected outcome.** An ownership edge is treated as ownership only when both
sides agree; contradictions fail closed; a corpus can be surveyed without
halting.

**Architecture boundary.** `native_core/core/capability/` — the same
already-ratified boundary. **No new boundary. Core region stays at eleven.**

**Specification.** INV-1 (*"owned by exactly one Department"*), INV-10, INV-11,
`capability_spec §2/§7/§10/§11`, PR-3 (Detect Don't Decide), PR-4 (fail closed).
**[A]** Per `§15`, this requires **no** new invariant, entity, authority,
lifecycle or dependency semantic — INV-1 already says *exactly one*; the work is
making that determinable now that the fact is represented twice. **No
escalation is required.**

**Implementation scope.** `ownership.py`, `exceptions.py`, `__init__.py`, and
the ownership conformance tests. `graph.py` is **not** modified: its INV-10
logic is correct once the keys it compares are verified, and changing it was
not necessary to close the gap.

---

## D-05. Construction Report

**Implemented.**

- `exceptions.py` — `DisputedCapabilityOwnership`, the named failure mode for
  the two representations contradicting each other about one edge. Distinct
  from `ConflictingCapabilityOwnership` (two Departments claiming one
  Capability).
- `ownership.py` — `OwnershipGraph.resolve` now requires the named Department to
  **also claim** the Capability before the edge counts as ownership; it fails
  closed (PR-4) and names both sides in the message. Added
  `disputed_ownership()` and `unbacked_ownership_claims()` — corpus surveys that
  **report and never raise** (PR-3), so a reconciliation pass sees every
  contradiction rather than the first.
- `__init__.py` — 22 exports (was 21).
- `tests/test_ownership_conformance.py` — `TestOwnershipEdgeAgreement`, 8 tests.

**Gap closure, verified empirically after the change.** G-2 now raises
`DisputedCapabilityOwnership` naming both `research` and `platform` and citing
INV-1. G-1 and G-3 are closed at the same point: an unverifiable owner is no
longer silently accepted as ownership, so a typo surfaces as an unresolved or
disputed edge rather than as a spurious cross-Department dependency. A fully
reconciled corpus reports nothing on all three queries.

**One conformance test updated, and why.**
`test_public_surface_is_exactly_the_declared_exports` is an enumeration guard
that fires whenever the public surface changes — its purpose is to force the
change to be declared, which is what happened here. Its expectation was extended
by one name with the authority written into its docstring: **INV-1 [E]** already
requires *"owned by exactly one Department"* and **`capability_spec §11` [E]**
already requires that an invalid ownership state fail closed. The new exception
**names an existing failure mode**; it introduces no invariant, entity, boundary,
lifecycle or governance semantic. **No test was weakened, and no test that
carries architectural evidence was touched** — in particular the eleven-boundary
test was not modified and passes.

**Regression.** `native_core` **537 OK** (1 expected failure — the `P7-F-2`
bounded exception admitted by `GDR-0014`, which expressly does not authorize its
repair) · `tools` **20 OK** · `bounded_exception` **29 OK**.

**External research.** **NOT USED.** The gap, its confirmation and its fix came
entirely from resident canonical sources and direct empirical probing of the
repository's own code. Nothing external was consulted, adapted or adopted, so
`§13`'s recording obligation has no entries.

## D-06. Architecture Escalation Package

**NOT PRODUCED — no genuine architecture gap was encountered.** T-2 and T-3 are
Architect-reserved and were left untouched rather than solved through
implementation (`§14`). T-4's blocker is an authority question, not an
architecture gap.
