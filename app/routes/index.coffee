'use strict'

exports.index = (req, res) ->
    res.render('index.jade')

exports.dist = (req, res) ->
    res.render('index.dist.jade')
