(function() {
  define(['./../module', 'services/crypto'], function(hMediaModule) {
    'use strict';
    return hMediaModule.controller('hMediaTestController', [
      '$http', 'crypto', function($http, crypto) {
        console.log($http);
        return console.log(crypto);
      }
    ]);
  });

}).call(this);
