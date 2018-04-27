# -*- coding: utf-8 -*-

import networkx as nx
from math import log

from requests_toolbelt import SSLAdapter
import requests
import ssl

s = requests.Session()
s.mount('https://', SSLAdapter(ssl.PROTOCOL_TLSv1))

G = nx.DiGraph()


def populate_currencies():
    return ('BTC', 'LTC')

# filtering out positive returns, generate graphs only for -log


def create_edges():
    '''
        Must add tuples for bidirectional exchange values
        @todo Hit API for list of pairs, then use four word phrase to generate
            possible new exchange names
    '''

    # @note Scrape btc-e for list of pairs

    # collect labeles to create edges
    #endpoint = 'https://blockchain.info/ticker'
    url = 'http://api.vircurex.com/api/get_info_for_1_currency.json'
    base = 'BTC'
    alt = 'NMC'
    currencies_list = populate_currencies()
    currencies_list = [
        (base, alt),
        ('BTC', 'LTC')
    ]
    for (i, j) in currencies_list:
        endpoint = '%s?base=%s&alt=%s' % (url, i, j)
        r = s.get(endpoint)
        last_trade = r.last_trade
        if i != j:
            G.add_edges_from(
                [
                    (i, j, {'weight': -log(last_trade)}),
                ]
            )


def calc_neg(ex1="USD", ex2="BTC"):
    #nx.astar_path(G, "USD", "BTC")
    nx.negative_edge_cycle(G)
    return nx.astar_path(G, ex1, ex2)

# Determine cost effective paths

# val_map = {'A': 1.0,
           #'D': 0.5714285714285714,
           #'H': 0.0}


# nx.astar_path(G,0,4)
#values = [val_map.get(node, 0.25) for node in G.nodes()]

# Specify the edges you want here
#red_edges = [('A', 'C'), ('E', 'C')]
# edge_colours = ['black' if not edge in red_edges else 'red'
                # for edge in G.edges()]
#black_edges = [edge for edge in G.edges() if edge not in red_edges]

# Need to create a layout when doing
# separate calls to draw nodes and edges
#pos = nx.spring_layout(G)
#nx.draw_networkx_nodes(G, pos, cmap=plt.get_cmap('jet'), node_color = values)
#nx.draw_networkx_edges(G, pos, edgelist=red_edges, edge_color='r', arrows=True)
#nx.draw_networkx_edges(G, pos, edgelist=black_edges, arrows=False)
# plt.show()

if __name__ == "__main__":
    create_edges()
