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

| Grant | Disposition | Basis |
|---|---|---|
| `4daebea9012d4cc7` | `COMPLETED` | bound plan completed (computed) |
| `0f7ac0785bd8442b` | `COMPLETED` | bound plan completed (computed) |
| `a437cdbbd29940af` | `COMPLETED` | bound plan completed (computed) |
| `4313bd2246124a94` | `REVOKED`, with reason *"REVOKED / CLOSED DUE TO UNEXECUTED OUT-OF-SCOPE STEP"* | Founder B1 (`docs/governance/acts/FD-AGENCY-001-S1-ESCALATION-CLOSURE-DECISION.md`). **Not** `COMPLETED`: the mechanism itself refuses `COMPLETED` for this grant, because its plan escalated |

## 6. Escalation responses (Founder B1 — F-S1-4 closed)

`tools/escalation_register.py` was changed **only** where a response is written and read:

- **Uncertified root:** the response is written beside the escalation, exactly as before. Same file, same payload shape. `basis` is added only if a caller passes it.
- **Certified root:** the response is **never** written beside the escalation.
  - It is written to `LIVE_RESPONSES` (`docs/architecture/agency/operations/escalation-responses/<root-name>/<id>.response.json`).
  - The write is guarded before any directory is created.
  - The response is bound to the escalation's sha256 and names its root and basis.
  - Without a response ledger, the write is **refused** rather than made in place.
- **Reading is opt-in:** `EscalationRegister(root, response_ledger=...)` and `reconstruct(root, response_ledger=...)`. An external response counts only if it names the escalation and the root, the escalation's bytes are unchanged, and the ledger is outside every certified root.
- **Unchanged:** closing still requires a `HumanAuthority`, and the register still has no method that approves or grants anything.

`tools.w4_continuity.operational_state(root)` is the reading that honours both live ledgers. `reconstruct(root)` with no ledger is the historical reading.

**Applied:** escalation `23f315ba9f504272` was answered by the Founder (B1), recorded at `operations/escalation-responses/w4-operations/23f315ba9f504272.response.json`. Its basis cites the decision instrument and its content sha256.

**Not changed:** `EscalationRegister.record()`, which raises new escalations, still writes into whatever root it is given. No new escalation is being raised into a certified root, and B1 authorizes only the response path.
