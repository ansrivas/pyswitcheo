# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests related to datatypes Fixed8 module."""

import pytest
from pyswitcheo.datatypes.fixed8 import Fixed8


@pytest.mark.parametrize("num, want", [
    (30, '005ed0b200000000'),
    (100, '00e40b5402000000'),
    (2, '00c2eb0b00000000'),
    (4000000, '0000e941cc6b0100'),
])
def test_Fixed8_num_to_fixed_8(num, want):
    """Tests for num_to_fixed_8."""
    got = Fixed8.num_to_fixed_8(num, size=8)
    assert want == got, "Expected {0} but received {1} for input {2}".format(want, got, num)
