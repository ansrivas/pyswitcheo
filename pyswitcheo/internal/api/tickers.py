# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""The tickers section consists of endpoints that allow retrieval of market data on Switcheo Exchange.
Authentication is not required for these endpoints.
"""
import logging
import requests
from pyswitcheo import utils
from pyswitcheo.internal.urls import tickers

logger = logging.getLogger(__name__)


def _get_candle_sticks(base_url, pair, start_time, end_time, interval):
    """Get candlestick chart data filtered by url parameters.

    Args:
        base_url (str)     : This paramter governs whether to connect to test or mainnet.
        pair (str)	       : Show chart data of this trading pair
        start_time (int)   : Start of time range for data in epoch seconds
        end_time (int)	   : End of time range for data in epoch seconds
        interval (int)	   : Candlestick period in minutes Possible values are: 1, 5, 30, 60, 360, 1440


    Returns:
        If response from the server is HTTP_OK (200) then this returns the requests.response object

        Example response:
        [
          {
            "time": "1531215240",
            "open": "0.00049408",
            "close": "0.00049238",
            "high": "0.000497",
            "low": "0.00048919",
            "volume": "110169445.0",
            "quote_volume": "222900002152.0"
          },
          {
            "time": "1531219800",
            "open": "0.00050366",
            "close": "0.00049408",
            "high": "0.00050366",
            "low": "0.00049408",
            "volume": "102398958.0",
            "quote_volume": "205800003323.0"
          },
          ...
        ]
    """
    url = utils.format_urls(base_url, tickers.CANDLE_STICKS)
    params = {
        "pair": pair,
        "start_time": start_time,
        "end_time": end_time,
        "interval": interval,
    }
    resp = requests.get(url, params=params)
    return utils.response_else_exception(resp)


def __get_prices(url, symbols=None, bases=None):
    """."""
    params = {}
    if symbols:
        params["symbols"] = symbols

    if bases:
        params["bases"] = bases

    logger.debug("Sending params in this request {params}".format(params=params))
    resp = requests.get(url, params=params)
    return utils.response_else_exception(resp)


def _get_last_twenty_four_hours(base_url):
    """Get 24-hour data for all pairs and markets.

    Args:
        base_url (str)  : This paramter governs whether to connect to test or mainnet.
    Returns:
        If response from the server is HTTP_OK (200) then this returns the requests.response object

    """
    url = utils.format_urls(base_url, tickers.LAST_TWENTY_FOUR_HOURS)
    return __get_prices(url)


def _get_last_price(base_url, symbols=None):
    """Get last price of given symbol(s). Defaults to all symbols.

    Args:
        base_url (str)       : This paramter governs whether to connect to test or mainnet..
        symbols (list[str])  : Return the price for these symbols for eg. ["SWTH"]

    Returns:
        If response from the server is HTTP_OK (200) then this returns the requests.response object

    """
    url = utils.format_urls(base_url, tickers.LAST_PRICE)
    return __get_prices(url, symbols)
