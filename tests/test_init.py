# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test modules."""


def test_init(hello_world):
    """Run a test."""
    import pyswitcheo

    # Test __init__
    assert hasattr(pyswitcheo, '__version__')

    # Test pytest fixtures
    assert(hello_world == "Hello World!")
