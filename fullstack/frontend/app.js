// The AIOS console. It renders what the backend reports and asks the backend
// to act; it never decides authority and never reaches AIOS directly.
// Every value from the backend is written with textContent, never as HTML.

import { createClient } from "./api.js";
import {
  SCOPES, classifyError, hasScope, outcomeLabel, runSummary, stateLabel,
  traceRow, validateRunForm,
} from "./model.js";

const client = createClient();
const $ = (selector) => document.querySelector(selector);
const state = { session: null, traceOffset: 0, traceLimit: 25 };

function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [key, value] of Object.entries(attrs)) {
    if (key === "class") node.className = value;
    else if (key === "dataset") Object.assign(node.dataset, value);
    else if (key === "onclick") node.addEventListener("click", value);
    else node.setAttribute(key, value);
  }
  for (const child of children.flat()) {
    if (child === null || child === undefined) continue;
    node.append(child instanceof Node ? child : document.createTextNode(String(child)));
  }
  return node;
}

function badge(stateName) {
  const { label, tone } = stateLabel(stateName);
  return el("span", { class: `badge tone-${tone}`, "data-state": stateName }, label);
}

function showBanner(error) {
  const banner = $("[data-testid=banner]");
  if (!error) {
    banner.hidden = true;
    banner.textContent = "";
    return;
  }
  banner.hidden = false;
  banner.dataset.kind = error.kind;
  banner.textContent = error.message;
}

function fillTable(testid, rows) {
  const body = $(`[data-testid=${testid}] tbody`);
  body.replaceChildren(...rows);
}

async function load(path) {
  const response = await client.get(path);
  if (!response.ok) {
    showBanner(classifyError(response.status, response.body));
    return null;
  }
  return response.body;
}

// -- health and session -----------------------------------------------------

async function refreshHealth() {
  const response = await client.get("/health");
  const node = $("[data-testid=health]");
  const status = response.ok ? response.body.status : response.status === 0 ? "offline" : "unavailable";
  node.dataset.state = status;
  node.querySelector(".label").textContent = response.ok
    ? `${response.body.status} · runtime ${response.body.runtime_state}`
    : classifyError(response.status, response.body).message;
}

async function refreshSession() {
  const response = await client.get("/session");
  state.session = response.ok ? response.body : null;
  const info = $("[data-testid=session-info]");
  if (response.ok) {
    info.replaceChildren(el("p", {}, "Signed in as ", el("strong", { "data-testid": "session-subject" }, response.body.subject)),
      el("p", {}, "Scopes: ", el("code", { "data-testid": "session-scopes" }, response.body.scopes.join(", ") || "none")));
  } else {
    info.replaceChildren(el("p", { "data-testid": "session-subject", class: "muted" },
      classifyError(response.status, response.body).message));
  }
  $("[data-testid=run-submit]").disabled = !hasScope(state.session, SCOPES.RUN_WORKFLOW);
}

// -- views ------------------------------------------------------------------

async function renderOverview() {
  const [runtime, runs] = await Promise.all([load("/runtime"), load("/runs")]);
  if (!runtime || !runs) return;
  const summary = runSummary(runs.runs);
  const card = (k, v, id) => el("div", { class: "card", "data-testid": id }, el("div", { class: "k" }, k), el("div", { class: "v" }, v));
  $("[data-testid=overview-cards]").replaceChildren(
    card("Runtime", runtime.state, "card-runtime-state"),
    card("Runtime identity", runtime.runtime_id, "card-runtime-id"),
    card("Hosted", Object.entries(runtime.hosted).filter(([, v]) => v).map(([k]) => k).join(", "), "card-hosted"),
    card("Runs", `${summary.total} · ${summary.succeeded} ok · ${summary.failed} failed`, "card-runs"),
    card("Authentication", runtime.authentication, "card-auth"),
  );
  const last = summary.last;
  $("[data-testid=overview-last-run]").replaceChildren(last
    ? el("span", {}, `${last.run_id} · ${last.workflow.key} · `, badge(last.state), ` · ${outcomeLabel(last)}`)
    : "No runs yet.");
}

async function renderWorkflows() {
  const [catalog, runs] = await Promise.all([load("/workflows"), load("/runs")]);
  if (!catalog || !runs) return;
  const select = $("[data-testid=run-workflow]");
  select.replaceChildren(...catalog.workflows.map((w) => el("option", { value: w.key }, `${w.title} (v${w.version})`)));
  $("[data-testid=catalog]").replaceChildren(...catalog.workflows.map((w) =>
    el("div", { class: "panel" }, el("strong", {}, w.title), el("span", { class: "muted" }, w.description),
      el("ol", {}, w.steps.map((s) => el("li", {}, `${s.step_key} — ${s.actor} · ${s.skill}`))))));
  fillTable("runs-table", runs.runs.map((run) =>
    el("tr", { class: "clickable", "data-run": run.run_id, onclick: () => renderRunDetail(run.run_id) },
      el("td", {}, run.run_id), el("td", {}, run.workflow.key), el("td", {}, badge(run.state)),
      el("td", {}, outcomeLabel(run)), el("td", {}, run.requested_by), el("td", {}, run.completed_at))));
}

function runView(run) {
  return el("div", { class: "panel", "data-testid": "run-view", "data-run": run.run_id },
    el("h2", {}, `${run.run_id} `, badge(run.state)),
    el("p", {}, "States: ", el("code", { "data-testid": "run-states" }, run.states.join(" → "))),
    run.failure_reason ? el("p", { "data-testid": "run-failure", class: "tone-bad" }, run.failure_reason) : null,
    el("p", { "data-testid": "run-outcome" }, "Outcome: ", outcomeLabel(run)),
    el("ul", { class: "steps" }, run.steps.map((step) => el("li", { "data-step": step.step_key },
      el("strong", {}, step.step_key), ` — ${step.actor} · ${step.skill} · `,
      el("span", { class: `badge tone-${step.status === "completed" ? "good" : step.status === "failed" ? "bad" : "neutral"}` }, step.status),
      step.reason ? el("div", { class: "muted" }, step.reason) : null,
      step.criteria ? el("ul", {}, step.criteria.map((c) => el("li", {}, `${c.satisfied ? "✓" : "✗"} ${c.required_text}`))) : null))),
    el("p", { class: "muted" }, `Trace records ${run.trace.from}–${run.trace.to - 1} (${run.trace.count}) · runtime ${run.runtime_id}`));
}

async function renderRunDetail(runId) {
  const run = await load(`/runs/${encodeURIComponent(runId)}`);
  if (run) $("[data-testid=run-detail]").replaceChildren(runView(run));
}

async function submitRun(event) {
  event.preventDefault();
  const form = event.currentTarget;
  const checked = validateRunForm(form.document.value, form.criteria.value);
  const errors = $("[data-testid=run-errors]");
  errors.replaceChildren(...checked.errors.map((e) => el("li", {}, e)));
  if (!checked.ok) return;
  const button = $("[data-testid=run-submit]");
  button.disabled = true;
  const response = await client.post("/runs", { workflow: form.workflow.value, inputs: checked.inputs });
  button.disabled = !hasScope(state.session, SCOPES.RUN_WORKFLOW);
  if (!response.ok) {
    const error = classifyError(response.status, response.body);
    errors.replaceChildren(el("li", { "data-testid": "run-refused" }, error.message));
    return;
  }
  showBanner(null);
  $("[data-testid=run-result]").replaceChildren(runView(response.body));
  await renderWorkflows();
}

async function renderTools() {
  const [tools, ledger] = await Promise.all([load("/tools"), load("/tools/invocations")]);
  if (!tools || !ledger) return;
  fillTable("tools-table", tools.tools.map((t) => el("tr", { "data-tool": t.key },
    el("td", {}, t.key), el("td", {}, t.version), el("td", {}, t.state), el("td", {}, t.actions.join(", ")),
    el("td", {}, t.metadata.effect ?? "—"))));
  fillTable("invocations-table", ledger.invocations.map((r) => el("tr", {},
    el("td", {}, r.tool_key), el("td", {}, r.caller), el("td", {}, r.governance_admitted ? "yes" : "no"),
    el("td", {}, r.execution_attempted ? "yes" : "no"), el("td", {}, r.disposition), el("td", {}, r.reason ?? "—"))));
}

async function renderTraces() {
  const page = await load(`/traces?offset=${state.traceOffset}&limit=${state.traceLimit}`);
  if (!page) return;
  fillTable("traces-table", page.records.map((record) => {
    const row = traceRow(record);
    return el("tr", { "data-position": row.position }, el("td", {}, row.position), el("td", {}, row.actor),
      el("td", {}, el("span", { class: `badge tone-${row.status === "success" ? "good" : "bad"}` }, row.status)),
      el("td", {}, row.tools), el("td", {}, row.skills), el("td", {}, row.runtime));
  }));
  const last = Math.min(page.offset + page.limit, page.total);
  $("[data-testid=traces-range]").textContent = page.total ? `${page.offset + 1}–${last} of ${page.total}` : "none";
  $("[data-testid=traces-prev]").disabled = page.offset === 0;
  $("[data-testid=traces-next]").disabled = last >= page.total;
}

async function renderAudit() {
  const page = await load("/audit?offset=0&limit=200");
  if (!page) return;
  fillTable("audit-table", page.entries.map((e) => el("tr", {},
    el("td", {}, e.position), el("td", {}, e.at), el("td", {}, e.subject ?? "—"), el("td", {}, e.method),
    el("td", {}, e.path), el("td", {}, e.scope), el("td", { class: e.decision === "allowed" ? "tone-good" : "tone-bad" }, e.decision))));
}

// Content a view rendered belongs to the principal it was rendered for. It is
// cleared before every render and whenever the credential changes, so a
// refusal never leaves an earlier principal's data on screen.
const DYNAMIC = ["overview-cards", "overview-last-run", "catalog", "run-result", "run-detail",
                 "traces-range", "session-info"];

function clearViews() {
  for (const body of document.querySelectorAll("main table tbody")) body.replaceChildren();
  for (const id of DYNAMIC) $(`[data-testid=${id}]`).replaceChildren();
}

const VIEWS = { overview: renderOverview, workflows: renderWorkflows, tools: renderTools,
                traces: renderTraces, audit: renderAudit, session: refreshSession };

async function show(view) {
  for (const button of document.querySelectorAll(".sidebar button")) {
    button.classList.toggle("active", button.dataset.view === view);
  }
  for (const name of Object.keys(VIEWS)) $(`#view-${name}`).hidden = name !== view;
  showBanner(null);
  clearViews();
  await VIEWS[view]();
}

function wire() {
  for (const button of document.querySelectorAll(".sidebar button")) {
    button.addEventListener("click", () => show(button.dataset.view));
  }
  $("[data-testid=run-form]").addEventListener("submit", submitRun);
  $("[data-testid=credential-form]").addEventListener("submit", async (event) => {
    event.preventDefault();
    client.setCredential(event.currentTarget.credential.value.trim());
    event.currentTarget.credential.value = "";
    clearViews();
    await refreshSession();
    await show("overview");
  });
  $("[data-testid=credential-clear]").addEventListener("click", async () => {
    client.setCredential("");
    clearViews();
    await refreshSession();
  });
  $("[data-testid=traces-prev]").addEventListener("click", () => {
    state.traceOffset = Math.max(0, state.traceOffset - state.traceLimit);
    renderTraces();
  });
  $("[data-testid=traces-next]").addEventListener("click", () => {
    state.traceOffset += state.traceLimit;
    renderTraces();
  });
}

async function boot() {
  wire();
  await refreshHealth();
  await refreshSession();
  await show(client.hasCredential() ? "overview" : "session");
  document.body.dataset.ready = "true";
}

boot();
