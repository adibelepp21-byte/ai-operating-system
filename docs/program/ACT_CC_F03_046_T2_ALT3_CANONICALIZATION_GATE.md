# `ACT-CC-F03-046` — T-2 / ALT-3 CANONICALIZATION GATE: *Workflow realizes Capability*

> **DRAFT — PREPARED BY THE CO-FOUNDER OFFICE · AWAITING FOUNDER ISSUANCE.**
> Produced under `ACT-CC-F03-045 §14`/`§18`. **This document confers no authority
> on itself.** It is a **canonicalization** gate, not a construction Act:
> `ACT-CC-F03-045 §10` places canonicalization and specification synchronization
> *before* construction authorization, and *"no stage may be silently skipped."*

**Predecessor:** `ACT-CC-F03-045` · **Decision consumed:** `DEC-F03-045 = OPTION C — ALT-3`
**Prepared:** 2026-08-21 · **Repository state:** `999bbc5`, tree clean

---

## §1 — Selected architectural outcome (`§18.1`)

```text
Workflow  —realizes→  Capability
```

Founder-selected direction, not yet canonical. Skill receives **no** direct
Capability relationship under ALT-3; T-2 is therefore **half closed**, and
`skill_spec §14` **[O]** remains reserved.

## §2 — Canonicalization requirements (`§18.2`)

**[E] Each of these is a change to a frozen or Architect-reserved artifact, and
each is Founder/Architect-reserved. None is within Co-Founder authority.**

| # | Artifact | Change required | Authority |
|---|---|---|---|
| C-1 | **Canonical Domain Model §4** | Add the relationship `Workflow **realizes** Capability` to the ratified 24-entry list, which today contains no Capability↔Workflow edge | Founder / Architect |
| C-2 | **Architecture Freeze §10** | Partially discharge *"Inferred relationships — Capability↔Skill/Workflow"*: the Workflow half enters the freeze, the Skill half remains `[O]` | Architect (Freeze §10: *"awaits an Architect decision before it enters any freeze"*) |
| C-3 | **Blueprint §10 — Workflow Package** | Its *Allowed dependencies* read **[A]** *"executed by runtime; composes skill"* — capability is **excluded**. Either admit capability, or confirm that a key-only reference takes no dependency (see `§4`) | Architect |

**[E] Correction to my own prior analysis.** The `ACT-CC-F03-044` package stated
that ALT-3 *"does not require changing Blueprint §7's Capability package, since
the direction is Workflow → Capability."* That remains true — but it did **not**
examine Blueprint **§10**, the *Workflow* package, whose allowed-dependency list
also excludes capability. **C-3 was therefore missing from that package's cost
estimate for ALT-3.** Disclosed rather than quietly added. It does not change
ALT-3's relative ranking against ALT-2 (which needs Domain Model **and**
Blueprint **and** probably a new invariant), and no ranking was offered anyway.

**[A] Mitigating fact:** Blueprint §10's list is tagged **[A]** — an engineering
abstraction — whereas Blueprint §7's Capability list is **[E]**. An `[A]` list is
a weaker constraint than an `[E]` one, which may make C-3 lighter than C-1.
**That is an observation for the Architect, not a determination.**

## §3 — Specification changes (`§18.3`)

| Spec | Current | After canonicalization |
|---|---|---|
| `workflow_spec §7` | **[E]** *"…composes Skills; **realizes Capabilities (Inferred, reserved)**"* | the parenthetical is discharged; the clause stands as ratified |
| `workflow_spec §14` | **[O]** *"Workflow↔Capability/Skill and Runtime↔Workflow relationships (Inferred)"* | Workflow↔Capability resolved; **Workflow↔Skill and Runtime↔Workflow remain [O]** |
| `capability_spec §12`/`§14` | **[O]** *"Capability↔Skill/Workflow composition is currently Inferred"* | **partially** resolved — Workflow only |
| `skill_spec §14` | **[O]** | **unchanged — remains reserved** |

**[E] No specification may be edited before C-1/C-2 land.** `§9` of the governing
Act prohibits modifying `capability_spec`, `skill_spec`, `workflow_spec`, the
Domain Model and the Architecture Freeze under that Act, and `§10` fixes
canonicalization ahead of specification synchronization.

## §4 — Construction scope, **if** separately authorized (`§18.4`)

**[P] Proposed, not authorized.** Construction requires its own authorization
after C-1…C-3 and the specification synchronization above.

- **A key-only reference, following the boundary's own established convention.**
  `core/workflow/declaration.py` already carries `AgentDefinitionRef` — *"A stub
  carrying only the reference the declaration needs… this boundary does not
  import it"* — and cites `core/capability/`'s `DepartmentRef` as the pattern. A
  `CapabilityRef(capability_key, capability_version)` stub would follow it
  exactly, letting Workflow name the Capability it realizes **without importing
  the capability boundary**. This is the same structure used for INV-2 clauses 1
  and 2, and it is what would keep C-3 minimal.
- A realization declaration on the Workflow model, plus queries.
- Cardinality, ownership, lifecycle and validation semantics are **not proposed
  here**: `ACT-CC-F03-044 §6` forbids assuming them, and no resident source
  supplies them. They must come from the canonicalization, not from code.

## §5 — Conformance obligations (`§18.5`)

**[E] One existing conformance test directly asserts the reservation this
decision would lift:**

`native_core/core/workflow/tests/test_workflow_conformance.py:535`

```python
def test_capability_composition_is_not_modelled(self):
    """workflow_spec §7/§14 [O]: Workflow↔Capability is Inferred, not frozen."""
    self.assertNotIn("capability", " ".join(workflow_pkg.__all__).lower())
```

It cites `workflow_spec §7`/`§14` **[O]** as its authority. Under the standing
discipline it may be revisited **only if that authority has legitimately
changed** — that is, **only after C-1/C-2 and the `§3` specification
synchronization**, never merely to let an implementation pass. Until then the
test is correct and must keep passing.

Also engaged: `FORBIDDEN_BOUNDARIES` in the same file **includes `"capability"`**
— a key-only reference (`§4`) preserves it untouched — and
`test_public_surface_is_exactly_the_declared_exports`, which would need its
enumeration extended, as the analogous guards did in `-039` and `-040`.

`test_runtime_relationship_is_not_modelled` is **out of scope** and must be left
alone: Runtime↔Workflow remains `[O]`.

## §6 — Rollback and preservation constraints (`§18.6`)

Preserve unchanged unless separately authorized: Engineering Constitution ·
Finding Register · the **eleven**-boundary Native Core constraint · the existing
Agent-mediated path `Capability ←implements— Agent Definition —specifies→
Skill/Workflow` · all ratified Capability/Skill/Workflow relationships · every
Founder-reserved decision listed in `ACT-CC-F03-045 §2`.

**[E] Historical `[O]` records must not be rewritten to erase their prior state**
(`§15`). Freeze §10's Inferred-relationships entry is **partially** discharged,
not deleted: the Skill half, Runtime↔Workflow and Agent-Instance↔Skill/Knowledge
all remain, and the record must show the Workflow half moved while the others
stayed.

**Rollback:** C-1…C-3 are additive; nothing is removed. If canonicalization is
later reversed, the added Domain Model entry and the specification discharges
revert, and the key-only reference is deletable without touching any other
boundary — no other package would import it.

## §7 — What this gate asks

Whether to proceed to **canonicalization** C-1…C-3. It asks for **no
construction**, and construction remains unauthorized until a separate Act
grants it after canonicalization and specification synchronization are complete.
