"""
Optimization contracts — ABSTRACTION ONLY (Blueprint §15; optimization_spec
§2/§5/§6/§10; PR-3).

Declares the two surfaces the Optimization boundary exposes. Every operation is
an `@abstractmethod` with a `...` body — this module implements no behavior.

    ObservationSource        — observe; produce observations
    ObservationPublication   — publish; expose what was observed and put forward

Both are **read-shaped**. Together they carry no verb that could reach outward:
no submit, send, notify, request, approve, promote, decide, or authorize appears
anywhere in this boundary. Per the P7-I27 Conflict A ruling, Optimization
publishes for **optional future consumption** and depends on Governance in no
way; the direction is inverted, so a consumer reads from Optimization rather
than Optimization calling a consumer.

Deliberately ABSENT (P7-I27 Conflict B ruling — Architect Reserved): signal
catalogue, evaluation scoring, prioritization model, optimization algorithm,
recommendation engine, ranking model, decision heuristics, promotion strategy.
No such surface is declared here, so none can be supplied by a realization
without first extending this contract under a future authorization.

Ownership: Optimization owns non-authoritative observations and proposals only.
Trace keeps immutable history (INV-5) · Memory keeps derivation · Knowledge
keeps semantics · Governance keeps authority (PR-3; INV-8) · Infrastructure
keeps facilities. No ownership is transferred here.

Dependencies: this package's `observation` and `proposals` only. Stdlib
otherwise. No module state, no singleton, no registry, no reflection.
"""

from __future__ import annotations

import abc
from typing import Tuple

from .observation import OptimizationObservation
from .proposals import OptimizationProposal


class ObservationSource(abc.ABC):
    """A place observations are read from.

    Detect-only: a source transcribes what it reads and evaluates nothing. It
    selects nothing, ranks nothing, and scores nothing — those are reserved."""

    @abc.abstractmethod
    def observe(self) -> "Tuple[OptimizationObservation, ...]":
        """Return every record this source currently holds, as observations, in
        the order read.

        Completeness is the contract: an implementation transcribes all records
        and filters none. Filtering would be selection, and selection is a
        judgement this boundary is not permitted to make (PR-3)."""
        ...


class ObservationPublication(abc.ABC):
    """What Optimization publishes, exposed for optional future consumption.

    Read-only in both directions: nothing here reaches a consumer, and nothing
    here accepts a decision. A consumer may read; Optimization never calls
    one."""

    @abc.abstractmethod
    def published(self) -> "Tuple[OptimizationObservation, ...]":
        """The observations recorded, in the order observed. Non-authoritative:
        Trace remains the authoritative history (INV-5)."""
        ...

    @abc.abstractmethod
    def proposals(self) -> "Tuple[OptimizationProposal, ...]":
        """The proposals put forward. Published, not submitted — Governance is
        not called, and nothing here promotes or authorizes (PR-3; INV-8)."""
        ...
