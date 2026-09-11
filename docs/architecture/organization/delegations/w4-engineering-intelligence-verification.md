# W4 Delegation — Engineering Intelligence Verification

> **Preserved history: the organizational representation of the first real W4
> operational grant**, `fd1f1302b0224b97`, which is now `REVOKED` and
> `SUPERSEDED`. `FD-P11-001 §20`: *"W3 Delegation is the organizational
> mechanism through which the authorized Delegation record is represented and
> tracked."*
>
> **This record said "live" until `ACT-CC-P11-013`.** It was true when written
> and stopped being true the next time the proof ran: `_revoke_stale_grants()`
> withdrew the grant it names and minted a successor, and nothing propagated,
> because no relation between the ledger and this layer existed. The correction
> is not to repoint it at the successor — that would erase the first execution
> from the organizational record — but to classify it truthfully as history and
> let the `CURRENT` projection live in its own file.
>
> **This record creates no authority.** It represents a grant that already
> exists, issued under `FD-P11-001 §9` and recorded at
> `docs/architecture/p11/w4-operations/fd1f1302b0224b97.delegation.json`.
> `§20`: W3 *"must not manufacture authority absent valid provenance"* — the
> provenance is cited below and resolves.
>
> **Why this directory was empty until now.** `ACT-CC-P11-005` built the W3
> mechanism and left the population at `0`, because authoring a delegation is an
> exercise of the authority being delegated and **no legitimate delegator
> existed**. `FD-P11-001 §4.1` created one. The empty population was correct
> then and would be incorrect now.

## Operational Grant

fd1f1302b0224b97

## Representation

HISTORICAL

Preserved deliberately. `ACT-CC-P11-013 §16`: *"Historical records must not be
destroyed merely to achieve apparent consistency."* `§20` requires the
reconciliation to distinguish preserved history from a stale claim to be live —
this record is the former, and the control that tells them apart reads this
section rather than guessing from the grant's status.

## Authority Source

claude-code-aios-co-founder

The delegator `FD-P11-001 §4.1` names. **Not a Department, and deliberately so**
— `§5` rejects Engineering or Platform becoming the W4 delegator *"merely by
virtue of being organizational/domain labels."*

## Authorized Scope

engineering-intelligence

Bounded by the recipient's own permitted surface, per `FD-P11-001 §16`:
`Delegated Authority ≤ Available Delegator Authority ∩ FD-P11-001 Scope ∩
Canonical Boundaries`.

## Delegated Actor

engineering-intelligence-instance-001

An **Agent Instance**, not an Agent Definition — `FD-P11-001 §6.1`: *"An Agent
Definition alone is insufficient."* Registered at
`docs/architecture/p11/w4-operations/engineering-intelligence-instance-001.instance.json`.

## Boundary

one execution of plan w4-first-execution-proof-plan-0. Resource boundary: read-only access to tools/w4_delegation.py; no network; no governance artifact is written.
Work scope is limited to the named plan steps `verify-delegation-elements`, `report-conformance`.

Termination: on completion of the bound plan, or on revocation by the authorized delegator.

## Accountability

claude-code-aios-co-founder

`FD-P11-001 §15` fixes the chain as **Agent Instance → delegator → Founder**, and
`§15.2` forecloses the disclaimer: delegation *"does not allow Claude to disclaim
responsibility by saying: 'The Agent Instance did it.'"* Ultimate human
governance accountability remains with the Founder and does not move.

## Verification

[The first real execution evidence](../../p11/w4-operations/first-execution.evidence.json)
records the run: two steps, both `success`, 13 of 13 conformance criteria
satisfied, no boundary crossed.

## Authorizing Instrument

[FD-P11-001](../../../governance/acts/FD-P11-001-W4-DELEGATION-AND-AGENT-INSTANCE-AUTHORIZATION.md) §9
