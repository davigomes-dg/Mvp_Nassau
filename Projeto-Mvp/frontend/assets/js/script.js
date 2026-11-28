import {
  apiRequest,
  checkApi,
  getCourses,
  simulateCourses,
} from "../../services/api.js";

const TOKEN_KEY = "notaee_access_token";
const authPanel = document.querySelector("#auth-panel");
const profilePanel = document.querySelector("#profile-panel");
const authFeedback = document.querySelector("#auth-feedback");
const profileFeedback = document.querySelector("#profile-feedback");
const simulationFeedback = document.querySelector("#simulation-feedback");
const loginForm = document.querySelector("#login-form");
const registerForm = document.querySelector("#register-form");
const profileForm = document.querySelector("#profile-form");
const simulationSection = document.querySelector("#simulation-section");
const simulationResults = document.querySelector("#simulation-results");
const logoutButton = document.querySelector("#logout-button");
const simulateButton = document.querySelector("#simulate-button");

function showMessage(element, message = "", kind = "") {
  if (!element) return;
  element.textContent = message;
  element.dataset.kind = kind;
}

function setConnectionStatus(elementId, message, state) {
  const element = document.getElementById(elementId);
  if (!element) return;
  element.textContent = message;
  element.dataset.state = state;
}

function messageFor(error) {
  if (error.details && typeof error.details === "object") {
    const details = Object.values(error.details)
      .map((item) => typeof item === "object" ? item.msg : item)
      .filter(Boolean)
      .join(" ");
    if (details) return error.message + " " + details;
  }
  return error.message || "Não foi possível concluir a solicitação.";
}

function setAuthView(view) {
  const isLogin = view === "login";
  loginForm.hidden = !isLogin;
  registerForm.hidden = isLogin;

  document.querySelectorAll("[data-auth-view]").forEach((button) => {
    const selected = button.dataset.authView === view;
    button.classList.toggle("is-active", selected);
    button.setAttribute("aria-selected", String(selected));
  });

  showMessage(authFeedback);
}

function setLoggedIn(user) {
  authPanel.hidden = true;
  profilePanel.hidden = false;
  logoutButton.hidden = false;
  document.querySelector("#welcome-message").textContent =
    "Olá, " + user.name + ".";
}

function setLoggedOut() {
  profilePanel.hidden = true;
  authPanel.hidden = false;
  logoutButton.hidden = true;
  profileForm.reset();
  simulationSection.hidden = true;
  simulationResults.replaceChildren();
}

function fillProfile(profile) {
  const scores = profile?.notas || {};
  const location = profile?.localizacao || {};

  Object.keys(scores).forEach((field) => {
    const input = profileForm.elements.namedItem(field);
    if (input) input.value = scores[field] ?? "";
  });
  Object.keys(location).forEach((field) => {
    const input = profileForm.elements.namedItem(field);
    if (input) input.value = location[field] ?? "";
  });
}

function collectProfilePayload() {
  const data = new FormData(profileForm);
  const score = (field) => {
    const value = String(data.get(field) ?? "").trim();
    if (value === "") return null;
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : null;
  };
  const text = (field) => {
    const value = String(data.get(field) ?? "").trim();
    return value || null;
  };

  return {
    notas: {
      linguagens: score("linguagens"),
      ciencias_humanas: score("ciencias_humanas"),
      ciencias_natureza: score("ciencias_natureza"),
      matematica: score("matematica"),
      redacao: score("redacao"),
    },
    localizacao: {
      cidade: text("cidade"),
      estado: text("estado"),
    },
  };
}

function authHeaders() {
  return {
    Authorization: "Bearer " + localStorage.getItem(TOKEN_KEY),
  };
}

async function openProfile(user) {
  setLoggedIn(user);
  showMessage(profileFeedback, "Carregando seu perfil…");

  try {
    const result = await apiRequest("/profile", {
      method: "GET",
      headers: authHeaders(),
    });
    fillProfile(result.profile);
    showMessage(profileFeedback);
    return true;
  } catch (error) {
    if (error.status === 401) {
      localStorage.removeItem(TOKEN_KEY);
      setLoggedOut();
      setAuthView("login");
      showMessage(authFeedback, "Sua sessão expirou. Entre novamente.", "error");
    } else {
      showMessage(profileFeedback, messageFor(error), "error");
    }
    return false;
  }
}

async function submitAuth(form, endpoint, includeName = false) {
  const submitButton = form.querySelector('button[type="submit"]');
  const data = new FormData(form);
  const payload = {
    email: String(data.get("email") || "").trim(),
    password: data.get("password"),
  };
  if (includeName) payload.name = String(data.get("name") || "").trim();

  submitButton.disabled = true;
  showMessage(authFeedback, "Conectando…");

  try {
    const result = await apiRequest(endpoint, {
      method: "POST",
      body: JSON.stringify(payload),
    });
    localStorage.setItem(TOKEN_KEY, result.access_token);
    form.reset();
    await openProfile(result.user);
  } catch (error) {
    showMessage(authFeedback, messageFor(error), "error");
  } finally {
    submitButton.disabled = false;
  }
}

async function saveProfile() {
  const result = await apiRequest("/profile", {
    method: "PUT",
    headers: authHeaders(),
    body: JSON.stringify(collectProfilePayload()),
  });
  fillProfile(result.profile);
  return result.profile;
}

function formatScore(value) {
  return new Intl.NumberFormat("pt-BR", {
    maximumFractionDigits: 2,
  }).format(Number(value));
}

function renderCourseCatalog(container, courses) {
  if (!container) return;
  container.replaceChildren();

  if (!courses.length) {
    const empty = document.createElement("p");
    empty.className = "muted";
    empty.textContent = "Nenhum curso está cadastrado na API.";
    container.appendChild(empty);
    return;
  }

  courses.forEach((course) => {
    const item = document.createElement("article");
    item.className = "course-item";

    const name = document.createElement("strong");
    name.textContent = course.nome;

    const details = document.createElement("span");
    const cutoff = Number.isFinite(Number(course.nota_corte_referencia))
      ? " · Corte " + formatScore(course.nota_corte_referencia)
      : "";
    details.textContent = (course.turno || "") + cutoff;

    item.append(name, details);
    container.appendChild(item);
  });
}

async function checkProfileService() {
  try {
    await checkApi();
    setConnectionStatus("api-status", "API de perfil online", "online");
  } catch (_error) {
    setConnectionStatus("api-status", "API de perfil indisponível", "offline");
  }
}

async function loadCourses() {
  try {
    const result = await getCourses();
    const courses = Array.isArray(result?.cursos) ? result.cursos : [];
    renderCourseCatalog(document.querySelector("#public-courses-list"), courses);
    renderCourseCatalog(document.querySelector("#courses-list"), courses);
    setConnectionStatus("simulator-status", "API de cursos online", "online");
  } catch (_error) {
    const unavailable = "Inicie a API de cursos para carregar o catálogo.";
    document.querySelectorAll("#public-courses-list, #courses-list").forEach((container) => {
      if (container) {
        container.replaceChildren();
        const message = document.createElement("p");
        message.className = "muted";
        message.textContent = unavailable;
        container.appendChild(message);
      }
    });
    setConnectionStatus("simulator-status", "API de cursos indisponível", "offline");
  }
}

function renderSimulation(result) {
  const summary = document.querySelector("#simulation-summary");
  const unit = result.unidade ? "Unidade: " + result.unidade : "";
  const location = result.local_informado
    ? "Local informado: " + result.local_informado
    : "";
  summary.textContent = [unit, location].filter(Boolean).join(" · ");

  simulationResults.replaceChildren();
  (result.resultados || []).forEach((course) => {
    const card = document.createElement("article");
    card.className = "result-card";

    const name = document.createElement("h3");
    name.textContent = course.curso;

    const score = document.createElement("div");
    score.className = "result-score";
    const scoreValue = document.createElement("strong");
    scoreValue.textContent = formatScore(course.media_ponderada);
    const scoreLabel = document.createElement("span");
    scoreLabel.textContent = "média ponderada";
    score.append(scoreValue, scoreLabel);

    const details = document.createElement("div");
    details.className = "result-detail";
    const cutoff = document.createElement("span");
    cutoff.textContent =
      "Nota de corte de referência: " + formatScore(course.nota_corte_referencia);
    const differenceValue = Number(course.diferenca_pontos);
    const difference = document.createElement("span");
    difference.textContent =
      "Diferença: " +
      (differenceValue > 0 ? "+" : "") +
      formatScore(differenceValue) +
      " pontos";
    details.append(cutoff, difference);

    const badge = document.createElement("span");
    badge.className = "result-badge" + (course.alcanca_corte ? " is-reached" : "");
    badge.textContent = course.alcanca_corte
      ? "Atinge o corte de referência"
      : "Abaixo do corte de referência";

    card.append(name, score, details, badge);
    simulationResults.appendChild(card);
  });

  simulationSection.hidden = false;
  simulationSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

document.querySelectorAll("[data-auth-view]").forEach((button) => {
  button.addEventListener("click", () => setAuthView(button.dataset.authView));
});

loginForm.addEventListener("submit", (event) => {
  event.preventDefault();
  submitAuth(loginForm, "/auth/login");
});

registerForm.addEventListener("submit", (event) => {
  event.preventDefault();
  submitAuth(registerForm, "/auth/register", true);
});

profileForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  showMessage(profileFeedback, "Salvando seu perfil…");
  try {
    await saveProfile();
    showMessage(profileFeedback, "Perfil salvo com sucesso.", "success");
  } catch (error) {
    showMessage(profileFeedback, messageFor(error), "error");
  }
});

simulateButton.addEventListener("click", async () => {
  if (!profileForm.reportValidity()) return;

  const profilePayload = collectProfilePayload();
  const scores = profilePayload.notas;
  const allScoresFilled = Object.values(scores).every(
    (value) => value !== null && Number.isFinite(value),
  );

  if (!allScoresFilled) {
    showMessage(
      simulationFeedback,
      "Preencha as cinco notas do ENEM para fazer a simulação.",
      "error",
    );
    simulationSection.hidden = false;
    simulationResults.replaceChildren();
    return;
  }

  simulateButton.disabled = true;
  simulationSection.hidden = false;
  simulationResults.replaceChildren();
  showMessage(simulationFeedback, "Salvando as notas e consultando os cursos…");

  try {
    const savedProfile = await saveProfile();
    const savedScores = savedProfile.notas;
    const savedLocation = savedProfile.localizacao;
    const result = await simulateCourses({
      linguagens: savedScores.linguagens,
      humanas: savedScores.ciencias_humanas,
      natureza: savedScores.ciencias_natureza,
      matematica: savedScores.matematica,
      redacao: savedScores.redacao,
      cidade: savedLocation.cidade || "Aracaju",
      uf: savedLocation.estado || "SE",
    });

    renderSimulation(result);
    showMessage(simulationFeedback, "Perfil salvo e simulação concluída.", "success");
    showMessage(profileFeedback, "Notas e localização salvas no seu perfil.", "success");
  } catch (error) {
    showMessage(simulationFeedback, messageFor(error), "error");
    if (error.status === 401) {
      localStorage.removeItem(TOKEN_KEY);
      setLoggedOut();
      setAuthView("login");
      showMessage(authFeedback, "Sua sessão expirou. Entre novamente.", "error");
    }
  } finally {
    simulateButton.disabled = false;
  }
});

logoutButton.addEventListener("click", async () => {
  const token = localStorage.getItem(TOKEN_KEY);
  logoutButton.disabled = true;

  try {
    if (token) {
      await apiRequest("/auth/logout", {
        method: "POST",
        headers: authHeaders(),
      });
    }
  } catch (_error) {
    // Encerra a sessão local mesmo se a rede estiver indisponível.
  }

  localStorage.removeItem(TOKEN_KEY);
  setLoggedOut();
  setAuthView("login");
  showMessage(authFeedback, "Sessão encerrada.", "success");
  logoutButton.disabled = false;
});

async function resumeSession() {
  const token = localStorage.getItem(TOKEN_KEY);
  if (!token) return;

  try {
    const result = await apiRequest("/auth/me", {
      method: "GET",
      headers: authHeaders(),
    });
    await openProfile(result.user);
  } catch (error) {
    if (error.status === 401) {
      localStorage.removeItem(TOKEN_KEY);
      showMessage(authFeedback, "Sua sessão expirou. Entre novamente.", "error");
    } else {
      showMessage(authFeedback, messageFor(error), "error");
    }
  }
}

setAuthView("login");
checkProfileService();
loadCourses();
resumeSession();
