"""Refuse any write into certified evidence, whatever API makes it.

Built under `GOAL-V2-004`. `tools/p12_certified_evidence_guard.py` refuses a
write only when the writer asks it first. Its static coverage test sees only
`write_text` and `write_bytes`. `GOAL-V2-003` (`B-03`) found five resident entry
points writing certified evidence past both, through Native Core storage
backends, registries and `open()`. Three of them refused only *after* a first
write had landed.

This module moves the refusal below every write API. It installs a CPython
audit hook (`sys.addaudithook`, PEP 578). The interpreter raises an audit event
before each file operation takes effect: `open` for writing, rename/replace,
remove, rmdir, mkdir, truncate, chmod, utime, link, symlink, the `shutil` copy,
move and rmtree family, and `sqlite3.connect`. It raises one before each process
launch too. When the operation would land in certified evidence, the hook
raises. The operation then never starts:

```text
TARGET CERTIFIED  →  REFUSE (CertifiedWriteRefused)  →  NO WRITE
```

**What is protected** is determined once, at installation, from two sources.
Neither source can reduce what the other protects:

* the guard, which resolves certification from the instruments and the Decision
  Register: certified evidence roots, and the certifying instruments;
* the certified-evidence manifests in `docs/governance/`, which are the
  certification reference, and the evidence roots they record.

Altering the Register or deleting a manifest therefore does not unprotect
anything. If the protected set cannot be determined at all, the barrier fails
closed: it refuses every write inside the repository and leaves only writes
outside it (temporary directories) alone.

**Live state stays writable.** The live operational roots
(`docs/operations/...`) are not certified, and the barrier does not touch them.
The barrier does not freeze a directory. It refuses exactly the paths
certification froze.

**Process launches.** A child process does not inherit an audit hook, so the
barrier governs what it may start:

* Python children must start with the bootstrap on `PYTHONPATH` (see
  `tools/certified_write_barrier_site/`). `install()` puts it there, so an
  inherited environment carries it. Flags that would skip it (`-I`, `-S`, `-E`)
  are refused.
* `git` may run a read-only subcommand against this repository. Any subcommand
  is allowed against another directory, such as a temporary repository or a
  disposable worktree.
* A shell, or any other program, is refused. What it would write cannot be
  known in advance, and an unknown is not safe.

**Installation** happens when the `tools` package is imported
(`tools/__init__.py`). Every resident entry point imports it before it can
write, and a static test holds that to be true. `install()` is idempotent.
There is one hook per process for each repository root.

Stated limits: an audit hook governs Python code in this interpreter. It does
not govern native code that writes by itself (C extensions, `ctypes`), or
`os.open(..., dir_fd=)` with a relative path, because that event does not carry
the `dir_fd`. No resident code uses either; a test holds the second to be true.
The manifests catch whatever passes anyway: they detect a change however it was
made.

Nothing here authorizes anything.
"""

from __future__ import annotations

import json
import os
import re
import sys
import threading
import types
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, List, Optional, Set, Tuple

from tools.p12_certified_evidence_guard import CertifiedEvidenceProtected

REPO_ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_DIR = REPO_ROOT / "tools" / "certified_write_barrier_site"
MANIFEST_GLOB = "AIOS_*CERTIFIED_EVIDENCE_MANIFEST*.json"
ENV_MARKER = "AIOS_CERTIFIED_WRITE_BARRIER"
REFUSAL_PREFIX = "CERTIFIED-WRITE-REFUSED"

# One registry per process, shared by every copy of this module that gets
# imported. Hooks cannot be removed, so installation must never repeat.
_REGISTRY_NAME = "_aios_certified_write_barrier_registry"

_WRITE_FLAGS = (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC
                | os.O_APPEND | getattr(os, "O_TMPFILE", 0))

READ_ONLY_GIT = frozenset({
    "ls-files", "ls-tree", "cat-file", "log", "show", "rev-parse", "diff",
    "status", "grep", "rev-list", "merge-base", "blame", "show-ref",
    "for-each-ref", "describe", "name-rev", "check-ignore", "version",
})
_SHELLS = frozenset({"sh", "bash", "dash", "zsh", "ksh", "csh", "tcsh", "fish"})
_PYTHON = re.compile(r"python[0-9.]*$")


class CertifiedWriteRefused(CertifiedEvidenceProtected, PermissionError):
    """A write, or a process that could write, was refused before it began.

    It is a `PermissionError` too. Code that already handles a denied write
    handles this one, and it does not mistake it for success.
    """


class _State:
    def __init__(self, repo_root: str) -> None:
        self.repo_root = repo_root
        self.roots: Set[str] = set()
        self.files: Set[str] = set()
        self.extra_roots: List[str] = []
        self.fail_closed = False
        self.reason = ""
        self.refusals: List[Tuple[str, str]] = []
        self.local = threading.local()


def _registry() -> types.ModuleType:
    registry = sys.modules.get(_REGISTRY_NAME)
    if registry is None:
        registry = types.ModuleType(_REGISTRY_NAME)
        registry.states = {}
        sys.modules[_REGISTRY_NAME] = registry
    return registry


def _norm(path: str) -> str:
    return os.path.normpath(os.path.abspath(path))


def _forms(path: str) -> Set[str]:
    return {_norm(path), os.path.realpath(path)}


def determine(repo_root: Path = REPO_ROOT) -> Tuple[Set[str], Set[str], str]:
    """The certified roots and files, from the guard and the manifests.

    Raises when neither can be read; `install` turns that into fail-closed.
    """
    from tools import p12_certified_evidence_guard as sentinel
    roots: Set[str] = set()
    files: Set[str] = set()
    sources = []
    register = repo_root / "docs/governance" / sentinel.REGISTER.name
    for root in sentinel.protected_roots(repo_root, register=register):
        roots |= _forms(str(root))
    for instrument in sentinel.protected_instruments(
            repo_root / "docs/governance/acts"):
        files |= _forms(str(instrument))
    sources.append("guard")
    for manifest in sorted((repo_root / "docs/governance").glob(MANIFEST_GLOB)):
        files |= _forms(str(manifest))
        record = json.loads(manifest.read_text(encoding="utf-8"))
        root = record.get("evidence_root")
        if isinstance(root, str) and root:
            roots |= _forms(str(repo_root / root))
    sources.append("manifests")
    return roots, files, "+".join(sources)


def _state(repo_root: Path = REPO_ROOT) -> Optional[_State]:
    return _registry().states.get(os.path.realpath(str(repo_root)))


def installed(repo_root: Path = REPO_ROOT) -> bool:
    return _state(repo_root) is not None


def install(repo_root: Path = REPO_ROOT) -> _State:
    """Install the barrier for `repo_root`, once per process."""
    key = os.path.realpath(str(repo_root))
    registry = _registry()
    if key in registry.states:
        return registry.states[key]
    state = _State(key)
    try:
        state.roots, state.files, state.reason = determine(Path(key))
    except Exception as error:   # undeterminable → refuse all writes in repo
        state.fail_closed = True
        state.roots = _forms(key)
        state.files = set()
        state.reason = f"fail-closed: {type(error).__name__}: {error}"
    _export_bootstrap()
    registry.states[key] = state
    sys.addaudithook(_make_hook(state))
    return state


def _export_bootstrap() -> None:
    """Make inherited environments start Python children barriered."""
    bootstrap = str(BOOTSTRAP_DIR)
    current = os.environ.get("PYTHONPATH", "")
    parts = [p for p in current.split(os.pathsep) if p]
    if bootstrap not in parts:
        os.environ["PYTHONPATH"] = os.pathsep.join([bootstrap] + parts)
    os.environ[ENV_MARKER] = "installed"


def status(repo_root: Path = REPO_ROOT) -> dict:
    state = _state(repo_root)
    if state is None:
        return {"installed": False}
    return {
        "installed": True,
        "fail_closed": state.fail_closed,
        "determined_by": state.reason,
        "protected_roots": sorted(os.path.relpath(r, state.repo_root)
                                  for r in state.roots),
        "protected_files": sorted(os.path.relpath(f, state.repo_root)
                                  for f in state.files),
        "refusals": list(state.refusals),
    }


def refuses(path, repo_root: Path = REPO_ROOT, ancestors: bool = False) -> bool:
    """Whether a write to `path` would be refused. A question; it writes nothing.

    Tests ask this about the real certified tree *before* attempting anything
    there, so a broken barrier fails the test without writing.
    """
    state = install(repo_root)
    target = _resolve(path)
    return target is None or _touches(state, target, ancestors)


@contextmanager
def protecting(path: Path, repo_root: Path = REPO_ROOT) -> Iterator[None]:
    """Protect one more root for the duration, so tests aim at a temp copy.

    Additive only. Nothing can be removed from the set determined at install.
    """
    state = install(repo_root)
    extra = os.path.realpath(str(path))
    state.extra_roots.append(extra)
    try:
        yield
    finally:
        state.extra_roots.remove(extra)


# --------------------------------------------------------------------------
# The hook.
# --------------------------------------------------------------------------

def _fd_path(fd: int) -> Optional[str]:
    try:
        return os.readlink(f"/proc/self/fd/{fd}")
    except (OSError, ValueError):
        return None


def _resolve(path, dir_fd=None) -> Optional[str]:
    """An absolute path for an audited argument, or None if it cannot be had."""
    if isinstance(path, int):
        return _fd_path(path)
    if path is None:
        return None
    try:
        text = os.fsdecode(path)
    except TypeError:
        return None
    if not os.path.isabs(text):
        # CPython audits an absent `dir_fd` as -1. Reading -1 as a descriptor
        # made every relative mkdir/rename/remove/chmod/utime unresolvable and
        # therefore refused, anywhere (found building P13 under P13-018).
        if isinstance(dir_fd, int) and dir_fd >= 0:
            base = _fd_path(dir_fd)
            if base is None:
                return None
            text = os.path.join(base, text)
        else:
            text = os.path.join(os.getcwd(), text)
    return text


def _touches(state: _State, path: str, ancestors: bool = False) -> bool:
    roots = list(state.roots) + state.extra_roots
    for form in _forms(path):
        if form in state.files:
            return True
        for root in roots:
            if form == root or form.startswith(root + os.sep):
                return True
        if ancestors:
            for guarded in roots + list(state.files):
                if guarded.startswith(form + os.sep):
                    return True
    return False


def _refuse(state: _State, event: str, target: str) -> None:
    state.refusals.append((event, target))
    try:
        sys.stderr.write(f"{REFUSAL_PREFIX}: {event} {target}\n")
    except Exception:
        pass
    raise CertifiedWriteRefused(
        f"{event}: {target} is certified evidence, or would reach it, and may "
        "not be written. Certified evidence is historical; persist new "
        "evidence to a live location.")


def _is_write_open(mode, flags) -> bool:
    if isinstance(mode, str) and any(c in mode for c in "wax+"):
        return True
    return isinstance(flags, int) and bool(flags & _WRITE_FLAGS)


def _check(state: _State, event: str, path, dir_fd=None,
           ancestors: bool = False, missing_is_unknown: bool = True) -> None:
    target = _resolve(path, dir_fd)
    if target is None:
        if missing_is_unknown:
            _refuse(state, event, f"<unresolvable {path!r}>")
        return
    if _touches(state, target, ancestors):
        _refuse(state, event, target)


def _git_permitted(state: _State, argv: List[str], cwd: str, env) -> bool:
    workdir = cwd
    work_tree = (env or os.environ).get("GIT_WORK_TREE")
    git_dir = (env or os.environ).get("GIT_DIR")
    i, sub = 1, None
    while i < len(argv):
        arg = argv[i]
        if arg in ("-C", "-c", "--work-tree", "--git-dir") and i + 1 < len(argv):
            value = argv[i + 1]
            if arg == "-C":
                workdir = os.path.join(workdir, value)
            elif arg == "--work-tree":
                work_tree = value
            elif arg == "--git-dir":
                git_dir = value
            i += 2
            continue
        if arg.startswith("--work-tree="):
            work_tree = arg.split("=", 1)[1]
        elif arg.startswith("--git-dir="):
            git_dir = arg.split("=", 1)[1]
        elif not arg.startswith("-"):
            sub = arg
            break
        i += 1
    rest = argv[i + 1:] if sub else []
    if any(a.startswith("--output") for a in rest):
        return False
    if sub in READ_ONLY_GIT:
        return True
    if sub == "worktree":
        return not any(_touches(state, os.path.join(workdir, a), ancestors=True)
                       for a in rest if not a.startswith("-"))
    targets = [workdir]
    if work_tree:
        targets.append(os.path.join(workdir, work_tree))
    if git_dir:
        targets.append(os.path.join(workdir, git_dir))
    repo = state.repo_root
    return not any(
        f == repo or f.startswith(repo + os.sep) for t in targets for f in _forms(t))


def _python_permitted(argv: List[str], env) -> bool:
    i = 1
    while i < len(argv):
        arg = argv[i]
        if arg in ("-c", "-m") or not arg.startswith("-"):
            break
        if arg in ("-X", "-W"):
            i += 2
            continue
        if not arg.startswith("--") and set(arg[1:]) & {"I", "S", "E"}:
            return False
        i += 1
    effective = os.environ if env is None else env
    paths = [p for p in str(effective.get("PYTHONPATH", "")).split(os.pathsep) if p]
    return any(os.path.isfile(os.path.join(p, "sitecustomize.py"))
               and os.path.basename(os.path.normpath(p))
               == BOOTSTRAP_DIR.name for p in paths)


def _launch_permitted(state: _State, executable, args, cwd, env) -> bool:
    if isinstance(args, (str, bytes, os.PathLike)):
        argv = [os.fsdecode(args)]
    else:
        argv = [os.fsdecode(a) for a in (args or [])]
    program = os.fsdecode(executable) if executable else (argv[0] if argv else "")
    name = os.path.basename(program)
    workdir = _norm(os.fsdecode(cwd)) if cwd else os.getcwd()
    if name in _SHELLS:
        return False
    if name == "git":
        return _git_permitted(state, argv, workdir, env)
    if (_PYTHON.match(name) or os.path.realpath(program)
            == os.path.realpath(sys.executable)):
        return _python_permitted(argv, env)
    return False


_FILE_EVENTS = frozenset({
    "open", "os.rename", "os.remove", "os.rmdir", "os.mkdir", "os.truncate",
    "os.chmod", "os.chown", "os.utime", "os.link", "os.symlink",
    "os.setxattr", "os.removexattr", "shutil.copyfile", "shutil.copymode",
    "shutil.copystat", "shutil.copytree", "shutil.move", "shutil.rmtree",
    "shutil.unpack_archive", "shutil.make_archive", "sqlite3.connect",
})
_LAUNCH_EVENTS = frozenset({
    "subprocess.Popen", "os.system", "os.exec", "os.spawn", "os.posix_spawn",
    "os.startfile", "pty.spawn",
})
_EVENTS = _FILE_EVENTS | _LAUNCH_EVENTS


def _make_hook(state: _State):
    def hook(event: str, args: tuple) -> None:
        if event not in _EVENTS:
            return
        local = state.local
        if getattr(local, "busy", False):
            return
        local.busy = True
        try:
            _dispatch(state, event, args)
        finally:
            local.busy = False
    return hook


def _dispatch(state: _State, event: str, args: tuple) -> None:
    if event == "open":
        path, mode, flags = args[0], args[1], args[2]
        if isinstance(path, int) or not _is_write_open(mode, flags):
            return
        _check(state, event, path)
    elif event in ("os.rename", "os.link"):
        _check(state, event, args[0], args[2], ancestors=True)
        _check(state, event, args[1], args[3], ancestors=True)
    elif event in ("os.remove", "os.rmdir"):
        _check(state, event, args[0], args[1], ancestors=True)
    elif event == "os.mkdir":
        target = _resolve(args[0], args[2])
        if target is not None and os.path.lexists(target):
            return      # it will fail with FileExistsError and write nothing
        _check(state, event, args[0], args[2])
    elif event == "os.truncate":
        _check(state, event, args[0])
    elif event in ("os.chmod", "os.chown", "os.utime"):
        _check(state, event, args[0], args[-1])
    elif event == "os.symlink":
        _check(state, event, args[1], args[2])
    elif event in ("os.setxattr", "os.removexattr"):
        _check(state, event, args[0])
    elif event in ("shutil.copyfile", "shutil.copymode", "shutil.copystat",
                   "shutil.copytree"):
        _check(state, event, args[1])
    elif event == "shutil.move":
        _check(state, event, args[0], ancestors=True)
        _check(state, event, args[1], ancestors=True)
    elif event == "shutil.rmtree":
        _check(state, event, args[0], args[1] if len(args) > 1 else None,
               ancestors=True)
    elif event == "shutil.unpack_archive":
        _check(state, event, args[1])
    elif event == "shutil.make_archive":
        _check(state, event, args[0])
    elif event == "sqlite3.connect":
        database = args[0]
        if isinstance(database, (str, bytes, os.PathLike)) \
                and os.fsdecode(database) != ":memory:":
            _check(state, event, database)
    elif event == "subprocess.Popen":
        executable, argv, cwd, env = args[0], args[1], args[2], args[3]
        if not _launch_permitted(state, executable, argv, cwd, env):
            _refuse(state, event, repr(argv))
    elif event in ("os.exec", "os.posix_spawn"):
        if not _launch_permitted(state, args[0], args[1], None, args[2]):
            _refuse(state, event, repr(args[1]))
    elif event == "os.spawn":
        if not _launch_permitted(state, args[1], args[2], None, args[3]):
            _refuse(state, event, repr(args[2]))
    else:   # os.system, os.startfile, pty.spawn: a shell or unknown program
        _refuse(state, event, repr(args))


def main() -> int:
    install()
    print(json.dumps(status(), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
