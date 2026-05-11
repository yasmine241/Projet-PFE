// 📊 Chargement des stats du dashboard
async function loadDashboard() {
    try {
        const data = await getDashboardStats();

        console.log("Dashboard data:", data);

        document.getElementById("totalTransactions").innerText = data.total_transactions;
        document.getElementById("fraudCount").innerText = data.fraud_count;
        document.getElementById("safeCount").innerText = data.safe_count;

        // 🚨 Alerte fraude
        const alertBox = document.getElementById("fraudAlert");

        if (data.fraud_count > 0) {
            alertBox.style.display = "block";
        } else {
            alertBox.style.display = "none";
        }

    } catch (error) {
        console.error("Erreur dashboard:", error);
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    requireAuth();

    await loadComponent("navbar", "../components/navbar.html");
    await loadComponent("sidebar", "../components/sidebar.html");

    loadDashboard();
    setInterval(loadDashboard, 5000);
});