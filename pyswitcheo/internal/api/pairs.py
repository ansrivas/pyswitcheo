# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Currency pairs deployed on Switcheo."""

import logging
import requests
from pyswitcheo import utils
from pyswitcheo.internal.urls import pairs

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
    url = utils.format_urls(base_url, pairs.LIST_CURRENCY_PAIRS)
    if bases:
        params["bases"] = bases
    resp = requests.get(url, params=params)
    return utils.response_else_exception(resp)
