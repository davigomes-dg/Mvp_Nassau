/**
 * Clientes HTTP para os dois serviços locais do MVP:
 * Flask (conta e perfil com SQLite) e FastAPI (catálogo e simulação de cursos).
 */
export const API_BASE_URL = "http://127.0.0.1:5000/api";
export const SIMULATOR_BASE_URL = "http://127.0.0.1:8000";

async function requestFrom(baseUrl, endpoint, options, serviceName) {
  const customHeaders = options.headers || {};
  const fetchOptions = { ...options };
  delete fetchOptions.headers;

  let response;
  try {
    response = await fetch(baseUrl + endpoint, {
      ...fetchOptions,
      headers: {
        "Content-Type": "application/json",
        ...customHeaders,
      },
    });
  } catch (_error) {
    throw new Error("Não foi possível conectar a " + serviceName + ". Confira se o serviço está iniciado.");
  }

  const contentType = response.headers.get("content-type") || "";
  let payload = null;
  if (contentType.includes("application/json")) {
    payload = await response.json();
  }

  if (!response.ok) {
    const rawMessage = payload?.error || payload?.detail || ("Erro HTTP " + response.status);
    const message = Array.isArray(rawMessage)
      ? rawMessage.map((item) => typeof item === "object" ? item.msg : item).filter(Boolean).join(" ")
      : rawMessage;
    const error = new Error(message);
    error.status = response.status;
    error.details = payload?.details || (Array.isArray(payload?.detail) ? payload.detail : null);
    throw error;
  }

  return payload;
}

export function apiRequest(endpoint, options = {}) {
  return requestFrom(API_BASE_URL, endpoint, options, "a API de perfil");
}

export function simulatorRequest(endpoint, options = {}) {
  return requestFrom(SIMULATOR_BASE_URL, endpoint, options, "a API de cursos");
}

export function checkApi() {
  return apiRequest("/health", { method: "GET" });
}

export function getCourses() {
  return simulatorRequest("/cursos", { method: "GET" });
}

export function simulateCourses(payload) {
  return simulatorRequest("/simular", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
