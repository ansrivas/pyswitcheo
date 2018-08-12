# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Contracts deployed by Switcheo."""

import logging
import requests
from pyswitcheo import utils
from pyswitcheo.internal.urls import contracts

logger = logging.getLogger(__name__)


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
    url = utils.format_urls(base_url, contracts.LIST_CONTRACTS)
    resp = requests.get(url)
    return utils.response_else_exception(resp)
