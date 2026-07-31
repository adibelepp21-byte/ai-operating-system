"""
Duplicate Canonical Key Detector.

Purpose: confirm no two instances of the same entity type share a
Canonical Key, per EARC's ratified per-type uniqueness scoping.

Validation scope: Canonical Key values, grouped by entity type, plus an
informational cross-type check.

Assumptions: uniqueness is required only within a type (per EARC §9),
not globally across all four types; a Skill and a Tool may in principle
share a bare slug without violating anything ratified.

False-positive risk: low.

Operational value: high — directly enforces a ratified invariant of the
identifier model with no other current enforcement mechanism.

Severity model: a same-type duplicate is "error" (violates a ratified
invariant). A cross-type duplicate bare slug is "informational" only
(not forbidden by EARC, but worth a human glance since it can make a
prose reference ambiguous to a reader who omits the type prefix). The
original single-file validator's docstring described this cross-type
check but never implemented it; this revision closes that gap.
"""

from collections import defaultdict

from .catalog import catalog_files, extract_canonical_key, read_text, rel, ENTITY_TYPES
from .models import Finding

NAME = "Duplicate Canonical Key Detector"


def run():
    findings = []
    per_type = {t: defaultdict(list) for t in ENTITY_TYPES}
    all_keys = []  # (etype, key, file)

    for etype, f in catalog_files():
        key = extract_canonical_key(read_text(f))
        if key is None:
            continue
        all_keys.append((etype, key, f))
        per_type.setdefault(etype, defaultdict(list))[key].append(f)

    for etype, keys in per_type.items():
        for key, files in keys.items():
            if len(files) > 1:
                paths = ", ".join(rel(p) for p in files)
                findings.append(Finding(
                    NAME, "error",
                    f"'{key}' used by {len(files)} files in {etype}/: {paths}",
                ))

    by_bare_slug = defaultdict(list)
    for etype, key, f in all_keys:
        bare = key.split(".", 1)[-1]
        by_bare_slug[bare].append((etype, key, f))

    for bare, entries in sorted(by_bare_slug.items()):
        types = {etype for etype, _, _ in entries}
        if len(types) > 1:
            paths = ", ".join(f"{k} ({rel(f)})" for _, k, f in entries)
            findings.append(Finding(
                NAME, "informational",
                f"slug '{bare}' reused across entity types: {paths}",
            ))

    return findings
