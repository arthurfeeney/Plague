import certifi
import urllib3
from plague.automata import AbsoluteURLFinder, RelativeURLFinder
import plague.crawler as crawler
from plague.frontier import FIFOFrontier, DomainPriorityFrontier
from plague.ust import SetUST, BloomFilter, SimpleDiskUST
import matplotlib.pyplot as plt
import networkx as nx


def main():
    url = ['https://w3schools.com', 'https://stackoverflow.com']
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                               ca_certs=certifi.where())
    A = RelativeURLFinder()
    f = DomainPriorityFrontier(limit=50)  #FIFOFrontier()
    ust = SimpleDiskUST('./', 'ust.dat')  #BloomFilter(.1, 10000)  #SetUST()
    c = crawler.Crawler(http, url, A, f, ust)

    G = nx.Graph()

    c.crawl_count_sites(count=50, download_path=None, graph=None)
    #for url in c.view_frontier():
    #    print(url)
    #print(len(c.view_frontier()))
    '''
    nx.drawing.nx_pylab.draw_kamada_kawai(G,
                                          node_size=10,
                                          node_color='r',
                                          alpha=0.5)
    plt.show()
    '''


if __name__ == "__main__":
    main()
