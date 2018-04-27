(function() {
  'use strict';
  exports.index = function(req, res) {
    return res.render('index.jade');
  };

  exports.dist = function(req, res) {
    return res.render('index.dist.jade');
  };

}).call(this);
