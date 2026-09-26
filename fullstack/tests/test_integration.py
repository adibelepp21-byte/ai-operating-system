"""FS-05 / FS-07 — the frontend and the full stack as one system.

* Frontend unit tests: `node --test` over `fullstack/frontend/tests/`.
* Scenarios B and C over a real loopback socket.
* The console in Chromium, driven by Playwright (`e2e/console.e2e.mjs`).

The browser test needs Node.js and Playwright. Where either is missing it is
skipped and says so; the recorded evidence names the environment it ran in.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from fullstack.tests.support import (
    OBSERVER_TOKEN, OPERATOR_TOKEN, REPO_ROOT, Harness, LiveServer)
from fullstack.tests.test_backend_api import RUN, run_body

NODE = shutil.which("node")
FRONTEND_TESTS = sorted((REPO_ROOT / "fullstack/frontend/tests").glob("*.test.mjs"))
E2E = REPO_ROOT / "fullstack/tests/e2e/console.e2e.mjs"


def _playwright() -> str:
    if not NODE:
        return ""
    npm = shutil.which("npm")
    if not npm:
        return ""
    root = subprocess.run([npm, "root", "-g"], capture_output=True, text=True).stdout.strip()
    candidate = Path(root) / "playwright"
    return str(candidate) if candidate.is_dir() else ""


@unittest.skipUnless(NODE, "Node.js is not available")
class FrontendUnits(unittest.TestCase):
    def test_the_frontend_modules_pass_their_tests(self):
        done = subprocess.run([NODE, "--test", *map(str, FRONTEND_TESTS)],
                              capture_output=True, text=True, cwd=str(REPO_ROOT), timeout=120)
        self.assertEqual(0, done.returncode, done.stdout[-2000:] + done.stderr[-2000:])
        self.assertIn("# fail 0", done.stdout)


class OverTheWire(unittest.TestCase):
    """Scenarios B and C through a real socket, as an external client sees them."""

    def setUp(self):
        self.h = Harness()
        self.server = LiveServer(self.h)

    def tearDown(self):
        self.server.close()
        self.h.close()

    def test_scenario_b_and_c(self):
        status, headers, run = self.server.request("POST", RUN, OPERATOR_TOKEN, run_body())
        self.assertEqual((201, "succeeded"), (status, run["state"]))
        self.assertEqual("nosniff", headers["X-Content-Type-Options"])
        status, _, failed = self.server.request("POST", RUN, OPERATOR_TOKEN,
                                                run_body(document="docs/absent.md"))
        self.assertEqual((201, "failed"), (status, failed["state"]))
        listed = self.server.request("GET", RUN, OBSERVER_TOKEN)[2]["runs"]
        self.assertEqual([failed["run_id"], run["run_id"]], [r["run_id"] for r in listed])
        traces = self.server.request("GET", "/api/v1/traces", OBSERVER_TOKEN)[2]
        self.assertEqual(5, traces["total"])

    def test_refusals_over_the_wire(self):
        self.assertEqual(401, self.server.request("GET", RUN)[0])
        self.assertEqual(403, self.server.request("POST", RUN, OBSERVER_TOKEN, run_body())[0])


PLAYWRIGHT = _playwright()


@unittest.skipUnless(PLAYWRIGHT, "Playwright for Node.js is not available")
class ConsoleInABrowser(unittest.TestCase):
    def test_the_console_end_to_end(self):
        h = Harness()
        server = LiveServer(h)
        artifacts = os.environ.get("AIOS_E2E_ARTIFACTS") or tempfile.mkdtemp()
        try:
            env = dict(os.environ, AIOS_E2E_URL=server.url, AIOS_E2E_OPERATOR=OPERATOR_TOKEN,
                       AIOS_E2E_OBSERVER=OBSERVER_TOKEN, PLAYWRIGHT_PATH=PLAYWRIGHT,
                       AIOS_E2E_ARTIFACTS=artifacts)
            done = subprocess.run([NODE, str(E2E)], capture_output=True, text=True,
                                  env=env, timeout=240)
        finally:
            server.close()
            h.close()
        self.assertEqual(0, done.returncode, done.stdout[-3000:] + done.stderr[-3000:])
        checks = [json.loads(line) for line in done.stdout.splitlines() if line.startswith("{")]
        self.assertEqual(12, len(checks), done.stdout)
        self.assertTrue(all(c["ok"] for c in checks))


if __name__ == "__main__":
    unittest.main()
