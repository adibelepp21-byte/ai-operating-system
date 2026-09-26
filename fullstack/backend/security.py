"""Principals, the authenticator port, scope authorization and audit (FS-06).

**Authentication is a port, and the shipped implementation refuses everyone.**
How a person proves who they are is Architect-reserved (Freeze `§10`;
`FD-FS-001` D2-A; decision package `FS-DP-02`). Until that is ratified,
`NoAuthenticator` is the production default: it authenticates nobody, so every
route but health answers 401. Tests inject their own authenticator; nothing in
this package ships one that accepts a credential.

**Authorization is by scope**, one per route, decided here and only here. The
frontend may ask which scopes it holds (`/api/v1/session`) in order to render,
but it never decides: the backend checks every request (Act NC-12).

**Audit** records every decision, allowed or refused: who, what route, which
scope, the outcome. It never records a header, a credential or a request body
(Act NC-10). It is append-only, through the certified `StorageFacility`.
"""

from __future__ import annotations

import abc
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable, FrozenSet, Iterator, List, Mapping, Optional

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
    """The default until `FS-DP-02` is ratified: nobody is authenticated."""

    mechanism = "none — FS-DP-02 not ratified; every protected route answers 401"

    def authenticate(self, headers: Mapping[str, str]) -> Optional[Principal]:
        return None


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
