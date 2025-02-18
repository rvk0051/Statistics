document.addEventListener("DOMContentLoaded", function () {
    fetchDataAndRenderChart(); // Load chart with default company
});

// Global chart instance
let companyChart;

// Fetch Data and Initialize Chart
function fetchDataAndRenderChart(company = null) {
    let url = `/get_chart_data/?company=${company || ''}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log(" Fetched Data:", data); // Debugging
            populateCompanyFilter(data);  // Populate dropdown
            updateChart(data.company_placement_data);  // Render chart
        })
        .catch(error => console.error('Error fetching data:', error));
}

// Populate Company Filter
function populateCompanyFilter(data) {
    let companyFilter = document.getElementById('companyFilter');

    // Remove previous options
    companyFilter.innerHTML = '';

    // Add new options
    data.companies.forEach(company => {
        let option = new Option(company, company);
        companyFilter.add(option);
    });
    // Set the dropdown value to the currently selected company
    companyFilter.value = data.default_company;
}

// Apply Filter and Update Chart (Triggered only when clicking "Apply Filters")
function applyFilter() {
    let selectedCompany = document.getElementById('companyFilter').value;
    console.log(` Applying Filter - Selected Company: ${selectedCompany}`);
    
    fetchDataAndRenderChart(selectedCompany); // Fetch data based on selected company

    // Update dropdown value to reflect selection
    document.getElementById('companyFilter').value = selectedCompany;
}

// Update Chart
function updateChart(data) {
    console.log("📊 Updating Chart with:", data);

    if (companyChart) companyChart.destroy(); // Destroy old chart if exists

    const ctx = document.getElementById('companyPlacementsChart').getContext('2d');

    if (data.length === 0) {
        console.warn(" No data available for the selected company.");
        return;
    }

    companyChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data.map(item => item.placement_year),
            datasets: [{
                label: 'Students Placed',
                data: data.map(item => item.students_placed),
                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: { 
            responsive: true, 
            animation: { duration: 1000 }, 
            scales: { y: { beginAtZero: true } } 
        }
    });
}
// Wait for the page to load
// Wait for the page to load
document.addEventListener("DOMContentLoaded", function () {
    fetchSalaryDistribution();
});

function fetchSalaryDistribution() {
    fetch("http://127.0.0.1:8000/get_salary_distribution/")
        .then(response => response.json())
        .then(data => {
            if (!data.salary_distribution || data.salary_distribution.length === 0) {
                console.warn("No salary data available.");
                return;
            }
            drawPieChart(data.salary_distribution);
        })
        .catch(error => console.error("Error fetching data:", error));
}

function drawPieChart(data) {
    let labels = data.map(item => item.salary_range);
    let values = data.map(item => item.students_count);

    let ctx = document.getElementById("salaryChart").getContext("2d");

    if (window.salaryChartInstance) {
        window.salaryChartInstance.destroy();
    }

    window.salaryChartInstance = new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                label: "Number of Students",
                data: values,
                backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40"],
                borderColor: "#fff",
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: "top" },
                tooltip: { enabled: true }
            }
        }
    });
}