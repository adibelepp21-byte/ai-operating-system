"""
Facility lifecycle foundation (Infrastructure spec §4; Blueprint §14, §19).

A Facility is a capability that sits *beneath* the entities — storage, the
external boundary, the execution substrate — provisioned, used within an
invoking action, and released, always subordinate to that action
(Infrastructure spec §4). A Facility is NOT an entity, NOT an actor, and
authors NO independent Trace (OQ-2; Infrastructure spec §9). It serves; it
does not govern (Infrastructure spec §10).

This module defines the common lifecycle every Infrastructure facility
obeys, and nothing more. It contains no storage, no external coupling, and
no governance — those live in the specific facilities that inherit this
base.

Fail Closed (PR-4; Infrastructure spec §11): a facility that has not been
provisioned, or whose provisioning failed, must refuse use rather than
silently degrade. `require_ready()` is how a facility (and the bootstrap
orchestrator) enforces that.
"""

from __future__ import annotations

import abc
from enum import Enum


class FacilityState(Enum):
    """The lifecycle states a facility moves through (Infrastructure spec §4).

    DECLARED   — constructed, not yet provisioned; unusable.
    PROVISIONED — provisioned successfully; usable.
    RELEASED   — released; unusable again.
    FAILED     — provisioning failed; unusable, terminal until re-declared.
    """

    DECLARED = "declared"
    PROVISIONED = "provisioned"
    RELEASED = "released"
    FAILED = "failed"


class FacilityUnavailable(RuntimeError):
    """Raised when a facility is used while not PROVISIONED.

    This is the concrete shape of Fail Closed for facilities: the invoking
    action halts accountably (the exception propagates to it) rather than
    receiving a degraded or partial facility (Infrastructure spec §11).
    """


class Facility(abc.ABC):
    """Base for every Infrastructure facility.

    Subclasses implement `_provision()` (establish the underlying capability)
    and `_release()` (tear it down). Neither may author Trace, own Knowledge,
    hold a non-Tool external dependency, or make a governance decision — those
    are forbidden here (Infrastructure spec §8, §9, §10; INV-12).
    """

    #: Human-readable facility name, for diagnostics only (not an identity,
    #: not a canonical key — Infrastructure owns no entity).
    name: str = "facility"

    def __init__(self, name: str | None = None):
        if name is not None:
            self.name = name
        self._state = FacilityState.DECLARED

    @property
    def state(self) -> FacilityState:
        return self._state

    @property
    def is_ready(self) -> bool:
        return self._state is FacilityState.PROVISIONED

    def provision(self) -> None:
        """Establish the underlying capability. Fail closed: on any error the
        facility becomes FAILED and the error propagates — it never comes up
        half-provisioned and reporting ready."""
        if self._state is FacilityState.PROVISIONED:
            return  # idempotent: provisioning an already-ready facility is a no-op
        try:
            self._provision()
        except Exception:
            self._state = FacilityState.FAILED
            raise
        self._state = FacilityState.PROVISIONED

    def release(self) -> None:
        """Release the underlying capability. Safe to call in any state;
        after it the facility is RELEASED and must be re-provisioned before
        further use."""
        if self._state is FacilityState.PROVISIONED:
            self._release()
        self._state = FacilityState.RELEASED

    def require_ready(self) -> None:
        """Fail closed if the facility is not PROVISIONED. Every usable
        operation on a concrete facility must call this first."""
        if self._state is not FacilityState.PROVISIONED:
            raise FacilityUnavailable(
                f"facility {self.name!r} is {self._state.value}, not provisioned"
            )

    # --- subclass contract ---

    @abc.abstractmethod
    def _provision(self) -> None:
        """Establish the capability. Must raise on failure (fail closed)."""

    def _release(self) -> None:
        """Tear down the capability. Default: nothing to release."""
        return None
