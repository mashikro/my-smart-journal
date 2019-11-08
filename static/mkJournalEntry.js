"use strict";

$(document).ready(() => {
    const morningButton = $('#morningButton');
    const nightButton = $('#nightButton');

    $('#morning-qs').hide();
    $('#night-qs').hide();

    morningButton.on('click', () => {
      $('#morning-qs').show();
      $('#night-qs').hide();
    });

    nightButton.on('click', () => {
      $('#night-qs').show();
      $('#morning-qs').hide();
    });

    console.log('Is this working????')
});
