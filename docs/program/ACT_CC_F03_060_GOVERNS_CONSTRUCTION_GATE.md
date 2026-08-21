# `ACT-CC-F03-060` — FOUNDER DECISION GATE: `governs` CONSTRUCTION AUTHORIZATION

> **DRAFT — PREPARED BY THE CO-FOUNDER OFFICE · AWAITING FOUNDER ISSUANCE.**
> Produced under `ACT-CC-F03-059 §15`, which states this successor **"must not be
> treated as automatically authorized"** by that Act. **It confers no authority
> on itself.** Construction remains unauthorized until this gate is issued and
> signed.

**Predecessor:** `ACT-CC-F03-059` · **Consumed:** `DEC-F03-059` (synchronization complete, zero mutations)
**Prepared:** 2026-08-21 · **Repository state:** `58ddfc5` + the synchronization record

---

## §1 — State entering this gate

```text
governs  DEFINED → RATIFIED (DEC-F03-057) → CANONICALIZED (DEC-F03-058)
         → SPECIFICATION SYNCHRONIZED (DEC-F03-059, zero mutations required)
         → CONSTRUCTION GATE  ← here
```

Every prior stage is complete. **This gate asks one question per target: may
construction begin, and on what exactly?**

---

## §2 — Construction Target A — `Capability governs Agent Definition`

### A.1 What the ratified semantics permit

Ratified interpretation **4** is explicit: this relationship **creates no package
dependency**. So the target is **not** an edge, a reference, a graph, or a
registry. `ACT-CC-F03-059 §7.1` names what it *is*:

> **[E] Domain Model §6:** an Agent Definition's *"version is **bound to the
> Capability contract version it implements**."*
>
> **[E] Actual:** `AgentDefinition.implemented_capabilities` is
> `Tuple[str, ...]` — capability **keys carrying no version**.

**The ratified constraint is unrepresented.** That is the whole of Target A.

### A.2 Proposed scope — **[P]**, minimal

Carry a Capability **contract version** alongside the key in
`implemented_capabilities`, so a Definition names *which version* of each
Capability contract it implements, as Domain Model §6 requires.

| | |
|---|---|
| Boundary | **`core/agent/` only** |
| New entity / boundary | **none** |
| Cross-boundary import | **none** — plain keys and versions, the convention already used for `owning_department_key` and the current `implemented_capabilities` |
| Package dependency | **none** — interpretation 4 preserved |
| Capability-side change | **none** |
| Lifecycle semantics | **none added** — interpretation 3 preserved |
| Conformance | the existing shape and enumeration guards will engage; both are legitimate authority changes if this gate authorizes the field change |

### A.3 **[D] One semantic question the Founder should settle, not me**

Domain Model §6 says the version is *"bound to"* the Capability contract version.
**It does not say what a binding failure is.** Two readings, and the difference is
material:

- **(a) Structural only.** The Definition *records* the contract version it
  implements. Nothing validates that the version exists. Minimal; consistent with
  interpretation 4 (no dependency, so the Capability side is not consulted).
- **(b) Reconciled.** A caller holding both sides checks that the recorded version
  matches a real Capability contract version — the pattern already used for INV-1,
  INV-2 clause 1 and INV-14, where neither boundary imports the other and a caller
  supplies the pairs.

**[A] (a) is the smaller step and cannot overreach; (b) matches this program's
established reconciliation pattern.** Both are defensible. **Choosing between them
is a semantic decision, so it is put here rather than taken.**

---

## §3 — Construction Target B — `Organization governs Platform Division`

### **[E] No concrete realization exists. Saying so, rather than inventing one.**

`ACT-CC-F03-059 §15` requires this be stated explicitly if true. **It is true.**

Ratified interpretation **5** holds that this edge is semantically canonicalized
while *"its concrete construction realization remains undefined and
unauthorized"*. The `-056` investigation found **ten of ten** `GOVERNS` properties
Unknown, and the only resident hint is Domain Model §2's *"semi-autonomous"* —
which presupposes a bounding party **without enumerating any bound**.

**There is nothing determinate to build.** A construction target requires a
constraint to enforce, and no ratified source supplies one for this edge.

**Recommended disposition: NO CONSTRUCTION TARGET.** Not deferred pending
analysis — analysis was done and came back empty. If concrete bounds are ever
wanted, they require a **new architectural definition track**, not a construction
gate.

---

## §4 — Boundaries for the executing Act

**Must not:** create any package dependency or cross-boundary import · add
lifecycle semantics · touch the Capability, Organization or Department boundaries ·
infer concrete bounds for Target B · modify the Domain Model, Freeze, Blueprint,
Constitution, Relationship Model or any specification · weaken a conformance test ·
construct anything for Target B.

**Entity count 12 · core boundaries 11 · the 26 ratified edges unchanged.**

---

## §5 — Founder decision block

```text
DEC-F03-060 — governs Construction Authorization

TARGET A — Capability governs Agent Definition (version binding)
  [ ] AUTHORIZE, structural only        (§2.3 reading (a))
  [ ] AUTHORIZE, with reconciliation    (§2.3 reading (b))
  [ ] DEFER

TARGET B — Organization governs Platform Division
  [ ] RECORD AS NO CONSTRUCTION TARGET  (recommended — §3)
  [ ] OPEN A NEW ARCHITECTURAL DEFINITION TRACK for its concrete bounds
  [ ] DEFER

Founder: ____________________
Date: ____________________
Confirmation: ____________________
```

Exactly one mark per target. **No default may be inferred for either.**

---

## §6 — Verification the executing Act must perform

Decision consumed exactly as recorded · the change confined to `core/agent/` ·
**no** cross-boundary import introduced, AST-verified · **no** Capability-side
change · **no** lifecycle semantics added · conformance tests updated only toward
their cited authority and never weakened · independent verification of the
binding before relying on new tests · full regression (`native_core`, `tools`,
`bounded_exception`) · canonical artifacts and specifications hash-identical ·
entity and boundary counts unchanged · governance mutations **0**.

---

## §7 — Out of scope

T-12 · OB-01 · PD-02 activation · `DEC-AE04` · `DEC-REVOCATION` ·
`DEC-ADOPTION` · `RG-2` · `RG-3` · the `GDR-0025`/`-0026` count correction.
