"""
Optimization fail-closed exceptions (Blueprint §15; optimization_spec §11; PR-4).

The named halt conditions of the Optimization boundary. Every one expresses Fail
Closed (PR-4; optimization_spec §11): *"if evaluation is uncertain, it proposes
nothing rather than deciding."* An observation or proposal that cannot be formed
accountably is refused, never degraded into a partial or guessed one.

Named `OptimizationError` following the established convention of the other
boundaries (`KnowledgeError`, `GovernanceError`, `RuntimeSubsystemError`), all of
which extend the builtin `RuntimeError` without shadowing it.

Ownership: Optimization. Dependencies: none (stdlib only). Prohibited: carrying
any authority, decision, or state (§6.2 invariant 2; PR-3).
"""

from __future__ import annotations


class OptimizationError(RuntimeError):
    """Base for every fail-closed Optimization halt (PR-4)."""


class InvalidObservation(OptimizationError):
    """Raised when an observation cannot be recorded accountably — an unknown
    source, an absent subject, or observed content that is not immutable. Fail
    closed: an unaccountable observation is never recorded."""


class InvalidProposal(OptimizationError):
    """Raised when a proposal cannot be formed accountably — an absent identity,
    or no observation to rest on. Fail closed: a proposal with no evidence
    behind it is never constructed, so an ungrounded proposal cannot exist."""


class InvalidOptimizationConfiguration(OptimizationError):
    """Raised when the boundary cannot be assembled accountably — a missing or
    wrong-typed injected reader. Fail closed: an unconfigurable Optimization is
    never coerced into a usable one."""
