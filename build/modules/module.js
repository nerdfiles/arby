(function() {
  define(['angular'], function(angular) {
    'use strict';
    var deps, hMediaModule;
    deps = [];
    return hMediaModule = angular.module('ngHyper.directives', deps);
  });

}).call(this);

(function() {
  define(['angular'], function(angular) {
    'use strict';
    var deps, omegaModule;
    deps = ['ngHyper.cryptoService'];
    return omegaModule = angular.module('ngOmega.directives', deps);
  });

}).call(this);
