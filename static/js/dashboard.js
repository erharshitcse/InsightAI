let myChart;
let colsActive = false;

async function uploadFile() {
    const file = document.getElementById('fileInput').files[0];
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch('/api/upload', { method: 'POST', body: formData });
    if(res.ok) {
        colsActive = true;
        document.getElementById('uploadStatus').classList.remove('hidden');
        alert("File Uploaded!");
    }
}

async function runQuery() {
    const query = document.getElementById('queryInput').value;
    if(!colsActive) return alert("Upload CSV first!");
    
    document.getElementById('loading').classList.remove('hidden');
    const res = await fetch('/api/query', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ query: query })
    });
    const result = await res.json();
    document.getElementById('loading').classList.add('hidden');

    document.getElementById('tableContainer').innerHTML = result.table_html;
    const ctx = document.getElementById('chartCanvas').getContext('2d');
    if(myChart) myChart.destroy();
    myChart = new Chart(ctx, {
        type: result.chart_type.includes('pie') ? 'pie' : (result.chart_type.includes('line') ? 'line' : 'bar'),
        data: {
            labels: result.labels,
            datasets: [{
                label: 'Data Points',
                data: result.values,
                backgroundColor: ['#3b82f6', '#10b981', '#f59e0b', '#ef4444'],
            }]
        },
        options: { responsive: true, plugins: { legend: { labels: { color: 'white' } } } }
    });
}