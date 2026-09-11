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

## The population, and what it is a projection of

**Three records: two `CURRENT` projections and one preserved `HISTORICAL`.**

```text
w3-current-engineering-intelligence-instance-001        CURRENT    → 4313bd2246124a94
w3-current-governance-artifact-integrity-instance-001   CURRENT    → 47eec2b87a284417
w4-engineering-intelligence-verification                HISTORICAL → fd1f1302b0224b97
```

**This directory was empty until `FD-P11-001`, and that emptiness was correct.**
`DP-01 §3 W3` authorizes *construction* of delegation records; it does not make
anyone a delegator. Writing *"Engineering delegates capability X to agent Y"* is
not a technical act — it is an exercise of the authority being delegated, and a
record whose only authority source is the executor who wrote it is precisely
what `DP-01 §3 W3`'s *"does not authorize itself"* forbids. So the mechanism was
built and the population left at `0`, the same order the P10 ownership loader
followed: mechanism before population, because the reverse is authority
manufactured by writing it down.

**`FD-P11-001 §4.1` created a delegator, and `§20` gave this directory a job:**

> W3 Delegation is the organizational mechanism through which the authorized
> Delegation record is represented and tracked.

Every record here now **projects a grant that already exists** in the operational
ledger. None of them creates authority, because none of them is the origin of
the grant it names.

---

## The ledger owns the delegation; this directory owns a view of it

```text
AUTHORIZED DELEGATION → OPERATIONAL LEDGER   identity · lifecycle · provenance
                              ↓
                       RECONCILIATION        tools/delegation_reconciliation.py
                              ↓
                W3 ORGANIZATIONAL REPRESENTATION   these records
```

Which layer owns what was **read off the resident implementation, not chosen**.
`W4DelegationRegistry.issue()` is the only place a `delegation_id` comes into
existence; `revoke()` is the only `ACTIVE → REVOKED` transition; the grant
carries its own `AuthorityProvenance`. A record in this directory carries none
of those. **So W3 never states a delegation status** — it states which grant it
represents and what the record is *for*, and the lifecycle is read from the
ledger on every check.

| Section | Says | Owned by |
|---|---|---|
| `## Operational Grant` | the `delegation_id` this record represents | ledger |
| `## Representation` | `CURRENT` or `HISTORICAL` — the role of the **record** | this directory |

`CURRENT` records are **generated** by `tools/delegation_reconciliation.py` and
rewritten on rotation. `HISTORICAL` records are written by hand and **never
modified by the tool** — `ACT-CC-P11-013 §16`: *"Historical records must not be
destroyed merely to achieve apparent consistency."*

---

## Why this section replaced one that said the opposite

Until `ACT-CC-P11-013` this README stated *"There are zero delegation records
here"* and *"The population is empty, and that is the record."* One record had
existed since the first W4 execution.

It went stale by the same mechanism the record itself did. Each proof run calls
`_revoke_stale_grants()`, withdraws the previous grant and mints a successor —
so the one W3 record ended up naming a **revoked** grant while two live grants
had no representation at all, and `tools/delegation_catalog.py` reported
`defects: 0` throughout, truthfully, because **all eleven of its checks compare a
record against the organizational population and none of them looks at the
ledger.** `defects: 0` was a true report from a checker that could not see the
thing that was wrong.

The reconciliation exists so that this class of drift is detectable rather than
narrated. Its defect classes are below.

---

## Reconciliation defects — `tools/delegation_reconciliation.py`

| Defect | Condition | Clause |
|---|---|---|
| `unrepresented-active-grant` | ledger `ACTIVE`, no `CURRENT` record | `§9` |
| `stale-active-claim` | `CURRENT` record, grant not `ACTIVE` | `§10` |
| `unknown-grant` | record names a grant no ledger holds | `§11` |
| `grant-reference-missing` | record names no grant at all | `§7` |
| `invalid-representation-role` | role absent or not `CURRENT`/`HISTORICAL` | `§20` |
| `duplicate-representation` | two `CURRENT` records for one grant | `§4.3` |
| `history-claims-live-grant` | `HISTORICAL` record of an `ACTIVE` grant | `§10` |
| `provenance-mismatch` | record contradicts the grant it names | `§12` |

**`unrepresented-active-grant` is the load-bearing one**, and it is the only
check whose subject is the *ledger* rather than a record — the direction nothing
was looking in. A record that does not exist cannot be inspected into
existence, so the check has to start from the grant.

**Lifecycle is derived, never stored here.** `ACTIVE` and `REVOKED` are the only
statuses the ledger writes. `SUPERSEDED` is a `REVOKED` grant named in an
evidence record's `superseded_grants`; `INVALID` is a grant whose authority
record no longer resolves; `MISSING` is referenced-but-absent; `UNKNOWN` is a
ledger file that will not parse — corruption, which is not absence.

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
