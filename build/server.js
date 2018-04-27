(function() {
  var app, baseDir, express, gzippo, http, path, routes;

  express = require('express');

  http = require('http');

  path = require('path');

  gzippo = require('gzippo');

  routes = require('../app/routes/base');

  app = module.exports = express();

  baseDir = __dirname;

  app.use(express.methodOverride());

  app.set('views', path.join(baseDir, '../build/foundation/'));

  app.set('view options', {
    layout: false,
    pretty: true
  });

  app.set('view engine', 'jade');

  app.use('/app', gzippo.staticGzip(path.join(baseDir, '../build'), {
    contentTypeMatch: /css|text|javascript|json/
  }));

  app.use('/images', gzippo.staticGzip(path.join(baseDir, '/images')));

  app.use('/vendor', gzippo.staticGzip(path.join(baseDir, '../vendor'), {
    contentTypeMatch: /css|text|javascript|json/
  }));

  app.use(app.router);

  app.get('/', routes.index);

  app.get('/deploy', routes.dist);

  app.listen(3000, function() {
    return console.log('Listening on 3000');
  });

  module.exports = app;

}).call(this);
