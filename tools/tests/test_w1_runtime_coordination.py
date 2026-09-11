"""`ACT-CC-P11-011 §37`/`§38` — the F1/F2/F3 conclusions, held as controls.

Three findings, each reached by discovery rather than construction:

* **F1-A** — the resident Runtime path already exists and is sufficient;
* **F2-B** — multi-agent participation is **not required** by W1 semantics;
* **F3-C** — the resident participant mechanism already satisfies the role.

`§1`: *"Absence of implementation is not proof of absence of a canonical
mechanism."* Every control below asserts a timeless invariant rather than an
absence (`§38`).
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

from native_core.core.infrastructure import build_default_infrastructure  # noqa: E402
from native_core.core.runtime import AIOSRuntime, RuntimeNotRunning  # noqa: E402
from native_core.core.runtime.execution import create_execution_layer  # noqa: E402
from native_core.core.workflow import (  # noqa: E402
    AgentInstanceRef, DirectCollaborationForbidden, SkillRef, Workflow,
    WorkflowComposition, WorkflowCoordination, WorkflowIdentity, WorkflowStep)

W1_OPS = REPO_ROOT / "docs/architecture/p11/w1-operations"
IDENTITY = WorkflowIdentity(workflow_key="governance-corpus-health-check",
                            workflow_version="1.0")


def _running_runtime(tmp, runtime_id="control-runtime"):
    bootstrap = build_default_infrastructure(base_dir=Path(tmp))
    bootstrap.establish()
    runtime = AIOSRuntime(runtime_id=runtime_id,
                          storage=bootstrap.get("storage"),
                          substrate=bootstrap.get("execution-substrate"))
    runtime.initialize()
    runtime.start()
    return runtime


def _composition(*instances):
    return WorkflowComposition(steps=tuple(
        WorkflowStep(f"step-{i}", AgentInstanceRef(key),
                     SkillRef("open-item-tracking-review"))
        for i, key in enumerate(instances)))


class F1_TheResidentRuntimePathExists(unittest.TestCase):
    """`§6`/`§7` — **F1-A**, proven by using it rather than by inspecting it.

    `ACT-CC-P11-010` used the injected-collaborator stand-in and labelled it as
    such. `§8` forbids representing that as the resident Runtime, so this
    exercises the real one: facilities from `build_default_infrastructure`, an
    `AIOSRuntime`, and an `Execution` from `create_execution_layer`.
    """

    def test_a_resident_runtime_hosts_a_workflow_subsystem(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = _running_runtime(tmp)
            try:
                self.assertEqual(type(runtime.workflows).__name__,
                                 "WorkflowSubsystem")
                execution = create_execution_layer(runtime)
                self.assertIs(execution.runtime, runtime)
                self.assertEqual(execution.context.runtime_id,
                                 runtime.runtime_id)
            finally:
                runtime.stop()

    def test_the_runtime_gates_its_subsystem_on_running(self):
        """`§10`: `RUNTIME HOSTING ≠ AUTHORITY CREATION`.

        The Runtime does not grant anything; it refuses when not RUNNING, and
        the refusal propagates rather than being worked around.
        """
        with tempfile.TemporaryDirectory() as tmp:
            runtime = _running_runtime(tmp)
            runtime.stop()
            with self.assertRaises(RuntimeNotRunning):
                _ = runtime.workflows
            with self.assertRaises(RuntimeNotRunning):
                create_execution_layer(runtime)

    def test_the_real_run_used_the_resident_path_not_an_injection(self):
        facts = json.loads((W1_OPS / "w1-coordination.evidence.json")
                           .read_text(encoding="utf-8"))["coordination"]
        self.assertEqual(facts["proof_level"], "REAL-RUNTIME")
        self.assertFalse(facts["subsystem_injected"])
        self.assertEqual(facts["subsystem_source"],
                         "execution.runtime.workflows")
        self.assertEqual(facts["runtime_state"], "RuntimeState.RUNNING")


class F2_MultiAgentIsNotRequired(unittest.TestCase):
    """`§11`–`§14` — **F2-B**, read from the canonical contract.

    `WorkflowCoordination` is *"Coordination of Agent Instances, bound to
    exactly one Workflow"*, and its own docstring settles the question: *"A
    coordination with an empty composition is structurally valid — it
    coordinates no one."* `is_multi_agent()` is *"Reported, never acted on
    (PR-3)."*

    So `is_multi_agent = False` is a **property of a valid coordination**, not a
    deficiency — which corrects my `ACT-CC-P11-010` frontier entry listing a
    second instance as actionable work.
    """

    def test_a_coordination_with_no_participants_is_structurally_valid(self):
        coordination = WorkflowCoordination(workflow=Workflow(identity=IDENTITY),
                                            composition=WorkflowComposition())
        self.assertTrue(coordination.is_empty())
        self.assertFalse(coordination.is_multi_agent())

    def test_a_single_participant_coordination_is_valid(self):
        coordination = WorkflowCoordination(
            workflow=Workflow(identity=IDENTITY),
            composition=_composition("instance-a"))
        self.assertFalse(coordination.is_empty())
        self.assertFalse(coordination.is_multi_agent())
        self.assertEqual(len(coordination.participants()), 1)

    def test_multi_agent_remains_available_and_is_merely_reported(self):
        """Not required is not the same as impossible."""
        coordination = WorkflowCoordination(
            workflow=Workflow(identity=IDENTITY),
            composition=_composition("instance-a", "instance-b"))
        self.assertTrue(coordination.is_multi_agent())
        self.assertEqual(len(coordination.participants()), 2)

    def test_coordination_cannot_exist_outside_a_workflow(self):
        """`INV-13`, which is what actually constrains coordination."""
        with self.assertRaises(DirectCollaborationForbidden):
            WorkflowCoordination(workflow="not-a-workflow",
                                 composition=_composition("instance-a"))


class F3_TheResidentParticipantSatisfiesTheRole(unittest.TestCase):
    """`§17`/`§18` — **F3-C**.

    I recorded *"no resident consumer for `governance-artifact-integrity-agent`"*
    as actionable in `ACT-CC-P11-010`. That is an absence of a **capability
    implementation**, not of the coordination mechanism: `§1` —
    *"Absence of implementation is not proof of absence of a canonical
    mechanism."*
    """

    def test_the_resident_participant_exists_and_drives_the_lifecycle(self):
        evidence = json.loads((W1_OPS / "w1-coordination.evidence.json")
                              .read_text(encoding="utf-8"))
        self.assertIn("SUCCEEDED", evidence["workflow_terminal_state"])
        self.assertEqual(evidence["coordination"]["completed_steps"],
                         evidence["workflow_steps"])

    def test_coordination_succeeded_without_a_capability_implementation(self):
        """The property, asserted from the run rather than from the consumer.

        **My first version imported `consumers.workflow_agent` to inspect its
        signature — and `tools/` may not import that region.** It is the second
        time I have crossed that boundary: `ACT-CC-P11-008` did it from
        `w4_first_run.py`, and the resolution then was to inject the performer.
        Doing it from a *test* is the same edge in the dependency graph.

        The fix is not a weaker assertion. The claim is that coordination needs
        no capability implementation, and the **real run proves it directly**:
        no consumer implements `governance-artifact-integrity`, and the Workflow
        still reached a terminal `SUCCEEDED` with both steps completed.
        """
        evidence = json.loads((W1_OPS / "w1-coordination.evidence.json")
                              .read_text(encoding="utf-8"))
        self.assertEqual(
            list((REPO_ROOT / "consumers").glob("governance_artifact*")), [])
        self.assertIn("SUCCEEDED", evidence["workflow_terminal_state"])
        self.assertEqual(evidence["coordination"]["completed_steps"],
                         evidence["workflow_steps"])


class NC08_09_NeitherWorkflowNorRuntimeCreatesAuthority(unittest.TestCase):
    """`§37` NC-08, NC-09."""

    def test_a_workflow_step_names_an_actor_without_authorizing_it(self):
        """Workflow accepts a key; it does not check or confer authority.

        This is why the handoff adapter must, and does — the authority check
        lives where authority lives, not in the coordination surface.
        """
        step = WorkflowStep("s", AgentInstanceRef("never-registered"),
                            SkillRef("open-item-tracking-review"))
        self.assertEqual(step.performed_by.agent_instance_key,
                         "never-registered")
        for name in dir(step):
            self.assertFalse(any(v in name.lower() for v in
                                 ("authorize", "grant", "permit")), name)

    def test_the_runtime_exposes_no_authorization_surface(self):
        with tempfile.TemporaryDirectory() as tmp:
            runtime = _running_runtime(tmp)
            try:
                offenders = [n for n in dir(runtime) if not n.startswith("_")
                             and any(v in n.lower() for v in
                                     ("authorize", "grant", "delegate",
                                      "approve"))]
                self.assertEqual(offenders, [])
            finally:
                runtime.stop()


class NC14_18_NoOverstatementAndNoInferredAbsence(unittest.TestCase):
    """`§37` NC-14 and NC-18 — the two this Act exists to enforce."""

    def test_the_run_reports_single_agent_honestly(self):
        facts = json.loads((W1_OPS / "w1-coordination.evidence.json")
                           .read_text(encoding="utf-8"))["coordination"]
        self.assertFalse(facts["is_multi_agent"])
        self.assertEqual(len(set(facts["participants"])), 1)

    def test_every_proof_stage_carries_an_explicit_label(self):
        """`§36`: no category may be silently promoted."""
        facts = json.loads((W1_OPS / "w1-coordination.evidence.json")
                           .read_text(encoding="utf-8"))["coordination"]
        self.assertIn(facts["proof_level"],
                      ("SIMULATED", "INJECTED", "TEST-HARNESS", "RESIDENT",
                       "REAL-RUNTIME", "REAL-MULTI-AGENT"))

    def test_the_label_must_agree_with_the_facts_it_summarizes(self):
        """Membership in the allowed set is not truth.

        **Found by a mutation probe that reported `OK`.** The control above
        checks only that the label is a recognised category — so a run could
        claim `REAL-MULTI-AGENT` while recording a single participant, and pass.
        `§36` forbids silent promotion, and a label nobody cross-checks is
        exactly how promotion stays silent.

        Each label is now tied to the evidence that would have to be true:
        `REAL-MULTI-AGENT` requires more than one participant;
        `REAL-RUNTIME` requires an uninjected subsystem and a RUNNING Runtime;
        `INJECTED` requires the opposite.
        """
        facts = json.loads((W1_OPS / "w1-coordination.evidence.json")
                           .read_text(encoding="utf-8"))["coordination"]
        level = facts["proof_level"]
        if level == "REAL-MULTI-AGENT":
            self.assertTrue(facts["is_multi_agent"])
            self.assertGreater(len(set(facts["participants"])), 1)
        if level == "REAL-RUNTIME":
            self.assertFalse(facts["subsystem_injected"])
            self.assertEqual(facts["subsystem_source"],
                             "execution.runtime.workflows")
            self.assertEqual(facts["runtime_state"], "RuntimeState.RUNNING")
        if level == "INJECTED":
            self.assertTrue(facts["subsystem_injected"])
        # And the weaker claim must not hide a stronger one going unlabelled.
        if facts["is_multi_agent"]:
            self.assertEqual(level, "REAL-MULTI-AGENT")

    def test_an_implementation_absence_is_not_an_architectural_absence(self):
        """NC-18, asserted against the actual finding.

        No resident consumer implements the governance-artifact-integrity
        capability — and the coordination mechanism exists regardless, which the
        real run proves.
        """
        consumers_dir = REPO_ROOT / "consumers"
        self.assertEqual(
            list(consumers_dir.glob("governance_artifact*")), [])
        self.assertTrue((consumers_dir / "workflow_agent.py").is_file())
        evidence = json.loads((W1_OPS / "w1-coordination.evidence.json")
                              .read_text(encoding="utf-8"))
        self.assertIn("SUCCEEDED", evidence["workflow_terminal_state"])


class ContinuityAcrossTheRuntimeBoundary(unittest.TestCase):
    """`§32`/`§33` — a fresh process reconstructs the W1 state."""

    def test_a_fresh_process_recovers_the_w1_run(self):
        program = ("import sys, json; sys.path.insert(0, sys.argv[1]);"
                   "from pathlib import Path;"
                   "from tools.w4_continuity import reconstruct;"
                   "s = reconstruct(Path(sys.argv[1]) / "
                   "'docs/architecture/p11/w1-operations');"
                   "print(json.dumps({'act': s['last_act'], "
                   "'plan': s['last_plan'], 'active': s['active_grants'], "
                   "'dup': s['duplicate_active']}))")
        proc = subprocess.run([sys.executable, "-c", program, str(REPO_ROOT)],
                              capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(proc.returncode, 0, proc.stderr)
        recovered = json.loads(proc.stdout)
        self.assertEqual(recovered["act"], "ACT-CC-P11-011")
        self.assertEqual(recovered["plan"], "w1-coordination-proof-plan-0")
        self.assertFalse(recovered["dup"])
        self.assertEqual(len(recovered["active"]), 1)

    def test_the_persisted_state_holds_at_most_one_live_grant(self):
        grants = [json.loads(p.read_text(encoding="utf-8"))
                  for p in W1_OPS.glob("*.delegation.json")]
        self.assertLessEqual(
            len([g for g in grants if g["status"] == "ACTIVE"]), 1)
        for grant in grants:
            if grant["status"] == "REVOKED":
                self.assertTrue(grant.get("revocation_reason", "").strip())

    def test_the_supersession_mechanism_actually_runs_on_a_rerun(self):
        """`§34`, exercised rather than observed.

        **Found by a mutation probe that reported `OK`.** Disabling the
        stale-grant sweep changed nothing the previous control could see,
        because that control reads files the *last real run* already tidied. A
        control that inspects a clean result cannot tell whether the thing that
        cleaned it still works.

        This drives two runs against a temporary root and asserts the second
        withdrew the first.
        """
        from tools.w1_coordination_run import _revoke_stale
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "g1.delegation.json").write_text(json.dumps({
                "delegation_id": "g1", "status": "ACTIVE",
                "recipient_instance": "inst"}), encoding="utf-8")
            (root / "g2.delegation.json").write_text(json.dumps({
                "delegation_id": "g2", "status": "ACTIVE",
                "recipient_instance": "other"}), encoding="utf-8")
            revoked = _revoke_stale(root, "inst")
            self.assertEqual(revoked, ("g1",))
            after = {json.loads((root / f"{k}.delegation.json")
                                .read_text(encoding="utf-8"))["status"]
                     for k in ("g1", "g2")}
            self.assertEqual(after, {"REVOKED", "ACTIVE"})
            reason = json.loads((root / "g1.delegation.json")
                                .read_text(encoding="utf-8"))
            self.assertTrue(reason["revocation_reason"].strip())


if __name__ == "__main__":
    unittest.main()
