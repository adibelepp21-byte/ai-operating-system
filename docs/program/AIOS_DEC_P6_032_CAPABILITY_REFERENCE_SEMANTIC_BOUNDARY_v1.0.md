# `DEC-P6-032` — Capability Reference Semantic Boundary Decision · Decision Record

**Identifier:** `DEC-P6-032`
**Subject:** Capability Reference Semantic Boundary — Definition layer vs. Execution layer
**Phase:** `P6-AES-01 — Agent Execution Semantics`
**Type:** Founder architectural boundary decision, issued directly
**Authority:** Founder / Architect
**Founder / Architect:** Moriarty.
**Date:** 2026-08-23
**Status:** **DECIDED**
**Recorded by:** Co-Founder office — Construction Phase, under scoped §3.2 delegation `DEL-T4.4-CF-001`
**Recording authority:** Program record only — see §6

---

## 1. Form of this instrument

[E] `DEC-P6-032` was issued **directly by the Founder**, not as the output of an
Act. There is no `ACT-CC-P6-032`.

[A] This is recorded precisely because it changes how the decision must be
filed. Every Phase-6 decision from `DEC-P6-029` onward has been the disposition
block of a numbered Act, and its record has lived inside that Act's package.
`DEC-P6-032` has no such parent. It is therefore filed as a **standalone
decision record**, following the repository's existing pattern for
directly-issued Founder decisions — `AIOS_DEC_AGENT_FACTORY_INV2_CLAUSE2_v1.0.md`,
`AIOS_DEC_AGENT_DEPT_OWNERSHIP_v1.0.md`, `AIOS_DEC_F03_045_T2_RATIFICATION_v1.0.md`
and six others in `docs/program/`.

[A] **Direct issuance is within Founder authority.** `DEC-P6-030` determination
10 constrains the issuance of *Acts* (*"`ACT-CC-P6-031` may be issued only as a
separate Founder-authorized readiness/remediation instrument"*); it does not
constrain the Founder from deciding directly. Nothing here required an Act.

---

## 2. Decision — recorded verbatim in substance

```
DEFER — EXECUTION-LAYER CAPABILITY REFERENCE REMAINS UNDECIDED
```

**The Founder confirms the following boundary:**

1. The Agent Definition layer **MAY** contain `implemented_capabilities` as a
   Definition-level capability declaration.
2. The existence of `implemented_capabilities` does **NOT** establish any
   semantic Capability reference at the Agent Execution layer.
3. No conclusion is authorized that Agent execution Capability reference is
   **REQUIRED**, **OPTIONAL**, or **PROHIBITED**.
4. The semantic relationship between Agent execution and Capability remains
   **Founder-controlled**.
5. **No implementation inference, existing field, test construction,
   `CapabilityGraph` primitive, `OwnershipGraph` primitive, or repository
   pattern may be used to select one of the three classifications.**
6. Capability invocation, Capability resolution, Capability binding, Agent
   Factory creation, bootstrap, registration, ownership resolution, or
   Capability execution remain **unauthorized** unless separately established by
   canonical authority.
7. The Definition-level `implemented_capabilities` decision does **not**
   authorize any Execution-level Capability behavior.
8. **No Construction Act may be prepared or executed** for the unresolved
   Execution-layer Capability reference solely on the basis of this decision.

### 2.1 Authority boundary

```
Construction Authority:       NONE
Mutation Authority:           NONE
Capability Binding Authority: NONE
Agent Factory Authority:      NONE
Commit Authority:             NONE
Synchronization Authority:    NONE
```

### 2.2 Readiness effect — six explicit non-effects

[E] This decision:

- does **NOT** make the Capability reference readiness condition **MET**;
- does **NOT** promote `P6-AES-01` to construction eligibility;
- does **NOT** create Class H;
- does **NOT** authorize Capability implementation;
- does **NOT** authorize Agent Factory construction;
- does **NOT** authorize Capability invocation or resolution.

[E] *"P6 readiness remains governed by the applicable readiness gate."*

### 2.3 Rationale — recorded

[E] *"The Definition layer and Execution layer represent different semantic
boundaries. A Definition may declare which Capability identities an Agent claims
to implement. This declaration does not, by itself, establish: runtime binding;
invocation semantics; resolution semantics; ownership semantics; authorization
semantics; lifecycle semantics; or execution participation semantics. Those
concerns require an explicit architectural decision."*

---

## 3. Relationship to prior findings — three ratifications and one bar

[A] `DEC-P6-032` engages three specific findings this office reported under
`ACT-CC-P6-031`. Recording the relationship precisely, because in each case the
decision does something different.

### 3.1 The layer distinction — RATIFIED

[A] `ACT-CC-P6-031 §4.1` reported, from source:

> `Agent DEFINITION layer` → Capability reference exists, by Founder decision
> (`DEC-AGENT-FACTORY-INV2-CLAUSE2 = OPTION A`); identity-only; caller-reconciled.
> `Agent EXECUTION layer` → nothing established; the decision is silent.

[A] Items 2 and 7 **ratify this as a governing boundary.** What this office
reported as a verification finding — *"treating the first as answering the second
would be a layer collapse"* — is now a standing rule.

[A] **One wording note.** Item 1 reads *"MAY contain"*; §4.1 recorded that the
field **does** exist and **was** authorized under `ACT-CC-F03-040`. Both are
true and neither displaces the other: item 1 states a permission, §4.1 stated a
fact about a prior decision. **Recorded rather than reconciled**, since a
permission and a historical authorization are different claims.

### 3.2 The graph primitives — BARRED AS SELECTORS

[A] `ACT-CC-P6-031 §5` surfaced that resolution primitives **do** exist in the
Capability boundary — `CapabilityGraph.implementers_of`,
`CapabilityGraph.unknown_implemented_capabilities`,
`OwnershipGraph.owner_of_agent_definition`,
`OwnershipGraph.resolve_agent_definitions` — all caller-mediated, taking
declarations as arguments, holding no Agent data.

[E] **Item 5 names both by name** and bars them, together with implementation
inference, existing fields, test construction and repository pattern, from being
used to select any of the three classifications.

[A] This is the decision responding to the finding: the primitives are real,
and their reality **may not be converted into a semantic selector.** Item 6
separately keeps *ownership resolution* itself unauthorized.

### 3.3 Readiness — RATIFIED

[A] `ACT-CC-P6-031 §10.1` reasoned that *"a deferral is a disposition, not a
resolution"*, and therefore held the Capability semantic condition **NOT MET**
despite `DEC-P6-031`.

[E] §2.2's first bullet states the same conclusion as a decision: this decision
*"does NOT make the Capability reference readiness condition MET."*

[A] **The reasoning is ratified by Founder act.** It was not adopted from this
office's finding — the finding and the decision are separately attributable, and
both are recorded here as such.

---

## 4. State after this decision

```
Phase:                       P6-AES-01 — FORMALLY ESTABLISHED
Classification:              CLASS C — FORMAL PHASE ESTABLISHED /
                             CONSTRUCTION DEFERRED
Readiness:                   NOT READY        (10 MET / 8 NOT MET — UNCHANGED)
Ladder position:             STATE A          (unchanged)

Capability self-execution:   FORBIDDEN BY CANON (Freeze §4)
Capability invocation:       UNAUTHORIZED
Capability resolution:       UNAUTHORIZED
Capability binding:          UNAUTHORIZED
Ownership resolution:        UNAUTHORIZED
Registration / bootstrap:    UNAUTHORIZED
Agent Factory:               UNAUTHORIZED

Capability reference —
  Definition layer:          MAY be declared; identity-only; caller-reconciled
  Execution layer:           UNDECIDED — Founder-controlled; REQUIRED / OPTIONAL /
                             PROHIBITED all unauthorized; no inference, field,
                             test, graph primitive or repository pattern may
                             select among them

Class H:                     EMPTY
Construction Target:         NONE ELIGIBLE
Construction Act:            MAY NOT BE PREPARED OR EXECUTED on this basis
Construction / Mutation /
  Commit / Synchronization /
  Capability Binding /
  Agent Factory Authority:   NONE

C-01 · P7-L-1 · P7-O-1 ·
  P7-O-2 · D-001…D-006:      PRESERVED
RU-5:                        OPEN — undischarged
Successor:                   NONE ASSIGNED
```

[E] **Repository state at recording** — verified, not asserted:

```
HEAD                       bb600ef = origin/claude/aios-genesis-planning-hmbvlc
native_core/               empty      tools/                empty
docs/architecture/         empty      docs/engineering/     empty
docs/constitution/         empty
docs/governance/           243 insertions / 0 deletions  (GDR-0028 only)
native_core                601 OK (expected failures = 1)
tools                       49 OK
```

---

## 5. What this record did not do

```
Source changes                    0
Canonical mutations               0
Governance Register mutations     0
participate() implementations     0
Capability execution primitives   0
Capability bindings created       0
Capability invocations created    0
Agent Factory created             0
Construction Acts prepared        0
Class H promotions                0
Founder decisions inferred        0
Readiness conditions promoted     0
Commits / pushes / syncs          0
Files created                     1   (this record)
```

[A] Item 8 of the decision bars **preparing** a Construction Act, not only
executing one. **None has been prepared.**

---

## 6. Recording boundary and persistence

[A] **No Governance Decision Register entry is authorized by this decision**, and
none was made. `GDR-0028` was written under a specific, bounded instrument
(`ACT-CC-P6-018` §13, *"Mutation Authority: BOUNDED — RATIFICATION RECORD
ONLY"*). Nothing in `DEC-P6-032` grants comparable authority, so this decision is
filed as a **program record** in `docs/program/` and the Register is untouched —
verified: its only diff remains the 243-insertion `GDR-0028` append.

[A] **Persistence.** `Commit Authority: NONE`. This record, like the four
decisions before it, exists **only in this container's working tree**:

```
GDR-0028                             UNCOMMITTED  (tracked file, 243 ins / 0 del)
DEC-P6-029 / P6-AES-01 package       UNTRACKED
DEC-P6-030 / P6-030 package          UNTRACKED
DEC-P6-031 / P6-031 package          UNTRACKED
DEC-P6-032 / this record             UNTRACKED
Persisted repository state           bb600ef
```

[A] **Five signed Founder decisions are now durable only in this session.**
Recorded as fact, not as a request. Persistence requires an explicit,
path-specific Founder authorization.

---

## 7. STOP

[A] This record created no Capability reference, binding, resolution,
invocation or execution surface; no Agent Factory, bootstrap or registration; no
`participate()` implementation; no Construction Act, prepared or executed. It
selected none of REQUIRED, OPTIONAL or PROHIBITED, and used no field, test,
graph primitive or repository pattern as a selector. It promoted no readiness
condition, created no Class H, mutated no canonical artifact, and inferred no
successor.

**`DEC-P6-032` recorded. STOP.**
