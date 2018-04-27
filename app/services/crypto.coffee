# @module services/crypto
define [
  'angular'
  'angular.crypto'
], (angular) ->
  'use strict'
  deps = []
  cryptoModule = angular.module 'ngHyper.cryptoModule', deps

  cryptoModule.service 'crypto', [
    '$http'
    'gdi2290.crypto'
    cryptoService
  ]

  # @name cryptoService
  cryptoService = ($http, $crypto) ->
    serviceInterface = @
    # @description
    # Hash a string.
    serviceInterface.hash = () ->
      console.log $http
    # @description
    # MD5
    serviceInterface.md5 = () ->
    # @description
    # Encrypt
    serviceInterface.encrypt = () ->
    # @description
    # Decrypt
    serviceInterface.decrypt = () ->
    serviceInterface

  cryptoModule
