(function() {
  define(['angular', 'angular.crypto'], function(angular) {
    'use strict';
    var cryptoModule, cryptoService, deps;
    deps = [];
    cryptoModule = angular.module('ngHyper.cryptoModule', deps);
    cryptoModule.service('crypto', ['$http', 'gdi2290.crypto', cryptoService]);
    cryptoService = function($http, $crypto) {
      var serviceInterface;
      serviceInterface = this;
      serviceInterface.hash = function() {
        return console.log($http);
      };
      serviceInterface.md5 = function() {};
      serviceInterface.encrypt = function() {};
      serviceInterface.decrypt = function() {};
      return serviceInterface;
    };
    return cryptoModule;
  });

}).call(this);
