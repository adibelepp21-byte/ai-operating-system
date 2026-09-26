// Pure presentation logic for the AIOS console. No DOM, no network: this is
// what `node --test` exercises. The console decides nothing about authority;
// these helpers only describe what the backend already decided.

export const SCOPES = Object.freeze({
  OBSERVE: "aios.observe",
  RUN_WORKFLOW: "aios.workflow.run",
  AUDIT: "aios.audit",
});

export const MAX_CRITERIA = 20;
export const MAX_CRITERION_CHARS = 200;

const STATES = {
  defined: { label: "Defined", tone: "neutral" },
  ready: { label: "Ready", tone: "neutral" },
  running: { label: "Running", tone: "active" },
  succeeded: { label: "Succeeded", tone: "good" },
  failed: { label: "Failed", tone: "bad" },
};

export function stateLabel(state) {
  return STATES[state] ?? { label: String(state ?? "unknown"), tone: "neutral" };
}

// Map a failed response to what the operator should be told. The backend's
// own `detail` is shown verbatim; nothing is inferred beyond the status.
export function classifyError(status, body) {
  const detail = body && typeof body.detail === "string" ? body.detail : "";
  switch (status) {
    case 0:
      return { kind: "offline", message: "The backend is unreachable." };
    case 401:
      return { kind: "unauthenticated",
               message: "Not signed in. Every AIOS view needs an authenticated principal." };
    case 403:
      return { kind: "forbidden", message: detail || "Your principal lacks the required scope." };
    case 503:
      return { kind: "unavailable", message: detail || "The AIOS Runtime is not running." };
    case 400:
    case 404:
    case 413:
      return { kind: "invalid", message: detail || "The request was refused." };
    default:
      return { kind: "error", message: detail || `Request failed (${status}).` };
  }
}

export function hasScope(session, scope) {
  return Boolean(session && Array.isArray(session.scopes) && session.scopes.includes(scope));
}

export function parseCriteria(text) {
  return String(text ?? "")
    .split("\n")
    .map((line) => line.trim())
    .filter((line) => line.length > 0);
}

// Mirrors the backend's input contract so the operator sees problems before
// sending. The backend validates again and is the one that decides.
export function validateRunForm(document, criteriaText) {
  const errors = [];
  const path = String(document ?? "").trim();
  const criteria = parseCriteria(criteriaText);
  if (!path) errors.push("Name a document under docs/.");
  else if (!path.startsWith("docs/")) errors.push("The document must lie under docs/.");
  if (criteria.length === 0) errors.push("State at least one criterion.");
  if (criteria.length > MAX_CRITERIA) errors.push(`At most ${MAX_CRITERIA} criteria.`);
  if (criteria.some((c) => c.length > MAX_CRITERION_CHARS)) {
    errors.push(`Each criterion is at most ${MAX_CRITERION_CHARS} characters.`);
  }
  return { ok: errors.length === 0, errors, inputs: { document: path, criteria } };
}

export function runSummary(runs) {
  const list = Array.isArray(runs) ? runs : [];
  const succeeded = list.filter((r) => r.state === "succeeded").length;
  const failed = list.filter((r) => r.state === "failed").length;
  return { total: list.length, succeeded, failed, last: list[0] ?? null };
}

export function outcomeLabel(run) {
  if (!run) return "—";
  if (run.state === "failed") return "Failed";
  if (!run.outcome) return "—";
  const { satisfied, total, conformant } = run.outcome;
  return `${conformant ? "Conformant" : "Not conformant"} (${satisfied}/${total})`;
}

export function traceRow(record) {
  return {
    position: record.position,
    actor: record.agent_instance,
    status: record.status,
    runtime: record.runtime,
    tools: (record.tools_used ?? []).join(", ") || "—",
    skills: (record.skills_used ?? []).join(", ") || "—",
  };
}
