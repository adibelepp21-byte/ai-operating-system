"""
Shared repository constants and file-reading helpers used by every
validator, the link classifier, and the dependency graph builder.

Kept as one small module (rather than duplicated per-validator) because
every validator in this package needs the same repository layout facts
and the same two or three regexes; this is genuine shared state, not
speculative abstraction.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
ORG_ROOT = REPO_ROOT / "docs" / "architecture" / "organization"
CATALOG_ROOT = ORG_ROOT / "execution-catalog"
ENTITY_TYPES = ["skill", "workflow", "runtime", "tool"]

CANONICAL_KEY_RE = re.compile(r"\*\*Canonical Key:\*\*\s*`([^`]+)`")
KEY_FORMAT_RE = re.compile(r"^(skill|workflow|runtime|tool)\.[a-z0-9]+(-[a-z0-9]+)*$")
MD_LINK_RE = re.compile(r"\]\(([^)]+\.md)\)")

REQUIRED_HEADERS = {
    "skill": ["## Metadata", "## Purpose / Description", "## Interface",
              "## Permitted Invocation Context", "## Version History"],
    "workflow": ["## Metadata", "## Purpose / Description", "## Composed Elements",
                 "## Compatibility Boundary Representation", "## Version History"],
    "runtime": ["## Metadata", "## Purpose / Description", "## Hosted Relationship",
                "## Compatibility Boundary Representation", "## Version History"],
    "tool": ["## Metadata", "## Purpose / Description", "## Interface",
             "## Version History"],
}


def catalog_files():
    files = []
    for etype in ENTITY_TYPES:
        d = CATALOG_ROOT / etype
        if d.is_dir():
            for f in sorted(d.glob("*.md")):
                files.append((etype, f))
    return files


def read_text(path):
    return path.read_text(encoding="utf-8")


def extract_canonical_key(text):
    m = CANONICAL_KEY_RE.search(text)
    return m.group(1) if m else None


def extract_md_links(text):
    return MD_LINK_RE.findall(text)


def rel(path):
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)
