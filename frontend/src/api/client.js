const BASE_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`API error ${res.status}: ${body}`);
  }
  return res.json();
}

export const api = {
  listInteractions: () => request("/api/interactions"),
  createInteraction: (payload) =>
    request("/api/interactions", { method: "POST", body: JSON.stringify(payload) }),
  updateInteraction: (id, payload) =>
    request(`/api/interactions/${id}`, { method: "PATCH", body: JSON.stringify(payload) }),
  sendChatMessage: (message, interactionId) =>
    request("/api/chat", {
      method: "POST",
      body: JSON.stringify({ message, interaction_id: interactionId || null }),
    }),
};
