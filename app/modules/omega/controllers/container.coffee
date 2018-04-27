# @module omega/controllers/container.coffee
define [
  './../module'
  'services/crypto'
], (hMediaModule) ->
  'use strict'
  hMediaModule.controller 'hMediaTestController', [
    '$http'
    'crypto'
    ($http, crypto) ->
      console.log $http
      console.log crypto
  ]
