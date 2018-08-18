# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""This section consists of endpoints that allow retrieval of Switcheo Exchange information.
Authentication is not required for these endpoints.
"""

import logging
import requests
from pyswitcheo import utils
from pyswitcheo.internal.urls import exchange

logger = logging.getLogger(__name__)


def _list_currency_pairs(base_url, bases=None):
    """Fetch available currency pairs on Switcheo Exchange filtered by the base parameter. Defaults to all pairs.

    Args:
        base_url (str)    : This paramter governs whether to connect to test or mainnet..
        bases (list[str]) : Provides pairs for these base symbols. Possible values are NEO, GAS, SWTH, USD.

    Returns:
        If response from the server is HTTP_OK (200) then this returns the requests.response object

        Example response
        [
          "GAS_NEO",
          "SWTH_NEO"
        ]
    """
    params = {}
    if bases:
        params["bases"] = bases

    url = utils.format_urls(base_url, exchange.LIST_CURRENCY_PAIRS)
    resp = requests.get(url, params=params)
    return utils.response_else_exception(resp)


def _get_exchange_timestamp(base_url):
    """Returns the current timestamp in the exchange.

    This value should be fetched and used when a timestamp parameter is required for API requests.
    If the timestamp used for your API request is not within an acceptable range of the exchange's
    timestamp then an invalid signature error will be returned. The acceptable range might vary, but it
    should be less than one minute.

    Returns:
        If response from the server is HTTP_OK (200) then this returns the requests.response object

        Example response
        {
          "timestamp": 1534392760908
        }
    """
    url = utils.format_urls(base_url, exchange.GET_TIMESTAMP)
    resp = requests.get(url)
    return utils.response_else_exception(resp)


def _list_contracts(base_url):
    """Fetch updated hashes of contracts deployed by Switcheo.

    Args:
        base_url (str): This paramter governs whether to connect to test or mainnet.

    Returns:
        If response from the server is HTTP_OK (200) then this returns the requests.response object

        Example response
        {
          "NEO":
          {
            "V1": "0ec5712e0f7c63e4b0fea31029a28cea5e9d551f",
            "V1_5": "c41d8b0c30252ce7e8b6d95e9ce13fdd68d2a5a8",
            "V2": "48756743d524af03aa75729e911651ffd3cbe7d8"
          }
        }
    """
    url = utils.format_urls(base_url, exchange.LIST_CONTRACTS)
    resp = requests.get(url)
    return utils.response_else_exception(resp)


def _get_contract_tokens_info(base_url):
    """Fetch updated hashes of contracts deployed by Switcheo along with their precision.

    Args:
        base_url (str): This paramter governs whether to connect to test or mainnet.

    Returns:
        If response from the server is HTTP_OK (200) then this returns the requests.response object

        Example response
        {
          "NEO": {
            "hash": "c56f33fc6ecfcd0c225c4ab356fee59390af8560be0e930faebe74a6daff7c9b",
            "decimals": 8
          },
          "GAS": {
            "hash": "602c79718b16e442de58778e148d0b1084e3b2dffd5de6b7b16cee7969282de7",
            "decimals": 8
          },
          "SWTH": {
            "hash": "ab38352559b8b203bde5fddfa0b07d8b2525e132",
            "decimals": 8
          },
          ...
        }
    """
    url = utils.format_urls(base_url, exchange.GET_TOKENS)
    resp = requests.get(url)
    return utils.response_else_exception(resp)
