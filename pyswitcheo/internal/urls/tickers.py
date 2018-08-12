# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""The tickers section consists of endpoints that allow retrieval of market data on Switcheo Exchange.
Authentication is not required for these endpoints.
"""

# Returns candlestick chart data filtered by url parameters.
CANDLE_STICKS = "/tickers/candlesticks"

# Returns 24-hour data for all pairs and markets.
LAST_TWENTY_FOUR_HOURS = "/tickers/last_24_hours"

# Returns last price of given symbol(s). Defaults to all symbols.
LAST_PRICE = "/tickers/last_price"
