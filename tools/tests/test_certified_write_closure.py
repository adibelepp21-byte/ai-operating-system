"""`GOAL-V2-004` — certified-evidence write closure for P10, P11 and P12.

```text
PREVENTION  tools/certified_write_barrier.py     every write API, refused first
DETECTION   tools/certified_evidence_integrity   every certified phase, by content
```

**Discipline.** No test here attempts a write into the real certified tree
unless it has first asserted that the write will be refused. Every mutation
(changed, added, deleted or unreadable files, an altered reference) runs
against a temporary copy. A broken barrier therefore fails these tests without
damaging certified evidence. `GOAL-V2-002` learned this the hard way
(record, X-3/X-4).
"""

from __future__ import annotations

import ast
import json
import os
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from tools import certified_evidence_integrity as integrity
from tools import certified_write_barrier as barrier
from tools import certified_write_probe as probe
from tools import p12_certified_evidence_guard as sentinel

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOTS = ("docs/architecture/platform-organization", "docs/architecture/p11",
         "docs/architecture/p12")
INSTRUMENTS = (
    "docs/governance/acts/FD-P10-005-CERTIFICATION-OF-PHASE-10-DEPARTMENT-ECOSYSTEM.md",
    "docs/governance/acts/FD-P11-002-P11-CERTIFICATION.md",
    "docs/governance/acts/FD-P12-006-P12-CERTIFICATION-AND-LIVE-VERIFICATION.md",
)
REFERENCES = (
    "docs/governance/AIOS_P10_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json",
    "docs/governance/AIOS_P11_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json",
    "docs/governance/AIOS_P12_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json",
    "docs/governance/AIOS_CERTIFIED_EVIDENCE_MANIFEST_INDEX_v1.0.json",
)
P11_FILE = "docs/architecture/p11/w4-operations/engineering-intelligence-instance-001.instance.json"
HANDOFF = ("docs/architecture/p12/AIOS-P12-FINAL-CERTIFICATION-AND-P13-"
           "TRANSITION-HANDOFF-RECORD.md")


class TheBarrierIsInstalledByTheToolsPackage(unittest.TestCase):

    def test_importing_tools_installs_it_determined_not_failed_closed(self):
        status = barrier.status()
        self.assertTrue(status["installed"])
        self.assertFalse(status["fail_closed"], status["determined_by"])
        self.assertEqual(status["determined_by"], "guard+manifests")

    def test_every_certified_root_instrument_and_reference_is_protected(self):
        for relative in ROOTS + INSTRUMENTS + REFERENCES:
            self.assertTrue(barrier.refuses(REPO_ROOT / relative), relative)
        for relative in ROOTS:
            self.assertTrue(barrier.refuses(REPO_ROOT / relative / "new.json"))

    def test_an_ancestor_of_a_certified_root_is_protected_from_removal(self):
        self.assertTrue(barrier.refuses(REPO_ROOT / "docs/architecture",
                                        ancestors=True))
        self.assertFalse(barrier.refuses(REPO_ROOT / "docs/architecture/x.md"))

    def test_live_state_and_ordinary_work_stay_writable(self):
        """The barrier refuses what certification froze, and nothing else."""
        for relative in ("docs/operations/runtime-observations/x.observation.json",
                         "docs/governance/acts/NEW-ACT.md",
                         "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md",
                         "docs/architecture/candidates/x.md"):
            self.assertFalse(barrier.refuses(REPO_ROOT / relative), relative)
        with tempfile.TemporaryDirectory() as tmp:
            self.assertFalse(barrier.refuses(Path(tmp) / "x"))

    def test_installation_is_idempotent(self):
        self.assertIs(barrier.install(), barrier.install())

    def test_a_python_child_starts_barriered(self):
        """A child does not inherit an audit hook. It inherits the bootstrap."""
        target = REPO_ROOT / "docs/architecture/p12/zz-child-probe.txt"
        self.assertTrue(barrier.refuses(target))
        program = (
            "import sys\n"
            "from tools import certified_write_barrier as b\n"
            "p = sys.argv[1]\n"
            "if not (b.installed() and b.refuses(p)):\n"
            "    print('UNPROTECTED'); raise SystemExit(3)\n"
            "try:\n"
            "    open(p, 'w')\n"
            "except b.CertifiedWriteRefused:\n"
            "    print('REFUSED')\n"
        )
        done = subprocess.run([sys.executable, "-c", program, str(target)],
                              capture_output=True, text=True, cwd=str(REPO_ROOT))
        self.assertEqual(done.stdout.strip(), "REFUSED", done.stderr)
        self.assertFalse(target.exists())


class EveryWriteApiIsRefusedBeforeItBegins(unittest.TestCase):
    """The same refusal, whatever API a writer reaches for.

    Aimed at a temporary root added through `protecting()`, which is additive.
    Each case asserts the refusal *and* that nothing changed.
    """

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        base = Path(self._tmp.name)
        self.root = base / "certified"
        self.root.mkdir()
        (self.root / "sub").mkdir()
        self.file = self.root / "evidence.json"
        self.file.write_text("certified", encoding="utf-8")
        self.outside = base / "outside"
        self.outside.mkdir()
        (self.outside / "src.txt").write_text("new", encoding="utf-8")
        self._ctx = barrier.protecting(self.root)
        self._ctx.__enter__()

    def tearDown(self):
        self._ctx.__exit__(None, None, None)
        self._tmp.cleanup()

    def _refused(self, action):
        with self.assertRaises(barrier.CertifiedWriteRefused):
            action()
        self.assertEqual(self.file.read_text(encoding="utf-8"), "certified")
        self.assertEqual(sorted(p.name for p in self.root.iterdir()),
                         ["evidence.json", "sub"])

    def test_reading_is_not_refused(self):
        self.assertEqual(self.file.read_text(encoding="utf-8"), "certified")
        with open(self.file, "rb") as handle:
            self.assertEqual(handle.read(), b"certified")

    def test_write_text_and_write_bytes(self):
        self._refused(lambda: self.file.write_text("x"))
        self._refused(lambda: self.file.write_bytes(b"x"))
        self._refused(lambda: (self.root / "new.json").write_text("x"))

    def test_open_in_every_writing_mode(self):
        for mode in ("w", "a", "x", "r+", "wb", "ab", "rb+"):
            target = self.root / "new.json" if mode == "x" else self.file
            self._refused(lambda: open(target, mode))

    def test_os_open_with_writing_flags(self):
        for flags in (os.O_WRONLY, os.O_RDWR, os.O_WRONLY | os.O_APPEND,
                      os.O_CREAT | os.O_WRONLY, os.O_TRUNC | os.O_WRONLY):
            self._refused(lambda: os.open(self.file, flags))

    def test_json_dump_through_an_open_handle(self):
        self._refused(lambda: json.dump({}, open(self.file, "w")))

    def test_replace_and_rename_into_and_out_of(self):
        self._refused(lambda: os.replace(self.outside / "src.txt", self.file))
        self._refused(lambda: os.rename(self.outside / "src.txt",
                                        self.root / "new.json"))
        self._refused(lambda: os.rename(self.file, self.outside / "moved"))
        self._refused(lambda: os.rename(self.root, self.outside / "moved"))

    def test_remove_unlink_rmdir_and_rmtree(self):
        self._refused(lambda: os.remove(self.file))
        self._refused(lambda: self.file.unlink())
        self._refused(lambda: os.rmdir(self.root / "sub"))
        self._refused(lambda: shutil.rmtree(self.root))
        self._refused(lambda: shutil.rmtree(self.root.parent))

    def test_mkdir_and_touch(self):
        self._refused(lambda: (self.root / "newdir").mkdir())
        self._refused(lambda: (self.root / "new.json").touch())
        self._refused(lambda: self.file.touch())
        # An existing directory with exist_ok writes nothing, and is not refused.
        (self.root / "sub").mkdir(exist_ok=True)

    def test_truncate_chmod_and_utime(self):
        self._refused(lambda: os.truncate(self.file, 0))
        self._refused(lambda: os.chmod(self.file, 0o600))
        self._refused(lambda: os.utime(self.file, (0, 0)))

    def test_links_into_and_out_of(self):
        self._refused(lambda: os.link(self.file, self.outside / "hard"))
        self._refused(lambda: os.symlink(self.outside / "src.txt",
                                         self.root / "link"))

    def test_the_shutil_copy_and_move_family(self):
        src = self.outside / "src.txt"
        self._refused(lambda: shutil.copyfile(src, self.file))
        self._refused(lambda: shutil.copy(src, self.root / "new.json"))
        self._refused(lambda: shutil.copy2(src, self.file))
        self._refused(lambda: shutil.copytree(self.outside, self.root / "tree"))
        self._refused(lambda: shutil.move(src, self.root / "new.json"))
        self._refused(lambda: shutil.move(self.file, self.outside / "out"))

    def test_sqlite_on_a_certified_path(self):
        self._refused(lambda: sqlite3.connect(self.root / "store.db"))

    def test_a_symlink_from_outside_does_not_launder_the_target(self):
        link = self.outside / "alias"
        os.symlink(self.root, link)
        self._refused(lambda: (link / "evidence.json").write_text("x"))

    def test_a_relative_path_is_resolved_before_it_is_judged(self):
        cwd = os.getcwd()
        os.chdir(self.root)
        try:
            self._refused(lambda: open("evidence.json", "a"))
        finally:
            os.chdir(cwd)

    def test_it_is_a_permission_error_too(self):
        with self.assertRaises(PermissionError):
            self.file.write_text("x")
        with self.assertRaises(sentinel.CertifiedEvidenceProtected):
            self.file.write_text("x")


class ProcessLaunchesAreGoverned(unittest.TestCase):

    def _refused(self, action):
        with self.assertRaises(barrier.CertifiedWriteRefused):
            action()

    def test_a_shell_is_refused(self):
        self._refused(lambda: subprocess.run(["sh", "-c", "true"]))
        self._refused(lambda: subprocess.run("true", shell=True))
        self._refused(lambda: os.system("true"))

    def test_an_unknown_program_is_refused(self):
        self._refused(lambda: subprocess.run(["true"]))

    def test_read_only_git_runs(self):
        done = subprocess.run(["git", "rev-parse", "HEAD"], cwd=str(REPO_ROOT),
                              capture_output=True, text=True)
        self.assertEqual(done.returncode, 0)

    def test_git_that_could_write_this_tree_is_refused(self):
        """Asked, not run: a broken barrier must not get to run it."""
        state = barrier.install()
        for argv in (["git", "checkout", "--", "docs"],
                     ["git", "restore", "docs/architecture/p12"],
                     ["git", "-C", str(REPO_ROOT), "reset", "--hard"],
                     ["git", "stash"],
                     ["git", "diff", "--output=docs/architecture/p12/x"]):
            self.assertFalse(barrier._launch_permitted(
                state, None, argv, str(REPO_ROOT), None), argv)

    def test_git_against_another_tree_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            done = subprocess.run(["git", "-C", tmp, "init", "-q"],
                                  capture_output=True)
            self.assertEqual(done.returncode, 0)

    def test_a_python_child_that_would_skip_the_bootstrap_is_refused(self):
        self._refused(lambda: subprocess.run([sys.executable, "-c", "pass"],
                                             env={}))
        self._refused(lambda: subprocess.run([sys.executable, "-I", "-c", "pass"]))
        self._refused(lambda: subprocess.run([sys.executable, "-S", "-c", "pass"]))
        self._refused(lambda: subprocess.run([sys.executable, "-E", "-c", "pass"]))


class ItFailsClosedWhenProtectionCannotBeDetermined(unittest.TestCase):

    def test_an_unreadable_reference_refuses_every_write_in_the_repository(self):
        """In a child, so the test process gains no hook over a temp root."""
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            (repo / "docs/governance").mkdir(parents=True)
            (repo / "docs/governance/AIOS_PX_CERTIFIED_EVIDENCE_MANIFEST_v1.0.json"
             ).write_text("{", encoding="utf-8")
            outside = Path(tmp) / "outside.txt"
            program = (
                "import sys\nfrom pathlib import Path\n"
                "from tools import certified_write_barrier as b\n"
                "s = b.install(Path(sys.argv[1]))\n"
                "print('FAIL-CLOSED' if s.fail_closed else 'DETERMINED')\n"
                "try:\n"
                "    open(Path(sys.argv[1]) / 'anything.txt', 'w')\n"
                "    print('WROTE')\n"
                "except b.CertifiedWriteRefused:\n"
                "    print('REFUSED')\n"
                "open(sys.argv[2], 'w').write('ok'); print('OUTSIDE-OK')\n"
            )
            done = subprocess.run(
                [sys.executable, "-c", program, str(repo), str(outside)],
                capture_output=True, text=True, cwd=str(REPO_ROOT))
            self.assertEqual(done.stdout.split(),
                             ["FAIL-CLOSED", "REFUSED", "OUTSIDE-OK"], done.stderr)
            self.assertFalse((repo / "anything.txt").exists())


_WRITE_CALLS = {"write_text", "write_bytes", "open", "mkdir", "makedirs", "touch",
                "unlink", "remove", "rmtree", "rename", "dump", "run", "Popen",
                "system", "copyfile", "copytree", "move", "truncate"}


def _is_main_guard(node: ast.AST) -> bool:
    return (isinstance(node, ast.If) and "__name__" in ast.unparse(node.test)
            and "__main__" in ast.unparse(node.test))


def _imports_tools(node: ast.AST) -> bool:
    if isinstance(node, ast.Import):
        return any(a.name.split(".")[0] == "tools" for a in node.names)
    return (isinstance(node, ast.ImportFrom) and not node.level
            and (node.module or "").split(".")[0] == "tools")


class EveryEntryPointInstallsTheBarrierBeforeItCanWrite(unittest.TestCase):
    """Static completeness. The probe shows the same thing by running them."""

    @classmethod
    def setUpClass(cls):
        found = probe.discover(REPO_ROOT)
        cls.entries = found["root"] + found["tools"] + found["package"] + found["other"]

    def test_entry_points_were_found(self):
        self.assertGreaterEqual(len(self.entries), 59)

    def test_each_installs_it_on_every_route_it_can_be_run_by(self):
        """Run with `-m`, a module in `tools` imports the package first.

        Run by path, it must import `tools` at module level before anything
        else runs. Otherwise it must do so as the first act of its `__main__`
        block. The one other safe shape is a module whose imports are relative,
        which cannot run by path at all: it fails at import, before any code.
        """
        uncovered = []
        for name in self.entries:
            tree = ast.parse((REPO_ROOT / name).read_text(encoding="utf-8"))
            first = next((s for s in tree.body
                          if isinstance(s, (ast.Import, ast.ImportFrom))
                          and (_imports_tools(s) or getattr(s, "level", 0))), None)
            if first is not None:
                continue
            guards = [s for s in tree.body if _is_main_guard(s)]
            head = guards[-1].body[:4] if guards else []
            if not any(_imports_tools(s) for s in head):
                uncovered.append(name)
        self.assertEqual(uncovered, [])

    def test_no_entry_point_writes_at_module_level(self):
        """The barrier is installed by import or at the start of `__main__`.
        Nothing may write before that, so nothing may write at import time."""
        offenders = []
        for name in self.entries:
            tree = ast.parse((REPO_ROOT / name).read_text(encoding="utf-8"))
            for stmt in tree.body:
                if isinstance(stmt, (ast.FunctionDef, ast.AsyncFunctionDef,
                                     ast.ClassDef)) or _is_main_guard(stmt):
                    continue
                for node in ast.walk(stmt):
                    if isinstance(node, ast.Call):
                        func = node.func
                        called = (func.attr if isinstance(func, ast.Attribute)
                                  else getattr(func, "id", ""))
                        if called in _WRITE_CALLS:
                            offenders.append(f"{name}:{node.lineno}")
        self.assertEqual(offenders, [])

    def test_no_resident_code_writes_relative_to_a_directory_descriptor(self):
        """The one stated gap in the audit events: `os.open(..., dir_fd=)`
        does not report its `dir_fd`. Hold that nothing resident uses it."""
        users = []
        names = subprocess.run(["git", "ls-files", "*.py"], cwd=str(REPO_ROOT),
                               capture_output=True, text=True).stdout.split()
        for name in names:
            if "/tests/" in name or name.startswith("docs/"):
                continue
            path = REPO_ROOT / name
            if not path.is_file():
                continue
            if re.search(r"\bdir_fd\s*=", path.read_text(encoding="utf-8")):
                users.append(name)
        # The barrier resolves `dir_fd` for the events that do carry it.
        self.assertEqual([u for u in users if u != "tools/certified_write_barrier.py"],
                         [])


def _copy_reference(tmp: Path) -> Path:
    """A disposable copy of everything detection reads."""
    repo = tmp / "repo"
    for relative in ROOTS:
        shutil.copytree(REPO_ROOT / relative, repo / relative,
                        ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(REPO_ROOT / "docs/governance/acts",
                    repo / "docs/governance/acts")
    for relative in REFERENCES + (
            "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md",):
        shutil.copyfile(REPO_ROOT / relative, repo / relative)
    return repo


class CertifiedEvidenceIsDetectedByContentForEveryPhase(unittest.TestCase):

    def test_every_certified_phase_holds(self):
        report = integrity.verify()
        self.assertTrue(report.holds, json.dumps(report.as_reported(), indent=1))
        counts = {k: len(v.intact) for k, v in report.phases.items()}
        self.assertEqual(counts, {"P10": 36, "P11": 58, "P12": 121})
        self.assertEqual(report.phases["P12"].declared_additions, (HANDOFF,))

    def test_every_certified_phase_has_a_manifest_and_nothing_else_does(self):
        index = integrity.load_index()
        certified = {f"P{n}" for n in sentinel.certified_phases()}
        self.assertEqual(set(index["phases"]), certified)

    def test_each_manifest_is_its_commit_not_a_claim(self):
        from tools import p12_certified_evidence_manifest as rebuild
        for phase, entry in integrity.load_index()["phases"].items():
            record = json.loads((REPO_ROOT / entry["manifest"]).read_text(
                encoding="utf-8"))
            rebuilt = rebuild.from_commit(entry["certified_commit"],
                                          evidence_root=entry["evidence_root"])
            if rebuilt is None:
                self.skipTest("certified commit not present in this clone")
            self.assertEqual(rebuilt, record["files"], phase)

    def test_the_p12_manifest_of_goal_002_is_unchanged_and_still_holds(self):
        from tools import p12_certified_evidence_manifest as p12
        self.assertTrue(p12.verify().holds)
        self.assertEqual(p12.verify().additions, (HANDOFF,))


class MutationControlsOnADisposableCopy(unittest.TestCase):
    """Each control is shown to fail loudly, and none touches the real tree."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = _copy_reference(Path(self._tmp.name))
        self.before = integrity.verify()

    def tearDown(self):
        self._tmp.cleanup()
        self.assertEqual(integrity.verify(), self.before,
                         "a mutation control changed the real tree")

    def _verify(self):
        return integrity.verify(repo_root=self.repo)

    def test_the_pristine_copy_holds(self):
        self.assertTrue(self._verify().holds,
                        json.dumps(self._verify().as_reported(), indent=1))

    def test_a_changed_certified_file_is_MODIFIED(self):
        target = P11_FILE
        (self.repo / target).write_text("changed", encoding="utf-8")
        report = self._verify()
        self.assertFalse(report.holds)
        self.assertEqual(report.phases["P11"].modified, (target,))

    def test_a_deleted_certified_file_is_MISSING(self):
        target = "docs/architecture/platform-organization/README.md"
        (self.repo / target).unlink()
        self.assertEqual(self._verify().phases["P10"].missing, (target,))

    def test_an_added_file_is_UNEXPECTED(self):
        target = "docs/architecture/p12/trace-stores/new.json"
        (self.repo / target).write_text("{}", encoding="utf-8")
        report = self._verify()
        self.assertFalse(report.holds)
        self.assertEqual(report.phases["P12"].unexpected, (target,))

    def test_an_unreadable_certified_path_is_UNREADABLE(self):
        target = P11_FILE
        (self.repo / target).unlink()
        (self.repo / target).mkdir()
        dangling = "docs/architecture/platform-organization/README.md"
        (self.repo / dangling).unlink()
        os.symlink(self.repo / "nowhere", self.repo / dangling)
        report = self._verify()
        self.assertEqual(report.phases["P11"].unreadable, (target,))
        self.assertEqual(report.phases["P10"].unreadable, (dangling,))

    def test_an_altered_manifest_is_a_reference_fault(self):
        path = self.repo / REFERENCES[1]
        record = json.loads(path.read_text(encoding="utf-8"))
        first = sorted(record["files"])[0]
        record["files"][first] = "0" * 64
        path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        report = self._verify()
        self.assertFalse(report.holds)
        self.assertIn("manifest altered", " ".join(report.phases["P11"].reference_faults))

    def test_an_altered_index_is_not_the_registered_index(self):
        path = self.repo / REFERENCES[3]
        record = json.loads(path.read_text(encoding="utf-8"))
        record["phases"]["P11"]["declared_additions"]["docs/architecture/p11/x"] = "?"
        path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        self.assertIn("index sha256 is not recorded in the Decision Register",
                      self._verify().faults)

    def test_an_altered_instrument_is_a_reference_fault(self):
        path = self.repo / INSTRUMENTS[0]
        path.write_text(path.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        faults = " ".join(self._verify().phases["P10"].reference_faults)
        self.assertIn("certifying instrument altered", faults)

    def test_a_certification_removed_from_the_register_is_a_fault(self):
        """Alter the certification reference: P12's resolution is struck."""
        register = self.repo / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
        register.write_text(register.read_text(encoding="utf-8").replace(
            "FD-P12-006", "FD-P12-XXX"), encoding="utf-8")
        self.assertIn("P12 has a manifest but is not certified",
                      self._verify().faults)

    def test_a_planted_instrument_does_not_resolve_on_a_shared_prefix(self):
        """`FD-P12-004`: a claim must resolve against a record. Before
        `GOAL-V2-004`, `_register_identity` accepted the prefix `FD-P12` for
        any `FD-P12-…` file, because the Register mentions other `FD-P12-`
        records. A planted, unregistered `FD-P12-999-…` instrument would
        therefore have resolved."""
        text = (self.repo / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
                ).read_text(encoding="utf-8")
        self.assertIsNone(sentinel._register_identity("FD-P12-999-FORGED", text))
        self.assertIsNotNone(sentinel._register_identity(
            "FD-P12-006-P12-CERTIFICATION-AND-LIVE-VERIFICATION", text))

    def test_a_deleted_manifest_is_a_fault(self):
        (self.repo / REFERENCES[0]).unlink()
        faults = " ".join(self._verify().phases["P10"].reference_faults)
        self.assertIn("manifest unreadable", faults)

    def test_a_struck_certification_does_not_unprotect_its_evidence(self):
        """Prevention reads the manifests too. Neither source can shrink it."""
        register = self.repo / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
        register.write_text(register.read_text(encoding="utf-8").replace(
            "FD-P12-006", "FD-P12-XXX"), encoding="utf-8")
        roots, _, _ = barrier.determine(self.repo)
        self.assertIn(os.path.realpath(self.repo / "docs/architecture/p12"), roots)

    def test_a_bypassed_barrier_is_still_caught_by_detection(self):
        """Remove prevention entirely (an unprotected copy) and write as B-03's
        writers did. Detection does not depend on how the write was made."""
        store = self.repo / "docs/architecture/p12/trace-stores/aios-corpus-health/trace"
        with open(store, "ab") as handle:
            handle.write(b"appended past the barrier\n")
        report = self._verify()
        self.assertFalse(report.holds)
        self.assertIn(str(store.relative_to(self.repo)),
                      report.phases["P12"].modified)


if __name__ == "__main__":
    unittest.main()
