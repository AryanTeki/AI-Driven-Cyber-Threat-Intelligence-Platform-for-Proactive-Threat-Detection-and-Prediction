document.addEventListener("DOMContentLoaded", () => {
    // Placeholder logs data
    const logsContainer = document.getElementById("logs-container");
    const logs = [
        "System started monitoring.",
        "Potential threat detected at 2024-11-25 12:34:56.",
        "Threat classified as 'High' severity."
    ];
    logs.forEach(log => {
        const p = document.createElement("p");
        p.textContent = log;
        logsContainer.appendChild(p);
    });

    // Placeholder threats data
    const threatsTable = document.getElementById("threats-table");
    const threats = [
        { id: 1, description: "Unauthorized login attempt", severity: "High", status: "Active" },
        { id: 2, description: "SQL Injection attack", severity: "Medium", status: "Resolved" }
    ];
    threats.forEach(threat => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${threat.id}</td>
            <td>${threat.description}</td>
            <td>${threat.severity}</td>
            <td>${threat.status}</td>
        `;
        threatsTable.appendChild(row);
    });

    // Placeholder for analytics chart
    const ctx = document.getElementById("severity-chart").getContext("2d");
    new Chart(ctx, {
        type: "pie",
        data: {
            labels: ["High", "Medium", "Low"],
            datasets: [{
                data: [5, 3, 2],
                backgroundColor: ["#e74c3c", "#f1c40f", "#2ecc71"]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: "bottom" }
            }
        }
    });
});
