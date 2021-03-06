#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import OrderedDict

from slpp import slpp as lua

"""
Tests for slpp
"""


def is_iterator(obj):
    """
    >>> assert is_iterator(list()) is True
    >>> assert is_iterator(int) is False
    """
    if isinstance(obj, (list, tuple)):
        return True
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def differ(value, origin):
    """
    Same:
    >>> differ(1, 1)
    >>> differ([2, 3], [2, 3])
    >>> differ({'1': 3, '4': '6'}, {'4': '6', '1': 3})
    >>> differ('4', '4')

    Different:
    >>> differ(1, 2)
    Traceback (most recent call last):
       ...
    AssertionError: 1 not match original: 2.
    >>> differ([2, 3], [3, 2])
    Traceback (most recent call last):
       ...
    AssertionError: 2 not match original: 3.
    >>> differ({'6': 4, '3': '1'}, {'4': '6', '1': 3})
    Traceback (most recent call last):
       ...
    AssertionError: {'3': '1', '6': 4} not match original: {'1': 3, '4': '6'};
    Key: 1, item: 3
    >>> differ('4', 'no')
    Traceback (most recent call last):
       ...
    AssertionError: 4 not match original: no.
    """

    if type(value) not in (type(origin), OrderedDict):
        raise AssertionError('Types does not match: {0}, {1}'.format(type(value), type(origin)))

    if isinstance(origin, dict):
        for key, item in origin.items():
            try:
                differ(value[key], item)
            except KeyError:
                raise AssertionError('''{0} not match original: {1};
Key: {2}, item: {3}'''.format(value, origin, key, item))
        return

    if isinstance(origin, basestring):
        assert value == origin, '{0} not match original: {1}.'.format(value, origin)
        return

    if is_iterator(origin):
        for i in range(0, len(origin)):
            try:
                differ(value[i], origin[i])
            except IndexError:
                raise AssertionError(
                    '{0} not match original: {1}. Item {2} not found'.format(
                        response, origin, origin[i]))
            except Exception, e:
                raise e
        return

    assert value == origin, '{0} not match original: {1}.'.format(value, origin)




def number_test():
    """
    Integer and float:
    >>> assert lua.decode('3') == 3
    >>> assert lua.decode('4.1') == 4.1

    Negative float:
    >>> assert lua.decode('-0.45') == -0.45

    Scientific:
    >>> assert lua.decode('3e-7') == 3e-7
    >>> assert lua.decode('-3.23e+17') == -3.23e+17

    Hex:
    >>> assert lua.decode('0x3a') == 0x3a

    #4
    >>> differ(lua.decode('''{      \
        ID = 0x74fa4cae,            \
        Version = 0x07c2,           \
        Manufacturer = 0x21544948    \
    }'''), {                        \
        'ID': 0x74fa4cae,           \
        'Version': 0x07c2,          \
        'Manufacturer': 0x21544948  \
    })
    """
    pass


def test_bool():
    """
    >>> assert lua.decode('false') == False
    >>> assert lua.decode('true') == True

    >>> assert lua.encode(False) == 'false'
    >>> assert lua.encode(True) == 'true'
    """
    pass


def test_nil():
    """
    >>> assert lua.decode('nil') == None
    >>> assert lua.encode(None) == 'nil'
    """
    pass


def table_test():
    """
    Bracketed string key:
    >>> assert lua.decode('{[10] = 1}') == {10: 1}

    Void table:
    >>> assert lua.decode('{nil}') == []

    Values-only table:
    >>> assert lua.decode('{"10"}') == ["10"]

    Last zero
    >>> assert lua.decode('{0, 1, 0}') == [0,1,0]
    """
    pass

def string_test():
    r"""
    Escape test:
    >>> assert lua.decode(r"'test\'s string'") == "test's string"

    Add escaping on encode:
    >>> assert lua.encode({'a': 'func("call()");'}) == '{\n\ta = "func(\\"call()\\");"\n}'
    """
    pass

def basic_test():
    """
    No data loss:

    >>> data = '{ array = { 65, 23, 5 }, dict = { string = "value", array = { 3, 6, 4}, mixed = { 43, 54.3, false, string = "value", 9 } } }'
    >>> d = lua.decode(data)
    >>> differ(d, lua.decode(lua.encode(d)))
    """
    pass


def unicode_test():
    ur"""
    >>> assert lua.encode(u'Привет') == '"\xd0\x9f\xd1\x80\xd0\xb8\xd0\xb2\xd0\xb5\xd1\x82"'
    >>> assert lua.encode({'s': u'Привет'}) == '{\n\ts = "Привет"\n}'
    """
    pass


def orderered_test():
    r"""
    >>> data = '{ array = { 65, 23, 5 }, dict = { string = "value", array = { 3, 6, 4}, mixed = { 43, 54.3, false, string = "value", 9 }} ["foo-bar"] = 1 }'
    >>> result = lua.decode(data, use_ordered=True)
    >>> assert [key for key in result] == ['array', 'dict', 'foo-bar']
    >>> assert isinstance(result, OrderedDict)
    """

def test_brackets_enforced():
    r"""
    >>> data = '{["foo%"] = 1, ["Bar"] = 2}'
    >>> result = lua.encode(lua.decode(data))
    >>> assert '["foo%"]' in result
    >>> assert 'Bar' in result
    >>> assert '["Bar"]' not in result
    """

if __name__ == '__main__':
    import doctest
    doctest.testmod()
