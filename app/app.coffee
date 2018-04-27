define [
  'angular'
  'uiRouter'
  'breeze'
  'breeze.angular.q'
  'services/crypto'
  'modules/hyper'
  'modules/omega'
], (angular) ->
  'use strict'
  deps = [
    'ui.router'
    'breeze.angular.q'
    'ngHyper.directives'
    'ngOmega.directives'
  ]
  angular.module 'ngHyper', deps
