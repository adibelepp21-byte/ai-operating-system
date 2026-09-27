"""The `StorageFacility` backend on Supabase (FS-DP-01 Option A, ratified by
`FS-ARCH-RAT-001`, Register `§68`).

```text
Trace · run records · audit  →  StorageFacility  →  SupabaseStorage  →  aios_records
```

It implements the certified contract (`native_core/core/infrastructure/
storage.py`) and adds nothing to it: append a record to a partition, read a
partition in append order, list the partitions. There is no edit and no
delete, here or in the database, where privileges and triggers refuse both
(`fullstack/deploy/supabase/migrations/`).

**Supabase is the backend, not the model.** The table holds opaque bytes per
partition; Trace, runs and audit keep their own meaning inside the record. A
record is sent and returned as bytes, unchanged. Like the local backend, a
record may not hold a raw newline, so either store can be exported to the other
without loss.

It talks to PostgREST over HTTPS with the standard library only, using a
server-side key the operator supplies. The key is sent in request headers and
nowhere else: never logged, never in an error, never in a record.

**Fail Closed** (PR-4): any failure to append or read raises
`StorageUnavailable`; there is no partial success and no local fallback.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Callable, Dict, Iterator, List, Optional, Tuple
from urllib.parse import quote

from native_core.core.infrastructure import StorageFacility

TABLE = "aios_records"
PARTITIONS_FUNCTION = "aios_partitions"
PAGE_ROWS = 1000
TIMEOUT_SECONDS = 10.0
MAX_PARTITION_CHARS = 200

#: (method, url, headers, body) → (status, body)
Transport = Callable[[str, str, Dict[str, str], Optional[bytes]], Tuple[int, bytes]]


class StorageUnavailable(RuntimeError):
    """The database could not complete a read or an append. Never carries the
    key, a header or a response body: only what failed and the status."""


def urllib_transport(method: str, url: str, headers: Dict[str, str],
                     body: Optional[bytes]) -> Tuple[int, bytes]:
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        return error.code, error.read()
    except (urllib.error.URLError, OSError) as error:
        raise StorageUnavailable(f"database unreachable ({type(error).__name__})") from None


class SupabaseStorage(StorageFacility):
    """Append-only partitions in the Supabase table `aios_records`."""

    name = "storage.supabase-append-only"

    def __init__(self, project_url: str, secret_key: str,
                 transport: Transport = urllib_transport):
        super().__init__()
        if not project_url.startswith("https://") or project_url.endswith("/"):
            raise ValueError("project_url must be an https origin without a trailing slash")
        if not isinstance(secret_key, str) or not secret_key.strip():
            raise ValueError("a server-side key is required")
        self._rest = project_url + "/rest/v1"
        self._key = secret_key
        self._transport = transport

    def __repr__(self) -> str:  # never the key
        return f"SupabaseStorage({self._rest!r})"

    # -- Facility -------------------------------------------------------------

    def _provision(self) -> None:
        # One read proves the table, the key and the privileges before the
        # Runtime is bootstrapped on this facility (Fail Closed).
        self._get(f"{self._rest}/{TABLE}?select=seq&limit=1", "provision")

    # -- StorageFacility ------------------------------------------------------

    def append(self, partition: str, record: bytes) -> None:
        self.require_ready()
        _check_partition(partition)
        if not isinstance(record, (bytes, bytearray)):
            raise TypeError("record must be bytes")
        if b"\n" in record:
            raise ValueError("record must not contain a raw newline; encode it before appending")
        body = json.dumps({"partition": partition,
                           "record": "\\x" + bytes(record).hex()}).encode("utf-8")
        status, _ = self._call("POST", f"{self._rest}/{TABLE}",
                               dict(self._headers(), **{"Content-Type": "application/json",
                                                        "Prefer": "return=minimal"}), body)
        if status != 201:
            raise StorageUnavailable(f"append to {partition!r} refused (HTTP {status})")

    def read(self, partition: str) -> Iterator[bytes]:
        self.require_ready()
        _check_partition(partition)
        records: List[bytes] = []
        after = 0
        while True:
            rows = self._get(f"{self._rest}/{TABLE}?select=seq,record"
                             f"&partition=eq.{quote(partition, safe='')}"
                             f"&seq=gt.{after}&order=seq.asc&limit={PAGE_ROWS}",
                             f"read of {partition!r}")
            for row in rows:
                records.append(_decode(row["record"]))
                after = row["seq"]
            if len(rows) < PAGE_ROWS:
                return iter(records)

    def partitions(self) -> Iterator[str]:
        self.require_ready()
        status, raw = self._call("POST", f"{self._rest}/rpc/{PARTITIONS_FUNCTION}",
                                 dict(self._headers(), **{"Content-Type": "application/json"}),
                                 b"{}")
        if status != 200:
            raise StorageUnavailable(f"partition listing refused (HTTP {status})")
        return iter(_json(raw, "partition listing"))

    # -- HTTP -----------------------------------------------------------------

    def _headers(self) -> Dict[str, str]:
        # As the Supabase clients send it: the key as `apikey`, and as the
        # bearer when there is no user session.
        return {"apikey": self._key, "Authorization": f"Bearer {self._key}",
                "Accept": "application/json"}

    def _get(self, url: str, what: str) -> list:
        status, raw = self._call("GET", url, self._headers(), None)
        if status != 200:
            raise StorageUnavailable(f"{what} refused (HTTP {status})")
        rows = _json(raw, what)
        if not isinstance(rows, list):
            raise StorageUnavailable(f"{what}: unexpected response")
        return rows

    def _call(self, method, url, headers, body) -> Tuple[int, bytes]:
        try:
            return self._transport(method, url, headers, body)
        except StorageUnavailable:
            raise
        except Exception as error:
            raise StorageUnavailable(f"database call failed ({type(error).__name__})") from None


def _check_partition(partition: str) -> None:
    # The local backend's rule, plus the table's length limit.
    if (not isinstance(partition, str) or not partition or "/" in partition
            or "\\" in partition or partition in (".", "..")
            or len(partition) > MAX_PARTITION_CHARS):
        raise ValueError(f"invalid partition name: {partition!r}")


def _decode(value: str) -> bytes:
    if not isinstance(value, str) or not value.startswith("\\x"):
        raise StorageUnavailable("a record came back in an unexpected encoding")
    return bytes.fromhex(value[2:])


def _json(raw: bytes, what: str):
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        raise StorageUnavailable(f"{what}: response is not JSON") from None
