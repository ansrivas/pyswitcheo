# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""This section consists of endpoints that allow retrieval of Switcheo Exchange information.
Authentication is not required for these endpoints.
"""

# Returns the current timestamp in the exchange, this value should be
# fetched and used when a timestamp parameter is required for API requests.
GET_TIMESTAMP = "/exchange/timestamp"

# Returns updated hashes of contracts deployed by Switcheo.
LIST_CONTRACTS = "/exchange/contracts"

# Returns updated hashes of contracts deployed by Switcheo.
GET_TOKENS = "/exchange/tokens"

# Retrieve available currency pairs on Switcheo Exchange filtered by the base parameter.
# Defaults to all pairs. The valid base currencies are currently: NEO, GAS, SWTH.
LIST_CURRENCY_PAIRS = "/exchange/pairs"
