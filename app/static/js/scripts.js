// Add any custom JavaScript code here
console.log("Custom scripts loaded.");

document.addEventListener('DOMContentLoaded', function() {
  // Fetch and display data for the dashboard
  fetchDataAndDisplay('/nutrition_data', 'nutritionChart', 'Nutrition Data', 'Nutrition');
  fetchDataAndDisplay('/sleep_data', 'sleepChart', 'Sleep Data', 'Hours');
  fetchDataAndDisplay('/mood_data', 'moodChart', 'Mood Data', 'Mood Level');
  fetchDataAndDisplay('/activity_data', 'activityChart', 'Activity Data', 'Activity');

  // Smooth scroll for internal links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      document.querySelector(this.getAttribute('href')).scrollIntoView({
        behavior: 'smooth'
      });
    });
  });

  // Example of adding dynamic behavior to elements (e.g., button click)
  document.querySelectorAll('.btn-dynamic').forEach(button => {
    button.addEventListener('click', function() {
      alert('Button clicked: ' + this.textContent);
    });
  });
});

// Function to fetch data and initialize charts
function fetchDataAndDisplay(apiEndpoint, canvasId, chartLabel, yAxisLabel) {
  fetch(apiEndpoint)
    .then(response => response.json())
    .then(data => {
      const ctx = document.getElementById(canvasId).getContext('2d');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: data.labels,
          datasets: [{
            label: chartLabel,
            data: data.values,
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
            pointBackgroundColor: 'rgba(75, 192, 192, 1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(75, 192, 192, 1)'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            yAxes: [{
              scaleLabel: {
                display: true,
                labelString: yAxisLabel
              },
              ticks: {
                beginAtZero: true
              }
            }]
          },
          tooltips: {
            mode: 'index',
            intersect: false
          },
          hover: {
            mode: 'nearest',
            intersect: true
          }
        }
      });
    })
    .catch(error => console.error('Error fetching data:', error));
}
