# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests related to crypto utils module"""

import pytest
import pyswitcheo.crypto_utils as cutils


@pytest.mark.parametrize("input_hex, want", [
    ('0101', True),
    ('', True),
    ('0x01', False),
])
def test_is_regex(input_hex, want):
    """Check regex parsing."""
    got = cutils.is_hex(input_hex)
    assert want == got, "Expected {0} but received {1} for input {2}".format(want, got, input_hex)


@pytest.mark.parametrize("input_hex, raises_exception", [
    (b'0x11', True),
])
def test_ensure_hex(input_hex, raises_exception):
    """Check regex parsing."""
    with pytest.raises(Exception) as excinfo:
        cutils.ensure_hex(input_hex)
        assert 'Expected a hexstring' in str(excinfo)


@pytest.mark.parametrize("input_hex, want", [
    ('0101', '0101'),
    ('010111', '110101'),
    ('abcdef', 'efcdab'),
])
def test_reverse_hex(input_hex, want):
    """Check regex parsing."""
    got = cutils.reverse_hex(input_hex)
    assert want == got, "Expected {0} but received {1} for input {2}".format(want, got, input_hex)


def test_num_to_hex_string():
    """Check num_to_hex_string conversion."""
    data = [(30, "1e"), (100, "64"), (2, "02"), (1000, "e8")]
    for inp, want in data:
        got = cutils.num_to_hex_string(inp)
        assert want == got, "Expected {0} but received {1} for input {2}".format(want, got, inp)

    num = -1
    with pytest.raises(Exception) as excinfo:
        cutils.num_to_hex_string(num=num, size=1, little_endian=False)
    assert 'num should be unsigned' in str(excinfo.value)

    size = 0.5
    with pytest.raises(Exception) as excinfo:
        cutils.num_to_hex_string(num=1, size=size, little_endian=False)
    assert 'size must be a whole integer' in str(excinfo.value)


@pytest.mark.parametrize("input_hex, want", [
    (30, '1e'),
    (100, '64'),
    (2, '02'),
    (12, '0c'),
    (1000, 'fde803'),
    (0xff, 'fdff00'),
    (100000, 'fea08601'),
    (4000000, 'fe00093d'),
])
def test_num_to_var_int(input_hex, want):
    """Check regex parsing."""
    got = cutils.num_to_var_int(input_hex)
    assert want == got, "Expected {0} but received {1} for input {2}".format(want, got, input_hex)
