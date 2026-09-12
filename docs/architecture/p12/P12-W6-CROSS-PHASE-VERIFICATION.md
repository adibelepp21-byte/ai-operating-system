# P12-W6 — cross-phase verification by exercise · `F-5` closed

> **`P12 CONSTRUCTED = FALSE`.** A work-package increment is not a phase result,
> and `W6` is **not** complete — `§19`: *"P12-W6 tidak boleh dianggap selesai
> hanya karena unit tests individual hijau."*
>
> `historical rewrite = 0` · `native_core changes = 0` · `p11 changes = 0`.

---

## 1. The requirement, from the body

`§45`: *"W6 verifies P4–P11 as an integrated operating system. Verification must
test relationships, not only isolated components."*
`§48`: **"A relationship is not considered verified merely because both surfaces
exist."**

`§19` names `CROSS-PHASE CONTRACTS` in the minimum scope, and closes by refusing
green unit tests as evidence of completion. 1 875 passing tests establish that
components work; **none of them establishes that anything crossed a phase.**

---

## 2. Two taxonomies, not one

The canonical phase list is **not** the eleven Native Core boundaries:

```text
P4 Runtime · P5 Intelligence · P6 Knowledge · P7 Memory
P8 Tools   · P9 Workflow     · P10 Department · P11 Organization
```

`P5`, `P8`, `P10` and `P11` have no 1:1 boundary — `P8` is *Tools* where the
boundary is `skill`. `§47` says *"the actual graph governs"*, so phases are
resolved to **the evidence that would show them exercised**, never to a boundary
whose name looks similar.

---

## 3. Only execution-produced evidence is admissible

An import, a registry entry, a Capability record and a conformance test each
establish that a surface **exists**. The only evidence accepted here is a record
produced **by an execution**: a durable Trace record naming what an Agent
Instance actually used, or an observation published by a real run.

---

## 4. Result — measured, and not clean

| Phase | Status | Evidence |
|---|---|---|
| `P4` Runtime | **EXERCISED** | Trace names runtime `p12-w4-durability-proof` |
| `P5` Intelligence | **EXERCISED** | Trace authored by `engineering-intelligence-instance-001` |
| `P6` Knowledge | **NOT EXERCISED** | `knowledge_consumed` empty in every Trace record |
| `P7` Memory | **NOT EXERCISED** | `memory_consumed` empty in every Trace record |
| `P8` Tools | **EXERCISED** | `tools_used` `w4_delegation.py` · `skills_used` `artifact-conformance-verification` |
| `P9` Workflow | **EXERCISED** | workflow observation published |
| `P10` Department | **EXERCISED** | delegated actor that **authored a Trace record** |
| `P11` Organization | **EXERCISED** | organizational work runtime `p11-w1-runtime` observed |

```text
exercised 6 · not exercised 2 · unknown 0
exercised_only_by_a_demonstrator: ('P4', 'P9')
```

**`P6` Knowledge and `P7` Memory have never been *consumed* by any execution in
this repository.** Both boundaries are built, conformance-tested and consumed by
other boundaries in the import graph — and no Agent Instance has ever recorded
consuming knowledge or memory. That is the most substantive `W6` finding
available today, and it was invisible while verification meant unit tests.

> **Corrected under `ACT-CC-P12-F15-001`.** This sentence first read *"never been
> **crossed** by any execution"*, which overstates what was measured. A real
> runtime **provisions** `KnowledgeSubsystem` and `MemorySubsystem` on every run,
> including the resident W1 work path — so the boundaries *are* reached by real
> execution. What has never happened is **consumption**: `knowledge_consumed` and
> `memory_consumed` are empty in every Trace record. `PROVISIONED ≠ CONSUMED`,
> and the verifier measured consumption, which is what the Trace vocabulary
> records.

**`P4` and `P9` are flagged demonstrator-only.** Their crossings exist because
proofs made them, not because the system's work did. Reporting six-of-eight
without that qualifier would repeat `F-10` exactly, where a coverage figure
counted its own demonstrator.

---

## 5. Two defects in this module, both mine, both caught before commit

### `D-1` — my `P10` predicate was itself a `§48` violation

It returned `EXERCISED` because delegation **records** exist. A verifier built to
refuse *"both surfaces exist"* cannot accept *"a record exists"* one function
later. Corrected to require the **intersection**: an actor named as a delegation
recipient **that also authored a Trace record**. It still passes — genuinely, on
different evidence.

### `D-2` — the predicates could not be pointed at other evidence

They took the evidence root as a **default argument**, bound at import. Patching
the module attribute changed nothing, so the control proving *"existence is not
exercise"* could not actually run against an empty corpus — a test that cannot
isolate is the same failure as a guard that cannot see. Roots are now read at
call time, and that control passes against a genuinely empty evidence store: with
no execution records, **nothing** is reported exercised, while every boundary and
organization record still exists.

---

## 6. Verification

```text
native_core 801 OK (1 expected failure) · consumers 276 OK · tools 811 OK = 1888
   tools +13 — cross-phase exercise conformance
citation 214 documents / 1149 citations / 0 errors · stale-state 509 / 0
p11 changes 0 · native_core changes 0 · Native Core 11 · protected read 0
```

---

## 7. Frontier

`F-5` — *"no cross-region integration test surface"* — **closed**: the surface
exists, and its first honest output is that two canonical phases have never been
crossed.

| ID | Frontier | Status |
|---|---|---|
| `F-15` | `P6` Knowledge and `P7` Memory have no execution evidence | **OPEN — AUTHORIZED**, and now measured rather than suspected |
| `F-14` | two work paths still publish no observation | OPEN — non-blocking |
| `F-13` | self-model does not distinguish work from demonstration subjects | NARROWED — `W6` now reports that distinction where it matters |

**`W6` is not complete.** `§19` names thirteen scope items; this increment
addresses `CROSS-PHASE CONTRACTS` and leaves cross-PD interfaces, mutation,
regression and fresh-process verification unbuilt at the phase level.
