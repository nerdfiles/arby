define [
  './../module'
], (hMediaModule) ->
  'use strict'
  hMediaModule.directive 'hyper', [
    '$location'
    ($location) ->
      linker = ($scope, element, attrs) ->
        console.log $scope
        console.log element
        console.log attrs
      link: linker
      restrict: 'E'
  ]
