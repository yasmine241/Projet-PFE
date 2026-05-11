// 👤 Chargement des clients
async function loadClients() {
    try {
        const data = await getClients(); // utilise /api/clients via api.js

        const container = document.getElementById("clientsList");
        container.innerHTML = "";

        if (!data || data.length === 0) {
            container.innerHTML = "<p class='text-muted'>Aucun client trouvé.</p>";
            return;
        }

        data.forEach(client => {
            container.innerHTML += `
                <div class="card p-2 m-2">
                    <h5>${client.prenom} ${client.nom}</h5>
                    <p>${client.email}</p>
                    <small>ID: ${client.id} — ${client.pays} — ${client.statut}</small>
                </div>
            `;
        });

    } catch (error) {
        console.error("Erreur clients:", error);
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    requireAuth();
    await loadComponent("navbar", "../components/navbar.html");
    await loadComponent("sidebar", "../components/sidebar.html");
    loadClients();
});
