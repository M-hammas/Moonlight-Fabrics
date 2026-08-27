const RAW_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000/api";
const BASE = RAW_BASE.replace(/\/$/, "");
const TOKEN_KEY = "sidra-fabrics_access_token";

async function request(path, options = {}) {
  const token = localStorage.getItem(TOKEN_KEY);
  const headers = { ...(options.body ? { "Content-Type": "application/json" } : {}), ...(options.headers || {}) };
  if (token) headers.Authorization = `Bearer ${token}`;

  let response;
  try {
    response = await fetch(`${BASE}${path}`, { ...options, headers });
  } catch {
    throw new Error("Unable to connect to Sidra Fabrics server. Start the backend on port 8000, or use Docker Compose.");
  }

  const text = await response.text();
  let data = null;
  try { data = text ? JSON.parse(text) : null; } catch { data = { detail: text }; }

  if (response.status === 401) {
    window.dispatchEvent(new Event("sidra-auth-expired"));
  }
  if (!response.ok) {
    const detail = data?.detail || data?.message || `Request failed (${response.status})`;
    throw new Error(typeof detail === "string" ? detail : "Request failed");
  }
  return data;
}

export const api = {
  get: (path, options = {}) => request(path, { ...options, method: "GET" }),
  post: (path, body, options = {}) => request(path, { ...options, method: "POST", body: JSON.stringify(body) }),
  put: (path, body, options = {}) => request(path, { ...options, method: "PUT", body: JSON.stringify(body) }),
  patch: (path, body, options = {}) => request(path, { ...options, method: "PATCH", body: JSON.stringify(body) }),
  delete: (path, options = {}) => request(path, { ...options, method: "DELETE" }),
};

export default api;
