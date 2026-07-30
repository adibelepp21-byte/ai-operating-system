"""
Filesystem facility (Infrastructure spec §2, §5a, §6; Blueprint §14).

A facility *beneath* the entities that resolves locations on the local
filesystem, so that storage facilities (and, later, the substrate
subsystems that use them) have a single, disciplined way to locate where
they may persist. It performs repository-root discovery and safe path
resolution within that root.

Strictly local. It holds NO external dependency (INV-12) — it touches only
the local filesystem through the Python standard library. It owns no
Knowledge, makes no governance decision, and authors no Trace (Infrastructure
spec §8, §9, §10).

Fail Closed (PR-4; Infrastructure spec §11): path resolution that would
escape the discovered root, or that is asked for before provisioning, halts
rather than returning an out-of-bounds or degraded path.
"""

from __future__ import annotations

from pathlib import Path

from .facility import Facility


class RootNotFound(RuntimeError):
    """Raised when a repository root cannot be discovered. Fail closed."""


class PathEscapesRoot(ValueError):
    """Raised when a requested path would resolve outside the facility root."""


def _discover_root(start: Path) -> Path:
    """Walk upward from `start` looking for a repository root marker (`.git`).
    Returns the first ancestor (including `start`) that contains one.

    Discovery is deterministic and local; it consults nothing external.
    """
    start = start.resolve()
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists():
            return candidate
    raise RootNotFound(f"no repository root (.git) found at or above {start}")


class FilesystemFacility(Facility):
    """Resolves paths beneath a single discovered root.

    `root` may be supplied explicitly (e.g. by the bootstrap orchestrator);
    if omitted, it is discovered by walking upward from this module's own
    location to the nearest repository root. The facility never resolves a
    path outside its root.
    """

    name = "filesystem"

    def __init__(self, root: Path | None = None):
        super().__init__()
        self._explicit_root = Path(root) if root is not None else None
        self._root: Path | None = None

    def _provision(self) -> None:
        if self._explicit_root is not None:
            root = self._explicit_root.resolve()
            if not root.is_dir():
                raise RootNotFound(f"supplied root is not a directory: {root}")
            self._root = root
        else:
            self._root = _discover_root(Path(__file__))

    @property
    def root(self) -> Path:
        self.require_ready()
        assert self._root is not None  # guaranteed by provision()
        return self._root

    def resolve(self, *parts: str) -> Path:
        """Resolve a path beneath the root. Fail closed if the result would
        escape the root (no path traversal out of bounds)."""
        self.require_ready()
        assert self._root is not None
        candidate = (self._root.joinpath(*parts)).resolve()
        if candidate != self._root and self._root not in candidate.parents:
            raise PathEscapesRoot(
                f"resolved path {candidate} escapes facility root {self._root}"
            )
        return candidate

    def exists(self, *parts: str) -> bool:
        return self.resolve(*parts).exists()
