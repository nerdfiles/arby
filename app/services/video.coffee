# @module services/video.coffee
define [
  'models/video'
], () ->
  serviceInterface = @
  # @name write_file
  serviceInterface.write_file = () ->
  # @name read_image
  serviceInterface.read_image = () ->
  # @name read_file
  serviceInterface.read_file = () ->
  # @name output_image
  serviceInterface.output_image = () ->
  # @name autocorrelate
  serviceInterface.autocorrelate = () ->
  # @name init
  serviceInterface.init = () ->
    @that = @
    @that.width = @that.autocorrelate data, length
    @that.heitht = length / @that.width
