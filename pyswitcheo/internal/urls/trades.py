# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""A trade represents a fill of an offer.
This happens when an incoming order matches an offer on the opposite side of the order book in price.
Trades can be seen on the Trade History column on Switcheo Exchange.
"""

# Retrieves trades that have already occurred on Switcheo Exchange filtered by the request parameters.
LIST_TRADES = "/trades"
