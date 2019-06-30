import pytest
import plague.url_util as uu


def test_domain_name():
    assert uu.domain_name('https://youtube.com') == 'https://youtube.com'
    assert (
        uu.domain_name('http://x.y.z.com/hithere/yolo') == 'http://x.y.z.com')
    assert (uu.domain_name('htt://yolo.com') == None)
    assert uu.domain_name('https://') == 'https://'


def test_remove_protocol():
    assert uu.remove_protocol('https://youtube.com') == 'youtube.com'
    assert uu.remove_protocol('http://youtube.com') == 'youtube.com'
    assert uu.remove_protocol('http://') == ''
    assert uu.remove_protocol('https://') == ''
