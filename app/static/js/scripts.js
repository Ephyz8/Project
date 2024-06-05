console.log("Custom scripts loaded.");

document.addEventListener("DOMContentLoaded", function() {
    // Fetch and display average data
    fetch('/dashboard_data')
        .then(response => response.json())
        .then(data => {
            console.log('Dashboard Data:', data);
            document.getElementById('averageSleepHours').textContent = data.avg_sleep_hours.toFixed(2) + " hours";
            document.getElementById('totalCalories').textContent = data.total_calories + " kcal";
            document.getElementById('moodTrends').textContent = JSON.stringify(data.mood_counts);
        })
        .catch(error => console.error('Error fetching dashboard data:', error));

    // Chart configurations
    const chartConfig = {
        type: 'line',
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    };

    // Fetch and display activity data
    fetch('/activity_data')
        .then(response => response.json())
        .then(data => {
            console.log('Activity Data:', data);
            const ctx = document.getElementById('activityChart').getContext('2d');
            new Chart(ctx, {
                ...chartConfig,
                data: {
                    labels: data.map(item => item.date),
                    datasets: [{
                        label: 'Steps',
                        data: data.map(item => item.steps),
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                }
            });
        })
        .catch(error => console.error('Error fetching activity data:', error));

    // Fetch and display nutrition data
    fetch('/nutrition_data')
        .then(response => response.json())
        .then(data => {
            console.log('Nutrition Data:', data);
            const ctx = document.getElementById('nutritionChart').getContext('2d');
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['Calories', 'Protein', 'Carbs', 'Fats'],
                    datasets: [{
                        label: 'Nutrition',
                        data: [
                            data.reduce((sum, n) => sum + n.calories, 0),
                            data.reduce((sum, n) => sum + n.protein, 0),
                            data.reduce((sum, n) => sum + n.carbs, 0),
                            data.reduce((sum, n) => sum + n.fats, 0)
                        ],
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)',
                            'rgba(75, 192, 192, 0.2)'
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)',
                            'rgba(75, 192, 192, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            });
        })
        .catch(error => console.error('Error fetching nutrition data:', error));

    // Fetch and display sleep data
    fetch('/sleep_data')
        .then(response => response.json())
        .then(data => {
            console.log('Sleep Data:', data);
            const ctx = document.getElementById('sleepChart').getContext('2d');
            new Chart(ctx, {
                ...chartConfig,
                data: {
                    labels: data.map(item => item.date),
                    datasets: [{
                        label: 'Sleep Hours',
                        data: data.map(item => item.hours),
                        backgroundColor: 'rgba(153, 102, 255, 0.2)',
                        borderColor: 'rgba(153, 102, 255, 1)',
                        borderWidth: 1
                    }]
                }
            });
        })
        .catch(error => console.error('Error fetching sleep data:', error));

    // Fetch and display mood data
    fetch('/mood_data')
        .then(response => response.json())
        .then(data => {
            console.log('Mood Data:', data);
            const ctx = document.getElementById('moodChart').getContext('2d');
            new Chart(ctx, {
                ...chartConfig,
                data: {
                    labels: data.map(item => item.date),
                    datasets: [{
                        label: 'Mood',
                        data: data.map(item => item.rating),
                        backgroundColor: 'rgba(255, 159, 64, 0.2)',
                        borderColor: 'rgba(255, 159, 64, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        r: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching mood data:', error));

    // Smooth scroll for internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });

    document.querySelectorAll('.btn-dynamic').forEach(button => {
        button.addEventListener('click', function() {
            alert('Button clicked: ' + this.textContent);
        });
    });

    // Flash message fade out
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.classList.add('fade-out');
        });
    }, 5000); // 5 seconds

    // Remove the alert from the DOM after it has faded out
    document.querySelectorAll('.alert').forEach(alert => {
        alert.addEventListener('transitionend', () => {
            if (alert.classList.contains('fade-out')) {
                alert.remove();
            }
        });
    });
});
