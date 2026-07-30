"""
Promotion-candidate generation (memory_spec §2, §5c, §10; Freeze INV-8; PR-3).

Memory MAY identify promotion candidates; it MUST NEVER approve, reject,
promote, govern, or make an authority decision (memory_spec §10; INV-8;
§6.2 invariant 2). Every candidate produced here is *merely an observation*
for the governed human review to decide upon — Governance decides, never
Memory.

Detect, Don't Decide (PR-3): the prioritization signal (`occurrence_count`)
MAY order candidates but MUST NEVER gate them. This module therefore emits a
candidate for **every** distinct observed memory — it filters nothing out and
sets no threshold; ordering is prioritization, and removing a candidate would
be gating (forbidden). There is deliberately no approve/reject/promote method
anywhere in this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence, Tuple

from .record import MemoryRecord


@dataclass(frozen=True)
class PromotionCandidate:
    """An observation offered to governed review. Carries no decision.

    `occurrence_count` is a non-gating prioritization signal (how often this
    (scope, content) was observed). It never authorizes promotion; it only
    helps a human reviewer order their attention (PR-3)."""

    scope: str
    observed_content: Any
    occurrence_count: int


def _hashable(value: Any):
    """Deterministic, hashable canonical form of derived content, for dedup.
    Mappings -> sorted tuple of (key, canonical(value)); sequences -> tuple;
    scalars unchanged."""
    if isinstance(value, dict):
        return tuple(sorted((k, _hashable(v)) for k, v in value.items()))
    try:
        items = value.items()  # MappingProxyType and other mappings
    except AttributeError:
        items = None
    if items is not None:
        return tuple(sorted((k, _hashable(v)) for k, v in items))
    if isinstance(value, (list, tuple)):
        return tuple(_hashable(v) for v in value)
    return value


def generate_candidates(memory_records: Sequence[MemoryRecord]) -> Tuple[PromotionCandidate, ...]:
    """Emit one candidate per distinct (scope, content) observation, ordered by
    occurrence_count (descending) then by first-seen order — a pure,
    deterministic prioritization. Filters nothing out; gates nothing; decides
    nothing. Governance decides whether any candidate becomes Knowledge
    (INV-8)."""
    order: list = []          # first-seen (scope, key) preserving discovery order
    counts: dict = {}
    contents: dict = {}
    for rec in memory_records:
        key = (rec.scope, _hashable(rec.content))
        if key not in counts:
            counts[key] = 0
            contents[key] = rec.content
            order.append(key)
        counts[key] += 1

    candidates = [
        PromotionCandidate(scope=key[0], observed_content=contents[key], occurrence_count=counts[key])
        for key in order
    ]
    # Stable prioritization: higher occurrence first, ties keep discovery order.
    candidates.sort(key=lambda c: -c.occurrence_count)
    return tuple(candidates)
