"""Trace boundary conformance tests (Native Core Blueprint §27).

Tests assert governance properties of the Trace subsystem — INV-4
(unconditional, one-per-write), INV-5 (immutable, append-only, no
edit/delete), INV-6 (captured content, self-contained), determinism,
fail-closed behaviour, and the absence of forbidden dependencies — not
implementation nicety. Standard-library `unittest` only (Blueprint §27, [O]).
"""
