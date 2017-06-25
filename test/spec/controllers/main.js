'use strict';

describe('ctrl', function () {
  beforeEach(module('arbyApp'));
  var ctrl, $scope;
  beforeEach(inject(function ($controller, $rootScope) {
    $scope = $rootScope.$new();
    ctrl = $controller('btcCtrl', {
      $scope: $scope
    });
  }));

  it('check spread', function () {
    expect($scope.spread.toPrecision(3)).toBe(0.004);
  });
});
