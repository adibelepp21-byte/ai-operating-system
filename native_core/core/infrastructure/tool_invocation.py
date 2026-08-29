"""
Phase 8 invocation governance — the wrapper above `ToolBoundary`
(`FD-P8-001 §4.4`–`§4.10`; `ACT-CC-P8-001 §6`, `§7`, `§9`, `§11` — `E8-03`,
`E8-04`, `E8-05`).

`ACT-CC-P8-001 §6.1` fixes this module's position and job:

> *"Governance shall operate through a governance wrapper above the existing
> Infrastructure ToolBoundary. The existing ToolBoundary remains the confinement
> and invocation capability foundation."*

So `ToolBoundary` is unchanged in character — it still confines external
coupling and still makes no governance decision. This layer sits above it,
decides whether an invocation may proceed, and **delegates only accepted
invocations downward**. A refused or invalid invocation never reaches
`ToolBoundary.invoke`, which is what `E8-05` requires be demonstrable rather than
asserted.

**Four outcomes, because two would hide the distinction that matters.**
`FD-P8-001 §4.9` requires success, governance refusal, invalid invocation and
execution failure to be structurally distinguishable, and forbids *"convert[ing]
refusal into a false execution failure or false success."* The Infrastructure
`Outcome` primitive carries two cases; `InvocationResult` carries four, and
records `execution_attempted` so a reader can tell a Tool that was never run from
one that ran and failed.

**Refusal is returned, not raised.** `ACT-CC-P8-001 §9.1` lists the conditions
that *"shall not rely on uncaught exceptions as the ordinary invocation
contract"* — unregistered, disabled, retired, unauthorized caller, invalid
contract, governance refusal — and they all return a structured result here.
Exceptions remain for what `shared/result.py` reserves them for: programming
error and impossible internal state.

**The invocation record is not the canonical Trace entity.** `E8-05` requires
verifiable evidence of every invocation attempt. It is deliberately *not*
`core/trace/`: Blueprint §14 gives Infrastructure no dependency on any sibling
boundary, Runtime authors no independent Trace (OQ-2), and `ACT-CC-P8-001 §11.4`
requires only that trace be **verifiable** — *"Phase 8 does not require: audit
database; external logging provider; distributed tracing; immutable event store;
long-term persistence engine."* So the ledger below is an in-process, verifiable
record owned by this layer. It creates no Trace, claims no INV-4 standing, and
adds no cross-boundary dependency.

**Callers are classed, not trusted.** `FD-P8-001 §4.6` lets an Agent *"select or
propose"* an invocation while withholding authority to bypass governance. A
caller therefore submits an `InvocationRequest` naming its own class, and this
layer decides — the request is a proposal, and nothing about constructing one
grants the authority to have it accepted.

Dependencies: stdlib, `shared`, and this package. No sibling core boundary.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from types import MappingProxyType
from typing import Any, List, Mapping, Optional, Tuple

from ...shared import Failure, Success
from .tool_boundary import ToolBoundary
from .tool_lifecycle import ToolDescriptor, ToolState
from .tool_registry import ToolRegistry


class CallerClass(Enum):
    """The classes of caller that may submit an invocation request.

    `AGENT` proposes; `EXECUTION` submits on behalf of a running execution;
    `SYSTEM` is an internal operational caller. The class is *declared* by the
    request and *evaluated* here — declaring a class is not being granted it,
    which is why the authorized set is a property of this layer rather than of
    the request.
    """

    AGENT = "agent"
    EXECUTION = "execution"
    SYSTEM = "system"
    UNKNOWN = "unknown"


#: Caller classes permitted to submit an invocation request. `UNKNOWN` is absent
#: deliberately: `E8-03` requires that an unauthorized caller be refused, and a
#: default that admitted anything would make that criterion unfalsifiable.
AUTHORIZED_CALLERS: Tuple[CallerClass, ...] = (
    CallerClass.AGENT,
    CallerClass.EXECUTION,
    CallerClass.SYSTEM,
)


class InvocationDisposition(Enum):
    """The four structurally distinguishable outcomes of `FD-P8-001 §4.9`."""

    SUCCESS = "success"
    GOVERNANCE_REFUSAL = "governance_refusal"
    INVALID_INVOCATION = "invalid_invocation"
    EXECUTION_FAILURE = "execution_failure"


@dataclass(frozen=True)
class InvocationRequest:
    """A proposal to invoke a Tool. Carries no authority of its own.

    Constructing one is what `FD-P8-001 §4.6` permits an Agent to do. It has no
    field that could mark it approved, because approval is this layer's act.
    """

    tool_key: str
    action: str
    parameters: Mapping[str, Any] = field(default_factory=dict)
    caller: CallerClass = CallerClass.AGENT
    invocation_id: str = "invocation"

    def __post_init__(self) -> None:
        object.__setattr__(self, "parameters", MappingProxyType(dict(self.parameters)))


@dataclass(frozen=True)
class InvocationResult:
    """The structured outcome of an invocation attempt (`E8-04`).

    `execution_attempted` is the field that makes refusal and failure impossible
    to confuse: a governance refusal always carries `False`, an execution failure
    always carries `True`. `E8-05.4` requires the record to prove *"whether
    execution was attempted"*, and a result that only carried a category could
    not.
    """

    disposition: InvocationDisposition
    invocation_id: str
    tool_key: str
    execution_attempted: bool
    value: Any = None
    reason: Optional[str] = None

    @property
    def is_success(self) -> bool:
        return self.disposition is InvocationDisposition.SUCCESS

    @property
    def is_refusal(self) -> bool:
        return self.disposition is InvocationDisposition.GOVERNANCE_REFUSAL

    @property
    def is_invalid(self) -> bool:
        return self.disposition is InvocationDisposition.INVALID_INVOCATION

    @property
    def is_execution_failure(self) -> bool:
        return self.disposition is InvocationDisposition.EXECUTION_FAILURE


@dataclass(frozen=True)
class InvocationRecord:
    """Verifiable evidence of one invocation attempt (`E8-05`).

    Records what `FD-P8-001 §4.10` requires it connect: invocation identity, Tool
    identity, caller class, the lifecycle/eligibility result, the governance
    disposition, whether execution was attempted, and the outcome category.
    Frozen — evidence that could be edited after the fact is not evidence.
    """

    invocation_id: str
    tool_key: str
    caller: CallerClass
    lifecycle_state: Optional[ToolState]
    governance_admitted: bool
    execution_attempted: bool
    disposition: InvocationDisposition
    reason: Optional[str] = None


class InvocationLedger:
    """The in-process, verifiable record of invocation attempts.

    Append-only to its callers: it exposes no removal and no mutation, because
    `E8-05` asks that refusals be *demonstrable*, and a ledger a caller could
    prune would demonstrate nothing.
    """

    def __init__(self) -> None:
        self._records: List[InvocationRecord] = []

    def record(self, entry: InvocationRecord) -> None:
        self._records.append(entry)

    @property
    def records(self) -> Tuple[InvocationRecord, ...]:
        return tuple(self._records)

    def for_tool(self, tool_key: str) -> Tuple[InvocationRecord, ...]:
        return tuple(r for r in self._records if r.tool_key == tool_key)

    def executed(self) -> Tuple[InvocationRecord, ...]:
        """Attempts that actually reached Tool execution."""
        return tuple(r for r in self._records if r.execution_attempted)

    def refused(self) -> Tuple[InvocationRecord, ...]:
        """Attempts refused before execution — governance or invalidity."""
        return tuple(r for r in self._records if not r.execution_attempted)


class ToolInvocationGovernance:
    """The governance wrapper above `ToolBoundary`.

    Constructed over the registry (lifecycle authority), the boundary
    (confinement and execution) and the ledger (evidence). It is the **only**
    surface through which a lawful invocation reaches a Tool.
    """

    def __init__(
        self,
        registry: ToolRegistry,
        boundary: ToolBoundary,
        ledger: "Optional[InvocationLedger]" = None,
        authorized_callers: "Optional[Tuple[CallerClass, ...]]" = None,
    ) -> None:
        self._registry = registry
        self._boundary = boundary
        self._ledger = ledger if ledger is not None else InvocationLedger()
        self._authorized = tuple(
            authorized_callers if authorized_callers is not None else AUTHORIZED_CALLERS
        )

    @property
    def ledger(self) -> InvocationLedger:
        return self._ledger

    @property
    def registry(self) -> ToolRegistry:
        """The lifecycle authority. Exposed for inspection; this wrapper never
        transitions a Tool — lifecycle is the registry's, and a governance layer
        that could enable a Tool it was about to admit would be deciding both
        halves of its own question."""
        return self._registry

    # -- the single lawful invocation path ---------------------------------

    def invoke(self, request: InvocationRequest) -> InvocationResult:
        """Govern an invocation request, and execute it only if it passes.

        The order is the criterion: every check below happens **before**
        `ToolBoundary.invoke` is reached, so a refused or invalid request cannot
        touch the Tool. `FD-P8-001 §6.3` requires the refusal path to fail
        closed, and `§4.4` forbids reaching the implementation *"before the
        required governance determination."*
        """
        descriptor = self._registry.describe(request.tool_key)

        # 1 — caller authority (FD-P8-001 §4.5.5)
        if request.caller not in self._authorized:
            return self._refuse(
                request, descriptor,
                f"caller class {request.caller.value!r} is not authorized to invoke Tools",
            )

        # 2 — Tool identity validity and registration (§4.5.1, §4.5.2)
        if descriptor is None:
            return self._refuse(
                request, None, f"no Tool is defined at {request.tool_key!r}"
            )
        if not self._registry.is_registered(request.tool_key):
            return self._refuse(
                request, descriptor,
                f"{descriptor.identity} is {descriptor.state.value!r} and is not registered",
            )

        # 3 — lifecycle eligibility (§4.5.3)
        if not descriptor.is_invocable:
            return self._refuse(
                request, descriptor,
                f"{descriptor.identity} is {descriptor.state.value!r} and is not invocable",
            )

        # 4 — invocation contract validity (§4.5.4). Invalid, not refused:
        #     the request was permitted to be made and is malformed.
        if not descriptor.contract.declares(request.action):
            return self._invalid(
                request, descriptor,
                f"{descriptor.identity} declares no action {request.action!r}",
            )
        missing = descriptor.contract.missing_parameters(request.action, request.parameters)
        if missing:
            return self._invalid(
                request, descriptor,
                f"invocation omits required parameter(s) {missing!r}",
            )

        # 5 — the Tool must also be attached at the confinement boundary.
        if not self._boundary.is_registered(request.tool_key):
            return self._refuse(
                request, descriptor,
                f"{descriptor.identity} is not attached at the Tool boundary",
            )

        # Governance admits. Only now is the Tool reached.
        return self._execute(request, descriptor)

    # -- internals ---------------------------------------------------------

    def _execute(self, request, descriptor) -> InvocationResult:
        """Delegate to the confinement boundary and classify what comes back.

        A `Failure` from the Tool is an **execution failure**, never a refusal:
        governance already admitted this invocation, and relabelling the result
        would misreport which gate stopped it.
        """
        outcome = self._boundary.invoke(
            request.tool_key, request.action, dict(request.parameters)
        )
        if isinstance(outcome, Success):
            return self._record_and_return(
                request, descriptor, True, True,
                InvocationDisposition.SUCCESS, value=outcome.value,
            )
        reason = outcome.reason if isinstance(outcome, Failure) else "tool returned no outcome"
        return self._record_and_return(
            request, descriptor, True, True,
            InvocationDisposition.EXECUTION_FAILURE, reason=reason,
        )

    def _refuse(self, request, descriptor, reason) -> InvocationResult:
        return self._record_and_return(
            request, descriptor, False, False,
            InvocationDisposition.GOVERNANCE_REFUSAL, reason=reason,
        )

    def _invalid(self, request, descriptor, reason) -> InvocationResult:
        return self._record_and_return(
            request, descriptor, False, False,
            InvocationDisposition.INVALID_INVOCATION, reason=reason,
        )

    def _record_and_return(
        self, request, descriptor: "Optional[ToolDescriptor]",
        admitted: bool, attempted: bool,
        disposition: InvocationDisposition,
        value: Any = None, reason: "Optional[str]" = None,
    ) -> InvocationResult:
        """Every path returns through here, so every attempt is recorded.

        There is no branch that produces a result without an entry — `E8-05.1`
        requires *"every lawful invocation attempt produces a verifiable
        trace"*, and a single unrecorded path would be the one that mattered.
        """
        self._ledger.record(
            InvocationRecord(
                invocation_id=request.invocation_id,
                tool_key=request.tool_key,
                caller=request.caller,
                lifecycle_state=descriptor.state if descriptor is not None else None,
                governance_admitted=admitted,
                execution_attempted=attempted,
                disposition=disposition,
                reason=reason,
            )
        )
        return InvocationResult(
            disposition=disposition,
            invocation_id=request.invocation_id,
            tool_key=request.tool_key,
            execution_attempted=attempted,
            value=value,
            reason=reason,
        )
