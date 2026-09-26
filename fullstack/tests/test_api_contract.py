"""The published API contract (FS-02 `§4`) and the running router are the same.

A route added to the code but not to the blueprint, or the reverse, fails
here, and so does a scope that differs between them.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

from fullstack.backend import contract

BLUEPRINT = (Path(__file__).resolve().parents[2]
             / "docs/fullstack/FS-02-FULL-STACK-ARCHITECTURE-BLUEPRINT.md")
ROW = re.compile(r"^\| (GET|POST) \| `([^`]+)` \| `?([a-z.]+)`? \|", re.MULTILINE)


class ContractMatchesBlueprint(unittest.TestCase):
    def test_every_route_and_scope_is_published(self):
        published = {(m, p, s) for m, p, s in ROW.findall(BLUEPRINT.read_text(encoding="utf-8"))}
        served = {(r.method, r.template, r.scope) for r in contract.ROUTES}
        self.assertEqual(served, published)

    def test_every_route_has_a_handler(self):
        from fullstack.backend.api import Application
        for route in contract.ROUTES:
            with self.subTest(route=route.handler):
                self.assertTrue(callable(getattr(Application, "_h_" + route.handler, None)))

    def test_every_error_code_is_named(self):
        self.assertEqual({400, 401, 403, 404, 405, 413, 500, 503}, set(contract.ERRORS))


if __name__ == "__main__":
    unittest.main()
