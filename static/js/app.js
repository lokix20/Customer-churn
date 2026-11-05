let personasList = [];
let chartsRendered = false;

// Initialize personas from backend
async function fetchStatsAndPersonas() {
    try {
        const res = await fetch('/api/stats');
        if (res.ok) {
            const data = await res.json();
            personasList = data.personas || [];
            initPersonaChips();
            if (personasList.length > 0) {
                loadPersona(0);
            }
        }
    } catch (err) {
        console.error("Failed to load platform stats:", err);
    }
}

function initPersonaChips() {
    const bar = document.getElementById('personaBar');
    if (!bar) return;
    bar.innerHTML = '';
    personasList.forEach((p, idx) => {
        const btn = document.createElement('button');
        btn.className = `persona-chip ${idx === 0 ? 'active' : ''}`;
        btn.innerText = p.name;
        btn.onclick = () => loadPersona(idx);
        bar.appendChild(btn);
    });
}

function loadPersona(idx) {
    const p = personasList[idx];
    if (!p) return;

    document.querySelectorAll('.persona-chip').forEach((c, i) => {
        c.classList.toggle('active', i === idx);
    });

    document.getElementById('tenure').value = p.tenure;
    document.getElementById('tenureVal').innerText = p.tenure;
    document.getElementById('MonthlyCharges').value = p.MonthlyCharges;
    document.getElementById('Contract').value = p.Contract;
    document.getElementById('InternetService').value = p.InternetService;
    document.getElementById('TechSupport').value = p.TechSupport;
    document.getElementById('OnlineSecurity').value = p.OnlineSecurity;
    document.getElementById('PaymentMethod').value = p.PaymentMethod;
    document.getElementById('PaperlessBilling').value = p.PaperlessBilling;
    document.getElementById('SeniorCitizen').value = p.SeniorCitizen;
    document.getElementById('Partner').value = p.Partner;

    triggerPredict();
}

function updateTenure(val) {
    document.getElementById('tenureVal').innerText = val;
    triggerPredict();
}

function calcTotal() {
    triggerPredict();
}

function switchTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));

    document.getElementById(`tab-${tabId}`).classList.add('active');
    
    const tabOrder = ['demo', 'analytics', 'presentation'];
    const btnIdx = tabOrder.indexOf(tabId);
    if (btnIdx >= 0) {
        document.querySelectorAll('.nav-btn')[btnIdx].classList.add('active');
    }

    if (tabId === 'analytics') {
        renderCharts();
    }
}

async function triggerPredict() {
    const calcStatus = document.getElementById('calcStatus');
    if (calcStatus) {
        calcStatus.innerText = "● Calculating...";
        calcStatus.style.color = "var(--accent-amber)";
    }

    const payload = {
        tenure: parseFloat(document.getElementById('tenure').value),
        MonthlyCharges: parseFloat(document.getElementById('MonthlyCharges').value),
        TotalCharges: parseFloat(document.getElementById('tenure').value) * parseFloat(document.getElementById('MonthlyCharges').value),
        Contract: document.getElementById('Contract').value,
        InternetService: document.getElementById('InternetService').value,
        TechSupport: document.getElementById('TechSupport').value,
        OnlineSecurity: document.getElementById('OnlineSecurity').value,
        PaymentMethod: document.getElementById('PaymentMethod').value,
        PaperlessBilling: document.getElementById('PaperlessBilling').value,
        SeniorCitizen: document.getElementById('SeniorCitizen').value,
        Partner: document.getElementById('Partner').value
    };

    try {
        const res = await fetch('/api/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        if (!res.ok) throw new Error('API Error');
        const data = await res.json();

        // Update probability display
        const pct = Math.round(data.churn_probability * 100);
        const probElem = document.getElementById('churnProbDisplay');
        probElem.innerText = `${pct}%`;

        // Update risk badge & gauge coloring
        const badge = document.getElementById('riskBadge');
        badge.className = 'badge-risk';
        if (data.risk_tier === 'HIGH') {
            badge.classList.add('risk-high');
            badge.innerText = 'HIGH CHURN RISK';
            probElem.style.color = 'var(--accent-rose)';
        } else if (data.risk_tier === 'MEDIUM') {
            badge.classList.add('risk-medium');
            badge.innerText = 'MEDIUM CHURN RISK';
            probElem.style.color = 'var(--accent-amber)';
        } else {
            badge.classList.add('risk-low');
            badge.innerText = 'LOW CHURN RISK (LOYAL)';
            probElem.style.color = 'var(--accent-emerald)';
        }

        // Update CLV & Expected Lifetime
        document.getElementById('clvDisplay').innerText = `$${Number(data.clv.clv_value).toLocaleString('en-US', { minimumFractionDigits: 2 })}`;
        document.getElementById('lifetimeDisplay').innerText = `${data.clv.expected_remaining_months} Mos`;

        // Update Recommendations
        const recsBox = document.getElementById('recsList');
        recsBox.innerHTML = '';
        data.recommendations.forEach(r => {
            const div = document.createElement('div');
            div.className = 'rec-item';
            div.innerHTML = `
                <div class="rec-title">${r.action}</div>
                <div class="rec-desc">${r.detail}</div>
                <div class="rec-impact">✦ ${r.impact}</div>
            `;
            recsBox.appendChild(div);
        });

        if (calcStatus) {
            calcStatus.innerText = "● Model Live";
            calcStatus.style.color = "var(--accent-emerald)";
        }
    } catch (err) {
        console.error("Prediction failed:", err);
        if (calcStatus) {
            calcStatus.innerText = "● Calculation Error";
            calcStatus.style.color = "var(--accent-rose)";
        }
    }
}

function renderCharts() {
    if (chartsRendered) return;
    chartsRendered = true;

    new Chart(document.getElementById('contractChart'), {
        type: 'bar',
        data: {
            labels: ['Month-to-Month', 'One Year', 'Two Year'],
            datasets: [{
                label: 'Churn Rate (%)',
                data: [42.7, 11.3, 2.8],
                backgroundColor: ['rgba(244, 63, 94, 0.7)', 'rgba(245, 158, 11, 0.7)', 'rgba(16, 185, 129, 0.7)'],
                borderColor: ['#f43f5e', '#f59e0b', '#10b981'],
                borderWidth: 1.5,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.06)' }, ticks: { color: '#94a3b8' } },
                x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
            }
        }
    });

    new Chart(document.getElementById('internetChart'), {
        type: 'bar',
        data: {
            labels: ['Fiber Optic', 'DSL', 'No Internet'],
            datasets: [{
                label: 'Churn Rate (%)',
                data: [41.9, 19.0, 7.4],
                backgroundColor: ['rgba(244, 63, 94, 0.7)', 'rgba(59, 130, 246, 0.7)', 'rgba(16, 185, 129, 0.7)'],
                borderColor: ['#f43f5e', '#3b82f6', '#10b981'],
                borderWidth: 1.5,
                borderRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.06)' }, ticks: { color: '#94a3b8' } },
                x: { grid: { display: false }, ticks: { color: '#94a3b8' } }
            }
        }
    });
}

window.addEventListener('DOMContentLoaded', () => {
    fetchStatsAndPersonas();
});
