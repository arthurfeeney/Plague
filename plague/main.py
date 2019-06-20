import certifi
import urllib3
from automata import AbsoluteURLFinder, RelativeURLFinder
import crawler as crawler
from frontier import FIFOFrontier
from ust import SetUST


def main():
    url = ['https://reddit.com', 'https://stackoverflow.com']
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                               ca_certs=certifi.where())
    A = RelativeURLFinder()
    f = FIFOFrontier()
    ust = SetUST()
    c = crawler.Crawler(http, url, A, f, ust)

    for i in range(64):
        c.crawl()
    for url in c.view_ust():
        print(url)
    print(len(c.view_frontier()))
    print(len(c.view_ust()))


if __name__ == "__main__":
    main()
