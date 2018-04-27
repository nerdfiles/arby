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

(function() {
  define(['../module'], function(omegaModule) {
    'use strict';
    return omegaModule.directive('omega', [
      '$location', function($location) {
        var linker;
        linker = function($scope, element, attrs) {
          console.log($scope);
          console.log(element);
          return console.log(attrs);
        };
        return {
          link: linker,
          restrict: 'E'
        };
      }
    ]);
  });

}).call(this);

(function() {
  define(['./../directives/container'], function() {
    return describe('hmedia', function() {
      return it('should present an ogg', function() {});
    });
  });

}).call(this);
