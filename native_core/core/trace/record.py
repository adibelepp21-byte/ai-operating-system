"""
Trace record (Architecture Freeze §3 INV-4/5/6; Domain Model §2.1; trace_spec §3).

A Trace record is the immutable, append-only, unconditional record of one
Agent-Instance action — the single permanent source of truth (Freeze
INV-4/5/6). This module defines the record and nothing else: it holds no
storage, no derivation, and no governance.

Required contents are exactly the ten ratified fields of Domain Model §2.1 —
no more. The record deliberately carries no `trace_id`, no `timestamp`, and
no `schema_version`: those are schema extensions, and "additional captured
fields, if ever needed, enter only by governed Domain-Model change"
(trace_spec §3, §12). Append order (provided by the storage facility) is the
ordering discipline; no timestamp field is introduced to supply it.

INV-6 / Capture, Don't Reference (PR-5): `knowledge_consumed` and
`memory_consumed` hold *captured content*, not references — the record is
self-contained, so its explainability never depends on the later existence
of any Memory or Knowledge item. The record is deeply immutable (INV-5):
sequences become tuples and mappings become read-only, recursively, at
construction.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Mapping

# Ratified action outcomes (Domain Model §2.1: success / failure / escalation).
VALID_STATUSES = frozenset({"success", "failure", "escalation"})

# The ten required content field names (Domain Model §2.1), in canonical order.
REQUIRED_FIELDS = (
    "agent_definition_version",
    "agent_instance",
    "runtime",
    "skills_used",
    "tools_used",
    "knowledge_consumed",
    "memory_consumed",
    "outputs",
    "cost_resource_metadata",
    "status",
)


def _freeze(value: Any) -> Any:
    """Deeply immutable snapshot: dict -> read-only mapping, list/tuple ->
    tuple, recursively; scalars unchanged. This is how INV-5 immutability is
    enforced structurally — a constructed record cannot be mutated, nor can
    its nested content."""
    if isinstance(value, Mapping):
        return MappingProxyType({k: _freeze(v) for k, v in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(v) for v in value)
    return value


def _to_plain(value: Any) -> Any:
    """Inverse of _freeze for serialization: read-only mapping -> dict,
    tuple -> list, recursively. Produces only JSON-native structures. The
    in-memory record stays frozen; only its serialized projection is plain."""
    if isinstance(value, Mapping):
        return {k: _to_plain(v) for k, v in value.items()}
    if isinstance(value, tuple):
        return [_to_plain(v) for v in value]
    return value


@dataclass(frozen=True)
class TraceRecord:
    """One immutable Trace record carrying exactly the Domain Model §2.1
    required contents. Frozen: no field may be reassigned (INV-5). There is
    intentionally no edit, update, or delete method anywhere."""

    agent_definition_version: str
    agent_instance: str
    runtime: str
    skills_used: tuple = ()
    tools_used: tuple = ()
    knowledge_consumed: tuple = ()   # captured content (INV-6), never references
    memory_consumed: tuple = ()      # captured content (INV-6), never references
    outputs: Any = None
    cost_resource_metadata: Mapping = field(default_factory=lambda: MappingProxyType({}))
    status: str = "success"

    def __post_init__(self):
        """Deep-freeze content-bearing fields so a record is immutable no
        matter how it is constructed — the public constructor, `new_record`,
        `from_mapping`, or any internal path (closes Phase 3.25 finding F-1).

        Uses object.__setattr__ because the dataclass is frozen; this runs
        once, at construction, and never mutates a record thereafter. It is
        idempotent: freezing already-frozen content leaves it unchanged. It
        introduces no field and changes no value's meaning — only its
        mutability (INV-5)."""
        for _name in (
            "skills_used",
            "tools_used",
            "knowledge_consumed",
            "memory_consumed",
            "outputs",
            "cost_resource_metadata",
        ):
            object.__setattr__(self, _name, _freeze(getattr(self, _name)))

    def to_mapping(self) -> dict:
        """Plain, JSON-native projection of the record for serialization.
        Deterministic: the same record always yields the same mapping."""
        return {
            "agent_definition_version": self.agent_definition_version,
            "agent_instance": self.agent_instance,
            "runtime": self.runtime,
            "skills_used": _to_plain(self.skills_used),
            "tools_used": _to_plain(self.tools_used),
            "knowledge_consumed": _to_plain(self.knowledge_consumed),
            "memory_consumed": _to_plain(self.memory_consumed),
            "outputs": _to_plain(self.outputs),
            "cost_resource_metadata": _to_plain(self.cost_resource_metadata),
            "status": self.status,
        }


class InvalidTraceRecord(ValueError):
    """Raised when a record cannot be constructed accountably. Fail closed:
    an un-constructable record is never silently coerced into a valid one."""


def _require_nonempty_str(name: str, value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InvalidTraceRecord(f"{name} must be a non-empty string")
    return value


def new_record(
    *,
    agent_definition_version: str,
    agent_instance: str,
    runtime: str,
    skills_used=(),
    tools_used=(),
    knowledge_consumed=(),
    memory_consumed=(),
    outputs: Any = None,
    cost_resource_metadata: Mapping | None = None,
    status: str = "success",
) -> TraceRecord:
    """Construct a TraceRecord, validating and deeply freezing its contents.

    Fail closed (PR-4): the acting identity fields (definition version,
    instance, runtime) must be present, and status must be one of the ratified
    outcomes; otherwise construction raises rather than producing a partial,
    unaccountable record. Keyword-only to prevent positional-argument
    mistakes in the ten required contents.
    """
    _require_nonempty_str("agent_definition_version", agent_definition_version)
    _require_nonempty_str("agent_instance", agent_instance)
    _require_nonempty_str("runtime", runtime)
    if status not in VALID_STATUSES:
        raise InvalidTraceRecord(f"status must be one of {sorted(VALID_STATUSES)}, got {status!r}")

    return TraceRecord(
        agent_definition_version=agent_definition_version,
        agent_instance=agent_instance,
        runtime=runtime,
        skills_used=_freeze(tuple(skills_used)),
        tools_used=_freeze(tuple(tools_used)),
        knowledge_consumed=_freeze(tuple(knowledge_consumed)),
        memory_consumed=_freeze(tuple(memory_consumed)),
        outputs=_freeze(outputs),
        cost_resource_metadata=_freeze(dict(cost_resource_metadata or {})),
        status=status,
    )


def from_mapping(mapping: Mapping) -> TraceRecord:
    """Reconstruct a record from its plain mapping (as read back from
    storage). Applies the same validation and freezing as construction, so a
    read record is exactly as immutable and accountable as a written one."""
    if not isinstance(mapping, Mapping):
        raise InvalidTraceRecord("record mapping must be a mapping")
    missing = [f for f in REQUIRED_FIELDS if f not in mapping]
    if missing:
        raise InvalidTraceRecord(f"record is missing required fields: {missing}")
    return new_record(
        agent_definition_version=mapping["agent_definition_version"],
        agent_instance=mapping["agent_instance"],
        runtime=mapping["runtime"],
        skills_used=mapping["skills_used"],
        tools_used=mapping["tools_used"],
        knowledge_consumed=mapping["knowledge_consumed"],
        memory_consumed=mapping["memory_consumed"],
        outputs=mapping["outputs"],
        cost_resource_metadata=mapping["cost_resource_metadata"],
        status=mapping["status"],
    )
