"""Run every resident entry point where it cannot hurt, and see what it writes.

Built under `GOAL-V2-004`. A static reading of the code tells you which write
calls exist. It does not tell you which of them an entry point actually reaches,
through which API, or whether a refusal comes before the first byte or after
it. This probe answers that by observation. It never runs in the authoritative
checkout:

```text
git worktree add --detach <scratch>/wt <commit>      disposable copy of <commit>
for each entry point, in each form it can be run:
    reset the copy to <commit>                        every run starts clean
    run it (stdin closed, bounded time)
    git status --porcelain --ignored                  what changed, and where
classify:  WRITES-CERTIFIED · GUARDED · SAFE · NON-WRITING · UNKNOWN
git worktree remove                                   nothing is left behind
```

Children get an explicit environment. When the write barrier is present in the
copy, `PYTHONPATH` names *the copy's* bootstrap, so a child protects the copy's
certified roots and imports the copy's code. It never picks up the code of the
checkout that launched the probe.

**Discovery is by content, not by a list.** An entry point is any tracked `.py`
file that carries a `__main__` guard, plus every `__main__.py`. Tests are the
exception, because a test runner executes them as a suite. They are run by
`suite` instead: one discovery run per suite root.

`--mutations` breaks each protection inside a disposable worktree instead: it
removes the barrier, aims a live writer at a certified root, changes, deletes,
adds or makes unreadable certified files, and alters the certification
reference. It reports what caught each one. Every write it makes passes the
guard. The guard refuses the authoritative tree and admits only the copy.

Run from a barriered process, the probe is barriered too, and it can then
launch children only in a copy that carries the barrier's bootstrap. A copy
without one (a commit from before `GOAL-V2-004`) must be probed from an
unbarriered shell. That is the probe failing closed.

Nothing here authorizes anything. The authoritative tree is only read, and the
report goes to stdout: the probe writes no file of its own.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from tools.p12_certified_evidence_guard import guard

REPO_ROOT = Path(__file__).resolve().parents[1]

WRITES_CERTIFIED = "WRITES-CERTIFIED"
GUARDED = "GUARDED"
SAFE = "SAFE"
NON_WRITING = "NON-WRITING"
RETIRED = "RETIRED/HISTORICAL"
UNKNOWN = "UNKNOWN"

HISTORY_PREFIX = "docs/architecture/history/"
BOOTSTRAP_DIR = "tools/certified_write_barrier_site"
# The probe is itself an entry point, so it finds and runs itself. Unchecked,
# every run starts another full probe, recursively. Children carry this marker,
# and a probe started with it refuses to run.
NESTED_MARKER = "AIOS_CERTIFIED_WRITE_PROBE_CHILD"
REFUSAL_MARKERS = ("CertifiedWriteRefused", "CertifiedEvidenceProtected",
                   "CERTIFIED-WRITE-REFUSED")
_PREFIXES = (
    "import json, sys; from pathlib import Path; sys.path.insert(0, '.');"
    "from tools import p12_certified_evidence_guard as s;"
    "r = Path('.').resolve();"
    "print(json.dumps(sorted("
    "[p.resolve().relative_to(r).as_posix() + '/' for p in s.protected_roots()]"
    " + [p.resolve().relative_to(r).as_posix() for p in s.protected_instruments()])))"
)
_MAIN_GUARD = re.compile(r"""__name__\s*==\s*['"]__main__['"]""")

# Invocations that aim a writer's own output argument at certified evidence.
# One per phase, and one each for an addition and a modification. They are the
# negative control "a live writer targeted at a certified root".
TARGETED: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    ("tools/validate_execution_catalog.py",
     ("--graph-out", "docs/architecture/platform-organization/README.md")),
    ("tools/validate_execution_catalog.py",
     ("--graph-out", "docs/architecture/p11/probe-graph.json")),
    ("tools.governance_index",
     ("--index", "docs/architecture/p12/probe-index.json", "build")),
    ("p12_w4_integrated_execution.py", ("probe",)),
    # P13-018: a real P13 cycle, which must write only docs/operations/p13.
    ("tools.p13.cycle", ("--invoker", "certified_write_probe",
                         "--intent", "probe: a cycle writes only its live root")),
)

SUITES: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    ("tools", ("-s", "tools/tests", "-t", ".")),
    ("native_core", ("-s", "native_core", "-t", ".")),
    ("consumers", ("-s", "consumers", "-t", ".")),
    ("bounded_exception", ("-s", "tools/bounded_exception/tests", "-t", ".")),
)


@dataclass
class Run:
    entry: str
    form: str
    argv: List[str]
    returncode: Optional[int]
    timed_out: bool
    refusals: int
    certified_changes: List[str] = field(default_factory=list)
    other_changes: List[str] = field(default_factory=list)
    classification: str = UNKNOWN
    tail: str = ""


def _git(*args: str, cwd: Path = REPO_ROOT, check: bool = True) -> str:
    return subprocess.run(("git",) + args, cwd=str(cwd), capture_output=True,
                          text=True, check=check).stdout


def certified_prefixes(root: Path = REPO_ROOT) -> Tuple[str, ...]:
    """What counts as certified, as the copy itself determines it.

    The guard decides from the Decision Register; the manifest index adds the
    roots it records. The instruments and the manifests themselves are
    included. A write to any of these is a certified write.
    """
    # Asked in a child, so the answer comes from the copy's own guard. This
    # process may already hold another checkout's `tools` package.
    asked = subprocess.run(
        [sys.executable, "-c", _PREFIXES], cwd=str(root), env=_environment(root),
        capture_output=True, text=True, check=True)
    prefixes = set(json.loads(asked.stdout))
    for manifest in sorted((root / "docs/governance").glob(
            "AIOS_*CERTIFIED_EVIDENCE_MANIFEST*.json")):
        prefixes.add(manifest.relative_to(root).as_posix())
        try:
            record = json.loads(manifest.read_text(encoding="utf-8"))
        except ValueError:
            continue
        if isinstance(record.get("evidence_root"), str):
            prefixes.add(record["evidence_root"].rstrip("/") + "/")
    return tuple(sorted(prefixes))


def is_certified(relative: str, prefixes: Sequence[str]) -> bool:
    return any(relative == p or (p.endswith("/") and relative.startswith(p))
               for p in prefixes)


def discover(root: Path) -> Dict[str, List[str]]:
    """Every entry point in the copy, grouped by how it is run."""
    found: Dict[str, List[str]] = {"root": [], "tools": [], "package": [],
                                   "history": [], "other": []}
    for name in _git("ls-files", "*.py", cwd=root).split("\n"):
        if not name or "/tests/" in name or name.startswith("tests/"):
            continue
        path = root / name
        text = path.read_text(encoding="utf-8", errors="replace")
        if path.name != "__main__.py" and not _MAIN_GUARD.search(text):
            continue
        if name.startswith(HISTORY_PREFIX):
            found["history"].append(name)
        elif path.name == "__main__.py":
            found["package"].append(name)
        elif "/" not in name:
            found["root"].append(name)
        elif name.startswith("tools/"):
            found["tools"].append(name)
        else:
            found["other"].append(name)
    return {k: sorted(v) for k, v in found.items()}


def _environment(root: Path) -> Dict[str, str]:
    env = {k: v for k, v in os.environ.items()
           if k not in ("PYTHONPATH", "GIT_DIR", "GIT_WORK_TREE",
                        "GIT_INDEX_FILE", "AIOS_CERTIFIED_WRITE_BARRIER")}
    bootstrap = root / BOOTSTRAP_DIR
    if bootstrap.is_dir():
        env["PYTHONPATH"] = str(bootstrap)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env[NESTED_MARKER] = "1"
    return env


def _changes(root: Path) -> List[str]:
    out = _git("status", "--porcelain=v1", "-z", "--untracked-files=all",
               "--ignored=matching", cwd=root)
    entries = [e for e in out.split("\0") if e]
    changed = []
    skip_next = False
    for entry in entries:
        if skip_next:           # the source half of a rename record
            skip_next = False
            continue
        status, name = entry[:2], entry[3:]
        if status[0] in "RC":
            skip_next = True
        if "__pycache__" in name.split("/"):
            continue
        changed.append(f"{status.strip() or '?'} {name}")
    return changed


def _reset(root: Path, commit: str) -> None:
    _git("reset", "--hard", "-q", commit, cwd=root)
    _git("clean", "-fdxq", cwd=root)


def classify(run: Run, entry: str) -> str:
    if run.certified_changes:
        return WRITES_CERTIFIED
    if run.timed_out:
        return UNKNOWN
    if entry.startswith(HISTORY_PREFIX):
        return RETIRED
    if run.refusals:
        return GUARDED
    if run.other_changes:
        return SAFE
    return NON_WRITING


def run_one(root: Path, commit: str, entry: str, form: str,
            argv: Sequence[str], prefixes: Sequence[str],
            timeout: int) -> Run:
    _reset(root, commit)
    timed_out, code, tail, refusals = False, None, "", 0
    try:
        done = subprocess.run(list(argv), cwd=str(root), env=_environment(root),
                              stdin=subprocess.DEVNULL, capture_output=True,
                              text=True, timeout=timeout)
        code = done.returncode
        text = done.stdout + "\n" + done.stderr
        refusals = sum(text.count(m) for m in REFUSAL_MARKERS)
        tail = "\n".join(done.stderr.strip().splitlines()[-2:])[-300:]
    except subprocess.TimeoutExpired:
        timed_out = True
    changes = _changes(root)
    certified = [c for c in changes if is_certified(c.split(" ", 1)[1], prefixes)]
    other = [c for c in changes if c not in certified]
    result = Run(entry, form, list(argv[1:]), code, timed_out, refusals,
                 certified, other, UNKNOWN, tail)
    result.classification = classify(result, entry)
    return result


def invocations(found: Dict[str, List[str]]) -> List[Tuple[str, str, List[str]]]:
    py = sys.executable
    plan: List[Tuple[str, str, List[str]]] = []
    for name in found["root"] + found["history"] + found["other"]:
        plan.append((name, "path", [py, name]))
    for name in found["tools"]:
        module = name[:-3].replace("/", ".")
        plan.append((name, "module", [py, "-m", module]))
        plan.append((name, "path", [py, name]))
    for name in found["package"]:
        module = name[:-len("/__main__.py")].replace("/", ".")
        plan.append((name, "module", [py, "-m", module]))
    for target, args in TARGETED:
        if target.endswith(".py"):
            plan.append((target, "targeted", [py, target, *args]))
        else:
            plan.append((target.replace(".", "/") + ".py", "targeted",
                         [py, "-m", target, *args]))
    for suite, args in SUITES:
        plan.append((f"suite:{suite}", "suite",
                     [py, "-m", "unittest", "discover", *args, "-q"]))
    return plan


def probe(commit: str = "HEAD", repo_root: Path = REPO_ROOT, timeout: int = 2400,
          only: Optional[Sequence[str]] = None, jobs: int = 1) -> dict:
    """Probe every entry point of `commit`, in `jobs` disposable worktrees."""
    import queue
    import threading

    commit = _git("rev-parse", commit, cwd=repo_root).strip()
    parent = Path(tempfile.mkdtemp(prefix="aios-write-probe-"))
    trees = [parent / f"wt{i}" for i in range(max(1, jobs))]
    for tree in trees:
        _git("worktree", "add", "--detach", "-q", str(tree), commit, cwd=repo_root)
    try:
        prefixes = certified_prefixes(trees[0])
        found = discover(trees[0])
        plan = [p for p in invocations(found)
                if not only or any(o in p[0] for o in only)]
        work: "queue.Queue" = queue.Queue()
        for position, item in enumerate(plan):
            work.put((position, item))
        results: Dict[int, Run] = {}

        def worker(tree: Path) -> None:
            while True:
                try:
                    position, (entry, form, argv) = work.get_nowait()
                except queue.Empty:
                    return
                results[position] = run_one(tree, commit, entry, form, argv,
                                            prefixes, timeout)

        threads = [threading.Thread(target=worker, args=(t,)) for t in trees]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        runs = [results[i] for i in sorted(results)]
        for tree in trees:
            _reset(tree, commit)
    finally:
        for tree in trees:
            _git("worktree", "remove", "--force", str(tree), cwd=repo_root,
                 check=False)
        _git("worktree", "prune", cwd=repo_root, check=False)
        shutil.rmtree(parent, ignore_errors=True)
    counts: Dict[str, int] = {}
    for r in runs:
        counts[r.classification] = counts.get(r.classification, 0) + 1
    return {
        "commit": commit,
        "certified_prefixes": list(prefixes),
        "entry_points": {k: len(v) for k, v in found.items()},
        "runs": [asdict(r) for r in runs],
        "classification_counts": counts,
        "certified_writes": sum(len(r.certified_changes) for r in runs),
        "holds": all(r.classification not in (WRITES_CERTIFIED, UNKNOWN)
                     for r in runs),
    }


_INTEGRITY = [sys.executable, "-m", "tools.certified_evidence_integrity"]
_REFUSES = [sys.executable, "-c",
            "from tools import certified_write_barrier as b;"
            "print(b.refuses('docs/architecture/p12/x.json'))"]


def _run(tree: Path, argv: Sequence[str], env: Optional[Dict[str, str]] = None,
         timeout: int = 600) -> Tuple[int, str]:
    done = subprocess.run(list(argv), cwd=str(tree),
                          env=env if env is not None else _environment(tree),
                          stdin=subprocess.DEVNULL, capture_output=True, text=True,
                          timeout=timeout)
    return done.returncode, done.stdout + done.stderr


def _integrity(tree: Path) -> dict:
    code, out = _run(tree, _INTEGRITY)
    try:
        report = json.loads(out[:out.rindex("}") + 1])
    except ValueError:
        return {"holds": None, "returncode": code, "raw": out[-300:]}
    findings = {phase: {k: v for k, v in result.items()
                        if k in ("MODIFIED", "MISSING", "UNREADABLE", "UNEXPECTED",
                                 "reference_faults") and v}
                for phase, result in report["phases"].items()}
    return {"holds": report["holds"], "returncode": code,
            "faults": report["faults"],
            "findings": {k: v for k, v in findings.items() if v}}


def _edit(path: Path, transform) -> None:
    """Every mutation write passes the guard. The copy's certified roots are not
    the authoritative tree's, so a copy passes and the real tree is refused."""
    guard(path).write_text(transform(path.read_text(encoding="utf-8")), encoding="utf-8")


def mutation_controls(commit: str = "HEAD", repo_root: Path = REPO_ROOT) -> dict:
    """Break each protection in a disposable worktree, and watch it be caught.

    Every mutation lands in a copy. The authoritative tree is only read, and
    its integrity is checked before and after so the report can show that.
    """
    commit = _git("rev-parse", commit, cwd=repo_root).strip()
    parent = Path(tempfile.mkdtemp(prefix="aios-mutation-"))
    tree = parent / "wt"
    _git("worktree", "add", "--detach", "-q", str(tree), commit, cwd=repo_root)
    controls = []
    authoritative_before = _integrity(repo_root)
    try:
        # M1 — remove the barrier entirely, and run a B-03 writer through it.
        _reset(tree, commit)
        # Both installation routes are removed: the package import, and the
        # bootstrap children start with. The bootstrap file stays in place,
        # empty, so the launch itself is still permitted.
        guard(tree / "tools/__init__.py").write_text('"""barrier removed"""\n',
                                                encoding="utf-8")
        guard(tree / BOOTSTRAP_DIR / "sitecustomize.py").write_text(
            '"""bootstrap removed"""\n', encoding="utf-8")
        code, out = _run(tree, [sys.executable, "w4_first_execution.py"])
        wrote = [c for c in _changes(tree) if " docs/architecture/" in c]
        controls.append({
            "control": "M1 remove / bypass write barrier",
            "mutation": "neither tools/__init__.py nor the bootstrap installs it",
            "certified_writes_in_copy": wrote,
            "detection": _integrity(tree),
        })

        # M2 — a live writer aimed at a certified root, barrier intact.
        _reset(tree, commit)
        code, out = _run(tree, [sys.executable, "tools/validate_execution_catalog.py",
                                "--graph-out",
                                "docs/architecture/p12/probe-graph.json"])
        controls.append({
            "control": "M2 target a live writer at a certified root",
            "refused": any(m in out for m in REFUSAL_MARKERS),
            "certified_writes_in_copy": [c for c in _changes(tree)
                                         if " docs/architecture/" in c],
        })

        # M3 — change, add, delete and make unreadable certified files.
        _reset(tree, commit)
        index = json.loads((tree / "docs/governance/"
                            "AIOS_CERTIFIED_EVIDENCE_MANIFEST_INDEX_v1.0.json"
                            ).read_text(encoding="utf-8"))
        firsts = {}
        for phase, entry in index["phases"].items():
            record = json.loads((tree / entry["manifest"]).read_text(encoding="utf-8"))
            firsts[phase] = sorted(record["files"])
        guard(tree / firsts["P10"][0]).write_text("changed\n", encoding="utf-8")
        (tree / firsts["P11"][0]).unlink()
        guard(tree / "docs/architecture/p12/added.json").write_text("{}", encoding="utf-8")
        (tree / firsts["P12"][0]).unlink()
        (tree / firsts["P12"][0]).mkdir()
        controls.append({
            "control": "M3 change / delete / add / unreadable",
            "mutation": {"MODIFIED": firsts["P10"][0], "MISSING": firsts["P11"][0],
                         "UNEXPECTED": "docs/architecture/p12/added.json",
                         "UNREADABLE": firsts["P12"][0]},
            "detection": _integrity(tree),
        })

        # M4 — alter the certification reference three ways.
        results = {}
        _reset(tree, commit)
        register = tree / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
        _edit(register, lambda t: t.replace("FD-P12-006", "FD-P12-XXX"))
        results["register strikes FD-P12-006"] = {
            "detection": _integrity(tree),
            "barrier_still_protects_p12": _run(tree, _REFUSES)[1].strip()}
        _reset(tree, commit)
        manifest = tree / index["phases"]["P11"]["manifest"]
        record = json.loads(manifest.read_text(encoding="utf-8"))
        record["files"][sorted(record["files"])[0]] = "0" * 64
        guard(manifest).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        results["P11 manifest hash altered"] = {"detection": _integrity(tree)}
        _reset(tree, commit)
        _edit(tree / index["phases"]["P10"]["certifying_instrument"],
              lambda t: t + "\n")
        results["FD-P10-005 altered"] = {"detection": _integrity(tree)}
        controls.append({"control": "M4 alter the certification reference",
                         "results": results})
        _reset(tree, commit)
    finally:
        _git("worktree", "remove", "--force", str(tree), cwd=repo_root, check=False)
        _git("worktree", "prune", cwd=repo_root, check=False)
        shutil.rmtree(parent, ignore_errors=True)
    return {"commit": commit, "controls": controls,
            "authoritative_before": authoritative_before,
            "authoritative_after": _integrity(repo_root)}


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Print the report on stdout. The probe itself writes no file."""
    if os.environ.get(NESTED_MARKER):
        print("refused: a probe does not run inside a probe", file=sys.stderr)
        return 3
    args = list(sys.argv[1:] if argv is None else argv)
    commit = "HEAD"
    only: List[str] = []
    jobs = 1
    while args:
        arg = args.pop(0)
        if arg == "--commit" and args:
            commit = args.pop(0)
        elif arg == "--only" and args:
            only.append(args.pop(0))
        elif arg == "--jobs" and args:
            jobs = int(args.pop(0))
        elif arg == "--mutations":
            print(json.dumps(mutation_controls(commit), indent=2))
            return 0
        else:
            print(f"unknown argument {arg}", file=sys.stderr)
            return 2
    report = probe(commit, only=only or None, jobs=jobs)
    print(json.dumps(report, indent=2))
    print(json.dumps({"classification_counts": report["classification_counts"],
                      "certified_writes": report["certified_writes"],
                      "holds": report["holds"]}), file=sys.stderr)
    return 0 if report["holds"] else 1


if __name__ == "__main__":
    # GOAL-V2-004: install the certified-write barrier before anything runs,
    # even when this file is run by path and has not imported `tools`.
    import os, sys  # noqa: E401
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import tools  # noqa: E402,F401
    raise SystemExit(main())
