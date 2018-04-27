(function() {
  define(['./controllers/hmedia', './directives/hmedia'], function() {});

}).call(this);

(function() {
  define(['./controllers/container', './directives/container'], function(controller, directive) {
    console.log(controller);
    return console.log(directive);
  });

}).call(this);
