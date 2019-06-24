#
# abstract base class
#
class URLFinder():
    def __init__(self):
        pass

    def next_char(self, html, idx):
        # starting at idx, this returns the offset from index of the next
        # non-whitespace character. If idx is at 95 and the next char is at
        # 100, this function returns 5.
        offset = 1
        while idx + offset < len(html) and html[idx + offset].isspace():
            offset += 1
        return offset

    def find_href(self, html, front):
        # another weird automata thing that looks for 'href' in the
        # html stirng. For the first found occurence, it returns
        # the index of the h.
        idx = front
        while idx < len(html) - len('href') + 1:
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

    def find_quote(self, html, front):
        idx = front
        while idx < len(html) and html[idx] != '"' and html[idx] != '\'':
            idx += 1
        return idx if idx < len(html) else -1

    def find_url(self, html, front):
        # return the start and end index of url.
        h_index = self.find_href(html, front)
        # no href was found
        if h_index == -1:
            return -1, -1

        start = self.find_quote(html, front)

        # find failed to find anything, so it returns - 1
        if start == h_index - 1:
            return -1, -1

        end = self.find_quote(html, start + 1)

        # did not find a closing quote
        if end == len(html):
            return -1, -1

        return start + 1, end - 1

    def find_urls(self, html):
        # automata-ish thing that looks for all <a ... href=...
        # (I don't think this is regular, so not really an FSA)
        # in the input html string

        urls = []

        idx = 0
        while idx < len(html):
            word_len = 0
            if html[idx + word_len] == '<':
                word_len += self.next_char(html, idx + word_len)
                if html[idx + word_len] == 'a':
                    f_url, b_url = self.find_url(html, idx + word_len)

                    if (f_url, b_url) == (-1, -1):
                        raise Exception('automate failed to find closing'
                                        'quote for url starting at {}'\
                                        .format(idx + word_len))

                    # adding +1 to f_url removes quotes ""
                    urls.append(html[f_url:b_url + 1])
                    idx = b_url + 1
                else:
                    idx += word_len
            else:
                idx += 1
        return urls

    def urls(self, html, current_url):
        # abstract function implemented in derived class.
        raise NotImplementedError('URLFinder.find_urls not implemented.')


#
# Derived class that only finds the Absolute urls.
#
class AbsoluteURLFinder(URLFinder):
    def __init__(self):
        super(AbsoluteURLFinder, self).__init__()

    def __unique_absolute(self, urls):
        absolute = ([
            url for url in urls if 'https://' in url or 'http://' in url
        ])
        return list(set(absolute))

    def urls(self, html, current_url):
        # current_url is not needed for this class. For modularity, it
        # needs to be passed in anyway.
        return self.__unique_absolute(self.find_urls(html))


#
# TotalURLFinder tries to get absolute and some of the relative urls.
#
class RelativeURLFinder(URLFinder):
    def __init__(self):
        super(RelativeURLFinder, self).__init__()

    def domain_name(self, absolute_url):
        # takes an absolute url, such as https://youtube.com/hithere
        # and returns https://youtube.com
        if 'https://' in absolute_url:
            end = absolute_url[len('https://'):].find('/')
            if end == -1:
                return absolute_url
            return absolute_url[:end + len('https://')]
        elif 'http://' in absolute_url:
            end = absolute_url[len('http://'):].find('/')
            if end == -1:
                return absolute_url
            return absolute_url[:end + len('http://')]
        else:
            return None

    def urls(self, html, current_url):
        current_domain = self.domain_name(current_url)
        if current_domain is None:
            raise Exception('RelativeURLFinder.urls: current_domain is None')
        dirty_urls = self.find_urls(html)
        abs_urls = []
        for url in dirty_urls:
            if len(url) > 7 and ('https://' in url or 'http://' in url):
                abs_urls.append(url)
            elif len(url) > 0 and url[0] == '/':
                abs_urls.append(current_domain + url)
        return list(set(abs_urls))
