define [
  './../module'
], (hMediaModule) ->
  'use strict'
  hMediaModule.controller 'hMediaTestController', [
    '$http'
    ($http) ->
      console.log $http
  ]
