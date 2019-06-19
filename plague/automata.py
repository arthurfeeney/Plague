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
        # looks for 'href' in the html stirng. For the first found
        # occurence, it returns the index of the h.
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

    def find_url(self, html, front):
        # return the start and end index of url.
        h_index = self.find_href(html, front)
        # no href was found
        if h_index == -1:
            return -1, -1

        start = h_index + html[h_index:].find('"')

        # find failed to find anything, so it returns - 1
        if start == h_index - 1:
            return -1, -1

        end = start + 1
        while end < len(html) and html[end] != '"':
            end += 1

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

    def urls(self, html):
        # abstract function implemented in derived class.
        raise NotImplementedError('URLFinder.find_urls not implemented.')


#
# Derived class that only finds Absolute urls.
#
class AbsoluteURLFinder(URLFinder):
    def __init__(self):
        super(AbsoluteURLFinder, self).__init__()

    def unique_absolute(self, urls):
        absolute = ([
            url for url in urls if 'https://' in url or 'http://' in url
        ])
        return list(set(absolute))

    def urls(self, html):
        return self.unique_absolute(self.find_urls(html))
