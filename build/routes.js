(function() {
  define(['app'], function(app) {
    'use strict';
    return app.config([
      '$stateProvider', function($stateProvider) {
        $stateProvider.state('test', {
          url: '/',
          templateUrl: '/app/pages/directives.test.html',
          controller: 'hMediaTestController'
        });
        return $stateProvider.state('test2', {
          url: '/test2',
          templateUrl: '/app/pages/directives.test.html',
          controller: 'hMediaTestController'
        });
      }
    ]);
  });

}).call(this);
