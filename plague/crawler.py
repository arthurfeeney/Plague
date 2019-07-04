import socket
import plague.url_util as uu


class Crawler(object):
    def __init__(self, http, seed_url, url_finder, frontier, ust, exclusion):
        self.http = http
        self.seed_url = seed_url
        self.url_finder = url_finder
        self.frontier = frontier
        self.frontier.add_many(self.seed_url)  # start with the seed url
        self.ust = ust
        self.exclusion = exclusion
        self.dns_cache = {}  # domain name -> ip-address
        self.num_url_crawled = 0

    def view_frontier(self):
        return self.frontier.view_frontier()

    def view_ust(self):
        return self.ust.view()

    def crawl_count_sites(self,
                          count,
                          download_path=None,
                          graph=None,
                          verbose=True):
        for i in range(count):
            self.crawl(count, download_path, graph, verbose)

    def crawl(self, count, download_path=None, graph=None, verbose=True):
        html, current_url = self.__get_page()
        self.num_url_crawled += 1
        if verbose:
            print('count: {num}/{denom}\t'
                  'site: {site}\t'.format(num=self.num_url_crawled,
                                          denom=count,
                                          site=current_url))

        if download_path:
            self.__download_page(download_path, current_url, html)

        new_urls = self.url_finder.urls(html, current_url)

        if graph is not None:
            graph.add_edges_from([(current_url, other) for other in new_urls])

        self.add_new_urls(new_urls)

    def add_new_urls(self, new_urls):
        # insert new urls that have not been seen to the frontier
        for url in new_urls:
            if not url in self.ust:  #and self.exclusion.test_url(url):
                self.frontier.add(url)
                self.ust.add(url)

    def __get_page(self):
        url = self.frontier.get()
        #url = self.__dns_lookup(url)
        try:
            # attempt connecting, downloading, and decoding the page
            r = self.http.request('GET', url, timeout=2.5)
            if r.status != 200:
                # if the site didn't respond successfully, try the next page.
                return self.__get_page()
            html = r.data.decode('utf-8')
        except:
            # if something went wrong, just try the next site
            return self.__get_page()
        return html, url

    def __dns_lookup(self, url):
        domain = uu.remove_protocol(uu.domain_name(url))
        if domain in self.dns_cache:
            # replace domain name with ip if its in the cache
            url = url.replace(domain, self.dns_cache[domain])
        else:
            # if domain name not in cache, add it
            self.dns_cache[domain] = socket.gethostbyname(domain)
        return url

    def __remove_slash(self, url):
        return url.replace('/', '_^_')

    def __download_page(self, download_path, url, html):
        f_name = self.__remove_slash(url)
        f = open(download_path + f_name, 'w+')
        f.write(html)
        f.close()
