function populate_rating_history(rating_history) {
    window.bullet_rating_chart = new Chart($('#rating-bullet')[0].getContext('2d'), {
        type: 'line',
        data: {
            labels: rating_history["bullet_labels"],
            datasets: [{
                data: rating_history["bullet_data"],
                fill: true,
                borderColor: 'rgb(244, 78, 86)',
                tension: 0.1,
                pointRadius: 0,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                display: false
            }
        }
    });
    
    window.blitz_rating_chart = new Chart($('#rating-blitz')[0].getContext('2d'), {
        type: 'line',
        data: {
            labels: rating_history["blitz_labels"],
            datasets: [{
                data: rating_history["blitz_data"],
                fill: true,
                borderColor: 'rgb(244, 78, 86)',
                tension: 0.1,
                pointRadius: 0,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                display: false
            }
        }
    });

    window.rapid_rating_chart = new Chart($('#rating-rapid')[0].getContext('2d'), {
        type: 'line',
        data: {
            labels: rating_history["rapid_labels"],
            datasets: [{
                data: rating_history["rapid_data"],
                fill: true,
                borderColor: 'rgb(244, 78, 86)',
                tension: 0.1,
                pointRadius: 0,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                display: false
            }
        }
    });

    window.classical_rating_chart = new Chart($('#rating-classical')[0].getContext('2d'), {
        type: 'line',
        data: {
            labels: rating_history["classical_labels"],
            datasets: [{
                data: rating_history["classical_data"],
                fill: true,
                borderColor: 'rgb(244, 78, 86)',
                tension: 0.1,
                pointRadius: 0,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                display: false
            }
        }
    });
}

$(document).ready(function () {
    $('ul.tabs').tabs();

    Chart.defaults.global.defaultFontColor = "#fff";

    window.games_pie_chart = new Chart($('#games-pie')[0].getContext('2d'), {
        type: 'pie',
        data: {
            datasets: [{
                data: [120, 380, 45, 17],
                backgroundColor: [
                    '#696969', '#808080', '#A9A9A9', '#C0C0C0', '#D3D3D3'
                ],
                label: 'Population'
            }],
            labels: ["bullet", "blitz", "rapid", "classical"]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            legend: {
                position: 'top',
                align: 'left'
            }
        }
    });
});