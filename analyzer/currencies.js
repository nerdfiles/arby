var _ = require('lodash')
var pick = require('es6-pick')

/**
 * @name Currencies
 * @returns {undefined}
 */
function Currencies(dataList) {
  var currencies = dataList.join('-')
  var contexts = []
  var context = {
    'btc_usd': () => {}
  }
  contexts.push(context)
  var selectCurrencyPair = _.map(dataList, (pair) => {
    return _.pick(contexts, pair)
  })

  return currencies

  ////////////

  /**
   * @name buy
   * @returns {undefined}
   */
  function buy() {}

  /**
   * @name contextCall
   * @returns {undefined}
   */
  function contextCall() {}

  /**
   * @name generateContextCall
   * @returns {undefined}
   */
  function generateContextCall() {}

  /**
   * @name path
   * @returns {undefined}
   */
  function path() {}

  /**
   * @name init
   * @returns {undefined}
   */
  function init() {}

  /**
   * @name loadCurrencies
   * @returns {undefined}
   */
  function loadCurrencies() {
  }
}
module.exports = Currencies
