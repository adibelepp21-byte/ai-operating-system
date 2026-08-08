"""
The fail-closed verifier (D-3).

Read-only by construction: this module imports nothing that writes, and
offers no serializer, no `--update`, no `--fix`, no `--accept`, and no
auto-registration. The `code -> verifier -> register` loop cannot close,
because the verifier has no path to the register except reading it.

Failure taxonomy — six of the seven cases fail; only one passes:

    UNREGISTERED_SITE        a site in declared scope is not registered
    ABSENT_REGISTERED_SITE   a registered site no longer exists
    DUPLICATE_IDENTITY       one identity registered more than once
    MALFORMED_REGISTER       the register cannot be parsed or validated
    UNAUTHORIZED_EXPANSION   an entry lies outside every declared scope
    UNRESOLVED_PROVENANCE    a finding, decision, or act does not resolve

The single passing case is: a registered identity exists, lies inside a
declared scope, and has fully resolvable provenance.

`UNAUTHORIZED_EXPANSION` is what makes the bound real. An entry whose
path is not inside any declared `scan_scope` root can never be checked
against reality, so it could tolerate anything. Rather than ignore such
an entry, the verifier fails on it.
"""

from dataclasses import dataclass
from pathlib import Path

from .identity import discover_sites
from .provenance import authorizing_act_is_well_formed
from .register import RegisterError, load_register

UNREGISTERED_SITE = "UNREGISTERED_SITE"
ABSENT_REGISTERED_SITE = "ABSENT_REGISTERED_SITE"
DUPLICATE_IDENTITY = "DUPLICATE_IDENTITY"
MALFORMED_REGISTER = "MALFORMED_REGISTER"
UNAUTHORIZED_EXPANSION = "UNAUTHORIZED_EXPANSION"
UNRESOLVED_PROVENANCE = "UNRESOLVED_PROVENANCE"


@dataclass(frozen=True)
class Failure:
    kind: str
    detail: str

    def __str__(self):
        return f"{self.kind}: {self.detail}"


def _identity_str(identity):
    return "{}::{}::{}#{}".format(*identity.as_tuple())


def _within(path, root):
    """True when a repo-relative path lies inside a repo-relative root."""
    if root in ("", "."):
        return True
    return path == root or path.startswith(root.rstrip("/") + "/")


def verify(register_path, repo_root, provenance):
    """Verify a register against the tree. Returns a tuple of Failures.

    An empty tuple means the register is valid and exactly bounds what
    exists. Any non-empty result is a failure — there is no warning
    level, and ambiguity always resolves to failure.
    """
    try:
        register = load_register(register_path)
    except (RegisterError, OSError) as exc:
        return (Failure(MALFORMED_REGISTER, str(exc)),)

    repo_root = Path(repo_root)
    failures = []

    # Duplicate identities.
    seen = {}
    for entry in register.entries:
        key = entry.identity.as_tuple()
        seen[key] = seen.get(key, 0) + 1
    for key, count in sorted(seen.items()):
        if count > 1:
            failures.append(
                Failure(
                    DUPLICATE_IDENTITY,
                    "{} registered {} times".format("::".join(str(p) for p in key), count),
                )
            )

    # Provenance.
    for entry in sorted(register.entries, key=lambda e: e.identity.as_tuple()):
        ident = _identity_str(entry.identity)
        if not provenance.finding_exists(entry.finding_id):
            failures.append(
                Failure(
                    UNRESOLVED_PROVENANCE,
                    f"{ident}: finding {entry.finding_id!r} does not resolve",
                )
            )
        if not provenance.decision_exists(entry.governance_decision_id):
            failures.append(
                Failure(
                    UNRESOLVED_PROVENANCE,
                    f"{ident}: governance decision "
                    f"{entry.governance_decision_id!r} does not resolve",
                )
            )
        if not authorizing_act_is_well_formed(entry.authorizing_act):
            failures.append(
                Failure(
                    UNRESOLVED_PROVENANCE,
                    f"{ident}: authorizing act {entry.authorizing_act!r} "
                    "does not name a directive",
                )
            )

    # Entries outside every declared scope can never be checked.
    roots = tuple(scope.root for scope in register.scan_scope)
    for entry in sorted(register.entries, key=lambda e: e.identity.as_tuple()):
        if not any(_within(entry.identity.path, root) for root in roots):
            failures.append(
                Failure(
                    UNAUTHORIZED_EXPANSION,
                    f"{_identity_str(entry.identity)} lies outside every declared scan scope",
                )
            )

    # Both directions of drift, per declared scope.
    registered = {entry.identity.as_tuple() for entry in register.entries}
    for scope in register.scan_scope:
        root = repo_root / scope.root
        if not root.is_dir():
            failures.append(
                Failure(
                    MALFORMED_REGISTER,
                    f"scan scope root {scope.root!r} is not a directory",
                )
            )
            continue
        try:
            discovered = discover_sites(root, scope.detector, repo_root)
        except (KeyError, SyntaxError, OSError) as exc:
            failures.append(Failure(MALFORMED_REGISTER, f"scan of {scope.root!r} failed: {exc}"))
            continue

        found = {site.identity.as_tuple() for site in discovered}
        for site in sorted(discovered, key=lambda s: s.identity.as_tuple()):
            if site.identity.as_tuple() not in registered:
                failures.append(
                    Failure(
                        UNREGISTERED_SITE,
                        f"{_identity_str(site.identity)} (line {site.line}) is not registered",
                    )
                )
        in_scope = sorted(
            key for key in registered if _within(key[0], scope.root)
        )
        for key in in_scope:
            if key not in found:
                failures.append(
                    Failure(
                        ABSENT_REGISTERED_SITE,
                        "{} is registered but no longer exists".format(
                            "::".join(str(part) for part in key)
                        ),
                    )
                )

    return tuple(failures)


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_REGISTER = Path(__file__).resolve().parent / "register.json"


def main():
    """Verify the canonical register. Returns a process exit code."""
    from .provenance import RegisterFileProvenance

    provenance = RegisterFileProvenance(
        finding_register=REPO_ROOT / "docs/governance/AIOS_FINDING_REGISTER_v1.0.md",
        decision_register=(
            REPO_ROOT / "docs/governance/AIOS_GOVERNANCE_DECISION_REGISTER_v1.0.md"
        ),
    )
    failures = verify(DEFAULT_REGISTER, REPO_ROOT, provenance)
    for failure in failures:
        print(f"error: {failure}")
    if failures:
        print(f"bounded exception register check failed: {len(failures)} failure(s)")
        return 1
    print("bounded exception register check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
