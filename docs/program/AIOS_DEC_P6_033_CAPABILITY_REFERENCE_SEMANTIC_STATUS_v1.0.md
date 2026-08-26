# `DEC-P6-033` — Agent → Capability Reference Semantic Status · Decision Record

**Identifier:** `DEC-P6-033` · **Predecessor:** `DEC-P6-032`
**Subject:** Agent → Capability reference semantic status at the **Execution Layer**
**Phase:** `P6-AES-01 — Agent Execution Semantics`
**Authority:** **Founder Reserved Authority** · **Decision Owner:** Founder / Moriarty
**Date:** 2026-08-26 · **Status:** **DECIDED**
**Recorded by:** Co-Founder office under `ACT-CC-P6-037` · **Recording authority:** program record — see §5

---

## 1. Decision

```
OPTION B — OPTIONAL
```

[E] The Agent → Capability reference is **OPTIONAL at the Execution Layer.**

## 2. Governing rule (verbatim, §8)

> *"The Agent → Capability reference is not a universal execution prerequisite.
> Its presence alone does not authorize capability invocation. Its semantic use
> is permitted only when an applicable canonical Execution contract explicitly
> defines that use."*

## 3. Boundaries the decision preserves

[E] **Definition ≠ Execution** (§9) — Definition-layer capability data does not determine execution behaviour; execution semantics may not be inferred from it.
[E] **Reference ≠ Invocation** (§10) — invocation authority requires an explicit canonical execution contract. Six things confer none: a reference existing · a capability being listed · a graph containing a relationship · ownership resolving · caller reconciliation succeeding · an implementation field being populated.
[E] **Specification ≠ Construction** (§11) — no capability invocation implementation, runtime change, execution machinery, Construction Target, Construction Act, frozen-architecture change or Constitution change is authorized.

## 4. Effect

```
Capability reference status   OPTIONAL — CANONICAL on persistence (§18)
Founder-reserved condition    RESOLVED
Readiness                     REASSESSMENT REQUIRED — not a promotion (§13)
Class H                       REASSESSMENT REQUIRED — not automatically OPEN,
                              not automatically construction-eligible (§14)
Construction                  NOT AUTHORIZED (§15)
Successor                     ACT-CC-P6-037 (§20)
```

[E] **§21 — the 13 evidence packages classified out of scope by `ACT-CC-P6-033` are not widened by this decision** and must not be staged because the semantic condition is resolved. Honoured: they remain untracked.

## 5. Recording boundary

[A] Filed as a **program record**, following the pattern of `AIOS_DEC_P6_032_…`, `AIOS_DEC_AGENT_FACTORY_INV2_CLAUSE2_…` and six others in `docs/program/`. **No Governance Decision Register entry is authorized by this decision and none was made** — `GDR-0028` was written under a specifically bounded instrument; nothing here grants comparable authority.

[A] Per §18, the status is **OPTIONAL — CANONICAL** from the commit that persists this record.

## 6. Consumption

[E] Consumed by `ACT-CC-P6-037`: specification reconciled at `agent_execution_semantics_spec.md` §18, with §2, §12 and §17.1 updated. Per §19 the choice is **not reopened**; a future material conflict is reported, never silently overridden.
