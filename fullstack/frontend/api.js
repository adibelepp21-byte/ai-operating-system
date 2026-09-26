// The console's only route to the backend: the API contract v1, same origin.
// The credential is whatever the operator entered; how credentials are issued
// is decided by FS-DP-02, and this client just forwards one if present.

const CREDENTIAL_KEY = "aios.console.credential";

export function createClient({ fetchImpl = globalThis.fetch, storage = null } = {}) {
  const store = storage ?? safeSessionStorage();

  function credential() {
    try {
      return store?.getItem(CREDENTIAL_KEY) ?? "";
    } catch {
      return "";
    }
  }

  async function request(method, path, body) {
    const headers = { Accept: "application/json" };
    const token = credential();
    if (token) headers.Authorization = `Bearer ${token}`;
    const init = { method, headers, credentials: "same-origin" };
    if (body !== undefined) {
      headers["Content-Type"] = "application/json";
      init.body = JSON.stringify(body);
    }
    let response;
    try {
      response = await fetchImpl(`/api/v1${path}`, init);
    } catch {
      return { ok: false, status: 0, body: null };
    }
    let parsed = null;
    try {
      parsed = await response.json();
    } catch {
      parsed = null;
    }
    return { ok: response.ok, status: response.status, body: parsed };
  }

  return {
    get: (path) => request("GET", path),
    post: (path, body) => request("POST", path, body),
    hasCredential: () => credential() !== "",
    setCredential(value) {
      try {
        if (value) store?.setItem(CREDENTIAL_KEY, value);
        else store?.removeItem(CREDENTIAL_KEY);
      } catch {
        /* storage unavailable: the credential lives only for this request */
      }
    },
  };
}

function safeSessionStorage() {
  try {
    return globalThis.sessionStorage ?? null;
  } catch {
    return null;
  }
}
