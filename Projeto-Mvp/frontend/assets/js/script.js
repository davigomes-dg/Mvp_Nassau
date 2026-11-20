import { apiRequest } from "../../services/api.js";

const TOKEN_KEY = "notaee_access_token";
const authPanel = document.querySelector("#auth-panel");
const profilePanel = document.querySelector("#profile-panel");
const authFeedback = document.querySelector("#auth-feedback");
const profileFeedback = document.querySelector("#profile-feedback");
const loginForm = document.querySelector("#login-form");
const registerForm = document.querySelector("#register-form");
const profileForm = document.querySelector("#profile-form");

function showMessage(element, message = "", kind = "") {
  element.textContent = message;
  element.dataset.kind = kind;
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
  document.querySelector("#welcome-message").textContent = "Olá, " + user.name + ". Seus dados ficam salvos na sua conta.";
  showMessage(authFeedback);
}

function fillProfile(profile) {
  Object.entries(profile.notas).forEach(([field, value]) => {
    profileForm.elements.namedItem(field).value = value ?? "";
  });
  Object.entries(profile.localizacao).forEach(([field, value]) => {
    profileForm.elements.namedItem(field).value = value ?? "";
  });
}

async function openProfile(user) {
  setLoggedIn(user);
  try {
    const result = await apiRequest("/profile", {
      headers: { Authorization: "Bearer " + localStorage.getItem(TOKEN_KEY) },
    });
    fillProfile(result.profile);
    showMessage(profileFeedback);
  } catch (error) {
    showMessage(profileFeedback, error.message, "error");
    if (error.status === 401) {
      localStorage.removeItem(TOKEN_KEY);
      authPanel.hidden = false;
      profilePanel.hidden = true;
    }
  }
}

async function submitAuth(form, endpoint, includeName = false) {
  const data = new FormData(form);
  const payload = {
    email: data.get("email").trim(),
    password: data.get("password"),
  };
  if (includeName) payload.name = data.get("name").trim();

  try {
    const result = await apiRequest(endpoint, {
      method: "POST",
      body: JSON.stringify(payload),
    });
    localStorage.setItem(TOKEN_KEY, result.access_token);
    form.reset();
    await openProfile(result.user);
  } catch (error) {
    showMessage(authFeedback, error.message, "error");
  }
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
  const data = new FormData(profileForm);
  const score = (field) => data.get(field) === "" ? null : Number(data.get(field));
  const payload = {
    notas: {
      linguagens: score("linguagens"),
      ciencias_humanas: score("ciencias_humanas"),
      ciencias_natureza: score("ciencias_natureza"),
      matematica: score("matematica"),
      redacao: score("redacao"),
    },
    localizacao: {
      cidade: data.get("cidade").trim() || null,
      estado: data.get("estado").trim() || null,
    },
  };

  try {
    const result = await apiRequest("/profile", {
      method: "PUT",
      headers: { Authorization: "Bearer " + localStorage.getItem(TOKEN_KEY) },
      body: JSON.stringify(payload),
    });
    fillProfile(result.profile);
    showMessage(profileFeedback, "Perfil salvo com sucesso.", "success");
  } catch (error) {
    showMessage(profileFeedback, error.message, "error");
  }
});

document.querySelector("#logout-button").addEventListener("click", async () => {
  const token = localStorage.getItem(TOKEN_KEY);
  try {
    if (token) {
      await apiRequest("/auth/logout", {
        method: "POST",
        headers: { Authorization: "Bearer " + token },
      });
    }
  } catch (_error) {
    // A sessão local será encerrada mesmo se a rede estiver indisponível.
  }
  localStorage.removeItem(TOKEN_KEY);
  profileForm.reset();
  profilePanel.hidden = true;
  authPanel.hidden = false;
  setAuthView("login");
});

async function resumeSession() {
  const token = localStorage.getItem(TOKEN_KEY);
  if (!token) return;

  try {
    const result = await apiRequest("/auth/me", {
      headers: { Authorization: "Bearer " + token },
    });
    await openProfile(result.user);
  } catch (error) {
    if (error.status === 401) localStorage.removeItem(TOKEN_KEY);
    showMessage(authFeedback, error.status === 401 ? "Sua sessão expirou. Entre novamente." : error.message, "error");
  }
}

resumeSession();
