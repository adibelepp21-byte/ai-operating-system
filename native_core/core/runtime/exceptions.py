"""
Runtime fail-closed exceptions (Blueprint §6; runtime_spec §11; PR-4).

The named halt conditions of the Runtime boundary. Every one expresses Fail
Closed (PR-4; runtime_spec §11): a Runtime operation that cannot proceed
accountably raises rather than degrading, and never proceeds on an invalid
lifecycle state.

Named `RuntimeSubsystemError` (not `RuntimeError`) so the builtin is never
shadowed. Ownership: Runtime. Dependencies: none (stdlib only). Prohibited:
carrying any authority, decision, or state (§6.2 invariant 2).
"""

from __future__ import annotations


class RuntimeSubsystemError(RuntimeError):
    """Base for every fail-closed Runtime halt (PR-4)."""


class InvalidLifecycleTransition(RuntimeSubsystemError):
    """Raised when a lifecycle transition is not permitted from the current
    state. Fail closed: the transition is refused and the state is unchanged —
    there is no implicit startup and no silent recovery."""


class RuntimeNotRunning(RuntimeSubsystemError):
    """Raised when a hosted resource or execution context is requested while the
    Runtime is not RUNNING. Fail closed: subsystem access is never granted
    outside the running state."""


class InvalidRuntimeConfiguration(RuntimeSubsystemError):
    """Raised when the Runtime cannot be constructed accountably — a missing or
    wrong-typed injected dependency, or an absent runtime identity. Fail closed:
    an unconfigurable Runtime is never coerced into a usable one."""
