define [
  'angular'
], (angular) ->
  'use strict'
  deps = [
    'ngHyper.cryptoService'
  ]
  omegaModule = angular.module 'ngOmega.directives', deps
