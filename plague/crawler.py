class Crawler(object):
    def __init__(self, http, seed_url, url_finder, frontier, ust):
        self.http = http
        self.seed_url = seed_url
        self.url_finder = url_finder
        self.frontier = frontier
        self.frontier.add_many(self.seed_url)  # start with the seed url
        self.ust = ust

    def view_frontier(self):
        return self.frontier.view_frontier()

    def view_ust(self):
        return self.ust.view()

    def __html_str(self, url):
        r = self.http.request('GET', url)
        html = r.data.decode('utf-8')
        return html

    def __get_page(self):
        url = self.frontier.get()
        #html = self.__html_str(current_url.strip())
        try:
            r = self.http.request('GET', url)
        except:
            return self.__get_page()
        #html = r.data.decode('utf-8')
        while r.status != 200:
            url = self.frontier.get()
            try:
                r = self.http.request('GET', url)
            except:
                return self.__get_page()
        try:
            html = r.data.decode('utf-8')
        except:
            return self.__get_page()
        return html, url

    def __remove_slash(self, url):
        return url.replace('/', '_^_')

    def crawl(self, download_path=None, graph=None):
        #current_url = self.frontier.get()
        html, current_url = self.__get_page(
        )  #self.__html_str(current_url.strip())

        if download_path:
            # don't want / in file name
            f_name = self.__remove_slash(current_url)
            f = open(download_path + f_name, 'w+')
            f.write(html)
            f.close()

        new_urls = self.url_finder.urls(html, current_url)

        if graph is not None:
            graph.add_edges_from([(current_url, other) for other in new_urls])

        # insert new urls that have not been seen to the frontier
        for url in new_urls:
            if not url in self.ust:
                self.frontier.add(url)
                self.ust.add(url)
