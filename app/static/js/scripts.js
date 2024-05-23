// Add any custom JavaScript code here
console.log("Custom scripts loaded.");
document.addEventListener('DOMContentLoaded', function() {
  fetch('/metrics_data')
      .then(response => response.json())
      .then(data => {
          const ctx = document.getElementById('myChart').getContext('2d');
          new Chart(ctx, {
              type: 'line',
              data: {
                  labels: data.labels,
                  datasets: [{
                      label: 'Health Metrics',
                      data: data.values,
                      backgroundColor: 'rgba(75, 192, 192, 0.2)',
                      borderColor: 'rgba(75, 192, 192, 1)',
                      borderWidth: 1
                  }]
              },
              options: {
                  scales: {
                      y: {
                          beginAtZero: true
                      }
                  }
              }
          });
      })
      .catch(error => console.error('Error fetching data:', error));
});
