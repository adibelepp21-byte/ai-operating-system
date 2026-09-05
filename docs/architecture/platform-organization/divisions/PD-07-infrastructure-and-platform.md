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
