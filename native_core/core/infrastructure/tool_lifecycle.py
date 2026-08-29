"""
Phase 8 Tool representation and lifecycle (`FD-P8-001 §4.1`, `§4.3` — `E8-01`,
`E8-02`).

`FD-P8-001` fixes what a Tool is: *"an identified capability that has an
invocation contract, accepts invocation input, executes through the Tool
boundary, produces a structured outcome or structured failure/refusal, and is
subject to governance policy before execution."* Decisively — *"A Tool is not
merely an arbitrary callable."*

This module defines what a Tool **is** across its lifecycle. It holds no
registry, no governance and no invocation; those are siblings.

**Why it lives in `infrastructure/`.** Native Core Blueprint §14 names the
Infrastructure package as *"facilities beneath entities + **the single external
boundary (Tool)**"*, and §3 places *"the Tool boundary in infrastructure"* in the
Execution category. This is the Tool's canonical home, and
`ACT-CC-P8-001 §5.4` directs that *"the existing Tool capability shall evolve
rather than being replaced with a new core boundary."* The core region therefore
stays at **eleven** boundaries; no twelfth is introduced.

**What this module does not become.** `ToolBoundary` (`tool_boundary.py`) remains
the confinement facility it has always been — it still makes no governance
decision. Lifecycle *state* lives here; the lifecycle *decision* at invocation
time lives in `tool_invocation.py`, above the boundary, exactly where
`ACT-CC-P8-001 §6.1` places it.

**Lifecycle.** The canonical sequence from `FD-P8-001 §4.3`:

```text
Defined → Registered → Enabled → Invoked → Succeeded / Failed → Disabled / Retired
```

`Invoked / Succeeded / Failed` are properties of an *invocation*, not durable
states of the Tool — a Tool does not stop being enabled because one call failed.
They are therefore recorded on the invocation record (`tool_invocation.py`) while
the Tool's own durable states are those a registry can hold. `FD-P8-001 §4.3`
permits this: *"Implementation may represent lifecycle internally in a different
technical form, provided the canonical lifecycle semantics remain preserved."*

Dependencies: stdlib and `shared` only. No sibling core boundary is imported —
Blueprint §14 gives Infrastructure no such dependency, and Phase 8 adds none.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any, Mapping, Tuple


class ToolLifecycleError(Exception):
    """Base for Tool lifecycle and representation failures."""


class InvalidToolDefinition(ToolLifecycleError, ValueError):
    """A Tool identity, contract or descriptor is malformed.

    Raised at construction so a malformed Tool never exists to be registered.
    `E8-01` requires identity, contract, metadata and lifecycle state; an object
    missing one of them is not a Tool, and admitting it would make the criterion
    unmeasurable.
    """


class InvalidToolTransition(ToolLifecycleError):
    """A lifecycle transition is not lawful from the current state.

    `FD-P8-001 §4.3` requires that a disabled or retired Tool *"MUST NOT remain
    lawfully executable through fallback, aliasing, implicit discovery, or
    another public bypass path."* Retirement being terminal is part of that: a
    retired Tool that could be re-enabled would make retirement a suggestion.
    """


class ToolState(Enum):
    """The durable lifecycle states a registered Tool occupies.

    `DEFINED` is a Tool that exists as a description but has not been registered
    — it is not reachable through the invocation path at all. `REGISTERED` is
    known but not yet eligible: `FD-P8-001 §4.2` states that *"registration alone
    does not necessarily establish eligibility."* `ENABLED` is the single
    invocable state. `DISABLED` is reversible; `RETIRED` is terminal.
    """

    DEFINED = "defined"
    REGISTERED = "registered"
    ENABLED = "enabled"
    DISABLED = "disabled"
    RETIRED = "retired"


#: The only state in which a Tool may be invoked (`E8-02`). Everything else —
#: including `REGISTERED`, which is known but not yet enabled — is ineligible.
INVOCABLE_STATES: Tuple[ToolState, ...] = (ToolState.ENABLED,)

#: Lawful transitions. Retirement is terminal by design.
LAWFUL_TRANSITIONS: Mapping[ToolState, Tuple[ToolState, ...]] = MappingProxyType({
    ToolState.DEFINED: (ToolState.REGISTERED,),
    ToolState.REGISTERED: (ToolState.ENABLED, ToolState.RETIRED),
    ToolState.ENABLED: (ToolState.DISABLED, ToolState.RETIRED),
    ToolState.DISABLED: (ToolState.ENABLED, ToolState.RETIRED),
    ToolState.RETIRED: (),
})


def _freeze(value: Any) -> Any:
    """Deeply immutable snapshot, local to this boundary."""
    if isinstance(value, Mapping):
        return MappingProxyType({k: _freeze(v) for k, v in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(v) for v in value)
    return value


@dataclass(frozen=True)
class ToolIdentity:
    """A Tool's stable identity (`E8-01.1`).

    `canonical_key` is the identity the registry and the existing `ToolBoundary`
    both address a Tool by, so a Tool has **one** identity across the Phase 8
    layer and the Phase 3.1 confinement facility rather than two that could
    drift apart.
    """

    canonical_key: str
    version: str = "1"

    def __post_init__(self) -> None:
        if not isinstance(self.canonical_key, str) or not self.canonical_key.strip():
            raise InvalidToolDefinition("a Tool must carry a non-empty canonical key")
        if not isinstance(self.version, str) or not self.version.strip():
            raise InvalidToolDefinition("a Tool must carry a version")

    def __str__(self) -> str:
        return f"{self.canonical_key}@{self.version}"


@dataclass(frozen=True)
class ToolContract:
    """A Tool's invocation contract (`E8-01.2`).

    Names the actions the Tool accepts and the parameters each action requires.
    This is what makes an invocation *checkable before execution*: `E8-04`
    requires that an invalid invocation *"does not reach Tool execution"*, and
    that is only possible if validity can be decided from a declared contract
    rather than discovered by calling the Tool and seeing what happens.
    """

    actions: Tuple[str, ...]
    required_parameters: Mapping[str, Tuple[str, ...]] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.actions, tuple) or not self.actions:
            raise InvalidToolDefinition("a Tool contract must declare at least one action")
        for action in self.actions:
            if not isinstance(action, str) or not action.strip():
                raise InvalidToolDefinition("a declared action must be named")
        object.__setattr__(self, "required_parameters", _freeze(dict(self.required_parameters)))
        for action in self.required_parameters:
            if action not in self.actions:
                raise InvalidToolDefinition(
                    f"contract declares parameters for undeclared action {action!r}"
                )

    def declares(self, action: str) -> bool:
        return action in self.actions

    def missing_parameters(self, action: str, parameters: Mapping[str, Any]) -> Tuple[str, ...]:
        """Which required parameters an invocation omits. Reports; decides
        nothing — the governance layer decides what to do about it."""
        required = self.required_parameters.get(action, ())
        return tuple(name for name in required if name not in parameters)


@dataclass(frozen=True)
class ToolDescriptor:
    """A Tool as the Phase 8 layer represents it (`E8-01`).

    Carries all four required elements: **identity**, **invocation contract**,
    **capability metadata**, and **lifecycle state**. Frozen — a descriptor whose
    state could be reassigned by whoever holds a reference would make every
    eligibility guarantee unenforceable, so transitions produce new descriptors
    (`transition_to`).
    """

    identity: ToolIdentity
    contract: ToolContract
    state: ToolState
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.identity, ToolIdentity):
            raise InvalidToolDefinition("a Tool descriptor requires a ToolIdentity")
        if not isinstance(self.contract, ToolContract):
            raise InvalidToolDefinition("a Tool descriptor requires a ToolContract")
        if not isinstance(self.state, ToolState):
            raise InvalidToolDefinition("a Tool descriptor requires a ToolState")
        object.__setattr__(self, "metadata", _freeze(dict(self.metadata)))

    @property
    def canonical_key(self) -> str:
        return self.identity.canonical_key

    @property
    def is_invocable(self) -> bool:
        """Whether lifecycle state permits invocation (`E8-02`). One condition
        among several — registration and contract validity are checked
        separately, and all must hold."""
        return self.state in INVOCABLE_STATES

    def transition_to(self, state: "ToolState") -> "ToolDescriptor":
        """Produce the same Tool in a new lawful state.

        Refuses an unlawful transition rather than coercing it. Identity,
        contract and metadata are preserved, so a Tool remains the same Tool
        across its lifecycle even as its eligibility changes.
        """
        if not isinstance(state, ToolState):
            raise InvalidToolTransition("a transition target must be a ToolState")
        allowed = LAWFUL_TRANSITIONS[self.state]
        if state not in allowed:
            raise InvalidToolTransition(
                f"{self.identity} cannot move {self.state.value!r} → {state.value!r}; "
                f"lawful targets are {tuple(s.value for s in allowed)!r}"
            )
        return ToolDescriptor(
            identity=self.identity,
            contract=self.contract,
            state=state,
            metadata=self.metadata,
        )
