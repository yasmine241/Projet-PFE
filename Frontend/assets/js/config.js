// ⚙️ Configuration globale
const API_URL = "http://127.0.0.1:5000";

// 🔐 Gestion du token JWT
function getToken() {
    return localStorage.getItem("token");
}

function setToken(token) {
    localStorage.setItem("token", token);
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "../pages/login.html";
}

// 🛡️ Redirection si non connecté
function requireAuth() {
    if (!getToken()) {
        window.location.href = "../pages/login.html";
    }
}

// 📦 Chargement dynamique des composants (sidebar, navbar)
async function loadComponent(id, path) {
    try {
        const res = await fetch(path);
        const html = await res.text();
        document.getElementById(id).innerHTML = html;
    } catch (e) {
        console.warn("Composant introuvable :", path);
    }
}
