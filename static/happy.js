"use strict";

$(document).ready(() => {
    console.log('Is this working?')
    const options = {
      responsive: true
    };

    let ctx = $('#happyChart').get(0).getContext('2d');
    console.log('here')

    $.get("/happy.json", (data) => {

        let happyChart = new Chart(ctx, {
                                        type: 'line',
                                        data: data,
                                        options: options
                                        });
        console.log('Hello')

        $('#chartLegend').html(happyChart.generateLegend());
        
        });
    
    console.log('how about now?')

    });

    
