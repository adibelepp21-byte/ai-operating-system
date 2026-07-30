"""Capability boundary conformance tests (Native Core Blueprint §27).

Tests assert the invariants Roadmap §9.6 names as this boundary's completion
criteria — INV-1 (exactly one owning Department), INV-9 (explicit versioned
dependencies), INV-10 (cross-Department dependencies governed, never silently
adopted), INV-11 (dependency graph queryable and observable, no undocumented
dependencies), INV-14 (zero-implementer capabilities flagged, not raised) —
together with the boundary's dependency rules and its absence of any execution
surface (capability_spec §5/§8; Freeze §4).

Standard-library `unittest` only. No external dependency (INV-12).
"""
