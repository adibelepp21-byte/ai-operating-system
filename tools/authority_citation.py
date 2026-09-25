"""Does a citation actually point at the Founder Decision it names?

Built under `GOAL-V2-005`. `AuthorityProvenance` (`tools/planning/goal.py`) is a
pointer. It proves that its `record` is a real file and, deliberately, nothing
more. The W4 registries (`tools/w4_delegation.py`,
`tools/agent_instance_registry.py`) then checked only that the *instrument
string* contained `FD-P11-001`. Together, those two checks accepted a
citation that named `FD-P11-001` while pointing at `README.md`, at `DP-01`, or
at any other resident file. That citation grants nothing and traces to nothing.

`FD-P11-001 §24` states the requirement this enforces, in the Founder's words:

```text
Delegation → authorized delegator → FD-P11-001 → Founder authority
"A Delegation that cannot produce this chain is invalid."
```

A citation produces the `FD-P11-001` link only when all three of these hold:

1. **the instrument names the identifier as a whole token.** `FD-P11-001 §9`
   qualifies; `FD-P11-0019` and `NOT-FD-P11-001` do not;
2. **the record is that instrument's own act.** It is a file under
   `docs/governance/acts/` whose name is the identifier, or the identifier
   followed by `-`;
3. **the identifier resolves in the Decision Register as a whole
   identifier.** This is the same whole-identifier rule the certified-evidence
   guard applies (`FD-P12-004`). A file planted in the acts directory is not a
   Founder Decision.

**What this still does not do** is the same thing `AuthorityProvenance` declines
to do: it does not decide that the cited instrument *grants* what the citing
artifact claims. That reading stays a human act. This establishes only that
the pointer points where it says it points.

If the Register cannot be read, the check fails closed.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[1]
ACTS_ROOT = "docs/governance/acts"
REGISTER = REPO_ROOT / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"


def _whole(identifier: str) -> "re.Pattern[str]":
    return re.compile(r"(?<![\w-])" + re.escape(identifier) + r"(?![-\w])")


def refusal(instrument: str, record: str, identifier: str,
            repo_root: Path = REPO_ROOT,
            register: Optional[Path] = None) -> Optional[str]:
    """Why this citation does not reach `identifier`, or None if it does."""
    if not _whole(identifier).search(instrument or ""):
        return (f"the citation names {instrument!r}, which is not "
                f"{identifier}")
    path = Path(record or "")
    if path.parent.as_posix() != ACTS_ROOT or not (
            path.stem == identifier or path.name.startswith(identifier + "-")):
        return (f"the citation names {identifier} but its record {record!r} "
                f"is not {identifier}'s act under {ACTS_ROOT}/")
    if not (repo_root / path).is_file():
        return f"the cited record {record!r} does not resolve"
    try:
        text = (register or repo_root / REGISTER.relative_to(REPO_ROOT)
                ).read_text(encoding="utf-8")
    except OSError as error:
        return (f"the Decision Register cannot be read ({error}); a citation "
                "cannot be resolved against it, so it is refused")
    if not _whole(identifier).search(text):
        return (f"{identifier} is not recorded in the Decision Register; a "
                "file in the acts directory is not a Founder Decision")
    return None
