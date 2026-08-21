# INV-15 Construction Record — Agent Definition specifies Skills and Workflows

**Executed under:** FOUNDER · `ACT-CC-F03-050` `DEC-F03-050 = OPTION A` · Moriarty · 21-08-2026
**Delivered as:** the `ACT-CC-F03-051` execution (`§19`)
**Result:** **CONSTRUCTION COMPLETE** · **STOP** (`§7`, `§20`)

---

## 1. Decision consumed

```text
DEC-F03-050 = OPTION A — AUTHORIZE construction INV-15
Scope: INV-15 — Agent Definition → specifies Skill/Workflow only.
Founder: Moriarty · Date: 21-08-2026 · Confirmation: Moriarty.
```

`§17` validity: one option checked · attribution · date · confirmation. **VALID.**

## 2. The Act's premise was tested, not assumed — and it very nearly failed

`§3` states INV-15 is *"unimplemented in the Agent Definition surface."* Testing
that against source produced a **finding that pointed the other way**, before a
fuller sweep resolved it.

**[E] The relationship is already modelled — twice, from the other side.**
`core/skill/declaration.py` and `core/workflow/declaration.py` each hold *"The
Skills/Workflows one Agent Definition specifies it is permitted to use"*, keyed
by `AgentDefinitionRef`, both citing Domain Model §4 and INV-15, both resolving
cardinality via **ADR-0007**. Verified empirically: an Agent Definition can
specify Skills, specify Workflows, specify none of either, and a repeated key
fails closed. Eleven existing conformance references to INV-15 already exist
across those two suites.

**[E] And `agent_spec §3 Owned Data` does not mention Skills or Workflows** — it
lists only Department ownership.

On that evidence alone the correct answer would have been *no construction
required*, as with T-3. **Two sources settle it the other way:**

| Source | Statement |
|---|---|
| **Canonical Domain Model §2** | **[E]** An Agent Definition is *"a stable, versioned specification: what a class of Agent does, **which Capabilities it implements**, **which Platform Division owns it**, **what behavior/permissions/Skills/Workflows it is allowed to use**, and what Runtime requirements it has."* |
| **Blueprint — Agent Package** | **[E]** *Responsibilities*: *"implement ≥1 Capability (INV-2); **may declare 0+ Skills/Workflows (INV-15)**; each Instance action → one Trace (INV-4)."* |

Domain Model §2 names **four** things an Agent Definition carries. Two were
already built onto this contract — `implemented_capabilities` (`-040`) and
`owning_department_key` (`-039`). The Skills/Workflows clause is the third, and
**Blueprint assigns that responsibility to the Agent package specifically.** The
Skill and Workflow modules hold the *owned entity's* view; this is the
Definition's own, and neither is derived from the other.

**The premise holds — on stronger evidence than the Act itself cited.**

## 3. Preconditions (`§11`)

INV-15 canonically ratified (4 Freeze references) · `agent_spec §2` sufficient ·
Agent boundary constraints unchanged · Skill and Workflow valid reference
targets · 0+ cardinality authoritative (INV-15 + ADR-0007) · T-2 Skill half
`[O]` in three places · `workflow_spec §14` finding intact · T-12 `[O]` ·
protected artifacts intact · `P7-F-2` untouched · core boundaries **11** ·
entity count **12** · tree clean.

## 4. Implementation

**`AgentDefinition.specified_skills` and `.specified_workflows`** — tuples of
plain keys. Two files changed, both in `native_core/core/agent/`.

- **Cardinality preserved exactly (`§5`).** Empty is valid for either or both —
  INV-15 and ADR-0007 are explicit that *"both empty declarations represent a
  valid architectural state."* **No** empty-guard was written, deliberately, in
  pointed contrast to `implemented_capabilities`, which requires ≥1 because
  INV-2 clause 2 says *at least one*. No maximum, and no uniqueness semantics
  beyond refusing a repeated key, which would make the declared set ambiguous —
  the same rule `SkillDeclaration` and `WorkflowDeclaration` already apply.
- **Plain keys (`§6`).** The Agent boundary's conformance forbids importing
  skill, workflow and capability; AST-verified that no such import exists.
- **Required, not defaulted.** Every other field of this contract is required and
  a guard asserts it, so an author writes `()` for "none" rather than omitting
  it. **[A] This is a construction-discipline choice, not a cardinality one** —
  INV-15 governs how many may be named, not whether the declaration is stated.
  It differs from `SkillDeclaration.skills`, which is defaulted; the divergence
  is recorded in the module so it is visible and reversible.
- **Only the Skills/Workflows clause was built.** Domain Model §2 names
  *behavior*, *permissions* and *Runtime requirements* in the same sentence;
  `§4` authorized none of them, and a test asserts they are absent.

### 4.1 A conformance guard was respected rather than amended

My first implementation factored the two declarations through a
`_validate_declaration` helper method. That tripped
`test_a_definition_is_descriptive_and_never_acts`, which asserts the class
carries **exactly** `__post_init__`. Rather than widen the guard to admit a
private helper — `§6`: *"no implementation detail may be promoted into
architectural authority merely because it is convenient"* — **the
implementation was rewritten** to inline the loop, and the guard stands
untouched. The class still has exactly one method. The boundary's no-assignment
rule was likewise respected: the duplicate check is a `len(set(...))`
comparison, not an accumulator.

## 5. Independent verification (`§12.6`) — before relying on new tests

Exercised directly in a fresh interpreter: both declarations empty · both
populated · a repeated skill key rejected · a repeated workflow key rejected ·
`None`, a list, an empty string and a non-text member each rejected for both
fields.

## 6. Conformance (`§12.7`) — updated toward cited authority

| Test | Change |
|---|---|
| `_definition` fixture | two arguments added |
| field-shape test | renamed to `test_it_carries_exactly_the_four_things_domain_model_2_names`; enumeration extended by two, docstring citing Domain Model §2 and naming what is deliberately absent |
| `test_every_field_is_required` | **extended** with a fourth arity case |
| halt-message guard | 9 → **12**, under its own *"one guard per declared field"* rule |

**Seven new tests** cover INV-15, including that zero-and-zero is valid, that no
maximum is imposed (50 keys accepted), and that behavior/permissions/runtime
requirements are **not** built.

**[E] The guard count was measured, not predicted.** Under `-040` I predicted 8
and the true count was 9; this time the count was read off the source before the
constant was written. Twelve is nine plus three apiece for the two new fields —
not a tuple, a non-text member, a duplicate — and **pointedly no empty guard**.

## 7. Verification (`§12.8`–`§12.10`)

| Check | Result |
|---|---|
| `native_core` | **584 OK** (was 577; +7) · 1 expected failure |
| `tools` · `bounded_exception` | **20 OK** · **29 OK** |
| Entity count · core boundaries | **12** · **11**, unchanged |
| Agent imports skill/workflow/capability | **NONE** — AST-verified |
| **T-2 Skill half** | `[O]` in three places — `capability_spec` **hash-identical** |
| **`workflow_spec §14` inconsistency** | untouched — `workflow_spec` **hash-identical** |
| **T-12** | `[O]` — Freeze **hash-identical** |
| Canonical artifacts | Domain Model, Freeze, Blueprint — **hash-identical** |
| Specifications | all three — **hash-identical** |
| Constitution · Finding Register | **hash-identical** |
| Governance mutations | **0** |
| `P7-F-2` / `GDR-0014` | untouched |

**[E] This construction changed no specification and no canonical artifact.**
The diff is two files plus this record.

## 8. Own-work disclosures

**1. My `-044` finding was under-evidenced.** It stated *"INV-15 is ratified and
unimplemented"* on the basis of inspecting the `AgentDefinition` dataclass alone.
It did not check whether the relationship was realized in the boundaries owning
the referenced entities — and it **was**, in `SkillDeclaration` and
`WorkflowDeclaration`. The conclusion survives, but only because Domain Model §2
and Blueprint's Agent-package responsibility supply a basis that finding never
cited. **The right answer was reached for a reason I had not established at the
time.**

**2. A defect in my own test code.** `test_malformed_declarations_fail_closed`
initially used the `_definition` helper, which coerces via `tuple(...)` — so a
`None` argument raised `TypeError` inside the helper and a list was silently
converted, masking exactly what the test existed to check. Rewritten to
construct `AgentDefinition` directly. Caught by the suite; disclosed, not
quietly fixed.

**3. Recorded in §4.1:** an implementation shape of mine collided with a
conformance guard, and the implementation gave way, not the guard.

## 9. Terminal state (`§20`)

**STOP.** Construction stopped at the authorized boundary. Nothing outside
INV-15 was touched.

**The three adjacent tracks `§18` records remain exactly where they were:**

| Track | State | Required authority |
|---|---|---|
| **A — T-2 Skill half** (`Capability↔Skill`) | `[O]` reserved | Architectural Decision / Ratification |
| **B — `workflow_spec §14`** (Workflow↔Skill classification) | `[D]` unresolved | Governance / Interpretation Decision |
| **C — T-12** (Knowledge admission model) | `[O]` Architect-reserved | Architectural Decision Track |

Also untouched: PD-02 activation · OB-01 · `DEC-AE04` · `DEC-REVOCATION` ·
`DEC-ADOPTION` · `RG-2` · `RG-3` · the `GDR-0025`/`-0026` count correction.

**Next frontier (`§12.12`):** no non-reserved engineering gap remains that this
program has identified. Every remaining item is a decision, not a build.
