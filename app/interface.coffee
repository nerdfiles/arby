# @module interface.coffee
require [
  'angular'
  'app'
  'routes'
], (angular) ->
  'use strict'
  require [
    'domReady!'
  ], (document) ->
    angular.bootstrap document, ['ngHyper']
