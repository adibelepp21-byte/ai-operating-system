"""`ACT-CC-P12-005` — real system work through an actual resident refusal site.

Proves resident consumption of `tools.p12_governance_escalation_join`, not
merely that it is importable. This script calls `tools.w4_first_run.run` —
one of the three real refusal-recording call sites wired this Act — with
three narrow, disclosed substitutions, each orthogonal to what is being
proven:

1. **`OPERATIONS` stays the resident `docs/architecture/p12/w4-operations/`
   root** — not the P11 historical one, which already holds
   `first-execution.evidence.json` under
   `tools/p12_certified_evidence_guard.guard`'s protection. `§10`/`§21` of
   this Act forbid working around that guard, so this script never points at
   the historical root. The P12 root is already trusted:
   `tools.p12_provenance_verification.DELEGATION_ROOTS` already searches it,
   and it already holds six real delegations from earlier P12 real
   executions.
2. **`INSTANCE_KEY` is a fresh value, not the module's own
   `engineering-intelligence-instance-001`.** That constant is shared with
   `p12_w4_integrated_execution.py`, which has already issued live grants
   into this same directory. `tools.w4_first_run._revoke_stale_grants` scans
   this directory for `ACTIVE` grants held by whatever instance key it is
   given and **revokes them** — real, in-place mutation, by design, for a
   genuine re-run of *this* proof. Run under the shared key, it would have
   revoked grants this Act does not own and other P12 evidence depends on
   staying `ACTIVE`. A fresh key sidesteps the collision entirely: nothing
   in this directory is registered to it, so nothing is found to revoke.
3. **`project()`** (`tools/delegation_reconciliation.py`) is not called
   against its production root, which is built from `docs/architecture/p11/`
   only. `project` maintains a different organizational-state surface
   (`W3`'s ledger projection) this Act does not touch or claim anything
   about; calling it here would raise for a reason unrelated to the
   escalation join. Monkeypatched to a no-op for the duration of this one
   call, disclosed rather than hidden.

Everything else is the real, unmodified `tools.w4_first_run.run` function:
real agent registration, real delegation issuance, real `W4Executor`, a real
out-of-scope step that `W4Executor` really refuses, real escalation
recording through the newly-wired `join_refusals_to_grants`, and a real
structural join written beside it.

`work_scope=("verify-delegation-elements",)` is passed explicitly — `run`'s
own default today grants both plan steps, which is why this script does not
rely on the default to reproduce a refusal. This is not a new work_scope
value: it is the exact one the resident historical escalation
(`23f315ba9f504272`) already shows was granted when `ACT-CC-P11-008` first
ran this function.
"""

from __future__ import annotations

import sys
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import tools.w4_first_run as w4_first_run  # noqa: E402
from tools.p12_governance_join_reader import resolve  # noqa: E402
from tools.p12_provenance_verification import delegation_records  # noqa: E402

OPERATIONS = REPO_ROOT / "docs/architecture/p12/w4-operations"

#: Distinct from `w4_first_run.INSTANCE_KEY` — see module docstring, point 2.
INSTANCE_KEY = "engineering-intelligence-instance-p12w3-005-001"


def _verify(lines, criterion_names):
    """A real, non-consumer verifier: does each required element name
    literally appear in the subject file's lines?

    `tools/` may not import `consumers/` (AST-enforced), so this cannot be
    `EngineeringIntelligenceAgent.verify` without a root-level entry point
    matching `w4_first_execution.py`'s own pattern. This performs the same
    class of real check — reading the actual file, asking the actual
    question — over resident repository tooling rather than a Platform
    consumer, the same disclosure `tools/w1_cross_department_run.py`'s own
    module docstring makes about its second step's performer.
    """
    joined = "\n".join(lines)
    return {name: (name in joined) for name in criterion_names}


def run() -> dict:
    OPERATIONS.mkdir(parents=True, exist_ok=True)
    with mock.patch.object(w4_first_run, "OPERATIONS", OPERATIONS), \
         mock.patch.object(w4_first_run, "INSTANCE_KEY", INSTANCE_KEY), \
         mock.patch.object(w4_first_run, "project", lambda delegation_id: None):
        evidence = w4_first_run.run(
            _verify, persist=True,
            work_scope=("verify-delegation-elements",))
    return evidence


def main() -> int:
    evidence = run()
    escalation_ids = evidence["escalations"]
    print(f"delegation_id      {evidence['delegation_id']}")
    print(f"boundary_crossed   {evidence['boundary_crossed']}")
    print(f"escalations        {escalation_ids}")

    if not escalation_ids:
        print("NO REFUSAL OCCURRED — nothing to join. This would falsify "
              "the premise this script exists to prove.")
        return 1

    known = {d["delegation_id"] for d in delegation_records()}
    verified = []
    for escalation_id in escalation_ids:
        result = resolve(OPERATIONS, OPERATIONS, escalation_id)
        print(f"  {escalation_id}  {result}")
        verified.append(result)

    all_joined = all(r["status"] == "JOINED" for r in verified)
    delegation_known = evidence["delegation_id"] in known
    print()
    print(f"all escalations independently JOINED: {all_joined}")
    print(f"delegation independently resolves:     {delegation_known}")
    print()
    print("Persisted under docs/architecture/p12/w4-operations/. "
          "The verdict above came from tools.p12_governance_join_reader, "
          "which imports nothing from the writer.")
    return 0 if (all_joined and delegation_known) else 1


if __name__ == "__main__":
    raise SystemExit(main())
