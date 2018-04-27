import urllib2
import json
import time
import pandas as pd
from pandas import Series, DataFrame
import os
import numpy as np
from decimal import *
from urllib2 import URLError
import btcelib

class AttrDict(dict):
    def __init__(self):
    self.__dict__ = self

keys = {
    'Key': 'GR9P1OAK-FOPNQSQJ-5JUHPEGK-755UGNME-429VVNDV',
    'Secret': '6b292d533cbedd795ee605b51f92f8ef38590d6f14c679764677ef51d11cdd44'
}

def getdata():
    cl = ['eth_btc', 'ltc_btc', 'ppc_btc']
    api = btcelib.PublicAPIv3('-'.join(cl))
    exchange_rate = api.call('depth', limit=150, ignore_invalid=1)
    return exchange_rate

def ltcbtc():
    try:
        # raw = urllib2.urlopen("http://pubapi.cryptsy.com/api.php?method=singleorderdata&marketid=3").read()
        raw = getdata()
        dictionary = raw
        # dictionary = json.loads(raw)
        #BID
        # import pdb; pdb.set_trace()
        # bidraw = dictionary['return']['LTC']['buyorders']
        newformatb = pd.DataFrame(dictionary['ltc_btc']['bids'])
        newnameb = newformatb.rename(columns={'price': 'BID'})
        global finalbid1
        finalbid1 = AttrDict()
        finalbid1.bid = newnameb[0:1]
        finalbid1.total = 150
        #ASK
        # askraw = dictionary['return']['LTC']['sellorders']
        # newformata = pd.DataFrame(askraw)
        newformata = pd.DataFrame(dictionary['ltc_btc']['asks'])
        newnamea = newformata.rename(columns={'price': 'ASK'})
        global finalask1
        finalask1 = AttrDict()
        finalask1.ask = newnamea[0:1]
        finalask1.total = 150
    except URLError, error:
        print error

def dogeltc():
    try:
        # raw = urllib2.urlopen("http://pubapi.cryptsy.com/api.php?method=singleorderdata&marketid=135").read()
        raw = getdata()
        dictionary = raw
        # dictionary = json.loads(raw)
    #BID
        # bidraw = dictionary['return']['DOGE']['buyorders']
        # newformatb = pd.DataFrame(bidraw)
        # import pdb; pdb.set_trace()
        newformatb = pd.DataFrame(dictionary['eth_btc']['bids'])
        newnameb = newformatb.rename(columns={'price': 'BID'})
        global finalbid2
        finalbid2 = AttrDict()
        finalbid2.bid = newnameb[0:1]
        finalbid2.total = 150

    #ASK
        # askraw = dictionary['return']['DOGE']['sellorders']
        # newformata = pd.DataFrame(askraw)
        newformata = pd.DataFrame(dictionary['eth_btc']['asks'])
        newnamea = newformata.rename(columns={'price': 'ASK'})
        global finalask2
        finalask2 = AttrDict()
        finalask2.ask = newnamea[0:1]
        finalask2.total = 150
    except URLError, error:
        print error

def dogebtc():
    try:

        # raw = urllib2.urlopen("http://pubapi.cryptsy.com/api.php?method=singleorderdata&marketid=132").read()
        raw = getdata()
        dictionary = raw
        # dictionary = json.loads(raw)
        # bidraw = dictionary['return']['DOGE']['buyorders']
        # newformatb = pd.DataFrame(bidraw)
        newformatb = pd.DataFrame(dictionary['ppc_btc']['bids'])
        newnameb = newformatb.rename(columns={'price': 'BID'})
        global finalbid3
        finalbid3 = AttrDict()
        finalbid3.bid = newnameb[0:1]
        finalbid3.total = 150

        # askraw = dictionary['return']['DOGE']['sellorders']
        # newformata = pd.DataFrame(askraw)
        newformata = pd.DataFrame(dictionary['ppc_btc']['asks'])
        newnamea = newformata.rename(columns={'price': 'ASK'})
        global finalask3
        finalask3 = AttrDict()
        finalask3.ask = newnamea[0:1]
        finalbid3.total = 150
    except URLError, error:
        print error

def arbitrage1():
    if True:
        capital = 10

        import pdb; pdb.set_trace()

        trade1 = capital / float(finalask2['ask'])
        currentask1 = float(finalask2['ask'])
        currentvoluem1 = float(finalask2['total'])

        #DOGE --> BTC i.e. selling DOGE
        trade2 = trade1 * float(finalbid3['bid'])
        currentbid2 = float(finalbid3['bid'])
        currentvoluem2 = float(finalbid3['total'])

        #BTC --> LTC i.e. buying LTC
        trade3 = trade2 / float(finalask1['ask'])
        currentask3 = float(finalask1['ask'])
        currentvoluem3 = float(finalask1['total'])

        PNL = trade3 - capital
        pnlp = decimal(PNL*100/capital)
        if PNL > 0:
            print "LTC/BTC undervalued: --> LTC to DOGE --> DOGE to BTC --> BTC to LTC"
            print "DOGE/LTC | ASK:",decimal(currentask1),"|Volume:", decimal(currentvoluem1),"LTC"
            print "DOGE/BTC | BID:",decimal(currentbid2),"| Volume:", decimal(currentvoluem2),"BTC"
            print "LTC/BTC | ASK:",decimal(currentask3),"| Volume:", decimal(currentvoluem3),"BTC"
            print "PNL absolut:", decimal(PNL), "PNL in %", pnlp
            vol1ltc = decimal(currentvoluem1)
            vol2ltc = currentvoluem2 / float(finalbid1['BID'])
            vol3ltc = currentvoluem3 / float(finalbid1['BID'])
            amount = min(vol1ltc, vol2ltc, vol3ltc)
            decamount = decimal(amount)
            print "Sell" ,decamount, "LTC"

def decimal(x):
    x = Decimal(x).quantize(Decimal('.000000001'), rounding=ROUND_DOWN)
    return x

while True:
    print "...Looking for triangular arbitrage opportunity", time.strftime('%I:%M:%S %p %Z')
    print
    ltcbtc()
    dogeltc()
    dogebtc()
    arbitrage1()
    time.sleep(2)
