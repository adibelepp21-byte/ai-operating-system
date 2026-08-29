"""
Phase 8 Tool Ecosystem composition root — dependency wiring only.

Mirrors the resident Knowledge and Memory composition roots rather than
inventing a third assembly style: it instantiates the Tool Ecosystem components
and wires them by constructor injection, contains no business logic, and holds no
state after returning.

Wiring graph (constructor injection only):

    ToolRegistry                                  (lifecycle authority)
    ToolBoundary            (Phase 3.1 confinement + execution foundation)
    InvocationLedger                              (verifiable invocation record)
        └─► ToolInvocationGovernance(registry, boundary, ledger)
                                                  (the wrapper above the boundary)

Ownership after construction is unchanged: the registry owns lifecycle; the
boundary owns confinement and execution; the ledger owns evidence; the governance
wrapper owns the invocation decision. The composition root owns none of them, and
a Runtime holding this bundle owns none of them either — `ACT-CC-P8-001 §8.3`
keeps Runtime an access host, and handing it an assembled bundle is what lets
that stay true.

The boundary is provisioned here because it is a `Facility` and an unprovisioned
facility fails closed on use; provisioning at assembly means the subsystem a
caller receives is usable or the assembly failed loudly.

Dependencies: this package and stdlib.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

from .tool_boundary import ToolBoundary
from .tool_invocation import (
    CallerClass,
    InvocationLedger,
    ToolInvocationGovernance,
)
from .tool_registry import ToolRegistry


@dataclass(frozen=True)
class ToolSubsystem:
    """The assembled Phase 8 Tool Ecosystem — an immutable bundle of the wired
    components. Exposes exactly the four collaborators and nothing else: no
    helper, no shortcut, and in particular no path that reaches `boundary.invoke`
    without passing `governance`."""

    registry: ToolRegistry
    governance: ToolInvocationGovernance
    boundary: ToolBoundary
    ledger: InvocationLedger


def create_tool_subsystem(
    authorized_callers: "Optional[Tuple[CallerClass, ...]]" = None,
) -> ToolSubsystem:
    """Assemble the Phase 8 Tool Ecosystem by constructor injection only.

    An optional authorized-caller set is the single policy input; everything else
    is structure. Repeated calls produce an identical graph topology over
    independent state.
    """
    registry = ToolRegistry()
    boundary = ToolBoundary()
    boundary.provision()
    ledger = InvocationLedger()
    governance = ToolInvocationGovernance(
        registry=registry,
        boundary=boundary,
        ledger=ledger,
        authorized_callers=authorized_callers,
    )
    return ToolSubsystem(
        registry=registry, governance=governance, boundary=boundary, ledger=ledger
    )
