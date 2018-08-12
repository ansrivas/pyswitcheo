# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests related to tickers end points"""

import pytest
from http import HTTPStatus
from pyswitcheo.internal.api import tickers
from pyswitcheo.utils import response_to_json


def test_get_candle_sticks(url):
    """Get candle sticks test."""
    # expected = json.loads('[{"time":"1531214820","open":"0.00045893","close":"0.00049953","high":"0.00049953",'
    #                       '"low":"0.00045893","volume":"68597677.0","quote_volume":"142900000330.0"},'
    #                       '{"time":"1531214880","open":"0.00045893","close":"0.00050373","high":"0.00050373",'
    #                       '"low":"0.00045893","volume":"71485077.0","quote_volume":"148600000330.0"}]')

    # contract_hash = "a195c1549e7da61b8da315765a790ac7e7633b82"

    response = tickers._get_candle_sticks(pair="SWTH_NEO", start_time=1532390400, end_time=1532736000, interval=1440,
                                          base_url=url.testnet)

    # Just sorting the incoming json based on `time` key to make sure the ordering inside json is maintained

    # def sorted_with_time(x):
    #     return x.get('time', 0)
    # assert sorted(expected, key=sorted_with_time) == sorted(response_to_json(response), key=sorted_with_time)
    json_response_list = response_to_json(response)
    assert len(json_response_list[0].keys()) > 0
    assert response.status_code == HTTPStatus.OK


def test_get_last_twenty_four_hours(url):
    """Get last twenty four hours of data."""

    response = tickers._get_last_twenty_four_hours(base_url=url.testnet)
    assert response.status_code == HTTPStatus.OK


# FIXME: (ansrivas) Symbols not working in getlastprice
@pytest.mark.parametrize("symbols, key, error_msg", [
    # (["SWTH"], "SWTH", "Testing last price with one symbol should not fail."),
    # (["NEO"], "NEO", "Testing last price with symbol NEO should not fail."),
    (None, "", "Testing last price with no symbols should return all the pairs."),
])
def test_get_last_price(symbols, key, error_msg, url):
    """Get last price for the resources."""

    response = tickers._get_last_price(url.testnet, symbols=symbols)
    assert response.status_code == HTTPStatus.OK, error_msg

    response_json = response_to_json(response)
    if symbols is None:
        assert len(response_json.keys()) > 0
    else:
        assert key in response_json.keys()
