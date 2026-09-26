// FS-07 — the console in a real browser, against a live backend over a socket.
//
// Run by fullstack/tests/test_integration.py, which starts the server and
// passes: AIOS_E2E_URL, AIOS_E2E_OPERATOR, AIOS_E2E_OBSERVER, PLAYWRIGHT_PATH,
// and optionally AIOS_E2E_ARTIFACTS (a directory for screenshots).
// Prints one JSON line per check; exits non-zero on the first failure.

import { createRequire } from "node:module";
import assert from "node:assert/strict";
import path from "node:path";

const require = createRequire(import.meta.url);
const { chromium } = require(process.env.PLAYWRIGHT_PATH);
const url = process.env.AIOS_E2E_URL;
const operator = process.env.AIOS_E2E_OPERATOR;
const observer = process.env.AIOS_E2E_OBSERVER;
const artifacts = process.env.AIOS_E2E_ARTIFACTS;
const DOC = "docs/architecture/AIOS_ARCHITECTURE_FREEZE_v1.0.md";

const tid = (id) => `[data-testid="${id}"]`;
const report = (check, detail = {}) => console.log(JSON.stringify({ check, ok: true, ...detail }));

async function shot(page, name) {
  if (artifacts) await page.screenshot({ path: path.join(artifacts, `${name}.png`), fullPage: true });
}

async function signIn(page, token) {
  await page.click('.sidebar button[data-view="session"]');
  await page.fill(tid("credential"), token);
  await page.click(tid("credential-save"));
  await page.waitForSelector(`${tid("view-overview")}:not([hidden])`);
}

async function startRun(page, document, criteria) {
  await page.click('.sidebar button[data-view="workflows"]');
  await page.waitForSelector(`${tid("run-workflow")} option`, { state: "attached" });
  await page.fill(tid("run-document"), document);
  await page.fill(tid("run-criteria"), criteria.join("\n"));
  const current = page.locator(`${tid("run-result")} ${tid("run-view")}`);
  const before = (await current.count()) ? await current.getAttribute("data-run") : null;
  await page.click(tid("run-submit"));
  await page.waitForFunction(
    ([sel, prev]) => { const n = document.querySelector(sel); return n && n.dataset.run !== prev; },
    [`${tid("run-result")} ${tid("run-view")}`, before]);
  return page.locator(`${tid("run-result")} ${tid("run-view")}`);
}

const browser = await chromium.launch();
const problems = [];
try {
  const page = await browser.newPage();
  page.on("pageerror", (e) => problems.push(`pageerror: ${e.message}`));
  page.on("console", (m) => { if (m.type() === "error") problems.push(`console: ${m.text()}`); });
  page.on("dialog", async (d) => { problems.push(`dialog: ${d.message()}`); await d.dismiss(); });

  await page.goto(url);
  await page.waitForSelector('body[data-ready="true"]');
  assert.match(await page.textContent(`${tid("health")} .label`), /ok · runtime running/);
  assert.match(await page.textContent(tid("session-subject")), /Not signed in/);
  report("unauthenticated console shows health and asks for sign-in");

  await signIn(page, operator);
  await page.waitForSelector(tid("card-runtime-state"));
  assert.equal((await page.textContent(`${tid("card-runtime-state")} .v`)).trim(), "running");
  report("overview reflects the live Runtime");
  await shot(page, "01-overview");

  // Scenario B — User → Start Workflow → Backend → Workflow → Runtime → Execution → Tool → Result → Frontend
  const ok = await startRun(page, DOC, ["INV-4", "Architect Reserved"]);
  assert.equal(await ok.locator(tid("run-states")).textContent(), "defined → ready → running → succeeded");
  assert.match(await ok.locator(tid("run-outcome")).textContent(), /Conformant \(2\/2\)/);
  report("scenario B: a workflow run succeeds end to end", { run: await ok.getAttribute("data-run") });
  await shot(page, "02-run-succeeded");

  // Scenario C — Execution failure → Runtime → Trace → Backend → Frontend → meaningful state
  const failed = await startRun(page, "docs/absent.md", ["INV-4"]);
  assert.equal(await failed.locator(tid("run-states")).textContent(), "defined → ready → running → failed");
  assert.match(await failed.locator(tid("run-failure")).textContent(), /docs\.read execution_failure/);
  report("scenario C: a tool failure is shown as a failed run with its reason");
  await shot(page, "03-run-failed");

  // Untrusted text is rendered as text, never as markup.
  const hostile = '<img src=x onerror="alert(1)">';
  const xss = await startRun(page, DOC, [hostile]);
  assert.ok((await xss.textContent()).includes(hostile));
  assert.equal(await page.locator(`${tid("run-result")} img`).count(), 0);
  report("user-supplied text is rendered inertly");

  await page.waitForFunction((sel) => document.querySelectorAll(sel).length === 3, `${tid("runs-table")} tbody tr`);
  await page.click(`${tid("runs-table")} tbody tr[data-run="run-00001"]`);
  await page.waitForSelector(`${tid("run-detail")} ${tid("run-view")}[data-run="run-00001"]`);
  report("runs are listed and open in detail");

  await page.click('.sidebar button[data-view="tools"]');
  await page.waitForSelector(`${tid("tools-table")} tr[data-tool="docs.read"]`);
  const dispositions = await page.$$eval(`${tid("invocations-table")} tbody tr td:nth-child(5)`, (c) => c.map((n) => n.textContent));
  assert.deepEqual(dispositions, ["success", "execution_failure", "success"]);
  report("tools and the governance ledger are visible", { dispositions });

  await page.click('.sidebar button[data-view="traces"]');
  await page.waitForFunction((sel) => document.querySelectorAll(sel).length === 8, `${tid("traces-table")} tbody tr`);
  const actors = await page.$$eval(`${tid("traces-table")} tbody tr td:nth-child(2)`, (c) => c.map((n) => n.textContent));
  assert.deepEqual(actors.slice(0, 3), ["tool-proposing-agent", "engineering-intelligence-agent", "workflow-participating-agent"]);
  report("traces show every agent action", { count: actors.length });
  await shot(page, "04-traces");

  await page.click('.sidebar button[data-view="audit"]');
  await page.waitForSelector(`${tid("audit-table")} tbody tr`);
  report("the audit view lists access decisions");

  // Least privilege, and the frontend is not the authority.
  await page.click('.sidebar button[data-view="session"]');
  await page.click(tid("credential-clear"));
  await signIn(page, observer);
  await page.click('.sidebar button[data-view="session"]');
  assert.equal(await page.textContent(tid("session-scopes")), "aios.observe");
  await page.click('.sidebar button[data-view="workflows"]');
  assert.equal(await page.isDisabled(tid("run-submit")), true);
  await page.$eval(tid("run-submit"), (b) => { b.disabled = false; });   // bypass the UI
  await page.fill(tid("run-document"), DOC);
  await page.fill(tid("run-criteria"), "INV-4");
  await page.click(tid("run-submit"));
  await page.waitForSelector(tid("run-refused"));
  assert.match(await page.textContent(tid("run-refused")), /scope aios\.workflow\.run is required/);
  report("an observer cannot run a workflow even with the UI bypassed");

  await page.click('.sidebar button[data-view="audit"]');
  await page.waitForSelector(`${tid("banner")}:not([hidden])`);
  assert.match(await page.textContent(tid("banner")), /scope aios\.audit is required/);
  report("the audit view is refused to an observer, and says why");
  await shot(page, "05-observer-refused");

  // Only the deliberate refusals may appear as console errors (failed fetches log nothing in Chromium,
  // but a 4xx response is reported by the browser as a resource error).
  const unexpected = problems.filter((p) => !/Failed to load resource: the server responded with a status of (403|401)/.test(p));
  assert.deepEqual(unexpected, []);
  report("no script error, CSP violation or dialog occurred");
} finally {
  await browser.close();
}
