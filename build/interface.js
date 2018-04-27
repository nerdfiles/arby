(function() {
  require(['angular', 'app', 'routes'], function(angular) {
    'use strict';
    return require(['domReady!'], function(document) {
      return angular.bootstrap(document, ['ngHyper']);
    });
  });

}).call(this);
