"""`docs.read` — the one Tool the application registers (FS-01 `§5`).

A Tool is the only place external access may live (INV-12), and reading a file
is external access. So a Workflow that reads a document does it the lawful way:
an Agent proposes, `ToolInvocationGovernance` decides, and only then does this
Tool run.

It reads and nothing else. It is confined to one directory (the repository's
`docs/`), accepts only regular `.md` and `.txt` files up to `MAX_BYTES`, and
refuses traversal, absolute paths, symlinks out of the root and hidden
segments. Every refusal is a `Failure` with a reason, so governance records an
execution failure rather than a silent empty read.
"""

from __future__ import annotations

import hashlib
from pathlib import Path, PurePosixPath

from native_core.core.infrastructure import ExternalTool, ToolContract, ToolIdentity
from native_core.shared import Failure, Success

KEY = "docs.read"
VERSION = "1"
ACTION = "read"
IDENTITY = ToolIdentity(canonical_key=KEY, version=VERSION)
CONTRACT = ToolContract(actions=(ACTION,), required_parameters={ACTION: ("path",)})
METADATA = {"effect": "read-only", "confined_to": "docs/",
            "suffixes": (".md", ".txt")}
MAX_BYTES = 2 * 1024 * 1024
SUFFIXES = (".md", ".txt")


class DocsReadTool(ExternalTool):
    """Reads one document beneath `root`/docs, returning its lines and hash."""

    def __init__(self, root: Path):
        self._root = Path(root).resolve()
        self._docs = (self._root / "docs").resolve()

    @property
    def canonical_key(self) -> str:
        return KEY

    def invoke(self, action: str, parameters: dict):
        if action != ACTION:
            return Failure(reason=f"{KEY} has no action {action!r}")
        path = parameters.get("path")
        problem = self._invalid(path)
        if problem:
            return Failure(reason=problem)
        target = (self._root / path).resolve()
        if self._docs not in target.parents:
            return Failure(reason=f"{path!r} resolves outside docs/")
        if not target.is_file():
            return Failure(reason=f"{path!r} is not a document in the repository")
        size = target.stat().st_size
        if size > MAX_BYTES:
            return Failure(reason=f"{path!r} is {size} bytes; the limit is {MAX_BYTES}")
        data = target.read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            return Failure(reason=f"{path!r} is not UTF-8 text")
        return Success(value={"path": path, "bytes": size,
                              "sha256": hashlib.sha256(data).hexdigest(),
                              "lines": tuple(text.splitlines())})

    @staticmethod
    def _invalid(path) -> str:
        if not isinstance(path, str) or not path.strip():
            return "path must be a non-empty string"
        if "\\" in path or "\x00" in path:
            return "path contains a forbidden character"
        pure = PurePosixPath(path)
        if pure.is_absolute():
            return "path must be relative to the repository root"
        if pure.parts[:1] != ("docs",):
            return "path must lie under docs/"
        if any(part in ("..", ".") or part.startswith(".") for part in pure.parts):
            return "path may not contain '.', '..' or hidden segments"
        if pure.suffix not in SUFFIXES:
            return f"only {', '.join(SUFFIXES)} documents can be read"
        return ""
