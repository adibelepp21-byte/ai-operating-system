# `DEC-F03-057` — `governs` Semantics · Ratification Record

**Recorded under:** FOUNDER / ARCHITECT · `ACT-CC-F03-057 §8` · **Recording date:** 2026-08-21
**Decision:** **OPTION A — RATIFY**

> **SEMANTIC RATIFICATION ONLY.** `§5`: no canonical artifact, Domain Model,
> Freeze, Blueprint, specification, conformance test or source may be mutated,
> and no construction is authorized. **None was.** `§11` fixes the only valid
> resulting state: **GOVERNS SEMANTICS RATIFIED → CANONICALIZATION PENDING →
> CONSTRUCTION NOT AUTHORIZED.**

---

## 1. Decision (`§8.1`–`§8.3`)

```text
DEC-F03-057
[X] OPTION A — RATIFY
Founder / Architect: Moriarty · Date: 21-08-2026 · Confirmation: Moriarty
```

**Validity verified:** exactly one option selected · attribution present · date
present · confirmation present.

**[O]** Two blocks carry the selection and **concur**: `§6` marks
`[X] AUTHORIZE RATIFICATION`, and the FINAL block marks `[X] OPTION A — RATIFY`
with attribution, date and confirmation. `§7`'s triple-checkbox block is blank.
Because nothing conflicts and no second option is marked anywhere, `§8.11`'s stop
condition is **not** triggered — there is no ambiguity to infer past. Recorded.

## 2. Ratified definition — preserved verbatim (`§8.4`)

> **A governs B when A bounds the discretion exercised over B without possessing
> B. The owner retains the discretion to act; the governor constrains the
> conditions under which that discretion is valid.**

## 3. Ratified interpretations — all six

1. **`governs` is distinct from `owns`.**
2. **`governs` does not imply ownership.** A governor may govern an entity it does not own.
3. **`governs` does not independently confer lifecycle authority.** Lifecycle actions remain subject to the authority canonical architecture already establishes.
4. **`Capability governs Agent Definition` does not create a package dependency.** The constraint is represented as an architectural constraint on the **governed** Agent Definition. No `CapabilityRef`, no Capability import, no new dependency edge, no Capability state inside Agent Definition.
5. **`Organization governs Platform Division` is semantically defined, but its concrete construction realization is not authorized.** Its concrete bounds remain for later work and were **not invented**.
6. **No additional semantics may be inferred from this ratification alone.**

## 4. Ratified relation table — preserved verbatim (`§3.2`)

| Relation | Meaning |
|---|---|
| `owns` | ownership / possession responsibility over an entity |
| `governs` | authority to bound the discretion exercised over the governed entity |
| `governs ≠ owns` | governance does not imply ownership |
| `owns ≠ lifecycle authority` | ownership does not automatically confer lifecycle authority |
| `governs ≠ lifecycle authority` | governance does not by itself confer lifecycle authority |

## 5. Evidence basis, preserved (`§2`, `§8.4`)

The definition was derived in `ACT-CC-F03-056` from resident canonical evidence
only — principally **Domain Model §6**'s Agent Definition row, which names owner,
governor and the concrete bound in one ratified clause: *"created/deprecated at
**Platform Division discretion** **within Capability governance**. Its version is
**bound to the Capability contract version it implements**."* Corroborated by the
uniform `govern*` pattern across INV-8, INV-10 and INV-14, all denoting review,
approval or constraint — never possession. **No external semantic authority was
used**, then or now.

## 6. What this ratification does *not* settle (`§12`)

Each remains a separate question for its proper stage: the **concrete bounds** of
`Organization governs Platform Division` · the **canonical representation** of the
relationship · **specification wording** · **implementation shape** ·
**construction scope** · **verification obligations**.

## 7. Verification (`§8.5`–`§8.8`)

| Check | Result |
|---|---|
| Canonicalization performed | **none** |
| Specification synchronization performed | **none** |
| Source / test mutation | **0 files** |
| Construction performed | **none** |
| Canonical artifacts | Domain Model, Freeze, Blueprint, Relationship Model, Constitution, Finding Register — **hash-identical** |
| Governance registers mutated | **0** |
| `native_core` · `tools` · `bounded_exception` | **584** · **20** · **29 OK**, unchanged |
| Entity count · core boundaries | **12** · **11** |

## 8. Resulting state (`§11`)

> **GOVERNS SEMANTICS RATIFIED → CANONICALIZATION PENDING → CONSTRUCTION NOT AUTHORIZED**

**Construction is not authorized**, and this record does not report it as such.

## 9. Successor (`§8.9`, `§9`)

`ACT_CC_F03_058_GOVERNS_CANONICALIZATION_GATE.md` — prepared, **awaiting Founder
issuance**. The mandatory sequence `Canonicalization → Specification
Synchronization Gate → Specification Synchronization → Construction Gate →
Construction → Verification` **may not be collapsed** (`§9`).
