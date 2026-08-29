"""
Tool boundary (Infrastructure spec §2, §5b, §10, §12; INV-12; Blueprint §14, §17).

The **single external boundary** of AIOS. INV-12: Tool is the only entity
type permitted to hold a direct external/vendor dependency; no other entity
may integrate with an outside system directly. Infrastructure's job here is
to *confine* all external coupling to this one boundary — to provide the
place where a Tool (built later, out of Stage I scope) would attach an
external capability, and to guarantee nothing else in the Native Core has
such a place.

Stage I builds the boundary as an ABSTRACTION ONLY. Per the Phase 3.1
directive and Infrastructure spec §5b/§12:
  - it defines the contract an external Tool must satisfy,
  - it provides a registration facility (Blueprint §17: a registry is a
    lookup facility, not an actor) so Tools can be registered and resolved
    by canonical key,
  - it connects to NOTHING external and holds NO external dependency itself
    (this module imports only the standard library and `shared`),
  - it authors no Trace and makes no governance decision (spec §9, §10).

External failures, when real Tools eventually exist, must surface through
this boundary rather than silently (spec §11). The boundary contract makes
that explicit: a Tool invocation returns an Outcome (Success | Failure),
never a silently-degraded value.
"""

from __future__ import annotations

import abc

from ...shared import Failure, Outcome, Success
from .facility import Facility


class ExternalTool(abc.ABC):
    """Contract every external Tool must satisfy to attach at the boundary.

    This is the ONLY place in the Native Core where an external/vendor
    dependency may live (INV-12). Concrete Tools are NOT part of Stage I;
    this abstract contract exists so the boundary can hold them later without
    any other subsystem gaining external reach.

    A Tool is identified by a `canonical_key` (assigned by governance, not by
    Infrastructure) and exposes a single `invoke`. `invoke` must return an
    Outcome so that external failure surfaces through the boundary as a
    Failure, never as a silent or partial value (spec §11).
    """

    @property
    @abc.abstractmethod
    def canonical_key(self) -> str:
        """The governance-assigned canonical key of this Tool."""

    @abc.abstractmethod
    def invoke(self, action: str, parameters: dict) -> Outcome:
        """Perform the external action. Returns Success | Failure."""


class ToolAlreadyRegistered(ValueError):
    """Raised when a canonical key is registered twice. Fail closed."""


class ToolNotRegistered(KeyError):
    """Raised when an unknown Tool is requested. Fail closed."""


class ToolBoundary(Facility):
    """The single external boundary: a registration/resolution facility for
    Tools (Blueprint §17 — a registry is a facility, not an actor).

    Registers no Tools of its own and integrates with nothing external. It is
    a lookup facility: register a Tool by its canonical key, resolve it by
    that key, invoke it through the boundary. Because every external Tool
    resolves through this one facility, Infrastructure can guarantee INV-12
    structurally — there is nowhere else to attach external capability.
    """

    name = "tool-boundary"

    def __init__(self):
        super().__init__()
        self._tools: dict[str, ExternalTool] = {}

    def _provision(self) -> None:
        # Nothing external to establish. The boundary is ready to accept
        # registrations. (There is intentionally no network, socket, client,
        # or vendor handle created here — INV-12.)
        self._tools = {}

    def register(self, tool: ExternalTool) -> None:
        """Register an external Tool by its canonical key. Fail closed on a
        duplicate key rather than silently replacing an existing binding."""
        self.require_ready()
        key = tool.canonical_key
        if not key or not key.strip():
            raise ValueError("tool canonical_key must be non-empty")
        if key in self._tools:
            raise ToolAlreadyRegistered(key)
        self._tools[key] = tool

    def is_registered(self, canonical_key: str) -> bool:
        self.require_ready()
        return canonical_key in self._tools

    def invoke(self, canonical_key: str, action: str, parameters: dict) -> Outcome:
        """Invoke a registered Tool through the boundary. Fail closed if the
        Tool is unknown; surface any Tool-reported failure as a Failure."""
        self.require_ready()
        tool = self._tools.get(canonical_key)
        if tool is None:
            raise ToolNotRegistered(canonical_key)
        outcome = tool.invoke(action, dict(parameters))
        # The boundary does not interpret success; it only guarantees the
        # shape. A Tool that returns a non-Outcome is itself violating the
        # contract — surface that as a Failure rather than passing it on.
        #
        # Repaired under `ACT-CC-P8-001 §10`. The previous guard tested
        # `hasattr(outcome, "__class__")`, which is true of every Python object
        # and therefore never fired: a Tool returning a bare string passed
        # straight through, contradicting this module's own documented
        # guarantee that invocation "returns an Outcome (Success | Failure),
        # never a silently-degraded value". The check now tests the actual
        # invariant. Repair authority is bounded to enforcing that existing
        # guarantee — no exception model is replaced and nothing else here is
        # redesigned.
        if not isinstance(outcome, (Success, Failure)):
            return Failure(
                reason=f"tool {canonical_key!r} returned a non-Outcome value",
                detail={"returned_type": type(outcome).__name__},
            )
        return outcome
