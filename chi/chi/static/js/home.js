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

function populate_bullet_performance(performance) {
    window.bullet_games_pie_chart = new Chart($('#bullet-games-pie')[0].getContext('2d'), {
        type: 'pie',
        data: {
            datasets: [{
                data: [performance["stat"]["count"]["rated"] - performance["stat"]["count"]["tour"], performance["stat"]["count"]["tour"], performance["stat"]["count"]["all"] - performance["stat"]["count"]["rated"]],
                backgroundColor: [
                    "rgb(244, 78, 86)", "rgba(244, 78, 86, 0.5)", "#aaa"
                ],
                label: 'Population'
            }],
            labels: ["rated", "tournament", "unrated"]
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

    window.bullet_results_pie_chart = new Chart($('#bullet-results-pie')[0].getContext('2d'), {
        type: 'pie',
        data: {
            datasets: [{
                data: [performance["stat"]["count"]["win"], performance["stat"]["count"]["loss"], performance["stat"]["count"]["draw"]],
                backgroundColor: [
                    "rgb(244, 78, 86)", "rgba(244, 78, 86, 0.5)", "#aaa"
                ],
                label: 'Population'
            }],
            labels: ["win", "loss", "draw"]
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
}

function populate_blitz_performance(performance) {
    window.blitz_games_pie_chart = new Chart($('#blitz-games-pie')[0].getContext('2d'), {
        type: 'pie',
        data: {
            datasets: [{
                data: [performance["stat"]["count"]["rated"] - performance["stat"]["count"]["tour"], performance["stat"]["count"]["tour"], performance["stat"]["count"]["all"] - performance["stat"]["count"]["rated"]],
                backgroundColor: [
                    "rgb(244, 78, 86)", "rgba(244, 78, 86, 0.5)", "#aaa"
                ],
                label: 'Population'
            }],
            labels: ["rated", "tournament", "unrated"]
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

    window.blitz_results_pie_chart = new Chart($('#blitz-results-pie')[0].getContext('2d'), {
        type: 'pie',
        data: {
            datasets: [{
                data: [performance["stat"]["count"]["win"], performance["stat"]["count"]["loss"], performance["stat"]["count"]["draw"]],
                backgroundColor: [
                    "rgb(244, 78, 86)", "rgba(244, 78, 86, 0.5)", "#aaa"
                ],
                label: 'Population'
            }],
            labels: ["win", "loss", "draw"]
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
}

function populate_rapid_performance(performance) {
    window.rapid_games_pie_chart = new Chart($('#rapid-games-pie')[0].getContext('2d'), {
        type: 'pie',
        data: {
            datasets: [{
                data: [performance["stat"]["count"]["rated"] - performance["stat"]["count"]["tour"], performance["stat"]["count"]["tour"], performance["stat"]["count"]["all"] - performance["stat"]["count"]["rated"]],
                backgroundColor: [
                    "rgb(244, 78, 86)", "rgba(244, 78, 86, 0.5)", "#aaa"
                ],
                label: 'Population'
            }],
            labels: ["rated", "tournament", "unrated"]
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

    window.rapid_results_pie_chart = new Chart($('#rapid-results-pie')[0].getContext('2d'), {
        type: 'pie',
        data: {
            datasets: [{
                data: [performance["stat"]["count"]["win"], performance["stat"]["count"]["loss"], performance["stat"]["count"]["draw"]],
                backgroundColor: [
                    "rgb(244, 78, 86)", "rgba(244, 78, 86, 0.5)", "#aaa"
                ],
                label: 'Population'
            }],
            labels: ["win", "loss", "draw"]
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
}

function populate_classical_performance(performance) {
    window.classical_games_pie_chart = new Chart($('#classical-games-pie')[0].getContext('2d'), {
        type: 'pie',
        data: {
            datasets: [{
                data: [performance["stat"]["count"]["rated"] - performance["stat"]["count"]["tour"], performance["stat"]["count"]["tour"], performance["stat"]["count"]["all"] - performance["stat"]["count"]["rated"]],
                backgroundColor: [
                    "rgb(244, 78, 86)", "rgba(244, 78, 86, 0.5)", "#aaa"
                ],
                label: 'Population'
            }],
            labels: ["rated", "tournament", "unrated"]
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

    window.classical_results_pie_chart = new Chart($('#classical-results-pie')[0].getContext('2d'), {
        type: 'pie',
        data: {
            datasets: [{
                data: [performance["stat"]["count"]["win"], performance["stat"]["count"]["loss"], performance["stat"]["count"]["draw"]],
                backgroundColor: [
                    "rgb(244, 78, 86)", "rgba(244, 78, 86, 0.5)", "#aaa"
                ],
                label: 'Population'
            }],
            labels: ["win", "loss", "draw"]
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
}

$(document).ready(function () {
    $('ul.tabs').tabs();
    Chart.defaults.global.defaultFontColor = "#fff";
});