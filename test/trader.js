/**
 * @fileOverview Opp and Finder
 */

var schedule = require('node-schedule');
var sheetsu = require('sheetsu-node');
var request = require('request');
var async = require('async');
var btoa = require('btoa');
var fs = require('fs');
var qs = require('querystring');
var exec = require('child_process').exec;
var R = require('ramda');
var _ = require('lodash');



var API_KEY = '9eq7ozkrpzxFnoyb4tpE';
var API_SECRET = 'VfGY3L7EeGzMqsRUky7yh7ViX2cabwGxMsG3oFsf';
var keyPair = API_KEY + ":" + API_SECRET;

var client_sheet = sheetsu({
  address    : '45f5f219183c',
  api_key    : API_KEY,
  api_secret : API_SECRET
});

var init = function () {

  exec("cat trading.json", {
    cwd: '/Users/nerdfiles/Tools/Festivals/test'
  }, function(error, stdout, stderr) {

    var requests = [];
    var d = JSON.parse(stdout);

    _.each(d, function (coin) {

      var j;
      var callback;
      requests.push(function (callback) {

        var btcusd = R.view(R.lensProp('btc_usd'), d.stats);
        var rows = [];
        var opp = {
          "spread" : ''+( parseFloat(d.lower) - parseFloat(d.upper) ) - 100,
          "grow"   : d.grow.join(' '),
          "btcusd" : btcusd
        };

        rows.push(opp);
        console.log(rows);

      });
    });

    async.series(requests, function (err, result) {
      console.log('Update historical data on currency pair', result);
    });

  });

};

var j = schedule.scheduleJob('*/5 * * * * *', function () {
  init();
}); // @see https://sheetsu.com/docs/beta#rates

init();



