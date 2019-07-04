import plague.url_util as uu


#
# abstract base class for finding urls
#
class URLFinder():
    def __init__(self):
        pass

    def urls(self, html, current_url):
        # abstract function implemented in derived class.
        raise NotImplementedError('URLFinder.find_urls not implemented.')

    def find_urls(self, html):
        # automata-ish thing that looks for all <a ... href=...
        # in the input html string
        # This seems pretty linear.
        urls = []

        idx = 0
        while idx < len(html):
            word_len = 0
            if html[idx + word_len] == '<':
                word_len += self.next_char(html, idx + word_len)
                if html[idx + word_len] == 'a':
                    f_url, b_url = self.find_url(html, idx + word_len)

                    if (f_url, b_url) != (-1, -1):
                        urls.append(html[f_url:b_url + 1])
                        idx = b_url + 1
                    else:
                        idx += word_len
                else:
                    idx += word_len
            else:
                idx += 1
        return urls

    def find_url(self, html, front):
        # return the start and end index of url.
        # returns -1, -1 when it "fails"

        # find the index of "h" in "href." Return failure if it isn't found
        h_index = self.find_href(html, front)
        if h_index == -1:
            return -1, -1

        # find the starting quote that wraps around the url.
        start = self.find_quote(html, front)
        if start == -1:
            return -1, -1

        # find the closing quote around the url.
        end = self.find_quote(html, start + 1)
        if end == -1:
            return -1, -1

        return start + 1, end - 1

    def find_quote(self, html, front):
        idx = front
        while idx < len(html) and html[idx] != '"' and html[idx] != '\'':
            if html[idx] == '>':
                # if it reachers a > before a quote, then it is probably
                # poorly written html.
                return -1
            idx += 1
        return idx if idx < len(html) else -1

    def find_href(self, html, front):
        # another weird automata thing that looks for 'href' in the
        # html stirng. For the first found occurence, it returns
        # the index of the h.
        idx = front
        while idx < len(html) - len('href') + 1 and html[idx] != '>':
            word_len = 0
            if html[idx + word_len] == 'h':
                word_len += 1
                if html[idx + word_len] == 'r':
                    word_len += 1
                    if html[idx + word_len] == 'e':
                        word_len += 1
                        if html[idx + word_len] == 'f':
                            return idx
                idx += word_len
            else:
                idx += 1
        # no href found
        return -1

    def next_char(self, html, idx):
        # starting at idx, this returns the offset from index of the next
        # non-whitespace character. If idx is at 95 and the next char is at
        # 100, this function returns 5.
        offset = 1
        while idx + offset < len(html) and html[idx + offset].isspace():
            offset += 1
        return offset


#
# Derived class that only finds the Absolute urls.
#
class AbsoluteURLFinder(URLFinder):
    def __init__(self):
        super(AbsoluteURLFinder, self).__init__()

    def urls(self, html, current_url):
        # current_url is not needed for this class. For modularity, it
        # needs to be passed in anyway.
        return self.__unique_absolute(self.find_urls(html))

    def __unique_absolute(self, urls):
        absolute = ([
            url for url in urls if 'https://' in url or 'http://' in url
        ])
        return list(set(absolute))


#
# TotalURLFinder tries to get absolute and some of the relative urls.
#
class RelativeURLFinder(URLFinder):
    def __init__(self):
        super(RelativeURLFinder, self).__init__()

    def urls(self, html, current_url):
        current_domain = uu.domain_name(current_url)
        if current_domain is None:
            raise Exception('RelativeURLFinder.urls: current_domain is None'
                            'given the url: ' + str(current_url))
        dirty_urls = self.find_urls(html)
        return self.__get_clean_urls(current_domain, dirty_urls)

    def __get_clean_urls(self, current_domain, dirty_urls):
        # the retrieved urls may not be valid or easily crawled.
        # This only gets the ones that are likely to work.
        abs_urls = []
        for url in dirty_urls:
            if not '.' in url[-4:]:
                if len(url) > 7 and ('https://' in url or 'http://' in url):
                    abs_urls.append(url)
                elif len(url) > 0 and url[0] == '/':
                    abs_urls.append(current_domain + url)
        return list(set(abs_urls))
