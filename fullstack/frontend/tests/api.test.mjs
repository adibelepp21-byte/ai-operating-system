import { test } from "node:test";
import assert from "node:assert/strict";
import { createClient } from "../api.js";

function memoryStorage() {
  const map = new Map();
  return { getItem: (k) => map.get(k) ?? null, setItem: (k, v) => map.set(k, v), removeItem: (k) => map.delete(k) };
}

function recordingFetch(status = 200, body = { ok: true }) {
  const calls = [];
  const fetchImpl = async (url, init) => {
    calls.push({ url, init });
    return { ok: status < 400, status, json: async () => body };
  };
  return { calls, fetchImpl };
}

test("requests go to the v1 API on the same origin", async () => {
  const { calls, fetchImpl } = recordingFetch();
  const client = createClient({ fetchImpl, storage: memoryStorage() });
  await client.get("/runtime");
  assert.equal(calls[0].url, "/api/v1/runtime");
  assert.equal(calls[0].init.credentials, "same-origin");
  assert.equal(calls[0].init.headers.Authorization, undefined);
});

test("a credential, when set, is forwarded and can be cleared", async () => {
  const { calls, fetchImpl } = recordingFetch();
  const client = createClient({ fetchImpl, storage: memoryStorage() });
  client.setCredential("abc");
  assert.equal(client.hasCredential(), true);
  await client.post("/runs", { workflow: "w" });
  assert.equal(calls[0].init.headers.Authorization, "Bearer abc");
  assert.equal(calls[0].init.headers["Content-Type"], "application/json");
  assert.equal(calls[0].init.body, JSON.stringify({ workflow: "w" }));
  client.setCredential("");
  assert.equal(client.hasCredential(), false);
});

test("refusals are returned, not thrown", async () => {
  const { fetchImpl } = recordingFetch(403, { error: "forbidden", detail: "scope aios.audit is required" });
  const response = await createClient({ fetchImpl, storage: memoryStorage() }).get("/audit");
  assert.deepEqual(response, { ok: false, status: 403, body: { error: "forbidden", detail: "scope aios.audit is required" } });
});

test("an unreachable backend is status 0", async () => {
  const client = createClient({ fetchImpl: async () => { throw new TypeError("network"); }, storage: memoryStorage() });
  assert.deepEqual(await client.get("/health"), { ok: false, status: 0, body: null });
});

test("a body that is not JSON does not break the client", async () => {
  const fetchImpl = async () => ({ ok: false, status: 502, json: async () => { throw new SyntaxError("html"); } });
  assert.deepEqual(await createClient({ fetchImpl, storage: memoryStorage() }).get("/health"),
                   { ok: false, status: 502, body: null });
});
