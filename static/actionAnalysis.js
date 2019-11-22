"use strict";

$(document).ready(() => {
    console.log("document.ready");
    let options = {
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
                text: 'Find anything here you should do more of?'
      },
      scales: {
        yAxes: [{
            ticks: {
                suggestedMin: 0,
                stepSize: 0.05
            },
            scaleLabel: {
                display: true,
                labelString: 'Amount of time you wrote this down'
            }
        }],
        xAxes: [{
            scaleLabel: {
                display: true,
                labelString: 'Date'
            }
        }]
      }
    };

 let ctx = $('#actionChart').get(0).getContext('2d');

    $.getJSON("/action.json", (data) => {

         let sentimentChart = new Chart(ctx, {
                                            type: 'bubble',
                                            data: data,
                                            options: options
                                            });

        }
        
        // $('#chartLegend').html(happyChart.generateLegend());
    
    });