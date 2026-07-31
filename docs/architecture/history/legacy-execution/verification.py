"""
Evidence Verification Layer — Tier 2.

Sits between Memory consumption (a cache hit) and trusting that hit.
Before any cached evidence is returned, this layer recomputes a
lightweight fingerprint of whatever file-shaped inputs the original
call referenced and compares it to the fingerprint recorded when that
cache entry was written. A mismatch — or a cache entry with no recorded
fingerprint at all — means verification fails closed: the entry is
treated as unverifiable, not trusted.

Deliberately generic, not Tool-specific, per the requirement to avoid
coupling verification to any one Tool implementation: it fingerprints
whatever parameter values happen to be real, existing file paths, using
a content hash (blake2b — correctness prioritized over speed, per the
Tier 2 principle "correctness before performance"; mtime+size was
considered and rejected as the primary signal because it can miss a
same-second, same-size edit). A Tool whose parameters reference no
files at all (e.g. text-similarity-comparison-interface, which compares
literal passed-in text) yields an empty fingerprint; verification for
such a call always succeeds, correctly — there is no external state
that could have drifted when the input *is* the content.

Kept isolated in its own module, imported by tool_executor.py only.
Tool adapters never import this and never know it exists.
"""

import hashlib
from pathlib import Path
from typing import Optional


def _fingerprint_file(path) -> Optional[str]:
    try:
        data = Path(path).read_bytes()
    except OSError:
        return None
    return hashlib.blake2b(data, digest_size=16).hexdigest()


def compute_fingerprint(parameters: dict) -> Optional[tuple]:
    """Fingerprints every parameter value that is a string pointing at
    a real, currently-existing file. Order-independent (sorted by key)
    so identical parameters always produce an identical fingerprint
    regardless of dict ordering. Returns None if nothing in the
    parameters resolves to a real file — the common case for
    content-only Tools."""
    parts = []
    for k in sorted(parameters):
        v = parameters.get(k)
        if isinstance(v, str):
            fp = _fingerprint_file(v)
            if fp is not None:
                parts.append(f"{k}={fp}")
    return tuple(parts) if parts else None


def verify(cached_fingerprint, current_parameters: dict) -> bool:
    """True if a cache entry is still safe to trust.

    - If the current parameters reference no real files at all AND the
      cache entry itself was written under that same condition
      (`cached_fingerprint` is also None), there is nothing external
      that could have drifted — always valid.
    - In every other case the recomputed current fingerprint must
      exactly match what was recorded. This covers two fail-closed
      scenarios by the same comparison: a cache entry written before
      this layer existed (no fingerprint ever recorded, but the current
      call now resolves a real file) does not match a real fingerprint;
      and a cache entry whose fingerprinted file has since been deleted
      or become unreadable (current recomputation returns None, but a
      real fingerprint was recorded) does not match either — compute_
      fingerprint() alone cannot tell "never had a file" apart from
      "had a file, it's gone now" (both yield None), so that
      distinction is made here by also checking whether a real
      fingerprint was ever recorded in the first place. Fails closed,
      not open, deliberately, in both cases."""
    current_fingerprint = compute_fingerprint(current_parameters)
    if cached_fingerprint is None and current_fingerprint is None:
        return True
    return cached_fingerprint == current_fingerprint
