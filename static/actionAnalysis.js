"use strict";
let formatDateStringForChart = (s) => {
    let d = new Date(s);
    return d.toDateString();
};


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
                // stepSize: 0.05
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
    console.log('hi mash')
    $.getJSON("/action.json", (data) => {

        console.log('are we getting the data', data)

         for (let i in data.labels) {
            console.log(data.labels[i]);
            data.labels[i] = formatDateStringForChart(data.labels[i]);
            console.log(data.labels[i]);

        }

         let sentimentChart = new Chart(ctx, {
                                            type: 'bubble',
                                            data: data,
                                            options: options
                                            });

        });
        
        // $('#chartLegend').html(happyChart.generateLegend());
    
    });