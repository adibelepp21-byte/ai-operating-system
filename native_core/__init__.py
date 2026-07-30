"""
AIOS Native Core.

The conformant implementation of the frozen AIOS architecture, built in
Phase 3 under the authority order: Constitution → Canonical Domain Model
→ Architecture Freeze → Engineering Specifications → Native Core Blueprint
→ Implementation Constitution. Nothing here may redefine anything above it
(Implementation Constitution §2, §4).

Structure mirrors the frozen architecture one-to-one (Native Core Blueprint
§2-§4): `core/` holds one module boundary per frozen subsystem; `shared/`
holds cross-boundary primitives and is a pure sink (everything may depend on
`shared`; `shared` depends on nothing in `core` — Blueprint §16).

Phase 3.1 (Stage I) implements the Infrastructure boundary only. No other
subsystem is implemented. This package is distinct from the legacy
`execution/` harness, which the Legacy Reuse Plan dispositions separately
and which this Native Core does not import or build upon.
"""
