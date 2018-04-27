require.config
  baseUrl: '.'
  paths:
    'domReady': '../vendor/requirejs-domready/domReady'
    'angular': '../vendor/angular/angular.min'
    'uiRouter': '../vendor/angular-ui-router/release/angular-ui-router.min'

    'interface': './interface'
    'app': './app'
    'routes': './routes'
  shim:
    'angular':
      exports: 'angular'
    'uiRouter': ['angular']
  priority: ['angular']
  deps: ['interface']
