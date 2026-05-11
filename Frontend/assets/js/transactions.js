// 📈 Chargement des transactions
async function loadTransactions() {
    try {
        const data = await getTransactions(); // utilise /api/transactions via api.js

        const table = document.getElementById("transactionsTable");
        table.innerHTML = "";

        if (!data || data.length === 0) {
            table.innerHTML = "<tr><td colspan='4' class='text-muted'>Aucune transaction.</td></tr>";
            return;
        }

        data.forEach(tx => {
            table.innerHTML += `
                <tr>
                    <td>${tx.id}</td>
                    <td>${tx.montant} €</td>
                    <td>${tx.date_transaction}</td>
                    <td>${tx.statut}</td>
                </tr>
            `;
        });

    } catch (error) {
        console.error("Erreur transactions:", error);
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    requireAuth();
    await loadComponent("navbar", "../components/navbar.html");
    await loadComponent("sidebar", "../components/sidebar.html");
    loadTransactions();
});
