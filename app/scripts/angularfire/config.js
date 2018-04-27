angular.module('firebase.config', [])
  .constant('FBURL', 'https://portcoin.firebaseio.com')
  .constant('SIMPLE_LOGIN_PROVIDERS', ['password','anonymous','twitter','github'])

  .constant('loginRedirectPath', '/login');