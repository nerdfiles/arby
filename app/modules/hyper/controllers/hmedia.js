(function() {
  define(['./../module'], function(hMediaModule) {
    'use strict';
    return hMediaModule.controller('hMediaTestController', [
      '$http', function($http) {
        return console.log($http);
      }
    ]);
  });

}).call(this);
