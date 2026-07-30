"""
Bootstrap / initialization orchestration (Blueprint §19, §23; Infrastructure spec §4, §11).

The ordered establishment of facilities so that no facility is available
before the facilities it depends on (Blueprint §19). Bootstrap performs no
governance decision and creates no entity; it only makes facilities ready in
dependency order (Blueprint §19), and it respects Fail Closed: if a required
lower facility cannot be provisioned, dependents are not started (PR-4;
Infrastructure spec §11).

Scope discipline: Stage I bootstraps only Infrastructure facilities. Bootstrap
does NOT initialize Trace, Memory, Governance, or any other subsystem — none
exists yet, and initialization order across subsystems is the Roadmap's
concern, realized only as each stage is authorized. This module is the
*mechanism* for ordered, fail-closed establishment; it is not a launcher for
the whole system.

Dependency registration: facilities are registered with an explicit list of
the facility names they depend on. Bootstrap provisions them in a
topologically-safe order and refuses to provision a facility whose
dependencies are unmet or failed. A dependency cycle is itself a fail-closed
error (the Native Core graph is acyclic — Blueprint §21).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .facility import Facility, FacilityState


class BootstrapError(RuntimeError):
    """Raised when facilities cannot be established in a valid order.

    Covers unknown dependencies, dependency cycles, and the failure of a
    required facility. Every case is fail closed: bootstrap stops and no
    dependent facility is provisioned."""


@dataclass
class _Registration:
    facility: Facility
    depends_on: tuple  # names of facilities this one requires


@dataclass
class Bootstrap:
    """Registers Infrastructure facilities and provisions them in dependency
    order, fail closed.

    Usage is register-then-establish: register every facility with its
    dependencies, then call `establish()` once. `establish()` provisions each
    facility after its dependencies, halting at the first failure with the
    partially-established facilities left in a known state (provisioned ones
    stay provisioned; the failed one is FAILED; un-reached ones stay
    DECLARED). `teardown()` releases in reverse order.
    """

    _registry: dict = field(default_factory=dict)
    _order: list = field(default_factory=list)  # provisioned order, for reverse teardown
    _established: bool = False

    def register(self, name: str, facility: Facility, depends_on=()) -> None:
        """Register a facility under a name, with the names of the facilities
        it depends on. Fail closed on a duplicate name."""
        if self._established:
            raise BootstrapError("cannot register after establish() has run")
        if not name or not name.strip():
            raise BootstrapError("facility name must be non-empty")
        if name in self._registry:
            raise BootstrapError(f"facility name already registered: {name!r}")
        self._registry[name] = _Registration(facility=facility, depends_on=tuple(depends_on))

    def _resolution_order(self) -> list:
        """Topological order of registered facilities. Fail closed on an
        unknown dependency or a cycle."""
        resolved: list = []
        resolved_set: set = set()
        # Deterministic iteration for a stable, reviewable order.
        pending = dict(sorted(self._registry.items()))

        # Validate dependency references up front (fail closed on unknowns).
        for name, reg in pending.items():
            for dep in reg.depends_on:
                if dep not in self._registry:
                    raise BootstrapError(f"facility {name!r} depends on unknown facility {dep!r}")

        # Kahn-style resolution with cycle detection.
        while pending:
            progressed = False
            for name in list(pending):
                deps = pending[name].depends_on
                if all(d in resolved_set for d in deps):
                    resolved.append(name)
                    resolved_set.add(name)
                    del pending[name]
                    progressed = True
            if not progressed:
                raise BootstrapError(
                    f"dependency cycle among facilities: {sorted(pending)} (graph must be acyclic)"
                )
        return resolved

    def establish(self) -> None:
        """Provision every registered facility in dependency order. Fail
        closed: on the first provisioning failure, stop; dependents are not
        provisioned."""
        if self._established:
            raise BootstrapError("establish() has already run")
        order = self._resolution_order()
        for name in order:
            reg = self._registry[name]
            # Refuse to start a facility whose dependency did not come up
            # ready (defence in depth beyond ordering — fail closed).
            for dep in reg.depends_on:
                if not self._registry[dep].facility.is_ready:
                    raise BootstrapError(
                        f"cannot provision {name!r}: dependency {dep!r} is "
                        f"{self._registry[dep].facility.state.value}, not provisioned"
                    )
            reg.facility.provision()  # raises on failure -> propagates, halts establish()
            self._order.append(name)
        self._established = True

    def teardown(self) -> None:
        """Release established facilities in reverse order."""
        for name in reversed(self._order):
            self._registry[name].facility.release()
        self._order.clear()
        self._established = False

    def get(self, name: str) -> Facility:
        """Resolve a registered facility by name. Fail closed if unknown."""
        if name not in self._registry:
            raise BootstrapError(f"unknown facility: {name!r}")
        return self._registry[name].facility

    @property
    def established(self) -> bool:
        return self._established

    def states(self) -> dict:
        """Diagnostic snapshot of every facility's lifecycle state."""
        return {name: reg.facility.state for name, reg in sorted(self._registry.items())}
