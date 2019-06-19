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
