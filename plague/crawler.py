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

    def crawl(self):
        current_url = self.frontier.get()

        html = self.__html_str(current_url)
        new_urls = self.url_finder.urls(html, current_url)

        # insert new urls that have not been seen to the frontier
        for url in new_urls:
            if not url in self.ust:
                self.frontier.add(url)
                self.ust.add(url)
