(function() {
  define(['angular', 'uiRouter', 'breeze', 'breeze.angular.q', 'services/crypto', 'modules/hyper', 'modules/omega'], function(angular) {
    'use strict';
    var deps;
    deps = ['ui.router', 'breeze.angular.q', 'ngHyper.directives', 'ngOmega.directives'];
    return angular.module('ngHyper', deps);
  });

}).call(this);
