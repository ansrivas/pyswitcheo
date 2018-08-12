# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""An offer represents an open order that rests on the Switcheo Exchange offer book.
Funds used to make an offer will be placed on hold unless the order is cancelled or filled.
"""

# Retrieves the best 70 offers (per side) on the offer book.
LIST_OFFERS = "/offers"
