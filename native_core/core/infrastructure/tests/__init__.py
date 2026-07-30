"""Infrastructure boundary conformance tests (Native Core Blueprint §27).

Testing is conformance to the frozen architecture, not implementation
detail: these tests assert that the Infrastructure boundary upholds its
governing invariants and constraints (INV-12 single external boundary,
OQ-2 no independent Trace, PR-4 fail closed, append-only storage, module
isolation). Written against the Python standard library `unittest` only —
no external test framework — since the test framework choice is [O] reserved
(Blueprint §27).
"""
