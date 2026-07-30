"""
Execution-layer fail-closed exceptions (Blueprint §6; runtime_spec §11; PR-4).

The Execution layer is **Runtime-owned internal structure**, so its errors extend
the Runtime boundary's error taxonomy (`RuntimeSubsystemError`) rather than
introducing a parallel one.

Every error here expresses Fail Closed (PR-4): an execution boundary that cannot
be formed accountably raises rather than degrading. These carry no authority, no
decision, and no state (§6.2 invariant 2).
"""

from __future__ import annotations

from ..exceptions import RuntimeSubsystemError


class ExecutionError(RuntimeSubsystemError):
    """Base for every fail-closed Execution-layer halt (PR-4)."""


class InvalidExecutionConfiguration(ExecutionError):
    """Raised when an execution boundary cannot be constructed accountably — a
    missing or wrong-typed injected dependency. Fail closed: an unconfigurable
    execution boundary is never coerced into a usable one."""
