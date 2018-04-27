(function() {
  require.config({
    baseUrl: 'app',
    paths: {
      'domReady': '../vendor/requirejs-domready/domReady',
      'angular': '../vendor/angular/angular',
      'uiRouter': '../vendor/angular-ui-router/release/angular-ui-router',
      'breeze': '../vendor/bower-breeze/breeze.debug',
      'breeze.angular.q': '../vendor/bower-breeze/labs/breeze.angular.q',
      'angular.crypto': '../vendor/angular-crypto/angular-crypto',
      'ngHyperIndex': './modules/hyper/index',
      'ngOmegaIndex': './modules/omega/index',
      'ngHyper': './modules/hyper/module',
      'ngOmega': './modules/omega/module',
      'services/crypto': './services/crypto',
      'models/video': './models/video',
      'interface': './interface',
      'app': './app',
      'routes': './routes',
      'modules/hyper': './modules/hyper/index',
      'modules/omega': './modules/omega/index'
    },
    shim: {
      'angular': {
        exports: 'angular'
      },
      'angular.crypto': {
        deps: ['angular']
      },
      'uiRouter': {
        deps: ['angular']
      },
      'breeze.angular.q': {
        deps: ['angular', 'breeze']
      }
    },
    priority: ['angular'],
    deps: ['interface']
  });

}).call(this);
