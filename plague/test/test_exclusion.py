import exclusion as E
import certifi
import urllib3


def test_test_url():
    e = E.Exclusion()
    assert not e.test_url('https://google.com/search')
    #assert e.test_url('https://google.com/search/about')
    #assert e.test_url('https://google.com/search/static')
    #assert e.test_url('https://google.com/maps/d/')
    #assert e.test_url('https://google.com/js/')
    assert not e.test_url('https://google.com/search/howsearchworks')
    assert not e.test_url('https://google.com/?hl=hi&')
    #assert e.test_url('https://google.com')
    assert e.test_url("http://www.musi-cal.com/")
    assert e.test_url('https://stackoverflow.com')
