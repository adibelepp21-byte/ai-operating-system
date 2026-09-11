"""
Line-boundary coherence between the deriver and the verifier.

`tools/derived_views.py` emits ``REGISTER:<number>`` as a **citable governance
pointer** — the locator a reader follows to check a lineage edge against the
Governance Decision Register. `tools/corpus_citation_audit.py` verifies
citations of exactly that shape.

If the two disagreed about what a line *is*, one tool's output would be
uncheckable by the other, and the disagreement would be **silent**: both would
report success while pointing at different text. Cycle 26 showed this is not
theoretical — ``str.splitlines()`` breaks on U+2028, U+0085 and related
separators that ``sed``, editors, and this corpus's own citations do not, and
fifty Markdown bodies under ``docs/architecture/volume-2/`` contain them.

So the property is asserted directly rather than assumed from two docstrings
that happen to say the same thing.

The hostile fixture is **built with** ``chr()`` **at import time**, never pasted
as literal characters, so the separators cannot be silently lost or normalised
by an editor, a diff viewer, or a terminal that renders them invisibly.
"""

from __future__ import annotations

import io
import re
import tempfile
import tokenize
import unittest
from pathlib import Path

from tools.corpus_citation_audit import _lines as audit_lines
from tools.derived_views import REGISTER
from tools.derived_views import _lines as derive_lines
from tools.governance_index import REPO_ROOT

#: Code points ``str.splitlines()`` treats as line breaks and a newline-only
#: split does not. Built numerically on purpose — see the module docstring.
SEPARATOR_CODE_POINTS = (
    0x2028,  # LINE SEPARATOR
    0x2029,  # PARAGRAPH SEPARATOR
    0x0085,  # NEXT LINE
    0x000B,  # LINE TABULATION
    0x000C,  # FORM FEED
    0x001C,  # FILE SEPARATOR
    0x001D,  # GROUP SEPARATOR
    0x001E,  # RECORD SEPARATOR
)

NON_NEWLINE_SEPARATORS = tuple(chr(point) for point in SEPARATOR_CODE_POINTS)

HOSTILE = "\n".join(
    ["first line"]
    + [
        "sep %d before%safter" % (index, separator)
        for index, separator in enumerate(NON_NEWLINE_SEPARATORS)
    ]
    + ["last line"]
)


def _write(text: str) -> Path:
    handle = tempfile.NamedTemporaryFile(
        "w", suffix=".md", encoding="utf-8", delete=False
    )
    handle.write(text)
    handle.close()
    return Path(handle.name)


def _code_without_strings(source: str) -> str:
    """Drop string literals, so prose *about* ``splitlines`` is not a call site.

    Written after an earlier version of this check failed on its own docstring.
    """
    kept = []
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type in (tokenize.STRING, tokenize.COMMENT):
            continue
        kept.append(token.string)
    return " ".join(kept)


class TheFixtureIsActuallyHostile(unittest.TestCase):
    """A coherence test over a benign fixture would prove nothing."""

    def test_the_python_default_splits_the_fixture_differently(self) -> None:
        self.assertNotEqual(
            len(HOSTILE.splitlines()),
            len(HOSTILE.split("\n")),
            "fixture no longer distinguishes the two splitting rules",
        )

    def test_every_separator_is_one_character_and_is_not_a_newline(self) -> None:
        for separator in NON_NEWLINE_SEPARATORS:
            self.assertEqual(len(separator), 1, repr(separator))
            self.assertNotEqual(separator, "\n", "a newline is not a counter-example")
            self.assertEqual(len(("a%sb" % separator).splitlines()), 2, repr(separator))


class TheDeriverAndTheVerifierAgree(unittest.TestCase):
    """The property that makes a derived citation checkable."""

    def test_they_agree_on_the_hostile_fixture(self) -> None:
        path = _write(HOSTILE)
        try:
            self.assertEqual(derive_lines(HOSTILE), audit_lines(path))
        finally:
            path.unlink()

    def test_they_agree_on_the_register_the_deriver_actually_cites(self) -> None:
        register = REPO_ROOT / REGISTER
        self.assertTrue(register.is_file(), REGISTER)
        self.assertEqual(
            derive_lines(register.read_text(encoding="utf-8")),
            audit_lines(register),
        )

    def test_neither_treats_a_separator_as_a_line_break(self) -> None:
        for separator in NON_NEWLINE_SEPARATORS:
            text = "alpha%sbeta" % separator
            path = _write(text)
            try:
                self.assertEqual(derive_lines(text), [text], repr(separator))
                self.assertEqual(audit_lines(path), [text], repr(separator))
            finally:
                path.unlink()


class NoToolInTheCitationFabricUsesThePythonDefault(unittest.TestCase):
    """Agreement today is not the same as agreement by construction.

    **The population was incomplete until `ACT-CC-P11-015`.** It listed the two
    tools that existed when the invariant was written. `tools/stale_state_audit.py`
    was added afterwards, emits findings as ``f"{rel}:{index + 1}"`` — the same
    ``path:line`` form this corpus cites and that `corpus_citation_audit`
    verifies — and its own ``_lines`` docstring claims *"the same rule the
    citation auditor and ``derived_views`` use."*

    It obeyed the rule by **convention**, and nothing held it to one. Changing
    its ``_lines`` to ``str.splitlines()`` would have broken cross-tool line
    agreement with every check still green.

    That is the third time in this programme that a control's population has
    been narrower than the invariant it names — after a loader that read one of
    two operational roots, and a continuity reader that knew one evidence
    filename. **A control that covers part of its population does not fail; it
    passes, on the part it covers.**
    """

    #: Every tool that publishes a ``path:line`` locator into the citation
    #: fabric. A tool joins this list when it emits one — not when someone
    #: remembers to add it.
    MODULES = ("tools/derived_views.py", "tools/corpus_citation_audit.py",
               "tools/stale_state_audit.py")

    def test_no_splitlines_call_survives_in_either_module(self) -> None:
        # ``.`` and ``splitlines`` are separate tokens, so the stripper's
        # single-space join can sit between them. An earlier version of this
        # pattern had no ``\s*`` there and could never have matched a real
        # call; the meta-test below is what caught it.
        call = re.compile(r"\.\s*splitlines\s*\(")
        for name in self.MODULES:
            code = _code_without_strings(
                (REPO_ROOT / name).read_text(encoding="utf-8")
            )
            self.assertIsNone(
                call.search(code),
                "%s calls str.splitlines(); the agreement above is accidental" % name,
            )

    def test_every_tool_emitting_a_path_line_locator_is_covered(self) -> None:
        """The guard that makes the list self-correcting.

        Without it, the next tool to emit ``path:line`` joins the fabric and
        silently escapes the invariant — which is exactly how this list came to
        be missing one.
        """
        # Keyed on the locator **alone**. The first version of this guard also
        # required the literal ``"source"`` to appear, which
        # ``derived_views.py`` does not contain — it passes ``source=`` as a
        # keyword. Dropping that module from ``MODULES`` then produced **no
        # finding at all**: a completeness guard with an incomplete population,
        # which is the defect it exists to catch, one level up. Caught by
        # mutating the list rather than by reading the code.
        locator = re.compile(r'f"\{[^"{}]*\}:\{[^"{}]*\}"')
        emitters = {
            "tools/%s" % path.name
            for path in sorted((REPO_ROOT / "tools").glob("*.py"))
            if locator.search(path.read_text(encoding="utf-8"))
        }
        self.assertTrue(emitters, "precondition: no emitter found at all")
        self.assertLessEqual(
            emitters, set(self.MODULES),
            "these emit a path:line locator and are not held to the "
            "newline-only rule: %s" % sorted(emitters - set(self.MODULES)))

    def test_the_check_still_sees_a_call_it_should_reject(self) -> None:
        """Guard against a stripper that deletes everything and passes."""
        code = _code_without_strings('x = "splitlines"\ny = text.splitlines()\n')
        self.assertIsNotNone(re.compile(r"\.\s*splitlines\s*\(").search(code))


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
