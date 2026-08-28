"""
Phase 5 — `E5-3`, the Engineering Intelligence first milestone.

`GDR-0005 §3.5.3` ratifies the criterion as an exact count:

    exactly two (2) of the seven sub-capabilities enumerated in Vol VI §3.2 —
    **Coding** and **Testing** — are implemented and verified. The remaining
    five (Architecture, Security, Review, Refactoring, Documentation) are
    **not** required for Phase 5 exit.

*Exactly two* is a ceiling as well as a floor. The five unrealized sub-abilities
are absent from this module by design, and their absence is asserted by the
conformance tests: realizing a sixth would broaden Phase 5 scope, which
`ACT-CC-P6/P1-6-076 §15` prohibits as firmly as it prohibits leaving the two
undone.

**What this module is.** The concrete realization of the *Engineering
Intelligence Agent* Definition, which declares exactly two authorized
behaviours:

  - *"Construct and change engineered artifacts within AIOS, within the Coding
    sub-ability"*, and
  - *"Verify engineered artifacts against their stated conformance criteria,
    within the Testing sub-ability"*.

**What "engineered artifact" is taken to mean here, and why it is bounded.** An
artifact is modelled as a named, immutable sequence of lines. That is deliberate
and conservative. The Agent Definition grants no filesystem authority, no
governance authority and no execution authority, so this consumer never writes
to the repository, never executes what it constructs, and never invokes a
process. An Agent that could rewrite the repository under its own judgement
would be claiming an authority the Definition explicitly withholds — *"It claims
no approval authority, no governance authority, no Architecture Decision Record
authority."* The Capability is *"independent of the models, tools, or techniques
used to deliver it"*, so a bounded, inspectable realization satisfies the
contract without inventing authority to go with it.

**Change is versioned, never in-place.** `change` returns a new `Artifact` and
leaves its input untouched, mirroring the discipline T-12 fixes for Knowledge —
*"a new version never replaces its predecessor in place"*. The reason is the
same in both places: an artifact that mutates under its caller destroys the
evidence of what was verified.

**Testing reports; it does not decide.** `verify` returns a result per stated
criterion and never raises on a failing check, per `PR-3` *Detect Don't Decide*.
A verification pass that halted on the first failure would hide the rest, and a
verification that raised would be making a governance judgement about an
artifact rather than reporting a fact about it. Malformed *inputs* still fail
closed — that is `PR-4`, and it is a different question from a failing check.

**Not a canonical entity.** `DEC-PHASE5-SEMANTICS` (Option B) fixes Phase 5 as
work *"against the existing ratified Capability architecture"*, not the creation
of an entity named Intelligence. The Architecture Freeze entity set stays at
**twelve**, the core region stays at **eleven** boundaries, and `native_core/`
is untouched by this work. This is an `ExecutionConsumer` realization resident in
`consumers/` under `DEC-P6-042`, exactly like `E-01` and the Phase 6 Knowledge
consumer.

Dependencies: the `Agent` contract, and the standard library. Nothing from
Knowledge, Governance, Memory, Trace or `tools/`; no Runtime type is imported
and the hosting Runtime is never named.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence, Tuple

from native_core.core.agent import Agent

#: The two sub-abilities `E5-3` places in Phase 5 scope. Recorded as data so the
#: conformance suite can assert the boundary rather than trusting prose.
REALIZED_SUB_ABILITIES: Tuple[str, ...] = ("Coding", "Testing")

#: The five `E5-3` explicitly excludes from Phase 5 exit. Present here as a
#: negative declaration — nothing in this module implements any of them.
UNREALIZED_SUB_ABILITIES: Tuple[str, ...] = (
    "Architecture",
    "Security",
    "Review",
    "Refactoring",
    "Documentation",
)


@dataclass(frozen=True)
class Artifact:
    """An engineered artifact: a name and its content, immutable once made.

    Frozen for the same reason `SubStep` is frozen — an artifact that callers
    could edit after verification would make the verification meaningless.
    """

    name: str
    lines: Tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("an engineered artifact must be named")
        if not isinstance(self.lines, tuple):
            raise TypeError("artifact content is an immutable sequence of lines")

    @property
    def text(self) -> str:
        """The artifact's content as a single string, for criteria stated over
        the whole rather than per line."""
        return "\n".join(self.lines)


@dataclass(frozen=True)
class ConformanceCriterion:
    """One stated conformance criterion an artifact is verified against.

    The criterion is supplied by the caller. This Agent does not author
    criteria: deciding what an artifact must satisfy is a governance or
    architectural judgement, and the Testing sub-ability is *"verify engineered
    artifacts **against their stated** conformance criteria"* — stated
    elsewhere, by someone else.
    """

    name: str
    required_text: str

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("a conformance criterion must be named")
        if not isinstance(self.required_text, str) or not self.required_text:
            raise ValueError("a conformance criterion must state what it requires")


@dataclass(frozen=True)
class CheckResult:
    """The outcome of one criterion against one artifact. A fact, not a verdict
    on the artifact's fitness — that judgement belongs to whoever stated the
    criteria."""

    artifact_name: str
    criterion_name: str
    satisfied: bool


class EngineeringIntelligenceAgent(Agent):
    """A concrete `Agent` realizing the Engineering Intelligence Agent
    Definition, bounded to Coding and Testing.

    The governing Capability declares seven sub-abilities and records that only
    Coding and Testing are realized in Phase 5. This class implements those two.
    It exposes no method for Architecture, Security, Review, Refactoring or
    Documentation, and the conformance suite asserts that it does not.
    """

    def __init__(
        self,
        artifact: "Optional[Artifact]" = None,
        criteria: "Optional[Sequence[ConformanceCriterion]]" = None,
    ) -> None:
        """Configure the artifact this Agent will verify when it participates,
        and the criteria it will verify against. Left unset, participation
        completes having verified nothing — an explicit absence."""
        self._artifact = artifact
        self._criteria: Tuple[ConformanceCriterion, ...] = tuple(criteria or ())
        self._constructed: Tuple[Artifact, ...] = ()
        self._results: Tuple[CheckResult, ...] = ()

    # -- observation ------------------------------------------------------

    @property
    def constructed(self) -> Tuple[Artifact, ...]:
        """Artifacts this Agent constructed or changed, in order. In-memory
        evidence for its own callers — not a Trace."""
        return self._constructed

    @property
    def results(self) -> Tuple[CheckResult, ...]:
        """Check results from the most recent verification, one per stated
        criterion, in the order the criteria were stated."""
        return self._results

    # -- Coding ------------------------------------------------------------

    def construct(self, name: str, lines: Sequence[str]) -> Artifact:
        """*Coding* — produce a new engineered artifact from stated content.

        Records what it produced so that a participation's effect is
        inspectable. It does not execute the artifact, and it does not write it
        anywhere: producing content and being authorized to install it are
        different powers, and this Agent Definition grants only the first.
        """
        artifact = Artifact(name=name, lines=tuple(lines))
        self._constructed = self._constructed + (artifact,)
        return artifact

    def change(self, artifact: Artifact, lines: Sequence[str]) -> Artifact:
        """*Coding* — produce a changed version of an existing artifact.

        Returns a **new** `Artifact` under the same name; the input is
        unmodified and remains valid evidence of the prior state. Nothing is
        replaced in place.
        """
        if not isinstance(artifact, Artifact):
            raise TypeError("only an engineered artifact can be changed")
        changed = Artifact(name=artifact.name, lines=tuple(lines))
        self._constructed = self._constructed + (changed,)
        return changed

    # -- Testing -----------------------------------------------------------

    def verify(
        self, artifact: Artifact, criteria: Sequence[ConformanceCriterion]
    ) -> Tuple[CheckResult, ...]:
        """*Testing* — check an artifact against its stated conformance criteria.

        Reports every criterion, including the ones that fail, and raises on
        none of them (`PR-3`). A malformed input — something that is not an
        artifact, or an empty criteria set — is a different matter and fails
        closed (`PR-4`): verifying against no criteria would report success
        while checking nothing.
        """
        if not isinstance(artifact, Artifact):
            raise TypeError("only an engineered artifact can be verified")
        stated = tuple(criteria)
        if not stated:
            raise ValueError(
                "verification requires at least one stated conformance criterion; "
                "an empty criteria set would report conformance without checking anything"
            )
        for criterion in stated:
            if not isinstance(criterion, ConformanceCriterion):
                raise TypeError("criteria are stated as ConformanceCriterion")
        self._results = tuple(
            CheckResult(
                artifact_name=artifact.name,
                criterion_name=criterion.name,
                satisfied=criterion.required_text in artifact.text,
            )
            for criterion in stated
        )
        return self._results

    @staticmethod
    def is_conformant(results: Sequence[CheckResult]) -> bool:
        """Whether every reported check was satisfied. A reading of results
        already produced — it performs no check of its own."""
        results = tuple(results)
        if not results:
            raise ValueError("conformance is not defined over an empty result set")
        return all(result.satisfied for result in results)

    # -- the Agent contract ------------------------------------------------

    def participate(self, execution: "object") -> None:
        """Participate in one bound Execution by verifying the configured
        artifact against its stated criteria **during** that Execution.

        This supplies `E5-4`'s *"berjalan nyata, bukan lagi rencana"*: the
        Testing sub-ability runs inside a participation handed out by a RUNNING
        Runtime. Completion is negative, per `agent_execution_semantics_spec`
        §13.3 — participation completes when this returns without raising, and
        the return stays `None` because no result model is ratified.
        """
        if self._artifact is not None and self._criteria:
            self.verify(self._artifact, self._criteria)
