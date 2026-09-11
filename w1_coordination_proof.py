"""Entry point for the first real `PLAN → WORKFLOW → COORDINATION` — `§20`.

At the repository root for the same reason as `w4_first_execution.py`: the run
needs the W1 machinery in `tools/` and the resident consumer in `consumers/`,
and those two regions are mutually forbidden from importing each other.

**What is exercised, stated precisely.** A real `WorkflowSubsystem`, a real
`WorkflowComposition` built by the authorized handoff, and real lifecycle
transitions `DEFINED → READY → RUNNING → SUCCEEDED` driven by the resident
`WorkflowParticipatingAgent`. The Execution context is the **injected-collaborator
stand-in** the consumer's own tests use, whose docstring says *"The real path is
exercised against a real Runtime in the companion module."* The Runtime-hosted
path is **not** exercised here and is reported as remaining frontier rather than
claimed.

Run:  ``python3 w1_coordination_proof.py``
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import tempfile  # noqa: E402

from native_core.core.infrastructure import (  # noqa: E402
    build_default_infrastructure)
from native_core.core.runtime import AIOSRuntime  # noqa: E402
from native_core.core.runtime.execution import create_execution_layer  # noqa: E402
from native_core.core.workflow import (  # noqa: E402
    Workflow, WorkflowCoordination, WorkflowIdentity)
from consumers.workflow_agent import WorkflowParticipatingAgent  # noqa: E402
from tools.w1_coordination_run import run  # noqa: E402


def perform(step):
    """The delegated work, executed under the W4 delegation."""
    return f"coordinated {step.key} via the sanctioned Workflow surface"


def coordinate(composition):
    """Drive the composed Workflow through its real lifecycle on the **resident
    Runtime** — `ACT-CC-P11-011 §9`.

    **No subsystem is injected.** `WorkflowParticipatingAgent` resolves it from
    ``execution.runtime.workflows``, which the Runtime gates on RUNNING. The
    whole path is resident: `build_default_infrastructure` assembles the
    facilities, `AIOSRuntime` hosts them, `create_execution_layer` issues the
    `Execution`, and the consumer takes the boundary it is given.

    `§36` labels: **RESIDENT · REAL-RUNTIME**. `ACT-CC-P11-010` used the
    injected-collaborator stand-in and said so; this supersedes that stage of
    the proof without retracting what it established.
    """
    identity = WorkflowIdentity(workflow_key="governance-corpus-health-check",
                                workflow_version="1.0")
    workflow = Workflow(identity=identity)

    with tempfile.TemporaryDirectory() as tmp:
        bootstrap = build_default_infrastructure(base_dir=Path(tmp))
        bootstrap.establish()
        runtime = AIOSRuntime(
            runtime_id="p11-w1-runtime",
            storage=bootstrap.get("storage"),
            substrate=bootstrap.get("execution-substrate"))
        runtime.initialize()
        runtime.start()
        execution = create_execution_layer(runtime)

        agent = WorkflowParticipatingAgent(
            workflow=workflow, composition=composition,
            performer=lambda step: f"performed {step.step_key}")
        terminal = agent.participate(execution)

        # `WorkflowCoordination` is the canonical coordination contract:
        # *"Coordination of Agent Instances, bound to exactly one Workflow"*.
        coordination = WorkflowCoordination(workflow=workflow,
                                            composition=composition)
        facts = {
            "proof_level": "REAL-RUNTIME",
            "subsystem_source": "execution.runtime.workflows",
            "subsystem_injected": False,
            "runtime_id": execution.runtime.runtime_id,
            "runtime_state": str(execution.runtime.state),
            "execution_context": str(execution.context),
            "participants": [r.agent_instance_key
                             for r in coordination.participants()],
            "is_multi_agent": coordination.is_multi_agent(),
            "is_empty": coordination.is_empty(),
            "completed_steps": list(agent.completed_steps),
        }
        runtime.stop()
        facts["runtime_state_after_stop"] = str(runtime.state)
    return terminal, facts


def main() -> int:
    evidence = run(perform, coordinate=coordinate)
    print(json.dumps({k: evidence[k] for k in (
        "agent_definition", "agent_instance", "delegation_id",
        "authority_chain", "prepared_steps", "workflow_steps",
        "acting_instances", "composed_skills", "coordination",
        "workflow_terminal_state", "superseded_grants",
        "boundary_crossed")}, indent=2))
    for outcome in evidence["outcomes"]:
        print(f"  {outcome['status']:<10} {outcome['step']:<22} "
              f"{outcome['detail']}")
    return 1 if evidence["boundary_crossed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
