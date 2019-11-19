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
                text: 'Sentiment Analysis for my Journal Entries'
      },
      scales: {
        yAxes: [{
            ticks: {
                suggestedMin: 0,
            },
            scaleLabel: {
                display: true,
                labelString: 'Sentiment Score'
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

    let ctx = $('#sentimentChart').get(0).getContext('2d');

    $.get("/sentiment-analysis.json", (data) => {
        console.log(data)
        let sentimentChart = new Chart(ctx, {
                                        type: 'bar',
                                        data: data,
                                        options: options
                                        });

        // $('#chartLegend').html(happyChart.generateLegend());
        
        });
    });