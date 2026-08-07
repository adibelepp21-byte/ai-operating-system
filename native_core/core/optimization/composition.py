"""
Optimization composition root — dependency wiring and detect-only sources
(Blueprint §15; optimization_spec §2/§4/§7; PR-3; PR-4).

The single canonical construction point for the Optimization object graph, and
the home of the two detect-only sources it wires. It follows the Knowledge
precedent, whose composition root likewise carries the assembled bundle
alongside its factory.

Wiring graph (dependency order):

    TraceReader  ─► TraceObservationSource  ─┐
    MemoryReader ─► MemoryObservationSource ─┴─► PassiveObservationPublication

Both readers are **injected, never constructed here**: their lifecycle belongs
to whoever established them, so this root takes no ownership of them.

Direction of dependency (P7-I27 Conflict A ruling): Optimization reads Trace and
Memory, and depends on Governance in **no** way. Nothing here submits, sends,
notifies, requests, promotes, authorizes, or decides. The publication is left to
be read; no consumer is ever called.

Deliberately ABSENT (P7-I27 Conflict B ruling — Architect Reserved): every form
of judgement. The sources transcribe **all** records, in the order read, with no
filter, no selection, no ordering change, no counting, no threshold, and no
score. Proposals are **injected**, never derived — deriving them would require
the reserved evaluation and prioritization models, so the boundary carries none.

Freshness: every call constructs a **new** graph. No caching, no memoization, no
lazy wiring, no module state, no singleton, no registry, no service locator, no
reflection, no dynamic import, no timestamp, no UUID, no randomness, no thread,
no async.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence, Tuple

from ..memory import MemoryReader
from ..trace import TraceReader
from .contract import ObservationPublication, ObservationSource
from .exceptions import InvalidOptimizationConfiguration
from .observation import MEMORY_SOURCE, TRACE_SOURCE, OptimizationObservation
from .proposals import OptimizationProposal


@dataclass(frozen=True)
class TraceObservationSource(ObservationSource):
    """Transcribes Trace records into observations. Reads only."""

    _reader: "TraceReader"

    def __post_init__(self):
        if not isinstance(self._reader, TraceReader):
            raise InvalidOptimizationConfiguration(
                "TraceObservationSource requires a TraceReader"
            )

    def observe(self) -> "Tuple[OptimizationObservation, ...]":
        # Every record, in the order read. No filter, no threshold, no ordering
        # change: selection would be a judgement (PR-3).
        return tuple(
            OptimizationObservation(
                source=TRACE_SOURCE,
                subject=record.agent_instance,
                observed=record,
            )
            for record in self._reader.read()
        )


@dataclass(frozen=True)
class MemoryObservationSource(ObservationSource):
    """Transcribes Memory records into observations. Reads only."""

    _reader: "MemoryReader"

    def __post_init__(self):
        if not isinstance(self._reader, MemoryReader):
            raise InvalidOptimizationConfiguration(
                "MemoryObservationSource requires a MemoryReader"
            )

    def observe(self) -> "Tuple[OptimizationObservation, ...]":
        return tuple(
            OptimizationObservation(
                source=MEMORY_SOURCE,
                subject=record.scope,
                observed=record,
            )
            for record in self._reader.read()
        )


@dataclass(frozen=True)
class PassiveObservationPublication(ObservationPublication):
    """An immutable publication: what was observed, and what was put forward.

    Passive by construction — it holds its content and exposes it. It calls
    nobody, notifies nobody, and accepts no decision."""

    _observations: "Tuple[OptimizationObservation, ...]"
    _proposals: "Tuple[OptimizationProposal, ...]"

    def __post_init__(self):
        for name, value, element in (
            ("observations", self._observations, OptimizationObservation),
            ("proposals", self._proposals, OptimizationProposal),
        ):
            if not isinstance(value, tuple):
                raise InvalidOptimizationConfiguration(f"{name} must be a tuple")
            for item in value:
                if not isinstance(item, element):
                    raise InvalidOptimizationConfiguration(
                        f"every element of {name} must be a {element.__name__}"
                    )

    def published(self) -> "Tuple[OptimizationObservation, ...]":
        return self._observations

    def proposals(self) -> "Tuple[OptimizationProposal, ...]":
        return self._proposals


def create_optimization(
    trace_reader: "TraceReader",
    memory_reader: "MemoryReader",
    proposals: "Sequence[OptimizationProposal]" = (),
) -> "ObservationPublication":
    """Assemble a fresh Optimization publication by constructor injection.

    Observes Trace first, then Memory, and publishes the result. Proposals are
    supplied by the caller and passed through unchanged: deriving a proposal
    would require the reserved evaluation and prioritization models, so this
    boundary derives none.

    Fail closed on a missing or wrong-typed reader (PR-4).
    """
    if not isinstance(trace_reader, TraceReader):
        raise InvalidOptimizationConfiguration(
            "create_optimization requires a Trace TraceReader"
        )
    if not isinstance(memory_reader, MemoryReader):
        raise InvalidOptimizationConfiguration(
            "create_optimization requires a Memory MemoryReader"
        )
    if isinstance(proposals, (str, bytes)) or not hasattr(proposals, "__iter__"):
        raise InvalidOptimizationConfiguration("proposals must be a sequence")

    observations = (
        TraceObservationSource(_reader=trace_reader).observe()
        + MemoryObservationSource(_reader=memory_reader).observe()
    )
    return PassiveObservationPublication(
        _observations=observations,
        _proposals=tuple(proposals),
    )
