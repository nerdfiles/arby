var express = require('express');

/**
 * @name Analyzer
 * @returns {undefined}
 */
function Analyzer() {
  var vm = express();
  vm.use((request, response, next) => {
    request.currencies = [
      'btc_usd',
      'btc_ltc'
    ]
    response.json = () => {
      var status = 200
      return (currencyController, dataList) => {
        var dataList = dataList || request.currencies
        var entity = require(path.join('.', currencyController))(dataList)
        var obj = entity
        return response.json(status, obj)
      }
    }
    return next()
  })
  vm.get('/currencies', (request, response) => {
    response.json()('currencies', request.currencies)
  })
  function action() {
    return (defaultAction) => {
      return {
        key: "trade_buy"
      }
    }
  }
  vm.listen(port, () => {
    console.log()
  })
}
module.exports = Analyzer;
