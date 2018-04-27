# coding: utf-8
# python: 2.7.3
# module: btcelib.py <http://pastebin.com/kABSEyYB>

# Copyright (c) 2014 by John Saturday <stozher@gmail.com>.
# The MIT License (MIT) <http://opensource.org/licenses/MIT>.
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

# Please feel free to donate some coins:
# BTC: 13buUVsVXG5YwhmP6g6Bgd35WZ7bKjJzwM
# LTC: Le3yV8mA3a7TrpQVHzpSSkBmKcd2Vw3NiR

"""\
BTC-E Trade API v1 and Public API v3

Copyright (c) 2014 by John Saturday <stozher@gmail.com>.
The MIT License (MIT) <http://opensource.org/licenses/MIT>.

BTC-E IS NOT AFFILIATED WITH THIS PROJECT; THIS IS A COMPLETELY
INDEPENDENT IMPLEMENTATION BASED ON THE BTC-E API DESCRIPTION.

Trade API v1 <https://wex.nz/tapi/docs>.
Public API v3 <https://wex.nz/api/3/docs>.

EXAMPLES:
>>> import btcelib
>>> api = btcelib.PublicAPIv3('btc_usd-ltc_btc')
>>> api.call('depth', limit=150, ignore_invalid=1)
... <OUTPUT>
>>> tapi = btcelib.TradeAPIv1({'Key': <>, 'Secret': <>})
>>> tapi.call('TradeHistory', pair='btc_usd', count=1000)
... <OUTPUT>

CLASSES:
    exceptions.Exception(exceptions.BaseException)
        APIError
    __builtin__.object
        BTCEConnection
            TradeAPIv1
                TradeAPI
            PublicAPIv2
                PublicAPI
            PublicAPIv3

exception btcelib.APIError
    Raise exception when the API returned an error.

class btcelib.BTCEConnection([compr[, timeout]])
    HTTPS persistent connection to the Trade/Public API.

    BTCEConnection.apirequest(url[, apikey[, **params]])
    BTCEConnection.jsonrequest(url[, apikey[, **params]])

    BTCEConnection.conn - shared connection between pairs and methods
    BTCEConnection.resp - last response <type 'httplib.HTTPResponse'>

class btcelib.TradeAPIv1(apikey[, compr[, timeout]])
    BTC-E Trade API v1.

    TradeAPIv1.call(method[, **params]) - method: getInfo || Trade ||
    ActiveOrders || OrderInfo || CancelOrder || TradeHistory ||
    TransHistory; params: param1=value1, param2=value2, ...

class btcelib.PublicAPIv2(pair[, compr[, timeout]])
    BTC-E Public API v2 - don't use, will be REMOVED soon!

    PublicAPIv2.call(method) - method: fee || ticker || trades || depth

class btcelib.PublicAPIv3([pair[, compr[, timeout]]])
    BTC-E Public API v3.

    PublicAPIv3.call(method[, **params]) - method: info || ticker ||
    depth || trades; params: ignore_invalid=1, limit=150 (max 2000)
"""

__date__ = "Tue, 21 Oct 2014 11:35:20 EEST"
__author__ = """John Saturday <stozher@gmail.com> BTC: 13buUVsVXG5YwhmP6g6Bgd35WZ7bKjJzwM LTC: Le3yV8mA3a7TrpQVHzpSSkBmKcd2Vw3NiR"""
__credits__ = "Alan McIntyre <https://github.com/alanmcintyre>"


import httplib
from decimal import Decimal

API_NN = 2             # : refresh time of the API (seconds)
CONN_TIMEOUT = 30      # : HTTPS connection timeout (seconds)

CF_COOKIE = '__cfduid' # : CloudFlare security cookie
BTCE_HOST = 'wex.nz'   # : BTC-E host (HTTPS connection)

JSON_PARSER = Decimal  # : JSON float and integer data parser

class APIError(Exception):
    """\
    Raise exception when the API returned an error."""
    pass

class BTCEConnection(object):
    """\
    HTTPS persistent connection to the Trade/Public API.
    @cvar conn: shared connection between pairs and methods
    @cvar resp: last response <type 'http.HTTPResponse'>"""

    #: default HTTPS headers
    _headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Accept': 'application/json',
            'Accept-Charset': 'utf-8'}
    #: POST only HTTPS headers
    _post_headers = {
            'Content-Type': 'application/x-www-form-urlencoded'}

    conn = None    #: shared connection between pairs and methods
    resp = None    #: last response <type 'httplib.HTTPResponse'>

    def __init__(self, compr=True, timeout=CONN_TIMEOUT):
        """\
        @param compr: connection compression (gzip, deflate)
        @param timeout: HTTPS connection timeout (seconds)
        @note: class connection compression and timeout"""

        self._compr = compr        #: HTTPS compression <type 'bool'>
        self._timeout = timeout    #: connection timeout <type 'int'>

        if self._compr:
            BTCEConnection._headers.update({
                    'Accept-Encoding': 'gzip, deflate'})
        else:
            BTCEConnection._headers.update({
                    'Accept-Encoding': 'identity'})

        if BTCEConnection.conn:
            BTCEConnection.conn.timeout = self._timeout
        else:
            BTCEConnection.conn = httplib.HTTPSConnection(
                    BTCE_HOST, strict=True, timeout=self._timeout)

    @classmethod
    def _cfcookie(cls):
        """\
        @raise RuntimeWarning: Missing CloudFlare '%s' cookie"""

        import Cookie
        import warnings

        cookie_header = cls.resp.getheader('Set-Cookie')
        try:
            cfcookie = Cookie.SimpleCookie(cookie_header)[CF_COOKIE]
        except (KeyError, Cookie.CookieError):
            if 'Cookie' not in cls._headers:
                message = "Missing CloudFlare '%s' cookie" % CF_COOKIE
                warnings.warn(message, RuntimeWarning, stacklevel=2)
        else:
            cls._headers.update({
                    'Cookie': cfcookie.OutputString('value')})

    @classmethod
    def _signature(cls, apikey, encoded_params):
        """\
        @param apikey: Trade API Key {'Key': <>, 'Secret': <>}
        @param encoded_params: Trade API method and parameters"""

        import hmac
        import hashlib

        signature = hmac.new(apikey['Secret'],
                msg=encoded_params, digestmod=hashlib.sha512)
        cls._post_headers.update({
                    'Key': apikey['Key'],
                    'Sign': signature.hexdigest()})

    @classmethod
    def apirequest(cls, url, apikey=None, **params):
        """\
        @param url: Trade/Public API URL without parameters
        @param apikey: Trade API Key {'Key': <>, 'Secret': <>}
        @param **params: Trade/Public API method and/or parameters
        @return: response body / JSON data <type 'str'>"""

        import zlib
        import urllib

        headers = cls._headers
        if 'tapi' in url:
            method = 'POST'
            encoded_params = urllib.urlencode(params)
            cls._signature(apikey, encoded_params)
            headers.update(cls._post_headers)
        else:
            method = 'GET'
            if params:
                url += '?%s' % urllib.urlencode(params)
            encoded_params = None

        while True:
            try:
                cls.conn.request(method, url, encoded_params, headers)
                cls.resp = cls.conn.getresponse()
            # XXX: <http://bugs.python.org/issue15082>, timeout, etc.
            except httplib.BadStatusLine:
                cls.conn.close()
                continue
            # IOError: ssl.SSLError, socket.error (gaierror, etc.)
            except (IOError, httplib.HTTPException):
                cls.conn.close()
                raise
            else:
                cls._cfcookie()
                break    # while exit: no errors

        jsondata = cls.resp.read()
        encoding = cls.resp.getheader('Content-Encoding')
        if encoding == 'gzip':
            jsondata = zlib.decompress(jsondata, zlib.MAX_WBITS+16)
        elif encoding == 'deflate':
            jsondata = zlib.decompress(jsondata, -zlib.MAX_WBITS)
        return jsondata

    @classmethod
    def jsonrequest(cls, url, apikey=None, **params):
        """\
        @raise APIError: when the API returned an error
        @return: parsed JSON data <type 'dict'>
        @see: BTCEConnection.apirequest"""

        import json

        data = json.loads(cls.apirequest(url, apikey, **params),
                parse_float=JSON_PARSER, parse_int=JSON_PARSER)
        try:
            message = data['error']
        except (KeyError, TypeError):
            return data    # method exit: no errors
        else:
            raise APIError(message)

class TradeAPIv1(BTCEConnection):
    """\
    BTC-E Trade API v1.
    @see: <https://wex.nz/tapi/docs>"""

    def __init__(self, apikey, **connkw):
        """\
        @param apikey: Trade API Key {'Key': <>, 'Secret': <>}
        @see: btcelib.BTCEConnection"""

        BTCEConnection.__init__(self, **connkw)
        self.apikey = apikey    #: Trade API Key <type 'dict'>
        self._nonce = None      #: incremental POST parameter (int>0)

    def _nextnonce(self):
        """\
        @return: 'nonce' POST parameter <type 'int'>"""

        import re

        # 'nonce' automatic detection
        if not self._nonce:
            try:
                self.jsonrequest('/tapi', self.apikey, nonce=None)
            except APIError as error:
                if 'invalid nonce' in error.message:
                    self._nonce = int(
                            re.search(r'\d+', error.message).group())
                else:
                    raise APIError(error.message)    # other errors

        self._nonce += 1
        return self._nonce

    def call(self, method, **params):
        """\
        @param method: 'getInfo' || 'Trade' || 'ActiveOrders' ||
        'OrderInfo' || 'CancelOrder' || 'TradeHistory' || 'TransHistory'
        @param **params: [param1=value1[, param2=value2[, ...]]]
        @return: <https://wex.nz/tapi/docs>"""

        url = '/tapi'
        params = params or {}
        params.update({'method': method, 'nonce': self._nextnonce()})
        return self.jsonrequest(url, self.apikey, **params)['return']

class TradeAPI(TradeAPIv1):
    """\
    BTC-E Trade API v1 - backward compatibility."""
    pass

class PublicAPIv2(BTCEConnection):
    """\
    BTC-E Public API v2 - don't use, will be REMOVED soon!"""

    def __init__(self, pair, **connkw):
        """\
        @param pair: 'btc_usd' || 'ltc_btc' || 'ltc_usd' || ...
        @see: btcelib.BTCEConnection"""

        BTCEConnection.__init__(self, **connkw)
        self.pair = pair    #: currency pair <type 'str'>

    def call(self, method):
        """\
        @param method: 'fee' || 'ticker' || 'trades' || 'depth'
        @return: <https://wex.nz/api/2/btc_usd/fee>
        @return: <https://wex.nz/api/2/btc_usd/ticker>
        @return: <https://wex.nz/api/2/btc_usd/trades>
        @return: <https://wex.nz/api/2/btc_usd/depth>"""

        url = '/api/2/%s/%s' % (self.pair, method)
        return self.jsonrequest(url)

class PublicAPI(PublicAPIv2):
    """\
    BTC-E Public API v2 - backward compatibility."""
    pass

class PublicAPIv3(BTCEConnection):
    """
    BTC-E Public API v3.
    @see: <https://wex.nz/api/3/docs>
    """

    def __init__(self, pair=None, **connkw):
        """\
        @param pair: '[btc_usd[-ltc_btc[-ltc_usd[-...]]]]'
        @see: btcelib.BTCEConnection"""

        BTCEConnection.__init__(self, **connkw)
        self.pair = pair or ''    #: currency pairs <type 'str'>

        # all pairs: 'btc_usd-ltc_btc-ltc_usd-...'
        if not self.pair:
            info = self.call('info')
            self.pair = '-'.join(info['pairs'].iterkeys())

    def call(self, method, **params):
        """\
        @param method: 'info' || 'ticker' || 'depth' || 'trades'
        @param **params: [ignore_invalid=1[, limit=150 (max 2000)]]
        @return: <https://wex.nz/api/3/docs>"""

        if method == 'info':
            url = '/api/3/%s' % method
        else:
            url = '/api/3/%s/%s' % (method, self.pair)
        return self.jsonrequest(url, **params)

