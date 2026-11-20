/**
 * Cliente HTTP centralizado para comunicação com a API Flask.
 * Ajuste a URL caso o endereço/porta do back-end seja alterado.
 */
export const API_BASE_URL = "http://127.0.0.1:5000/api";

export async function apiRequest(endpoint, options = {}) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });

  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json")
    ? await response.json()
    : null;

  if (!response.ok) {
    const error = new Error(payload?.error || `Erro HTTP ${response.status}`);
    error.status = response.status;
    error.details = payload?.details || null;
    throw error;
  }

  return payload;
}

/** Endpoint simples para verificar a comunicação com o back-end. */
export function checkApi() {
  return apiRequest("/health", { method: "GET" });
}
