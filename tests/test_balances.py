# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests related to balances end points"""

from http import HTTPStatus
from pyswitcheo.internal.api import balances
from pyswitcheo.utils import response_to_json


def test_list_balances(url):
    """Test end points related to balances."""

    contract_hashes_list = ["a195c1549e7da61b8da315765a790ac7e7633b82"]
    addresses_list = ["ANVLCD3xqGXKhDnrivpVFvDLcvkpgPbbMt"]
    response = balances._list_balances(base_url=url.testnet,
                                       addresses=addresses_list,
                                       contract_hashes=contract_hashes_list)

    json_response = response_to_json(response)
    assert response.status_code == HTTPStatus.OK
    assert sorted(['confirmed', 'confirming', 'locked']) == sorted(list(json_response.keys()))
