"""
Tool invocation.

Retains the request/execution/evidence/failure separation introduced in
the Execution Foundation Stabilization Phase (ToolRequest / ToolExecution
with succeeded / evidence / error). This phase (Real Capability
Integration) replaces the prior stub for
tool.cross-reference-link-validator-interface with a real repository
analysis capability — it performs the actual check its own Interface
field describes, against real files on disk, rather than a scripted
placeholder.

Real implementation's own contract, matching the directive's required
shape exactly:

  Input:  repository_path, reference_target, expected_reference
          (plus citing_document, kept for evidence/traceability — which
          document made the citation is not part of the resolution
          check itself, but is worth recording).
  Output: {"resolved": bool, "evidence": dict | None, "failure_reason": str | None}

Improvements over the prior heuristic:
  - **Heading-aware matching**: a heading regex now captures the actual
    heading level and title text, not just a boolean.
  - **Target ownership verification**: "resolved" is only True when the
    expected reference is one of the *target document's own* headings —
    a bare textual mention elsewhere in the document (e.g. citing a
    different document's section number in prose) is reported as
    resolved=False with match_type "mention_only", not conflated with a
    real match. This is the same distinction introduced last phase,
    carried into the new input/output contract.
  - **Evidence extraction**: on a real match, the actual heading text is
    returned as evidence, not only a match/no-match verdict.

No authentication model, vendor API framework, infrastructure
abstraction, or permission-model change is introduced. Tool remains the
sole entity permitted a direct external dependency (Domain Model §7
invariant 12); this implementation still holds none — it only reads
local repository files under the given repository_path.
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from .governance_reader import canonical_key, read
from .tool_executor import ToolExecutor
from .tool_registry import ToolRegistry

HEADING_RE_TMPL = r"^(#+)\s*{n}\.\s*(.+)$"


@dataclass(frozen=True)
class ToolRequest:
    """The requested action — what the caller asked the Tool to do,
    captured before any execution occurs."""
    tool_canonical_key: str
    action: str
    parameters: dict


@dataclass(frozen=True)
class ToolExecution:
    """The result of actually running a Tool. `succeeded` reflects
    whether the implementation ran to completion without raising — it
    is independent of the semantic outcome carried in `evidence` (a
    Tool can succeed at running and still report resolved=False).

    Tier 2 additions (all default so nothing reading only the original
    four fields is affected): `fingerprint` is the content-hash
    signature verification.py computed for this call's file-shaped
    parameters (None if none); `from_cache` and `verification_status`
    report what the Evidence Verification Layer decided — see
    tool_executor.py."""
    request: ToolRequest
    succeeded: bool
    evidence: Optional[dict]
    error: Optional[str] = None
    fingerprint: Optional[tuple] = None
    from_cache: bool = False
    verification_status: str = "not_applicable"


def load_canonical_key(tool_path):
    return canonical_key(read(tool_path))


def invoke(tool_path, action, **parameters):
    """Public entry point, signature and core return fields unchanged
    since before Tier 1 (`request`/`succeeded`/`evidence`/`error`).
    Internally now delegates to a module-level ToolExecutor (see
    _registry()/_executor() below), which as of Tier 2 also performs
    cache verification when a cache is attached — the default executor
    has none, so production behavior here remains unaffected; the new
    fields (`fingerprint`, `from_cache`, `verification_status`) are
    additive and default to inert values when no cache is in play."""
    key = load_canonical_key(tool_path)
    request = ToolRequest(tool_canonical_key=key, action=action, parameters=parameters)
    result = _executor().execute(request)
    return ToolExecution(
        request=request, succeeded=result.succeeded, evidence=result.raw, error=result.error,
        fingerprint=result.fingerprint, from_cache=result.from_cache, verification_status=result.verification_status,
    )


def _registry():
    global _REGISTRY
    if _REGISTRY is None:
        _REGISTRY = ToolRegistry()
        for tool_key, adapter in IMPLEMENTATIONS.items():
            _REGISTRY.register(tool_key, adapter, cache_key_fn=CACHE_KEY_FNS.get(tool_key), legacy=tool_key not in CACHE_KEY_FNS)
    return _REGISTRY


def _executor():
    global _EXECUTOR
    if _EXECUTOR is None:
        _EXECUTOR = ToolExecutor(_registry())
    return _EXECUTOR


_REGISTRY = None
_EXECUTOR = None


def _resolve_target(repository_path, reference_target):
    target_path = Path(reference_target)
    if not target_path.is_absolute():
        target_path = Path(repository_path) / reference_target
    return target_path.resolve()


def _cross_reference_link_validator(citing_document, repository_path, reference_target, expected_reference):
    """Real repository analysis: does `reference_target` exist under
    `repository_path`, and does it own `expected_reference` (e.g. "§7")
    as one of its own numbered headings?"""
    target_path = _resolve_target(repository_path, reference_target)

    if not target_path.is_file():
        return {
            "resolved": False, "evidence": None,
            "failure_reason": f"reference_target does not resolve: {reference_target}",
        }

    text = target_path.read_text(encoding="utf-8")
    section_num = re.sub(r"[^\d]", "", expected_reference or "")

    if not section_num:
        return {
            "resolved": True,
            "evidence": {"match_type": "file_only", "file": target_path.name, "citing_document": str(citing_document)},
            "failure_reason": None,
        }

    heading_re = re.compile(HEADING_RE_TMPL.format(n=section_num), re.MULTILINE)
    match = heading_re.search(text)
    if match:
        return {
            "resolved": True,
            "evidence": {
                "match_type": "heading",
                "heading_level": len(match.group(1)),
                "heading_text": match.group(2).strip(),
                "file": target_path.name,
                "citing_document": str(citing_document),
            },
            "failure_reason": None,
        }

    if f"§{section_num}" in text:
        return {
            "resolved": False,
            "evidence": {"match_type": "mention_only", "file": target_path.name, "citing_document": str(citing_document)},
            "failure_reason": (
                f"§{section_num} is mentioned in {target_path.name} but is not one of "
                "its own headings — likely a citation to a different document's section"
            ),
        }

    return {
        "resolved": False, "evidence": None,
        "failure_reason": f"§{section_num} not found anywhere in {target_path.name}",
    }


def _document_structure_parser(document_path):
    """Real implementation for tool.document-structure-parser-interface,
    added in the Memory Expansion Validation Phase to extend the
    harness's Skill/Tool category coverage. Matches the Tool's own
    declared Interface exactly: reads a document, returns its
    recognized structural elements (heading level, section number if
    present, title) in order — no content interpretation."""
    path = Path(document_path)
    if not path.is_file():
        return {"resolved": False, "elements": None, "failure_reason": f"document does not resolve: {document_path}"}

    elements = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("#"):
            continue
        level = len(stripped) - len(stripped.lstrip("#"))
        rest = stripped.lstrip("#").strip()
        num_match = re.match(r"^(\d+)\.\s*(.*)$", rest)
        elements.append({
            "level": level,
            "number": num_match.group(1) if num_match else None,
            "title": num_match.group(2) if num_match else rest,
        })
    return {"resolved": True, "elements": elements, "failure_reason": None}


def _text_similarity_comparison(passage_a, passage_b):
    """Real implementation for tool.text-similarity-comparison-interface.
    Uses Python's standard-library difflib.SequenceMatcher — no external
    or vendor dependency, consistent with every other Tool implemented
    so far. Returns a 0.0-1.0 similarity ratio, not a claim about
    semantic meaning: two passages can be lexically similar without
    meaning the same thing, and this stub makes no attempt to
    distinguish that — a real, disclosed limitation."""
    import difflib
    if not passage_a or not passage_b:
        return {"resolved": False, "similarity": None, "failure_reason": "one or both passages are empty"}
    ratio = difflib.SequenceMatcher(None, passage_a, passage_b).ratio()
    return {"resolved": True, "similarity": round(ratio, 4), "failure_reason": None}


IMPLEMENTATIONS = {
    "tool.cross-reference-link-validator-interface": _cross_reference_link_validator,
    "tool.document-structure-parser-interface": _document_structure_parser,
    "tool.text-similarity-comparison-interface": _text_similarity_comparison,
}


# --- Tier 1 cache-key derivers, one per Tool, registered incrementally ---
# (Stages 3-5). Each replaces what was, before Tier 1, hardcoded and
# Tool-specific logic living only in memory/consumption.py. Registering
# one here has NO behavioral effect until Stage 6 attaches an actual
# cache to the default executor — ToolExecutor._check_cache() returns
# None immediately whenever self.cache is None, regardless of whether a
# cache_key_fn is registered. This is what makes Stages 3-5 verifiably
# inert: the function exists and is tested in isolation, but nothing
# live consults it yet.

def _text_similarity_cache_key(request):
    """Stage 3 (lowest risk: used by 1 Skill -- duplicate-content-detection
    -- with zero real findings observed in any prior run)."""
    p = request.parameters
    return ("tool.text-similarity-comparison-interface", p.get("passage_a"), p.get("passage_b"))


def _document_structure_cache_key(request):
    """Stage 4."""
    p = request.parameters
    return ("tool.document-structure-parser-interface", p.get("document_path"))


def _cross_reference_cache_key(request):
    """Stage 5. Formalizes the same (reference_target, expected_reference)
    identity memory/consumption.py already derived by hand -- now
    registered once, generically, instead of hardcoded at the one call
    site that used it."""
    p = request.parameters
    return ("tool.cross-reference-link-validator-interface", p.get("reference_target"), p.get("expected_reference"))


# Populated one Tool at a time during Tier 1 migration (Stages 3-5). A
# tool_key present here has a registered cache-key deriver and is no
# longer "legacy" in ToolRegistry terms; absent means still legacy.
CACHE_KEY_FNS = {
    "tool.text-similarity-comparison-interface": _text_similarity_cache_key,
    "tool.document-structure-parser-interface": _document_structure_cache_key,
    "tool.cross-reference-link-validator-interface": _cross_reference_cache_key,
}
