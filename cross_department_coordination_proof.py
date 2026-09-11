"""Entry point — the cross-Department coordination `E11-04` requires.

Here rather than in `tools/` for the reason `w4_first_execution.py` records:
wiring a real performer needs `consumers/`, and `tools/` may not import that
region. Both assertions are AST-based, so a guarded import would violate them
exactly as a top-level one does.

**Both steps perform real work, and neither was written for `E11-04`.**

* `verify-artifact-conformance` runs `EngineeringIntelligenceAgent.verify` —
  the **Testing** sub-ability `ADR-0008` established on 2026-07-30 and
  `consumers/engineering_intelligence_agent.py` implemented on 2026-09-02 —
  against `tools/w4_delegation.py` and the `FD-P11-001 §13` conformance
  criteria. It **writes a conformance record.**
* `verify-citation-discipline` runs the resident corpus citation audit over
  **that record**, checking that every pointer it carries resolves.

The dependency is therefore an ordering constraint and not a declaration: the
second step reads what the first wrote, and reports `MISSING` if it is not
there. The two could not be exchanged.

**Reported precisely.** Step two's performer is **resident repository tooling**,
`tools/corpus_citation_audit.py`, not a Platform consumer — no consumer realizes
`governance-artifact-integrity`, and `ACT-CC-P11-012` classified building one as
`OPTIONAL`. The work is genuine and the performer is named for what it is. That
is the same discipline `w1_coordination_proof.py` applied when it labelled its
own performer a stand-in.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from native_core.core.infrastructure import (  # noqa: E402
    build_default_infrastructure)
from native_core.core.runtime import AIOSRuntime  # noqa: E402
from native_core.core.runtime.execution import create_execution_layer  # noqa: E402
from native_core.core.workflow import (  # noqa: E402
    Workflow, WorkflowCoordination, WorkflowIdentity)
from consumers.engineering_intelligence_agent import (  # noqa: E402
    Artifact, ConformanceCriterion, EngineeringIntelligenceAgent)
from consumers.workflow_agent import WorkflowParticipatingAgent  # noqa: E402
from tools.corpus_citation_audit import audit  # noqa: E402
from tools.w1_cross_department_run import (  # noqa: E402
    OPERATIONS, WORKFLOW_KEY, run)
from tools.w4_delegation import REQUIRED_ELEMENTS  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent
SUBJECT = REPO_ROOT / "tools" / "w4_delegation.py"
RECORD = OPERATIONS / "conformance-record.md"


def _verify_conformance() -> str:
    """*Testing* — the Engineering Department's real work, and it writes."""
    agent = EngineeringIntelligenceAgent()
    lines = tuple(SUBJECT.read_text(encoding="utf-8").split("\n"))
    criteria = tuple(ConformanceCriterion(name=name, required_text=name)
                     for name in REQUIRED_ELEMENTS)
    results = agent.verify(Artifact(name=SUBJECT.name, lines=lines), criteria)
    satisfied = [r.criterion_name for r in results if r.satisfied]
    unsatisfied = [r.criterion_name for r in results if not r.satisfied]

    OPERATIONS.mkdir(parents=True, exist_ok=True)
    RECORD.write_text("\n".join((
        "# Conformance Record — tools/w4_delegation.py",
        "",
        "> Produced by an Agent Instance of the",
        "> [Engineering Intelligence Agent](../../organization/engineering/agent-definitions/engineering-intelligence-agent.md)",
        "> composing [`skill.artifact-conformance-verification`](../../organization/execution-catalog/skill/artifact-conformance-verification.md).",
        "> It reports; it decides nothing.",
        "",
        "## Subject and criteria",
        "",
        "Artifact verified: `tools/w4_delegation.py`.",
        "",
        "Criteria stated by",
        "`docs/governance/acts/FD-P11-001-W4-DELEGATION-AND-AGENT-INSTANCE-AUTHORIZATION.md`",
        "§13, and read from `tools/w4_delegation.py` as `REQUIRED_ELEMENTS`.",
        "",
        "Delegation authority: `docs/governance/acts/DP-01-P11-FOUNDER-AUTHORIZATION.md`.",
        "",
        f"- satisfied: {len(satisfied)} of {len(results)}",
        f"- unsatisfied: {unsatisfied or 'none'}",
        "",
    )), encoding="utf-8")
    return (f"verified {len(satisfied)}/{len(results)} conformance criteria "
            f"against {SUBJECT.name}; record written to {RECORD.name}")


def _verify_citation_discipline() -> str:
    """*Citation discipline* — over the record the previous step wrote."""
    if not RECORD.is_file():
        return "MISSING: the conformance record does not exist; nothing to check"
    report = audit([str(RECORD.relative_to(REPO_ROOT))])
    return (f"checked {RECORD.name}: {report['citations_checked']} citation(s), "
            f"{report['errors']} unresolvable, {report['warnings']} warning(s)")


PERFORMERS = {
    "verify-artifact-conformance": _verify_conformance,
    "verify-citation-discipline": _verify_citation_discipline,
}


def perform(step):
    return PERFORMERS[step.key]()


def coordinate(composition):
    """Drive the composed two-Department Workflow on the **resident Runtime**."""
    identity = WorkflowIdentity(workflow_key=WORKFLOW_KEY,
                                workflow_version="1.0")
    workflow = Workflow(identity=identity)
    with tempfile.TemporaryDirectory() as tmp:
        bootstrap = build_default_infrastructure(base_dir=Path(tmp))
        bootstrap.establish()
        runtime = AIOSRuntime(runtime_id="p11-cross-department-runtime",
                              storage=bootstrap.get("storage"),
                              substrate=bootstrap.get("execution-substrate"))
        runtime.initialize()
        runtime.start()
        execution = create_execution_layer(runtime)
        agent = WorkflowParticipatingAgent(
            workflow=workflow, composition=composition,
            performer=lambda step: f"performed {step.step_key}")
        terminal = agent.participate(execution)
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
            "work_performer_engineering": "consumers.engineering_intelligence_agent"
                                          ".EngineeringIntelligenceAgent.verify "
                                          "(RESIDENT CONSUMER)",
            "work_performer_platform": "tools.corpus_citation_audit.audit "
                                       "(RESIDENT REPOSITORY TOOLING — no "
                                       "Platform consumer exists)",
        }
        runtime.stop()
        facts["runtime_state_after_stop"] = str(runtime.state)
    return terminal, facts


def main() -> int:
    evidence = run(perform, coordinate=coordinate)
    print(json.dumps(evidence, indent=2))
    print()
    for outcome in evidence["outcomes"]:
        print(f"  {outcome['status']:<10} {outcome['step']:<28} {outcome['detail']}")
    print(f"\n  departments: {evidence['departments']} "
          f"→ cross_department = {evidence['cross_department']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
