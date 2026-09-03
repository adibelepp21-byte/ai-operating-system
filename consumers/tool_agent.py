"""
Phase 8 — the Agent side of governed Tool invocation (`E8-03`).

`FD-P8-001 §4.4` fixes `E8-03` on a path, not a call:

```text
Authorized Caller → Invocation Request → Tool Boundary → Governance Check
                  → Tool Execution → Structured Outcome / Failure
```

and `ACT-CC-P8-001 §13` requires it demonstrated through a real Runtime. This
module is the consumer that makes that path traversable.

**What an Agent may and may not do, made structural.** `FD-P8-001 §4.6` lets an
Agent *"select or propose a Tool"* and *"submit or contribute invocation input
through the authorized path"*, while withholding authority to register Tools,
alter lifecycle, enable or disable Tools, bypass governance, or *"directly invoke
Tool implementation through a lawful public path."* So this Agent:

  - **proposes** by constructing an `InvocationRequest`, which carries no
    approval field and confers nothing;
  - **submits** it to `ToolInvocationGovernance`, which decides;
  - **never registers, enables, disables or retires.** It exposes no such
    method, and the conformance suite asserts their absence rather than trusting
    this paragraph;
  - **never reaches `ToolBoundary.invoke`.** It holds no reference to the
    boundary at all — the only Tool surface it touches is the governance
    wrapper, so there is no code path here by which it could bypass the gate.

A refusal is returned and recorded, not retried: an Agent that re-proposed until
something was admitted would be manufacturing the authorization the wrapper
withheld. Refusal, invalidity and execution failure are kept apart exactly as the
wrapper reports them — collapsing them here would defeat `E8-04` one layer above
where it is enforced.

**How it reaches the Tool Ecosystem.** Two modes, and the second is the
architectural one. A governance wrapper may be injected for focused unit
evidence; or omitted, in which case `participate` resolves it from the Execution
it is handed — `execution.runtime.tools.governance`. That property is
RUNNING-gated by the Runtime itself, and Runtime is an access host only, so a
consumer reaching Tools through the Runtime hosting it adds no authority and
bypasses nothing.

Dependencies: the `Agent` contract and the Infrastructure public surface. No
Runtime type is imported and the hosting Runtime is never named.
"""

from __future__ import annotations

from typing import Any, List, Optional, Tuple

from native_core.core.agent import Agent
from native_core.core.infrastructure import (
    CallerClass,
    InvocationDisposition,
    InvocationRequest,
    InvocationResult,
    ToolInvocationGovernance,
)
from native_core.core.trace import TraceWriter

from .observation import TracedAction, runtime_identity


class ToolProposingAgent(Agent):
    """A concrete `Agent` that proposes Tool invocations through the lawful
    governance path.

    Construction takes the governance wrapper by injection, or nothing, in which
    case it is resolved from the hosting Runtime at participation time.
    """

    def __init__(
        self,
        governance: "Optional[ToolInvocationGovernance]" = None,
        proposal: "Optional[tuple]" = None,
        caller: CallerClass = CallerClass.AGENT,
        trace_writer: "Optional[TraceWriter]" = None,
    ) -> None:
        if governance is not None and not isinstance(governance, ToolInvocationGovernance):
            raise TypeError("a Tool-proposing Agent requires a ToolInvocationGovernance")
        self._governance = governance
        self._proposal = proposal
        self._caller = caller
        self._trace_writer = trace_writer
        self._results: List[InvocationResult] = []

    # -- observation ------------------------------------------------------

    @property
    def results(self) -> Tuple["InvocationResult", ...]:
        """Every invocation result this Agent received, in order — admitted and
        refused alike. Ordinary in-memory evidence for its own callers; the
        authoritative record is the wrapper's ledger, not this."""
        return tuple(self._results)

    @property
    def executed(self) -> Tuple["InvocationResult", ...]:
        """Results whose invocation actually reached Tool execution."""
        return tuple(r for r in self._results if r.execution_attempted)

    @property
    def refused(self) -> Tuple["InvocationResult", ...]:
        """Results the boundary stopped before execution — refusal or
        invalidity. Surfaced rather than hidden: a refusal the Agent could not
        observe would be indistinguishable from a Tool that silently did
        nothing."""
        return tuple(r for r in self._results if not r.execution_attempted)

    # -- proposal ----------------------------------------------------------

    def compose(
        self, tool_key: str, action: str, parameters: "Optional[dict]" = None,
        invocation_id: str = "invocation",
    ) -> InvocationRequest:
        """Compose an invocation proposal.

        All this does is construct a request. It reaches no boundary, consults
        no registry, and confers no authority — `FD-P8-001 §4.6` permits exactly
        this, and the request type carries no field that could pretend the
        proposal was approved.
        """
        return InvocationRequest(
            tool_key=tool_key,
            action=action,
            parameters=parameters or {},
            caller=self._caller,
            invocation_id=invocation_id,
        )

    def propose(self, request: InvocationRequest) -> InvocationResult:
        """Submit a proposal to the governance wrapper and let it decide.

        Returns whatever the wrapper returns, unaltered. The Agent does not
        re-classify the outcome: relabelling a refusal as a failure — or a
        failure as a refusal — is what `FD-P8-001 §4.9` forbids, and doing it
        here would defeat the criterion just outside the boundary that enforces
        it.
        """
        if self._governance is None:
            raise RuntimeError("propose requires an injected ToolInvocationGovernance; "
                               "otherwise propose through participate(execution)")
        return self._submit(self._governance, request)

    # -- internal ----------------------------------------------------------

    def _submit(self, governance, request) -> InvocationResult:
        result = governance.invoke(request)
        self._results.append(result)
        return result

    def _resolve(self, execution: "object") -> "ToolInvocationGovernance":
        """Return the governance wrapper this participation will use.

        An injected wrapper wins when present. Otherwise it comes from the
        Runtime hosting this Execution — `execution.runtime.tools.governance` —
        which is RUNNING-gated by the Runtime itself. This consumer adds no
        access control and bypasses none: if the Runtime is not RUNNING, the
        Runtime refuses and the refusal propagates.
        """
        if self._governance is not None:
            return self._governance
        return execution.runtime.tools.governance

    # -- the Agent contract ------------------------------------------------

    def participate(self, execution: "object") -> None:
        """Participate in one bound Execution by proposing the configured Tool
        invocation **during** that Execution.

        This is the `E8-03` path in one method. Completion is defined
        negatively, per `agent_execution_semantics_spec` §13.3: participation
        completes when this returns without raising. A governance refusal is not
        an exception and does not prevent completion — the Agent proposed
        lawfully and was lawfully refused, which is a completed participation
        with a recorded refusal, not a failed one.
        """
        governance = self._resolve(execution)
        with TracedAction(
            self._trace_writer,
            agent_instance="tool-proposing-agent",
            runtime=runtime_identity(execution),
        ) as observed:
            if self._proposal is None:
                return
            tool_key, action, parameters = self._proposal
            observed.used_tool(tool_key)
            result = self._submit(
                governance,
                InvocationRequest(
                    tool_key=tool_key,
                    action=action,
                    parameters=parameters or {},
                    caller=self._caller,
                    invocation_id="participation",
                ),
            )
            # `ACT-CC-R2A-IMPL-001 §12`: a governance refusal is an observable
            # action outcome, not an absence of one. Participation still
            # completes lawfully — the Agent proposed correctly and was
            # correctly refused — so this reports the outcome without altering
            # control flow, and the single record carries `failure`.
            #
            # The branch is on the **disposition**, not on
            # `execution_attempted`. `ACT-CC-R6-SYSTEMIC-001` proved why: an
            # `EXECUTION_FAILURE` reaches the Tool and therefore has
            # `execution_attempted=True`, so keying on that predicate filed a
            # genuinely failed invocation as `success` — and
            # `tools/derived_views.py`, which selects failures by
            # `status == "failure"`, could not see it. Only `SUCCESS` is a
            # successful outcome; every other ratified disposition is a failed
            # one. `execution_attempted` remains what it always was — evidence
            # about whether protected execution occurred — and the
            # `InvocationLedger` still carries that distinction separately.
            if result.disposition is InvocationDisposition.SUCCESS:
                observed.produced({"disposition": result.disposition.name})
            else:
                observed.failed(f"{result.disposition.name} for {tool_key}.{action}")
