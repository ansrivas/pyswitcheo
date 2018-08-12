# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""An offer represents an open order that rests on the Switcheo Exchange offer book.
Funds used to make an offer will be placed on hold unless the order is cancelled or filled
"""
import requests
from pyswitcheo import utils
from pyswitcheo.internal.urls.offers import LIST_OFFERS


def _list_offers(base_url, blockchain, pair, contract_hash):
    """Retrieves the best 70 offers (per side) on the offer book.

    Args:
        base_url (str): This paramter governs whether to connect to test or mainnet..
        blockchain (str)   : Only return offers from this blockchain. Possible values are neo.
        pair (str)         : Only return offers from this pair, for eg. SWTH_NEO
        contract_hash (str): Only return offers for the contract hash. e.g. eed0d2e14b0027f5f30ade45f2b23dc57dd54ad2

    Returns:
        If response from the server is HTTP_OK (200) then this returns the requests.response object

        Example response:
        [
            {
             "id": "b3a91e19-3726-4d09-8488-7c22eca76fc0",
             "offer_asset": "SWTH",
             "want_asset": "NEO",
             "available_amount": 2550000013,
             "offer_amount": 4000000000,
             "want_amount": 320000000
            }
        ]
    """
    params = {"blockchain": blockchain, "pair": pair, "contract_hash": contract_hash}
    url = utils.format_urls(base_url, LIST_OFFERS)
    resp = requests.get(url, params=params)
    return utils.response_else_exception(resp)
