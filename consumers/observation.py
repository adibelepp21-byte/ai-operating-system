"""
R2-A — the connective wire between an Agent-Instance action and the existing
durable Trace substrate (`ACT-CC-R2A-IMPL-001`; `AIOS-R2A-IC-001`).

`ACT-CC-R1-SYSTEMIC-001` found the Trace boundary complete and never called:
`TraceRecord` already carries `agent_instance · runtime · skills_used ·
tools_used · knowledge_consumed · memory_consumed · outputs · status`, and
`TraceWriter` already persists it through a `StorageFacility` — yet no
execution path authored a single record. INV-4 had no realization.

This module supplies the missing call. It adds **no** subsystem, **no**
boundary, and **no** schema field. Every part it uses already existed.

**Who authors, and who merely writes.** `ACT-CC-R2-NATIVE-001` selected the
concrete consumer Agent as the semantic author, because INV-4 assigns the Trace
to the *actor* and `workflow_spec §9` states that *"the step's actor authors the
Trace"*. Every other candidate is barred by its own conformance suite — Runtime
by `test_no_trace_identifier_exists_in_the_boundary`, the Agent boundary by
`trace ∈ FORBIDDEN_BOUNDARIES`, Workflow by `test_workflow_authors_no_trace`.
Those bars are canonical (INV-4, OQ-2), and R2-A leaves all three intact.

So the split is deliberate and narrow:

  - the **Agent** decides *that* an action happened and *what its outcome was*;
  - `TracedAction` decides *nothing*. It formats the record the Agent described
    and calls the writer exactly once.

`§14` forbids double authorship, and this is why exactly-one is structural
rather than a convention: an action's record is written in `__exit__`, once,
whatever the outcome. There is no second write path, and no branch that can
skip the first.

**Outcome mapping** (`§3`, `§31`). The Agent contract already fixes the action
boundary and its terminal semantics — `agent_execution_semantics_spec §13.3`:
*"participation completes when this returns without raising."* So:

```text
participate() returns            → status = success
participate() raises             → status = failure   (and the error propagates)
Agent reports a refusal/failure  → status = failure   (§12: refusal is an outcome)
```

`escalation` is **not** produced here. `ACT-CC-R2A-IMPL-001 §2` freezes it as
N/A for R2-A: the repository has no producing semantic for it, and the contract
forbids inventing one. It remains ratified vocabulary in `VALID_STATUSES`
(Domain Model §2.1) with no producer — recorded as a finding, not resolved by
this Act.

**Writer provisioning is optional by construction.** An Agent given no writer
authors nothing and behaves exactly as it did before R2-A. That keeps the
change minimal (`§54`) and leaves the existing suite untouched (`§38`). The
exactly-one invariant is therefore stated precisely: *when a writer is
provisioned, one action produces exactly one durable record.*

Dependencies: the Trace public surface only. No Runtime type is imported, and
nothing here reaches a boundary the consumer layer could not already reach.
"""

from __future__ import annotations

from typing import Any, List, Optional

from native_core.core.trace import TraceWriter, new_record

#: What an Agent reports when it has no definition version of its own. The
#: schema requires the field; inventing a version would be fabrication, which
#: `§9` forbids, so a single explicit placeholder is used and is visible as one.
UNVERSIONED = "unversioned"


class TracedAction:
    """One Agent-Instance action, observed exactly once.

    Used as a context manager around the body of `Agent.participate`. On exit
    it writes a single `TraceRecord` describing the action's terminal outcome.

    The Agent supplies the meaning — which Tools it reached, which Knowledge or
    Memory it consumed, what it produced, and whether its own semantics call the
    outcome a failure. This object supplies none of that and decides none of it.
    """

    def __init__(
        self,
        writer: "Optional[TraceWriter]",
        agent_instance: str,
        runtime: str,
        agent_definition_version: str = UNVERSIONED,
    ) -> None:
        if writer is not None and not isinstance(writer, TraceWriter):
            raise TypeError("an observed action requires a TraceWriter or None")
        self._writer = writer
        self._agent_instance = agent_instance
        self._runtime = runtime
        self._version = agent_definition_version
        self._skills: List[str] = []
        self._tools: List[str] = []
        self._knowledge: List[str] = []
        self._memory: List[str] = []
        self._outputs: Any = None
        self._failed = False
        self._written = False

    # -- what the Agent reports -------------------------------------------

    def used_skill(self, key: str) -> None:
        self._skills.append(key)

    def used_tool(self, key: str) -> None:
        self._tools.append(key)

    def consumed_knowledge(self, key: str) -> None:
        self._knowledge.append(key)

    def consumed_memory(self, key: str) -> None:
        self._memory.append(key)

    def produced(self, outputs: Any) -> None:
        self._outputs = outputs

    def failed(self, reason: str) -> None:
        """Report that the action's outcome was a failure.

        For outcomes the Agent itself classifies — a governance refusal, a
        terminal `FAILED` workflow — where `participate` still returns
        normally. `§12` is explicit that a refusal is an observable action
        outcome, and `§19` maps it to `failure` with execution *not* having
        occurred. Calling this does not raise and does not alter control flow;
        it only fixes the status the single record will carry.
        """
        self._failed = True
        if self._outputs is None:
            self._outputs = {"reason": reason}

    # -- observation -------------------------------------------------------

    @property
    def written(self) -> bool:
        """Whether this action's record has been written. Evidence for the
        exactly-one property, and the guard that makes a second write
        impossible."""
        return self._written

    # -- the single authoring point ---------------------------------------

    def __enter__(self) -> "TracedAction":
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        """Write exactly one record, then let any exception propagate.

        Returning False re-raises, so `participate`'s negative-completion
        contract (`§13.3`) is unchanged: an action that failed still fails for
        its caller, and now leaves durable evidence that it did.
        """
        status = "failure" if (exc_type is not None or self._failed) else "success"
        if exc_type is not None and self._outputs is None:
            self._outputs = {"error": f"{exc_type.__name__}: {exc}"}
        self._write(status)
        return False

    def _write(self, status: str) -> None:
        """The one place a Trace is authored for an Agent action.

        Guarded against a second write. `§13` requires exactly one record per
        action for every supported terminal outcome, and a re-entered or
        re-exited action must not be able to produce a duplicate.
        """
        if self._writer is None or self._written:
            return
        self._writer.write(
            new_record(
                agent_definition_version=self._version,
                agent_instance=self._agent_instance,
                runtime=self._runtime,
                skills_used=tuple(self._skills),
                tools_used=tuple(self._tools),
                knowledge_consumed=tuple(self._knowledge),
                memory_consumed=tuple(self._memory),
                outputs=self._outputs,
                status=status,
            )
        )
        self._written = True


def runtime_identity(execution: "object") -> str:
    """The hosting Runtime's identity, read from the Execution the Agent was
    handed.

    Read, never constructed: the consumer takes the boundary it is given. Falls
    back to an explicit placeholder rather than fabricating an identity when an
    Execution stand-in carries none — `§9` forbids inventing context.
    """
    runtime = getattr(execution, "runtime", None)
    return str(getattr(runtime, "runtime_id", "unknown-runtime"))
