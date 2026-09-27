"""Principals, the authenticator port, scope authorization and audit (FS-06).

**Authentication is a port.** The ratified mechanism is `FS-DP-02` B3,
operator bearer tokens (Architect decision, Register `§81`):
`OperatorTokenAuthenticator`. The host holds only SHA-256 hashes of the
tokens, each with a subject and scopes, in `AIOS_OPERATOR_TOKENS`; the
operator holds the tokens. With no configuration, or a configuration that does
not parse exactly, it authenticates nobody, so every route but health answers
401 (fail closed). `NoAuthenticator` remains the explicit refuse-everyone port.

**Authorization is by scope**, one per route, decided here and only here. The
frontend may ask which scopes it holds (`/api/v1/session`) in order to render,
but it never decides: the backend checks every request (Act NC-12).

**Audit** records every decision, allowed or refused: who, what route, which
scope, the outcome. It never records a header, a credential or a request body
(Act NC-10). It is append-only, through the certified `StorageFacility`.
"""

from __future__ import annotations

import abc
import hashlib
import hmac
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, FrozenSet, Iterator, List, Mapping, Optional, Tuple

from native_core.core.infrastructure import StorageFacility

OBSERVE = "aios.observe"
RUN_WORKFLOW = "aios.workflow.run"
AUDIT = "aios.audit"
SCOPES = (OBSERVE, RUN_WORKFLOW, AUDIT)

#: A route open to anyone. Only liveness uses it.
PUBLIC = "public"
#: A route open to any authenticated principal, whatever its scopes.
AUTHENTICATED = "authenticated"

AUDIT_PARTITION = "fullstack-audit"
#: The audit entry format; successor formats are read beside it (FS-04 `§4`).
AUDIT_FORMAT = "fullstack.audit/1"


@dataclass(frozen=True)
class Principal:
    """Who is asking, and what the authenticator granted them. An application
    principal, not an AIOS entity: it holds no AIOS authority (FS-DP-02 A1)."""

    subject: str
    scopes: FrozenSet[str]

    def __post_init__(self):
        if not isinstance(self.subject, str) or not self.subject.strip():
            raise ValueError("a principal has a subject")
        object.__setattr__(self, "scopes", frozenset(self.scopes))
        unknown = self.scopes - set(SCOPES)
        if unknown:
            raise ValueError(f"unknown scope(s): {sorted(unknown)}")


class Authenticator(abc.ABC):
    """The authentication port. Returns a principal, or None for nobody."""

    #: Named in `/api/v1/health` so an operator can see which mechanism runs.
    mechanism = "unspecified"

    @abc.abstractmethod
    def authenticate(self, headers: Mapping[str, str]) -> Optional[Principal]:
        """`headers` has lower-case names. Must not raise on a bad credential:
        a credential that does not verify is simply nobody."""


class NoAuthenticator(Authenticator):
    """Nobody is authenticated."""

    mechanism = "none — no authenticator configured; every protected route answers 401"

    def authenticate(self, headers: Mapping[str, str]) -> Optional[Principal]:
        return None


#: Where the host keeps the operator-token configuration (FS-DP-02 B3).
OPERATOR_TOKENS_VARIABLE = "AIOS_OPERATOR_TOKENS"
#: The one scheme accepted, and the token grammar of RFC 6750 `b64token`.
_BEARER = re.compile(r"Bearer ([A-Za-z0-9\-._~+/]+=*)", re.IGNORECASE)
MAX_TOKEN_CHARS = 512
_SHA256_HEX = re.compile(r"[0-9a-f]{64}")
_ENTRY_KEYS = {"subject", "sha256", "scopes"}


class OperatorTokenConfigurationError(ValueError):
    """The operator-token configuration does not parse exactly. Its message
    never quotes the configuration."""


def token_sha256(token: str) -> str:
    """The server-side representation of a token: its SHA-256, in lower-case hex."""
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def parse_operator_tokens(text: str) -> Tuple[Tuple[str, Principal], ...]:
    """`AIOS_OPERATOR_TOKENS` → ((sha256, principal), ...), or refuse it whole.

    The value is a JSON array of objects, one per principal::

        [{"subject": "founder", "sha256": "<64 hex>",
          "scopes": ["aios.observe", "aios.workflow.run", "aios.audit"]}]

    `sha256` is the hash of the token, never the token: an entry with any key
    but `subject`, `sha256` and `scopes` is refused, so a plaintext token cannot
    be configured by mistake. `scopes` defaults to `aios.observe` alone (least
    privilege, package `FS-DP-02`); the others are granted explicitly. Two
    entries may not share a hash or a subject."""
    try:
        entries = json.loads(text)
    except ValueError:
        raise OperatorTokenConfigurationError("not JSON") from None
    if not isinstance(entries, list):
        raise OperatorTokenConfigurationError("not a JSON array")
    parsed, hashes, subjects = [], set(), set()
    for number, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            raise OperatorTokenConfigurationError(f"entry {number} is not an object")
        unknown = set(entry) - _ENTRY_KEYS
        if unknown:
            raise OperatorTokenConfigurationError(
                f"entry {number} has unknown key(s) {sorted(unknown)}")
        digest, subject = entry.get("sha256"), entry.get("subject")
        scopes = entry.get("scopes", [OBSERVE])
        if not isinstance(digest, str) or not _SHA256_HEX.fullmatch(digest):
            raise OperatorTokenConfigurationError(
                f"entry {number}: sha256 must be 64 lower-case hex digits")
        if not isinstance(scopes, list) or not all(isinstance(x, str) for x in scopes):
            raise OperatorTokenConfigurationError(f"entry {number}: scopes must be a list")
        try:
            principal = Principal(subject, frozenset(scopes))
        except (ValueError, TypeError, AttributeError):
            raise OperatorTokenConfigurationError(
                f"entry {number}: a subject and known scopes are required") from None
        if digest in hashes or principal.subject in subjects:
            raise OperatorTokenConfigurationError(
                f"entry {number} repeats a hash or a subject")
        hashes.add(digest)
        subjects.add(principal.subject)
        parsed.append((digest, principal))
    return tuple(parsed)


class OperatorTokenAuthenticator(Authenticator):
    """`FS-DP-02` B3: operator bearer tokens, verified against hashes.

    The presented token is hashed and compared with every configured hash in
    constant time; the token itself is neither kept nor returned. Anything but
    `Authorization: Bearer <b64token>` authenticates nobody."""

    mechanism = "operator bearer tokens (FS-DP-02 B3)"
    #: Why the configuration authenticates nobody, if it does; never its value.
    configuration_error: Optional[str] = None

    def __init__(self, entries: Tuple[Tuple[str, Principal], ...] = ()):
        self._entries = tuple(entries)

    @classmethod
    def from_configuration(cls, text: Optional[str]) -> "OperatorTokenAuthenticator":
        """Empty or absent: nobody. Unparseable: nobody, and the reason is kept
        (never the value) for the operator to read in `configuration_error`."""
        if text is None or not text.strip():
            authenticator = cls(())
            authenticator.configuration_error = "not configured"
            return authenticator
        try:
            authenticator = cls(parse_operator_tokens(text))
            authenticator.configuration_error = None
        except OperatorTokenConfigurationError as error:
            authenticator = cls(())
            authenticator.configuration_error = f"refused: {error}"
        return authenticator

    @classmethod
    def from_environment(cls, environment: Mapping[str, str]) -> "OperatorTokenAuthenticator":
        return cls.from_configuration(environment.get(OPERATOR_TOKENS_VARIABLE))

    def authenticate(self, headers: Mapping[str, str]) -> Optional[Principal]:
        value = headers.get("authorization")
        if not isinstance(value, str) or len(value) > MAX_TOKEN_CHARS + len("Bearer "):
            return None
        match = _BEARER.fullmatch(value)
        if match is None:
            return None
        presented = token_sha256(match.group(1))
        found = None
        for digest, principal in self._entries:  # no early exit: constant work
            if hmac.compare_digest(presented, digest):
                found = principal
        return found


@dataclass(frozen=True)
class Decision:
    allowed: bool
    status: int
    error: Optional[str]
    subject: Optional[str]


def authorize(principal: Optional[Principal], scope: str) -> Decision:
    """The single authorization rule. Fails closed on an unknown scope name."""
    subject = principal.subject if principal else None
    if scope == PUBLIC:
        return Decision(True, 200, None, subject)
    if principal is None:
        return Decision(False, 401, "unauthenticated", None)
    if scope == AUTHENTICATED:
        return Decision(True, 200, None, subject)
    if scope not in SCOPES:
        return Decision(False, 403, "forbidden", subject)
    if scope not in principal.scopes:
        return Decision(False, 403, "forbidden", subject)
    return Decision(True, 200, None, subject)


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


class AuditLedger:
    """Append-only record of access decisions, one partition of the store."""

    FIELDS = ("format", "at", "request_id", "subject", "method", "path", "scope",
              "decision", "status")

    def __init__(self, storage: StorageFacility, clock: Callable[[], str] = _utc,
                 partition: str = AUDIT_PARTITION):
        self._storage = storage
        self._clock = clock
        self._partition = partition

    def record(self, *, request_id: str, subject: Optional[str], method: str,
               path: str, scope: str, decision: str, status: int) -> None:
        entry = {"format": AUDIT_FORMAT, "at": self._clock(), "request_id": request_id,
                 "subject": subject, "method": method, "path": path,
                 "scope": scope, "decision": decision, "status": status}
        self._storage.append(self._partition, json.dumps(
            entry, sort_keys=True, separators=(",", ":")).encode("utf-8"))

    def entries(self) -> Iterator[dict]:
        for position, raw in enumerate(self._storage.read(self._partition)):
            entry = json.loads(raw.decode("utf-8"))
            entry["position"] = position
            yield entry

    def page(self, offset: int, limit: int) -> List[dict]:
        return [e for e in self.entries() if offset <= e["position"] < offset + limit]
