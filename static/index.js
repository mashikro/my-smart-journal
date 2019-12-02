"use strict";

$(document).ready(() => {
    const loginButton = $('#LoginButton');
    const createAccountButton = $('#CreateAccountButton');

    $('#loginForm').hide();
    $('#createAccountForm').hide();

    loginButton.on('click', () => {
      $('#loginForm').show();
      $('#createAccountForm').hide();
    });

    createAccountButton.on('click', () => {
      $('#createAccountForm').show();
      $('#loginForm').hide();
    });

    console.log('Is this working????')
});
