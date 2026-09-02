"""
Composition root for the Phase 9 Workflow execution lifecycle
(`FD-P9-001`; `ACT-CC-P9-001 §8.1`).

The Runtime that hosts Workflow execution must be able to obtain an assembled
lifecycle **without constructing its internals**. That distinction is the whole
of `§8.3` — *"Hosting is not ownership"* — expressed in wiring: Runtime calls
`create_workflow_subsystem()` and holds what comes back, exactly as it already
does for Knowledge (`create_knowledge_subsystem`), Memory (`FD-P7-002`) and the
Tool Ecosystem (`ACT-CC-P8-001`). It never reaches inside.

The bundle carries the lifecycle authority and its read-only monitoring view as
**separate** references. A host given only this bundle can ask for a lawful
transition and can observe state; it cannot redefine what is lawful, and the
monitoring half cannot mutate anything at all.

Dependencies: this package only. No Runtime type is imported here and no
Runtime is named — the hosting edge runs Runtime → Workflow and not back, which
is what keeps `§8.3`'s prohibition on ownership inversion structural.
"""

from __future__ import annotations

from dataclasses import dataclass

from .lifecycle import WorkflowLifecycle, WorkflowMonitor


@dataclass(frozen=True)
class WorkflowSubsystem:
    """The assembled Phase 9 Workflow execution lifecycle.

    Frozen: a host that could swap the lifecycle out from under the monitor
    would be redefining lifecycle ownership, which `§11.2` reserves to the
    Workflow boundary.
    """

    lifecycle: WorkflowLifecycle
    monitor: WorkflowMonitor


def create_workflow_subsystem() -> WorkflowSubsystem:
    """Assemble the Workflow execution lifecycle and its monitoring view.

    Takes no collaborator. `§12.4` states that monitoring need not introduce a
    database, external observability infrastructure, distributed tracing,
    dashboards, schedulers or persistence engines, so nothing is injected and
    nothing is required — the subsystem is complete in itself, and a Workflow
    lifecycle begins empty because `§10.2` keeps *"zero Workflows"* a valid
    state.
    """
    lifecycle = WorkflowLifecycle()
    return WorkflowSubsystem(lifecycle=lifecycle, monitor=WorkflowMonitor(lifecycle))
