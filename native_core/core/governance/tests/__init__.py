"""Governance boundary conformance tests (Native Core Blueprint §27).

Tests assert governance properties — human authority absolute (§6.2 invariant
2), no automatic approval/rejection/promotion (PR-3), fail closed (PR-4),
reject absolute, never creates Knowledge / mutates Memory / mutates Trace,
dependency isolation, and determinism — not implementation nicety.
Standard-library `unittest` only (Blueprint §27).
"""
