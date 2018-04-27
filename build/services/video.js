(function() {
  define(['models/video'], function() {
    var serviceInterface;
    serviceInterface = this;
    serviceInterface.write_file = function() {};
    serviceInterface.read_image = function() {};
    serviceInterface.read_file = function() {};
    serviceInterface.output_image = function() {};
    serviceInterface.autocorrelate = function() {};
    return serviceInterface.init = function() {
      this.that = this;
      this.that.width = this.that.autocorrelate(data, length);
      return this.that.heitht = length / this.that.width;
    };
  });

}).call(this);
