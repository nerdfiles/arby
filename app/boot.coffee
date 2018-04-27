# @fileOverview boot.coffee
# Booter for angular-hyper.
require.config
  baseUrl: 'app'

  paths:

    # Application Dependencies
    'domReady'                 : '../vendor/requirejs-domready/domReady'
    'angular'                  : '../vendor/angular/angular'
    'uiRouter'                 : '../vendor/angular-ui-router/release/angular-ui-router'
    'breeze'                   : '../vendor/bower-breeze/breeze.debug'
    'breeze.angular.q'         : '../vendor/bower-breeze/labs/breeze.angular.q'
    'angular.crypto'           : '../vendor/angular-crypto/angular-crypto'

    # Application Modules
    'ngHyperIndex'             : './modules/hyper/index'
    'ngOmegaIndex'             : './modules/omega/index'
    'ngHyper'                  : './modules/hyper/module'
    'ngOmega'                  : './modules/omega/module'

    # Application Services
    'services/crypto'          : './services/crypto'

    # Application Models
    'models/video'             : './models/video'

    # Application Core
    'interface'                : './interface'
    'app'                      : './app'
    'routes'                   : './routes'

    # Application Modules
    'modules/hyper'            : './modules/hyper/index'
    'modules/omega'            : './modules/omega/index'

  shim:
    'angular':
      exports: 'angular'
    'angular.crypto':
      deps: [
          'angular'
      ]
    'uiRouter':
      deps: [
        'angular'
      ]
    'breeze.angular.q':
      deps: [
        'angular'
        'breeze'
      ]

  priority: [
    'angular'
  ]

  deps: [
    'interface'
  ]
