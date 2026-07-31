"""Skill boundary conformance tests (Native Core Blueprint §27).

Tests assert the invariants Roadmap §9.7 names as this boundary's completion
criteria — INV-15 (an Agent Definition may specify zero or more Skills; an
empty declaration is a valid architectural state), INV-12 (Tool is the only
entity permitted an external dependency, so this boundary holds none), INV-4
(every Agent Instance action produces exactly one Trace, so a Skill authors
none of its own) — together with the boundary's dependency rules, its absence
of any execution surface, and the reserved status of registry and discovery
(skill_spec §5/§8/§13/§14; Blueprint §9; Freeze §4).

Standard-library `unittest` only. No external dependency (INV-12).
"""
