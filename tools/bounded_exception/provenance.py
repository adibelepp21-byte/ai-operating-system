"""
Provenance resolution.

An entry may only be trusted if the governance that admitted it can be
found. Each entry therefore names three things, and all three must
resolve:

- **Finding ID** — the recorded finding the exception belongs to, which
  must appear in the Finding Register.
- **Governance Decision ID** — the Architect act that admitted it, which
  must appear in the Governance Decision Register.
- **Authorizing act** — the directive under which the entry was written.

This is the structural reason the register cannot expand itself. An
entry cannot be added before the governance record that admits it
exists, because the verifier resolves the reference and fails when it
does not resolve. There is no path from "the code changed" to "the
register grew" that does not pass through a governance artifact.

Resolution is read-only and injected by constructor, so tests exercise
it against synthetic registers without touching the real corpus and
without creating any governance entry.

Resolution rule: an identifier resolves when it appears in its register
file in one of exactly two structural positions — a Markdown heading
line that names it, or the leading cell of a table row where that cell
is the identifier alone. Matching is on the exact token, not a substring
of a longer identifier — `GDR-001` must not resolve merely because
`GDR-0012` exists.

Prose alone does not resolve. An identifier named only in narrative — a
forward-looking insertion pointer such as "GDR-0015 onward", or a
sentence discussing an entry that does not yet exist — is not a recorded
entry and must not be treated as one. Accepting token presence anywhere
in the file was the P7-I61 D.4 defect: a pointer to a future entry
resolved as though the entry already existed, so the register's
fail-closed guarantee held only by accident of wording.

False-negative risk: an identifier recorded in a register by some form
other than these two positions would not resolve, and would fail closed.
"""

import re
from abc import ABC, abstractmethod
from pathlib import Path

AUTHORIZING_ACT = re.compile(r"^P\d+-I\d+$")
HEADING = re.compile(r"^ {0,3}#{1,6}\s")
CELL_DECORATION = " `*_"


class ProvenanceResolver(ABC):
    """Declares the resolution contract. Implementations are read-only."""

    @abstractmethod
    def finding_exists(self, finding_id):
        """True when the finding identifier is recorded."""

    @abstractmethod
    def decision_exists(self, decision_id):
        """True when the governance decision identifier is recorded."""


def _names_token(line, token):
    return re.search(rf"(?<![0-9A-Za-z-]){re.escape(token)}(?![0-9A-Za-z-])", line) is not None


def _leading_cell(line):
    """The first cell of a table row, stripped of markup, or None."""
    stripped = line.strip()
    if not stripped.startswith("|"):
        return None
    return stripped.strip("|").split("|")[0].strip(CELL_DECORATION)


def _identifier_recorded(text, identifier):
    """True when the identifier occupies a structural position.

    Two positions count, and only these two: a heading line that names
    the identifier, and the leading cell of a table row where the cell
    is the identifier alone. Everything else — including prose that
    merely mentions the identifier — is not a record of it.
    """
    for line in text.splitlines():
        if HEADING.match(line) and _names_token(line, identifier):
            return True
        if _leading_cell(line) == identifier:
            return True
    return False


class RegisterFileProvenance(ProvenanceResolver):
    """Resolves identifiers against two governance register files."""

    def __init__(self, finding_register, decision_register):
        self._finding_register = Path(finding_register)
        self._decision_register = Path(decision_register)

    def _read(self, path):
        if not path.is_file():
            return None
        return path.read_text(encoding="utf-8")

    def finding_exists(self, finding_id):
        text = self._read(self._finding_register)
        return text is not None and _identifier_recorded(text, finding_id)

    def decision_exists(self, decision_id):
        text = self._read(self._decision_register)
        return text is not None and _identifier_recorded(text, decision_id)


def authorizing_act_is_well_formed(act):
    """The authorizing act must name a directive, e.g. `P7-I52`."""
    return bool(AUTHORIZING_ACT.match(act))
