"""S-OPS — the dedicated operational proof surface for E13-05 (`FDR-3`).

Owner: *S-OPS operational proof surface*. Definition:
`docs/operations/s-ops/S-OPS-DEFINITION.md`. Executable authority: `P13-ENV-02`
(Delegation Register `§15`), for the two transitions below on the one object
below.

The surface holds one object, `S-OPS-01`: a scheduled operational window whose
state is OPEN or CLOSED. Its contract (definition `§3`) says which state its
schedule requires:

```text
BEFORE → CLOSED     WITHIN → OPEN     AFTER → CLOSED
```

This module is the surface's only writer. It offers these operations and no
others:

* `provision`: the operator creates the object once, CLOSED, with its window.
  It refuses if the object exists. Provisioning is environment, not action.
* `transition`: `open` (CLOSED → OPEN, only WITHIN) or `close` (OPEN →
  CLOSED, only outside the window). It compares and sets on the recorded state,
  and the history is appended, never rewritten.
* `read` and `observe`: reading, for P13 and for anyone.

Nothing here changes the window, deletes the object, rewrites its history,
creates a second object, or writes outside the root it is given. P13 imports
this module. This module imports nothing from P13.

    python -m tools.s_ops.surface [show]
    python -m tools.s_ops.surface provision --opens-at <UTC> --closes-at <UTC> --actor <who>
"""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = "docs/operations/s-ops"
OBJECT_ID = "S-OPS-01"
#: The one object, as `P13-ENV-02` names it.
OBJECT = f"{ROOT}/{OBJECT_ID}.json"
OWNER = "S-OPS operational proof surface"
KIND = "scheduled operational window"
DEFINITION = f"{ROOT}/S-OPS-DEFINITION.md"
AUTHORITY = "FDR-3"

CLOSED, OPEN = "CLOSED", "OPEN"
STATES = (CLOSED, OPEN)
BEFORE, WITHIN, AFTER = "BEFORE", "WITHIN", "AFTER"
UNPROVISIONED = "UNPROVISIONED"
#: The contract: the state the schedule requires in each phase (definition §3).
REQUIRED: Dict[str, str] = {BEFORE: CLOSED, WITHIN: OPEN, AFTER: CLOSED}
#: The only transitions: name → (from, to, the phases in which it is permitted).
TRANSITIONS = {"open": (CLOSED, OPEN, (WITHIN,)),
               "close": (OPEN, CLOSED, (BEFORE, AFTER))}


class SurfaceError(ValueError):
    """An operation the surface does not permit. Nothing was written."""


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _instant(text) -> datetime:
    try:
        value = datetime.fromisoformat(str(text).replace("Z", "+00:00"))
    except ValueError as error:
        raise SurfaceError(f"{text!r} is not an instant ({error})") from None
    if value.tzinfo is None:
        raise SurfaceError(f"{text!r} names no timezone")
    return value


def phase(window: Dict[str, str], at: datetime) -> str:
    """Where `at` falls in the window. Observed, never stored."""
    if at < _instant(window["opens_at"]):
        return BEFORE
    if at < _instant(window["closes_at"]):
        return WITHIN
    return AFTER


def path(root: Path) -> Path:
    return Path(root) / f"{OBJECT_ID}.json"


def _check(obj: dict) -> dict:
    if obj.get("object") != OBJECT_ID or obj.get("owner") != OWNER:
        raise SurfaceError(f"not {OBJECT_ID} of the {OWNER} "
                           f"(object {obj.get('object')!r}, owner {obj.get('owner')!r})")
    if obj.get("state") not in STATES:
        raise SurfaceError(f"{obj.get('state')!r} is not a state of {OBJECT_ID}")
    window = obj.get("window") or {}
    if not _instant(window.get("opens_at")) < _instant(window.get("closes_at")):
        raise SurfaceError("the window must open before it closes")
    if not isinstance(obj.get("history"), list) or not obj["history"]:
        raise SurfaceError(f"{OBJECT_ID} carries no history")
    return obj


def read(root: Path) -> Optional[dict]:
    """The object, or None when it is not provisioned. A malformed object, or
    one this surface does not own, raises: it is not S-OPS state."""
    file = path(root)
    if not file.exists():
        return None
    return _check(json.loads(file.read_text(encoding="utf-8")))


def observe(root: Path, at: datetime) -> dict:
    obj = read(root)
    if obj is None:
        return {"state": UNPROVISIONED, "phase": UNPROVISIONED, "window": None}
    return {"state": obj["state"], "phase": phase(obj["window"], at),
            "window": dict(obj["window"])}


def provision(root: Path, *, opens_at: str, closes_at: str, actor: str,
              at: Optional[datetime] = None) -> dict:
    """The operator creates the object once, CLOSED. It is never re-created."""
    if not (actor or "").strip():
        raise SurfaceError("provisioning is done by someone, and recorded")
    at = at or utcnow()
    obj = _check({
        "object": OBJECT_ID, "owner": OWNER, "kind": KIND,
        "definition": DEFINITION, "authority": AUTHORITY,
        "state": CLOSED,
        "window": {"opens_at": _instant(opens_at).isoformat(),
                   "closes_at": _instant(closes_at).isoformat()},
        "history": [{"at": at.isoformat(), "event": "provisioned", "from": None,
                     "to": CLOSED, "actor": actor,
                     "basis": f"{AUTHORITY}; definition §9 (the operator provisions)"}]})
    Path(root).mkdir(parents=True, exist_ok=True)
    try:
        with open(path(root), "x", encoding="utf-8") as handle:
            json.dump(obj, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
    except FileExistsError:
        raise SurfaceError(f"{OBJECT_ID} is already provisioned; it is never "
                           "re-created") from None
    return obj


def transition(root: Path, name: str, *, actor: str, basis: str,
               at: Optional[datetime] = None) -> dict:
    """`open` or `close`, if and only if the contract permits it now."""
    if name not in TRANSITIONS:
        raise SurfaceError(f"{name!r} is not a transition of {OBJECT_ID}")
    source, target, phases = TRANSITIONS[name]
    at = at or utcnow()
    obj = read(root)
    if obj is None:
        raise SurfaceError(f"{OBJECT_ID} is not provisioned")
    if obj["state"] != source:
        raise SurfaceError(f"{name}: {OBJECT_ID} is {obj['state']}, not {source}")
    now = phase(obj["window"], at)
    if now not in phases:
        raise SurfaceError(f"{name}: {OBJECT_ID}'s window phase is {now}; "
                           f"{name} is permitted only {'/'.join(phases)}")
    entry = {"at": at.isoformat(), "event": name, "from": source, "to": target,
             "phase": now, "actor": actor, "basis": basis}
    _replace(root, dict(obj, state=target, history=list(obj["history"]) + [entry]))
    return {"object": OBJECT_ID, **entry}


def _replace(root: Path, obj: dict) -> None:
    """Write the whole object at once, so a reader never sees half of it."""
    handle, temporary = tempfile.mkstemp(dir=str(root), prefix=f".{OBJECT_ID}.",
                                         suffix=".tmp")
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as out:
            json.dump(obj, out, indent=2, ensure_ascii=False)
            out.write("\n")
        os.replace(temporary, path(root))
    except BaseException:
        if os.path.exists(temporary):
            os.unlink(temporary)
        raise


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("show", help="print the object and its phase now (default)")
    make = sub.add_parser("provision", help="the operator creates the object once")
    make.add_argument("--opens-at", required=True)
    make.add_argument("--closes-at", required=True)
    make.add_argument("--actor", required=True)
    args = parser.parse_args(argv)
    root = REPO_ROOT / ROOT
    if args.command == "provision":
        obj = provision(root, opens_at=args.opens_at, closes_at=args.closes_at,
                        actor=args.actor)
    else:
        obj = read(root)
    now = utcnow()
    print(json.dumps({"observed_at": now.isoformat(), "object": obj,
                      "phase": phase(obj["window"], now) if obj else UNPROVISIONED},
                     indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    # GOAL-V2-004: install the certified-write barrier before anything runs,
    # even when this file is run by path and has not imported `tools`.
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    import tools  # noqa: E402,F401
    raise SystemExit(main())
