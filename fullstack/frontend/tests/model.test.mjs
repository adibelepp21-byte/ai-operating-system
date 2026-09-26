import { test } from "node:test";
import assert from "node:assert/strict";
import {
  SCOPES, classifyError, hasScope, outcomeLabel, parseCriteria, runSummary,
  stateLabel, traceRow, validateRunForm,
} from "../model.js";

test("every lifecycle state has a label and a tone", () => {
  assert.deepEqual(stateLabel("succeeded"), { label: "Succeeded", tone: "good" });
  assert.deepEqual(stateLabel("failed"), { label: "Failed", tone: "bad" });
  assert.deepEqual(stateLabel("running"), { label: "Running", tone: "active" });
  assert.equal(stateLabel("mystery").tone, "neutral");
});

test("errors are described from the status, with the backend's own detail", () => {
  assert.equal(classifyError(0, null).kind, "offline");
  assert.equal(classifyError(401, {}).kind, "unauthenticated");
  assert.equal(classifyError(403, { detail: "scope aios.audit is required" }).message,
               "scope aios.audit is required");
  assert.equal(classifyError(503, {}).kind, "unavailable");
  assert.equal(classifyError(400, { detail: "bad" }).message, "bad");
  assert.equal(classifyError(500, null).kind, "error");
});

test("scopes are read, never assumed", () => {
  assert.equal(hasScope(null, SCOPES.OBSERVE), false);
  assert.equal(hasScope({ scopes: [SCOPES.OBSERVE] }, SCOPES.RUN_WORKFLOW), false);
  assert.equal(hasScope({ scopes: [SCOPES.RUN_WORKFLOW] }, SCOPES.RUN_WORKFLOW), true);
});

test("criteria are one per line, blanks dropped", () => {
  assert.deepEqual(parseCriteria(" INV-4 \n\n  Architect Reserved\n"), ["INV-4", "Architect Reserved"]);
  assert.deepEqual(parseCriteria(undefined), []);
});

test("the run form mirrors the backend's input contract", () => {
  assert.equal(validateRunForm("docs/a.md", "x").ok, true);
  assert.deepEqual(validateRunForm("docs/a.md", "x").inputs, { document: "docs/a.md", criteria: ["x"] });
  assert.equal(validateRunForm("", "x").ok, false);
  assert.equal(validateRunForm("README.md", "x").ok, false);
  assert.equal(validateRunForm("docs/a.md", "").ok, false);
  assert.equal(validateRunForm("docs/a.md", Array(21).fill("x").join("\n")).ok, false);
  assert.equal(validateRunForm("docs/a.md", "y".repeat(201)).ok, false);
});

test("run summaries count terminal states", () => {
  const runs = [{ state: "failed" }, { state: "succeeded" }, { state: "succeeded" }];
  assert.deepEqual(runSummary(runs), { total: 3, succeeded: 2, failed: 1, last: runs[0] });
  assert.deepEqual(runSummary(undefined), { total: 0, succeeded: 0, failed: 0, last: null });
});

test("outcomes say what was verified", () => {
  assert.equal(outcomeLabel({ state: "succeeded", outcome: { conformant: true, satisfied: 2, total: 2 } }),
               "Conformant (2/2)");
  assert.equal(outcomeLabel({ state: "succeeded", outcome: { conformant: false, satisfied: 1, total: 2 } }),
               "Not conformant (1/2)");
  assert.equal(outcomeLabel({ state: "failed", outcome: null }), "Failed");
});

test("a trace row carries the actor and what it used", () => {
  const row = traceRow({ position: 4, agent_instance: "tool-proposing-agent", status: "success",
                         runtime: "r", tools_used: ["docs.read"], skills_used: [] });
  assert.deepEqual(row, { position: 4, actor: "tool-proposing-agent", status: "success",
                          runtime: "r", tools: "docs.read", skills: "—" });
});
