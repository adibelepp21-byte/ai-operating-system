"""
Register format (D-1) and strict, read-only loading.

The register is JSON: a data artifact, diffable in review, parseable with
the standard library alone, and carrying no executable content.

Schema
------

    {
      "version": 1,
      "scan_scope": [ {"root": "<repo-relative dir>",
                       "detector": "<detector name>"} ],
      "entries":    [ {"identity": {"path": ..., "qualname": ...,
                                    "exception": ..., "ordinal": ...},
                       "category": ...,
                       "rationale": ...,
                       "finding_id": ...,
                       "governance_decision_id": ...,
                       "authorizing_act": ...,
                       "line": <optional int, navigational only>} ]
    }

Every listed field is required except `line`. Unknown fields are a
failure, not a courtesy: a register whose shape is not fully understood
cannot be said to bound anything.

Deliberately absent
-------------------

- **No status / lifecycle field.** Governance here is append-only: an
  entry exists or it does not. A mutable status would duplicate that as
  drifting state.
- **No registration timestamp.** The program forbids timestamps in
  source, and git already records when an entry was added and by which
  commit.

This module never writes. There is no serializer, by construction.
"""

import json
from dataclasses import dataclass
from pathlib import Path

from .identity import SiteIdentity

SCHEMA_VERSION = 1

_IDENTITY_FIELDS = {"path", "qualname", "exception", "ordinal"}
_ENTRY_REQUIRED = {
    "identity",
    "category",
    "rationale",
    "finding_id",
    "governance_decision_id",
    "authorizing_act",
}
_ENTRY_OPTIONAL = {"line"}
_SCOPE_FIELDS = {"root", "detector"}
_TOP_LEVEL = {"version", "scan_scope", "entries"}


class RegisterError(Exception):
    """A register that cannot be trusted. Always fatal — never a warning."""


@dataclass(frozen=True)
class ScanScope:
    root: str
    detector: str


@dataclass(frozen=True)
class RegisterEntry:
    identity: SiteIdentity
    category: str
    rationale: str
    finding_id: str
    governance_decision_id: str
    authorizing_act: str
    line: int | None


@dataclass(frozen=True)
class Register:
    version: int
    scan_scope: tuple
    entries: tuple


def _require_mapping(value, what):
    if not isinstance(value, dict):
        raise RegisterError(f"{what} must be an object")
    return value


def _require_str(mapping, key, what):
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise RegisterError(f"{what}: '{key}' must be a non-empty string")
    return value


def _parse_identity(raw):
    mapping = _require_mapping(raw, "entry identity")
    unknown = set(mapping) - _IDENTITY_FIELDS
    if unknown:
        raise RegisterError(f"entry identity has unknown field(s): {sorted(unknown)}")
    missing = _IDENTITY_FIELDS - set(mapping)
    if missing:
        raise RegisterError(f"entry identity missing field(s): {sorted(missing)}")
    ordinal = mapping["ordinal"]
    if not isinstance(ordinal, int) or isinstance(ordinal, bool) or ordinal < 0:
        raise RegisterError("entry identity: 'ordinal' must be a non-negative integer")
    return SiteIdentity(
        path=_require_str(mapping, "path", "entry identity"),
        qualname=_require_str(mapping, "qualname", "entry identity"),
        exception=_require_str(mapping, "exception", "entry identity"),
        ordinal=ordinal,
    )


def _parse_entry(raw):
    mapping = _require_mapping(raw, "register entry")
    unknown = set(mapping) - _ENTRY_REQUIRED - _ENTRY_OPTIONAL
    if unknown:
        raise RegisterError(f"register entry has unknown field(s): {sorted(unknown)}")
    missing = _ENTRY_REQUIRED - set(mapping)
    if missing:
        raise RegisterError(f"register entry missing field(s): {sorted(missing)}")
    line = mapping.get("line")
    if line is not None and (not isinstance(line, int) or isinstance(line, bool)):
        raise RegisterError("register entry: 'line' must be an integer when present")
    return RegisterEntry(
        identity=_parse_identity(mapping["identity"]),
        category=_require_str(mapping, "category", "register entry"),
        rationale=_require_str(mapping, "rationale", "register entry"),
        finding_id=_require_str(mapping, "finding_id", "register entry"),
        governance_decision_id=_require_str(
            mapping, "governance_decision_id", "register entry"
        ),
        authorizing_act=_require_str(mapping, "authorizing_act", "register entry"),
        line=line,
    )


def _parse_scope(raw):
    mapping = _require_mapping(raw, "scan scope")
    unknown = set(mapping) - _SCOPE_FIELDS
    if unknown:
        raise RegisterError(f"scan scope has unknown field(s): {sorted(unknown)}")
    missing = _SCOPE_FIELDS - set(mapping)
    if missing:
        raise RegisterError(f"scan scope missing field(s): {sorted(missing)}")
    return ScanScope(
        root=_require_str(mapping, "root", "scan scope"),
        detector=_require_str(mapping, "detector", "scan scope"),
    )


def load_register(path):
    """Parse and strictly validate a register. Raises RegisterError on any doubt."""
    text = Path(path).read_text(encoding="utf-8")
    try:
        raw = json.loads(text)
    except json.JSONDecodeError as exc:
        raise RegisterError(f"register is not valid JSON: {exc}") from exc

    mapping = _require_mapping(raw, "register")
    unknown = set(mapping) - _TOP_LEVEL
    if unknown:
        raise RegisterError(f"register has unknown field(s): {sorted(unknown)}")
    missing = _TOP_LEVEL - set(mapping)
    if missing:
        raise RegisterError(f"register missing field(s): {sorted(missing)}")

    version = mapping["version"]
    if version != SCHEMA_VERSION:
        raise RegisterError(
            f"register version {version!r} is not the supported version {SCHEMA_VERSION}"
        )
    if not isinstance(mapping["scan_scope"], list):
        raise RegisterError("register: 'scan_scope' must be a list")
    if not isinstance(mapping["entries"], list):
        raise RegisterError("register: 'entries' must be a list")

    return Register(
        version=version,
        scan_scope=tuple(_parse_scope(item) for item in mapping["scan_scope"]),
        entries=tuple(_parse_entry(item) for item in mapping["entries"]),
    )
