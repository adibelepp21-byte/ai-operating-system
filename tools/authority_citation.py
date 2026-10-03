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


# ---- Founder Goal intake (FD-AGENCY-001 · S-3) -------------------------------
#
# A Founder Goal / Target reaches the CEO as a Founder message, persisted
# verbatim as an act (the `GOAL-V2-00N` acts, the S-directives), its content
# hash recorded in the Decision Register. A planning `Goal` that claims to be
# the Founder's must point at such an instrument **and quote it**: otherwise
# whoever wrote the Goal, not the Founder, would be its author.
#
# This reads; it creates nothing. It answers one question about a citation and
# a statement, and the caller (the CEO) decides what to do with the answer.

_FOUNDER_HEADER = re.compile(r"from the Founder|Issued by:\*\*\s*Founder")
_FENCE_OPEN, _FENCE_CLOSE = "````text\n", "\n````"


def founder_text(record: str, repo_root: Path = REPO_ROOT) -> Optional[str]:
    """The verbatim Founder content of a persisted instrument, or None."""
    try:
        text = (repo_root / record).read_text(encoding="utf-8")
    except OSError:
        return None
    if _FENCE_OPEN not in text or _FENCE_CLOSE not in text:
        return None
    return text[text.index(_FENCE_OPEN) + len(_FENCE_OPEN) - 1:text.rindex(_FENCE_CLOSE)]


def founder_goal_refusal(instrument: str, record: str, statement: str,
                         repo_root: Path = REPO_ROOT,
                         register: Optional[Path] = None) -> Optional[str]:
    """Why ``statement`` is not a Founder Goal quoted from ``record``, or None.

    All of these must hold:

    1. the citation reaches the instrument named by the record (`refusal`): the
       record is that instrument's own act, and the instrument is recorded in
       the Decision Register;
    2. the act is a persisted **Founder** message: its header says so, and the
       sha256 of its verbatim content is recorded in the Decision Register, so
       the content is the registered one;
    3. the statement occurs **verbatim** in that content: the Goal says what the
       Founder said, not a paraphrase.
    """
    identifier = Path(record or "").stem
    reached = refusal(instrument, record, identifier, repo_root, register)
    if reached:
        return reached
    content = founder_text(record, repo_root)
    if content is None:
        return f"{record} holds no verbatim Founder content"
    header = (repo_root / record).read_text(encoding="utf-8").split(_FENCE_OPEN, 1)[0]
    if not _FOUNDER_HEADER.search(header):
        return f"{record} is not recorded as a message from the Founder"
    import hashlib
    # Two recording conventions exist in the corpus: the `GOAL-V2` acts hash
    # the fenced content without its leading newline, later acts with it. Either
    # registered digest identifies the same verbatim content.
    digests = {hashlib.sha256(c.encode("utf-8")).hexdigest()
               for c in (content, content[1:] if content.startswith("\n") else content)}
    try:
        registered = (register or repo_root / REGISTER.relative_to(REPO_ROOT)
                      ).read_text(encoding="utf-8")
    except OSError as error:
        return f"the Decision Register cannot be read ({error})"
    # Older entries abbreviate the digest to 16 hex digits and an ellipsis.
    if not any(d in registered or f"{d[:16]}…" in registered for d in digests):
        return (f"the content of {record} (sha256 {min(digests)[:12]}…) is not "
                "the registered content; a changed instrument is not the Founder's")
    if not isinstance(statement, str) or not statement.strip():
        return "a Founder Goal requires a statement"
    if statement not in content:
        return ("the statement is not a verbatim quotation of the Founder "
                "instrument; a Goal may not alter Founder intent")
    return None
