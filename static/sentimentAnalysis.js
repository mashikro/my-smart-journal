"use strict";
// Need to change date coming in as string to Date JS object 
// when working with clustered bar graphs

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
                text: 'Sentiment Analysis for my Journal Entries'
      },
      scales: {
        yAxes: [{
            ticks: {
                suggestedMin: 0,
                stepSize: 0.05
            },
            scaleLabel: {
                display: true,
                labelString: 'Sentiment Score'
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

    let ctx = $('#sentimentChart').get(0).getContext('2d');

    $.getJSON("/sentiment-analysis.json", (data) => {

        
        // for (let i = 0; i < data.labels.length; i++) {
        //     data.labels[i] = formatDateStringForChart(data.labels[i]);
        // }

        // format dates using helper func from above
        for (let date of data.labels) {
            date = formatDateStringForChart(date);
        }
        
        let sentimentChart = new Chart(ctx, {
                                            type: 'bar',
                                            data: data,
                                            options: options
                                            });
        
        
        // $('#chartLegend').html(happyChart.generateLegend());
    
    });
});
