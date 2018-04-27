# @module omega/directives/container.coffee
define [
  '../module'
], (omegaModule) ->
  'use strict'
  omegaModule.directive 'omega', [
    '$location'
    ($location) ->
      linker = ($scope, element, attrs) ->
        console.log $scope
        console.log element
        console.log attrs
      link: linker
      restrict: 'E'
  ]
