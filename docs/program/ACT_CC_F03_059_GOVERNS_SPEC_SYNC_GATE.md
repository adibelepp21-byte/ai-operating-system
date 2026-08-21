# `ACT-CC-F03-059` — `governs` SPECIFICATION SYNCHRONIZATION GATE

> **DRAFT — PREPARED BY THE CO-FOUNDER OFFICE · AWAITING FOUNDER ISSUANCE.**
> Produced under `ACT-CC-F03-058 §12`. **This document confers no authority on
> itself.** Until issued, the specification lag `ACT-CC-F03-058 §6` expects
> remains open and construction stays unauthorized.

**Predecessor:** `ACT-CC-F03-058` · **Consumed:** `DEC-F03-058` (canonicalization complete)
**Type:** Specification Synchronization Gate · **Construction authority:** NONE
**Prepared:** 2026-08-21 · **Repository state:** `b66e923` + the authorized canonicalization

---

## §1 — State entering this gate

```text
governs semantics  RATIFIED (DEC-F03-057)  →  CANONICALIZED (DEC-F03-058)
                   →  SPECIFICATION SYNCHRONIZATION PENDING  →  CONSTRUCTION NOT AUTHORIZED
```

Canonical Domain Model §4.1 now carries the ratified definition and its five
preserved interpretations. `ACT-CC-F03-058 §6` expressly left `workflow_spec`,
`skill_spec` and `capability_spec` untouched and called the resulting lag
expected. **This gate asks which specifications, if any, must now catch up.**

## §2 — Assessment: what actually lags

**[E] Determined from source.** `governs` appears in **none** of
`capability_spec`, `agent_spec`, `skill_spec` or `workflow_spec`. The
canonicalization added terminology to the Domain Model and changed no
relationship, so **nothing in any specification is now contradicted.**

**[E] One specification does use the verb, and it corroborates the ratified
definition rather than conflicting with it.** `governance_spec §3`:

> **[E]** *"Governance **owns no execution entity**; it **governs** the
> Memory→Knowledge edge and authority (Mapping §5)."*

That is governance **without** ownership — ratified interpretation 2, stated
independently and predating the ratification. It is **not** a third `governs`
edge for canonicalization: Governance is a layer, not a Domain Model entity, and
the sentence does not appear in Domain Model §4's ratified relationship list.
`ACT-CC-F03-058 §5` forbids introducing additional `governs` relationships, and
none is proposed. **No change to `governance_spec` is needed or sought.**

*(An earlier draft of this section claimed `governs` appeared in no engineering
specification at all. That over-generalized from a four-file search; corrected
here before issuance.)*

| Spec | Contradicted by §4.1? | Candidate change |
|---|---|---|
| `capability_spec` | **No** | **[D]** record that a Capability *governs* the Agent Definitions implementing it, and that this creates no dependency — §7 today lists allowed dependencies without mentioning governance |
| `agent_spec` | **No** | **[D]** record that an Agent Definition's version is bound to the Capability contract version it implements — Domain Model §6 states it; `agent_spec §3` *Owned Data* does not |
| `skill_spec` · `workflow_spec` | **No** | **none** — neither entity participates in a `governs` edge |
| `department_spec` · `organization_spec` | **No** | **[D]** record that an Organization governs its Platform Divisions, semantically only, bounds undetermined |

**[A] The honest reading: none of these is *forced*.** No specification asserts
anything false. Each candidate is an *addition* that would make a specification
more complete, not a correction of an error. That distinction matters — this
program has previously corrected specifications that genuinely contradicted
canon, and this is not that case.

## §3 — **[D] The one that is more than cosmetic**

The `agent_spec` candidate is different in kind. Domain Model §6 states **[E]**:

> *"Its version is **bound to the Capability contract version it implements**."*

`AgentDefinition.implemented_capabilities` is `Tuple[str, ...]` — **capability
keys carrying no version**. So the ratified binding is unrepresented in the
implementation, and `agent_spec` does not state it either.

**Synchronizing `agent_spec` to say so would make the gap explicit and would make
the downstream construction target specification-backed.** Declining to
synchronize leaves the target resting on Domain Model §6 alone — which is
sufficient authority, but leaves the specification silent on a constraint its own
entity must satisfy.

**This is the decision this gate exists to take.**

## §4 — Boundaries for the executing Act

**May:** add to the specifications this gate's decision block authorizes, in the
minimum text required; cite `DEC-F03-057`/`DEC-F03-058` for traceability.

**Must not:** introduce any semantics beyond the five ratified interpretations ·
state concrete bounds for `Organization governs Platform Division` · add lifecycle
authority · create any package dependency or cross-boundary import · modify the
Domain Model, Freeze or Blueprint · modify source or tests · construct.

**Entity count 12; core boundaries 11; the 26 ratified edges unchanged.**

## §5 — Founder / Architect decision block

```text
DEC-F03-059 — governs Specification Synchronization

S-1  capability_spec — record the governance relation, no dependency
     [ ] AUTHORIZE      [ ] DECLINE

S-2  agent_spec — record the Capability-contract version binding (§3)
     [ ] AUTHORIZE      [ ] DECLINE

S-3  department_spec / organization_spec — record Organization governance,
     semantics only, bounds undetermined
     [ ] AUTHORIZE      [ ] DECLINE

S-4  skill_spec / workflow_spec
     [X] NO CHANGE — neither entity participates in a governs edge (pre-marked
         from evidence; countermand if the Architect disagrees)

Founder / Architect: ____________________
Date: ____________________
Confirmation: ____________________
```

**Declining all of S-1…S-3 is a coherent outcome**, not a failure: `§2` shows no
specification is contradicted. The construction target survives either way, since
Domain Model §6 already carries the binding.

## §6 — Successor sequence, not collapsible

```text
Specification Synchronization → Construction Gate → Construction → Verification
```

**The construction target, unchanged and still needing no new semantic choice:**
bind `AgentDefinition.implemented_capabilities` to Capability contract *versions*,
per Domain Model §6. Single boundary, `core/agent/` only. **Not authorized by
this gate.**

## §7 — Out of scope

T-12 · OB-01 · PD-02 activation · `DEC-AE04` · `DEC-REVOCATION` ·
`DEC-ADOPTION` · `RG-2` · `RG-3` · the `GDR-0025`/`-0026` count correction · the
concrete bounds of `Organization governs Platform Division`.
