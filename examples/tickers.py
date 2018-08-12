# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""Ticker related information from Switcheo Dex."""

import json
from http import HTTPStatus
from pyswitcheo.api import SwitcheoApi

if __name__ == '__main__':
    client = SwitcheoApi(base_url="https://test-api.switcheo.network")
    resp = client.get_candle_sticks(pair="SWTH_NEO", start_time=1433736037,
                                    end_time=1533736037,
                                    interval=1440)
    if resp.status_code == HTTPStatus.OK:
        print(json.loads(resp.text.encode("UTF-8")))
