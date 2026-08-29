"""
Phase 8 Tool registry — registration and lifecycle authority (`FD-P8-001 §4.2`,
`§4.3`; `ACT-CC-P8-001 §5.3`, `§5.4` — `E8-01`, `E8-02`).

`FD-P8-001 §4.2` states the rule this module exists to enforce:

> *"No valid registration → no lawful invocation."*

The registry owns Tool **lifecycle authority**: define, register, enable,
disable, retire, and the eligibility question that the invocation governance
layer asks before any Tool runs. `ACT-CC-P8-001 §5.4` places that authority here
— *"Tool lifecycle authority shall reside within the Tool capability layer"* —
and `§8.3` withholds it from Runtime, which *"shall not own Tool registration
authority, Tool lifecycle authority, Tool governance decision authority."*

**A registry is a lookup facility, not an actor.** Blueprint §17 says so, and
`tool_boundary.py` already records it. This registry decides lifecycle state
transitions and reports eligibility; it does not invoke, does not execute, and
does not decide whether a *caller* is authorized — that is the invocation
governance layer's question, and keeping the two apart is what stops the registry
from quietly becoming the governance gate.

**Registration is two-sided, deliberately.** A Tool is registered here (its
descriptor and lifecycle) *and* at the existing `ToolBoundary` (its executable
attachment). Both are required before invocation: the descriptor alone describes
a Tool that cannot run, and a boundary attachment alone is an implementation with
no governed identity. `E8-02` needs exactly this — a Tool that is *known* but not
*eligible* must be distinguishable from one that is both.

Dependencies: stdlib, `shared`, and this package. No sibling core boundary.
"""

from __future__ import annotations

from typing import Dict, Optional, Tuple

from .tool_lifecycle import (
    InvalidToolDefinition,
    InvalidToolTransition,
    ToolContract,
    ToolDescriptor,
    ToolIdentity,
    ToolLifecycleError,
    ToolState,
)


class ToolNotDefined(ToolLifecycleError, KeyError):
    """An operation names a Tool the registry does not hold.

    Distinct from a Tool being ineligible: asking to enable a Tool that was never
    defined is an invalid *operation*, whereas invoking a disabled Tool is a
    lawful request with a refusal for an answer.
    """


class ToolAlreadyDefined(ToolLifecycleError, ValueError):
    """A Tool with this canonical key is already held.

    Fails closed rather than overwriting: silently replacing a registered Tool
    would let a later definition inherit an earlier one's enabled state, which is
    precisely the *"aliasing"* path `FD-P8-001 §4.3` forbids.
    """


class ToolRegistry:
    """Registration and lifecycle authority for Phase 8 Tools.

    Holds descriptors keyed by canonical key. It has no reference to the
    invocation path, no caller model and no execution capability — it cannot
    invoke a Tool even by accident.
    """

    def __init__(self) -> None:
        self._tools: Dict[str, ToolDescriptor] = {}

    # -- definition and registration --------------------------------------

    def define(
        self,
        identity: ToolIdentity,
        contract: ToolContract,
        metadata: "Optional[dict]" = None,
    ) -> ToolDescriptor:
        """Define a Tool without registering it (`Defined`).

        The descriptor exists and is addressable, and is **not** invocable: a
        defined-but-unregistered Tool is the first negative control `E8-01.6`
        asks for.
        """
        if not isinstance(identity, ToolIdentity):
            raise InvalidToolDefinition("define requires a ToolIdentity")
        key = identity.canonical_key
        if key in self._tools:
            raise ToolAlreadyDefined(f"a Tool is already defined at {key!r}")
        descriptor = ToolDescriptor(
            identity=identity,
            contract=contract,
            state=ToolState.DEFINED,
            metadata=metadata or {},
        )
        self._tools[key] = descriptor
        return descriptor

    def register(self, canonical_key: str) -> ToolDescriptor:
        """`Defined → Registered`. Known to the ecosystem, not yet eligible."""
        return self._transition(canonical_key, ToolState.REGISTERED)

    def enable(self, canonical_key: str) -> ToolDescriptor:
        """`Registered | Disabled → Enabled`. The only invocable state."""
        return self._transition(canonical_key, ToolState.ENABLED)

    def disable(self, canonical_key: str) -> ToolDescriptor:
        """`Enabled → Disabled`. Reversible; the Tool stops being invocable
        immediately, with no grace path and no fallback."""
        return self._transition(canonical_key, ToolState.DISABLED)

    def retire(self, canonical_key: str) -> ToolDescriptor:
        """`Registered | Enabled | Disabled → Retired`. Terminal.

        A retired Tool has no lawful transition back. `FD-P8-001 §8.3` requires
        that *"no fallback, alias, or public bypass may silently restore
        eligibility"*, and terminality is how that is guaranteed rather than
        merely intended.
        """
        return self._transition(canonical_key, ToolState.RETIRED)

    # -- lookup (no decision) ----------------------------------------------

    def describe(self, canonical_key: str) -> Optional[ToolDescriptor]:
        """The descriptor at a key, in whatever state, or `None`.

        An explicit absence, never a fabricated descriptor. The governance layer
        turns that absence into a structured refusal; the registry does not
        decide what absence means.
        """
        return self._tools.get(canonical_key)

    def is_registered(self, canonical_key: str) -> bool:
        """Whether the key names a Tool that has at least been registered.

        `DEFINED` is not registered — `FD-P8-001 §4.2` makes registration the
        gate, and a merely defined Tool has not passed it.
        """
        descriptor = self._tools.get(canonical_key)
        return descriptor is not None and descriptor.state is not ToolState.DEFINED

    def is_invocable(self, canonical_key: str) -> bool:
        """Whether lifecycle state currently permits invocation.

        One input to the governance decision, not the decision itself.
        """
        descriptor = self._tools.get(canonical_key)
        return descriptor is not None and descriptor.is_invocable

    def keys(self) -> Tuple[str, ...]:
        """Every canonical key the registry holds, in definition order."""
        return tuple(self._tools)

    def invocable_keys(self) -> Tuple[str, ...]:
        """Every key whose Tool is currently invocable."""
        return tuple(k for k, d in self._tools.items() if d.is_invocable)

    # -- internal ----------------------------------------------------------

    def _transition(self, canonical_key: str, state: ToolState) -> ToolDescriptor:
        descriptor = self._tools.get(canonical_key)
        if descriptor is None:
            raise ToolNotDefined(canonical_key)
        moved = descriptor.transition_to(state)  # raises InvalidToolTransition
        self._tools[canonical_key] = moved
        return moved
