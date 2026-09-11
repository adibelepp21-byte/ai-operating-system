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

from native_core.core.workflow import (  # noqa: E402
    Workflow, WorkflowIdentity, create_workflow_subsystem)
from consumers.workflow_agent import WorkflowParticipatingAgent  # noqa: E402
from tools.w1_coordination_run import run  # noqa: E402


class _Execution:
    """The resident injected-collaborator stand-in, matching
    `consumers/tests/test_workflow_agent.py`."""

    def __init__(self, runtime=None):
        self.runtime = runtime


def perform(step):
    return f"coordinated {step.key} via the sanctioned Workflow surface"


def coordinate(composition):
    """Drive the composed Workflow through its real lifecycle."""
    # Key and version read from the resident record, not invented.
    identity = WorkflowIdentity(workflow_key="governance-corpus-health-check",
                                workflow_version="1.0")
    agent = WorkflowParticipatingAgent(
        subsystem=create_workflow_subsystem(),
        workflow=Workflow(identity=identity),
        composition=composition,
        performer=lambda step: f"performed {step.step_key}")
    return agent.participate(_Execution())


def main() -> int:
    evidence = run(perform, coordinate=coordinate)
    print(json.dumps({k: evidence[k] for k in (
        "agent_definition", "agent_instance", "delegation_id",
        "authority_chain", "prepared_steps", "workflow_steps",
        "acting_instances", "composed_skills", "is_multi_agent",
        "workflow_terminal_state", "superseded_grants",
        "boundary_crossed")}, indent=2))
    for outcome in evidence["outcomes"]:
        print(f"  {outcome['status']:<10} {outcome['step']:<22} "
              f"{outcome['detail']}")
    return 1 if evidence["boundary_crossed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
