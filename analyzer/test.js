
var log = console.log
Object.prototype.create = function() {
  var self = this
  log('a')
  return self
}

/**
 * __reverse__
 *
 * @param head
 * @returns {undefined}
 */
function __reverse__(head) {
  var h, q, p

  if (!head) {
    return head
  }

  h = head
  q = null
  p = h.hext

  while (p) {
    h.next = q
    q = h
    h = p
    p = h.next
  }

  h.next = q

  return h
}

var DList = {
  init: function(niList) {
    var self = this
    if (niList)
      _.extend(self, niList)
    return self
  },
  reverse: __reverse__
}

var tinylist = Object.create(DList).init()

var Model = {},
  Operation = {},
  View = {},
  Event = {}

Model.__init__ = function() {
  return 'a'
}

var m = Object.create(Model)
