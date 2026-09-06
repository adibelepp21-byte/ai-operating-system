# PD-07 — Infrastructure & Platform

> **Status: DERIVED.** Constructed under `FDE-P10-FRONTIER-02`, Decision A.
> Below the Established section is bounded derivation, **not canonical**.

| | |
|---|---|
| **CPID** | `PD-07` — permanent |
| **Established name** | Infrastructure & Platform |
| **Established domain** | Infrastructure / platform domain |
| **Primary construction target** | Foundational platform services |
| **Maturity** | EVIDENCE-READY → **CONSTRUCTED (derived)** |

---

## 1. Established (source constraint)

- Frozen `PD-02 C8:122` — ***"PD-07 tetap memiliki ownership atas Infrastructure"*** — PD-07 **retains** ownership over Infrastructure. A prose binding.
- Frozen `PD-02 A5:329` — `Infrastructure Execution │ **NONE** │ Infrastructure owner`.
- Frozen `PD-02 A3:121` — PD-02 may not *"memiliki infrastructure execution"*.
- Frozen `PD-02 A4:285` — domain label **Infrastructure**.

## 2. A constraint this division inherits from the ratified architecture

Infrastructure is one of the **eleven frozen core subsystem boundaries**, and the
corpus already carries a strong, independently-reviewed rule about what
infrastructure may be:

> *"**infrastructure facilities are never independent actors** — not for tracing,
> not for governance, not for authority"* — `AIOS_INFRASTRUCTURE_AUDITING_PRINCIPLE_REVIEW`,
> with three ratified consequences: facilities produce no independent Trace
> record, make no governance decision, and hold no authority.

**This bounds PD-07's construction in a way no other division is bounded.** The
division may own the Infrastructure *domain*; the facilities within it are
explicitly **not actors**. Any derived structure that gave infrastructure
facilities decision-making or authority would contradict a ratified review, so
none does.

## 3. Derived organizational structure

| Part | Derivation for PD-07 |
|---|---|
| **A — Identity & Mandate** | Infrastructure / platform domain; retains Infrastructure ownership; provides foundational platform services |
| **B — Organization** | Candidate decomposition: platform services · facility provision · operational substrate. **Derived** |
| **C — Governance** | Governed **by** others: facilities make no governance decisions. PD-07 as a division may hold domain ownership; its facilities hold none |
| **D — Operating** | Service provision lifecycle: provision → operate → observe → retire. **Derived** |
| **E — Performance** | Service availability and conformance. **Derived** |

## 4. The distinction that must not collapse here

```text
PD-07                     the division — may own a domain
infrastructure facility   never an independent actor (ratified)
```

`Provider ≠ actor`. A division owning a domain of non-actors is coherent; a
facility acquiring authority because its owning division has some is not.

## 5. Unresolved

Whether "Infrastructure & Platform" is one domain or two ("Platform" may denote
the Platform Organization itself, which would be a different and much larger
scope) — **UNKNOWN and material** · binding to the `infrastructure` frozen
subsystem · relationship to PD-05 where runtime meets substrate · what
"foundational platform services" enumerates.

## 6. Not constructed

No facility granted actor status, authority, or governance capacity. No binding
to `native_core/core/infrastructure/`. The Infrastructure/Platform scope
question left open. Nothing canonicalized or frozen.


---

## Model layer — what canon establishes for every Platform Division

**Integrated 2026-09-06, Cycle 25.** The four model artifacts in the parent
directory answer all ten construction dimensions **at model level**, from
canonical and frozen source. They apply to this division as to every other, and
**assign it nothing**.

| Established for every division | Source |
|---|---|
| Owns **exactly two** entity types — Capability (inv. 1) and Agent Definition (inv. 2), each *"exactly one Platform Division"* | `DIVISION-OWNERSHIP-MODEL.md` |
| Owns **none** of Skill, Workflow, Tool, Runtime (*"owned centrally"*) or Trace (*"owned by no one"*) | same |
| `home ≠ ownership ≠ privacy` for Knowledge; `accountable-for ≠ owns` for Agent Instance | same · `E-91` |
| Its **own creation, retirement and naming** are *"architectural decision, architect approval"* | `DIVISION-LIFECYCLE-AND-AUTHORITY-MODEL.md` |
| Its **one affirmative discretion**: Agent Definitions are *"created/deprecated at Platform Division discretion within Capability governance"* | same · `E-84` |
| `governs ≠ owns ≠ lifecycle authority` | `Domain Model §4` · `E-85` |
| Capability creation is *"intentionally… restricted to architect-approved decisions… not a gap"* | `DIVISION-CAPABILITY-ARCHITECTURE-EVOLUTION-MODEL.md` · `E-87` |
| The Spine is **three levels**, *"not to be deepened or bypassed without an architectural decision"* | `Domain Model §8` · `E-90` |
| Repository layout is a **projection** of the model — `correspondence ≠ ownership` | `IMPLEMENTATION-CORRESPONDENCE-MAP.md` · `E-90` |
| Performance follows the `E1`–`E10` chain, corroborated across two divisions; **`measurement ≠ authority`** | `DIVISION-OPERATION-AND-PERFORMANCE-MODEL.md` · `E-93` |
| Operation is a **position and shape**, domain-adapted — not common content | same · `E-94` |

**This changes nothing about this division's own content.** Per-division content
remains blocked at `G-01`/`ESC-C7-01`, and per-division **assignment** remains
reserved at `G-09`/`G-10`. `ACT-CC-P10-FINAL §26`: a division is **not** complete
because one dimension is.

### Specific to `PD-07`

- **The `§5` item *"binding to the `infrastructure` frozen subsystem"* is
  answered as far as authority allows.** `native_core/core/infrastructure/`
  exists (14 modules, 2,651 lines, layer 9). The relationship is **name
  correspondence, not ownership** — `Domain Model §8` places repository layout
  outside the model as a *projection* (`E-90`). **The binding itself remains
  unmade**, and would engage invariant 1 and `DEL §3.2` exclusions 9 and 10.
- **The *"Infrastructure & **Platform**"* scope question is not resolvable by
  constructing a `Platform` entity.** `Domain Model §9` makes
  *Product/Service/Platform/Ecosystem* *"exposure/maturity postures of a
  Capability, not new structural concepts."* The question stays open; one wrong
  way to close it is now excluded.
