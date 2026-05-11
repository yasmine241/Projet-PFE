// 🚨 Détection de fraude
async function checkFraud() {
    const amount = document.getElementById("amount").value;

    if (!amount || isNaN(amount)) {
        alert("Veuillez entrer un montant valide.");
        return;
    }

    try {
        const result = await detectFraud({ amount: parseFloat(amount) }); // utilise /api/fraud/detect via api.js

        const output = document.getElementById("result");

        if (result.is_fraud) {
            output.innerHTML = "🚨 FRAUDE DÉTECTÉE";
            output.style.color = "red";
        } else {
            output.innerHTML = "✅ Transaction SAFE";
            output.style.color = "green";
        }

    } catch (error) {
        console.error("Erreur détection fraude:", error);
    }
}

document.addEventListener("DOMContentLoaded", async () => {
    requireAuth();
    await loadComponent("navbar", "../components/navbar.html");
    await loadComponent("sidebar", "../components/sidebar.html");
});
