// app/static/js/dashboard.js

// Charts initialization
let threatChart;
let logChart;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeCharts();
    startDataPolling();
});

function initializeCharts() {
    // Threat Severity Chart
    const threatCtx = document.getElementById('threatChart').getContext('2d');
    threatChart = new Chart(threatCtx, {
        type: 'pie',
        data: {
            labels: ['Critical', 'High', 'Medium', 'Low'],
            datasets: [{
                data: [0, 0, 0, 0],
                backgroundColor: [
                    '#dc3545', // Critical - Red
                    '#ffc107', // High - Yellow
                    '#17a2b8', // Medium - Blue
                    '#28a745'  // Low - Green
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Threat Severity Distribution'
                }
            }
        }
    });

    // Log Activity Chart
    const logCtx = document.getElementById('logChart').getContext('2d');
    logChart = new Chart(logCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Log Events',
                data: [],
                backgroundColor: '#4299e1'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Log Activity Over Time'
                }
            }
        }
    });
}

function startDataPolling() {
    // Poll for new threats
    setInterval(updateThreats, 2000);
    // Poll for new logs
    setInterval(updateLogs, 2000);
}

async function updateThreats() {
    try {
        const response = await fetch('/api/latest-threats');
        const threats = await response.json();
        
        // Update threat chart
        const severityCounts = {
            'Critical': 0,
            'High': 0,
            'Medium': 0,
            'Low': 0
        };
        
        threats.forEach(threat => {
            severityCounts[threat.ml_severity.prediction]++;
        });
        
        threatChart.data.datasets[0].data = Object.values(severityCounts);
        threatChart.update();
        
        // Update recent threats list
        const recentThreatsDiv = document.getElementById('recentThreats');
        recentThreatsDiv.innerHTML = threats.slice(-10).reverse().map(threat => `
            <div class="p-2 border-b border-gray-200">
                <div class="flex justify-between">
                    <span class="font-semibold">${threat.threat_type}</span>
                    <span class="text-sm text-gray-500">${threat.timestamp}</span>
                </div>
                <div class="text-sm">
                    Source IP: ${threat.source_ip} → ${threat.destination_ip}
                    <span class="ml-2 px-2 py-1 rounded text-white text-xs"
                          style="background-color: ${getSeverityColor(threat.ml_severity.prediction)}">
                        ${threat.ml_severity.prediction}
                    </span>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error updating threats:', error);
    }
}

async function updateLogs() {
    try {
        const response = await fetch('/api/latest-logs');
        const logs = await response.json();
        
        // Update log chart
        const timestamps = logs.slice(-10).map(log => log.timestamp);
        const counts = logs.slice(-10).map((_, index) => index + 1);
        
        logChart.data.labels = timestamps;
        logChart.data.datasets[0].data = counts;
        logChart.update();
        
        // Update recent logs list
        const recentLogsDiv = document.getElementById('recentLogs');
        recentLogsDiv.innerHTML = logs.slice(-10).reverse().map(log => `
            <div class="p-2 border-b border-gray-200">
                <div class="flex justify-between">
                    <span class="font-semibold">${log.log_type}</span>
                    <span class="text-sm text-gray-500">${log.timestamp}</span>
                </div>
                <div class="text-sm">
                    ${log.message}
                    <span class="ml-2 px-2 py-1 rounded text-white text-xs"
                          style="background-color: ${getStatusColor(log.status)}">
                        ${log.status}
                    </span>
                </div>
            </div>
        `).join('');
    } catch (error) {
        console.error('Error updating logs:', error);
    }
}

function getSeverityColor(severity) {
    const colors = {
        'Critical': '#dc3545',
        'High': '#ffc107',
        'Medium': '#17a2b8',
        'Low': '#28a745'
    };
    return colors[severity] || '#6c757d';
}

function getStatusColor(status) {
    const colors = {
        'SUCCESS': '#28a745',
        'FAILURE': '#dc3545',
        'WARNING': '#ffc107',
        'ERROR': '#dc3545',
        'INFO': '#17a2b8'
    };
    return colors[status] || '#6c757d';
}