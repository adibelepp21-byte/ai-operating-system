"""
Phase 6 — the Agent side of *"Agent dapat mengambil dan memperbarui pengetahuan
tervalidasi."*

Master Program **Volume II §4.3** states the Phase 6 exit condition as a single
sentence: an Agent can **retrieve** and **update** **validated** knowledge. This
module is the consumer that makes that sentence demonstrable. It adds no
capability to the Knowledge subsystem and holds no authority over it; it is the
missing *caller*, and nothing else.

**Why it lives here and not in `native_core/core/agent/`.** That is a contract
boundary whose conformance suite pins it shut: one cross-boundary import, no
Execution type, no naming of the hosting Runtime, no new raise site. `agent.py`
records the consequence in its own words — it *"imports nothing from Knowledge,
Memory, Governance, Trace, Infrastructure"*. Those constraints are not obstacles
to route around; they are what keeps a contract boundary a contract boundary.
`E-01` established the alternative under `DEC-P6-042`: the consumer moves out,
and the boundary is preserved by placing the caller outside it rather than
weakening it to let the caller in. Not one core assertion changes for this file
to exist.

**Authority direction, which this module must not disturb.** T-12 ratifies
exactly one admission gate — the Governance subsystem's promotion authorization,
affirmative `True` only — and the direction is strictly *Governance → Knowledge*.
So this Agent:

  - **reads** through `KnowledgeRetrieval`, the consumption surface, and reads
    only what is already Active;
  - **updates** by handing a candidate and a `GovernanceReview` to the existing
    `KnowledgeAdmission`, which decides;
  - **never decides.** It records no `ReviewDecision`, constructs no
    `GovernanceReview`, and holds no `HumanAuthority`. It cannot approve its own
    proposal, and there is no code path here by which it could.

An update that Governance has not authorized raises out of `admit` and this
module lets it raise. Catching it to return a soft failure would convert a
fail-closed gate into a fail-open one, which is the single thing PR-4 exists to
prevent.

**What "validated" means here.** `tervalidasi` is read as *admitted* — a version
that passed the governed gate into Active state, per T-12's ratified lifecycle
{Candidate → Active → Superseded}. `knowledge_spec §3` places validity
*conditions* on an explicitly **orthogonal** axis, and their catalogue is
deferred under `T12-D-003`; this module therefore asserts nothing about them and
reads nothing from them. The reasoning is recorded in the Act record; if the
Founder binds the term differently, `read` is where the change lands.

**How it reaches Knowledge.** Two modes, and the second is the architectural
one. Collaborators may be injected directly — useful for focused unit evidence —
or omitted, in which case `participate` resolves them from the Execution it is
handed: `execution.runtime.knowledge`. That path is not invented here. The
Execution contract already names it — *"Reaching Knowledge through
`runtime.knowledge` still passes the Runtime's own RUNNING-only access control —
Execution adds no authority and bypasses nothing"* — and `Runtime.knowledge` is
RUNNING-gated and fails closed otherwise. A consumer that takes its Knowledge
access from the Runtime hosting it is simply what *hosting* means.

Dependencies: the `Agent` contract and the Knowledge public surface. Nothing
from `tools/`, no Runtime type imported, no Governance type it could act through
— the hosting Runtime is reached through the Execution it is given, never named.
"""

from __future__ import annotations

from typing import List, Optional, Tuple

from native_core.core.agent import Agent
from native_core.core.knowledge import KnowledgeAdmission, KnowledgeRetrieval, KnowledgeVersion
from native_core.core.trace import TraceWriter

from .observation import TracedAction, runtime_identity


class KnowledgeConsumingAgent(Agent):
    """A concrete `Agent` that reads admitted Knowledge and proposes updates
    through the governed admission path.

    Construction takes the two Knowledge collaborators by injection — the read
    surface and the admission gate. It takes no Governance object: a
    `GovernanceReview` is supplied per proposal by the caller that holds it, so
    this consumer never has a standing authorization to reuse.
    """

    def __init__(
        self,
        retrieval: "Optional[KnowledgeRetrieval]" = None,
        admission: "Optional[KnowledgeAdmission]" = None,
        knowledge_item_key: Optional[str] = None,
        proposal: "Optional[tuple]" = None,
        trace_writer: "Optional[TraceWriter]" = None,
    ) -> None:
        self._trace_writer = trace_writer
        if retrieval is not None and not isinstance(retrieval, KnowledgeRetrieval):
            raise TypeError("a Knowledge-consuming Agent requires a KnowledgeRetrieval")
        if admission is not None and not isinstance(admission, KnowledgeAdmission):
            raise TypeError("a Knowledge-consuming Agent requires a KnowledgeAdmission")
        self._retrieval = retrieval
        self._admission = admission
        self._key = knowledge_item_key
        self._proposal = proposal
        self._read: List[KnowledgeVersion] = []
        self._admitted: List[KnowledgeVersion] = []

    # -- observation ------------------------------------------------------

    @property
    def knowledge_read(self) -> Tuple["KnowledgeVersion", ...]:
        """Versions this Agent obtained, in order. Ordinary in-memory evidence
        for its own callers and tests — not a Trace. Trace is authored by the
        Runtime under INV-4 and nothing here writes or substitutes for it."""
        return tuple(self._read)

    @property
    def knowledge_admitted(self) -> Tuple["KnowledgeVersion", ...]:
        """Versions admitted as a result of this Agent's proposals, in order.
        The admission was Governance's; the proposal was this Agent's."""
        return tuple(self._admitted)

    # -- the two halves of the exit statement ------------------------------

    def _resolve(self, execution: "object"):
        """Return the (retrieval, admission) pair this participation will use.

        Injected collaborators win when present. Otherwise the pair comes from
        the Runtime hosting this Execution — `execution.runtime.knowledge` —
        which is RUNNING-gated by the Runtime itself. This consumer adds no
        access control and bypasses none: if the Runtime is not RUNNING, the
        Runtime refuses and the refusal propagates.
        """
        if self._retrieval is not None and self._admission is not None:
            return self._retrieval, self._admission
        subsystem = execution.runtime.knowledge
        return subsystem.retrieval, subsystem.admission

    def read(self, knowledge_item_key: str) -> Optional["KnowledgeVersion"]:
        """*mengambil* — obtain the Active admitted version for a key.

        Delegates to the consumption surface and adds nothing. A key with no
        Active version yields `None`: an explicit absence, never a fabricated
        value. An unadmitted candidate is not reachable through this path at
        all, which is what makes what it returns *validated*.
        """
        if self._retrieval is None:
            raise RuntimeError("read requires an injected KnowledgeRetrieval; "
                               "otherwise read through participate(execution)")
        version = self._retrieval.active(knowledge_item_key)
        if version is not None:
            self._read.append(version)
        return version

    def history(self, knowledge_item_key: str) -> Tuple["KnowledgeVersion", ...]:
        """The append-only version history for a key, through the same surface."""
        return self._retrieval.history(knowledge_item_key)

    def propose(self, candidate: "object", authorization: "object") -> "KnowledgeVersion":
        """*memperbarui* — propose an update and let Governance decide.

        The proposal is this Agent's; the decision is not. `admit` consults the
        supplied `GovernanceReview` and refuses unless it authorizes this exact
        candidate. Refusal raises, and the raise is not caught here: a consumer
        that softened a fail-closed gate would be claiming an authority it does
        not hold.
        """
        if self._admission is None:
            raise RuntimeError("propose requires an injected KnowledgeAdmission; "
                               "otherwise propose through participate(execution)")
        version = self._admission.admit(candidate, authorization)
        self._admitted.append(version)
        return version

    # -- the Agent contract ------------------------------------------------

    def participate(self, execution: "object") -> None:
        """Participate in one bound Execution by reading the Knowledge item this
        Agent was configured for.

        Completion is defined negatively, per `agent_execution_semantics_spec`
        §13.3: participation completes when this returns without raising. There
        is no result value because no result model is ratified. Reading nothing
        — because no key was configured, or because the key has no Active
        version — is a completion, not a failure; this consumer manufactures no
        failure condition it does not have.
        """
        with TracedAction(
            self._trace_writer,
            agent_instance="knowledge-consuming-agent",
            runtime=runtime_identity(execution),
        ):
            retrieval, admission = self._resolve(execution)
            if self._proposal is not None:
                candidate, authorization = self._proposal
                self._admitted.append(admission.admit(candidate, authorization))
            if self._key is not None:
                version = retrieval.active(self._key)
                if version is not None:
                    self._read.append(version)
