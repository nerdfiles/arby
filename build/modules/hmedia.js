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

(function() {
  define(['./../directives/hmedia'], function() {
    return describe('hmedia', function() {
      return it('should present an ogg', function() {});
    });
  });

}).call(this);
