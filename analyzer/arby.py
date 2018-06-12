# -*- coding:utf-8 -*-
'''
technically a bloom filter can be used to deterministically evaluate iterations
of eh statistical probabilities available to subsets of pairs within a
O(log n) - O(n)
'''

# import matplotlib.pyplot as plt
import btcelib
#import numpy as np
#import json
import math
import operator
from functools import reduce
from networkx import nx
from twisted.internet import task
from twisted.internet import reactor
from twisted.internet.defer import Deferred
#from twisted.web.client import Agent
from pprint import pprint
import time
import datetime as dt
import sys
import time
import datetime
import json
from jsonsempai import magic
from currencies import hodloo_currencies
from currencies import forex_currencies
from currencies import noeuros_currencies
from currencies import crypto_currencies
from currencies import noeth_currencies
from currencies import eth_currencies

# from graphviz import Source
# from graphviz import Digraph

# g = Digraph('G', filename='update.gv')

class DecimalEncoder(json.JSONEncoder):

    def _iterencode(self, o, markers=None):
        if isinstance(o, decimal.Decimal):
            # wanted a simple yield str(o) in the next line,
            # but that would mean a yield on the line with super(...),
            # which wouldn't work (see my comment below), so...
            return (str(o) for o in [o])
        return super(DecimalEncoder, self)._iterencode(o, markers)

trade_amount = 0
co = 0
keys = {
    'Key': 'GR9P1OAK-FOPNQSQJ-5JUHPEGK-755UGNME-429VVNDV',
    'Secret': '6b292d533cbedd795ee605b51f92f8ef38590d6f14c679764677ef51d11cdd44'
}

G = nx.DiGraph()

def namer():
    '''
    @description
    Pick a portfolio
    '''

    sel = str(sys.argv[2])

    if sel == 'hodloo_currencies':
        c = hodloo_currencies
    elif sel == 'forex_currencies':
        c = forex_currencies
    elif sel == 'noeuros_currencies':
        c = noeuros_currencies
    elif sel == 'crypto_currencies':
        c = crypto_currencies
    elif sel == 'noeth_currencies':
        c = noeth_currencies
    elif sel == 'eth_currencies':
        c = eth_currencies

    return c

def loadCurrencies():
    '''
    Build Currencies List

    List legitimate currency pairs for WEX url.

    '''

    currencies = namer()
    currencies_list = '-'.join(currencies)
    return currencies_list


def generateContext(currencies_list=None):

    '''
    Generate Context

    @param {list} currencies_list

    '''

    currencies_list = loadCurrencies()
    api = btcelib.PublicAPIv3(currencies_list)
    return api

def generateContextCalls(api=None):
    '''
    Generate Context Calls

    '''

    api = generateContext()
    exchange_rate = api.call('ticker', limit=150, ignore_invalid=1)

    ts = time.time()

    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H.%M.%S')

    # pprint(exchange_rate)

    # HOLD
    # f = open("%s.json" % (st), "a")
    # f.write(str(exchange_rate))
    # f.close()

    ds = {
        key: val['sell'] for key, val in exchange_rate.iteritems()
    }

    db = {
        key: val['buy'] for key, val in exchange_rate.iteritems()
    }

    # pprint(ds)
    # pprint(db)

    price_dict = {}

    for label, r in db.iteritems():
        base, alt = label.split("_")
        p = (base, alt, {
          'weight': -1.0 * math.log(float(r))
        })
        G.add_edges_from([p])
        # g.edge(p)
        conj = base + '_' + alt
        price_dict[conj] = float(r)

    for label, r in ds.iteritems():
        base, alt = label.split("_")
        p = (alt, base, {
          'weight': -1.0 * math.log(1 / float(r))
        })
        G.add_edges_from([p])
        # g.edge(p)
        conj = alt + '_' + base
        price_dict[conj] = 1 / float(r)

    neg_check = nx.negative_edge_cycle(G)

    return {
        'check': neg_check,
        'edge_data': dict(db.items() + ds.items()),
        'price_dict': price_dict
    }


def generate_path():
    '''
    Generate Path

    '''

    ctx = generateContextCalls()
    ub_grow = nx.astar_path(G, 'usd', 'btc')

    if ctx['check']:

        ub_moneyWalk = []

        tf = 0

        for i in ub_grow[1:]:

            item = ub_grow.index(i)

            key_finder = ub_grow[item - 1] + '_' + ub_grow[(item)]

            key = ctx['price_dict'][key_finder]

            ub_moneyWalk.append(key)

            tf += .002

        # percent growth
        # @TODO Calculate Transaction fees (.2 of 1%)
        pg = ((reduce(operator.mul, ub_moneyWalk, 1) - 1) * 100) - (tf)

        # print 'Lower: %s' % (pg,)
        # multiplied by 100 units of base currency
        pgm = 100 * reduce(operator.mul, ub_moneyWalk, 1)
        # print 'Upper %s' % (pgm,)
    else:
        # print 'Sorry, you suck. No money for you.'
        print('{}')

    return {
        'context': ctx['edge_data'],
        'grow': ub_grow,
        'lower': str(pg),
        'upper': str(pgm)
    }


def buy(pair=(), config='getInfo', context=None, last=None, timer=None):
    '''
    Buy

    '''

    global co
    global trade_amount

    trade_buy_pair = '%s_%s' % pair
    trade_rate = 0.1
    trade_type = 'buy'

    trade_amount = 100  # e.g., $100
    co += 1

    api = btcelib.TradeAPI(keys)

    if co != (timer):
        # print('Jump...')
        # print(trade_buy_pair)
        if config == 'Trade':
            c = api.call(config,
                         type=trade_type,
                         pair=trade_buy_pair,
                         rate=trade_rate,
                         amount=str(trade_amount),)
        else:
            c = api.call(config,
                         pair=trade_buy_pair,
                         count=100,)

    else:
        # print('Trade resolve...')
        # print(last)
        if config == 'Trade':
            lc = api.call(config,
                          type=trade_type,
                          pair=last,
                          rate=trade_rate,
                          amount=str(trade_amount),)
        else:
            lc = api.call(config,
                          pair=last,
                          count=100,)


def trade_buy():
    '''
    Trade Buy
    '''

    path = generate_path()
    buy_path = path['grow']
    list_values = [v for v in path.values()]
    report = {}
    report['lower'] = list_values[0]
    report['upper'] = list_values[1]
    report['grow'] = list_values[2]
    lower_stats = report['lower']
    higher_stats = report['upper']

    report['stats'] = {str(k): str(v) for k, v in list_values[3].items()}

    #config = 'Trade'
    config = 'getInfo'

    # print 'Checking...'
    print(lower_stats)
    print(higher_stats)
    # print path
    print(buy_path)

    pprint(report)

    outputfilename = '/Users/nerdfiles/Tools/Festivals/test/trading.json'
    with open(outputfilename, 'wb') as outfile:
        buy_report = json.dumps(report)
        json.dump(report, outfile)

    last_item_of_path = buy_path[(len(buy_path) - 1):][0]
    first_item_of_path = buy_path[0:1][0]
    resolve_buy_path = '%s_%s' % (last_item_of_path, first_item_of_path)
    lng = len(buy_path)

    for i in buy_path:

        if (buy_path.index(i)+1) <= len(buy_path):

            if buy_path.index(i)+1 == len(buy_path):
                buy(('', '', ), config, path['context'], resolve_buy_path, lng)
                return

            pair = (
                buy_path[buy_path.index(i)],
                buy_path[buy_path.index(i)+1],
            )

            buy(pair, config, path['context'], resolve_buy_path, lng)


def init():
    trade_buy()


class BTCELooper (object):

    '''
    BTCELooper
    '''

    def cp_process_request(self, return_obj):
        print("In callback")
        # pprint(return_obj)

    def cb_process_error(self, return_obj):
        print("In Errorback")
        # pprint(return_obj)
        self.loopstopper()

    def send_request(self):
        init()


def arbitrage():
    '''
    Arbitrage
    '''

    looper = BTCELooper()
    list_call = task.LoopingCall(looper.send_request)
    looper.loopstopper = list_call.stop

    # Every N seconds
    list_call.start(5)

    time_now = dt.datetime.now()
    t = time_now.time()

    time_given = int(sys.argv[1]) if len(sys.argv) > 1 else 10800

    delta = dt.timedelta(seconds=time_given)
    updated_timenow = (dt.datetime.combine(dt.date(1, 1, 1), t) + delta).time()

    str_timenow = t.strftime('%H:%M:%S')
    str_updated_timenow = updated_timenow.strftime('%H:%M:%S')

    def getSec(s):
        l = s.split(':')
        return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])

    startStr = str(str_timenow)
    futureStr = str(str_updated_timenow)
    fut = getSec(futureStr)
    sta = getSec(startStr)

    reactor.callLater(time_given, reactor.stop)
    reactor.run()

arbitrage()
