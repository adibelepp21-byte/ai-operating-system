"""
Execution Catalog Integrity Checker.

Purpose: a consolidated structural check that each artifact contains the
section headers its own Framework's Document Structure Requirements
specify, and that its declared Owning designation and Version fields are
present.

Validation scope: section headers and two Metadata fields per file.

Assumptions: header text matches each Framework's §8 wording exactly; a
differently-worded but equivalent header would be missed.

False-positive risk: medium — relies on exact header string matching.

Operational value: high as a single summary check of overall structural
conformance across the whole catalog.

Severity model: always "error" — a missing required section or field is
a structural non-conformance with the artifact's own governing
Framework, not a matter of degree.
"""

from .catalog import catalog_files, read_text, rel, REQUIRED_HEADERS
from .models import Finding

NAME = "Execution Catalog Integrity Checker"


def run():
    findings = []
    for etype, f in catalog_files():
        text = read_text(f)
        for header in REQUIRED_HEADERS[etype]:
            if header not in text:
                findings.append(Finding(NAME, "error", f"missing required section '{header}'", rel(f)))
        if "**Owning designation:**" not in text:
            findings.append(Finding(NAME, "error", "missing Owning designation field", rel(f)))
        if "**Version:**" not in text:
            findings.append(Finding(NAME, "error", "missing Version field", rel(f)))
    return findings
