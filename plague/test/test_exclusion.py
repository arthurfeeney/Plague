import exclusion as E
import certifi
import urllib3


def test_test_url():
    e = E.Exclusion()
    assert not e.test_url('https://google.com/search')
    #assert e.test_url('https://google.com/search/about')
    #assert e.test_url('https://google.com/out')
