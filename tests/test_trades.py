# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests related to trades end points"""

import pytest
from http import HTTPStatus
from jsonschema import validate
from pyswitcheo.internal.api import trades
from pyswitcheo.utils import response_to_json
from pyswitcheo.schemas import LIST_TRADES_SCHEMA


@pytest.mark.parametrize("pair, contract_hash, error_msg", [
    ("SWTH_NEO", "a195c1549e7da61b8da315765a790ac7e7633b82", "list_trades with base NEO should not fail."),
    ("SWTH_NEO", "unknown_contract_hash", "list_trades with unknown_contract hash should return empty list."),
])
def test_list_trades(pair, contract_hash, error_msg, url):
    """Get list of trades."""

    # This is another format to query
    # response = trades._list_trades(base_url=url.testnet, contract_hash=contract_hash, pair=pair,
    #                                from_time=1531387142, to_time=1531387439, limit=2)
    response = trades._list_trades(base_url=url.testnet, contract_hash=contract_hash, pair=pair, limit=2)
    json_response = response_to_json(response)
    if contract_hash == "unknown_contract_hash":
        assert len(json_response) == 0
    else:
        # If there is data, it should match the schema
        assert validate(json_response, LIST_TRADES_SCHEMA) is None, "Failed to validate response from List offers"
        # If there is data, since we used limit, there should be only two entries
        assert len(json_response) == 2
    assert response.status_code == HTTPStatus.OK, error_msg
