"""
Exception-site identity and discovery.

Identity is the four-tuple

    (relative module path, enclosing qualified name, exception class name,
     ordinal within enclosing scope)

Line number is retained as navigational metadata and is deliberately NOT
part of identity: line numbers churn on any edit above a site, which
would make the register unusable. The ordinal changes only when sites are
added, removed, or reordered inside the same scope — which is exactly
when re-authorization is appropriate (P7-I52 §7).

Detection is AST-based. Traversal is deterministic: `ast.NodeVisitor`
walks child fields in source order, so ordinals are assigned in source
order and the same tree always yields the same identities.
"""

import ast
from dataclasses import dataclass
from pathlib import Path

MODULE_SCOPE = "<module>"


@dataclass(frozen=True)
class SiteIdentity:
    """The identifying tuple. Two sites are the same site iff these are equal."""

    path: str
    qualname: str
    exception: str
    ordinal: int

    def as_tuple(self):
        return (self.path, self.qualname, self.exception, self.ordinal)


@dataclass(frozen=True)
class Site:
    """A discovered exception site: its identity plus navigational metadata."""

    identity: SiteIdentity
    line: int


def _callee_name(func):
    """Return the called name for `raise Name(...)` or `raise mod.Name(...)`."""
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return func.attr
    return None


def container_arg_raise(node):
    """Detector: `raise X(<container literal>, ...)`.

    Returns the exception class name when a raise passes a list, tuple,
    dict, or set literal as a positional argument — a halt whose message
    renders as a structured object rather than as text. Returns None
    otherwise.
    """
    exc = node.exc
    if not isinstance(exc, ast.Call):
        return None
    name = _callee_name(exc.func)
    if name is None:
        return None
    for arg in exc.args:
        if isinstance(arg, (ast.List, ast.Tuple, ast.Dict, ast.Set)):
            return name
    return None


DETECTORS = {
    "container_arg_raise": container_arg_raise,
}


class _SiteCollector(ast.NodeVisitor):
    """Walks one module, tracking enclosing scope and per-scope ordinals."""

    def __init__(self, detector, path):
        self._detector = detector
        self._path = path
        self._stack = []
        self._counts = {}
        self.sites = []

    def _scope(self):
        return ".".join(self._stack) if self._stack else MODULE_SCOPE

    def _visit_scope(self, node):
        self._stack.append(node.name)
        self.generic_visit(node)
        self._stack.pop()

    visit_FunctionDef = _visit_scope
    visit_AsyncFunctionDef = _visit_scope
    visit_ClassDef = _visit_scope

    def visit_Raise(self, node):
        exception = self._detector(node)
        if exception is not None:
            scope = self._scope()
            ordinal = self._counts.get(scope, 0)
            self._counts[scope] = ordinal + 1
            self.sites.append(
                Site(
                    identity=SiteIdentity(
                        path=self._path,
                        qualname=scope,
                        exception=exception,
                        ordinal=ordinal,
                    ),
                    line=node.lineno,
                )
            )
        self.generic_visit(node)


def discover_sites(root, detector_name, repo_root):
    """Discover every exception site under `root`, deterministically ordered.

    `root` and `repo_root` are Paths. Paths in identities are recorded
    relative to `repo_root` with forward slashes, so identities do not
    depend on where the repository is checked out.
    """
    detector = DETECTORS.get(detector_name)
    if detector is None:
        raise KeyError(f"unknown detector: {detector_name}")

    root = Path(root)
    repo_root = Path(repo_root)
    found = []
    for source in sorted(root.rglob("*.py")):
        if "__pycache__" in source.parts:
            continue
        relative = source.resolve().relative_to(repo_root.resolve()).as_posix()
        tree = ast.parse(source.read_text(encoding="utf-8"))
        collector = _SiteCollector(detector, relative)
        collector.visit(tree)
        found.extend(collector.sites)
    return tuple(found)
