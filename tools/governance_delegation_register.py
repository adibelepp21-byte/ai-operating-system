"""Read the governance Delegation Register and report which delegations are in force.

Built under `ACT-CC-GOV-V2-RESUME-001` (first V2 Goal / Target: a verified
post-V2 operational baseline). The baseline found that the self-model answered
*"What authority do I have?"* from a list written into code. That list was
sourced to `DP-01 §8`, a P11 instrument. After Co-Founder V2 was registered
(`DEL-CFV2-CEO-001`, `GDR-0038`), the list no longer described the operative
delegation, and nothing in the system could tell. This module reads the answer
from the register instead.

**The register is append-only, and that decides how it has to be read.** A
superseded entry keeps its original text, including its original
`| **Status** | **ACTIVE** |` row (Register `§2`). The supersession is
recorded later, in an appended `#### Supersession mark — ...` section. A reader
that takes each entry's own Status row at face value therefore reports a
superseded delegation as active. This one applies the marks.

**This module owns no truth and grants nothing.** It reports what the register
states. It never reports that a caller holds authority:

```text
REGISTER READING  ≠  AUTHORIZATION
```
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
REGISTER = REPO_ROOT / "docs/governance/AIOS_DELEGATION_REGISTER_v1.0.md"

_DEL_ID = r"DEL-[A-Za-z0-9][A-Za-z0-9.]*(?:-[A-Za-z0-9][A-Za-z0-9.]*)*"
_ENTRY_RE = re.compile(r"^###\s+(?P<id>" + _DEL_ID + r")\s+[—-]\s+(?P<title>.+?)\s*$")
_MARK_RE = re.compile(r"^####\s+Supersession mark\b(?P<rest>.*)$")
_ROW_RE = re.compile(r"^\|\s*\*\*(?P<label>[^*|]+?)\*\*\s*\|\s*(?P<value>.*?)\s*\|\s*$")
_ANY_DEL = re.compile(_DEL_ID)


class DelegationRegisterUnreadable(RuntimeError):
    """The register could not be read, so no delegation state can be reported."""


@dataclass(frozen=True)
class Delegation:
    identifier: str
    title: str
    role: str
    scope: str
    declared_status: str
    effective_status: str
    superseded_by: Tuple[str, ...]
    source: str

    @property
    def in_force(self) -> bool:
        return self.effective_status.upper().startswith("ACTIVE")

    def as_reported(self) -> Dict[str, object]:
        return {
            "identifier": self.identifier,
            "title": self.title,
            "role": self.role,
            "scope": self.scope,
            "declared_status": self.declared_status,
            "effective_status": self.effective_status,
            "superseded_by": list(self.superseded_by),
            "source": self.source,
        }


def _clean(value: str) -> str:
    return re.sub(r"[*`]", "", value).strip()


def read_register(register: Path = REGISTER) -> List[Delegation]:
    """Every `### DEL-…` entry, with supersession marks applied.

    Fails closed: an unreadable register raises. It never returns an empty list
    that a caller could mistake for *"no delegation is in force"*.
    """
    try:
        lines = register.read_text(encoding="utf-8").split("\n")
    except OSError as error:
        raise DelegationRegisterUnreadable(f"{register}: {error}") from error

    entries: Dict[str, Dict[str, object]] = {}
    order: List[str] = []
    marks: Dict[str, List[str]] = {}
    current: Optional[str] = None
    mark_target: Optional[str] = None

    for number, line in enumerate(lines, 1):
        entry = _ENTRY_RE.match(line)
        if entry:
            current, mark_target = entry.group("id"), None
            if current not in entries:
                entries[current] = {"title": entry.group("title"), "fields": {},
                                    "line": number}
                order.append(current)
            continue
        if line.startswith("## ") or (line.startswith("### ") and not entry):
            current, mark_target = None, None
            continue
        mark = _MARK_RE.match(line)
        if mark:
            ids = _ANY_DEL.findall(mark.group("rest"))
            mark_target = ids[0] if ids else None
            current = None
            continue
        if line.startswith("#### "):
            mark_target = None
        row = _ROW_RE.match(line)
        if row is None:
            continue
        label, value = row.group("label").strip(), row.group("value")
        if mark_target and label.lower().startswith("status from") \
                and "SUPERSEDED" in value.upper():
            by = [i for i in _ANY_DEL.findall(value) if i != mark_target]
            marks.setdefault(mark_target, []).extend(by)
            continue
        if current is not None:
            entries[current]["fields"].setdefault(label, value)  # type: ignore[index]

    rel = register.relative_to(REPO_ROOT) if register.is_relative_to(REPO_ROOT) else register
    result: List[Delegation] = []
    for identifier in order:
        data = entries[identifier]
        fields: Dict[str, str] = data["fields"]  # type: ignore[assignment]
        declared = _clean(fields.get("Status", "")) or "UNSTATED"
        superseded = tuple(dict.fromkeys(marks.get(identifier, ())))
        effective = "SUPERSEDED" if identifier in marks else declared
        result.append(Delegation(
            identifier=identifier,
            title=str(data["title"]),
            role=_clean(fields.get("Delegated Role", fields.get("Delegate", ""))),
            scope=_clean(fields.get("Scope", "")),
            declared_status=declared,
            effective_status=effective,
            superseded_by=superseded,
            source=f"{rel}:{data['line']}",
        ))
    return result


def in_force(register: Path = REGISTER) -> List[Delegation]:
    """Delegations whose effective status is ACTIVE (dormant ones included)."""
    return [d for d in read_register(register) if d.in_force]


def main() -> int:
    import json
    print(json.dumps([d.as_reported() for d in read_register()], indent=2,
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    # GOAL-V2-004: install the certified-write barrier before anything runs,
    # even when this file is run by path and has not imported `tools`.
    import os, sys  # noqa: E401
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import tools  # noqa: E402,F401
    raise SystemExit(main())
