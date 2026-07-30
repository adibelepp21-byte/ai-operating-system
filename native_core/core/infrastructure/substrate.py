"""
Execution substrate facility (Infrastructure spec §2, §5c; Blueprint §14, §23).

Provides the execution substrate *to Runtime* (Infrastructure spec §5c) —
the facility beneath the Runtime subsystem on which Agent Instances will
later be hosted. Stage I provides the substrate as a facility boundary only:
Runtime is out of scope, so this module contains NO hosting logic, NO
scheduling, NO allocation, and NO execution — those belong to Runtime
(runtime_spec), not to Infrastructure.

What this facility legitimately provides beneath Runtime is the notion of a
provisioned, releasable substrate handle whose lifecycle is subordinate to
the invoking action (spec §4), and which authors no independent Trace
(OQ-2; spec §9). The concrete substrate backend is replaceable beneath the
entities and is [O] reserved (spec §12/§13); this module fixes the boundary,
not the backend.

Strictly local: holds NO external dependency (INV-12); owns no Knowledge;
makes no governance decision (spec §8-§10).
"""

from __future__ import annotations

import abc

from .facility import Facility


class ExecutionSubstrate(Facility):
    """Abstract substrate beneath Runtime.

    Concrete substrate backends are replaceable and reserved (spec §12/§13).
    The facility fixes only that a substrate is provisioned and released as a
    subordinate facility, and that it is not itself an actor: it hosts nothing
    on its own and authors no Trace. Runtime (a later stage) will drive
    execution *on* a substrate; the substrate does not drive itself.
    """

    name = "execution-substrate"

    @abc.abstractmethod
    def is_available(self) -> bool:
        """Report whether the substrate can currently host execution.

        This is a facility-health question, not an execution action — it
        produces no Trace and makes no decision. Runtime consults it; the
        substrate does not act on the answer itself."""


class LocalExecutionSubstrate(ExecutionSubstrate):
    """The minimal in-process substrate boundary.

    Represents "execution happens in this local process." It provisions no
    external resource and holds no external dependency (INV-12). It contains
    no hosting/scheduling logic — that is Runtime's, reserved to a later
    stage. It exists so Runtime has a substrate facility to be handed, and so
    the dependency direction (Runtime → Infrastructure substrate) has a real
    endpoint from Stage I onward.
    """

    name = "execution-substrate.local"

    def _provision(self) -> None:
        # No external resource to establish; the local process is the
        # substrate. Nothing here starts a thread, process, connection, or
        # scheduler — that would be Runtime behaviour and is out of scope.
        return None

    def is_available(self) -> bool:
        return self.is_ready
