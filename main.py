import certifi
import urllib3
from plague.automata import AbsoluteURLFinder, RelativeURLFinder
import plague.crawler as crawler
from plague.frontier import *
from plague.ust import *
from plague.exclusion import *
import matplotlib.pyplot as plt
import networkx as nx


def main():
    url = ['https://w3schools.com', 'https://stackoverflow.com']
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                               ca_certs=certifi.where())
    A = RelativeURLFinder()
    #f = MemoryDomainPriorityFrontier(limit=None)
    f = memory_seen_priority_frontier(limit=None)
    ust = BloomFilter(.01, 2000)
    exclusion = Exclusion()
    #ust = DiskBloomFilter(.1, 10000, './',
    #                      'ust.dat')  #BloomFilter(.1, 10000)  #SetUST()
    c = crawler.Crawler(http, url, A, f, ust, exclusion)

    G = nx.Graph()

    c.crawl_count_sites(count=4000, download_path=None, graph=G)

    remove = [node for node, degree in G.degree() if degree < 2]
    G.remove_nodes_from(remove)

    print('drawing graph')
    nx.drawing.nx_pylab.draw_kamada_kawai(G,
                                          node_size=5,
                                          node_color='r',
                                          alpha=0.5)
    plt.show()


if __name__ == "__main__":
    main()
