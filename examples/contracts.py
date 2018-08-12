# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Get available contracts on Switcheo Dex."""

import json
from http import HTTPStatus
from pyswitcheo.api import SwitcheoApi

if __name__ == '__main__':
    client = SwitcheoApi(base_url="https://test-api.switcheo.network")

    resp = client.list_contracts()
    if resp.status_code == HTTPStatus.OK:
        print(json.loads(resp.text.encode("UTF-8")))
