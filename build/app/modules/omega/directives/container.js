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
