# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""A trade represents a fill of an offer.
This happens when an incoming order matches an offer on the opposite side of the order book in price.
Trades can be seen on the Trade History column on Switcheo Exchange.
"""
import logging
import requests
from pyswitcheo import utils
from pyswitcheo.internal.urls import trades

logger = logging.getLogger(__name__)


def _list_trades(
    base_url, contract_hash, pair, from_time=None, to_time=None, limit=None
):
    """Retrieve trades that have already occurred on Switcheo Exchange filtered by the request parameters.

    Args:
        base_url (str): This paramter governs whether to connect to test or mainnet.
        contract_hash (str) : Only return trades for this contract hash.
        pair (str)          : Only return trades for this pair.
        from_time (int)     : Only return trades after this time in epoch seconds.
        to_time (int)       : Only return trades before this time in epoch seconds.
        limit (int)         : Only return this number of trades (min: 1, max: 10000, default: 5000).

    Returns:
        If response from the server is HTTP_OK (200) then this returns the requests.response object

        Example response:
        [
          {
            "id": "712a5019-3a23-463e-b0e1-80e9f0ad4f91",
            "fill_amount": 9122032316,
            "take_amount": 20921746,
            "event_time": "2018-06-08T11:32:03.219Z",
            "is_buy": false
          },
          {
            "id": "5d7e42a2-a8f3-40a9-bce5-7304921ff691",
            "fill_amount": 280477933,
            "take_amount": 4207169,
            "event_time": "2018-06-08T11:31:42.200Z",
            "is_buy": false
          },
          ...
        ]
    """
    url = utils.format_urls(base_url, trades.LIST_TRADES)
    params = {
        "contract_hash": contract_hash,
        "pair": pair,
        "from": from_time,
        "to": to_time,
        "limit": limit,
    }
    resp = requests.get(url, params=params)
    return utils.response_else_exception(resp)
