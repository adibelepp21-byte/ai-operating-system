"""`ACT-CC-P12-008 §10` — falsification for the corrected consumer measurement.

Five mandatory negative controls, one class each, plus the controls that keep
the semantic classification honest. The measurement being checked answers two
questions that were conflated for as long as it was written:

```text
who imports the surface        →  importers_of()
who actually consumes it (§16) →  consumers_of()
```

`§9` forbids correcting a metric toward a desired W6 state, so the controls
here are written to fail if the correction over-reaches as readily as if it
under-reaches: `NC-02` and `NC-03` both drive the measurement to find *fewer*
consumers, and `NC-04` is the one that would fail if the correction had simply
counted every importer to make `CONSUMER` satisfy.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools import p12_state_verification as sv
from tools import p12_consumer_evidence_verifier as cev

REPO_ROOT = Path(__file__).resolve().parents[2]
SURFACE = "tools.p12_operational_state"


def _world(files: dict) -> tempfile.TemporaryDirectory:
    tmp = tempfile.TemporaryDirectory()
    for name, body in files.items():
        path = Path(tmp.name) / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")
    return tmp


class NC01ThePreviouslyMissedImportShape(unittest.TestCase):
    """The shape every resident importer uses, and the one the superseded
    implementation could not see: `node.module` is ``tools``, and the surface's
    name is in `alias.name`."""

    SHAPES = {
        "plain.py": "from pkg import surface\nE = surface.project()\n",
        "aliased.py": "from pkg import surface as s\nE = s.project()\n",
        "dotted.py": "import pkg.surface\nE = pkg.surface.project()\n",
        "dotted_alias.py": "import pkg.surface as s\nE = s.project()\n",
        "member.py": "from pkg.surface import project\nE = project()\n",
    }

    def test_every_resident_import_form_is_recognized(self):
        files = {"pkg/__init__.py": "", "pkg/surface.py": "def project():\n    return ()\n"}
        files.update(self.SHAPES)
        tmp = _world(files)
        self.addCleanup(tmp.cleanup)
        with mock.patch.object(sv, "REPO_ROOT", Path(tmp.name)):
            found = set(sv.consumers_of("pkg.surface"))
        self.assertEqual(set(self.SHAPES), found)

    def test_the_superseded_rule_missed_the_aliased_form(self):
        """Kept as a control on the fix: the old rule collected only
        `node.module`, which is ``pkg`` for four of the five shapes above."""
        import ast
        tree = ast.parse(self.SHAPES["aliased.py"])
        old_shape = [n.module for n in ast.walk(tree)
                     if isinstance(n, ast.ImportFrom) and n.module]
        self.assertEqual(["pkg"], old_shape)
        self.assertNotIn("surface", old_shape[0])

    def test_the_live_surface_is_imported_through_that_shape(self):
        self.assertEqual(3, len(sv.importers_of(SURFACE)))


class NC02AnIrrelevantTextualReference(unittest.TestCase):
    """A file that merely spells the identifier must not become a consumer."""

    def test_prose_and_strings_naming_the_surface_are_not_imports(self):
        tmp = _world({
            "pkg/__init__.py": "",
            "pkg/surface.py": "def project():\n    return ()\n",
            "talker.py": ('"""A module about pkg.surface and surface.project."""\n'
                          'NOTE = "from pkg import surface"\n'
                          '# import pkg.surface\n'
                          'OTHER = "surface.project()"\n'),
        })
        self.addCleanup(tmp.cleanup)
        with mock.patch.object(sv, "REPO_ROOT", Path(tmp.name)):
            self.assertEqual((), sv.importers_of("pkg.surface"))
            self.assertEqual((), sv.consumers_of("pkg.surface"))


class NC03AnUnrelatedImport(unittest.TestCase):
    """An import that does not establish the relation must not count —
    including the prefix case the superseded implementation got wrong in the
    *opposite* direction from `NC-01`."""

    def test_a_module_whose_name_contains_the_surfaces_is_not_the_surface(self):
        tmp = _world({
            "pkg/__init__.py": "",
            "pkg/surface.py": "def project():\n    return ()\n",
            "pkg/surface_verifier.py": "def project():\n    return ()\n",
            "reader.py": "from pkg import surface_verifier as v\nE = v.project()\n",
        })
        self.addCleanup(tmp.cleanup)
        with mock.patch.object(sv, "REPO_ROOT", Path(tmp.name)):
            self.assertEqual((), sv.importers_of("pkg.surface"))
            self.assertEqual(("reader.py",),
                             sv.importers_of("pkg.surface_verifier"))

    def test_the_superseded_rule_would_have_counted_the_prefix_match(self):
        """`"p12_operational_state" in "tools.p12_operational_state_verifier"`
        is `True`. The old expression was `any(stem in module ...)`, so the
        same line that missed a real consumer would have invented a false one."""
        self.assertIn("p12_operational_state", "tools.p12_operational_state_verifier")
        self.assertNotIn("tools/p12_operational_state_verifier.py",
                         sv.importers_of(SURFACE))

    def test_an_unrelated_module_is_not_a_consumer(self):
        tmp = _world({
            "pkg/__init__.py": "",
            "pkg/surface.py": "def project():\n    return ()\n",
            "elsewhere.py": "import json\nE = json.dumps({})\n",
        })
        self.addCleanup(tmp.cleanup)
        with mock.patch.object(sv, "REPO_ROOT", Path(tmp.name)):
            self.assertEqual((), sv.importers_of("pkg.surface"))


class NC04VerifierOnlyUsage(unittest.TestCase):
    """`§16` names `verification` a consumer kind — and still requires evidence
    that the module *actually consumes the state*. Both halves are controlled
    here: a verifier is not disqualified for being one, and an importer that
    only ever reads its own substituted fixture is not promoted for being one.
    """

    def test_an_importer_that_never_reads_is_not_a_consumer(self):
        tmp = _world({
            "pkg/__init__.py": "",
            "pkg/surface.py": "def project():\n    return ()\n",
            "importer.py": "from pkg import surface as s\nNAME = s.__name__\n",
        })
        self.addCleanup(tmp.cleanup)
        with mock.patch.object(sv, "REPO_ROOT", Path(tmp.name)):
            self.assertEqual(("importer.py",), sv.importers_of("pkg.surface"))
            self.assertEqual((), sv.consumers_of("pkg.surface"))

    def test_a_read_over_a_substituted_source_set_is_not_a_consumption(self):
        tmp = _world({
            "pkg/__init__.py": "",
            "pkg/surface.py": "SOURCES = ()\ndef project():\n    return ()\n",
            "fixture.py": ("from unittest import mock\n"
                           "from pkg import surface as s\n"
                           "def probe():\n"
                           "    with mock.patch.object(s, 'SOURCES', ()):\n"
                           "        return s.project()\n"),
        })
        self.addCleanup(tmp.cleanup)
        with mock.patch.object(sv, "REPO_ROOT", Path(tmp.name)):
            evidence = {e.module: e for e in sv.consumption_evidence("pkg.surface")}
            self.assertEqual((), evidence["fixture.py"].reads)
            self.assertEqual(("project",), evidence["fixture.py"].fixture_reads)
            self.assertEqual((), sv.consumers_of("pkg.surface"))

    def test_the_resident_fixture_only_reader_is_excluded(self):
        self.assertIn("tools/p12_mutation_verification.py",
                      sv.importers_of(SURFACE))
        self.assertNotIn("tools/p12_mutation_verification.py",
                         sv.consumers_of(SURFACE))

    def test_a_verifier_that_really_reads_is_included(self):
        """The inverse control. If this ever stops holding, the correction has
        started disqualifying a kind `§16` names."""
        self.assertIn("tools/p12_negative_control_verification.py",
                      sv.consumers_of(SURFACE))

    def test_dynamic_observation_reaches_the_same_split(self):
        """Independent of the AST entirely: the runtime observer watches the
        substitution happen."""
        by_module = {o.module: o for o in cev.observations()}
        fixture_only = by_module["tools.p12_mutation_verification"]
        self.assertEqual((), fixture_only.resident_reads)
        self.assertTrue(fixture_only.substituted_reads)
        real = by_module["tools.p12_self_model_contract"]
        self.assertTrue(real.resident_reads)


class NC05FreshProcessReproduction(unittest.TestCase):
    """The measurement must not depend on state held by this process."""

    def test_the_corrected_measurement_reproduces_in_a_fresh_process(self):
        code = ("import sys; sys.path.insert(0, %r)\n"
                "from tools import p12_state_verification as sv\n"
                "print(sv.consumers_of(sv.SURFACE))\n"
                "print(sv.importers_of(sv.SURFACE))\n"
                "print({r.link: r.status for r in sv.verify()}['CONSUMER'])\n"
                % str(REPO_ROOT))
        result = subprocess.run([sys.executable, "-c", code],
                                capture_output=True, text=True, cwd=REPO_ROOT)
        self.assertEqual(0, result.returncode, result.stderr)
        lines = result.stdout.strip().splitlines()
        self.assertEqual(repr(sv.consumers_of(SURFACE)), lines[0])
        self.assertEqual(repr(sv.importers_of(SURFACE)), lines[1])
        self.assertEqual("SATISFIED", lines[2])


class TheSemanticClassificationRestsOnTheInstrument(unittest.TestCase):
    """`§3` / `§8` — the kinds come from `§16`'s body, not from this module.

    `ACT-CC-P12-006` and `-007` recorded *"is a verifier a consumer?"* as
    semantically unsettled. It was not: `§16 State Consumers` enumerates the
    kinds, and `verification`, `self-model`, `observability` and `evidence` are
    four of the nine. The prior classification was taken from this module's own
    docstring, which quotes `§16`'s first and last sentences and omits the list
    between them — precisely the reading `§3` forbids.
    """

    BLUEPRINT = ("docs/architecture/p12/"
                 "AIOS_P12_ROADMAP_PRD_CONSTRUCTION_BLUEPRINT_v1.0.md")

    def test_the_enumerated_kinds_are_the_instruments_own(self):
        body = (REPO_ROOT / self.BLUEPRINT).read_text(encoding="utf-8")
        start = body.index("16. State Consumers")
        section = body[start:body.index("17. State Authority", start)]
        for kind in sv.CONSUMER_KINDS:
            with self.subTest(kind):
                self.assertIn(kind, section)

    def test_verification_and_self_model_are_named_consumer_kinds(self):
        self.assertIn("verification", sv.CONSUMER_KINDS)
        self.assertIn("self-model", sv.CONSUMER_KINDS)

    def test_the_evidence_requirement_is_the_instruments_own(self):
        body = (REPO_ROOT / self.BLUEPRINT).read_text(encoding="utf-8")
        self.assertIn(
            "Each claimed consumer requires evidence that it actually "
            "consumes the state.", body)

    def test_a_test_module_is_still_not_a_consumer(self):
        """`§16` lists nine kinds and `test` is not among them."""
        self.assertNotIn("test", sv.CONSUMER_KINDS)
        self.assertFalse([c for c in sv.importers_of(SURFACE) if "test" in c])


class TheMeasurementReadsNothingItShouldNotWrite(unittest.TestCase):
    def test_neither_module_writes(self):
        import ast
        for module in ("p12_state_verification.py",
                       "p12_consumer_evidence_verifier.py"):
            with self.subTest(module):
                source = (REPO_ROOT / "tools" / module).read_text(encoding="utf-8")
                names = {n.func.attr for n in ast.walk(ast.parse(source))
                         if isinstance(n, ast.Call)
                         and isinstance(n.func, ast.Attribute)}
                for forbidden in ("write_text", "mkdir", "unlink", "replace"):
                    self.assertNotIn(forbidden, names)

    def test_the_independent_verifier_does_not_import_the_measurement(self):
        """`§4.1.C` — independence, read by AST rather than asserted."""
        import ast
        tree = ast.parse((REPO_ROOT / "tools" /
                          "p12_consumer_evidence_verifier.py")
                         .read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                imported.update(f"{node.module}.{a.name}" for a in node.names)
            elif isinstance(node, ast.Import):
                imported.update(a.name for a in node.names)
        offending = [n for n in imported if "p12_state_verification" in n
                     and not n.endswith(".main")]
        self.assertEqual([], offending,
                         "the verifier must not import what it verifies; the "
                         "claim is passed in by the caller")


if __name__ == "__main__":
    unittest.main()
