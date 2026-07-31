"""
Minimal, read-only governance-document parsing shared across this
execution harness.

Deliberately not imported from tools/validators/ — that package
validates documents; this package drives them. The two are independent,
differently-purposed implementation-tier layers; duplicating a handful
of small regexes here is cheaper than coupling them together before
there is any evidence that coupling is worth its cost.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ORG_ROOT = REPO_ROOT / "docs" / "architecture" / "organization"
CATALOG_ROOT = ORG_ROOT / "execution-catalog"

CANONICAL_KEY_RE = re.compile(r"\*\*Canonical Key:\*\*\s*`([^`]+)`")
VERSION_RE = re.compile(r"\*\*Version:\*\*\s*([^\n]+)")
MD_LINK_RE = re.compile(r"\]\(([^)]+\.md)\)")


def read(path):
    return Path(path).read_text(encoding="utf-8")


def canonical_key(text):
    m = CANONICAL_KEY_RE.search(text)
    return m.group(1) if m else None


def version(text):
    m = VERSION_RE.search(text)
    return m.group(1).strip() if m else "unknown"


def section_body(text, header):
    pattern = re.compile(rf"^## {re.escape(header)}\s*\n(.*?)(?=^## |\Z)", re.MULTILINE | re.DOTALL)
    m = pattern.search(text)
    return m.group(1) if m else ""


def section_links(text, header):
    body = section_body(text, header)
    return [l for l in MD_LINK_RE.findall(body) if not l.startswith("http")]
