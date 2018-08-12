# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Bunch of fixtures to be used across the tests."""

import pytest
from collections import namedtuple
from pyswitcheo.api import SwitcheoApi


@pytest.fixture(scope="function")
def hello_world(request):
    """Create a test fixture."""
    hw = "Hello World!"

    def tear_down():
        # clean up here
        pass

    request.addfinalizer(tear_down)
    return hw


@pytest.fixture(scope="session")
def url(request):
    """Returns base_url for testing."""
    URL = namedtuple('URL', ['mainnet', 'testnet'])

    # For actual trading and market data, the mainnet URL will be used:
    # When developing application, the testnet URL should be used:
    url = URL(mainnet="https://api.switcheo.network/v2/", testnet="https://test-api.switcheo.network/v2/")

    def tear_down():
        # clean up here
        pass

    request.addfinalizer(tear_down)
    return url


@pytest.fixture(scope="session")
def deposit_swth_before_withdrawal(request, url):
    """Deposits 10 swth in contract before testing withdrawal"""

    def tear_down():
        # clean up here
        pass

    request.addfinalizer(tear_down)

    # encrypted_key = b"6PYKozqwKwRYi77GN3AwTwXEssJZWbfneYKEYbiSeuNtVTGPFT2Q7EJpjY"
    # pub_key = "ANVLCD3xqGXKhDnrivpVFvDLcvkpgPbbMt"
    client = SwitcheoApi(base_url="https://test-api.switcheo.network")

    priv_key_wif = 'L4FSnRosoUv22cCu5z7VEEGd2uQWTK7Me83vZxgQQEsJZ2MReHbu'
    deposit_response = client.deposit(priv_key_wif=priv_key_wif, asset_id="SWTH", amount=50,
                                      contract_hash="a195c1549e7da61b8da315765a790ac7e7633b82",
                                      blockchain="neo")
    print(deposit_response.text)
