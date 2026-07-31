"""
Relative Link Validator.

Purpose: confirm every relative Markdown link in every catalog artifact
resolves to a real file on disk.

Validation scope: every .md link in every execution-catalog file,
including links to Framework documents and Agent Definition instances,
not just intra-catalog links.

Assumptions: links are standard Markdown [text](path) syntax; no
HTML-style links are used anywhere in the corpus (confirmed true by
inspection).

False-positive risk: low — file existence is a binary, objective check.

Operational value: high — this exact check caught a real, systematic
defect (an off-by-one path depth in every Framework back-link) during
Governance Freeze Gamma.

Severity model: every finding is "error" — a non-resolving link is
always a defect, never a matter of interpretation.
"""

from .catalog import catalog_files, extract_md_links, read_text, rel
from .models import Finding

NAME = "Relative Link Validator"


def run():
    findings = []
    for etype, f in catalog_files():
        text = read_text(f)
        for link in extract_md_links(text):
            if link.startswith("http"):
                continue
            target = (f.parent / link).resolve()
            if not target.is_file():
                findings.append(Finding(NAME, "error", f"-> {link}: does not resolve", rel(f)))
    return findings
