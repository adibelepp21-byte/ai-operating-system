"""
Canonical Key Validator.

Purpose: confirm every instance's declared Canonical Key matches the
ratified format <entity-type>.<stable-name-slug> (EARC §9, EARC
Amendment v1.1), and that the type prefix matches the subdirectory the
instance actually lives in.

Validation scope: the Metadata section's Canonical Key line only.

Assumptions: the key is recorded as "**Canonical Key:** `...`" in
Markdown, since no dedicated field or fixed serialization exists yet.

False-positive risk: medium — any author phrasing the key differently
(e.g. without backticks) would be missed, not flagged, since this
validator does not attempt to guess at alternate phrasings.

Operational value: high — this is the one property every instance
depends on the most (EARC's Canonical Identifier Model), and it is
currently unenforced by anything except author care.

Severity model: every finding here is "error" — a malformed or
misprefixed key breaks the Canonical Identifier Model the whole catalog
depends on for reference integrity; there is no lesser-severity variant.
"""

from .catalog import catalog_files, extract_canonical_key, read_text, rel, KEY_FORMAT_RE
from .models import Finding

NAME = "Canonical Key Validator"


def run():
    findings = []
    for etype, f in catalog_files():
        text = read_text(f)
        key = extract_canonical_key(text)
        if key is None:
            findings.append(Finding(NAME, "error", "no Canonical Key found", rel(f)))
            continue
        if not KEY_FORMAT_RE.match(key):
            findings.append(Finding(
                NAME, "error",
                f"'{key}' does not match <entity-type>.<stable-name-slug>", rel(f),
            ))
            continue
        prefix = key.split(".", 1)[0]
        if prefix != etype:
            findings.append(Finding(
                NAME, "error",
                f"key prefix '{prefix}' does not match directory '{etype}'", rel(f),
            ))
    return findings
