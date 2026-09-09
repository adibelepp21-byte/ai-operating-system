# Cross-PD Interface Registry

> **Required by:** `ACT-CC-AIOS-FULL-SYSTEM-RESOLUTION-AND-AUTONOMOUS-CONTINUATION-GATE-v1.0 §19`;
> candidate v2.0 `§21`. **Built 2026-09-09.** Previously required by the
> `P10–P13 Blueprint` and the `Gap Closure Roadmap` and **never built**.
>
> **This registry records evidenced interfaces only.** Where resident evidence
> establishes no interface, the row reads `UNKNOWN` and stays that way. An
> `UNKNOWN` here is a measurement, not an omission.

---

## 0. How a row gets in

A row requires a **declared dependency or relation in a division's own corpus**,
carried into this corpus with an `E-` identifier. **Co-occurrence is not an
edge.** Two divisions mentioning each other in prose does not create a row —
that test was run and rejected 41 mention-pairs that no declaration supports.

## 1. Evidenced edges — the complete set

**Five edges. Two source divisions. Eight divisions declare nothing.**

| # | Source PD | Target PD | Capability / domain | Interface | Owner | Consumer | Authority | Dependency | Lifecycle | Evidence | Verification |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `X-01` | **PD-03** Governance & Compliance | **PD-02** Architecture Office | Architecture | *not declared* | PD-02 | PD-03 | `PD-03 A1 §22` self-declaration | `PRIMARY DEPENDENCIES: Architecture` | governed | **`E-33`**, propagated `E-42` | **DECLARED — interface undefined** |
| `X-02` | **PD-03** | **PD-08** Security | Security | *not declared* | PD-08 | PD-03 | `PD-03 A1 §22` | `PRIMARY DEPENDENCIES: Security` | governed | **`E-33`**, `E-42` | **DECLARED — interface undefined** |
| `X-03` | **PD-03** | **PD-09** Quality & Evaluation | Quality | *not declared* | PD-09 | PD-03 | `PD-03 A1 §22` | `PRIMARY DEPENDENCIES: Quality` | governed | **`E-33`**, `E-42` | **DECLARED — interface undefined** |
| `X-04` | **PD-04** Knowledge & Intelligence | **PD-06** AI Engineering | AI Engineering | *not declared* | PD-06 | PD-04 | `PD-04 A1` self-declaration | `Primary Dependencies: AI Engineering` | governed | **`E-24`**, `E-42` | **DECLARED — interface undefined** |
| `X-05` | **PD-04** | **PD-05** Runtime & Execution | Runtime | *not declared* | PD-05 | PD-04 | `PD-04 A1` | `Primary Dependencies: Runtime` | governed | **`E-24`**, `E-42` | **DECLARED — interface undefined** |

**Every one of the five is `DECLARED — interface undefined`.** A declared
dependency names *what* a division depends on. **None of the five names an
interface, a contract, a version, or a governing mechanism** — which
`INV-9`/`INV-10` require for a governed cross-unit dependency.

## 2. What the registry measures about itself

| Measure | Value |
|---|---:|
| Divisions | 10 |
| Divisions declaring any dependency | **2** (PD-03, PD-04) |
| Divisions declaring none | **8** |
| Evidenced edges | **5** |
| Possible ordered pairs | 90 |
| Edge coverage | **5.6 %** |
| Edges with a defined interface | **0** |
| Edges with a version | **0** |
| Edges with a governing mechanism named | **0** |

## 3. The invariant this registry makes measurable

`Freeze §6`: *"Capability depends-on Capability — **governed, versioned**
(`INV-9`/`INV-10`); **forbidden**: silent/cross-Dept ungoverned."*

**All five evidenced edges are cross-unit dependencies with no governance
mechanism and no version recorded.** Under `INV-10` a silent cross-unit
dependency is forbidden.

**This is NOT reported as five invariant violations**, for a reason that must be
stated rather than assumed: `INV-9`/`INV-10` govern **Capability→Capability**
dependencies. These five are **division→domain** declarations. Whether a
division's declared domain dependency *is* a Capability dependency **is not
determinable from resident sources** — and `G-09` means the unit population
itself is undetermined.

```text
POSSIBLE INV-10 EXPOSURE — NOT ASSERTED
Determinable only after ADR-0029 settles the unit population.
```

**No violation is claimed, and none is ruled out.** Recording which it is would
require the decision `ADR-0029` reserves.

## 4. The eight silent divisions

`PD-01`, `PD-02`, `PD-05`, `PD-06`, `PD-07`, `PD-08`, `PD-09`, `PD-10` declare
**no** dependencies in resident evidence.

**That is a source state, not a finding of independence.** Six of the eight
appear only as *targets* of another division's declaration. `PD-01` and `PD-07`
appear in **no** evidenced edge in either direction — for `PD-07` this remains
its only relationship datum of any kind.

**Disposition:** `SOURCE-GAP`. The Volume 1 / Volume 2 corpora for these
divisions are non-resident (`ESC-C7-01`), and their declarations, if any, live
there. **Not recoverable in this repository.**

## 5. What this registry does not do

It does not infer an edge from a mention, invent an interface for a declared
dependency, assign ownership a division has not claimed, or convert
`DECLARED` into `VERIFIED`. **`DECLARED ≠ DEFINED ≠ VERIFIED ≠ OPERATIONAL.`**
