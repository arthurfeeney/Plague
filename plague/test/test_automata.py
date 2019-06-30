import sys
sys.path.append('../')

import pytest
from automata import URLFinder, RelativeURLFinder


def test_next_char():
    a = URLFinder()
    assert a.next_char('a  b', 0) == 3

    assert a.next_char('  a a', 0) == 2
    assert a.next_char('  a a', 2) == 2

    assert a.next_char(' ab  a', 0) == 1
    assert a.next_char(' ab  a', 1) == 1
    assert a.next_char(' ab  a', 2) == 3

    assert a.next_char('a \t\r\nb', 0) == 5

    assert a.next_char('<a href="link"> </a>', 0) == 1
    assert a.next_char('<a href="link"> </a>', 1) == 2
    assert a.next_char('<a href="link"> </a>', 5) == 1
    assert a.next_char('<a href="link"> </a>', 14) == 2


def test_find_href():
    a = URLFinder()
    assert a.find_href('<a poop href yolo', 0) == 8
    assert a.find_href('<a poop href yolo', 4) == 8
    assert a.find_href('<a poop href yolo', 8) == 8
    assert a.find_href('<a poop href href', 9) == 13
    assert a.find_href('<a poop hr ef href', 0) == 14
    assert a.find_href('<a poop hr ef h ref', 0) == -1
    assert a.find_href('href hey', 0) == 0
    assert a.find_href('href="hi"', 0) == 0


def test_find_quote():
    a = URLFinder()
    assert a.find_quote('hi" there', 0) == 2
    assert a.find_quote('hi" there', 4) == -1
    assert a.find_quote('hi\' there', 0) == 2
    assert a.find_quote('" yo', 0) == 0
    assert a.find_quote('" yo', 1) == -1
    assert a.find_quote('poop "', 1) == 5
    assert a.find_quote('"', 0) == 0
    assert a.find_quote('"', 1) == -1
    assert a.find_quote('"', 10) == -1


def test_find_url():
    a = URLFinder()
    assert a.find_url('href="hi"', 0) == (6, 7)
    assert 'href="hi"' [6:8] == 'hi'
    assert a.find_url('yolo boy href="hi"', 0) == (15, 16)
    #assert a.find_url('href', 0)
    assert a.find_url('href="ab" href="b"', 0) == (6, 7)
    assert a.find_url('href="ab" href="b"', 9) == (16, 16)
    assert 'href="ab" href="b"' [15 + 1:17] == 'b'
    # lots of malformed things
    assert a.find_url('href="abcd>"', 0) == (-1, -1)
    assert a.find_url('="abcd>"', 0) == (-1, -1)
    assert a.find_url('="abcd', 0) == (-1, -1)
    assert a.find_url('href="abcd', 0) == (-1, -1)
    assert a.find_url('href=abcd">', 0) == (-1, -1)
    assert a.find_url('href=abcd"', 0) == (-1, -1)


def test_automata():
    a = URLFinder()
    assert a.find_urls('') == []
    assert a.find_urls('<a href="yolo"> </a>') == ['yolo']
    assert a.find_urls('<a href="yolo"> </a>'
                       '<a href="swag"> </a>') == ['yolo', 'swag']

    assert a.find_urls('<a href="yolo"> </a>'
                       '<a href="swag"> </a> sfasdf'
                       'the time? <a qwop href="ninja"'
                       'it is 11>') == ['yolo', 'swag', 'ninja']

    assert a.find_urls("<a href='yolo'> </a>"
                       "<a href='swag'> </a> sfasdf"
                       "the time? <a qwop href='ninja'"
                       "it is 11>") == ['yolo', 'swag', 'ninja']
