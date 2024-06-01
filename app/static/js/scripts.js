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
  fetch(apiEndpoint, { method: 'GET' })
    .then(response => response.json())
    .then(data => {
      const labels = data.map(item => item.date || item.timestamp);
      const values = data.map(item => {
        if (apiEndpoint === '/nutrition_data') {
          return item.calories;
        } else if (apiEndpoint === '/sleep_data') {
          return item.hours;
        } else if (apiEndpoint === '/mood_data') {
          return item.rating;  // Ensure the correct field is used for mood data
        } else if (apiEndpoint === '/activity_data') {
          return item.steps;
        }
      });

      const ctx = document.getElementById(canvasId).getContext('2d');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [{
            label: chartLabel,
            data: values,
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
          maintainAspectRatio: true,
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
          },
          layout: {
            padding: {
              left: 10,
              right: 10,
              top: 10,
              bottom: 10
            }
          }
        }
      });
    })
    .catch(error => console.error('Error fetching data:', error));
}
