"""
Failure/result signaling primitive (Native Core Blueprint §16).

A minimal, explicit way to represent "this succeeded with a value" versus
"this failed, closed, with a stated reason" — the vocabulary in which
Fail-Closed behaviour (PR-4) is expressed across the Native Core without
each boundary re-inventing it.

This is a primitive, not a policy: it carries no external dependency, no
governance authority, and no entity ownership (Blueprint §16). It decides
nothing; it only names the two outcomes a facility operation may have.

Deliberately NOT an exception hierarchy replacement: boundaries may still
raise for programming errors. `Outcome` is for expected, checkable outcomes
where a caller must be forced to confront failure rather than receive a
silently-degraded value — the essence of Fail Closed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Generic, Optional, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Success(Generic[T]):
    """A completed operation carrying its value. Immutable."""

    value: T


@dataclass(frozen=True)
class Failure:
    """A halted operation carrying a stated reason. Immutable.

    `reason` is a human-readable, non-empty explanation. `detail` is an
    optional structured payload for callers that need more than the string.
    A Failure never carries a usable value — that is the point: a caller
    cannot mistake a failure for a degraded success.
    """

    reason: str
    detail: Optional[dict] = field(default=None)

    def __post_init__(self):
        if not self.reason or not self.reason.strip():
            # Fail closed even about our own construction: a reasonless
            # failure would be an un-diagnosable halt.
            raise ValueError("Failure.reason must be a non-empty explanation")


# An Outcome is exactly one of Success | Failure. Callers must check which.
Outcome = Any  # documented union; kept as Any to avoid importing typing.Union machinery at call sites


def is_success(outcome: Any) -> bool:
    return isinstance(outcome, Success)


def is_failure(outcome: Any) -> bool:
    return isinstance(outcome, Failure)
