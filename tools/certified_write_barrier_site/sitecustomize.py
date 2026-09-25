"""Start every Python child of a barriered process barriered too.

`GOAL-V2-004`. An audit hook lives in one interpreter and a child process does
not inherit it. `tools.certified_write_barrier.install()` puts this directory
first on `PYTHONPATH`, and the barrier refuses to launch a Python child without
it. The child imports this file at startup, before any of its own code runs,
and installs the barrier for the repository this file belongs to.

If installation fails, the child is not left unprotected. A minimal hook takes
over, and it refuses every write inside the repository.

Afterwards, whatever `sitecustomize` the interpreter would otherwise have loaded
still runs. This file adds a barrier; it does not replace site configuration.
"""

import importlib.machinery
import importlib.util
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))


def _fallback() -> None:
    root = os.path.realpath(_ROOT)

    def refuse_inside_repo(event, args):
        if event != "open" or isinstance(args[0], int):
            if event not in ("os.rename", "os.remove", "os.rmdir", "os.mkdir",
                             "os.truncate", "shutil.rmtree", "shutil.move",
                             "shutil.copyfile", "subprocess.Popen", "os.system"):
                return
        elif not ((isinstance(args[1], str) and any(c in args[1] for c in "wax+"))
                  or (isinstance(args[2], int) and args[2] & (
                      os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))):
            return
        raise PermissionError(
            f"CERTIFIED-WRITE-REFUSED: {event}: the certified-write barrier "
            f"could not be installed, so writes inside {root} are refused")

    sys.addaudithook(refuse_inside_repo)


def _install() -> None:
    inserted = _ROOT not in sys.path
    if inserted:
        sys.path.insert(0, _ROOT)
    try:
        from tools import certified_write_barrier
        if not certified_write_barrier.installed():
            certified_write_barrier.install()
    except BaseException:
        _fallback()
    finally:
        if inserted and _ROOT in sys.path:
            sys.path.remove(_ROOT)


def _chain() -> None:
    """Run the `sitecustomize` this one shadows, if there is one."""
    here = os.path.realpath(_HERE)
    path = [p for p in sys.path if os.path.realpath(p or ".") != here]
    spec = importlib.machinery.PathFinder.find_spec("sitecustomize", path)
    if spec is None or spec.loader is None:
        return
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)


_install()
_chain()
