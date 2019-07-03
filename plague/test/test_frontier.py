import sys
sys.path.append('../')

from frontier import *


def test_fifo_frontier():
    f = FIFOFrontier()
    assert (f.view_frontier() == [])
    f.add('hi')
    f.add('yo')
    f.add('swag')
    assert not f.empty()
    assert (f.view_frontier() == ['hi', 'yo', 'swag'])
    assert (f.get() == 'hi')
    assert (f.view_frontier() == ['yo', 'swag'])
    assert (f.get() == 'yo')
    assert (f.view_frontier() == ['swag'])
    assert (f.get() == 'swag')
    assert (f.view_frontier() == [])
    assert f.empty()


def test_k_oldest():
    # test for DomainPriorityFrontier.__k_oldest
    f = MemoryDomainPriorityFrontier()

    urls = [
        'https://hi.com/two', 'http://there.com/xyz', 'https://ninja.com/abc'
    ]
    for url in urls:
        f.add(url)

    assert f.k_oldest(1) == ['https://hi.com']
    assert f.k_oldest(2) == ['https://hi.com', 'http://there.com']


def test_dp_frontier_limit():
    f = MemoryDomainPriorityFrontier(limit=2)
    urls = [
        'https://hi.com/two', 'http://there.com/xyz', 'https://ninja.com/abc'
    ]
    for url in urls:
        f.add(url)
    assert list(f.last_pulled.keys()) == ['https://ninja.com']
