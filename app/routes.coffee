define [
  'app'
], (app) ->
  'use strict'
  app.config [
    '$stateProvider'
    ($stateProvider) ->
      $stateProvider.state 'test',
        url: '/'
        templateUrl: '/app/pages/directives.test.html'
        controller: 'hMediaTestController'
      $stateProvider.state 'test2',
        url: '/test2'
        templateUrl: '/app/pages/directives.test.html'
        controller: 'hMediaTestController'
  ]
