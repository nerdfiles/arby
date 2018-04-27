(function() {
  define(['./../module'], function(hMediaModule) {
    'use strict';
    return hMediaModule.directive('hyper', [
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
