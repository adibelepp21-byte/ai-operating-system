"""
Execution session (Blueprint §6; runtime_spec §3/§6).

`ExecutionSession` is the concrete execution boundary object. Its **entire**
responsibility is to bind a Runtime to an ExecutionContext — nothing else.

It owns no planning, no execution logic, no queue, no scheduler, no workflow,
no agent, no retries, no threads, no futures, no timers. It is merely the
canonical boundary object every future execution consumer will receive.

Immutability: a frozen dataclass over private fields, exposed through read-only
properties. The private-field form is deliberate — it lets the frozen dataclass
satisfy the `Execution` contract's abstract properties while remaining truly
immutable (a public-field dataclass would leave the inherited abstract
properties unsatisfied). It is constructed only by the Execution composition
root.

Ownership: transient execution boundary only. Dependencies: this package's
`contract`/`context` and the Runtime `contract` above it. Stdlib otherwise.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..contract import Runtime
from .context import ExecutionContext
from .contract import Execution
from .exceptions import InvalidExecutionConfiguration


@dataclass(frozen=True)
class ExecutionSession(Execution):
    """An immutable binding of a hosting Runtime to an execution identity."""

    _runtime: "Runtime"
    _context: "ExecutionContext"

    def __post_init__(self):
        if not isinstance(self._runtime, Runtime):
            raise InvalidExecutionConfiguration("execution session requires a Runtime")
        if not isinstance(self._context, ExecutionContext):
            raise InvalidExecutionConfiguration("execution session requires an ExecutionContext")

    @property
    def runtime(self) -> "Runtime":
        return self._runtime

    @property
    def context(self) -> "ExecutionContext":
        return self._context
