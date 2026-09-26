"""Test support: a test-only authenticator, in-process calls, a live server.

`TokenAuthenticator` lives here, under `tests/`, on purpose. The production
composition ships `NoAuthenticator` until `FS-DP-02` is ratified; no
credential-accepting authenticator exists outside the tests.
"""

from __future__ import annotations

import io
import json
import tempfile
import threading
import urllib.error
import urllib.request
from pathlib import Path
from typing import Mapping, Optional
from wsgiref.simple_server import WSGIRequestHandler, make_server
from wsgiref.util import setup_testing_defaults

from fullstack.backend.api import create_app
from fullstack.backend.security import (
    AUDIT, OBSERVE, RUN_WORKFLOW, Authenticator, Principal)

REPO_ROOT = Path(__file__).resolve().parents[2]

OPERATOR_TOKEN = "test-operator-token-1f4c"
OBSERVER_TOKEN = "test-observer-token-9a2e"


class TokenAuthenticator(Authenticator):
    """Bearer tokens mapped to principals. **Test only.**"""

    mechanism = "test bearer tokens (tests only)"

    def __init__(self, tokens: Mapping[str, Principal]):
        self._tokens = dict(tokens)

    def authenticate(self, headers):
        value = headers.get("authorization", "")
        if not value.startswith("Bearer "):
            return None
        return self._tokens.get(value[len("Bearer "):])


def default_authenticator() -> TokenAuthenticator:
    return TokenAuthenticator({
        OPERATOR_TOKEN: Principal("operator@test", {OBSERVE, RUN_WORKFLOW, AUDIT}),
        OBSERVER_TOKEN: Principal("observer@test", {OBSERVE}),
    })


class Harness:
    """A started application over a temporary data directory."""

    def __init__(self, authenticator: Optional[Authenticator] = None, data_dir=None,
                 **options):
        self._tmp = None
        if data_dir is None:
            self._tmp = tempfile.TemporaryDirectory()
            data_dir = Path(self._tmp.name)
        self.data_dir = Path(data_dir)
        self.app, self.aios = create_app(self.data_dir, REPO_ROOT,
                                         authenticator or default_authenticator(),
                                         **options)

    def close(self):
        self.aios.stop()
        if self._tmp is not None:
            self._tmp.cleanup()

    def call(self, method: str, path: str, token: Optional[str] = None, body=None,
             content_type="application/json", raw: Optional[bytes] = None):
        """Call the WSGI application in-process. Returns (status, headers, payload)."""
        query = ""
        if "?" in path:
            path, query = path.split("?", 1)
        data = raw if raw is not None else (
            json.dumps(body).encode("utf-8") if body is not None else b"")
        environ = {"REQUEST_METHOD": method, "PATH_INFO": path, "QUERY_STRING": query,
                   "CONTENT_LENGTH": str(len(data)), "wsgi.input": io.BytesIO(data)}
        if content_type and data:
            environ["CONTENT_TYPE"] = content_type
        if token is not None:
            environ["HTTP_AUTHORIZATION"] = f"Bearer {token}"
        setup_testing_defaults(environ)
        captured = {}

        def start_response(status, headers):
            captured["status"] = int(status.split()[0])
            captured["headers"] = dict(headers)

        payload = b"".join(self.app(environ, start_response))
        ctype = captured["headers"].get("Content-Type", "")
        parsed = json.loads(payload) if ctype.startswith("application/json") else payload
        return captured["status"], captured["headers"], parsed


class _Quiet(WSGIRequestHandler):
    def log_message(self, *args):
        pass


class LiveServer:
    """The same application behind a real loopback socket, on a free port."""

    def __init__(self, harness: Harness):
        self.harness = harness
        self._server = make_server("127.0.0.1", 0, harness.app, handler_class=_Quiet)
        self.url = f"http://127.0.0.1:{self._server.server_port}"
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()

    def request(self, method, path, token=None, body=None):
        data = json.dumps(body).encode("utf-8") if body is not None else None
        request = urllib.request.Request(self.url + path, data=data, method=method)
        if data is not None:
            request.add_header("Content-Type", "application/json")
        if token:
            request.add_header("Authorization", f"Bearer {token}")
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.status, dict(response.headers), json.loads(response.read())
        except urllib.error.HTTPError as error:
            return error.code, dict(error.headers), json.loads(error.read())

    def close(self):
        self._server.shutdown()
        self._server.server_close()
