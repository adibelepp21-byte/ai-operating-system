"""
Cross-Reference Validator.

Purpose: confirm that instance-to-instance relationships declared in
prose point to files that actually exist and, where the link is
classified as a governed relationship shape, that the target is the
expected entity type and carries a valid Canonical Key.

Validation scope: every Markdown link in each catalog file's body,
classified by link_classifier.classify() before being checked. Prior to
this revision, this validator treated every link identically; link
classification is this phase's precision improvement (see
link_classifier.py for the exact category mapping).

Assumptions: classification is heuristic (path-pattern based, not a
machine-structured relationship field, since none exists yet); a link a
human would recognize as a relationship reference but whose path doesn't
match a known pattern falls back to "navigation convenience" and is not
type-checked.

False-positive risk:
  - "wrong target type for this relationship" (error): low — the two
    classified relationship shapes (Workflow composition, Skill
    invocation) are unambiguous once a link is classified as one of
    them.
  - "target has no Canonical Key" (warning): remains high by design, as
    in the original single-file validator — this only fires for
    catalog-internal targets, and every catalog file already carries a
    key today, so it currently never fires. Kept as a warning rather
    than an error because a target legitimately outside the catalog
    would trip it without being a defect.

Operational value: medium-high for catching broken or miswired
relationships; classification materially improves precision over
treating every link as equivalent.
"""

from . import catalog
from .catalog import catalog_files, extract_canonical_key, extract_md_links, read_text, rel
from .link_classifier import classify, EXPECTED_TARGET_TYPE
from .models import Finding

NAME = "Cross-Reference Validator"


def run():
    findings = []
    for etype, f in catalog_files():
        text = read_text(f)
        for link in extract_md_links(text):
            if link.startswith("http"):
                continue
            target = (f.parent / link).resolve()
            if not target.is_file():
                continue  # covered by Relative Link Validator
            category = classify(etype, f, target, catalog.CATALOG_ROOT)

            expected_type = EXPECTED_TARGET_TYPE.get(category)
            if expected_type:
                try:
                    actual_type = target.relative_to(catalog.CATALOG_ROOT).parts[0]
                except ValueError:
                    actual_type = None
                if actual_type != expected_type:
                    findings.append(Finding(
                        NAME, "error",
                        f"-> {link}: classified as '{category}' but target is in "
                        f"'{actual_type}/', expected '{expected_type}/'",
                        rel(f),
                    ))
                    continue

            if catalog.CATALOG_ROOT in target.parents and not extract_canonical_key(read_text(target)):
                findings.append(Finding(
                    NAME, "warning",
                    f"-> {link} ({category}): target has no Canonical Key",
                    rel(f),
                ))
    return findings
