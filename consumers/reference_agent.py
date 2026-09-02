"""
E-01 — the first concrete execution consumer.

A realization of the `Agent` contract, resident outside
`native_core/core/agent/`. Its purpose is to demonstrate that the contract is
realizable: that a concrete consumer can be constructed, handed a bound
`Execution` by a running Runtime, and complete.

**Completion, per `agent_execution_semantics_spec` §13.3.** Participation
outcomes are exactly *rejected · completed · failed*, and completion is defined
negatively: a participation completes when `participate` returns and does not
raise. There is no success value, because no result model is ratified
(`consumer.py:75`). This consumer therefore returns `None`, and that return *is*
the completion signal.

**It does not reject.** §4 is explicit: *"Rejection is not the consumer's
decision to make about its own admission."* Both realized rejection conditions —
`RuntimeNotRunning` and `InvalidExecutionConfiguration` — are enforced at the
Runtime/Execution boundary before a consumer is reached, and *"a consumer that
refuses work it was given has failed, not rejected."*

**It adds no precondition check.** §13.2's four preconditions are enforced
upstream and structurally: `create_context` is RUNNING-gated, so an
`ExecutionContext` cannot be minted while the Runtime is not RUNNING;
`ExecutionSession.__post_init__` refuses a malformed binding; and `participate`
is abstract, so a non-implementor cannot be constructed. §17.2 states the rule
directly — *"Specifying preconditions does not authorize adding a precondition
check."* Re-checking upstream guarantees here would duplicate enforcement and
claim a gate this consumer does not hold.

**It manufactures no failure.** §5 places failure under `ExecutionError` and adds
no new base. This consumer has no work that can fail, so it declares no failure
condition it does not have — inventing one to look complete would be exactly the
implementation-by-implication §17.2 forbids.

**What it observes is not a Trace.** `participated_sequences` is ordinary
in-memory evidence that participation occurred, held by the consumer for its own
callers and tests. Trace is authored by the Runtime under INV-4 and is the only
durable record (`spec` §16); nothing here writes, reads, or substitutes for it.

Reaching `execution.context.execution_sequence` is precisely what residency
outside the core makes possible: inside `native_core/core/agent/` the identifier
constraint forbids naming the hosting Runtime at all, so the Execution boundary
could be received but never inspected.

Dependencies: the `Agent` contract only — the single public export of the agent
boundary. It imports no Execution type, no Runtime type, and nothing from
`tools/`. The `execution` it receives is used, never constructed.
"""

from __future__ import annotations

from typing import List, Tuple

from native_core.core.agent import Agent
from native_core.core.trace import TraceWriter

from .observation import TracedAction, runtime_identity


class ReferenceAgent(Agent):
    """A concrete `Agent` that participates in a bound `Execution` and completes.

    Deliberately minimal: it demonstrates the contract, and claims nothing
    beyond it. It carries no capability, no skill, no workflow, no definition
    and no instance identity — those belong to the governed construction
    reserved to the Architect, not to a consumer proving realizability.
    """

    def __init__(self, trace_writer: "Optional[TraceWriter]" = None) -> None:
        self._trace_writer = trace_writer
        self._sequences: List[int] = []

    @property
    def participated_sequences(self) -> Tuple[int, ...]:
        """The execution ordinals this consumer has participated in, in order.

        In-memory evidence for this consumer's own callers. Not a Trace, not
        durable, and not a substitute for either.
        """
        return tuple(self._sequences)

    def participate(self, execution: "object") -> None:
        """Take part in one bound `Execution`, then complete.

        Returning is the completion signal (§13.3). The bound execution is read,
        never constructed and never re-bound: a consumer receives the boundary
        it is given.
        """
        with TracedAction(
            self._trace_writer,
            agent_instance="reference-agent",
            runtime=runtime_identity(execution),
        ):
            self._sequences.append(execution.context.execution_sequence)
