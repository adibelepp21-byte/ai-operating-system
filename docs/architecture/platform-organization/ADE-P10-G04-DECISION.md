# ADE-P10-G04 — Organization ↔ Runtime Representation Decision

> **ISSUED.** Architect decision, exercised under `APT-CD1.1-AA-001` on the
> surface opened by the Founder's decision-event package.

| Field | Value |
|---|---|
| **Event ID** | `ADE-P10-G04` |
| **Decision** | **OPTION A — the existing construct is the organizational representation** |
| **Architect** | Claude Code / Co-Founder |
| **Authority Ref** | `APT-CD1.1-AA-001` — Founder-appointed 2026-08-15, **ACTIVE**; scopes `§3.1 A`, `C`, `D` |
| **Effective From** | 2026-09-05 |
| **Issuance State** | **ISSUED** |

---

## 1. The question

> *Does the existing `Department` construct already serve as the organizational
> representation required by the architecture, or is an additional
> organizational representation/bridge required?*

## 2. Decision

**Option A.** The construct already serves as that representation — and the
premise of the question needs correcting before the answer makes sense.

**`Department` and `Platform Division` are not two constructs. They are one
entity under two names.** The Canonical Domain Model §2 states it directly:

> **Platform Division** — *"A bounded, semi-autonomous unit of accountability
> with its own domain vocabulary. Owns Capabilities and Agent Definitions.
> **Historical alias: Department** — see ADR-0010."*

`ADR-0010` — **Status: Approved**, Decision Owner Architect (Founder) — executed
the rename *"by bounded amendment rather than global migration"*, implementing
Founder decision **FD-6** as recorded at **`GDR-0020`**, across the Domain
Model's §1 entity-category table, §2 entity definitions, and **INV-1** and
**INV-2**. `ADR-0011` applied it to the Capability and Agent Definition rows and
the §3 lifecycle prose.

So the organizational representation is not missing and does not need building.
It is in the **frozen Domain Model spine**:

```text
| Spine | Organization, Platform Division, Capability |

Organization  owns    Platform Division
Organization  governs Platform Division
Capability    owned by exactly one Platform Division
Agent Def.    owned by exactly one Platform Division
```

`PD-01`…`PD-10` are Platform Divisions. The entity that represents them is
canonical, ratified, and already invariant-bearing.

## 3. Operative consequences

Per the event's Option A:

- **No additional organizational boundary is created.** The Native Core's eleven frozen subsystem boundaries stand untouched; **no twelfth is required, and none is sought.**
- **No organizational-runtime bridge is constructed.** The conceptual gap G-04 named does not exist as posed.
- **Future P10 operationalization may use the existing representation**, subject to applicable architecture.

## 4. What this decision does not do

It authorizes **no** P10 runtime construction, autonomous delegation engine, live
organizational state machine, or production orchestration. It amends no frozen
architecture — it recognises canon already ratified. It resolves **only** the
representation question, and reaches no other frontier (`§6` no cross-event
inference).

## 5. Correction — I had this wrong, repeatedly

Across `ACT-CC-P10-0`, `ACT-CC-P10-1` and `ACT-CC-FRONTIER-01` I stated that
`native_core`'s `Department` is *"a different entity"* from a Platform Division,
and built on it: that organizational runtime would need a twelfth boundary, that
no source↔runtime bridge existed, and that G-04 was an open architectural
question. **The claim was false.** `Department` is the recorded historical alias
of `Platform Division`, by an Approved ADR that predates every one of those
statements.

The error's shape is worth naming: I read the implementation's identifier
(`class Department`) as evidence of a distinct entity, without checking the
Domain Model's own alias record. **An implementation name is not an entity
identity** — the same discipline as `G-08`'s *reference count ≠ definition*,
applied to a name instead of a count, and I failed it while having recorded it.

Affected statements stand in committed artifacts and are corrected here rather
than rewritten there, preserving the record.

## 6. New finding — implementation lag, not architectural gap

`native_core/core/capability/ownership.py:98` still declares `class Department`,
and `DepartmentIdentity`, `DepartmentRef`, `InvalidDepartment`,
`UnknownDepartment`, `UngovernedCrossDepartmentDependency` carry the historical
alias throughout. `ADR-0010` chose *"bounded amendment rather than global
migration"*, so **this is expected and lawful, not a defect** — the alias is
recorded precisely so existing usages remain valid.

It is recorded as a **conformance observation**: the implementation names the
entity by its historical alias while the Domain Model names it canonically.
Whether to migrate is a separate architectural question with its own cost, and
**is not decided here**.

## 7. Evidence

| | Source | Bearing |
|---|---|---|
| Canonical Domain Model §2 | entity definition + alias record | **decisive** |
| Canonical Domain Model §1, §7 | Spine row; INV-1, INV-2 | representation is invariant-bearing |
| `ADR-0010` — **Approved** | the rename; FD-6; `GDR-0020` | authority for the alias |
| `ADR-0011` | applied to Capability / Agent Definition rows | scope of the rename |
| `AIOS_NATIVE_CORE_BLUEPRINT` :31 | *"exactly the eleven … no more"* | why no twelfth is sought |
| `ownership.py:98` | `class Department` | conformance observation §6 |
