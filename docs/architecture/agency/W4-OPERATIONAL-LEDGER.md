# W4 Operational Ledger — Live Disposition of Delegations

| Field | Value |
|---|---|
| **Authority** | `FD-AGENCY-001` S-1 Founder Decision, Q-S1-A = **A2** (`docs/governance/acts/FD-AGENCY-001-S1-TERMINAL-STATE-DECISION.md`; Register `§136`) |
| **Closes** | S-1 gaps C-1 (no completed state), C-2 (in-process-only revoke), C-3 (certified roots hold live state). F-S1-4 is addressed only as far as A2 requires (see `§6`) |
| **Code** | `tools/w4_delegation.py` (`plan_completion`, `record_disposition`, `read_dispositions`, `LIVE_LEDGER`); `tools/w4_continuity.py` (`reconstruct(..., operational_ledger=...)`) |
| **Ledger** | `docs/architecture/agency/operations/w4-dispositions/<root-name>/<delegation-id>.disposition.json` |
| **Tests** | `tools/tests/test_w4_operational_ledger.py` (18 tests; mutation-checked) |

---

## 1. Two facts, kept apart

| Fact | Where | Values | Mutable? |
|---|---|---|---|
| **Historical status** | the delegation record itself (`*.delegation.json`) | `ACTIVE`, `REVOKED` (unchanged contract) | Only where the record is not certified evidence. In `docs/architecture/p11` **never** (FD-P11-002, enforced by P12-F12) |
| **Operational disposition** | the live ledger, one file per grant | `COMPLETED`, `REVOKED` | Written once, append-only. Never edited |

**Operational status** = the disposition, if a valid one exists; otherwise the historical status.

The reader never merges the two facts:
- `historical_active_grants` reports what the records say;
- `active_grants` reports what is still live once the ledger is honoured.

## 2. Disposition semantics

| Disposition | Meaning | Established by |
|---|---|---|
| `COMPLETED` | The grant ended by its own termination condition: *"on completion of the bound plan"* | **Computed** by `plan_completion()`, never asserted. Exactly one evidence record names the bound plan (from the lifecycle boundary) and the grant; every outcome is `success`; no escalation was raised; the workflow, where recorded, reached `SUCCEEDED`; every work-scope step has a success outcome |
| `REVOKED` | The delegator withdrew the grant (`FD-P11-001` revocation), for a record that cannot be rewritten in place | A written reason. This is a removal of authority, so it needs no new provenance |

## 3. Rules the mechanism enforces

1. **Recorder.** Only `Claude Code / AIOS Co-Founder` (`FD-P11-001 §4.1`), and only if that is the grant's own delegator. The accountable party does not move.
2. **No reinterpretation.** A disposition is accepted only over a historically `ACTIVE` grant. A `REVOKED` record is never re-read as anything else.
3. **Append-only.** One disposition per grant. A second one is refused.
4. **Bound to bytes.** The disposition stores the sha256 of the delegation record and, for `COMPLETED`, of the evidence. If either changes, the reader reports a **fault** and does not honour the disposition. The grant then keeps its historical status, and `continuation_conditions` reports `DISPOSITION FAULTS`.
5. **Outside the certified boundary.** The write is guarded (`p12_certified_evidence_guard.guard`) before any directory is created. If the ledger ever ends up inside a certified root, the reader honours nothing from it and reports why.
6. **Rebuildable.** The reader derives everything from files: delegation records, evidence and dispositions. Nothing is cached, and nothing comes from a previous run.
7. **Opt-in reading.** `reconstruct(root)` without a ledger returns the historical reading, identical to before. Certified P11 measurements (E11) stay reproducible. Honouring the ledger is an explicit choice: `reconstruct(root, operational_ledger=LIVE_LEDGER)`.

## 4. What is unchanged

- The delegation contract: `ACTIVE` / `REVOKED`, the `§13` elements, `issue`, `revoke`.
- Every certified byte under `docs/architecture/p11`.
- W3 projections (`tools/delegation_reconciliation.py`). They are reconciled against the historical ledger, which still says `ACTIVE`, so they remain consistent. Whether W3 should follow operational state is **not** decided here.
- No new subsystem, entity, state machine or authority. Three functions and an opt-in parameter.

## 5. Applied (S-1)

The three grants whose termination condition S-1 established were recorded `COMPLETED`:
- `4daebea9012d4cc7`;
- `0f7ac0785bd8442b`;
- `a437cdbbd29940af`.

**`4313bd2246124a94` was not dispositioned.** Its plan did not complete, and its escalation `23f315ba9f504272` is deferred by the Founder (Q-S1-B). It stays operationally `ACTIVE`.

## 6. F-S1-4 (escalation response write)

`EscalationRegister.record_response()` still writes beside the escalation, which for `23f315ba` is a certified root. A2 does not authorize changing the escalation register, and Q-S1-B is deferred. So this record does **not** change it.

Before any response to a certified-root escalation is persisted, the same pattern applies: a response recorded outside the certified boundary. That is a separate, bounded change for when Q-S1-B is decided.
