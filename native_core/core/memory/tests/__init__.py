"""Memory boundary conformance tests (Native Core Blueprint §27).

Tests assert governance properties of the Memory subsystem — derives only
from Trace, never mutates Trace (INV-5), candidate-generation only with no
promotion or authority (INV-8; PR-3), dependency isolation, fail-closed
(PR-4), legacy isolation, determinism, and round-trip/derivation correctness
— not implementation nicety. Standard-library `unittest` only (Blueprint §27).
"""
