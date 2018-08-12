# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""List contract balances of the given address and contract.
The purpose of this endpoint is to allow convenient querying of a user's balance across multiple blockchains,
for example, if you want to retrieve a user's NEO and ethereum balances.
As such, when using this endpoint, balances for the specified addresses and contract hashes will be merged and summed.
"""
import requests
from pyswitcheo import utils
from pyswitcheo.internal.urls.balances import LIST_BALANCES
from pyswitcheo.crypto_utils import get_script_hash_from_address


def _list_balances(base_url, addresses, contract_hashes):
    """List contract balances of the given address and contract hashes.

    NOTE: The address gets converted to scripthash internally
    Args:
        base_url (str)               : This paramter governs whether to connect to test or mainnet..
        addresses (list[str])        : Only return balances for these addresses.
        contract_hashes (list[str])  : Only return balances from these contract hashes.

    Returns:
        If response from the server is HTTP_OK (200) then this returns the requests.response object

        Example response:
        {
          "confirming": {
            "GAS": [
              {
                "event_type": "withdrawal",
                "asset_id": "602c79718b16e442de58778de6b7b16cee7969282de7",
                "amount": -100000000,
                "transaction_hash": null,
                "created_at": "2018-07-12T10:48:48.866Z"
              }
            ]
          },
          "confirmed": {
            "GAS": "47320000000.0",
            "SWTH": "421549852102.0",
            "NEO": "50269113921.0"
          },
          "locked": {
            "GAS": "500000000.0",
            "NEO": "1564605000.0"
          }
        }
    """
    addresses = [get_script_hash_from_address(address) for address in addresses]
    params = {"addresses": addresses, "contract_hashes": contract_hashes}
    url = utils.format_urls(base_url, LIST_BALANCES)
    resp = requests.get(url, params=params)
    return utils.response_else_exception(resp)
