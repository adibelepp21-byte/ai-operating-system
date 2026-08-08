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

Assumption: an identifier is considered resolvable when it appears in
its register file as a heading or table identifier. Matching is on the
exact token, not a substring of a longer identifier — `GDR-001` must not
resolve merely because `GDR-0012` exists.

False-positive risk: low. False-negative risk: an identifier recorded in
a register by some form other than a literal token would not resolve,
and would fail closed.
"""

import re
from abc import ABC, abstractmethod
from pathlib import Path

AUTHORIZING_ACT = re.compile(r"^P\d+-I\d+$")


class ProvenanceResolver(ABC):
    """Declares the resolution contract. Implementations are read-only."""

    @abstractmethod
    def finding_exists(self, finding_id):
        """True when the finding identifier is recorded."""

    @abstractmethod
    def decision_exists(self, decision_id):
        """True when the governance decision identifier is recorded."""


def _token_present(text, token):
    return re.search(rf"(?<![0-9A-Za-z-]){re.escape(token)}(?![0-9A-Za-z-])", text) is not None


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
        return text is not None and _token_present(text, finding_id)

    def decision_exists(self, decision_id):
        text = self._read(self._decision_register)
        return text is not None and _token_present(text, decision_id)


def authorizing_act_is_well_formed(act):
    """The authorizing act must name a directive, e.g. `P7-I52`."""
    return bool(AUTHORIZING_ACT.match(act))
