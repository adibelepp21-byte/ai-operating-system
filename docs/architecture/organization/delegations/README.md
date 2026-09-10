# Organizational Delegations

> **Phase 11 organizational layer.** Established by
> [`DP-01`](../../../governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md) `§3 W3`,
> shaped by [`DP-04`](../../p11/DP-04-P11-ORGANIZATIONAL-ENTITY-MODEL.md) `§8.3`,
> surfaced by [`DP-03`](../../p11/DP-03-P11-ORGANIZATIONAL-ARCHITECTURAL-SURFACE.md) `§8.2`.
>
> **This directory is not a Department.** It is excluded by name in
> `tools/organization_catalog.py`, because it carries a README with an H1 and
> would otherwise be read as one.

---

## The population is empty, and that is the record

**There are zero delegation records here.** The loader
(`tools/delegation_catalog.py`) reports `0`, its tests prove every defect class
can fire against fixtures, and nothing is pending.

This is deliberate. `DP-01 §3 W3` authorizes *construction* of delegation
records, tracking, boundaries and verification. It does not make me a delegator.
Writing a file that says *"Engineering delegates capability X to agent Y"* is
not a technical act — **it is an exercise of the authority being delegated**.
`DP-01 §3 W3` fixes that delegation *"does not create authority"* and *"does not
authorize itself"*; `DP-04 §8.3` forbids it to *"create authority that does not
already exist."* A record I authored would be a delegation whose only authority
source is the executor who wrote it.

The P10 ownership loader stood in the same position: it existed before
`FD-P10-003` authorized the population it would read. **Mechanism before
population is the correct order here; the reverse is authority manufactured by
writing it down.**

---

## Record shape

Fixed by `DP-04 §8.3` — not chosen here:

```text
AUTHORITY SOURCE → AUTHORIZED SCOPE → DELEGATED ACTOR / UNIT
                 → BOUNDARY → ACCOUNTABILITY → VERIFICATION
```

so that the organizational layer may state

```text
A delegates B
for capability/work X
within authority boundary Y
under accountability condition Z
```

**without introducing another Native Core subsystem.** The core region remains
at *"exactly the eleven frozen subsystem boundaries — no more"*
(Native Core Blueprint `§4`).

Each record is one `<key>.md` file with these sections:

| Section | Content | Cross-checked against |
|---|---|---|
| `## Authority Source` | Department key | must be an established Department |
| `## Authorized Scope` | Capability key | must be **owned by** the authority source |
| `## Delegated Actor` | Department or Agent Definition key | must exist in the population |
| `## Boundary` | prose | presence only |
| `## Accountability` | key of the unit that **remains** accountable | must **not** be the delegated actor |
| `## Verification` | link to the verification mechanism | link must resolve on disk |
| `## Authorizing Instrument` | link to the instrument that authorizes it | link must resolve on disk |

`## Authorizing Instrument` is **not a seventh concept.** `DP-04 §8.3` lists
what a delegation records; this section is how a record is made to obey
`DP-01 §3 W3`'s *"does not authorize itself"* — a clause that appears in `DP-01`
and **not** in `DP-04 §8.3`. Without it, a self-authorizing
delegation is not merely undetected — it is **unrepresentable**, so no check
could ever find one.

---

## What the checks enforce, and why each is structural

Every check compares **two independent statements**. None matches prose, so
none can be satisfied by wording.

**The two instruments word these prohibitions differently**, and the column
below names which one each quotation is taken from. They are not
interchangeable: `DP-01 §3 W3` is the only source of *"does not authorize
itself"*, and neither instrument contains the phrase *"does not transfer
ultimate accountability"* — `DP-04 §8.3` lists the bare item *"transfer ultimate
accountability"* under *"Delegation shall NOT"*.

| Defect | Clause it enforces | Source |
|---|---|---|
| `scope-not-owned` | *"does not create authority"* — a unit cannot delegate what it never held | `DP-01 §3 W3` |
| `authority-source-unknown` | *"does not expand constitutional authority"* — authority from nowhere | `DP-01 §3 W3` |
| `actor-unknown` | a boundary with no subject is not a boundary | structural |
| `self-delegation` | creates no boundary while presenting as one | structural |
| `accountability-transferred` | *"transfer ultimate accountability"* | `DP-04 §8.3` |
| `authorizing-instrument-unresolvable` | *"does not authorize itself"* | `DP-01 §3 W3` |
| `verification-unresolvable` | verification that points at nothing is not verification | structural |
| `missing-section` / `empty-section` | the shape `DP-04 §8.3` fixes, present in full | `DP-04 §8.3` |

**`scope-not-owned` is the load-bearing one.** It is the check that makes this
directory something other than a place to write claims: a delegation from
Engineering of a Capability that Platform owns fails, and it fails against the
ownership graph frozen in P10, not against anything asserted here.

---

## What delegation is not

`DP-04 §8.3`, its seven items verbatim. Delegation shall **not**
*"become Governance"*, *"become Ownership"*, *"become Execution"*, *"become a
replacement for authority"*, *"transfer ultimate accountability"*, *"create
authority that does not already exist"*, or *"expand constitutional or Founder
authority."*

`DP-01 §3 W3` states its own five, which are worded differently and include one
`DP-04 §8.3` does not carry — delegation *"does not create authority"*, *"does
not transfer ultimate Founder accountability"*, *"does not become Governance"*,
*"does not expand constitutional authority"*, *"does not authorize itself."*

And from the programme's standing distinctions:

```text
Governance ≠ Execution          Authority ≠ Ownership
Coordination ≠ Ownership        Compliance ≠ Operational Execution
Delegation ≠ Transfer of Ultimate Accountability
```
