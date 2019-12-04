"use strict";


// https://www.html5rocks.com/en/tutorials/canvas/hidpi/
function setupCanvas(canvas) {
  // Get the device pixel ratio, falling back to 1.
  var dpr = window.devicePixelRatio || 1;
  // Get the size of the canvas in CSS pixels.
  var rect = canvas.getBoundingClientRect();
  // Give the canvas pixel dimensions of their CSS
  // size * the device pixel ratio.
  canvas.width = rect.width * dpr;
  canvas.height = rect.height * dpr;
  //var ctx = canvas.getContext('2d');
  // Scale all drawing operations by the dpr, so you
  // don't have to worry about the difference.
  //ctx.scale(dpr, dpr);
  //return ctx;
}


$(document).ready(() => {
    console.log("document.ready");
    
    $.getJSON("/action.json", (data) => {
       
       // console.log('are we getting the data', data)

       let canvas=document.getElementById('actionChart');
       setupCanvas(canvas);
        WordCloud(canvas, { 
            list: data['data'],   
            // backgroundColor: '#f2dfd7', 
            backgroundColor: "#E8F2DA",
            fontFamily: 'Times, serif',
            weightFactor: function (size) {
                return size*30;
            }

                            }); 

        });
            
    });