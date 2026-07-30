"""
Memory record (Domain Model §6/§6.1; memory_spec §1/§3; Freeze INV-7/8).

A Memory record is a dynamic, provisional, non-authoritative record of what
an Agent Instance encountered, *derived from Trace* (memory_spec §1). It is
scoped by the producing Agent Instance (Domain Model §5), deliberately
without a stable identity across derivations (§3), and recomputable from
Trace (§3, §11).

This module defines the record and the single, minimal derivation from a
Trace record. It holds no storage, no promotion, and no governance. Memory
never writes Trace (INV-5) and never becomes authoritative (INV-8).

The record is deeply immutable: content derived from a hardened Trace record
is already immutable, and `__post_init__` freezes any directly-constructed
content as well, so no Memory record is mutable. This is hygiene, not a
schema claim — the derivation heuristic itself is replaceable (§12, [O]).
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping


def _freeze(value: Any) -> Any:
    """Deeply immutable snapshot: mapping -> read-only mapping, list/tuple ->
    tuple, recursively. Local to Memory so the boundary is self-contained
    (module isolation)."""
    if isinstance(value, Mapping):
        return MappingProxyType({k: _freeze(v) for k, v in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(v) for v in value)
    return value


@dataclass(frozen=True)
class MemoryRecord:
    """One derived, scoped, provisional observation of what an Agent Instance
    encountered. Frozen and deeply immutable. Carries no stable identity."""

    scope: str          # the producing Agent Instance (Domain Model §5 scoping)
    content: Any = None  # what was encountered (derived from Trace outputs)

    def __post_init__(self):
        object.__setattr__(self, "content", _freeze(self.content))


def derive_from_trace(trace_record) -> MemoryRecord:
    """Derive one Memory record from one Trace record (memory_spec §5a; §6.1).

    Baseline derivation: the record's scope is the acting Agent Instance, and
    its content is what that action produced/encountered (the Trace record's
    outputs). This reads the Trace record only; it never mutates it (INV-5).
    The derivation is deterministic (same Trace record -> equal Memory record)
    and recomputable. Richer derivation heuristics are replaceable and [O]
    reserved (§12).
    """
    return MemoryRecord(scope=trace_record.agent_instance, content=trace_record.outputs)
