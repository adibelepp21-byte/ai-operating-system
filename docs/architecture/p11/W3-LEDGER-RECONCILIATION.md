# W3 Delegation ↔ Operational Ledger Reconciliation

> **Executed under `ACT-CC-P11-013`** — 2026-09-11. An **authorized construction
> Act**, narrow to one frontier: the relation `ACT-CC-P11-012` proved missing.
>
> `P11 AUTHORIZED = TRUE` · `E11 RATIFIED = FALSE` · Native Core = **11** ·
> protected packages = **13 untracked, UNTOUCHED** · no new entity, no new
> subsystem, no new Agent Instance, no new consumer, no new authority.

---

## A. Executive result

**The gap is closed, and closing it exposed two controls that had been passing
for reasons unrelated to their claims.**

```text
BEFORE (ACT-CC-P11-012)          AFTER (measured, this Act)
  ACTIVE grants        : 2         ACTIVE grants          : 2
  W3 active repr.      : 0         W3 active repr.        : 2
  W3 stale references  : 1         W3 stale references    : 0
  reconciliation ctrls : 0         reconciliation defects : 8 classes, 44 tests
                                   W3 records             : 3  (2 CURRENT, 1 HISTORICAL)
                                   ledger grants          : 13 (2 ACTIVE, 9 REVOKED, 2 SUPERSEDED)
```

`§34` warns not to assume the expected numbers hold. They did not: the ledger
grew from 12 grants to 13 and the live W1 grant changed identity, because this
Act ran the W1 proof for real to prove that rotation now carries the projection
with it.

---

## B. Architecture

### The direction was read off the implementation, not chosen

`W4DelegationRegistry.issue()` is the only place a `delegation_id` comes into
existence; `revoke()` is the only `ACTIVE → REVOKED` transition; the grant
carries its own `AuthorityProvenance`. A W3 record carries none of those. The
ledger therefore owns identity, lifecycle and provenance, and W3 is a
**projection** — `§5`'s desired shape, established by evidence rather than
preference:

```text
AUTHORIZED DELEGATION → OPERATIONAL LEDGER   identity · lifecycle · provenance
                              ↓
                       RECONCILIATION        tools/delegation_reconciliation.py
                              ↓
                W3 ORGANIZATIONAL REPRESENTATION
```

**`§6` — one canonical delegation.** The module holds no grants, issues none,
and can change no `status`. That is asserted by AST over its own source: it
references no `W4DelegationRegistry`, no `AgentInstanceRegistry`, no `uuid`, no
`issue`, no `revoke`.

### Two sections, and why neither is a new concept (`§7`, `§28`)

| Section | Says | Owned by |
|---|---|---|
| `## Operational Grant` | the `delegation_id` this record represents | **ledger** |
| `## Representation` | `CURRENT` or `HISTORICAL` — the role of the **record** | W3 |

`§7` forbids minting an identifier to make reconciliation easier. None was
minted: `delegation_id` already existed and already appeared in the hand-written
record — inside a blockquote sentence, where the only way to recover it was to
pattern-match sixteen hex characters out of English prose. The section gives an
existing identifier a declared home, which is what turns *"which grant does this
record represent?"* into a question with an answer.

`## Representation` is deliberately **not a status**. `§5` forbids creating W3
status authority when the ledger owns lifecycle, so W3 never writes `ACTIVE` or
`REVOKED`. It states what the record is *for*; the lifecycle it is checked
against is re-read from the ledger on every run.

### Alternatives considered and rejected

| Alternative | Why rejected |
|---|---|
| Host reconciliation in `delegation_catalog.py` | Its checks resolve records against the organizational **population**; reconciliation resolves them against the **ledger**. Folding one in would make the organizational layer depend on operational state it does not own. |
| Host it in `w4_continuity.py` | Mirror objection: that module is W5, and W5 would then own W3 correctness. |
| A new consumer | `§27` — a module under `tools/` is not a consumer, and no consumer was necessary. Convenience would not have been sufficient. |
| One W3 file per grant, so each rotation leaves a `HISTORICAL` record | A **second store of the same facts** — the duplicate delegation model `§6` forbids, in the shape it is easiest to build by accident. The ledger already keeps every grant it ever issued. |
| Parse the grant id out of the existing prose | Substring reasoning as an architecture. Four defects in this programme have come from exactly that. |
| Disable stale-grant revocation | `§14` forbids it, and it would trade a tracking defect for the unbounded grant `FD-P11-001 §29` prohibits. |

---

## C. Engineering

**Created**

| File | What |
|---|---|
| `tools/delegation_reconciliation.py` | the relation: `read_ledger`, `read_projections`, `reconcile`, `project`, `project_all` |
| `tools/tests/test_delegation_reconciliation.py` | 44 tests — probes `A`–`F`, mutation, false-positive, idempotency, fresh-process, contract |
| `docs/.../delegations/w3-current-engineering-intelligence-instance-001.md` | generated `CURRENT` projection |
| `docs/.../delegations/w3-current-governance-artifact-integrity-instance-001.md` | generated `CURRENT` projection |

**Modified**

| File | What |
|---|---|
| `tools/delegation_catalog.py` | `INSTANCE_ROOTS` — read **every** operational root, not one |
| `tools/w4_first_run.py`, `tools/w1_coordination_run.py` | `project()` after rotation (`§14`, `§15`) |
| `docs/.../delegations/README.md` | the section asserting an empty population, replaced |
| `docs/.../w4-engineering-intelligence-verification.md` | classified `HISTORICAL`, grant named |
| `tools/tests/test_p11_integration_reconciliation.py` | one proxy control re-anchored |
| `tools/tests/test_plan_to_workflow_gate.py` | one proxy control re-anchored |

**Deleted**: none. `§16` — no historical record was destroyed.

---

## D. Reconciliation

### The eight defect classes (`§4.3`)

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

**`unrepresented-active-grant` is load-bearing, and it is the only check whose
subject is the ledger rather than a record.** That is the direction nothing was
looking in: a record that does not exist cannot be inspected into existence, so
the check has to start from the grant. Every one of the eleven pre-existing W3
checks starts from a record, which is why all eleven were green while both live
grants were unrepresented.

### Lifecycle, derived and never stored (`§8`)

`ACTIVE` and `REVOKED` are the only statuses the ledger writes. The rest are
derived from resident data:

- `SUPERSEDED` — a `REVOKED` grant named in some evidence record's
  `superseded_grants`. The rotation `§14` requires be addressed had already been
  leaving that trail.
- `INVALID` — an `ACTIVE` grant whose `authority_record` no longer resolves.
  `§12`: a grant does not become valid because a record exists.
- `MISSING` — referenced by W3, absent from every ledger root.
- `UNKNOWN` — a ledger file that will not parse. Corruption is not absence.

### Discrepancies found and resolved

| Discrepancy | Resolution |
|---|---|
| `4313bd2246124a94` `ACTIVE`, unrepresented | `CURRENT` projection generated |
| `47eec2b87a284417` `ACTIVE`, unrepresented | `CURRENT` projection generated; later rotated to `94a4df7aca4543ef`, projection followed |
| Only W3 record named `fd1f1302b0224b97` (`SUPERSEDED`) and called itself live | classified `HISTORICAL` — **not repointed**, which would have erased the first execution from the organizational record |
| `README.md` asserted an empty population | rewritten |
| `governance-artifact-integrity-instance-001` reported `actor-unknown` | see `§E` — a real pre-existing defect |

### Unresolved, and deliberately so

**Escalation `23f315ba9f504272` remains `OPEN`.** `§25` does not authorize
resolving it, and the reconciliation evidence proves no technical resolution:
the refusal is that `report-conformance` lies outside the delegated work scope,
and answering it *is* widening a delegation — `FD-P11-001 §12` item 12.

---

## E. Verification

```text
tools       667 OK   (was 623 — +44)
consumers   276 OK
native_core 801 OK   (1 expected failure)
citation audit  166 documents / 0 errors
stale-state     477 documents / 0 assertions
delegation_catalog       defects: 0
delegation_reconciliation defects: 0
```

**Real execution (`§18` Probe F on the resident corpus, and `§14`).** The W1
coordination proof was run for real. It revoked `47eec2b87a284417`, minted
`94a4df7aca4543ef`, and the projection followed automatically:

```text
BEFORE  active ['4313bd2246124a94', '47eec2b87a284417']   represented both   defects 0
RUN     w1_coordination_proof.py → WorkflowState.SUCCEEDED, 2 steps, 0 refusals
AFTER   active ['4313bd2246124a94', '94a4df7aca4543ef']   represented both   defects 0
        47eec2b87a284417 → SUPERSEDED
```

**That exact sequence is what created the stale record in the first place.** It
now leaves the tracking correct, which is `§14`'s stated goal stated as an
observed outcome rather than a design intention.

**Bounded, and reported as such.** The W4 proof was **not** re-run — see `§G`.
`§14` is proven on the W1 path, through the identical wiring.

**Probes (`§18`) — each asserts one specific defect kind, not merely that
something fired.** A control asserting *some* defect would pass for any of the
eight.

| Probe | Asserted | Mutation (`§19`) |
|---|---|---|
| A active grant missing from W3 | `unrepresented-active-grant`, **from zero projections** | representing it clears exactly that defect |
| B W3 points to revoked grant | `stale-active-claim`, for all four non-`ACTIVE` lifecycles | reclassifying the **record** as history clears it |
| C nonexistent grant | `unknown-grant`, and it counts as representing nothing | pointing at the real grant clears it |
| D invalid provenance | `INVALID` lifecycle on disk; `provenance-mismatch` on actor and on scope | matching the grant clears it |
| E duplicate representation | `duplicate-representation` | removing one clears it |
| F valid synchronized state | **no defects**, on fixtures and on the real corpus | — |

**False-positive controls (`§20`).** A revoked grant with no projection is
clean. A `HISTORICAL` projection of a `SUPERSEDED` grant is clean. The resident
`HISTORICAL` record is asserted **by name** not to appear among defects — if
`§20` were unimplemented it would be the first thing to fire. And the boundary
holds in both directions: `HISTORICAL` is a claim too, and a false one when the
grant is still `ACTIVE`.

**Reachability.** Every one of the eight declared defect kinds is produced by a
fixture, and the declared list is asserted equal to the reachable set. A kind no
fixture can produce is a claim, not a control.

**Idempotency (`§17`).** `reconcile()` is stable across repeated calls;
`project_all()` three times leaves every file byte-identical and creates no new
ones. **And the control that proves that test is not inspecting an
already-clean state**: a record is mutated to name a nonexistent grant,
`unknown-grant` is asserted to fire, `project_all()` is asserted to restore the
original bytes without adding a file. Inspecting a clean result and calling it
idempotence is a defect this programme has already made once.

**Fresh process (`§22`).** A separate interpreter reconciles to the same
defects, the same active set, the same representation and the same lifecycle map
— and no `REVOKED` or `SUPERSEDED` grant appears in the represented set.

**Contract (`§21`, `§23`, `§24`).** The module references no `W4Executor`,
`ExecutionSession` or `AIOSRuntime` — W3 opens no execution path. The result
carries no key named `authorized`, `approved`, `granted` or `permitted`: W6 may
observe a discrepancy, it may not resolve authority. No defect kind contains
`authorize` or `approve`.

---

## F. Governance

`FD-P11-001` consumed: `§20` (W3 represents and tracks), `§29` (a delegation is
a lifecycle object), `§12` items 12–17 (what reconciliation may not do), `§16`
(delegated ≤ available), `§9` (provenance).

**No authority was created.** Every record written projects a grant that already
existed, was issued by the delegator `§4.1` names, and cites an instrument that
resolves on disk. `project()` refuses a grant that is absent, not `ACTIVE`, or
whose provenance does not resolve — so `REVOKED → ACTIVE` is unreachable through
this path, and that is tested rather than asserted.

### Two controls that were passing for reasons unrelated to their claims

Both are re-anchored, not weakened. The invariant each was reaching for is now
asserted directly; neither was relaxed to accommodate an implementation.

**`test_the_resident_population_now_represents_the_live_grant`** asserted
`len(resident) == 1` — a **population count** standing in for the claim in its
own name. The count was one because one record had been written by hand. It
would have gone on passing while the live grant went unrepresented, **and it
did**: `ACT-CC-P11-012` found the record pointing at a revoked grant with this
control green throughout. Now asserted against the ledger.

**`test_no_agent_instance_population_exists_to_draw_from`** asserted that
`docs/architecture/organization` contained no path matching `*instance*`. Its
premise — *no Agent Instance population exists* — **was already false when it
was written**: `FD-P11-001 §7` authorized instances and `ACT-CC-P11-008`
registered one. It stayed green only because instance records live under
`docs/architecture/p11/`, a directory it did not look in. It was matching
**filenames**, so it would equally have fired on any document whose title
contained the word. Now: every instance an organizational record names must be
in the registered population.

That is the eleventh and twelfth proxy control of this programme, and the second
one whose premise was false on the day it was written.

### A real defect the construction exposed

`delegation_catalog.registered_instances()` read `w4-operations` **only**. The
single root was invisible for as long as no W3 record named a W1 instance. The
moment reconciliation projected the live W1 grant, the loader reported its
recipient as `actor-unknown` — an instance registered on disk since
`ACT-CC-P11-011`, reported absent because the loader was looking in one of the
two places instances live.

**A population loader that knows part of the population does not fail. It passes,
on the part it can see.** Fixed here because `S1` is unreachable without it.

---

## G. Classified, not fixed (`§31`)

**Re-running the W4 first-execution proof would duplicate an open,
human-reserved escalation.** Escalation ids are `uuid4`, and the register has no
same-subject deduplication, so a second run would raise the same
`report-conformance` refusal and persist a second record of a question that is
already `OPEN` and reserved to the Founder.

This is why the W4 proof was not re-run in this Act. `§25` does not authorize
resolving that escalation, and duplicating it would be worse than leaving it —
so the behaviour is **classified and left**, per `§31`: *"If unrelated defects
are discovered: CLASSIFY rather than silently expanding scope."*

```text
CLASS   : ACTIONABLE, outside this Act's frontier
SURFACE : tools/escalation_register.py — no same-subject idempotency
IMPACT  : a re-run inflates the count of open human-reserved items
```

---

## H. Protected boundary

```text
13 untracked protected paths : UNTOUCHED
other uncommitted paths      : 0
```

Not read, not modified, not renamed, not relocated, not normalized, not staged,
not committed, not deleted, and not used as authority for anything in this Act.

---

## I. Gap closure (`§35`)

```text
GAP          W3 organizational delegation records are not reconciled against the
             operational delegation ledger, and no defect class compares them.
REMEDIATION  tools/delegation_reconciliation.py — 8 defect classes, ledger-first
             for the load-bearing one; two CURRENT projections generated; the
             stale record classified HISTORICAL rather than repointed; rotation
             wired to carry the projection.
EVIDENCE     real W1 run: rotation 47eec2b87a284417 → 94a4df7aca4543ef with the
             projection following, 0 defects before and after.
VERIFICATION 44 tests — 6 probes, mutation on every control, false-positive in
             both directions, reachability of all 8 kinds, idempotency with a
             mutate-and-repair control, fresh-process reconstruction.
PERSISTED    3 W3 records, 13 ledger grants, both auditors clean.
GAP CLOSED   yes — and measured, not declared.
```

---

## J. Post-construction rediscovery (`§36`, `§37`)

`§36` is explicit that completing this Act does not mean `P11 EXHAUSTED`, and
`§37` that closure of this frontier is no evidence another specific one exists.
So the sweep was run again, from disk, looking for the **same shape** as the gap
just closed — a relation between two things each already marked done, with no
control comparing them.

| Probe | Question | Result |
|---|---|---|
| R1 | Does any evidence record name an escalation with no record, or any record go unnamed? | `dangling=[] orphan=[]` — consistent |
| R2 | Does any grant name a recipient instance with no record on disk? | none |
| R3 | Does any instance record name a non-resident Agent Definition? | both resolve |
| R4 | Are there continuity snapshots disagreeing with the ledger? | none exist |

**No new actionable frontier was found by the sweep.** One was found by doing
the work: the escalation duplication in `§G`.

### W1–W7 state

| Package | State | Evidence |
|---|---|---|
| **W1** Coordination | satisfied | real Runtime-hosted coordination, `proof_level: REAL-RUNTIME`, terminal `SUCCEEDED`, re-run this Act |
| **W2** Planning | satisfied | `PLAN → SEQUENCE → ADAPT → REVISE`; prioritization reserved and structurally absent |
| **W3** Delegation | **satisfied — closed this Act** | 3 records, 2 `CURRENT` + 1 `HISTORICAL`, 8 reconciliation classes, 0 defects |
| **W4** Execution | satisfied | 13/13 conformance on the first real execution; grant bounded and revocable |
| **W5** Continuity | satisfied | fresh-process reconstruction, extended to the reconciliation this Act |
| **W6** Performance | satisfied | detect-only; the reconciliation result carries no approval-shaped key |
| **W7** Governance boundary | satisfied | one escalation `OPEN` and human-reserved; no boundary crossed |

---

## K. Exhaustion (`§39`)

```text
P11 ACTIONABLE FRONTIER:
  1. Escalation register has no same-subject idempotency, so re-running the W4
     proof duplicates an open human-reserved escalation (§G).
     ACTIONABLE — outside this Act's authorized frontier.

P11 RESERVED FRONTIER:
  2. Prioritization / ranking / decision heuristics — Architect-reserved,
     DP-01 §2, §3 W2, NC-08.
  3. Escalation 23f315ba9f504272 — human-reserved; answering it widens a
     delegated scope, FD-P11-001 §12 item 12.
  4. E11 ratification, P12 authorization, Native Core #12 — Founder-reserved.

P11 OPTIONAL FRONTIER:
  5. Multi-agent coordination proof — permitted, not required.
  6. A consumer implementing governance-artifact-integrity — the canonical
     implementer is the Agent Definition, and it exists.

P11 SOURCE-GAP:
  7. Co-Founder Delegation Charter — non-resident, and modifying it is excluded
     from this delegation regardless.
  8. ACT-CC-P11-008 … 013 are not persisted to docs/governance/acts/. Their
     coded verdict scales remain unreadable.

P11 BLOCKED:
  none.

P11 EXHAUSTION:
  NOT EXHAUSTED — one actionable frontier remains, and it is not this one.
  No exhaustion claim is made on the strength of completing this Act (§39).
```

**`§38`.** Item 1 is `ACTIONABLE + AUTHORIZED`? — **no.** It is actionable, and
this Act's authority is bounded to *"construction of the W3 organizational
delegation ↔ operational delegation ledger reconciliation mechanism and its
verification"* (`§41`), which the escalation register is not. It therefore
requires an explicit Act, and is reported rather than taken.
