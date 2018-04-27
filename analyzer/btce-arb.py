# -*- coding: utf-8 -*-

import json
import urllib2
import requests
import math
import operator
from networkx import *
from functools import reduce
from pprint import pprint
import pygraphviz as pgv

# Define Graph
G = nx.DiGraph()
#A = to_agraph(G)
#X1 = from_agraph(A)


def loadCurrencies():
    '''
    Build Currencies List
    '''
    # list legitimate currency pairs for btc-e url
    currencies = ['btc_usd',
                  'btc_rur',
                  'btc_eur',
                  'ltc_btc',
		  'ltc_usd',
                  'ltc_rur',
                  'ltc_eur',
                  'nmc_btc',
                  'nmc_usd',
                  'nvc_btc',
                  'nvc_usd',
                  'usd_rur',
		  'eur_usd',
                  'eur_rur',
                  'ppc_btc',
                  'ppc_usd',
		  'dsh_btc',
		  'eth_btc',
		  'eth_usd',
		  'eth_ltc',
                  'eth_rur',]

    return currencies

price_dict = {}

def api_wrap(url='https://btc-e.com/api/2/%s/ticker'):
    '''
    API Wrap should store data via Firebase. Use angularFire.

    |------------------------|
    |                        |
    |                        |
    |                        |
    |                        |
    |                        |
    |                        |
    |                        |
    |                        |
    |                        |
    |                        |
    |------------------------|

    Imagine Cantor's Proof for a Slingshot Assertion which might yield nothing
    beyond it.
    '''

    # list of exchange rates
    exchange_rates = []

    # Pull ticker data, transform into json,
    # fill exchange_rate array

    for i in loadCurrencies():
        _url = url % (i)
        #response = urllib2.urlopen(_url)
        response = requests.get(_url, verify=False)
        ticker = response.content
        res = json.loads(ticker)

        prices = res['ticker']

        high = prices['high']
        low = prices['low']
        avg = prices['avg']

        vol = prices['vol']
        vol_cur = prices['vol_cur']

        last = prices['last']
        buy = prices['buy']
        sell = prices['sell']

        updated = prices['updated']
        server_time = prices['server_time']

        exchange_rates.append(last)

    return {
        'exchange_rates': exchange_rates,
        'price_table': price_dict
    }


def checker(ex = None):
    '''
    Checker
    '''
    currencies = loadCurrencies()
    # split curriencs, add market price from api into price_dict
    # define a function to reduce redundancy

    for i in currencies:
        base, alt = currencies[currencies.index(i)].split("_")
        for r in ex['exchange_rates']:
            if currencies.index(i) == ex['exchange_rates'].index(r):
                conjoined = base + '_' + alt
                G.add_edges_from([
                    (
                        base,
                        alt,
                        {'weight': -1.0 * math.log(float(r))}
                    )
                ])
                ex['price_table'][conjoined] = float(r)
                #print conjoined, price_dict[conjoined]

    for i in currencies:
        base, alt = currencies[currencies.index(i)].split("_")
        for r in ex['exchange_rates']:
            if currencies.index(i) == ex['exchange_rates'].index(r):
                conjoined = alt + '_' + base
                G.add_edges_from([
                    (
                        alt,
                        base,
                        {'weight': -1.0 * math.log(1 / float(r))}
                    )
                ])
                ex['price_table'][conjoined] = 1 / float(r)
                #print conjoined, price_dict[conjoined]

    #import pdb; pdb.set_trace()

    # check for negative edge cycle
    neg_check = nx.negative_edge_cycle(G)

    return neg_check


def init(ex = None):
    '''
    Init
    '''
    neg_check = checker(ex)

    # nx.draw_graphviz(G)
    #nx.write_dot(G, 'graph.dot')

    if neg_check:
        print("Let's arb it up!")
        ub_grow = nx.astar_path(G, 'usd', 'btc')
        print ub_grow

        # A.write('graph.dot')

        #bu_grow = nx.astar_path(G, 'btc', 'usd')
        #ul_grow = nx.astar_path(G, 'usd', 'ltc')
        #lu_grow = nx.astar_path(G, 'ltc', 'usd')
        #bl_grow = nx.astar_path(G, 'btc', 'ltc')
        #lb_grow = nx.astar_path(G, 'ltc', 'btc')

        #bu_moneyWalk = []
        #for i in bu_grow[1:]:
            #key_finder = bu_grow[bu_grow.index(i) - 1] + '_' + bu_grow[(bu_grow.index(i))]
            #if key_finder in locals():
                #bu_moneyWalk.append(ex['price_table'][key_finder])

        # percent growth
        #print (reduce(operator.mul, bu_moneyWalk, 1) - 1) * 100
        # multiplied by 100 units of base currency
        #print 100 * reduce(operator.mul, bu_moneyWalk, 1)

        # create list of short path nodes for math purposes
        # define a function for this, to be reusable for other pairs
        ub_moneyWalk = []
        #pprint(ex['price_table'])
        for i in ub_grow[1:]:
            key_finder = ub_grow[ ub_grow.index(i) - 1 ] + '_' + ub_grow[ (ub_grow.index(i)) ]
            key = ex['price_table'][key_finder]
            ub_moneyWalk.append(key)

        print ex['price_table']['btc_usd']
        ub_moneyWalk.append(ex['price_table']['btc_usd'])

        # percent growth
        print (reduce(operator.mul, ub_moneyWalk, 1) - 1) * 100
        # multiplied by 100 units of base currency
        print 100 * reduce(operator.mul, ub_moneyWalk, 1)

if __name__ == "__main__":
    print 'Are you ready to arb?'
    ex = api_wrap()
    init(ex)
