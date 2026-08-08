"""
Bounded Exception Register — mechanism establishment (MB-01).

Purpose: provide an identity-based, append-only, fail-closed record of
conformance exceptions that a governance act has explicitly tolerated,
together with a read-only verifier that fails both when an unregistered
exception site appears and when a registered site has disappeared.

Validation scope: only the roots a register explicitly declares in its
`scan_scope`. A register that declares no scope scans nothing.

Assumptions: exception sites are discoverable by static analysis of
Python source; a site's enclosing qualified name and its ordinal within
that scope are stable under edits made elsewhere in the file.

False-positive risk: low for detection (AST-based, not textual), but
identity is deliberately strict — a site that moves scope, or that
changes ordinal because a sibling site was added or reordered, is
reported as both an absent registration and an unregistered site. That
is intended: a structural reorder is observable architectural change and
requires re-authorization.

Operational value: converts an unbounded tolerance ("this test is
expected to fail") into an enumerated one ("these specific sites, and no
others").

Severity model: always failure. There is no warning level. Ambiguity
resolves to failure in every case.

Authority: ADR-0009 (Approved); MB-01 Stage 1 (P7-I48); Stage 2
implementation authorized by P7-I52. This package implements the
mechanism only. It registers nothing, and it is applied to no boundary.
"""

from .identity import Site, SiteIdentity, discover_sites
from .register import Register, RegisterEntry, RegisterError, load_register
from .provenance import ProvenanceResolver, RegisterFileProvenance
from .verifier import Failure, verify

__all__ = [
    "Failure",
    "ProvenanceResolver",
    "Register",
    "RegisterEntry",
    "RegisterError",
    "RegisterFileProvenance",
    "Site",
    "SiteIdentity",
    "discover_sites",
    "load_register",
    "verify",
]
