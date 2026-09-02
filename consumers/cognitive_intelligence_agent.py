"""
Phase 5 — `E5-2`, the Cognitive Intelligence first milestone.

`GDR-0005 §3.5.3` ratifies the criterion as a count, not a prose aspiration:

    a single unit of execution work is decomposed into two (2) or more ordered
    sub-steps, demonstrated on real execution rather than plan.

Its source is Volume VI §3.1 — *"modul Planning dasar yang dapat memecah satu
Execution Contract menjadi sub-langkah berurutan"* — and `GDR-0005` records that
the subject was deliberately *"generalised to keep the criterion
architecture-neutral, with the source term preserved here for traceability."*
That generalisation is load-bearing and this module honours it: what follows
realizes a **decomposition contract**, not a Planner.

**What this module is not, stated before what it is.** `DEC-PHASE5-SEMANTICS`
(Option B, Founder, 2026-08-21) excludes expanding Phase 5 *"into a canonical
entity named Intelligence, nor into Planner, Scheduler, Execution Orchestrator,
Cognitive Engine as a new entity"*, and the Phase 5 Construction Cycle records
`T-6` Planner as **NOT AUTHORIZED**. So:

  - no canonical entity is introduced — the Architecture Freeze entity set stays
    at **twelve** and the core region stays at **eleven** boundaries;
  - nothing here is registered into `native_core/`, which this work does not
    touch at all;
  - this is an `ExecutionConsumer` realization, the same architectural species
    as `E-01` and the Phase 6 Knowledge consumer, and nothing more.

**What it is.** The concrete realization of the *Cognitive Intelligence Agent*
Definition, which is itself an approved artifact: `ADR-0008` (Approved)
established the Cognitive Intelligence Capability, and the Agent Definition at
`docs/architecture/organization/engineering/agent-definitions/cognitive-intelligence-agent.md`
declares exactly two authorized behaviours —

  - *"Decompose a unit of execution work into constituent sub-steps"*, and
  - *"Establish the order in which those sub-steps are to be carried out"* —

adding, decisively for this file: *"This Agent Definition produces decomposition
and ordering only; it does not itself carry out the work it decomposes."* There
is therefore no execution path here that runs a sub-step, and that absence is
asserted by the conformance tests rather than merely intended.

**Why it lives in `consumers/`.** Same reason as every other consumer: the Agent
contract boundary's suite pins it shut, and `DEC-P6-042` established that a
concrete implementation moves out rather than the boundary being weakened to let
it in. `native_core/` is unmodified by Phase 5.

**Decomposition is derived, never invented.** The unit of work states its own
sequence; this module reads that statement and preserves it. It fabricates no
sub-step that the stated work does not contain, and when a unit yields fewer
than two sub-steps it raises `IndecomposableUnitOfWork` rather than padding the
result to reach the number the criterion counts. Manufacturing a second sub-step
to satisfy `E5-2` would be measuring the measurement instead of the work —
`PR-4`, fail closed.

**Technology neutrality.** Engineering Constitution §6.2 invariant 1 forbids a
technology, language, framework, model, vendor or infrastructure decision, and
the Agent Definition's Runtime Requirements are stated *"only in the abstract"*.
Nothing here names or implies a model, provider, API or product; the
decomposition is a deterministic reading of stated structure.

Dependencies: the `Agent` contract, and the standard library. No Knowledge, no
Governance, no Memory, no Trace, no Runtime type — the hosting Runtime is
reached only through the `Execution` this consumer is handed, and is never
named.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence, Tuple

from native_core.core.agent import Agent
from native_core.core.trace import TraceWriter

from .observation import TracedAction, runtime_identity

#: The separators a unit of work may use to state its own ordering. These are
#: reading conventions for stated structure, not a grammar this module imposes:
#: a caller may instead supply already-separated steps, in which case no
#: separator is consulted at all.
SEQUENCE_SEPARATORS: Tuple[str, ...] = (";", " then ", " lalu ", " kemudian ")


class IndecomposableUnitOfWork(ValueError):
    """A stated unit of work yields fewer than two ordered sub-steps.

    Named rather than generic, because the condition is meaningful: `E5-2`
    counts sub-steps, and a unit that states only one step has not been
    decomposed. Raising keeps the criterion honest — the alternative, inventing
    a second sub-step, would satisfy the count while destroying what the count
    measures.
    """


@dataclass(frozen=True)
class SubStep:
    """One ordered constituent of a decomposed unit of work.

    Frozen, following the Native Core convention for data contracts: a
    decomposition that could be edited after the fact would not be evidence of
    what the Agent produced. `ordinal` is 1-based and dense, and expresses the
    *"order in which those sub-steps are to be carried out"* that the Agent
    Definition authorizes this Agent to establish.
    """

    ordinal: int
    description: str

    def __post_init__(self) -> None:
        if self.ordinal < 1:
            raise ValueError("a sub-step ordinal is 1-based")
        if not self.description.strip():
            raise ValueError("a sub-step must describe work")


class CognitiveIntelligenceAgent(Agent):
    """A concrete `Agent` realizing the Cognitive Intelligence Agent Definition,
    bounded to its recorded Phase 5 realization.

    The governing Capability declares three sub-abilities — Reasoning, Planning,
    Reflection — and records that only *"task decomposition"* and *"ordered
    planning"* are realized in Phase 5. This class implements those two and
    nothing adjacent to them: there is no reflection surface, no review
    surface, and no method that carries out decomposed work.
    """

    def __init__(self, unit_of_work: Optional[str] = None,
                 trace_writer: "Optional[TraceWriter]" = None) -> None:
        """Configure the unit of work this Agent will decompose when it
        participates. Left unset, participation completes having decomposed
        nothing — an explicit absence, never a fabricated decomposition."""
        self._trace_writer = trace_writer
        self._unit_of_work = unit_of_work
        self._decomposition: Tuple[SubStep, ...] = ()

    # -- observation ------------------------------------------------------

    @property
    def decomposition(self) -> Tuple[SubStep, ...]:
        """The ordered sub-steps produced by the most recent decomposition.

        Ordinary in-memory evidence for this Agent's own callers and tests —
        **not** a Trace. Trace is authored by the Runtime under INV-4, and
        nothing here writes or substitutes for it.
        """
        return self._decomposition

    # -- the realized Phase 5 elements -------------------------------------

    def decompose(self, unit_of_work: str) -> Tuple[SubStep, ...]:
        """*task decomposition* + *ordered planning* — read a stated unit of
        execution work and return its constituent sub-steps in stated order.

        The two authorized behaviours are one operation here because ordering is
        not a second pass over the result: the stated sequence *is* the order,
        and preserving it is what "establish the order" means when the work
        states its own. Nothing is reordered, scored, or optimized — that would
        be a judgement this Agent Definition does not authorize.

        Raises `IndecomposableUnitOfWork` when fewer than two sub-steps are
        stated, per `PR-4`.
        """
        parts = self._split(unit_of_work)
        if len(parts) < 2:
            raise IndecomposableUnitOfWork(
                "a unit of work must state two or more sub-steps to be decomposed; "
                f"{len(parts)} found in {unit_of_work!r}"
            )
        self._decomposition = tuple(
            SubStep(ordinal=index, description=text)
            for index, text in enumerate(parts, start=1)
        )
        return self._decomposition

    def decompose_stated_steps(self, steps: Sequence[str]) -> Tuple[SubStep, ...]:
        """The same operation for a unit of work whose steps are already
        separated by its caller, so that no separator convention is consulted.

        This exists because the separator list is a reading aid, not a
        requirement of the criterion: `E5-2` counts ordered sub-steps, and how
        the unit stated them is immaterial to whether it was decomposed.
        """
        parts = [text.strip() for text in steps if text and text.strip()]
        if len(parts) < 2:
            raise IndecomposableUnitOfWork(
                "a unit of work must state two or more sub-steps to be decomposed; "
                f"{len(parts)} found"
            )
        self._decomposition = tuple(
            SubStep(ordinal=index, description=text)
            for index, text in enumerate(parts, start=1)
        )
        return self._decomposition

    @staticmethod
    def _split(unit_of_work: str) -> Tuple[str, ...]:
        """Read the stated sequence. Deterministic, and it adds nothing: every
        returned fragment is a substring of what was handed in."""
        if not isinstance(unit_of_work, str):
            raise TypeError("a unit of execution work is stated as text")
        fragments = [unit_of_work]
        for separator in SEQUENCE_SEPARATORS:
            next_fragments: list = []
            for fragment in fragments:
                next_fragments.extend(fragment.split(separator))
            fragments = next_fragments
        return tuple(text.strip() for text in fragments if text and text.strip())

    # -- the Agent contract ------------------------------------------------

    def participate(self, execution: "object") -> None:
        """Participate in one bound Execution by decomposing the configured unit
        of work **during** that Execution.

        This is what `E5-2`'s *"demonstrated on real execution rather than
        plan"* asks for: the decomposition happens inside a participation
        handed out by a RUNNING Runtime, not in a document describing one.

        Completion is defined negatively, per `agent_execution_semantics_spec`
        §13.3: participation completes when this returns without raising. There
        is no result value because no result model is ratified — the
        decomposition is read from `decomposition`, and the return stays `None`.
        """
        with TracedAction(
            self._trace_writer,
            agent_instance="cognitive-intelligence-agent",
            runtime=runtime_identity(execution),
        ):
            if self._unit_of_work is not None:
                self.decompose(self._unit_of_work)
