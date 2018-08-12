# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Get balances from Switcheo Dex."""

import json
from http import HTTPStatus
from pyswitcheo.api import SwitcheoApi

if __name__ == '__main__':
    client = SwitcheoApi(base_url="https://test-api.switcheo.network")

    pubkey = "ANVLCD3xqGXKhDnrivpVFvDLcvkpgPbbMt"
    contract_hash = ["a195c1549e7da61b8da315765a790ac7e7633b82"]

    resp = client.list_balances(addresses=pubkey, contract_hashes=contract_hash)
    if resp.status_code == HTTPStatus.OK:
        print(json.loads(resp.text.encode("UTF-8")))
