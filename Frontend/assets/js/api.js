// 🌐 Requête authentifiée générique
async function authFetch(url, options = {}) {
    const token = getToken();

    const response = await fetch(API_URL + url, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            "Authorization": token ? `Bearer ${token}` : "",
            ...options.headers
        }
    });

    // 🔴 Session expirée → logout
    if (response.status === 401) {
        logout();
        alert("Session expirée. Veuillez vous reconnecter.");
        return;
    }

    // 🔴 Erreur serveur
    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.message || "Erreur API");
    }

    return response.json();
}

// 📊 Dashboard
async function getDashboardStats() {
    return await authFetch("/api/dashboard");
}

// 📈 Transactions
async function getTransactions() {
    return await authFetch("/api/transactions");
}

// 👤 Clients
async function getClients() {
    return await authFetch("/api/clients");
}

// 🚨 Détection fraude
async function detectFraud(transaction) {
    return await authFetch("/api/fraud/detect", {
        method: "POST",
        body: JSON.stringify(transaction)
    });
}
function getToken() {
    return localStorage.getItem("token");
}
function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}