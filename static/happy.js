"use strict";

$(document).ready(() => {
    const options = {
      responsive: true,
      maintainAspectRatio: true,
      scales: {
        yAxes: [{
            ticks: {
                suggestedMin: 0,
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

    
