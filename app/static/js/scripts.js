{% block scripts %}
<div>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script>
    console.log("Custom scripts loaded.");

    document.addEventListener('DOMContentLoaded', function() {
      // Fetch and display data for the dashboard
      fetchDataAndDisplay('/nutrition_data', 'nutritionChart', 'Nutrition Data', 'Nutrition', 'pie');
      fetchDataAndDisplay('/sleep_data', 'sleepChart', 'Sleep Data', 'Hours', 'line');
      fetchDataAndDisplay('/mood_data', 'moodChart', 'Mood Data', 'Mood Level', 'radar');
      fetchDataAndDisplay('/activity_data', 'activityChart', 'Activity Data', 'Steps', 'bar');

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
    function fetchDataAndDisplay(apiEndpoint, canvasId, chartLabel, yAxisLabel, chartType) {
      fetch(apiEndpoint, { method: 'GET' })
        .then(response => response.json())
        .then(data => {
          let labels = [];
          let values = [];

          if (apiEndpoint === '/nutrition_data') {
            labels = ['Calories', 'Protein', 'Carbs', 'Fats'];
            values = [data.calories, data.protein, data.carbs, data.fats];
          } else {
            labels = data.map(item => item.date || item.timestamp);
            values = data.map(item => {
              if (apiEndpoint === '/sleep_data') return item.hours;
              if (apiEndpoint === '/mood_data') return item.mood;
              if (apiEndpoint === '/activity_data') return item.steps;
            });
          }

          const ctx = document.getElementById(canvasId).getContext('2d');
          new Chart(ctx, {
            type: chartType,
            data: {
              labels: labels,
              datasets: [{
                label: chartLabel,
                data: values,
                backgroundColor: chartType === 'pie' ? [
                  'rgba(255, 99, 132, 0.2)',
                  'rgba(54, 162, 235, 0.2)',
                  'rgba(255, 206, 86, 0.2)',
                  'rgba(75, 192, 192, 0.2)'
                ] : 'rgba(75, 192, 192, 0.2)',
                borderColor: chartType === 'pie' ? [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)',
                  'rgba(255, 206, 86, 1)',
                  'rgba(75, 192, 192, 1)'
                ] : 'rgba(75, 192, 192, 1)',
                borderWidth: 1
              }]
            },
            options: {
              responsive: true,
              maintainAspectRatio: false,
              scales: chartType !== 'pie' ? {
                yAxes: [{
                  scaleLabel: {
                    display: true,
                    labelString: yAxisLabel
                  },
                  ticks: {
                    beginAtZero: true
                  }
                }]
              } : {},
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
  </script>
</div>
{% endblock %}
