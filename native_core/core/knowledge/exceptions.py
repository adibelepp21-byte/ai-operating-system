"""
Knowledge fail-closed exceptions (Blueprint §12; knowledge_spec §11; PR-4;
Phase 3.308 Blueprint B10).

The named halt conditions of the Knowledge boundary. Every one expresses
Fail Closed (PR-4): a Knowledge operation that cannot proceed *accountably*
raises rather than returning a degraded or partial value, and never admits,
returns, or authorizes on the absence of positive evidence (3.308 B10).

Skeleton phase (3.310): these are structural declarations only — class names
and docstrings, no behavior, no logic. The raising sites are wired in the
later authorized implementation phases.

Ownership: Knowledge. Dependencies: none (stdlib only). Prohibited: carrying
any authority, decision, or state (§6.2 invariant 2).
"""

from __future__ import annotations


class KnowledgeError(RuntimeError):
    """Base for every fail-closed Knowledge halt. A Knowledge operation that
    cannot proceed accountably raises a subclass of this (PR-4)."""


class UnauthorizedPromotion(KnowledgeError):
    """Raised when admission/revision is attempted without an affirmative,
    provenance-verified Governance authorization for *that* candidate
    (INV-8; 3.308 B10.1–B10.4). Default deny — absence/ambiguity ⇒ raise."""


class InvalidKnowledgeVersion(KnowledgeError):
    """Raised when a version cannot be constructed accountably — missing
    identity or content, or a non-candidate content basis (3.308 B10.5–B10.6).
    Fail closed: an un-constructable version is never coerced into a valid one."""


class VersionNotFound(KnowledgeError):
    """Raised when a requested Knowledge item/version does not exist. Retrieval
    never fabricates a default-authoritative value on a miss (3.308 B10.8)."""


class KnowledgeStorageUnavailable(KnowledgeError):
    """Raised when the Knowledge storage facility is not provisioned/available.
    Fail closed: no silent success on an unavailable store (3.308 B10.7)."""
