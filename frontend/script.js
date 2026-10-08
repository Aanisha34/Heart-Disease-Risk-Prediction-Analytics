const API_BASE = 'https://heart-disease-risk-prediction-analytics.onrender.com';

document.addEventListener('DOMContentLoaded', () => {
    loadAnalytics();

    document.getElementById('predictionForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const formData = {
            age: document.getElementById('age').value,
            sex: document.getElementById('sex').value,
            cp: document.getElementById('cp').value,
            trestbps: document.getElementById('trestbps').value,
            chol: document.getElementById('chol').value,
            fbs: document.getElementById('fbs').value,
            restecg: document.getElementById('restecg').value,
            thalach: document.getElementById('thalach').value,
            exang: document.getElementById('exang').value,
            oldpeak: document.getElementById('oldpeak').value,
            slope: document.getElementById('slope').value,
            ca: document.getElementById('ca').value
        };

        try {
            const response = await fetch('https://heart-disease-risk-prediction-analytics.onrender.com/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            const data = await response.json();
            const resultBox = document.getElementById('resultBox');
            const resultText = document.getElementById('resultText');
            const riskScore = document.getElementById('riskScore');

            resultBox.classList.remove('hidden', 'high-risk', 'low-risk');
            if (data.prediction === 1) {
                resultBox.classList.add('high-risk');
                resultText.innerText = '⚠️ High Risk of Heart Disease Detected';
            } else {
                resultBox.classList.add('low-risk');
                resultText.innerText = '✅ Low Risk / Normal Patient Condition';
            }
            riskScore.innerText = `Risk Percentage: ${data.risk_percentage}%`;

        } catch (error) {
            alert('Error connecting to Backend Server. Please make sure app.py is running on port 5000.');
        }
    });
});

async function loadAnalytics() {
    try {
        const res = await fetch(`${API_BASE}/analytics`);
        const data = await res.json();

        document.getElementById('totalRecords').innerText = data.total_records || '-';
        document.getElementById('avgAge').innerText = data.avg_age || '-';

        // Target Chart
        const ctxTarget = document.getElementById('targetChart').getContext('2d');
        new Chart(ctxTarget, {
            type: 'doughnut',
            data: {
                labels: ['Heart Disease', 'Healthy / Normal'],
                datasets: [{
                    data: [data.disease_cases, data.healthy_cases],
                    backgroundColor: ['#e53e3e', '#38a169']
                }]
            },
            options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
        });

        // Age Group Chart
        const ageLabels = Object.keys(data.age_distribution || {});
        const ageValues = Object.values(data.age_distribution || {});
        const ctxAge = document.getElementById('ageChart').getContext('2d');
        new Chart(ctxAge, {
            type: 'bar',
            data: {
                labels: ageLabels,
                datasets: [{
                    label: 'Patient Count',
                    data: ageValues,
                    backgroundColor: '#4299e1'
                }]
            },
            options: { responsive: true, plugins: { legend: { display: false } } }
        });

    } catch (e) {
        console.log('Analytics unavailable or server offline.');
    }
}