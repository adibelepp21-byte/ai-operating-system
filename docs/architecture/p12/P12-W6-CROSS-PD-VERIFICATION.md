# P12-W6 — cross-PD interfaces · currency verified, interfaces not

> **Zero cross-PD interfaces are verified, and none can be** until an interface
> is defined. `P12 CONSTRUCTED = FALSE` · `E12 RATIFIED = FALSE` — nothing here
> depends on ratification and nothing approaches `F-16` or `F-17`.

---

## 1. The requirement, and what stops it

`§19` names `CROSS-PD INTERFACES` in W6's minimum scope. `§48`: *"A relationship
is not considered verified merely because both surfaces exist."*

`CROSS-PD-INTERFACE-REGISTRY.md` has been resident since 2026-09-09. Its five
evidenced edges each record:

```text
Interface:    not declared
Verification: DECLARED — interface undefined
```

**An undefined interface cannot be exercised**, so `§48`'s standard cannot be met
here by any amount of work. Two boundaries hold it there, both pre-existing and
both already on the record:

| Boundary | Basis |
|---|---|
| **SOURCE GAP** | eight divisions' Volume 1/2 corpora are non-resident (`ESC-C7-01`) — *"Not recoverable in this repository"* |
| **ARCHITECT-RESERVED** | `INV-10` applicability awaits `ADR-0029` / `ADP-P10-001` |

The registry already refuses to cross either: `POSSIBLE INV-10 EXPOSURE — NOT
ASSERTED`, and *"No violation is claimed, and none is ruled out."* **This
increment claims none either.**

---

## 2. Falsification, before concluding

| Hypothesis | Result |
|---|---|
| an interface has been defined since 2026-09-09 | **FALSIFIED** — 29 commits touched the corpus; the only near-hit is a P3 record stating *"No API, signature, Runtime assumption, or interface is defined here"* |
| the registry's evidence has decayed | **FALSIFIED** — `E-24`, `E-33`, `E-42` all still resolve in the Evidence Ledger |
| `§19`'s `CROSS-PD INTERFACES` is `§48`'s hybrid list | **FALSIFIED** — `§19` names PD interfaces explicitly and separately |
| implementation relationships could stand in for PD interfaces | **NOT PURSUED** — that would require a PD ↔ implementation assignment, which is `F-17`, and this Act does not approach it |

---

## 3. What *is* verifiable, and was

The registry's rows are the **only resident evidence** of these edges — the
divisions' own volumes are non-resident — so the edges cannot be independently
recomputed. What can be verified is the registry's **currency and internal
consistency**:

```text
evidenced edges                 CURRENT   recorded 5     measured 5
possible ordered pairs          CURRENT   recorded 90    measured 90    n(n-1)
edge coverage %                 CURRENT   recorded 5.6   measured 5.6
edges with a defined interface  CURRENT   recorded 0     measured 0
evidence identifiers resolve    CURRENT   3 cited        0 unresolved
division population             CURRENT   recorded 10    measured 10

checks 6 · current 6 · drifted 0 · interfaces_verified 0
```

**The registry is current.** That is not the same claim as the interfaces being
verified, and the module returns `interfaces_verified: 0` alongside the named
blocking boundaries so the two can never be read as one.

---

## 4. Six-of-six is what a checker reading nothing would report

So it is proved able to drift:

| Mutation | Result |
|---|---|
| remove an edge row | `evidenced edges` **DRIFTED** |
| give an edge a defined interface | `edges with a defined interface` **DRIFTED** |
| break the Evidence Ledger | `evidence identifiers resolve` **DRIFTED** |
| remove the registry | **UNAVAILABLE**, `current == 0` |

The second control matters most: **acquiring a defined interface is the single
change that would make cross-PD verification possible**, so the checker must
notice it the moment it happens rather than continue reporting a comfortable
zero.

---

## 5. What this does not convert

The registry's `§5`: it does not infer an edge from a mention, invent an
interface, assign unclaimed ownership, or convert `DECLARED` into `VERIFIED`.

**Nothing built on top of it does either.** Tests assert that no check claims an
`INV-10` violation, that none rules one out, and that `interfaces_verified`
stays `0`.

```text
DECLARED ≠ DEFINED ≠ VERIFIED ≠ OPERATIONAL
```

---

## 6. Verification

```text
native_core 801 OK (1 expected failure) · consumers 276 OK · tools 836 OK = 1913
citation 221 documents / 1165 citations / 0 errors · stale-state 514 / 0
   tools +11 — cross-PD currency conformance, including four mutation controls
fresh-process 8/8 reproduced · certified evidence changes 0 · protected read 0
Native Core 11 · historical rewrite 0
```

## 7. `W6` scope after this increment

```text
CROSS-PHASE CONTRACTS   addressed
FRESH PROCESS           addressed
CROSS-PD INTERFACES     addressed as far as resident evidence permits —
                        currency verified; interfaces unverifiable, blocked
MUTATION · REGRESSION   per-module only, not phase level
```

`F-18` records the block: **cross-PD interface verification requires an interface
definition, which is Architect-reserved and source-blocked.** It is a boundary,
not a task, and it is neither `F-16` nor `F-17`.
