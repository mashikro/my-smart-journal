"use strict";

$(document).ready(() => {
    const options = {
        responsive: true,
        maintainAspectRatio: true,
        legend: {
            display: true,
            label: {
                fontColor: '#17cfcf',
            }
        },
        title: {
                display: true,
                text: 'Your Happiness Trend'
        },
      scales: {
        yAxes: [{
            ticks: {
                suggestedMin: 0,
            },
            scaleLabel: {
                display: true,
                labelString: 'Happiness Score'
            }

        }],
        xAxes: [{
            type: "time",
            time: {
                unit: 'day'
            },
            scaleLabel: {
                display: true,
                labelString: 'Date'
            }
        }]
      }
    };

    let ctx = $('#happyChart').get(0).getContext('2d');

    $.get("/happy.json", (data) => {

        let happyChart = new Chart(ctx, {
                                        type: 'line',
                                        data: data,
                                        options: options
                                        });

        $('#chartLegend').html(happyChart.generateLegend());
        
        });
    });

    
