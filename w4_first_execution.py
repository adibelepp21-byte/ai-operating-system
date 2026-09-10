"""Entry point for the first real W4 execution — `ACT-CC-P11-008 §21`.

**Why this file is at the repository root and not in `tools/` or `consumers/`.**

The run needs two things that live in mutually isolated regions: the authority
chain machinery in `tools/`, and the resident agent in `consumers/` that the
Engineering Intelligence Capability record names as realizing the Testing
sub-ability. Those regions may not reach each other —
`consumers/tests/test_reference_agent.py` asserts that nothing under `tools/`
imports `consumers`, and three consumer suites assert the reverse.

Both assertions are AST-based, so an import inside an `if __name__` guard counts
exactly as a top-level one does. That is right: an import inside a guard is still
an edge in the dependency graph, and a boundary that held only at module scope
would not be a boundary.

**So the wiring has nowhere to live except outside both**, which is what this
file is. It is an entry point, not a region: no package, no `__init__`, nothing
imports it.

I found this the way it should be found — by violating it. The first version of
`tools/w4_first_run.py` imported the consumer directly, the invariant failed, and
the resolution improved the design: `run()` now takes an injected performer, so
the machinery that enforces the authority chain no longer knows which module does
the work. A Delegation names an **instance and a capability**, never an
implementation, and the code now matches that.

Run:  ``python3 w4_first_execution.py``
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from consumers.engineering_intelligence_agent import (  # noqa: E402
    Artifact,
    ConformanceCriterion,
    EngineeringIntelligenceAgent,
)
from tools.w4_first_run import SUBJECT, run  # noqa: E402


def verify(lines, criterion_names):
    """The delegated work, performed by the resident consumer.

    `ACT-CC-P11-008 §21` requires *"actual execution machinery"*. This is it:
    `EngineeringIntelligenceAgent.verify` is the Testing sub-ability the
    Engineering Intelligence Capability record says the consumer realizes, and
    the record adds that the consumer *"holds no authority"* — which is why it
    can be the performer without being the authority.
    """
    agent = EngineeringIntelligenceAgent()
    criteria = tuple(ConformanceCriterion(name=name, required_text=name)
                     for name in criterion_names)
    results = agent.verify(Artifact(name=SUBJECT.name, lines=lines), criteria)
    return {result.criterion_name: result.satisfied for result in results}


def main() -> int:
    evidence = run(verify)
    print(json.dumps({key: evidence[key] for key in (
        "agent_definition", "agent_instance", "delegation_id",
        "authority_chain", "criteria_total", "criteria_satisfied",
        "criteria_unsatisfied", "boundary_crossed")}, indent=2))
    for outcome in evidence["outcomes"]:
        print(f"  {outcome['status']:<10} {outcome['step']:<28} "
              f"{outcome['detail']}")
    return 1 if evidence["boundary_crossed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
