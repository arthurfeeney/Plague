#
# Utility functions for parsing URLSs and such.
#


def domain_name(absolute_url):
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
